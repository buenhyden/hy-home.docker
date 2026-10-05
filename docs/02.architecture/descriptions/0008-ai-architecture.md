---
title: "AI Infrastructure Architecture Description"
version: "1.0.3"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "architecture"
artifact_id: "AD-0008"
parent_ids:
- "REQ-0009"
created: "2026-03-26"
---
# AI Infrastructure Architecture Description

## Overview

### Overview

## Scope

### Scope

### Context and Stakeholders

This document defines the reference architecture and quality attributes of the `08-ai` layer. It provides structural guidelines on GPU resource allocation, service boundaries, and data flow for high-performance local LLM inference and RAG systems.

### Stakeholders and Concerns

Requirement owners, implementers, and operators share the concerns recorded in this section and the following views. Only concerns confirmed in the existing document are covered here.

The `08-ai` layer is the core area responsible for the system's "intelligence" and owns the privacy-preserving local inference engine and the UI/RAG interface that uses it. Local inference uses NVIDIA GPU resources; optional provider/API egress requires separate authorization and is not ruled out by the tier name.

### System Boundaries

This section preserves the system boundaries, consumption relationships, non-goals, and constraints the current document already records.

- **Owns**:
  - LLM inference engine (`Ollama`)
  - AI user interface and RAG orchestrator (`Open WebUI`)
  - Local model weight and configuration management
  - ComfyUI image-workflow interface and its declared workflow mounts
  - Open Notebook and its nested SurrealDB knowledge-work state
  - MLflow experiment tracking and feature-owned PostgreSQL provisioning
  - Crawl4AI extraction interface and its separate egress boundary
- **Consumes**:
  - GPU hardware resources (via NVIDIA Container Toolkit)
  - Shared Qdrant for explicitly configured vector consumers; current Open WebUI uses local Chroma with `VECTOR_DB` unset
  - Management PostgreSQL and SeaweedFS for MLflow metadata/artifacts
  - User authentication and SSO (`02-auth/keycloak`)
- **Does Not Own**:
  - The vector processing server itself (the Qdrant instance is owned by the Data layer)
  - The service monitoring collector (owned by the Observability layer)
- **Non-goals**:
  - High-end GPU cluster computing (focused on optimizing a single node or a single resource group)
  - Providing a direct model training environment

### Traceability

The disposition of the upstream requirement and the related decision/implementation specs are owned by the PRD, ADR, and Spec links in `Related Documents`. This description does not replace the role of those documents.

## Architecture

### Architecture

### Components

### Viewpoints and Views

This section uses the context, component, or deployment representation as the view for the relevant concern.

The system operates as a hybrid structure.

1. **Inference Layer (Backend)**: Ollama directly controls the model store and GPU and provides an OpenAI-compatible API.
2. **Interaction Layer (Frontend/Orchestrator)**: Open WebUI performs RAG logic (Embedding -> Search -> Augment) alongside the chat UI. Vectors sit in Open WebUI's local storage; Qdrant is not used (`VECTOR_DB` is unset).

### AI Agent Architecture

- **Model/Provider Strategy**: Designates local Ollama as the default provider, with a fallback strategy to external APIs (Claude/OpenAI) supported only for important tasks.
- **Tooling Boundary**: The agent uses the Ollama API as its interface and does not directly manipulate model weights or the GPU driver.
- **Latency / Cost Budget**: Maximizes resource efficiency by minimizing the number of model reloads and using a lightweight embedding model (`qwen3-embedding:0.6b`).

### Data Flow

### Data and Control Flows

Data and control flows include only the interactions specified in this section and the existing infrastructure/deployment description.

- **Key Entities / Flows**: User Prompt → Open WebUI (RAG Context Enrich) → Ollama (Inference) → Response Streaming.
- **Storage Strategy**: Large model files (`${DEFAULT_AI_MODEL_DIR}/ollama`) connect directly to the host's large-scale storage through a bind mount.
- **Data Boundaries**: Open WebUI SQLite, uploads and local Chroma belong to its data volume; Qdrant is not its configured vector backend. ComfyUI declares `/root`-based mounts, but active image `/opt` paths may differ; do not claim coverage until path reconciliation is verified. Open Notebook recovery coordinates app data, SurrealDB and its encryption key. MLflow coordinates PostgreSQL metadata with SeaweedFS artifacts; Jupyter notebooks remain owned by Analytics. Context storage/egress must be checked for the selected consumer.

### Deployment View

- **Runtime / Platform**: Docker Compose v3.8+ (NVIDIA Container Support).
- **Deployment Model**: Ollama/exporter, Open WebUI, and ComfyUI are
  owner-confirmed `HOME` capabilities. `ai` selects the full target;
  `ai-llm` selects Ollama/Open WebUI, `ollama` selects Ollama/exporter, and
  `ai-image` selects ComfyUI. Compose resource declarations are source limits,
  not measured shared-GPU headroom. `notebook`/`surrealdb`, `mlops`/`data-science` and Crawl4AI retain their existing optional profiles; `ai` does not select every package now located in this directory.
- **Operational Evidence**: Real-time GPU status check through `nvidia-smi` and the `ollama-exporter` dashboard.

## Quality Attributes

### Quality Scenarios

Quality scenarios point to the existing configuration these attributes apply to and the verification expectations tied to the failure boundary. Concrete execution evidence belongs to the related Spec and Operations documents.

- **Performance**: CUDA acceleration and model quantization are workload choices; source declarations do not establish measured latency or shared-GPU capacity.
- **Security**: Authentication is service-specific. Open WebUI uses native OIDC, Open Notebook password-file authentication and gateway CIDR controls, and MLflow a browser ForwardAuth route. MLflow's direct SDK path on all four declared networks is not equivalently authenticated. Provider egress, Crawl4AI routes and loopback publications retain their explicit boundaries.
- **Reliability**: Healthchecks provide process/application signals; an unhealthy status alone does not restart a container or prove application recovery.
- **Scalability**: Additional worker/GPU capacity requires approved resource and topology changes; no automatic horizontal scaling is established.
- **Observability**: Continuously monitors VRAM usage, model load status, and API call statistics through `ollama-exporter`.

## Related Documents

- **PRD**: [009-ai.md](../../01.requirements/0009-ai.md)
- **Spec**: [009-ai/spec.md](0008-ai-architecture.md)
- **ADR**: [0008-ollama-openwebui-local-ai.md](../decisions/0008-ollama-openwebui-local-ai.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
