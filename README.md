# Obsidian Design Intelligence

## Design Intelligence Operating System

Obsidian Design Intelligence (ODI) is the design-intelligence layer of the Niceone Obsidian ecosystem. It turns design intent, evidence, knowledge, reasoning, execution, validation, measurement, and learning into a governed system rather than a collection of prompts or generators.

> **Core principle:** design intelligence proposes; governance authorizes; execution produces; validation verifies; evidence determines what becomes trusted.

## System Loop

```text
INTENT
  ↓
CONTEXT
  ↓
EVIDENCE
  ↓
KNOWLEDGE
  ↓
REASONING
  ↓
DECISION
  ↓
EXECUTION
  ↓
VALIDATION
  ↓
MEASUREMENT
  ↓
LEARNING
  ↓
CONTROLLED EVOLUTION
  ↺
```

## Canonical Architecture

```text
                         ┌──────────────────────────┐
                         │       CONTROL PLANE       │
                         │ intent · policy · config  │
                         │ registry · authorization │
                         └────────────┬─────────────┘
                                      │
                                      ▼
┌──────────────┐       ┌──────────────────────────┐       ┌───────────────┐
│ KNOWLEDGE    │──────▶│       INTELLIGENCE       │──────▶│ EXECUTION     │
│ FABRIC       │       │ context · reasoning      │       │ FABRIC        │
│ evidence     │       │ planning · decisions    │       │ capabilities  │
│ ontology     │       │ routing · synthesis     │       │ tools · media │
│ retrieval    │       └────────────┬─────────────┘       │ workflows     │
└──────────────┘                    │                     └───────┬───────┘
                                    ▼                             │
                         ┌──────────────────────┐                │
                         │ VALIDATION / EVAL    │◀───────────────┘
                         │ quality · policy     │
                         │ visual · production  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ OBSERVABILITY        │
                         │ traces · cost ·      │
                         │ latency · outcomes   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ LEARNING / EVOLUTION  │
                         │ experiments · replay  │
                         │ candidates · canary  │
                         └──────────────────────┘
```

## Structural Rules

1. **Intent is not execution authority.**
2. **Knowledge is separated from memory.**
3. **Evidence is first-class data.**
4. **Capabilities are stable contracts; agents and tools are providers.**
5. **Planning is separated from execution.**
6. **Validation is part of the execution lifecycle, not an afterthought.**
7. **Visual generation is a capability family, not the system kernel.**
8. **Every consequential action produces traceable state and evidence.**
9. **Learning creates candidates; governance controls activation.**
10. **Production changes are versioned, measurable, and reversible.**

## Repository Layout

```text
obsidian-design-intelligence/
├── docs/                 # architecture, contracts, governance, research
├── src/                  # executable ODI packages
├── knowledge/            # curated design intelligence and evidence
├── schemas/              # machine-readable contracts
├── skills/               # governed design/visual skill definitions
├── workflows/            # reusable execution graphs
├── evaluations/          # datasets, evaluators, benchmarks
├── configs/              # environment-neutral configuration
├── scripts/              # development and maintenance tooling
└── tests/                # unit, integration, contract, evaluation tests
```

## Relationship to Niceone Obsidian

ODI is intentionally compatible with the governance and execution doctrine established by the Niceone Obsidian Intelligence System (OIS). OIS provides the broader governed execution substrate; ODI specializes that substrate for design intelligence, visual reasoning, design systems, creative production, and evidence-driven design decisions.

The previous repository establishes the principles of capability contracts, registries, policy boundaries, execution, validation, recovery, observability, measurement, learning, and controlled evolution. ODI reuses those architectural principles rather than duplicating them.

## Reference Architecture Research

The architecture is informed by patterns observed in production AI and design systems, including agent architecture libraries, RAG/context engines, LLM gateways, workflow platforms, skill systems, model runtimes, and design-intelligence tooling. See [`docs/research/reference-architectures.md`](docs/research/reference-architectures.md).

## Status

**Phase:** Architecture foundation  
**Evidence level:** Designed / repository scaffolded  
**Production status:** Not production-verified

Architecture claims must not be treated as implementation claims. Implementation, tests, integration, runtime, security, deployment, and rollback evidence are required before a capability is marked production verified.
