---
title: "Evaluation Migration and Recovery Acceptance"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-TSK-0009"
parent_ids:
- "SPEC-0190"
- "SPEC-0190-PLAN-0001"
created: "2026-09-29"
---

# Evaluation Migration and Recovery Acceptance

## Objective

Implement Plan W9: move the four evaluation subsystem sources from evals to
.agents/evaluations, preserve actual consumers and historical continuity, and
add recovery review evaluation using the existing model-free engine.

## Inputs

- [Approved Spec](../spec.md) and [approved Plan](../plan.md), including the
  owner-selected migration and exact historical-baseline amendment.
- [W7 evidence](tsk-0007-workflow-and-handoff.md): committed cf540281f;
  evaluator fixtures 10/10 and regressions 38/38, ET 54/54 PASS.
- [W8 task](tsk-0008-native-hooks.md) owns disjoint native/hook files.
- Exact file ownership is the Plan W9 map. Root owns this Task, Spec, Plan and
  commits. Mechanical migration precedes evaluator changes; writers hand off
  shared files explicitly. No index changes by workers or overlapping writers.
- Approved local changes, checks, independent review and logical commits only.

## Work Log

Read-only consumer audit selected .agents/evaluations for all four dedicated
subsystem files, retaining ordinary tests and fixtures in tests. No duplicate
source or permanent redirect is needed. Preserve executable modes.

The old evaluation README is absent from metadata's historical base corpus.
Use the existing lifecycle helper for one exact trusted historical-path mapping;
retain type, identity, lifecycle and introduced-body checks. No new migration
engine, schema, profile, unrestricted inventory exclusion or state override.

## Verification Evidence

Mechanical baseline: pre-move E 10/10 fixtures and 38/38 regressions PASS;
post-move same 10/38 PASS in 0.110s. Two migration regressions witnessed RED,
then GREEN 2/2 in 0.514s. Source and runner mode bits were preserved.
Registry tests: 106/106 PASS in 38.989s; focused body-continuity regression
retains introduced missing-heading detection. Initial combined ET/consumer
194-test run had two failures: unavailable pre-commit on sanitized PATH and
an earlier module-level import breaking direct --help. The existing local/system
pre-commit fixture uses its installed binary through an explicit sanitized PATH;
no remote hook installation. Function-local imports preserve the direct-script
help interface without sys.path mutation. Final reruns are recorded below.

Initial L: 94/95 passed; one moved catalog relative link was still stale and
was corrected. The historical 2870-link capture warning remains separate.
Metadata against 567e9ea00: selected=13, violations=0, legacy_exceptions=0,
transition_overrides=0. An earlier fda093e05 comparison also included a later
new active W10 Task and correctly rejected its missing initial draft at that
older base; the actual W10 predecessors are separately committed. The later
base still contains all four original evals sources, so migration continuity
was verified against real old blobs without an override.
Entrypoint links: documents=990, links=9936, failures=0, warnings=0, exit 0.
Renderer: providers=2, drift=0, exit 0.

Independent review found and required corrections for keyword-only READY
acceptance, repeated reviewer/implementer/approver identity, current restore
success claims, and a Git glob omitting the direct child shell runner. Paired
negative tests closed those findings in the final technical review; earlier
passing checkpoints were not treated as acceptance of the reported defects.

Recovery rubric is fixed before scoring: state/ownership, backup or justified
rebuild, consistency, retention/capacity, key custody, dependency order, versions,
isolation, RPO/RTO objectives versus observations, application acceptance,
stop/partial-result conditions and three distinct responsible people. Use the
existing 0.50 safety-fixture threshold plus mandatory completeness/refusal
conditions. Synthetic no-skill examples are not native efficacy observations.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| R15/R20/R31/R32/R33/R36/R38/R39 | W9 | Static/local PASS; native/hosted/runtime NOT_RUN | Existing evaluation subsystem and its registered consumers |

Final technical receipts (registered unittest adapter; sanitized PATH includes
the existing user-local pre-commit executable only where its local/system fixture
requires it): E fixtures 11/11 and regressions 54/54 PASS, exit 0; ET 57/57 PASS
in 24.829s; G 53/53 PASS in 92.621s. One earlier ET rerun had one failure whose
detail was lost in contributor output summarization; the subsequent unchanged
run passed. Its cause is unconfirmed and this receipt does not assert flake-free
execution. ET plus gate adapters: 82/82 PASS in 25.311s. The previously failed
consumer cases and continuity/direct-help probes passed in the focused 59/59
run (27.361s). Sixteen owned Python files passed pinned Ruff lint/format checks.
Bash syntax and diff checks passed. Manifest CLI PASS; GitHub workflow contract
PASS (five workflows, seven jobs, eight actions); native renderer drift zero.

