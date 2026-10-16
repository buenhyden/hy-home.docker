---
title: "Historical Link Classification Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0010"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-16"
---

# Historical Link Classification Task

## Overview

### Objective

Classify the 2,870 links counted by the standing `historical-links-unrecorded`
warning of `check-document-links.py --mode all`. This Task owns criterion 21
only. It does not reopen TSK-0009 or change its criterion 20 decision.

## Inputs and Authorization

The direct user request on 2026-10-16 authorized starting this classification
and then recording it as W26 in a separate branch. The input is published main
`2de045e3b6f79967b4b4050e5cff53ee0b38158f`. The authorization covers this
documentation change, its branch, pull request, and merge through the protected
path. It does not authorize an archived-body edit, a retention-catalog row, a
checker change, or any runtime action.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0010 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0010 | ready | in-progress | #warning-source |
| SPEC-0212-TSK-0010 | in-progress | completed | #classification |

### Warning source

`scripts/lib/document_governance/links.py` counts a historical link as
unrecorded when its archive retention unit has no capture source in
`docs/98.archive/retention-catalog.md`. That catalog states that records
preserved before it existed are not loaded retroactively. The warning is
therefore an intended visibility signal for pre-catalog units, not a defect,
and adding catalog rows for those units would contradict the catalog contract.

### Classification

A read-only analysis reused the checker's own graph builder, retention-unit
mapping, and capture-source loader, so it counted exactly the same 2,870 links
in 174 units (`completed` 311, `retired` 2,501, `superseded` 58). Each link
was then resolved as a Git object at the parent of the last commit that touched
its record's pre-archive origin path (`preserved_origin_path`). Unresolved links
were retried relative to the archive path at that commit and at the archive
capture commit, and then along the record's `git log --follow` rename hops.

| Class | Links | Meaning |
| --- | --- | --- |
| Resolves at the pre-archive origin | 2,558 | Valid historical link |
| Resolves archive-relative at origin or capture | 87 | Link depth was rewritten for the archive location |
| Resolves at an earlier rename hop | 19 | Record was renamed more than once |
| Same-document anchor | 4 | No file target |
| Unresolved at the pre-archive origin | 202 | Residual set below |

151 of 174 units resolve completely. The 202 residual links sit in 23 units:
20 `retired/90.references/audits/*/README.md` units (193 links),
`retired/90.references/research/0001-agentic-research-pack-refresh/README.md`
(7 links), and one directory link each in
`retired/03.specs/0091-workspace-doc-consistency-2026-05/` and
`retired/03.specs/0092-workspace-consistency-2026-05b/`.

All 20 audit units have a Git rename from a flat
`docs/90.references/audits/ref-<id>.md` file to `<id>/README.md` that kept the
relative links unchanged, so those links were already unresolvable at the
immediate origin. For example, `49522aa1d` renamed
`ref-0003-ci-qa-parser-graphify-decision.md`. Re-resolving the 199 file links
of those 20 units from the flat path at each rename commit's parent resolves
187 and leaves 12, which target paths already absent when the flat record was
written. At most 21 of the 2,870 links (those 12, plus the 7 research links
and the 2 directory links) therefore lack a proven historical resolution.

| ID | P | Path@SHA | Classification | Problem | Disposition | Owner | AC | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R13-011 | P02/P04 | `docs/98.archive/retention-catalog.md@2de045e3b` | reproduced | 2,870 pre-catalog historical links have no capture source. | retain warning; no catalog row | Stage 98 archive owner | 21 | Unrecorded link count |
| R13-012 | P02 | `docs/98.archive/retired/90.references/audits/*/README.md@2de045e3b` | reproduced | 20 audit records were renamed into directory READMEs without relative-link rewrites. | retain frozen bodies | Stage 98 archive owner | 21 | Pre-rename resolution |
| R13-013 | P02 | 23 residual units `@2de045e3b` | static | At most 21 links lack a proven historical target. | retain; no current-reference impact | Stage 98 archive owner | 21 | Origin resolution |

No current document is affected: current links are checked separately and the
same full run reports 0 failures.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Unrecorded link count | 21 | W26 | Checker graph, retention unit, and capture-source reuse over `docs/98.archive/*.md` | Main `2de045e3b6f79967b4b4050e5cff53ee0b38158f` | PASS | Count 2,870 in 174 units, equal to the checker warning | required | - |
| Origin resolution | 21 | W26 | `git cat-file -e <origin-parent>:<target>` with archive-relative, capture, and rename-hop retries | Same main; Git 2.43.0; Python 3.12.3 | PASS | 2,558 / 87 / 19 / 4 resolved classes; 202 residual in 23 units | required | - |
| Rename cause | 21 | W26 | `git log --diff-filter=R` over each audit unit and its flat `ref-` path | Same main | PASS | 20 of 20 audit units renamed from a flat `ref-` file; the research unit has no such rename | required | - |
| Pre-rename resolution | 21 | W26 | `git cat-file -e <rename-parent>:<target>` from the flat path | Same main | PASS | 187 of 199 file links resolve; 12 do not | required | - |
| Current link regression | 21 | W26 | `check-document-links.py --mode all` | Same main | PASS | 0 failures; 1 warning (`historical-links-unrecorded`, 2,870) | required | - |
| Changed document metadata | 21 | W26 | `check-document-metadata.py --mode check-changed --base-ref origin/main` | This branch | PASS | Selected Spec, Plan, and this Task; 0 violations | required | - |

The analysis scripts ran from an ignored session scratch directory and are not
a durable artifact; the method above and the Git objects at the named commits
reproduce every count.

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 21 | accepted | Unrecorded link count, Origin resolution, Rename cause, Pre-rename resolution, Current link regression, Changed document metadata | The warning set is classified with a proven cause for the rename residual; no archived body, catalog row, or checker changes. | SPEC-0212 TSK-0010 |

## Review and Completion

This Task completes on the source evidence above. It makes no hosted, merge,
or runtime claim; those are observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [R13 reconciliation Task](tsk-0009-r13-reconciliation.md)
