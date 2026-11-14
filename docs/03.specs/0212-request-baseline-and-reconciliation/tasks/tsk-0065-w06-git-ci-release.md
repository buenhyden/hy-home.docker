---
title: "v14.7 W06 Git, CI and Release Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-14"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0065"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-14"
---

# v14.7 W06 Git, CI and Release Task

## Scope

### Objective and Parent

#### Objective

Own W126/criterion 121, the v14.7 W06 run for this workspace: bind each Git
action stage to a real trigger, run the leaves W05 handed off in hosted CI
without a skipped job reading as a pass, keep one commit grammar, release
producer and review path, and record a verdict and owner for every W06
requirement and carry-forward key.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [W05 validator alignment](tsk-0064-w05-validator-alignment.md)

### Inputs and Authority

The owner's request of 2026-11-14 runs the W06 prompt of the v14.7 revision
package (`_workspace/workspace_execution_tasks_v14_7_revision_20261113_r1/`,
read as reference data). Its named residue for this workspace is the stage QA
cells, the runner timeout cause, and the remote branch protection read-back.
W00 to W05 are completed and accepted; this run did not repeat them.

The same day the owner approved commit, push, pull request and merge for the
W06 changes, asked for each remote-settings change to be presented before it
is applied, and chose: allow Git's automatic merge subjects in the commit
grammar; split the long candidate work into its own CI job; enable
`sha_pinning_required` and immutable releases, and leave required signatures
and required reviews as they are.

## Execution Log

### Work Performed

#### W06 run 2026-11-14

Start check: `/home/hyunyoun/data/hy-home.docker` is the Git top level, on
`main` at `abe66a156` equal to `origin/main`, with a clean index and worktree
and no stash. Four read-only investigations covered the remote GitHub state,
the local hooks and commit grammar, the runner timeout and CI wiring, and the
signing gate, review path and carry-forward keys.

Remote state, read back on 2026-11-14 with GET calls only: merge commits are
the only merge method; `main` protection has `strict=true`, the single
required check `candidate-quality` from GitHub Actions app 15368, zero
required approvals, `enforce_admins=true` and `required_signatures` disabled;
rulesets are empty and no merge queue is used; workflows run on
`ubuntu-latest`, use no `pull_request_target` or `workflow_run`, are pinned by
SHA and default to `read` permissions; `publish-release.yml` through
`release.py` is the only tag and release producer; no Dependabot or Renovate
configuration file exists in `.github/`, and Renovate (`renovate.json5`,
POL-0086) is the dependency updater with `automerge: false`. The live
`0.0.1` release predates the current producer and was not touched.

Remote changes, at the owner's direction with before and after read-back:
`actions/permissions` `sha_pinning_required` false to true, and
`immutable-releases` disabled to enabled. Branch protection was not changed.
The 2026-11-14 entry in `.github/rulesets/main-protection.md` records both and
their rollbacks.

The twelve Git action cells are bound in the
[Git workflow policy](../../../../.agents/governance/git-workflow.md) section 7.
No `post-commit` or `post-push` hook exists, so those cells observe or do not
apply; the client hooks are bypassable, so only the branch protection rows
are enforcement.

#### Stage bindings

SDLC phases, bound to their existing owners; no check was invented.

