---
profile_id: research
status: active
artifact_id: RES-0002
artifact_type: research
parent_ids:
  - SPEC-0137
created: 2026-08-28
updated: 2026-08-28
observed_at: 2026-08-28
supersedes:
  - RES-0001
---

# Agentic Engineering Research Pack

## Question

What external engineering research and local application evidence can guide an
advisory, branch-only agentic engineering pack without claiming provider
entitlement, runtime execution, Task 9 acceptance, or final integration?

## Scope

This is the draft `RES-0002` pack authorized by SPEC-0137's pre-acceptance
exception. It currently contains this README, two foundation leaves, four D2
analysis leaves, four D3 model/catalog/memory leaves, five D4 SDLC/docs
leaves, three D5 delivery/quality leaves, and two D6 infrastructure/security
leaves. The
`observed_at` date measures local draft measurement, not external access.

| Area | Inventory |
| --- | --- |
| Foundation | [README](./README.md), [workspace-baseline](./workspace-baseline.md), [scope-application-matrix](./scope-application-matrix.md) |
| Agentic | [harness engineering](./harness-engineering.md), [loop engineering](./loop-engineering.md), [provider implementation comparison](./provider-implementation-comparison.md), [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md), [provider model landscape](./provider-model-landscape.md), [agent model selection](./agent-model-selection.md), [AI agent catalogs](./ai-agent-catalogs.md), [memory hierarchy](./memory-hierarchy.md) |
| SDLC and documentation | [spec-driven SDLC](./spec-driven-sdlc.md), [SDLC document roles](./sdlc-document-roles.md), [document metadata lifecycle](./document-metadata-lifecycle.md), [documentation architecture](./documentation-architecture.md), [LLM Wiki system](./llm-wiki-system.md) |
| Delivery and quality | [automation pipeline workflow](./automation-pipeline-workflow.md), [quality CI and formatting](./quality-ci-formatting.md), [verification and validation](./verification-validation.md) |
| Infrastructure and security | [Docker Compose infrastructure](./docker-compose-infrastructure.md), [security governance](./security-governance.md) |

Identity reconciliation and any main-merge cleanup are deferred.
`SDLCDOC-ADR-002` and `SDLCDOC-ADR-003` remain `UNVERIFIED`.

## Requirement-by-Scope Matrix

This aggregate is a closed relevance index, not an adoption, entitlement,
runtime, or claim-verification assertion. Each `applies` cell means the named
owner's Scope Application table supplies the detailed
condition, verification, and limit for that scope. No additional source or
claim is created by this aggregation.

