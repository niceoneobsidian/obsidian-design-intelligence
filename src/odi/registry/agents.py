from dataclasses import dataclass
from odi.registry.base import Registry

@dataclass(frozen=True)
class AgentDefinition:
    id: str
    name: str
    role: str
    capabilities: tuple[str, ...] = ()
    system_policy: str = ""

class AgentRegistry(Registry[AgentDefinition]):
    def resolve_for(self, capability_id: str) -> tuple[AgentDefinition, ...]:
        return tuple(a for a in self.list() if capability_id in a.capabilities)
