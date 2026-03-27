<!-- Target: docs/02.ard/0013-open-webui-architecture.md -->

# Open WebUI Architecture Reference Document (ARD)

---

## Open WebUI Architecture Reference Document

## Overview (KR)

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
- **Scalability**: Stateless interface (metadata in SQLite volume), potential for horizontal scaling if database is externalized.
- **Observability**: Healthcheck endpoint at port 8080.
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
- **Operational Evidence**: `docker logs open-webui`, `curl localhost:8080/health`.

## AI Agent Architecture Requirements (If Applicable)

- **Model/Provider Strategy**: Local Ollama backend using `ghcr.io/open-webui/open-webui:v0.8.5-cuda`.
- **Tooling Boundary**: Access to Ollama API for model listing and RAG indexing.
- **Memory & Context Strategy**: SQLite-based chat persistence.
- **Guardrail Boundary**: SSO access control and GPU resource limits.

## Related Documents

- **PRD**: `[../01.prd/2026-03-27-08-ai-open-webui.md]`
- **Spec**: `[../04.specs/08-ai/open-webui.md]`
- **Plan**: `[../05.plans/2026-03-27-08-ai-open-webui-plan.md]`
- **ADR**: `[../03.adr/0016-open-webui-implementation.md]`
