---
title: "OpenBao Maintenance Window Readiness Task"
version: "0.1.32"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-22"
layer: "specs"
artifact_id: "SPEC-0243-TSK-0001"
parent_ids:
- "SPEC-0243-PLAN-0001"
created: "2026-10-14"
---

# OpenBao Maintenance Window Readiness Task

## Overview

### Objective

Make RUN-0085's maintenance window executable, as SPEC-0243 states.

## Inputs and Authorization

- **Request:** on 2026-10-14 the owner asked to review the maintenance window,
  then to review and proceed, and chose "readiness Spec 작성"
  (AskUserQuestion).
- **Baseline:** branch `claude/single-admin-host-custody` (PR #478) on
  `main` `4421d30f1`, because both change RUN-0085.
- **Not done:** no window step, HOME change or secret read. W0's read-only
  commands ran on 2026-10-14 (below).

## Work Log

### v28 local residual work plan — 2026-10-22

- **Input and authority:** user attachment v28 SHA-256
  `b497f05146cbd7002262f819bb5a1d9d620d161f3c2a6b0ac4d9827c920c1a89`,
  baseline `73433adc`, local branch `codex/v28-local-residuals`. The user chose
  to keep the existing deadline and prepare improvements. This retains D1's
  2026-11-15 expiry without new acceptance or policy change. Referenced
  dependencies were not supplied with the attachment.
- **Ownership and order:** doc-writer owns RUN-0085 and this Spec/Plan/Task,
  first aligning A1/A2 context, stop/recovery/Finish gates and C2 current state.
  The code worker owns strict snapshot `entity_id == ""` (B1), TLS native probe
  timeout 60 seconds (B3) and its existing callers. QA owns the existing opt-in
  semantic restore harness (B2) and actual runbook-function regression. C1 QA
  owns SEC01 `update-ledger.json`, `verification.json`, README and
  `test_update_gates.py`: preserve historical aggregates and distinguish the
  reported 12+2 cases / 508.185+276.412 seconds by module and aggregation.
  Unavailable raw argv/exit/start/end/logs stay NOT_VERIFIED. Refresh source
  census drift through the registered generator only; no native claim transfers
  to a changed hash. Workers preserve one another's changes.
- **Execution boundary:** documentation, source, synthetic tests and local
  review only. Actual scale/force-sync, HOME/native Docker, credentials, root,
  locks, sudo cleanup and remote writes are NOT_RUN without separate authority.
  A3/B4/D1 receive concrete handoffs with required inputs and recovery bounds.
  Preserve POL-0085, previous receipts and historical unreviewed-step records.
- **Budget:** the user's numeric budget is UNKNOWN. One active command per
  writer, at most seven workers overall; one minimal syntax/metadata/link and
  changed-surface regression pass, with one narrower diagnosis/retry on failure.
  Validate native harness changes with opt-in disabled; do not claim native
  success or approve installation pins from those checks.
- **Recovery and completion:** retain original source and operational assets.
  A reviewed revert of this logical diff is source recovery, not runtime rollback
  or Raft downgrade. New pinned files require a new approved commit/manifest,
  installation match and independent review for the next window. Record document
  checks, code regression, independent review and missing evidence separately;
  do not aggregate them into full v28 or operational acceptance.

### W0 Read-only Observation

On 2026-10-14 the security Compose validation passed (2 services);
`bao status` showed initialized, unsealed, active, Raft, version 2.6.2; the
pinned owned image is present locally with digest `46bf9b5c3ae3`; the system
disk is 88% used with 29 GB free; the last backup run (03:43 KST) failed only
on the known missing snapshot token; the audit and data directories match
their recorded device and inode; `/etc/logrotate.d/openbao` is absent. W0's
own image check matched nothing, because it searched `^openbao/openbao`
while the pin is `hy-home/openbao`; SPEC-0242 fixed it.

### W1 Window Text

From the `iac-reviewer` review, RUN-0085 (0.12.0) now states:

- SEC01's actual status for the owned image: admitted only for the next
  bounded native validation, HOME acceptance (criterion 15) pending.
- W0 prerequisites: pause or avoid the daily backup timer; deploy the Traefik
  CA mount before W4 (D1); compare running and declared Prometheus, Gatus and
  Traefik; decide on OpenBao-down alerts during W4.
- A new W1c that applies the renderer policies and token roles with root
  before W3 (D2), BLOCKED until a reviewed command exists.
- W4: stop if either the W3b receipt or the W3a restore is missing, record
  the Raft mount identity before and after, never confirm Compose's volume
  recreate prompt, and do not open W4 until a cut-over procedure or a
  fix-forward decision is recorded.
- W5: create the Agent with `up --no-start` so the helper finds it stopped,
  and recreate Prometheus with `up -d --force-recreate` only when its running
  image matches the pin, instead of `restart`, which cannot apply the CA mount (D4).
- Step 6 names the tracked restore tool and its likely image failure (D3).

The OpenBao README now lists `obs_net` for the Agent.

An independent `iac-reviewer` re-review of `8e28414f5` returned FAIL on two
gaps: W3a was not marked BLOCKED despite D3, and no step recreated Gatus,
which keeps alerting after W4 without the CA mount. W3a now says BLOCKED with
D3 and the missing W4 producers, and W5 recreates Gatus under the same
conditions as Prometheus, BLOCKED until the W6 override exists. Notes
applied: the Raft identity comes from `docker inspect` of the mount rather
than the host path; Prometheus and Gatus use `--force-recreate`; the timer
window includes its random delay; the rollback pointer points down.

The re-review of `0a3930f8a` passed with notes. Applied: Gatus is checked by
its local image ID rather than a digest pin, and, since Compose already
declares its CA mount, it follows the same condition as Prometheus.

### W2 Restore Server Start

Neither the pinned owned image (`46bf9b5c`) nor the old image (`11fd73a2`)
has `/bin/bao`; both install `/usr/bin/bao`, and both images' entrypoint
writes `BAO_LOCAL_CONFIG` to `/openbao/config/local.json` and adds `-config`.
So `--entrypoint /bin/bao ... server` failed on both, not only the candidate.
`protected-semantic-restore.py` now starts each server through the image's
own entrypoint with `server`, and adds a private 1 MiB `/openbao/config`
tmpfs owned by 100:1000 because the root filesystem is read-only. A unit
assertion pins that: no `--entrypoint`, the image and `server` last, and the
tmpfs present; it failed on the old code and passes now. The suite ran 26
tests OK in a clone checked out under umask 022; under this session's umask
002 one loader test fails because it rejects group-writable files, an
artifact of the checkout, not of the code.

A native probe built the tool's exact create arguments, pointed them at a
synthetic empty target with throwaway TLS and no network, and ran both
images: each server came up uninitialized and sealed on Raft (2.7.1 owned,
2.6.2 old). With the pre-fix arguments `docker start` failed. No probe
container was left. RUN-0085's W1 manifest now pins the new module SHA256
`44f3d475bef1b8fdf8ca679cb7a5fe97eab4aeace5d279d8f0a59b4fcdaf4984`. An actual
restore and canary read still need the W4 inputs.

An independent `security-auditor` review of that fix passed with notes and
warned that later steps in the same flow were unproven. A native synthetic
probe then ran init, unseal, login, snapshot save and restore with the tool's
server arguments and found four more defects: `bao operator unseal` and
`bao login` without an argument refuse non-terminal stdin (`docker exec -i`
has no TTY), so the post-restore foreign-share denial check passed for the
wrong reason; neither image has `/usr/bin/stat`; and root with every
capability dropped cannot read the 0400 snapshot owned by the host user, nor
the token, while the CLI also needs a writable `/tmp`. The fix uses
`write sys/unseal key=-` and `login -no-print -`, busybox `/bin/stat`,
restores as the server user with a 0440 snapshot (group 1000) and adds a
16 MiB `/tmp` tmpfs. New assertions failed on the earlier code (3 failures)
and pass now; both suites ran OK under umask 022. Natively, on both images,
restore as the server user with the 0440 snapshot returned 0, and the old
forms failed with permission denied. RUN-0085 pins the new SHA256 of both
modules.

The `security-auditor` re-review of that fix failed one item: the
foreign-share denial check sent a single throwaway share, but Shamir unseal
cannot reject a share below the threshold, so with the working stdin form it
would return 0 and stop every restore as indeterminate. A native run on both
images confirmed it: after restoring a 2-of-3 snapshot, the first foreign
share returned 0 with the server sealed and progress 1, the second returned
"invalid key", and after `-reset` two original shares unsealed it. The check
now requires the first share to leave the server sealed at progress 1 and the
second to fail. New assertions failed on the earlier code (1 failure, 1
error) and pass now. `/tmp` grew to 40 MiB to cover the 32 MiB snapshot
admission limit. Module SHA256s now pinned in RUN-0085:
`protected-semantic-restore.py`
`67f47ef51dea688de6a0f7d8300311ba53dda0fa11070055bd9ec2cb3b14181c`,
`protected-semantic-execution.py`
`137a8509f7e5180afad16008ca4c4903cc1386cdc3635e94d620d782dfd1d39b`.

The third re-review passed with notes: the second share must now fail with
"invalid key" specifically, so an unrelated failure cannot pass the check, and
the wording notes are applied.

### W3 Renderer Role Apply

Nothing applied the renderer policies, token roles or AppRole that W3a and
W5 assume, and `operator.hcl` cannot write `sys/policies/acl`, so W1c needs
root. The new `protected-renderer-roles.py` loads the token helper by its
pinned hash and reuses its root input, custody, pinned TLS and response
checks. It writes four policies (`renderer`, `renderer-issuer`,
`renderer-cleanup`, `hy-home-operator`), two token roles and the
`hy-home-renderer` AppRole from hash-pinned tracked files, in that order and
once each. Before any write it reads every target and stores the result in
custody `prior-state.json` for rollback; after each write it reads the target
back and stops as INDETERMINATE on any difference. A missing AppRole blocks
before any write, because the deployed Agent holds its RoleID. The receipt
`state.json` holds only paths, SHA-256 of prior and applied values, and a
changed flag. It creates no credential.

Eleven unit tests cover the target set and hashes, duration readback, source
tampering, the binding pin, root and cluster checks, the missing AppRole,
readback difference, write failure and the request allowlist. Removing the
AppRole check and the readback comparison makes two of them fail; restored,
all pass under umask 022. Two opt-in native tests ran the real tool against
an owned synthetic server on both the owned image and the running HOME image:
a stale `renderer` policy and a differently configured AppRole were replaced,
the RoleID stayed the same, a root-issued request through each token role
returned the reviewed five-minute non-renewable identity, the issuer token
could create a wrapped SecretID but not an unwrapped one, and a second run
reported no change. The rehearsal's server, CA, address, cluster and AppRole
mount are synthetic, the tool sees the fixture's host name and port in place
of HOME's, and the 2.6.2 run bypasses the fixture's helper-tag probe. RUN-0085 pins the new helper and the seven config files in
the W1 manifest and replaces the BLOCKED W1c text with the command.

Independent reviews of `5c2dd4601` both passed with notes (`security-auditor`
four Low; `iac-reviewer` three Medium, two Low). Applied:

- A read-only `plan` operation records the same receipt without writing; the
  runbook runs it first and applies only after the owner accepts any change to
  `hy-home-operator`, `renderer` or the AppRole, then checks Agent health.
- Role fields the reviewed files omit (period, CIDRs, use count, globs, token
  type) are written at their defaults. Token role reads omit
  `token_bound_cidrs` and `token_num_uses` when empty on both images, so the
  readback expects them absent.
- `BindingBlocked` from a changed config prints BLOCKED instead of a
  traceback; the token module is loaded with no-follow, regular, single-link
  and size checks; POST sends the held reviewed body.
- The runbook captures each exit status, keeps W2 and W3 closed unless the
  receipt says `RENDERER_ROLES_APPLIED`, decides rollback before root is
  revoked (rollback BLOCKED without a reviewed command), copies
  `prior-state.json` to durable owner storage, and names W1c wherever root
  use is listed.
- The native test now runs `plan` first and confirms nothing changed, then
  has an operator-policy token, not root, create both role tokens with
  `policies` as a string, as W5 sends it, and be refused a one-hour TTL. A
  probe showed the operator policy's `policies = ["renderer-issuer"]` limit
  admits the string form and refuses a JSON list, which matches W5's text.

The `iac-reviewer` re-review of `3e080d999` passed with notes (three Low, two
Nits). Applied: a native probe on both images showed `allowed_entity_aliases`
and `token_no_default_policy` read back as written, so every field a role
read returns is now written at its default except the AppRole's
`local_secret_ids`, fixed at creation; the runbook has a literal `apply`
block with its exit check, says a `plan` exit 2 wrote nothing, compares the
plan and apply `prior_sha256` values, stops at W1c if the Agent is unhealthy,
and W7 keeps root while a W1c rollback decision is open. The test is now in
`.github/workflow-contract.yml`, so CI runs it.

### W4 W3a Input Producers

`protected-restore-inputs.py` produces the four inputs the restore client
consumes, each as a new owner-private file that is never overwritten:

- `lease-start` records the writer-stop time before W3; `lease-bind` then
  writes the quiescence lease bound to the W3 receipt's SHA-256 and refuses a
  snapshot saved before writers stopped or a lease longer than 90 minutes.
- `bundle` extracts the seven Agent files from one reviewed commit through
  `git show` with a clean environment, mode 0400, plus the
  `{source_revision, sha256}` receipt the restore client checks. The renderer
  helper keeps its existing installer.
- `security-receipt` freezes the two OpenBao ledger rows with the ledger's
  SHA-256.
- `contract` validates the snapshot archive, matches it to the W3 receipt
  and the lease, resolves the candidate image ID, and writes the contract only
  through the restore client's own `_contract` schema check.

Ten unit tests feed each output to the restore client's validators: the
bound lease passes `QuiescenceLease.recheck` and fails after expiry, the
bundle matches its revision, and the contract passes `_contract` while a
mismatched snapshot or a wrong candidate writes nothing. With the loader's
mode checks they ran in a umask 022 clone (36 OK with the restore suite).
Removing the lease's start-before-save check fails one test; removing the
contract's snapshot hash check is still caught by the lease hash check.
RUN-0085 adds `lease-start` before the W3 save, `lease-bind` after it, the
input commands before W3a, and pins the producer in the W1 manifest.

Independent reviews of `0294deaf8`: `security-auditor` APPROVE with notes
(one Medium); `iac-reviewer` REJECT, because criterion 4 had no native
rehearsal and the candidate was not bound to the approved commit. Applied:

- The producer reads Git through held descriptors, verifies `^{commit}` and
  rechecks the checkout identity, as `install-renderer-issuer.sh` does; the
  candidate is the one owned image the Compose file pins at that commit.
- `contract` checks that both receipts name the revision, deletes a contract
  that fails the restore's schema check, and the lease refuses a save more
  than 30 minutes after writers stopped. Every failure prints BLOCKED.
- RUN-0085: one commit for helper, bundle, receipt and candidate; a shell
  function instead of a word-split string; exit checks; the contract digest
  captured into the variables the restore reads; FD 4 opened and closed
  around the restore; a BLOCKED rerun keeps the lease; the restore starts at
  least 17 minutes before expiry; the inputs are copied to durable owner
  storage; the lease records the operator's claim rather than proving it.
- A native rehearsal now runs the whole chain on a real 2.6.2 synthetic
  server: a real Raft snapshot, `lease-start`/`lease-bind`, the real helper
  installer, `bundle`, `security-receipt` and `contract` through the CLI,
  then the restore client's own `_contract`, `QuiescenceLease`, `Admission`
  with `pre_read`, and `preflight`, stopping before any effect.

The rehearsal found two defects. The restore preflight compared
`docker image inspect --platform=linux/amd64` against the old image ID, but
under the containerd store that returns the multi-arch tag's platform
manifest (`e29524…`), so W3a would always stop on HOME; it now compares the
local image ID with `linux/amd64` (unit test RED on the old code, GREEN
after). And `lease-bind` truncated its clock to seconds, so a bind in the
same second as the save was refused; it no longer truncates. 15 producer
tests (including the native one) and the restore suite pass in a umask 022
clone. RUN-0085 repins `protected-semantic-restore.py` (`0cb31922…`) and the
producer (`0bfc1bac…`).

The `iac-reviewer` re-review of `f00837af5` passed with notes (all Low).
Applied: the native class sits above the `__main__` guard; any self-check
failure deletes the contract; each receipt is checked and hashed from one
read; `security-receipt` reads the ledger at the approved revision through
the held repository and records that revision; `image_id` runs Docker with
the restore's fixed `PATH`; the fixture's tag probe uses the local image ID,
so both native tests drop their copied workaround; new tests cover a wrong
platform and a failed `docker` in the producer and the restore preflight;
the runbook's rerun text names which paths change; and a new test checks
every W1 manifest pin against its file. A GitGuardian finding on PR #485 was
a synthetic secret-file path in a test, not a secret, but the scan covers
history and the branch cannot be rewritten, so W5/W6 moved to
`claude/window-w5-w6` (#486) as one commit and W4 was rebuilt on it. In a
umask 022 clone, 66 tests passed with every native rehearsal (W3 on both
images, W4 end to end, W5 restic). RUN-0085 repins the producer
(`f0807d5e…`).

### W5 R2 Artifact Transfer

`offsite.sh` gains an `artifact` action for the existing `restic-offsite`
job, with the same image, secrets and egress-only network. It refuses a
missing or symlinked input. It backs up only `raft-pre-upgrade.snap` and its
receipt from a read-only `/artifact` mount under a fixed tag and host, takes
the snapshot ID from restic's JSON summary, then reads each file back with
`restic dump` and compares SHA-256 with the local bytes. It prints one
value-free JSON receipt (names, sizes, SHA-256, snapshot ID). It never
deletes or retries. RUN-0085 replaces the BLOCKED W3b text with a read-only
`snapshots` reachability check followed by the action.

A contract test pins that the branch adds and reads back but never forgets,
prunes, unlocks or removes; dropping the read-back makes it fail. An opt-in
native rehearsal ran the real script in `restic/restic:0.19.1` with no
network against a local repository (a mounted wrapper sets
`RESTIC_REPOSITORY`, which the script otherwise points at R2) and synthetic
secrets: a 300 kB random snapshot and its receipt were stored and proved, and
a symlinked receipt stopped with exit 64 before any snapshot. The existing
Compose baseline gates still pass. On 2026-10-14 the owner approved (AskUserQuestion) the read-only R2
rehearsal in criterion 5. It ran `snapshots --no-lock`, which writes not
even a lock file: the repository was reachable and decrypted with 45
snapshots and none under the W3 tag. RUN-0085's reachability check now uses
the same lock-free form.

An independent `security-auditor` review of `bab3124fc` passed with notes
(two Low). Applied: the branch sets `pipefail`, so a failed restic is not
hidden behind `sed` or `sha256sum`, and a failed read-back says so; empty
inputs are refused; and the snapshot's SHA-256 must appear in its W3 receipt
before anything is sent. The runbook notes that a lone W3 snapshot survives
the monthly prune, so its removal is a separate owner decision. The native
rehearsal now also stops a snapshot its receipt does not name and an empty
receipt with exit 64, before any backup (5 tests OK).

### W6 CA Mounts, Logrotate and W4 Rollback

A read-only comparison on 2026-10-14 found that Compose already declares the
OpenBao CA mount for Traefik, Prometheus and Gatus, but none of the running
containers has it. Gatus runs the current `hy/gatus:local` image ID, so the
plain recreate in RUN-0085 applies. Traefik runs v3.7.13 and Prometheus
v3.14.0, while Compose pins v3.7.14 and v3.15.0, so a plain recreate would
also upgrade them. Two `x-hyhome-overlay` files, `compose.window-ca.override.yml`
beside each service's Compose file, pin each to the
running image by digest and changes nothing else: `docker compose config`
with and without it differs only in those two `image` values, and the merged
model keeps the CA mount targets. A contract test pins that shape.

PR #486's operations-catalog gate rejected a single override with `services`
under `infra/` as an unincluded Compose file, so it became two
`x-hyhome-overlay` files, each based on its service's Compose file; the gate
then passes.

The hourly logrotate call is a drop-in for the host's existing
`logrotate.timer` that resets `OnCalendar` to hourly and sets
`AccuracySec=5m`, so the one
`logrotate.service` keeps the shared config, state and lock. A copy of the
host's timer and service with the drop-in passed `systemd-analyze verify`.
Installing it is the owner's sudo step.

For W4's way back, the owner chose fix-forward on 2026-10-14
(AskUserQuestion, "Fix-forward (Recommended)"): no rollback to the old
image; only unfixable Raft damage holds HOME and opens the W3 snapshot
restore under separate approval. RUN-0085 records the decision and the two
override commands.

An independent `iac-reviewer` review of `ccfa88e05` passed with notes (four
Medium, five Low). Applied: the W4 paragraph now states fix-forward as the
one rule, what HOME looks like if it does not finish in the window, and the
Raft-damage exception, and Rollback or Recovery points to it; the logrotate
text lists the size, hourly and `dateext` effects, an inventory command, the
undo and a unit-level check; W0 names the drift-check method (main checkout,
`docker inspect` mounts, networks and resources against `compose config`,
image by ID) and a check that each pinned override reference resolves; a
different Gatus image is BLOCKED because W6 has no Gatus override; W0's
approval is the owner's; the drop-in moved to `config/systemd/` so it is
never read as a logrotate rule; the override says when to retire it; the
OpenBao README lists the new files; and `.github/workflow-contract.yml` now
runs the W5 and W6 tests in CI.

### Second Readiness Review and Window Text

An independent `iac-reviewer` readiness review of the whole window on the
W4 branch, with every unit in place, returned NOT READY on 2026-10-14: D1-D4
are fixed in source, but the text still stopped W4/W5 on SEC01 criterion 15,
the targets could not fit 60 minutes, W6 rotation could not be seen in the
window, W3a's status contradicted itself, an un-revoked root could be lost
on tmpfs, and the W5 token step put credentials through the terminal.

The owner decided (AskUserQuestion, 2026-10-14): a 120-minute window with
W6 rotation and W7's next backup moved to post-window observation; the
W4/W5 SEC01 gate is the window-only image acceptance plus a stable lookup
within 7 days, not criterion 15; an Alertmanager silence over the window;
and the old `p01-operator.token` is revoked and deleted.

RUN-0085 now has a timing table with W1c, W3a and W3b rows, a 110-minute
target in a 120-minute window and clock stop points (T+15, T+60, T+85); the
SEC01 gate as decided; W0 checks for a running backup, `Persistent=true`,
the clean approved checkout, the operator inputs, the image, Agent, `/dev/shm`
and target baselines, and the old token; the silence from W3 to W7; the W3
writer list; a consistent W3a status; W6 and W7 checks split into window and
post-window parts; a custody path for a root left un-revoked; and a W5 step
in which only the operator credential is typed and the two short tokens go
from the server's CLI into variables. A full native `perform()` rehearsal of
the restore remains open.

An independent `security-auditor` review of the W1 text, the W6 overlays and
logrotate files, and this text returned REJECT on 2026-10-15 with no
Critical finding and three blocking ones: the un-revoked root path kept a
non-expiring root on persistent disk, the old-token step put the value in
argv and deleted the file whether or not the revoke worked, and the hidden
prompt only works in bash while the operator's shell is zsh. RUN-0085 now
keeps only the root accessor and shreds the value, revokes by accessor in
the next window, passes the old token by variable with a policy check and
deletes it only after a confirmed revoke, and runs every block in
`bash --noprofile --norc` without history. It also applies the notes: the
W7 operator file lives on tmpfs and is revoked and removed; the silence
starts at W3, covers only the expected alerts, ends at T+120 and records
what fired; the SEC01 acceptance lasts until criterion 15 or a new image
and a security fix in a newer stable fails the gate; step 3 uses absolute
paths; W0 checks that Docker debug logging is off; and W0 reviews the
release notes the overlays skip. The logrotate `--type container` and
stale-audit alert notes stay open as follow-ups.

An independent `iac-reviewer` review of W2, W5 and this text returned NOT
READY on 2026-10-15. W5 passed with notes. W2 failed: the restore's Agent
step runs `chown -R` as root with only `CHOWN`, and root cannot read the
operator's 0770 and 0700 input directories. A native run with the same
flags on the old image reproduced it (exit 1, "Permission denied"); adding
`DAC_READ_SEARCH` gave exit 0. The fix, its test and a full native
`perform()` rehearsal belong to a separate change, and W3a is BLOCKED until
they pass. The text findings are applied here: the targets add up to 110
minutes, so W3b now runs before W3a and the stops are T+15, T+45 (W3b),
T+55 (W3a) and T+80 (W4); one cleanup applies at any stop; stale signature
and 60-minute text is gone; the no-login rule covers W3 to the end of W3a;
W0 requires bash and Linger or a second session; W3a passes all four
secrets by FD, because the root exists only in custody; and W3b treats any
non-zero exit and a stale R2 lock as stops.

### Restore Agent Fix and Full Rehearsal

The Agent prep now adds `DAC_READ_SEARCH` and the preflight refuses a
`noexec` `/dev/shm` (#492). A full native rehearsal then drove
`orchestrate()` and `perform()` on synthetic resources: a fake HOME on the
old image with KV canaries and renderer roles applied by
`protected-renderer-roles.py apply`, every input from the producers, the old
image restore into a throwaway target, the candidate upgrade on the owned
image, helper issuance, Agent render and comparison, and token revoke. Only
ATTEMPT, LEDGER, TARGET, CLUSTER and PARENT_IDENTITY are patched, in the test
process. It found four more defects, each of which would have ended W3a
INDETERMINATE: login to the still-sealed new server, token creation with an
empty body (explicit max TTL 0, which the helper refuses), a 204 revoke
parsed as JSON, and UID 100 Agent files the operator could not remove, which
also left rendered values in `/dev/shm`. The restore now unseals with the new
server's own shares before login, sends the W5 token body, takes the revoke
exit status as the result, and reclaims the stopped Agent's files. W3a stays
BLOCKED until independent re-reviews pass.

The re-reviews of those fixes split. The `iac-reviewer` returned FAIL on one
blocking finding: RUN-0085 sets `umask 077` before the restore, so `tls/`
came out 0700 and the UID 100 server could not read its certificate, which
the umask 022 rehearsal could not show. It also found that cleanup missed the
gap between the prep chown and token creation, and that revoke and reclaim ran
on the shared runner, so a spent deadline or a dead watcher, the likely
failures, would skip them. The `security-auditor` returned APPROVE with notes,
with one Medium finding on the same cleanup paths: rendered values could stay
in `/dev/shm` with no report.

The client now sets `tls/` to 0750 and the Agent input directories to 0755
explicitly, so the prep chown runs as root with `CHOWN` alone, without
`DAC_READ_SEARCH`. Everything after the prep container sits inside a revoke
and reclaim block, which revokes only issued tokens. Revoke and reclaim run on
a fresh runner with no watcher probe. A UID 100 container with no capability
deletes the Agent files where they were written, and `perform` reclaims again
after cleanup. A retained attempt directory prints
`RESIDUE: /dev/shm attempt directory retained`. Each login waits for the
active node (`is_self`). Preflight checks every container and network name
the run creates. The native test runs `orchestrate()` under umask 077 and
asserts that no attempt container, volume, network or `/dev/shm` directory
remains. RUN-0085 pins the module as
`83e587c8f221ede08073bf0636c207fda74f0a0530e874e62458bc635db02b4a`, records
HOME's audit and mount lists in W0, and says how to handle a residue. W3a
stays BLOCKED until independent re-reviews of these fixes pass.

### Owner Host Preparation

On 2026-10-15 the owner reported running the pre-window host steps. A
read-only check from this session confirmed four of them:

- the hourly `logrotate.timer` drop-in is loaded, with its next run within the hour;
- `/etc/logrotate.d/openbao` is root-owned 0644 and byte-identical to the tracked rule;
- Linger is on;
- Docker debug logging is off.

The owner reported that the old `p01-operator.token` lookup was denied, so the
token had already expired, and the file was deleted with `shred -u`. The HOME
TLS preflight was run by the owner; this session did not observe its output.

The owner then recreated Traefik on its SEC01-accepted Compose pin before the
window. A read-only check on 2026-10-15 showed:

- the container runs image `575fa15b`, is healthy and has 0 restarts;
- `/openbao-ca/ca.pem` is present in the container;
- its log has no error since the recreate.

### Final Readiness Review

Independent `iac-reviewer` and `security-auditor` reviews of the whole window
at main `12ab97dab` ran on 2026-10-15.

**Security review: APPROVE with notes.**

- **Closed:** F2, F3 and F5 to F10.
- **Partly closed:** F1 and F4.
- **New findings:** two Medium, about a root left un-revoked:
  - the root can be rebuilt from the OTP and the encoded token that remain in the W1 custody;
  - no tool records the root accessor.

**IaC review: NOT READY.** Its earlier timing, W6, W3a, W5-mint and secret-input findings are closed. New findings:

- **High (the same root problem):** a root left un-revoked can still be rebuilt from the W1 custody.
- **Medium, owner decisions:** the OpenBao acceptance period, and the Agent after an early stop.
- **Medium, text:** hy-home.k8s writers never resumed, shell variables lost on `exit`, stale Traefik text.
- **Low:** several stale or contradictory lines.

The owner decided through the interactive question that:

- the owned OpenBao acceptance lasts until SEC01 criterion 15 or a new image;
- after an early stop the Agent stays stopped until the next window's W5, since its one-time SecretID is spent and consumers keep using the rendered files.

**RUN-0085 changes.** At any stop:

- every file in both custody directories and the W3a secret directory is shredded;
- every OpenBao operator token used in the window is revoked;
- the hy-home.k8s writers are resumed;
- the Agent stays stopped.

A root left un-revoked is found in the next window by listing accessors with a new root, without recording any accessor.

Window logins write to a 0600 tmpfs file instead of the token helper. The window runs in one bash shell in the main checkout, whose non-secret path variables are saved for a reopened shell.

Smaller fixes:

- the stale Traefik, logrotate, W3a and Prometheus text is corrected, and the drift comparison checks Compose pins;
- the W3a HOME read token is taken before W3, and a stop after W2 keeps the installed snapshot token;
- the shared UID 100 is recorded as a residual, and both overlay headers now say rollback only.

**Re-review of these fixes.** The security re-review returned APPROVE with notes. The IaC re-review returned NOT READY on four text gaps:

- the stop cleanup against the INDETERMINATE preserve rules;
- the W0 Agent baseline after an early stop;
- operator tokens that had to be shown to reach W1 and W3a;
- revoking all access without first proving a fresh OIDC login.

It passed the last restore deltas with notes.

RUN-0085 now:

- resolves INDETERMINATE before cleanup;
- keeps an unresolved W2 custody with `P01_KEEP_W2=1`;
- proves a fresh OIDC login before dropping root and the last token;
- copies the credential-free evidence first;
- shreds with fixed globs, rehearsed on fake directories, including dotfiles.

Other changes:

- W1 and W3a take the operator token by FD from a tmpfs file filled at a hidden prompt, because the host has no `bao` CLI.
- The W0 Agent baseline accepts a recorded stop.
- The stranded-root sweep is an exact block after W1 and before W3. It was rehearsed on a throwaway dev server, where it revoked the old root and kept the new one.
- The unencrypted host swap and the full UID 100 asset list are recorded as residuals.

**Rounds 3 to 5.** Each round fixed what the last one found, and each fix was rehearsed. Round 5 closed it:

- **IaC review:** READY with Low notes only, at `0d59ce192`.
- **Security review:** APPROVE with notes.

After round 5 the Low notes were applied:

- a kept root also keeps the path-variable file, needs `unset` before the cleanup is re-run, and needs Linger or a session;
- the sweep reads policies from stdout only, treats either message for a vanished token as gone, prints unexpected errors, and the counts of a re-run are added;
- the restore contract variables are saved;
- the attempt nonce is recorded only as present.

A dev-server rehearsal of the sweep used five parent root tokens with child roots and a stderr warning containing "root" on every call. It gave `revoked=11 remaining=0`, and kept the non-root token and the new root.

**Historical scope mismatch, before r10.** Contract 6 in the Spec still said the overlays kept the running images. #497 changed that by SEC01 acceptance, and this Task originally recorded it without editing the Spec. The r10 source reconciliation below corrects that current contract; this paragraph preserves the earlier mismatch and does not establish approval of the draft Spec.

### Policy and Guide Alignment

On 2026-10-15 the owner asked whether the runbook, policy and guide covered the window. Only RUN-0085 did:

- POL-0085 had none of the window rules or the new exceptions;
- the guide still described a host `bao login` that stores the token through the token helper, but the host has no `bao` CLI.

The owner chose (AskUserQuestion) to update both, and to accept the four window residuals until 2026-11-15:

- the shared UID 100;
- the unencrypted swap;
- the loss of admin access after a sealed-server cleanup;
- a kept W2 custody.

Changes:

- **POL-0085** now has:
  - a "Maintenance window credential handling" rule set;
  - an "SEC01 image acceptances" table that records the owner's existing OpenBao, Traefik and Prometheus decisions with their expiry and closure;
  - a "Maintenance window residuals" table, each row with scope, risk and closure condition;
  - the audit rotation owner, with the missing stalled-rotation alert.
- **The guide** states that the host has no CLI and that window logins avoid the token helper, and adds a short window overview.
- **RUN-0085** points its residual notes to the policy.

An independent `rules-engineer` review returned FAIL on text only. Its findings:

- the token channel rule left out the single-command environment variable that RUN-0085 uses;
- the operator-token and kept-root rules lacked their exceptions and time limit;
- the Traefik and Prometheus acceptance sat outside POL-0085's scope, and was weaker than the owner's record (early revocation, the unauthenticated in-network Prometheus path, the image identities, signatures shown as accepted rather than open);
- several Low wording gaps.

The owner asked for the move into the service policies. Applied:

- POL-0085 states the full token channel, both token exceptions and the kept-root limit, extends the root-use rule to the window root, keeps only the OpenBao acceptance, closes the kept-W2 row on a reviewed recovery only, and gives the stalled-rotation alert gap an owner and closure condition.
- POL-0013 and POL-0045 now each hold their own image acceptance.
- The guide and RUN-0085 use the same channel wording and link to the policy.

The parallel `security-auditor` review was stopped unfinished when the owner asked to wrap up. It must run on the PR before merge.

### Current Status and Handoff

Status on 2026-10-15:

| Area | State |
| --- | --- |
| Criteria 1 to 7 | Accepted |
| Source, tools and window text | Merged up to #501 |
| Traefik | Runs its SEC01-accepted pin |
| Prometheus | Moves to its pin at W5 |
| Host preparation (logrotate rule and drop-in, Linger, Docker debug off, old operator token) | Done |
| Window | Scheduled for 2026-10-22, 14:00 to 16:00 KST |
| Policy and guide alignment | In its own PR, pending a `security-auditor` review |

Remaining, in order:

1. Merge the policy and guide PR after its security review.
2. On 2026-10-21, run a fresh SEC01 stable lookup, then the owner runs `git pull --ff-only` in the main checkout. `P01_APPROVED_COMMIT` is that commit once its CI passes.
3. On 2026-10-22 from 13:30, W0. At 14:00 the owner approves the window separately, then W1 to W7 per RUN-0085.
4. After the window:
   - observe the first audit rotation and the next backup snapshot;
   - cover the Prometheus and Gatus CA mounts (W5);
   - decide on 2026-11-15 on the image acceptances and window residuals.
5. Later, each with separate approval: W8 cold boot, P06 consumer migration, SEC01 criterion 15, and closing the Spec, Plan and Task, which stay `draft` until the window evidence exists.

Known gaps:

- the HOME TLS preflight output was not observed here;
- `5b7b8b32f` was rehearsed but not reviewed;
- the sweep's per-accessor time is unmeasured;
- there is no stalled audit rotation alert.

All session worktrees and merged or superseded `claude/*` branches were removed. Only this PR's branch remains. The owner removes the session scratch under `/tmp/claude-1000/` with sudo (some files are UID 100) and the leftover `/dev/shm/p01-rehearsal-*` directories.

### R10 source and operational handoff reconciliation — 2026-10-15

[SPEC-0212 TSK-0007](../../0212-request-baseline-and-reconciliation/tasks/tsk-0007-r10-reconciliation.md)
owns the current reconciliation request. Contract 6 and Plan W6 now state
the source behavior already recorded above: promotion uses the service's
accepted Compose pin, and the pre-window-image overrides serve rollback only.
The original dated review failures, owner decisions and criterion acceptance
rows remain historical evidence, with no new acceptance inferred here.

The earlier instruction to leave this package draft until the window evidence
exists mixed readiness acceptance with operational execution. Criteria 1 to 7
cover source readiness; the live window is outside this Spec's scope.
Spec and Plan remain draft because the recorded criterion decisions do not
separately approve these amended parent documents. This Task retains its draft
frontmatter under those parents; it does not mean the recorded work or accepted
criteria were unexecuted. Pending source review, including the policy/guide
security review and later source deltas, must have its own actual receipt.
Future package closure must follow the lifecycle contract on that source
evidence rather than wait for an unrelated deployment result.

Window authorization, W0 checks, HOME restore and cold-boot evidence remain
separate under [RUN-0085](../../../05.operations/runbooks/04-security-and-secrets/0085-openbao.md)
and [SPEC-0204 TSK-0006](../../0204-service-integration-security-and-operations/tasks/tsk-0006-openbao-trust-bootstrap-and-recovery.md).
This reconciliation performs none of those operations; their current action
status is `NOT_RUN`. The scheduled window and dated runtime observations above
are retained as recorded, without a new deployment or recovery claim.

[SPEC-0242](../../0242-single-admin-openbao-custody/spec.md) replaced SPEC-0240;
the withdrawn backup-exclusion/rekey proposal is already preserved under
`docs/98.archive/superseded/03.specs/0240-unseal-backup-exclusion/`. Its current
Policy/ADR references explain the supersession; they do not reactivate it.
The protected token, issuer, Raft and restore suites have direct gate consumers
and distinct failure checks, so they remain. Neither a review filename nor
completion of the change establishes that its regressions are disposable.

### Delta review and owner approval — 2026-10-20

The owner asked for the OpenBao work to be reviewed and then approved it
("OpenBao 작업 검토후 승인"). The handoff above requires
`P01_APPROVED_COMMIT` to have no source change since `bf87a9b6a`. That no
longer holds. Main `532ff831e` carries the PR #520 Traefik rate-limit chain,
the PR #526 Restic allowlist change and two OpenBao test edits. Open PR #528
changes `offsite.sh`, which includes the W3b `artifact` action.

Two read-only subagent reviews of that delta were run. They were requested by
this session and are not owner review.

- `iac-reviewer`: NOT READY as of 2026-10-20. The source and window text
  hold. The blocker is runtime: at 13:12–13:14 R2 returned `repository does
  not exist`, so the W3b precheck would fail after W1–W3 had used the root
  ceremony and the Agent's one-time SecretID. The Traefik limit (100/s, burst
  200 per router and peer) carries the OIDC login and the host helpers'
  gateway calls, well under the burst. The Agent, the Prometheus scrape and
  Gatus bypass the gateway. If #528 merges first, W3b exits 66 while R2 is
  above the cap.
- `security-auditor`: APPROVE WITH NOTES, nothing blocking. R2 keys are never
  printed, and the guard fails closed on every traced path. Notes applied in
  #528: the size parser requires a total for every file type; each pending
  size is checked as a number; the size is assigned before it is printed;
  the guard's `stats` uses `--no-lock`; and the `cmd` allowlist is described
  as an accident guard, not a boundary.

Changes made from the reviews (PR #528): RUN-0085 W0 now lists R2 snapshots
and the stored bytes, and does not open the window unless the same
repository answers and the stored bytes plus 1.05 × the W3 snapshot and
receipt fit under the cap. It forbids `init` as a repair. W3b's stop list
adds exit 66.

Status: the approval covers the reviewed delta above, so `P01_APPROVED_COMMIT`
is the main commit at W0 whose window-relevant change since `bf87a9b6a` is
limited to it. The window is still scheduled for 2026-10-22 14:00–16:00 KST,
with the SEC01 lookup on 2026-10-21 and W0 at 13:30. It is BLOCKED until the
W0 R2 gate passes. At 16:13 a read-only bucket listing showed the bucket
empty (no `config`, `keys/`, `snapshots/`, `index/` or `data/` object; SPEC-0204
TSK-0009). The owner deleted it to stay under 10 GB, so W3b has no
repository to store into until a new one is initialized. While R2 holds about 9.35 GB, a working repository would refuse W3b
under the 9 GB cap, so the window also needs either room in R2 or an owner
decision on where W3b stores the artifact. No window step was run.

R2 unblocked — 2026-10-20 20:10: on the owner's "R2 재초기화 진행" the empty
bucket was initialized as repository `f6973d0274`, the first copy exited 0
(36 snapshots, `R2 repository size: 5498639079 bytes`) and `check` found no
errors (SPEC-0204 TSK-0009). The W0 R2 gate now has a repository to read and
about 3.5 GB of room under the 9 GB cap, so the R2 blocker is cleared. It is
re-checked at W0 on 2026-10-22, after two more daily copies. The window still
needs the SEC01 lookup on 2026-10-21 and the remaining W0 checks.

SEC01 lookup — 2026-10-21: the lookup found Go 1.27.3 with a crypto/x509
fix, and the owner approved replacing the image ("이미지 교체 승인"). Branch
`fix/openbao-go1273-r2` rebuilds the owned image (manifest `a58fb110…`),
moves the protected scripts' pinned hashes, RUN-0085's `P01_SOURCE_MANIFEST`
and the update ledger to it, and fixes the rehearsal fixture's bind modes; the
isolated native suite then passed 14 of 14 (SPEC-0204 TSK-0009). That delta is
window-relevant and was not part of the 2026-10-20 approval above, so
`P01_APPROVED_COMMIT` cannot be set until the branch merges and the owner
approves this delta too. W0 also re-checks that the HOME tag for the new
manifest is present. Until both hold the window stays BLOCKED; if they are not
done before W0 at 13:30 on 2026-10-22, the window moves.

Owner approval — 2026-10-21: PR #540 merged as `main`
`31633e6b4359f937669d09d44a7450eb0afe49ec`, and the owner approved this delta
for `P01_APPROVED_COMMIT` before W0 ("W0(10-22 13:30) 전에 이번 변경분을
P01_APPROVED_COMMIT으로 승인"). As with the 2026-10-20 approval,
`P01_APPROVED_COMMIT` is the `main` commit at W0 whose window-relevant change
since `31633e6b4` is none; later documentation-only records (such as this one)
do not change that. The SEC01 gate for the window now rests on this approval
and the 2026-10-21 lookup. W0 still runs its own checks, including the R2 gate
and the HOME tag for manifest `a58fb110`; the window is no longer BLOCKED on the
image.

Backup state seen on 2026-10-21 (journal, read-only): every daily
`hyhome-backup` run since 2026-10-12 exits 1 at the OpenBao step because
`secrets/backup/openbao/snapshot_token.txt` does not exist yet
(`hyhome-backup.sh:184-187`). The rest of each run still completes; on
2026-10-21 pgBackRest, two Restic snapshots, `check` and the R2 copy all ran.
So only the OpenBao Raft snapshot is missing, but the whole-run success time is
not refreshed and the 26-hour freshness alert stays on. W3 creates the snapshot
token; the first daily run after the window must exit 0, and that is a window
acceptance check.

Prometheus step change — 2026-10-21: the 2026-10-20 SEC01 rollout already
recreated Prometheus on the Compose pin with the OpenBao CA mount, so the
window's rollback overlay (`compose.window-ca.override.yml`, the 3.14 image)
would only downgrade TSDB data written by v3.15.0. On the owner's choice ("W0
전에 수정") the overlay is removed, RUN-0085 reduces the Prometheus step to a W0
`docker inspect` check of the image and the mount with no recreation, and
`test_openbao_window_overrides.py` fails if a Prometheus overlay returns. This
is window-relevant. The owner approved it for `P01_APPROVED_COMMIT` on
2026-10-21 ("P01_APPROVED_COMMIT 승인"), so `P01_APPROVED_COMMIT` is the `main`
commit that merges this change, provided no later window-relevant change lands
before W0; W0 records that commit.

### Window attempt moved to 2026-10-21 — closed at W1

The owner moved the window forward ("OpenBao window는 지금 진행한다"; W7 stays
on its plan). W0 ran from 21:07 KST on main
`7ecf84d47c86a8daf2612202defce40a2528e5e8`, whose only change since
`5c77e8681` is the Prometheus restore script, its tests and documents (none
window-relevant). The checks recorded below hold no values.

| W0 check | Result |
| --- | --- |
| Checkout, `COMPOSE_FILE`, override file | Clean, `HEAD` = `origin/main`, none, none |
| Compose validation (security), `bao status` | PASS; Sealed false, 2.6.2, Shamir 2-of-3, raft |
| Pinned image `a58fb110`, running images | Present; OpenBao and Agent `11fd73a2` healthy; Prometheus `efd719c9` and Traefik `575fa15b` on their pins with the CA mounts; Gatus `503e6af2` |
| Running versus declared mounts and networks | Same, apart from Compose secrets |
| TLS preflight | `TLS_MATERIAL PASS` |
| R2 gate | Repository answers (40 snapshots); 5.214 GiB stored, under the 9 GB cap |
| Host | Docker debug false, `jq`, Linger yes, tmpfs without `noexec`, audit and data identities unchanged, logrotate rule hash and hourly drop-in present, restore target absent |
| Backup | Last run 17:30:57 exit 1 at the OpenBao snapshot step only; the owner stopped the timer |
| Renderer helper | Installed for `7ecf84d47` under the owner's tools directory after one retry (a mistyped repository path failed closed); the receipt matched a scratch install |
| Audit, secrets and auth lists | 403 for `hy-home-operator`, which has no `sys/audit`, `sys/mounts` or `sys/auth` read. Owner decision: read them with the W1 root before W1c; RUN-0085 now says so |

W1 BLOCKED twice (from about 21:28), each time before any root attempt: the
custody held only `.lock`, and the server showed no attempt. Cause: OpenBao 2.6.2
and 2.7.1 return the authenticated `sys/generate-root-token/attempt` and
`update` fields under `data`, while `protected-maintenance.py` read them at the
top level, so `started` was never `false` and the client stopped before reading
the shares. Unit tests used the same unwrapped fake, and the native rehearsal
never ran this client. The owner closed the window: both operator tokens were
revoked and removed, the timer was started again (next run 03:30), and no
OpenBao state changed.

The fix reads those responses through `data` and keeps the full raw responses
in custody. Against throwaway 2-of-3 servers on localhost (images `11fd73a2`
2.6.2 and `a58fb110` 2.7.1, in-memory storage, with a stub for the OIDC policy
check), the old client returns BLOCKED with only `.lock`, and the fix returns
DELIVERED with a root that passes `check_root`. A bad first share leaves the
attempt cancelled by the server and reports INDETERMINATE, as designed for a
submitted final share. The fake API now uses the data-wrapped shape, and a new
test refuses an unwrapped status before any POST; the old client fails 7 of
these tests. The hash chain moved through `protected-raft-snapshot.py`,
`protected-semantic-restore.py`, `protected-token-operations.py`,
`protected-renderer-roles.py` and the RUN-0085 source manifest. This is
window-relevant: the window stays BLOCKED until the change merges and the owner
approves it for `P01_APPROVED_COMMIT`. The helper must then be installed again
for the new commit.

PR #546 merged as `ed5739e8de93eb490f74fab75a999754f24abc1d`, the same tree as
the reviewed branch head `75186800a`. A `security-auditor` review (requested by
this session, not owner review) returned APPROVE WITH NOTES; its three notes
were applied before the merge: an unprovable cancel after an attempt starts
exits 2, a test covers malformed responses after the start, and the RUN-0085
root list check runs under `pipefail`. CI passed. The isolated native rehearsal
(`HYHOME_OPENBAO_REHEARSAL=1`) was not green in one run on the branch:

| Run | Result |
| --- | --- |
| Full suite, uncommitted tree | 11 of 12 PASS; `native limited roles/journal/wrapped delivery failed` |
| Single trust test, committed | FAIL at `TLS_MATERIAL FAIL check=native-user-read`, a `timeout 20 docker run`; throwaway container starts then took 12–17 s (load about 11, IO pressure about 30%) |
| Full suite, committed | 11 of 12 PASS; the same delivery step failed |
| Single trust test, branch `75186800a`, 22:22 | PASS in 483.5 s |
| Single trust test, main `7ecf84d47`, 22:30 | PASS in 458.3 s |

The files on the delivery path (`issue-renderer-secret-id.sh`,
`renderer-issuance.py`, `renderer-request.sh`, the installer, OpenBao config
and the rehearsal fixture and clients) are byte-identical between the two
commits, and the delivery step waits up to 180 s for the Agent. The failures
are attributed to host load, not to this change; that is an inference from the
identical inputs and the paired passes. Each of the 12 native tests has passed
on the branch at least once, but no single full run passed. The window remains
BLOCKED until the owner approves `P01_APPROVED_COMMIT` for the merged change.

### Second window attempt 2026-10-21 — stopped before W1c apply

After #547 the owner approved `P01_APPROVED_COMMIT` =
`a633d878227093e875e21faa39b291cb3edec616` ("승인 (Recommended)") and asked to
run the window at once ("지금 진행"). W0 was re-run read-only at 23:07 KST and
passed as in the first attempt (R2 5.214 GiB stored); the timer was stopped and
the renderer helper installed for `a633d878`. No values are recorded below.

| Step | Result |
| --- | --- |
| W1 | `DELIVERED`; custody `state.json` `{"state":"DELIVERED","operator_healthy":true}` |
| Old-root sweep, first run | Exit 1 before any revoke: the W1 block leaves `set -C` on, so the sweep could not write its own `2>"$err"` file, and its `exit 1` closed the shell |
| Old-root sweep, second run | One `lookup-accessor` call returned 403 and the block stopped. A status-only re-read then returned 200 for all 5 accessors (policies `prometheus`, `default k8s-bootstrap`, `root` twice, `default hy-home-operator`); the 403 was not reproduced or explained |
| Old-root sweep, third run | `revoked=1`, `remaining=0` |
| Audit, secrets and auth lists (W1 root) | Audit none; secrets `cubbyhole`, `identity`, `secret/` kv, `sys`; auth `approle`, `kubernetes`, `oidc`, `token`. No plugin or audit device that W3a cannot open |
| W1c plan | `RENDERER_ROLES_PLANNED`; all 7 targets change. `renderer`, `renderer-issuer`, `renderer-cleanup` and both token roles are absent on HOME. `hy-home-operator` loses direct `auth/approle/role/hy-home-renderer/secret-id` and gains the two 5-minute token-create roles, as designed |
| W1c AppRole difference | HOME: policy `hy-home-renderer`, `token_period` 86400, ttl and max 0. Source: policy `renderer`, ttl 1h, max 24h, no period. With the single-use SecretID removed after reading, the Agent could not log in again about 24 h after W5 |

On that finding the owner stopped before apply ("쓰기 전 중단 (Recommended)"),
so nothing was written to HOME apart from the one old root the sweep revoked. A
fresh OIDC login proved operator access (the first paste was not a token and
was rejected with 403), the root was revoked (`ROOT_REVOKED_OPERATOR_HEALTHY`),
the w1 and w7 operator tokens were revoked with `revoke-self`, the cleanup block
ran and the timer was started again. External Secrets and the silence were
never touched. Credential-free receipts are in the owner's
`ops-snapshots/openbao-window-20261021b/`. The plan custody directory was left
behind because the cleanup glob lacked `p01-roles-plan.*`.

The owner chose a 24 h periodic renderer token ("period 24h 유지 (Recommended)").
`79c93e3d9` sets `token_period` 24h with ttl and max 0. On a throwaway 2.6.2
server the helper payload read back without a difference; login gave policies
`default renderer`, period 86400, `explicit_max_ttl` 0, renewable; renew-self
returned 86400; a SecretID replay was refused with 400. The same commit clears
noclobber inside the sweep subshell, adds `p01-roles-plan.*` to cleanup and
names the External Secrets controller as the W3 k8s writer.

An `iac-reviewer` review (requested by this session) returned READY WITH NOTES.
Applied in `bcdf29200`: the native rehearsal now asserts a renewable 24 h
periodic token, and the unit readback checks the cleared explicit max. It also
found that the External Secrets Deployment is managed by Argo CD
`platform-external-secrets-operator` under `root-platform`, both with
`selfHeal`, so RUN-0085 W3 now pauses both auto-syncs and saves the replicas and
sync policy before scaling to 0, and restores them afterwards, with owner
approval each window. The owner accepted the unbounded renderer token ("수용하고
POL-0085에 기록 (Recommended)"), and POL-0085 lists it as a residual until
2026-11-15. W5 still does not revoke the previous Agent token. The review also
noted that `verification.json` blocks that claim validity for the current
candidate were already stale before this change; that is not fixed here.

Native rehearsal on `bcdf29200`: two runs failed one or two timing checks
(`TLS_MATERIAL … native-user-read`, a TLS request timeout), and one run that
was meant to pause Airflow did not, because the container names reached
`docker stop` as one word. With the Airflow worker, DAG processor, scheduler and
triggerer stopped (owner approval "Airflow 일시 중지 후 실행 (Recommended)") the
suite passed 12 of 12 in 508.2 s; Airflow was started again. The input digest
`2264174ff7726d68108e7f8e9592c6f9e1db30e0b301e67ead98e0bc493d46f0` was
recomputed from the 34-file binding at `bcdf29200`; only `renderer-role.json`
and `test_openbao_rehearsal.py` differ from the previous binding. The candidate
suite then passed 2 of 2 on the same commit (276.4 s), covering the 14 tests of
the attempt 8 scope across two runs. The SEC01 ledger now binds that commit and
both log digests; the attempt 8 receipt and its binding moved to history with
an invalidation reason. HOME runtime was unchanged.

### Window 2026-10-22 07:00 — W1c and W2 applied, closed at W3

After #548 the owner approved `P01_APPROVED_COMMIT` =
`ea064f0b754c0845d2a9351ff93dac4aada7fb98` ("승인 (Recommended)") and chose a
07:00 window. W0 ran from 07:06 KST at that commit (load 6.8, IO pressure 8%).
The TLS preflight failed once with `TLS_MATERIAL FAIL check=native-user-read`
and passed on two reruns in 13 s and 11 s; a bare `docker run` of the image took
10.9 s against the check's 20 s limit, so the failure is read as a timeout. R2
held 5.251 GiB, the 03:30 backup had exited at 03:40, and the other W0 checks
held as before. No values are recorded below.

| Step | Result |
| --- | --- |
| W1, first try 07:13:57 | Stopped after `initialization.json`, with an empty `update-1.json`; the next pre-check saw `started:false`, so the attempt did not remain. Its status line was not reported |
| W1, second try 07:16 | `DELIVERED` |
| Old-root sweep | `revoked=0`, `remaining=0` (the `set +C` fix held) |
| W1c plan 07:17 | Same priors as the 2026-10-21 plan. AppRole now differs only in policy (`hy-home-renderer` to `renderer`), period 86400 and ttl/max 0 kept. Agent templates read only the Keycloak and Grafana paths that `renderer` allows |
| W1c apply 07:18 | `RENDERER_ROLES_APPLIED`, priors equal to the plan |
| W1c apply 07:20 (repeated) | `RENDERER_ROLES_APPLIED` with every target unchanged; a no-op |
| W2 07:18 | `SNAPSHOT_TOKEN_DELIVERED`; a repeat at 07:22 stopped before any request because the token existed |
| W3 writers | Silence `bb820476-729a-4c88-886f-684b66108695`; Agent stopped. Patching off auto-sync on `root-platform` and `platform-external-secrets-operator` (owner approval "ESO 정지 승인") was undone by `platform-cluster-config` and ApplicationSet `apps-generator`, and ESO came back at 1. On the owner's choice the Argo CD application and applicationset controllers were scaled to 0 (an unreviewed step), then ESO stayed at 0 |
| W3 lease | `LEASE_STARTED` |
| W3 snapshot | `BLOCKED` at the first `check_lookup`, before any renewal or download; the `.partial` files stayed empty |

Cause: `protected-raft-snapshot.py` required `token_policies` and
`identity_policies` in `lookup-self`, and both 2.6.2 and 2.7.1 omit them.
`check_renewal` was correct. Because a fix needs review and a new approval, the
window was closed at 07:35. The Argo CD controllers and ESO were scaled back to
1, the root was revoked (`ROOT_REVOKED_OPERATOR_HEALTHY`), the w1 and w7 tokens
were revoked, the cleanup ran and the timer was started. The w3a `revoke-self`
returned 2; its paste was never size-checked, so it may not have been a token,
and an OIDC token would expire within 4 h. Receipts are in the owner's
`ops-snapshots/openbao-window-20261022/`.

HOME now has the W1c policies and roles and the W2 snapshot token. The Agent is
stopped as RUN-0085 requires after a W3 stop; consumers keep their rendered
files until W5 of the next window. During the window only the
pre-existing `OpenBaoMetricsScrapeFailing` and
`OpenBaoAgentMetricsScrapeFailing` fired. A manual `hyhome-backup` run at 07:49
exited 0 (`Result=success`): the daily OpenBao Raft snapshot ran through
`hyhome-backup.sh` with the new token for the first time since 2026-10-12, and
R2 received the copy (5,661,951,661 bytes stored).

The fix accepts the omitted fields and still rejects a present wrong value. On
throwaway raft servers (images `11fd73a2` and `a58fb110`), the old helper is
BLOCKED at the first lookup, and the fixed one passes lookup, renewal, lookup,
seal, a 200 snapshot download of about 19 KB and archive validation. RUN-0085
W3 now describes the controller scale-down instead of the Application patch.
The next window starts at W1; W1c should plan no change and W2 is skipped once
the installed token is confirmed renewable.

### Window 2026-10-22 11:00 — W3a INDETERMINATE, closed before W4

After #549 the owner approved `P01_APPROVED_COMMIT` =
`14df75345432c13723206a41feac571762aef578` and started the window at once.
PRs #550–#554 changed no pinned file; the 15 blocks were re-extracted from that
commit and the 17 W1 manifest hashes matched. W0 held (TLS preflight PASS twice
in 13 s, load 6.4, IO pressure 12%, backup 07:49 exit 0, no silences). No values
are recorded below.

| Step | Result |
| --- | --- |
| W1, T=10:59:04 | 17 manifest files OK, `DELIVERED` |
| Old-root sweep | `revoked=0`, `remaining=0`; `audit` list empty, as expected before W4 |
| W1c plan | `RENDERER_ROLES_PLANNED`, all 7 targets `changed:false`; apply skipped |
| W2 | Skipped: the installed token served the 07:49 backup |
| W3 writers 11:02:44 | Silence `6e867678-3934-47f2-a4ca-b237551de25c`. Argo CD application controller, then applicationset controller, then ESO scaled to 0 (saved 1/1/1, 0 pods); Agent still stopped from the last window. The owner ran the step without a reply to the approval question; recorded as approval by execution |
| W3 lease and snapshot | `LEASE_STARTED`/`LEASE_BOUND` `a78d820d…`, `SAVED` 59,420 B, sha `36c57d80…`, Raft index 115150, 2.6.2 |
| W3b | `W3B_STORED`, restic `c07dcd25` tag `hy-home-openbao-w3`; a dump from R2 hashes to the same sha |
| W3a inputs | `BUNDLE_WRITTEN 3b78e285…`, `SECURITY_RECEIPT 04f2438f…`, contract `8c96c07e…` |
| W3a review | Agent checks plus an independent security-auditor binding review: GO. Lease and receipt file hashes matched the contract; target absent, parent 2064/115612004 |
| W3a restore 11:08:55 | `INDETERMINATE: retain target and ledger; do not retry` after about 100 s; the block exited the shell |

The ledger `.p01-restore-20261014-05.attempt.json` reads `indeterminate`, and
the target `p01-restore-20261014-05` (owned by the container user) is retained;
the attempt name is spent. No container, volume or network with label
`hy-home.attempt=p01-restore-20261014-05` and no `/dev/shm` attempt directory
remained. The client prints only the final line, so the failing step is
unknown; it is to be reproduced offline, not retried on HOME.

The window closed at 11:17 without W4. Root revoked
(`ROOT_REVOKED_OPERATOR_HEALTHY`), w1 and w7 `revoke-self=0`, w3a returned 2
(the restore client holds that token; an OIDC token expires within 4 h),
cleanup rc=0. ESO, then the applicationset controller, then the application
controller were scaled back to 1 and rolled out; ClusterSecretStore Ready, all
6 ExternalSecrets `SecretSynced`, every Application Synced/Healthy; the
backup timer is active. Receipts, the contract, both lease files, the security
receipt and the ledger copy are in the owner's
`ops-snapshots/openbao-window-20261022b/`.

HOME is unchanged: 2.6.2 with the pre-hardening listener (plain HTTP, no audit
device) and the Agent stopped. Firing during the window, none caused by it:
`OpenBaoMetricsScrapeFailing` and `GatusEndpointFailing` (security/OpenBao),
both because the checks expect TLS; `OpenBaoAgentMetricsScrapeFailing`;
`ContainerHighThrottleRate`; and `ContainerHighMemoryUsage` for the k8s Alloy
pod.

### W3a INDETERMINATE cause and fix — 2026-10-22

The retained target's file times and the Docker daemon log place the failure
in the Agent step: the old server restored at 11:09:28, the candidate and the
restore Agent (`2618af73…`) started at 11:10:14, its health check ran at
11:10:21, and the client's reclaim stopped the Agent at 11:10:25 before the
ledger turned `indeterminate` at 11:10:36. No token-creation write followed the
health check, so the helper had succeeded and the rendered-value comparison
failed.

`protected-semantic-restore.py` had never run against real Docker; its tests
use fakes. A throwaway rehearsal ran the real `perform()` at `14df75345`
(constants patched to a scratch attempt and a synthetic cluster) against a
HOME-shaped 2.6.2 raft source with an HTTP listener, KV v2, the
renderer/issuer/cleanup/operator policies, the `hy-home-renderer` AppRole and
the two token roles from the repository. With plain canary values it was
accepted. With a Grafana value ending in a newline it was `INDETERMINATE` in
`_agent_run`, the HOME result. The templates trim their own whitespace
(`{{- … -}}`), so the rendered file is the exact value, and the client's
`rstrip("\n")` removed the value's own newline.

The fix compares the rendered file exactly and moves the next attempt to
`p01-restore-20261022-06` (the `-05` target and ledger stay retained). The unit
fake now renders the exact bytes, one value ending in a newline; it fails on
the old client and passes on the new one. Both rehearsals, newline and plain,
are accepted with the fixed client. The owner's values-free check found that both HOME canary files end in a
newline (no carriage return), which confirms the cause.

### Window 2026-10-22 12:30 — upgraded to 2.7.1

The owner approved `P01_APPROVED_COMMIT` =
`090352d0583d45b6d0d83470955ac0b4bb6a7b5e` (#556) and started at once. All 17
W1 manifest pins matched and the 15 blocks were re-extracted; only the client
pin changed. W0 held (TLS preflight 12 s, load 6.0). No values are recorded.

| Step | Result |
| --- | --- |
| W1, sweep, W1c plan | `DELIVERED`; `remaining=0`; all 7 targets `changed:false`, apply and W2 skipped |
| W3 writers | Silence `baa45277-7fdf-46ee-8c35-7f21d839cb24` (3 h, also `GatusEndpointFailing`); Argo CD controllers and ESO to 0 (saved 1/1/1); recorded as approval by execution, as before |
| W3 lease, snapshot, W3b | Lease `bc0fb363…`; snapshot sha `63f00be6…` 59,420 B, Raft index 115754; restic `8fe28d5c`, a dump from R2 hashes the same |
| W3a inputs and review | Contract `a07fe0ae…` for `p01-restore-20261022-06`; installed client `766bbc66…` equals the pin; agent checks plus an independent security-auditor binding review: GO |
| W3a restore | `accepted` in the `-06` ledger (12:40–12:42). A later re-run in a fresh shell without the variables stopped at the missing lease file before any effect |
| W4 | Recreated at 12:42:55; same data mount; unsealed; 2.7.1+hyhome, active |
| W5 | The runbook block failed with 403 at `auth/token/create/renderer-issuer`: its CLI `renewable=false no_default_policy=true` arrive as strings, and the operator policy's `allowed_parameters` accept only the booleans (reproduced on a throwaway 2.7.1 server). With owner approval the same request was sent as JSON booleans; `W5 rc=0`, Agent `healthy` |
| W6 | HTTPS answers and plain HTTP is refused; `audit.json` grew 260,752→263,517 B in 20 s; `up` 1 for `openbao` and `openbao-agent`; Gatus OpenBao `success=true`; both `.version` files re-rendered, the password files unchanged |
| W7 | `ROOT_REVOKED_OPERATOR_HEALTHY`; w1 `revoke-self=0`, w3a/w5/w7 returned 2 (spent or expiring OIDC tokens) |
| Close | cleanup rc=0; ESO and both Argo CD controllers back to 1; timer active; a manual backup at 13:00:31 `Result=success` |

After the restore, ESO saw 403 for about two minutes (12:54–12:56) on
`lookup-self` and reads, then synced; `argocd-external-valkey` stayed in
`SecretSyncedError` until a forced refresh at 13:02:54, after which every
ExternalSecret is synced and every Application Synced/Healthy. The cause of the
short 403 window is open. Receipts, the contract, both lease files, the security
receipt and the ledger are in the owner's `ops-snapshots/openbao-window-20261022c/`.

HOME now runs 2.7.1+hyhome.go1.27.3.net0.60.0.r1 with TLS and the config-owned
audit device, and the Agent renders again. The W5 typed-JSON runbook fix was subsequently merged (#557) and is reused.
Open: the short ESO 403 cause and confirming the silence disposition after the
alerts are recorded. Those original close observations are repository-reported;
raw operational receipts are unavailable in the current session.

### v28 current execution assessment and remaining handoff — 2026-10-22

The operational results below are **REPOSITORY_REPORTED /
RAW_EVIDENCE_UNAVAILABLE** from the earlier Work Log. This session did not open
raw operational receipts and does not claim these as new executions. Keep failed
`-05` and accepted `-06` as separate attempts. The earlier "never run against real
Docker" statement describes its investigation baseline; later native and HOME
records supersede its current applicability. Draft status or earlier accepted
readiness criteria do not accept all operations.

| Step | Preserved input, execution and later result | Current disposition and residual |
| --- | --- | --- |
| W1 / old-root sweep | 11:00 `14df753…`, 12:30 `090352d…`: DELIVERED, remaining=0 | Reuse; new source requires new approved pins |
| W1c | Both windows all7 changed:false, apply skipped; earlier role apply retained | Do not reapply periodic24h/max0 |
| W2 | Both skipped; installed token used by 07:49 backup | Preserve INDETERMINATE lock/custody rules |
| W3 writers | Three controllers0 in both windows, original1/1/1; approval by execution recorded | Preserve unreviewed-step history; no current UID/replica/window authority |
| W3 snapshot / W3b | 11:00 sha36c57d80…, restic c07dcd25; 12:30 sha63f00be6…, restic8fe28d5c, matching R2 dump reported | Historical artifacts only; do not repeat as a new snapshot |
| W3a `-05` | 11:08:55 start, indeterminate after about100s, retained ledger/target | Spent; never retry; A3 disposition below |
| W3a `-06` | contract a07fe0ae…, client766bbc66…, accepted12:40–12:42 | Spent; next attempt needs new name/constants/review |
| W4 | Recreated12:42:55, same data mount, unsealed2.7.1+hyhome | HOME is no longer the2.6.2 baseline; cold boot separate |
| W5 | String booleans403, then owner-approved JSON booleans rc0/Agent healthy | Reuse merged#557 fix; old Agent token remains B4 |
| W6 | audit260752→263517B/20s, OpenBao/Agent up1, Gatus success, versions rendered | Natural rotation/inode/capacity trend unobserved |
| W7 / Close | ROOT_REVOKED_OPERATOR_HEALTHY, cleanup0, controller1 restored; most ESO recovered, valkey needed forced refresh | Do not turn revoke-self2 into success; ESO cause UNKNOWN |
| Manual backup | 13:00:31 Result=success reported | Does not accept scheduled backup/off-host restore/cold boot |

**A1/A2 local edits.** RUN-0085's existing W3 now binds context, current UID and
original replicas; stops the two Argo controllers before ESO; checks
zero desired/current/ready and no pods after30s and immediately before snapshot;
and stops on query failure, restoring only attempted changes in ESO→ApplicationSet
→Application Controller order. Finish checks Store Ready, the approved exact six
namespace/name/Store bindings, refreshTime after Finish, Ready True/SecretSynced
and related Applications Synced/Healthy. The six names, installed ESO/Argo
versions, cache options and policy applicability are missing, so read-only
metadata discovery and operator approval of the exact set precede writes. With
cause still unknown, force-sync is limited to one approved request per failed
expected resource and bounded rechecks. Actual cluster commands and separate
restart-versus-restore ESO/TokenReview reproduction are NOT_RUN.

**A3 exact disposition handoff.** Preserve accepted `-06` ledger, contract and
receipts. Before deleting its container-UID-owned target, verify its exact path,
parent device/inode, mount, symlink/hardlink state, references and absence of
active processes/containers; resolve recovery dependencies and obtain the owner's
specific approval and sudo executor. Acceptance does not authorize ledger
removal. Proposed `-05` disposition is retention until the next window/review;
owner decision is PENDING. The two p01-client and two p01-inputs directories
under `/run/user/1000`, and their lack of credentials, are user reports only.
Deletion is NOT_RUN without current UID, four exact paths, permission/no-secret/
nonreference/inactive checks and owner authority. Choose approved exact-list
cleanup or disappearance at a later natural reboot; no glob deletion or reboot
for cleanup. Root custody and W2 locks are outside this cleanup.

**B4 old Agent token: BLOCKED / SOURCE_NOT_IMPLEMENTED.** Existing issuance
v1/v2 journal and matching_accessor/lookup/destroy concern SecretID generations
and SecretID accessors. They do not identify Agent login token generations.
Do not add token fields to the current secret-free journal contract. Since
start-agent replaces the old sink, protected exact-generation capture must
precede stop/new issuance. health-agent/ready proves two KV bytes/versions and
Agent StartedAt; actual application consumption remains P06 acceptance.

The concrete candidate extends the **same journal with an explicitly private,
sensitive v3** and durable phases prepared→issuing→delivered→verified→revoking→complete.
Preserve v1/v2 recovery. Bind old/new generations to cluster/source/image,
StartedAt, creation time, auth path/role, exact policies and protected custody
reference. Atomically persist prepared, then capture the old sink token through
nofollow, bounded, owner0600, stable descriptors into separately authorized
custody. Verify a distinct new generation/current sink, both KV versions, P06
consumption and renewal/readback before durable revoke intent and old-token
revoke-self. Public receipts contain no token/accessor/hash. Alternative:
capture the exact sensitive accessor and use a short-lived revoker constrained
by required/allowed_parameters; this adds policy/producer review and allows no
accessor LIST or wildcard.

Resume inputs: approved capture path/owner/retention/destruction, v3 anchor and
recovery contract, selected-version revoke-self capability, P06 consumer verifier,
and child-lease/rollback disposition. Required tests preserve v1/v2 and cover
interruption at each phase, old=current/wrong generation/multiple targets, sink
races/restart, missing or unsafe journal/custody, timeout/403/sealed/expired.
Acceptance requires old renew and both KV reads denied while new read/renew
remain healthy. Timeout preserves INDETERMINATE intent for bounded reconciliation,
never blind retry. A403 alone is not expiry proof. Preserve the current healthy
sink, administrator/backup tokens and unrelated accessors. This proposal links
to D1-renderer; it neither ends the risk nor authorizes a revoke.

**Local implementation and checks.** B1's snapshot helper now requires an explicit
empty-string entity_id; missing/null/nonempty/wrong types fail without widening
operator authorization. Worker evidence: RED7 failing subcases, GREEN31 tests;
helper SHA-256 `d5dd5086981bf9dfff7977e527ed28cb760194fe32157945e05ef5342633d174`,
also updated in RUN-0085's active manifest. B3 keeps OpenSSL's existing10-second
bounds, raises the native user probe to60 seconds with kill grace5, and gives
its two existing native callers190 seconds for the full bounded path. Failure,
timeout or signal retains exact unique tracking metadata for later daemon
reconciliation; an immediate empty list does not prove late creation impossible.
No broad cleanup is used. Worker evidence: final10 synthetic TLS tests PASS,
shell syntax and shellcheck warning level PASS; actual wall-clock25/61-second
or daemon execution NOT_RUN. TLS source SHA-256
`63d0de9d25be70400f90aa18956c5919fdde86832bad008a8cef533ae4676841`.

B2 reuses the existing full_perform harness for plain and trailing-newline
values, adds empty-value refusal before restore and proves the opt-in skip
precedes HOME fixture/subprocess access. Worker run of restore-input and restore
modules:57 selected,53 PASS,4 native SKIP,1.986 seconds. These are separate from
historical native successes, and the expanded native paths are NOT_RUN.
The synthetic RUN command suite executes the actual Bash functions with real
bash/jq and fake kubectl; it verifies exact-six/freshness/Store/Application
checks, API failure distinction and changed-only reverse restoration with UID
refusal. Worker run with existing Agent contract/metrics tests:36 PASS,14.690
seconds. Mutating freshness or removing UID protection caused expected failures.
This proves command gates, not cluster recovery or ESO cache behavior. A later
explicit original-zero-replica case also passed. The final worker run selecting
window overrides, restore inputs and semantic restore had69 tests:65 PASS,
4 native SKIP,4.110 seconds; eight of its tests execute the runbook functions.
That selection is separate from the preceding36-test Agent-inclusive run.

Document validation: five new Bash blocks passed syntax and seven temporary
synthetic ESO-gate probes passed. Markdownlint on the four owned documents found
two blank-line issues, then passed after correction. The first metadata/link
checks found English-document language and historical version-literal deficits;
only new text was aligned to the documents' language and same-line historical
exceptions. The repository-wide check also reported unrelated errors whose
baseline applicability requires separate classification. The single corrected
metadata retry selected these four paths, reported no violation on any of them,
and exited1 with146 other/global violations, including SPEC-0212's legacy-table
contract error. Its public diagnostic log is `/tmp/v28-openbao-doc-metadata.log`,
SHA-256 `0675bd31f00956c000ca1110f2910bcc5e284607a35aaba9c9c8177b861a5cf7`.
This is not a metadata PASS or proof that all other findings predate the task.
The root coordinator owns final links and independent review disposition. Original Task Evidence, Criterion Acceptance and Review
bodies from the Evidence heading onward remain byte-for-byte equal to HEAD.

**D1 improvement proposals and owner decision.** The user chose to retain the
existing deadline and prepare improvements. The three risks retain2026-11-15;
no new expiry or acceptance is recorded.

| Risk | Improvement alternatives before the deadline | Evidence and approval boundary |
| --- | --- | --- |
| Renderer | Reconsider periodic24h/max0 exception or choose finite explicit max plus scheduled reauthentication/SecretID issuance; include B4 old-generation cleanup | Role readback, renewal bound/stopped-renewal expiry, new-issuance failure recovery, out-of-scope read denial, cold boot/P06; do not claim retroactive effect on existing tokens |
| Sealed custody | Reconsider the current exception or use time-bounded custody and verified unseal/OIDC/alternative management before disposition | Preserve last administrator; review quorum/shares/reboot/swap and success/failure/interruption; no deletion/unseal/root issuance before approval |
| W2 uncertainty | Reconsider lock/custody retention and next-W2/W3 block, or reconcile exact attempt/server accessor/role/partial delivery | Account for possible issuance, token validity and last management access; missing-journal/expiry/partial-failure tests and owner acceptance; no forced unlock/duplicate issuance |

Before2026-11-15, the owner must select each alternative's operational cost,
compensating controls, new expiry or closure condition, executor and authority.
Without a decision, hold only new changes relying on that risk; do not stop the
current service or remove the last access. Other POL-0085 risks, including shared
UID, swap and single-file custody, remain with their existing owners. No policy
was modified in this session.

### Final local verification — v28, 2026-10-22

The final source input is based on `73433adc1b685582741604d8acc1f6f70be0adbe`
on `codex/v28-local-residuals`. Independent `/root/review_changes` approved
the 20-file source manifest
`acaded64bf2edccea2973e3084c4f017ead8cac6bd0e3b254f7e99e13edb041c`.
The separate security/IaC review `v28-security-iac-20261022-01` found no
remaining blocking source finding; its initial TLS late-create finding was
resolved by retaining tracking metadata and reporting pending reconciliation.
The final review also checked the corrected 0245/0246 evidence references.
These verdicts authorize no runtime operation or criterion acceptance.

Final local checks and their actual boundaries:

- Snapshot regression: 31 PASS; synthetic TLS probe: 10 PASS.
- Restore-input, semantic-restore and window suites: 69 tests, 65 PASS and
  4 opt-in Native SKIP. These are one reported invocation, not a sum of
  overlapping test runs. Eight window cases execute actual fenced runbook
  functions with fake kubectl and real Bash/jq.
- Supply-chain regression: 28 PASS; CI contract regression: 28 PASS.
  These are separate invocations. Current evidence remains source-only.
- `python3 scripts/validation/check-document-metadata.py --mode check-changed
  --base-ref 73433adc1b685582741604d8acc1f6f70be0adbe`: exit 0,
  selected 9, violations 0. The earlier invalid legacy-table append and
  three invalid Resolves references were corrected without changing their
  validators or historical rows. The 145 archive type errors were cascades
  of failed package validation and are absent on this corrected input.
- `python3 scripts/validation/check-document-links.py --mode all`: exit 0,
  1,328 documents, 11,789 links, zero failures and one warning about 2,870
  historical links without capture sources. Historical resolution remains
  unverified. The final result-only Task notes add no link destinations.
- The public changed/local-only runner exited 1 at
  `ci-gate-local-toolchain` before executing a leaf: local Python 3.12.3
  differs from the hosted 3.14.8 pin. The installed standalone 3.14.8 build
  also lacks the required memfd seal constants. No gate was bypassed.
- `graphify update .` completed: 28,958 nodes and 50,556 edges. SQL/HCL
  extraction reported missing optional parsers; no LLM labeling ran.

The current 42-input assessment has manifest
`078f9d12c3c73d5cada9deb436cbf09708b9f7e4343628f6d6318226fe5b721f`;
its Native validity is false and its current Native/HOME results remain
NOT_RUN. B1 operator binding, B4 implementation, A3 cleanup, P06 consumption,
the complete ROOT supplier/security audit and owner acceptance remain open.
The first normal commit attempt stopped at the pinned Ruff format check for
the new TLS test. Formatting with the registered 0.15.12 binary preserved its
Python AST; the current input manifest above was refreshed afterward.
Normal local commits follow installed hooks; main integration, remote CI,
push, PR, deployment and operational changes remain NOT_RUN.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Readiness review | 7 | W1 | Independent `iac-reviewer` readiness review of RUN-0085 0.10.4: NOT READY | `f0984f3c0` | FAIL | Inputs and Authorization | - |
| Text review | 7 | W1 | Independent `iac-reviewer` re-review of the W1 text: W3a not BLOCKED; Gatus never recreated | `8e28414f5` | FAIL | W1 Window Text | - |
| Text checks | 1 | W1 | Changed metadata 0 violations; links `--mode all` PASS; markdownlint 0; operations catalog and OpenBao consumer contract tests OK | Branch after `8e28414f5` | PASS | W1 Window Text | - |
| Text re-review | 7 | W1 | Independent `iac-reviewer` re-review: PASS with notes, notes applied | `0a3930f8a` | PASS | W1 Window Text | Text review |
| Server start unit | 2 | W2 | Server-argument assertion RED on the old code, GREEN after; suite 26 OK under umask 022 | Branch on `claude/window-readiness` | PASS | W2 Restore Server Start | - |
| Server start native | 2 | W2 | Tool's create arguments on a synthetic empty target, both images: uninitialized, sealed, Raft; pre-fix arguments fail to start | Owned `46bf9b5c`, old `11fd73a2` | PASS | W2 Restore Server Start | - |
| Server start review | 7 | W2 | Independent `security-auditor` review of the server start fix: PASS with notes | `e439fc1a6` | PASS | W2 Restore Server Start | - |
| Restore flow unit | 2 | W2 | Unseal, login, stat, restore user and snapshot mode assertions RED on the earlier code (3 failures), GREEN after; both suites OK under umask 022 | Branch | PASS | W2 Restore Server Start | - |
| Restore flow native | 2 | W2 | Synthetic init, unseal, login, snapshot save and restore on both images: restore as server user with 0440 snapshot returns 0; old forms fail | Owned `46bf9b5c`, old `11fd73a2` | PASS | W2 Restore Server Start | - |
| Restore flow review | 7 | W2 | Independent `security-auditor` re-review: foreign-share denial check stops every restore | Branch `205fb7593` | FAIL | W2 Restore Server Start | - |
| Denial check fix | 2, 7 | W2 | Two-share denial assertions RED on the earlier code, GREEN after; native on both images: first foreign share sealed at progress 1, second invalid key, originals unseal | Branch | PASS | W2 Restore Server Start | Restore flow review |
| Restore flow re-review | 7 | W2 | Independent `security-auditor` third review: PASS with notes, notes applied | `01b4150b4` | PASS | W2 Restore Server Start | Restore flow review |
| Role apply unit | 3 | W3 | 11 unit tests OK under umask 022; removing the AppRole check and readback comparison fails 2 | `455dffd70` | PASS | W3 Renderer Role Apply | - |
| Role apply native | 3 | W3 | Real tool on an owned synthetic server, both images: targets replaced and read back, RoleID kept, role tokens exact, wrapped SecretID only, second run unchanged | `455dffd70` on owned `46bf9b5c`, old `11fd73a2` | PASS | W3 Renderer Role Apply | - |
| Role apply reviews | 7 | W3 | Independent `security-auditor` and `iac-reviewer` reviews: both PASS with notes, notes applied | `5c2dd4601` | PASS | W3 Renderer Role Apply | - |
| Role apply fixes | 3 | W3 | 17 tests OK under umask 022 with both native runs: plan writes nothing, operator token makes the W5 request, defaults read back; removing the BindingBlocked catch or the plan write guard fails 2 | `d4a4455c4` on owned `46bf9b5c`, old `11fd73a2` | PASS | W3 Renderer Role Apply | - |
| Role apply re-review | 7 | W3 | Independent `iac-reviewer` re-review of the fixes: PASS with notes, notes applied; 17 tests OK with both native runs; CI gate tests OK | `3e080d999` | PASS | W3 Renderer Role Apply | - |
| Restore input producers | 4 | W4 | 10 unit tests through the restore client's own lease and contract validators, OK in a umask 022 clone with the restore suite (36); start-before-save mutation fails a test | `33763dd1d` | PASS | W4 W3a Input Producers | - |
| Restore input reviews | 4, 7 | W4 | `security-auditor` APPROVE with notes; `iac-reviewer` REJECT: no native rehearsal, candidate not bound to the commit | `0294deaf8` | FAIL | W4 W3a Input Producers | - |
| Restore input native | 4 | W4 | Real 2.6.2 synthetic snapshot through every producer CLI and the restore's `_contract`, `QuiescenceLease`, `Admission.pre_read` and `preflight`; preflight platform-ID defect fixed (RED then GREEN); 15 tests OK in a umask 022 clone | `863eafa40` on old `11fd73a2` | PASS | W4 W3a Input Producers | Restore input reviews |
| Restore input re-review | 7 | W4 | Independent `iac-reviewer` re-review: PASS with notes, notes applied; 66 tests OK with all native rehearsals in a umask 022 clone; manifest pin test OK | `a4dbc0f9e` | PASS | W4 W3a Input Producers | Restore input reviews |
| Second readiness review | 7 | W1 | Independent `iac-reviewer` readiness review of the whole window: NOT READY (SEC01 gate text, timing, W6 timing, W3a status, root custody, W5 token step) | `a4dbc0f9e` branch | FAIL | Second Readiness Review and Window Text | - |
| Window security review | 7 | W1 | Independent `security-auditor` review of W1, W6 and the window text: REJECT (un-revoked root on disk, old token in argv, zsh prompt) | Branch `claude/window-text-r2` | FAIL | Second Readiness Review and Window Text | - |
| Window IaC review | 7 | W2 | Independent `iac-reviewer` review of W2, W5 and the window text: NOT READY (Agent input chown fails natively, timing, stop path, W3a secret input) | Branch `claude/window-text-r2` | FAIL | Second Readiness Review and Window Text | - |
| Host logrotate install | 6 | W6 | Read-only: timer drop-in loaded with the next run within an hour; `/etc/logrotate.d/openbao` root 0644, SHA-256 equal to the tracked rule | Host 2026-10-15 | PASS | Owner Host Preparation | - |
| Window host prerequisites | 1 | W1 | Read-only: Linger yes, Docker debug false; owner-reported: old operator token expired (lookup denied) and shredded; TLS preflight run by the owner, output not observed here | Host 2026-10-15 | PASS | Owner Host Preparation | - |
| Traefik pin recreate | 6 | W6 | Read-only after the owner's recreate: image `575fa15b`, healthy, 0 restarts, `/openbao-ca/ca.pem` present, no log error | Host 2026-10-15 | PASS | Owner Host Preparation | - |
| Final IaC readiness review | 7 | W1 | Independent `iac-reviewer` review of the whole window: NOT READY (root rebuildable from W1 custody; acceptance period; Agent after an early stop; k8s writers; shell state; stale text) | `12ab97dab` | FAIL | Final Readiness Review | - |
| Final security readiness review | 7 | W1 | Independent `security-auditor` review of the whole window: APPROVE with notes (root rebuildable from W1 custody; no accessor capture; operator tokens left live) | `12ab97dab` | PASS | Final Readiness Review | - |
| Final review text fixes | 1 | W1 | Owner decisions recorded; RUN-0085 text fixed; overlay headers rollback-only; markdownlint 0, links PASS, overlay tests OK | Branch `claude/window-final-review` | PASS | Final Readiness Review | - |
| Final IaC re-review | 7 | W1 | Independent `iac-reviewer` re-review of #499: NOT READY (cleanup against INDETERMINATE rules, W0 Agent baseline after a stop, tokens shown to reach W1 and W3a, no fresh-login proof before revoking); restore deltas `c9aa69b89` and `3cbde6376` PASS with notes | `adacb8a6c` | FAIL | Final Readiness Review | - |
| Final security re-review | 7 | W1 | Independent `security-auditor` re-review of #499: APPROVE with notes (stranded-root sweep had no exact command; exit2 precedence; W1 and W3a prompts; cleanup guards; swap and UID 100 residuals) | `adacb8a6c` | PASS | Final Readiness Review | - |
| Final re-review text fixes | 1 | W1 | RUN-0085 cleanup order, W2 keep, fresh-login proof, evidence copy, FD token inputs, Agent baseline, exact sweep; cleanup block rehearsed on fake directories; sweep rehearsed on a throwaway dev server | Branch `claude/window-final-review` | PASS | Final Readiness Review | - |
| Final IaC re-review 2 | 7 | W1 | Independent `iac-reviewer` re-review of `dc2378c74`: NOT READY (sealed-server rules contradict the login proof; the sweep can fail open); N1 to N3 closed | `297b65ee0` | FAIL | Final Readiness Review | - |
| Final security re-review 2 | 7 | W1 | Independent `security-auditor` re-review of `dc2378c74`: APPROVE with notes (sweep can fail open; sweep only when a strand is known; sealed case; W1c wording; W7 file name; login proof command) | `297b65ee0` | PASS | Final Readiness Review | - |
| Final re-review 2 text fixes | 1 | W1 | Sealed exemption and an exact login proof with its own token; sweep in a pipefail subshell that stops on any list or lookup failure and recounts to 0, run after W1 in every window; W0 checks `jq`; W0 and W7 token files named; W2 kept means W2 and W3 BLOCKED; path variables saved in each block; sweep rehearsed on a dev server: `jq` failure exits 1, success revokes 2 and recounts 0 | Branch `claude/window-final-review` | PASS | Final Readiness Review | - |
| Final IaC re-review 3 | 7 | W1 | Independent `iac-reviewer` re-review of `a78f5073c`: NOT READY (an unsealed OIDC failure still shredded the only root, with no keep switch); round-3 findings closed | `98303ca92` | FAIL | Final Readiness Review | - |
| Final security re-review 3 | 7 | W1 | Independent `security-auditor` re-review of `a78f5073c`: APPROVE with notes; N1 to N7 closed; Low: sweep aborts on a vanished accessor, no W1 pointer, empty `self`, no root keep switch | `98303ca92` | PASS | Final Readiness Review | - |
| Final re-review 3 text fixes | 1 | W1 | `P01_KEEP_ROOT` keeps W1 custody and operator token files on an unsealed OIDC failure; sealed-only root strand; `P01_KEEP_W2` persists; receipts copied; sweep treats `invalid accessor` and `No token found` as gone, requires a non-empty `self`, may re-run once; W1 points to the sweep; dev-server rehearsal with a cascaded child root: `revoked=3 remaining=0`, re-run `revoked=0`; keep switch rehearsed on fake directories | Branch `claude/window-final-review` | PASS | Final Readiness Review | - |
| Final IaC re-review 4 | 7 | W1 | Independent `iac-reviewer` re-review of `0d59ce192`: READY with Low notes only; every earlier finding closed | `c61f3ca95` | PASS | Final Readiness Review | Readiness review, Second readiness review, Window security review, Window IaC review, Final IaC readiness review, Final IaC re-review, Final IaC re-review 2, Final IaC re-review 3 |
| Final security re-review 4 | 7 | W1 | Independent `security-auditor` re-review of `0d59ce192`: APPROVE with notes (Low: stderr mixed into the root test, gone messages split by branch, keep path removed the vars file) | `c61f3ca95` | PASS | Final Readiness Review | - |
| Final re-review 4 text fixes | 1 | W1 | Low notes applied; sweep rehearsed on a dev server with five parent and child root pairs and an injected stderr `root` warning: `revoked=11 remaining=0`, non-root token and new root kept | Branch `claude/window-final-review` | PASS | Final Readiness Review | - |
| Policy and guide alignment | 1 | W1 | Owner decisions recorded; POL-0085 window rules, SEC01 acceptances and residual exceptions with expiry 2026-11-15; guide login and window overview; markdownlint 0, links PASS | Branch `claude/openbao-policy-guide` | PASS | Policy and Guide Alignment | - |
| Policy rules review | 1 | W1 | Independent `rules-engineer` review: FAIL (token channel and exceptions, kept-root limit, Traefik and Prometheus acceptance out of scope and weaker than the owner record, Low wording) | `bbc15d1d1` | FAIL | Policy and Guide Alignment | - |
| Policy rules fixes | 1 | W1 | All findings applied; image acceptances moved to POL-0013 and POL-0045 as the owner asked; markdownlint 0, links PASS; security review still required | Branch `claude/openbao-policy-guide` | PASS | Policy and Guide Alignment | Policy rules review |
| Agent input fix | 2 | W2 | Native chown with the restore's flags: exit 1 without `DAC_READ_SEARCH`, 0 with it; new assertions RED on the earlier code, GREEN after; 47 OK and native preflight 17 OK in a umask 022 clone | `2e3683771` (#492) | PASS | Restore Agent Fix and Full Rehearsal | - |
| Full restore rehearsal | 2 | W2 | Native `orchestrate()` and `perform()` on synthetic resources, old `11fd73a2` restore and owned `46bf9b5c` candidate and Agent: ledger `accepted`, no attempt containers left; four defects fixed with RED then GREEN unit assertions; restore-input suite 18 OK with `HYHOME_OPENBAO_REHEARSAL=1` in a umask 022 clone | `564f4049c` | PASS | Restore Agent Fix and Full Rehearsal | - |
| Restore fix IaC re-review | 7 | W2 | Independent `iac-reviewer` re-review of #492 and #495: FAIL (umask 077 leaves `tls/` unreadable to the server; cleanup misses the pre-token gap and depends on the shared runner) | `bc552bf9b` | FAIL | Restore Agent Fix and Full Rehearsal | - |
| Restore fix security re-review | 7 | W2 | Independent `security-auditor` re-review of #492 and #495: APPROVE with notes (Medium: rendered values can stay in `/dev/shm` on failure paths) | `bc552bf9b` | PASS | Restore Agent Fix and Full Rehearsal | - |
| Restore review fixes | 2, 7 | W2 | 11 new or changed unit assertions RED on the earlier module (`tls/` 0700 under umask 077), restore suite 32 OK after in a umask 022 clone; native `perform()` with `orchestrate()` under umask 077: the earlier module ends INDETERMINATE, the fixed module ends `accepted` with no attempt container, volume, network or `/dev/shm` directory left; native suite 2 OK | `6fd36be4a` | PASS | Restore Agent Fix and Full Rehearsal | Restore fix IaC re-review |
| Restore fix second IaC re-review | 7 | W2 | Independent `iac-reviewer` re-review of #498: PASS with notes; H1, M1, M2, L1, L3 closed; W2 READY with notes (failure-path time budget, interrupted-run checks) | `efc4a68bb` | PASS | Restore Agent Fix and Full Rehearsal | - |
| Restore fix second security re-review | 7 | W2 | Independent `security-auditor` re-review of #498: APPROVE with notes; F1 and F2 closed; notes: unverified Agent stop, 0777 mount points, Agent AppRole token not revoked | `efc4a68bb` | PASS | Restore Agent Fix and Full Rehearsal | - |
| Restore re-review notes | 2 | W2 | Reclaim confirms the Agent is not running, mount points 0755, Agent AppRole login leases revoked on the candidate, preflight refuses an operator GID other than 1000; new assertions RED on the earlier module (4); 70 unit OK and native restore-input suite 18 OK in a umask 022 clone | `c9aa69b89` | PASS | Restore Agent Fix and Full Rehearsal | - |
| Restore notes delta review | 7 | W2 | Independent `security-auditor` review of `c9aa69b89`: APPROVE with notes; notes applied: only "No such container" counts as a stopped Agent, effective GID check, failure-path budget about 9 minutes, interrupted-run checks by attempt label; new assertions RED on the earlier module (2); W3a no longer BLOCKED | Branch `claude/restore-review-fixes` | PASS | Restore Agent Fix and Full Rehearsal | - |
| Window text round 2 | 1 | W1 | Owner decisions recorded; RUN-0085 text fixed; metadata check-changed 0, links PASS, markdownlint 0, related suites 70 OK | Branch `claude/window-text-r2` | PASS | Second Readiness Review and Window Text | - |
| R2 artifact action | 5 | W5 | Contract test OK, read-back removal fails it; native rehearsal in `restic/restic:0.19.1`, no network, local repository: both files stored and proved, symlinked input exits 64 before backup; Compose baseline gates OK | `bab3124fc` | PASS | W5 R2 Artifact Transfer | - |
| R2 read-only rehearsal | 5 | W5 | `restic-offsite cmd snapshots --no-lock --json` against HOME's R2 repository, owner-approved: reachable and decrypted, 45 snapshots, latest 2026-10-13T18:42:46, none tagged `hy-home-openbao-w3`; no write, no lock | HOME R2 on 2026-10-14 | PASS | W5 R2 Artifact Transfer | - |
| R2 artifact review | 7 | W5 | Independent `security-auditor` review: PASS with notes, notes applied; 5 tests OK including the native rehearsal | `bab3124fc` | PASS | W5 R2 Artifact Transfer | - |
| Window overrides | 6 | W6 | Compose config with and without the override differs only in the Traefik and Prometheus image; CA mounts kept; contract test OK; timer drop-in passes `systemd-analyze verify` on a copy of the host units | `ccfa88e05`; running images observed 2026-10-14 | PASS | W6 CA Mounts, Logrotate and W4 Rollback | - |
| W4 rollback decision | 6 | W6 | Owner chose fix-forward (AskUserQuestion) | Owner answer 2026-10-14 | PASS | W6 CA Mounts, Logrotate and W4 Rollback | - |
| W6 review | 7 | W6 | Independent `iac-reviewer` review: PASS with notes, notes applied; contract tests and CI gate tests OK | `ccfa88e05` | PASS | W6 CA Mounts, Logrotate and W4 Rollback | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | accepted | Text checks, Text re-review | Owner accepted 2026-10-14 |
| 2 | accepted | Server start native, Restore flow native, Denial check fix | Owner accepted 2026-10-14 |
| 3 | accepted | Role apply native, Role apply fixes, Role apply re-review | Owner accepted 2026-10-14 |
| 4 | accepted | Restore input native | Owner accepted 2026-10-15 after #486 and #487 merged |
| 5 | accepted | R2 artifact action, R2 read-only rehearsal | Owner accepted 2026-10-15 after #486 and #487 merged |
| 6 | accepted | Window overrides, W4 rollback decision | Owner accepted 2026-10-15 after #486 and #487 merged |
| 7 | accepted | Final IaC re-review 4, Final security re-review 4 | Owner accepted 2026-10-15 after #499 merged |

## Review and Completion

On 2026-10-14 the owner (AskUserQuestion) accepted criteria 1 to 3, whose
evidence is on main, and chose to accept criteria 4 to 7 once #486 and #487
merge. #486 and #487 merged on 2026-10-15 KST, so criteria 4 to 6 are accepted as
the owner chose. Criterion 7 stays pending: the second readiness review
returned NOT READY at the time. The per-unit reviews it found missing ran later
(see the Evidence table), and the final readiness review below governs
criterion 7.

On 2026-10-15 the owner was asked through AskUserQuestion and chose to accept
criterion 7 once #499 merged. #499 merged the same day, so criterion 7 is
accepted. The evidence is the fifth IaC re-review (READY) and the security
re-review (APPROVE with notes). The Low notes applied after them in
`5b7b8b32f` were rehearsed but not independently reviewed. Accepting the
criterion does not approve the window itself: the window still needs owner
approval, `P01_APPROVED_COMMIT`, a SEC01 stable lookup within 7 days of the
window start, and the W0 runtime checks.

The owner scheduled the window (AskUserQuestion, 2026-10-15) for Thursday
2026-10-22, 14:00 to 16:00 KST. This avoids the 03:30 backup, so H3 is not
needed.

What the schedule implies:

- The 2026-10-14 SEC01 lookup does not cover a start on 2026-10-22, so a fresh
  lookup must run on or after 2026-10-15 14:00 KST. The plan is 2026-10-21.
- The Traefik and Prometheus acceptance expires on 2026-11-15, so it covers
  the window.
- `P01_APPROVED_COMMIT` is the default-branch commit at W0, after its CI passes
  and with no source change since `bf87a9b6a`. This record's own merge commit
  qualifies.
- Scheduling is not approval: the owner approves the window separately at W0.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
