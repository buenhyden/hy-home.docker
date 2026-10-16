---
title: "Host Storage Tiering Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0246-TSK-0001"
parent_ids:
- "SPEC-0246-PLAN-0001"
created: "2026-10-16"
---

# Host Storage Tiering Task

## Overview

### Objective

Execute W1–W6 of the SPEC-0246 Plan and record who ran each step, the exact
commands, and the observed results. This Task owns criteria 1–5.

## Inputs and Authorization

On 2026-10-16 the user directed the Ollama SSD move and the containerd move,
chose the proposed order, and asked that the disk optimization method be
applied in the Spec, Plan, and Task. The user also approved archiving unused,
tagged, non-Task-pinned images to the loopback registry. Root-only steps
(stopping system units, editing `/etc`, copying root-owned files) are run by
the owner in a separate terminal; the agent cannot use `sudo`. Remote merges
remain with the owner.

## Work Log

### Spec approval

The user approved the placement policy, execution order, and boundaries
above on 2026-10-16.

### Plan approval

The user approved the W1–W6 order with the containerd move first.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0246 | draft | approved | #spec-approval |
| SPEC-0246-PLAN-0001 | draft | approved | #plan-approval |

### Baseline observation

Before any change: root filesystem 85% used after earlier cleanup (95% at the
start of the day); `/var/lib/containerd` 127 GB; Docker images 102.1 GB with
48 in use; build cache 14.48 GB; 832 volumes, of which 39 are active; Ollama
models 14 GB on the HDD. The pre-migration snapshot is stored at
`/home/hyunyoun/storage/ops-snapshots/containerd-migration-20261016/`
(`containers.tsv` 69 rows, 58 healthy; `images.tsv` 98 rows;
`volumes.txt` 832 rows; `docker-info.txt`; `df.txt`).

### W1 owner procedure

Run in a separate terminal, after the agent confirms no local gate is using
Docker:

```bash
sudo systemctl stop docker.socket docker containerd
sudo mkdir -p /home/hyunyoun/storage/containerd
sudo rsync -aHAXS --numeric-ids --info=progress2 /var/lib/containerd/ /home/hyunyoun/storage/containerd/
sudo rsync -aHAXS --numeric-ids --dry-run --itemize-changes /var/lib/containerd/ /home/hyunyoun/storage/containerd/ | head
sudo cp /etc/containerd/config.toml /etc/containerd/config.toml.bak-20261016
sudo sed -i 's#^root = "/var/lib/containerd"$#root = "/home/hyunyoun/storage/containerd"#' /etc/containerd/config.toml
for s in containerd docker; do
  sudo mkdir -p /etc/systemd/system/$s.service.d
  printf '[Unit]\nRequiresMountsFor=/home/hyunyoun/storage\n' | sudo tee /etc/systemd/system/$s.service.d/storage-mount.conf
done
sudo systemctl daemon-reload
sudo mv /var/lib/containerd /var/lib/containerd.old
sudo systemctl start containerd docker
```

The dry-run must print nothing. Remove `/var/lib/containerd.old` only after
the agent records criterion 1 as passing. Rollback restores
`config.toml.bak-20261016`, moves `.old` back, and starts the units.

### W2 owner procedure

Before the W1 restart, add
`"builder": { "gc": { "enabled": true, "defaultKeepStorage": "10GB" } }` to
the top-level object of `/etc/docker/daemon.json`, keeping `runtimes` and
`data-root`, then confirm it with
`sudo python3 -m json.tool /etc/docker/daemon.json`.

### W3 owner copy step

After the agent stops Ollama, copy the root-owned model directory:

```bash
sudo mkdir -p /home/hyunyoun/fast-volumes/ai/ollama
sudo rsync -aHAX --numeric-ids --info=progress2 /home/hyunyoun/storage/volumes/ai/ollama/ /home/hyunyoun/fast-volumes/ai/ollama/
sudo rsync -aHAX --numeric-ids --dry-run --itemize-changes /home/hyunyoun/storage/volumes/ai/ollama/ /home/hyunyoun/fast-volumes/ai/ollama/ | head
```

### W4 image archive

The agent tagged each image as `127.0.0.1:5000/<ref>`, pushed it, compared
the pushed digest with the registry's `Docker-Content-Digest`, and removed the
local tags only when they matched. Nineteen unused images pinned by a Task or
named in a Spec were excluded, as were 27 untagged images.
`hy-home/openbao:oci-format-smoke-20261014` failed to push (two image IDs
share that tag) and was left in place.

