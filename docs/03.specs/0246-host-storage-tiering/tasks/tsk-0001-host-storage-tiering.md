---
title: "Host Storage Tiering Task"
version: "0.1.10"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0246-TSK-0001"
parent_ids:
- "SPEC-0246-PLAN-0001"
created: "2026-10-16"
---

# Host Storage Tiering Task

## Overview

### Objective

Execute W1–W7 of the SPEC-0246 Plan and record who ran each step, the exact
commands, and the observed results. This Task owns criteria 1–6. W7 follows
W3, and W6 follows W7.

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

On 2026-10-20 the agent rechecked the policy read-only: Docker 29.8.2,
buildx 0.37.1 and BuildKit 0.33.1 on the `docker` driver; rules 1–3 still
carry `Reserved Space: 10GiB` without `Max Used Space`, and `docker buildx du`
reports 15.31 GB. The Plan's W2 check now verifies that floor instead of a cap;
the FAIL row below stays as recorded.

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

### W7 write-rate tooling

`scripts/operations/storage-write-rate.py` takes t1 the same way and compares
it with t0. The t0 `wbytes` column sums every line of each container's
cgroup `io.stat`, so dm-0 (`ubuntu--vg-ubuntu--lv`) repeats the SSD line:
Traefik's t0 value, 12,009,472, is twice its 8:0 line. The tool keeps that
sum so t0 and t1 compare, and treats store bytes as an upper bound. A window
under 24 h, a changed StartedAt, a decreased counter, a missing row, or
missing SMART input defers the store.

A read-only probe at 2026-10-20T03:04:17+09:00 (about 3 h after t0) found all
five stores with the same StartedAt as t0 and returned `DEFER` for every
store because the window is under 24 h. t1 is due at
2026-10-20T23:51:52+09:00:

```bash
python scripts/operations/storage-write-rate.py collect /home/hyunyoun/storage/ops-snapshots/w7-write-rate-20261019 t1
python scripts/operations/storage-write-rate.py compare /home/hyunyoun/storage/ops-snapshots/w7-write-rate-20261019 \
  --smart-used-percent <used> --smart-host-bytes <Total_LBAs_Written × 512>
```

The owner rereads SMART at t1. A store whose StartedAt changed needs a new
24-hour window.

### W7 first window result — 2026-10-21

t1 was taken at 2026-10-21T05:56:08+09:00 (window 108,256 s). Disks are
valid: sda (SSD) 56,311,934,976 bytes, about 44.9 GB a day, and sdb
170,309,713,920 bytes, about 135.9 GB a day. Every store is `DEFER`. Alloy,
Prometheus, Pyroscope and Tempo were recreated in the 2026-10-20 image
rollouts (SEC01 TSK-0009), so their counters reset. Loki kept its StartedAt
and is deferred only because SMART was not supplied: reading SMART needs the
owner's sudo. A new window started at 2026-10-21T05:56:40+09:00 under
`/home/hyunyoun/storage/ops-snapshots/w7-write-rate-20261021/`; its t1 is
due at 2026-10-22T05:56:40+09:00, with the owner's SMART reading at the same
time. Loki can be decided from the first window once SMART is read:

```bash
python3 scripts/operations/storage-write-rate.py compare /home/hyunyoun/storage/ops-snapshots/w7-write-rate-20261019 \
  --smart-used-percent <used> --smart-host-bytes <Total_LBAs_Written × 512>
```

The owner read SMART at about 06:30 on 2026-10-21, about 35 minutes after t1:
`Percent_Lifetime_Remain` 24 used, `Total_LBAs_Written` 81,875,803,541
(41,920,411,412,992 bytes; 110,809,312 LBAs, about 56.7 GB, since 2026-10-19).
With these values the comparison gives an SSD baseline of 8.09 years and
Loki `ELIGIBLE`: 2,201,448,448 bytes in the window, about 1.76 GB a day
(an upper bound), and 7.78 years with Loki on the SSD, inside the five-year
budget. That is eligibility only; the move itself is a separate owner
decision. Alloy, Prometheus, Pyroscope and Tempo wait for the second window.

