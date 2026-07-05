---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/sdlc-spec-archive-candidates.md -->

# Reference: SDLC Spec Archive Candidates

## Overview

This report classifies current `docs/03.specs` surfaces and records the
`PLN-DRA-004` disposition results. It identifies completed historical work
products, active canonical specs, draft design/audit specs, and follow-up
candidate groups.

## Purpose

The approved restructure design says historical specs default to archive when
they describe completed work and no longer serve as active implementation
contracts. This report records candidate evidence and final `PLN-DRA-004`
dispositions; it does not move or delete any spec.

## Repository Role

This report supports `PLN-DRA-002` and the `PLN-DRA-004` Stage 03 disposition
batch. It is not a tombstone ledger and does not approve removal of active
links without replacement evidence.

## Scope

### In Scope

- Tracked Markdown under `docs/03.specs/**`.
- Stage 03 status distribution.
- Completed spec candidates and prior draft/active follow-up candidates.
- Link and tombstone prerequisites for future move/remove batches.
- Final `PLN-DRA-004` status/routing decisions.

### Out of Scope

- Moving specs to `docs/98.archive`.
- Creating tombstones.
- Rewriting completed evidence.
- Retiring currently active restructure or domain specs without replacement
  evidence.

## Definitions / Facts

- **Active canonical**: current domain or design guidance that remains part of
  the active chain.
- **Historical archive candidate**: completed work product that may move to
  `docs/98.archive` after link and replacement evidence.
- **Evidence preserve**: completed or draft audit evidence that should remain
  readable in place unless a future plan proves it is no longer active.
- **Prior draft follow-up**: a design/audit spec that needed status or archive
  review before target mutation at the time of the original `PLN-DRA-004`
  candidate review.

## Method

| Evidence ID | Command or Read | Result Summary | Use |
| --- | --- | --- | --- |
| DRA-SDL-001 | `git ls-files 'docs/03.specs/**/*.md' \| wc -l` | 51 tracked Stage 03 Markdown files. | Stage 03 corpus baseline. |
| DRA-SDL-002 | `git ls-files 'docs/03.specs/**/spec.md' \| wc -l` | 26 tracked Stage 03 `spec.md` files. | Spec-file baseline. |
| DRA-SDL-003 | `rg --no-filename -o '^status: [a-z-]+' docs/03.specs --glob '*.md' \| sort \| uniq -c` | Audit baseline had 17 `active`, 9 `completed`, and 7 `draft` status rows. After `PLN-DRA-004`, current counts are recorded in the disposition results. | Candidate status split. |
| DRA-SDL-004 | `rg -l '^status: completed' docs/03.specs --glob '*.md'` | 9 completed Stage 03 files were identified. | Historical archive candidate list. |
| DRA-SDL-005 | `rg -l '^status: draft' docs/03.specs --glob '*.md'` | 7 draft Stage 03 files were identified. | Draft follow-up list. |
| DRA-SDL-006 | Reads of Stage 03 README and parent design spec | Stage 03 README still routes to active/current specs, including recent design specs. | Confirms relink prerequisites before archive moves. |

## Completed Candidate List

| Candidate | Preliminary Disposition | Rationale | Future Batch |
| --- | --- | --- | --- |
| `docs/03.specs/093-docs-taxonomy-agent-first-migration/spec.md` | `historical-archive` candidate | Completed migration work product. | `PLN-DRA-004` |
| `docs/03.specs/094-harness-agent-first-engineering/spec.md` | `historical-archive` or `evidence-preserve` candidate | Completed harness work may still support current governance references. | `PLN-DRA-004` |
| `docs/03.specs/097-home-docker-revalidation-deferred-follow-up/spec.md` | `historical-archive` candidate | Completed follow-up design. | `PLN-DRA-004` |
| `docs/03.specs/095-infra-secrets-docs-refresh/spec.md` | `historical-archive` or `evidence-preserve` candidate | Completed infra/secrets/docs work with redaction boundaries. | `PLN-DRA-004` |
| `docs/03.specs/096-llm-wiki-agent-first-completion/spec.md` | `historical-archive` or `evidence-preserve` candidate | Completed LLM Wiki work may still explain generated index history. | `PLN-DRA-004` |
| `docs/03.specs/098-standardize-infra-net/spec.md` | `historical-archive` candidate | Completed network standardization design. | `PLN-DRA-004` |
| `docs/03.specs/090-workspace-audit-2026-05/spec.md` | `evidence-preserve` candidate | Historical audit snapshot; prior work warns not to rewrite audit history. | `PLN-DRA-004` |
| `docs/03.specs/092-workspace-consistency-2026-05b/spec.md` | `historical-archive` or `evidence-preserve` candidate | Completed consistency design/audit work product. | `PLN-DRA-004` |
| `docs/03.specs/091-workspace-doc-consistency-2026-05/spec.md` | `historical-archive` or `evidence-preserve` candidate | Completed consistency design/audit work product. | `PLN-DRA-004` |

