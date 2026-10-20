---
title: "n8n Native Notification Rehearsal Task"
version: "0.2.2"
type: "sdlc/task"
status: "blocked"
owner: "@buenhyden"
updated: "2026-10-20"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0019"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-16"
---

# n8n Native Notification Rehearsal Task

## Overview

### Objective

W74 prepares and, after independent prechange and safety approval, executes the
existing inactive notifier workflow through a genuine n8n queue worker,
external task runner, PostgreSQL outbox and isolated Mailpit SMTP capture. It
also proves explicit no-send reconciliation and serial empty restoration of
separate n8n metadata and DEV databases. This is supporting evidence for
criterion 19; TSK-0013 remains its durable acceptance owner.

## Inputs and Authorization

The direct infrastructure request and controller's bounded 2026-10-16 dispatch
authorize six focused test files, this draft Task and W74 registration. The
fixture uses only synthetic random credentials in an owned 0700 attempt
directory with 0600 files. It has no host ports, HOME or LAB mounts, live
volumes, real external SMTP, private keys or external applications. The
tracked workflow, custom node, SQL migrations and package files remain frozen.

Exact reviewed images are created by immutable ID with separately verified
runtime config identity. The n8n candidate is bound to source binding
`03892eb1a9a485b454e48c8222ecebc116d67a846560bf97fb8a783e5f6d8985`.
The runners and Mailpit images use their reviewed linux/amd64 digest
descriptors. All Docker creates remain blocked until the independent reviewers
approve the frozen source and a fresh host readiness check passes.

## Work Log

### W74 source and execution boundary

The steady seven-container topology is capped at 3136 MiB and 1.60 CPU:
metadata PostgreSQL, DEV PostgreSQL, Valkey, n8n main, n8n worker, external
runner and Mailpit. Four internal networks expose no host ports. Exact aliases
provide only the required control, runner, DEV and capture paths. Every steady
service role uses a read-only root, capability drop, no-new-privileges, fixed
nonroot user,
equal memory/swap limit, CPU/PID limit and reviewed tmpfs. PostgreSQL's declared
`/var/lib/postgresql` volume is covered by uid70 tmpfs and anonymous volumes are
rejected. The bounded transient `secret-prep` role alone uses root with only
`CHOWN`, 32 MiB, 0.05 CPU, 16 PIDs, no network and one exact bind before its
immediate removal. The workload cutoff is T+780 seconds, reserving 120 seconds
for exact identity-checked cleanup within the 15-minute attempt deadline.

The host lock is shared with W75. Existing owner-labeled containers or networks,
either fixture's stale attempt directory, name collision, insufficient
headroom, wrong image/config identity or changed secret metadata fails before
create or start. Docker work calls are bounded to 60 seconds. Partial create
and network failures retain immutable pending ownership records before
returning a sanitized failure. Cleanup adopts only exact pending identities,
requires a final empty attempt-label sweep and retains identities it cannot
remove. Host cleanup validates device, inode, owner, mode and link count and
never uses recursive deletion.

SwapFree remains a recorded receipt value but is not a standalone admission
predicate. The host's configured swap occupancy is stale capacity evidence and
does not by itself describe pressure during this bounded run. Admission retains
the 7 GiB available-memory floor, the 3 GiB runtime stop-new-work floor, CPU,
disk and inode thresholds, serial ownership, and exact per-container
`MemorySwap == Memory` limits. The independent coordinator requires both
bounded interval endpoints to report memory PSI full `avg10=0.00` and
`avg60=0.00`, with zero `oom_kill` and `pswpout` deltas. PSI full-total
microseconds remain recorded evidence rather than an admission predicate. The
fixture separately checks the 3 GiB available-memory floor before Docker work;
this operational observation is not a continuous watchdog and does not weaken
the fixture's hard caps.

The imported private workflow copy changes only execution retention settings
needed for a safe terminal execution oracle. Its tracked and bound SHA256 plus
the three-field settings delta enter the sanitized receipt. Each manual run must
reach a terminal REST execution state before the next seed or phase. Successful
delivery additionally requires the terminal `Acknowledged` Code node, proving
the external runner completed actual graph work. The ambiguous SMTP path must
terminate in error after the redaction Code node and persist `unknown` with no
acceptance time, token, lease or capture increase.

Before operator `not_sent` reconciliation, the old execution is terminal,
worker and runner are stopped, the notifier has no database session and the
isolated capture count is unchanged. The event records the exact attempt and a
SHA256 of the fixture-only pre-accept connect failure. This does not prove an
accepted-response-loss case or exactly-once delivery. After explicit
reconciliation, one new terminal execution may send and acknowledge the row.

Restoration stops all writers and verifies zero non-admin sessions before both
dumps. Roles are dumped without passwords; separate random synthetic role
passwords are reapplied from private inputs. Binary dumps move only through
uid70-owned bounded bind files, with size and SHA256 checked before and after
generation replacement. Old containers are removed before empty generation-2
targets start. Restored inactive workflow and audit history must persist, old
rows must not resend and a new terminal execution must capture once.

### Source preparation receipt

The default command `python3 -m unittest
tests.validation.test_opsflow_native_boundaries
tests.validation.test_opsflow_native_rehearsal` passes sixteen boundary guards and
skips the actual native case once without the complete exact selector. The
guards cover partial/wrong opt-in, aggregate resource caps, nonzero and raised
partial-create recovery, raised network-create recovery, late cleanup adoption,
final residual denial, failed stop/removal identity retention, repeated DEV
cluster hardening, cleanup receipt emission after a boundary failure and safe
ordinary-network mismatch diagnostics. Those diagnostics expose only lifecycle,
expected-keyset, empty-versus-matching network-ID and required-alias booleans.
Successful cleanup now emits explicit empty failure and final-sweep ID lists in
addition to empty retained and pending identities. Scoped Ruff lint and format
checks pass.

The first independently approved attempt
`opsflow-native-6fe0cd2ae23f5bad8a58a6b4` ended `ERROR` after 3.627 seconds
when the transient `secret-prep` container's pre-start network metadata did not
match the original empty-network assertion. Docker 29 represents `--network
none` as an exact built-in `none` endpoint, verified read-only after cleanup.
No service container started and no database or workflow phase began. Cleanup
passed its final label sweep with no retained container, network, pending role
or attempt directory. The sanitized pre-create values were 10,633,192 KiB
available memory, 3,093,116 KiB free swap, 18,167,554,048 bytes free disk and
75% free inodes.

