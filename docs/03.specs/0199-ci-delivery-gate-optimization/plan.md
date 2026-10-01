---
title: "CI Delivery Gate Optimization Implementation Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0199-PLAN-0001"
parent_ids:
- "SPEC-0199"
created: "2026-10-01"
---

# CI Delivery Gate Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` or `superpowers:executing-plans` to
> implement this plan task by task. Steps use checkbox syntax for tracking.

**Goal:** Run repository QA once at its useful delivery boundary, retain
revision-specific security checks, and move only `main-current` after a
successful main-push audit.

**Architecture:** Keep the existing `changed` and `full` public profiles.
The PR job remains the required `validation-changed` context; a distinct
main-push job calls the existing registered Zizmor adapter and uploads SARIF,
while manual dispatch alone runs `full`. A dependent least-privilege job uses
a tested Git ref update with a lease to move `main-current`.

**Tech Stack:** GitHub Actions YAML, the existing Python gate/checker modules,
Bash/Git, Markdown and the Stage 99 registry. No new dependency.

**Spec:** [SPEC-0199](spec.md).

## Objective

Implement acceptance criteria 1-7 in the approved Spec without changing
global Git hooks, protected-main settings, service runtime or release tags.
Preserve current `validation-changed` identity and the registered full manual
audit. The approved written Spec is committed at `ba15875eb`. Its first
integration introduced it as `draft` because the Stage 99 changed-boundary
gate requires a new Spec's initial status to be draft; record subsequent
review/approved/active transitions only after a trusted base contains that
initial draft. User approval of the written Spec on 2026-10-01 is execution
planning authority, not a claim that lifecycle validation already advanced.

## Dependencies

- Reconfirm exact main/origin/main and protected required-context read-back
  before delivery. The 2026-10-01 observation was `validation-changed`,
  strict=true, with no remote tag ruleset. Do not alter protection merely to
  make the new workflow pass.
- Read bootstrap/provider, REQ-0024, AD-0027, SPEC-0199 and the current Task
  before implementation. Apply the canonical CI/CD skill and task checklist.
- Keep concurrent or unrelated files untouched. The untracked
  `infra/04-data/dev-db/docker-compose.yml` observed during planning is not
  a SPEC-0199 input and must not be staged or deleted.
- No blanket script/test removal. The baseline manifest shows live consumers
  for rehearsal and QA scripts; a name or age alone is not deletion evidence.
- The actual `core.hooksPath` points outside this repository. Repository
  changes can correct the declared hooks and agent Stop route, not silently
  change that global installation.
- Real GitHub tag movement is a remote mutation. The delivery Task must bind
  user authorization to `buenhyden/hy-home.docker` and
  `refs/tags/main-current`, record before/after SHAs, and stop if that
  authorization or hosted check is absent.

### Global constraints

Write Spec, Plan and Task prose in English. Write README and Stage 05
explanatory prose in Korean. Keep one canonical verification matrix in
`.agents/governance/quality-standards.md`. Existing release tags and
`generate-changelog.yml` remain release-only. Do not add a second gate runner,
PAT, global hook mutation, workflow-level PR path filter or new service.
Every script/test removal needs a consumer, replacement and regression record.

### Review focus

1. PR body/base edit masquerades as a title-only edit: W3's test permits
   title-only fast path only when the trusted event change set is exactly title.
2. A stale main run moves the tag backward: W4's bare-remote test advances
   main before the tag action and requires a nonzero result with unchanged tag.
3. Concurrent tag movement is overwritten: W4's lease test changes the remote
   tag between read and push and requires a rejected update.
4. A failed merged-SHA scan still updates the tag: W4's workflow test proves
   the tag job depends on successful main-push security.
5. Declared hooks differ from installed hooks: W1/W5 record both observations
   and do not report global hook deployment from a tracked YAML edit.

## Execution Sequence

0. **W0 — Stage 03 lifecycle bootstrap.** After Plan approval, integrate
   the initial draft package and advance Spec/Plan status through each
   registered transition on a trusted main base before starting an active
   implementation Task.
1. **W1 — Baseline and Task evidence.** Inventory exact invocation owners,
   remote required checks, hook installation, disabled workflow registrations,
   and script/test consumers. No deletion without evidence.
