---
title: "AI Runtime Pin Verification Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0226-TSK-0001"
parent_ids:
- "SPEC-0226-PLAN-0001"
created: "2026-10-10"
---

# AI Runtime Pin Verification Task

## Objective

Verify, pin and bound the requested Ollama and Open WebUI images, prove their
backup and feature paths in isolation and bring HOME in line.

## Inputs and Authorization

The owner's prompt 15 asks for `ollama/ollama:0.40.0` and
`ghcr.io/open-webui/open-webui:v0.11.4-cuda` and, where they are already
applied, verification instead of a duplicate change; on 2026-10-10 the owner
said to continue. Both tags were on `main` (SPEC-0212 item 18) and HOME had
run them for 27 hours. HOME steps recreate only `ollama` and `open-webui`.

## Work Log

### W1 Source Facts

| Item | Ollama | Open WebUI |
| --- | --- | --- |
| Release | v0.40.0, 2026-09-25 (v0.40.2 is newer; not taken, the tag is the owner's) | v0.11.4, 2026-09-21, latest |
| Registry index digest | `sha256:1bef639749741b375e9a1eb2c1346fb57ce52f5432de1f74846e44ccc18e1687`, linux/amd64 and arm64 | `sha256:61fabfa095801b4f0cf4de7320edc1e2ac9a011b41ddadbba20fe3542e7747b1`, linux/amd64 and arm64 |
| HOME image ID | Same digest | Same digest |
| Previous tag (rollback reference) | 0.35.0 `sha256:2a6e883b917fc543389599dae79918f5cac9e1438890506982f44aa4f5625d01` | v0.11.3-cuda `sha256:f27666b889001e1d2c639ca4af527aad6e466bd1a1ac70cae5ce13dfe35ebae6` |
| Licence | MIT | Open WebUI licence (repository reports NOASSERTION) |
| Upstream advisories affecting the pin | 0 of 16 (GitHub advisory database) | 0 of 194 (repository and pip advisories); four medium-to-high ones are fixed in 0.11.4 |
| CUDA | GTX 1060, compute 6.1: `cuda_v13` skips it, `cuda_v12` runs it; driver 580.178.04, CUDA 13.0 | No GPU device; `torch.cuda.is_available()` is `False` |

Image-layer scanning with the repository's pinned Grype did not run: its
database download needs the `Grype DB network approval: confirmed` line in
`infra/supply-chain.network-approvals.md`, which is not on file.

On 2026-10-10 (SPEC-0229) the pinned Grype scanned both saved images offline
against a database built 2026-10-09. The scan ran; the risk decision on its
findings is the owner's:

| Image | Critical | High | Medium | Low/negligible/unknown | Notes |
| --- | --- | --- | --- | --- | --- |
| Ollama | 2 | 20 | 94 | 30 | All Critical and High are Go modules in the binary (`golang.org/x/crypto` v0.43.0, the Go 1.26.0 standard library, `x/image`, `x/text`); each is fixed upstream, so it needs a newer Ollama build |
| Open WebUI (CUDA) | 72 | 530 | 476 | 902 | 490 Critical/High are Debian 12 packages (431 won't-fix or not yet fixed); the fixable Python and binary ones include `pypdf`, `cryptography`, `pyjwt`, `unstructured`, `sentence-transformers`, bundled `ffmpeg`, Python 3.11.16 and Node 24.15, all needing a newer image |

Grype does not show whether a vulnerable path is reachable in these services.

Open WebUI v0.11.3 and v0.11.4 have the same 58 migrations and head
`d4c1a8e37b62`, so an image-only rollback needs no data restore.

### W2 Pins and Limits

Both Compose images became `tag@sha256:<index digest>`; the version
projection and Renovate's Compose file list follow. Measured on HOME:

| Model | Load | Total | VRAM | Context |
| --- | --- | --- | --- | --- |
| `tev1:0.8b` | 33 s | 0.83 GiB | 0.83 GiB | 2,050 |
| `qwen3-embedding:4b` | 12-242 s | 4.07 GiB | 4.07 GiB | 4,096 |
| `qwen3:8b` | 229 s; twice HTTP 500 at the 5 m timeout | 6.12 GiB | 4.75 GiB | 4,096 |

The model store is on the HDD `sdb`, measured at 99 % utilisation with
Ollama reading about 3 MB/s; a 12 GiB container limit did not help (HTTP 500
at 303 s) and a single parallel slot left `qwen3:8b` partly on the CPU
(4.68 of 5.56 GiB, 574 s load, 13.8 tokens/s). Ollama therefore gets
`OLLAMA_LOAD_TIMEOUT=15m` (its stall limit for a load, per the v0.40.0
source), a queue of 16 and `OLLAMA_NO_CLOUD=1`, and keeps two parallel slots
and one loaded model. Open WebUI 0.11.4 applies no total aiohttp timeout when
`AIOHTTP_CLIENT_TIMEOUT` is unset (`None`; 300 only for an invalid value), so
the review's finding led to removing the 960 s value, which would have cut
off long streamed answers.

### W3 Backup and Restore

`ai/ollama/models/manifests` and `manifests-v2` join the restic state set; the
blobs stay out. `ollama pull` fetches by name and tag, so after a loss each
model is pulled again by name and its digest is compared with the restored
manifest; a tag that has moved upstream shows up as a mismatch rather than
being accepted silently. The re-pull itself was not rehearsed. The running Open WebUI kept its
session key only in the container layer (`/app/backend/.webui_secret_key`),
because the key-file fix of `06d2a8953` merged after the container was created
on 2026-10-08, so the state set's key entry found no file.

The isolated rehearsal copied an online SQLite backup, the uploads and the
live key straight from the running container into a new volume without
writing them to the host, started the pinned image there with no network and a
dummy OIDC secret, and copied the Ollama manifest trees from the model
directory into another volume. It proves the restored data starts; it did not
go through a restic snapshot:

| Check | HOME | Restored |
| --- | --- | --- |
| Alembic head | `d4c1a8e37b62` | `d4c1a8e37b62` |
| Users, chats, files, config rows | 1, 0, 0, 352 | 1, 0, 0, 352 |
| Session key | Container layer | Loaded from the volume file |
| Health | — | `{"status":true}` |
| Ollama models and digests | 5 | Identical 5 |

### W4 Features

An isolated Open WebUI on the pinned image, with a fresh volume and two local
test accounts, used HOME Ollama over `ai_net`:

| Check | Result |
| --- | --- |
| Model list | 6 entries, all HOME models plus the arena model |
| Streaming chat | 200, `text/event-stream`, 2,248 chunks in 54.5 s; `tev1` streams its reasoning in `thinking` first |
| Cancel | Stream closed after 5 chunks; the next request returned 200 |
| RAG | Upload 200, embedding with `qwen3-embedding:4b` completed in 127 s, retrieval returned the test codeword |
| Isolation | The second user got 404 reading, downloading and deleting the first user's file |
| Delete | Owner delete 200, then 404 |
| Unauthenticated model list | 401 |
| Socket.IO | Polling refused by design (WebSocket only); the WebSocket upgrade returns 101 in the container and through the gateway |
| Exporter | `ollama-exporter` target up, 54 series |

Through the gateway, `/health` returned 200 and `/oauth/oidc/login` redirected
to Keycloak's authorisation endpoint. Persisted settings matched Compose for
the login form, signup, Ollama URL and embedding engine and model;
`webui.url` was an empty row left by the per-key config migration, which hides
`WEBUI_URL`. No Docker socket, terminal server or GPU device is configured.

### W5 HOME Rollout

Run from `15ccd7d35` on 2026-10-10 (KST), recreating only `ollama` and
`open-webui`:

| Step | Result |
| --- | --- |
| Rollback data | Online SQLite backup and the running key in the Docker volume `owui-prerollout-226`; previous checkout `b2745167d` |
| Key | Running key copied into the data volume (mode 600); byte-identical to the backup after recreation; log reads it from `/app/backend/data/.webui_secret_key` |
| `.env` | `OLLAMA_MAX_QUEUE` value 128 → 16; key set unchanged |
| Persisted setting | With Open WebUI stopped, the empty `webui.url` row was removed; on start Open WebUI stored the Compose `WEBUI_URL` there |
| Recreation | Both healthy; image IDs equal the pinned digests; `ollama --version` 0.40.0, `/api/version` 0.11.4 |
| Ollama settings | Load timeout 15 m, queue 16, cloud off, 2 slots, 1 loaded model; CUDA compute 6.1 on `cuda_v12` |
| Open WebUI state | Login form and signup off, Ollama URL and embedding model unchanged, 1 user, 352 config rows, no error lines |
| Canary | Open WebUI to Ollama 200; gateway health 200; WebSocket 101; OIDC redirect to the registered callback with S256; `tev1` inference 200 in 3.5 s on the GPU; exporter up |

After the review, Open WebUI alone was recreated again from `9f1b570f9` to drop
`AIOHTTP_CLIENT_TIMEOUT`: healthy on the same digest, the variable absent, the
key read from the volume and byte-identical to the backup, gateway health 200.

The sign-in, sign-out and token refresh of a real user through Keycloak need
the owner's browser session and were not run.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Source facts | 1 | W1 | Registry, release, licence and advisory queries; Ollama GPU log | `c3ce31973` | PASS | W1 Source Facts | accepted |
| Image scan | 1 | W1 | Pinned Grype, offline, DB built 2026-10-09 (SPEC-0229) | `32fb2e69d` | PASS | W1 Source Facts | pending |
| Pins and limits | 2 | W2 | Contract tests; Compose rendering; version sync | `41a711771` | PASS | W2 Pins and Limits | accepted |
| Restore | 3 | W3 | Isolated SQLite, upload, key and catalog restore | `2ac1db09c` | PASS | W3 Backup and Restore | accepted |
| Features | 4 | W4 | Isolated feature rehearsal; GPU measurement; gateway checks | `2ac1db09c` | PASS | W4 Features | accepted |
| Restic snapshot contents | 3 | W3 | State-set backup, then listing the key and catalog paths | — | NOT_RUN | W3 Backup and Restore | pending |
| HOME rollout | 5 | W5 | Key, setting, version, health and gateway checks | `15ccd7d35` | PASS | W5 HOME Rollout | accepted |
| Owner sign-in canary | 5 | W5 | Owner-attested report; Traefik and Keycloak logs | `f75275651` | PASS | Review and Completion | accepted |
| Hardening baseline | 6 | W6 | `check-all-hardening.sh` | `16c4794a8` | PASS | Review and Completion | accepted |
| Changed gate | 6 | W6 | `run-ci-gate.py --profile changed --local-only`, base `c3ce31973` | `16c4794a8` | PASS | Review and Completion | accepted |
| Staged style check | 6 | W6 | `run-ci-precommit.sh --mode local-staged` over `c3ce31973..HEAD` | `16c4794a8` | PASS | Review and Completion | accepted |
| Remote candidate | 6 | W6 | `candidate-quality` run 37965521891, base `c3ce31973` | `9ff118f08` | PASS | Review and Completion | accepted |

## Review and Completion

An independent review found no critical issue and two important ones (rollback
digests truncated; restore evidence not through restic and re-pull untested)
plus eight minor ones; `9f1b570f9` resolves them or records them as NOT_RUN.
The first changed-gate run failed one file-mode test because the worktree was
checked out with umask 002 (Git records mode 755); with group write removed
locally the gate passed (rc 0). The first `candidate-quality` run (run
37964682882, head `7d74231f9`) failed the operations catalog: the generated
service inventory still listed the old Ollama environment keys. The local
`--local-only` gate does not run that check; the re-rendered inventory passes
`check-operations-catalog.py`. Run 37965521891 passed on head `9ff118f08`
and PR #402 merged as `1f552ac78` (recorded with SPEC-0228). The nightly
backup of 2026-10-10 skipped Restic because the state repository exceeded
its budget (SPEC-0228), so no snapshot yet holds the key and catalog.
On 2026-10-10 the owner reported the Keycloak sign-in check complete. The logs
cannot corroborate a fresh OIDC flow: Traefik, which logs every request, shows
no `/oauth/oidc/login` or callback for Open WebUI after the rollout other than
the two redirect checks of W4 and W5; Open WebUI writes no access log; and
Keycloak logs only error events. The check therefore rests on the owner's
report, which is consistent with an existing session (four-week JWT) still
being accepted after recreation. Not complete: the restic snapshot listing
(first possible on the 2026-10-11 run) and the owner's decision on the scan
findings remain.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
