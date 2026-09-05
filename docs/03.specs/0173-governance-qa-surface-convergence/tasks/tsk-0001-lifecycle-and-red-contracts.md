---
title: "Lifecycle Reconciliation and RED Contracts Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0173-TSK-0001"
parent_ids:
- "SPEC-0173"
- "SPEC-0173-PLAN-0001"
created: "2026-09-05"
identity_recovery_decisions:
- source_commit: "db21aebf079fcc4e867779861b49c2283b7f8f01"
  source_path: "docs/90.references/research/0085-workspace-engineering-main-baseline-assessment/REQUEST-SCOPE.md"
  source_artifact_id: "RES-0085-SCOPE"
  target_path: "docs/90.references/research/0085-workspace-engineering-main-baseline-assessment/m0001-request-scope.md"
  target_artifact_id: "RES-0085-m0001"
  disposition: "consolidated"
---

# Lifecycle Reconciliation and RED Contracts Task

## Objective

Reconcile the completed SPEC-0172 outcome with the current document-lifecycle
contract, then establish failing tests for the ownership and residue boundaries
that SPEC-0173 will change.

## Inputs

- [SPEC-0173](../spec.md) and its [implementation plan](../plan.md).
- The current SPEC-0172 package, Stage 03 index, Stage 98 catalog, registry,
  lifecycle validator, and Git recovery rules.
- The baseline invocation, script, test, fixture, document, and provider
  findings recorded in the Plan.

## Work Log

### Baseline and activation

- Work runs in the isolated
  `codex/0173-governance-qa-surface-convergence` worktree from
  `main@71da6654e2fa3def174b238ad309c92fe46e9dae`.
- The first clean-baseline full profile exposed stale generated DATA-0076 and
  DATA-0082 after the planning package was added. The owning LLM Wiki generator
  refreshed only those outputs; its check and the rerun full profile passed.
- SPEC-0173 advanced through separate review, approval, and activation commits.
  An attempted active Plan with only an approved Spec was rejected, so the
  valid sequence keeps the Plan approved until the Spec becomes active.

### SPEC-0172 lifecycle and RED evidence

- The index/status regression first failed because SPEC-0172 was `draft` while
  the Stage 03 row claimed `active`. The test was made generic across every
  current Spec and passed after the lifecycle advanced through review,
  approval, and activation in separate commits.
- A standalone terminal tree with completed Spec, Plan, and Task was rejected
  by three `active-stage-occupancy` findings. The Plan was corrected so Spec
  completion, archive preservation, and transient-body removal form one atomic
  result tree rather than an invalid intermediate commit.
- At active-state commit
  `10e0d016fd83763db477c3d4375eb6a3e8daad1e`, `git ls-tree` and
  `git cat-file -e` proved the Plan and Task as regular blobs. Their exact blob
  IDs are `0d92744d3beae1db8438eea7942aebe80bf6b7ce` and
  `2a5778517aa8e84013d8c0ed2fc70671dfc9ecff`.
- The first independent policy review found that the Task still owned exact
  Hosted, provider, runtime, remote-protection, and RES-0085 recovery evidence.
  The durable outcome was written into the completed Spec, current protection
  and research consumers were cut over, and the reciprocal RES-0085 recovery
  decision moved to this Task before deletion.
- REQ-0026, AD-0030, ADR-0031, Stage 00, Stage 03, Stage 98, the Registry, and
  the executable lifecycle description now agree: completed Spec owns the
  durable outcome; a Plan or Task without a current consumer is transient and
  must remain exactly recoverable from Git.
- RES-0002, RES-0084, and RES-0085 were not merged. They respectively own the
  current workspace baseline, GitHub Actions mechanics, and the dated request
  boundary/recovery record, so the user's conditional same-purpose criterion
  is not met.

## Verification Evidence

