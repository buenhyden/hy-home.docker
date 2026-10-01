---
title: "Offsite Backup Target"
version: "0.2.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "architecture"
artifact_id: "ADR-0041"
parent_ids:
- "AD-0004"
created: "2026-09-25"
---

# ADR-0041: Offsite Backup Target

## Context

Per POL-0021 control 1, the Restic and pgBackRest repositories are on a
different physical disk from the source. But all copies are on one host.

- `BACKUP_STATE_REPO_DIR` (system SSD): the pgBackRest repository
  `pgbackrest/` (`aes-256-cbc`, BKP-001) and the Restic repository
  `restic/` (BKP-002) for data-disk state.
- `BACKUP_HOST_REPO_DIR` (data disk): the Restic repository holding
  `secrets/` and `.env` (BKP-002). This repository also holds BKP-001 and
  SEC-003 (the OpenBao unseal share file).

So host theft, fire, flooding, a power incident, simultaneous damage to both
disks, or ransomware that encrypts the whole host **loses every copy**. Only
the offline copies of BKP-001/BKP-002 (control 3) remain, and no recoverable
data is left.

Measurements (from the `repository sizes` line of the `hyhome-backup.service`
journal, no secrets):

| Date (KST) | state repository (pgBackRest + Restic) | host repository |
| --- | --- | --- |
| 2026-09-23 | 429 MiB | 1 MiB |
| 2026-09-24 | 581 MiB | 1 MiB |
| 2026-09-25 | 777 MiB | 1 MiB |

The state repository is bounded by the `BACKUP_STATE_MAX_GIB` budget of 5 GiB
(control 2). The costs below are therefore estimated against the **5 GiB
cap**. pgBackRest self-shrinks via `repo1-retention-full=2`, but Restic keeps
growing until an approved `forget-prune`.

## Decision Drivers

- Recovery must be possible even if the host is lost (the gap in POL-0021
  control 1).
- Restic already encrypts client-side, so a remote site receives only
  ciphertext. The pgBackRest repository is also encrypted with BKP-001.
- The recovery path must not depend on OpenBao. Losing the host also loses
  OpenBao.
- Keep new credentials to a minimum and do not grow the offline-storage
  target.
- Operational burden must stay at a personal home lab level (unattended
  timer, minimal manual procedure).
- The remote copy must not be deletable by ransomware or mistake.

## Options Considered

Costs are **order-of-magnitude estimates** based on public list prices and
are reconfirmed at decision time.

| Option | Monthly cost (<=5 GiB) | Host-loss coverage | Recovery time (5 GiB) | Operational burden | New secrets |
| --- | --- | --- | --- | --- | --- |
| (a) Second local disk / USB rotation | One-time disk purchase | Weak against fire/theft since it is the same location. Partial coverage if the rotated disk is kept off-premises | Minutes (local) | Manual rotation, easy to forget | None |
| (b) S3-compatible cloud | Nearly 0 to about $7 | Covered | Within tens of minutes (line speed) | Unattended timer | 1-2 remote access keys |
| (c) SFTP / rest-server on another device | Cost of the peer device | Covered (if a different location) | Depends on peer's line | Requires maintaining and trusting the peer device | SSH key or rest-server account |
| (d) Defer | 0 | None | Not applicable | None | None |

### (a) Second local disk or USB rotation

- **Method**: Create a repository on an external disk with
  `restic init --from-repo … --copy-chunker-params` and replicate the two
  repositories with `restic copy`. For pgBackRest, either copy the directory
  or place a second repository via `repo2-path`.
- **Good**: Lowest cost and fastest recovery. No network or external account
  needed.
- **Bad**: The connected disk is exposed to the same host incident
  (ransomware, power). Fire and theft are not covered unless the rotated disk
  is kept in a different location. Manual rotation easily stops happening.
- **Encryption**: Restic and pgBackRest encryption applies unchanged.
- **Repository changes**: Optional copy step and mount-presence check in the
  orchestrator, plus a POL-0021 row.

