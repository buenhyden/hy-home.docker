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
- 2026-09-27: The owner approved the Plan ("승인"). Execution started on branch
  `docs/readme-navigation-language-contract` from `ff5c0497f`: W1 through W7
  and W13 run directly under executing-plans, and W8 through W12 are
  dispatched to area implementers under subagent-driven development.
- Baseline, measured on `main` `f30b168e2` in a clean detached worktree:
  `tests/validation` ran 674 tests with 2 failures
  (`test_gatus_oidc`, `test_openwebui_oidc_entrypoint`, both file-permission
  checks of entrypoint scripts). `tests/lib` ran 806 tests with 1 failure
  (`test_identity_history` high-water check).
- W1: calibration of `hangul_ratio` over the tracked corpus put Korean prose
  that is dense with technical terms at 0.12 to 0.20, and mostly-English
  documents at 0.08 or below. `KO_MIN_RATIO` is 0.12 and `EN_MAX_RATIO` is
  0.02.
- The changed gate profile was run member by member, without
  `check-conftest-policy.sh`. That member runs `docker compose run` and `down`,
  which this request forbids, and `run-ci-gate.py` offers no member exclusion.
  Every other member returned 0 after W3, W4 and W5, W6, and W7.

## Verification Evidence

W1 through W7 carry red-then-green evidence recorded in the commits below.
Final gate evidence is recorded at W13.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: `ProfileLanguageTests` and `test_language` red, then green (`e18c2d8fc`) | `docs/99.templates/registry.json` |
| 2 | W2, W13 | NOT_RUN | `.agents/governance/documentation-protocol.md` |
| 3 | W1, W3, W13 | NOT_RUN | `.agents/governance/documentation-protocol.md` |
| 4 | W6 | PASS: 26 of 26 catalog lines identical after the move; archive tests 169 OK; lifecycle violations 0 (`fe050df6d`) | `docs/98.archive/retention-catalog.md` |
| 5 | W4 | PASS: the directory-route test fails on the old README (4 != 37) and passes on the new one (`cbbce9254`) | `docs/03.specs/README.md` |
| 6 | W5 | PASS: `TemplateRoutingTests` red, then green (`cbbce9254`) | `docs/99.templates/registry.json` |
| 7 | W7 | NOT_RUN | `.agents/governance/documentation-protocol.md` |
| 8 | W8, W9, W10, W11, W12 | NOT_RUN | each README |
| 9 | W13 | NOT_RUN | N/A: gate evidence only |

## Review Evidence

- W7, `rules-engineer`, read-only: 20 findings, 2 critical and 7 important.
  Both critical findings were fixed. The root README language table was
  handed to the W8 implementer, and REQ-0024-NFR-0010 was amended in W7.
  Findings 3 through 18 and 20 were fixed in W7. Finding 19, the incidents
  README, went to W9. Finding 3 was kept as written: the protocol states the
  enforcement W13 activates on this branch. Finding 12's side note, removing
  machine-shaped tables, was ruled unnecessary, because the only
  machine-header table left, the Retention Catalog, now lives in an English
  record. `.claude/output-styles/hy-home.md` is an authored native file, and
  renderer parity passed (`drift=0`).

## Commit Ledger

- `4b2f2ca9e` docs(specs): Add SPEC-0184 and ADR-0044 for README navigation
  and language.
- `ff5c0497f` docs(specs): Draft the SPEC-0184 Plan and Task for review.
- `e18c2d8fc` W1: declare document language per Registry profile.
- `6122fa0b0` W2: add the inactive navigation link check.
- `0eb6362a0` W3: enforce declared language on READMEs and changed bodies.
- `cbbce9254` W4 and W5: route the Stage 03 and template indexes by
  directory.
- `fe050df6d` W6: move the Retention Catalog into its own record.

## Rulings

- `KO_MIN_RATIO` is 0.12, not the Plan's 0.20, after corpus calibration.
- W4 and W5 share one commit, because both change `reference.py` and
  `test_reference.py`.
- The test that required status copies in the Stage 03 index was replaced by
  a directory-route test.
- W6: the base read falls back to the old README path when the record is
  absent at base, marked `ponytail:`, and P3 removes it. The catalog record
  is allowed at the Stage 98 root but not required. The new record starts
  at `draft`.
- The area implementers run in parallel on disjoint file lists and never
  touch the Git index. The controller runs the `humanize-korean` pass and
  commits each area.

## Deferred Items

- P2: non-README language migration and full language enforcement.
- P3: dead `load_artifact_contract`, the foundation-wave branch in
  `lifecycle/contract.py`, and any transitional base read added in W6.
