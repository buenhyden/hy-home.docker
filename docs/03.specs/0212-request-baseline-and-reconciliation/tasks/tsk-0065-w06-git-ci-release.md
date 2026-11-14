---
title: "v14.7 W06 Git, CI and Release Task"
version: "0.2.0"
type: "sdlc/task"
status: "completed"
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

| Cell | Stages (SDLC; DOC) | Trigger and input | SHAs | Runner | Entrypoint | Writer | Consumer | Action | Invalidation | Failure | Evidence | Approval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Commit before | SDLC-IMPLEMENTATION; changed paths' DOC stage | agent route; index tree | HEAD, index tree | local | `run-ci-precommit.sh --mode local-staged` | agent in its worktree | the commit hook | RUN | index change | non-zero exit, no commit | Task | none |
| Commit during | SDLC-IMPLEMENTATION; changed paths' DOC stage | `git commit`; index and message file | HEAD, index | local, bypassable | installed `pre-commit` and `commit-msg` | committer | Git | RUN | `--no-verify` | blocks the commit | terminal | none |
| Commit after | n/a | no hook | n/a | n/a | n/a | n/a | n/a | NOT_APPLICABLE | n/a | n/a | n/a | n/a |
| Push before | SDLC-IMPLEMENTATION; n/a | `git push`; refs on stdin | remote old, local new | local, bypassable | `pre-push-guard.sh` | pusher | Git | RUN | hook not installed | refuses `refs/heads/main` | stderr | none |
| Push during | SDLC-PROMOTION; n/a | server ref update | old, new | hosted | branch protection | owner (settings) | GitHub | OBSERVE | settings change | server refuses | read-back | owner |
| Push after | SDLC-OPERATIONS; DOC-S00 to DOC-S99 by path | `push` on `main` | parent, `GITHUB_SHA` | hosted | `main-security` | workflow run | code scanning, owner | OBSERVE | next push | reports only | security evidence artifact | `security-events: write` |
| PR before | n/a | none | n/a | n/a | n/a | n/a | n/a | NOT_APPLICABLE | n/a | n/a | n/a | opening a PR is a remote write |
| PR during | SDLC-IMPLEMENTATION, SDLC-SPEC; DOC stages by path rule | `pull_request`; merge ref | base, head, merge `GITHUB_SHA` | hosted, `contents: read` | candidate shards, then the `candidate-quality` aggregate | workflow run | aggregate, branch protection | RUN | new push or base move | fails closed | per-shard evidence artifact | none |
| PR after | SDLC-VERIFICATION; same | job end; evidence files | as PR during | hosted | `actions/upload-artifact` | workflow run | Task evidence, reviewer | OBSERVE | rerun | missing artifact | same | none |
| Merge before | SDLC-VERIFICATION; n/a | merge attempt; required check | strict up to date | hosted | branch protection | GitHub | merger | RUN (server) | base move | blocks | check status | owner |
| Merge during | n/a | merge commit; no `merge_group` | n/a | n/a | n/a | n/a | n/a | NOT_APPLICABLE | n/a | n/a | n/a | a queue needs approval |
| Merge after | SDLC-PROMOTION; DOC stages by path | `push` on `main`; merged SHA | candidate tree | hosted | `main-security` | workflow run | Task promotion receipt | REUSE | n/a | reports only | security evidence artifact | as Push after |

Required counterexamples, each mapped to a test read on 2026-11-14 (the
`tests/` prefix is omitted):

| Counterexample | Test | Source |
| --- | --- | --- |
| Partial stage | `validation/test_ci_gate_plan.py` `test_automatic_pre_commit_sees_index_content_and_untracked_paths` | existing |
| Newline and leading-space filenames | `validation/test_agent_governance_ci_routing.py` `test_installed_commit_hook_checks_index_for_awkward_filenames` | #1005 |
| First push and ref deletion | same file, `test_guard_stdin_refuses_main_deletion_and_allows_new_branch` | #1005 |
| Latest base move | none; strict branch protection refuses an out-of-date head | server observation |
| PR head, merge SHA and parents | `lib/gate/test_ci_gate_adapters.py` `test_pr_range_rejects_wrong_merge_parents_and_empty_history`; `validation/test_ci_gate_plan.py` `test_pull_request_identity_is_bound_to_raw_merge_topology` | existing |
| Skipped, neutral, cancelled, timed out, failed or missing shard | `lib/gate/test_github_workflow_contract.py` `test_aggregate_fails_unless_every_needed_job_succeeded` | shard PR |
| Skipped or zero tests in a leaf | `lib/gate/test_ci_gate_adapters.py` `test_required_unittest_gate_rejects_skipped_tests`, `test_run_unittest_rejects_zero_tests_and_missing_execution_summary` | existing |
| Another run's or revision's evidence | `lib/gate/test_ci_gate_evidence.py` `test_open_rejects_evidence_seeded_by_another_run_or_revision` | shard PR |
| Permission co-mutation | `lib/gate/test_github_workflow_contract.py` `test_required_permission_contract_co_mutations_fail_baseline` | existing |
| `merge_group` without a queue | same file, `test_merge_group_trigger_is_rejected_even_when_the_contract_lists_it` | shard PR |
| `post-commit` failure | `validation/test_agent_governance_ci_routing.py` `test_default_install_hook_types_have_no_post_commit_claim`; no hook exists to fail | #1005 |
| YAML `on` spellings | `lib/gate/test_github_workflow_contract.py` `test_mixed_yaml_on_spellings_are_rejected_as_ambiguous` | existing |
| Stale generator | `validation/test_script_manifest.py` `test_generated_checks_fail_closed_on_stale_missing_and_mutating_commands` | existing |
| Toolchain drift | `lib/gate/test_ci_gate_evidence.py` `test_other_python_version_is_rejected`; `validation/test_ci_gate_plan.py` `test_local_run_with_a_mismatched_toolchain_executes_nothing` | existing |
| One-parent commit with a merge subject | `lib/gate/test_ci_gate_adapters.py` `test_commit_range_rejects_a_single_parent_merge_prefixed_commit` | #1005 |
| Tracked worktree drift | `validation/test_ci_gate_plan.py` `test_local_evidence_head_rejects_tracked_worktree_drift` | existing |

