---
title: "Opsflow Notifier Recovery Task"
version: "0.5.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-05"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0044"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-02"
---

# Opsflow Notifier Recovery Task

## Overview

This Task owns the approved P05 local notifier source, isolated test and
handoff evidence. It is distinct from historical SPEC-0204 P05 and does not
cancel or rebuild its accepted n8n C19/C22 queue/schedule scope.

### Objective

Implement bounded manual no-send reprocessing, restored/in-flight recovery
safety and selected notifier credential refresh. Reuse the existing queue,
schedule and storage contracts; add no new binary consumer or storage service.

## Inputs and Authorization

The direct approved P05 plan authorizes local source, configuration,
documentation, owned synthetic isolated tests, independent review and a normal
local logical commit. Observed start: clean HEAD
`e14ebe0fd5e562f8c7557bd9408a1985d9971c5c`, initially on
`codex/p04-opsflow-data-path`. The CI writer subsequently created
`codex/p05-n8n-outbox-recovery` at the same parent without losing document
changes. These are observations, not required future constants.

Operating services, actual credentials, host changes, external mail delivery,
external repositories and remote integration are excluded. Shared MNG Valkey
remains the default. P04 remains TEST_RESIDUAL; its full Worker/restore result
is not a hidden prerequisite for independent P05 source/fixture work.

Governing inputs: REQ-0027, AD-0031, the approved SPEC-0212 Spec/Plan,
current notifier/SQL/fixture source and the preserved SPEC-0204 C19/C22 record.
Historical 2.43.6 acceptance, current declared/cached image and private workflow
state are separate evidence. Private bodies and actual secrets are not read.

## Work Log

### Issued single-writer leases

Each writer records exact existing-path fingerprints before editing; new paths
record ABSENT. Changed shared input pauses only the affected slice. Actor names
below grant no account or operating permission. Acceptance owner, writer,
reviewer, data owner and operational accepter remain separate.

| Scope | Single writer | Independent review | Boundary |
| --- | --- | --- | --- |
| New SQL007/008 and directly related SQL tests | `/root/p04_pipeline` reused as P05 SQL writer | code/security/SQL reviewer | Existing manifest-pipeline SQL directory, new migration/check files only; issued001–006 unchanged |
| OpsflowSmtp TypeScript, Node tests and directly required workflow generator/export | `/root/p04_uri` reused as P05 Node writer | code/security reviewer | Existing manifest-outbox-notifier package; exact path receipt before edit; no unrelated workflow or credential producer |
| Owned synthetic native fixture, optional authenticated Mailpit STARTTLS profile and P12 seam compatibility | `/root/p04_native` reused as P05 QA writer | independent QA/security/IaC review | Coordinate profile path with Node writer first; no Node/SQL test ownership overlap, no actual delivery or HOME credentials |
| Spec/Plan, this Task, DATA-0096 and scoped living notifier/n8n documents | `/root/p04_docs` reused as P05 documentation writer | independent document review | Existing evidence owners reused; no completed Task body or P04 acceptance rewrite |
| New Docker-free scenario regression file | `/root/p04_pipeline` under a separate root-issued QA lease | independent QA review | Only new tests/validation/test_p05_opsflow_scenario.py; ABSENT baseline; no edit of native author source or other tests |
| CI selector/script manifest registration | `/root/p03_docs_impl` | independent CI review | Exact registration slices only; projection/catalog writer remains separate from living-doc writer |
| Current source-preparation receipt/hash parity | `/root/p04_infra` assigned as P08 source-preparation writer | independent supply-chain/source review | Exact canonical receipt only; documentation writer does not own this correction or image updates |

### Exact initial source path packets

- SQL writer `/root/p04_pipeline` owns new
  `infra/07-workflow/airflow/workloads/manifest-pipeline/sql/007_notification_recovery.sql`,
  `sql/008_checks.sql` in that same directory, and new
  `tests/validation/test_p05_notification_recovery.py`; all were ABSENT.
  Predecessor005 remains
  `85eb63d22f2967ac84996f561a14ca3433e429eaf55a597d294478e21dfe00c2`
  and006 remains `38eb6b22e99e573c40cd1fa920af7a3cc5945d0ce0a53e9d2872983834c0ef76`.
  The approved management APIs are
  `requeue_dead_notification(bigint,integer,uuid,text) → boolean` and
  `quarantine_restored_notification(bigint,integer,uuid,text) → boolean`;
  final parameter semantics, grants and evidence are owned by this SQL writer.
- Node writer `/root/p04_uri` owns the existing OpsflowSmtp package source:
  `OpsflowSmtp.node.ts` before
  `eb4c88949d5b9547a2572754c46275e921e60232f5032c82ddf293701915f146`,
  `transport.ts` before
  `7b685f776d9d0475aa5cb164b9088218353820524a1d82a8b4b47c99433159f6`
  and directly affected Node/adapter/protocol/transport tests. The new
  `tests/starttls.test.cjs` was ABSENT. Existing factory argument4 remains
  compatible; capture profile is argument5, with explicit `mailpit-plain-v1`/`mailpit-starttls-auth-v1`
  selection for fixed `mailpit:1025`. The original public export retains the plain default; the authenticated fixture selects its profile explicitly.
- QA writer `/root/p04_native` owns new
  `tests/validation/_p05_opsflow_native.py`, `_p05_opsflow_recovery.py` and
  `test_p05_opsflow_native.py`, plus the coordinated P12 seam slice. The coordinator
  later assigned the same QA writer sole ownership of new
  `tests/validation/_p05_opsflow_registration.py` (ABSENT baseline) for the
  same-tag authenticated editor registration route with existing60-second stage
  bounds; it adds no operating or generic public-API authority. No second
  writer edits Node/SQL tests. Exact profile/export path ownership is released
  between QA and Node writers before either edits that shared path.

Documentation baseline metadata is retained locally at
`_workspace/repo-support/analysis/p05/doc-baseline.json`:
Spec SHA `1a118c18e6d84f5961d2821078e119ece994bf4e981417b8f17a87afd933de69`,
Plan `28b67cb3df6a4f77310ef374f2f378b7eac2dfc5f8fe2628b538389f298c373b`,
DATA README `7838371b55998c38ab77cdfb08d6ce75263cc8300f5546f1133d07606b2da138`
and payload `513a742753ee06d46d172164929faa89c38e0cff96b21f8e003b2118e8b8f195`.
This new Task was ABSENT. Actual data owner and operational accepter remain
UNASSIGNED until the trusted owner identifies them.

### Frozen source and scoped verification receipts

SQL007 SHA `8fc05ddcefe86d64c51d9ad130472c019558ac41f86d8f346478aa503dab0d32`
and008 `f0f39f09341bb0783c10f27c136aea40ff770b2edbbf9ffd37dee618db3d4e77`
were independently reviewed for code/security by `/root/p04_uri` with no actionable finding.
Missing007 RED became two focused source/immutable checks GREEN; the combined
existing SQL contract suite passed 19. Those initial checks were source-only. A later owned SQL-only PostgreSQL
rehearsal passed the fourteen behavior checks below; full n8n/SMTP recovery
remains separate.
Management function calls require an `opsflow_migrator` session explicitly using
`SET ROLE opsflow_owner`; existing INHERIT=false/SET=true membership and schema
USAGE are preserved, rather than granting more authority to make a test pass.

The frozen public Node input hashes are retained in
`_workspace/repo-support/analysis/p05/node-public-packet.json`: node
`53f5e47b5c5c7b45a242257ddfc3d7a45b51b4251971d4efa6183c7b1cbe51ca`,
transport `4117e28fd9c3b1134c9328397dba0e02b2968ec18f55204b3218f62f0a52c14c`,
node test `9b7b813e7a07adef7f7bd62ce001f1efbae6006e15b17633b72170d19749f56d`,
transport test `3319f3f070030f9040262b53502db3c1e78bff7dcb86e988cf419551f20facc5`
and STARTTLS test `e64e92f0c0f87b13d28012530ad5b5c4b424080e3c15db7a1f8413c7f9ce7ae4`.

The Node writer's authorized host package run passed 38 tests without skips in
2.430102965 seconds. Compiled production coverage: lines 97.51%, branches 95.56%,
functions 88.57%. Eight owned loopback Nodemailer STARTTLS cases include peer CA/name,
authentication, downgrade refusal, cancellation and post-DATA uncertainty.
The restricted initial run failed eight loopback cases with EPERM; the scoped
host run resolved that environment limitation. Independent code/security source
review by `/root/p04_pipeline` approved the same five frozen hashes with no
actionable finding; native n8n Worker/Mailpit execution is a
separate axis. No generator/export change was required.

P12 offline seam RED was six tests with five failures; current scoped seam GREEN
is seven tests. It checks independent data-version hashing, bounded quarantine
bytes/metadata/replay and fail-closed quarantine storage failure. It proves no
real DB/outbox count, Worker publication or P04 full restore. Parent's independent
combined seam/version-bundle rerun completed 17 tests with 15 PASS and 2 SKIP.

The P08 writer owns only canonical `update-ledger.json` (before
`a25b4092a88dd088a56e97b947bd51f3c5ad206e352edb4fcf57f8e3aa4c1911`)
and `build-inputs.json` (before
`0cfecf09cc6765a8253fc3a6eceea8ceb77388c1c158d494e8c525d564fcea91`)
in `infra/09-platform-ops/security-updates/`. At 2026-11-02T10:17:50.127809Z,
the current 17-input SOURCE_REVIEW_ONLY binding is
`07b103a9ce739ec565f5f42ef7166feadc71355d276f8fec2bfdfffe135b88e4`.
Previous binding 57ad4d23… was appended intact to each historical list (12→13).
Current root include_inputs and historical native verification remain unchanged;
this local source binding does not establish signatures, a rebuilt image, native
execution, HOME readiness, rotation or recovery. Focused stale-receipt RED became
eight WorkflowVersionBundle checks PASS without skips; independent source-binding receipt review approved the exact public-input match and preserved history.