2. **W2 — Local and agent boundary.** Remove expensive declared public
   pre-commit/pre-push routes and Stop's mandatory changed-profile run while
   retaining cheap unique checks and CI pre-commit recursion safety.
3. **W3 — PR required context.** Keep `validation-changed` for all PRs,
   restricting title-only edits to the git-flow check while other revisions
   run the existing changed selection.
4. **W4 — Merged security and channel tag.** Make `full` manual-only; run
   registered Zizmor/SARIF on main push and move the leased channel tag only
   after success.
5. **W5 — Canonical governance and integration.** Update policy, knowledge
   and operations surfaces, run focused/integrated checks, obtain independent
   review and hosted evidence, then complete the Spec package.

### Task 0: W0 — Stage 03 lifecycle bootstrap

**Files:** Modify only this package's `spec.md` and `plan.md` lifecycle
metadata/approval provenance; create `tasks/tsk-0001-delivery-gate-baseline.md`
only after both parents are active.

**Interfaces:** Produces a validated active Spec/Plan and a current Task for
W1-W5. It does not change CI execution behavior.

- [ ] After the user approves this written Plan and an execution method,
  deliver the initial draft Spec/Plan package through a protected PR. Record
  exact merged SHA and hosted required check.
- [ ] On a main base that contains the draft package, advance Spec
  `draft → review → approved → active` and Plan
  `draft → approved → active` without skipping registered transitions.
  Run the changed metadata check and required hosted check at each transition.
  Because the validator compares a PR to its main base, merge each
  transition before authoring its successor when the base would otherwise
  show an invalid direct jump. Do not bypass protection to shorten this.
- [ ] Create the current Task in `draft` after active parents exist and
  record approval/lifecycle receipts there. Verify the package graph and
  begin W1 only when it is valid.

### Task 1: W1 — Baseline and Task evidence

**Files:** Modify `tasks/tsk-0001-delivery-gate-baseline.md`; inspect
`.github/workflows/`, `.github/workflow-contract.yml`,
`scripts/manifest.yaml`, `tests/` and local hook configuration read-only.

**Interfaces:** Produces an exact phase → command → revision/environment →
consumer/replacement matrix for W2-W5. The Task is the sole evidence ledger.

- [ ] Record `git rev-parse HEAD`, `git config --get core.hooksPath`,
  current branch/worktree state, required remote checks and active/disabled
  remote workflow IDs. Do not infer a hosted run from tracked YAML.
- [ ] For each apparent one-off, legacy, deprecated or duplicate file, record
  manifest lifecycle, callers, test reachability, replacement and disposition.
  Expected baseline: no justified file deletion; revise only with new evidence.
- [ ] Run `python3 scripts/validation/run-ci-gate.py --profile changed --explain`
  and `python3 scripts/validation/check-github-workflow-contract.py`;
  save selected leaves and any environment limits. Expected: both exit 0.
  Commit the Task baseline separately from implementation.

### Task 2: W2 — Local and agent boundary

**Files:** Modify `.pre-commit-config.yaml`,
`scripts/validation/run-ci-precommit.sh`,
`scripts/hooks/agent-event-hook.sh`, `.codex/hooks.json`,
`.claude/settings.json` only where their binding changes; test
`tests/validation/test_run_ci_precommit.sh`,
`tests/validation/test_hook_rules.py` and
`tests/validation/test_agent_governance_ci_routing.py`.

**Interfaces:** The CI-only pre-commit wrapper still rejects caller `SKIP`
and runs cheap hooks; Stop no longer starts `run-ci-gate.py`. W3 keeps the
hosted PR quality owner.

- [ ] Add failing tests proving no public profile is bound to declared
  pre-commit/pre-push or agent Stop, and proving cheap hooks/CI recursion
  guard remain. Run the focused tests and capture expected failures.
- [ ] Remove only `public-validation-changed` and
  `public-validation-full` hook registrations. Reconcile the wrapper's
  skip list by removing the now-obsolete skip value while still rejecting
  caller-controlled `SKIP`; CI pre-commit cannot recurse through a public
  hook that no longer exists.
- [ ] Replace Stop's mandatory full changed-profile execution with a cheap
  completion/status boundary; preserve explicit failure reporting and
  provider parity. Update the two tracked provider bindings only if their
  invoked command or timeout needs to change.
