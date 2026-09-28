---
title: "README Navigation and Language Contract"
version: "0.2.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-09-28"
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
- W8 through W12: area implementers rewrote each README in Korean and applied
  the navigation rule. The controller reviewed each area, ran a conservative
  `humanize-korean` pass on every batch of at most about 25K characters, and
  committed the area.
- 2026-09-28: the owner merged `main` (`7d46c4e56`) into the branch at
  `fc11ae3f9` and put the W9 working state in a stash. `main` had adopted the
  Standard 3.0 Retention Catalog record independently, so the W6 move is now
  part of `main`. The W9 working tree matched the stash. Two humanize inputs
  had gone stale after the merge and were packed again before the last
  batches ran.
- The merge commit had the branch as its first parent. The Registry's merged
  allocation lineage accepts identities only through a merge whose first
  parent descends from the base. `main` reserved ADR-0044 and SPEC-0184 for
  this branch (SPEC-0185 Task, Inputs), yet `check-changed` against `main`
  reported `identity-reuse-forbidden` for `adr` and `spec`.
- 2026-09-28: on the owner's instruction, the merge was rebuilt with `main` as
  first parent (`841b47a99`, same tree as `fc11ae3f9`). The eight later commits
  were replayed onto it with identical trees. `check-changed` against `main`
  then reported 0 violations. `backup/readme-contract-pre-reparent` keeps the
  old history. The owner's stash was dropped after its commit was kept as
  `backup/stash-pre-main-integration`, because 35 of its 59 files differ from
  both HEAD and `main`.
- 2026-09-28: the owner resolved W14 M6 and M7 on this branch. The tree parser
  now reads each diagram's own indent width (`2fccbb236`). A new
  `incident-year-readme` profile lets `docs/05.operations/incidents/2026/`
  carry a Korean README that routes to its incident folders (`c781ef79f`).
  The owner chose local `main` integration for lifecycle promotion, and
  separate packages for P3 and then P2, with approval gates.

- 2026-09-28: the branch was merged into the local `main` at `72928676e`
  (not pushed). `82da63633` lets the operations catalog accept the incident
  year README beside its packets. Lifecycle promotion follows on the local
  `main`: the Spec moves through review; the Spec and Plan approvals are the
  owner's two "승인" answers of 2026-09-27; ADR-0044 is accepted, and the
  Spec, Plan, and Task are completed on the owner's instruction of
  2026-09-28 to process the drafts and ADR-0044.

## Verification Evidence

W1 through W7 carry red-then-green evidence recorded in the commits below.
Final gate evidence was recorded at W13 on 2026-09-28, after the `main` merge.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: `ProfileLanguageTests` and `test_language` red, then green (`e18c2d8fc`) | `docs/99.templates/registry.json` |
| 2 | W2, W13 | PASS: `NavigationModeTests` through `run_mode`; `--mode navigation` 964 documents, failures 0 (`8e661bc00`) | `.agents/governance/documentation-protocol.md` |
| 3 | W1, W3, W13 | PASS: `LanguageModeTests` and `DeclaredLanguageBodyTests`; `--mode language` 964 documents, failures 0 (`8e661bc00`) | `.agents/governance/documentation-protocol.md` |
| 4 | W6 | PASS: 26 of 26 catalog lines identical after the move; archive tests 169 OK; lifecycle violations 0 (`fe050df6d`) | `docs/98.archive/retention-catalog.md` |
| 5 | W4 | PASS: the directory-route test fails on the old README (4 != 37) and passes on the new one (`cbbce9254`) | `docs/03.specs/README.md` |
| 6 | W5 | PASS: `TemplateRoutingTests` red, then green (`cbbce9254`) | `docs/99.templates/registry.json` |
| 7 | W7 | PASS: hook-rule, heading, and Registry tests OK; renderer parity `drift=0` (`3774bb73d`) | `.agents/governance/documentation-protocol.md` |
| 8 | W8, W9, W10, W11, W12 | PASS: every README passes `--mode language` and `--mode navigation`; humanize gates OK or known false-positive WARN (`2c358eb51`, `37b48b702`, `acac7bd9e`, `7e3e08185`, `be949f338`) | each README |
| 9 | W13 | PARTIAL: `tests/lib` 936 OK at W13 and `tests/lib/document_governance` 736 OK after the W14 fixes; `tests/validation` 675 OK (23 skipped) before and after; links `--mode all` failures 0; every changed-profile member except `check-conftest-policy.sh` returns 0, including metadata `check-changed` after the merge was rebuilt. `check-conftest-policy.sh` was not run (blocked) | N/A: gate evidence only |

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

- W14, fresh whole-branch reviewer, read-only: 0 critical, 4 important,
  8 minor. One fix pass:
  - I1 fixed: lifecycle checks that validate an existing body (canonical
    replacement, partition Plan) no longer inherit `document-language-mismatch`.
  - I2 fixed: protocol, ADR-0044, and spec rule 3 now say that a deeper link
    from a collection README is a citation. The test name states that intent.
  - I3 fixed: the per-script purpose table in `scripts/README.md` and the
    OpenBao policy scopes are restored in Korean. Both directories hold direct
    files, so they are collection READMEs.
  - I4 fixed: a failed `git ls-files` now yields `navigation-tree-unavailable`
    instead of a silent pass.
  - M1 fixed: backticked folder labels are judged, and a label must name the
    folder it resolves to. M2 fixed: a directory that cannot be read is not a
    route. M3 fixed: frozen Stage 98 READMEs are not judged by `navigation`.
    M5 fixed: spec rule 4 matches the token stripping `language.py` does, and
    the identifier-table test fails when identifier stripping is removed.
  - M8 kept: SPEC-0179 defines the `보관 승인 대기` marker as a derived
    navigation label, not a lifecycle status.
  - M4 goes to P2. M6 and M7 were fixed afterwards at the owner's request.

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
- `3774bb73d` W7: state the document language priority and README
  navigation once.
- `b64ec0afa` W2 fix: accept a folder route to a child with no Markdown index.
- `acac7bd9e` W10: governance and provider READMEs in Korean.
- `2c358eb51` W8: repository-surface READMEs in Korean.
- `7e3e08185` W11: gateway through messaging READMEs in Korean.
- `be949f338` W12: observability through laboratory READMEs in Korean.
- `841b47a99` owner merge of `main`, rebuilt with `main` as first parent.
- `37b48b702` W9: `docs/` READMEs in Korean.
- `f977b1bff` W12 follow-up: drop the duplicate `pushgateway` token.
- `ab8e279d0` register `test_language`; pin the Korean scripts README.
- `8e661bc00` W13: activate the navigation and language link modes.
- `5aeaf6432` W14 fix: tighten the navigation and language checks.
- `5b3b489e4` W14 fix: collection README deeper links are citations.
- `9ce4304a6` W14 fix: restore the script purposes and OpenBao policy scopes.
- `2fccbb236` read navigation tree depth from each diagram's own indent.
- `c781ef79f` route the 2026 incident records through a year README.

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
- Humanize batches are at most about 25K characters, one conservative
  monolith call each, without chunking. The shim split W8 into 121 chunks.
- The Copyright and MIT footers removed from 10 `infra/04-data` READMEs stay
  removed. The dispatch asked for it, and no LICENSE file backs the claim.

## Deferred Items

- P2: non-README language migration and full language enforcement,
  including `.github/repository-surface.md`, which the `repository-readme`
  profile declares `ko` but which reads in English (W14 M4).
- P3: dead `load_artifact_contract`, the foundation-wave branch in
  `lifecycle/contract.py`, and any transitional base read added in W6.
