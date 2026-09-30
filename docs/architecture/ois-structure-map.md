# OIS → ODI Structure Map

This map records which architectural concerns are inherited from the Niceone Obsidian substrate and which remain owned by ODI.

| Concern | OIS substrate | ODI | Rule |
|---|---|---|---|
| Core lifecycle | Authoritative | Adapter only | Do not fork runtime semantics |
| Contracts | Canonical | Design-domain contracts | Extend by composition |
| Capability registry | Platform registry | Design capability registrations | Same discovery model |
| Agent registry | Platform registry | Design agent registrations | Agents consume capabilities |
| Model gateway | Provider-neutral | Design routing requirements | No vendor lock-in |
| Policy | Authoritative | Design policy definitions | ODI cannot bypass policy |
| Planning | Generic | Design planning strategies | Planning before execution |
| Orchestration | Generic | Design workflows | Declarative where practical |
| Execution | Generic | Design providers | Side effects through execution port |
| Recovery | Generic | Design recovery policies | Checkpoint and replay |
| Evidence | Authoritative | Design evidence producers | Provenance follows decisions |
| Validation | Generic gates | Design evaluators | Output is untrusted until validated |
| Observability | Platform telemetry | Design metrics | Shared trace identity |
| Memory | Platform boundary | Design memory schemas | Knowledge is not memory |
| Evaluation | Generic evaluation lifecycle | Design benchmarks | Promotion requires evidence |
| Evolution | Governed promotion | Design candidates | Candidate ≠ active |

## Dependency direction

```text
ODI design domain
      ↓
ODI adapters / protocols
      ↓
OIS substrate contracts
      ↓
OIS runtime and governance
      ↓
providers / infrastructure
```

No reverse dependency should make the OIS substrate import ODI design-domain logic.

## Anti-patterns explicitly prohibited

- copying `ois/` into `src/odi/`;
- introducing a second policy engine for design execution;
- introducing a second generic agent runtime;
- bypassing the execution boundary from a design capability;
- treating model-provider APIs as ODI contracts;
- allowing evolution to activate itself without evaluation and promotion;
- declaring a design artifact trusted merely because generation completed.
