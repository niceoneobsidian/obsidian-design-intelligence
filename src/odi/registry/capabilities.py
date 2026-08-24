"""Capability registry boundary.

The registry stores contracts, not provider-specific implementation details.
"""

from odi.core.contracts import CapabilityContract


class CapabilityRegistry:
    def __init__(self) -> None:
        self._items: dict[str, CapabilityContract] = {}

    def register(self, capability: CapabilityContract) -> None:
        if capability.id in self._items:
            raise ValueError(f"Capability already registered: {capability.id}")
        self._items[capability.id] = capability

    def get(self, capability_id: str) -> CapabilityContract:
        return self._items[capability_id]

    def list(self) -> tuple[CapabilityContract, ...]:
        return tuple(self._items.values())
