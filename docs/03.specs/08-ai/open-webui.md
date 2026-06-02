---
status: active
---
<!-- Target: docs/03.specs/08-ai/open-webui.md -->

# Open WebUI Technical Specification (Spec)

---

## Overview (KR)

이 문서는 Open WebUI의 기술 설계와 구현 계약을 정의하는 명세서다. PRD 요구를 기술적으로 구체화하고, 인프라 배포 및 타 서비스(Ollama, Qdrant)와의 연동 기준이 된다. 현재 root `docker-compose.yml`에서 Open WebUI include는 주석 처리되어 있으므로, 이 문서는 standalone/root-commented optional 구현 계약을 설명한다.

## Strategic Boundaries & Non-goals

- **Owns**: Deployment spec for `open-webui` service, environment configuration for RAG, local volume mapping.
- **Runtime Surface**: `infra/08-ai/open-webui/docker-compose.yml` exists, but the root include is commented out; promote it to root-active only after explicit runtime approval.
- **Does Not Own**: Ollama API endpoints (managed in `08-ai/ollama`), Qdrant server config (managed in `04-data/qdrant`).

## Related Inputs

- **PRD**: [../../01.requirements/2026-03-27-08-ai-open-webui.md](../../01.requirements/2026-03-27-08-ai-open-webui.md)
- **ARD**: [../../02.architecture/requirements/0013-open-webui-architecture.md](../../02.architecture/requirements/0013-open-webui-architecture.md)
- **Related ADRs**: [../../02.architecture/decisions/0016-open-webui-implementation.md](../../02.architecture/decisions/0016-open-webui-implementation.md)

## Contracts

- **Config Contract**:
  - `OLLAMA_BASE_URL`: External API endpoint for inference.
  - `VECTOR_DB_URL`: External API endpoint for vector operations.
  - `RAG_EMBEDDING_MODEL`: Specified embedding model (default: `qwen3-embedding:0.6b`).
- **Data / Interface Contract**:
  - Users interact via HTTPS (Port 443 via Traefik).
  - Internal communication on Port 8080.
- **Governance Contract**:
  - Must use `sso-auth@file` middleware for all web routes.

## Core Design

- **Component Boundary**: Dockerized SvelteKit frontend + Python FastAPI backend.
- **Key Dependencies**:
  - `ghcr.io/open-webui/open-webui:v0.8.5-cuda`
  - `ollama` (inference)
  - `qdrant` (vector storage)
- **SPEC-OPENWEBUI-01**: Open WebUI Docker Image: `ghcr.io/open-webui/open-webui:v0.8.5-cuda`
- **SPEC-OPENWEBUI-02**: Ollama Integration via `OLLAMA_BASE_URL` env.
- **SPEC-OPENWEBUI-03**: Qdrant Integration via `VECTOR_DB_URL` env.
- **SPEC-OPENWEBUI-04**: Persistent volume: `${DEFAULT_AI_MODEL_DIR}/open-webui:/app/backend/data`.
- **Tech Stack**: Docker, SvelteKit, Python, CUDA.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - User sessions, chat state, uploads, and RAG metadata live under `/app/backend/data`.
  - Vector retrieval data is delegated to Qdrant through `VECTOR_DB_URL`.
  - Model inference data is delegated to Ollama through `OLLAMA_BASE_URL`.
- **Migration / Transition Plan**:
  - Preserve `${DEFAULT_AI_MODEL_DIR}/open-webui` as the stateful volume boundary.
  - Keep embedding model defaults aligned with the parent AI spec before changing RAG behavior.

## Interfaces & Data Structures

### Core Interfaces

```bash
# Verify container connectivity to Ollama
docker exec open-webui curl -f ${OLLAMA_BASE_URL}/api/tags

# Verify healthcheck endpoint
curl -f http://localhost:${OLLAMA_WEB_UI_PORT:-8080}/health
```

## Verification

```bash
docker compose -f infra/08-ai/open-webui/docker-compose.yml config
docker exec open-webui curl -f ${OLLAMA_BASE_URL}/api/tags
docker exec open-webui curl -f ${VECTOR_DB_URL}/collections
curl -f http://localhost:${OLLAMA_WEB_UI_PORT:-8080}/health
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Web UI is accessible via `https://chat.local.hy` (or configured domain).
- **VAL-SPC-002**: RAG indexing completes successfully against a test PDF file.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-03-27-08-ai-open-webui-plan.md](../../04.execution/plans/2026-03-27-08-ai-open-webui-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-27-08-ai-open-webui-tasks.md](../../04.execution/tasks/2026-03-27-08-ai-open-webui-tasks.md)
- **Guide**: [../../05.operations/guides/08-ai/open-webui.md](../../05.operations/guides/08-ai/open-webui.md)
- **Policy**: [../../05.operations/policies/08-ai/open-webui.md](../../05.operations/policies/08-ai/open-webui.md)
- **Runbook**: [../../05.operations/runbooks/08-ai/open-webui.md](../../05.operations/runbooks/08-ai/open-webui.md)
