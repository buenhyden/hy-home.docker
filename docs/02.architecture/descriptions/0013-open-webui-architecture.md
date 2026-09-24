---
title: "Open WebUI Architecture Description"
version: "1.0.2"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "architecture"
artifact_id: "AD-0013"
parent_ids:
- "REQ-0013"
created: "2026-03-27"
---
# Open WebUI Architecture Description

---

## Context and Stakeholders

이 문서는 Open WebUI의 참조 아키텍처와 품질 속성을 정의한다. 시스템 경계, 책임, 데이터 흐름(Ollama 인터페이스, Qdrant RAG 통합), 운영 관점을 정리하는 기준 문서다.

### Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

Open WebUI acts as the presentation layer and orchestration hub for AI services. it bridges the gap between raw API backends (Ollama) and end-users, while also providing the logic for document-based RAG.

## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

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

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: CUDA-accelerated backend for embedding generation.
- **Security**: Native Keycloak OIDC; the gateway provides TLS and the standard chain, while password login, signup, email merge and OAuth role/group management are disabled in Compose.
- **Reliability**: Dependency on Ollama healthchecks (service_healthy).
- **Scalability**: Stateful interface with metadata in the `${DEFAULT_AI_MODEL_DIR}/open-webui` volume; horizontal scaling requires externalizing the database first.
- **Observability**: Healthcheck endpoint at container port `${OLLAMA_WEBUI_PORT:-8080}`.
- **Operability**: Containerized deployment with environment-driven config.

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

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

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

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

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [../../01.requirements/0013-ai-open-webui.md](../../01.requirements/0013-ai-open-webui.md)
- **Spec**: [../../03.specs/009-ai/open-webui.md](0008-ai-architecture.md)
- **ADR**: [../decisions/0016-open-webui-implementation.md](../decisions/0016-open-webui-implementation.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
