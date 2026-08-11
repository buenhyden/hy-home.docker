---
status: active
artifact_id: ad-0013
artifact_type: architecture-description
parent_ids:
  - prd-013
created: 2026-03-27
updated: 2026-08-10
---
# Open WebUI Architecture Description

---

## Open WebUI Architecture Description

## Overview and Context

이 문서는 Open WebUI의 참조 아키텍처와 품질 속성을 정의한다. 시스템 경계, 책임, 데이터 흐름(Ollama 인터페이스, Qdrant RAG 통합), 운영 관점을 정리하는 기준 문서다.

## Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

Open WebUI acts as the presentation layer and orchestration hub for AI services. it bridges the gap between raw API backends (Ollama) and end-users, while also providing the logic for document-based RAG.

## Boundaries and Constraints

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

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

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: CUDA-accelerated backend for embedding generation.
- **Security**: Mandatory SSO integration via Traefik middlewares.
- **Reliability**: Dependency on Ollama healthchecks (service_healthy).
- **Scalability**: Stateful interface with metadata in the `${DEFAULT_AI_MODEL_DIR}/open-webui` volume; horizontal scaling requires externalizing the database first.
- **Observability**: Healthcheck endpoint at container port `${OLLAMA_WEBUI_PORT:-8080}`.
- **Operability**: Containerized deployment with environment-driven config.

## Architecture Views

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

Open WebUI is deployed as a Docker container within the `ai` tier. It sits behind Traefik, which provides TLS and SSO. It communicates internally via the `infra_net` with Ollama and Qdrant.

## Data and Infrastructure

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

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

## AI Agent Architecture Descriptions (If Applicable)

- **Model/Provider Strategy**: Local Ollama backend using `ghcr.io/open-webui/open-webui:v0.10.2-cuda`.
- **Tooling Boundary**: Access to Ollama API for model listing and RAG indexing.
- **Memory & Context Strategy**: SQLite-based chat persistence.
- **Guardrail Boundary**: SSO access control and GPU resource limits.

## Decision and Requirement Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [../../01.requirements/prd-013-ai-open-webui.md](../../01.requirements/prd-013-ai-open-webui.md)
- **Spec**: [../../03.specs/009-ai/open-webui.md](../../03.specs/spec-0009-ai/spec.md)
- **Plan**: ../../04.execution/plans/2026-03-27-08-ai-open-webui-plan.md
- **ADR**: [../decisions/adr-0016-open-webui-implementation.md](../decisions/adr-0016-open-webui-implementation.md)
