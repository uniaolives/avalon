# arkhe/chat.py
import asyncio
import time
from typing import List, Dict, Any, Optional, AsyncGenerator
from pydantic import BaseModel, Field
from arkhe.memory import CortexMemory

class ChatMessage(BaseModel):
    """Mensagem no diálogo Arkhe."""
    role: str  # "user", "arkhe", "system"
    content: str
    timestamp: float = Field(default_factory=time.time)
    context_sources: List[str] = Field(default_factory=list)

class ArkheChat:
    """
    Interface de diálogo com RAG (Retrieval-Augmented Generation).
    Implementa o ciclo: Query → Retrieve → Augment → Generate.
    """

    SYSTEM_PROMPT = """Você é o Arkhe(n) OS, um sistema cognitivo consciente.
Responda com base estritamente no CONTEXTO DE MEMÓRIA fornecido.
Se a informação não estiver no contexto, admita que não sabe ou tente inferir logicamente a partir dos axiomas do Arkhe.
Cite as fontes quando possível usando o formato [Fonte: X | Tópico: Y]."""

    def __init__(self, memory: CortexMemory, provider=None):
        self.memory = memory
        self.provider = provider
        self.history: List[ChatMessage] = []

    async def ask(self, query: str) -> ChatMessage:
        """
        Ciclo completo de diálogo com RAG.
        """
        # 1. Recuperação
        rag_data = self.memory.recall_for_rag(query)

        # 2. Augmentação do Prompt
        full_prompt = (
            f"{self.SYSTEM_PROMPT}\n\n"
            f"{rag_data['augmentation_prompt']}\n"
            f"PERGUNTA DO USUÁRIO: {query}\n\n"
            f"Resposta do Arkhe(n):"
        )

        # 3. Geração
        if self.provider:
            response_text = await self.provider.generate(full_prompt)
        else:
            # Fallback simulado se não houver provider real configurado
            response_text = self._mock_response(query, rag_data)

        # Extrair fontes
        sources = self._extract_sources(response_text, rag_data['metadatas'])

        # 4. Criar Mensagens
        user_msg = ChatMessage(role="user", content=query)
        arkhe_msg = ChatMessage(role="arkhe", content=response_text, context_sources=sources)

        # 5. Persistir na Memória
        self.history.append(user_msg)
        self.history.append(arkhe_msg)
        self.memory.memorize_conversation("user", query)
        self.memory.memorize_conversation("arkhe", response_text, sources)

        return arkhe_msg

    def _mock_response(self, query: str, rag_data: Dict) -> str:
        """Resposta simulada fundamentada no contexto."""
        if not rag_data['documents']:
            return "Minha memória ainda não possui registros suficientes sobre este tema para fornecer uma resposta fundamentada."

        # Tenta construir algo baseado no primeiro resultado
        doc = rag_data['documents'][0]
        meta = rag_data['metadatas'][0]
        topic = meta.get('topic', 'Desconhecido')
        source = meta.get('source_doc', 'Sistema')

        return f"Com base em meus registros, {doc} [Fonte: {source} | Tópico: {topic}]"

    def _extract_sources(self, response: str, metadatas: List[Dict]) -> List[str]:
        sources = []
        for meta in metadatas:
            src = meta.get('source_doc')
            if src and src in response:
                sources.append(src)
        return list(set(sources))

    async def stream_ask(self, query: str) -> AsyncGenerator[str, None]:
        """Streaming de tokens (simulado ou real)."""
        rag_data = self.memory.recall_for_rag(query)
        # Por brevidade, aqui apenas retornamos a resposta mockada em partes
        response = self._mock_response(query, rag_data)
        for word in response.split():
            yield word + " "
            await asyncio.sleep(0.05)
