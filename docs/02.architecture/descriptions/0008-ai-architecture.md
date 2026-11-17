---
title: "AI Infrastructure Architecture Description"
version: "1.3.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "architecture"
artifact_id: "AD-0008"
parent_ids:
- "REQ-0009"
created: "2026-03-26"
---

# AI Infrastructure Architecture Description

## Context and Boundaries

### System Boundary

- **Owns:** HOME Ollama inference and its model store;
  ComfyUI and its declared workflow mounts; Open Notebook with its nested
  SurrealDB; MLflow tracking and its feature-owned PostgreSQL provisioning;
  Crawl4AI with its separate egress gateway.
- **Consumes:** GPUs through the NVIDIA Container Toolkit; `mng-pg` and
  SeaweedFS for MLflow metadata and artifacts; Keycloak for SSO; shared Qdrant
  only for consumers explicitly configured for it.
- **Does not own:** the independent Open WebUI LAB, the Qdrant instance
  (`04-data`), the monitoring collectors (`06-observability`), or Jupyter
  notebooks (Analytics LAB).
- **Non-goals:** multi-node GPU clusters and model training environments.

#### Purpose and Readers

`08-ai` owns privacy-preserving local inference and the interfaces that use
it: GPU allocation, service boundaries and data flow for local LLM inference,
RAG chat, image workflows, knowledge notebooks, experiment tracking and web
extraction. Local inference uses NVIDIA GPUs; provider or API egress needs
separate authorization.

#### Context

The root Compose declares gateway routes for ComfyUI, Open Notebook and MLflow when their optional profiles are selected. The tier consumes GPUs through the NVIDIA Container Toolkit, `mng-pg` and SeaweedFS for MLflow, Keycloak for SSO, and Qdrant only for explicitly configured consumers. Crawl4AI reaches the internet only through `crawl4ai-egress`. The independent Open WebUI LAB requires a separately approved and reachable Ollama endpoint.

### Constraints

Local inference uses NVIDIA GPUs, and provider or API egress needs separate authorization. Multi-node GPU clusters and model training environments are non-goals; Compose resource declarations are source limits, not measured shared-GPU headroom.

## Structure

### Building Blocks

1. **Inference:** `ollama` controls the model store and the GPU (NVIDIA device
   reservation) and serves an OpenAI-compatible API; `ollama-exporter` exports
   its metrics.
2. **LAB neighbor:** [Open WebUI](0013-open-webui-architecture.md) evaluates
   chat and RAG with its own local vector store and isolated data root.
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

### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Ollama OpenAI-compatible API | `ollama` | Authorized callers and configured consumers | OpenAI-compatible API behind ForwardAuth | The description records no failure handling for this interface. |
| Ollama metrics | `ollama-exporter` | The description names no consumer for this interface. | The description links no contract for this interface. | The description records no failure handling for this interface. |
| ComfyUI gateway route | `comfyui` | The description names no consumer for this interface. | ForwardAuth | The description records no failure handling for this interface. |
| Open Notebook gateway route | `open_notebook` | The description names no consumer for this interface. | Password-file authentication with an admin IP allow list | The description records service-level recovery only: Open Notebook recovery coordinates app data, SurrealDB and its encryption key. |
| MLflow browser route and SDK path | `mlflow` | The description names no consumer for this interface. | ForwardAuth for the browser route only | The description records service-level recovery only: MLflow coordinates `mng-pg` metadata with SeaweedFS artifacts. |
| Crawl4AI internet egress | `crawl4ai-egress` | `crawl4ai` | The description links no contract for this interface. | The description records no failure handling for this interface. |
| GPU access | NVIDIA Container Toolkit | `ollama` and `comfyui` | NVIDIA device reservation and `gpus: all` | The description records no failure handling for this interface. |
| Keycloak SSO | Keycloak (`02-auth`) | The description names no consumer for this interface. | The description links no contract for this interface. | The description records no failure handling for this interface. |
| Qdrant vector store | Qdrant (`04-data`) | Consumers explicitly configured for it | The description links no contract for this interface. | The description records no failure handling for this interface. |

Ollama serves an OpenAI-compatible API that consumers use instead of touching model weights or the GPU driver. The Open WebUI LAB declares native OIDC. Ollama, ComfyUI and the MLflow browser route use ForwardAuth. Open Notebook uses password-file authentication with an admin IP allow list.

## Runtime Behavior

### Normal Flow

#### Runtime View

```text
Authorized caller -> approved Ollama endpoint (inference or embedding) -> response
```

- The Compose declaration owns the Ollama model-store mount at
  `${DEFAULT_AI_MODEL_DIR}/ollama`; no successful model-store recovery is
  asserted.
- The isolated LAB owns Open WebUI state and its access and deployment conditions.
- ComfyUI mounts its `models`, `custom_nodes`, `input`, `output` and `user`
  volumes at `/root/ComfyUI/<dir>`, where the image runs; the data moved there
  on 2026-11-08. Its Hugging Face and Torch caches mount separately under
  `/home/comfyui/.cache`.
- Open Notebook recovery coordinates app data, SurrealDB and its encryption
  key. MLflow coordinates `mng-pg` metadata with SeaweedFS artifacts.

#### Deployment View

`ai` and `ai-llm` select the HOME Ollama, its exporter and Qdrant. `ollama` selects
Ollama and its exporter. `ai-image` explicitly selects the optional root ComfyUI.
Its standalone LAB placement remains planned. `notebook` (Open
Notebook and SurrealDB, SurrealDB also by `surrealdb`), `mlops` and
`data-science` (MLflow) and `crawl4ai` are optional capability profiles; `ai`
does not select them. Compose resource declarations are source limits, not
measured shared-GPU headroom.

### Failure and Recovery

MLflow's SDK path is not authenticated like its browser route (see Risks below). Health checks are process and application signals and do not alone restart a container or prove recovery; Open Notebook and MLflow recovery are coordinated as described under Runtime View.

## Quality Scenarios

### Scenarios

#### Quality Attributes

- **Performance:** CUDA acceleration and quantization are workload choices; no
  measured latency or shared-GPU capacity is established.
- **Security:** The Open WebUI LAB declares native OIDC. Ollama, ComfyUI and the MLflow
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
- `ai` and `ai-llm` select Qdrant. Treat use by any given consumer as a
  separate configuration and runtime question.

### Trade-offs

- Local Ollama inference on NVIDIA GPUs is the source-default model path for
  privacy-preserving inference; provider or API egress needs separate
  authorization, and cloud paths are separate future contracts, not a
  fallback (Purpose and Readers, Building Blocks, Evolution).
- Multi-node GPU clusters, model training and automatic scaling are not
  provided; more capacity needs approved resource and topology changes, and no
  measured latency or shared-GPU capacity is established (Constraints,
  Quality Attributes).
- MLflow's SDK path on `edge_net`, `ai_net`, `mng_data_net` and `object_net`
  is not authenticated like its browser route (Risks).

## Decisions and Adoption

### Decisions

- [ADR-0008 original local AI decision](../decisions/0008-ollama-openwebui-local-ai.md)
- [ADR-0062 current HOME and LAB membership](../decisions/0062-home-lab-membership.md)

### Adoption Boundaries

#### Requirement Mapping

- [REQ-0009 AI requirements](../../01.requirements/0009-ai.md)

#### Currentness and Lineage

- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- This document carries the SPEC-0267 secondary-listener hardening outcome; that package is retired and its body is in version history.

#### Evolution

Switching Open WebUI to Qdrant or enabling a cloud model path each needs a
Stage 03 change and egress approval.
