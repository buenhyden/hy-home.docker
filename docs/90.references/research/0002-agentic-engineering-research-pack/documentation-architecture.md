---
status: active
artifact_id: reference:agentic-engineering-research:documentation-architecture
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Documentation Architecture

## Overview

Diataxis organizes reader needs; C4 communicates software structure through
views; arc42 supplies a tailorable architecture-document outline; ADRs retain
individual decisions. These practices overlap in communication but do not
replace lifecycle ownership or one another.

## Purpose

Provide a bounded, source-aware comparison for documentation design without
claiming local adoption, mandatory tool use, or missing ADR relationships.

## Scope

The preserved Diataxis observation is dated 2026-08-08. C4, arc42, and ADR
direct-page evidence is retained from Task 0004 at 2026-08-28. The rendered
Diataxis site is `UNVERIFIED`; the pinned source is the retained evidence.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `DOCARCH-DIATAXIS-BASE-001` | Four modes are tutorial/learning, how-to/task, reference/information, and explanation/understanding; structure grows incrementally. | historical retained source | HISTORICAL VERIFIED | retained dated pack | Choose form by reader need. |
| `DOCARCH-C4-001` | Useful C4 levels are context, container, component, and code; notation makes views self-contained with scope, legend, labels, technology and accessible directed relationships. | retained delta evidence | VERIFIED | Task 0004 C4 records | A container is not Docker proof. |
| `DOCARCH-ARC42-001` | arc42 tailors goals, constraints, context, strategy, building blocks, runtime, deployment, concepts, decisions, quality, risks/debt, and glossary. | retained delta evidence | VERIFIED | Task 0004 ARC42 record | Equal depth is not mandatory. |
| `DOCARCH-COMP-001` | Advisory composition: Diataxis selects form, C4 supplies a view, arc42 an outline; `SDLCDOC-ADR-001` supports ADR role but `SDLCDOC-ADR-002`/`003` are `UNVERIFIED`. | advisory synthesis | ADVISORY | local typed documents | No ADR lifecycle or AD/Spec relationship inference. |

| Compared practices | Purpose | Granularity | Artifact / view | Relationship and evidence boundary |
| --- | --- | --- | --- | --- |
| Diataxis and C4 | Diataxis selects tutorial/learning, how-to/task, reference/information, or explanation/understanding; C4 communicates software structure. | Reader need versus context, container, component, and code levels. | Prose form versus a self-contained structural diagram. | `DOCARCH-DIATAXIS-BASE-001` and `DOCARCH-C4-001`; neither selects a lifecycle owner. |
| C4 and arc42 | C4 makes a selected structural view legible; arc42 provides a tailorable outline. | A C4 level versus twelve arc42 sections. | Diagram/view versus architecture-document outline. | `DOCARCH-C4-001` and `DOCARCH-ARC42-001`; select only the needed depth. |
| arc42 and ADR | arc42 includes decisions in an outline; an ADR records a decision-ready choice. | Outline section versus one decision. | Architecture document versus structured Markdown decision record. | `DOCARCH-ARC42-001` and `SDLCDOC-ADR-001`; lifecycle is `SDLCDOC-ADR-002` (`UNVERIFIED`) and AD/Spec relation is `SDLCDOC-ADR-003` (`UNVERIFIED`). |

Every ADR comparison in this leaf cites `SDLCDOC-ADR-001`,
`SDLCDOC-ADR-002`, and `SDLCDOC-ADR-003`: ADR role is supported, while lifecycle
and Architecture Description/Spec relationship assertions remain `UNVERIFIED`.

## Architecture Practice Delta Claims

| Claim ID | Owner leaf | Evidence mode | Source family |
| --- | --- | --- | --- |
| `DOCARCH-C4-001` | `documentation-architecture.md` | source-backed | `https://c4model.com/` |
| `DOCARCH-ARC42-001` | `documentation-architecture.md` | source-backed | `https://arc42.org/` |
| `DOCARCH-COMP-001` | `documentation-architecture.md` | synthesis-only | `—` |