A job's `needs` result is never `neutral` on GitHub; the case is tested so
the aggregate stays closed if a later check-run consumer reads it.

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
| SPEC-0212-TSK-0065 | in-progress | completed | #criterion-decisions |

### Blockers and Decisions

- Required signatures and required reviews stay off by the owner's choice of
  2026-11-14; the read-back records them.
- No Dependabot configuration is added: Renovate is the single updater.
- DOC-S90 snapshot freshness has no checker: the generated reference data
  under `docs/90.references/data/` is dated and regenerated by its own
  producer. Owner: W11 adoption review, which decides whether a freshness
  leaf is worth adding.
- Hosting `leaf.docs-traceability` exposed a defect already on `main`: the
  2026-11-13 service README common form linked individual Stage 05 runbooks
  and a Stage 99 template from outside `docs/`, which the
  [documentation protocol](../../../../.agents/governance/documentation-protocol.md)
  forbids. Following that requirement, the links route through folder
  READMEs instead; the check and the policy are unchanged.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Remote read-back | 121 | W126 | remote-observation | GET `repos`, `branches/main/protection`, `rulesets`, `rules/branches/main`, `actions/permissions`, `immutable-releases` on 2026-11-14 | PASS | Values recorded under W06 run 2026-11-14; no call refused | required | - |
| Remote settings change | 121 | W126 | remote-mutation | PUT `actions/permissions` with `sha_pinning_required=true`; PUT `immutable-releases`, at the owner's direction | PASS | Before `false`/`enabled:false`; after `true`/`enabled:true` | required | - |
| Preflight timing | 121 | W126 | timing-baseline | `bash scripts/validation/check-candidate-preflight.sh` at `abe66a156`, Python 3.12.3, run alone | PASS | exit 0 in 182 s; budget 900 s | optional | - |
| Hooks and grammar | 121 | W126 | remote-candidate | PR #1005: merge-prefix grammar, one-parent merge-prefix rejection in `check-commit-range`, `--check-hooks`, release downgrade refusal; tests written RED first | PASS | `candidate-quality` success; merged as `bf81ab106`; two MEDIUM security findings fixed before merge | required | - |
| Document version downgrade | 121 | W126 | remote-candidate | PR #1006: `check-document-metadata.py --mode check-changed` reports `version-downgrade` when a changed document's SemVer is lower than its base; `VersionDowngradeTests` written RED first | PASS | `candidate-quality` success in 9 min 55 s; merged as `f0b13094b`; review PASS; the SemVer parser is a private copy so `release.py` stays a standalone script | required | - |
| Counterexample map | 121 | W126 | test-inventory | Read-only search of `origin/main` and `feat/w06-ci-split` for each required counterexample | PASS | Every case maps to a named test except the latest base move, a server observation; `neutral` was added to the aggregate test | required | - |
| Shard split local | 121 | W126 | unit-tests | `feat/w06-ci-split` gate, workflow-contract, release and supply-chain suites, Python 3.12.3 | PASS | 204 tests OK before the main merge, 169 OK after; review PASS with M1–M3 fixed | required | - |
| Governance record | 121 | W126 | remote-candidate | PR #1008: governance text, Spec criterion 121, Plan W126 and this Task's bindings | PASS | `candidate-quality` success in 5 min; merged as `856bd359e` | required | - |
| Shard split hosted first run | 121 | W126 | remote-candidate | PR #1007 at `66d1daacf`, run 43545382947 | FAIL | `candidate-core` PASS in 14 min 29 s with every leaf PASS; `candidate-documents` FAIL after 4 min 9 s on `leaf.docs-traceability` (`check-document-links.py --mode all`, 64 `stage-link-outside-docs` findings in 33 READMEs outside `docs/`, the same on `main`), three later leaves NOT_RUN; the aggregate failed closed | required | - |
| Link routes | 121 | W126 | remote-candidate | PR #1009: 34 READMEs outside `docs/` route runbook and template links through folder READMEs; checker and policy unchanged | PASS | `check-document-links.py --mode all` exit 0, failures 0 (64 before); `candidate-quality` success in 13 min 6 s; merged as `737910721` | required | - |
| Shard split hosted second run | 121 | W126 | remote-candidate | PR #1007 at `df9b1f574`, run 43552961434, after #1009 | FAIL | `candidate-core` PASS in 14 min 5 s; `candidate-documents` FAIL on `leaf.local-document-metadata-tests`: `test_repository_contracts_reject_fragmented_in_progress_task_evidence` clones the detached merge-ref checkout and `git branch -M main` fails; library leaf NOT_RUN; the aggregate failed closed | required | - |
| Fixture git RED | 121 | W126 | red-green-proof | `FixtureGitTests.test_init_git_names_main_from_a_detached_clone` before the fix | FAIL | `RuntimeError: fatal: cannot rename the current branch while not on any`, the hosted error | required | - |
| Fixture git GREEN | 121 | W126 | red-green-proof | `_support.init_git` uses `git checkout -B main`; `metadata.test_reference` at `deea4dbf2` | PASS | module OK; the failing test unchanged | required | Fixture git RED |
| Shard split hosted final | 121 | W126 | remote-candidate | PR #1007 at `deea4dbf2`, run 43555699221 | PASS | `candidate-core` 16 min 10 s; `candidate-documents` 15 min 1 s with all four leaves PASS and 956 tests run (21 lifecycle, 164 metadata, 771 library), equal to the local counts; `candidate-quality` success; merged as `b38664681` | required | Shard split hosted first run, Shard split hosted second run |
| Budget RED | 121 | W126 | red-green-proof | `test_hosted_job_timeout_covers_its_leaf_budgets_in_sequence` with the leaf at 15 minutes and the job at 90 | FAIL | `100 not less than or equal to 90` | required | - |
| Budget GREEN | 121 | W126 | red-green-proof | Same test with the job at 100; `check-github-workflow-contract.py`; gate contract and plan suites | PASS | 163 tests OK; contract PASS | required | Budget RED |