### W7 second window result — 2026-10-22

t1 was taken at 2026-10-22T08:57:16+09:00 (window 97,236 s) under
`/home/hyunyoun/storage/ops-snapshots/w7-write-rate-20261021/`. Every store
kept its StartedAt. The owner read SMART after t1:
`Percent_Lifetime_Remain` 24 used and `Total_LBAs_Written` 81,993,720,429
(41,980,784,859,648 bytes). sda wrote 60,772,003,840 bytes, about 54.0 GB a
day, which leaves an SSD baseline of 6.74 years. Each store is `ELIGIBLE`
alone (bytes a day are upper bounds; years are with that store on the SSD):

| Store | Bytes a day | Years |
| --- | --- | --- |
| Tempo | 1.34 GB | 6.58 |
| Prometheus | 4.84 GB | 6.19 |
| Loki | 5.58 GB | 6.11 |
| Alloy | 8.96 GB | 5.78 |
| Pyroscope | 16.82 GB | 5.14 |

The tool judges each store alone. The five-year budget leaves about
18.8 GB a day above the baseline, so all five together give 3.98 years and
are rejected. Loki wrote about 1.76 GB a day in the first window and 5.58 GB
a day in this one, so a margin is kept. The owner decided on 2026-10-22 to
move Tempo and Prometheus (6.05 years together) and keep Loki, Alloy and
Pyroscope on the HDD; `compare-summary.txt` in the window directory holds the
per-store output.

### W7 Tempo and Prometheus move

`PROMETHEUS_DATA_DIR` and `TEMPO_DATA_DIR` override the two volume devices,
as `OLLAMA_MODEL_DIR` does for Ollama; empty keeps the HDD path. Prometheus
holds 7.0 GB and Tempo 39 MB, and the root filesystem has 102 GB free, so the
`HostSystemDiskLow` threshold of 25 GiB is not reached. The procedure follows
W3: the owner runs a first copy while both services run, the agent stops
them, the owner runs a final `rsync --delete` whose dry-run prints nothing,
adds both keys to the local `.env`, removes the two volumes and recreates the
services. Alert rules are not evaluated while Prometheus is stopped, so the
move needs a short window.

```bash
sudo mkdir -p /home/hyunyoun/fast-volumes/obs/prometheus /home/hyunyoun/fast-volumes/obs/tempo
for s in prometheus tempo; do sudo rsync -aHAX --numeric-ids --delete /home/hyunyoun/storage/volumes/obs/$s/ /home/hyunyoun/fast-volumes/obs/$s/; done
for s in prometheus tempo; do sudo rsync -aHAX --numeric-ids --delete --dry-run --itemize-changes /home/hyunyoun/storage/volumes/obs/$s/ /home/hyunyoun/fast-volumes/obs/$s/ | head; done
```

Acceptance: each volume's device is the SSD path, Prometheus answers a query
for a time before the move, Tempo is ready, and both services are healthy.
The HDD copies are removed only after that.

### W7 Tempo and Prometheus move result — 2026-10-22

The owner ran the first copy while both services ran; rsync reported
`file has vanished` for six Tempo `live-store` files (exit 24), which Tempo
removes as it flushes. The agent stopped both at 10:33:32: Prometheus exited 0,
and Tempo was killed after the 60 s timeout (exit 137). The owner ran the final
copy with an empty dry-run, added `PROMETHEUS_DATA_DIR` and `TEMPO_DATA_DIR` to
the local `.env`, removed the two containers and volumes, and recreated both.

