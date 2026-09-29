"""Composition root for the ODI architecture.

This module wires the structural planes together without selecting concrete
vendors, models, vector stores, image engines, or production integrations.
"""

from dataclasses import dataclass

from odi.context.engine import ContextEngine
from odi.design.capability import DesignCapabilityFabric
from odi.evidence.ledger import EvidenceLedger
from odi.execution.runtime import ExecutionRuntime
from odi.knowledge.fabric import KnowledgeFabric
from odi.model_gateway.gateway import ModelGateway
from odi.observability.telemetry import TelemetrySink
from odi.registry.agents import AgentRegistry
from odi.registry.capabilities import CapabilityRegistry
from odi.registry.models import ModelRegistry
from odi.supervision.supervisor import Supervisor
from odi.validation.engine import ValidationEngine


@dataclass
class ODIKernel:
    capabilities: CapabilityRegistry
    agents: AgentRegistry
    models: ModelRegistry
    model_gateway: ModelGateway
    knowledge: KnowledgeFabric
    context: ContextEngine
    supervisor: Supervisor
    runtime: ExecutionRuntime
    validation: ValidationEngine
    evidence: EvidenceLedger
    telemetry: TelemetrySink
    design: DesignCapabilityFabric


def build_kernel(runtime: ExecutionRuntime) -> ODIKernel:
    return ODIKernel(
        CapabilityRegistry(),
        AgentRegistry(),
        ModelRegistry(),
        ModelGateway(),
        KnowledgeFabric(),
        ContextEngine(),
        Supervisor(),
        runtime,
        ValidationEngine(),
        EvidenceLedger(),
        TelemetrySink(),
        DesignCapabilityFabric(),
    )