The first correction modeled the post-start `none` endpoint. The independently
approved retry `opsflow-native-bba6e2f639b1355d7b51d8b7` then ended `ERROR`
after 2.510 seconds at the same pre-start check, with only the safe categories
`network` and `security`. Cleanup again passed with no retained identity,
pending role or attempt directory. Its sanitized pre-create values were
10,873,480 KiB available memory, 3,099,516 KiB free swap, 18,128,121,856 bytes
free disk and 75% free inodes. Independent prechange review identified the
created-state no-network representation as empty endpoint IDs until start. The
next source correction therefore distinguishes the address-free `created`
endpoint from exact built-in-ID `running`/`exited` endpoints. It also records
only boolean field-shape facts if the no-network contract fails again.
The separately authorized exact runner and Mailpit digest pulls occurred after
the corrected n8n build was idle.

A separately approved no-start probe
`opsflow-native-93e3b15d55cd683a7cc48aec` created only the exact transient
Valkey `secret-prep` container, with no network creation, mount, secret, start
or exec. The created-state no-network contract passed; the probe ended
`PROBE_ERROR` only on the `security` category. Cleanup and final sweeps passed
with no retained identity, pending role or attempt directory. Its sanitized
pre-create values were 10,290,260 KiB available memory, 3,098,236 KiB free
swap, 18,149,117,952 bytes free disk and 75% free inodes. The diagnostic now
records booleans for exact CapDrop, prefixed and declared CapAdd spellings and
the equals and colon SecurityOpt spellings, without recording actual values.
The Docker interfaces may expose the sole allowed CHOWN capability as `CHOWN`
or `CAP_CHOWN`, while the CLI parser preserves the non-seccomp security-option
string. The corrected inspect contract maps only those two closed spellings to
one semantic CHOWN and rejects duplicates, malformed names and every other
capability. Raw capability metadata must be null or an exact string array;
CapDrop and SecurityOpt must be exact singleton string arrays, so mappings,
scalars, mixed elements and duplicate values fail closed. The contract still
requires exact authored `no-new-privileges=true`; the colon security-option
form remains diagnostic only and does not relax the security check.

The next diagnostic entry is the frozen temporary driver
`/tmp/hyhome-n8n-secretprep-lifecycle-probe.py`, SHA256
`ed3e8703a417814af728674ff14348af37e561359d6e5fe47960c0838b11a291`.
The driver and its invocation receipt are regular uid1000, mode 0600,
single-link files. The receipt
`/tmp/hyhome-n8n-secretprep-lifecycle-probe.receipt.json`, SHA256
`a8bc57d26405c3c5620be39d72572f812c445b1d9076718bf38298c6d4e51713`,
binds the driver, cwd, exact clean environment and argv, five source hashes,
resource limits and `NOT_RUN` status.
Its exact invocation is `/usr/bin/env -i PATH=/usr/bin:/bin
PYTHONPATH=/tmp/hyhome-infra-spec0204 OPSFLOW_N8N_NATIVE_IMAGE=sha256:1fda18a541144ae5519ac97bcaffa4e24fad0e71d424606d230464bec8fce153
OPSFLOW_N8N_NATIVE_CONTEXT=default /usr/bin/python3 -B -s -S -P
/tmp/hyhome-n8n-secretprep-lifecycle-probe.py`. It asserts the five reviewed
source hashes before constructing the fixture, limits work to 120 seconds and
cleanup to the 240-second global boundary, and creates one 32 MiB, 0.05 CPU
Valkey `secret-prep` container with user 0, network none, CHOWN and `/bin/true`.
It creates no mount, secret or Docker network. Boolean-only created,
post-start and post-wait network/security facts are captured before contract
assertions; wait must return zero, and the nested finalizer always emits the
sanitized cleanup and retained-identity receipt.

The first lifecycle entry `opsflow-native-3fc3100a8c1de3211ed9edfb` ended
`PROBE_ERROR` after 4.3 seconds before container creation or the first phase
observation because the clean invocation omitted the fixture's two explicit
native image/context selectors. Source hashes matched. Cleanup passed, the
retained and pending identity lists were empty, the attempt directory was
removed, and independent owner-label, attempt-directory and lock checks were
empty/free. The corrected invocation receipt adds only the exact immutable
n8n image ID and `default` context selectors required by the reviewed
preflight. The receipt preserved its pre-run `NOT_RUN` input status and was
then independently approved for one execution.

The corrected lifecycle entry `opsflow-native-82cb863f93407d1cc2931f2d`
reached create, start, wait-zero and post-wait observation. Created-state and
all security facts passed; Docker exposed canonical `CAP_CHOWN`, exact
`no-new-privileges=true` and exact CapDrop. The entry ended `PROBE_ERROR`
because the old validator required a nonempty endpoint ID after exit. Both
post-start and post-wait observations retained the exact built-in `none`
network ID, cleared the endpoint ID and kept all address and optional fields
empty/null. Wait-zero makes the post-wait state definitively exited. Cleanup
and independent final sweeps passed with no retained or pending identity,
attempt directory or held lock. The evidence-based correction now requires
created with both IDs empty, running with exact network ID and valid endpoint
ID, and exited with exact network ID and empty endpoint ID. Other states,
mixed identity shapes, addresses and aliases remain rejected.

The full-run controller is a separate private, single-run packet. Its initial
receipt was `NOT_RUN`. Its protected input-closure manifest binds the package initializers,
storage and shared Docker/DB helpers, this Task, native source, provisioner,
manifest, cluster guard, migrations and tracked workflow before repository
import. The controller retains live-drained stdout and stderr in exclusive 0600
files capped at 2 MiB each, captures exactly one bounded receipt independently,
and prints only a schema-selected controller result. It sends one cleanup-aware
interrupt at T+780, reserves through T+900 for the fixture finalizer, then uses
bounded TERM/KILL group reaping. Every catchable controller exit path reaps the
exact child group. PASS requires exit zero, native and cleanup PASS, no cleanup
failure, and empty retained, pending and final-sweep identities.

The independently approved full entry
`opsflow-native-a82be747a94c2b73a41687c4` ended `ERROR` with child exit 1
after about 21 seconds, before any database or workflow phase. Docker 29 kept
the exact expected owned network name and required alias on the created
container but reported an empty network ID. The safe facts were
`expected_keyset=true`, `network_ids_empty=true`, `network_ids_match=false`,
`required_aliases_present=true` and `state_created=true`; the failure category
was only `network`. Cleanup passed with no failure, swept ID, retained identity,
pending role or attempt directory. Independent owner-label sweeps were empty,
both fixture attempt-directory globs were empty and the shared lock was free.
The bounded private stdout was 1025 bytes with SHA256 `a65795128c6773521ce6925563a6e74d49f501065013af19fc63bca517dddb58`;
stderr was 1749 bytes with SHA256 `290c85d991c37a352174501583b7659562889f5bfeb48f229642e20e30a23301`.
Neither stream overflowed. During the coordinator's interval, `oom_kill` stayed
zero while memory PSI full-total increased by 33,165 and `pswpout` by 28, so
the runtime pressure policy held all retry work.

