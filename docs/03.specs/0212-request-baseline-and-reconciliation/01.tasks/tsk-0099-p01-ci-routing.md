---
title: "P01 CI Routing and Document Validation Task"
version: "0.3.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-23"
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
Maintain the merged P01-CI-ROUTING implementation against the current 1.1.0
request, reusing P00's finding F-DKR-003 and excluding completed work from
reimplementation. The original 1.0.0 execution below remains dated evidence.

### Inputs and Authority

The current direct user request authorizes P01 reconciliation, verification,
commit, push, PR and merge only. Its package is
`_workspace/workspace_governance_remediation_1_1_0_20261120/`: README,
P01 prompt, decisions-20261120, execution contract, questions, sources, D01,
Docker profile and findings. No other workspace profile is an implementation
input. The following original-request details are historical provenance,
not instructions to read the earlier package.

The original direct user request authorized P01 implementation, verification, commit,
push, PR and merge, and explicitly excluded automatic execution of other
prompts. The only external package input was
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
After context recovery, request revision `ae5db1914fee1a47af68a46609a21ab6`
and brief revision 5 bind only this Task and the CLI regression fixture.
The clean baseline is `59623b56da169281103453c7e9fa2f34916bdaf8`;
the P01 delivery authorization and exclusive writer boundary are unchanged.
Brief revisions 6 and 7 extend this same P01 correction to the link CLI and
its existing regression module, then the optional Hermes invocation bindings
and the existing P03/P11 workflow-contract tests. No service implementation
or earlier prompt is reopened.
After link correction commit `2bcc4436f2bff883fc79754b954e059367488a94`,
brief revision 8 rebinds only the runner, its two existing Hermes contract
test consumers and this Task. The prior test writer has handed back those
files; no parallel writer remains on this delta.
Brief revision 9 binds this result-only update to merged baseline
`16d2be3f6c4c9a8b0de69e0224b5b6c6727432df` on
`codex/p01-ci-evidence`. Implementation source is frozen and reused.

## Execution Log

### Work Performed

#### Current 1.1.0 maintenance boundary

