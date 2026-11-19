---
title: "P01 CI Routing and Document Validation Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-20"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0099"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-20"
---

# P01 CI Routing and Document Validation Task

## Scope

### Objective and Parent

Own criterion 155 and W171 under the [Spec](../spec.md) and [Plan](../plan.md).
Apply P01-CI-ROUTING 1.0.0 to the current Docker workspace, reusing P00's
finding F-DKR-003 and excluding completed work from reimplementation.

### Inputs and Authority

The direct user request authorizes P01 implementation, verification, commit,
push, PR and merge, and explicitly excludes automatic execution of other
prompts. The only external package input is
`_workspace/workspace_governance_remediation_1_0_0_20261119/`: README,
P01 prompt, execution contract, questions, sources, D01, Docker profile and
findings. No other repository or old package supplies implementation.

Observed root is `/home/hyunyoun/data/hy-home.docker`, Git common directory
is `/home/hyunyoun/data/hy-home.docker/.git`. Initial branch was `main`, HEAD
`5b02e40dfd26545ca1215b4432252446fcee239b`, status empty. The only change
since profile SHA `ef7b6eed51de19da72fb2c8230b02428333218dc` is the existing
P00 documentation commit. It is reused as a prerequisite, not repeated.
The P01 delivery branch is `codex/p01-ci-routing` from that current state.

Request revision `7104090df9b44e56c15d0e0a28a49a1d`, session
`01a1f47d-2e14-7c32-b0f7-008007421623`, brief `P01-CI-ROUTING-docker`
revision 4 records the final exact writer paths. Binding and dispatch checks passed;
native authorization and the user's requested delivery remain separate facts.

## Execution Log

### Work Performed

#### Discovery and exclusions

The current workflow already uses complete event-specific NUL-separated Git
diffs, both rename paths, PR head and authenticated merge changes, and local
committed/index/working/untracked unions. Missing bases and malformed inputs
raise errors. `candidate-quality` runs with `always()` on PRs and requires
routing success plus each selected job's actual success; an unselected shard
may be skipped. No whole-workflow path filter or merge queue is configured.
The separate `main-security` lane is retained. These are maintained features,
not new P01 implementation claims.

Confirmed gaps: the document library regression leaf combines unrelated
modules, repository-integrity makes Hermes checks mandatory even for ordinary
documents, an empty changed set still selects fallback suites, metadata
validates every record before filtering output, and completion-section readers
repeatedly parse identical Markdown. The existing document graph already
reads each document once for link modes; preserve that shared graph.

#### Writers and exact scope

| Owner | Paths |
| --- | --- |
| CI writer | `.github/workflow-contract.yml`; `scripts/lib/gate/ci_gate_contract.py`; `tests/lib/gate/test_ci_gate_contract.py`; `tests/validation/test_ci_gate_plan.py`; `tests/validation/test_ci_gate_execution_context.py` |
| Plan transport writer | `.github/workflows/ci-quality.yml`; `scripts/validation/ci_gate_runner.py`; `scripts/lib/gate/github_workflow_contract.py`; `tests/lib/gate/test_github_workflow_contract.py`; `tests/validation/test_ci_gate_model.py` |
| Document writer | `scripts/lib/document_governance/spec_packages.py`, `metadata/reference.py`, `links.py`, `lifecycle/public.py`; `scripts/validation/check-document-links.py`; existing `test_spec_packages.py`, `test_metadata_validator.py`, `test_links.py` under `tests/lib/document_governance/`; `tests/validation/lifecycle/test_public.py` |
| Coordinator | This Task and the same-package Spec and Plan |
| Coordinator regression correction | `tests/lib/document_governance/metadata/test_reference.py`: retain native findings and assert that main does not repeat the native record-validation pass |

Each writer checks the prepared request/brief and owns only these paths.
Independent reviewers do not edit the implementation. No new wrapper,
dependency, permanent timing ledger or fixed corpus count is planned.

#### Git event and check boundaries

