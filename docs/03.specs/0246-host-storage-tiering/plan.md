---
title: "Host Storage Tiering Plan"
version: "0.2.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-20"
layer: "specs"
artifact_id: "SPEC-0246-PLAN-0001"
parent_ids:
- "SPEC-0246"
created: "2026-10-16"
---

# Host Storage Tiering Plan

## Overview

Apply the SPEC-0246 placement policy in dependency order. The containerd move
comes first because it frees the SSD space that the Ollama move and later
SEC01 image pulls need.

## Scope

The work covers the host configuration, one Compose variable, cleanup driven
by an ownership inventory, and promotion of the policy to an operations
owner. Image upgrades stay with SPEC-0204 SEC01; archiving an image that an
upgrade replaces reuses W4's procedure.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Record the pre-migration snapshot; the owner stops Docker, copies `/var/lib/containerd` to the HDD, changes containerd `root`, adds the mount dependency, keeps `.old`, and restarts | None | TSK-0001 | rsync dry-run shows no difference; image, container, and health comparison against the snapshot; `df` before and after removing `.old` |
| W2 | 3 | The owner adds `builder.gc` with `defaultKeepStorage` 10 GB to `daemon.json`, before the W1 restart | None | TSK-0001 | `json.tool` parses; `docker buildx inspect` shows GC enabled with the 10 GiB reserved-space floor the owner accepted in place of a hard cap |
| W3 | 2 | Add `OLLAMA_MODEL_DIR` to the Ollama Compose file, README, and `.env.example`; stop Ollama; the owner copies the root-owned model directory to the SSD; recreate the volume; start | W1 | TSK-0001 | Rendered Compose device; model list equality; first-load time of one named model before and after |
| W4 | 3 | Archive unused, tagged images that no Task pins to the loopback registry, and remove the local copy only after digest verification | None | TSK-0001 | Ledger row per image: local ID, stored digest, identical or platform-manifest |
| W5 | 3, 4 | Inventory dangling volumes and stray containers by owner; remove only unowned items; recreate the registry container from its Compose pin | W1 | TSK-0001 | Inventory with owner per item; registry image digest equals the Compose pin |
| W7 | 6 | The owner reads SSD SMART counters; the agent measures each observability store's 24-hour write rate with `scripts/operations/storage-write-rate.py`, records a keep-or-move decision, and moves an approved store through a per-store override variable with the W3 procedure | W3 | TSK-0001 | SMART wear and written-bytes before and after; per-store write rate, where a window under 24 h, a restart, or a counter decrease defers the store; rendered device; the store's data and health after the move |
| W6 | 5 | Promote the placement policy to the current operations owner | W1–W5, W7 | TSK-0001 | Changed document metadata and link checks |

## Verification Plan

Source changes use the changed-document metadata and link checks, the Compose
render for the Ollama service, and the affected hardening check. Host changes
are verified by direct observation: `docker info`, `docker image ls`, the
container and health list, `df`, and the registry manifest digest. Every
comparison uses the pre-migration snapshot stored under
`/home/hyunyoun/storage/ops-snapshots/`. A hosted CI result does not prove a
host change.

## Risks and Recovery

### Risks and Rollback

- W1 stops every container for the copy. Rollback: stop the units, restore
  the backed-up `config.toml`, move `/var/lib/containerd.old` back, and start.
- Image layers on the HDD make cold container starts slower. This is the
  accepted trade-off; Ollama stays on the SSD.
- Without the mount dependency, a boot that starts containerd before the HDD
  mounts would create an empty root on the SSD; W1 adds the dependency first.
- W3 rollback: unset `OLLAMA_MODEL_DIR` and recreate the volume; the HDD copy
  is kept until criterion 2 passes.
- Ollama's GPU discovery gives up after 30 s per library. Reading the
  1.3 GB `cuda_v12` libraries cold from the busy HDD image store took longer,
  and the server fell back to the CPU. The Ollama entrypoint now reads those
  libraries before `ollama serve`. The read is best-effort: a missing
  directory logs a `cat` error and the server still starts, so the
  `inference compute` log line naming CUDA0 after any Ollama start is the GPU
  check, and an upgrade that moves the library directory must update the
  entrypoint.
- W7 adds SSD writes. A store moves only within the endurance budget in the
  Spec; rollback unsets its override and recreates its volume from the HDD
  copy, which is kept until criterion 6 passes.
- W4 stores a multi-platform image as its platform manifest, so a re-pulled
  image ID differs from the original index ID. Task-pinned images are
  excluded until their owner updates the pin.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-host-storage-tiering.md)
