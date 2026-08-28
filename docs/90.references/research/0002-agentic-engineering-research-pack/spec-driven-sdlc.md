---
status: draft
artifact_id: reference:agentic-engineering-research-draft:spec-driven-sdlc
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Spec-Driven SDLC

## Overview

Spec-driven work makes an approved problem statement, an executable change
proposal, and its durable record distinct artifacts. It is a way to reduce
ambiguity before implementation; it is not evidence that a repository runs a
particular command workflow.

## Purpose

Compare retained SpecKit and OpenSpec flows with this workspace's durable
Spec/Plan/Task ownership, without adopting either tool's commands or claiming
standards conformance.

## Scope

This analysis uses retained observations only. The ISO catalogue records broad
life-cycle and requirements topics; it does not grant access to paid clauses or
prove a current process conforms to ISO/IEC/IEEE 12207, 29148, or 42010.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `SSD-001` | Retained 2026-08-14 SpecKit evidence describes a ten-phase flow from constitution and specification through planning, tasks, implementation, and analysis. | historical retained source | HISTORICAL VERIFIED | retained `../2026-08-08-agentic-engineering-research-pack/spec-driven-sdlc.md:196-197` and source rows 250+ | Treat the phases as a comparison model, not a local command contract. |
| `SSD-002` | Retained 2026-08-14 OpenSpec evidence separates explore, propose, apply, and archive, with live specs, in-flight changes, and archived changes. | historical retained source | HISTORICAL VERIFIED | retained `../2026-08-08-agentic-engineering-research-pack/spec-driven-sdlc.md:196-197` and source rows 250+ | Compare these states to durable local artifacts rather than importing slash commands. |
| `SSD-003` | This workspace assigns approved behavior to a Spec, proposed execution to a Plan, and progress/evidence to a Task; cleanup of Plan/Task material requires durable capture and approval. | tracked workspace configuration | VERIFIED | `docs/03.specs/` | A local change should preserve those owner boundaries. |
| `SSD-004` | ISO/IEC/IEEE 12207:2026 publicly describes life-cycle processes from conception through retirement and iterative use; the public abstracts for 29148:2018 and 42010:2022 describe requirements and architecture-description topics. | historical retained source | HISTORICAL VERIFIED | Task 0001 ledger | Use as vocabulary only; no clause-level compliance conclusion follows. |

The useful comparison is state-oriented: an OpenSpec live specification resembles
the local approved Spec, an in-flight proposal resembles local Plan/Task work,
and an archive resembles retained history. The mapping is advisory because
local ownership and approval rules, not a tool state, decide authority.

An SDLC still needs a complete learning loop: Requirements Package captures
needs; Architecture Description and decision records communicate structure and
choices; Spec, Plan, and Task form the change contract; implementation and QA
produce bounded verification evidence; operations use catalog and incident
records; postmortems feed preventive learning; and living documents retire when
replaced. A failed check or unresolved evidence returns to the original owner
(requirements, architecture, delivery, operations, or QA), rather than being
silently repaired by an adjacent artifact.

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SSD-SRC-001` | `SSD-001` | SpecKit flow / GitHub | [immutable SpecKit tree](https://github.com/github/spec-kit/tree/83883a2ebad7e7de667fd00381b100d597faf846) | historical retained source | pin `83883a2ebad7e7de667fd00381b100d597faf846` | 2026-08-14 | This retained pin, not the older 2026-08-08 pin, supports the ten-phase description. |
| `SSD-SRC-002` | `SSD-002` | OpenSpec workflow / Fission-AI | [immutable OpenSpec README](https://raw.githubusercontent.com/Fission-AI/OpenSpec/2826b8889e5223a9a8095d4428b60b56597e1020/README.md) | historical retained source | pin `2826b8889e5223a9a8095d4428b60b56597e1020` | 2026-08-14 | Retained workflow observation; no command was executed here. |
| `SSD-SRC-003` | `SSD-003` | SPEC-0153 and documentation cleanup / workspace | [SPEC-0153](../../../03.specs/0153-workspace-governance-simplification/spec.md); [Stage 03 README](../../../03.specs/README.md) | tracked workspace configuration | `29d947b4bec58bec35d8555c27f2b3550634fe43` | 2026-08-28 | Configuration documents do not prove enforcement. |
| `SSD-SRC-004` | `SSD-004` | ISO public catalogues / ISO | `https://www.iso.org/standard/90219.html`; `https://www.iso.org/standard/72089.html`; `https://www.iso.org/standard/74393.html` | historical retained source | public catalogue records | 2026-08-08 | Abstract/catalogue material is not paid standard text or conformance evidence. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Relate agent work to a durable Spec and Task. | Inspect the current Spec package. | No agent execution is proved. |
| architecture | applies | Keep architecture intent in its typed owner. | Check the current Stage 03 Spec/Plan/Task route before a decision. | Tool phases do not assign architecture authority. |
| common | applies | Preserve approved handoff and capture rules. | Review the scoped diff. | Advisory comparison only. |
| docs | applies | Use Spec/Plan/Task roles when documenting work. | Check frontmatter and links. | No workflow adoption is implied. |
| infra | applies | Connect infrastructure change intent to its Spec/Plan/Task owner. | Check the scoped package and infrastructure owner. | No runtime evidence. |
| ops | applies | Feed operational incidents and learning back to their owner. | Confirm catalog or incident-packet path. | No operation is inferred. |
| qa | applies | Capture checks against the Task. | Inspect recorded check evidence. | A record is not a green suite. |
| security | applies | Retain approval and source boundaries. | Review cited local sources. | No control effectiveness is evaluated. |

## Maintenance

Refresh only from an approved retained source update or a reviewed local
ownership change. Do not turn tool commands, catalogue abstracts, or old status
flags into current conformance claims.

## Related Documents

- [SDLC document roles](./sdlc-document-roles.md)
- [Document metadata lifecycle](./document-metadata-lifecycle.md)
- [SPEC-0137](../../../03.specs/0137-agentic-research-pack-rebuild/spec.md)
