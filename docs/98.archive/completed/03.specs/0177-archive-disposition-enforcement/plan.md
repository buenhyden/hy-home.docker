---
title: "Archive Disposition Enforcement Implementation Plan"
version: "1.4.0"
type: "sdlc/plan"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-16"
layer: "specs"
artifact_id: "SPEC-0177-PLAN-0001"
parent_ids:
- "SPEC-0177"
created: "2026-09-15"
---

# Archive Disposition Enforcement Implementation Plan

## Objective

Move the registered checks onto the Stage 98 model the policy already states,
without rewriting a sealed record and without an integration in which the policy
and a check disagree without a named transition.

## Dependencies

- The policy section, the Stage 98 README, `REQ-0026`, `AD-0030`, and `ADR-0035`
  landed in the change that opened this package.
- The Spec's four Open Questions were answered by the operator on 2026-09-15,
  and the approval review's findings were settled in the Spec before approval.
- The operator approved the amendment on 2026-09-15 after the assessment
  RES-0096 records. It changes no status and lands with W5. RES-0096 and the
  Task entries written that day call it W4b; the registered completion contract
  admits only a `W` followed by digits, so the unit carries the next free number,
  W9, while keeping its execution position after W4.
- Each document admits one lifecycle transition per integration. The package
  therefore takes five integrations: approval; activation, which landed W3, W6,
  and W4; W5 with W9, with the switch still at `transition`; adoption with W7;
  and completion with W8.

## Execution Sequence

Two steps precede the sequence and carry no acceptance criterion, so they are
recorded here rather than numbered as work units: opening the package, which
allocated `ADR-0035` and `SPEC-0177`, applied the policy text with its transition
paragraph, and recorded the measured link graph; and approval, which answered the
Open Questions and settled the approval review. The Task's Work Log keeps both
under their original names, W1 and W2, and the Commit Ledger keeps their commits.

1. W3: Add `common.archive_disposition_model` at `transition` with the test that
   binds `adopted` to `ADR-0035`, found by identity in Stage 02 or Stage 98,
   having left `proposed` through `accepted`, and move the link boundary
   behind it. Files: `docs/99.templates/registry.json`,
   `scripts/lib/document_governance/registry.py`,
   `scripts/lib/document_governance/links.py`,
   `tests/lib/document_governance/test_links.py`,
   `tests/lib/document_governance/test_registry.py`.
2. W4: Add the Retention Catalog check and the change-aware rule that a preserved
   record added without its row is rejected, inert at `transition`, with the
   comparison base passed into the recovery run. Files:
   `scripts/lib/document_governance/archive.py`,
   `scripts/lib/document_governance/lifecycle/recovery.py`,
   `scripts/validation/check-document-corpus-lifecycle.py`,
   `tests/lib/document_governance/test_archive.py`, and the recovery tests.
3. W9: Extend the Retention Catalog to the units and names `ADR-0035` already
   states, inert at `transition`: an Incident bundle directory as a tree unit,
   with package and bundle shapes read from the Registry `spec` and `incident`
   path patterns; the per-class `Names` forms of Behavior Contract 7, with
   identifiers recognized by the Registry profiles' `artifact_id_pattern`
   values; and coverage over
   every regular file a change adds. Files:
   `scripts/lib/document_governance/archive.py`,
   `tests/lib/document_governance/test_archive.py`. It lands in the integration
   that carries W5.
4. W5: Parse and validate the new Tombstone and Migration shapes beside the
   sealed ones, add `sealed_section_shapes` support, reject an added sealed-shape
   record, apply the exactly-one withdrawal rule, and let
   `_recorded_retirements` accept a catalog row, inert at `transition`. Files:
   `scripts/lib/document_governance/archive.py`,
   `scripts/lib/document_governance/registry.py`,
   `scripts/lib/document_governance/metadata/heading.py` with the base passed from
   `scripts/validation/check-document-metadata.py --mode check-changed`,
   `scripts/lib/document_governance/spec_packages.py`, and their tests.
5. W6: Register `resolved`: `PRESERVED_DISPOSITIONS`, the
   `archive-record-resolved` profile, `load_archive` admission behind the switch,
   and the literal sites in `archive.py`, `links.py`, and
   `lifecycle/recovery.py`, with a fixture test. Files: those modules,
   `docs/99.templates/registry.json`, `tests/lib/document_governance/test_archive.py`,
   `tests/lib/document_governance/metadata/test_reference.py`.
6. W7: Adopt the model in one result tree: the switch, the Registry section
   lists, both templates, `ADR-0035` accepted with `ADR-0033`'s surviving rules
   restated, `ADR-0033` preserved with its catalog row and repointed links, and
   the rewrite of every surface criterion 9 names.
7. W8: Run the changed profile, obtain an independent review, and complete and
   preserve the package with its own catalog row.

| Acceptance criterion | Work unit |
| --- | --- |
| 1 | W3, W4, W9, W5, W6 |
| 2 | W3 |
| 3 | W6 |
| 4 | W4, W9 |
| 5 | W5, W7 |
| 6 | W5 |
| 7 | W4, W9 |
| 8 | W7 |
| 9 | W7 |
| 10 | W8 |
| 11 | W8 |

## Risk and Rollback

| Risk | Guard | Recovery |
| --- | --- | --- |
| A new rule changes findings on the real corpus before adoption | Every new rule reads the switch, and criterion 1 compares findings at `transition` | Revert the unit; the switch stays `transition` |
| A sealed record fails after W7 | W7 runs the corpus check over every tracked Tombstone and Migration before its commit | Revert W7; the switch returns to `transition` |
| The pairing is released with no withdrawal owner | W5's exactly-one rule lands with W4's catalog check already present | Revert W5 |
| Adoption lands while a text surface still describes the transition | W7 edits the switch and every surface criterion 9 names together | Leave `ADR-0035` at `proposed` and the switch at `transition` |

## Verification

The Task records every command, exit code, review finding, and PASS, FAIL,
BLOCKED, NOT_RUN, or N/A state. Completion requires every acceptance criterion
in the Spec to have a receipt row per criterion and work-unit pair.

## Rulings

- No sealed Tombstone, Migration, or frozen body is edited.
- A guard that fires is treated as correct until proven otherwise.
- No `resolved/` directory is created without a closed Incident to hold.
- Tests are written first and fail first for every rule W3 to W6 add.
