---
status: active
---
<!-- Target: docs/02.architecture/requirements/0013-open-webui-architecture.md -->

# Open WebUI Architecture Reference Document (ARD)

---

## Open WebUI Architecture Reference Document

## Overview

이 문서는 Open WebUI의 참조 아키텍처와 품질 속성을 정의한다. 시스템 경계, 책임, 데이터 흐름(Ollama 인터페이스, Qdrant RAG 통합), 운영 관점을 정리하는 기준 문서다.

## Summary

Open WebUI acts as the presentation layer and orchestration hub for AI services. it bridges the gap between raw API backends (Ollama) and end-users, while also providing the logic for document-based RAG.

## Boundaries & Non-goals

- **Owns**:
  - Web UI (Frontend/Backend).
  - RAG orchestration logic.
  - User/Chat metadata storage (SQLite).
- **Consumes**:
  - Model Inference APIs (`ollama`).
  - Vector Search APIs (`qdrant`).
  - SSO Authentication (`oauth2-proxy` / `traefik`).
- **Does Not Own**:
  - LLM Model Weights.
  - Persistent Vector Data.
- **Non-goals**:
  - Handling raw model training or fine-tuning.

## Quality Attributes

- **Performance**: CUDA-accelerated backend for embedding generation.
- **Security**: Mandatory SSO integration via Traefik middlewares.
- **Reliability**: Dependency on Ollama healthchecks (service_healthy).
- **Scalability**: Stateful interface with metadata in the `${DEFAULT_AI_MODEL_DIR}/open-webui` volume; horizontal scaling requires externalizing the database first.
- **Observability**: Healthcheck endpoint at container port `${OLLAMA_WEBUI_PORT:-8080}`.
- **Operability**: Containerized deployment with environment-driven config.

## System Overview & Context

Open WebUI is deployed as a Docker container within the `ai` tier. It sits behind Traefik, which provides TLS and SSO. It communicates internally via the `infra_net` with Ollama and Qdrant.

## Data Architecture

- **Key Entities / Flows**:
  - User Input -> Open WebUI -> Ollama (Inference).
  - Document Upload -> Open WebUI -> Ollama (Embedding) -> Qdrant (Storage).
  - Query -> Open WebUI -> Qdrant (Retrieval) -> Context + Prompt -> Ollama (Generation).
- **Storage Strategy**:
  - `/app/backend/data` (Volumes: Chat history, locally indexed Lite DB).
- **Data Boundaries**:
  - Vector data is strictly owned by Qdrant.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker (Linux / CUDA).
- **Deployment Model**: `docker-compose` profile: `ai`.
- **Operational Evidence**: `docker logs open-webui`, `docker compose exec open-webui curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health`.

## AI Agent Architecture Requirements (If Applicable)

- **Model/Provider Strategy**: Local Ollama backend using `ghcr.io/open-webui/open-webui:v0.10.2-cuda`.
- **Tooling Boundary**: Access to Ollama API for model listing and RAG indexing.
- **Memory & Context Strategy**: SQLite-based chat persistence.
- **Guardrail Boundary**: SSO access control and GPU resource limits.

## Related Documents

- **PRD**: [../../01.requirements/013-ai-open-webui.md](../../01.requirements/013-ai-open-webui.md)
- **Spec**: [../../03.specs/009-ai/open-webui.md](../../03.specs/009-ai/open-webui.md)
- **Plan**: [../../04.execution/plans/2026-03-27-08-ai-open-webui-plan.md](../../04.execution/plans/2026-03-27-08-ai-open-webui-plan.md)
- **ADR**: [../decisions/0016-open-webui-implementation.md](../decisions/0016-open-webui-implementation.md)
