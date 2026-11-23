---
title: "P07 Environment Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-20"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0105"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-20"
---

# P07 Environment Task

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Objective and Parent

Own criterion161/W177 in the [Spec](../spec.md) and [Plan](../plan.md).
Complete shared resource admission and owned execution recovery through the
existing Compose/LAB/dispatch paths; preserve verified environments.

##### Inputs and Authority

The direct P07-ENVIRONMENT1.1.0 request authorizes this current workspace,
scoped implementation, bounded environment observations and normal
commit/push/PR/merge. Matching README, P07, execution contract, confirmed
Q01–Q04, D07 and supplied sources plus Docker profile/findings are inputs.
No earlier package or another live workspace is required.

Initial root is runtime-resolved in the private binding, common-dir.git,
branch codex/p01-ci-evidence, HEADc98e4e4f8450de94cadadc064c428c78ea915112,
tree clean. Latest PR1138/1139 integrated P06; open1047/1048 are unrelated
Renovate updates and remain untouched. Brief P07-ENVIRONMENT-docker-1.1.0
revision1 initially covers this Task/Spec/Plan; implementation scopes must be
expanded before writes. Request249cb7d829fb4f34281fdbe2f79954a7, digest
f7c1e8782aa0edaf73cc70eca7775a94fd6dcb4170c3f35b34730a5a8a877202.
Direct user authorization is authority; this record and draft status are not. Revision2 binds
shared admission, LAB/Compose and dispatch implementation/test scopes; revision3
adds the cohesive dispatch_process library/test and current maintenance owner.
One writer owns each of those code slices; root owns Task/Spec/Plan, environment
and maintenance guidance, manifest and CI registration. No writer shares files.

The final source review found two missed failure conditions: pre-process spawn
failure could retain a worker reservation, and LAB readiness accepted an
exited-zero restartable service. Both now have durable regressions and repairs.
An evidence-table separator failure was also corrected; runtime LAB proof,
GitHub delivery and owner acceptance remain separate work.

#### Execution Log

##### Work Performed

Read current bootstrap/provider, matching inputs, actual source and P06 Task.
Two read-only discovery contexts trace existing runner and Compose consumers.
Graphify query/report is advisory: snapshot3ea422ae differs from HEAD and
inferred cross-root edges require tracked-source corroboration.

Preserve actual89-service inventory, explicit dependency/companion closure,
LAB footprints, existing numeric product limits and P06 selected native proof.
The real new defects are unlocked check/start races, missing pending resource
reservations and mandatory direct-start admission, non-atomic static LAB
ledger ownership, and dispatch Popen-before-PGID/identity recording. A pure
four-service discovery case separately permits split[a,b] and[c,d] at one
empty running snapshot while rejecting their combined set; durable RED/GREEN
verification remains implementation work, not a claimed current test PASS.

Shared admission uses a private user/host namespace rather than a per-clone
ledger; daemon identity scopes service inventory while numeric reservations
share the host store. Product LAB limits and existing disk reserve/manifest
estimates stay their owners. The canonical active maintenance guide owns
mutable helper operation; environment onboarding owns setup/boundaries. This
preserves the P05 typed authority contract without broadening the checker or
moving environment policy into agent surfaces.

The selected plain shell environment combines installed systemd user resource
control and Bubblewrap allowlisted filesystem/network access. A bounded dummy
host probe started Bubblewrap successfully; that is namespace readiness only,
not a source-write, Docker access or native model success. The existing P06
Codex/Claude routes are separately reused. Missing hard controls refuse this
managed shell route; unsupported capabilities are not hidden by an unrestricted
fallback. Provider-specific actual workers remain P12, not this shell probe.

##### Blockers and Decisions

No Q01–Q04 question is reopened. Current Linux, Docker29.9.2/Compose5.6.1,
Codex0.169.0 ChatGPT and Claude2.1.329 existing first-party Max are available.
Readiness uses public version/account-kind fields only. Managed tool access
to the Docker socket requires normal action approval; approved read-only
engine info succeeded. Do not mistake that tool restriction for daemon failure.