| Check | Result |
| --- | --- |
| Initial full baseline | First run failed only on stale DATA-0076/DATA-0082; owner regeneration and unchanged-contract rerun passed, exit 0 |
| Index/status RED | Failed on SPEC-0172 draft-versus-active drift before lifecycle transition |
| SPEC-0172 forward transitions | review, approved, and active commits each passed changed metadata, corpus lifecycle, Spec-package tests, and diff check |
| Transient recovery | `git ls-tree`, two `git cat-file -e` checks, and exact blob IDs above passed at `10e0d016` |
| Spec package contracts | 24 tests passed, including Spec-only completion preservation and all-current-index status parity |
| Archive and identity history | 25 archive tests and 19 identity-history tests passed |
| Lifecycle entrypoints | 15 tests passed |
| Changed metadata | Final heading-corrected check selected 18 paths with 0 violations, 0 legacy exceptions, and 0 transition overrides |
| Corpus lifecycle and recovery | 0 lifecycle violations; 3 migrations, 104 tombstones, 141 preserved paths, 250 decisions, 338 recovery rows, 0 recovery violations |
| Document links | 689 documents, 5,759 links, 0 failures |
| LLM Wiki freshness | both generated outputs fresh |
| Whitespace | `git diff --check`, exit 0 |
| Controlled all-files candidate | First exact-tree run failed because Ruff rewrote one comprehension in `test_spec_packages.py`; changed paths 1, unexpected paths 0. Second run exposed MD001. The initial h2 correction conflicted with the Plan body contract, so constraints now belong to `Objective` and `Related Documents` is restored as h2. Tree `b112999b` passed all-files before the metadata correction; the preservation commit procedure validates its final exact tree again |

The formatter and heading corrections are applied. The final full profile
belongs to Task 6 after all Tasks change the same aggregate surfaces.

## Review Evidence

The first independent rules-engineer review returned `BLOCKED` with no P0 and
three P1 findings: incomplete current-consumer cutover, conflicting
preservation authorities, and stale Task evidence. It also identified weak
status/prose-only tests. The correction transfers exact evidence to durable
owners, aligns REQ/AD/ADR/Stage 00/03/98 and executable prose, exercises
Spec-only preservation with a Plan and Task present, and validates every
current index status. After the Plan heading was placed under the registered
`Objective` section, the final independent re-review reproduced metadata,
Spec-package, link, diff, consumer, and blob checks and returned `PASS` with no
P0, P1, P2, or P3 finding.

## Commit Ledger

| Commit | Scope |
| --- | --- |
| `726e5e2d` | Refresh planning-package generated indexes after the baseline freshness failure |
| `03968b23`, `5f15a01e`, `69375b24` | Advance SPEC-0173 through review, approval, and activation |
| `2aa6a40c`, `d9d03685`, `10e0d016` | Advance SPEC-0172 through review, approval, and activation without skipping lifecycle edges |

The atomic preservation and Task-completion commit SHAs are recorded after
those commits exist; this Task does not predict its own commit identity.

## Rulings

- Preserve the completed SPEC-0172 Spec as durable evidence under the Stage 98
  route required by the current policy.
- Treat the Plan and Task bodies as transient artifacts recoverable from
  Git; do not create archive copies that compete with the completed Spec.
- Correct the stale Stage 00 preservation sentence so Stage 00, the current
  Stage 03 index, and the Registry agree on transient Plan/Task removal.
- Add RED contracts before changing gate, script, test, fixture, document, or
  provider behavior.

## Deferred Items

- Hosted execution, remote control-plane mutation, provider entitlement,
  deployment, release, push, pull request, and merge are outside this Task.
- The final full gate, Task 6 review, and branch-finish decision occur only
  after Tasks 2-6 complete. This Task's pre-completion all-files wrapper runs
  against an exact clean candidate tree before the preservation commit.

## Related Documents

- [SPEC-0173 package](../spec.md)
- [SPEC-0173 implementation plan](../plan.md)
- [Stage 03 index](../../README.md)
