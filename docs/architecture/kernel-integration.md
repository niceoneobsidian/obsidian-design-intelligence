# Niceone Obsidian Kernel Integration

## Purpose

This repository is the design-intelligence specialization of the Niceone Obsidian ecosystem. The shared execution structures developed in `niceone-obsidian` are integrated here as design-domain control contracts rather than duplicated as provider-specific agents.

## Integrated structures

| OIS structure | ODI integration | Status |
|---|---|---|
| Capability Registry | `odi.registry.capabilities.CapabilityRegistry` | integrated |
| Agent Registry | `odi.registry.agents.AgentRegistry` | integrated |
| Capability / Agent Routing | `odi.control.router.CapabilityRouter` | integrated foundation |
| Policy Engine | `odi.control.policy.PolicyEngine` | integrated |
| Approval Matrix | `odi.control.policy.ApprovalMatrix` | integrated foundation |
| Workflow / Execution State | `odi.control.state.WorkflowState` | integrated |
| Execution Identity | `odi.control.state.ExecutionIdentity` | integrated |
| Checkpoint Store | `odi.control.checkpoint.CheckpointStore` | integrated foundation |
| Failure Classification | `odi.control.recovery.FailureClass` | integrated |
| Recovery Policy | `odi.control.recovery.RecoveryPolicy` | integrated |
| Supervisor | `odi.control.supervisor.Supervisor` | integrated foundation |
| Evaluation Harness | `odi.evaluation.evaluator.Evaluator` | integrated |
| Evaluation Dataset | `odi.evaluation.evaluator.EvaluationDataset` | integrated |
| Candidate Evaluation | `odi.evaluation.evaluator.Candidate` | integrated |
| Promotion Control | `odi.evaluation.evaluator.PromotionDecision` | integrated |

## Architectural boundary

The integration follows this direction:

```text
Niceone Obsidian
  shared governed execution substrate
            |
            v
Obsidian Design Intelligence
  design capabilities + design knowledge + design evaluation
```

ODI must not recreate the kernel as a second independent runtime. It consumes the same concepts and preserves the control-plane ordering:

```text
Intent
  -> Context
  -> Policy Gate
  -> Capability Routing
  -> Planning / Orchestration
  -> Execution
  -> Validation / Evaluation
  -> Checkpoint
  -> Recovery / Escalation
  -> Evidence / Observability
  -> Learning / Evolution
```

## Source alignment

The integration is based on the existing Niceone Obsidian kernel work, including its versioned registry primitives, capability/agent routing, policy checks, execution state, supervisor, bounded recovery and durable checkpoint tests. The ODI layer adapts those structures to its existing `CapabilityContract`, `ExecutionContext`, evidence, validation and design capability contracts.

## Remaining production boundary

These integrations are intentionally deterministic foundations. Distributed service discovery, durable external checkpoint storage, production authorization providers, distributed rollback, multi-tenant infrastructure and deployment-specific orchestration remain infrastructure concerns and should be integrated behind these contracts rather than embedded into design capabilities.
