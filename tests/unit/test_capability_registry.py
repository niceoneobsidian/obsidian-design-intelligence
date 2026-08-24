from odi.core import CapabilityContract, LifecycleState, RiskClass
from odi.registry.capabilities import CapabilityRegistry


def test_register_and_get_capability() -> None:
    registry = CapabilityRegistry()
    capability = CapabilityContract(
        id="design.system.generate",
        name="Generate Design System",
        version="0.1.0",
        input_schema={"type": "object"},
        output_schema={"type": "object"},
        risk_class=RiskClass.LOW,
        lifecycle_state=LifecycleState.DESIGNED,
    )

    registry.register(capability)

    assert registry.get("design.system.generate") == capability
    assert registry.list() == (capability,)