### (b) S3-compatible cloud (Restic's default backend)

The Restic version pinned by Compose supports `s3:`, `b2:`, `azure:`, `gs:`,
`rest:`, and `sftp:` backends by default. pgBackRest can place a second
repository via `repo2-type=s3` (and `gcs`, `azure`, `sftp`).

| Provider | Storage unit price (list) | Monthly cost for 5 GiB | Caveats |
| --- | --- | --- | --- |
| Backblaze B2 | About $6-7/TB-month | About $0.03 | Egress free up to 3x stored volume. Bucket-scoped application key and Object Lock support |
| Cloudflare R2 | About $0.015/GB-month, 10 GB free | $0 (free tier) | Egress free. Bucket-scoped API token |
| Wasabi | About $7/TB-month, 1 TB minimum billed | About $7 | 90-day minimum retention billing. Expensive for a small repository |
| AWS S3 Glacier Instant Retrieval | About $0.004/GB-month + about $0.03/GB retrieval | About $0.02 + retrieval fee on recovery | 90-day minimum billing. Restic `check`/`prune` reads index and packs, accumulating retrieval fees. Little benefit for a small repository |

- **Method**: Create a remote Restic repository with the state repository's
  chunker settings, and after a local backup and `check`, upload state and
  host snapshots with `restic copy`. pgBackRest either sends WAL and backups
  directly with `repo2-type=s3`, or uploads the pgBackRest repository
  directory into the remote Restic. The former keeps WAL-level RPO remotely
  too, but needs remote keys and egress on the `mng-pg` container. The latter
  gives day-level RPO and needs care with files being written during copy.
- **Good**: Location is separated and it runs unattended. Cost is near zero.
  Since Restic already encrypts, the provider sees only ciphertext.
- **Bad**: Creates a new remote credential and egress path (currently
  `restic` uses `network_mode: none`). The provider account itself becomes a
  new single point of failure. If a key with delete permission leaks, the
  remote copy could also be wiped, so Object Lock or separated delete
  permission is needed.
- **Encryption**: Restic (BKP-002 or a new repository password) and
  pgBackRest (BKP-001) client-side encryption. If the remote repository
  receives the host repository, all of `secrets/` ends up external, protected
  only by BKP-002. Offline storage of BKP-002 becomes that much more
  important.
- **Credential storage**: A new file under `secrets/backup/` and a
  `SENSITIVE_ENV_VARS` row (for example BKP-003 for the remote repository key
  ID/application key, BKP-004 if pgBackRest `repo2` is used). Inject only as
  0600, Docker Secret, and keep an offline copy. **Do not store in OpenBao**:
  if recovery after host loss needs OpenBao, recovery falls into a circular
  dependency.
- **Recovery time**: About 7 minutes to receive 5 GiB at 100 Mbps, plus
  Restic restore and pgBackRest restore time. B2 and R2 have effectively no
  egress cost at this scale.
- **Repository changes**: A separate `restic-offsite` job with egress (or a
  copy-only network), a copy step and failure exit code in the orchestrator,
  two new secrets and registry rows, `gen-secrets.sh` metadata, a POL-0021
  control 1 edit, initialization/recovery procedure in RUN-0021, and
  `BackupContractTests` expansion.

### (c) SFTP or rest-server to another device (family, friend, NAS)

- **Method**: Run `rest-server --append-only` or an SFTP account on a device
  in another location and send with `restic copy`. The connection needs a
  private path such as WireGuard.
- **Good**: No monthly fee. An `--append-only` rest-server prevents this host
  from deleting remote snapshots.
- **Bad**: Depends on the peer device's availability, disk, updates, and
  trust. The peer may need to help during recovery. Requires newly operating
  a network path and open port or VPN.
- **Encryption**: Restic client-side encryption, so the peer cannot read the
  content.
