---
profile_id: spec
status: active
artifact_id: SPEC-0009
artifact_type: spec
parent_ids:
  - AD-0013
  - AD-0023
created: 2026-07-05
updated: 2026-08-14
---
# 08-AI Optimization Hardening Technical Specification

## Overview

This document is the optimization/hardening technical specification for the `infra/08-ai` tier (Ollama, Open WebUI). It defines gateway boundary security, GPU concurrency control, exporter health-gating, stateful operating consistency, CI policy gates, and catalog-based expansion requirements as implementation contracts. Because AI compose includes are currently commented out in the root `docker-compose.yml`, this specification describes the owned implementation and the standalone/root-commented optional execution contract.

## Strategic Boundaries & Non-goals

- **Owns**:
  - Ollama/Open WebUI Traefik middleware contract
  - Ollama concurrency/queue/resource protection contract
  - Open WebUI stateful template contract
  - `ollama-exporter` dependency/healthcheck contract
  - `scripts/hardening/check-all-hardening.sh 08-ai` policy gate contract
- **Does Not Own**:
  - Model training/fine-tuning pipelines
  - Qdrant internal operating policy/schema
  - External LLM provider integration policy

## Related Inputs

- **PRD**: [../../01.requirements/0020-ai-optimization-hardening.md](../../01.requirements/0020-ai-optimization-hardening.md)
- **ARD**: [../../02.architecture/descriptions/0023-ai-optimization-hardening-architecture.md](../../02.architecture/descriptions/0023-ai-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../02.architecture/decisions/0008-ollama-openwebui-local-ai.md](../../02.architecture/decisions/0008-ollama-openwebui-local-ai.md)
  - [../../02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - `infra/08-ai/ollama/docker-compose.yml` and `infra/08-ai/open-webui/docker-compose.yml` are currently root-commented optional includes.
  - Ollama/Open WebUI public routers use `gateway-standard-chain@file,sso-errors@file,sso-auth@file`.
  - Ollama declares `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, and `OLLAMA_MAX_QUEUE`.
  - Open WebUI uses `template-stateful-med`.
  - `ollama-exporter` has an `ollama` `service_healthy` dependency and a metrics healthcheck.
  - Both compose files include an `infra_net` external network declaration.
- **Data / Interface Contract**:
  - Keep the Open WebUI -> Ollama (`OLLAMA_BASE_URL`) + Qdrant (`VECTOR_DB_URL`) connection.
  - Keep the default embedding model as `qwen3-embedding:0.6b`.
- **Governance Contract**:
  - Passing `scripts/hardening/check-all-hardening.sh 08-ai` is the AI tier hardening baseline.
  - The CI `infrastructure-hardening` job blocks regressions at PR time through the full hardening baseline.

## Core Design

- **Gateway Security Plane**:
  - AI public paths enforce the gateway standard chain and SSO chain after TLS termination.
- **Inference Runtime Plane**:
  - Ollama uses concurrency/queue limits to suppress GPU overload.
- **Stateful Control Plane**:
  - Open WebUI follows the stateful template policy as a stateful service.
- **Observability Plane**:
  - The exporter starts on a health basis and verifies the metrics endpoint through a healthcheck.

## Data Modeling & Storage Strategy

- Ollama model data uses the `${DEFAULT_AI_MODEL_DIR}/ollama` bind volume.
- Open WebUI state data uses the `${DEFAULT_AI_MODEL_DIR}/open-webui` bind volume.
- Conversation/RAG data retention policy is controlled by the operations policy document (`docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/policy.md`).

## Interfaces & Data Structures

### AI Hardening Control Surface

```yaml
ai_hardening_controls:
  ingress_security:
    ollama: gateway-standard-chain + sso-errors + sso-auth
    open_webui: gateway-standard-chain + sso-errors + sso-auth
  gpu_safeguards:
    ollama_num_parallel: required
    ollama_max_loaded_models: required
    ollama_max_queue: required
  startup_health_contract:
    ollama_exporter_depends_on_ollama_health: required
    ollama_exporter_metrics_healthcheck: required
  stateful_policy:
    open_webui_template: template-stateful-med
```

## Edge Cases & Error Handling

- If concurrency limits are too low, response latency can increase; tune them with operating metrics.
- Missing middleware chains can create authentication bypass paths, so CI gates block them immediately.
- If exporter healthchecks fail, inspect the metrics path/port and the `OLLAMA_EXPORTER_PORT` value.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: AI router access policy regression
  - **Fallback**: roll back to the most recent working compose routing settings
  - **Human Escalation**: Gateway/Auth operations approver
- **Failure Mode**: Ollama GPU overload/queue backlog
  - **Fallback**: readjust concurrency/queue limits to conservative values
  - **Human Escalation**: AI Platform Owner
- **Failure Mode**: exporter metrics observability failure
  - **Fallback**: restore the healthcheck/depends_on contract, then restart
  - **Human Escalation**: SRE on-call

## Verification

```bash
bash scripts/hardening/check-all-hardening.sh 08-ai
HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh
bash scripts/validation/check-template-security-baseline.sh
python3 scripts/validation/check-document-links.py --mode traceability
```

## Success Criteria & Verification Plan

- **VAL-AI-001**: root-active compose validation and optional AI hardening checks pass.
- **VAL-AI-002**: AI hardening baseline script has zero failures.
- **VAL-AI-003**: PRD~Runbook optimization-hardening document links remain consistent.
- **VAL-AI-004**: catalog `08-ai` expansion items (model promotion, access separation, log policy) are reflected in Plan/Tasks/Operations.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: ../../04.execution/plans/2026-03-28-08-ai-optimization-hardening-plan.md
- **Tasks**: ../../04.execution/tasks/2026-03-28-08-ai-optimization-hardening-tasks.md
- **Guide**: [../../05.operations/guides/08-ai/optimization-hardening.md](../../05.operations/catalog/08-ai/ops-0058-optimization-hardening/guide.md)
- **Policy**: [../../05.operations/policies/08-ai/optimization-hardening.md](../../05.operations/catalog/08-ai/ops-0058-optimization-hardening/policy.md)
- **Runbook**: [../../05.operations/runbooks/08-ai/optimization-hardening.md](../../05.operations/catalog/08-ai/ops-0058-optimization-hardening/runbook.md)
- **Governance**: [Infrastructure optimization governance](../../05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md)

## Merged Open WebUI Component Contract

---

### Overview

This specification defines the technical design and implementation contract for Open WebUI. It translates PRD requirements into deployable infrastructure criteria and integration boundaries with adjacent services such as Ollama and Qdrant. Because the Open WebUI include is currently commented out in the root `docker-compose.yml`, this document describes the standalone/root-commented optional implementation contract.

### Strategic Boundaries & Non-goals

- **Owns**: Deployment spec for `open-webui` service, environment configuration for RAG, local volume mapping.
- **Runtime Surface**: `infra/08-ai/open-webui/docker-compose.yml` exists, but the root include is commented out; promote it to root-active only after explicit runtime approval.
- **Does Not Own**: Ollama API endpoints (managed in `08-ai/ollama`), Qdrant server config (managed in `04-data/qdrant`).

### Related Inputs

- **PRD**: [../../01.requirements/0013-ai-open-webui.md](../../01.requirements/0013-ai-open-webui.md)
- **ARD**: [../../02.architecture/descriptions/0013-open-webui-architecture.md](../../02.architecture/descriptions/0013-open-webui-architecture.md)
- **Related ADRs**: [../../02.architecture/decisions/0016-open-webui-implementation.md](../../02.architecture/decisions/0016-open-webui-implementation.md)

### Contracts

- **Config Contract**:
  - `OLLAMA_BASE_URL`: External API endpoint for inference.
  - `VECTOR_DB_URL`: External API endpoint for vector operations.
  - `RAG_EMBEDDING_MODEL`: Specified embedding model (default: `qwen3-embedding:0.6b`).
- **Data / Interface Contract**:
  - Users interact via HTTPS (Port 443 via Traefik).
  - Internal communication on Port 8080.
- **Governance Contract**:
  - Must use `sso-auth@file` middleware for all web routes.

### Core Design

- **Component Boundary**: Dockerized SvelteKit frontend + Python FastAPI backend.
- **Key Dependencies**:
  - `ghcr.io/open-webui/open-webui:v0.10.2-cuda`
  - `ollama` (inference)
  - `qdrant` (vector storage)
- **SPEC-OPENWEBUI-01**: Open WebUI Docker Image: `ghcr.io/open-webui/open-webui:v0.10.2-cuda`
- **SPEC-OPENWEBUI-02**: Ollama Integration via `OLLAMA_BASE_URL` env.
- **SPEC-OPENWEBUI-03**: Qdrant Integration via `VECTOR_DB_URL` env.
- **SPEC-OPENWEBUI-04**: Persistent volume: `${DEFAULT_AI_MODEL_DIR}/open-webui:/app/backend/data`.
- **Tech Stack**: Docker, SvelteKit, Python, CUDA.

### Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - User sessions, chat state, uploads, and RAG metadata live under `/app/backend/data`.
  - Vector retrieval data is delegated to Qdrant through `VECTOR_DB_URL`.
  - Model inference data is delegated to Ollama through `OLLAMA_BASE_URL`.
- **Migration / Transition Plan**:
  - Preserve `${DEFAULT_AI_MODEL_DIR}/open-webui` as the stateful volume boundary.
  - Keep embedding model defaults aligned with the parent AI spec before changing RAG behavior.

### Interfaces & Data Structures

#### Core Interfaces

```bash
# Verify container connectivity to Ollama
docker compose exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags

# Verify container-internal healthcheck endpoint
docker compose exec open-webui curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health
```

### Verification

```bash
bash scripts/hardening/check-all-hardening.sh 08-ai
HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh
docker compose exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags
docker compose exec open-webui curl -f http://qdrant:${QDRANT_PORT:-6333}/collections
docker compose exec open-webui curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health
```

### Success Criteria & Verification Plan

- **VAL-SPC-001**: Web UI is accessible via `https://chat.local.hy` (or configured domain).
- **VAL-SPC-002**: RAG indexing completes successfully against a test PDF file.

### Related Documents

- **Plan**: ../../04.execution/plans/2026-03-27-08-ai-open-webui-plan.md
- **Tasks**: ../../04.execution/tasks/2026-03-27-08-ai-open-webui-tasks.md
- **Guide**: [../../05.operations/guides/08-ai/open-webui.md](../../05.operations/catalog/08-ai/ops-0057-open-webui/guide.md)
- **Policy**: [../../05.operations/policies/08-ai/open-webui.md](../../05.operations/catalog/08-ai/ops-0057-open-webui/policy.md)
- **Runbook**: [../../05.operations/runbooks/08-ai/open-webui.md](../../05.operations/catalog/08-ai/ops-0057-open-webui/runbook.md)

## Boundaries and Inputs

The preserved ownership boundaries, dependencies, and inputs above remain authoritative.

## Behavior Contract

The behaviors and invariants already specified above remain the package behavior contract.

## Technical Approach

The implementation and component design recorded above remain the technical approach.

## Interfaces and Data

The interfaces, configuration, and data shapes recorded above remain authoritative.

## Failure Modes and Guardrails

The safety, validation, and operational constraints above remain the package guardrails.

## Acceptance Contract

The verification and success conditions above remain the acceptance contract.

## Traceability

The requirement, architecture, operations, and evidence links above provide traceability.
