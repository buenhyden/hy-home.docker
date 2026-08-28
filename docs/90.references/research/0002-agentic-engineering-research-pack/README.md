---
profile_id: research
status: draft
artifact_id: RES-0002
artifact_type: research
parent_ids:
  - SPEC-0137
created: 2026-08-28
updated: 2026-08-28
observed_at: 2026-08-28
---

# Agentic Engineering Research Pack

## Question

What external engineering research and local application evidence can guide an
advisory, branch-only agentic engineering pack without claiming provider
entitlement, runtime execution, Task 9 acceptance, or final integration?

## Scope

This is the draft `RES-0002` pack authorized by SPEC-0137's pre-acceptance
exception. It currently contains this README and two authored foundation
leaves; the remaining eighteen inventory entries are future draft work. The
`observed_at` date measures local draft measurement, not external access.

| Area | Inventory |
| --- | --- |
| Foundation | [README](./README.md), [workspace-baseline](./workspace-baseline.md), [scope-application-matrix](./scope-application-matrix.md) |
| Agentic | `harness-engineering.md`, `loop-engineering.md`, `provider-implementation-comparison.md`, `agent-instructions-vibe-coding.md`, `provider-model-landscape.md`, `agent-model-selection.md`, `ai-agent-catalogs.md`, `memory-hierarchy.md` |
| SDLC and documentation | `spec-driven-sdlc.md`, `sdlc-document-roles.md`, `document-metadata-lifecycle.md`, `documentation-architecture.md`, `llm-wiki-system.md` |
| Delivery and quality | `automation-pipeline-workflow.md`, `quality-ci-formatting.md`, `verification-validation.md` |
| Infrastructure and security | `docker-compose-infrastructure.md`, `security-governance.md` |

The final subject/category × scope matrix is D7 work and is not yet covered by
this partial draft. Identity reconciliation and any main-merge cleanup are
deferred. `SDLCDOC-ADR-002` and `SDLCDOC-ADR-003` remain `UNVERIFIED`; no claim row is owned
here for them until D4 creates their owning leaf and evidence-limited links.

## Method

The foundation remeasured tracked files at baseline
`264a6d1d64a41c329cd86b5978fb47f38503673f`. It uses configuration evidence
only: configuration documents establish declared routing or controls, never
runtime execution, provider acceptance, entitlement, remote enforcement, or
secrets. The current `main` snapshot `d6cac43d77653e833732ec589f333db333222e07`
is recorded only as an unchanged comparison, not as Task 9 acceptance.

Claims use the leaf prefix plus `-NNN`; sources use `<prefix>-SRC-NNN`. Each
leaf uses the same claim table (`Claim ID`, `Claim`, `Evidence class`, `State`,
`Workspace target`, `Implication`) and source table (`Source ID`, `Claim IDs`,
`Title / publisher`, `URL or path`, `Class`, `Revision / observed`, `Accessed at`,
`Caveat`). These are working content conventions for this draft, not policy.

## Findings

The authored evidence is limited to a reproducible workspace baseline and the
closed eight-scope routing model. The 2026-08-23 source roster is not per-claim
proof. Retained Task 0001 ledger observations retain their original 2026-08-08
and 2026-08-09 dates; Task 0004's architecture-delta record is dated 2026-08-28.
Graphify revision `f8a72211` is stale advisory material and is not used as proof.

### Claim Index

| Claim ID | Owner leaf | State |
| --- | --- | --- |
| `WB-001` | [workspace-baseline](./workspace-baseline.md) | VERIFIED (tracked baseline) |
| `WB-002` | [workspace-baseline](./workspace-baseline.md) | VERIFIED (tracked configuration) |
| `SAM-001` | [scope-application-matrix](./scope-application-matrix.md) | VERIFIED (tracked specification) |
| `SAM-002` | [scope-application-matrix](./scope-application-matrix.md) | VERIFIED (tracked governance routing) |

## Sources

### Source Index

| Source ID | Owner leaf |
| --- | --- |
| `WB-SRC-001` | [workspace-baseline](./workspace-baseline.md) |
| `WB-SRC-002` | [workspace-baseline](./workspace-baseline.md) |
| `WB-SRC-003` | [workspace-baseline](./workspace-baseline.md) |
| `SAM-SRC-001` | [scope-application-matrix](./scope-application-matrix.md) |
| `SAM-SRC-002` | [scope-application-matrix](./scope-application-matrix.md) |

## Implications

Later leaves may reuse these conventions and link only to files that exist at
their authoring unit. `SCOPE-COMP-001` and the three composition-link sections
belong exclusively to D4, after all three participating files exist.

## Traceability

- Governing specification: [SPEC-0137](../../../03.specs/0137-agentic-research-pack-rebuild/spec.md).
- Current execution ledger: [Task 0004](../../../03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md).
- Current local baseline: [workspace baseline](./workspace-baseline.md).
- Closed-scope routing: [scope application matrix](./scope-application-matrix.md).
