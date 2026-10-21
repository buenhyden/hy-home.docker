---
title: "Observability CA Execution Task"
version: "0.1.22"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-21"
layer: "specs"
artifact_id: "SPEC-0245-TSK-0001"
parent_ids:
- "SPEC-0245-PLAN-0001"
created: "2026-10-16"
---

# Observability CA Execution Task

## Overview

### Objective

Complete service-specific backup and isolated-recovery rehearsals for
Prometheus and Gatus before either CA recreation, then recreate Prometheus
before Gatus while preserving production data boundaries.

## Inputs and Authorization

- **Request:** on 2026-10-16 the owner authorized the current host's
  Prometheus and Gatus backup/restore validation followed by their bounded CA
  application and recreation.
- **Authorization boundary:** this Task covers only the two named services,
  one at a time, in Plan order. It excludes secret or raw-data capture,
  OpenBao operations, a stack-wide restart, an unreviewed image pull, a
  Prometheus upgrade, manual data manipulation, volume deletion, and
  production-data restoration or replacement.
- **Baseline:** `main` `89eb43f683a11587cf4f125be534ae720c20a55c`.
- **Known starting observation:** Prometheus was observed on its 3.14 rollback
  image and both named services lacked the required CA mount at runtime. Gatus
  requires a no-network/no-pull minimal delta image with `FROM` its exact
  current running immutable base and `COPY` of only the reviewed tracked
  CA-aware entrypoint, with its binary unchanged, before recreation; a
  same-image recreation is not accepted as CA evidence.
- **Planned protected artifacts:** the reviewed backup/isolated-restore packet
  selects `/home/hyunyoun/storage/backups/r13-observability-ca-20261016-01`.
  Workspace artifacts require mode 0700 and isolated-restore tar siblings mode
  0400. The path shares device 2064 with production data, so it is a
  pre-recreate recovery gate only, not a disk-failure disaster-recovery claim.

## Work Log

### Initial State

The approved Spec and Plan define the execution order. No backup, isolated
restore, image build, CA application, recreation, or operational review has
run under this Task.

### Spec Approval

The direct 2026-10-16 user authorization approved the bounded SPEC-0245
contract before this Task was created.

### Plan Approval

The same direct authorization approved SPEC-0245-PLAN-0001's bounded work and
verification sequence before this Task was created.

### Ready Transition

On 2026-10-16, W1 bound the exact, value-free backup phase contract and its
two guard helpers to the selected host-local protected artifact path. The
contract specifies the two recovery gates before either CA recreation, the
Prometheus-then-Gatus recreation order, same-device non-DR limitation, and
the mode-0700 workspace/mode-0400 tar-sibling controls. This makes the Task
`ready` to begin a reviewed W2 or W3 gate; it is not a backup, restore, image
build, service recreation, or operational-review result.

The Task transitions to `in-progress` only when an approved W2 or W3 recovery
gate actually starts. The reviewed recovery packet must still pass its
independent IaC/security review before the relevant operation proceeds.

### In-progress Transition

On 2026-10-16, independent IaC and security reviews returned READY for the
backup phase only, bound to the final W1 packet. The operator was released to
hash-recheck that packet and start the approved W2/W3 recovery gate. This
transition records the release and start boundary only; it does not claim any
backup, restore, image build, CA application, recreation, or health outcome.

### Backup Capture Receipts

The approved backup phase captured both production service archives on
2026-10-16. These are capture receipts only: their independent integrity
rehashes and isolated restores have not run, and neither receipt authorizes a
CA change.

- **Prometheus (W2):** receipt `e325f552…`; archive SHA-256 prefix
  `2bb0edc…`, 6,860,012,544 bytes. The service stop/restart timestamps were
  `23:31:10Z` and `23:42:33Z` (reported locally as 08:31–08:42 KST). The
  post-capture check found the original container ID and image unchanged and
  the service healthy; no helper remained.
