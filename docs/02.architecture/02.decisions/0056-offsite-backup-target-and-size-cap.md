---
title: "Offsite Backup Target with an Enforced Size Cap"
version: "1.1.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-25"
layer: "architecture"
artifact_id: "ADR-0056"
parent_ids:
- "AD-0004"
created: "2026-11-06"
---

# ADR-0056: Offsite Backup Target with an Enforced Size Cap

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-decision payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context

##### Problem and Drivers

Per POL-0021 control 1, the Restic and pgBackRest repositories sit on a
different physical disk from their source, but every copy is on one host. Host
theft, fire, flooding, a power incident, damage to both disks, or ransomware
that encrypts the host would lose every copy; only the offline copies of the
repository keys (BKP-001, BKP-002) would remain.

- `BACKUP_STATE_REPO_DIR` (system SSD) holds the pgBackRest repository
  (`aes-256-cbc`, BKP-001) and the Restic repository for data-disk state
  (BKP-002). Its local budget `BACKUP_STATE_MAX_GIB` is 8 GiB since 2026-10-10,
  when the owner raised it from 5 GiB and excluded the Loki and Tempo SeaweedFS
  collections (SPEC-0228).
- `BACKUP_HOST_REPO_DIR` (data disk) holds the Restic repository of `secrets/`
  and `.env` (BKP-002), which includes BKP-001 and the OpenBao unseal share
  file (SEC-003).

The offsite copy is implemented. `infra/09-platform-ops/restic/offsite.sh`
copies the snapshots of both local repositories into one Cloudflare R2 Restic
repository, and `restic-offsite` is the only backup job with egress, on its own
`restic_offsite_net`. On 2026-10-20 the owner ruled that the R2 repository must
never pass 10 GB. `offsite.sh` refuses every upload that could take the stored
bytes past 7.5 GB (`max_bytes=7500000000`, lowered from 9 GB by the owner on
2026-11-25), counts every stored file including
unused packs, fails closed when it cannot read the size, and allows the cap only
to be lowered (`BACKUP_OFFSITE_MAX_BYTES`). The bucket has a 30-day lock.

Drivers:

- Recovery must survive loss of the host.
- Restic and pgBackRest already encrypt client-side, so the remote site sees
  only ciphertext.
- Recovery must not depend on OpenBao, which is lost with the host.
- New credentials stay few, and the operation stays unattended.
- The remote copy must not be deletable by ransomware or mistake.
- The remote repository must never pass the owner's 10 GB ceiling.

###### Sources
<!-- core-payload-level:4 -->

Size evidence was the `repository sizes` line of the `hyhome-backup.service`
journal (429 to 777 MiB, 2026-09-23 to 25). No runtime state is claimed.

- [AD-0004 Data architecture](../01.descriptions/0004-data-architecture.md)
- [POL-0021 Backup and restore](../../05.operations/02.policies/10.platform-and-backup/0021-backup-and-restore.md)
- [RUN-0021 Backup and restore](../../05.operations/03.runbooks/10.platform-and-backup/0021-backup-and-restore.md)
- [Offsite entrypoint](../../../infra/09-platform-ops/restic/offsite.sh)
- [ADR-0042 OpenBao unseal method](0042-openbao-unseal-method.md)
- [Restic repositories](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html)

##### Decision Scope

This decision covers the offsite copy of the local Restic and pgBackRest
repositories: the remote target, its size cap, its credentials and its egress
boundary. WAL-level remote RPO through `repo2-type=s3` is left to a new
decision.

#### Options

##### Considered Options

Costs are order-of-magnitude list-price estimates from 2026-09-25.

| Option | Monthly cost | Host-loss coverage | Burden | New secrets |
| --- | --- | --- | --- | --- |
| (a) Second local disk or USB rotation | One-time disk | Weak unless the rotated disk is kept elsewhere | Manual rotation | None |
| (b) S3-compatible cloud | About $0 to $7 | Covered | Unattended timer | 1 to 2 keys |
| (c) SFTP or rest-server on a peer device | Peer device | Covered if remote | Peer maintenance and VPN | SSH key or account |
| (d) Defer | $0 | None | None | None |

##### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| (a) Second local disk or USB rotation | One-time disk cost and no new secrets. | Weak host-loss coverage unless the rotated disk is kept elsewhere, and rotation is manual. | Rejected; the attached disk shares host incidents, and rotation lapses. |
| (b) S3-compatible cloud | About $0 to $7 monthly, covers host loss, and runs on an unattended timer; Cloudflare R2 has a free tier up to 10 GB, free egress and a bucket-scoped token. | Needs 1 to 2 keys; uploads stop at the cap until the owner prunes, a leaked BKP-002 plus R2 access exposes every secret, and the R2 account is a new single point of failure. | Selected as Cloudflare R2; Backblaze B2 was viable, while Wasabi (1 TB minimum billing) and S3 Glacier Instant Retrieval (retrieval fees on `check` and `prune`) were rejected for a small repository. |
| (c) SFTP or rest-server on a peer device | Covers host loss if the peer is remote. | Needs a peer device, peer maintenance and VPN, and an SSH key or account. | Rejected; depends on a peer's availability, trust and a new network path. |
| (d) Defer | No cost, burden or new secrets. | No host-loss coverage. | Rejected; leaves total loss on host loss. |

