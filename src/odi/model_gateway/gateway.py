from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ModelRequest:
    model_id: str
    operation: str
    payload: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class ModelResponse:
    model_id: str
    output: Any
    usage: dict[str, Any] = field(default_factory=dict)
    raw: Any = None

class ModelProvider(ABC):
    @abstractmethod
    def invoke(self, request: ModelRequest) -> ModelResponse: ...

class ModelGateway:
    """Provider-neutral boundary for model routing, policy and telemetry."""
    def __init__(self) -> None:
        self._providers: dict[str, ModelProvider] = {}

    def register_provider(self, provider_id: str, provider: ModelProvider) -> None:
        if provider_id in self._providers:
            raise ValueError(f"Provider already registered: {provider_id}")
        self._providers[provider_id] = provider

    def invoke(self, provider_id: str, request: ModelRequest) -> ModelResponse:
        return self._providers[provider_id].invoke(request)
