---
title: "OpenBao Maintenance Window Readiness Task"
version: "0.1.16"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-15"
layer: "specs"
artifact_id: "SPEC-0243-TSK-0001"
parent_ids:
- "SPEC-0243-PLAN-0001"
created: "2026-10-14"
---

# OpenBao Maintenance Window Readiness Task

## Objective

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
| Restore input re-review | 7 | W4 | Independent `iac-reviewer` re-review: PASS with notes, notes applied; 66 tests OK with all native rehearsals in a umask 022 clone; manifest pin test OK | `a4dbc0f9e` | PASS | W4 W3a Input Producers | - |
| Second readiness review | 7 | W1 | Independent `iac-reviewer` readiness review of the whole window: NOT READY (SEC01 gate text, timing, W6 timing, W3a status, root custody, W5 token step) | `a4dbc0f9e` branch | FAIL | Second Readiness Review and Window Text | - |
| Window security review | 7 | W1 | Independent `security-auditor` review of W1, W6 and the window text: REJECT (un-revoked root on disk, old token in argv, zsh prompt) | Branch `claude/window-text-r2` | FAIL | Second Readiness Review and Window Text | - |
| Window IaC review | 7 | W2 | Independent `iac-reviewer` review of W2, W5 and the window text: NOT READY (Agent input chown fails natively, timing, stop path, W3a secret input) | Branch `claude/window-text-r2` | FAIL | Second Readiness Review and Window Text | - |
| Host logrotate install | 6 | W6 | Read-only: timer drop-in loaded with the next run within an hour; `/etc/logrotate.d/openbao` root 0644, SHA-256 equal to the tracked rule | Host 2026-10-15 | PASS | Owner Host Preparation | - |
| Window host prerequisites | 1 | W1 | Read-only: Linger yes, Docker debug false; owner-reported: old operator token expired (lookup denied) and shredded; TLS preflight run by the owner, output not observed here | Host 2026-10-15 | PASS | Owner Host Preparation | - |
| Agent input fix | 2 | W2 | Native chown with the restore's flags: exit 1 without `DAC_READ_SEARCH`, 0 with it; new assertions RED on the earlier code, GREEN after; 47 OK and native preflight 17 OK in a umask 022 clone | `2e3683771` (#492) | PASS | Restore Agent Fix and Full Rehearsal | - |
| Full restore rehearsal | 2 | W2 | Native `orchestrate()` and `perform()` on synthetic resources, old `11fd73a2` restore and owned `46bf9b5c` candidate and Agent: ledger `accepted`, no attempt containers left; four defects fixed with RED then GREEN unit assertions; restore-input suite 18 OK with `HYHOME_OPENBAO_REHEARSAL=1` in a umask 022 clone | `564f4049c` | PASS | Restore Agent Fix and Full Rehearsal | - |
| Restore fix IaC re-review | 7 | W2 | Independent `iac-reviewer` re-review of #492 and #495: FAIL (umask 077 leaves `tls/` unreadable to the server; cleanup misses the pre-token gap and depends on the shared runner) | `bc552bf9b` | FAIL | Restore Agent Fix and Full Rehearsal | - |
| Restore fix security re-review | 7 | W2 | Independent `security-auditor` re-review of #492 and #495: APPROVE with notes (Medium: rendered values can stay in `/dev/shm` on failure paths) | `bc552bf9b` | PASS | Restore Agent Fix and Full Rehearsal | - |
| Restore review fixes | 2, 7 | W2 | 11 new or changed unit assertions RED on the earlier module (`tls/` 0700 under umask 077), restore suite 32 OK after in a umask 022 clone; native `perform()` with `orchestrate()` under umask 077: the earlier module ends INDETERMINATE, the fixed module ends `accepted` with no attempt container, volume, network or `/dev/shm` directory left; native suite 2 OK | `6fd36be4a` | PASS | Restore Agent Fix and Full Rehearsal | Restore fix IaC re-review |
| Restore fix second IaC re-review | 7 | W2 | Independent `iac-reviewer` re-review of #498: PASS with notes; H1, M1, M2, L1, L3 closed; W2 READY with notes (failure-path time budget, interrupted-run checks) | `efc4a68bb` | PASS | Restore Agent Fix and Full Rehearsal | - |
| Restore fix second security re-review | 7 | W2 | Independent `security-auditor` re-review of #498: APPROVE with notes; F1 and F2 closed; notes: unverified Agent stop, 0777 mount points, Agent AppRole token not revoked | `efc4a68bb` | PASS | Restore Agent Fix and Full Rehearsal | - |
| Restore re-review notes | 2 | W2 | Reclaim confirms the Agent is not running, mount points 0755, Agent AppRole login leases revoked on the candidate, preflight refuses an operator GID other than 1000; new assertions RED on the earlier module (4); 70 unit OK and native restore-input suite 18 OK in a umask 022 clone | `c9aa69b89` | PASS | Restore Agent Fix and Full Rehearsal | - |
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
| 7 | pending | - | - |

## Review and Completion

On 2026-10-14 the owner (AskUserQuestion) accepted criteria 1 to 3, whose
evidence is on main, and chose to accept criteria 4 to 7 once #486 and #487
merge. #486 and #487 merged on 2026-10-15 KST, so criteria 4 to 6 are accepted as
the owner chose. Criterion 7 stays pending: the second readiness review
returned NOT READY, and per-unit reviews it found missing (security for W1
and W6, IaC for W2 and W5) are still to run. The window stays NOT READY.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