The evidence-based validator correction keeps the exact owned network-name set
and exact required alias. Created endpoints require empty network and endpoint
IDs; running endpoints require the exact owned network ID and a valid endpoint
ID; exited endpoints require the exact owned network ID and an empty endpoint
ID. Unknown states, foreign networks, malformed IDs and extra aliases remain
rejected. This source correction does not turn the failed entry into a pass and
does not authorize a retry.

The independently approved corrected entry
`opsflow-native-682d738be9149c22cb21b508` used closure `c1e3834d...`,
wrapper `0965f04e...` and invocation `43917855...`. It passed the corrected
created-network boundary, provisioned the isolated metadata and DEV PostgreSQL
clusters, Valkey and Mailpit, and created and started n8n main. It then ended
`ERROR` when the bounded main `/healthz/readiness` check expired, before worker,
external runner, workflow import or any business execution. The private stdout,
stderr and controller receipt were respectively 1,341, 2,588 and 338 bytes with
SHA256 `6d3fa2f11e9d715c5ae2146553e4291bb5bb470dfb83a5a3e6fb73ee45f15a29`,
`a80fea609c20e400d8b954cac43618caa2b1c8ac08efe84d709d141019283bbf`
and `31a3bfdac6eef1bb079ee93174a2c2a8a5695a359ad01c42e9ab21a3063b914e`.
Neither stream overflowed and exactly one receipt was retained.

The automatic receipt truthfully recorded cleanup `FAIL` with `container` and
`host_held_for_owned_resource`: an already absent DEV PostgreSQL container ID
remained in the in-memory pending record, so the exact attempt directory stayed
held. The separately recorded manual reconciliation found no exact-attempt or
owner-labeled container or network, validated and unlinked only the 16 expected
bounded private entries, removed the empty 0700 attempt directory and confirmed
both attempt globs empty and the shared lock free. This is a reconciliation
`PASS`, not a rewrite of the automatic cleanup result. The coordinator measured
zero `oom_kill` and `pswpout` increase but PSI memory full-total increased by
55,409, so all further runtime remains held. The source-only follow-up records
closed boolean state/OOM/exit/log-pattern facts on main-readiness failure and
treats an exact previously verified CID as removed when the post-removal inspect
proves it absent; its focused regressions do not authorize another attempt.
The protected diagnostic-only entry recreates only secrets, owned networks,
metadata and DEV PostgreSQL, Valkey, Mailpit and n8n main, then stops after the
same readiness check. It has a 240-second work cutoff plus a 120-second cleanup
reserve. Controller `PASS` means only that closed main-start evidence and exact
cleanup completed; native workflow, worker, external runner, SMTP, reconciliation
and restore remain explicitly `NOT_RUN`.

The independently approved diagnostic entry
`opsflow-native-f8906dfa40d5ddc79af55c83` ended controller `ERROR` with child
exit 1 after about 149 seconds. It reached `main_started`, obtained an exact
owned-container inspection and found n8n main `exited` with a nonzero exit;
`created`, `running`, `restarting`, exit-zero and OOM-killed were false. The
bounded log tail was available, but every reviewed closed classifier was false:
ready, migration started, migration finished, database initialization,
database authentication, encryption and permission/read-only-filesystem. No
raw log text, environment value, credential or secret entered the receipt.
The worker, external runner, workflow execution, SMTP, reconciliation and
restore remained `NOT_RUN`. This evidence rules out a slow in-progress
migration or CPU-bound readiness wait for this attempt; it does not identify
the immediate exit cause and does not justify increasing the timeout.

Fixture cleanup was exactly `PASS`: `cleanup_failures` and both swept-ID lists
were empty, all retained container, network and pending-role lists were empty,
the attempt directory was null, and independent owner-resource, attempt-glob
and lock checks were empty/free. The private stdout, stderr and controller
receipt were respectively 1,872, 0 and 390 bytes with SHA256
`66ec1b5d1e56061373def0554b06b0b83ec13ce8ebde6f1787934ab7a61cfa89`,
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
and `3eb5efdce509bc78d190c19991ab412cb9fe77d91653b3b977d30f11bf7cc8f7`.
The coordinator observed zero `oom_kill` and `pswpout` increase, while PSI
memory full-total increased by 76,947 microseconds; no rerun is authorized.

Read-only comparison against the immutable image's tracked
`docker-entrypoint.sh` identified the deterministic pre-n8n exit. The entrypoint
requires underscore-named `n8n_db_password`, `n8n_valkey_password`,
`n8n_encryption_key` and `n8n_runner_auth_token` secret paths, while the fixture
mounted hyphenated targets. It also permits the isolated broker only as the
`n8n-valkey:n8n_valkey_password` selection, and its package bridge requires the
configured user folder to exist before Node starts. The fixture used the
unsupported `valkey` selection and a nonexistent `/tmp/n8n-user` path. This
explains the immediate exit before n8n could emit any migration or database
classifier.

The focused entrypoint-alignment guard first failed on the old broker alias.
The minimal source correction mounts the four exact underscore targets, sets
both the entrypoint selection and Bull queue host to the isolated
`n8n-valkey` alias, and uses the existing uid1000 mode-0700 `/tmp` tmpfs as
`N8N_USER_FOLDER`. It neither changes HOME nor weakens the entrypoint's secret,
broker or package checks. The guard and the complete Docker-free suite now pass;
this source-only correction does not convert either actual `ERROR` into a pass
or authorize another run.

The independently approved entrypoint-aligned full entry
`opsflow-native-4acc80c2e4e136cd810ac5c1` used the 19-file closure
`08dbb117...`, wrapper `5431d3c6...` and invocation `cb4a1f3f...`. It ended
controller `ERROR` with child exit 1 after about 162 seconds. The corrected
entrypoint contract prevented the earlier immediate exit: main remained
running with exit-zero metadata, was not OOM-killed, and its bounded log
classifier observed both migration start and finish. The readiness classifier
did not observe the ready marker, while database initialization,
authentication, encryption and permission classifiers were false. This does
not prove slow startup or identify the readiness cause. Worker, runner,
workflow, SMTP, reconciliation and restore remained `NOT_RUN`.

Cleanup was exactly `PASS`, with empty cleanup failures, swept IDs, retained
container and network IDs, pending roles, and a null attempt directory.
Independent owner-resource and attempt-directory sweeps were empty and the
shared lock was free. Private stdout, stderr and controller receipt were 1,612,
2,001 and 336 bytes with SHA256 `bd7c2c3b42b9dd9b27c30e0a212e71b2eda416aa9d8fa89d3fec2e8598f418a0`,
`ee75f4d3d83ebc33ab8c4b854293a080487281bec847128e099d21ab11ba33f6`
and `c8b64a3a96699c182907700f342910205bc802b505b11dfcff11503f8e52a954`.
The coordinator recorded zero `oom_kill` and `pswpout` deltas, PSI full-total
increased by 29,532 microseconds, both final PSI average endpoints were zero,
and available memory remained 14,497,058,816 bytes.