Existing configured LAB limits10CPU/27924MiB/max1/max1440minutes/readiness600s
and product0107 host reserve/external allowances remain distinct from measured
host capacity12CPU/33575419904bytes memory. Reuse these limits, do not infer
unlimited disk/native processes. Build bounded profiles and report actual
mechanisms, remaining quota limits and unobserved billing without fake PASS.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 161 | W177 | method=review; tool=-; command=- | Clean c98e4e4f; matching1.1.0 package/D07; Docker-only profile/findings, current entrypoints and owner documents | PASS | Actual root/common-dir/branch/HEAD and latest/open PRs read. Existing selection and native observations separated from actual admission/recovery defects. Discovery and design only, not implementation or live startup | required | - |
| E02 | 161 | W177 | method=observation; tool=-; command=read-only installed-version, account-kind, and Docker daemon observation | Current host public version/account fields and read-only daemon info | PASS | Linux6.8.0-147/x86_64; Python3.12.3, uv0.13.1, Node26.10.0, bubblewrap0.9.0; Docker engine29.9.2/Compose5.6.1/cgroupv2; existing Codex ChatGPT and Claude firstPartyMax login. Engine read needs normal approved host action. No container mutation, credential output or new model call | required | - |
| E03 | 161 | W177 | method=review; tool=-; command=- | TSK0104 E02/E07/E10 and source1138/receipt1139; current versions unchanged | PASS | Codex read-only-parent OS refusal/inheritance and Claude instrumented refusal plus separate routine Read/Grep/Glob review remain scoped. No P06 environment-only probe remains. Older Desktop/writable-parent failures remain failed/ineligible; no P08/P12 feature or whole-host isolation claimed | required | - |
| E04 | 161 | W177 | method=review; tool=-; command=- | Brief revisions2/3; actual existing89-service selection, LAB and dispatch callers | PASS | Three disjoint implementation scopes: shared admission/core tests, LAB/Compose consumers/tests, dispatch gated process lifecycle/tests. Root registers mirrored modules once and current mutable maintenance owners; no new runner or approval ledger. Actual semantic implementation and test results remain separate | required | - |
| E05 | 161 | W177 | method=automated; tool=Python3.12.3; unittest; command=python3 -m unittest tests.lib.ops.test_environment_admission | Shared core frozen693f0d8d753a6cdfc5a8448188cf84196b146e4283e9c9ac895bc6930877b402; actual34behavior tests | PASS | Initial missing-module RED observed by writer; final root run exit0/34tests0.295s. Separate-process split requests, conservative overlap, transaction callback, numeric/runtime budgets, live/unknown/token/daemon fencing, noTTLreclaim, malformed/private state and release-only recovery covered. Writer in-memory executable-line measurement457/498=91.77%, not branch/fullchild coverage. Verified closed operational records are deleted, not a completion history | required | - |
| E06 | 161 | W177 | method=observation; tool=Python3.12.3; actual local Docker/source/state paths; command=execution_admission(ROOT) against the actual host | Current actual host execution_admission() before a service start | FAIL | Factory could read actual local Docker/source but core rejected unsafe_state_directory: existing ~/.local/state is0775, while HOME0750 and .local0755; proposed execution directory did not exist. This is a real default-location implementation failure, not missing daemon/provider permission. Do not chmod existing user directories or relax private-path checks; fix all callers to one dedicated private base, then repeat only this readiness check | required | - |
| E07 | 161 | W177 | method=observation; tool=Python3.12.3; actual local Docker/source/state paths; command=execution_admission(ROOT) against the actual host | Real numeric retry after dedicated-private-base fix7c36ac50; actual local daemon/root inventory | FAIL | Retry exit0/private path works, actual89inventory/0active/0LAB; hostCPU10 with observed9 and memory headroom2000683008bytes. Source review finds its disk headroom2.384TB excludes the native worktree/state filesystem with about65.7GBfree. Do not treat exit0 as complete readiness. Include every participating filesystem and derive conservative minimum actual headroom; retain host ceilings and private checks | required | - |
| E08 | 161 | W177 | method=observation; tool=Python3.12.3; actual local Docker/source/state paths; command=execution_admission(ROOT) against the actual host | Core3045b7f0 and frozen factoryeb0852de; actual local host/root and all participating filesystems | PASS | Real retry exit0: actual89inventory,0active/0LAB, private base0700; original user .local/state remains0775. HostCPU10 with about1CPU headroom; memory29280436224byte ceiling and2000683008byte headroom; disk240226689024byte conservative ceiling and38704078848byte headroom across actual root/capture/state/Docker/HOME/LAB filesystems. New36core and multi-FS regressions protect both repairs. No service effect or host ceiling increase | required | E06,E07 |
| E09 | 161 | W177 | method=automated; tool=Python3.12.3; unittest; command=python3 -m unittest tests.lib.ops.test_environment_admission tests.lib.ops.test_dispatch_process tests.lib.ops.test_compose_start tests.validation.test_lab_controller tests.validation.test_work_dispatch | Frozen core3045b7f0, dispatcher9d608243/helper3521131c, LABeb0852de/Compose3e9d3931 and mirrored behavior tests | PASS | Core36PASS with91.83% executable coverage; root helper/dispatcher54run30.833s exit0 includes1opt-inNativeNOT_RUN (53executed); writer consumer147tests27.843sPASS. In-memory changed-line coverage LAB85.00%/Compose81.08%, helper82.46%/runner85.28%; not complete branch or native child coverage. Witnessed RED covers split races, reused PID, spawn-before-record, lost journal and multi-FS accounting; no coverage dependency/report created | required | - |
| E10 | 161 | W177 | method=automated; tool=repository registered gates; command=registered manifest, changed selector and surface-ownership checks | Initial staged18path source and new shared test registrations | FAIL | Existing manifest checker found new row/consumer ordering errors; gate explain and surface-ownership failed because new changed-root rules included mandatory roots rather than canonical optional consumer roots. Selector returned failure, no green fallback. Follow-up manifest check also correctly rejected declaring Compose as a direct core consumer when it actually calls the LAB factory; register only actual immediate imports. Fix registration only, preserve checker strictness and affected actual consumers | required | - |
| E11 | 161 | W177 | method=automated; tool=repository registered gates; command=registered manifest, changed selector and surface-ownership checks | Corrected staged manifest and workflow ownership overc98e4e4f | PASS | Script manifest valid; existing surface-ownership8tests0.465s exit0; changed-selector explain exit0 with bounded existing optional consumer roots and mandatory agent checks retained. No checker relaxation or dead import. Metadata111selected0violations; local links929documents/174selected0failures0warnings; governance0failures. Root joint5module run237tests61.484s exit0 with1NativeNOT_RUN,236executed | required | E10 |
| E12 | 161 | W177 | method=observation; tool=Python3.12.3; systemd user scope, Bubblewrap, shared admission; command=HYHOME_INTEGRATION=1 python3 -m unittest tests.lib.ops.test_dispatch_process.NativeShellBoundaryTests.test_actual_selected_shell_boundary_and_owned_cleanup | HYHOME_INTEGRATION=1 python3 -m unittest tests.lib.ops.test_dispatch_process.NativeShellBoundaryTests.test_actual_selected_shell_boundary_and_owned_cleanup; frozen actual production admission/full89inventory | PASS | Approved host execution exit0/1test6.284s. Real normal read/owned write and read-only minimal Git succeed; synthetic outside read/write, dummy Unix socket, host loopback endpoint and synthetic secret env are denied/absent. Actual systemd query confirms1CPU/512MiB/Tasks256/runtime20s plus control group; token scope and reservation cleanup verified. No model call, product start, real secret or production endpoint probe; plain shell isolation is distinct from P06 vendor CLI proof | required | - |
| E13 | 161 | W177 | method=observation; tool=Python3.12.3; Docker Compose5.6.1; preflight only; command=python3 scripts/operations/lab.py --env-file owned-private-env check p07-environment-probe | Owned temporary p07-environment-probe fixture using cached immutable Python image, before any service effect | FAIL | Existing lab.py check exit1: Compose5.6.1 rejects pids_limit32 with absent deploy.resources.limits.pids. This is a temporary fixture configuration failure before admission/start; no production mutation | required | - |
| E14 | 161 | W177 | method=observation; tool=Python3.12.3; Docker Compose5.6.1; preflight only; command=python3 scripts/operations/lab.py --env-file owned-private-env check p07-environment-probe | Same actual-root89 preflight after matching both explicit PID limits32 | PASS | Existing lab.py --env-file owned-private-env check p07-environment-probe exit0; selected one service0.1CPU/128MiB, problems empty. No new image download, secret/data mount or service effect. Actual startup/readiness/cleanup still due after source review; four owned fixture files and private data/env are temporary | required | E13 |
| E15 | 161 | W177 | method=automated; tool=Graphify AST-only local update; no LLM; command=graphify update . | Current P07 Python/source changes; existing ignored advisory graph | PASS | AST-only no-LLM update exit0,42161nodes73882edges1580communities; graph/report/html refreshed. Existing SQL/HCL parser dependencies absent and unrelated inferred/context coverage remain limitations. These are graph observations, not a fixed-count test, runtime proof or whole-repository semantic audit | optional | - |
| E16 | 161 | W177 | method=review; tool=Claude CLI2.1.329; existing first-party Max OAuth; opus5.5/high; direct context; Glob/Grep/Read only; command=- | Candidate patch over c98e4e4f; reviewer examined patch lines1–3405 and targeted searches | FAIL | Actual Claude CLI2.1.329, existing first-party Max OAuth, opus5.5/high, read-only Glob/Grep/Read tool catalog, direct context, 151.27s,14 turns, SDK estimate USD0.997988. Reviewer did not read test hunks3406–end or governing owner/probe inputs, so this is not full review. Confirmed H1: failed root start retains all free disk without recovery entrypoint; M1: disk check occurs outside admission transaction; M2: ProcessError/LabError escape. M3 timeout caller impact and low findings remain to trace. No raw stream retained | required | - |
| E17 | 161 | W177 | method=automated; tool=Python3.12.3; unittest; command=python3 -m unittest tests.lib.ops.test_environment_admission tests.lib.ops.test_compose_start tests.lib.ops.test_dispatch_process | Current working tree after E16 repairs; three affected modules | PASS | Focused exit0;96 tests,1 opt-in Native NOT_RUN,95 executed. Covers atomic minimum-plus-remaining disk reservation, no outside-transaction resample, structured domain failure, recovery token/CLI, exact controller stop, setup-failure rollback and project reconciliation; partial/unknown resources retain claim. Synthetic behavior only; no native recovery or LAB runtime acceptance | required | - |
| E18 | 161 | W177 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.ops.test_environment_admission tests.lib.ops.test_dispatch_process tests.lib.ops.test_compose_start tests.validation.test_lab_controller tests.validation.test_work_dispatch | Current P07 working tree after recovery and one-shot policy fixes | PASS | Focused five-module suite:249tests,1 opt-in Native NOT_RUN,248 executed; exit0 in58.101s. Covers setup cleanup, bounded diagnostics, one-shot recovery, exact resource accounting, LAB and dispatch regressions. Synthetic/local tests; does not prove live LAB start or human acceptance | required | - |
| E19 | 161 | W177 | method=review; tool=independent read-only reviewer; command=final review of staged and unstaged P07 diff | Current P07 repair delta, tests, owner and probe inputs | NOT_RUN | The first follow-up reviewer reached its usage limit, so that review did not run in that context. The equivalent independent review later completed as E32 | required | - |
| E20 | 161 | W177 | method=automated; tool=Python3.12.3; command=python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main | Current changed documents against origin/main merge base c98e4e4f | PASS | Exit0; selected111 documents,0 violations,0 transition overrides | required | - |
| E21 | 161 | W177 | method=automated; tool=Python3.12.3; command=python3 scripts/validation/check-document-links.py --mode all --changed | Current changed-document links and catalog pairs | PASS | Exit0;929 documents,9116 links,174 selected,0 failures,0 warnings | required | - |
| E22 | 161 | W177 | method=automated; tool=Python3.12.3; command=python3 scripts/validation/check-document-corpus-lifecycle.py --readiness | Current Stage 03 corpus and active-stage occupancy | PASS | Exit0; lifecycle violations0 and occupancy violations0. Overall readiness reports SPEC-0212 not-ready because assigned tasks remain open and criterion161 is pending; unrelated package readiness also remains open | required | - |
| E23 | 161 | W177 | method=automated; tool=Graphify AST-only; command=graphify update . | Current P07 Python/source changes and ignored advisory graph | PASS | Exit0;42161 nodes,73882 edges,1580 communities refreshed; no LLM. SQL/HCL parsers remain unavailable and graph semantics remain advisory | optional | - |
| E24 | 161 | W177 | method=automated; tool=repository local staged hooks; command=bash scripts/validation/run-ci-precommit.sh --mode local-staged | Initial staged P07 candidate before markdownlint and Ruff formatting repairs | FAIL | Exit1. File-size/conflict/YAML/secret checks passed; markdownlint found duplicate blank lines and angle-bracket fixture notation, Ruff requested formatting on seven Python files. Corrections were applied to the same candidate; no source functionality changed in these formatting fixes | required | - |
| E25 | 161 | W177 | method=automated; tool=repository local staged hooks; command=bash scripts/validation/run-ci-precommit.sh --mode local-staged | Current staged P07 candidate after markdown and Ruff formatting repairs | PASS | Exit0. All applicable hooks passed: size, conflicts, line endings, yamllint, markdownlint, Ruff format/check, secret scan, EOF and whitespace; other file-type hooks skipped because no matching staged files | required | E24 |
| E26 | 161 | W177 | method=automated; tool=Python3.12.3; command=python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main | Current Task candidate after E24/E25 insertion | FAIL | The evidence table was split by a blank line; checker reported `registered evidence table must be contiguous`. The blank line was removed without changing evidence content | required | - |
| E27 | 161 | W177 | method=automated; tool=Python3.12.3; command=python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main | Current changed documents after evidence-table repair; merge base c98e4e4f | PASS | Exit0; selected111, violations0, transition overrides0 | required | E26 |
| E28 | 161 | W177 | method=review; tool=independent read-only reviewer; command=final review of staged and unstaged P07 diff | Candidate before latest repair, including source and test diff | FAIL | Review found that Popen failure before returning a process could retain an identity-less reservation, and LAB readiness accepted exited-zero services without restart:no. Both findings were repaired and regression-tested | required | - |
| E29 | 161 | W177 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.ops.test_dispatch_process.SpawnFailureTests.test_popen_failure_releases_only_an_absent_owned_worker_reservation tests.validation.test_lab_controller.LifecycleTests.test_wait_ready_rejects_successful_exit_for_restartable_service | New regressions before repair | FAIL | RED confirmed both review findings: Popen failure retained the claim and exited-zero restartable LAB was accepted | required | - |
| E30 | 161 | W177 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.ops.test_dispatch_process.SpawnFailureTests.test_popen_failure_releases_only_an_absent_owned_worker_reservation tests.validation.test_lab_controller.LifecycleTests.test_wait_ready_rejects_successful_exit_for_restartable_service | Current repaired source and regressions | PASS | Exit0; both new regressions passed after the repairs | required | E29 |
| E31 | 161 | W177 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.ops.test_environment_admission tests.lib.ops.test_dispatch_process tests.lib.ops.test_compose_start tests.validation.test_lab_controller tests.validation.test_work_dispatch | Current repaired P07 source and all five affected modules | PASS | Exit0;252 tests run,1 opt-in Native skipped,251 executed;58.828s. This is local/synthetic proof, not native LAB acceptance | required | - |
| E32 | 161 | W177 | method=review; tool=independent read-only reviewer; command=final review of staged and unstaged P07 diff | Updated 19-file P07 candidate, both repairs and regressions, owner inputs and probe boundaries | PASS | Independent source review found no remaining source-level blockers. It confirmed exact reservation/scope checks for pre-spawn cleanup and restart:no enforcement for exited-zero readiness. It did not verify runtime, remote checks or human acceptance | required | E19,E28 |
| E33 | 161 | W177 | method=observation; tool=Docker29.9.2/Compose5.6.1; command=existing lab.py check/up/down/status path for p07-environment-probe | Owned temporary one-service fixture, cached immutable image, private env/data root; preflight then 10-minute lease | FAIL | Preflight passed with no external-container conflicts. Actual up reported `lab-p07-proof-1 is unhealthy` and the ledger entered failed state. Immediate project-scoped inspection found no container, so the healthcheck cause is unobserved. Owned down returned0; status records stopped/project_running=false | required | - |
| E34 | 161 | W177 | method=observation; tool=Docker CLI and existing Admission API; command=read-only post-cleanup ownership verification | The P07 probe token/project after owned down | PASS | Exit0; project reservations0, matching containers0, matching networks0. No volumes or images were deleted | required | - |
| E35 | 161 | W177 | method=automated; tool=repository local staged hooks; command=bash scripts/validation/run-ci-precommit.sh --mode local-staged | Final P07 candidate after review repairs and runtime evidence | FAIL | Exit1. All applicable hooks passed except Ruff format, which requested formatting in scripts/lib/ops/dispatch_process.py. Formatting was applied; functional tests are unchanged | required | - |
| E36 | 161 | W177 | method=automated; tool=repository local staged hooks; command=bash scripts/validation/run-ci-precommit.sh --mode local-staged | Final staged P07 candidate after Ruff formatting | PASS | Exit0. All applicable hooks passed: size, conflicts, line endings, yamllint, markdownlint, Ruff format/check, secret scan, EOF and whitespace; other file-type hooks skipped because no matching staged files | required | E35 |
| E37 | 161 | W177 | method=automated; tool=GitHub Actions candidate-quality; command=gh pr checks 1142 | PR#1142 head28fd01d4469c018204e294e62d9286bb3435477f; run45113476560 and uploaded candidate-core result artifact | FAIL | `leaf.repository-integrity-regressions` failed two `test_mutation_classes_follow_observed_script_behavior` subtests: the expected mutation map omitted the two new P07 runtime libraries. Other selected gate rows passed. This was a test expectation gap, not a source or manifest validation failure | required | - |
| E38 | 161 | W177 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_script_manifest.ScriptManifestTests.test_mutation_classes_follow_observed_script_behavior -v | Current P07 runtime manifest and updated mutation expectation map | PASS | Exit0; the existing behavior regression passes for the registered scripts, including both P07 libraries. It reproduces the failed CI assertion locally and verifies the correction; it does not resolve the separate hosted candidate-quality result | required | - |
| E39 | 161 | W177 | method=automated; tool=Python3.12.3; command=python3 scripts/validation/check-script-manifest.py | Current P07 script manifest and repository inventory | PASS | Exit0; script manifest valid | required | - |
| E40 | 161 | W177 | method=automated; tool=Python3.12.3; command=python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main | Current P07 Task and changed documents; merge base c98e4e4f | PASS | Exit0; selected109 documents,0 violations,0 transition overrides | required | - |
| E41 | 161 | W177 | method=automated; tool=Python3.12.3; command=python3 scripts/validation/check-document-links.py --mode all --changed | Current P07 Task and changed-document links | PASS | Exit0;929 documents,9116 links,3 selected,0 failures,0 warnings | required | - |
| E42 | 161 | W177 | method=automated; tool=Python3.12.3; command=python3 scripts/validation/check-document-corpus-lifecycle.py --readiness | Current Stage03 corpus and active-stage occupancy | PASS | Exit0; lifecycle violations0 and occupancy violations0. SPEC-0212 remains not-ready because open Tasks/criteria include criterion161; this is not a lifecycle validation violation | required | - |
| E43 | 161 | W177 | method=automated; tool=repository local staged hooks; command=bash scripts/validation/run-ci-precommit.sh --mode local-staged | Current staged P07 mutation-map repair and Task evidence update | PASS | Exit0; staged-file, conflict, line ending, Markdown, Ruff, secret, EOF and whitespace checks passed; non-matching file checks skipped | required | - |