On 2026-11-20, the current root and common directory remain those recorded
above. Branch `codex/p01-ci-evidence`, HEAD
`60f905d41663147745256120b6e840fa4ba20959` and remote main agree; the
working tree is clean. The branch's ahead marker describes committed
history, not unowned edits. P00 1.1.0 is merged through
[PR1128](https://github.com/buenhyden/hy-home.docker/pull/1128).
Request revision `1272c1f821bb8a9a614b3cdfb0d659eb` and brief
`P01-CI-ROUTING-docker-1.1.0` revision 1 bind this Task alone. The coordinator
is its exclusive writer; the audit worker has no write assignment. No
partial implementation or concurrent writer is inherited.

The current matching D01 still has design version 1.0.0. Q-01–Q-04 have
been compared with P01; none changes its CI input, trust or result contract.
The previously completed eleven areas remain excluded by their actual
receipts, without introducing a fixed-count completion gate. Open PR1047
and PR1048 retain their previously observed heads and remain separate image
updates; neither is merged or treated as current implementation.

Only four Spec/Plan/Task files differ between final implementation head
`a6e797d0` and this baseline. Workflow, selector, runner, document libraries,
regression consumers, manifest, lock/toolchain and policy inputs are unchanged.
Reuse their source-level results and dated hosted evidence; this does not
claim that an old run tested a new candidate or an unchanged live service.
[PR1127](https://github.com/buenhyden/hy-home.docker/pull/1127) delivered the
result-only receipt as `b8ddeee632ed44dc4ecb2cda0e29d3c586618e1f`; its
[run44582373102](https://github.com/buenhyden/hy-home.docker/actions/runs/44582373102)
passed routing/core/required aggregate with documents correctly unselected.

| P01 requirement | Maintained implementation and evidence |
| --- | --- |
| 1: Events, consumers and timing | Workflow contract, `ci-quality.yml` and gate runner; event table and separated observed queue/setup/plan/leaf/aggregate boundaries below; E11/E12/E33. No p95 or total speedup claim. |
| 2: Complete event union and self-regression | Existing gate change discovery, execution contexts and contract root rules; both rename sides, deletion, global consumers and runner regressions; E03/E04/E08/E09. |
| 3: Honest result aggregation | Existing always-reporting `candidate-quality`; selected missing/skip/cancel/error blocks, valid unselected shard is N/A; E08/E09/E32/E33. No whole-workflow path filter or active merge queue. |
| 4: Shared parsing and affected closure | Existing `spec_packages.py`, `links.py`, `metadata/reference.py`, `lifecycle/public.py` and link CLI; immutable parse reuse, complete indexes, changed/inbound scope, global expansion and fail-closed base discovery; E06/E16/E17/E19/E21/E26/E28. |
| 5: Meaningful reuse and event separation | Existing shared prepared plan, authenticated candidate and exact invocation bindings; PR quality and merge security have different consumers. E08/E09/E12/E30/E31/E33, unchanged source and trust scope. No new persistent result cache or privileged PR route. |
| 6: Representative selection cases | Existing gate/plan/context and document tests cover document/code/manifest/lock/rename/delete/global/empty/error cases; E03/E04/E08/E09/E17/E31. P04 must map any new form consumer into this same selector. |

No known P01 implementation gap was found. Only this nonterminal Task's
current authority, maintenance evidence and next input change. Existing
Spec criterion 155 and Plan W171 remain the contract and owner; no new
Spec, wrapper, test, completion ledger or approval gate is needed. Fresh
document checks and the new PR's required CI verify this documentation delta.

[PR1129](https://github.com/buenhyden/hy-home.docker/pull/1129) delivers this
one-file maintenance update. Its first head `7af95e1cb73f20f5924e483a569a3313a6c7dd2e`
passed routing/core/required aggregate in run44589566583. Brief revision 2
rebinds the same Task after that commit for this observed receipt only.
Final receipt-head checks and merge are read back from the PR; this paragraph
does not claim that an unexecuted candidate or owner acceptance passed.

#### R01 1.2.0 feedback repair boundary

The direct R01-FEEDBACK 1.2.0 request on 2026-11-23 reuses criterion 155/W171
from clean `main` 0a500aa1 on branch `codex/r01-feedback-1-2-0`. D18, D21 and
the Docker findings D23-04/05/06 select three narrow repairs; D23-07 (staged
`write-tree` candidate and light pre-push) is retained unchanged. P01/P02 are
not re-run.

- **Discovery (D23-06):** the Hermes registration loop left `_function` as a
  module alias of `TestHermesCandidate`, so unittest discovery ran 16 cases
  twice. A repository scan found no other aliased TestCase. The loop
  variables are deleted and unique discovery is pinned.
- **Document checks (D23-04):** one-document profiling showed the repeated
  work. Lifecycle `--readiness` loaded the Spec Packages twice. The
  content-keyed Markdown parse cache held 8 entries for about 1000 documents.
  Each historical registry read re-ran `rev-parse`, `ls-tree`, `cat-file`,
  JSON parse and the depth walk. The repairs reuse the packages already
  loaded, size the cache for the corpus, and cache only immutable commit and
  blob names while returning fresh JSON. Nothing is cached across processes,
  and no candidate-produced cache is trusted.
- **Regression leaves (D23-05):** `leaf.execution-environment-regressions`
  takes the admission, Compose-start/observation and LAB controller, layout,
  isolation, credential and Locust modules out of the two broad bundles; the
  full profile still reaches each module once. Admission and dispatch changes
  now select only this leaf, not both bundles (about 150 modules). LAB and
  Compose-start paths keep reaching Compose-baseline through
  `local.template-security-baseline`, whose children now include the new leaf,
  so no LAB consumer is lost. QUALITY-STANDARDS-R75 names the leaf in the
  closed hosted set; dispatch tests stay local-only under the same rule.
- **Correction:** an initial root-only simulation suggested that PR1143's
  LAB change selected no LAB tests. The expanded plan shows they ran through
  the template-security aggregate, so this is recorded as no gap.

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
| Coordinator delivery correction | Existing `tests/lib/gate/test_p03_workflow_contract.py` and `test_p11_workflow_contract.py`: preserve exact optional bindings, mutation rejection, routing and all five contexts |

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

#### Hosted delivery result

Final run [44576522487](https://github.com/buenhyden/hy-home.docker/actions/runs/44576522487)
examined head `a6e797d0bfb99fb515012c4da0fd65b3450f1b4f` against base
`ef7b6eed51de19da72fb2c8230b02428333218dc` and authenticated merge candidate
`0704be89ef613ecfcac278b9c4fe588db93bc410`. Routing, core, documents and
required `candidate-quality` all succeeded. CodeQL and GitGuardian also
succeeded; `main-security` is correctly not applicable to this PR event.

This N=1 run took 24 minutes 27 seconds (17:22:41–17:47:08 UTC).
Run creation to routing start was 3 seconds; routing's job envelope was
15 seconds, with plan computation below whole-second timestamp resolution.
Both shards started 2 seconds after routing completed. Core setup before
validation was 18 seconds, validation 257 seconds and afterward 5 seconds.
Document setup was 19 seconds, validation 1419 seconds and afterward
4 seconds. Aggregate scheduling took 2 seconds after documents completed;
its job took 2 seconds, with the predicate below whole-second resolution.
Hosted logs report 404 tests across 11 core modules and 1142 across 29
document modules; these observations are not standing corpus-count checks.
The Spec Package module passed 162 tests in 452.040 seconds. This broad
26-file P01 diff differs from PR1125's two-helper change, so neither total
speedup nor equivalent-input regression or p95 is established by comparing
those runs. The same-input selection and parse measurements above remain
the bounded performance evidence.

[PR1126](https://github.com/buenhyden/hy-home.docker/pull/1126) was merged
at 2026-11-19 17:49:04 UTC as
`16d2be3f6c4c9a8b0de69e0224b5b6c6727432df`, after read-back showed
the current head, all required results and a clean merge state. No protection
or hook was bypassed. This result-only receipt is delivered through a
separate ordinary PR, without repeating the source implementation.

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
E10 and E18 describe their original frozen implementation snapshots, not
newly calculated coverage totals after hosted corrections. The unchanged
statements retain that evidence; E23/E26/E30/E31 verify the corrections.

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
| E22 | 155 | W171 | Shared-plan CLI tests through the hosted adapter boundary | PR 1126 head 59623b56; run 44572365371 candidate-core | FAIL | Two new CLI tests inherited the adapter's descriptor root instead of their canonical fixture root. Local open-directory-descriptor reproduction: 11 tests, two identical noncanonical-root failures. Actual routing producer passed; no production boundary is relaxed | required | - |
| E23 | 155 | W171 | Shared-plan CLI tests through the hosted adapter boundary | Canonical fixture scoped with enterContext/patch.dict; existing run_adapter API, run-unittest tests.validation.test_ci_gate_model -v; PATH-only child environment | PASS | 19 tests PASS in 2.308 seconds through the real descriptor-adopting adapter; direct descriptor reproduction also passes 19 tests and asserts restoration of inherited environment. Tamper, stale, missing-plan and single-plan assertions remain intact; production source unchanged | required | E22 |
| E24 | 155 | W171 | Independent review of hosted fixture correction | Three-line test-only delta after 59623b56 | PASS | Read-only reviewer approved; independently reproduced both affected tests with inherited descriptor root: two PASS in 0.381 seconds, environment restored; no production or security boundary changed | required | - |
| E25 | 155 | W171 | Ordinary link CLI behavior through the adapter boundary | Cancelled first hosted document job 135730769559; local inherited descriptor reproduction | FAIL | Three existing ordinary/impact subprocess tests fail because P01's eager metadata imports validate a descriptor not inherited by the child. Local reproduction confirms three failures in 1.048 seconds; cancellation is not a successful document result | required | - |
| E26 | 155 | W171 | Ordinary link CLI behavior through the adapter boundary | Metadata imports scoped to changed discovery; unchanged metadata guards; run_adapter run-unittest tests.lib.document_governance.test_links -v | PASS | Full existing links module: 151 tests PASS in 153.105 seconds through the real adapter. Subsequent clean-fixture assertion checked by ChangedDocumentScopeTests: 13 PASS in 6.544 seconds. Persistent ordinary-mode fixture carries a closed descriptor; changed Git/base failures remain errors. Script Manifest PASS | required | E25 |
| E27 | 155 | W171 | Independent review of late-import correction | First link CLI delta and Git-failure mock | FAIL | Reviewer found that mocking identity._run_git before lifecycle's first import can retain the mock in lifecycle; three-test order yielded two PASS and one FAIL. Production import boundary itself approved | required | - |
| E28 | 155 | W171 | Independent review of late-import correction | Added clean-fixture discovery assertion before injecting Git failure | PASS | Same reviewer reran the previously failing order: three tests PASS in 2.080 seconds; normal empty diff verified and real helper initialized before mocking; production/security verdict approved | required | E27 |
| E29 | 155 | W171 | Optional Hermes binding and regression ownership | Hosted run 44574168668 candidate-core; existing P03/P11 tests and adapted mutation cases | FAIL | Four obsolete mandatory-validator lookups fail after optional routing. Adapted eight tests expose 12 accepted cross-script or unknown-ID cases; an intermediate binding fix still accepts two substitutions with another generic admitted checker. These are correction work, not waived old requirements | required | - |
| E30 | 155 | W171 | Optional Hermes binding and regression ownership | Immutable gate-ID to exact script/argv mapping before generic admission; updated existing P03/P11 tests; unchanged selection scopes | PASS | Direct combined P03/P11/model: 27 tests PASS in 3.710 seconds. Real adapter separately runs P03 four PASS in 0.535 seconds, P11 four PASS in 1.087 seconds, model 19 PASS in 2.390 seconds. All five contexts preserve exact checks; missing nodes, swapped/other checkers, bad argv and unknown identities are refused. Ruff and diff checks PASS | required | E29 |
| E31 | 155 | W171 | Independent review of optional Hermes correction | Final immutable binding and existing P03/P11 regression delta | PASS | Reviewer approved source/security and preserved obligations; independently ran eight tests PASS in 1.455 seconds and 150 exact/malformed binding assertions across five contexts. Generic/adapter substitutions and unknown IDs are refused; no files edited by reviewer | required | - |
| E32 | 155 | W171 | Hosted candidate-quality aggregate | Earlier runs 44572365371 and 44574168668 | FAIL | Both required aggregates failed; first documents job was cancelled after core failure, second core/documents failed. No cancellation or missing success was presented as PASS. Defects are recorded and corrected above | required | - |
| E33 | 155 | W171 | Hosted candidate-quality aggregate | Final head a6e797d0; authenticated candidate 0704be89; run 44576522487 | PASS | Routing/core/documents/aggregate success; 404 core and 1142 document tests in this run; GitHub read-back confirms current-head checks and clean merge state. Exact time boundaries above; unchanged earlier review evidence reused | required | E32 |
| E34 | 155 | W171 | Authorized P01 implementation delivery | PR1126 current head a6e797d0 after required checks | PASS | GitHub merge and read-back confirm merge commit 16d2be3f6c4c9a8b0de69e0224b5b6c6727432df at 2026-11-19 17:49:04 UTC. Fast-forward local reconciliation preserved a clean tree; owner acceptance is not inferred | required | - |
| E35 | 155 | W171 | Result-only receipt authoring checks | This Task delta against 16d2be3f | PASS | .venv/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref 16d2be3f: selected one record, zero violations; .venv/bin/python scripts/validation/check-document-links.py --mode all --changed --base-ref 16d2be3f: two selected documents, zero failures/warnings; .venv/bin/python scripts/validation/check-document-corpus-lifecycle.py: zero corpus/occupancy violations. All three commands exited 0; selected-plan explanation and diff check passed | required | - |
| E36 | 155 | W171 | Matching 1.1.0 requirement/decision and dependency comparison | Clean HEAD 60f905d4; final implementation a6e797d0; P00 PR1128; matching P01/D01/Docker inputs | PASS | Six requirements mapped above; only four existing execution documents changed since implementation. Source/test/tool/contract scope unchanged; reuse dated successful results without replay or new acceptance claim | required | - |
| E37 | 155 | W171 | Separate requirement-to-consumer inspection and low-risk author diff check | P01 1.1.0; unchanged tracked source and this Task delta | PASS | Inspection worker found no blocking implementation gap and confirmed six mappings against source/tests, corroborating the stale advisory graph. No writes or test replay; this is not a new enforced read-only runtime observation. Author checked exact one-file diff, historical/current authority, generation-7 shape, pending acceptance and absence of private payloads | required | - |
| E38 | 155 | W171 | .venv/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref 60f905d4; .venv/bin/python scripts/validation/check-document-links.py --mode all --changed --base-ref 60f905d4; .venv/bin/python scripts/validation/check-document-corpus-lifecycle.py | Current 1.1.0 Task maintenance delta | PASS | All exit 0: one selected metadata record, zero violations; three selected link documents, zero failures/warnings; corpus/occupancy violations zero. Existing generation-7 form preserved. Changed-plan explanation and git diff --check passed; counts describe observations only. No permanent diagnostic or progress artifact created; matching input package retained | required | - |
| E39 | 155 | W171 | Hosted maintenance candidate and authorized remote delivery read-back | PR1129 head 7af95e1c against base 60f905d4 | PASS | [Run44589566583](https://github.com/buenhyden/hy-home.docker/actions/runs/44589566583): routing/core/required candidate-quality success; document shard explicitly unselected and main-security N/A for PR. Commit and dedicated branch push completed normally. Strict current-head required check/admin/conversation protection remains enforced, with zero approving reviews required. Final receipt-head result and merge remain separate PR observations | required | - |
| E40 | 155 | W171 | R01 1.2.0 package, D18/D21 and Docker finding review | Clean main 0a500aa1; D23-04/05/06/07 | PASS | Three repairs selected; D23-07 retained; P01/P02 not re-run | required | - |
| E41 | 155 | W171 | python3 -m unittest tests.validation.test_hermes_candidate_validator | New unique-discovery regression before the fix | FAIL | Witnessed RED: 32 discovered cases for 16 unique Hermes functions | required | - |
| E42 | 155 | W171 | python3 -m unittest tests.validation.test_hermes_candidate_validator | Loop variables deleted | PASS | Exit0; 17 tests (16 Hermes cases once plus the discovery check) | required | E41 |
| E43 | 155 | W171 | cProfile of check-document-metadata.py --mode check-changed and check-document-corpus-lifecycle.py --readiness | One-line edit to this Task over 0a500aa1 | PASS | Hot paths: lifecycle load_spec_packages 2 calls/265.7s; markdown parse 3215 times through an 8-entry cache; 3627 historical registry reads and 17.3M depth-walk calls. Profiling observation only | required | - |
| E44 | 155 | W171 | python3 -m unittest tests.validation.lifecycle.test_public tests.lib.document_governance.test_registry | Readiness-reuse and immutable revision-cache regressions before the fix | FAIL | Witnessed RED: readiness reloaded the Spec Packages once more; old registry source had no immutable-object cache | required | - |
| E45 | 155 | W171 | python3 -m unittest tests.validation.lifecycle.test_public tests.lib.document_governance.test_registry | Shared parse and revision caches with single package load | PASS | Exit0; 184 tests | required | E44 |
| E46 | 155 | W171 | /usr/bin/time of the same two document checks, before and after, same host | Before: worktree of main 0a500aa1; after: this branch. Both with the identical one-line Task edit and base equal to their own commit | PASS | Metadata 157.09s/135MB to 105.03s/214MB, both selected1 with the same one finding. Lifecycle 197.80s/99MB to 72.85s/170MB with identical output. One sample each on a host with load about 6-7; not a p95 or guarantee. An after-run against origin/main selected 862 documents because validator code changed, so it is not comparable | required | - |
| E47 | 155 | W171 | python3 -m unittest tests.validation.test_ci_gate_plan.CiGateRunnerContractTests.test_execution_environment_changes_select_their_consumer_leaf | New consumer-routing regression before the contract change | FAIL | Witnessed RED: leaf.execution-environment-regressions not found for LAB, admission, dispatch or Compose-start paths | required | - |
| E48 | 155 | W171 | python3 -m unittest tests.validation.test_ci_gate_plan tests.validation.test_p07_ci_routing tests.validation.test_p09_ci_routing tests.lib.gate.test_ci_gate_contract tests.lib.test_surface_ownership tests.lib.gate.test_github_workflow_contract | First contract split | FAIL | 35 failures from the aggregate-children and hosted-set pins, then 5 from the P07 routing and optional-skip pins. Each pin was updated to the deliberate partition | required | - |
| E49 | 155 | W171 | python3 -m unittest tests.validation.test_ci_gate_plan.CiGateRunnerContractTests.test_execution_environment_changes_select_their_consumer_leaf | Corrected contract | PASS | Exit0 in local and pull_request contexts; admission and dispatch select neither broad bundle | required | E47 |
| E50 | 155 | W171 | python3 -m unittest tests.validation.test_ci_gate_plan tests.validation.test_p07_ci_routing tests.validation.test_p09_ci_routing tests.lib.gate.test_ci_gate_contract tests.lib.test_surface_ownership tests.lib.gate.test_github_workflow_contract | Corrected contract, gate code and pins | PASS | Exit0; 212 tests including surface ownership; each module is reached once | required | E48 |
| E51 | 155 | W171 | python3 -m unittest over the eight execution-environment leaf modules | New leaf contents | PASS | Exit0; 243 tests in 40.58s. The adapter refuses direct invocation outside the runner, so the modules ran under unittest | required | - |

### Resolution Links

E03/E06/E08 resolve the witnessed RED cases. E16 resolves E15 through the
actual metadata correction and independent delta review, reusing unchanged
slices. E21 resolves the obsolete duplicate-call expectation in E20 while
retaining native findings and actual-flow coverage. No failure is waived by
acceptance prose or an unrelated security verdict.
E23 resolves the hosted fixture failure in E22; the updated PR's own
successful hosted aggregate is subsequently recorded by E33.
E26 resolves the actual link CLI import regression; E28 resolves test-order
contamination discovered during review. Those local results did not stand in
for the interrupted hosted document job; E33 records the completed candidate.
E30 resolves the optional-binding defect and migrates its existing contract
tests without dropping routing, context or fail-closed obligations.
E33 resolves the earlier hosted aggregate failures in E32 for the corrected
candidate. The local correction checks and the actual hosted aggregate are
different observations; neither substitutes for owner acceptance.
For R01 1.2.0, E42, E45, E49 and E50 resolve the witnessed failures E41, E44,
E47 and E48. E46 compares the same candidate on the same host.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 155 | pending | E16, E17, E19, E21, E23, E26, E28, E30, E31, E33, E34, E36, E37, E38, E42, E45, E46, E49, E50, E51 | Implementation, verification and merge complete; 1.1.0 maintenance confirmed; owner acceptance remains separate | @buenhyden |

### Remaining Conditions

Local implementation, focused RED/GREEN checks, scoped added-statement
coverage, same-input timing and independent review are complete. Hosted PR
required checks and requested implementation delivery are complete; owner
acceptance remains pending. No known P01 implementation defect is deferred
as runtime observation. No full repository suite or live service was run.
Existing P00 operational conditions are not closed by this CI task.
R01 1.2.0 repairs are implemented and locally verified; their hosted PR
result is recorded with the delivery. Owner acceptance remains pending.

## Handoff

### Promotion Receipt

Durable selection behavior belongs to the workflow contract and gate library;
parse/scope behavior belongs to the existing document libraries. Their tests
and actual consumers change with them. This Task is the only execution record.
Criterion 155/W171 is implemented by `59623b56`, corrected by `97cadafa`,
`2bcc4436` and `a6e797d0`, and integrated by `16d2be3f`. The workflow contract,
workflow, gate/document libraries and existing regression consumers listed
above are the durable targets. E33 verifies the actual hosted consumer and
E34 records delivery; the Criterion Decisions row deliberately remains pending.

P01-owned one-off timing and review prompt/result/log files were removed;
inline probes and temporary fixture directories left no tracked artifact.
The matching input package remains for P02 through P17. Persistent regression
tests, private request state, dependency caches and advisory Graphify output
are not cleanup candidates. No unrelated active work was deleted.

### Next Owner

After P01 verification and requested delivery, the next input is
`_workspace/workspace_governance_remediation_1_1_0_20261120/prompts/P02-LOCAL-FEEDBACK.md`.
Its prerequisite is P00 1.1.0's merged result and P01's maintained implementation,
verification and exclusions. Criterion 155 owner acceptance remains pending;
do not infer it from prompt entry, merge or this maintenance decision. Do not execute
P02 automatically. Preserve the matching package through P17; remove only
P01-owned one-off timing/test artifacts when finished.