Static comparison confirms the fixture's `127.0.0.1:5678/healthz/readiness`
probe matches the production Compose endpoint and port. One remaining concrete
fixture divergence set `N8N_CUSTOM_EXTENSIONS` to the nonexistent read-only
HOME path even though the production contract requires that variable absent
and the immutable bridge installs the package below `N8N_USER_FOLDER`. A
focused guard first failed on that divergence; the source-only correction
removes the variable without changing the endpoint, timeout or resource caps.
The readiness cause remains unknown.

For a future independently approved failure only, the fixture now retains the
first bounded Docker log result as exclusive 0600 stdout and stderr files,
each capped at 256 KiB and retaining equal head and terminal-tail portions when
the source is larger. A protected finite manifest binds the exact identities
and hashes of every existing fixture secret/dump file, both streams, the owned
0700 attempt directory and its empty Docker client configuration directory;
the private controller receipt separately binds the manifest file's own
identity and hash. Missing, extra, replaced, linked or mutated entries fail
closed. Public output contains no raw text, argv, input or secret.

After independent zero-resource verification, the protected verifier reads
the bound files with nofollow descriptors and requires stable pre/post descriptor
metadata plus the same current nofollow named-path identity. It redacts the
fixture's synthetic secret values and their URL, JSON and Base64 encodings plus
URL credentials and token assignments, and derives only a short private
exception/frame summary. Reconciliation anchors each read and unlink to the
verified parent directory descriptor, repeats the full file identity and hash
check immediately before unlink, and refuses a replaced path without deleting
the replacement. The originals remain held until that diagnosis and a
separately authorized exact unlink. Cleanup reports the distinct
`failure_evidence_retained` category and keeps the host attempt barrier in the
meantime. Cleanup also finalizes its receipt and releases the owned lock before
re-raising an original `KeyboardInterrupt` or `SystemExit`; ordinary cleanup
errors remain fail-closed `RehearsalFailure` results. This evidence contract
does not authorize another run.

The registered native unittest invokes the business scenario inside its own
exactly-once finalization boundary rather than relying on `tearDown`, which
Python can bypass for `KeyboardInterrupt`. `finish()` always attempts fixture
cleanup and emits the one protected receipt from `finally`; inherited teardown
is a no-op. If both the scenario and finalization raise, the original scenario
exception and traceback take precedence while the cleanup failure remains in
the finalized receipt. A finalization-only cancellation still propagates after
the receipt is emitted.

The five PostgreSQL-owned secret/dump inputs use uid70 and the Valkey server
secret uses uid999. Only those six synthetic files use mode 0640 while
preserving the single captured host effective GID; their exact host-owned parent
remains mode 0700. This lets the container owner use the bind and the trusted
host controller hash and redact retained evidence. Every uid1000 secret,
failure stream and manifest remains mode 0600. Creation, post-chown, protected
manifest and reconciliation checks bind the exact uid, gid and mode.

After one ownership-verified `rm -f -v`, cleanup may poll only that exact CID
for at most five seconds within the existing final deadline. It does not retry
removal: only the closed Docker `No such object/container` result releases the
identity. A present or unknown result continues within that same bound and is
recorded only as finite present, exact-absent and unknown counts; an unknown
result is never accepted as absence. Continued presence, persistent unknown or
deadline expiry retains the identity.
The cleanup-level regression requires one removal call and the original role
and CID in the retained receipt when the exact absence poll stays present or
returns an unknown result.
Cancellation propagates through the poll after the normal receipt and host
boundary finalizer. This corrects delayed daemon-side removal observation
without changing Docker call timeouts or the global cleanup reserve.

The independently approved V6 selected gate was the exact
`OpsflowN8nNativeRehearsal.test_actual_queue_runner_capture_unknown_reconcile_and_restore`
selector bound by 21-file closure `79d87951...`, wrapper `a33d5e01...` and
invocation `8991c4f9...`. Attempt
`opsflow-native-c1f01b3306c1837874354e04` ended controller `ERROR` after about
four seconds in `create_secrets -> chown_secret -> remove`, with the protected
traceback reporting only `owned container removal failed`. It did not reach
network creation, PostgreSQL, n8n main, worker, runner, workflow, SMTP or
restore. The first exact-CID poll response shape was not retained and therefore
remains `UNKNOWN`; the later exact read-only inspect and owner sweeps proved the
CID absent. This is a fixture removal-observation blocker owned by TSK-0019/W74,
not an application or workflow result.

Automatic cleanup truthfully remained `FAIL` with `container` and
`host_held_for_owned_resource`, one retained secret-prep CID/pending role and
the host attempt barrier. Protected stdout, stderr and controller receipt were
949, 1,862 and 338 bytes with SHA256 `3bb12b95...`, `437088f9...` and
`1596fb51...`; neither stream overflowed. Under explicit reconciliation
authority, current-state manifest `be975e70...` bound the exact 0700 parent,
empty Docker config and sole uid70/gid1000 mode-0640 metadata PostgreSQL secret
before dirfd-anchored revalidation and unlink. Pre/post owner sweeps were empty,
the exact directory became absent and the shared lock was exact and free.
The protected V6 outputs and current-state manifest remain the retained failure
and reconciliation record; this later reconciliation `PASS` does not rewrite
the scenario `ERROR` or automatic cleanup `FAIL`.

The independently approved V8 selected gate used the same exact unittest
selector with 21-file closure `ce774cbd...`, wrapper `1374718a...` and
invocation `488578de...`. Its packet corrected the controller's removal-fact
contract to the nine roles actually created by the scenario, including the
bounded `capture-probe`. Attempt
`opsflow-native-3c3c406319dcbd90d4fa4f71` ended controller `ERROR` during the
first secret-prep removal, before network creation, PostgreSQL, n8n main,
worker, runner, workflow, SMTP or restore. Automatic cleanup truthfully
remained `FAIL` with `container` and `host_held_for_owned_resource`, one
retained secret-prep CID/pending role and no removal-fact result. No business
or database behavior was exercised.

The protected, synthetic-secret-redacted traceback proves that the exact-CID
absence poll exhausted its shortened cleanup window while revalidating Docker
context identity: `DockerClientBoundary` raised `subprocess.TimeoutExpired`
from its `docker info` query with about 0.021 seconds remaining, before the
poll could return finite facts. A subsequent read-only calibration of the same
now-absent owned CID returned code 1, one whitespace-only stdout byte and the
exact canonical no-such-object stderr. This identifies a fixture parser and
deadline-handling defect, not an n8n or workflow result: the validator required
raw-empty stdout, classified Docker 29's newline as unknown, then attempted
another context validation at the exhausted deadline.