Both volumes now bind `/home/hyunyoun/fast-volumes/obs/{prometheus,tempo}`,
and both services are healthy. Prometheus answers `count(up)` for a time three
days before the move (37) and now (65), its head starts at the 2026-10-22 08:00
block boundary, and all 20 rule groups are `ok`. Tempo is `ready`; at startup it
dropped one WAL block without `meta.json`, which on the HDD copy holds a single
0-byte file created at the kill, so no trace data was lost. The firing
`OpenBaoMetricsScrapeFailing` and `OpenBaoAgentMetricsScrapeFailing` predate the
move: the server still runs its pre-TLS listener (RUN-0085 `TLS_PREPARED /
NOT_DEPLOYED`) and the Agent is stopped until W5. Removing the HDD copies
under `/home/hyunyoun/storage/volumes/obs/` is the owner's step.

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
HDD), measured the same way. After criterion 2 passed, the owner removed the
HDD copy at `/home/hyunyoun/storage/volumes/ai/ollama`.

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

### W5 inventory and cleanup

On 2026-10-20, 749 of 830 volumes were dangling, and a recheck before removal
found no container referencing any candidate:

| Group | Count | Size | Content and owner | Decision |
| --- | --- | --- | --- | --- |
| Empty anonymous volumes | 653 | 0 | Test and rehearsal residue, 2026-10-08 to 10-15; no owner | Removed |
| Anonymous volumes with data | 51 | 15.5 GB | LAB run residue, 2026-10-08 to 10-11: Kafka logs (7, 12.9 GB), numbered data directories (30, 1.9 GB), SonarQube, Prometheus, MongoDB; unnamed, so no Compose project can reattach them | Removed at the owner's direction |
| LAB named volumes | 35 | 0 | `hy-home-lab-*` and `s0214loc-*` binds to finished sessions' `/tmp` scratchpads, all missing | Removed |
| `hy-home-infra_*` volumes | 9 | - | Services whose profiles are not running (Kafka 2 and 3, Airflow Valkey, Stalwart, and others); Compose-owned | Kept |
| `owui-prerollout-226` | 1 | - | Open WebUI pre-rollout backup (SPEC-0226) | Kept |

The three `Created` containers (`jolly_fermi`, `busy_austin`, `sharp_joliot`)
from local MCP clients and the superseded `registry:3` image were removed at
the owner's direction; the four exited one-shot provision containers are
Compose-owned and kept. The owner ran the removals. Afterwards 91 volumes
remain, 10 of them dangling (the kept rows), and 58 containers are healthy
with none unhealthy. HDD use fell from 186 GB to 166 GB.

The registry ran `registry:3` (`325b4b29b041`). The agent recreated it from
the Compose pin; it runs `registry:3.1.2@sha256:ddf754342cfc…`, is healthy,
and still lists all 19 archived repositories (the `alpine` manifest returns
HTTP 200). An `alpine:3.22` pulled during the inventory was removed again.

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

### W7 current-evidence reconciliation — 2026-10-22

The second-window and move-result sections above supersede the initial
waiting description for current progress. Their recorded SMART inputs,
97,236 s stable-counter window, individual upper-bound write rates, combined
6.05-year projection, owner selection and successful move are reused below.
The initial NOT_RUN evidence row remains an initial-state observation; no
measurement, migration, historical query or health check was repeated here.
Protected snapshot/compare files and raw runtime logs were not re-read in this
documentation session. The separately scoped later observations carry no
`Resolves` claim against the initial NOT_RUN row; the current Criterion
Acceptance explanation names the later evidence while remaining pending.

Criterion 6 still needs its owner's explicit acceptance of the complete
recorded scope, including the reported Tempo WAL handling and remaining HDD
copies. Their deletion remains the owner's separate exact-path step and is
not authorized by this reconciliation. W6 and criterion 5 wait for criterion
6 acceptance; no operations-policy promotion is performed here. Criteria
1–4 and the accepted GC-floor decision remain unchanged.

### v29 W7 input-boundary correction — 2026-10-22