- **Gatus (W3):** receipt `e325f552…`; archive SHA-256 prefix `01f0f92d…`,
  4,541,440 bytes. The service stop/restart timestamps were `23:46:05Z` and
  `23:46:25Z` (reported locally as 08:46 KST). The post-capture check found
  the original container ID and image unchanged and the service healthy; no
  helper remained.

The receipts are durable task evidence for the completed captures. A separate
independent rehash and each isolated restore remain required recovery gates.

### Structural Validation Receipt

Before the backup-capture receipt commit, the complete active-document
metadata selection passed at source snapshot `78684ac`. This validates the
seven selected document records and their lifecycle bindings at that snapshot;
it does not validate the later receipt edit, the pending independent rehashes
or restores, or any runtime CA result.

### Isolated Restore Plan and Release Receipts

The initial isolated-mode `restore-01` packet was prepared against workspace
identity `174588272`. Its frozen contract SHA-256 was
`dd027cad5a53e84eeb4ef091a059e9ba146eee0fe9a9a7b8f3fd721fdd81d13f` and
its restore script SHA-256 was
`8d49b6aa3ff2f7cb16d72a92efcaeec4d180b730b108049f40bede1d702d68f1`.
All restore helpers and their tests passed the pre-execution packet check.
Before GO or any restore execution, the packet was superseded because the
target-inode row was incomplete. It remains a non-executed historical plan
receipt.

The subsequent `1b930069…`/`965a751a…` candidate was also superseded before
GO or execution after immutable-tree identity reblessing. The final release
candidate binds contract SHA-256
`e65e379c168749d2a4f106cdaa1af5a482831869dcae53d8811fb0e52a81e07b` and
restore script SHA-256
`10391132b53bf001dc284b2a3ef17c299a24fc4d267ecaf1fe95024ec89beffe`; helpers
are unchanged. Independent IaC, security, and operator reviews are READY, and
the root released the first restore phase only.

The released scope is `restore-01` for two new isolated clones with no
production writes. Before either clone starts, the operator must recompute the
full source hash once and recheck the same-inode metadata. The production
target ledger remains unused. A quarantined execution-evidence leaf may retain
only sanitized clone identities, source/hash and inode checks, and bounded
restore health/data-shape results; it excludes raw payloads, secrets, and
production-target state. No isolated restore has started or completed. These
plan and release receipts change neither the required integrity rehashes nor
the pending acceptance of criteria 2 and 3.

### Isolated Restore Attempt 01 Failure

The released `restore-01` reached its synthetic-ownership probe and failed
closed. Its immutable sanitized failure receipt SHA-256 is
`77c2fe7ec8ee76d5cc12fed60ca944fc05123723fba37c73696772a20f56f236`.
Cleanup passed; no labeled isolated container remained, no archive was
extracted, and the original containers retained their exact identities,
healthy state, and restart count 0.

Read-only confirmation found that the exact BusyBox tar 1.37 lacks
`--same-owner` but supports `--numeric-owner`. A prior quote/unbound-variable
launcher diagnostic occurred before script entry and created no restore state;
it is not classified as this attempt failure. A new reviewed sibling attempt
is required before any retry. CA work remains blocked.

### Isolated Restore Attempt 02 Release

`restore-02` is a new, unused sibling attempt under the same approved parent;
it preserves Attempt 01's immutable failure receipt. Its final v2 contract
SHA-256 is
`6aea3453f2fab65d93a885759fa8a9358eceab3d433636aec61f443ed95fd1e5`, restore
script SHA-256 is
`8203382c97f0b6b8816cca7bb1ac0799b1472bdad6506128b5638f143de90cf3`, and
test SHA-256 is
`18fcb193a3d29a491b251bc93b0a50c13c878398f4c1e1e2f7e03dbdc96c16b3`.
The helpers are unchanged.