### Current item dispositions

| Item | Criterion | Work Unit | Current disposition | Current contract |
| --- | --- | --- | --- | --- |
| P05.01 | 72 | W77 | REUSE_ACCEPTED | Preserve original C19/C22 queue/schedule scope; current exact-source/image/private equivalence needs its own evidence |
| P05.02 | 73 | W78 | TEST_RESIDUAL | One explicitly approved manual no-send dead retry; preserve attempts/audit, restore sending to unknown and enforce in-flight recovery barrier |
| P05.03 | 74 | W79 | NO_CHANGE | No new binary storage; selected notifier rejects input.binary and exact queue/default-storage behavior is reconciled |
| P05.04 | 75 | W80 | SOURCE_READY | Explicit optional authenticated isolated Mailpit STARTTLS and next-execution same-ID credential refresh; actual producer/rotation remains P06-owned |

Source, static checks, synthetic/isolated tests, historical operator acceptance,
this execution's direct operation, credential rotation, independent restore,
remote CI and final acceptance are independent axes. Direct HOME operation,
actual rotation/restore, remote CI and P12 final acceptance remain NOT_RUN.

### Implementation, refusal and recovery contract

Do not bulk-reset dead/unknown rows or erase attempts. One manual no-send
reprocess consumes one explicit owner approval and retains its audit evidence;
capture absence alone is not proof of no SMTP acceptance. Restored sending
becomes unknown, and a live execution must cross the reviewed recovery barrier
before a separate restored target resumes. No active worker or unverified
in-flight socket is treated as quiesced from process-start metadata alone.

The selected notifier rejects input.binary and uses supported PostgreSQL/SMTP
paths. The optional test profile supplies authenticated STARTTLS only to exact
owned fixture targets. Same-ID material refresh is tested on the next native
execution; it does not rotate an operating credential or prove an actual P06
producer. Exact source interfaces and file leases are recorded before edits.

Preflight existing tools, exact cached images, trusted UID/path ownership and
resources. Use one owned cluster at a time, preserve bounded attempts and
failure receipts, and never weaken guards or pull images to manufacture PASS.
RED/GREEN tests must cover normal, rejection, interruption and recovery with
at least 80% new executable-code coverage. Independent reviews, registered local
gates, graphify and source fingerprint comparison precede local delivery.

### Native fixture preparation before execution

The QA writer's first prelaunch packet binds `_p05_opsflow_native.py` to
`776ae030a4badb00a8d50ae57f114b473800f80c9bd547a79ccc717946504d98`,
`_p05_opsflow_recovery.py` to
`bc70d322399f8687d32d3b2191451c3afe0e4de8e448c52bf3bbf38767ef1f84`,
and `test_p05_opsflow_native.py` to
`b01e36d033341e8b9d58b86f400bfb7a4bf9ea42c9e2a0cdd34ab9a10068feec`.
These are dated prelaunch observations, not immutable target hashes or runtime
acceptance. The focused native/P12 run completed eleven tests: ten PASS and one
explicit native SKIP. New full-fixture coverage and actual execution are pending.

An offline owned candidate build/readback matched the current six dist artifacts
and161 runtime Nodemailer files. An old candidate carrying10.1.0 was rejected;
the selected locked dependency10.1.4, core2.43.6 and framework package2.43.4 are
separate version identities. This fixture artifact is not a new operating image
release or signature/provenance acceptance. Explicit prefix `opsflow_native`
is an isolated test choice and does not prove production `n8n` queue equivalence.
The proposed budget is2400 seconds work plus120 cleanup with the preserved
3296MiB/1.75CPU aggregate; preflight and independent source review must precede
any runtime. Running/prepared evidence is never PASS for the business path.

Before full execution, source crosscheck corrected an incorrect fixture expectation:
wrong AUTH material had been expected to enter retry, whereas the selected
transport conservatively returns uncertain and the workflow records unknown.
The fixture now preserves those unknown rows and publishes fresh rows for the
corrected-material requests. No production uncertainty rule was weakened and
capture absence is not used as no-send proof. The recovery barrier follows
terminal executions; it proves quiesced old processes/sockets/jobs, not an
interruption of an actively sending SMTP execution. That active-send interruption
scope remains a separate TEST_RESIDUAL unless directly exercised.

### Docker-free fixture control-flow regression

The separately assigned QA writer created only
`tests/validation/test_p05_opsflow_scenario.py` (ABSENT baseline), frozen SHA
`2bdbb0f683d05d7f090c0dbad9e851b34ad023932ee8a6cd939f0c5109bcb768`.
Thirteen stateful scenario tests plus four existing guards passed without skips
in0.284 seconds. Whole-file line trace includes imports and retains the line0
marker with no denominator exclusions: native fixture446/448=99.5536%, recovery
validator22/23=95.6522%. The target native source was
`95183c2940117d3e540db3492281bedc33518867e7ea1c2828ff4e905ef5e7e6`.
The receipt is `_workspace/repo-support/analysis/p05/scenario-qa-summary.json`.

These doubles verify phase ordering, unknown not resent, fresh corrected rows,
missing DB restoration cannot PASS, failed barriers prevent teardown, cancellation
finally and the file-path TLS-key guard boundary. An in-memory validator-bypass
mutation produced three expected failures without source edits; it is a test
sensitivity check, not the production RED or an actual service test. The later
reviewed packet is recorded below. This unit PASS never resolves the full runtime ERROR below.

The follow-up source handles already-inactive workflows without an invalid
deactivate call, while retaining inactive-state readback. The latest scenario
file is `b86aa25714674fb376fe6aa6c1749deccf6dc448d73fda357c8378afe4439614`;
its native target is `e38a82068f33ad92bc0dd62f3143abad177205fa41bd1dee6786f3461905822f`
and guard test is `64878846a07be33b54f1633435d72955b38730175e73fd4e2720ac732e6861f3`.
Fourteen scenarios plus five guards passed19/19 without skips. Whole Python
native source coverage is447/449=99.5546%; recovery remains22/23=95.6522%.
The runner now executes the in-memory bypass mutation separately and computes
its actual one-test/three-subtest-failure/zero-error result; mutation counts are
excluded from GREEN coverage. Earlier summary/logs are preserved as
`*.before-active-fix`. This covers Python/doubles, excluding embedded JavaScript
execution and actual Docker/SMTP/DB/restore. Independent reviewer `/root/p04_uri`
approved the exact latest packet, reran19 tests without skips in0.058 seconds,
independently recomputed447/449 and22/23, and replayed the actual memory-only
mutation with one test/three expected assertion failures/zero errors.

The candidate-owner correction adds runtime-lock/deployment-manifest and closed
root-owned artifact metadata checks. Its current helper SHA is
`4199be5ae56ed4d96a8b50966b9b6b1a8b93a924c213066ab89a26e47765caa8`,
guard `b295ab96b03edc2db705713432ca282bc50fa88b50533c3fed10a273760f585e`
and scenario `97dcc2ec81450c6b805f400b59bf3ee4d267dcf7df83143a195ec25df3009c5f`.
Fifteen scenarios plus six guards passed21/21 without skips in0.311 seconds;
the current whole Python helper trace is511/513=99.6101%, recovery22/23=95.6522%.
Dynamic mutation still produced three expected failures separately from GREEN
coverage. The old packet is preserved as `*.before-owner-fix`. Independent
reviewer `/root/p04_uri` approved the exact current four hashes, reran21 tests
without skips and independently recomputed511/513 and22/23. Candidate
ownership/byte checks and doubles do not prove
Worker, SMTP credentials or restoration. Earlier e38/19-test metrics remain dated
and are not substituted for the changed helper's trace.

The registration follow-up binds native source
`a0c99bb5882d2f45ce785d0021116c2c181aabf741eca34c8deeb7a09022911b`,
registration helper `074291db8db4faed87648f0761c60d7a47a4d08fb7b74e061ea1d718f2146df6`,
guards `e30c0783cc94eb9d80eb8e5e05c52abb3e52eec5f2b01e7abafc7e8cac626fd9`
and scenario `e9d5c6fa93554ed28185ddd99b940a0644dc4d00bb1f85794acc4336c1464d90`.
The source-only run passed23 tests without skips in0.742 seconds. Whole Python
line coverage: native516/518=99.6139%, registration100/106=94.3396%, recovery22/23=95.6522%.
Actual bind/register method tests include normal and wrong-owner/ID/inactive,
create/readback and private-write failure refusal. Dynamic in-memory mutation
still produced three expected failures separately. Prior packets are preserved
before-registration. Independent reviewer `/root/p04_uri` approved the exact
five hashes, reran23 tests without skips and independently recomputed all three
coverage ratios. Embedded JavaScript, real editor POST, SMTP and restoration
remain separate from this trace.

### First full-fixture execution

The first full candidate rehearsal ended ERROR after134.276 seconds; cleanup
was PASS, with zero owned containers/networks, absent attempt directory and
released serial lock. The sanitized receipt is
`_workspace/repo-support/analysis/p05/native-full-summary.json` (initial source
`56a34282f409101857a0fb02e53c475b3d950fb43ad3f574f4731f2b6e21d875`). DB migrations/checks and Valkey preparation completed, but before
Mailpit creation the existing secret-environment guard rejected the key-file
path environment variable. No key value was exposed. Worker execution, SMTP,
same-ID refresh and restoration were NOT_RUN in this attempt. The initial
failure is preserved; a fixture-only change to supported file-path CLI options
requires source review and its own terminal retry receipt. The correction uses
`--smtp-tls-key=/run/secrets/server.key`, a file path, while preserving the original
secret-environment guard. Its focused RED/GREEN command completed twelve tests:
eleven PASS and one native SKIP; that source check does not resolve this full failure. No operating service
or actual credential action is inferred from this guarded failure.

