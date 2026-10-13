---
title: "Generation 6 Reader Corrections"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0233"
parent_ids:
- "REQ-0026"
- "AD-0030"
- "ADR-0048"
created: "2026-10-13"
---

# Generation 6 Reader Corrections

## Overview

On 2026-10-13 the owner asked for a review of the SPEC-0231 acceptance
criteria and ADR-0048. An independent read-only review of `main` `b1a6976f4`
found that the generation 6 reader does not yet do what SPEC-0231 and
ADR-0048 state:

- SPEC-0231 contract 5 says every criterion has exactly one Criterion
  Acceptance row; the reader rejects a second row but never reports a missing
  one.
- Contract 6 says an item may be `completed` only when its criteria are
  accepted or `not-required`; the reader checks that only for a whole
  `completed` Task, so a single-mode Task and an equivalent multi-item Task
  can be judged differently. SDLC was worded to match the code.
- Contract 7 says a package leaves for the completed archive only from a ready
  base revision; the reader applies that only when the base Spec is
  `approved`, so a `draft` base whose archived copy says `approved` passes.
- Six enforced rules have no failing fixture.
- ADR-0048 replaces all of ADR-0037 decisions 1 to 3 although rules in
  decisions 2 and 3 stay in force; the decisions README lists ADR-0044, 0045
  and 0046 as proposed though their files are accepted; the Stage 02
  sub-READMEs still repeat `### Usage`.

## Scope

In scope: `scripts/lib/document_governance/spec_packages.py`, its generation 6
tests, the SDLC policy text for these rules, ADR-0048 (text only, status
unchanged), the decisions and descriptions READMEs, AD-0030's Related
Documents, and the acceptance rows the new check requires in the active
corpus. Out of scope: ADR-0048 acceptance and every Spec or Task status
change, which are the owner's decisions.

## Contracts

1. A Spec criterion that the Plan assigns to a current, non-cancelled Task
   must have exactly one Criterion Acceptance row in the package; a missing
   row fails. A criterion whose assigned Tasks are all historical or
   cancelled needs no row.
2. A `completed` Task or a `completed` item needs `PASS` evidence for every
   pair of its work, unless the criterion is `not-required`, and every
   criterion its Task decides for that work `accepted` or `not-required`.
3. Under generation 6 a package enters the completed archive only when its
   base revision has an approved Spec and an empty readiness predicate, and
   the preserved copy keeps every base member with its status. Superseded
   preservation keeps its own checks.
4. ADR-0048 states rules 1 to 3 and replaces only ADR-0037 decision 1, except
   its last sentence, and the completion-receipt clauses of decisions 2 and 3.

## Acceptance Criteria

1. A test fails on a missing acceptance row and passes with one row; the
   active corpus passes.
2. A test fails a `completed` item whose criterion is `pending`, and one test
   shows single-mode and multi-item Tasks judging equivalent work alike.
3. A test shows a `draft` base revision not entering the completed archive
   and an `approved`, ready one entering it.
4. Each of these rules has a passing and a failing fixture: multi-item Task
   with a frontmatter `status`, fewer than two Execution Items, items not
   covering the Task's Work Units, a Criterion Acceptance row outside the
   Plan assignment, acceptance Evidence citing another Task's row, and a
   non-`PASS` row that resolves.
5. SDLC, ADR-0048, the decisions README, AD-0030 and the Stage 02 READMEs
   state the corrected rules; an independent rules review finds nothing
   blocking.
6. The changed gate and `candidate-quality` pass.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-generation-6-reader-corrections.md)
- [SPEC-0231](../0231-task-lifecycle-generation-6/spec.md)