Before archive handling, the packet performs its embedded synthetic-ownership
proof with BusyBox's supported numeric-owner default and omits the unsupported
flag. All nine create-CID exactness, uncertainty-file, truthful-`UNKNOWN`, and
cleanup guards are bound to the v2 packet. Independent IaC and security
reviews are READY. Root GO remains conditional on operator READY, this Task
receipt, and fresh hash rechecks. No restore-02 action has run, and CA work
remains blocked until a successful recovery gate.

### Isolated Restore Attempt 02 Failure

`restore-02` failed closed at its synthetic-owner stage before any archive
handling. Its immutable sanitized failure receipt SHA-256 is
`977651535b5659d29c039ee5088d74b96319d6cabf53a2a53779bd3778158ee1`.
The Docker CID file contained the standard 64-hex form with no trailing
newline. Bash `read` populated the ID but returned 1 at EOF, and the guard
incorrectly classified it as `UNKNOWN_CREATE`.

Both independent reviewers accepted this as a truthful failure. It is a guard
source defect, not backup corruption: no archive was extracted, no helper
remained, and the original services remained healthy. No CA or image-build
work started. A newly reviewed `restore-03` sibling is required; Attempt 01
and Attempt 02 receipts remain preserved.

### Isolated Restore Attempt 03 Release

`restore-03` is a new, unused sibling that preserves both prior failure
receipts. Its final v3 contract SHA-256 is
`322414d13c3655155b95cd2ad84a25b0307fdf085283e3ee9830d3f90cf213a4`, restore
script SHA-256 is
`174d5bf307ca944ac5b8ea7ae15c4595dc6edf18b76580e66830963a9662a438`, and
test SHA-256 is
`8153f9003713ab9b36db669dc828179c144cbb88961b43a557f2e2486184bf0a`.
Helpers are unchanged.

The v3 packet confirms zero Attempt 02 labels and the absence of nine old
names, then handles the real 64-hex/no-line-feed CID form. Its related
regressions passed. Independent IaC and security reviews are READY. Root GO
remains conditional on operator READY, this Task receipt, and immediate hash
and target checks. No restore-03 action has run, and CA work remains blocked
until the recovery gate succeeds.

### Isolated Restore Attempt 03 Failure

`restore-03` completed the full Prometheus archive extraction, then failed
closed at `prometheus-offline-preflight` with exit 1. Its immutable sanitized
receipt SHA-256 is
`ee9900e4df12a952ee8956d921c7f3c80ba496e943158823e4720786c65a67aa`, mode
0400, inode `174588497`. Cleanup passed; scratch artifacts are quarantined;
the original services remain healthy with restart count 0. No CA, image-build,
or retry action ran.

The diagnosis remains open. This receipt does not infer archive corruption or
accept either recovery gate.

### Prometheus image decision and runtime state — 2026-10-21

The owner chose to keep Prometheus on the installed image
(`prom/prometheus:v3.15.0`, digest `efd719c9`) instead of the 3.14 rollback
image this package was written for; the Spec and Plan now name v3.15.0.

Read-only observation on 2026-10-21: the SEC01 observability rollout
(SPEC-0204 TSK-0009, 2026-10-20 10:30–10:42 +09:00) stopped Prometheus, took a
cold copy `prometheus-data.tar` (6,697,427,456 bytes, under
`/home/hyunyoun/storage/backups/obs-images-20261020/`) and recreated it on
v3.15.0. Because Compose declares the bind, the running container now mounts
`/etc/prometheus/openbao-ca.pem` read-only. That recreation ran under the SEC01
approval, not under W2: no isolated restore of a Prometheus backup has passed
(restore-01 to restore-03 failed above and stay preserved). Gatus
(`hy/gatus:local`, started 2026-10-19) mounts only the home root CA, not the
OpenBao CA.