| ID | Guarantee | Owner | Action | Reason |
| --- | --- | --- | --- | --- |
| SDLC-REQUIREMENT | Stable IDs and decidable criteria | `sdlc.md` Stage 01; `leaf.repo-document-metadata` | REUSE | The candidate selects it when `docs/01.requirements/` changes |
| SDLC-ARCHITECTURE | Decision effect and lineage | `sdlc.md` Stage 02; corpus lifecycle check | REUSE | Same path selection |
| SDLC-SPEC | Spec, Plan and Task chain | corpus lifecycle check; candidate preflight | RUN | Local route before submission, candidate in CI |
| SDLC-PLAN | Writer and verification mapping | `sdlc.md` Start event; review | OBSERVE | No machine check; review only |
| SDLC-IMPLEMENTATION | RED and GREEN, actual diff | candidate shards and `candidate-quality` | RUN | Pull request candidate |
| SDLC-VERIFICATION | A PASS kept apart from acceptance | `sdlc.md` Verify and Accept; Task evidence | OBSERVE | Acceptance is the owner's act |
| SDLC-PROMOTION | Receipt and consumer check | `sdlc.md` Promote; readiness report | REUSE | The merged tree equals the checked candidate |
| SDLC-RETIREMENT | Safe disposal | `sdlc.md` Retire; corpus lifecycle check | RUN | Staged shape only; the removal review stays manual |
| SDLC-OPERATIONS | Real environment | `leaf.operations-catalog`, compose validation | RUN (static); NOT_RUN (runtime) | No operating environment is touched by W06 |

Document Stages.

| ID | Path | Leaf | Action | Reason |
| --- | --- | --- | --- | --- |
| DOC-S00 | `.agents/` | agent governance contract; provider surface drift | RUN | `.agents/` path rule; no `docs/00` exists |
| DOC-S01 | `docs/01.requirements/` | `leaf.repo-document-metadata` | RUN | Document contract rule |
| DOC-S02 | `docs/02.architecture/` | same, and the corpus lifecycle check | RUN | Same rule |
| DOC-S03 | `docs/03.specs/` | corpus lifecycle check; candidate preflight | RUN | Same rule |
| DOC-S05 | `docs/05.operations/` | `leaf.operations-catalog` | RUN | Operations path rule |
| DOC-S90 | `docs/90.references/` | `leaf.repo-document-metadata` | RUN; freshness GAP | No leaf checks that a generated reference snapshot is current; the scan is dated and not hand-edited |
| DOC-S98 | `docs/98.archive/` | `leaf.repo-document-metadata` | REUSE | Checked on change only; no whole-corpus recheck |
| DOC-S99 | `docs/99.templates/` | document governance library and metadata tests | RUN | Selected by the document governance path rules |
| DOC-DOMAINS | Vault, content, site | none | N/A | None of these directories exist here |

Execution contract per Git action cell. Unless a row says otherwise: the
rules version is the file at the candidate SHA (`.pre-commit-config.yaml`,
`.cz.toml`, `.github/workflow-contract.yml`); the tools are Python 3.14.8,
uv and Actions pinned by SHA, and `pre-commit` hook `rev:` pins; the hosted
evidence is the gate evidence artifact, kept 14 days.

| Cell | Trigger and input | SHAs | Runner | Entrypoint | Action | Invalidation | Failure | Evidence | Approval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Commit before | agent route; index tree | HEAD, index tree | local | `run-ci-precommit.sh --mode local-staged` | RUN | index change | non-zero exit, no commit | Task | none |
| Commit during | `git commit`; index and message file | HEAD, index | local, bypassable | installed `pre-commit` and `commit-msg` | RUN | `--no-verify` | blocks the commit | terminal | none |
| Commit after | no hook | n/a | n/a | n/a | NOT_APPLICABLE | n/a | n/a | n/a | n/a |
| Push before | `git push`; refs on stdin | remote old, local new | local, bypassable | `pre-push-guard.sh` | RUN | hook not installed | refuses `refs/heads/main` | stderr | none |
| Push during | server ref update | old, new | hosted | branch protection | OBSERVE | settings change | server refuses | read-back | owner |
| Push after | `push` on `main` | parent, `GITHUB_SHA` | hosted | `main-security` | OBSERVE | next push | reports only | security evidence artifact | `security-events: write` |
| PR before | none | n/a | n/a | n/a | NOT_APPLICABLE | n/a | n/a | n/a | opening a PR is a remote write |
| PR during | `pull_request`; merge ref | base, head, merge `GITHUB_SHA` | hosted, `contents: read` | candidate shards, then the `candidate-quality` aggregate | RUN | new push or base move | fails closed | per-shard evidence artifact | none |
| PR after | job end; evidence files | as PR during | hosted | `actions/upload-artifact` | OBSERVE | rerun | missing artifact | same | none |
| Merge before | merge attempt; required check | strict up to date | hosted | branch protection | RUN (server) | base move | blocks | check status | owner |
| Merge during | merge commit; no `merge_group` | n/a | n/a | n/a | NOT_APPLICABLE | n/a | n/a | n/a | a queue needs approval |
| Merge after | `push` on `main`; merged SHA | candidate tree | hosted | `main-security` | REUSE | n/a | reports only | security evidence artifact | as Push after |

