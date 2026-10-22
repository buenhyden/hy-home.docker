---
title: "QA04 Execution Evidence and ROOT Release Support"
version: "0.3.1"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-22"
layer: "specs"
artifact_id: "SPEC-0211-TSK-0003"
parent_ids:
- "SPEC-0211-PLAN-0001"
created: "2026-10-16"
---

# QA04 Execution Evidence and ROOT Release Support

## Overview

### Objective

Support the existing SPEC-0211 acceptance criteria with reproducible toolchain
identity, durable per-gate execution evidence from the existing runner, and an
explicit ROOT infrastructure promotion boundary in RUN-0009. This Task owns the
new QA04 Q4/Q6/Q7 support unit after the hosted-contract correction is integrated.
It owns no additional Spec criterion or Criterion Acceptance decision.

Preserve the single workflow contract and existing orchestration. Do not add a
workflow, permanent service, scanner, parallel registry, fourth hosted unittest
promotion, or per-event/service-count acceptance gate.

## Inputs and Authorization

### QA04 User Authorization

The user's execution prompt 04 on 2026-10-16 steers the continuing infrastructure
audit and expressly requests actual changed-profile, FULL-profile and
requirements validation, current remote-check evidence, toolchain and execution
identity, artifact custody, rollback, and release-stage separation. This is the
request-specific authorization for the actual FULL audit below. The ordinary
policy against mandatory full-profile repetition remains the default elsewhere.
Model-only selection, a prior unrelated run, or explain output does not satisfy
this user's actual FULL request. Valid same-input evidence remains reusable
elsewhere under the existing input, mode and trust-identity contract.

This source and QA work does not authorize operational credential use, real
datasets, ROOT/HOME mutation, release publication, protection/ruleset PATCH,
paid jobs, or broad cleanup. Current protection requires `candidate-quality`
from GitHub Actions App 15368 under a separately approved setting change.
Record fresh protection and effective-rule observations independently; source
changes do not authorize a remote correction or weaken the current check.

### Baseline and Dependency Boundary

PR 505/W70 integrated as main
`2de045e3b6f79967b4b4050e5cff53ee0b38158f` after exact head
`9bf618a80d192d974d494b164b8af4df07dfb6ae` passed the required
`candidate-quality`, CodeQL and GitGuardian checks. This Task starts from that
integration SHA. Do not rebase away prior receipt references. Preserve
Task0001's sole pending criterion decisions and Task0002's historical failures
and bounded source evidence.

The approved editorial input for ROOT promotion is identified by SHA256
`e573213186c5e9588708153803511e728e08e02059dd95994f040ef4abd795fc`.
It proposes one subsection and small Overview/Trigger/Verification amendments
to the existing RUN-0009. This is a review-input identity, not a temporary path
or independent policy authority. The implemented Runbook and its owning Task
become the reviewable canonical result.

### Ownership and Allowed Surface

The CI audit implementer is the sole source and Plan writer for this unit;
the root agent integrates and records delivery. Independent code/security
reviewers do not implement the reviewed change. The following is the bounded
candidate scope; add a file only when its actual caller contract requires it
and the reviewer receives the exact expanded diff:

- `scripts/validation/ci_gate_runner.py` and its existing CLI adapter
  `scripts/validation/run-ci-gate.py`.
- Existing contract/adapter owners in `scripts/lib/gate/` and
  `.github/workflow-contract.yml` only if the reviewed evidence interface needs
  their current registration or argv contract; no new gate or hosted promotion.
- `.github/workflows/ci-quality.yml` only for the existing job's bounded,
  secret-safe evidence handoff, retaining immutable Action pins and least
  privilege; no additional workflow or deployment job.
- Existing focused gate tests under `tests/lib/gate/` and
  `tests/validation/test_ci_gate_execution_context.py`,
  `test_ci_gate_model.py`, and `test_ci_gate_plan.py`.
- `scripts/requirements.txt`, `scripts/requirements-pre-commit.txt`, one
  derived hash-locked controller input, their actual CI install caller, and
  existing caller documentation/manifest registration required to keep that
  input selected and reviewable.
- `scripts/README.md` only for the existing dependency-install and local-tool
  caller contract; no user-global environment or installer mutation.
- `docs/05.operations/runbooks/10-platform-and-backup/0009-release-management.md`,
  this Task, and the co-located Plan. Read dependency manifests and existing
  supply-chain JSON owners; do not silently upgrade tools or alter image pins.

Native fixture/Plan/Task files owned by the workflow implementers, private
configuration, user-global hooks/tooling, and LAB runtime are outside this unit.

## Work Log

