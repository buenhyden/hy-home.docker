<!-- Target: docs/04.specs/08-ai/open-webui.md -->

# Open WebUI Technical Specification (Spec)

---

# Open WebUI Specification

## Overview (KR)

이 문서는 Open WebUI의 기술 설계와 구현 계약을 정의하는 명세서다. PRD 요구를 기술적으로 구체화하고, 인프라 배포 및 타 서비스(Ollama, Qdrant)와의 연동 기준이 된다.

## Strategic Boundaries & Non-goals

- **Owns**: Deployment spec for `open-webui` service, environment configuration for RAG, local volume mapping.
- **Does Not Own**: Ollama API endpoints (managed in `08-ai/ollama`), Qdrant server config (managed in `04-data/qdrant`).

## Related Inputs

- **PRD**: `[../../01.prd/2026-03-27-08-ai-open-webui.md]`
- **ARD**: `[../../02.ard/0013-open-webui-architecture.md]`
- **Related ADRs**: `[../../03.adr/0016-open-webui-implementation.md]`

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
- **SPEC-OPENWEBUI-01**: Open WebUI Docker Image: `ghcr.io/open-webui/open-webui:main`
- **SPEC-OPENWEBUI-02**: Ollama Integration via `OLLAMA_BASE_URL` env.
- **SPEC-OPENWEBUI-03**: Qdrant Integration via `VECTOR_DB_URL` env.
- **SPEC-OPENWEBUI-04**: Persistent volume: `${DEFAULT_AI_MODEL_DIR}/open-webui:/app/backend/data`.
- **Tech Stack**: Docker, SvelteKit, Python, CUDA.

## Key Components

```bash
# Verify container connectivity to Ollama
docker exec open-webui curl -f ${OLLAMA_BASE_URL}/api/tags

# Verify healthcheck endpoint
curl -f http://localhost:${OLLAMA_WEB_UI_PORT:-8080}/health
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Web UI is accessible via `https://chat.local.hy` (or configured domain).
- **VAL-SPC-002**: RAG indexing completes successfully against a test PDF file.

## Related Documents

- **Plan**: `[../../05.plans/2026-03-27-08-ai-open-webui-plan.md]`
- **Tasks**: `[../../06.tasks/2026-03-27-08-ai-open-webui-tasks.md]`
- **Runbook**: `[../../09.runbooks/08-ai/open-webui.md]`
