---
title: 'Infrastructure AI Implementation Spec'
status: 'Draft'
version: '1.0'
owner: 'AI Infrastructure Engineer'
prd_reference: '../../../docs/prd/ai-prd.md'
api_reference: 'N/A'
arch_reference: '../../../ARCHITECTURE.md'
tags: ['spec', 'infra', 'ai', 'ollama', 'open-webui', 'qdrant']
---

# Implementation Specification (Spec)

> **Status**: Draft
> **Related PRD**: [docs/prd/ai-prd.md](../../../docs/prd/ai-prd.md)
> **Related Architecture**: [ARCHITECTURE.md](../../../ARCHITECTURE.md)

_Target Directory: `specs/infra/ai/spec.md`_

---

## 0. Pre-Implementation Checklist (Governance)

### 0.1 Architecture / Tech Stack

| Item               | Check Question                                        | Required | Alignment Notes | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | --------------- | ----------------- |
| Architecture Style | Is the style Monolith/Modular Monolith/Microservices? | Must     | Root-only Docker Compose stack with profile-based optionality. | Section 1 |
| Service Boundaries | Are module boundaries documented (diagram/text)?      | Must     | Boundaries are defined by `ai` profile + per-service Compose files. | Section 5 |
| Domain Model       | Are core domain entities and relationships defined?   | Must     | N/A (infrastructure stack; no domain model). | N/A |
| Backend Stack      | Are language/framework/libs (web, ORM, auth) decided? | Must     | N/A (no backend code shipped in this repo for AI stack). | N/A |
| Frontend Stack     | Are framework/state/build tools decided?              | Must     | `open-webui` container provides UI; no in-repo frontend build. | Section 1 |

### 0.2 Quality / Testing / Security

| Item            | Check Question                                 | Required | Alignment Notes | Where to document |
| --------------- | ---------------------------------------------- | -------- | --------------- | ----------------- |
| Test Strategy   | Levels (Unit/Integration/E2E/Load) defined?    | Must     | Compose schema validation + container healthchecks + basic endpoint smoke checks. | Section 7 |
| Test Tooling    | Agreed framework/runner and mock strategy?     | Must     | `docker compose config -q` (static) + runtime smoke checks (manual/local). | Section 7 |
| Coverage Policy | Are goals defined as numbers (e.g. 100%)?      | Must     | N/A (no code-level tests in this spec). | N/A |
| AuthN/AuthZ     | Is auth approach designed (token/OAuth/RBAC)?  | Must     | External access is via Traefik routers; middleware/SSO is out of scope for this spec. | Section 4 |
| Data Protection | Encryption/access policies for sensitive data? | Must     | Secrets are file-injected via Docker secrets; no plaintext secrets in Compose env. | Section 9 |
| Performance     | Are Core Web Vitals/Latency metrics targeted?  | Must     | N/A (infra-only). | N/A |
| Accessibility   | Is WCAG compliance integrated (contrast/ARIA)? | Must     | N/A (third-party UI). | N/A |

### 0.3 Operations / Deployment / Monitoring

| Item         | Check Question                                           | Required | Alignment Notes | Where to document |
| ------------ | -------------------------------------------------------- | -------- | --------------- | ----------------- |
| Environments | Are tiers (dev/staging/prod) clarified for this feature? | Must     | Local/internal development environment only. | Section 9 |
| Logging      | Required structured logs defined (fields, IDs)?          | Must     | Containers use Loki logging driver via `infra/common-optimizations.yml`. | Section 9 |
| Monitoring   | Metrics and dashboards defined (RED/USE)?                | Must     | Exporters expose `/metrics`; scraping/dashboards belong to the Observability spec. | Section 9 |
| Alerts       | Are alert thresholds and routing defined?                | Must     | N/A (handled in Observability spec). | N/A |
| Backups      | Are backup policies defined for added data?              | Must     | Model/vector persistence is host-mapped volumes; backup policy is out of scope. | Section 9 |

---

## 1. Technical Overview & Architecture Style

This spec defines the local AI stack for development use:

- **Ollama** for local model inference (GPU passthrough optional).
- **Open WebUI** for a chat UI over the internal Ollama endpoint.
- **Qdrant** as the local vector store for RAG experiments.

**Execution model**: the stack is enabled via the standard Compose profile `ai` and runs inside `infra_net` using Docker internal DNS (no static IPs).

## 2. Coded Requirements (Traceability)

| ID                | Requirement Description | Priority | Parent PRD REQ |
| ----------------- | ----------------------- | -------- | -------------- |
| **REQ-SPC-AI-001** | AI stack MUST be gated behind the `ai` profile (root-only entrypoint). | High | REQ-PRD-AI-FUN-01 |
| **REQ-SPC-AI-002** | Services MUST use internal DNS (no `ipv4_address` pinning). | High | REQ-PRD-AI-FUN-03 |
| **REQ-SPC-AI-003** | Model and state directories MUST persist via host-mapped volumes. | High | REQ-PRD-AI-FUN-03 |
| **SEC-SPC-AI-001** | Secrets MUST NOT be passed as plaintext environment variables. | Critical | N/A |

## 3. Data Modeling & Storage Strategy

- **Ollama models**: `${DEFAULT_AI_MODEL_DIR}/ollama`
- **Open WebUI data**: `${DEFAULT_AI_MODEL_DIR}/open-webui`
- **Qdrant storage**: `${DEFAULT_DATA_DIR}/qdrant/data`

## 4. Interfaces & Data Structures

### 4.1 Core Interfaces

- **Ollama internal API**: `http://ollama:${OLLAMA_PORT:-11434}`
- **Open WebUI internal**: `http://open-webui:8080`
- **Qdrant internal API**: `http://qdrant:${QDRANT_PORT:-6333}`

### 4.2 AuthN / AuthZ

- External exposure is via Traefik host routing. Any SSO/OIDC middleware should be tracked via ADR/ARD and implemented explicitly (not implied).

## 5. Component Breakdown

- **`infra/08-ai/ollama/docker-compose.yml`**: `ollama` + `ollama-exporter` (profile `ai`)
- **`infra/08-ai/open-webui/docker-compose.yml`**: `open-webui` (profile `ai`)
- **`infra/04-data/qdrant/docker-compose.yml`**: `qdrant` (profile `ai`)

## 6. Edge Cases & Error Handling

- **No GPU available**: Ollama may fail to start if GPU reservations are enabled on a host without NVIDIA runtime support.
- **Large model downloads**: Ensure host disk capacity under `${DEFAULT_AI_MODEL_DIR}`.

## 7. Verification Plan (Testing & QA)

- **[VAL-AI-001] Compose schema**: `COMPOSE_PROFILES=core,data,obs,ai docker compose --env-file .env.example config -q`
- **[VAL-AI-002] Healthchecks (runtime)**: `docker compose --profile ai up -d` then `docker compose ps` shows `healthy` where defined.
- **[VAL-AI-003] Endpoint smoke**: `curl -fsS http://localhost:${OLLAMA_PORT:-11434}/api/tags` (from host or within container).

## 8. Non-Functional Requirements (NFR) & Scalability

- **Resource isolation**: AI services must declare CPU/memory bounds via shared templates.
- **Portability**: No hard-coded IPs; DNS-only connectivity inside `infra_net`.

## 9. Operations & Observability

- **Logging**: Loki logging driver (configured via `infra/common-optimizations.yml`).
- **Metrics**: `ollama-exporter` exposes metrics on `:${OLLAMA_EXPORTER_PORT:-11435}` inside `infra_net`.
- **Sensitive Data Handling**: All secrets must be mounted under `/run/secrets/*` and never logged.