### W71 Toolchain Identity and Secure Artifact Contract

Source implementation and focused verification are complete; hosted artifact
publication remains `NOT_RUN` until an exact-head PR run. The focused work first
reproduced the confirmed absence or mismatch of the requested identity/custody
contract using focused RED cases. Derive
identity from the actual selected executable paths and bytes, interpreter/tool
versions, tracked dependency manifests and resolved allowlisted package
name/version inventory. Separate declared lock hashes from observed installed
dependency identity and record unresolved transitive reproducibility honestly.
Do not emit credentials, environment values, authenticated package URLs, or
private config. Do not install global tools or change global/builder settings.
Pin the hosted controller to Python 3.14.8, Node 24.22.0 and uv 0.12.18 with
the reviewed Linux x86-64 uv checksum. Disable setup-uv caching explicitly,
disable setup-node package-manager caching, and omit setup-python caching.
The one derived dependency lock must install with hashes on both supported
local Python 3.12 and hosted Python 3.14 without network-time re-resolution.

Bind source/base/head/merge or staged input, contract/configuration, mode/history
and trust context to the ordered execution plan. Hashes are dated observations,
not a claim that installed files became immutable. Review revalidation and
failure behavior when source, executable or dependency identity changes.

Define one bounded artifact contract consumed by the existing runner and
existing CI job: exact owned output directory, exclusive regular files,
0700/0600 ownership, no symlink/hardlink replacement, bounded sizes and safe
atomic persistence. Record sanitized structured metadata, UTC times, SHA256,
retention/custody and the owning Task. Raw logs, private paths and secrets must
not enter tracked evidence or public artifacts. Unknown publication/capture
state remains incomplete; a hard kill cannot be represented as a complete
receipt. Test path replacement, duplicate output, malformed identity,
secret-shaped values and stale/mismatched input without Docker or credentials.

Current receipt:

- The single generated controller lock installed with `--require-hashes` in
  isolated Python 3.12.3 and Python 3.14.8 environments; both resolved the same
  lock with its exact applicable package set and `zizmor==1.28.0`. The repository
  workflow pins Python 3.14.8, Node 24.22.0 and uv 0.12.18 plus the reviewed uv
  checksum, and disables uv/Node caches explicitly.
- The plan records captured Git/Python/uv versions and byte hashes, the four
  dependency input hashes, every applicable locked installed name/version and
  public ImageOS/ImageVersion/architecture. The runner image digest remains the
  honest `NOT_AVAILABLE`. A selected Node version is declared before setup and
  its observed version/hash is recorded in the result after setup.
- The evidence store tests include executable hash drift, bounded typed fields,
  path replacement, exclusive output, canonical JSON and plan/result/manifest
  hash linkage. The final focused seven-module batch ran 216 tests with zero
  failures; the typed workflow checker reported 5 workflows, 7 jobs and 9 pinned
  actions.

### W72 Existing Runner Per-Gate Execution Evidence

Source implementation and focused verification are complete and use W71. The
existing plan and executor were extended without a second runner. Before
dispatch, persist
the ordered selected gate IDs, registered argv/suites/timeouts, invocation
identity and every remaining gate as NOT_RUN. During actual execution record
per-gate UTC/monotonic timing, start/terminal status, exit or timeout/cancellation
classification and bounded artifact identity. Do not manufacture timing for an
unexecuted gate or turn an optional native skip into native PASS.

Preserve the existing first-failure exit, descriptor verification, closed
hosted set, authenticated event/Git/Python capture and process-group cleanup.
When `CI_GATE_EVIDENCE_DIR` is explicitly set for a normal local changed or FULL
run, bind the receipt to the clean tracked `HEAD`, a numeric local run identity
and observed local tools without projecting GitHub event or App identity.
Local `--requirements` remains unsupported because hosted prerequisites require
the authenticated pull-request merge topology.
On early failure/cancellation retain the actual terminal gate and all later
NOT_RUN nodes; a receipt-write failure or incomplete finalization is observable
and never masks the original failure. A hard-killed RUNNING node stays uncertain.
Focused RED/GREEN must prove success, early nonzero, timeout, cancellation,
partial/incomplete evidence, stale or wrong-input reuse and no duplicate
execution. Use harmless synthetic registered children for lifecycle tests.
Persist a STARTED or equivalent incomplete phase before child dispatch so a
hard kill cannot misreport the active leaf as NOT_RUN or fabricate an exit.

Current receipt:

- Candidate and main-security reuse the registered runner/adapter surfaces and
  upload only `plan.json`, `result.json` and `evidence-manifest.json` through the
  exact pinned evidence action for 14 days. Main-security separately records the
  existing `leaf.zizmor` invocation and the SARIF hash without copying SARIF into
  the evidence artifact.
- Focused lifecycle tests prove STARTED persistence, success, first nonzero,
  timeout, signal cancellation, later selected `NOT_RUN`, hard-kill incomplete
  state, stale input, directory replacement and original-failure precedence.
  Explicit local evidence binds a clean tracked HEAD and observed local tools;
  it does not project GitHub identity and does not admit local `--requirements`.
- Standard-library line tracing measured the whole new evidence module at
  702/832 executable lines (84.38%). The union of the 87-test full focused trace
  and the 25-test lifecycle/tool-identity trace measured the 19 changed runner
  evidence functions at 485/592 lines (81.93%). These are scoped line metrics,
  not branch or whole-repository coverage.

### W73 ROOT Release Boundary and Actual QA04 Evidence

The approved RUN-0009 editorial change is implemented on W72 while the final
integrated executions remain `NOT_RUN`. It preserves the repository SemVer producer and default
no-full-repeat rule. The actual ROOT image-promotion subsection requires
candidate artifact/build identity, same-digest scan/SBOM/signature/provenance
and platform identity, unit/contract, isolated native, stateful migrator rehearsal,
independent restore, explicit approval/promotion and HOME functional readback
as distinct evidence. Reviewed stateless N/A needs actual impact reasoning;
NULL/UNKNOWN/NOT_RUN and a merely complete ledger do not authorize promotion.
Reuse existing security ledger/verification and service Runbook owners, not a
new registry, scanner, build workflow or generic production command.

Reproduce the source-to-consumer/test/gate planning joins from the existing
operations catalog, independent ROOT source parser and CI selector. Keep all
service rows' original consumer/recovery/operations/update-owner authorities.
Record current 13-layer coverage, selected leaf argv/timeouts/suites and
before/after path counterexamples, including unknown/delete/rename behavior.
Counts and model assertions describe that input only and prove no runtime flow.

On the final integrated source run the actual changed and explicit FULL
profiles plus their requirements paths under the reviewed owned toolchain.
Record exact commands, selected and unselected nodes, input SHA, duration,
exit/result, legitimate skips and earlier failures. Do not substitute model or
explain output for execution. Keep within the Task's recorded time/RAM/disk
budgets; an interrupted audit remains partial with remaining gates NOT_RUN.

Observe candidate-quality, CodeQL and GitGuardian at the actual final PR head,
then separately observe main-security at the actual merged SHA. Record check
issuer/App identity, run/job/head and pending/missing/failed results honestly.
Record the current strict App-bound required check and empty effective rules
without claiming workflow-source immutability or remote tamper-proofing. No
PATCH or synthetic enforcement smoke runs occur under this Task. Actual
deployment/native/migration/restore/HOME receipts remain with their service
Tasks and are not created by local QA.

Current receipt:

- RUN-0009 is frozen at source SHA256
  `fa9c4453a77da423762e57214662e4ad400eaa34340b549f8b716cbfef14feba`.
  Markdown, 11 links, 9 unchanged Bash blocks and diff checks passed; the final
  exact-file metadata check remains required before E05 can pass.
- E07, E08 and E09 remain `NOT_RUN`. They require the final integrated 0204 plus
  W71/W72 source, actual changed/FULL execution and requirements/current-head
  remote observations. This source delivery does not relabel those future
  receipts or close the Task.

### Hosted PR 508 observations

