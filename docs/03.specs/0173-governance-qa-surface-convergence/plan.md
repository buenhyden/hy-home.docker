---
title: "Governance and QA Surface Convergence Implementation Plan"
version: "0.10.0"
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

The reviewed W16 planning delivery and its local integration are complete.
The user's subsequent instruction to inspect the Task and Plan and proceed
authorizes W17-W21 implementation in the reviewed scope. Execute W19, W18 and
W17 as separate coherent units, then W20 by domain starting with auth; W21
verification applies to each unit and the final approved result. Operations
execution planning remains on hold, including synthetic runtime rehearsals.
Task 0006 owns approval and evidence; package status is not execution approval.
The latest separate user instruction prioritizes committing the in-progress
snapshot, integrating it into local main and force-cleaning the task-owned
branch/worktrees. Task 0006 records this disposition and the remaining findings;
Git integration does not promote incomplete work units or package status.

## Dependencies

- Current Requirements/Architecture: REQ-0024, REQ-0026, AD-0027, AD-0030,
  accepted ADR-0032 and ADR-0033. Preservation-owner promotion is already done.
- Existing six-suite DAG and public changed/full commands, script inventory,
  Stage 99 registry, both schemas, templates, parsers, and tests.
- A clean linked worktree from fetched main, explicit task ownership, installed
  repository dependencies, read-only policy review and independent diff review.
- No remote writes, service operations, real secrets, global installation,
  history rewriting, or arbitrary hook skips. Preserve the implementation
  branch/worktrees; integration or cleanup requires a separate user request.

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
15. W15: Record reviewed option A verification and apply the current Task's disposition.
16. W16: Review remaining QA and document debt and author the proposed follow-up.
17. W17: Converge the legacy graph and inactive parser consumers after approval.
18. W18: Separate current corpus coverage from stable audit and recovery census.
19. W19: Remove active operations-document authoring residue after approval.
20. W20: Consolidate architecture owners by independently reviewed domain.
21. W21: Verify approved units and record local completion without runtime claims.
22. W22: Give manifest evidence one grammar and close the W17 consumer finding.
23. W23: Bound stage-document links outside `docs/` to one entry point.
24. W24: Remove CI setup that has no consumer and record the QA execution map.
25. W25: Return operations controls that restate agent governance to their owner.
26. W26: Give merge and branch-lifecycle rules a single owner.
27. W27: Run the global provider hooks and the workspace hooks together.

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
only reviewed logical units through normal installed Git hooks. Apply the
current Task's explicitly authorized local integration and cleanup after
verification; package lifecycle remains active/in-progress.

The primary checkout was clean at branch creation and was the initial writer
because its relative hooksPath resolves the normal hooks there. Use a dedicated
declared-dependency environment without changing hooks or persistent Git configuration.
An ignored real `.env` in the primary checkout prevents public QA there under
the no-secret scope. The completed transfer moved only verified task-owned
tracked changes to the linked checkout and restored those exact primary paths
at baseline main. Continue validation in the linked checkout; the current Task
owns later integration and cleanup. Bind its
Git operations to the complete unchanged common hooks directory with command
local `core.hooksPath`; this restores normal hooks without a persistent setting
change or skipped hook. Independent review precedes staging and commit.
Root alone updates shared package evidence and manifest. Each contributor owns
only its named files; policy/code reviewers remain read-only and independent.

### W16: Current planning deliverable

Owner: documentation contributor; independent reviewer: read-only rules-engineer.
Write only this Spec, Plan and Task 0006. Reuse REQ-0024-FR-0007,
REQ-0024-FR-0008, REQ-0024-NFR-0013, REQ-0026-FR-0004, REQ-0026-FR-0005,
REQ-0026-FR-0009, REQ-0026-FR-0012 and REQ-0026-NFR-0006. No schema or template
change is needed: the registered sections already hold decisions and evidence.

1. Bind the investigation to current local main and distinguish the stored
   origin/main ref from fresh hosted evidence. Inspect only safe tracked source.
2. Trace public suites, graph validation, inactive parser calls, census inputs
   and document owners. Put dated counts and the domain-pair list only in Task.
3. Compare in-place cleanup with general parser restoration, census removal and
   corpus-wide merging. Prefer existing owners, conditional removal and domain
   batches. Record the user's operations-planning hold without a runtime task.
4. Review proposed criteria 26-30 and work units for coverage and approval scope.
   Validate the three authored documents, obtain independent review and create
   one planning commit. This completed W16 work unit grants no W17-W21 authority.
   Apply the later explicit local
   integration/cleanup request only after verifying the delivered commit and
   preservation of every task-owned review copy; use fast-forward integration
   and ordinary worktree removal and merged-branch deletion.

