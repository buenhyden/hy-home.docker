---
title: "AI Infrastructure Architecture Description"
version: "1.2.2"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-14"
layer: "architecture"
artifact_id: "AD-0008"
parent_ids:
- "REQ-0009"
created: "2026-03-26"
---

# AI Infrastructure Architecture Description

## Overview

### Purpose and Readers

`08-ai` owns privacy-preserving local inference and the interfaces that use
it: GPU allocation, service boundaries and data flow for local LLM inference,
RAG chat, image workflows, knowledge notebooks, experiment tracking and web
extraction. Local inference uses NVIDIA GPUs; provider or API egress needs
separate authorization.

### System Boundary

- **Owns:** Ollama inference and its model store; Open WebUI chat and RAG;
  ComfyUI and its declared workflow mounts; Open Notebook with its nested
  SurrealDB; MLflow tracking and its feature-owned PostgreSQL provisioning;
  Crawl4AI with its separate egress gateway.
- **Consumes:** GPUs through the NVIDIA Container Toolkit; `mng-pg` and
  SeaweedFS for MLflow metadata and artifacts; Keycloak for SSO; shared Qdrant
  only for consumers explicitly configured for it.
- **Does not own:** the Qdrant instance (`04-data`), the monitoring collectors
  (`06-observability`), or Jupyter notebooks (Analytics LAB).
- **Non-goals:** multi-node GPU clusters and model training environments.

## Context and Constraints

### Context

Users reach Open WebUI, ComfyUI, Open Notebook and MLflow through the gateway. The tier consumes GPUs through the NVIDIA Container Toolkit, `mng-pg` and SeaweedFS for MLflow, Keycloak for SSO, and Qdrant only for explicitly configured consumers. Crawl4AI reaches the internet only through `crawl4ai-egress`.

### Constraints

Local inference uses NVIDIA GPUs, and provider or API egress needs separate authorization. Multi-node GPU clusters and model training environments are non-goals; Compose resource declarations are source limits, not measured shared-GPU headroom.

## Current Structure

### Building Blocks

1. **Inference:** `ollama` controls the model store and the GPU (NVIDIA device
   reservation) and serves an OpenAI-compatible API; `ollama-exporter` exports
   its metrics.
2. **Interaction:** `open-webui` runs chat and RAG (embed, search, augment).
   `VECTOR_DB` is unset, so vectors stay in its local Chroma store, not Qdrant.
3. **Image:** `comfyui` uses `gpus: all`.
4. **Knowledge and experiments:** `open_notebook` with `surrealdb`; `mlflow`
   with `mlflow-db-provision`.
5. **Extraction:** `crawl4ai` reaches the internet only through
   `crawl4ai-egress`.

Local Ollama is the current source-default model path. An Ollama-mediated
cloud path and a direct cloud path are separate future contracts, not a
fallback or an authorized egress path. Stored product-provider state was not
read and is `UNKNOWN`. Consumers use the Ollama API and never touch model
weights or the GPU driver. The proposed Notebook registration names
`gemma4:e2b` for chat and `embeddinggemma-2:740m` for 768-dimensional
embeddings; the declaration does not prove either model is downloaded,
registered or working.

### Runtime and Deployment

#### Runtime View

```text
User prompt -> Open WebUI (RAG context) -> Ollama (inference) -> streamed response
```

- The Compose declaration owns the Ollama model-store mount at
  `${DEFAULT_AI_MODEL_DIR}/ollama`; no successful model-store recovery is
  asserted.
- Open WebUI SQLite, uploads and local Chroma live in its data volume.
- ComfyUI mounts its `models`, `custom_nodes`, `input`, `output` and `user`
  volumes at `/root/ComfyUI/<dir>`, where the image runs; the data moved there
  on 2026-11-08. Its Hugging Face and Torch caches mount separately under
  `/home/comfyui/.cache`.
- Open Notebook recovery coordinates app data, SurrealDB and its encryption
  key. MLflow coordinates `mng-pg` metadata with SeaweedFS artifacts.

#### Deployment View

`ai` selects Ollama with its exporter, Open WebUI, ComfyUI and Qdrant;
`ai-llm` selects Ollama, Open WebUI and Qdrant; `ollama` selects Ollama and
its exporter; `ai-image` selects ComfyUI. These are HOME. `notebook` (Open
Notebook and SurrealDB, SurrealDB also by `surrealdb`), `mlops` and
`data-science` (MLflow) and `crawl4ai` are optional capability profiles; `ai`
does not select them. Compose resource declarations are source limits, not
measured shared-GPU headroom.

## Interfaces

### Contracts

Ollama serves an OpenAI-compatible API that consumers use instead of touching model weights or the GPU driver. Open WebUI uses native OIDC; Ollama, ComfyUI and the MLflow browser route use ForwardAuth; Open Notebook uses password-file authentication with an admin IP allow list.

### Failure Boundaries

MLflow's SDK path is not authenticated like its browser route (see Risks below). Health checks are process and application signals and do not alone restart a container or prove recovery; Open Notebook and MLflow recovery are coordinated as described under Runtime View.

## Decisions

### Decision Links

- [ADR-0008 Ollama and Open WebUI local AI](../decisions/0008-ollama-openwebui-local-ai.md)

### Quality and Risks

#### Quality Attributes

- **Performance:** CUDA acceleration and quantization are workload choices; no
  measured latency or shared-GPU capacity is established.
- **Security:** Open WebUI uses native OIDC; Ollama, ComfyUI and the MLflow
  browser route use ForwardAuth; Open Notebook uses password-file
  authentication with an admin IP allow list. Crawl4AI egress and loopback
  publications keep their explicit boundaries.
- **Reliability:** health checks are process and application signals; an
  unhealthy status alone neither restarts a container nor proves recovery.
- **Scalability:** more worker or GPU capacity needs approved resource and
  topology changes; there is no automatic scaling.
- **Observability:** `ollama-exporter` reports model and API metrics; VRAM is
  covered by `dcgm-exporter` under `obs-gpu`.

#### Risks

- MLflow's SDK path on `edge_net`, `ai_net`, `mng_data_net` and `object_net`
  is not authenticated like its browser route.
- `ai` and `ai-llm` start Qdrant although Open WebUI does not use it.

## Traceability

### Requirement Mapping

- [REQ-0009 AI requirements](../../01.requirements/0009-ai.md)

### Currentness and Lineage

- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- This document carries the SPEC-0267 secondary-listener hardening outcome; that package is retired and its body is in version history.

#### Evolution

Switching Open WebUI to Qdrant or enabling a cloud model path each needs a
Stage 03 change and egress approval.
