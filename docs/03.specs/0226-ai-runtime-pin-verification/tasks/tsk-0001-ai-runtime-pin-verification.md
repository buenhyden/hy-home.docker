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
| Registry index digest | `sha256:1bef6397…e1687`, linux/amd64 and arm64 | `sha256:61fabfa0…747b1`, linux/amd64 and arm64 |
| HOME image ID | Same digest | Same digest |
| Previous tag (rollback reference) | 0.35.0 `sha256:2a6e883b…25d01` | v0.11.3-cuda `sha256:f27666b8…bae6` |
| Licence | MIT | Open WebUI licence (repository reports NOASSERTION) |
| Upstream advisories affecting the pin | 0 of 16 (GitHub advisory database) | 0 of 194 (repository and pip advisories); four medium-to-high ones are fixed in 0.11.4 |
| CUDA | GTX 1060, compute 6.1: `cuda_v13` skips it, `cuda_v12` runs it; driver 580.178.04, CUDA 13.0 | No GPU device; `torch.cuda.is_available()` is `False` |

Image-layer scanning with the repository's pinned Grype did not run: its
database download needs the `Grype DB network approval: confirmed` line in
`infra/supply-chain.network-approvals.md`, which is not on file.

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
`OLLAMA_LOAD_TIMEOUT=15m`, a queue of 16 and `OLLAMA_NO_CLOUD=1`, keeps two
parallel slots and one loaded model, and Open WebUI waits 960 s.

### W3 Backup and Restore

`ai/ollama/models/manifests` and `manifests-v2` join the restic state set; the
blobs stay out and are re-pulled by digest. The running Open WebUI kept its
session key only in the container layer (`/app/backend/.webui_secret_key`),
because the key-file fix of `06d2a8953` merged after the container was created
on 2026-10-08, so the state set's key entry found no file.

The isolated rehearsal copied an online SQLite backup, the uploads and the
live key into a new volume without writing them to the host, started the
pinned image there with no network and a dummy OIDC secret, and restored the
Ollama manifests into another volume:

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

Pending.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Source facts | 1 | W1 | Registry, release, licence and advisory queries; Ollama GPU log | `c3ce31973` | PASS | W1 Source Facts | accepted |
| Image scan | 1 | W1 | Pinned Grype | — | NOT_RUN | W1 Source Facts | pending |
| Pins and limits | 2 | W2 | Contract tests; Compose rendering; version sync | `41a711771` | PASS | W2 Pins and Limits | accepted |
| Restore | 3 | W3 | Isolated SQLite, upload, key and catalog restore | `2ac1db09c` | PASS | W3 Backup and Restore | accepted |
| Features | 4 | W4 | Isolated feature rehearsal; GPU measurement; gateway checks | `2ac1db09c` | PASS | W4 Features | accepted |

## Review and Completion

Not complete: the HOME rollout, the owner's sign-in canary and validation
remain.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