The direct v29 continuation and completed investigation gate authorize a
source-only correction on baseline
`49fd95a6ed482d7194c840b43b73a030be6f3d5d`. The existing comparison accepted
a changed major:minor under the same device name and accepted negative,
out-of-range, Boolean or nonfinite SMART inputs. These defects were reproduced
with synthetic snapshots; no actual sample or migration was repeated.

The existing parser now preserves major:minor internally while keeping
`parse_diskstats`'s bytes-per-device return contract. A changed identity
invalidates that disk and defers stores using the SSD rate. Malformed,
duplicate or negative counters are input errors. SMART used percentage must
be a finite number in 0–100; supplied host bytes must be a positive finite
integer, excluding Boolean. Missing SMART or zero used percentage still
returns DEFER because the wear slope cannot be estimated; 100 percent used
reports zero projected years and KEEP_HDD. Nonfinite or unrepresentable
calculations fail, and the CLI emits only finite JSON or exits 2 without a
result document. The three snapshot files and prior accounting remain intact.

The unchanged-production RED run counted 28 tests and exited 1 with 22 failing
subcases and three errors across the date and W7 regressions. Focused GREEN
passed all 28 in 0.599 s. After adding a calculation-range boundary case, the
full affected run used official Python 3.14.8 with its existing controller
lock and umask 022:

```sh
/tmp/hyhome-v28-toolchain-venv/bin/python -m unittest \
  tests.validation.test_compose_baseline_gates \
  tests.lib.ops.test_storage_write_rate \
  tests.lib.ops.test_root_resource_assessment \
  tests.validation.test_root_resource_contract -v
```

All seven native-rehearsal opt-ins were explicitly unset as listed in the
P07 correction record. Result: exit 0, 163 tests counted, 133 PASS and
30 native SKIP, 31.727 s. Synthetic CLI cases cover invalid SMART exit 2 with
empty stdout as well as valid/deferred/error results. Scoped Ruff 0.15.12
check and format passed. No native fixture or daemon-changing command ran.

The pinned environment lacks `coverage`; none was installed. A bounded
standard-library `trace` rerun passed 29 tests and measured 82/86 (95.35%)
statement lines across the changed W7 comparison, parser and numeric helpers.
This excludes the unchanged actual collector and does not claim branch or
whole-module coverage. The measured library SHA256 is
`afb7266aecd157af8acf9fa167cd353e42e21eb19e6551a8db6127954ca6bb05`.

Retained mode-0600 receipts are `/tmp/hyhome-v29-resources-red.log` SHA256
`aea436b80bda67f1071266b6d697876dd80474f1b71cc7bffa9a15df24368b48`,
`/tmp/hyhome-v29-resources-green-focused.log` SHA256
`64db5032f078c851326737f1aec4766f7d2e795462fae269087d7ae4238c67c3`,
`/tmp/hyhome-v29-resources-green-full.log` SHA256
`8554f27583544e24a8fdf717c406b757dd42a7a3c3df3fad66926d3ec4c8a3bf`,
and `/tmp/hyhome-v29-resources-coverage.json` SHA256
`eb8f1e6d66bcdd350c46a3a16ea0b37ed90985917f67fbfeb948bb40f926278d`.

The existing format has no boot ID, mount/filesystem binding, collector
identity or input hashes. Equal major:minor and StartedAt therefore cannot
prove complete device/boot/provenance continuity; historical unknowns are
not filled with invented facts. The SMART-based projection remains distinct
from manufacturer-rated TBW and any new lifetime acceptance. Those facts,
current mount/data/query/trace/backup validation, the reported WAL handling,
remaining HDD-copy disposition and explicit criterion 6 owner acceptance are
still scoped residuals. They do not block this input-validation correction.

Existing Evidence and Criterion Acceptance rows, the GC-floor decision and
W7 samples/move receipts are unchanged. Criteria 1–4 stay accepted; criterion
6 remains pending and W6/criterion 5 still waits for it. No host collection,
24-hour measurement, SMART read, copy, prune, migration, recreation, token
operation, remote write or policy promotion ran. Root owns final review,
registered gates and commits.