### W17: Graph and parser cutover

Owner: writable CI/CD contributor. Root alone coordinates shared contract,
manifest and Task changes; independent code/security reviewers do not write.
Files: `.github/workflow-contract.yml`, `scripts/lib/gate/ci_gate_contract.py`,
`scripts/lib/gate/github_workflow_contract.py`, `scripts/lib/gate/ci_gate_adapters.py`,
`scripts/validation/ci_gate_runner.py`, the active
`scripts/validation/check-storybook-contract.sh` graph consumer, their existing `tests/lib/gate/` and
`tests/validation/test_ci_gate_*.py` consumers, and affected manifest/docs only.

1. Capture expanded invocation and setup plans for changed/local,
   changed/pull_request, full/local, full/push and full/workflow_dispatch using
   existing planner APIs and controlled test contexts. Do not execute hosted
   commands by spoofing CI variables. Cover docs, provider, workflow, root-only
   settings, locks/shared libraries, staged/unstaged/partial, rename/delete/add,
   spaces, empty diff, initial commit and missing/shallow base cases.
2. Trace the suite-unreachable nodes through job-root structural validation and
   all registered consumers. Migrate or remove that obsolete composition in one
   coherent contract/parser/runner/test change. Preserve required job identities,
   strict JSON parsing, active setup prerequisites and context restrictions.
3. Map skipped semantic-parser cases to active behavior owners: dynamic shell
   rejection, helper/graph cycles, symlink escape, executable mode, bounded input,
   argv/env admission and required failure propagation. Retire only the unused
   parser closure; keep active helpers and add missing negative cases first.
4. Compare before/after semantic leaf coverage and invocation multiplicity.
   The confirmed eval overlap retains the existing bounded-output adapter and
   fixture unittest leaf; remove only the direct duplicate evaluator route.
   Verify child failure, output boundaries and one effective eval call per
   selected context. Preserve the inner evaluator's existing pre-execution
   tracked-file and object-identity check using the current verifier, without
   scheduling a second evaluation. Preserve active frontend setup prerequisites when removing
   obsolete structural pins; unchanged valid plans alone do not prove malformed
   contracts still fail closed.
   Exercise workflow contract and gate library/CLI regressions. Review the exact
   diff before the graph cutover commit; no test-count or node-count target.

### W18: Census and audit consumer reconciliation

Depends on W17 only where changed graph selection affects the validation route.
Owner: writable validation contributor, with read-only preservation review.
Files: `scripts/validation/audit_criterion_contract.py`,
`check-agentic-audit-semantic-freshness.py`, `agentic-audit-semantic-contract.json`
and `generate-audit-implementation-matrix.sh` in that directory, their two audit
test modules, `tests/validation/test_workspace_governance_migration.py`, affected
canonical `docs/90.references/audits/` reports and generated DATA-0065.

1. Classify every candidate as stable criterion identity, historical recovery
   proof, current corpus rule or derived presentation. Retain historical
   migration counts/digests while they bind the preserved approved selection;
   do not substitute today's files or silently remove that evidence test.
2. Preserve the criterion manifest/schema as the independent completeness
   expectation. Replace redundant literal display-count assertions with owner
   results; keep missing/duplicate/unexpected criterion and invalid-field tests.
   Changing audit-pack membership requires a separately reviewed contract change.
3. Correct current DML-09 corpus claims and misleading legacy labels from live
   registry/path evidence. Preserve dated observations as dated evidence. Review
   semantic closure assertions against their actual current owners rather than
   adding required Task prose. Keep stale-output and unsafe-input rejection.
4. Regenerate DATA-0065 with its registered generator, check freshness and a
   second write's byte identity. Run the audit criterion/semantic tests and
   history recovery tests if their owner changes; commit source, tests and output
   together. No permanent second census registry or automatic historical rewrite.

### W19: Active authoring-residue cleanup

Owner: documentation contributor. Files: the Task-inventoried tracked Markdown
under `docs/05.operations/`, AD-0030's current risk description, and affected
metadata tests only if a behavior gap is demonstrated. The existing
`TARGET_TEMPLATE_LITERALS` contract remains the owner of forbidden target residue.

1. Derive the exact current target list with tracked-path inspection, excluding
   frozen archives and legitimate quoted examples. Inspect context before edits.
2. Remove only obsolete authoring comments. Preserve procedure commands, values,
   IDs, ownership and lifecycle; no runtime runbook is designed or executed.
3. Compare procedure content before/after and run changed metadata plus operations
   catalog/link validation. The metadata report does not generate these markers.
   Update AD-0030 only after the finding is resolved, then commit this separate
   documentation unit. Do not convert the observed file count into a gate.

