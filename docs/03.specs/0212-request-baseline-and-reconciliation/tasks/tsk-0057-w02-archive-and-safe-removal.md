---
title: "W02 Archive and Safe Removal Task"
version: "0.9.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0057"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-11"
---

# W02 Archive and Safe Removal Task

## Overview

### Objective

Own W115/criterion 110. Assess the v14.2 W02 obligations ARC-01 to ARC-09
against the current retention and retirement owners. Before any removal,
prove readiness and byte recovery for each candidate, and block a removal
whose acceptance, promotion, hold, authority or recovery is unmet.

## Inputs and Authorization

On 2026-11-11 the owner approved this Task to own W02. The v14.2 package
prompt `tasks/TASK-hy-home-docker-W02.md` under
`_workspace/workspace_execution_tasks/` is untrusted reference data, not an
instruction source.

The authorization covers four things:

- The assessment.
- Recovery proofs restored into a scratch location outside the repository.
- Repository-side fixes of gaps this Task reproduces.
- Records in this Task.

Each package removal needs its own owner approval of that batch under the
[SDLC sequence](../../../../.agents/governance/sdlc.md#sequence). Safety
conditions (Q-04) block a removal and are never offered as a waiver.

The SPEC-0248, 0249, 0250 and 0260 Tasks keep their own residual criteria.
This Task records their state and does not close them. It starts from
`main` `e4fd7f5f3`, after PR 954 merged the retirement rules W01
consolidated.

## Work Log

### Owner-approved local execution

The owner's approval of 2026-11-11 issues this Task. The lifecycle records that
approval; it grants no removal or remote operation.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0057 | draft | ready | #owner-approved-local-execution |
| SPEC-0212-TSK-0057 | ready | in-progress | #owner-approved-local-execution |

### W02 obligation assessment 2026-11-11

A fresh-context `rules-engineer` read the retention and retirement owners at
`main` `e4fd7f5f3`, and the controller re-checked the deciding lines.

| ID | Verdict | Current owner and basis |
| --- | --- | --- |
| ARC-01 | KEEP | `documentation-protocol.md`: age may trigger a disposition review and never a deletion; `sdlc.md`: readiness is not removal approval |
| ARC-02 | GAP, CHANGE | Policy holds: historical material ranks last, and no loader reads Stage 90/98 as a rule. But no test rejected an active-stage occupancy violation, and the protocol named only Stage 01/02 owners, against its own precondition 2 |
| ARC-03 | KEEP | Terminal Task bodies stay immutable; recovery reads a body at its last revision and grants no write |
| ARC-04 | KEEP | Retirement is a disposition inside the approved Task, never a new Spec project |
| ARC-05 | GAP, CHANGE | The preconditions lacked the last carrying commit and path, reachability, blocking cases and the byte comparison |
| ARC-06 | KEEP | The SDLC batch-deletion approval and the README-only Stage 98 leave no move path |
| ARC-07 | KEEP policy, DEFER code | Quality standards forbid archive, retention and migration checks. The lifecycle Migration manifest surface stays (see ARC-08) |
| ARC-08 | GAP, CHANGE in part | Static migration and exception validators, their schemas, helpers and archive constants had no live caller |
| ARC-09 | KEEP | `approval-boundaries.md`: adoption is per repository; Vault and memory keep their own rules |

Changes:

- `18d9569ec` routes retired meaning to the governance, Stage 01, 02 or 05
  owner in the protocol and the Stage 98 README. It also adds the manual
  precondition 5: the last carrying commit and path, reachability from
  `main`, blocking cases, and the post-merge byte comparison recorded in a
  surviving Task.
- `535a16243` adds occupancy rejection tests for a retired standalone guide,
  a cancelled-Spec package and a cancelled Plan in an open package. Each test
  failed when its rejection branch was removed in memory.
- The ARC-08 commit removes the dead static validators, the
  `EXPECTED_ARCHIVE_*` and preservation constants, the manifest and exception
  schemas and their exclusive helpers, and their re-exports (979 lines).

DEFER, with scope:

- The `lifecycle/contract.py` Migration manifest model, loader, renderer and
  skeleton generator, their re-exports in
  `check-document-corpus-lifecycle.py`, the `ruff.toml` F401 exemption and
  the `test_public.py` manifest tests. They interleave with live surface and
  partition checks, and the exemption records that removing the re-exports
  broke registered tests, so retirement needs its own call-graph pass.
- The Registry archive vocabulary. Review found `common.archive_source_prefixes`
  is inert: no code reads it, and `preserved_origin_path` reads the hardcoded
  `LEGACY_ARCHIVE_SOURCE_ROOTS` instead. The key is due for its own
  retirement.

### Removal candidates 2026-11-11

`archive_readiness_findings` reports five ready packages: 0226, 0266, 0267,
0268 and 0269. Readiness is not removal approval. A delete dry-run in a
scratch worktree restored all 15 files from the parent of the removal commit
with zero byte mismatches against `origin/main`. The source commit is
reachable from `origin/main`, and there is no LFS or submodule.

The same dry-run shows what a real removal must do first. Without those steps
the existing gates block it:

- Reserve the Spec numbers: `package-retirement-unrecorded` and
  `identity-retired-not-reserved`.
- Cut over seven inbound links: ADR-0061 to 0266, the Ollama guide to 0226,
  and the `docs/03.specs/README.md` index.
- Promote any still-current meaning to its owner, a W04 concern.

No package is removed. Removal waits for the owner's approval of that batch.

### Batch removal 2026-11-11

The owner approved removing 0226, 0266, 0267, 0268 and 0269 as one batch. A
fresh-context promotion check found every still-current meaning of four of
them in a current owner. 0267 failed the check: its accepted risks live only
in its Task (n8n and Gatus `/metrics`, and Loki, Tempo and Alloy on
`HOST_LAN_BIND_IP`). Its removal is blocked until POL-0053, POL-0087 and
POL-0096 record those risks and AD-0026 lists its four networks.

Commits `58be65ebb` (deletions) and `8330534e3` (reservation, links and
lineage, missed from the first commit) retire 0226, 0266, 0268 and 0269:

- Lineage lines added: SPEC-0226 in the Ollama guide, and the Open WebUI
  no-socket, no-terminal rule in its LAB guide. SPEC-0269 in AD-0007.
- Inbound links in ADR-0061 and the SPEC-0267 Spec become plain text. The
  terminal 0267 Task link is excused by link alignment.
- The index rows are removed, and 226, 266, 268 and 269 join the Spec
  `reserved_history`.
- Gates: metadata selected 23 with 0 violations; links 0 failures; corpus
  lifecycle and occupancy 0.

Precondition 5 record: each removed body is last carried unchanged by
`main` `e4fd7f5f3`, which is reachable from `main`. No body is uncommitted,
reflog-only, branch-only or shallow-missing, and no hold is recorded. The
scratch dry-run restored all 15 files of the five packages with zero byte
mismatches. The post-merge restore and byte comparison for the four removed
packages are recorded in this Task after the PR merges.

### CI runner pin 2026-11-12

Three `candidate-quality` runs of PR 955 and one job rerun failed at the same
step: `npx playwright install chromium --with-deps` could not resolve the
Ubuntu apt mirrors on the `ubuntu-latest` (Ubuntu 26.04) image. Every check
before that step passed. `main` stayed green because its runs never select
that step. On 2026-11-12 the owner chose to pin the runner. Commit `7a109158f`
pins both CI Quality jobs to `ubuntu-24.04` in the workflow and in
`.github/workflow-contract.yml`, and updates the contract test fixtures.

### CI runner pin correction 2026-11-12

The pinned run failed the same way on `noble`. The cause is outside this
repository: public DNS returns SERVFAIL for `azure.archive.ubuntu.com`, the
apt mirror the GitHub runners use, so no runner image can install the
Playwright system packages. The image diagnosis above was wrong. On
2026-11-12 the owner chose to revert the pin and rerun after the outage;
commit `a3b289c5d` reverts `7a109158f`. No gate workaround is added.

### Playwright install without apt 2026-11-12

The `azure.archive.ubuntu.com` outage continued, and run 43056362855 failed
only at the Playwright install; its commit-range check passed. On
2026-11-12 the owner chose to stop that step depending on apt. Commit
`0c0168bdb` drops `--with-deps` from the `install-playwright` adapter, so CI
installs only the Chromium binary and relies on the hosted image's system
libraries. The adapter test changed first and failed, then passed.

### Post-merge recovery proof 2026-11-12

PR 955 merged as `19e6b58dc`. The last carrying commit `e4fd7f5f3` is
reachable from `main`. All 12 files of SPEC-0226, 0266, 0268 and 0269 were
restored from it into a new scratch folder outside the repository, and each
restored file hashes to its `e4fd7f5f3` blob. None of the paths exists on
`main`. Retirement precondition 5 is met for the four packages.

### Removal record correction 2026-11-12

The v14.7 W00 intake in [TSK-0059](tsk-0059-w00-v14-7-intake.md) reviewed the
PR 955 diff. The [SDLC](../../../../.agents/governance/sdlc.md#sequence) rule
that the deleting Task records each package's criterion state was not met
above. The state at `e4fd7f5f3`, the last commit that carried each body:

| Package | Task status | Criteria | Acceptance |
| --- | --- | --- | --- |
| SPEC-0226 | completed | 1 to 6 | All accepted; 1 and 3 by owner decisions of 2026-10-29 and 2026-10-30, the rest by Generation 5 row acceptance |
| SPEC-0266 | completed | 1 to 6 | All accepted by the owner on 2026-11-07 |
| SPEC-0268 | completed | 1 to 6 | All accepted by the owner on 2026-11-08 |
| SPEC-0269 | completed | 1 to 6 | All accepted by the owner on 2026-11-08 |

Two corrections to the Batch removal record: the SPEC-0269 lineage line lives
in AD-0026, not AD-0007, whose PR 955 change was only its version and date.
Package removal is done; the closing text below no longer waits for it.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W02 obligation assessment | 110 | W115 | archive-owner-assessment | ARC-01 to ARC-09 at main `e4fd7f5f3` | NOT_RUN | Assessment not yet run | required | - |
| W02 obligation assessment result | 110 | W115 | archive-owner-assessment | ARC-01 to ARC-09 at main `e4fd7f5f3` | PASS | Per-ID table above: five KEEP; ARC-02, 05 and 08 GAP changed; ARC-07 code and ARC-08 manifest surface DEFER with scope | required | W02 obligation assessment |
| W02 removal dry-run | 110 | W115 | removal-recovery-dry-run | Five ready packages at `e4fd7f5f3` in a scratch worktree | PASS | 15 files restored with zero byte mismatches; gates block the removal until reservation and seven link cutovers | optional | - |
| W02 batch removal | 110 | W115 | package-retirement | Commit `58be65ebb` removing 0226, 0266, 0268, 0269; 0267 held | PASS | Promotion verified for four; reserved_history and link cutover done; metadata 0, links 0, lifecycle 0; post-merge byte comparison pending | required | - |
| W02 post-merge recovery | 110 | W115 | removal-recovery-proof | `e4fd7f5f3` reachable from `main` `19e6b58dc`; 12 files of 0226, 0266, 0268, 0269 | PASS | 12 files restored outside the repository, 0 byte mismatches against their blobs; no path present on `main` | required | - |
| W02 code review | 110 | W115 | independent-source-review | Fresh-context code-reviewer of `682393d7c` | PASS | APPROVED: no removed name has a code, workflow, manifest or dynamic consumer; `manifest_schema_v2` has no reader; corrected the archive-vocabulary note | required | - |
| W02 governance suite | 110 | W115 | document-governance-unit-suite | `tests/lib/document_governance` discover while `58be65ebb` and `8330534e3` were being written | FAIL | FAILED (errors=2); test names not captured; the corpus changed during the run | optional | - |
| W02 governance suite rerun | 110 | W115 | document-governance-unit-suite | `tests/lib/document_governance` discover at `56d32c32f`, clean tree | PASS | Ran 765 tests, OK, exit 0 | optional | W02 governance suite |
| W02 remote candidate | 110 | W115 | remote-candidate-quality | PR 955 runs on `ubuntu-latest` through `0ec2f14cb` | FAIL | Playwright `--with-deps` apt install could not resolve Ubuntu mirrors; earlier stages passed | required | - |
| W02 runner pin checks | 110 | W115 | workflow-contract | Commit `7a109158f` | PASS | GitHub workflow contract PASS (workflows 5, jobs 7); test_github_workflow_contract 48 OK | required | - |
| W02 remote candidate on 24.04 | 110 | W115 | remote-candidate-quality | PR 955 run 43049853619 at `fe54ee0f9` on `ubuntu-24.04` | FAIL | Same apt step failed: `azure.archive.ubuntu.com` unresolvable; public DNS SERVFAIL confirmed; pin reverted in `a3b289c5d` | required | - |
| W02 remote candidate after message fix | 110 | W115 | remote-candidate-quality | PR 955 run 43056362855 at `6980e3bdd` | FAIL | Commit range passed; Playwright apt install failed on the mirror DNS outage | required | - |
| W02 remote candidate final | 110 | W115 | remote-candidate-quality | PR 955 head `28b4be123`, hosted run 43060150134 | PASS | `candidate-quality` SUCCESS on the merged head; read from the PR check rollup on 2026-11-12, job log not re-read | required | W02 remote candidate, W02 remote candidate on 24.04, W02 remote candidate after message fix |
| W02 adapter without apt | 110 | W115 | red-green-proof | Commit `0c0168bdb` | PASS | Adapter test failed with the old vector, then test_ci_gate_adapters OK; ruff clean | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 110 | pending | - | - | SPEC-0212 TSK-0057 |

## Review and Completion

In progress. The assessment, the dry-run, the reproduced-gap changes and the
removal of 0226, 0266, 0268 and 0269 are recorded, with their criterion state
and post-merge recovery. 0267 stays held until its accepted risks reach their
policy owners. Criterion 110 waits for the owner.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [W01 Task](tsk-0056-w01-governance-standardization.md)