### Resolution Links

Fixture git RED is resolved by Fixture git GREEN, and the Shard split hosted
first and second runs by the Shard split hosted final run. Budget RED is
resolved by Budget GREEN.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 121 | accepted | Remote read-back, Remote settings change, Hooks and grammar, Document version downgrade, Counterexample map, Governance record, Link routes, Fixture git GREEN, Shard split hosted final | Owner @buenhyden accepted on 2026-11-14 in this chat, after #1010 merged; OPEN-14, DOC-S90 freshness (W11), the latest base move and the single documents-shard measurement stay as recorded | SPEC-0212 TSK-0065 |

### Remaining Conditions

Criterion 121 is accepted and the Task is completed; every W06 unit is
merged (#1005 to #1010). State per axis: approval as the owner gave it on
2026-11-14; acceptance as in Criterion Decisions; merge as each remote
candidate row records; operation: none, since W06 changed no runtime. Limits:
OPEN-14 stays a likely misattribution because the original evidence is gone;
DOC-S90 freshness has no checker (W11); the latest base move is a server
observation, not a test; the documents shard measured 15 min 1 s against its
90-minute budget on one run only. Q-07 runs only after W11.

## Handoff

### Promotion Receipt

| Criterion | Work Unit | Task result | Target | Consumer update and check |
| --- | --- | --- | --- | --- |
| 121 | W126 | Hooks and grammar | `.cz.toml`, `ci_gate_adapters.py` commit-range check, `install-pre-push-guard.sh --check-hooks`, `release.py` downgrade refusal (merge `bf81ab106`) | `test_ci_gate_adapters`, `test_agent_governance_ci_routing`, `test_release` |
| 121 | W126 | Document version downgrade | `metadata/version.py`, `metadata/reference.py` (merge `f0b13094b`) | `metadata.test_lifecycle`; metadata check-changed |
| 121 | W126 | Governance record | `github-governance.md` 1.9.0, `agentic.md` 1.8.0, `git-workflow.md` 1.7.0, `documentation-protocol.md` 3.28.0, `main-protection.md` (merge `856bd359e`) | links alignment; metadata check-changed |
| 121 | W126 | Link routes | 34 READMEs outside `docs/` (merge `737910721`) | `check-document-links.py --mode all` in `candidate-documents` |
| 121 | W126 | Shard split hosted final, Fixture git GREEN | `ci-quality.yml` shards and aggregate, `.github/workflow-contract.yml` `hosted_jobs`, `run-ci-gate.py --job`, metadata fixture helper (merge `b38664681`) | `test_github_workflow_contract`, `test_ci_gate_contract`; required check `candidate-quality` |

### Next Owner

None: the Task is completed. The next W07 run opens its own Task; @buenhyden owns starting it.
