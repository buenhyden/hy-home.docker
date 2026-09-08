---
title: "Governance and QA Surface Convergence Implementation Plan"
version: "0.6.2"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-09-09"
layer: "specs"
artifact_id: "SPEC-0173-PLAN-0001"
parent_ids:
- "SPEC-0173"
created: "2026-09-05"
---

# Governance and QA Surface Convergence Implementation Plan

## Objective

Implement the 2026-09-08 local convergence authorized in [the Spec](spec.md),
using the registered execution workflow with independent review.
Task 0006 owns inventory, decisions, commands, results, reviews, and commits.
The existing W1-W6 migration is implemented; its dated evidence is preserved.

## Dependencies

- Current Requirements/Architecture: REQ-0024, REQ-0026, AD-0027, AD-0030,
  accepted ADR-0032 and ADR-0033. Preservation-owner promotion is already done.
- Existing six-suite DAG and public changed/full commands, script inventory,
  Stage 99 registry, both schemas, templates, parsers, and tests.
- A clean linked worktree from fetched main, explicit task ownership, installed
  repository dependencies, read-only policy review and independent diff review.
- No remote writes, service operations, real secrets, global installation,
  history rewriting, or arbitrary hook skips. Follow the current Task's
  branch/worktree preservation decision; option A authorizes no integration.

## Execution Sequence

1. W1: Preserve the reviewed authority decision and provenance.
2. W2: Preserve implemented canonical/provider contracts and static evidence.
3. W3: Preserve document, gate and test ownership contracts and acceptance mappings.
4. W4: Preserve bootstrap, hook, evaluation and CI routing; separate live evidence.
5. W5: Preserve source cutover, generated outputs and archive dispositions.
6. W6: Reconcile post-integration evidence without promoting blocked acceptance.
7. W7: Reconcile current documentation, policy and template consumers.
8. W8: Repair changed-path selection and optional frontend impact routing.
9. W9: Unify formatting ownership and executable commit contracts.
10. W10: Remove redundant workflow execution and finalize verified local evidence.
11. W11: Repair native edit payload translation and narrow project permissions.
12. W12: Correct the approved option A ownership and execution guidance.
13. W13: Preserve prepared tools in the post-edit hook.
14. W14: Reuse the audit generator's validated pack and refresh its output.
15. W15: Record reviewed option A verification and preserve the branch.

### W1-W6: Preserve integrated migration

Retain existing role/skill identities, canonical source boundaries, gate
uniqueness, deterministic fixtures, full-package archive preservation, and
historical review evidence. Acceptance criteria 1-16 retain their original
W1-W6 mapping in Task 0006. Correct current Spec/Plan/Task navigation against
actual durable owners without rewriting frozen evidence or claiming runtime.

### W7: Reconcile documentation and policy consumers

Owner: approved documentation contributor; reviewer: read-only rules-engineer.
Files: this package, `.agents/governance/{git-workflow,github-governance,
quality-standards,sdlc}.md`, `.agents/knowledge/`, and affected prompts/template
consumers only where evidence shows a mismatch. Stage 99 registry/schemas stay
unchanged unless a real shape change is required; template guidance routes to
policy instead of repeating completion obligations.

1. Compare SDLC, registry, both schemas, templates and actual parser consumers.
2. Correct current stale claims: accepted ADR-0033, historical checkpoints,
   quality jobs versus required status, conditionally skipped jobs versus a
   workflow that never reports, and approved recovery from fresh read-back.
3. Expand existing vocabulary with QA/CI/CD, workflow/job, check/fix, fixture,
   approval/evidence, local completion and merge readiness.
4. Validate metadata, links, corpus lifecycle, registry/template regressions,
   provider renderer, and exact diff. Obtain independent policy review before
   committing this logical documentation unit.

### W8: Repair changed-path and hook selection

Owner: writable CI/CD contributor. Files: `.pre-commit-config.yaml`,
`.github/workflow-contract.yml`, `scripts/validation/ci_gate_runner.py`, existing
`scripts/lib/gate/ci_gate_contract.py`, `tests/lib/gate/test_ci_gate_contract.py`,
`tests/validation/test_ci_gate_*.py`, and related selector consumers.
Produces the same public CLI and six-suite selection, without a new wrapper.

1. Reproduce root-only omission with parsed pre-commit hook filters and the
   real public contract. In temporary Git repos exercise staged, unstaged,
   partial, add/delete/rename, spaces, empty, initial and missing/shallow bases.