##### Resolution Links

E08 resolves E06/E07 through the actual corrected readiness observation.
E11 resolves E10 through the existing registration and selection checks. E14
resolves E13 through the corrected fixture preflight. E17 records focused
synthetic checks for the H1/M1/M2 repairs; E16 remains the original incomplete
review. E25 resolves E24, E27 resolves E26, E30 resolves E29, and E32 resolves
the unavailable review attempt E19 and findings E28. E20-E23 record document,
lifecycle and advisory graph checks. E36 resolves the formatting failure E35.
E38 locally confirms the mutation expectation repair and E39 confirms the
registered manifest. Neither local check resolves the separate hosted
candidate-quality failure in E37; the same hosted check must pass on the new
head. The hosted candidate-quality rerun remains pending.
The bounded LAB start remains failed although owned cleanup passed; delivery
and human acceptance remain open. Prior failures stay recorded and are not
hidden by a successful alternative.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 161 | pending | E01,E02,E03 | Discovery, implementation and focused tests recorded; independent review, native runtime, delivery and human acceptance remain due. Intent undecided, accepted by nobody | @buenhyden |

##### Remaining Conditions

Focused synthetic regressions, durable owner updates and the corrected
independent source review are recorded. The hosted candidate-quality check
failed on two stale mutation expectations; their local repair and manifest
check pass, and the hosted rerun is still due. The owned single-LAB attempt
failed at readiness and its cleanup passed; its healthcheck cause is no longer
observable after the controller removed the failed container. Resolve that
cause and pass the bounded runtime case before accepting the criterion. Keep
actual human acceptance pending; retain live/uncertain reservations and
preexisting unrelated work.

#### Handoff

##### Promotion Receipt

Existing environment onboarding owns workspace setup and boundary semantics;
product policy/Compose/LAB own service limits and data; existing runners and
mirrored tests own execution. This Task owns execution evidence only. No new
permanent completion ledger or parallel runner is authorized.

##### Next Owner

Continue only P07. Identify matching P08 and prerequisites after actual P07
results; do not execute the next prompt. Keep the input package through P17.
Remove only owned disposable probes/results after durable recording; preserve
persistent regressions, private execution state and unrelated active work.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