Root final frozen consumer verification: 355/355 PASS in 155.870s, exit 0,
using the registered run-unittest adapter with sanitized PATH and these modules:
tests.validation.test_agent_output_eval_fixtures;
tests.lib.document_governance.test_registry;
tests.lib.document_governance.metadata.test_profile;
tests.validation.lifecycle.test_contract;
tests.lib.gate.test_ci_gate_adapters;
tests.validation.test_validator_entrypoints;
tests.validation.test_script_manifest;
tests.validation.test_ci_gate_plan;
tests.validation.test_ci_gate_execution_context;
tests.lib.gate.test_github_workflow_contract.
Expected rejection diagnostics from mutated negative fixtures are not failed
unittests. Final public evaluator CLI: 11/11 fixtures and 54/54 regressions PASS,
exit 0. C: repository/all failures=0; R: providers=2 drift=0.

All four original source paths are absent. The destination contains exactly
README.md, agent_output_eval.py, fixture-catalog.md and the shell runner. Git
modes remain 100644 for documentation and 100755 for executables. Active-surface
search finds only the exact historical README mapping, its negative tests, and
two preserved dated knowledge observations using evals paths; no live old caller
or compatibility source remains. Five workflow YAML identities are unchanged.

Final L after the separately reviewed multiline HTML correction: 96/96 PASS
in 97.396s, exit 0. Whole-branch reviewer approves the local/static change with
explicit observation limits; no unresolved code finding remains.

### Project-only Skill Stocktake

Static reconciliation: 24 unique active canonical skills, exactly 24 role
references across 14 roles, one direct role consumer per skill, orphan=0.
All 24 openai metadata files disallow implicit invocation; all 24 Claude skill
projections point at their canonical source and disable model invocation.
Codex has zero duplicated skill copies, as its adapter requires. The Provider
Registry has exactly 48 skill-source entries (SKILL and openai metadata).
This is declared routing, not usage frequency or native invocation evidence.

The Spec's per-skill table owns each retention rationale. Actual file-level
dispositions under `.agents/skills/<name>/SKILL.md` are:

| Disposition | Exact skill names | Consumer evidence |
| --- | --- | --- |
| Unchanged retain (17) | adr-writing; change-review-execution; ci-cd-patterns; code-review-dimensions; compose-stack-agent; container-threat-modeling; deployment-pipeline-design; docker-compose-patterns; e2e-testing; execution-plan-agent; knowledge-map-agent; policy-gate-agent; requirements-to-design-agent; security-audit; task-breakdown-agent; test-authoring; workspace-audit-revalidation | Existing direct role skill_ids; distinct procedures retained |
| Modified existing (5) | incident-response; infra-cross-validate; ops-runbook-agent; infra-validate; style-validation | Recovery routing or actual helper contract changes in W4-W6; final helper corrections in W10 |
| Retained bundle, modified source (1) | provider-model-evaluation | eval-engineer; current README link changes, two resources unchanged |
| New (1) | stateful-recovery-contract-review | iac-reviewer; three existing skills and explicit hook/workflow handoffs route sanitized review |

The ten reachable regular procedure resources reconcile eight original plus two
new: modified infra-validate/scripts/static-checks.sh and
style-validation/scripts/classify-changed-files.sh; new recovery reference and
verdict asset; unchanged policy-gate-agent, provider-model-evaluation and
security-audit reference/asset pairs. Openai metadata and native projections
are not counted as procedure resources. No project/global cache or usage data
was read or written by this stocktake; it is an explicit local equivalent of
the unavailable skill-stocktake skill, not a native skill invocation.

## Review Evidence

Independent ten-document prose, metadata/registration boundary and evaluator
technical review: PASS/CLEAR after correcting broken relative links, stale rows,
historical provenance and the recorded acceptance findings. Evaluation
responses are input data, never automatically loaded execution instructions.

## Commit Ledger

Root records actual draft, ready and in-progress predecessors before GO.
Draft 6b320a653, ready cc26e19cc and in-progress fda093e05 each passed
metadata validation before GO. W8 completed separately in e2d5b0482.
Implementation and independent review are complete; this Task records local
W9 acceptance only. Final lifecycle validation against c0d16924c passed: selected=14, violations=0,
legacy_exceptions=0 and transition_overrides=0.

## Rulings

- Register exactly four canonical evaluation files; reject unknown siblings.
- Replace the existing README profile path and exclude only the code-owned
  catalog from document inventory, retaining its executable contract checks.
- Add fixture and typed threshold together; retain score interfaces and existing
  failure detection. Remove obsolete current criteria, not historical evidence.
- Preserve all-six-suite impact, existing workflow identities and test ownership.
- Project-only skill stocktake reuses the existing disposition table; no global
  cache, personal usage data, new framework or speculative packaging modes.

## Deferred Items

W10 owns final branch acceptance. Native, editor, hosted, paid-budget and actual
recovery observations remain separate and unclaimed by static fixtures.