| Event/input | Existing consumer and P01 treatment |
| --- | --- |
| Commit before/during: staged bytes and message | Installed pre-commit/commit-msg hooks; preserve narrow style/secret/message checks and partial-stage boundary. |
| Push before: outgoing refs | Existing pre-push main-ref guard; no repeated branch full suite. |
| PR before: current change union | Existing public changed selector explains actual consumers; local focused tests remain separate from hosted evidence. |
| PR during: authenticated candidate | `candidate-routing`, `candidate-core`, `candidate-documents`; split document regression consumers, retain candidate provenance and exact argv. |
| PR aggregate | Existing `candidate-quality`; missing/cancelled/failed/error is not N/A or PASS. |
| Merge before | Existing required checks/protection and review; no new local full or per-task SHA approval requirement. |
| Merge after | Existing main-security consumer; do not repeat the same quality predicate as a new merge gate. |
| Explicit full/manual/final integration | Expand genuinely global contracts to all affected consumers; keep full module ownership unique. |

#### Timing boundary

Authenticated read of run 44534944033 (PR 1125) confirms the old document
job's validation step was 1079 seconds (13:35:53–13:53:52 UTC), with 17
seconds from job start to validation and 4 seconds afterward. The core
validation was 584 seconds (13:35:48–13:45:32), setup before validation 25
seconds; prerequisite selection took 1 second. Routing selection and the
aggregate predicate each fit within timestamp resolution (0 whole seconds),
with 12-second routing and 3-second aggregate job envelopes. Job scheduling
and setup are distinct from leaf calculation. The run started at 13:35:18;
core/routing job starts at 13:35:23 leave 5 seconds before those jobs, the
document job starts 1 second after routing completes, and the aggregate starts
2 seconds after documents complete. These prior hosted observations
do not establish this candidate's performance; no p95 is inferred from N=1.

Read-back of main protection requires strict `candidate-quality`, enforces
administrators and conversation resolution, and requires zero approving PR
reviews. Local independent implementation/security review remains necessary.
Remote main is still `ef7b6eed`; delivery therefore includes the already
authored P00 prerequisite commit, without rerunning or modifying its work.

#### Implementation and measured scope

The old library leaf is replaced by five disjoint consumer groups. Existing
root rules admit bounded exclusions for known consumer routes, while new
document helpers retain subsystem regression coverage. Ordinary documents
exclude Hermes; existing Hermes-owned paths still select their exact checks.
Valid empty diffs have no selected suite. Invalid or unmapped inputs fail.

Routing now computes a shared plan once. Shards verify the candidate topology,
actual complete diff, contract/manifest identity, selected nodes and exact
argv/environment/order before using it for prerequisites and execution. The
digest is integrity, not authorization. A sampled plan was 8,379 bytes;
120,000 bytes is the fail-closed transport bound protecting the environment's
single-string limit. No new artifact, secret, permission or action pin is added.

Document changes share immutable completion lines and CommonMark edges,
return fresh caller-owned lists, and share historical Git input context on
the lifecycle route. Changed validation retains complete indexes and limits
document checks to actual consumers. Navigation-loop probing found an
intermediate overexpansion: a single document selected 844 of 915 documents.
Separating direct references from transitive typed relations, without treating
unchanged ancestor READMEs as new impact targets, now selects 2 for TSK-0098,
45 for RUN-0021 and 4 for the workspace glossary on that same graph. These
are observations, not standing corpus-size tests.

For the identical `links.py` plus `observe.py` change, selected hosted leaves
fell from 13 to 11 and unittest module selectors from 29 to 13. Local first
plan computation changed from 0.065516 to 0.096962 seconds; five subsequent
samples ranged 0.063355–0.064949 before and 0.072668–0.114718 after. Selection
is narrower, but these measurements do not show a planning-time speedup.

An isolated comparison used the exact 88,442-byte baseline Spec text and old
function recovered from Git, with identical resulting visible lines. First
parse was 0.082580 seconds before and 0.098419 after (N=1 each). Warm batches
of eight calls, N=5, were 0.030122–0.045809 seconds before and
0.000070–0.000079 after. These are in-process parse observations under local
Python 3.12.3 and concurrent host load, not a disk-cold or hosted p95 claim.

### Blockers and Decisions

No Q-01–Q-04 decision blocks P01. Permission, privacy, native provider,
external deletion and paid execution scopes are unchanged. Previously merged
work is not reopened. P00's current Task and the eleven previously completed
areas are reused by their existing evidence, without replaying their prompts.