- (a) rejected: the attached disk shares host incidents, and rotation lapses.
- (c) rejected: depends on a peer's availability, trust and a new network path.
- (d) rejected: leaves total loss on host loss.
- (b) selected, Cloudflare R2: free tier up to 10 GB, free egress, a
  bucket-scoped token. Backblaze B2 was viable; Wasabi (1 TB minimum billing)
  and S3 Glacier Instant Retrieval (retrieval fees on `check` and `prune`)
  were rejected for a small repository.
- Trade-off: when the cap is reached, uploads stop until the owner prunes; the
  remote copy then ages.
- Trade-off: the remote copy carries all of `secrets/` and SEC-003 under
  BKP-002; a leaked BKP-002 plus R2 access exposes every secret, so BKP-002's
  offline storage matters more.
- Trade-off: the R2 account is a new single point of failure for the offsite
  copy.

#### Decision

##### Chosen Option

1. One remote Restic repository in a Cloudflare R2 bucket receives the state
   and host snapshots by `restic copy` after the local backup and `check`.
2. pgBackRest reaches the remote copy through its repository directory in the
   state set (day-level remote RPO). WAL-level remote RPO through
   `repo2-type=s3` needs a new decision.
3. The R2 repository never passes 10 GB. Every upload that could take the
   stored bytes past 7.5 GB is refused; the projection adds 5% for pack
   headers, index files and estimate error. The cap may be lowered, never
   raised, without a new decision. The owner lowered it from 9 GB to 7.5 GB on
   2026-11-25: space is reclaimed by removing unused packs and, when that is not
   enough, by an owner-approved trim of the oldest snapshots on both sides.
4. The bucket keeps a 30-day lock, and the host token is scoped to that bucket.
   The daily run never deletes; remote `forget-prune` is a separate,
   owner-run monthly procedure, `prune` is the owner-run removal of packs
   no snapshot uses, and `trim` the owner-run removal of snapshots older than
   an approved date, run on the local repositories with the same date so the
   next copy does not upload them again (RUN-0021 8.5). Snapshot times are not upload times, so
   either can meet objects still under the lock.
5. R2 credentials live only as files under `secrets/backup/` (0600, injected
   as Docker Secrets) plus an offline copy; they are never stored in OpenBao.
6. Only `restic-offsite` has egress, on `restic_offsite_net`.

##### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. The owner ruled the 10 GB
ceiling on 2026-10-20; no separate approval record is linked. Effective from
2026-11-06.

###### Supersession
<!-- core-payload-level:4 -->

This record replaces ADR-0041, deleted in the same change (ADR-0051); ADR-0041
is historical and non-authoritative. ADR-0041,
decided by the owner on 2026-09-25, chose an S3-compatible cloud, Cloudflare
R2, over a second local or rotated disk, an SFTP or rest-server peer, and
deferral; placed one remote Restic repository in R2 filled by `restic copy`
after the local backup and `check`; loaded the pgBackRest repository directory
into the remote Restic (day-level remote RPO, no keys or egress on `mng-pg`);
required a bucket lock, a bucket-scoped token and a manual remote
`forget-prune`; and kept R2 credentials as files under `secrets/backup/`, not in
OpenBao. It sized the copy against a 5 GiB cap that "fits inside the free tier
(10 GB)". Every decision carries forward; the cap is now an enforced upload
limit under the owner's 10 GB ceiling, 9 GB at adoption and 7.5 GB since
2026-11-25.

#### Consequences

##### Impacts

- Positive: host loss no longer loses every copy.
- Positive: the size cap keeps the copy inside the free tier and fails closed.

##### Follow-up

On 2026-11-17 the owner, @buenhyden, directed an in-place amendment of this
record: its sections moved line for line to the core decision form, and the
options table under Trade-offs was derived from the options it records. The
decision text is unchanged.

On 2026-11-25 the owner directed a second in-place amendment:
the upload cap moved from 9 GB to 7.5 GB, and remote space is reclaimed by an
owner-run `prune` that deletes only packs no snapshot uses, because the 30-day
lock refused the remote `forget-prune` (SPEC-0204 TSK-0006).

If a cloud KMS is later chosen for OpenBao unseal
([ADR-0042](0042-openbao-unseal-method.md)), decide whether it shares the R2
provider account.

###### Compliance
<!-- core-payload-level:4 -->

`offsite.sh`, `hyhome-backup.sh` and the Compose baseline tests enforce the cap,
the egress boundary and the no-delete daily run. POL-0021 control 1 records the
remote copy and its RPO; RUN-0021 holds the host-loss recovery order.

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