### W20: Architecture consolidation

Owner: documentation contributor; each pair's current frontmatter/CODEOWNERS
owner reviews its semantic transfer (currently `@buenhyden` for the listed
Descriptions). Dependencies: implementation scope approval and the per-pair comparison, not
runtime execution. Files: the Description pairs listed in Task 0006, their
existing Requirement/ADR and Stage 05 inbound consumers, registered indexes,
AD-0030, `tests/lib/document_governance/test_taxonomy.py` and necessary Stage 98
lifecycle records. No unrelated infra changes.

1. Start with auth as a pilot, then security/data, messaging/observability,
   workflow/AI, and tooling/laboratory. Make each domain a reviewable commit;
   dependency links must resolve at each intermediate commit.
2. For each pair, map source section/obligation to destination section and mark
   duplicate, distinct, obsolete or unresolved. Compare the underlying tracked
   configuration and accepted ADR when claims conflict; preserve unresolved
   content and stop only that domain's retirement until its owner decides.
3. Merge retained design into the base Description, with procedures routed to
   existing Stage 05 owners. Correct misleading link labels as well as targets.
   Preserve stable IDs; no abbreviated requirement IDs or blanket prefix rewrite.
4. Apply registered supersession/archive/recovery after transfer and review.
   Preserve the selected source bytes and valid identity history. Update inbound
   links and indexes atomically; do not rewrite existing frozen archive bodies.
5. Use `python3 scripts/knowledge/generate-llm-wiki.py --write` only when indexed
   paths change, then `--check`. Verify metadata, all links and corpus lifecycle,
   plus relevant archive/identity regressions. Update the taxonomy test
   `AD_TO_REQUIREMENT_PACKAGE` active mapping in the same domain cutover and
   preserve retired/superseded ID and parent evidence through the existing
   archive/recovery checks. Record each reviewed disposition
   in the existing Task table, not a new migration framework or progress ledger.

### W21: Final QA and local delivery evidence

Depends on completion of the approved W17-W20 subset; excluded units remain
NOT_RUN and cannot satisfy their proposed acceptance. Root integrates receipts.
Use `.agents/governance/quality-standards.md` as the verification owner and the
same public entrypoint for local/hosted definitions. Record focused test results,
selected invocations, tool/config versions, cwd, setup count, duplicate count
and measured wall time in Task for comparable inputs. Do not compare different
contexts as a speed improvement.

Run the applicable changed profile after edits and local full for the shared
graph/validator cutover in a prepared Linux/WSL2 linked checkout with `/proc`,
pidfd and proper reaping. Bind evidence to HEAD plus the actual index/working-tree
inputs. Keep baseline resolution fail-closed and do not reuse another snapshot's
PASS. If final all-files is needed, it requires explicit authorization for the
eventual implemented scope and the existing clean-worktree/exact-path wrapper
contract. Neither W16 nor the completed option A approval authorizes that run.
It is not a new unconditional gate. Normal commit hooks remain.
Hosted run/job/SHA/event and managed automation observations require their real
read-back; no dispatch/push is authorized here. Operations planning and execution
stay on hold. Preserve the branch/worktree unless separately authorized.

### W22: One manifest evidence grammar

Owner: writable validation contributor. Files: `scripts/validation/check-script-manifest.py`,
`scripts/manifest.yaml`, `tests/validation/_script_manifest_support.py` and
`tests/validation/test_script_manifest.py`.

1. Establish which implementation the gate actually uses before proposing a row.
   The suite carried a second, looser grammar; a row could pass one and fail the
   other, which is how the omission rationale survived a passing checker.
2. Extend the gate grammar by one hop into a module-level helper that starts a
   child process, and keep a local helper that starts none as a negative case.
   Do not follow helper chains: at depth two every local call reaches subprocess.
3. Point the suite at the gate implementation and delete the duplicate. Keep the
   inventory-only rejections the tests own, and keep the checker loader inside
   the test module, because that call is the module's own use evidence.

### W23: One entry point into stage documents

Owner: documentation contributor with validation ownership for the mode. Files:
`scripts/lib/document_governance/links.py`, `scripts/validation/check-document-links.py`,
`scripts/lib/document_governance/operations_catalog.py`, `tests/lib/document_governance/test_links.py`,
`.agents/governance/documentation-protocol.md` and the affected documents outside `docs/`.

1. Widen the selection to tracked Markdown plus `llms.txt` before adding a rule.
   A named support list decided which outside documents were read at all, so the
   violations were invisible rather than tolerated. Tracked selection also keeps
   the untracked Markdown under `projects/` out of the graph.
