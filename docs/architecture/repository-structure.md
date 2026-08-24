# Repository Structural Boundaries

## Top-Level Structure

```text
src/                 executable system
  odi/
    core/            domain primitives and lifecycle
    contracts/       protocol and schema adapters
    control/         control-plane services
    cognition/       context, reasoning, planning
    knowledge/       retrieval and knowledge services
    memory/          memory streams and state
    registry/        capability, agent, tool, model, workflow registries
    orchestration/   plan and workflow coordination
    capabilities/    design-intelligence capability implementations
    execution/       execution runtime and side-effect boundaries
    validation/      validation and quality gates
    evidence/        provenance and evidence packages
    observability/   traces, metrics, events
    evaluation/      evaluators and benchmark runtime
    evolution/       replay, experiments, candidates, promotion
    interfaces/      API and CLI boundaries

docs/                system documentation and architecture research
knowledge/           curated domain knowledge, not runtime state
schemas/             machine-readable contracts
skills/              governed, discoverable skill packages
workflows/           declarative workflow definitions
evaluations/         datasets and evaluation definitions
configs/             safe configuration templates
scripts/             development and maintenance commands
tests/               verification layers
```

## What Does Not Belong in the Kernel

- Provider-specific image-generation code
- Prompt collections
- UI component implementations
- Raw datasets
- Model weights
- Vendor credentials
- One-off workflow scripts
- Experimental algorithms without contracts
- Unvalidated self-modifying behavior

## What Belongs in the Kernel

Only stable domain contracts and lifecycle primitives required to govern execution belong in `src/odi/core`.

## Knowledge Boundary

`knowledge/` is source-controlled, curated design intelligence. It is not a dump of scraped content. Every reusable rule should carry provenance, confidence, scope, and lifecycle metadata.

## Skill Boundary

A skill is an operationally discoverable capability description. A skill may reference capabilities and tools, but its instructions do not bypass policy or execution contracts.

The skill model follows the useful pattern of explicit skill directories, metadata, routing, and scoped availability observed in modern agent systems.

## Workflow Boundary

Workflows compose capabilities. They should be declarative wherever practical and should remain inspectable, versioned, testable, and replayable.