The first hosted runs of PR [#508](https://github.com/buenhyden/hy-home.docker/pull/508)
exposed four defects that local focused tests could not reach. Each fix is a
separate logical commit on the PR branch.

1. The hosted `setup-python` interpreter is installed `0o100777` and owned by
   the runner user, so the group/other-write rejection failed with `EPERM` on
   every hosted run. The capture steps now remove group and other write
   (`chmod go-w`) from the resolved `python3` and `uv` before hashing, and the
   workflow contract pins that command. The rejection itself is unchanged.
2. `leaf.compose-baseline-regressions` passes 80 explicit module arguments, but
   the evidence row bound was 64. The bound is now 256, with an accepted
   81-argument regression and a rejected 257-argument case.
3. `scripts/lib/gate/ci_gate_evidence.py` had no script-manifest row.
4. `tests.lib.gate.test_ci_gate_evidence` was not reachable from the full
   profile; it now runs in `leaf.ci-gate-contract-regressions`.

Diagnostic messages now name the OS reason, file mode, and failing gate ID;
they expose no path content or secret value. These observations do not run
E07 or E08 and do not change any criterion decision.

### Local FULL observations on main

Two local `python3 scripts/validation/run-ci-gate.py --profile full` runs on
main `875d77c45` are recorded as observations, not as E08: E08 requires the
final integrated input.

1. Run 1 took 43:51 wall clock with a 180 MB peak RSS and exited 254. The
   checkout was created under umask 002, so tracked helpers were mode 664 and
   the existing group-writable rejection stopped an OpenBao issuance test.
   The owner set umask 022; the agent removed group write from tracked files.
2. Run 2 took 39:31 with a 177 MB peak RSS and exited 1: 773 tests ran with
   one failure. `test_registry_high_water_is_not_below_repository_history`
   scanned every local ref and found SPEC-0246 on the unmerged branch of
   PR #512, so it reported `registry high_water=245 observed=246`. The same
   test failed the same way in the records of SPEC-0224, SPEC-0231, SPEC-0232,
   SPEC-0235 and SPEC-0204. The full-history metadata gate run alone on the
   same main reports the same finding in 171 s.

### W74 Real-Tree Test Duplication

A per-test profile of the document-governance and lifecycle modules (940
tests, 1,929 s run in isolation) showed six tests taking 794 s. Each one ran
a real-tree check that the full profile already runs as a gate, or ran it
more than once. Each test now keeps its rule, checked once or against a
fixture:

| Test | Before | After | Change |
| --- | --- | --- | --- |
| `test_reference` fragmented in-progress evidence | 264 s | 134 s | The package load is the control; the second real-tree contract run is removed |
| `test_reference` workspace inventory coupling | 127 s | under 1 s | The rule moved to `_workspace_inventory_findings()` and is called directly |
| `test_profile` current Requirement packages | 124 s | under 1 s | The `check-contracts` subprocess is removed; `leaf.repo-document-metadata` runs it |
| `test_links` repository modes | 118 s | 56 s | One `--mode all` run replaces four processes; the non-mutation check is kept |
| `lifecycle/test_public` default route (two tests) | 160 s | 88 s | One run checks both the legacy-contract mock and the report lines |
| `test_identity_history` high-water against history | real-tree `--all` scan | under 1 s | A synthetic issued set pins `identity-history-regression` at `high_water + 1` |

`test_lab_isolation.test_a_lab_service_cannot_be_targeted_through_the_root`
is removed. Its nine root renders are implied by the wildcard root render,
which already proves that no LAB service is in the root model.

The full-history gate still scans every ref, so local FULL on main fails
while another branch holds a newly allocated identity. Whether that scan
should cover only refs reachable from HEAD is an owner decision; this Task
does not change it.

The local changed profile on this branch did not reach a clean result in
either available interpreter, and every failure is environmental:

- System Python 3.12.3 (Ubuntu `jsonschema`, no `referencing`): every suite
  through the 1,051-test suite passed, including the 152-test metadata suite
  in 261 s (589 s in FULL run 1) and the 773-test suite in 1,041 s. The
  525-test suite failed with 16 failures and 17 errors: 17 modules could not
  import `referencing`, and `gen-secrets.sh` ran the embedded checks with the
  `python3` found first on `PATH`.
- Python 3.14.8 from `uv`, with `scripts/requirements-controller.lock`
  installed with hashes in a scratch environment: those 205 tests passed. The
  1,051-test suite then failed with 11 errors in the OpsFlow CA tests, because
  this interpreter's OpenSSL lists no default CA certificates; they pass on
  the system interpreter.

No failing test exercises a file W74 changes. Both local FULL runs on main also
used the system interpreter, while hosted CI uses Python 3.14.8 with the
controller lock, so local FULL has not matched the hosted toolchain; the
runner records the interpreter but does not reject a mismatch. That check is
a follow-up outside W74. The hosted changed profile on the PR is the
authoritative result for this branch.

### W75 Local FULL Reproducibility

The owner asked on 2026-10-16 to review and proceed with the open W74
decisions.

- Identity history scope. `check-contracts --history-scope full` scanned every
  local ref, so FULL on main failed while any other branch held a new
  allocation, and hosted checkouts with `fetch-depth: 0` see every pushed
  branch. The scan now covers commits reachable from HEAD, and the
  `collect_issued_identities` default matches. An unmerged allocation on
  another branch still meets the Registry `high_water` line as a merge
  conflict, and the strict up-to-date rule makes the branch re-run this scan
  over main's history. Stage 99 states this scope. A fixture with an
  allocation only on another branch reads 98 by default and 99 with `--all`.
- Local toolchain check. A LOCAL run that executes gates now fails with
  `ci-gate-local-toolchain` before running anything when the interpreter
  differs from the `python-version` pin in `ci-quality.yml`, when an active
  `requirements-controller.lock` package is missing or at another version, or
  when the build lacks the memfd seal constants. The last case is the `uv`
  standalone 3.14.8 build, which failed the OpsFlow CA tests in E23.
  `--explain` is not an execution and is not checked. The hosted build from
  `actions/python-versions` (`python-3.14.8-linux-24.04-x64`) with the lock
  installed passed the 205 tests and the OpsFlow modules that failed in E23.
  The quality policy describes the check.
- PostgreSQL rehearsal. Every HOME PostgreSQL service is on 18.6; the only
  PostgreSQL 17 is the LAB cluster (`spilo-17`), so the 17 to 18 logical
  upgrade rehearsal of RUN-0032 still has a consumer and stays a regression.
  The full profile runs only `--check-config-only` and unit tests, neither of
  which starts a container. A stale comment naming 17.6 is corrected. Moving
  the target pin from 18.4 to the HOME 18.6 digest needs a real rehearsal run
  and stays with the SPEC-0204 SEC01 Task-pinned image updates.

The changed profile on this branch then passed locally for the first time,
with the hosted build (RUNPATH set to `$ORIGIN/../lib` so it runs outside
`/opt/hostedtoolcache`) and the controller lock: every suite passed in
2,666 s with a 181 MB peak RSS, including the 774-test suite in 1,156 s and
the 1,051-test suite with 80 skips.

### v28 local continuation preflight — 2026-10-22

The user expressly requested completion of remaining v28 local implementation,
Python toolchain recovery and actual full QA, reusing completed work. Operational
changes, real token revocation and remote PR/push remain outside this execution.
The existing 2026-11-15 D1 deadline remains unchanged; improvement proposals do
not constitute a new risk acceptance. W73/W75 provide the existing QA owner;
this continuation adds no criterion or second orchestration surface.

- Input: branch `codex/v28-local-residuals`, prior implementation through
  `016c4ac6e`; final clean HEAD will be captured by the existing runner after
  current B1 and public supplier observations are reviewed and committed.
  Reuse the six existing logical commits and their valid scoped evidence.
- Plan: actual `run-ci-gate.py --profile full`, LOCAL trust context, all 33
  selected registered executable leaves, with the existing per-gate timeouts
  (300–2700 seconds). `--explain` is selection evidence only. The selected
  prerequisites are Python, controller lock, Node and Docker. Hosted-only
  frontend/dependency audit/style/commit leaves remain excluded by the contract;
  native/HOME opt-in flags remain disabled. `--requirements` requires an
  authenticated PR context and is NOT_RUN locally; do not forge that context.
- Tools: official `actions/python-versions` Python 3.14.8 Ubuntu 24.04 x64
  release `3.14.8-36806082737`, archive SHA256
  `fa74abc70a55c10f6631967784878704eef81bbde9b8ec27469534f6ba997cb3`;
  API digest and official checksum file verified. Scratch venv has all 36
  exact controller-lock packages installed with hashes and binary wheels.
  Lock SHA256 `d05a5fb50e29e3d44587b34abacf2713eaea83c7c88ff84127d9cbfe96a193e2`.
  Real memfd `F_ADD_SEALS` self-check returned seals 15; local toolchain
  mismatch check returned None. The original Python executable SHA256 was
  `a5230d8adbd26c2185d77fb003597c4ee9c44c2369fc179122ff7c3a3a58ae59`;
  scratch-only RUNPATH relocation to `$ORIGIN/../lib` produced
  `62e177f6f9523e24ae0591438b7556e14c58fea1219a5c449615e3ff9d2e12ed`.
  Sanitized-environment executable capture passed. Verified official uv 0.12.18
  and Node 24.22.0 archives respectively hash to
  `89eadd7c76fc063887959510d5ba0ab1264dfd5f1143b925ddb73021a40acf16`
  and `cc2f601cee82d9a5a233302fe307abc600727035fd7d2c3a3571755989e95008`.
  Their executable SHA256 values are
  `b97ae0e1ed3661fcd0c446cc59d81f5720c24d35627b21814a7581fb67eba673`
  and `67ca5783febb8bf85736c79fcdd92c8d6d465a0eb2a082672bcdfa76a506751c`.
  Bundled npm is 11.19.1; no project dependency or browser install was selected.
- Permission: repository and `/tmp` writes only; public official downloads
  are scoped toolchain/research inputs. No user-global configuration change.
  Current read-only Docker prerequisite observation returned permission denied
  at `/var/run/docker.sock`; do not widen daemon permissions. A blocked Docker
  leaf must retain its failure and remaining leaves their actual states.
- Budget: UNKNOWN. Failure owner: root QA coordinator; one narrow retry per
  diagnosed slice, preserve original failure, never weaken assertions or fake
  interpreter/seal/CI identities. Keep stdout/stderr and existing runner
  receipts under private `/tmp/hyhome-v28-*` custody; local scratch retention
  does not establish durable hosted artifact or operational acceptance.
- Writers: root owns this QA Task and final integration; B1 worker owns the
  maintenance helper, caller-required source pins, existing tests and RUN-0085/
  SPEC-0243 evidence; supplier worker gathers public metadata in `/tmp` only.
  Independent review is read-only. Freeze repository writers before clean-HEAD
  execution and normal hooked commits.

### v28 local CLI evidence initialization correction — 2026-10-22

Preflight found that `CI_GATE_EVIDENCE_DIR` on an actual LOCAL CLI run built
an execution request and immediately opened a plan that had never been seeded.
Only the PR-only `--requirements` route seeded it; manually prepared test plans
had hidden the missing local route. The user-authorized QA continuation owns
this small W72/W75 repair in the existing runner and execution-context test.
The local branch now seeds the verified plan using the same captured request
before executing it. PR prerequisite/execution behavior, clean-HEAD identity,
private output custody, existing-path rejection and per-gate terminal states
retain their existing owners and checks. No second runner or new gate is added.
Focused RED/GREEN, registered regressions and independent review are recorded
with the actual results below; this paragraph itself asserts no QA PASS.

The new actual-descriptor CLI test first failed with
`ci-gate-evidence-invalid: evidence output must be a private regular directory`
on the unmodified local route, then passed after the two-line seed guard.
Pinned Ruff 0.15.12 check and format check passed. A worker's wider synthetic
run reported a sandbox-only hosted-topology error: this sandbox maps system
Git ownership to UID 65534, while the trusted-host guard requires UID 0.
The guard was preserved. Root's actual-host rerun of the registered runner
regression selection (`tests.validation.test_ci_gate_model`,
`tests.validation.test_ci_gate_plan`,
`tests.validation.test_ci_gate_execution_context`, `-q`) passed all 82 tests
in 18.806 seconds, exit 0. No Docker or live provider was used in this rerun.
The reviewed two-file diff SHA256 is
`49a194bd642e4f116f1b5a85e0d9cb8a3f075c0007847ec6ea1bff88044c2590`.
Independent code/security review approved that exact two-file source diff
with no blocking findings; its scope excludes the later full/Docker result.

Actual-host read-only prerequisite observations supersede only the earlier
sandbox availability failures: `/usr/bin/git` is UID 0, mode 0755; Docker is
29.8.2. The exact pinned Conftest image is already local. No container exists
for project `hyhome-conftest-gate` or fixed name `/conftest`; these observations
do not themselves authorize another project or operational mutation. Requested
FULL QA may use the registered network-none, read-only public-source Conftest
job after independent readiness review. Native/HOME opt-in cases remain off;
no image pull, HOME service start, token operation or remote action is included.
The runner receives actual local context and captures its own tool identities.

### v28 actual FULL terminal result and bounded continuation — 2026-10-22

The actual LOCAL full-profile invocation on clean implementation HEAD
`d7bec9a9a4318caa60cc0f5f99a1de6cfa71a580`, official hosted Python 3.14.8,
controller lock, uv 0.12.18 and Node 24.22.0, ended exit 1 after 2679.66 seconds:
26 registered gates PASS, workflow-contract regressions FAIL, six later gates
NOT_RUN. This is a failed full invocation, not aggregate PASS. The retained
plan/result and log are under `/tmp/hyhome-v28-full-d7bec9a9a-umask022-20261022`.
LOCAL identity records base_sha NOT_AVAILABLE; candidate preflight separately
used main `73433adc1b685582741604d8acc1f6f70be0adbe` as its comparison base.

The failing 44-test module had one failure: its explicit required-selector
expectation omitted the already registered Prometheus isolated-restore and
OpenBao TLS modules. Both modules remained required, before the opt-in skip
boundary, and their Compose baseline gate passed. The exact literal expectation
was extended by two lines; no assertion was weakened and no expected value
was derived from the actual contract. The failed test then passed, and the
same registered 44-test module passed in 11.553 seconds, exit 0, no skips.
Pinned Ruff 0.15.12 lint/format checks passed. Independent source review approved
diff `cb1e0d13b427895ba2dcd5889772d086b50ad8b56b4275e89ded032bd8bdd1c3`.

The user's latest request explicitly requires reuse of completed verification
and completion of the remaining QA. Continue the six NOT_RUN registered nodes
through the existing runner's verified-plan/evidence APIs on a new clean HEAD;
do not replay the 26 unaffected successes or disguise separate invocations as
one successful FULL process. Node IDs, argv, cwd, mode, trust, toolchain,
source/config differences and actual per-slice results must stay explicit.
Documentation reconciliations receive their affected metadata/link/style checks;
no implementation, image pin, native opt-in or runtime configuration is changed
by those documentary corrections. Budget UNKNOWN, original node timeouts apply,
one narrower retry per diagnosed slice; root owns failures and the final record.
Conftest completed in its isolated project; post-run container and network
queries for `hyhome-conftest-gate` returned empty. No HOME change or token
operation was executed. Operational/remote actions remain separate selections
for later explicit approval after local delivery; token revocation is excluded.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0211-TSK-0003 | draft | ready | #qa04-user-authorization |
| SPEC-0211-TSK-0003 | ready | in-progress | #w71-toolchain-identity-and-secure-artifact-contract |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E00-W70-integration | 2, 3, 5 | W71 | hosted-contract-prerequisite | PR 505 head `9bf618a80d192d974d494b164b8af4df07dfb6ae`; main `2de045e3b6f79967b4b4050e5cff53ee0b38158f` | PASS | Task0002 and exact-head remote checks | required | - |
| E01-toolchain-red-green | 2, 3, 5 | W71 | exact-toolchain-dependency-identity | Post-W70 reviewed source and selected tools | PASS | Work Log: W71 | required | - |
| E02-artifact-custody | 3, 5 | W71 | secure-bounded-evidence-contract | Owned synthetic output and hostile path cases | PASS | Work Log: W71 | required | - |
| E03-runner-terminal-states | 2, 3, 5 | W72 | per-gate-execution-evidence | Existing runner success/failure/timeout/cancellation cases | PASS | Work Log: W72 | required | - |
| E04-remaining-not-run | 2, 3, 5 | W72 | durable-early-stop-evidence | Partial execution and interrupted receipt | PASS | Work Log: W72 | required | - |
| E05-release-docs | 3, 4, 5 | W73 | root-promotion-boundary | Existing RUN-0009 and current supply-chain owners | NOT_RUN | Work Log: W73 | required | - |
| E06-source-selection | 2, 5 | W73 | service-and-path-selection-joins | Final source closure and before/after path cases | NOT_RUN | Work Log: W73 | required | - |
| E07-actual-changed | 2, 3, 5 | W73 | qa04-changed-and-requirements | Final integrated input and reviewed toolchain | NOT_RUN | Work Log: W73 | required | - |
| E08-actual-full | 2, 3, 5 | W73 | qa04-explicit-full-and-requirements | Same declared final input and full audit mode | NOT_RUN | Work Log: W73 | required | - |
| E09-remote-current-head | 3, 5 | W73 | exact-head-remote-and-protection-observation | Final PR and merged-main identities | NOT_RUN | Work Log: W73 | required | - |
| E10-independent-review | 2, 3, 4, 5 | W73 | final-source-and-evidence-review | Frozen logical diff and actual receipts | NOT_RUN | Review and Completion | required | - |
| E11-hosted-toolchain-mode | 2, 3, 5 | W71 | hosted-toolchain-identity | PR 508 runs `38855633760`, `38857315650` | FAIL | `EPERM`: interpreter mode `0o100777`, owner is runner | required | - |
| E12-hosted-toolchain-mode-green | 2, 3, 5 | W71 | hosted-toolchain-identity | PR 508 run `38857640474` after `chmod go-w` capture | PASS | Prerequisite selection passed | required | E11-hosted-toolchain-mode |
| E13-hosted-argv-bound | 2, 3, 5 | W72 | hosted-evidence-row-bound | PR 508 run `38857498273` | FAIL | `leaf.compose-baseline-regressions` argv 81 exceeded 64 | required | - |
| E14-hosted-argv-bound-green | 2, 3, 5 | W72 | hosted-evidence-row-bound | PR 508 run `38857640474` after the 256 bound | PASS | Evidence rows accepted; changed validation started | required | E13-hosted-argv-bound |
| E15-manifest-row | 2, 5 | W72 | script-manifest-coverage | PR 508 run `38857640474` | FAIL | `manifest-record-missing` for `ci_gate_evidence.py` | required | - |
| E16-manifest-row-green | 2, 5 | W72 | script-manifest-coverage | `check-script-manifest.py`; PR 508 run `38858240031` | PASS | No manifest finding | required | E15-manifest-row |
| E17-full-profile-reachability | 2, 5 | W72 | full-profile-test-reachability | PR 508 run `38858240031` | FAIL | `test_ci_gate_evidence` unreachable from the full profile | required | - |
| E18-full-profile-reachability-green | 2, 5 | W72 | full-profile-test-reachability | `test_surface_ownership`; PR 508 run `38860325987` | PASS | 955 tests OK (79 skipped) | required | E17-full-profile-reachability |
| E19-local-full-main-umask | 2, 5 | W73 | local-full-observation | `run-ci-gate.py --profile full` on main `875d77c45`, run 1 | FAIL | Work Log: Local FULL observations on main, item 1 (exit 254, 43:51) | required | - |
| E20-local-full-main-refs | 2, 5 | W73 | local-full-observation | Same command on the same main, run 2 | FAIL | Work Log: Local FULL observations on main, item 2 (1 of 773 failed, 39:31) | required | - |
| E21-full-test-profile | 1, 2 | W74 | per-test-timing | 940 document-governance and lifecycle tests run in isolation | PASS | Work Log: W74 Real-Tree Test Duplication (six tests, 794 s) | required | - |
| E22-real-tree-dedup | 1, 2 | W74 | focused-red-green | Seven rewritten tests; ruff check and format | PASS | Work Log: W74 Real-Tree Test Duplication (all pass; 515 s removed) | required | - |
| E23-local-changed-branch | 1, 2 | W74 | local-changed-profile | `run-ci-gate.py --profile changed` on `4500700ea` in system 3.12.3 and `uv` 3.14.8 | FAIL | Work Log: W74 Real-Tree Test Duplication (environment-only failures; hosted result pending) | required | - |
| E24-history-scope | 1, 2 | W75 | focused-red-green | `test_default_scan_ignores_an_unmerged_branch_allocation`; `check-document-metadata.py --mode check-contracts --history-scope full` | PASS | Work Log: W75 Local FULL Reproducibility (fixture 98 versus 99; gate violations 0 in 144 s) | required | - |
| E25-local-toolchain-check | 1, 2 | W75 | focused-red-green | `LocalToolchainTests`; `test_local_run_with_a_mismatched_toolchain_executes_nothing`; runner on system Python 3.12.3 | PASS | Work Log: W75 Local FULL Reproducibility (system run stops with `ci-gate-local-toolchain`) | required | - |
| E26-local-changed-hosted-build | 1, 2 | W75 | local-changed-profile | `run-ci-gate.py --profile changed` with hosted Python 3.14.8 and the controller lock | PASS | Work Log: W75 Local FULL Reproducibility (exit 0, 2,666 s) | required | - |

## Criterion Acceptance

This support Task has no Criterion Acceptance table. SPEC-0211-TSK-0001 retains
the sole durable decisions for criteria1–5; all remain pending until their
current owner records an actual decision. W71–W75 provide supporting evidence
for criteria2–5 without adding, accepting, rejecting or reassigning a criterion.

## Review and Completion

Keep this new Task draft at initial issuance. Completion requires focused
RED/GREEN for the changed behavior, relevant actual registered checks, independent
source/security review, protected artifact correctness, actual requested
changed/FULL/requirements results and current remote observations. Any missing
required execution stays open; a result-only continuation revalidates only its
affected source/docs and does not replay unrelated valid slices.

Commit W71, W72 and W73 as independently reviewable logical units when feasible;
record a coupled-unit reason if their small source/evidence interface cannot
stand alone. Normal hooks remain enabled. Before shared-worktree commits,
coordinate paused writers or use a clean staging worktree because hooks may
auto-stash foreign unstaged work. Preserve existing owners' bytes and receipts.
Root records exact source/merge SHAs, current check results, custody/retention,
rollback and blocker owners; no commit or remote publication is implied by
this proposal.

This Task was issued `draft` in `14fd25d1f` as required and merged by PR #508. Its recorded authorization and executed W71/W72 work make `in-progress` the current state; W73 evidence E05–E10 remains NOT_RUN and no criterion decision changes.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Existing acceptance owner](tsk-0001-qa-scope-and-delivery-rationalization.md)
- [Hosted contract prerequisite](tsk-0002-hosted-contract-and-tier13-hardening.md)
- [Release Runbook](../../../05.operations/runbooks/10-platform-and-backup/0009-release-management.md)
- [Dependency update policy](../../../05.operations/policies/10-platform-and-backup/0086-dependency-version-management.md)