The second full candidate rehearsal ended ERROR after463.761 seconds at the
preserved300-second Main readiness limit. Mailpit was healthy and DB/Valkey
preparation passed, but n8n Main exited1 because the owned candidate's public
dist owner1000 conflicted with the existing launcher's root-owner requirement.
This candidate-artifact mismatch is distinct from the first path-variable guard.
Readback byte/hash parity alone did not test ownership. Cleanup passed with zero
owned containers/networks and the serial lock released. Worker, native credential,
SMTP and restoration remained NOT_RUN. Both failed attempts are retained; any
candidate-only ownership correction and later trial need their own artifact
review and terminal receipt, without changing the existing launcher checks.

The later owned candidate's independent readback verified171 files and56
directories with expected root ownership/modes, exact current bytes, cached-base
ancestry and normal-entrypoint `--version`. Its readback receipt digest is
`7998cc500ebd1a2b41735e07e61220850f930d20b17647eae313b07aa99b1471`.
Candidate image9dea… and fixture bindingd4b… are separate from P08's public
SOURCE_REVIEW_ONLY binding. The reviewed full trial retained the same
2400/120-second bounds; preparation/entrypoint validation is not Worker,
credential, SMTP or restore acceptance. Prior failed candidates and both terminal
ERROR receipts remain retained.

The root-owned candidate's third full trial ended ERROR after485.257 seconds.
Mailpit, Main and Worker readiness returned200 and Runner registration passed;
the unchanged60-second `n8n import:workflow` bound was reached during
workflow_binding. Cleanup passed. First business execution, SMTP capture,
credential refresh and restoration were NOT_RUN. This scoped readiness progress
does not resolve any full-rehearsal failure. The same-version editor REST route
is being investigated as a fixture-only alternative, with no timeout extension;
its applicability and any later trial remain separate evidence.
The new registration helper was independently approved against the immutable
2.43.6 controller, entity mapper, creation service, project and ownership source
listed in DATA research. It uses the authenticated owner editor session, verifies
personal-project ownership and inactive registration, and preserves the60-second
limit. This is a version-bound internal editor API, not a stable public API;
actual POST/readback and business execution remain pending isolated execution.

In the later editor-REST trial, the QA writer reported actual personal-project
and inactive-registration readback, followed by first Worker→Bull queue→verified
STARTTLS/AUTH Mailpit delivery, SQL accepted_by_smtp and exactly one safe capture.
The fixed phase advanced to same_id_credential_refresh after those assertions.
This is scoped progress in a still-running owned trial, not overall native PASS;
wrong-old/new material, next-execution refresh and restoration still await their
actual terminal receipt. Earlier trials' NOT_RUN business stages remain historical
facts and are not rewritten by this later progress.

### Final owned editor-REST native result

The later trial passed in747.701 seconds with cleanup PASS. I directly inspected
the sanitized structured receipt
`_workspace/repo-support/analysis/p05/native-editor-rest-receipt.json`, attempt
`opsflow-native-d4364f2ebc5f9fb0bc35f290`. Exact test image is
`sha256:9dea19678689c032ef0ea086893fdc8e8d8edc4fba75d2104f0948aa38b02bc5`,
fixture binding `d4b51ceee2814e553e4919e34f5396231f65e711b6500afe125ba3720deb350a`,
with the historical accepted n8n image as cached base. These identities remain
separate from P08's public source-preparation binding.

Six terminal executions were recorded. The actual Worker/Bull/verified STARTTLS
AUTH route produced SQL accepted_by_smtp and safe capture. Wrong new and wrong
old material became unknown without extra capture; the same credential ID used
refreshed material on the next execution. The inactive personal-project editor
registration/readback passed; cold CLI import was NOT_RUN in this successful
path, so the earlier485.257-second CLI ERROR remains history.

The barrier verified inactive workflow, old process/socket absence, held SMTP
egress and absence of exact old Bull execution IDs1–5. Fresh generation2 restored
roles, DEV DB and n8n metadata with the original synthetic encryption key, and
execution6 consumed the restored SMTP credential and delivered successfully.
Execution6 used a fresh run; the test did not replay the same pre-restore input
or assert equivalence of prior unknown/accepted outbox rows, attempt/audit state
and their next-claim behavior. Those full outbox-meaning checks remain
TEST_RESIDUAL alongside active-send interruption. Paired restoration acceptance
is limited to recorded DB/metadata restore and same-key credential reuse.
The receipt explicitly states `recovery_scope=QUIESCED_ONLY` and
`live_inflight_interruption=TEST_RESIDUAL`. This does not prove interruption of
an actively transmitting SMTP execution or actual HOME recovery.

Cleanup reported exact absence for every owned role, empty container/network
retention and sweep lists, no attempt directory and released serial lock. The
fixture intentionally saves synthetic execution data for assertions; this private
fixture settings delta does not change the public inactive export's disabled
execution-data storage. Real credentials/rotation, external recipient delivery,
operating services, remote CI and P12 final acceptance remain NOT_RUN. All three
prior ERROR receipts are preserved; scoped native PASS closes their identical
rehearsal check without rewriting their historical outcomes. Independent reviewer
`/root/p04_uri` approved receipt SHA256
`a241ae94965752fc9378e0fcdea3da3444687c0f3be1a2517cc12e7d20388a94`
only for these observed fields and explicitly retained the recovery residuals.

### Restore replay and active-send interruption (2026-11-04)

The owner's 2026-11-04 request to re-review the n8n notification consumer
contract authorized closing the two residuals above in the owned native
scenario. Source commits after rebasing onto `1425b017b` are `465d37d77` and
`a1e9ab4eb` on `test/opsflow-notifier-replay-residuals`. Attempt 3's native
helper SHA was
`f9a9005326a488b4907ddbc21671b1521d914321286e98fadda6a45c80482eb0` and
recovery validator SHA was
`61c11dce6ffd6c216e01a6f68d46454f26e66207ddf7897396e6e965031dcc4a`.
The rules come from SQL001/007 and the transport, not from new behavior:

- `publish_manifest` returns `replayed` for an identical run and adds no outbox row.
- `claim_notification` selects only `pending`/`retry` rows under `attempt_limit`.
- `unknown` leaves only through operator `reconcile_notification`.
- Any stall after `sendMail` starts is `uncertain`, recorded as `unknown`.

After the quiesced barrier, the scenario snapshots every outbox, attempt
reconciliation, recovery audit and run row. Lease tokens are compared only
for presence. Restored rows must be identical. All five pre-restore inputs
are then replayed and must return `replayed` with an unchanged snapshot and
zero claimable rows. The next fresh claim must leave every old row
byte-identical and accept only the fresh row on attempt 1. Generation 2
capture must hold that one message and no pre-restore run.