2. Make public hooks reach every changed path; let the public contract select
   suites. Add root tool/commit inputs to sufficient contract impact rules.
   A cross-owner rename must include source and destination influence.
3. Preserve local working-tree union semantics. Automatic pre-commit sees index
   content for tracked files plus visible untracked files; it does not prove a
   pure index snapshot. Reject unresolved hosted bases instead of local fallback.
   Keep optional frontend roots behind explicit contract impact rules. Known
   documentation changes omit unrelated browser/build work; shared inputs and
   unknown paths remain conservative. Full and mandatory security roots remain.
4. Run focused selector/plan/context tests and explain representative inputs;
   compare selected leaves, uniqueness and observed execution time. Preserve
   cycle, environment, argv, descriptor and process-cleanup checks.
5. Review exact diff, stage only owned paths, and create a logical commit.

### W9: Unify formatting and commit contracts

Owner: writable CI/CD contributor with documentation scope.
Files: `.cz.toml`, `.gitmessage`, `cliff.toml`, commit policy/prompt and hook
consumers, `scripts/lib/gate/ci_gate_adapters.py`, and focused gate tests.
Consumes `.cz.toml`; produces one message/type contract shared by PR checking
and the existing commit-msg hook. No new public command or plugin is required
unless existing APIs cannot express a verified requirement.

1. Reproduce release/deps and subject/scope drift between current validators.
2. Read `.cz.toml` from the existing bounded repository-root adapter. Keep
   tool-specific parser representations only with parity for every accepted
   type, scope, breaking marker/footer, body/trailer, length and punctuation.
3. Make every authored example pass. Ensure changelog parser ordering reaches
   release suppression and breaking changes; retain automation/merge handling.
4. Inspect formatter/linter owners per actual file scope, use explicit fix only
   for touched files, and prove a second format check produces no diff.
5. Run message/PR/changelog regressions; validate each proposed commit message
   cheaply before automatic Git hooks. Review and commit the coherent unit.

### W10: Remove redundant workflow and finalize evidence

Owner: writable CI/CD contributor; independent security and code review.
Files: `.github/workflows/tech-stack-version-sync.yml`, workflow contract/checker,
`tests/lib/gate/test_github_workflow_contract.py`, tech-stack tests,
`scripts/manifest.yaml`, and directly linked policy/index/navigation.

1. Compare exact command/argv/cwd/config/input/event with the required drift leaf.
2. Delete the duplicate workflow and migrate all active consumers and parity
   tests together. Keep required leaf failures and full input coverage.
3. Validate workflow/event/action/permission contracts, shell/eval tests, public
   changed/full explain and execution where inputs permit, full Python discovery,
   generator write/check and affected package-local QA.
4. Record real remote read-back separately from local runs; do not dispatch.
   Record missing setup/network/container inputs honestly and continue safe work.
5. Review each logical diff and commit. Use the controlled final all-files wrapper
   only with actual tracked Task, reviewed owned prefixes, and clean linked
   worktree. Review any resulting formatter diff and verify idempotence.
6. Finish with verified status and ownership under the completion checklist.
   Use current Task authorization for local integration and cleanup. Separate
   native/hosted observations remain unverified until actually run; they are not
   additional local acceptance gates. Terminal package lifecycle follows its
   own atomic preservation procedure, not a condition added to local merging.

### W11: Repair provider edit routing

Owner: writable hook contributor; independent code/security review. Files:
existing `scripts/hooks/` consumers, a shared import-only parser under
`scripts/lib/hooks/`, `.claude/settings.json`, and focused library/hook tests.

1. Reproduce Claude absolute-path rejection and Codex decoded patch omission.
2. Share normalized edit targets and replacement text across PreToolUse policy
   and PostToolUse checks. Accept physical in-root absolute paths, preserve
   path/symlink/hardlink guards, and reject malformed or empty edit payloads.
3. Remove the two arbitrary Git/Python allow grants; retain narrow existing
   native commands. Do not add provider-local policy or another wrapper.
4. Verify multi-file Add/Update/Delete/Move, secret/path blocks, source-preserving
   check mode and Stop retry tests. Check registered projection parity; regenerate
   only if a registered source changes. Keep live delivery explicitly NOT_RUN.
5. Obtain exact diff security/code review and commit the coherent unit.

### W12-W15: Approved option A

