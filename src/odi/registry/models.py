from dataclasses import dataclass
from odi.registry.base import Registry

@dataclass(frozen=True)
class ModelDefinition:
    id: str
    provider: str
    model: str
    modalities: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()
    context_window: int | None = None
    metadata: dict[str, object] | None = None

class ModelRegistry(Registry[ModelDefinition]):
    def compatible(self, capability_id: str) -> tuple[ModelDefinition, ...]:
        return tuple(m for m in self.list() if capability_id in m.capabilities)