Under explicit current-state reconciliation authority, protected manifest
`b8161bc0...` bound the exact 0700 parent, empty Docker config and sole
uid70/gid1000 mode-0640 metadata PostgreSQL secret before stable descriptor,
nofollow named-path and dirfd-relative unlink checks. Protected reconciliation
receipt `c1f37dda...` records `PASS`; the attempt directory is absent, both
owner-resource sweeps and attempt globs are empty, and the shared lock is free.
This current-state cleanup does not rewrite the V8 scenario `ERROR` or automatic
cleanup `FAIL`.

The focused RED reproduced both observed failure shapes: canonical absence with
whitespace-only stdout was rejected, and a boundary `TimeoutExpired` escaped
without facts. The minimal GREEN accepts only ASCII-whitespace-empty stdout
alongside the unchanged exact CID-specific canonical stderr, so arbitrary
stdout and foreign-CID errors remain unknown. A boundary timeout now records
one terminal unknown observation and returns failure without extending the
deadline or issuing another Docker call; `KeyboardInterrupt` and `SystemExit`
still propagate and the original deadline is restored. This source-only fix
does not authorize another run.

The independently approved V9 selected gate used 21-file closure `704e7068...`,
wrapper `b8e71b8b...` and invocation `dff3d261...`. Attempt
`opsflow-native-27b88b6963181a1efe2ec41a` passed the corrected secret-prep
absence path and provisioned the isolated metadata and DEV PostgreSQL clusters,
Valkey and Mailpit. n8n main stayed running with exit-zero metadata and completed
the observed migrations, but the bounded readiness wait expired before worker,
external runner, workflow import or any business execution. The receipt records
native `ERROR`; queue/runner/SMTP/reconciliation/restore remain `NOT_RUN`.

Every created container was exactly absent after one removal request: the
finite facts cover secret-prep, metadata and DEV PostgreSQL, Valkey, Mailpit,
main and the not-started worker. Automatic cleanup intentionally recorded
`FAIL` only as `failure_evidence_retained`; all Docker retained IDs, pending
roles and swept-ID lists were empty. Protected stdout, stderr and controller
receipt were 7,826, 2,551 and 379 bytes with SHA256
`0f8b4e3e94187780c2330c0032b3409f334180b4b31dec789265758b291622f1`,
`c9e337855d9ec8b46c7f0c5bf3569bb5354eedf5b65ae94f6dc154db76953273`
and `1de63ff46e983627676cf443f7b791a63cc1e4a72525f9b94c1ae06f2888968d`;
neither stream overflowed.

The protected verifier bound all 17 retained fixture/evidence files plus the
metadata manifest and found no synthetic-secret variant in the sanitized
diagnosis. Main was running, exit-zero and not OOM-killed; migration start and
finish were observed, while database initialization, authentication,
encryption and permission classifiers were false. Stderr was empty. The
redacted log tail ended after the final migration, deprecation notices and a
license renewal skip; it contained no exception. This evidence does not
distinguish an HTTP non-ready status from a refused/timed-out fetch or Docker
exec failure, so the readiness cause remains `UNKNOWN` and the 90-second bound
is unchanged.

After independent Docker-zero and exact custody review, protected input
`d4c19915...` and diagnosis `93a520fd...` authorized exact evidence
reconciliation. Receipt
`aeb77db4a3fa2f5c4b674a9de09877b2694dd86f3283272c49238f0a359bdff3`
records all 18 files revalidated and the attempt directory absent. Independent
post-reconciliation owner sweeps and both attempt globs were empty and the
shared lock was free. This reconciliation `PASS` does not rewrite the V9
runtime `ERROR` or intentional automatic cleanup `FAIL`.

Read-only review of the exact upstream `n8n@2.43.6` tag shows that the existing
`n8n ready on` classifier is a pre-migration HTTP-init log and can be evicted
from the final 200-line tail; it is not proof of final readiness. Final HTTP
readiness requires connected, migrated and fully-ready state after the complete
server start chain. The worker, interactive owner setup and external runner are
not prerequisites for that transition. Post-license community-package,
authorization-role and Redis-backed role-cache initialization remain possible
unobserved waits, but no configuration defect is proven.

The next source-only diagnostic sets fixture-local debug logging and replaces
the one-bit fetch with bounded, no-body liveness and readiness probes. Its
closed receipt separately records Docker-exec success/timeout, validated HTTP
status, and a finite fetch-error class. Malformed, duplicate, extra, body-like
or unknown output fails closed and never reaches the public controller; raw
debug logs continue through the reviewed private evidence custody path. The
probe keeps the existing 90-second readiness, container caps and global
deadlines and does not authorize another run.

The independently approved V10 selected gate used the registered
`leaf.compose-baseline-regressions` route and the exact public unittest selector
`tests.validation.test_opsflow_native_rehearsal.OpsflowN8nNativeRehearsal.test_actual_queue_runner_capture_unknown_reconcile_and_restore`
under profile `ISOLATED_NATIVE`; no private credential argument entered the
registered module argv. Its input Git HEAD was
`6da5723b2490b20497ee0ac5d666da27c4526a31`, based on
`5a88c7937bf427021f2fd0441e04b1011ecd28a9`. The 22-file WIP source closure was
`b96671175fd66e110b8bd5071467611119c42287ec457aaad9f49d51763ae249`,
with wrapper `9bd106a2...`, guard `a2f21f12...` and invocation `9836b862...`.
Attempt `opsflow-native-13cd6f25afb881fd7b361fe1` ran from
2026-10-16 06:49:06+09:00 through 06:52:04+09:00 and ended controller `ERROR`
with child exit 1. It is not a native pass.

The observed runtime config identities were n8n
`sha256:1fda18a541144ae5519ac97bcaffa4e24fad0e71d424606d230464bec8fce153`,
PostgreSQL `sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873`,
Valkey `sha256:a0dbf4c1d5708782907c10e2c72deff317518518b5288a58416981d9db95d30b`
and Mailpit
`sha256:94f6b70c1436defae6799d9ac7ff0eeff9540465b842026d5cdb018f1c0234ea`.
The runner image remained selected by immutable index
`sha256:3168a82b29b3a8ec9acbe876d9e654b3333dfd630b257f6cc2bc81fc5f93b2bf`
with reviewed runtime config `sha256:28c5a510d7624e5ce079d2204e4d8421bc96ced83ebc2e1717d6ee33a0ccc1bb`,
but runner was not started. The closed health probe itself exited zero without
timeout and produced valid bounded output, while both liveness and readiness
had null status and the finite `other` error class. Main readiness therefore
expired before worker, external runner, workflow import, SMTP or restoration.
The actual failure remains unknown: the V10 result does not prove that n8n
returned a non-ready HTTP status or that startup was merely slow.

