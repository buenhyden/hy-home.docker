---
title: "Archive Occupancy, Route Citation, and Frozen Identity Implementation Plan"
version: "1.2.0"
type: "sdlc/plan"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-16"
layer: "specs"
artifact_id: "SPEC-0178-PLAN-0001"
parent_ids:
- "SPEC-0178"
created: "2026-09-16"
---

# Archive Occupancy, Route Citation, and Frozen Identity Implementation Plan

## Objective

Move the occupancy, archive link, and Retention Catalog source checks onto
`ADR-0036`, require a closure date on a resolved Incident, and accept `ADR-0036`
in the result tree that makes every one of those checks live.

## Dependencies

- SPEC-0177 is completed and preserved, `ADR-0035` is `accepted`, and
  `common.archive_disposition_model` is `adopted`, before W3 starts.
- The operator approved taking this package forward on 2026-09-16, including
  RES-0096 item A11.
- Each document admits one lifecycle transition per integration, judged against
  the upstream base. The package therefore takes four integrations: review
  with W1; approval with W2; activation and acceptance with W3 to W7; and
  completion with W8.
- The registered lifecycles admit no forward edge that skips a state, so each document
  has exactly one status path across those four integrations. The Spec moves
  `draft`, `review`, `approved`, `active`, `completed`; the Plan moves `draft`,
  `approved`, `active`, `completed`; and the Task moves `draft`, `ready`,
  `in-progress`, `completed`. The Task therefore reaches `ready` at W2 and
  `in-progress` at W3 to W7, and no integration may set it to `in-progress`
  from `draft`.

## Execution Sequence

Two steps precede the sequence and carry no acceptance criterion, so they are
recorded here rather than numbered as work units: W1, which added RES-0096 item
A11 to the Spec, settled its Open Question, and put the Spec to review with this
Plan and its Task as drafts; and W2, which obtained two independent approval
reviews, settled their findings, and approved the Spec and this Plan. The
registered completion contract requires a receipt for every numbered work unit,
and neither produces acceptance evidence. The Task's Work Log keeps both under
those names and the Commit Ledger keeps their commits.

1. W3: Judge Stage 03 occupancy per package and admit a `completed` Task in an
   unfinished package. Files: `scripts/lib/document_governance/archive.py`,
   `tests/lib/document_governance/test_archive.py`.
2. W4: Reject every source's link to a route record before the incident and
   postmortem exception applies. Files:
   `scripts/lib/document_governance/links.py`,
   `tests/lib/document_governance/test_links.py`.
3. W5: Declare `common.frozen_transition_fields` and compare each catalog unit
   with its `Source` object by members, modes, body bytes, and registered
   frontmatter fields. Files: `docs/99.templates/registry.json`,
   `docs/99.templates/contracts/document-profile.schema.json`,
   `scripts/lib/document_governance/archive.py`,
   `tests/lib/document_governance/test_archive.py`,
   `tests/lib/document_governance/test_registry.py`.
4. W6: Require `resolved_at` on a `resolved` Incident. Files:
   `docs/99.templates/registry.json`,
   `tests/lib/document_governance/test_registry.py`.
5. W7: In the result tree that lands W3 to W6: accept `ADR-0036` with its
   `supersedes` naming `ADR-0035` and the surviving rules restated; preserve
   `ADR-0035` under `docs/98.archive/superseded/` with its catalog row; repoint
   every active document that links `ADR-0035` by path or labels its status, so
   that no active-stage link to that path remains; and amend every text surface
   the Spec names, which includes the new `REQ-0026` requirement owning incident
   closure evidence, the pre-move evidence-commit statement in the policy under
   Retention by status with its matching item in
   `.agents/governance/task-checklists.md`, and the byte-identity sentence in
   the Stage 98 README How to Work in This Area list.
6. W8: Run the changed profile, obtain an independent exact-diff review, and
   complete and preserve the package with its own catalog row.

| Acceptance criterion | Work unit |
| --- | --- |
| 1 | W3 |
| 2 | W4 |
| 3 | W5 |
| 4 | W5 |
| 5 | W3, W4, W5, W6, W7 |
| 6 | W7 |
| 7 | W8 |
| 8 | W8 |
| 9 | W6 |

## Risk and Rollback

| Risk | Guard | Recovery |
| --- | --- | --- |
| A check goes live before `ADR-0036` is accepted | W3 to W7 land in one result tree | Revert that integration; `ADR-0036` stays `proposed` |
| A frozen body fails the source comparison | Only records with a catalog row are compared, and every row is checked before the integration | Correct the row, never the frozen body |
| A completing change writes evidence in its move | The source comparison reports the body difference | Move the evidence into the commit before the move |

## Verification

The Task records every command, exit code, review finding, and PASS, FAIL,
BLOCKED, NOT_RUN, or N/A state up to the commit that holds every content change,
which is the last tree the Task can still be written in. Completion requires a
receipt row for every acceptance criterion and work-unit pair. W1 and W2 carry
no acceptance criterion and are evidenced by their Work Log entries alone.

## Rulings

- No sealed record or frozen body is edited.
- Tests are written first and fail first for every rule W3 to W6 add.