## Prior Follow-Up List

| Candidate | Preliminary Disposition | Rationale | Future Batch |
| --- | --- | --- | --- |
| `docs/03.specs/105-agentic-engineering-implementation-audit-pack/README.md` | `evidence-preserve` / `completed` follow-up | Resolved after the Stage 90 audit pack and Stage 04 evidence were implemented. | 2026-07-05 lifecycle cleanup |
| `docs/03.specs/105-agentic-engineering-implementation-audit-pack/spec.md` | `evidence-preserve` / `completed` follow-up | Resolved after the Stage 90 audit pack and Stage 04 evidence were implemented. | 2026-07-05 lifecycle cleanup |
| `docs/03.specs/103-document-restructure-audit-contract-archive/README.md` | `active-canonical` | Current approved design entrypoint. | No archive in current wave. |
| `docs/03.specs/103-document-restructure-audit-contract-archive/spec.md` | `active-canonical` | Current approved design spec. | No archive in current wave. |
| `docs/03.specs/100-template-system-contract-standardization/spec.md` | `historical-archive` or `evidence-preserve` review | Prior design work appears implemented; verify links before archive. | `PLN-DRA-004` |
| `docs/03.specs/101-template-system-reorganization/README.md` | `historical-archive` or `evidence-preserve` review | Prior design work appears implemented; verify parent routing. | `PLN-DRA-004` |
| `docs/03.specs/101-template-system-reorganization/spec.md` | `historical-archive` or `evidence-preserve` review | Prior design work appears implemented; verify parent routing. | `PLN-DRA-004` |

## PLN-DRA-004 Disposition Results

`PLN-DRA-004` did not create `docs/98.archive/**` tombstones. Link review found
no conflicting Stage 03 current-truth document that should leave the active
chain immediately. Completed historical specs remain as evidence or active
contract inputs when current operations, research, plans, or task records still
consume them.

| Target | Final Disposition | Action | Replacement / Current Pointer |
| --- | --- | --- | --- |
| `docs/03.specs/093-docs-taxonomy-agent-first-migration/spec.md` | `evidence-preserve` | Kept in place; no archive tombstone. | Stage 04 taxonomy plan/task remain the evidence chain. |
| `docs/03.specs/094-harness-agent-first-engineering/spec.md` | `active-canonical` / `evidence-preserve` | Kept in place because Stage 90 research and Stage 05 operations still reference it. | HAFE operations guide, policy, and validation runbook. |
| `docs/03.specs/097-home-docker-revalidation-deferred-follow-up/spec.md` | `evidence-preserve` | Kept in place; no archive tombstone. | Stage 04 deferred follow-up plan/task. |
| `docs/03.specs/095-infra-secrets-docs-refresh/spec.md` | `evidence-preserve` | Kept in place; no archive tombstone. | Stage 04 infra/secrets/docs refresh plan/task and docs index. |
| `docs/03.specs/096-llm-wiki-agent-first-completion/spec.md` | `evidence-preserve` | Kept in place; no archive tombstone. | LLM Wiki generator/index contract and Stage 04 evidence. |
| `docs/03.specs/098-standardize-infra-net/spec.md` | `active-canonical` | Kept in place because operations runbooks use it as the current authoritative IP mapping contract. | Stage 05 infra_net guide/runbook and architecture requirements/decision. |
| `docs/03.specs/090-workspace-audit-2026-05/spec.md` | `evidence-preserve` | Kept in place; no archive tombstone. | Historical audit chain and comparison guides. |
| `docs/03.specs/092-workspace-consistency-2026-05b/spec.md` | `evidence-preserve` | Kept in place; no archive tombstone. | Follow-up governance consistency plan/task. |
| `docs/03.specs/091-workspace-doc-consistency-2026-05/spec.md` | `evidence-preserve` | Kept in place; no archive tombstone. | Predecessor to `workspace-consistency-2026-05b`. |
| `docs/03.specs/105-agentic-engineering-implementation-audit-pack/README.md` | `evidence-preserve` / `completed` | Kept in place and later marked completed after the Stage 90 audit pack and Stage 04 evidence were implemented. | Stage 90 agentic engineering implementation audit pack and Stage 04 evidence. |
| `docs/03.specs/105-agentic-engineering-implementation-audit-pack/spec.md` | `evidence-preserve` / `completed` | Kept in place and later marked completed after the Stage 90 audit pack and Stage 04 evidence were implemented. | Stage 90 agentic engineering implementation audit pack and Stage 04 evidence. |
| `docs/03.specs/103-document-restructure-audit-contract-archive/README.md` | `active-canonical` | Status changed to `active`. | Current `PLN-DRA-*` implementation chain. |
| `docs/03.specs/103-document-restructure-audit-contract-archive/spec.md` | `active-canonical` | Status changed to `active`. | Current `PLN-DRA-*` implementation chain. |
| `docs/03.specs/100-template-system-contract-standardization/spec.md` | `evidence-preserve` | Status changed to `completed`; kept as implementation evidence. | Stage 99 support contracts and Stage 04 standardization task. |
| `docs/03.specs/101-template-system-reorganization/README.md` | `evidence-preserve` / `superseded` | Status changed to `superseded`; body points to the replacement spec. | `docs/03.specs/100-template-system-contract-standardization/spec.md` |
| `docs/03.specs/101-template-system-reorganization/spec.md` | `evidence-preserve` / `superseded` | Status changed to `superseded`; body points to the replacement spec. | `docs/03.specs/100-template-system-contract-standardization/spec.md` |

