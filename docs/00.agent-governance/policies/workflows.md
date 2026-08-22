---
profile_id: governance-policy
layer: agentic
---

# Workflows

This document owns repeatable provider-neutral workflow order. Provider
adapters may map native controls but may not redefine these states.

## SDLC Workflow

1. Capture long-lived, solution-independent needs in Stage 01.
2. Capture current structure and durable decisions in Stage 02.
3. Define a bounded change contract, approach, plan, and Task in Stage 03.
4. Implement only approved Task scope and verify its acceptance contract.
5. Maintain operator knowledge and runtime procedures in Stage 05.
6. Preserve external evidence in Stage 90 and minimal recovery in Stage 98.

`sdlc.md` owns stage boundaries, the Stage 99 registry owns document shapes
and lifecycle values, and `scripts/` owns executable validation.

## Supporting Workflows

- Infrastructure: `compose-stack-agent` -> `infra-validate` -> independent review.
- Code review: self-verification -> findings -> owner resolution -> re-verification.
- Quality: tests first for behavior changes -> QA verification -> Task evidence.
- Security: audit plus threat modeling; escalate exposed secrets or critical risk.
- Incident: response record -> corrective action routed to its canonical stage.
- Governance: source change -> validation -> regeneration -> independent review.

Agents run all-files pre-commit only through
`scripts/validation/run-agent-precommit-all-files.sh` and only after the
task-owned state is a Git-visible, non-ignored repository change.

## Skill Lifecycle

Reusable procedures follow discovery, applicability, canonical Stage 00 source,
registered projection, focused validation, and evidence. Provider projections
do not own this lifecycle.

## Related Documents

- [SDLC](../sdlc.md)
- [Agentic policy](./agentic.md)
- [Stage authoring matrix](stage-authoring-matrix.md)
- [Provider capability matrix](provider-capability-matrix.md)