Automatic cleanup remained `FAIL` with `network` and
`host_held_for_owned_resource`, while its swept container and network ID lists
were empty. Independent owner-resource sweeps were empty and the shared lock
was free. The protected stdout, stderr and controller receipt were 8,115,
2,217 and 413 bytes with SHA256 `8bba4b9f...`, `c8e7cf12...` and `62aafab9...`;
neither stream overflowed. Creation-identity verification covered all 17
retained files plus the metadata manifest. Protected diagnosis `07853acb...`
contained only closed health facts and a redacted debug line, with no exception
or secret. Exact reconciliation input `d0b79aae...` was independently checked;
receipt `5b4882fcc6d9c551f33892b83a147f27082a6e07a8183715462d44376427dc5b`
then revalidated all 18 paths and removed the attempt directory. Independent
final owner sweeps and both attempt globs were empty and the mode-0600 lock was
free. This later reconciliation `PASS` preserves the original runtime `ERROR`
and automatic cleanup `FAIL`. These `/tmp` artifacts have local-only,
best-effort retention and are not guaranteed durable; TSK-0019/W74 owns their
disposition.

The next bounded diagnostic is a temporary single-container Node calibration,
not another full native attempt. Docker-free RED first failed because its
source did not yet exist; the initial GREEN passed four closed parser and cancellation
tests. The successor adds fatal-stage classification, exact semantic PASS and
create, CID-file and discovery cancellation propagation; GREEN now passes six
tests. Temporary source `/tmp/hyhome-n8n-node-calibration.py` has SHA256
`544bd5312a4c6f0771079d7802d868424d1773bad3a2deeecd4e9a11a76016de`;
its test has SHA256
`0351104b4952dce7c2dd73a8e6e7d615f5e0be6dd62828d91e0f7a57ca36cd6b`.
Both are uid1000, mode 0600 and single-link. The proposed exact n8n-image
container has no mount, secret, port or Docker network. The fixed `node:http`
client opens a loopback-only server returning status 204, destroys the response
without retaining a body, closes the server, then requires the same ephemeral
port to supply the refusal observation under an absolute two-second deadline.
The receipt contains only booleans and closed error name/code-source/code
enums, never response bodies, messages, stacks or environment. The prior V10
fetch `other` result remains unexplained historical evidence. Runtime remains
`NOT_RUN` pending two source reviews, a coherent packet and a new explicit
serial admission.

The first admitted calibration wrapper invocation exited 125 with the closed
`controller_boundary` category before creating a container. The reviewed
closure still bound `test_opsflow_native_evidence.py` at `4cba1edc...`, while
an independently authorized failure-evidence RED had already changed that
input. All calibration outputs remained absent, owner container and network
sweeps and both attempt globs were empty, and the shared lock was exact and
free. The calibration therefore remains `NOT_RUN`; the stale packet is not
reused and a coherent successor requires both reviews and fresh admission.

The later coherent V3 calibration packet also remained `NOT_RUN`. Its exact
25-file closure `5be181a8...`, wrapper `228e687c...`, guard `1ae794a2...` and
invocation `b76c173b...` passed both independent reviews and fresh admission,
but the child exited 1 at 2026-10-16 07:30:08+09:00 before constructing the
fixture or calling Docker. Protected stdout was empty with SHA256 `e3b0c442...`;
protected stderr was 457 bytes with SHA256 `2e2ccfc...`; and the controller
receipt had SHA256 `0193938d...`. The private traceback identified only a local
temporary-driver `ImportError`: `memory_bytes` was imported from the ownership
module although the reviewed implementation lives in the inputs module.
Independent owner-resource and attempt-directory sweeps were empty and the
shared lock was exact and free. No Node transport observation exists from this
attempt. A Docker-free real-import regression reproduced the error RED, and
the minimal import correction passes seven tests both normally and with
optimized Python; the V3 runtime receipt remains unchanged and is not a pass.

The corrected V4 calibration used source `41e01fed...`, guard `13df29ac...`,
25-file closure `f0d68e41...`, wrapper `7f247521...` and invocation
`3ddc8465...` against immutable n8n image
`sha256:1fda18a541144ae5519ac97bcaffa4e24fad0e71d424606d230464bec8fce153`.
Attempt `opsflow-native-df3b68d32747542c672bcd74` ran from
2026-10-16 07:52:46+09:00 through 07:52:54+09:00 and ended controller, child,
calibration and cleanup `PASS` with one closed receipt and empty retained state.
The fixed `node:http` client observed a loopback 204 response without reading a
body, closed the server and then observed same-port `ECONNREFUSED` through the
direct error-code branch. Protected stdout was 606 bytes with SHA256
`453962ee...`, stderr was empty with SHA256 `e3b0c442...`, and the 671-byte
receipt had SHA256 `d0f6f37b...`; all were uid1000 mode 0600 single-link.
Independent owner-resource and attempt-directory sweeps were empty and the
shared lock was exact and free. The receipt explicitly keeps native execution
`NOT_RUN`: it validates only the candidate status-only transport and neither
explains V10 fetch `other` nor validates API or Mailpit body-fetch consumers.

The next source-only GREEN reuses that exact calibrated client for main,
worker-broker and Mailpit readiness status calls with an absolute two-second
deadline, response-body destruction, strict 2xx acceptance, an internal URL
allowlist and finite direct or nested network-error facts. API and message-body
fetch consumers remain unchanged. The focused RED failed because the shared
status helper did not exist; GREEN passes four focused tests and the complete
38-test Docker-free source selection with one expected native skip. No timeout,
image, capability or product behavior changed, and another full execution
requires a new coherent packet, both reviews and fresh serial admission.
An explicit stdlib trace over the five new Python helper functions covered 45
of 49 statement lines (91.84%); the four uncovered lines are expression
continuations rather than untested result branches.

The V10 API and Mailpit body-fetch failure remained a one-bit exit and therefore
could have made a later full attempt inconclusive even after the calibrated
status-only client change. A focused RED first failed because the shared closed
failure encoder and parser did not exist. The minimal GREEN leaves successful
REST and Mailpit body operations unchanged while classifying only nonzero
failures as HTTP status, unavailable fetch, finite direct or nested transport
code, invalid JSON response or unknown. It accepts only the two reviewed
consumers, nonzero exit, empty stderr and one duplicate-free JSON object of at
most 4 KiB. Cookies, request inputs, response bodies, messages, stacks,
environment values and raw subprocess output never enter the receipt.

Real Node regressions require uncoded `Error` and `TypeError` to become the
canonical unknown fact; only direct or nested reviewed network codes become
transport facts. Invalid-body `SyntaxError`, `TypeError` and `AbortError` keep
closed response-invalid relations, and the Mailpit detail request now rejects
a non-2xx response instead of treating it as a safe unmatched message. Nine
focused tests pass normally and with optimized Python, including malformed,
duplicate, oversized, impossible-relation and cancellation cases. The complete
Docker-free n8n source selection passes 42 tests with one exact
native skip in both modes. Protected scoped coverage receipt
`25c12f4f6238c555c5e958c8bc3d3cecc43d2f379797a8c8aac43fb191dd5540`
records 48 of 57 executable lines (84.21%) in
`body_fetch_failure_facts`. This is source-only evidence: V10's prior fetch
`other` remains unexplained, and no API, SMTP, workflow or restore runtime is
promoted by these tests. Another full run still requires a newly bound packet,
both independent reviews and fresh serial admission.