- [ ] Run `bash tests/validation/test_run_ci_precommit.sh`,
  `python3 -m unittest tests.validation.test_hook_rules
  tests.validation.test_agent_governance_ci_routing -v`, and
  `python3 scripts/validation/check-agent-governance-contract.py
  --mode repository --section providers`. Expected: all exit 0. Commit;
  do not edit `/home/hyunyoun/.codex/git-hooks`.

### Task 3: W3 — PR required context

**Files:** Modify `.github/workflows/ci-quality.yml`,
`scripts/validation/ci_gate_runner.py`,
`scripts/lib/gate/github_workflow_contract.py` and
`.github/workflow-contract.yml`; test
`tests/validation/test_ci_gate_plan.py`,
`tests/validation/test_ci_gate_execution_context.py`,
`tests/lib/gate/test_github_workflow_contract.py` and
`tests/validation/test_agent_governance_ci_routing.py`.

**Interfaces:** The existing `--profile changed` remains the one static
command in `validation-changed`. Add
`_is_title_only_edit(environ: Mapping[str, str]) -> bool` in the runner:
read a size-bounded `GITHUB_EVENT_PATH` JSON only for a GitHub PR `edited`
event, return true only when `changes` has exactly the `title` key, and
return false on missing/malformed/ambiguous input. True selects only the
registered `ci.git-flow-contract` root; false uses current changed-path
roots. Never interpolate payload values into shell or accept a caller-supplied
arbitrary root list.

- [ ] Add failing `test_title_only_edit_runs_git_flow_only`,
  `test_ambiguous_edit_runs_changed_profile`, and workflow trigger/filter
  cases for open/synchronize/reopen. Assert that the required job remains
  eligible for all PRs. A stale or missing hosted status is verified at W5,
  not simulated as a local success. Capture the expected failures.
- [ ] Pass the trusted event action/change-set to the runner, admit the
  title-only route, and keep `validation-changed` as the required job on
  every PR to main. Update the focused checker without weakening its
  checkout, SHA, permission or event checks.
- [ ] Run `python3 -m unittest tests.validation.test_ci_gate_plan
  tests.validation.test_ci_gate_execution_context
  tests.lib.gate.test_github_workflow_contract -v` and
  `python3 scripts/validation/check-github-workflow-contract.py`.
  Expected: all exit 0. Commit before W4, preserving the same required
  check name.

### Task 4: W4 — Merged security and channel tag

**Files:** Modify `.github/workflows/ci-quality.yml`,
`.github/workflow-contract.yml` and
`scripts/lib/gate/github_workflow_contract.py`; create
`scripts/operations/update-main-current-tag.sh` and
`tests/validation/test_update_main_current_tag.sh`; register the reusable
script and test in `scripts/manifest.yaml`. Update the focused workflow
tests. The existing `scripts/lib/gate/ci_gate_adapters.py` owns the
`run-zizmor-sarif` action; reuse it unchanged unless a focused failure
proves a gap.

**Interfaces:** `validation-full` executes `--profile full` only for
`workflow_dispatch`. Main push executes
`python3 scripts/lib/gate/ci_gate_adapters.py run-zizmor-sarif` and uploads
`results.sarif`. A dependent tag job with `contents: write` invokes the
tag script with `GITHUB_SHA`, `GITHUB_REF=refs/heads/main` and the
checkout's authenticated `origin`. The script accepts no tag name argument;
it touches only lightweight `refs/tags/main-current`.

- [ ] Add a failing bare-remote shell test for absent tag, already-current
  tag, stale main, concurrent tag movement, annotated-tag refusal and
  failed remote update. Assert unchanged release tag in every case.
- [ ] Add failing workflow tests for main-push/manual separation, registered
  Zizmor command and SARIF upload, tag `needs`/event guard, job-scoped token
  permissions, and a skipped/failed audit leaving the tag job ineligible.
- [ ] Implement the script using `git ls-remote` plus a
  `--force-with-lease=refs/tags/main-current:<expected>` update. Recheck
  remote main immediately before the push; refuse stale SHA, malformed
  inputs or annotated channel tag. Do not force-push main or a release tag.
- [ ] Route push/manual jobs and their static commands in the existing
  workflow contract and checker. Run the focused tests, shell syntax,
  `python3 scripts/validation/check-github-workflow-contract.py`,
  `python3 scripts/validation/check-script-manifest.py` and
  `bash tests/validation/test_update_main_current_tag.sh`; commit. Expected:
  all exit 0. If the manifest entrypoint differs, use the registered command
  from `scripts/manifest.yaml` rather than a parallel validator.