Consequences for this Task: criterion 2's order (backup and isolated restore
before recreation) cannot be met for the recreation that already happened, so
it is recorded as a deviation, not a PASS. What remains testable is an
isolated restore of the 10-20 cold copy on v3.15.0, and the Prometheus OpenBao
scrape over that CA once OpenBao serves TLS after the SPEC-0243 window. Gatus
still needs its W3 backup, isolated restore and the CA-aware delta image.
No restore, recreation or CA action ran here.

### Tracked isolated restore procedure — 2026-10-21

The restore-01 to restore-03 packet (contract, script and test) is not in the
repository or in the attempt workspace, and restore-03's preflight failure is
still undiagnosed, so the owner chose a new tracked procedure ("새 절차 작성 후
실행"). `scripts/operations/prometheus-isolated-restore.py` takes a stopped-volume
tar and its SHA-256, refuses a hash mismatch or an existing work directory
before any Docker call, extracts into a new 0700 directory as the invoking
user, and runs the Compose-pinned v3.15.0 image with `--network=none`,
`--pull=never`, `--cap-drop=ALL`, no-new-privileges, 2 GiB and one CPU, a
configuration with no scrape targets and a retention long enough that no
restored block is deleted. It records the seconds to `/-/ready` and `count(up)`
one hour and seven days before the newest block, always removes its container
and removes the scratch directory unless `--keep`. Six unit tests cover the
image pin, both refusals, the isolation flags, the query times, an empty query
and a never-ready server; RUN-0045 names the command and the script is
registered in the manifest and the CI contract.

This replaces the lost packet for W2's restore step; it does not check rule
health or Alertmanager delivery. The planned input is the 2026-10-20 cold copy
(SHA-256 `c9cb29e5…`). The run waits for independent review and for the
SPEC-0243 window to finish, and its `ready_seconds` becomes the first measured
RTO input for the observability tier (SPEC-0218 TSK-0002). Nothing ran yet.

### Gatus image identity and entrypoint — 2026-10-21

Read-only observation: the running Gatus container and `hy/gatus:local` are the
same image, `sha256:c52ad951…` (built 2026-09-19), so RUN-0085's window
condition for recreating Gatus holds. That image's
`/usr/local/bin/gatus-oidc-entrypoint.sh` has SHA-256 `dc6b66e2…` and no
`OPENBAO_CA` handling, while the tracked
`infra/06-observability/gatus/docker-entrypoint.sh` (last changed 2026-10-10)
has SHA-256 `4d4264b5…`. A same-image recreation in the window would add the CA
mount without an entrypoint that reads it, so it would not apply the CA. CA
application still needs W3 here: a consistent Gatus backup and isolated restore,
then a no-network delta image `FROM` `c52ad951` that copies only the tracked
entrypoint, then recreation. The base identity above is now recorded. Nothing
was built or recreated.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0245 | draft | approved | #spec-approval |
| SPEC-0245-PLAN-0001 | draft | approved | #plan-approval |
| SPEC-0245-TSK-0001 | draft | ready | #ready-transition |
| SPEC-0245-TSK-0001 | ready | in-progress | #in-progress-transition |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Initial operational execution state | 1 | W1 | No preflight, backup, isolated restore, image build, recreation, review, or selected gate had run when this Task was created | Initial record on `89eb43f683a11587cf4f125be534ae720c20a55c` | NOT_RUN | Initial State | optional | - |
| Ready backup packet binding | 1 | W1 | SHA-256 binding of the final frozen backup phase contract and guard helpers | Contract `d70944844623e5733a7e6dff4a5e999bf29078a5f5c0bd91fd11e48950db0d88`; phase script `1ce35b3a0e4759f4b37b8c6d0f86d48d41c8452dc92d0f32179835561cf7475a`; archive guard `a85ab831c3369f1d04b5dc6abd14fa83ae5bb4ced495f594d85955474c42b385` | PASS | Ready Transition | required | - |
| Backup phase independent reviews | 7 | W7 | Independent IaC and security reviews of the final backup phase packet | READY limited to backup phase; no execution outcome | PASS | In-progress Transition | required | - |
| Prometheus backup capture | 2 | W2 | Reviewed Prometheus backup capture | Receipt `e325f552…`; archive SHA-256 prefix `2bb0edc…`; 6,860,012,544 bytes; stop `23:31:10Z`, restart `23:42:33Z`; original ID/image and health retained | PASS | Backup Capture Receipts | required | - |
| Gatus backup capture | 3 | W3 | Reviewed Gatus backup capture | Receipt `e325f552…`; archive SHA-256 prefix `01f0f92d…`; 4,541,440 bytes; stop `23:46:05Z`, restart `23:46:25Z`; original ID/image and health retained | PASS | Backup Capture Receipts | required | - |
| Prometheus backup integrity rehash | 2 | W2 | Independent rehash of the captured Prometheus archive | Not yet run after capture | NOT_RUN | Backup Capture Receipts | required | - |
| Gatus backup integrity rehash | 3 | W3 | Independent rehash of the captured Gatus archive | Not yet run after capture | NOT_RUN | Backup Capture Receipts | required | - |
| Prometheus isolated restore | 2 | W2 | Isolated restoration and validation of the captured Prometheus archive | Not yet run | NOT_RUN | Backup Capture Receipts | required | - |
| Gatus isolated restore | 3 | W3 | Isolated restoration and validation of the captured Gatus archive | Not yet run | NOT_RUN | Backup Capture Receipts | required | - |
| Pre-capture document metadata validation | 7 | W7 | `rtk proxy python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 89eb43f683a11587cf4f125be534ae720c20a55c --changed-path docs/03.specs/0244-native-memory-controlled-verification/spec.md --changed-path docs/03.specs/0244-native-memory-controlled-verification/plan.md --changed-path docs/03.specs/0244-native-memory-controlled-verification/tasks/tsk-0001-native-memory-controlled-verification.md --changed-path docs/03.specs/0245-observability-ca-execution/spec.md --changed-path docs/03.specs/0245-observability-ca-execution/plan.md --changed-path docs/03.specs/0245-observability-ca-execution/tasks/tsk-0001-observability-ca-execution.md --changed-path docs/03.specs/README.md --changed-path docs/99.templates/registry.json` | Snapshot `78684ac`; exit 0; selected 7; violations 0; legacy exceptions 0; transition overrides 0; predates backup-capture receipt `23224aa` | PASS | Structural Validation Receipt | required | - |
| Initial Prometheus isolated restore plan binding | 2 | W2 | Bind the initial isolated-mode Prometheus restore packet to its frozen contract and script | `restore-01`; workspace identity `174588272`; contract `dd027cad5a53e84eeb4ef091a059e9ba146eee0fe9a9a7b8f3fd721fdd81d13f`; script `8d49b6aa3ff2f7cb16d72a92efcaeec4d180b730b108049f40bede1d702d68f1`; helpers/tests PASS; target-inode row gap; superseded before GO/execution | NOT_RUN | Isolated Restore Plan and Release Receipts | required | - |
| Initial Gatus isolated restore plan binding | 3 | W3 | Bind the initial isolated-mode Gatus restore packet to its frozen contract and script | `restore-01`; workspace identity `174588272`; contract `dd027cad5a53e84eeb4ef091a059e9ba146eee0fe9a9a7b8f3fd721fdd81d13f`; script `8d49b6aa3ff2f7cb16d72a92efcaeec4d180b730b108049f40bede1d702d68f1`; helpers/tests PASS; target-inode row gap; superseded before GO/execution | NOT_RUN | Isolated Restore Plan and Release Receipts | required | - |
| Intermediate Prometheus restore candidate | 2 | W2 | Record the reblessed candidate before the final immutable-tree release candidate | Contract prefix `1b930069…`; script prefix `965a751a…`; immutable-tree identity reblessing required; superseded before GO/execution | NOT_RUN | Isolated Restore Plan and Release Receipts | required | - |
| Intermediate Gatus restore candidate | 3 | W3 | Record the reblessed candidate before the final immutable-tree release candidate | Contract prefix `1b930069…`; script prefix `965a751a…`; immutable-tree identity reblessing required; superseded before GO/execution | NOT_RUN | Isolated Restore Plan and Release Receipts | required | - |
| Released Prometheus isolated restore plan | 2 | W2 | Independent READY reviews and root release for the first isolated Prometheus clone | Contract `e65e379c168749d2a4f106cdaa1af5a482831869dcae53d8811fb0e52a81e07b`; script `10391132b53bf001dc284b2a3ef17c299a24fc4d267ecaf1fe95024ec89beffe`; helpers unchanged; IaC/security/operator READY; full source hash and same-inode metadata recheck required before execution | PASS | Isolated Restore Plan and Release Receipts | required | - |
| Released Gatus isolated restore plan | 3 | W3 | Independent READY reviews and root release for the first isolated Gatus clone | Contract `e65e379c168749d2a4f106cdaa1af5a482831869dcae53d8811fb0e52a81e07b`; script `10391132b53bf001dc284b2a3ef17c299a24fc4d267ecaf1fe95024ec89beffe`; helpers unchanged; IaC/security/operator READY; full source hash and same-inode metadata recheck required before execution | PASS | Isolated Restore Plan and Release Receipts | required | - |
| Isolated restore quarantine evidence leaf | 2 | W2 | Retain only sanitized execution evidence for the released isolated clones | No clone execution receipt yet; raw payloads, secrets, and production-target state excluded | NOT_RUN | Isolated Restore Plan and Release Receipts | required | - |
| Isolated restore attempt 01 | 2 | W2 | Released synthetic-ownership probe for the first isolated restore attempt | Failure receipt `77c2fe7ec8ee76d5cc12fed60ca944fc05123723fba37c73696772a20f56f236`; BusyBox tar 1.37 lacks `--same-owner` and supports `--numeric-owner`; no archive extraction; no labeled container; cleanup PASS; originals exact healthy with restart count 0 | FAIL | Isolated Restore Attempt 01 Failure | required | - |
| Isolated restore attempt 01 containment | 6 | W6 | Contain the failed isolated attempt and preserve production boundaries | Cleanup PASS; no isolated container or archive extraction; originals exact healthy with restart count 0; CA work blocked pending a new reviewed sibling | PASS | Isolated Restore Attempt 01 Failure | required | - |
| Released Prometheus isolated restore attempt 02 plan | 2 | W2 | Independent READY reviews and conditional root GO for the new Prometheus isolated-clone sibling | Contract `6aea3453f2fab65d93a885759fa8a9358eceab3d433636aec61f443ed95fd1e5`; script `8203382c97f0b6b8816cca7bb1ac0799b1472bdad6506128b5638f143de90cf3`; test `18fcb193a3d29a491b251bc93b0a50c13c878398f4c1e1e2f7e03dbdc96c16b3`; helpers unchanged; synthetic ownership before archives; numeric-owner default; nine guards bound; operator READY/hash rechecks pending | PASS | Isolated Restore Attempt 02 Release | required | - |
| Released Gatus isolated restore attempt 02 plan | 3 | W3 | Independent READY reviews and conditional root GO for the new Gatus isolated-clone sibling | Contract `6aea3453f2fab65d93a885759fa8a9358eceab3d433636aec61f443ed95fd1e5`; script `8203382c97f0b6b8816cca7bb1ac0799b1472bdad6506128b5638f143de90cf3`; test `18fcb193a3d29a491b251bc93b0a50c13c878398f4c1e1e2f7e03dbdc96c16b3`; helpers unchanged; synthetic ownership before archives; numeric-owner default; nine guards bound; operator READY/hash rechecks pending | PASS | Isolated Restore Attempt 02 Release | required | - |
| Isolated restore attempt 02 | 2 | W2 | Released synthetic-owner stage for the second isolated restore attempt | Failure receipt `977651535b5659d29c039ee5088d74b96319d6cabf53a2a53779bd3778158ee1`; 64-hex CID file without trailing newline; Bash `read` populated ID but returned 1 at EOF; guard classified `UNKNOWN_CREATE`; no archive extraction; no helper; originals healthy | FAIL | Isolated Restore Attempt 02 Failure | required | - |
| Isolated restore attempt 02 containment | 6 | W6 | Contain the failed isolated attempt and preserve production boundaries | Independent reviewers accepted the truthful guard-source failure; no archive extraction; no helper; originals healthy; no CA/image-build work; restore-03 review required | PASS | Isolated Restore Attempt 02 Failure | required | - |
| Released Prometheus isolated restore attempt 03 plan | 2 | W2 | Independent READY reviews and conditional root GO for the new Prometheus isolated-clone sibling | Contract `322414d13c3655155b95cd2ad84a25b0307fdf085283e3ee9830d3f90cf213a4`; script `174d5bf307ca944ac5b8ea7ae15c4595dc6edf18b76580e66830963a9662a438`; test `8153f9003713ab9b36db669dc828179c144cbb88961b43a557f2e2486184bf0a`; helpers unchanged; zero attempt-02 labels/nine old names absent; 64-hex/no-LF regression PASS; operator READY/hash and target checks pending | PASS | Isolated Restore Attempt 03 Release | required | - |
| Released Gatus isolated restore attempt 03 plan | 3 | W3 | Independent READY reviews and conditional root GO for the new Gatus isolated-clone sibling | Contract `322414d13c3655155b95cd2ad84a25b0307fdf085283e3ee9830d3f90cf213a4`; script `174d5bf307ca944ac5b8ea7ae15c4595dc6edf18b76580e66830963a9662a438`; test `8153f9003713ab9b36db669dc828179c144cbb88961b43a557f2e2486184bf0a`; helpers unchanged; zero attempt-02 labels/nine old names absent; 64-hex/no-LF regression PASS; operator READY/hash and target checks pending | PASS | Isolated Restore Attempt 03 Release | required | - |
| Isolated restore attempt 03 | 2 | W2 | Released Prometheus isolated restore through offline preflight | Receipt `ee9900e4df12a952ee8956d921c7f3c80ba496e943158823e4720786c65a67aa`; full Prometheus extraction completed; `prometheus-offline-preflight` exit 1; receipt mode 0400/inode `174588497`; cleanup PASS; scratch quarantined; originals healthy/restart 0; diagnosis open | FAIL | Isolated Restore Attempt 03 Failure | required | - |
| Isolated restore attempt 03 containment | 6 | W6 | Contain the failed Prometheus isolated restore and preserve production boundaries | Cleanup PASS; scratch quarantined; originals healthy/restart 0; no CA, image-build, or retry; no archive-corruption inference | PASS | Isolated Restore Attempt 03 Failure | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | Await W1 preflight | @buenhyden |
| 2 | pending | - | Backup captured; await independent rehash and isolated restore | @buenhyden |
| 3 | pending | - | Backup captured; await independent rehash and isolated restore | @buenhyden |
| 4 | pending | - | Await W3 build identity | @buenhyden |
| 5 | pending | - | Await W4 and W5 service results | @buenhyden |
| 6 | pending | - | Await W6 outcome if a gate fails | @buenhyden |
| 7 | pending | - | Await W7 reviews and checks | @buenhyden |

## Review and Completion

This Task has no accepted criterion. Completion requires the service-specific
execution evidence listed in SPEC-0245; a source-only check, image build, or
Compose render does not prove a production backup, isolated restore, or CA
application.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
