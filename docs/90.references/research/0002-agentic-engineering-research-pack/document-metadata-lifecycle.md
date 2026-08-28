---
status: draft
artifact_id: reference:agentic-engineering-research-draft:document-metadata-lifecycle
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Document Metadata Lifecycle

## Overview

Metadata makes document identity, lifecycle, and parent relationships machine
checkable, while document prose supplies the human explanation. It does not
make configuration into proof that a document has been reviewed or executed.

## Purpose

Describe the current registry-backed lifecycle model and its limits for this
draft research pack.

## Scope

The sole machine authority is `docs/99.templates/registry.json`; `support/` is
legacy according to the Stage 99 README. This leaf does not alter either.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `DML-001` | Covered SDLC/operations artifact profiles share required fields `profile_id`, `status`, `artifact_id`, `artifact_type`, `parent_ids`, `created`, and `updated`; the generic-reference exception intentionally differs. | tracked workspace configuration | VERIFIED | `docs/99.templates/registry.json` | Select the declared profile rather than inventing a parallel schema. |
| `DML-002` | Three illustrated registry families distinguish living-document `draft`/`active`/`superseded`/`retired`, execution `draft`/`active`/`blocked`/`completed`/`cancelled`, and incident `open`/`mitigated`/`closed` states. | tracked workspace configuration | VERIFIED | registry lifecycle entries | Supersession and retirement are distinct; status wording must follow the registered family. |
| `DML-003` | This research leaf uses the generic-reference draft contract and defers final identity reconciliation. | tracked workspace configuration | VERIFIED | SPEC-0137 | Draft metadata does not establish Task 9 acceptance. |
| `DML-004` | Identity (`artifact_id`) differs from a path: profile path patterns, `artifact_type`, `parent_ids`, dates, and status together make routing and handoff inspectable. | tracked workspace configuration | VERIFIED | registry and generic-reference contract | A rename or a link alone must not silently transfer authority. |
| `DML-005` | Validation can check selected metadata and local links, but it cannot prove review quality, source sufficiency, runtime execution, or remote enforcement. | tracked workspace configuration | VERIFIED | validation contract | Keep evidence state separate from validator exit status. |

Required frontmatter gives a consumer enough information to identify the
artifact and its parent boundary; required sections give the human reader the
handoff content. `artifact_id` is identity, while a profile path pattern only
routes that identity. Concrete parent examples are `REQ` to `AD`, Spec to
Plan/Task, and Incident to Postmortem. Status describes lifecycle, not quality:
a Task can record a failed check, an Incident can be open/mitigated/closed, and
a living document may be superseded or retired according to its registered
family. Stage 03 cleanup is permitted only after durable capture and approval;
that is a preservation boundary, not an ADR lifecycle assertion.

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DML-SRC-001` | `DML-001`, `DML-002` | Document registry / workspace | [registry](../../../99.templates/registry.json); [Stage 99 README](../../../99.templates/README.md) | tracked workspace configuration | `29d947b4bec58bec35d8555c27f2b3550634fe43` | 2026-08-28 | Declared schema and lifecycle, not observed enforcement. |
| `DML-SRC-002` | `DML-003`, `DML-004`, `DML-005` | SPEC-0137 draft exception, Stage 03, and validation contract / workspace | [Approved Pre-Acceptance Draft Exception](../../../03.specs/0137-agentic-research-pack-rebuild/spec.md#approved-pre-acceptance-draft-exception) (`DML-003`); [SPEC-0153](../../../03.specs/0153-workspace-governance-simplification/spec.md), [Stage 03 README](../../../03.specs/README.md), and [metadata validator](../../../../scripts/validation/check-document-metadata.py) (`DML-004`, `DML-005`) | tracked workspace configuration | `29d947b4bec58bec35d8555c27f2b3550634fe43` | 2026-08-28 | Field/link checks do not prove content truth, review quality, source sufficiency, or runtime execution. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Give agent-authored records typed metadata. | Check the declared profile. | No execution proof. |
| architecture | applies | Use AD and ADR profiles for their distinct roles. | Inspect registry paths. | This leaf does not settle ADR gaps. |
| common | applies | Preserve identity and status fields. | Run scoped metadata validation. | Validation is syntactic. |
| docs | applies | Maintain one registry authority. | Confirm registry references. | `support/` is legacy. |
| infra | applies | Use typed metadata for infrastructure-owned documents. | Check the registered profile and owner path. | No deployment inference. |
| ops | applies | Use incident and runbook lifecycle profiles. | Inspect registry entries. | No live operation claim. |
| qa | applies | Check metadata before publication. | Record check result in Task. | Check does not establish content correctness. |
| security | applies | Avoid secret values in metadata. | Inspect scoped diff. | No security-control test. |

## Maintenance

Update only when the registry or the approved generic-reference contract
changes. Keep lifecycle descriptions separate from ADR evidence gaps.

## Related Documents

- [SDLC document roles](./sdlc-document-roles.md)
- [LLM Wiki system](./llm-wiki-system.md)
- [Scope application matrix](./scope-application-matrix.md)
