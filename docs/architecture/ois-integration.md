# OIS Integration Contract

## Purpose

Obsidian Design Intelligence (ODI) is a domain specialization of Niceone Obsidian Intelligence System (OIS). ODI must consume the OIS execution substrate rather than fork or redefine it.

## Boundary

```text
OIS substrate
  contracts → registries → policy → planning → orchestration → execution
  recovery → evidence → validation → observability → evolution
                         │
                         ▼
ODI specialization
  design capabilities → design agents → design workflows → design evaluators
  brand → audience → competitive → research → identity → typography → production
```

## Reuse rules

1. OIS owns generic execution lifecycle semantics.
2. ODI owns design-domain contracts, capabilities, agents, knowledge, evaluators and workflows.
3. ODI may define adapters/protocols for OIS integration, but must not duplicate an OIS runtime.
4. Provider implementations remain behind registries and gateways.
5. Evidence, validation, policy and lifecycle state must remain first-class.
6. Design workflows must be inspectable, versioned, testable and replayable.
7. Learning may create candidates; promotion remains governed and reversible.

## Canonical lifecycle

```text
intent
  ↓
context + evidence
  ↓
plan
  ↓
policy gate
  ↓
capability / agent routing
  ↓
execution
  ↓
validation
  ↓
checkpoint
  ↓
measurement
  ↓
learning
  ↓
governed evolution
```

## Integration status

This document defines the ODI-side contract. It does not claim that an external OIS runtime is installed as a Python dependency. Until that package boundary is formally published, ODI uses provider-neutral protocols and adapters.

## Non-goals

- Copying the OIS repository into ODI.
- Reimplementing generic agent runtime behavior.
- Embedding provider credentials in ODI.
- Allowing design agents to bypass policy gates.
- Treating generated artifacts as trusted without validation and evidence.
