---
profile_id: governance-policy
layer: agentic
---

# Stage Authoring Matrix

| Stage | Purpose | Canonical owner | Completion evidence |
| --- | --- | --- | --- |
| 00 | policies, roles, provider adapters, skills | Stage 00 plus provider registry | contract, renderer parity, Task |
| 01 | solution-independent requirements | Requirement Package | acceptance and traceability |
| 02 | current structure and durable decisions | Description or ADR | architecture traceability |
| 03 | implementable change contract and execution | Spec Package | focused tests, Task, review |
| 05 | operational knowledge and incidents | Operations catalog | safe procedure and observed result |
| 90 | non-normative evidence | Research, Audit, or Data | provenance and observation date |
| 98 | minimal recovery navigation | Migration or Tombstone | recovery commit |
| 99 | document contracts | registry, schemas, templates | registry/schema tests |

Provider discovery uses generated `.claude/skills/` and `.agents/skills/`, but
canonical reusable procedures remain in Stage 00 `skills/`.

## Related Documents

- [Documentation protocol](documentation-protocol.md)
- [SDLC](../sdlc.md)
- [Stage 99 registry](../../99.templates/registry.json)
