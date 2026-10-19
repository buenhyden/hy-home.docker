---
title: "Host Storage Tiering"
version: "0.2.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-20"
layer: "specs"
artifact_id: "SPEC-0246"
parent_ids:
- "REQ-0027"
- "AD-0031"
created: "2026-10-16"
---

# Host Storage Tiering

## Overview

The home host has a 256 GB SSD (`sda`, root filesystem) and a 2.7 TB HDD
(`sdb`, mounted at `/home/hyunyoun/storage`). On 2026-10-16 the root
filesystem reached 95%. Docker 29.8.2 uses the containerd image store
(`io.containerd.snapshotter.v1`), so image layers and build cache live under
containerd's root, `/var/lib/containerd` (127 GB on the SSD), although
Docker's `data-root` is already on the HDD. Ollama models (14 GB) sit on the
HDD, where model loading is slow.

After the move, on 2026-10-19, the HDD was busy for 65% of the seven days of
uptime and 61% in an idle sample, while the SSD stayed near 0%. Most of the
HDD writes come from the observability stores, and a cold read of Ollama's
1.3 GB CUDA libraries from the HDD image store outlasted its GPU discovery.

This Spec defines one placement and growth policy for every Docker storage
class on this host and applies it.

## Scope

In scope: the containerd root and its boot-time mount dependency; Docker
build-cache garbage collection; a configurable Ollama model directory; an
archive path for unused images through the loopback registry; removal of
unowned dangling volumes and stray containers after an ownership inventory;
the running registry container matching its Compose pin; and a measured
placement decision for the write-heavy observability stores.

Out of scope: image version upgrades and their security review, which
SPEC-0204 SEC01 owns; k3s and the k3d cluster, which belong to the Kubernetes
repository; moving service data that W7 does not name; and deleting
anything an inventory does not prove unowned.

## Contracts

### Placement policy

| Storage class | Tier | Location | Growth control |
| --- | --- | --- | --- |
| Image layers and snapshots | HDD | containerd `root` = `/home/hyunyoun/storage/containerd` | Unused images are archived to the registry, then removed locally |
| Build cache | HDD (inside the containerd root) | BuildKit | `builder.gc` with `defaultKeepStorage` 10 GB |
| Container metadata and json-file logs | HDD | Docker `data-root` = `/home/hyunyoun/storage/docker-root/docker` | Shared logging default `max-size` 10m × `max-file` 3 |
| Service named volumes | HDD | `${DEFAULT_MOUNT_VOLUME_PATH}` subdirectories | Owned by each service |
| Ollama models | SSD | `${OLLAMA_MODEL_DIR}` (local `.env`) | Model set owned by the AI tier |
| Registry blobs | HDD | `${DEFAULT_REGISTRY_DIR}` | Archive ledger per pushed image |
| Write-heavy observability stores (Prometheus, Loki, Tempo, Pyroscope, Alloy) | HDD until W7 decides | Per-store override variable, as for Ollama | SSD endurance budget measured in W7 |
| Root filesystem free space | SSD | `/` | Existing `HostSystemDiskLow` alert at 25 GiB free |

A service moves to the SSD only when a measured latency problem names it and
SSD free space after the move stays above the existing alert threshold.
Datastores remain on the HDD; their current data sets are small. A store
that W7 names moves only when its measured write rate, added to the SSD's
current rate, keeps the drive's projected wear within its rated endurance for
five years.

### Execution boundary

- The `containerd` and `docker` units declare
  `RequiresMountsFor=/home/hyunyoun/storage`, so neither starts on an
  unmounted HDD path.
- `infra/08-ai/ollama/docker-compose.yml` binds
  `${OLLAMA_MODEL_DIR:-${DEFAULT_AI_MODEL_DIR}/ollama}`. An unset variable
  keeps the current location.
- An image is archived only after the registry's stored manifest digest
  equals the pushed digest. A multi-platform local index is archived as its
  platform manifest, and the ledger records that difference.
- Root-only host changes are executed by the owner; source changes and
  verification are executed by the agent. The Task records who ran each step.

## Acceptance Criteria

1. After the containerd move, the image list, the container set, and every
   health status equal the recorded pre-migration snapshot. After the old
   root is removed, the root filesystem has at least 100 GB more free space.
2. Ollama serves the same model list from the SSD path, and the first-load
   time of one named model is measured before and after the move.
3. Build-cache garbage collection is configured. The volume and container
   cleanup removes only items the inventory shows unowned, and every
   archived image has a digest-verified ledger row.
4. The running registry container uses the Compose-pinned image.
5. The placement policy is promoted to a current operations owner once
   criteria 1–4 and 6 are accepted.
6. W7 records the SSD's SMART wear and written-bytes counters, the 24-hour
   write rate of each write-heavy observability store, and a keep-or-move
   decision for each; a moved store serves its existing data from the SSD.

## Failure Conditions

Stop and roll back the containerd move if copy verification reports any
difference, if containerd or Docker fails to start, or if a container that
was healthy before is unhealthy after. Keep `/var/lib/containerd.old` until
criterion 1 passes. Keep the Ollama HDD copy until criterion 2 passes. Do not
remove a volume, container, or image whose owner is unknown or whose archive
digest is unverified.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-host-storage-tiering.md)
- [Home host requirement](../../01.requirements/0027-home-development-host.md)
- [Home host architecture](../../02.architecture/descriptions/0031-home-development-host.md)
- [Integration owner](../0204-service-integration-security-and-operations/spec.md)