2. Add the rule as a mode on the existing graph. Reuse the existing parser for
   fences, inline code, anchors and normalization; no separate regex pass.
3. Remediate by keeping the label and moving the path into code text, and add
   the entry-point link once per affected document. Where the old link was
   already broken, remove the reference: a text path to a file that is not there
   is the same stale claim. Fix canonical sources and regenerate provider
   projections rather than editing generated adapters.
4. Correct the documents that taught the rejected pattern, including the hook
   example and the validator's own README and constraint guidance.

### W24: CI setup with a consumer

Owner: writable CI/CD contributor. Files: `.github/workflows/ci-quality.yml`,
`.github/workflow-contract.yml`, `scripts/lib/gate/github_workflow_contract.py`
and `tests/lib/gate/test_github_workflow_contract.py`.

1. Prove the step is unused across gate leaves, requirements files and the hook
   runner's own code before removing it.
2. Remove the step, its registered action and its allowed-action entry together,
   so an unregistered action still fails the parity check.
3. Record the measured local execution map. Compare only equal contexts, and do
   not convert a single hosted observation into a threshold.

## Risk and Rollback

| Risk | Guard | Recovery |
| --- | --- | --- |
| Selector omits an affected owner | Real Git snapshot and semantic suite cases | Revert reviewed selector commit |
| Commit tools disagree | Accepted/rejected message and translation matrix | Revert coherent commit-contract unit |
| Workflow removal loses detection | Required drift leaf and failure propagation regression | Restore workflow unit from Git |
| Check mutates authored source | Explicit check mode or controlled isolated validation | Review task-owned diff; never reset others |
| Static success is promoted to runtime or hosted evidence | Per-command context and target SHA in Task | Correct evidence classification |
| Archive or identity changes manufacture completion | Preserve frozen bytes and current package states | Revert only authored Task-owned changes |
| Legacy removal hides a safety gap | Map each removed route to active behavior coverage | Restore the coherent contract/parser/test unit |
| Dynamic expected counts accept missing audit rows | Keep independent stable criterion membership | Restore the criterion owner and regenerated output |
| Consolidation loses a unique security or data obligation | Per-domain clause mapping and current frontmatter/CODEOWNERS owner review before retirement | Restore that domain's reviewed source and links from Git |
| Documentation work silently becomes runtime planning | Explicit user hold applies to W16-W21 | Remove the out-of-scope plan and correct its Task disposition |

## Verification

Use existing public commands and focused tests, then independent review before
logical commits. Task 0006 records exact command, context, target snapshot,
exit, result, cost when measured, approval/review source, and recovery.
Acceptance 17 maps to W8, 18 to W9, 19 to W10, and 20 to W7/W10.
Acceptance 21 maps to W11.
Acceptance 22 maps to W13, 23 to W14, and 24 to W12/W14/W15.
Domain-logic coverage is N/A for validation/configuration-only changes;
behavioral safety regressions remain mandatory for changed validators.

For the continuation, criterion 25 maps to W16; criteria 26/27/28/29/30 map
to W17/W18/W19/W20/W21 respectively. Criteria 31/32/33 map to W22/W23/W24. Planning verification is limited to
metadata contracts, changed document checks, links, LLM Wiki freshness and the
policy-selected public changed route. Actual commands and exits belong in Task.
The future minimum regression commands, used only for their approved changes,
are:

```bash
PYTHONPATH=. python3 -m unittest tests.lib.gate.test_ci_gate_contract tests.lib.gate.test_github_workflow_contract
PYTHONPATH=. python3 -m unittest tests.validation.test_audit_criterion_contract tests.validation.test_agentic_audit_semantic_freshness
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-document-links.py --mode all
python3 scripts/validation/check-document-corpus-lifecycle.py
python3 scripts/knowledge/generate-llm-wiki.py --check
python3 scripts/validation/run-ci-gate.py --profile changed --explain
python3 scripts/validation/run-ci-gate.py --profile changed
python3 scripts/validation/run-ci-gate.py --profile full
```

Select changed runner/selector, archive/identity, shell/eval and package-local
regressions from the existing contract where applicable; Python discovery alone
is not evidence of all repository tests. Explain output is planning evidence
only. W16 does not run W17-W21 regressions or full QA merely to document them.

## Rulings

- The user's explicit approval governs in-scope implementation choices; skill
  defaults do not add a second design approval, SDLC tree, or progress ledger.
- Stage 99 retains document shapes; Task evidence retains execution states.
- Current local completion, hosted verification and merge readiness are separate.

## Related Documents

- [Specification](spec.md)
- [Task 0006](tasks/tsk-0006-generated-evidence-and-final-verification.md)
- [Stage 03 index](../README.md)
