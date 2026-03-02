# arkhe/orchestrator.py
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .providers import GeminiProvider, OllamaProvider, BaseLLMProvider
from .state_reconciler import StateReconciler, LLMState, ReconciliationStrategy
from .telemetry import TelemetryCollector
from .memory import CortexMemory

@dataclass
class ProcessingResult:
    document_id: str
    reconciled_state: Dict[str, Any]
    individual_states: List[LLMState]
    metrics: Dict[str, Any]

class DocumentProcessor:
    """
    Orquestrador principal do Arkhe(n) OS.
    Coordena paralelismo, reconciliação e telemetria.
    """

    def __init__(
        self,
        gemini_key: Optional[str] = None,
        ollama_url: str = "http://localhost:11434",
        reconciliation_strategy: ReconciliationStrategy = ReconciliationStrategy.SMART_MERGE,
        memory_path: str = "./arkhe_memory"
    ):
        self.telemetry = TelemetryCollector()
        self.reconciler = StateReconciler(strategy=reconciliation_strategy)
        self.memory = CortexMemory(path=memory_path)

        # Inicializar provedores
        self.providers: List[BaseLLMProvider] = []

        if gemini_key:
            self.providers.append(GeminiProvider(
                api_key=gemini_key,
                telemetry=self.telemetry,
                schema=self._get_output_schema()
            ))

        self.providers.append(OllamaProvider(
            base_url=ollama_url,
            telemetry=self.telemetry,
            schema=self._get_output_schema()
        ))

        # Fallback local if nothing else
        if not self.providers:
             self.providers.append(OllamaProvider(
                model="tinyllama",
                telemetry=self.telemetry
            ))

    def _get_output_schema(self) -> Dict[str, Any]:
        """Schema padrão para validação de outputs."""
        return {
            "type": "object",
            "properties": {
                "analysis": {"type": "string"},
                "confidence": {"type": "number"},
                "metadata": {"type": "object"}
            },
            "required": ["analysis"]
        }

    async def process_document(
        self,
        document: str,
        document_id: str,
        context: Optional[Dict] = None
    ) -> ProcessingResult:
        """
        Processa documento em paralelo através de múltiplos LLMs.
        """
        # Criar tarefas paralelas
        tasks = [
            self._call_provider(provider, document, context)
            for provider in self.providers
        ]

        # Executar com gather (paralelismo real)
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Converter para estados LLM
        states: List[LLMState] = []
        for i, result in enumerate(results):
            provider_name = self.providers[i].provider_type.value

            if isinstance(result, Exception):
                # Falha — criar estado de erro com baixa confiança
                states.append(LLMState(
                    provider=provider_name,
                    content={"error": str(result)},
                    context_hash="",
                    timestamp=asyncio.get_event_loop().time(),
                    confidence=0.0
                ))
            else:
                content = result.get("content")
                states.append(LLMState(
                    provider=provider_name,
                    content=content,
                    context_hash=self._hash_document(document),
                    timestamp=asyncio.get_event_loop().time(),
                    confidence=content.get("confidence", 0.5) if isinstance(content, dict) else 0.5
                ))

        # Reconciliar estados
        reconciled = await self.reconciler.reconcile(states, document_id)

        # Memorizar insights (Bloco 843)
        self._memorize_reconciled_state(reconciled, document_id)

        return ProcessingResult(
            document_id=document_id,
            reconciled_state=reconciled,
            individual_states=states,
            metrics=self.telemetry.get_stats()
        )

    async def _call_provider(
        self,
        provider: BaseLLMProvider,
        document: str,
        context: Optional[Dict]
    ) -> Dict[str, Any]:
        """Wrapper para chamada de provedor com contexto."""
        async with provider:
            enriched_prompt = self._enrich_prompt(document)
            return await provider.generate(enriched_prompt, context)

    def _enrich_prompt(self, document: str) -> str:
        """Adiciona instruções de formatação ao prompt."""
        return f"Analyze the following document and return JSON: {document}"

    def _hash_document(self, document: str) -> str:
        import hashlib
        return hashlib.sha256(document.encode()).hexdigest()[:16]

    def _memorize_reconciled_state(self, reconciled: Dict[str, Any], doc_id: str):
        """Persiste insights validados no Vector DB."""
        content = reconciled.get("content")
        if not isinstance(content, dict):
            return

        # No Arkhe, cada campo relevante do conteúdo pode ser um insight
        analysis = content.get("analysis", "")
        confidence = content.get("confidence", 0.5)

        # Filtro de Coerência (C > 0.8)
        if confidence > 0.8 and analysis:
            self.memory.memorize_insight(
                topic="document_analysis",
                summary=analysis,
                confidence=confidence,
                doc_id=doc_id,
                related_nodes=content.get("metadata", {}).get("related_nodes", [])
            )