W12 owns `.claude/provider.md`, `.github/CODEOWNERS`,
`.agents/governance/github-governance.md`, `tests/README.md`, and
`docs/02.architecture/descriptions/0030-document-lifecycle-governance.md`.
Correct the suite owner, migrated eval paths, changelog-check meaning, real
metadata base selection, and stale generator claim. Preserve the known active
operations-marker and architecture debt. Use metadata/link/workflow/provider
checks; obtain independent policy and exact diff review before a docs commit.

W13 owns `scripts/hooks/post-tool-validate.sh`,
`scripts/operations/use-qa-ci-tools.sh`, its existing entrypoint/hook regressions,
and the corresponding `scripts/README.md` guidance. Reproduce prepared Python
being replaced by a synthetic user-global binary. Separate explicit bootstrap
from automatic post-edit execution and preserve existing PATH priority. Cover
prepared tools, explicit extra paths, missing tools, repeated bootstrap, and
check-mode source preservation. Do not add a new wrapper or version registry.

W14 owns `scripts/validation/check-agentic-audit-semantic-freshness.py`,
`scripts/validation/generate-audit-implementation-matrix.sh`, their existing
audit tests, and the registered matrix output. Return the validated pack with
the semantic result and consume it once in the generator; accept no caller
supplied PASS or stale cache. First demonstrate the repeated pack validation,
then test exact-once generation plus malformed/semantic/stale-output failures.
Render current overview/candidate paths from existing path owners, regenerate
the matrix, check freshness and a second write's byte identity. Retain the
standalone validators, census and public graph; their redesign is option B.

W15 owns shared Spec/Plan/Task and manifest integration. Run focused regressions,
the applicable local public profile, generated checks and independent review.
Final all-files QA uses the existing wrapper with this tracked Task and an exact
reviewed path list in an initially clean linked worktree. Record command,
snapshot, exit and observed cost; run no hosted-only wrapper locally. Commit
only reviewed logical units through normal installed Git hooks. Keep branch
and worktree; package lifecycle remains active/in-progress.

The primary checkout was clean at branch creation and was the initial writer
because its relative hooksPath resolves the normal hooks there. Use a dedicated
declared-dependency environment without changing hooks or persistent Git configuration.
An ignored real `.env` in the primary checkout prevents public QA there under
the no-secret scope. Freeze and transfer only verified task-owned tracked
changes to the linked checkout, then restore those exact primary paths and
return primary to unchanged main. The linked checkout owns delivery. Bind its
Git operations to the complete unchanged common hooks directory with command
local `core.hooksPath`; this restores normal hooks without a persistent setting
change or skipped hook. Independent review precedes staging and commit.
Root alone updates shared package evidence and manifest. Each contributor owns
only its named files; policy/code reviewers remain read-only and independent.

## Risk and Rollback

| Risk | Guard | Recovery |
| --- | --- | --- |
| Selector omits an affected owner | Real Git snapshot and semantic suite cases | Revert reviewed selector commit |
| Commit tools disagree | Accepted/rejected message and translation matrix | Revert coherent commit-contract unit |
| Workflow removal loses detection | Required drift leaf and failure propagation regression | Restore workflow unit from Git |
| Check mutates authored source | Explicit check mode or controlled isolated validation | Review task-owned diff; never reset others |
| Static success is promoted to runtime or hosted evidence | Per-command context and target SHA in Task | Correct evidence classification |
| Archive or identity changes manufacture completion | Preserve frozen bytes and current package states | Revert only authored Task-owned changes |

## Verification

Use existing public commands and focused tests, then independent review before
logical commits. Task 0006 records exact command, context, target snapshot,
exit, result, cost when measured, approval/review source, and recovery.
Acceptance 17 maps to W8, 18 to W9, 19 to W10, and 20 to W7/W10.
Acceptance 21 maps to W11.
Acceptance 22 maps to W13, 23 to W14, and 24 to W12/W14/W15.
Domain-logic coverage is N/A for validation/configuration-only changes;
behavioral safety regressions remain mandatory for changed validators.

## Rulings

- The user's explicit approval governs in-scope implementation choices; skill
  defaults do not add a second design approval, SDLC tree, or progress ledger.
- Stage 99 retains document shapes; Task evidence retains execution states.
- Current local completion, hosted verification and merge readiness are separate.

## Related Documents

- [Specification](spec.md)
- [Task 0006](tasks/tsk-0006-generated-evidence-and-final-verification.md)
- [Stage 03 index](../README.md)