Current Stage 03 status count after the 2026-07-05 lifecycle cleanup:

| Status | Count | Meaning |
| --- | ---: | --- |
| `active` | 19 | Active domain specs and current design surfaces. |
| `completed` | 16 | Finished specs retained as valid evidence. |
| `superseded` | 2 | Prior template-system reorganization surfaces pointing to the current replacement. |

## Findings

| ID | Surface | Finding | Disposition | Recommended Batch |
| --- | --- | --- | --- | --- |
| DRA-SDL-001 | Completed Stage 03 specs | Link review found no completed spec that should leave the active chain in this batch; completed historical specs remain evidence or active inputs. | `active-canonical` / `evidence-preserve` | Done in `PLN-DRA-004`; no tombstones created. |
| DRA-SDL-002 | Draft Stage 03 specs | The prior draft rows have been reclassified: current document restructure remains active, template contract standardization and the later agentic audit-pack design are completed, and template reorganization is superseded. No Stage 03 draft rows remain. | `active-canonical` / `evidence-preserve` / `completed` | Updated by the 2026-07-05 lifecycle cleanup; no agentic audit-pack future approval item remains. |
| DRA-SDL-003 | Current document restructure spec | The current design spec and README are active for this wave. | `active-canonical` | Done in `PLN-DRA-004`; no target move. |
| DRA-SDL-004 | Active domain specs | 17 active Stage 03 files include canonical domain specs and current design references. | `active-canonical` | No broad archive. |

## Source Rules

- Do not archive a spec until active README links and related documents are
  synchronized.
- Use archive tombstones rather than preserving stale bodies when a document is
  removed from the active chain.
- Preserve historical audit evidence unless a future task proves active
  current-guidance conflict.
- Keep candidate classification separate from move/delete approval.

## Sources

- [Document restructure design spec](../../../03.specs/103-document-restructure-audit-contract-archive/spec.md) - Defines the Stage 03 archive model.
- [Stage 03 README](../../../03.specs/README.md) - Supplies current Stage 03 routing.
- [Archive template](../../../99.templates/templates/common/archive.template.md) - Defines tombstone shape for future archive moves.
- [Historical evidence preservation](../2026-07-03-workspace-document-contract-audit-pack/historical-evidence-preservation.md) - Supplies preservation rules for completed evidence.
- [Document restructure task evidence](../../../04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md) - Supplies baseline and protected boundaries.

## Maintenance

- **Owner**: Documentation Specialist / Repository Maintainer.
- **Review Cadence**: Review before every `docs/03.specs` archive or delete
  batch.
- **Update Trigger**: Update when Stage 03 status values, links, or archive
  candidates change.

## Related Documents

- [Document restructure audit references](./README.md)
- [Restructure gap register](./restructure-gap-register.md)
- [Frontmatter profile inventory](./frontmatter-profile-inventory.md)
- [Document restructure implementation plan](../../../04.execution/plans/2026-07-04-document-restructure-audit-contract-archive.md)
