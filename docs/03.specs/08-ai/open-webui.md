---
status: active
---
<!-- Target: docs/03.specs/08-ai/open-webui.md -->

# Open WebUI Technical Specification (Spec)

---

## Overview

This specification defines the technical design and implementation contract for Open WebUI. It translates PRD requirements into deployable infrastructure criteria and integration boundaries with adjacent services such as Ollama and Qdrant. Because the Open WebUI include is currently commented out in the root `docker-compose.yml`, this document describes the standalone/root-commented optional implementation contract.

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
  - `ghcr.io/open-webui/open-webui:v0.9.6-cuda`
  - `ollama` (inference)
  - `qdrant` (vector storage)
- **SPEC-OPENWEBUI-01**: Open WebUI Docker Image: `ghcr.io/open-webui/open-webui:v0.9.6-cuda`
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
docker compose exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags

# Verify container-internal healthcheck endpoint
docker compose exec open-webui curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health
```

## Verification

```bash
bash scripts/hardening/check-all-hardening.sh 08-ai
HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh
docker compose exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags
docker compose exec open-webui curl -f http://qdrant:${QDRANT_PORT:-6333}/collections
docker compose exec open-webui curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health
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