## Architecture Practice Direct-Page Evidence

| Page key | Source ID | Claim ID | Family root | Direct URL | Accessed at | State |
| --- | --- | --- | --- | --- | --- | --- |
| `C4-INTRODUCTION` | `DA-SRC-001` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/introduction` | 2026-08-28 | VERIFIED |
| `C4-ABSTRACTIONS` | `DA-SRC-002` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/abstractions` | 2026-08-28 | VERIFIED |
| `C4-DIAGRAMS` | `DA-SRC-003` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/diagrams` | 2026-08-28 | VERIFIED |
| `C4-NOTATION` | `DA-SRC-004` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/diagrams/notation` | 2026-08-28 | VERIFIED |
| `ARC42-OVERVIEW` | `DA-SRC-005` | `DOCARCH-ARC42-001` | `https://arc42.org/` | `https://arc42.org/overview/` | 2026-08-28 | VERIFIED |

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DA-SRC-001` | `DOCARCH-C4-001` | Introduction / C4 model | [C4 introduction](https://c4model.com/introduction) | retained delta evidence | no stated revision | 2026-08-28 | Architecture communication and progressive views only. |
| `DA-SRC-002` | `DOCARCH-C4-001` | Abstractions / C4 model | [C4 abstractions](https://c4model.com/abstractions) | retained delta evidence | no stated revision | 2026-08-28 | Container is an application/data store, not Docker. |
| `DA-SRC-003` | `DOCARCH-C4-001` | Diagrams / C4 model | [C4 diagrams](https://c4model.com/diagrams) | retained delta evidence | no stated revision | 2026-08-28 | Useful levels, not every level, are supported. |
| `DA-SRC-004` | `DOCARCH-C4-001` | Notation / C4 model | [C4 notation](https://c4model.com/diagrams/notation) | retained delta evidence | no stated revision | 2026-08-28 | Notation guidance is not a local gate. |
| `DA-SRC-005` | `DOCARCH-ARC42-001` | Template Overview / arc42 | [arc42 overview](https://arc42.org/overview/) | retained delta evidence | no stated revision | 2026-08-28 | Tailorable overview; linked documents were not visited. |
| `DA-SRC-006` | `DOCARCH-DIATAXIS-BASE-001` | Diataxis pinned source / evildmp | [pinned source](https://github.com/evildmp/diataxis-documentation-framework/tree/957c09ca40b4a1edc23874f713e01937d50d54d5/source) | historical retained source | pin `957c09ca40b4a1edc23874f713e01937d50d54d5` | 2026-08-08 | Pinned source verified; rendered site is UNVERIFIED. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Present agent boundaries at a useful C4 level. | Review view type and labels. | No system is modelled here. |
| architecture | applies | Combine outline, structural view, and decision record deliberately. | Check typed owner and links. | ADR gaps remain UNVERIFIED. |
| common | applies | Choose reader mode before structure. | Inspect intended audience. | Advisory synthesis. |
| docs | applies | Use Diataxis form and self-contained diagrams where useful. | Check scope, legend, and links. | No mandatory template. |
| infra | applies | Use deployment views only when useful. | Review local infrastructure owner. | C4 container is not Docker proof. |
| ops | applies | Use dynamic/deployment communication for an operational concern. | Confirm operating artifact owner. | No operation observed. |
| qa | applies | Review diagrams for clarity and accessibility. | Inspect labels and abbreviations. | No formal accessibility certification. |
| security | applies | Include threat-relevant relationships when scoped. | Review diagram evidence. | No threat-model execution. |

## Architecture Practice Composition Links

- [SDLC document roles](./sdlc-document-roles.md)
- [Scope application matrix](./scope-application-matrix.md)

## Maintenance

Refresh direct-page rows only through approved evidence work. Keep composition
explicitly advisory and do not turn the ADR gaps into lifecycle or relationship
claims.

## Related Documents

- [SDLC document roles](./sdlc-document-roles.md)
- [Scope application matrix](./scope-application-matrix.md)
- [LLM Wiki system](./llm-wiki-system.md)
