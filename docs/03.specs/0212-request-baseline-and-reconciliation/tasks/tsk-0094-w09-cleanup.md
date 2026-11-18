---
title: "W09 Cleanup Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-19"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0094"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-19"
---

# W09 Cleanup Task

## Scope

### Objective and Parent

Own criterion 150 and work unit W166 under the [Spec](../spec.md) and
[Plan](../plan.md). Bring cleanup to the 4.2.0 W09-CLEANUP design with D14,
D06 and D07: the canonical commands and checks run without the 4.2.0
package or any staging content, durable stores stay apart from scratch, and
only owner-approved one-off material is removed.

### Inputs and Authority

The direct 2026-11-19 request runs W09-CLEANUP from the git-ignored 4.2.0
package. On 2026-11-19 the owner approved deleting one exact leftover
folder. D14 removes the package itself only after acceptance, in
Q07-CUTOVER, and later prompts (W11-ACCEPT, Q07-CUTOVER and the others not
yet run) still read it, so it stays.

## Execution Log

### Work Performed

#### Survey on 2026-11-19

No tracked runtime file names the 4.2.0 package; its name appears only in
historical Task evidence and the glossary. `_workspace/` is the declared
staging surface: Git tracks its seven contract READMEs and ignores the
rest. Its untracked content and owners:

| Path | Owner and use | Disposition |
| --- | --- | --- |
| `workspace_governance_4_2_0_20261116/` (2.1 MiB) | Package input for the remaining prompts | Keep until Q07 |
| `repo-support/task-2026-07-23-…/grype-db-seed` (3.2 GiB) | Grype database cache that `verify-sample-service-supply-chain.sh` reads and `seed-grype-db-cache.sh` writes | Keep: regenerable, but a costly download |
| `repo-support/analysis/` (98 MiB) | Workspace inventory output and the p07 plans and selections that `compose_start.py` and `compose_observation.py` read | Keep |
| `repo-support/hermes-report-source-2026-11-06/` | Hermes report sources, written on 2026-11-19 | Keep: in use |
| `repo-support/{openbao,valkey}-native-evidence/` | Native evidence; `infra/09-platform-ops/security-updates/verification.json` names the OpenBao index | Keep |
| `diagnostics/` | Diagnostic staging | Keep |
| `.w07-posttooluse-a4dcc45e4b7b/` | Unrecorded W07 PostToolUse probe: one 3-byte README, no reference, not open, no symlink | Deleted on approval |

The other staging defaults in scripts are output folders the scripts
create on their next run, as the staging contract allows, so they are
kept. Durable state lives outside `_workspace/`: the capture, analysis,
forecast and dispatch stores in the ignored `.workspace-capture/` and the
shared memory in the ignored `.workspace-memory/` (R46). The four dispatch
runs left no worktree and stay as W10-PARALLEL evidence. No extra Git
worktree remains, and the `codex/*` branches are outside this work.

#### Clean worktree

A detached worktree of `origin/main` at `509686a49`, where `_workspace/`
held only the seven tracked READMEs, ran the canonical checks and the
memory, brief, capture, analysis, forecast, dispatch, observe and LAB
suites. The memory command reached the shared store, the observe command
reported from the stores, and the brief status refused fail-closed,
because that worktree is a different workspace with no binding. The
worktree was removed afterwards.

#### Deletion

On the owner's approval the folder `_workspace/.w07-posttooluse-a4dcc45e4b7b/`
was removed after checking that it was a directory, not a symlink, and
held only `README.md`; nothing else was touched.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0094 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0094 | ready | in-progress | #survey-on-2026-11-19 |

### Blockers and Decisions

None. The package and the staging content above are kept on purpose; the
package goes in Q07-CUTOVER after acceptance.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Package references | 150 | W166 | `git grep` for the package name and `/mnt/data` | Tracked tree at `061260311` | PASS | No runtime reference; historical Task evidence and the glossary only | required | - |
| Clean suites | 150 | W166 | 12 memory, brief, capture, analysis, forecast, dispatch, observe and LAB test modules | Clean worktree at `509686a49` | PASS | 246 tests in 39.4 s | required | - |
| Clean checks | 150 | W166 | Governance contract, script manifest, provider renderer `--check` | Clean worktree at `509686a49` | PASS | Each exit 0; renderer drift 0 | required | - |
| Clean commands | 150 | W166 | `agent_memory.py usage`, `observe.py report`, `request_brief status` | Clean worktree at `509686a49` | PASS | Memory store read, observe report in 0.071 s, brief refused fail-closed | required | - |
| Approved deletion | 150 | W166 | Directory, symlink and content checks, then `rm` and `rmdir` of the exact paths | `_workspace/.w07-posttooluse-a4dcc45e4b7b/` | PASS | Removed; `git status` unchanged | required | - |

### Resolution Links

None.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 150 | pending | Package references, Clean suites, Clean checks, Clean commands, Approved deletion | Awaits the owner's decision | @buenhyden |

### Remaining Conditions

The package is removed only in Q07-CUTOVER after acceptance.

## Handoff

### Promotion Receipt

The `_workspace` README staging contract and R46 already hold the rules;
nothing new is promoted.

### Next Owner

The owner decides criterion 150.