#### Lifecycle Events

This newly added Task starts at draft under the recorded package contract.
Execution, checks, merge and owner acceptance are separate axes.

## Verification Evidence

### Results

The Registry's recorded generation 7 applies to SPEC-0212: use its existing
nine-column Evidence and five-column Criterion Decisions forms. Future
expanded templates do not change this package's consumer contract.

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 155 | W171 | Current Git state, P00 evidence and CI source/consumer review | HEAD 5b02e40df; matching P01/D01/Docker inputs | PASS | Read-only discovery; exact state and preserved boundaries above; implementation checks follow | required | - |
| E02 | 155 | W171 | P01 focused selector regressions in tests.lib.gate.test_ci_gate_contract | Baseline source before implementation | FAIL | Witnessed RED: initial three tests produced five failures for empty diff, consumer leaf and Hermes scope | required | - |
| E03 | 155 | W171 | P01 focused selector regressions in tests.lib.gate.test_ci_gate_contract | Implemented consumer rules | PASS | GREEN new selector cases; unsafe/duplicate/unowned exclusions and mixed/global/new-helper coverage retained | required | E02 |
| E04 | 155 | W171 | .venv/bin/python -m unittest tests.lib.gate.test_ci_gate_contract tests.validation.test_ci_gate_plan tests.validation.test_ci_gate_execution_context tests.lib.test_surface_ownership | Frozen selector source | PASS | Exit 0; 158 tests, 64.837 seconds; full-profile module ownership remains unique | required | - |
| E05 | 155 | W171 | P01 focused document regressions: CompletionParseReuseTests, ChangedMetadataClosureTests, ChangedDocumentScopeTests and shared-context case | Baseline source | FAIL | RED 10 tests: one failure and eight errors exposed missing APIs/CLI, repeated parse and unshared context | required | - |
| E06 | 155 | W171 | P01 focused document regressions: CompletionParseReuseTests, ChangedMetadataClosureTests, ChangedDocumentScopeTests and shared-context case | Implemented document source | PASS | GREEN 14 focused tests in 6.900 seconds; later scope edge cases separately checked | required | E05 |
| E07 | 155 | W171 | PreparedCandidatePlanTests in tests.validation.test_ci_gate_model | Before producer/consumer implementation | FAIL | RED four missing-function errors | required | - |
| E08 | 155 | W171 | PreparedCandidatePlanTests in tests.validation.test_ci_gate_model | Frozen shared-plan implementation | PASS | GREEN 11 tests, 1.168 seconds; tamper, stale, rehashed omissions, invalid invocation, empty/missing/oversized and manifest guards | required | E07 |
| E09 | 155 | W171 | .venv/bin/python -m unittest tests.validation.test_ci_gate_model tests.lib.gate.test_github_workflow_contract | Shared-plan/workflow source | PASS | 77 tests, 30.244 seconds before subsequent narrow test-only additions; a later 78-test run also passed, not combined with that count | required | - |
| E10 | 155 | W171 | In-process stdlib trace over focused current regression tests; AST added-statement first-lines | Added gate/runner/workflow source statements | PASS | Selector 9/11 (81.8 percent); runner 69/84 (82.1 percent); workflow checker 5/6 (83.3 percent). Added-statement exercise only, not branch or full-module coverage; no dependency installed | required | - |
| E11 | 155 | W171 | Same-input selection and immutable parse comparison | Baseline versus implemented source; exact inputs in Timing boundary | PASS | Output/selection observations above; cold and warm separated; no total CI speedup or p95 inferred | required | - |
| E12 | 155 | W171 | .venv/bin/python scripts/validation/check-script-manifest.py; .venv/bin/python scripts/validation/check-github-workflow-contract.py | Current manifest and workflow/runner contract | PASS | Exit 0; script manifest valid; five workflows, ten jobs and nine pinned actions valid | required | - |
| E13 | 155 | W171 | .venv/bin/python scripts/validation/check-document-links.py --mode all --changed --base-ref 5b02e40df | P01 global document-checker change | PASS | Exit 0; full affected document graph, zero failures and warnings; source edits correctly expand scope | required | - |
| E14 | 155 | W171 | .venv/bin/python scripts/validation/check-document-corpus-lifecycle.py | P01 current corpus | PASS | Exit 0; corpus and active-stage occupancy violations 0; not retirement approval | required | - |
| E15 | 155 | W171 | Independent code/spec and security review of P01 logical diff | git diff 5b02e40df plus Task0099; Codex CLI 0.169.0 read-only parent | FAIL | Security: no actionable finding; code/spec: per-record metadata selection occurs after a second whole-record validation loop and unrelated errors escape. Correction required | required | - |
| E16 | 155 | W171 | Independent code/spec and security review of P01 logical diff | Corrected metadata native/global-flow delta; unchanged reviewed slices reused | PASS | Read-only CLI delta review approves and explicitly resolves E15; selected records validate once, complete indexes/global invariants remain, actual controls broaden scope; no actionable security finding | required | E15 |
| E17 | 155 | W171 | Affected document implementation modules and focused correction cases | Frozen document source and final native/global/nav/colon corrections | PASS | Spec Package module 162 tests in 886.052 seconds; earlier link/metadata/public batch 168 in 187.610 seconds; final 17 targeted corrections in 7.476 seconds. Separate runs, not a combined suite or hosted speedup | required | - |
| E18 | 155 | W171 | In-process stdlib trace over focused document tests; AST added-statement first-lines | Five changed document production files | PASS | Final 20 tests; 140/154 added statements (90.91 percent); exact-filename filter avoids stdlib basename-ignore collision. Not branch/full-module coverage; no artifact or new dependency | required | - |
| E19 | 155 | W171 | .venv/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref 5b02e40df --changed-path docs/03.specs/0212-request-baseline-and-reconciliation/spec.md --changed-path docs/03.specs/0212-request-baseline-and-reconciliation/plan.md --changed-path docs/03.specs/0212-request-baseline-and-reconciliation/01.tasks/tsk-0099-p01-ci-routing.md | Final metadata source; real global controls retained alongside explicit docs | PASS | Exit 0; selected 849 managed records, violations 0, overrides 0. Global expansion was observed, not inferred from local runner mode | required | - |
| E20 | 155 | W171 | Metadata contract/CLI regression invariants | Final production source; existing metadata validator/reference modules | FAIL | .venv/bin/python -m unittest tests.lib.document_governance.test_metadata_validator tests.lib.document_governance.metadata.test_reference: 49/50 passed, 255.572 seconds. One old test mocked the native pass then required main to repeat validate_record | required | - |
| E21 | 155 | W171 | Metadata contract/CLI regression invariants | Unchanged production; corrected duplicate-call expectation and actual native flow | PASS | Reused unaffected 49 PASS results; reran test_changed_mode_retains_repository_contract_findings plus ChangedMetadataClosureTests: five tests PASS in 2.312 seconds. Native error retention remains asserted; main must not repeat validation. This is scoped resolution, not a claimed 50-test rerun | required | E20 |

