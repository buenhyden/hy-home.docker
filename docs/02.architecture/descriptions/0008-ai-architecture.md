---
title: "AI Infrastructure Architecture Description"
version: "1.0.2"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0008"
parent_ids:
- "REQ-0009"
created: "2026-03-26"
---
# AI Infrastructure Architecture Description

## Context and Stakeholders

This document defines the reference architecture and quality attributes of the `08-ai` layer. It provides structural guidelines on GPU resource allocation, service boundaries, and data flow for high-performance local LLM inference and RAG systems.

### Stakeholders and Concerns

Requirement owners, implementers, and operators share the concerns recorded in this section and the following views. Only concerns confirmed in the existing document are covered here.

The `08-ai` layer is the core area responsible for the system's "intelligence" and owns the privacy-preserving local inference engine and the UI/RAG interface that uses it. It intensively uses NVIDIA GPU resources for inference computation and builds an independent AI ecosystem that does not depend on external model APIs.

## System Boundaries

This section preserves the system boundaries, consumption relationships, non-goals, and constraints the current document already records.

- **Owns**:
  - LLM inference engine (`Ollama`)
  - AI user interface and RAG orchestrator (`Open WebUI`)
  - Local model weight and configuration management
  - ComfyUI image-workflow interface and its persistent workflow assets
- **Consumes**:
  - GPU hardware resources (via NVIDIA Container Toolkit)
  - Vector database (`04-data/qdrant`)
  - User authentication and SSO (`02-auth/keycloak`)
- **Does Not Own**:
  - The vector processing server itself (the Qdrant instance is owned by the Data layer)
  - The service monitoring collector (owned by the Observability layer)
- **Non-goals**:
  - High-end GPU cluster computing (focused on optimizing a single node or a single resource group)
  - Providing a direct model training environment

## Quality Attributes

### Quality Scenarios

Quality scenarios point to the existing configuration these attributes apply to and the verification expectations tied to the failure boundary. Concrete execution evidence belongs to the related Spec and Operations documents.

- **Performance**: Achieves low-latency inference through NVIDIA CUDA acceleration. Recommends using FP16/INT8 quantized models.
- **Security**: All data stays within the project's internal network (`ai_net`), with strict RBAC applied through Keycloak.
- **Reliability**: Monitors inference engine status and performs automatic recovery through Healthcheck.
- **Scalability**: Horizontal scaling through added Worker containers as needed (subject to compliance with the GPU allocation policy).
- **Observability**: Continuously monitors VRAM usage, model load status, and API call statistics through `ollama-exporter`.

## Components

### Viewpoints and Views

This section uses the context, component, or deployment representation as the view for the relevant concern.

The system operates as a hybrid structure.

1. **Inference Layer (Backend)**: Ollama directly controls the model store and GPU and provides an OpenAI-compatible API.
2. **Interaction Layer (Frontend/Orchestrator)**: Open WebUI performs RAG logic (Embedding -> Search -> Augment) alongside the chat UI. Vectors sit in Open WebUI's local storage; Qdrant is not used (`VECTOR_DB` is unset).

### AI Agent Architecture

- **Model/Provider Strategy**: Designates local Ollama as the default provider, with a fallback strategy to external APIs (Claude/OpenAI) supported only for important tasks.
- **Tooling Boundary**: The agent uses the Ollama API as its interface and does not directly manipulate model weights or the GPU driver.
- **Latency / Cost Budget**: Maximizes resource efficiency by minimizing the number of model reloads and using a lightweight embedding model (`qwen3-embedding:0.6b`).

## Data Flow

### Data and Control Flows

Data and control flows include only the interactions specified in this section and the existing infrastructure/deployment description.

- **Key Entities / Flows**: User Prompt → Open WebUI (RAG Context Enrich) → Ollama (Inference) → Response Streaming.
- **Storage Strategy**: Large model files (`${DEFAULT_AI_MODEL_DIR}/ollama`) connect directly to the host's large-scale storage through a bind mount.
- **Data Boundaries**: User/chat/upload state sits in Open WebUI's default SQLite
  data volume, and vector state sits in Qdrant; the two stores are recovered
  through coordination by separate owners. ComfyUI workflow/user/input/output/custom-node
  state and model provenance sit in that service's mounts. Context is passed to
  the inference engine only transiently.

## Deployment View

- **Runtime / Platform**: Docker Compose v3.8+ (NVIDIA Container Support).
- **Deployment Model**: Ollama/exporter, Open WebUI, and ComfyUI are
  owner-confirmed `HOME` capabilities. `ai` selects the full target;
  `ai-llm` selects Ollama/Open WebUI, `ollama` selects Ollama/exporter, and
  `ai-image` selects ComfyUI. Compose resource declarations are source limits,
  not measured shared-GPU headroom.
- **Operational Evidence**: Real-time GPU status check through `nvidia-smi` and the `ollama-exporter` dashboard.

## Traceability

The disposition of the upstream requirement and the related decision/implementation specs are owned by the PRD, ADR, and Spec links in `Related Documents`. This description does not replace the role of those documents.

## Related Documents

- **PRD**: [009-ai.md](../../01.requirements/0009-ai.md)
- **Spec**: [009-ai/spec.md](0008-ai-architecture.md)
- **ADR**: [0008-ollama-openwebui-local-ai.md](../decisions/0008-ollama-openwebui-local-ai.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
