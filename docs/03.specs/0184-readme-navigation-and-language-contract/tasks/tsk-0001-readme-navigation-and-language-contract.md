---
title: "README Navigation and Language Contract"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0184-TSK-0001"
parent_ids:
- "SPEC-0184"
- "SPEC-0184-PLAN-0001"
created: "2026-09-27"
---

# README Navigation and Language Contract

## Objective

Execute W1 through W14 of the [Plan](../plan.md) and record the evidence for
every acceptance criterion of [SPEC-0184](../spec.md).

## Inputs

- The owner request of 2026-09-27. It decomposes the work into P1 (this
  package), P2 (non-README language migration), and P3 (script and
  dead-code cleanup).
- The README inventory at baseline `f30b168e2`:
  - 186 tracked READMEs: 116 active, 65 frozen, 2 generated, 3 under
    `tests/` and `_workspace/`.
  - 36 folder routers, 11 of which link documents below a child.
- The contract audit:
  - No language or navigation field exists.
  - The `indexes` and `template_catalog` checks require enumeration.
  - `archive.py` parses the README catalog byte-exact.
- Audit findings that route to other owners: SPEC-0183 and ADR-0043 are
  implemented but still `draft` and `proposed`, and SPEC-0179 and ADR-0037
  are stalled. They are not changed by this package.

## Work Log

- 2026-09-27: The owner approved the three-package decomposition, approach A,
  and the written Spec at `4b2f2ca9e` ("승인"). Plan drafted for review.
- 2026-09-27: The branch keeps Spec, Plan, and Task at `draft`. The metadata
  gate requires a document that is new against `main` to start at `draft`, and
  this request authorizes no push or merge. The owner approvals are recorded
  here with their revisions. The `review`, `approved`, and `active` promotions
  happen when the branch is integrated, the way SPEC-0182 moved through
  `280c33263`, `e229ec9d0`, and `7efc375d4`.

## Verification Evidence

Not started.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | NOT_RUN | `docs/99.templates/registry.json` |
| 2 | W2, W13 | NOT_RUN | `.agents/governance/documentation-protocol.md` |
| 3 | W1, W3, W13 | NOT_RUN | `.agents/governance/documentation-protocol.md` |
| 4 | W6 | NOT_RUN | `docs/98.archive/retention-catalog.md` |
| 5 | W4 | NOT_RUN | `docs/03.specs/README.md` |
| 6 | W5 | NOT_RUN | `docs/99.templates/registry.json` |
| 7 | W7 | NOT_RUN | `.agents/governance/documentation-protocol.md` |
| 8 | W8, W9, W10, W11, W12 | NOT_RUN | each README |
| 9 | W13 | NOT_RUN | N/A: gate evidence only |

## Review Evidence

None yet.

## Commit Ledger

- `4b2f2ca9e` docs(specs): Add SPEC-0184 and ADR-0044 for README navigation
  and language.

## Rulings

None yet.

## Deferred Items

- P2: non-README language migration and full language enforcement.
- P3: dead `load_artifact_contract`, the foundation-wave branch in
  `lifecycle/contract.py`, and any transitional base read added in W6.