### Resolution Links

E03/E06/E08 resolve the witnessed RED cases. E16 resolves E15 through the
actual metadata correction and independent delta review, reusing unchanged
slices. E21 resolves the obsolete duplicate-call expectation in E20 while
retaining native findings and actual-flow coverage. No failure is waived by
acceptance prose or an unrelated security verdict.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 155 | pending | E01 | Owner acceptance is separate from implementation and delivery | @buenhyden |

### Remaining Conditions

Local implementation, focused RED/GREEN checks, scoped added-statement
coverage, same-input timing and independent review are complete. Hosted PR
required checks and delivery remain to be observed; owner acceptance remains
separate. No full repository suite or live service was run. Existing P00
operational conditions are not closed by this CI task.

## Handoff

### Promotion Receipt

Durable selection behavior belongs to the workflow contract and gate library;
parse/scope behavior belongs to the existing document libraries. Their tests
and actual consumers change with them. This Task is the only execution record.

### Next Owner

After P01 verification and requested delivery, the next input is
`_workspace/workspace_governance_remediation_1_0_0_20261119/prompts/P02-LOCAL-FEEDBACK.md`.
Its prerequisite is P00 and P01's actual result and exclusions. Do not execute
P02 automatically. Preserve the matching package through P17; remove only
P01-owned one-off timing/test artifacts when finished.
