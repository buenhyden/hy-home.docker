---
title: "Generation 6 Reader Corrections Task"
version: "0.2.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0233-TSK-0001"
parent_ids:
- "SPEC-0233-PLAN-0001"
created: "2026-10-13"
---

# Generation 6 Reader Corrections Task

## Objective

Make the generation 6 reader and its text do what SPEC-0231 and ADR-0048
state, as the 2026-10-13 review found.

## Inputs and Authorization

On 2026-10-13 the owner asked to review SPEC-0231 criteria 1 to 6, SPEC-0232
criteria 1 to 6 and ADR-0048. The request authorizes source, test and
document changes, logical commits, the branch push and its pull request. ADR
acceptance and every Spec or Task status change stay with the owner. Baseline
`main` `958349408`.

## Work Log

### Starting State

An independent read-only `code-reviewer` review of `b1a6976f4` found the gaps
the Spec lists, at `spec_packages.py` lines 1686 to 1689 (second row only),
1766 to 1784 (acceptance checked for a whole completed Task only) and 5204 to
5215 (departure gate only for an `approved` base).

### W1 Exactly One Acceptance Row

After the Criterion Acceptance loop, `_v6_evidence_contract` reports the first
criterion that the Plan assigns to a current, non-cancelled Task and that has
no row. On the active corpus this found SPEC-0204 criteria 5 and 10: neither
had evidence when SPEC-0231 migrated the corpus, so contract 8 gave them no
row. Each now has a `pending` row in the lowest-numbered current Task the
Plan assigns it to: criterion 5 in TSK-0001 (W5), criterion 10 in TSK-0016
(W65). No decision was made for either. No other package lacks a row.

### W2 Item Closure

The per-group loop now checks both rules for a `completed` Task or a
`completed` item: `PASS` for every pair of its work, and every criterion its
Task decides for that work `accepted` or `not-required`. The separate whole-
Task check is gone because the single-mode group is the whole Task. A test
runs three cases through a Plan split over two single-mode Tasks and through
one multi-item Task, and both reach the same judgment. SDLC (1.4.1) now says
the item rule and exactly one row in a current Task.

### W3 Departure Gate

`_ordinary_preserved_paths` computes readiness for every base package and
skips only the completed disposition when the base is not ready or its Spec is
not `approved`. A `draft` base whose archived copy says `approved` is no longer
preserved; an `approved` ready base still is. Superseded preservation keeps
its own checks, which it skipped before whenever an `approved` base was not
ready.

After the rules review (W5), the gate also refuses a ready `cancelled` base
whose copy says `approved`, and a copy whose members differ from the base in
status or Execution Items. `_preserved_package_is_terminal` now compares each
base member's status and items with the copy instead of only member paths.
Both cases fail on the reader before this fix and pass after it.

### W4 Rule Fixtures

New passing and failing cases cover a multi-item Task with a frontmatter
`status` (through `_parse_document`), one Execution Item, items that do not
cover the Task's Work Units, a Criterion Acceptance row outside the Plan
assignment, acceptance Evidence naming a missing row, and a `FAIL` row in the
resolving position. Existing fixtures that had only a criterion 1 row gained
a `pending` criterion 2 row. `test_generation6` now has 28 tests. Against the
`main` reader, the four behavior tests fail (missing row, item criteria,
mode equivalence, departure gate); the six rule fixtures pass there because
those rules were already enforced.

### W5 Text

ADR-0048 (0.2.0, still `proposed`) states the exactly-one row, the item rule
and the completed-archive gate, and replaces only ADR-0037 decision 1, except
its last sentence, and the completion-receipt clauses of decisions 2 and 3; it
names the rules from those decisions that stay in force. The decisions README
(1.6.4) says the
same, lists ADR-0044, 0045 and 0046 as accepted as their files say, and its
`### Usage` repeats became `### Audience` and `### Authoring Flow`, as did the
descriptions README (1.1.6). AD-0030 (2.1.1) links ADR-0048.

An independent `rules-engineer` review of `c1cd329a5` returned changes
required:

- `sdlc.md` and ADR-0048 said "exactly one row" for every criterion, but the
  code exempts criteria whose assigned Tasks are all historical or cancelled.
  Both texts now state the exemption.
- The completed-archive gate let a ready `cancelled` base enter the completed
  archive with an `approved` copy, and did not compare member statuses. Fixed
  in W3.
- ADR-0048 said a ready `cancelled` or `superseded` package may wait in Stage
  03, while AD-0030 and the occupancy check keep no member of such a package
  there. ADR-0048 and `sdlc.md` now let only an approved Spec wait, and AD-0030
  points to ADR-0048 for the readiness definition instead of restating it.
- ADR-0048 now keeps in force ADR-0037's whole-package disposition approval
  and the unfinished-package rule, and defines an unfinished package.
- The decisions README lost a blank line inside its inventory, lists
  ADR-0045 to 0047 in its Structure tree, and calls ADR-0032 accepted as its
  file does.

A second review of the corrected text is recorded in the Evidence.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rows | 1 | W1 | Missing-row test RED on `main` then GREEN; corpus lifecycle (0 violations); repository contract integration tests (14) | Branch on `958349408` | PASS | W1 Exactly One Acceptance Row | - |
| Items | 2 | W2 | Item and equivalence tests RED on `main` then GREEN | Branch on `958349408` | PASS | W2 Item Closure | - |
| Departure | 3 | W3 | Departure test RED on `main` then GREEN | Branch on `958349408` | PASS | W3 Departure Gate | - |
| Fixtures | 4 | W4 | `test_generation6` (28); Spec package and archive suites (158); metadata suites (141) | Branch on `958349408` | PASS | W4 Rule Fixtures | - |
| Text | 5 | W5 | Governance contract (0 failures); active (573) and changed (11) metadata checks, 0 violations | Branch on `958349408` | PASS | W5 Text | - |
| Departure status | 3 | W3 | Cancelled-base and changed-copy cases RED on `c1cd329a5` then GREEN; `test_generation6` (28) | Branch | PASS | W3 Departure Gate | - |
| Rules review | 5 | W5 | Independent `rules-engineer` review | `c1cd329a5` | FAIL | W5 Text | - |
| Rules re-review | 5 | W5 | Independent `rules-engineer` review of the corrected text: approve with notes, notes applied | Corrected branch | PASS | W5 Text | Rules review |
| Gate | 6 | W6 | Changed gate; candidate quality | Branch | NOT_RUN | Work Log | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | pending | - | - |
| 2 | pending | - | - |
| 3 | pending | - | - |
| 4 | pending | - | - |
| 5 | pending | - | - |
| 6 | pending | - | - |

## Review and Completion

No criterion is accepted until the owner accepts it.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