The first V13 packet announcement bound wrapper `5921c7c1...`, guard
`8b92976e...` and invocation `75e97596...`, but was revoked before any runtime
GO. The wrapper defined the private body-failure validator but its receipt
parser did not call it. Correcting that defect and adding an actual malformed
receipt regression changed the same temporary paths to wrapper `9988cc6d...`
and guard `33d84db8...` while the invocation still bound the prior hashes. The
announced bytes were not retained unchanged at those paths, so V13 has no
accepted packet verdict and remains `NOT_RUN`; no Docker action or native
attempt occurred. Its replacement uses unique V14 paths and is frozen only
after the Task, closure, wrapper, guard and invocation hashes all match.

The failure-evidence RED also proved that bounded raw Docker output could
contain a synthetic secret on disk before later diagnosis redaction. The
minimal GREEN moves the raw, URL, Base64, JSON, URL-credential, Bearer,
credential-field, token and opaque-value redaction into one pure OpsFlow helper
and applies it before bounding or exclusive stream writes. Each family still
owns identity-bound secret collection. The n8n disk-content regression covers
a known secret at the retained head, truncation boundary and tail plus URL,
Bearer and encoded forms. Missing and empty secret registries fail before
either stream file is created. Thirty-six Docker-free source tests pass with
one expected native skip, and the optimized 18-test evidence module passes.

V14 and V15 remained controller packets only and never ran Docker. Automatic
approval review rejected the proposed in-place V14 closure edit because a Task
hash change would leave the reviewed wrapper and invocation binding
inconsistent and violate the no-same-path-edit freeze; the rejected mutation
was not applied. V15 therefore used unique paths and bound unchanged Task
`939da5f1...`, but safety review found that an oversized receipt-prefix line
was discarded without incrementing the prefix count. An oversized first line
followed by one valid receipt could appear to be an exact-one receipt. V15 was
revoked as `NOT_RUN`. A pre-terminal Task edit was separately rejected because
the Task was still a frozen V15 input, so this history was deferred rather than
worked around. V16 counts discarded prefix lines at newline and EOF, including
split prefixes; oversized-plus-valid input now counts two and rejects. Seven
wrapper guards pass normally and optimized.

The independently approved V16 packet bound 23 inputs in closure
`fbc375afc893a2186e8b279e6186693a0c0cea753a76b864bbee427ea7306109`,
wrapper `a54ef2e59b4147c5c25a84130cef7e5fc3721051336026ab4d84d134dda796fa`,
guard `76f080551431dd6f83c0e7b4863b04a03b80a53142f4f548d442512799f1f056`
and invocation `e66745f7788740238ab44c5b8fa14e5e9f1387b3d34fbaee221bdec705483772`.
Its Git input was HEAD `6da5723b2490b20497ee0ac5d666da27c4526a31`
on base `5a88c7937bf427021f2fd0441e04b1011ecd28a9`. The registered route remained
`leaf.compose-baseline-regressions`, profile `ISOLATED_NATIVE`, using the public
module selector already recorded for V10; no credential parameter entered the
registered argv.

Attempt `opsflow-native-2ec503712c8d786a8978e2bd` ran from
2026-10-16 08:39:49+09:00 through 08:43:43+09:00 and ended controller `ERROR`
with child exit 1. Runtime configs were n8n
`sha256:1fda18a541144ae5519ac97bcaffa4e24fad0e71d424606d230464bec8fce153`, PostgreSQL
`sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873`, Valkey
`sha256:a0dbf4c1d5708782907c10e2c72deff317518518b5288a58416981d9db95d30b` and Mailpit
`sha256:94f6b70c1436defae6799d9ac7ff0eeff9540465b842026d5cdb018f1c0234ea`.
The selected runner index/config remained
`sha256:3168a82b29b3a8ec9acbe876d9e654b3333dfd630b257f6cc2bc81fc5f93b2bf` /
`sha256:28c5a510d7624e5ce079d2204e4d8421bc96ced83ebc2e1717d6ee33a0ccc1bb`,
but runner never started. Main stayed running and non-OOM, the closed probe exited
zero with liveness 200 and readiness 503, and migration start and finish were
observed without DB initialization/authentication, encryption or permission
errors. Official 2.43.6 semantics require connected, migrated and fully-ready
predicates for readiness 200. Which predicate or startup wait remained false is
`UNKNOWN`; neither a timeout increase nor a configuration change is justified.

Automatic cleanup remained `FAIL` with `container` and
`host_held_for_owned_resource`. Independent owner container/network sweeps were
empty and the lock was free, while one exact evidence barrier remains. Protected
stdout, stderr and receipt were 8,427, 2,217 and 528 bytes with SHA256
`e8c63016cc5bd99c27e8e45ffc5ff9de3729872cff5c7b67756ed56b26010197`,
`6549ebf584842cf43f8824bc4abeab59346ee04e1985a05742c86c0b2cddddab` and
`12be1432668ffcc40de6cb03c39dab36fe8fdeaa07b97ff8599af12aee438977`;
neither stream overflowed.
Identity/hash custody passed for 18 bound regular files and the empty Docker config directory. Protected diagnosis
`8fbf5871ba76e7358c5f95db8e7198fd012a8fac51e0abde7ce9c08ef1db9972`, controller diagnosis `32351a79b0353cece16813085cab2153f0e9a2975e13848d970672d9e01f7d12` and reconciliation input
`1e5b29b465945521d9796854fa7624ea39bd5aac70bc714ff0cca37dc36c24ae` preserve runtime `ERROR` and automatic cleanup `FAIL`. Manual V1/V2 stayed `NOT_RUN` after self-review found receipt/lock pathname-binding gaps. After direct exact approval, reviewed V3 removed only the retained barrier.
Before receipt `c848413e07050e249272667c980db8b8a115148a939c9651bb07bd1f979f7d17` (5,896 bytes) and post receipt `2aa7d8662f3c9b34351d1f38cba26f3199f4e6aaa8a4bbe56eaa0d366257e58f` (788 bytes)
bind that manual `PASS`; independent final zero found both attempt globs and owner resources empty and the lock exact/free.
Local `/tmp` receipts have no durability guarantee. This later cleanup does not rewrite the native result; worker, runner, workflow import, SMTP and restore remain `NOT_RUN`.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0019 | draft | ready | #inputs-and-authorization |
| SPEC-0204-TSK-0019 | ready | in-progress | #w74-source-and-execution-boundary |
| SPEC-0204-TSK-0019 | in-progress | blocked | #review-and-completion |

