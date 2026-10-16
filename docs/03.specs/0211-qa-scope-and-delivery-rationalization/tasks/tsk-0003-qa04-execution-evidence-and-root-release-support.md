---
title: "QA04 Execution Evidence and ROOT Release Support"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-16"
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

## Criterion Acceptance

This support Task has no Criterion Acceptance table. SPEC-0211-TSK-0001 retains
the sole durable decisions for criteria1–5; all remain pending until their
current owner records an actual decision. W71–W74 provide supporting evidence
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
