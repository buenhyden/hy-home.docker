---
title: "AI Runtime Pin Verification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0226"
parent_ids:
- "REQ-0009"
- "REQ-0013"
- "AD-0008"
- "AD-0013"
created: "2026-10-10"
---

# AI Runtime Pin Verification

## Overview

The owner asked for `ollama/ollama:0.40.0` and
`ghcr.io/open-webui/open-webui:v0.11.4-cuda`, and for verification instead of
a duplicate change when the tags are already applied. Both tags were merged
earlier and run on HOME, but no record covered the registry digest, upstream
advisories, the wrapper and OIDC behaviour on the new image, a tested restore,
CUDA use, GPU memory or the user-facing features. Measuring them found that
Ollama model loads from the shared HDD exceed Ollama's default load timeout,
and that the Open WebUI secret-key fix had never reached the running
container.

## Scope

In scope: the Ollama and Open WebUI Compose services, their version
projection and Renovate tracking, Ollama load and queue limits, the Open WebUI
secret key and persisted settings, the restic state set for both, isolated
restore and feature rehearsals, the GPU memory measurement, the affected
Stage 05 documents and the HOME rollout of these two services. Out of scope:
moving the model store off the HDD, changing the embedding model, ComfyUI
settings and the OIDC client in Keycloak.

## Contracts

1. Identity. Each image is pinned as the requested tag plus its registry index
   digest; the declared reference, the running image and the binary or
   package version agree. The previous tags' digests are kept as rollback
   references.
2. Load limits. Ollama allows a 15 minute model load, queues at most 16
   requests and has ollama.com cloud models off; Open WebUI waits longer than
   one cold load. `OLLAMA_NUM_PARALLEL` 2 and `OLLAMA_MAX_LOADED_MODELS` 1
   stay, because one slot did not make the largest model fit in VRAM.
3. Open WebUI state. The session key lives in the data volume and is backed
   up; Compose environment values are not silently overridden by empty rows
   left by a migration; no GPU device, Docker socket or terminal server is
   exposed. The CUDA image runs without a GPU and its local GPU features are
   unused.
4. Recovery. The SQLite database (online backup), uploads and key restore into
   a separate volume and start on the pinned image; the Ollama manifest
   catalog restores with identical model digests, and blobs are re-pulled by
   digest. Image rollback and data restore are separate steps.

## Acceptance Criteria

1. The tags, registry digests, running images, versions, licences, upstream
   advisories and CUDA prerequisites are recorded, with any check that could
   not run and its reason.
2. Compose, the version projection and Renovate carry the digest pins and the
   load, queue and cloud limits, and contract tests cover them.
3. An isolated restore of Open WebUI and of the Ollama catalog matches HOME,
   and the backup set includes the key and the catalog.
4. An isolated Open WebUI on the pinned image passes model list, streaming
   chat, cancel, RAG upload, query and delete, cross-user isolation and the
   Socket.IO handshake against HOME Ollama; GPU memory per model is measured.
5. HOME runs both services from the pinned references with the existing
   session key and sign-in settings; steps that need the owner are NOT_RUN.
6. The changed gate, the staged style check and `candidate-quality` pass.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-ai-runtime-pin-verification.md)