### Task 5: W5 — Canonical governance and integrated delivery

**Files:** Modify `.agents/governance/quality-standards.md`,
`.agents/governance/github-governance.md`,
`.agents/governance/git-workflow.md`,
`.agents/knowledge/verification-surface-map.md`,
`.github/repository-surface.md`,
`docs/05.operations/runbooks/0009-release-management.md` and applicable
`scripts/README.md` or `tests/validation/README.md` only when instructions
actually change. Update this Plan/Tasks and Spec lifecycle through allowed
Stage 99 transitions.

**Interfaces:** One policy matrix owns phase selection; the knowledge map
routes to it. The runbook explains channel-tag failure/retry separately from
release-tag readiness. No new policy copy or second inventory.

- [ ] Write policy and navigation changes in their required languages,
  including a conditional channel-tag exception, old/new SHA evidence,
  stale-run recovery and the global-hook limitation.
- [ ] Run focused hook/gate/workflow tests, document metadata/link/language
  checks, `python3 scripts/validation/run-ci-gate.py --profile changed`,
  and an explicit `full` audit if the final approved Task calls for it.
  Record local-only and CI-only results separately.
- [ ] Obtain independent read-only review of the exact diff; fix high
  findings. Deliver through the protected PR after required hosted
  `validation-changed` passes; observe main-push security and tag result.
  No direct main push or protection bypass.
- [ ] In the current Task, map each SPEC-0199 acceptance criterion to W0-W5,
  actual check output, durable owner and any unverified result. Complete
  Plan, Task and Spec only after all required results pass; leave open
  otherwise. Sync local main to observed origin/main and clean only this
  task's branch/worktree when authorized and safe.

## Risk and Rollback

The main risk is losing a required check through event/filter drift. Keep
`validation-changed` stable, test edited/base-change routing, and revert the
workflow commit if hosted checks become absent or pending. If main-push
security fails, fix the source and rerun against current main; do not move
the tag manually. If tag movement fails, preserve the old pointer and retry
the idempotent job after inspecting main and tag SHAs. A tag rollback changes
only `main-current` to the recorded prior SHA and needs its own exact remote
authorization. Revert repository commits for local hook/policy regressions;
the out-of-repo global hook remains untouched. Do not delete disabled
remote workflow registrations in this package without separate explicit
remote-state review.

## Verification

| Spec criterion | Work unit | Exact proof |
| --- | --- | --- |
| 1. Phase matrix and installed-hook boundary | W0, W1, W5 | Task invocation/consumer matrix; `git config --get core.hooksPath`; governance diff review |
| 2. No routine local public gate | W2 | `bash tests/validation/test_run_ci_precommit.sh`; hook-rule and routing unit tests |
| 3. Required PR context and edited routing | W3, W5 | gate plan/execution-context/workflow unit tests; hosted `validation-changed` on exact PR SHA |
| 4. Narrow main push and retained manual full | W4, W5 | workflow checker and tests; local `full` command; hosted manual dispatch only if separately authorized |
| 5. Safe `main-current` movement | W4, W5 | bare-remote tag test; successful main-push run; remote tag/main SHA read-back |
| 6. Evidence-based script/test disposition | W1, W4 | Task consumer inventory; script manifest and test reachability checks |
| 7. Policy, docs and actual delivery | W5 | metadata/link/language checks, independent review, hosted run URLs and Task receipt |

Manual `full` proves the retained audit route but does not stand in for
real GitHub events. The hosted PR and main-push run URLs, exact SHAs,
SARIF upload and tag read-back are required acceptance evidence; a local
simulator cannot claim those outcomes. Do not repeat a passing full gate
merely because another stage occurred unless source or environment
changed materially.

## Rulings

The approved design selected a mutable non-release `main-current` tag.
The minimal main-push route reuses the already registered Zizmor adapter
directly instead of adding a third public profile or another gate runner.
The initial script/test audit found no deletion candidate with a proven
replacement; W1 may change that finding only with specific consumer and
regression evidence. The user selected native same-session implementation with one
independent whole-branch reviewer on 2026-10-02; W2-W4 share the workflow
contract and runner interfaces.
