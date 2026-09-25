---
title: "SeaweedFS Operations Policy"
version: "1.5.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-25"
layer: "operations"
artifact_id: "POL-0024"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# SeaweedFS Operations Policy

## Overview

This policy binds current source configuration to data protection, security,
resource, lifecycle and independently verifiable operator controls.

## Policy Scope

SeaweedFS is the S3 object store; it replaced MinIO in SPEC-0180 S07. It is HOME: every profile that selects an S3 consumer (`storage`,
`obs`, `logs`, `tracing`, `nginx`, `mlops`, `data-science`, `lakehouse`) also
selects the four services and `seaweedfs-buckets`, as do `seaweedfs` and
`storage-seaweedfs`; `lakehouse` also selects `seaweedfs-table-bucket`.
Terrakube (`iac`, an automation profile HOME excludes) runs with `storage`.

## Controls

- **Persistent set.** Master (`-mdir=/data`), volume (`-dir=/data`) and the
  filer's embedded leveldb2 store (`/data/filerldb2`) each have a bind volume
  under `${DEFAULT_DATA_DIR}/seaweedfs`. The embedded store is chosen over an
  external database: it adds no start or recovery dependency, and the filer
  metadata export is its portable form. A `/data` mount alone never proves the
  path; the rehearsal checks the files land there.
- **S3 identities.** `seaweedfs-s3` starts only with explicit identities built
  from secrets (admin: `SEAWEEDFS_S3_ADMIN_ACCESS_KEY` and STRG-010). With
  identities present, anonymous requests are refused. Every consumer added in
  S07 has its own identity in `config/s3-identities.conf`, scoped to its
  bucket (loki, tempo, mlflow, terrakube, lakehouse); no consumer uses admin, and
  `anonymous` may only read objects in `cdn-bucket`. Buckets are created by
  `seaweedfs-buckets`, never by a consumer.
- **No IAM bypass.** Volume and filer HTTP require JWTs signed with STRG-008 and
  STRG-009 for reads and writes. Only the S3 route exists; master and filer have
  no Traefik route, and a CDN is a public-read bucket through S3, never the
  filer.
- **Internal transport.** Every gRPC port uses mutual TLS from a SeaweedFS-only
  CA (`bin/gen-grpc-certs.sh`; the CA key is discarded after issuance). S3 is
  plain HTTP on `object_net` with SigV4 signatures, and HTTPS through Traefik
  for host clients. Master, volume and filer are only on `seaweed_internal`
  (internal); the master's unauthenticated `/dir/assign` is reachable only
  there.
- **Minimal surface.** The Lance listener and the embedded IAM API are off.
  The Iceberg REST catalog listens on `${SEAWEEDFS_ICEBERG_PORT:-8181}` on
  `object_net` only, with no route; it signs with the same identities (SigV4).
  Only the `lakehouse` table bucket exists, owned by admin. Its policy grants
  the `lakehouse` identity catalog and table actions only (no policy change,
  no bucket deletion); `seaweedfs-table-bucket` rewrites it on every run, so a
  hand-edited policy does not survive.
- **Metrics.** Only `seaweedfs-s3` serves metrics, on `9327`, scraped by
  Prometheus as job `seaweedfs-s3`. The listener is not published and has no
  Traefik route, but any `edge_net` service can reach it; that is accepted
  because it carries request counters and latencies only (low sensitivity).
  Master, volume and filer are not exposed for scraping.
  `SeaweedFSS3Down` and `SeaweedFSDataDiskLow` live in
  `alert_rules.local.datastores.yml`; the disk rule pins the node-exporter
  mountpoint of the data-disk filesystem and must follow it if
  `DEFAULT_MOUNT_VOLUME_PATH` moves.
- **Capacity.** The volume server stops accepting writes below 20 GiB free on
  the data disk (`-minFreeSpace`, POL-0035). Same-host replicas are not host
  availability, so replication is `000`.

### Backup and restore

The daily orchestrator (RUN-0021) pauses vacuum, saves filer metadata with
`fs.meta.save`, lets Restic read the volume and master trees, and re-enables
vacuum on exit. Needles are append-only, so objects written before the
metadata export restore intact. An object overwritten or deleted while Restic
reads the volume files may restore as missing, and a volume index copied after
its data file may list needles past its end (checked with `volume.fsck` on
restore). The recovery point is therefore the export time, minus objects
changed inside the Restic window. The set lives in the encrypted Restic state
repository on the other physical disk, inside the 5 GiB budget (POL-0021).
Keep daily sets for 30 days and weekly sets for 90 days. The target is RPO
24 hours and RTO 8 hours; the isolated rehearsal proves the method, not the
HOME timing.

Restore on an empty target at the same version: volume and master trees in
place, an empty filer store, then `fs.meta.load`, then S3 reads. Cutover,
deletion or state reuse on HOME needs separate approval.

### Change policy

Image updates need an official release and license review plus a passing
`SeaweedfsRehearsalTests` run. Identity, key or certificate rotation restarts
every component and needs approval. A new consumer identity is added in the
same change as that consumer's cutover.

## Exceptions

A FUSE mount needs separate approval. Exceptions do not authorize runtime mutation, plaintext secrets, raw active
storage copies or same-host availability claims.

## Verification

Verify root configuration and scoped static policy checks, then require an
isolated compatible restore with application-level acceptance before promotion or
cutover. Record unverified runtime properties explicitly.

## Review Cadence

Review after profile, image, volume, credential, consumer, retention or upstream
lifecycle change and at least annually while retained.

## Traceability

- Runtime source: [SeaweedFS Compose](../../../infra/04-data/lake-and-object/seaweedfs/docker-compose.yml).
- Artifact: `POL-0024`; parent: `AD-0004`.
- Runtime authority remains the linked Compose/source files; exact pins stay there.

### References

- [Data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup)
- [Security configuration](https://github.com/seaweedfs/seaweedfs/wiki/Security-Configuration)
- [Runbook](../runbooks/0024-seaweedfs.md)

## Related Documents

- [Domain catalog](../README.md)
