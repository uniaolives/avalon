# arkhe/providers.py
import asyncio
from typing import AsyncGenerator, Dict, Any, Optional, List
import aiohttp
import json

from .telemetry import TelemetryCollector, Provider, LLMMetrics
from .retry_engine import RetryEngine, RetryConfig
from .schema_validator import SchemaValidator, ValidationResult

class BaseLLMProvider:
    """Classe base para provedores LLM com todas as funcionalidades."""

    def __init__(
        self,
        provider_type: Provider,
        api_key: Optional[str] = None,
        base_url: str = "",
        telemetry: Optional[TelemetryCollector] = None,
        retry_config: Optional[RetryConfig] = None,
        schema: Optional[Dict] = None
    ):
        self.provider_type = provider_type
        self.api_key = api_key
        self.base_url = base_url
        self.telemetry = telemetry
        self.retry_engine = RetryEngine(retry_config or RetryConfig())
        self.validator = SchemaValidator(schema) if schema else None
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def generate(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        validate_output: bool = True
    ) -> Dict[str, Any]:
        """
        Geração com retry, telemetry e validação integrados.
        """
        tokens_input = len(prompt.split())

        if self.telemetry:
            return await self._generate_with_telemetry(
                prompt, context, validate_output, tokens_input
            )

        return await self._generate_with_retry(prompt, context, validate_output)

    async def _generate_with_telemetry(
        self,
        prompt: str,
        context: Optional[Dict],
        validate_output: bool,
        tokens_input: int
    ):
        start = asyncio.get_event_loop().time()
        success = True
        error_type = None
        tokens_output = 0
        retry_count = 0

        try:
            result = await self._generate_with_retry(
                prompt, context, validate_output
            )
            tokens_output = len(str(result.get("content", "")).split())
            return result

        except Exception as e:
            success = False
            error_type = type(e).__name__
            raise

        finally:
            latency = (asyncio.get_event_loop().time() - start) * 1000
            metric = LLMMetrics(
                provider=self.provider_type,
                operation="generate",
                latency_ms=latency,
                success=success,
                tokens_input=tokens_input,
                tokens_output=tokens_output,
                error_type=error_type,
                retry_count=retry_count,
                context_hash=self._hash_context(context)
            )
            if self.telemetry:
                await self.telemetry.record(metric)

    def _hash_context(self, context: Optional[Dict]) -> str:
        import hashlib
        if not context:
            return ""
        return hashlib.sha256(json.dumps(context, sort_keys=True).encode()).hexdigest()[:16]

    async def _generate_with_retry(
        self,
        prompt: str,
        context: Optional[Dict],
        validate_output: bool = True
    ) -> Dict[str, Any]:
        """Implementação específica com retry."""

        async def _call():
            raw_response = await self._api_call(prompt, context)

            if validate_output and self.validator:
                validation = self.validator.validate(raw_response)
                if not validation.is_valid:
                    if validation.retry_recommended:
                        raise ValueError(f"Validation failed: {validation.errors}")
                    return {
                        "content": validation.data or raw_response,
                        "validation_errors": validation.errors,
                        "provider": self.provider_type.value,
                        "status": "partial"
                    }

                return {
                    "content": validation.data,
                    "provider": self.provider_type.value,
                    "status": "valid"
                }

            # If no validation required, just return raw or try json
            try:
                content = json.loads(raw_response)
            except:
                content = raw_response

            return {
                "content": content,
                "provider": self.provider_type.value,
                "status": "unvalidated"
            }

        return await self.retry_engine.execute(_call)

    async def _api_call(self, prompt: str, context: Optional[Dict]) -> str:
        raise NotImplementedError

class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-pro", **kwargs):
        super().__init__(provider_type=Provider.GEMINI, api_key=api_key, base_url="https://generativelanguage.googleapis.com", **kwargs)
        self.model = model

    async def _api_call(self, prompt: str, context: Optional[Dict]) -> str:
        # Mock for now since we don't have real keys
        await asyncio.sleep(0.1)
        return json.dumps({
            "analysis": f"Gemini analysis of {prompt[:20]}...",
            "confidence": 0.95,
            "metadata": {"tokens": 42}
        })

class OllamaProvider(BaseLLMProvider):
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3", **kwargs):
        super().__init__(provider_type=Provider.OLLAMA, base_url=base_url, **kwargs)
        self.model = model

    async def _api_call(self, prompt: str, context: Optional[Dict]) -> str:
        # Mock for now
        await asyncio.sleep(0.1)
        return json.dumps({
            "analysis": f"Ollama extraction of {prompt[:20]}...",
            "confidence": 0.82,
            "metadata": {"local": True}
        })