| Image | Local ID | Registry digest | Identity |
| --- | --- | --- | --- |
| `alpine:3.22` | `5291449c3df7` | `3e9b4b680bfc` | platform-manifest |
| `couchdb:3.5.2` | `5fc596110eac` | `6785bd4bec3d` | platform-manifest |
| `curlimages/curl:8.22.0` | `58adaa4e8dca` | `43366cd60f22` | platform-manifest |
| `ghcr.io/hadolint/hadolint:v2.14.0` | `27086352fd5e` | `e9dbf5113239` | platform-manifest |
| `ghcr.io/zalando/spilo-17:4.0-p3` | `b7db9e8f62e8` | `17bf371c9241` | platform-manifest |
| `haproxy:3.4.4` | `b3b426904258` | `1fc351581a4f` | platform-manifest |
| `hy-home-lab-opensearch-opensearch-node1:latest` | `f5c3348a3999` | `f5c3348a3999` | identical |
| `hy-home-lab-opensearch-opensearch-node2:latest` | `a099fbcbe80f` | `a099fbcbe80f` | identical |
| `hy-home-lab-opensearch-opensearch-node3:latest` | `9848d54470d1` | `9848d54470d1` | identical |
| `hy-home/stalwart-config:0.16.25-cli1.0.13-local` | `b03df4ab2048` | `b03df4ab2048` | identical |
| `mongo-express:1-18-alpine3.19` | `7b4471277e3b` | `96f81d04fe1a` | platform-manifest |
| `openpolicyagent/conftest:v0.70.1` | `82f23e0e1f3f` | `3db690da9904` | platform-manifest |
| `opensearchproject/opensearch-dashboards:3.8.0` | `7fb7ec1b33f1` | `647672283fbb` | platform-manifest |
| `quay.io/coreos/etcd:v3.7.1` | `3c66a5191d37` | `9fc5c86dedac` | platform-manifest |
| `sonarqube:26.9.0.129388-community` | `c0f1160bccfa` | `2561a3ceb4e8` | platform-manifest |

`platform-manifest` means the local multi-platform index was stored as its
single-platform manifest, so a re-pulled image ID differs from the original.
Digests are shown as their first 12 hexadecimal characters.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pre-migration snapshot | 1 | W1 | `docker ps -a`, `docker image ls`, `docker volume ls`, `docker info`, `df` | Host state 2026-10-16 | PASS | `/home/hyunyoun/storage/ops-snapshots/containerd-migration-20261016/` | required | - |
| Containerd move | 1 | W1 | Owner procedure and agent comparison against the snapshot | Owner-run host change | NOT_RUN | Work Log: W1 owner procedure | required | - |
| Build-cache limit | 3 | W2 | `daemon.json` parse and `docker buildx du` after a build | Owner-run host change | NOT_RUN | Work Log: W2 owner procedure | required | - |
| Ollama SSD move | 2 | W3 | Rendered device, model list, first-load time before and after | Compose change and owner copy | NOT_RUN | Work Log: W3 owner copy step | required | - |
| Image archive | 3 | W4 | Push, stored-digest comparison, local removal | 16 approved candidates | PASS | Work Log: W4 image archive (15 archived, 1 push failure left in place) | required | - |
| Volume and container cleanup | 3 | W5 | Ownership inventory and removal of unowned items | Host state after W1 | NOT_RUN | Work Log | required | - |
| Registry pin | 4 | W5 | Running image digest equals the Compose pin | Running `registry:3` versus pinned `registry:3.1.2@sha256:ddf754342cfc…` | NOT_RUN | Work Log | required | - |
| Policy promotion | 5 | W6 | Changed metadata and link checks | Operations owner document | NOT_RUN | Work Log | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | Pre-migration snapshot, Containerd move | Waits for the owner-run move and comparison. | SPEC-0246 TSK-0001 |
| 2 | pending | Ollama SSD move | Waits for W1 and the owner copy. | SPEC-0246 TSK-0001 |
| 3 | pending | Build-cache limit, Image archive, Volume and container cleanup | Archive done; limit and cleanup remain. | SPEC-0246 TSK-0001 |
| 4 | pending | Registry pin | Waits for W5. | SPEC-0246 TSK-0001 |
| 5 | pending | Policy promotion | Waits for criteria 1–4. | SPEC-0246 TSK-0001 |

## Review and Completion

This Task is issued `draft`. It completes only when every criterion is
accepted on direct host observation; a hosted CI result does not prove a host
change.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