### Criterion 6 acceptance and W6 policy draft (2026-10-27)

A read-only check showed `hy-home-infra_prometheus-data` and
`hy-home-infra_tempo-data` binding `/home/hyunyoun/fast-volumes/obs/prometheus`
and `/home/hyunyoun/fast-volumes/obs/tempo`, both services healthy, and no
Prometheus or Tempo directory left under the HDD observability path; Loki,
Alloy and Pyroscope remain there. Removing the HDD copies was the owner's
step; this session observed only their absence and holds no record of who
removed them or when. `systemctl show -p RequiresMountsFor,DropInPaths` read
`/home/hyunyoun/storage` for both `docker` (drop-in `10-data-disk.conf`) and
`containerd` (drop-in `storage-mount.conf`). The owner then explicitly accepted
criterion 6. W6 created POL-0102 Host Storage Placement Policy under
`docs/05.operations/policies/10-platform-and-backup/` as a draft, with the
operations-subject high-water raised to 102. Activating it and owner
acceptance of criterion 5 remain.

### Criterion 5 acceptance and POL-0102 activation (2026-10-27)

The owner chose "Accept and activate". POL-0102 moved from draft to active at
version 0.2.0, and its overview now states the current standard. An
independent rules review checked the activation before delivery. Criteria 1–6
are all accepted; the Task's completion transition is left to the owner.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pre-migration snapshot | 1 | W1 | `docker ps -a`, `docker image ls`, `docker volume ls`, `docker info`, `df` | Host state 2026-10-16 | PASS | `/home/hyunyoun/storage/ops-snapshots/containerd-migration-20261016/` | required | - |
| Containerd move | 1 | W1 | Owner procedure and agent comparison against the snapshot | Owner-run host change and r2 snapshot | PASS | Work Log: W1 result | required | - |
| Build-cache limit | 3 | W2 | `daemon.json` parse and `docker buildx du` after a build | Owner-run host change | FAIL | Work Log: W2 result (15.31 GB after a build) | required | - |
| Build-cache floor decision | 3 | W2 | `daemon.json` parse and `docker buildx du` after a build | Owner-accepted policy: GC enabled with a 10 GB reserved-space floor, observed in `docker buildx inspect` | PASS | Work Log: W2 result | required | Build-cache limit |
| Ollama SSD move | 2 | W3 | Rendered device, model list, first-load time before and after | Compose change and owner copy | PASS | Work Log: W3 result (318.4 s to 55.9 s) | required | - |
| Image archive | 3 | W4 | Push, stored-digest comparison, local removal | 16 approved candidates | PASS | Work Log: W4 image archive (15 archived, 1 push failure left in place) | required | - |
| Volume and container cleanup | 3 | W5 | Ownership inventory and removal of unowned items | Host state after W1 | PASS | Work Log: W5 inventory and cleanup (739 removed, 10 kept) | required | - |
| Registry pin | 4 | W5 | Running image digest equals the Compose pin | Running `registry:3` versus pinned `registry:3.1.2@sha256:ddf754342cfc…` | PASS | Work Log: W5 inventory and cleanup | required | - |
| Observability store placement | 6 | W7 | SMART counters, per-store write rate, keep-or-move decision | Disk load analysis; first window (t0 2026-10-19T23:51:52, t1 2026-10-21T05:56:08) Loki ELIGIBLE with SMART (7.78 years), four stores DEFER; second window t0 2026-10-21T05:56:40 | NOT_RUN | Work Log: Disk load analysis | required | - |
| Policy promotion | 5 | W6 | Changed metadata and link checks | Operations owner document | NOT_RUN | Work Log | required | - |
| W7 second-window placement decision | 6 | W7 | Reuse the documented stable-counter sample, SMART values and owner selection | 2026-10-21 05:56:40 to 2026-10-22 08:57:16 +09:00; 97,236 s; SMART 24 percent used and 81,993,720,429 LBAs; Tempo and Prometheus selected, combined projection 6.05 years; Loki/Alloy/Pyroscope retained on HDD; raw files not re-read | PASS | W7 second window result — 2026-10-22; W7 current-evidence reconciliation — 2026-10-22 | required | - |
| W7 selected-store SSD move | 6 | W7 | Reuse the documented owner copy, bounded recreation, data query and health results | Recorded 2026-10-22 move; SSD bind devices, both services healthy; Prometheus historical count(up) 37 and current 65, 20 rule groups ok; Tempo ready and one empty WAL block dropped; HDD copies retained for owner handling | PASS | W7 Tempo and Prometheus move result — 2026-10-22; W7 current-evidence reconciliation — 2026-10-22 | required | - |
| Observability store placement second window | 6 | W7 | SMART counters, per-store write rate, keep-or-move decision | Second stable window 2026-10-21T05:56:40 to 2026-10-22T08:57:16 +09:00 with SMART counters; owner kept Loki, Alloy and Pyroscope on HDD and moved Tempo and Prometheus | PASS | W7 second-window placement decision; #criterion-6-acceptance-and-w6-policy-draft-2026-10-27 | required | Observability store placement |
| C6 owner acceptance | 6 | W7 | Read-only `docker volume inspect` and health check, HDD observability path listing, then explicit owner acceptance | 2026-10-27 main d6164df8e | PASS | #criterion-6-acceptance-and-w6-policy-draft-2026-10-27; SSD devices, healthy services, former HDD copies absent | required | - |
| W6 policy draft | 5 | W6 | Changed-document metadata, operations catalog and all-link checks | POL-0102 draft and operations-subject high-water 102; independent review findings applied | PASS | `run-ci-gate.py --profile changed` exit 0 on base d6164df8e: metadata changed 3/0 violations, links 11,861/0 failures, operations-catalog PASS; activation and criterion 5 acceptance remain | required | - |
| Policy promotion activation | 5 | W6 | Changed metadata and link checks | POL-0102 status draft to active with owner approval and independent rules review | PASS | #criterion-5-acceptance-and-pol-0102-activation-2026-10-27 | required | Policy promotion |
| C5 owner acceptance | 5 | W6 | Explicit owner acceptance after the active policy review | Owner decision 2026-10-27 | PASS | #criterion-5-acceptance-and-pol-0102-activation-2026-10-27 | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | Pre-migration snapshot, Containerd move | Health, images, and k3d nodes match the r2 snapshot on 2026-10-19. | SPEC-0246 TSK-0001 |
| 2 | accepted | Ollama SSD move | Same model list from the SSD path; first load 318.4 s before and 55.9 s after. | SPEC-0246 TSK-0001 |
| 3 | accepted | Build-cache limit, Build-cache floor decision, Image archive, Volume and container cleanup | Floor accepted, archive digest-verified, and only unowned items removed. | SPEC-0246 TSK-0001 |
| 4 | accepted | Registry pin | The running image digest equals the Compose pin. | SPEC-0246 TSK-0001 |
| 5 | accepted | W6 policy draft, Policy promotion activation, C5 owner acceptance | Owner accepted on 2026-10-27; POL-0102 is active after an independent rules review. | SPEC-0246 TSK-0001 |
| 6 | accepted | W7 second-window placement decision, W7 selected-store SSD move, C6 owner acceptance | Owner accepted on 2026-10-27 after read-only verification: Prometheus and Tempo volumes bind SSD `fast-volumes/obs/*`, both healthy, former HDD copies absent; Loki, Alloy and Pyroscope stay on HDD. | SPEC-0246 TSK-0001 |

## Review and Completion

This Task was issued `draft` in PR #512; the pre-migration snapshot and W4 make it `in-progress`. It completes only when every criterion is
accepted on direct host observation; a hosted CI result does not prove a host
change.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