- **Credential storage**: Keep the SSH key or rest-server account in
  `secrets/backup/` and a registry row, with an offline copy.
- **Repository changes**: The same job and copy step as (b), plus VPN or SSH
  configuration.

### (d) Defer

- **Good**: Nothing to do right now.
- **Bad**: The state where host loss loses everything remains. SPEC-0182
  criterion 10 requires an owner and a trigger or date when deferring.

## Decision

Use **(b) S3-compatible cloud, Cloudflare R2** (owner decision, 2026-09-25).

- Place a single remote Restic repository in an R2 bucket, and upload state
  and host snapshots with `restic copy` after the local backup and `check`.
  The 5 GiB cap fits inside the free tier (10 GB) and free egress.
- pgBackRest starts by loading its repository directory into the remote
  Restic (day-level remote RPO, no egress or keys on `mng-pg`). If WAL-level
  RPO becomes necessary remotely too, a new decision opens to move to
  `repo2-type=s3`.
- Enable lock (retention rules) on the bucket, and scope this host's token to
  that bucket only. Remote `forget-prune` is kept as a separate manual
  procedure.
- Store R2 credentials only as a file under `secrets/backup/` (0600, injected
  as a Docker Secret) plus an offline copy; do not store them in OpenBao.

## Consequences

- **If (b) is chosen**:
  - POL-0021 control 1 changes from "offsite recovery is not provided" to a
    sentence recording the remote copy and its RPO.
  - One backup job gets external egress for the first time. Only that job is
    attached to the egress network.
  - Offline storage and rotation procedures are needed for the new secrets
    (BKP-003, and BKP-004 if applicable).
  - The remote copy carries all of `secrets/` and SEC-003, encrypted with
    BKP-002. If BKP-002 leaks, remote account access alone exposes every
    secret.
  - Add the host-loss recovery procedure (new host, offline keys, remote
    restore order) to RUN-0021.
- **If (a) or (c) is chosen**: Cost is low, but manual rotation or peer device
  maintenance becomes an operational burden.
- **If (d) is chosen**: The risk is accepted as-is, and this ADR reopens when
  a trigger arrives.

## Traceability

- Parent: [AD-0004 Data Architecture](../descriptions/0004-data-architecture.md)
- Spec: [SPEC-0182](../../03.specs/0182-home-residual-backlog/spec.md) criterion 10, Plan W10,
  [Task 0003](../../03.specs/0182-home-residual-backlog/tasks/tsk-0003-recovery-and-auth-acceptance.md)
- Policy: [POL-0021](../../05.operations/policies/0021-backup-and-restore.md)
  control 1–3; Runbook: [RUN-0021](../../05.operations/runbooks/0021-backup-and-restore.md)
- Runtime sources: [Restic Compose](https://github.com/buenhyden/hy-home.docker/blob/c26bc8026254dffd7d51fc45b4081a1f80f855f2/infra/09-tooling/restic/docker-compose.yml),
  [orchestrator](https://github.com/buenhyden/hy-home.docker/blob/c26bc8026254dffd7d51fc45b4081a1f80f855f2/infra/09-tooling/restic/bin/hyhome-backup.sh),
  [pgBackRest configuration](../../../infra/04-data/mng-db/pg/backup/pgbackrest.conf)
- Size basis: the `repository sizes` line of `journalctl -u hyhome-backup.service`
  (2026-09-23 to 25).

## Follow-up

- Implement the R2 offsite copy and record in Task 0003 the evidence that the
  owner prepared the bucket, token, and first `restic init`.
- If [ADR-0042](0042-openbao-unseal-method.md) chooses a cloud KMS, decide
  together whether to use the same provider account.

### Official references

- [Restic repository backends](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html)
  and [copying snapshots between repositories](https://restic.readthedocs.io/en/stable/045_working_with_repos.html)
- [pgBackRest multiple repositories and S3](https://pgbackrest.org/user-guide.html)
- [rest-server append-only mode](https://github.com/restic/rest-server)