### Fixture runner switch removal — 2026-10-20

On the owner's instruction `_n8n_env` in
`tests/validation/_opsflow_native_fixture.py` no longer passes
`N8N_RUNNERS_ENABLED=true`. n8n 2.x reports the variable as no longer needed
and the HOME Compose removed it in the same change (TSK-0017).
`test_opsflow_native_boundaries` now rejects it. No other fixture value
changed, and no Docker resource was created. The fixture file's bytes, and so
any earlier fixture source hash, changed: the frozen-source review and the
fresh host readiness check that gate the next W74 run must cover this revision.
Earlier W74 receipts stay valid for the revision they name.

### V16 readiness predicate review — 2026-10-20

The owner asked for the blocked R15–R17 chain to be reviewed and resolved.
This section supersedes the V16 conclusion above that the false predicate was
`UNKNOWN` and that no timeout change was justified; the V16 record itself is
kept as it was.

Source. The 2.43.6 image (`hy-home/sec01-n8n:2.43.6-opsflow-03892eb1a9a4`,
config `1fda18a5…`, the V16 runtime) answers `/healthz/readiness` with 200 only
when `connected && migrated && fullyReady` (`dist/abstract-server.js`); the
worker's handler adds the Redis client (`dist/scaling/worker-server.js`).
`fullyReady` is set by `markAsReady()` after `super.start()` returns
(`dist/server.js`). That start awaits `configure()`, logs `Version: …` once and
runs the `n8n.ready` hooks; the fixture sets no `EXTERNAL_HOOK_FILES`.

V16 evidence. The retained V16 streams still match their recorded hashes
(`e8c63016…`, `6549ebf5…`). Their `main_readiness_failure` facts came from
`docker logs --tail 200`. In 2.43.6, `n8n ready on ::, port 5678` is written
when the listener starts, before the migration lock, so on a fresh database
the ~300 migration lines push it out of the last 200 lines. `log_ready=False`
therefore does not mean the listener was missing (liveness was 200), and
`log_migration_finished` matches the first finished migration, not the last.

Measurement. `w74ready-deaecfd83f82`, 2026-10-20 17:10–17:16 +09:00, with
the fixture's images (n8n `1fda18a5…`, PostgreSQL `77f58511…`, Valkey
`a0dbf4c1…`), caps (`RESOURCE_CAPS`, `TMPFS`), environment, synthetic
secrets, an internal network and the fixture's `node_status_probe` every
0.25 s. Host load averaged 5.9–8.3. Logs and the receipt are retained in
`/home/hyunyoun/storage/ops-snapshots/w74-readiness-20261020/` (0700) with
`SHA256SUMS` (all four `OK` on re-check); receipt `cf791714…`. 0 containers and 0 networks were left.
The directory is host-local, like the V16 `/tmp` receipts, and has no durability guarantee.

| Phase | First URL 200 | Ready | Log |
| --- | --- | --- | --- |
| Main, fresh database | 36.6 s | 117.9 s | `main-gen1.log` `5a27f9c7…`: 934 lines, 300 finished migrations, listener line 14, `Version:` line 904 |
| Worker broker `:5679/healthz` | 80.0 s | 80.0 s | `worker.log` `5eee3a07…`, 17 lines |
| Main, migrated database | 52.6 s | 80.6 s | `main-gen2.log` `9ac43f3a…`, 313 lines, `Version:` line 283 |

An earlier unretained session sample, with a 2 s `wget` probe and a
concurrent quality run, reached main readiness at 208 s. `Editor is now
accessible` does not appear in the fixture's logs.

Two samples and one log set are consistent with V16's 503 being a main start
still running when the 90 s wait expired. They do not prove that this is what
happened in V16, whose full log was not kept. The worker's 80 s against its
90 s wait leaves no margin.

Cause fix (source): both the main and the worker broker waits become 300 s,
about 1.4 times the slowest observed main start. `main_readiness_failure_facts`
retains its `--tail 200` copy first, in its own `try`, then reads the whole log
for the facts, and adds `log_version`. The facts therefore come from a log that
is not retained; the retained tail cannot reproduce them. The fixture's
13-minute work deadline is unchanged. The scaled worst case for main, worker
and the second main start is about 500 s of waiting, which leaves under
5 minutes for the stages before and after them. Those stages are not measured,
so the deadline is a recorded risk. Docker-free suites
(`test_opsflow_native_boundaries`, `_evidence`, `_health_probe`, `_rehearsal`): OK, 1 skipped.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Default boundary guards | 19 | W74 | Fail-closed target, recovery, cleanup and resource contracts | New focused fixture source | PASS | W74 source and execution boundary | required | - |
| Actual queue/runner/SMTP execution | 19 | W74 | Terminal workflow, external Code node, capture and unknown isolation | Exact reviewed images and independent GO | ERROR | W74 source and execution boundary | required | - |
| Reconciliation and empty restore | 19 | W74 | Quiesced no-send evidence, one resend and separate DB replacement | Synthetic owned state | NOT_RUN | W74 source and execution boundary | required | - |

## Criterion Acceptance

Criterion 19 retains TSK-0013 as its durable acceptance owner. TSK-0016 retains complete
vertical acceptance. W74 adds supporting native evidence only and does not add an acceptance-criteria row.

## Review and Completion

Runtime work is blocked: V16 proved liveness 200 and readiness 503, while the false connected, migrated or fully-ready predicate or exact startup stage remains `UNKNOWN`. This new artifact must retain its required initial `draft` frontmatter until that baseline lands; the truthful follow-up chain is `draft → ready → in-progress → blocked`. Owner `@buenhyden` and named n8n implementer `native_workflow_rehearsal` may resume only with exact protected startup-stage/predicate evidence and a source-reviewed cause fix under fresh review and an approved slot; blind rerun and guessed timeout, egress or license changes are prohibited, joint same-data execution remains `NOT_RUN`/`BLOCKED`, and manual cleanup does not complete HOME deployment, recovery, real SMTP or exactly-once delivery.

PR #509 landed the draft baseline, so the stated chain now applies and the current status is `blocked`. The blocker, owner and resume condition are the ones stated above.

2026-10-20 update. A source cause fix exists (above), with retained
reproduction evidence at the fixture caps. That evidence is not V16's own;
whether it meets "exact protected startup-stage/predicate evidence" is the
owner's call, and the owner asked for the blocker to be resolved. An
independent `code-reviewer` first returned REQUEST CHANGES; after the changes,
its re-review at `6e5c76cdc` returned APPROVE WITH NOTES. Still open: the
native rerun in an approved slot. Until it passes, the status stays `blocked`.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [P05 Task](tsk-0013-p05-n8n-outbox-notifier.md)
- [P10 Task](tsk-0016-p10-opsflow-acceptance.md)