| Subject / category | Owner leaf | agentic | architecture | common | docs | infra | ops | qa | security |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Workspace measurement | [workspace baseline](./workspace-baseline.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Scope application | [scope application matrix](./scope-application-matrix.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Harness elements | [harness engineering](./harness-engineering.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Workspace harness and loop systems, environment, and rules | [harness engineering](./harness-engineering.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Loop feedback, stopping, and escalation | [loop engineering](./loop-engineering.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Claude implementation | [provider implementation comparison](./provider-implementation-comparison.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Codex implementation | [provider implementation comparison](./provider-implementation-comparison.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Common Claude/Codex environment, rules, and system | [provider implementation comparison](./provider-implementation-comparison.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Instruction context | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Model landscape | [provider model landscape](./provider-model-landscape.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Work-aware model and configuration selection | [agent model selection](./agent-model-selection.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| AI agent catalogs / agency-agents | [AI agent catalogs](./ai-agent-catalogs.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Short-term memory | [memory hierarchy](./memory-hierarchy.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Long-term memory | [memory hierarchy](./memory-hierarchy.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Domain memory | [memory hierarchy](./memory-hierarchy.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Memory management | [memory hierarchy](./memory-hierarchy.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Spec-driven development | [spec-driven SDLC](./spec-driven-sdlc.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| SDLC | [spec-driven SDLC](./spec-driven-sdlc.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| PRD | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Architecture Description | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Local historical ARD | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| ADR role and decision scope | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| ADR lifecycle, status, and supersession | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| ADR relationships | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| SPEC | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| PLAN | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| TASK | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Guide | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Incident | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Postmortem | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Policy | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Release evidence practice | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Runbook | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Document metadata and lifecycle | [document metadata lifecycle](./document-metadata-lifecycle.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Diataxis | [documentation architecture](./documentation-architecture.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| C4 Model | [documentation architecture](./documentation-architecture.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| arc42 | [documentation architecture](./documentation-architecture.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Architecture-practice composition | [documentation architecture](./documentation-architecture.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| LLM Wiki | [LLM Wiki system](./llm-wiki-system.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| CI/CD | [automation pipeline workflow](./automation-pipeline-workflow.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| GitHub Actions | [automation pipeline workflow](./automation-pipeline-workflow.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| QA formatting | [quality CI and formatting](./quality-ci-formatting.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| QA linting | [quality CI and formatting](./quality-ci-formatting.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| QA testing | [quality CI and formatting](./quality-ci-formatting.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| QA syntax errors | [quality CI and formatting](./quality-ci-formatting.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Verification | [verification and validation](./verification-validation.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Validation | [verification and validation](./verification-validation.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Docker Compose | [Docker Compose infrastructure](./docker-compose-infrastructure.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Infrastructure | [Docker Compose infrastructure](./docker-compose-infrastructure.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Security | [security governance](./security-governance.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |

The matrix has 50 subject/category rows, eight closed dispositions per row,
and exactly one owner leaf per row. It does not change any leaf's claim state:
the two ADR gaps remain literally `UNVERIFIED`, and DCI feature/OCI/source/
entitlement gaps are not promoted.

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
closed eight-scope routing model, D2's advisory harness, loop, provider, and
instruction analysis, and D3's model-control, static-selection, catalog-intake,
and provider-memory boundaries. D4 adds retained SDLC/document evidence and an
evidence-limited C4/arc42/ADR composition. D5 adds declared automation,
quality-control, and V&V boundaries. D6 adds non-runtime Compose and layered
secure-SDLC/supply-chain boundaries. The 2026-08-23 source roster is not
per-claim proof.
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
| `PML-001` | [provider model landscape](./provider-model-landscape.md) | VERIFIED (tracked configuration) |
| `PML-002` | [provider model landscape](./provider-model-landscape.md) | HISTORICAL VERIFIED (retained official observation) |
| `PML-003` | [provider model landscape](./provider-model-landscape.md) | UNVERIFIED |
| `PML-004` | [provider model landscape](./provider-model-landscape.md) | ADVISORY |
| `AMS-001` | [agent model selection](./agent-model-selection.md) | VERIFIED (tracked configuration) |
| `AMS-002` | [agent model selection](./agent-model-selection.md) | ADVISORY |
| `AMS-003` | [agent model selection](./agent-model-selection.md) | HISTORICAL VERIFIED (retained official observation) |
| `AMS-004` | [agent model selection](./agent-model-selection.md) | VERIFIED (tracked configuration) |
| `AAC-001` | [AI agent catalogs](./ai-agent-catalogs.md) | HISTORICAL VERIFIED (retained fixed source) |
| `AAC-002` | [AI agent catalogs](./ai-agent-catalogs.md) | HISTORICAL VERIFIED (retained fixed source) |
| `AAC-003` | [AI agent catalogs](./ai-agent-catalogs.md) | HISTORICAL VERIFIED (retained fixed source) |
| `AAC-004` | [AI agent catalogs](./ai-agent-catalogs.md) | VERIFIED (tracked governance) |
| `MH-001` | [memory hierarchy](./memory-hierarchy.md) | HISTORICAL VERIFIED (retained official observation) |
| `MH-002` | [memory hierarchy](./memory-hierarchy.md) | HISTORICAL VERIFIED (retained official observation) |
| `MH-003` | [memory hierarchy](./memory-hierarchy.md) | UNVERIFIED |
| `MH-004` | [memory hierarchy](./memory-hierarchy.md) | ADVISORY |
| `SSD-001` | [spec-driven SDLC](./spec-driven-sdlc.md) | HISTORICAL VERIFIED |
| `SSD-002` | [spec-driven SDLC](./spec-driven-sdlc.md) | HISTORICAL VERIFIED |
| `SSD-003` | [spec-driven SDLC](./spec-driven-sdlc.md) | VERIFIED (tracked configuration) |
| `DML-001` | [document metadata lifecycle](./document-metadata-lifecycle.md) | VERIFIED (tracked configuration) |
| `DML-004` | [document metadata lifecycle](./document-metadata-lifecycle.md) | VERIFIED (tracked configuration) |
| `LWS-001` | [LLM Wiki system](./llm-wiki-system.md) | VERIFIED (tracked configuration) |
| `LWS-003` | [LLM Wiki system](./llm-wiki-system.md) | VERIFIED (tracked configuration) |
| `SSD-004` | [spec-driven SDLC](./spec-driven-sdlc.md) | HISTORICAL VERIFIED |
| `DML-002` | [document metadata lifecycle](./document-metadata-lifecycle.md) | VERIFIED (tracked configuration) |
| `DML-003` | [document metadata lifecycle](./document-metadata-lifecycle.md) | VERIFIED (tracked configuration) |
| `DML-005` | [document metadata lifecycle](./document-metadata-lifecycle.md) | VERIFIED (tracked configuration) |
| `LWS-002` | [LLM Wiki system](./llm-wiki-system.md) | VERIFIED (tracked configuration) |
| `LWS-004` | [LLM Wiki system](./llm-wiki-system.md) | HISTORICAL VERIFIED |
| `SDR-001` | [SDLC document roles](./sdlc-document-roles.md) | VERIFIED (tracked configuration) |
| `SDR-002` | [SDLC document roles](./sdlc-document-roles.md) | VERIFIED (tracked configuration) |
| `SDR-003` | [SDLC document roles](./sdlc-document-roles.md) | VERIFIED (tracked + historical retained source) |
| `SDR-004` | [SDLC document roles](./sdlc-document-roles.md) | HISTORICAL VERIFIED |
| `SDR-005` | [SDLC document roles](./sdlc-document-roles.md) | VERIFIED (tracked configuration) |
| `SDR-006` | [SDLC document roles](./sdlc-document-roles.md) | HISTORICAL VERIFIED |
| `DOCARCH-DIATAXIS-BASE-001` | [documentation architecture](./documentation-architecture.md) | HISTORICAL VERIFIED |
| `SCOPE-COMP-001` | [scope application matrix](./scope-application-matrix.md) | ADVISORY |
| `DOCARCH-C4-001` | [documentation architecture](./documentation-architecture.md) | VERIFIED |
| `DOCARCH-ARC42-001` | [documentation architecture](./documentation-architecture.md) | VERIFIED |
| `DOCARCH-COMP-001` | [documentation architecture](./documentation-architecture.md) | ADVISORY |
| `SDLCDOC-ADR-001` | [SDLC document roles](./sdlc-document-roles.md) | VERIFIED |
| `SDLCDOC-ADR-002` | [SDLC document roles](./sdlc-document-roles.md) | UNVERIFIED |
| `SDLCDOC-ADR-003` | [SDLC document roles](./sdlc-document-roles.md) | UNVERIFIED |
| `APW-001` | [automation pipeline workflow](./automation-pipeline-workflow.md) | VERIFIED (tracked configuration) |
| `APW-002` | [automation pipeline workflow](./automation-pipeline-workflow.md) | VERIFIED (tracked configuration) |
| `APW-003` | [automation pipeline workflow](./automation-pipeline-workflow.md) | HISTORICAL VERIFIED (retained official observation) |
| `QCF-001` | [quality CI and formatting](./quality-ci-formatting.md) | VERIFIED (tracked configuration) |
| `QCF-002` | [quality CI and formatting](./quality-ci-formatting.md) | VERIFIED (tracked configuration) |
| `QCF-003` | [quality CI and formatting](./quality-ci-formatting.md) | HISTORICAL VERIFIED (retained official observation) |
| `VV-001` | [verification and validation](./verification-validation.md) | VERIFIED (tracked configuration) |
| `VV-002` | [verification and validation](./verification-validation.md) | HISTORICAL VERIFIED (retained official observation) |
| `VV-003` | [verification and validation](./verification-validation.md) | VERIFIED (tracked governance) |
| `DCI-001` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) | VERIFIED (tracked configuration) |
| `DCI-002` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) | HISTORICAL VERIFIED (retained official observation) |
| `DCI-003` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) | UNVERIFIED |
| `SG-001` | [security governance](./security-governance.md) | HISTORICAL VERIFIED (retained official observation) |
| `SG-002` | [security governance](./security-governance.md) | HISTORICAL VERIFIED (retained official observation) |
| `SG-003` | [security governance](./security-governance.md) | HISTORICAL VERIFIED (retained official observation) |
| `SG-004` | [security governance](./security-governance.md) | VERIFIED (tracked configuration) |

## Architecture Practice Delta Claim Index

| Claim ID | Owner leaf | Evidence mode | Source family |
| --- | --- | --- | --- |
| `DOCARCH-C4-001` | `documentation-architecture.md` | source-backed | `https://c4model.com/` |
| `DOCARCH-ARC42-001` | `documentation-architecture.md` | source-backed | `https://arc42.org/` |
| `DOCARCH-COMP-001` | `documentation-architecture.md` | synthesis-only | `—` |
| `SDLCDOC-ADR-001` | `sdlc-document-roles.md` | source-backed | `https://adr.github.io/` |
| `SDLCDOC-ADR-002` | `sdlc-document-roles.md` | source-backed | `https://adr.github.io/` |
| `SDLCDOC-ADR-003` | `sdlc-document-roles.md` | source-backed | `https://adr.github.io/` |
| `SCOPE-COMP-001` | `scope-application-matrix.md` | synthesis-only | `—` |

## Architecture Practice Direct-Page Index

| Page key | Source ID | Claim ID | Family root | Direct URL | Accessed at | State |
| --- | --- | --- | --- | --- | --- | --- |
| `C4-INTRODUCTION` | `DA-SRC-001` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/introduction` | 2026-08-28 | VERIFIED |
| `C4-ABSTRACTIONS` | `DA-SRC-002` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/abstractions` | 2026-08-28 | VERIFIED |
| `C4-DIAGRAMS` | `DA-SRC-003` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/diagrams` | 2026-08-28 | VERIFIED |
| `C4-NOTATION` | `DA-SRC-004` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/diagrams/notation` | 2026-08-28 | VERIFIED |
| `ARC42-OVERVIEW` | `DA-SRC-005` | `DOCARCH-ARC42-001` | `https://arc42.org/` | `https://arc42.org/overview/` | 2026-08-28 | VERIFIED |
| `ADR-ROLE` | `SDR-SRC-001` | `SDLCDOC-ADR-001` | `https://adr.github.io/` | `https://adr.github.io/madr/decisions/0000-use-markdown-architectural-decision-records.html` | 2026-08-28 | VERIFIED |
| `ADR-LIFECYCLE` | `SDR-SRC-002` | `SDLCDOC-ADR-002` | `https://adr.github.io/` | `https://adr.github.io/madr/decisions/0008-add-status-field.html` | 2026-08-28 | UNVERIFIED |
| `ADR-RELATIONSHIPS` | `SDR-SRC-003` | `SDLCDOC-ADR-003` | `https://adr.github.io/` | `https://adr.github.io/madr/` | 2026-08-28 | UNVERIFIED |

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
| `PML-SRC-001` | [provider model landscape](./provider-model-landscape.md) |
| `PML-SRC-002` | [provider model landscape](./provider-model-landscape.md) |
| `PML-SRC-003` | [provider model landscape](./provider-model-landscape.md) |
| `PML-SRC-004` | [provider model landscape](./provider-model-landscape.md) |
| `PML-SRC-005` | [provider model landscape](./provider-model-landscape.md) |
| `AMS-SRC-001` | [agent model selection](./agent-model-selection.md) |
| `AMS-SRC-002` | [agent model selection](./agent-model-selection.md) |
| `AMS-SRC-003` | [agent model selection](./agent-model-selection.md) |
| `AAC-SRC-001` | [AI agent catalogs](./ai-agent-catalogs.md) |
| `AAC-SRC-002` | [AI agent catalogs](./ai-agent-catalogs.md) |
| `AAC-SRC-003` | [AI agent catalogs](./ai-agent-catalogs.md) |
| `AAC-SRC-004` | [AI agent catalogs](./ai-agent-catalogs.md) |
| `MH-SRC-001` | [memory hierarchy](./memory-hierarchy.md) |
| `MH-SRC-002` | [memory hierarchy](./memory-hierarchy.md) |
| `MH-SRC-003` | [memory hierarchy](./memory-hierarchy.md) |
| `SSD-SRC-001` | [spec-driven SDLC](./spec-driven-sdlc.md) |
| `SSD-SRC-002` | [spec-driven SDLC](./spec-driven-sdlc.md) |
| `SSD-SRC-003` | [spec-driven SDLC](./spec-driven-sdlc.md) |
| `SSD-SRC-004` | [spec-driven SDLC](./spec-driven-sdlc.md) |
| `DML-SRC-001` | [document metadata lifecycle](./document-metadata-lifecycle.md) |
| `DML-SRC-002` | [document metadata lifecycle](./document-metadata-lifecycle.md) |
| `LWS-SRC-001` | [LLM Wiki system](./llm-wiki-system.md) |
| `LWS-SRC-002` | [LLM Wiki system](./llm-wiki-system.md) |
| `LWS-SRC-003` | [LLM Wiki system](./llm-wiki-system.md) |
| `DA-SRC-001` | [documentation architecture](./documentation-architecture.md) |
| `DA-SRC-002` | [documentation architecture](./documentation-architecture.md) |
| `DA-SRC-003` | [documentation architecture](./documentation-architecture.md) |
| `DA-SRC-004` | [documentation architecture](./documentation-architecture.md) |
| `DA-SRC-005` | [documentation architecture](./documentation-architecture.md) |
| `DA-SRC-006` | [documentation architecture](./documentation-architecture.md) |
| `SDR-SRC-001` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-002` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-003` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-004` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-005` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-006` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-007` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-008` | [SDLC document roles](./sdlc-document-roles.md) |
| `APW-SRC-001` | [automation pipeline workflow](./automation-pipeline-workflow.md) |
| `APW-SRC-002` | [automation pipeline workflow](./automation-pipeline-workflow.md) |
| `APW-SRC-003` | [automation pipeline workflow](./automation-pipeline-workflow.md) |
| `APW-SRC-004` | [automation pipeline workflow](./automation-pipeline-workflow.md) |
| `APW-SRC-005` | [automation pipeline workflow](./automation-pipeline-workflow.md) |
| `QCF-SRC-001` | [quality CI and formatting](./quality-ci-formatting.md) |
| `QCF-SRC-002` | [quality CI and formatting](./quality-ci-formatting.md) |
| `QCF-SRC-003` | [quality CI and formatting](./quality-ci-formatting.md) |
| `QCF-SRC-004` | [quality CI and formatting](./quality-ci-formatting.md) |
| `QCF-SRC-005` | [quality CI and formatting](./quality-ci-formatting.md) |
| `VV-SRC-001` | [verification and validation](./verification-validation.md) |
| `VV-SRC-002` | [verification and validation](./verification-validation.md) |
| `VV-SRC-003` | [verification and validation](./verification-validation.md) |
| `DCI-SRC-001` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) |
| `DCI-SRC-002` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) |
| `DCI-SRC-003` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) |
| `DCI-SRC-004` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) |
| `SG-SRC-001` | [security governance](./security-governance.md) |
| `SG-SRC-002` | [security governance](./security-governance.md) |
| `SG-SRC-003` | [security governance](./security-governance.md) |
| `SG-SRC-004` | [security governance](./security-governance.md) |
| `SG-SRC-005` | [security governance](./security-governance.md) |
| `SG-SRC-006` | [security governance](./security-governance.md) |
| `SG-SRC-007` | [security governance](./security-governance.md) |
| `SG-SRC-008` | [security governance](./security-governance.md) |
| `SG-SRC-009` | [security governance](./security-governance.md) |

## Implications

Later leaves may reuse these conventions and link only to files that exist at
their authoring unit. D2 distinguishes retained historical provider capability
from current tracked configuration and labels its cross-surface recommendation
as advisory. D3 adds native model-control boundaries, static (not dynamic)
selection, a pinned catalog intake path, and advisory provider-memory controls.
D4 adds retained SDLC/document evidence and an evidence-limited C4/arc42/ADR
composition. `DOCARCH-COMP-001` and `SCOPE-COMP-001` are advisory synthesis;
the two ADR gaps remain `UNVERIFIED`. D5 distinguishes configuration from local,
hosted, enforced, runtime, validation, and acceptance evidence. D6 keeps
Compose declarations distinct from execution and frames secure-SDLC and
supply-chain sources as advisory, source-bounded inputs rather than local
assurance.

## Traceability

- Governing specification: [SPEC-0137](../../../03.specs/0137-agentic-research-pack-rebuild/spec.md).
- Current execution ledger: [Task 0004](../../../03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md).
- Current local baseline: [workspace baseline](./workspace-baseline.md).
- Closed-scope routing: [scope application matrix](./scope-application-matrix.md).
- D2 harness boundary: [harness engineering](./harness-engineering.md).
- D2 provider comparison: [provider implementation comparison](./provider-implementation-comparison.md).
- D3 model landscape: [provider model landscape](./provider-model-landscape.md).
- D3 selection: [agent model selection](./agent-model-selection.md).
- D3 catalog intake: [AI agent catalogs](./ai-agent-catalogs.md).
- D3 memory boundary: [memory hierarchy](./memory-hierarchy.md).
- D4 SDLC flow: [spec-driven SDLC](./spec-driven-sdlc.md).
- D4 document roles: [SDLC document roles](./sdlc-document-roles.md).
- D4 metadata: [document metadata lifecycle](./document-metadata-lifecycle.md).
- D4 architecture composition: [documentation architecture](./documentation-architecture.md).
- D4 LLM Wiki boundary: [LLM Wiki system](./llm-wiki-system.md).
- D5 automation boundary: [automation pipeline workflow](./automation-pipeline-workflow.md).
- D5 quality taxonomy: [quality CI and formatting](./quality-ci-formatting.md).
- D5 V&V responsibility model: [verification and validation](./verification-validation.md).
- D6 Compose infrastructure boundary: [Docker Compose infrastructure](./docker-compose-infrastructure.md).
- D6 security governance boundary: [security governance](./security-governance.md).
