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
exception. It currently contains this README, two foundation leaves, and four
D2 analysis leaves; the remaining fourteen inventory entries are future draft work. The
`observed_at` date measures local draft measurement, not external access.

| Area | Inventory |
| --- | --- |
| Foundation | [README](./README.md), [workspace-baseline](./workspace-baseline.md), [scope-application-matrix](./scope-application-matrix.md) |
| Agentic | [harness engineering](./harness-engineering.md), [loop engineering](./loop-engineering.md), [provider implementation comparison](./provider-implementation-comparison.md), [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md), `provider-model-landscape.md`, `agent-model-selection.md`, `ai-agent-catalogs.md`, `memory-hierarchy.md` |
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

The authored evidence now includes a reproducible workspace baseline, the
closed eight-scope routing model, and D2's advisory harness, loop, provider,
and instruction analysis. The 2026-08-23 source roster is not per-claim proof.
Retained Task 0001 ledger observations retain their original 2026-08-08 and
2026-08-09 dates; Task 0004's architecture-delta record is dated 2026-08-28.
Graphify revision `f8a72211` is stale advisory material and is not used as proof.

### Claim Index

| Claim ID | Owner leaf | State |
| --- | --- | --- |
| `WB-001` | [workspace-baseline](./workspace-baseline.md) | VERIFIED (tracked baseline) |
| `WB-002` | [workspace-baseline](./workspace-baseline.md) | VERIFIED (tracked configuration) |
| `SAM-001` | [scope-application-matrix](./scope-application-matrix.md) | VERIFIED (tracked specification) |
| `SAM-002` | [scope-application-matrix](./scope-application-matrix.md) | VERIFIED (tracked governance routing) |
| `HE-001` | [harness engineering](./harness-engineering.md) | VERIFIED (tracked configuration) |
| `HE-002` | [harness engineering](./harness-engineering.md) | VERIFIED (tracked configuration) |
| `HE-003` | [harness engineering](./harness-engineering.md) | HISTORICAL VERIFIED (retained official observation) |
| `HE-004` | [harness engineering](./harness-engineering.md) | VERIFIED (tracked configuration) |
| `HE-005` | [harness engineering](./harness-engineering.md) | HISTORICAL VERIFIED (retained official observation) |
| `LE-001` | [loop engineering](./loop-engineering.md) | VERIFIED (tracked configuration) |
| `LE-002` | [loop engineering](./loop-engineering.md) | VERIFIED (tracked configuration) |
| `LE-003` | [loop engineering](./loop-engineering.md) | VERIFIED (tracked configuration) |
| `LE-004` | [loop engineering](./loop-engineering.md) | HISTORICAL VERIFIED (retained official observation) |
| `LE-005` | [loop engineering](./loop-engineering.md) | HISTORICAL VERIFIED (retained external study) |
| `PIC-001` | [provider implementation comparison](./provider-implementation-comparison.md) | VERIFIED (tracked configuration) |
| `PIC-002` | [provider implementation comparison](./provider-implementation-comparison.md) | VERIFIED (tracked configuration) |
| `PIC-003` | [provider implementation comparison](./provider-implementation-comparison.md) | VERIFIED (tracked configuration) |
| `PIC-004` | [provider implementation comparison](./provider-implementation-comparison.md) | HISTORICAL VERIFIED (retained official observation) |
| `PIC-005` | [provider implementation comparison](./provider-implementation-comparison.md) | HISTORICAL VERIFIED (retained official observation) |
| `PIC-006` | [provider implementation comparison](./provider-implementation-comparison.md) | HISTORICAL VERIFIED (retained official observation) |
| `PIC-007` | [provider implementation comparison](./provider-implementation-comparison.md) | HISTORICAL VERIFIED (retained official observation) |
| `AIV-001` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) | VERIFIED (tracked configuration) |
| `AIV-002` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) | VERIFIED (tracked configuration) |
| `AIV-003` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) | HISTORICAL VERIFIED (retained official observation) |
| `AIV-004` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) | ADVISORY |
| `AIV-005` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) | HISTORICAL VERIFIED (retained official observation) |

## Sources

### Source Index

| Source ID | Owner leaf |
| --- | --- |
| `WB-SRC-001` | [workspace-baseline](./workspace-baseline.md) |
| `WB-SRC-002` | [workspace-baseline](./workspace-baseline.md) |
| `WB-SRC-003` | [workspace-baseline](./workspace-baseline.md) |
| `SAM-SRC-001` | [scope-application-matrix](./scope-application-matrix.md) |
| `SAM-SRC-002` | [scope-application-matrix](./scope-application-matrix.md) |
| `HE-SRC-001` | [harness engineering](./harness-engineering.md) |
| `HE-SRC-002` | [harness engineering](./harness-engineering.md) |
| `HE-SRC-003` | [harness engineering](./harness-engineering.md) |
| `HE-SRC-004` | [harness engineering](./harness-engineering.md) |
| `HE-SRC-005` | [harness engineering](./harness-engineering.md) |
| `HE-SRC-006` | [harness engineering](./harness-engineering.md) |
| `HE-SRC-007` | [harness engineering](./harness-engineering.md) |
| `LE-SRC-001` | [loop engineering](./loop-engineering.md) |
| `LE-SRC-002` | [loop engineering](./loop-engineering.md) |
| `LE-SRC-003` | [loop engineering](./loop-engineering.md) |
| `LE-SRC-004` | [loop engineering](./loop-engineering.md) |
| `PIC-SRC-001` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-002` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-003` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-004` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-005` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-006` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-007` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-008` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-009` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `AIV-SRC-001` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) |
| `AIV-SRC-002` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) |
| `AIV-SRC-003` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) |
| `AIV-SRC-004` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) |
| `AIV-SRC-005` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) |

## Implications

Later leaves may reuse these conventions and link only to files that exist at
their authoring unit. D2 distinguishes retained historical provider capability
from current tracked configuration and labels its cross-surface recommendation
as advisory. `SCOPE-COMP-001` and the three composition-link sections belong
exclusively to D4, after all three participating files exist.

## Traceability

- Governing specification: [SPEC-0137](../../../03.specs/0137-agentic-research-pack-rebuild/spec.md).
- Current execution ledger: [Task 0004](../../../03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md).
- Current local baseline: [workspace baseline](./workspace-baseline.md).
- Closed-scope routing: [scope application matrix](./scope-application-matrix.md).
- D2 harness boundary: [harness engineering](./harness-engineering.md).
- D2 provider comparison: [provider implementation comparison](./provider-implementation-comparison.md).
