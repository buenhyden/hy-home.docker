---
title: "CI Delivery Gate Execution"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0199-TSK-0001"
parent_ids:
- "SPEC-0199"
- "SPEC-0199-PLAN-0001"
created: "2026-10-02"
---

# CI Delivery Gate Execution

## Objective

Execute [SPEC-0199](../spec.md) and its [Plan](../plan.md) through W0-W5: assign each heavy QA route to its useful delivery boundary, preserve the required PR context, audit the merged revision, and advance only the `main-current` channel tag after successful main-push security checks.

## Inputs

The user approved the written Spec, Plan, same-session implementation, and independent final review on 2026-10-02. The user explicitly authorized protected PR delivery for `buenhyden/hy-home.docker` from `codex/spec-0199-execution`, including push, hosted validation, and merge. Release tags, global Git hooks, and remote workflow registrations remain outside this authorization. The active parent package was integrated through protected PRs [#330](https://github.com/buenhyden/hy-home.docker/pull/330), [#331](https://github.com/buenhyden/hy-home.docker/pull/331), [#332](https://github.com/buenhyden/hy-home.docker/pull/332), and [#333](https://github.com/buenhyden/hy-home.docker/pull/333); each required `validation-changed` check passed before merge. The active baseline main commit is `2d0d571ae276487810f071995c77ab8559e30a53`.

## Work Log

- W0: The Spec advanced draft → review → approved → active and the Plan advanced draft → approved → active on trusted main bases. The active Spec's requirement child references were qualified after the first #333 hosted check exposed an active-only regression; the corrected run passed.
- W1 baseline at `eabf04245c76010fd1bbfeff9790e3570100f7c0`: this isolated worktree was clean on `codex/spec-0199-execution`, two local commits ahead of its remote branch. `origin/main` was `2d0d571ae276487810f071995c77ab8559e30a53`; the original checkout remained on `codex/ci-qa-dedup` and was untouched. The installed `core.hooksPath` was `/home/hyunyoun/.codex/git-hooks` (outside this repository). Its pre-commit scans added lines for high-signal secrets; its pre-push reported no supported checks for this repository. These observations do not prove the tracked pre-commit declaration is installed.
- W1 remote read-back: main requires `validation-changed` from GitHub Actions app 15368 with `strict=true`. Active workflow IDs: Dependabot Updates 222509952, CodeQL 223086017, PR Labeler 227337751, Stale 227337752, Release Changelog 237914540, CI Quality Gates 237982135, Greeting 237994187, and Dependency Graph 282786058. IDs 350504656 (`governance-audit-tools.yml`) and 350527175 (`governance-apply-candidate.yml`) are disabled remote registrations with no tracked workflow file; no remote deletion is authorized. Remote tags contain only release tag `0.0.1` at `cb1343c8cb9c4872c24f82a0963f163909abc524`; `main-current` is absent.

| Phase | Baseline command and owner | Revision or environment | W2-W5 disposition |
| --- | --- | --- | --- |
| Commit | Installed ECC pre-commit secret scan; declared `.pre-commit-config.yaml` also binds `public-validation-changed` to `run-ci-gate.py --profile changed` | Local staged bytes; declared hook is not installed here | Keep unique secret/format/message checks; remove the declared duplicate public gate in W2 |
| Feature push | Installed ECC pre-push has no supported checks here; declared pre-push binds `public-validation-full` | Local branch tip; declared hook is not installed here | Remove declared full gate in W2; focused checks remain explicit |
| Agent Stop | Both provider bindings call `agent-event-hook.sh Stop`, which runs changed after dirty Git status with a 540-second budget | Local working tree, often the same edits checked earlier | Remove the automatic changed run in W2; keep cheap status and completion diagnostics |
| PR to main | `validation-changed` calls `run-ci-gate.py --profile changed` for opened, synchronized, reopened, and edited PRs; title-only edits still run the full changed selection | Hosted candidate SHA and main comparison base; required strict context | Keep required name and changed-profile revision gate for title edits as well |
| Main push | `validation-full` calls `run-ci-gate.py --profile full` and uploads Zizmor SARIF | Hosted merged SHA; repeats PR-owned QA suites | Replace routine full with registered Zizmor/SARIF security job in W4 |
| Manual dispatch | `validation-full` calls `run-ci-gate.py --profile full` and uploads SARIF | Explicit selected ref | Retain deliberate full audit in W4 |
| Other hosted security | CodeQL default setup and external GitGuardian run independently | Their hosted revision and service context | Retain as distinct external observations |
| Main tag | No `main-current` updater; release tag `0.0.1` exists | Remote refs | Add leased channel update only after successful main-push security in W4 |

The script manifest has 76 entries, all `active`, `retain`, and without a successor; none is marked deprecated or retired. The apparent one-off, legacy, and duplicate candidates below have live reachability. A script/test name or an old regression fixture is not removal evidence.

| Candidate | Live consumers and regression reachability | Replacement and disposition |
| --- | --- | --- |
| `.agents/evaluations/run-agent-output-eval-fixtures.sh` | Gate adapter plus `test_agent_output_eval_fixtures.py` and entrypoint tests | No replacement; retain active fixture runner |
| `scripts/operations/rehearse-postgres-logical-upgrade.sh` | Workflow contract, PostgreSQL rehearsal runbook, `test_postgres_logical_upgrade_rehearsal.py` via `leaf.supply-chain-fixture-policy` | No replacement; retain active config-only and opt-in rehearsal |
| `scripts/operations/rehearse-sample-service-delivery.sh` | Release runbook and `test_sample_service_delivery_rehearsal.py` via `leaf.supply-chain-fixture-policy` | No replacement; retain opt-in rehearsal |
| `scripts/security/verify-sample-service-supply-chain.sh` | Release runbook, Grype seed and wrapper tests | No replacement; retain supply-chain check |
| `scripts/validation/check-template-security-baseline.sh` | Workflow contract and Compose baseline regressions | No replacement; retain security baseline |
| `scripts/validation/run-ci-precommit.sh` and `test_run_ci_precommit.sh` | `leaf.pre-commit` and `leaf.ci-precommit-regressions` | Retain wrapper and tests; remove only stale public-hook skip IDs in W2 |
| `scripts/validation/check-github-workflow-contract.py` and `test_github_workflow_contract.py` | Registered checker and `leaf.workflow-contract-regressions`; checker validates current YAML, tests validate mutations | Complementary, not duplicates; retain |
| `scripts/validation/run-ci-gate.py`, `ci_gate_runner.py`, and gate plan tests | Public CLI wraps a registered runner; runner tests are reached by `leaf.ci-gate-runner-regressions` | No replacement; retain the single public runner |
| `test_agent_governance_ci_routing.py` and `test_hook_rules.py` | `leaf.repo-contracts-control-plane-regressions` and `leaf.local-hook-rule-tests` guard provider routing and rule evaluation | Retain; update obsolete Stop assertions in W2 |
| Declared public hooks and Stop changed gate | Same profile repeats before the PR gate, with no distinct installed result | Invocation removal in W2; retained PR context is the replacement owner |

W1 command evidence: `run-ci-gate.py --profile changed --explain` exited 0 and selected seven repository-integrity validators (`check-script-manifest.py`, `check-github-workflow-contract.py`, `check-quickwin-baseline.sh`, `check-storybook-contract.sh`, `check-supply-chain-policy.py`, `check-conftest-policy.sh`, and `check-template-security-baseline.sh`). This local snapshot selects the fallback suite because the branch has no uncommitted paths; it is not a hosted PR run. `check-github-workflow-contract.py` exited 0 (`workflows=5`, `jobs=7`, `actions=8`). W2-W5 remain pending at the W1 baseline.

- W2 RED: `test_run_ci_precommit.sh` failed because the wrapper still supplied obsolete public-hook `SKIP` values. Three focused routing tests failed because declared public hooks and Stop's changed-profile/timeout path still existed; these failures were observed before implementation.
- W2 GREEN: removed only two declared `public-validation-*` hook registrations; the CI wrapper now rejects caller `SKIP` and invokes cheap pre-commit hooks without its own skip list. Both provider Stop paths still inspect Git status, report parse/status errors, enforce the logical-commit boundary, and honor deferred paths, but never start `run-ci-gate.py`. Provider commands and registered timeouts did not change, so no generated provider binding was edited.
- W2 final checks: wrapper contract PASS; 131 hook, routing, deferred-path, and workflow regression tests PASS; provider contract PASS (`failures=0`); script manifest and workflow contract PASS; Bash syntax, cached pinned Ruff 0.15.12 check/format, and ShellCheck 0.11.0 PASS. The external `core.hooksPath` remained untouched. The tracked declaration affects future installations, not the observed global hook.
- W2 test disposition: `test_precommit_selector_admits_every_contract_changed_prefix` was the only deleted test. Its precondition (two public pre-commit profile hooks) no longer exists after W2, so its selector parity assertion became false by design. `test_public_hooks_are_absent_and_cheap_hooks_remain`, the existing gate path-selection tests, and `test_public_gate_surfaces_do_not_copy_atomic_commands` provide the replacement assertions. No script file was deleted.

- W3 RED: the title-only route and trusted `PR_ACTION` projection failed focused tests before implementation. W3 GREEN: the runner admits a bounded, regular, unambiguous GitHub `edited` event with only `changes.title` and selects the registered git-flow root; malformed or mixed edits take the existing changed route. The required `validation-changed` job name, PR triggers and static command remain unchanged. 85 gate-plan, execution-context and workflow-contract tests passed, and the workflow checker passed (`workflows=5`, `jobs=7`, `actions=8`).
- W3 test-output incident: an initial failing mock assertion serialized the inherited process environment into a local tool transcript. The test now clears inherited environment values and uses nonserializing call-count assertions. No credential values were added to tracked files. GitHub, Hugging Face and Vault/OpenBao credentials present in that process environment should be rotated by their owners; transcript retention and rotation are external to this repository change.

- W4 RED: the bare-remote tag test failed before the updater existed. W4 GREEN: `validation-full` is manual-only; the main-push `main-security` job runs the registered Zizmor adapter and uploads SARIF, and `update-main-current` depends on its success with job-scoped `contents: write`. A bare-remote test passed creation, idempotence, stale-main refusal, annotated-tag refusal, failed remote push, concurrent tag lease rejection, and release-tag preservation. 136 combined gate, routing and workflow tests passed; the workflow checker passed (`workflows=5`, `jobs=9`, `actions=8`); manifest, shell syntax, ShellCheck, Ruff and active-document metadata checks passed. Hosted main-push execution and remote tag movement remain unobserved until protected merge.

- W5 independent-review correction: the first title-only optimization could let an `edited` run cancel a pending `synchronize` run and satisfy the same required status with only git-flow. The fast path and `PR_ACTION` projection were removed. A focused regression now proves even a title-only `edited` payload executes changed-path collection plus git-flow and document gates. The review also found a new runbook heading forbidden by the changed-body contract; the content was retained under the existing Overview and `check-changed --base-ref origin/main` passed with zero violations. The initial 85-test W3 result describes the superseded candidate, not the final route.

- W5 local integration: the first broad `changed` run reached the OIDC entrypoint tests and failed only because two unrelated checkout files had local mode `775` under umask `002`, although Git records both as `100755`. Resetting those two worktree permissions to `755` changed no tracked bytes or Git mode; both failing tests then passed. The second broad run exposed an existing gate-model test that assumed every workflow job calls the public gate; it now checks the two jobs that actually do, and the 91 focused gate/workflow tests pass. A third broad run reached the final manifest regressions and found that the new tag updater was omitted from the test support table of known runtime-mutating scripts. The table now identifies it as `runtime`, and the focused failing test passes. The final broad changed run passed (exit 0) on `b566c8f65`; the mode correction was local environment repair.

- W5 protected delivery: PR [#334](https://github.com/buenhyden/hy-home.docker/pull/334) first failed its required check only because its title started with a lowercase word after `ci:`. The corrected title passed the local git-flow adapter and hosted `validation-changed` on head `b566c8f656f6f5e32f566917a4ef5b8af967bcb6` (run [36931132251](https://github.com/buenhyden/hy-home.docker/actions/runs/36931132251)). The protected merge produced `18c96231a0410ef1a605a664adf7621669ea6e0e` on main. Main-push run [36933310788](https://github.com/buenhyden/hy-home.docker/actions/runs/36933310788) passed `main-security`, including SARIF upload, then passed `update-main-current`. The tag receipt was `old=<absent> new=18c96231a0410ef1a605a664adf7621669ea6e0e`; remote main and `main-current` matched, and release tag `0.0.1` stayed at `cb1343c8cb9c4872c24f82a0963f163909abc524`. Task ready and in-progress transitions then passed protected PRs [#335](https://github.com/buenhyden/hy-home.docker/pull/335) and [#336](https://github.com/buenhyden/hy-home.docker/pull/336), merged as `09b011a5080c51efe44fe2b812db82be676f9a06` and `5152dc3d50eced317b5b516834ce02af79ef3f5b`. Main-push security and channel-tag jobs succeeded after the ready transition; the terminal Spec, Plan and Task candidate is recorded below.

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: phase matrix, installed-hook boundary, remote required context, workflow inventory and consumer evidence recorded | [Quality standards](../../../../.agents/governance/quality-standards.md) |
| 2 | W2 | PASS: declared public hooks and agent Stop duplicate removed; wrapper, provider and 131 routing regressions passed | [Quality standards](../../../../.agents/governance/quality-standards.md) |
| 3 | W3 | PASS: required PR identity and edited-event changed selection retained; PR #334 run 36931132251 passed on b566c8f65 | [Workflow contract](../../../../.github/workflow-contract.yml) |
| 4 | W4 | PASS: manual full remains separate; merged-SHA run 36933310788 passed registered Zizmor audit and SARIF upload without full QA | [Quality workflow](../../../../.github/workflows/ci-quality.yml) |
| 5 | W4 | PASS: bare-remote safety tests passed; main-current moved from absent to merge SHA 18c96231a after security success, release tag unchanged | [Release runbook](../../../05.operations/runbooks/0009-release-management.md) |
| 6 | W1 | PASS: 76 original active manifest entries reviewed, one obsolete selector test removed with replacement, no script deletion justified | [Script manifest](../../../../scripts/manifest.yaml) |
| 7 | W5 | PASS: policies and operations guidance aligned; local changed gate, independent review, protected PR and merged-main checks passed | [Quality standards](../../../../.agents/governance/quality-standards.md) |

## Review Evidence

Independent read-only review found two blocking issues: a forbidden runbook heading and the unsafe title-only shortcut under the required PR context. Both were corrected in W5; changed-document metadata and the edited-event regression passed. The same independent reviewer re-reviewed the corrected diff and found no remaining merge blocker. The workflow checker also rejects extra execution-control keys on the main security and tag jobs, including `continue-on-error`; its mutation test passed.

## Commit Ledger

The W0 parent package is integrated at `2d0d571ae276487810f071995c77ab8559e30a53`. W1 baseline started at `eabf04245c76010fd1bbfeff9790e3570100f7c0` and was committed separately as `7f267070b`. W2 `e0d5186ea`, W3 `a84994405` (superseded title shortcut corrected in W5), W4 `371f9f3d5`, W5 `108b507f3` and `b566c8f65` were integrated by PR #334 as `18c96231a`.

## Rulings

- An active Plan requires an already active Spec, so Spec approval preceded the combined Spec/Plan activation.
- The installed `core.hooksPath` points outside this repository; tracked hook edits cannot change that installation.
- Name or age alone does not justify deleting a script or test. Each removal needs a live-consumer and replacement analysis.

## Deferred Items

Credential values inherited by an initial failing W3 test were printed into a local tool transcript. The test harness no longer serializes the environment, and no recognized credential values were found in tracked changes; credential owners should rotate the exposed GitHub, Hugging Face and Vault/OpenBao credentials and review their audit logs. Transcript retention and rotation are external to this repository package. Hosted PR/main-push checks and remote tag read-back passed as recorded above.
