---
title: "Host Storage Tiering Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-20"
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

### Spec amendment approval

On 2026-10-19 the user directed: "hdd와 ssd의 디스크 구성과 현재 상황에서
docker의 최적화 사용을 위해 어떻게 해야할지 조사하고 분석하여 이를 위한
계획을 수립하여 구현한다(ollama SSD 이동 포함)." The disk load analysis
below adds criterion 6 and W7 to the Spec and Plan.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0246 | draft | approved | #spec-approval |
| SPEC-0246-PLAN-0001 | draft | approved | #plan-approval |
| SPEC-0246-TSK-0001 | draft | ready | #inputs-and-authorization |
| SPEC-0246-TSK-0001 | ready | in-progress | #baseline-observation |

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
sudo mkdir -p /etc/systemd/system/containerd.service.d
printf '[Unit]\nRequiresMountsFor=/home/hyunyoun/storage\n' | sudo tee /etc/systemd/system/containerd.service.d/storage-mount.conf
sudo systemctl daemon-reload
sudo mv /var/lib/containerd /var/lib/containerd.old
sudo systemctl start containerd docker
```

Docker already declares the same dependency in
`/etc/systemd/system/docker.service.d/10-data-disk.conf`, so only containerd
gets a drop-in. k3s runs its own containerd at
`/run/k3s/containerd/containerd.sock` and is not stopped. The dry-run must
print nothing. Remove `/var/lib/containerd.old` only after
the agent records criterion 1 as passing. Rollback restores
`config.toml.bak-20261016`, moves `.old` back, and starts the units.

### W1 result

The owner ran the procedure on 2026-10-16 after a refreshed snapshot at
`/home/hyunyoun/storage/ops-snapshots/containerd-migration-20261016-r2/`
(69 containers, 58 healthy; 98 images; 832 volumes). Docker reports the
`io.containerd.snapshotter.v1` driver, `config.toml` names
`/home/hyunyoun/storage/containerd`, and `/var/lib/containerd.old` remains.

Recovery needed three owner steps, none caused by the new root:

- `keycloak` exited 128 because a containerd shim from the restart (no child
  process) still held its task, so `docker start` returned
  `task … already exists`. The owner killed the shim on 2026-10-19 and the
  agent started the container; no other shim lacked a running container.
- On 2026-10-17 at 20:55 KST, with `dockerd` unchanged since the move,
  OpenBao and the five k3d nodes were stopped through the API and OpenBao
  restarted sealed. Gatus, kafbat-ui, and oauth2-proxy then looped on OIDC
  discovery. The owner unsealed OpenBao (RUN-0098 steps 4–6) and ran
  `k3d cluster start hyhome`; the agent started `k3d-hyhome-agent-1`, which
  that command left stopped.
- After these steps, on 2026-10-19: 58 healthy and 0 unhealthy containers,
  every snapshot image present, and all four k3d nodes `Ready`. The only
  missing container is `p01-sweep-probe4`, a `--rm` probe removed by the stop
  together with its two anonymous volumes (830 volumes). Three `Created`
  containers from 2026-10-18 belong to local MCP clients and are outside this
  Task.

### W2 owner procedure

Before the W1 restart, add
`"builder": { "gc": { "enabled": true, "defaultKeepStorage": "10GB" } }` to
the top-level object of `/etc/docker/daemon.json`, keeping `runtimes` and
`data-root`, then confirm it with
`sudo python3 -m json.tool /etc/docker/daemon.json`:

```bash
sudo cp /etc/docker/daemon.json /etc/docker/daemon.json.bak-20261016
sudo python3 -c 'import json,pathlib; p=pathlib.Path("/etc/docker/daemon.json"); d=json.loads(p.read_text()); d["builder"]={"gc":{"enabled":True,"defaultKeepStorage":"10GB"}}; p.write_text(json.dumps(d,indent=4)+"\n")'
sudo python3 -m json.tool /etc/docker/daemon.json
```

### W2 result

`/etc/docker/daemon.json` (written 2026-10-16 22:20 KST, backup
`daemon.json.bak-20261016`) parses and keeps `data-root` and the `nvidia`
runtime. `docker buildx inspect` shows the policy derived from it: rules 1–3
carry `Reserved Space: 10GiB` and no `Max Used Space`. On 2026-10-19 a
one-file `FROM scratch` build left `docker buildx du` at 15.31 GB, above the
10 GB intent, and no prune was logged. Whether `defaultKeepStorage` alone caps
the cache under this BuildKit version is not established. The next step is an
owner decision between adding an explicit `defaultMaxUsedSpace` (another daemon
restart, so another OpenBao unseal) and accepting the reserved-space floor.
On 2026-10-19 the owner accepted the 10 GB reserved-space floor, so the
cache is bounded by BuildKit's default policies rather than a hard cap.

### Disk load analysis

Observed on 2026-10-19 after 7.3 days of uptime, from `/proc/diskstats`:

| Disk | Busy time | Busy in a 20 s sample | Read | Written |
| --- | --- | --- | --- | --- |
| SSD `sda` (Crucial MX300 275 GB) | 5.5% | 0% | 366 GB | 596 GB |
| HDD `sdb` (Toshiba DT01ACA3 3 TB) | 65% | 61% | 195 GB | 980 GB |

Writes by container since each one's last start (two to three days), from
`docker stats`: Pyroscope 42.9 GB, Alloy 26.6 GB, `mng-pg` 22.7 GB, Loki
19.7 GB, SeaweedFS volume 18.0 GB, Prometheus 9.7 GB, Tempo 5.4 GB, Kafka
3.8 GB. The SSD has 143 GB free; swap (`/swap.img`, 8 GB on the SSD) holds
6.7 GB with `vm.swappiness` 60. Both disks use `mq-deadline`. The SSD already
writes about 85 GB a day (about 31 TB a year), and its rated endurance and
current wear are not yet read, so a move to the SSD needs SMART first (W7).

### W7 SMART reading and write-rate start

The owner read the SSD's SMART attributes on 2026-10-19: power-on 39,902 h
(4.55 years), `Percent_Lifetime_Remain` normalized 76 (24% used), no
reallocated events, and `Total_LBAs_Written` 81,764,994,229, which is 41.9 TB
of host writes. That is about 0.57% of lifetime per TB written. At the
seven-day rate (31 TB a year) the drive has about 4.3 years left; adding the
observability stores' recent writes (about 42 GB a day) would leave about
2.9 years, outside the five-year budget, so moving all of them is rejected.
The seven-day window includes SSD writes from before the containerd move,
and swap is full (8 GB, about 45 GB swapped out in seven days), so the
post-move rate is measured directly. The t0 snapshot (`/proc/diskstats` and
each container's cgroup `wbytes`) was taken at 2026-10-19T23:51:52+09:00 under
`/home/hyunyoun/storage/ops-snapshots/w7-write-rate-20261019/`; t1 follows 24
hours later.

### Ollama 0.40.6 runtime

SEC01 TSK-0009 owns the 0.40.6 pin (PR #516). On 2026-10-19 a
`docker compose up -d ollama` started from an IDE terminal at 22:50 KST, before main
carried the new pin, recreated Ollama on 0.40.3 while the image pull drove the
load average to 383. The agent stopped its own concurrent run, waited, then
recreated Ollama from main on 0.40.6.

The first 0.40.6 start fell back to the CPU: GPU discovery for `cuda_v12`
and `cuda_v13` hit the 30 s watchdog, and 0.40.0 in a probe container timed out
the same way. 0.40.6 supports the GPU: probes found CUDA0 (GTX 1060, compute
6.1, `cuda_v12`) in 1.7 s. A restart right after the probes found CUDA0. The
cause is identified under W3 result. The 0.40.0 and 0.40.3 images were removed at the
owner's direction.

`ollama pull` refreshed all five installed models. `tev1:0.8b` (now
`abc31fdb0bf5`, requires 0.40.4) and `embeddinggemma-2:740m` (now
`f4981a15b998`) changed; `gemma4:e4b`, `gemma4:e2b` and `lfm2.5:8b` were
already current. `tev1` answered `/v1/systemone` on the GPU and
`embeddinggemma-2` returned 768-dimension embeddings.

### W3 baseline

On 0.40.6, from the HDD, `gemma4:e2b` (4.6 GB) took 318.4 s to load
(`load_duration`, `keep_alive` 0, one generated token), with the HDD at
about 60% busy.

### W3 result

On 2026-10-20 the owner ran a first copy with Ollama running, the agent
stopped Ollama, the owner ran a final `rsync --delete` whose dry-run printed
nothing, and the owner removed the `ollama-data` volume and recreated the
service; the agent cannot remove volumes in this session. The volume device
is `/home/hyunyoun/fast-volumes/ai/ollama`, `.env` and `.env.example` hold
the same keys, and the model list shows the same five names and IDs.

The new container fell back to the CPU twice. Probes with each service
constraint alone (CPU, memory and PID limits, dropped capabilities with
`no-new-privileges` and `init`, the service environment, the model volume)
all found CUDA0, and a service restart right after them found CUDA0. The
owner then enabled NVIDIA persistence mode with an `nvidia-persistenced`
drop-in that removes `--no-persistence-mode`; the next restart still fell back.
A probe with every service constraint failed once and then passed four times
in a row, so the failure depends on cache state, not configuration. In the
failing debug run the `cuda_v12` (1.3 GB) and `cuda_v13` (818 MB) probes
each took the full 30 s while `vulkan` (39 MB) took 0.2 s: the libraries were
read cold from the HDD image store, whose page cache the full swap shows is
under pressure. The Ollama entrypoint now reads `cuda_v12` before
`ollama serve`; a probe with that entrypoint found CUDA0.

On CUDA0, from the SSD, `gemma4:e2b` took 55.9 s to load (318.4 s from the
HDD), measured the same way. The HDD copy at
`/home/hyunyoun/storage/volumes/ai/ollama` stays until the owner removes it.

### W3 owner copy step

After the agent stops Ollama, copy the root-owned model directory:

The owner then adds
`OLLAMA_MODEL_DIR=/home/hyunyoun/fast-volumes/ai/ollama` to the local `.env`,
and the agent removes and recreates the `ollama-data` volume and the service.

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
| Containerd move | 1 | W1 | Owner procedure and agent comparison against the snapshot | Owner-run host change and r2 snapshot | PASS | Work Log: W1 result | required | - |
| Build-cache limit | 3 | W2 | `daemon.json` parse and `docker buildx du` after a build | Owner-run host change | FAIL | Work Log: W2 result (15.31 GB after a build) | required | - |
| Build-cache floor decision | 3 | W2 | `daemon.json` parse and `docker buildx du` after a build | Owner-accepted policy: GC enabled with a 10 GB reserved-space floor, observed in `docker buildx inspect` | PASS | Work Log: W2 result | required | Build-cache limit |
| Ollama SSD move | 2 | W3 | Rendered device, model list, first-load time before and after | Compose change and owner copy | PASS | Work Log: W3 result (318.4 s to 55.9 s) | required | - |
| Image archive | 3 | W4 | Push, stored-digest comparison, local removal | 16 approved candidates | PASS | Work Log: W4 image archive (15 archived, 1 push failure left in place) | required | - |
| Volume and container cleanup | 3 | W5 | Ownership inventory and removal of unowned items | Host state after W1 | NOT_RUN | Work Log | required | - |
| Registry pin | 4 | W5 | Running image digest equals the Compose pin | Running `registry:3` versus pinned `registry:3.1.2@sha256:ddf754342cfc…` | NOT_RUN | Work Log | required | - |
| Observability store placement | 6 | W7 | SMART counters, per-store write rate, keep-or-move decision | Disk load analysis | NOT_RUN | Work Log: Disk load analysis | required | - |
| Policy promotion | 5 | W6 | Changed metadata and link checks | Operations owner document | NOT_RUN | Work Log | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | Pre-migration snapshot, Containerd move | Health, images, and k3d nodes match the r2 snapshot on 2026-10-19. | SPEC-0246 TSK-0001 |
| 2 | accepted | Ollama SSD move | Same model list from the SSD path; first load 318.4 s before and 55.9 s after. | SPEC-0246 TSK-0001 |
| 3 | pending | Build-cache limit, Build-cache floor decision, Image archive, Volume and container cleanup | Archive done and the floor accepted; cleanup remains. | SPEC-0246 TSK-0001 |
| 4 | pending | Registry pin | Waits for W5. | SPEC-0246 TSK-0001 |
| 5 | pending | Policy promotion | Waits for criteria 1–4 and 6. | SPEC-0246 TSK-0001 |
| 6 | pending | Observability store placement | Waits for the SMART reading and W3. | SPEC-0246 TSK-0001 |

## Review and Completion

This Task was issued `draft` in PR #512; the pre-migration snapshot and W4 make it `in-progress`. It completes only when every criterion is
accepted on direct host observation; a hosted CI result does not prove a host
change.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