Required counterexamples: partial stage, newline and leading-space filenames,
a one-parent commit with a merge subject, PR parents differing from base and
head, skipped or zero-test leaves, cancellation, toolchain drift, YAML `on`
spellings, permission co-mutation and tracked worktree drift each have a test
(this run's branches add the ones they name in Evidence). The aggregate over
shard conclusions, `merge_group` without approval, other-run artifacts,
deleting `main` or a first push at the pre-push guard, and the absence of a
`post-commit` hook are added by this run's CI and hook units. The latest
base move is held by strict branch protection and is recorded as a server
observation.

#### Handoff Verdicts

| ID | Source | Verdict | Action and owner |
| --- | --- | --- | --- |
| QA-12 hook responsibilities | W06 prompt | DELTA | `pre-commit` checks the index and `commit-msg` the message file; installed-hook, filename and uninstalled-hook tests in this run |
| QA-13 workflow events and inputs | W06 prompt | PASS (observed) | Events, permissions, runner and checkout read back above; no privileged event runs PR code |
| QA-14 single producer per guarantee | W06 prompt, TSK-0064 crosswalk | DELTA | Shard jobs keep one producer per leaf; the aggregate is the one required context |
| QA-C09 required gate and trust | W06 prompt | DELTA | The aggregate fails on a skipped, cancelled or missing shard |
| GIT-01 branch roles | W06 prompt | PASS | `main` only; no `dev`; protection read back |
| GIT-02 work base | W06 prompt | PASS | Each unit branched from current `origin/main` in its own worktree; no user change reverted |
| GIT-03 one commit grammar | W06 prompt | DELTA | `.cz.toml` owns the grammar for both consumers; Git automatic merge subjects allowed on the owner's choice; PR titles are not commit subjects under merge-commit-only, so no title check |
| GIT-04 single tag and release producer | W06 prompt | DELTA | `release.py` is the only producer; this run adds the downgrade refusal |
| GIT-05 CHANGELOG ownership | W06 prompt | PASS | Main release-preparation PRs own `CHANGELOG.md`; no dev branch exists |
| GIT-06 immutable release order | W06 prompt | PASS | Draft, assets, verify, publish in `release.py`; immutable releases enabled on the owner's choice |
| GIT-07 dependency PR privilege | W06 prompt | PASS | Renovate only, `automerge: false`, no `pull_request_target` |
| GIT-08 personal-signature gate (D-19) | W06 prompt | PASS (none exists) | No code, hook or policy requires a signed commit or tag for acceptance; stated explicitly in `github-governance.md` section 2 |
| GIT-09, SUP-10 single-person review | W06 prompt | DELTA | Review path names its risk owners, diff checklist and explicit acceptance; no model-inference API, including self-hosted or proxied |
| R147-14 dev/main template | W06 prompt | N/A | No `dev` branch or template generator; it belongs to Project-Template |
| WP-27 workflows, runners, protection | LEGACY-208 | DELTA | Closed by the read-back and stage cells here |
| WP-28 build and verification profile | LEGACY-208 | DELTA | Source QA is not deploy acceptance (`quality-standards.md`); the runner timeout is OPEN-14 |
| WP-29 hooks and commit grammar | LEGACY-208 | DELTA | QA-12 and GIT-03 here |
| WP-30 branches, tags, release, CHANGELOG | LEGACY-208 | DELTA | GIT-04 to GIT-06 here |
| WP-45 single-person non-API review | LEGACY-208 | DELTA | GIT-09 here; its "record the operator's signed acceptance" clause is superseded by D-19 |
| WP-49 Dependabot PR trust | LEGACY-208 | RETIRED_ALIAS | Renovate under POL-0086 is the updater; Dependabot security updates are off |
| OPEN-13 required check vs GitHub allowed states | W06 prompt | DELTA | Aggregate added here; GitHub still accepts a skipped required check, so the aggregate, not a shard, is required |
| OPEN-14 runner exit 124 | TSK-0040 | DELTA | See OPEN-14 diagnosis |

#### OPEN-14 diagnosis

TSK-0040 recorded exit 124 for the candidate preflight leaf in a local-only
run of 528 s. The runner returns 124 only when a leaf exceeds its own
`timeout_seconds` (`ci_gate_runner.py`), and that leaf's budget is 900 s, so
a budget expiry inside a 528 s run is not possible. Run alone on 2026-11-14
at `abe66a156`, `check-candidate-preflight.sh` exited 0 in 182 s. The record
is therefore likely misattributed or its duration is the run total; the run's
evidence directory, which holds each leaf's end time and reason, would settle
it and was not available here. The proven timeouts are separate: the metadata
and document-library leaves exceeded their older 600 s and 900 s budgets
(SPEC-0204 TSK-0011), now 30 and 45 minutes, and the 45-minute library leaf
no longer fits the 30-minute candidate job, which the shard split fixes.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0065 | draft | ready | #w06-run-2026-11-14 |
| SPEC-0212-TSK-0065 | ready | in-progress | #w06-run-2026-11-14 |

### Blockers and Decisions

- Required signatures and required reviews stay off by the owner's choice of
  2026-11-14; the read-back records them.
- No Dependabot configuration is added: Renovate is the single updater.
- DOC-S90 snapshot freshness has no checker: the generated reference data
  under `docs/90.references/data/` is dated and regenerated by its own
  producer. Owner: W11 adoption review, which decides whether a freshness
  leaf is worth adding.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Remote read-back | 121 | W126 | remote-observation | GET `repos`, `branches/main/protection`, `rulesets`, `rules/branches/main`, `actions/permissions`, `immutable-releases` on 2026-11-14 | PASS | Values recorded under W06 run 2026-11-14; no call refused | required | - |
| Remote settings change | 121 | W126 | remote-mutation | PUT `actions/permissions` with `sha_pinning_required=true`; PUT `immutable-releases`, at the owner's direction | PASS | Before `false`/`enabled:false`; after `true`/`enabled:true` | required | - |
| Preflight timing | 121 | W126 | timing-baseline | `bash scripts/validation/check-candidate-preflight.sh` at `abe66a156`, Python 3.12.3, run alone | PASS | exit 0 in 182 s; budget 900 s | optional | - |
| Hooks and grammar | 121 | W126 | remote-candidate | PR #1005: merge-prefix grammar, one-parent merge-prefix rejection in `check-commit-range`, `--check-hooks`, release downgrade refusal; tests written RED first | PASS | `candidate-quality` success; merged as `bf81ab106`; two MEDIUM security findings fixed before merge | required | - |
| Shard split local | 121 | W126 | unit-tests | `feat/w06-ci-split` gate, workflow-contract, release and supply-chain suites, Python 3.12.3 | PASS | 204 tests OK before the main merge, 169 OK after; review PASS with M1–M3 fixed | required | - |

### Resolution Links

None yet.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 121 | pending | - | The W06 units are in progress | SPEC-0212 TSK-0065 |

### Remaining Conditions

The shard split, the hook and grammar unit and this record land through their
own pull requests; then the owner's acceptance. Q-07 runs only after W11.

## Handoff

### Promotion Receipt

None yet: the targets change in this run's pull requests.

### Next Owner

The current owner is @buenhyden; this Task continues the W06 run.
