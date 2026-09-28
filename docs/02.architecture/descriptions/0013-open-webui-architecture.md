---
title: "Open WebUI Architecture Description"
version: "1.0.3"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0013"
parent_ids:
- "REQ-0013"
created: "2026-03-27"
---
# Open WebUI Architecture Description

---

## Context and Stakeholders

This document defines the reference architecture and quality attributes of Open WebUI. It is the baseline document that records the system boundary, responsibilities, data flow (Ollama interface, Qdrant RAG integration), and the operational view.

### Stakeholders and Concerns

Requirement owners, implementers, and operators share the concerns recorded in this section and the following views. Only concerns confirmed in the existing document are covered here.

Open WebUI acts as the presentation layer and orchestration hub for AI services. it bridges the gap between raw API backends (Ollama) and end-users, while also providing the logic for document-based RAG.

## System Boundaries

This section preserves the system boundary, consumption relationships, non-goals, and constraints already recorded in the current document.

- **Owns**:
  - Web UI (Frontend/Backend).
  - RAG orchestration logic.
  - User/Chat metadata storage (SQLite).
- **Consumes**:
  - Model Inference APIs (`ollama`).
  - Vector Search APIs (`qdrant`).
  - Native Keycloak OIDC through the `home-openwebui` client and Traefik's standard gateway chain.
- **Does Not Own**:
  - LLM Model Weights.
  - Persistent Vector Data.
- **Non-goals**:
  - Handling raw model training or fine-tuning.

## Quality Attributes

### Quality Scenarios

The quality scenarios point to the existing configuration, failure boundary, and verification expectation to which the attributes below apply. Concrete execution evidence is owned by the related Spec and Operations documents.

- **Performance**: CUDA-accelerated backend for embedding generation.
- **Security**: Native Keycloak OIDC; the gateway provides TLS and the standard chain, while password login, signup, email merge and OAuth role/group management are disabled in Compose.
- **Reliability**: Dependency on Ollama healthchecks (service_healthy).
- **Scalability**: Stateful interface with metadata in the `${DEFAULT_AI_MODEL_DIR}/open-webui` volume; horizontal scaling requires externalizing the database first.
- **Observability**: Healthcheck endpoint at container port `${OLLAMA_WEBUI_PORT:-8080}`.
- **Operability**: Containerized deployment with environment-driven config.

## Components

### Viewpoints and Views

The context, component, or deployment representation in this section serves as the view for that concern.

Open WebUI is deployed as a Docker container within the `ai` tier. Traefik
terminates TLS and applies `gateway-standard-chain@file`; Open WebUI owns
authentication through its native Keycloak OIDC client `home-openwebui`.
Traefik does not apply the proxy `sso-auth@file` middleware to this router.
Open WebUI communicates internally via `ai_net` with Ollama; RAG vectors stay in its local store.

### AI Agent Architecture

- **Model/Provider Strategy**: Local Ollama backend using the image declared in [Open WebUI Compose](../../../infra/08-ai/open-webui/docker-compose.yml).
- **Tooling Boundary**: Access to Ollama API for model listing and RAG indexing.
- **Memory & Context Strategy**: SQLite-based chat persistence.
- **Guardrail Boundary**: gateway TLS/standard controls, application-native OIDC,
  and source GPU/resource limits.

## Data Flow

### Data and Control Flows

The data and control flows include only the interactions specified in this section and the existing infrastructure/deployment descriptions.

- **Key Entities / Flows**:
  - User Input -> Open WebUI -> Ollama (Inference).
  - Document Upload -> Open WebUI -> Ollama (Embedding) -> local vector store (Storage).
  - Query -> Open WebUI -> local vector store (Retrieval) -> Context + Prompt -> Ollama (Generation).
- **Storage Strategy**:
  - `/app/backend/data` (default SQLite database, chat/user state, uploads and application data).
- **Data Boundaries**:
  - Vector data is strictly owned by Qdrant.

## Deployment View

- **Runtime / Platform**: Docker (Linux / CUDA).
- **Deployment Model**: owner-confirmed `HOME`; Compose profiles `ai` and
  `ai-llm`. Current source uses native Keycloak OIDC client `home-openwebui`
  behind `gateway-standard-chain@file` and does not use
  `sso-auth@file`.
- **Operational Evidence**: `docker logs open-webui`, `docker compose exec open-webui curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health`.

Open WebUI must stop writes before SQLite/data-volume capture. Restore first to
an isolated project and coordinate the separately owned Qdrant snapshot before
RAG verification; neither a live filesystem copy nor a WebUI-only backup proves
complete RAG recovery.

## Traceability

The disposition of the parent requirement and the related decision/implementation specs are owned by the PRD, ADR, and Spec links in `Related Documents`. This description does not replace the role of those documents.

## Related Documents

- **PRD**: [../../01.requirements/0013-ai-open-webui.md](../../01.requirements/0013-ai-open-webui.md)
- **Spec**: [../../03.specs/009-ai/open-webui.md](0008-ai-architecture.md)
- **ADR**: [../decisions/0016-open-webui-implementation.md](../decisions/0016-open-webui-implementation.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