For the active send, a fixture-only STARTTLS endpoint (`smtp-hold`)
replaces the stopped Mailpit under alias `mailpit`. It uses the owned
synthetic certificate and the existing ephemeral capture-probe caps
(128MiB/0.10CPU while Mailpit's 192MiB is stopped), so the reviewed
aggregate does not grow. It answers up to `354` and then never replies.
It stores nothing and prints closed facts only. A loopback check against
the package Nodemailer observed verified STARTTLS/AUTH, DATA, held body
and the client's own ETIMEDOUT at 5.05 seconds. The worker is stopped
while the body is held, within the 5-second transport socket timeout.
The row must then be `unknown` or `sending`, never success or retry. After
Mailpit/worker/runner restart, one fresh claim must deliver while the
interrupted row keeps its state and attempt and is never captured.

New guard tests were written first: 14 tests with 6 errors (validators
absent). Final Docker-free GREEN is 33 tests, 32 PASS and 1 native SKIP.
Five separate weakenings each turned the suites RED: interruption accepting
success/retry (3 failures), restore ignoring drift (2), replay ignoring new
rows (1), next claim ignoring old rows (2) and recovery ignoring a resend (1).
Stdlib-trace coverage of executable lines added since `b08e1bdbf` is native
172/173 and recovery 56/56. Whole files are 645/647 and 79/79.

Native attempt 1 ended ERROR in 1.872 seconds at preflight. The invocation
omitted the existing exact image/context selection; no container was
created, and cleanup was PASS. Attempt 2 (`opsflow-native-af0c888e5e75900431de413e`)
ended ERROR in 724.780 seconds. It held the session mid-DATA, issued the
worker stop 0.487 seconds after detection, and the row was `unknown`. The
interrupted execution never became terminal, and the quiesced barrier then
refused restore (`recovery barrier incomplete`). Cleanup was PASS with
nothing retained. Attempt 3 (`opsflow-native-18877650611b9ad82a8035a5`)
moved the interruption after the restore checks and passed in 852.821
seconds with cleanup PASS. It recorded the interrupted Bull job still
present after its worker stopped (matching 1). This confirms the cause of
attempt 2's refusal: the barrier correctly failed closed on a surviving
in-flight job. Attempt 3 receipt facts:

- Restored snapshot: 10 rows, 5 outbox rows (3 accepted, 2 unknown),
  identical, SHA `9af7ad82cb8306937eb2c259f85816a1caac1a30efc04ae9734de2644c1db8d5`.
- Replay: 5 replayed, 0 claimable; next claim left old rows unchanged and
  accepted only the fresh row.
- Interruption: DATA started, body held, session open at stop, 0.411
  seconds detection-to-stop, row `unknown`, execution 7 not terminal.
- Recovery: row stayed `unknown` on attempt 1, was not resent, and the
  fresh row was accepted.

The 2400/120-second bounds were unchanged. Post-run census found zero owned
containers, networks and attempt directories, and the serial lock was free.
Receipts and logs are in the executing worktree's ignored
`_workspace/repo-support/analysis/p05/replay-residuals/`. The native-run3
receipt SHA256 is
`cf43208d549d19afa4fb9e069449b132b6625711b4b6267e11bd5da2dc533f6b`.

#### Independent review and kill-based correction

The independent code review returned CHANGES_REQUESTED, with one important
and two minor findings:

- **Important:** the stopped-worker facts could not tell a stop-caused
  interruption from the transport's own 5-second `socketTimeout`.
  `fixture.stop()` waits 10 seconds, and the n8n queue-mode documentation sets
  `N8N_GRACEFUL_SHUTDOWN_TIMEOUT` to 30 seconds by default for running jobs.
  A gracefully stopping worker could therefore let the transport time out,
  record `unknown`, and still pass. Attempts 2 and 3 are consistent with that
  path, so attempt 3's interruption result is superseded. Its restore,
  replay and next-claim results stand.
- **Minor:** the detection-to-stop latency excluded polling and log
  round-trips.
- **Minor:** the next-claim filter matched the fresh run_id as a substring.

Fix (source commit `d94f7440c` after rebasing onto `1425b017b`):

- The worker is now SIGKILLed while the body is held, so no node code can
  run after the kill. The row must stay `sending`; `unknown` is rejected as
  the transport-timeout path.
- The hold endpoint emits its own body epoch timestamp and body-to-close
  milliseconds. The client close must come within 5000 milliseconds, and the
  session must still be open when the kill is issued.
- Recovery expires the lease by fixture-only superuser time travel, the same
  precedent as `fast_forward_sql`. The next claim must then record
  `lease_expired_delivery_unknown` on attempt 1, without a resend.
- The next-claim filter compares the parsed run_id field.

A loopback check on the new endpoint separates the two paths. The client's
own timeout closed at 5004 ms after the body (rejected). A SIGKILLed client
closed at 346 ms.

Final helper SHAs are native
`6fdb8b62878629bcec22351a5b0ceaafe512366523108ca695104abbaeb86287` and
recovery `e924d9f3030b60284c2e824b75e6dd0b0c7977b28f9f5b9c81cd50b6ea6d19ed`.
The new guards first failed (16 tests: 2 failures, 1 error). Final
Docker-free GREEN is 35 tests, 34 PASS and 1 native SKIP. Six separate
weakenings each turned the suites RED:

- unknown accepted as an interruption (1 failure);
- close time ignored (3);
- restore drift ignored (2);
- replay new rows ignored (1);
- substring filter restored (1);
- resend ignored (1).

Coverage of executable lines added since `1425b017b` is native 196/198 and
recovery 88/88.

The single native rerun, attempt 4 (`opsflow-native-e676807076f07cf48424ae89`),
passed in 731.029 seconds with cleanup PASS and nothing retained. Receipt
`native-run4-receipt.json` has SHA256
`b21b2f7b1cd7e66c94550512c3fceb02f71301e6005fbbade20b184ad89c939c`.

- Restore, replay and next claim matched attempt 3: 10 identical rows,
  5 replayed, 0 claimable, fresh row only.
- Interruption: the session was open when the kill was issued, the client
  closed 1020 ms after the body, and the row stayed `sending`.
- `body_to_kill_ms=3257` is an upper bound measured after the kill and the
  stopped-state poll returned, not the instant of the signal. The exact
  kill-issue time was not recorded separately.
- The interrupted execution stayed non-terminal, and its Bull job survived
  (matching 1).
- After the lease expired, the next claim recorded
  `unknown|1|lease_expired_delivery_unknown`, nothing was resent, and the
  fresh row was accepted.

Unchanged limits and zero owned residue held, and the lock was free.

Aggregate caps: Docker limits apply only to running containers. The hold
runs only while Mailpit is stopped and is removed before Mailpit restarts.
Its 128MiB/0.10CPU therefore replaces Mailpit's 192MiB/0.10CPU, lowering
the running aggregate by 64MiB.

Remaining limits:

- Restore with an interrupted job still in the broker is refused by the
  barrier, and no reviewed route clears that job, so it stays TEST_RESIDUAL.
- The interrupted execution remains non-terminal in n8n metadata.
- Same-input replay covers repeated publication, not replay of an n8n execution.
- Re-review of the kill-based correction is pending.

### Interrupted broker job and execution recovery (2026-11-05)

The owner's 2026-11-05 request to review and then implement the remaining
T05 items authorized this increment. Branch
`fix/opsflow-notifier-interrupted-job-recovery` from `729d16da7`.

#### Review before code

The n8n documentation, retrieved 2026-11-05, does not describe what happens to
a job or execution after a worker crash:

- <https://docs.n8n.io/hosting/scaling/queue-mode/> gives only
  `N8N_GRACEFUL_SHUTDOWN_TIMEOUT` (30 seconds) for workers to finish running
  jobs.
- <https://docs.n8n.io/hosting/configuration/environment-variables/queue-mode/>
  lists `QUEUE_WORKER_LOCK_DURATION` 60000 ms, `QUEUE_WORKER_LOCK_RENEW_TIME`
  10000 ms and `QUEUE_WORKER_STALLED_INTERVAL` 30000 ms, and marks
  `QUEUE_WORKER_MAX_STALLED_COUNT` removed in 2.0.

Crash recovery is therefore NOT_VERIFIED in the documentation. The behavior
relied on was read from the cached declared image `n8nio/n8n:2.43.6`
(`sha256:dd580fe1…`, the candidate's base). The files were copied from a
stopped, network-none container that was then removed:

- `dist/scaling/scaling.service.js` creates the Bull queue with
  `maxStalledCount: 0`. `addJob` sets `removeOnFail` to
  `executions.queueRetention.keepLastFailed`, which defaults to 0
  (`N8N_EXECUTIONS_QUEUE_KEEP_LAST_FAILED`).
- Bull 4.16.4 (n8n-patched) `moveStalledJobsToWait-7.lua` runs only in a
  processing worker: at startup and then every `stalledInterval`. When an
  active job has no lock and its stalled count exceeds 0, the script moves it
  to failed instead of wait. It publishes `job stalled more than
  maxStalledCount` and, with `removeOnFail` 0, deletes the job.
- `dist/workflow-runner.js`: main, which still awaits the job, maps that
  message to `MaxStalledCountError`. After a 30-second recheck window it calls
  `markAsCrashedWithoutCounting(executionId, 'stall')`. The execution
  repository sets `status='crashed'` and `stoppedAt`.
- Main's own sweep for executions without a queue job is
  `N8N_EXECUTIONS_QUEUE_RECOVERY_INTERVAL` (180 minutes). It is not relied on.
- The fixture and HOME n8n environments set none of these variables.

The smallest correct route is n8n's own route (a). Restart a worker with
polling held and main still running, then wait until the exact job is gone and
the execution is `crashed`. No job is deleted by the fixture or an operator,
and the barrier is not weakened. A failed job kept by a non-zero retention
still matches the probe, which also scans failed and completed jobs, so the
barrier fails closed. The outbox row was already safe through lease expiry.

#### Implementation and guards

- The interruption now runs before the quiesced barrier, as in the earlier
  barrier-refusal attempt.
- `recover_interrupted` records the exact job count before the worker restart.
  It then waits up to `STALL_RECOVERY_SECONDS` = 60 + 3×30 = 150 seconds and
  reads the execution status (existing 60-second wait).
  `validate_queue_recovery` accepts only `{jobs_before_restart: 1,
  jobs_after_recovery: 0, execution_status: crashed}`.
- The barrier gains `old_executions_terminal`: every old execution must have
  `stoppedAt` in n8n's REST record.
- The existing 2400/120-second bounds are unchanged. The new 150-second wait
  is derived from the image defaults above; the measured settle time was
  38 seconds.

The new guards first failed: 37 tests with 10 failures, 3 errors and 1 native
SKIP (`guards-red.log`). GREEN is 37 tests, 36 PASS and 1 native SKIP. Five
separate weakenings each turned the suites RED:

- the barrier ignores the terminal field (9 failures);
- recovery accepts a surviving job (1);
- recovery accepts a non-crashed execution (5);
- the rehearsal skips the recovery check (3);
- the fence reports terminal without reading n8n (1).

Stdlib-trace coverage of executable lines added since `729d16da7` is native
29/29 and recovery 13/13. Whole files are 690/693 and 124/124.

#### Native results

Every attempt used the same candidate `9dea1967` and binding `d4b51cee`:

- Attempt 1 (`opsflow-native-7e474cd8911ee7b6feba9c22`) ended ERROR at
  preflight in 0.282 seconds. It selected the base image id instead of the
  candidate image id. No container was created, and cleanup was PASS.
- Attempt 2 (`opsflow-native-45a8e72bbcaa702c57d0174c`) ended ERROR in
  832.489 seconds. n8n recovery passed: job 1→0 and execution 6 `crashed` in
  38.389 seconds. The barrier then passed with seven old executions terminal,
  and the restore and seven-input replay passed. The post-restore publication
  then failed because its capture time (2026-11-26) was older than the
  reordered interruption inputs, so `publish_manifest` recorded it as
  `historical`. The scenario double now refuses an older capture. That rule
  first failed two scenario tests, and GREEN is again 37/36 PASS/1 SKIP. The
  fix is commit `1d76b7135`.
- Attempt 3 (`opsflow-native-7d3e7050dc522b4ab9cc6caa`, native helper
  `038d4207…`, recovery `c9c26338…`) passed in 799.181 seconds with cleanup
  PASS:
  - Kill: the session was open at the kill, and the client closed 911 ms after
    the body. `body_to_kill_ms` was 2594, and the row stayed `sending`.
  - Before recovery, execution 6 was `not_terminal` and its Bull job survived
    (1).
  - After the worker restart, n8n removed the job (0) and marked execution 6
    `crashed` in 38.074 seconds.
  - Lease expiry gave `unknown|1|lease_expired_delivery_unknown` with no
    resend, and the fresh row was accepted.
  - The barrier passed with executions 1–7 all terminal and no broker jobs.
  - The restored snapshot had 14 rows and 7 outbox rows (4 accepted,
    3 unknown), identical. Replay gave 7 replayed and 0 claimable, and the next
    claim was fresh-only.
  - Receipt `native-run3-receipt.json` SHA256 is
    `47b1b878d0310e0f9f9d92d65ff2d3bc25ed02fac02faacbe1b4fc554aff33d0`.

After every attempt the census found zero owned containers and networks.
Receipts and logs are in the ignored
`_workspace/repo-support/analysis/p05/interrupted-job-recovery/`. The failed
attempts' logs are also kept under `retained/`.

The guarded operator step is in the
[n8n Runbook](../../../05.operations/runbooks/08-workflows-and-automation/0053-n8n.md#강제-종료된-worker의-queue-job과-실행-기록).
HOME execution is NOT_RUN. An independent review of this increment is NOT_RUN.

### Main restart, crashed-execution retry and HOME check (2026-11-05)

The owner's 2026-11-05 request asked to apply the recovery procedure to HOME
operations (approval given), to cover a main restart, and to apply a replay
of the n8n execution itself, then to finish the remaining T05 items. Branch
`test/opsflow-notifier-main-restart-and-retry` from `f0ce46fda`.

#### HOME application

Read-only inspection on 2026-11-05 used the `mnginspector` Valkey account
and a read-only metadata session. The `n8n:jobs` active, wait, delayed,
paused and failed keys were all absent, and no execution was `new` or
`running`. The Opsflow notifier workflow is not installed in HOME; the only
active workflow is `HermesBlogIngest`. The queue settings are the n8n
defaults the rehearsal assumes. With no target the procedure restarts
nothing, so the HOME worker and main restarts were not run. The read-only
step is now step 0 of RUN-0053.

#### Source review

Read from the declared image `n8nio/n8n:2.43.6`:

- `ScalingService.setupQueue` runs `scheduleQueueRecovery(0)` on the leader
  at startup. `recoverFromQueue` marks `new`/`running` executions with no
  active or waiting job `crashed`. The next check is
  `N8N_EXECUTIONS_QUEUE_RECOVERY_INTERVAL` (180 minutes) later.
- `ExecutionService.retry` copies the stored execution data. A run with no
  `executionData` is refused, and `UnexpectedError("The retry did not start
  for an unknown reason.")` is thrown when no post-execute result is
  attached.

#### Native result

Attempt 13 on code `a4bf785d9`, after the review fixes (candidate
`9dea1967…`, binding `d4b51cee…`), passed in 980.804 seconds with cleanup
PASS and zero owned residue:

- Main alive: SIGKILL mid-DATA (open session, body-to-kill 2435 ms), job
  1→0 and execution 6 `crashed` in 37.533 seconds.
- Main also killed: job 1 at 10573 ms after the kill signal, before lock
  expiry. The worker deleted it (0) while execution 8 stayed `running`.
  After the main restart it was `crashed` in 61.262 seconds, with its data
  row kept (1→1) and REST readable. The interrupted row became
  `unknown|1|lease_expired_delivery_unknown` with no resend.
- Retry: both crashed executions had an empty start stack and no run data.
  n8n's retry ended `error` once (creating execution 10) and `not_started`
  (HTTP 500, no execution created) once. Execution 10 was terminal before
  the state checks. Nothing was claimed or resent and the outbox was
  unchanged, with a claimable fresh row present. A new execution then
  delivered that row on its first attempt.
- Barrier passed with executions 1–11 terminal, including retry execution
  10, and no jobs. The restore was identical (20 rows, 10 outbox: 6
  accepted, 4 unknown). Replay gave 10 replayed and 0 claimable; the next
  claim was fresh-only.
- Receipt `native-run13-receipt.json` SHA256 is
  `84f8eda39e71f0c2914ec30d2c292af6cfeac42dd01e6ea60c1e1268c396aefe`.
  Attempt 12 (`17a61823…`, code `ef2ca463a`) had passed before the review
  fixes and is superseded.

So n8n's own retry cannot replay a worker-killed notifier execution. The
replay is a new execution of the workflow, and the interrupted row stays
`unknown` for reconciliation.

#### Review

The independent review of `f0ce46fda..174155ab5` returned CHANGES_REQUESTED
with two Important findings. First, any HTTP 500 was read as `not_started`,
so a job queued before the 500 could claim after the checks. Second, retry
executions were outside the barrier. It also made four Minor findings: kill
monotonic time taken after the stop wait, equality instead of exact types,
a resend refused only after a new execution, and two source-only runbook
claims. Commits `a4bf785d9` and `395e1fe64` fix all six. Each `retryOf`
execution is read from the metadata DB, must be terminal before the state
checks, and joins the barrier.

#### Failed attempts

Each attempt's cleanup passed with zero owned residue. Logs are in the
ignored `_workspace/repo-support/analysis/p05/main-restart-retry/`.

| Attempt | Stop | Cause and correction |
| --- | --- | --- |
| 1 | Preflight, 0.4 s | Image selection variables omitted |
| 2 | Publish, 546 s | SQL003 one run per source per UTC date; inputs given own dates (`404713ac7`) |
| 3 | Settle probe, 504 s | Bull `getJobs` returns null for a job removed mid-scan; probe skips it (`fe30fd4bd`) |
| 4 | Main-restart check, 683 s | REST read 404; status now read from metadata DB (`92b0166d8`) |
| 5 | DEV provision, 115 s | Socket readiness passed on the init server; TCP readiness (`068c21e6c`) |
| 6–8 | Retry, 742–793 s | Retry delivered nothing; traces showed the empty stack (`07a601c88`, `22675499d`, `393620db4`, `16fc953d3`) |
| 9 | Post-restart execution, 767 s | Stale runner registration line; count must increase (`cc115befd`) |
| 10 | Interruption, 424 s | Kill time included the stop wait; timed at signal (`6db614394`) |
| 11 | Retry, 713 s | Retry answered HTTP 500; recorded as `not_started` (`ef2ca463a`) |

RUN-0053 1.10.0 adds steps 0, 6 and 7. HOME worker and main restarts remain
NOT_RUN because there is no target.

### Actual isolated SQL-only verification

The first guarded attempt stopped before007 after the driver expected a different
SQLSTATE for the direct no-SET-ROLE call; cleanup passed. Existing authority was
preserved. The corrected driver observed direct-call denial42501 and explicitly
selected the existing owner role in the migrator session. The retry passed in
41.292 seconds with cleanup PASS, exact cached PostgreSQL image
`sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873`,
network-none, postgres user, read-only root,768MiB equal memory/swap,1CPU and128PIDs.
Its receipt is `_workspace/repo-support/analysis/p05/sql-native-summary.json`.
The failed 13.990-second original is retained in `sql-native-attempt1-summary.json`;
the final QA driver SHA is `dd3a3b6793db29f2103056b643d32f4ec2a9777558eecb530cb77adc688f9ebf`.

Fourteen actual behavior items passed: default five attempts, one extra approved
attempt, lifetime-attempt preservation, idempotent request, conflicting request
refusal, approval transaction rollback, operator-only boundary, current-attempt
reconciled proof, sent/unknown refusal, invalid-input refusal, integer-overflow
refusal, capped high-attempt backoff, future-lease restored sending to unknown,
and parallel recovery conflict. Actual migrations/predecessor/wrong-version,
drift atomic refusal and independent read-only v5 checker also passed.

The native-only Python QA driver trace was 224/284=78.87323943661971%, below 80%.
A separate successful source-unit trace executed 14 provably disjoint method-body
lines: 33–36,40–41,43–50. The actual native trace wraps only `RecoverySQLProbe.run`
and never invokes those `RecoverySourceTests` methods. Keeping the same 284-line
full-file denominator and ignoring every other unit line yields a conservative
combined minimum 238/284=83.80281690140845%. The independent parent reviewed the
supplement `sql-qa-coverage-supplement.json`; no additional cluster ran for this
metric. Native-only coverage remains 78.873%; the combined lower bound meets 80%
for the Python QA driver, not PostgreSQL stored-function coverage. Neither metric
proves full n8n Worker/SMTP/metadata restoration, HOME operation or real delivery.

### Independent living-document review

The independent P08 writer `/root/p04_infra` reviewed the nine assigned living
document deltas against current source, without editing them. Two minor findings
were corrected by the sole document writer: remove an inaccurate notifier-function
count in the node README, and label the guide's V6 failure as historical Task0020
while linking current P04 Task0043 TEST_RESIDUAL. Narrow re-review approved all
nine exact file hashes with no remaining finding at the first document freeze
(packet SHA256 `d5da116413c190ca07ec2578a93e7d68dd403e8c4e623ce491571d5b32166709`).
A later clarification in three documents explicitly requires the existing
`SET ROLE opsflow_owner` management context, with no source/grant change.
The current `_workspace/repo-support/analysis/p05/living-doc-current.json` packet
is `abbede46808302625cb805695e264c0112604b38038f2712d6afb4ee31525378`;
its narrow follow-up review was independently approved with no remaining finding.
This is changed-document/source-contract review, not whole-corpus or runtime acceptance.

### Cross-owner residuals

The old source-preparation receipt named n8n Compose hash `8792…`
instead of current `63c9…`; P08 corrected only its canonical current source binding
and retained the prior source/native history. Updated JSON SHAs are
`5298c88f3deb5ddecb0fb332694451a0f345b2883ff87c29bff56d4524992afd`
(update-ledger) and `fd340323c992c9ea572c99f878accf0b2239578088119e063665e77bd43db47d`
(build-inputs). Independent source-binding review found no actionable finding.
Five P12 seam tests belong to the QA compatibility slice and consume P04's
current manifest interface; they do not close P04 actual Worker/restore.
GHSA-prmc-fg87-r4gh affects authenticated cross-origin HTTP redirects in 2.43.6.
The selected notifier uses PostgreSQL/SMTP, not that HTTP node path; private
workflows are uninspected. P08 evaluates the advisory and image update under
its own consumer/recovery contract; P05 does not upgrade the image.

### Existing CI admission residual

The CI writer's read-only `scripts/validation/run-ci-gate.py --profile changed
--explain` returned nonzero for only `[ci-gate-public-execution-parity]`:
`leaf.p03-hermes: every invocation requires selected validator or exact internal admission`.
This observation used the current worktree at base HEAD e14ebe0…; it is not a
remote CI result or a clean-baseline execution inferred from unchanged HEAD.
The same residual was recorded in P04 history and remains P03/CI-owned. The
probe-time contract SHA is `0fd5cad491be3030c2bc90676f8b3abf1910009f312afd502457a5cd5453b79a`,
validator `454e4883ff9253c5b0c8977c2e155b746296d55e593167989262238d81b36d5c`
and runner `9a7a8bdf327fa12efc322bd9553f04a271b7d0c2e1820b8cceeff46d71eee457`.
After the later P05 registration-helper selector addition, the final current
contract SHA is `95deb0da017de31f2c07998358c38d31d483ba245e939a2bc3b26f12a828f997`.
That source change is not a newly executed explain result or a resolution of
the unchanged P03 admission failure.
No route/admission rule is weakened to hide this failure; passing P05 local
checks cannot resolve it. No prior raw receipt exists for this CI-writer probe;
its reported command/result and these public fingerprints are the available evidence.

### Final public census and source comparison

The no-render `scan --connections` completed successfully at
2026-11-02T11:52:56.169761Z, followed by metadata validation PASS. Accessible
file-entry coverage is41857/41857; public file rows2311, text denominator2304.
Six fingerprint-matching complete review records are reused and80 partial
records are separate; hashing did not create review credit. This scan did not
render any of17 discovered entrypoint cases. Actual declared-service operation
and restore remain0/112 each; owned fixture containers never increment those
operating denominators. Declaration analysis produced223 contextual service
rows and31 connections from68 candidate sources (16 extracting sources, one
unhandled source). These lists are not full product registration or execution.

Against the clean e14ebe0… source baseline, Git/source fingerprints show10 new,
21 modified and zero removed public paths, with31 unique P05 writer leases.
HEAD remains the same and the current branch is codex/p05-n8n-outbox-recovery.
The separate comparison to the prior published P04 payload shows10 additions,
26 changes,26 invalidated review inputs and2 invalidated connection inputs.
Its five extra changed paths are already-committed P04 post-scan updates:
Task0043, the generated catalog, manifest README, URI test and P02 test.
They are not P05 source edits, and completed/P04 Task bodies remain unchanged
against HEAD. Comparison artifacts are `git-source-comparison.json` and
`published-inventory-comparison.json` in the ignored P05 analysis directory.
No clean-start full accessible-file census is invented from this source baseline.

The generated inventory excludes its own hash to prevent recursive calculation.
Final evidence-only Task edits refresh only their dependent fingerprint/review/
writer rows after validation; they do not rerun global render or claim a new
whole-corpus body review. Public changes are31 owned paths; private metadata
remains local. Operating/data-owner grants are not inferred from these leases.

### Final reviews and registered local checks

Independent document reviewer `/root/p04_infra` approved all fourteen matching
Doc/DATA hashes, all31 unique P05 writer leases and before/current fingerprints,
plus the native receipt's exact recovery limits. The one CI fingerprint-epoch
wording finding was corrected and narrowly re-approved at packet
`2ef5d82f207a9c524d1669444ea4fc3e86cf18dd4829da3f7e872450e21fe23b`.
The present changes only add actual verification evidence and refresh dependent
Task/Data metadata; they do not change tested source or the approved living docs.

The CI writer reported exit0 for changed metadata (base e14), links alignment,
operations catalog, Registry/contracts and corpus lifecycle. `graphify update .`
completed exit0 as AST-only:97 unsupported/non-shebang files skipped,20 SQL and9
HCL files lacked optional tree-sitter parsers, and5 other code files had no symbols.
No dependency was installed, and these formats were not graph/semantically
validated. The source graph was unchanged by the final evidence-only correction;
no redundant graph rerun is claimed.

The existing Node package's `npm audit --package-lock-only --ignore-scripts --json`
first failed restricted DNS, then passed in the authorized host context with zero
vulnerabilities across155 lockfile dependencies. No install or lifecycle script
ran. This is source-package lock audit, not container-image/SBOM/provenance PASS.
`pip-audit` was absent from PATH and no Python manifest/lock changed; it was not
invoked or installed. Python audit remains NOT_RUN/tool-unavailable and is handed
to P08 with the broader supply-chain scope. The sanitized secondary report is
`_workspace/repo-support/analysis/p05/local-gate-summary.json`; it labels CI-writer
reports rather than inventing a new documentation-writer execution.

At this evidence freeze the normal staged wrapper still awaits final staging;
its result is NOT_RUN here. The final exact staged payload must pass that wrapper
before the local logical commit. Remote CI remains NOT_RUN, and the unchanged
P03 global explain/admission failure remains unresolved by these local checks.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Issued P05 baseline and leases | 72 | W77 | Git/status and public source fingerprint readback | Clean e14ebe0fd5e562f8c7557bd9408a1985d9971c5c and governing sources | PASS | Inputs and Authorization; doc-baseline.json at 2026-11-02T10:07:03Z | required | - |
| SQL recovery source initial RED | 73 | W78 | SQL source and immutable migration contracts | New007 absent | FAIL | SQL writer: missing007 before implementation | required | - |
| SQL recovery source GREEN | 73 | W78 | SQL source and immutable migration contracts | Frozen007/008 and focused tests | PASS | Two focused checks GREEN;19 combined contract checks; actual PG NOT_RUN | required | SQL recovery source initial RED |
| Independent SQL source review | 73 | W78 | Exact frozen SQL code/security review | 0078fc05ddc…;008f0f39f09… | PASS | Independent /root/p04_uri source review: no actionable finding; actual PG semantics separate | required | - |
| Independent Node source review | 75 | W80 | Exact frozen Node code/security review | Current writer frozen package | PASS | Independent /root/p04_pipeline same-five-hash source review: approved; native Worker separate | required | - |
| Restricted loopback environment | 75 | W80 | Owned loopback Nodemailer STARTTLS cases | Initial restricted process | FAIL | Eight EPERM failures opening loopback; no actual credential | required | - |
| Authorized loopback STARTTLS | 75 | W80 | Owned loopback Nodemailer STARTTLS cases | Same synthetic CA/account cases on authorized host | PASS | Eight loopback cases; full package38PASS0skip; line97.51/branch95.56/function88.57 | required | Restricted loopback environment |
| P08 source-binding parity initial RED | 72 | W77 | Current canonical source-preparation bundle parity | Old8792… Compose hash/current63c9… | FAIL | Focused1FAIL0.016s; prior history preserved | required | - |
| P08 source-binding parity GREEN | 72 | W77 | Current canonical source-preparation bundle parity | Updated17-input SOURCE_REVIEW_ONLY mirror binding | PASS | WorkflowVersionBundle8PASS0skip0.099s; root independent mirror/history review approved | required | P08 source-binding parity initial RED |
| P12 offline seam initial RED | 73 | W78 | Offline manifest quarantine/data-version seam | Current P04 interface against old seam | FAIL | Six tests/five failures0.036s | required | - |
| P12 offline seam GREEN | 73 | W78 | Offline manifest quarantine/data-version seam | Updated independent hash and quarantine assertions | PASS | Seven tests0.046s; root combined rerun15PASS2SKIP; no actual DB/Worker/P04 restore proof | required | P12 offline seam initial RED |
| Living-document review initial findings | 73 | W78 | Nine living-document changed-contract review | Function-count wording and historical V6 attribution | FAIL | Independent reviewer two minor findings; source behavior unchanged | required | - |
| Living-document review corrected | 73 | W78 | Nine living-document changed-contract review | Nine matching hashes at first document freeze | PASS | Independent /root/p04_infra re-review approved packet d5da1164…; no remaining finding | required | Living-document review initial findings |
| SQL-only runtime initial refusal | 73 | W78 | Guarded actual PostgreSQL recovery behavior | First driver expected incorrect direct-call SQLSTATE before007 | FAIL | First attempt stopped; cleanup PASS; original failed receipt retained | required | - |
| SQL-only runtime corrected | 73 | W78 | Guarded actual PostgreSQL recovery behavior | Exact cached PG and existing explicit owner context | PASS | sql-native-summary.json:14behavior items PASS41.292s; direct42501; migration/drift/checker PASS; cleanup PASS | required | SQL-only runtime initial refusal |
| SQL QA driver coverage | 73 | W78 | New Python QA driver line coverage80percent | Actual SQL-only driver trace | FAIL | 224/284=78.87323943661971%; native-only driver trace; stored-function coverage not measured | required | - |
| Combined SQL QA driver coverage | 73 | W78 | New Python QA driver line coverage80percent | Native trace plus separate successful source-unit trace | PASS | sql-qa-coverage-supplement.json:14proven disjoint lines; conservative238/284≥83.8028%; driver only, no stored-function coverage claim | required | SQL QA driver coverage |
| Independent focused Python regression | 73 | W78 | Six-module related source/unit regression | n8n outbox workflow/contract/rehearsal;P12 seam;P05 SQL/native modules | PASS | Parent independent run32tests:31PASS1SKIP,exit0; skipped owned runtime prerequisite is not runtime acceptance | required | - |
| Independent package coverage rerun | 75 | W80 | Registered Node package coverage command | Same public package; approved host-local owned loopback | PASS | CI author rerun38/38PASS2.366s; line97.51/branch95.56/function88.57; restricted loopback attempt blocked separately; no native Worker proof | required | - |
| Full candidate native first attempt | 75 | W80 | Current-artifact n8n STARTTLS credential/recovery rehearsal | First reviewed candidate and owned synthetic fixture | FAIL | Actual ERROR134.276s:existing secret-env guard rejected key-file path variable before Mailpit;DB/Valkey prepared;Worker/SMTP/refresh/restore NOT_RUN;cleanupPASS | required | - |
| Docker-free scenario controls | 73 | W78 | Stateful fixture control-flow and whole-source line coverage | New13scenario cases plus4guards; no Docker/services | PASS | First scenario-qa-summary.json preserved before-active-fix:17PASS0skip; fixture446/44899.5536%; recovery22/2395.6522%; mutation3expectedFAIL; initial packet superseded by latest reviewed source below | required | - |
| e38 Docker-free scenario controls | 73 | W78 | Stateful fixture control-flow and whole-source line coverage | Latest14scenarios+5guards, already-inactive readback, no Docker | PASS | Current scenario-qa-summary.json:19PASS0skip; Python447/44999.5546%,recovery22/2395.6522%; actual separate mutation3expectedFAIL; embeddedJS/native excluded; independent /root/p04_uri19PASS and coverage/mutation recomputation approved | required | - |
| Full candidate native second attempt | 75 | W80 | Current-artifact n8n STARTTLS credential/recovery rehearsal | Corrected file-path CLI; unchanged readiness guard | FAIL | Actual ERROR463.761s at300sMainreadiness; candidate dist owner1000 vs requiredroot;Mailpithealthy,DB/Valkeyready;Worker/refresh/restore NOT_RUN;cleanupPASS/owned0 | required | - |
| Candidate-owner scenario controls | 73 | W78 | Stateful fixture control-flow and whole-source line coverage | Helper4199be5a/guardb295ab96/scenario97dcc2ec | PASS | Current summary21PASS0skip; Pythonhelper511/51399.6101%,recovery22/2395.6522%; actual separate mutation3expectedFAIL; embeddedJS/native excluded; independent /root/p04_uri21PASS/recomputedcoverage approved | required | - |
| Existing global CI admission residual | 72 | W77 | Global changed-profile public-execution admission | Current worktree at basee14ebe0; unchanged P03 leaf | FAIL | CI writer readonly explain nonzero:leaf.p03-hermes requires selected validator or exact internal admission; separate P03/CI handoff; not remote CI | required | - |
| Full candidate native third attempt | 75 | W80 | Current-artifact n8n STARTTLS credential/recovery rehearsal | Reviewed root-owned candidate and unchanged stage limits | FAIL | Actual ERROR485.257s:60simport:workflow bound in workflow_binding;Mailpit/Main/Workerready200+Runnerregistered;firstbusiness/SMTP/refresh/restoreNOT_RUN;cleanupPASS | required | - |
| Registration scenario controls | 73 | W78 | Stateful fixture control-flow and whole-source line coverage | Nativea0c99bb5/registration074291db/scenarioe9d5c6fa | PASS | Current summary23PASS0skip; Pythonnative516/51899.6139%,registration100/10694.3396%,recovery22/2395.6522%; embeddedJS/realREST/native excluded; independent /root/p04_uri23PASS/recomputedcoverage approved | required | - |
| Final candidate native quiesced rehearsal | 75 | W80 | Current-artifact n8n STARTTLS credential/recovery rehearsal | Reviewed editorREST candidate9dea1967/bindingd4b51cee | PASS | native-editor-rest-receipt.json:747.701s,6terminalexecutions;TLSAUTHqueue/unknownnoextra/sameIDrefresh/gen2samekeyrestorePASS;QUIESCED_ONLY/liveinflightTEST_RESIDUAL;cleanupPASS/owned0 | required | Full candidate native first attempt, Full candidate native second attempt, Full candidate native third attempt |
| Final workspace inventory and comparisons | 72 | W77 | Workspace metadata validation and scoped source comparison | Frozen source;no-render scan--connections | PASS | Scan41857entries/2304text/6complete80partial;validatePASS;clean-e14diff10new21modified0removed;priorpublished10new26changed+2connections;operating0/112 | required | - |
| Final independent document review | 72 | W77 | Exact Doc/DATA scope and writer-fingerprint review | Fourteen matching hashes;31uniqueP05leases | PASS | Independent /root/p04_infra approved all; sole minor CI epoch wording corrected/reapproved; native recovery limitations preserved | required | - |
| Final registered document and catalog gates | 72 | W77 | Registered metadata/links/catalog/Registry/lifecycle checks | Frozen current source/documents at basee14 | PASS | Actual CI writer exit0 for changedmetadata,links,catalog,Registrycontracts,corpuslifecycle; local-gate-summary.json secondary report | required | - |
| AST knowledge graph update | 72 | W77 | AST-only graphify update command | Final tested source | PASS | Exit0;97skipped,20SQL+9HCLmissingoptionalparsers,5othernosymbols;no dependency install/fullsemanticclaim | required | - |
| Restricted Node package audit | 75 | W80 | Selected Node package lock audit | Existing unchanged package lock | FAIL | Restricted DNS failure only; no installation/scripts | required | - |
| Authorized Node package audit | 75 | W80 | Selected Node package lock audit | Same existing lock/authorized host context | PASS | npm audit--package-lock-only--ignore-scripts--json:0vulnerabilities/155deps,exit0;not container-image/provenance audit | required | Restricted Node package audit |
| Python dependency audit availability | 73 | W78 | Applicable Python audit capability | No Python manifest/lock changes;pip-audit PATH check | NOT_RUN | Tool absent/notinvoked/notinstalled;no Python auditPASS;P08supply-chain handoff | required | - |
| Normal staged payload wrapper | 72 | W77 | Registered normal local-staged validation | Final staging after this evidence update | NOT_RUN | Await exact staging/actual hook receipt; no prospectivePASS | required | - |
| Notifier retry/recovery source and tests | 73 | W78 | Approved SQL/Node/native normal-rejection-recovery checks | Reviewed final components and actual owned receipts | PASS | SQL14behavior,Node38tests and native6executions/quiescedrestorePASS; liveactiveSMTPinterruption explicitly TEST_RESIDUAL | required | - |
| Selected binary/storage contract | 74 | W79 | Exact-source and input.binary rejection checks | Tagged2.43.6 binary-data.config.ts and selected node/test | PASS | Tagged unset-mode queue→database fallback; node binary/cardinality rejection in38PASS; no new storage/consumer and actual overrides uninspected | required | - |
| Isolated STARTTLS and same-ID refresh | 75 | W80 | Owned authenticated SMTP and next-execution credential tests | Synthetic isolated fixture only | PASS | Actual final receipt:Worker/Bull/TLSAUTH/sameIDnext-exec/old-newnegatives/restoredcredentialPASS; operating delivery/rotation NOT_RUN | required | - |
| Restore replay and interruption guards initial RED | 73 | W78 | Restore equivalence, same-input replay, next-claim and active-send interruption guards | New guard tests before validators existed | FAIL | replay-residuals/guards-red.log:14tests,6errors(validators absent),1native SKIP | required | - |
| Restore replay and interruption guards GREEN | 73 | W78 | Restore equivalence, same-input replay, next-claim and active-send interruption guards | Native f9a90053/recovery 61c11dce and scenario doubles | PASS | 33tests:32PASS1nativeSKIP;5separate weakenings RED(3/2/1/2/1);new executable lines native172/173,recovery56/56;no Docker | required | Restore replay and interruption guards initial RED |
| Native replay/interruption invocation attempt | 73 | W78 | Current-artifact native restore replay and active-send interruption rehearsal | Same candidate 9dea1967/binding d4b51cee, selection env omitted | FAIL | Actual ERROR1.872s at preflight:exact image/context selection required;no container created;cleanupPASS | required | - |
| Native replay/interruption barrier refusal | 73 | W78 | Current-artifact native restore replay and active-send interruption rehearsal | Interruption before quiesced restore | FAIL | Actual ERROR724.780s:held mid-DATA,stop0.487s,row unknown;interrupted execution not terminal;quiesced barrier refused restore;cleanupPASS/retained none | required | - |
| Native replay/interruption rehearsal | 73 | W78 | Current-artifact native restore replay and active-send interruption rehearsal | Interruption after restore checks with in-place worker recovery | PASS | native-run3-receipt.json cf43208d:852.821s;restored10rows identical;5replayed/0claimable;next claim fresh-only;held mid-DATA,stop0.411s,row unknown;broker job survived(1);no resend,fresh accepted;cleanupPASS/owned0 | required | Native replay/interruption invocation attempt, Native replay/interruption barrier refusal |
| Independent replay/interruption code review | 73 | W78 | Independent code review of the replay/interruption increment | Branch commits through 8a1b32892 before correction | FAIL | CHANGES_REQUESTED:stopped-worker facts could not exclude the transport 5s socketTimeout(important);latency excluded polling;substring run_id filter(minor);re-review pending | required | - |
| Review-fix guards initial RED | 73 | W78 | Kill-based interruption, hold timing and parsed run_id guards | New guards before the correction | FAIL | review-guards-red.log:16tests,2failures,1error(parse_hold absent),1native SKIP | required | - |
| Review-fix guards GREEN | 73 | W78 | Kill-based interruption, hold timing and parsed run_id guards | Native 6fdb8b62/recovery e924d9f3 and scenario doubles | PASS | 35tests:34PASS1nativeSKIP;6weakenings RED(1/3/2/1/1/1);loopback timeout close5004ms vs kill346ms;new lines native196/198,recovery88/88 | required | Review-fix guards initial RED |
| Native kill-based interruption rehearsal | 73 | W78 | Current-artifact native restore replay and active-send interruption rehearsal | Rebased d94f7440c, same candidate 9dea1967/binding d4b51cee | PASS | native-run4-receipt.json b21b2f7b:731.029s;restore/replay/next-claim as attempt3;session open at kill,close1020ms<5000,row sending;expired lease→unknown/1/lease_expired_delivery_unknown,no resend,fresh accepted;broker job survived(1);cleanupPASS/owned0 | required | - |
| Independent replay/interruption code re-review | 73 | W78 | Independent code review of the replay/interruption increment | Correction d94f7440c and TSK-0044 v0.3.0 | PASS | APPROVED: kill-based interruption requires `sending` and a sub-5000 ms close against `socketTimeout: 5000`; latency from the hold timestamp; parsed run_id filter; the fixture-only lease expiry targets only the interrupted `sending` row and rejects zero or several rows | required | Independent replay/interruption code review |
| n8n stall-recovery guards initial RED | 73 | W78 | Interrupted queue job recovery and terminal-execution barrier guards | New guards before validate_queue_recovery and old_executions_terminal existed | FAIL | interrupted-job-recovery/guards-red.log:37tests,10failures,3errors,1native SKIP | required | - |
| n8n stall-recovery guards GREEN | 73 | W78 | Interrupted queue job recovery and terminal-execution barrier guards | Commit 54194cbbc and scenario doubles | PASS | 37tests:36PASS1nativeSKIP;5weakenings RED(9/1/5/3/1);new lines since 729d16da7 native29/29,recovery13/13;no Docker | required | n8n stall-recovery guards initial RED |
| Post-restore capture-order guard RED | 73 | W78 | Post-restore capture ordering guard | Double refusing an older capture as SQL001 does, before the fix | FAIL | interrupted-job-recovery/capture-order-red.log:37tests,2failures,1native SKIP | required | - |
| Post-restore capture-order guard GREEN | 73 | W78 | Post-restore capture ordering guard | Commit 1d76b7135 | PASS | 37tests:36PASS1nativeSKIP; mutations still RED | required | Post-restore capture-order guard RED |
| Native stall-recovery invocation attempt | 73 | W78 | Current-artifact native interrupted-job recovery and restore rehearsal | Same candidate 9dea1967/binding d4b51cee, base id selected | FAIL | Actual ERROR0.282s at preflight:exact candidate image selection required;no container;cleanupPASS | required | - |
| Native stall-recovery capture-order refusal | 73 | W78 | Current-artifact native interrupted-job recovery and restore rehearsal | Commit 54194cbbc | FAIL | Actual ERROR832.489s:n8n job1→0,execution crashed38.389s;barrier PASS(7 terminal);restore/replay PASS;post-restore publish historical(older capture);cleanupPASS/owned0 | required | - |
| Native stall-recovery restore rehearsal | 73 | W78 | Current-artifact native interrupted-job recovery and restore rehearsal | Commit 1d76b7135, same candidate 9dea1967/binding d4b51cee | PASS | native-run3-receipt.json 47b1b878:799.181s;kill close911ms,row sending;job survived(1)→n8n removed(0),execution6 crashed38.074s;lease expiry unknown/1/lease_expired_delivery_unknown,no resend;barrier PASS with executions1–7 terminal;14rows identical;7replayed/0claimable;next claim fresh-only;cleanupPASS/owned0 | required | Native stall-recovery invocation attempt, Native stall-recovery capture-order refusal |
| Stall-recovery changed metadata initial | 73 | W78 | Changed-document metadata against origin/main | Runbook RUN-0053 v1.9.0 and this Task | FAIL | check-changed:1violation runtime-version-literal(image tag in runbook body) | required | - |
| Stall-recovery changed metadata corrected | 73 | W78 | Changed-document metadata against origin/main | Runbook names the Dockerfile N8N_VERSION instead of a tag | PASS | check-changed selected2 violations0; links mode all PASS; corpus lifecycle 0; operations catalog PASS | required | Stall-recovery changed metadata initial |
| Independent stall-recovery code review | 73 | W78 | Independent code review of the stall-recovery increment | Commits 54194cbbc,1d76b7135 | NOT_RUN | No independent reviewer ran in this session | required | - |
| Independent stall-recovery code re-review | 73 | W78 | Independent code review of the stall-recovery increment | Commits 54194cbbc, 1d76b7135, 04df40b4d, 155e8d579 plus the minor-finding fix | PASS | APPROVED, no Critical/Important: assertions need n8n-driven job removal and a `crashed` execution (probe scans all job states, exact 1/0 ints); no queue deletion or barrier weakening; 150 s bound derived from lock and stall intervals; session cookie stripped from receipts; runbook step approval-gated. Minor findings fixed: only the settle timeout is tolerated, the job count uses the full probe result via `broker_job_count` (new test RED then GREEN, P05 suites 38 tests OK, 1 native skip) | required | Independent stall-recovery code review |
| Main-restart and retry guards initial RED | 73 | W78 | Main-restart queue recovery and crashed-execution retry guards | New guards before validate_main_restart_recovery and validate_execution_retry existed | FAIL | 20 tests: 2 errors (missing validators), 1 native SKIP | required | - |
| Main-restart and retry guards GREEN | 73 | W78 | Main-restart queue recovery and crashed-execution retry guards | Commits 69e47d4ec through ef2ca463a and scenario doubles | PASS | P05 unit and scenario tests all OK, 1 native SKIP; doubles refuse no startup recovery, stale runner, retry claim/resend/unbound, non-empty stack, same-date input | required | Main-restart and retry guards initial RED |
| Native main-restart and retry attempts 1-11 | 73 | W78 | Current-artifact native main-restart recovery and crashed-execution retry rehearsal | Commits 69e47d4ec through 6db614394 | FAIL | main-restart-retry/native-attempt*.log: causes in the Failed attempts table; cleanup PASS, owned residue 0 each | required | - |
| Native main-restart and retry rehearsal | 73 | W78 | Current-artifact native main-restart recovery and crashed-execution retry rehearsal | Commit a4bf785d9, candidate 9dea1967/binding d4b51cee | PASS | native-run13-receipt.json 84f8eda3: 980.804 s; main-restart job 1→0, running→crashed 61.262 s, data 1→1; retry error/not_started, retry execution 10 terminal and fenced, 0 claimed, 0 resent, outbox unchanged; new execution delivered; barrier 1–11, restore, replay PASS | required | Native main-restart and retry attempts 1-11 |
| Independent main-restart and retry code review | 73 | W78 | Independent code review of the main-restart and retry increment | Range f0ce46fda..174155ab5 | FAIL | CHANGES_REQUESTED: 2 Important (500 mapping could hide a late claim; retry executions outside barrier), 4 Minor | required | - |
| HOME n8n recovery target inspection | 73 | W78 | Read-only HOME queue and execution target check | mng-valkey mnginspector and read-only n8n metadata session, 2026-11-05 | PASS | jobs active/wait/delayed/paused/failed absent; 0 new/running executions; Opsflow notifier not installed; no restart run | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 72 | pending | Issued P05 baseline and leases, P08 source-binding parity GREEN, Final workspace inventory and comparisons | REUSE_ACCEPTED only for original C19/C22 scope; current source/image/runtime equivalence separate. | SPEC-0212 TSK-0044 |
| 73 | pending | SQL recovery source GREEN, Independent SQL source review, SQL-only runtime corrected, SQL QA driver coverage, Combined SQL QA driver coverage, Final candidate native quiesced rehearsal, Restore replay and interruption guards GREEN, Review-fix guards GREEN, Native kill-based interruption rehearsal, Independent replay/interruption code re-review, n8n stall-recovery guards GREEN, Post-restore capture-order guard GREEN, Native stall-recovery restore rehearsal, Independent stall-recovery code re-review, Main-restart and retry guards GREEN, Native main-restart and retry rehearsal, HOME n8n recovery target inspection | TEST_RESIDUAL: reviewed source and actual SQL-only behavior PASS; native-only driver trace below80 but combined conservative83.8028% meets80; paired DB/metadata+same-key fresh credential consumption PASS; isolated same-input replay, restored outbox-state equivalence and next-claim PASS; the stopped-worker interruption result was superseded by review, and the SIGKILL mid-DATA interruption with lease-expiry recovery PASS (Native kill-based interruption rehearsal); the correction passed independent re-review. The two former residuals pass in the isolated fixture through n8n 2.43.6's own stall recovery (Native stall-recovery restore rehearsal): the surviving job was removed by n8n, the interrupted execution became `crashed`, and the strengthened barrier then accepted restore. The criterion passed independent review; it stays TEST_RESIDUAL because the same-input replay covers repeated publication, not replay of an n8n execution, and HOME operation is NOT_RUN. | SPEC-0212 TSK-0044 |
| 74 | pending | Selected binary/storage contract | NO_CHANGE for storage adoption; scoped source/rejection checks PASS, installed/private override and operational behavior separate. | SPEC-0212 TSK-0044 |
| 75 | pending | Isolated STARTTLS and same-ID refresh, Final candidate native quiesced rehearsal | SOURCE_READY with scoped actual native increment PASS; formal owner acceptance, actual P06 producer and operating rotation remain separate. | SPEC-0212 TSK-0044 |

## Review and Completion

Current source and owned isolated implementation receipts are recorded above.
Independent source/document reviews, metadata/links/catalog/Registry/lifecycle
checks and source comparison are complete within their stated scopes. The
normal staged wrapper awaits final staging and must pass before commit; Python
audit is tool-unavailable, and remote CI is NOT_RUN. Same-input replay,
restored outbox-state equivalence and SIGKILL mid-DATA interruption with
lease-expiry recovery have isolated native PASS. The review's
CHANGES_REQUESTED finding is fixed and passed re-review. Restore after an
interrupted broker job now has isolated native PASS through n8n's own stall
recovery, and the interrupted execution is recorded `crashed`. With main also
restarted, the leader's startup queue recovery records it `crashed` (isolated
native PASS). n8n's retry of a crashed execution was measured as a no-op, and
replay is a new execution. HOME inspection found no target, so the HOME
restarts are NOT_RUN. P03 global CI
admission remains an explicit residual.
All future outcomes must bind exact source, actor, environment, time and receipt
without cancelling accepted history or promoting a lower evidence axis.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Workspace inventory](../../../90.references/data/0096-workspace-inventory/README.md)
- [P04 data path residual](tsk-0043-opsflow-data-path.md)
- [Historical P05 notifier Task](../../0204-service-integration-security-and-operations/tasks/tsk-0013-p05-n8n-outbox-notifier.md)
