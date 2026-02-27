---
goal: 'Create a deterministic, spec-compliant implementation path for the local AI stack (Ollama + Open WebUI + Qdrant) gated by Docker Compose profiles.'
version: '1.0'
date_created: '2026-02-27'
last_updated: '2026-02-27'
owner: 'AI Infrastructure Engineer'
status: 'Planned'
tags: ['implementation', 'planning', 'infra', 'ai', 'ollama', 'open-webui', 'qdrant', 'docker-compose']
stack: 'docker'
---

# AI Infrastructure Implementation Plan

_Target Directory: `specs/infra/ai/plan.md`_

## 1. Context & Introduction

This plan implements and verifies the local AI stack defined in `specs/infra/ai/spec.md` and the product intent in `docs/prd/ai-prd.md`.

The AI stack MUST be:
- enabled via the Compose profile `ai`,
- internally connected via Docker DNS on `infra_net`,
- persistent via host-mapped volumes,
- and secrets-safe (no plaintext secrets in environment variables).

## 2. Goals & In-Scope

- **Goals:**
  - Ensure the AI stack is gated behind `ai` profile and root orchestration.
  - Ensure storage and network connectivity match the spec and `.env.example`.
  - Ensure the stack can be statically validated via `docker compose ... config -q`.
- **In-Scope (Scope of this Plan):**
  - Root orchestration and included compose files for: Ollama, Open WebUI, Qdrant.
  - Documentation drift fixes if the current repo state deviates from the spec.

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Distributed inference, multi-host orchestration, or training pipelines.
  - Defining or implying SSO/OIDC policies not explicitly configured in gateway middleware.
- **Out-of-Scope:**
  - Changing model choice, embedding strategy, or runtime tuning beyond what is required for spec compliance.

## 4. Requirements & Constraints

_Note: Use Machine-Readable Identifiers (e.g., `[REQ-...]`) for traceability._

- **Requirements:**
  - `[REQ-AI-001]`: AI stack MUST be gated behind the `ai` profile in root orchestration (maps to `REQ-SPC-AI-001`).
  - `[REQ-AI-002]`: Internal connectivity MUST use Docker DNS; no static IP pinning (maps to `REQ-SPC-AI-002`).
  - `[REQ-AI-003]`: Model/state MUST persist via host-mapped volumes (maps to `REQ-SPC-AI-003`).
  - `[SEC-AI-001]`: Secrets MUST NOT be passed as plaintext environment variables (maps to `SEC-SPC-AI-001`).
  - `[AC-AI-001]`: (from `STORY-AI-01`) Given Ollama is running, when sending a chat completion request, then a valid JSON response is returned.
- **Constraints:**
  - Root `docker-compose.yml` remains the single supported entrypoint.
  - Bind-mount paths MUST remain stable under `${DEFAULT_AI_MODEL_DIR}` / `${DEFAULT_DATA_DIR}` (do not break existing volumes).

## 5. Work Breakdown (Tasks & Traceability)

| Task     | Description | Files Affected | Target REQ | Validation Criteria |
| -------- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Validate profile gating and root include wiring for the AI stack. | `docker-compose.yml`, `infra/08-ai/ollama/docker-compose.yml`, `infra/08-ai/open-webui/docker-compose.yml`, `infra/04-data/qdrant/docker-compose.yml` | [REQ-AI-001] | `COMPOSE_PROFILES=core,data,obs,ai docker compose --env-file .env.example config -q` exits `0`. |
| TASK-002 | Ensure DNS-only internal connectivity between Open WebUI, Ollama, and Qdrant. | `infra/08-ai/open-webui/docker-compose.yml`, `infra/08-ai/ollama/docker-compose.yml`, `infra/04-data/qdrant/docker-compose.yml` | [REQ-AI-002] | `rg -n "ipv4_address" infra/08-ai infra/04-data/qdrant` returns 0 matches. |
| TASK-003 | Ensure AI stack persistence matches spec: Ollama/Open WebUI under `${DEFAULT_AI_MODEL_DIR}`, Qdrant under `${DEFAULT_DATA_DIR}`. | `infra/08-ai/ollama/docker-compose.yml`, `infra/08-ai/open-webui/docker-compose.yml`, `infra/04-data/qdrant/docker-compose.yml`, `.env.example` | [REQ-AI-003] | Volume `device:` paths match the spec’s storage strategy. |
| TASK-004 | Verify secrets posture: do not introduce plaintext secrets in AI stack env. If any auth is needed, use `/run/secrets/*`. | `infra/08-ai/ollama/docker-compose.yml`, `infra/08-ai/open-webui/docker-compose.yml`, `specs/infra/ai/spec.md` | [SEC-AI-001] | No `*_PASSWORD` / tokens are added as plaintext env; secret needs documented and mounted via secrets. |
| TASK-005 | Add/update contributor docs for the AI stack (profile enablement, storage paths, prerequisites). | `infra/08-ai/README.md`, `README.md` | [REQ-AI-001] | Docs state the exact `COMPOSE_PROFILES=...` verification and `up` commands without ambiguity. |

**Traceability Matrix**

| Spec / PRD Item | Plan Task(s) | Verification(s) |
| --------------- | ------------ | --------------- |
| `REQ-SPC-AI-001` | `TASK-001` | `VAL-AI-PLN-001` |
| `REQ-SPC-AI-002` | `TASK-002` | `VAL-AI-PLN-002` |
| `REQ-SPC-AI-003` | `TASK-003` | `VAL-AI-PLN-001` |
| `SEC-SPC-AI-001` | `TASK-004` | `VAL-AI-PLN-001` |
| `STORY-AI-01` | `TASK-001`, `TASK-005` | `VAL-AI-PLN-003` |

**Estimates**

| Task | Priority | Points |
| ---- | -------- | ------ |
| TASK-001 | P0 | 2 |
| TASK-002 | P0 | 2 |
| TASK-003 | P0 | 2 |
| TASK-004 | P0 | 3 |
| TASK-005 | P1 | 1 |

## 6. Verification Plan

| ID          | Level       | Description | Command / How to Run | Pass Criteria |
| ----------- | ----------- | ----------- | -------------------- | ------------- |
| VAL-AI-PLN-001 | Lint/Build | Compose schema validation with AI profile enabled. | `COMPOSE_PROFILES=core,data,obs,ai docker compose --env-file .env.example config -q` | Exit `0` |
| VAL-AI-PLN-002 | Integration | Runtime healthchecks for AI services (where defined). | `COMPOSE_PROFILES=ai docker compose --env-file .env.example up -d && docker compose ps` | Services are `running`; healthchecks are `healthy` where defined |
| VAL-AI-PLN-003 | Integration | PRD acceptance proxy: validate API responds with JSON without requiring a model download. | `curl -fsS http://localhost:${OLLAMA_PORT:-11434}/api/tags >/dev/null` | Exit `0` |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Host lacks GPU runtime support | High | Document prerequisites and ensure config does not hard-require GPU on unsupported hosts. |
| Disk usage from model downloads | Medium | Document storage paths under `${DEFAULT_AI_MODEL_DIR}` and expected capacity. |

## 8. Completion Criteria

- [ ] All tasks completed
- [ ] Verification checks passed
- [ ] Documentation updated

## 9. References

- **PRD**: `docs/prd/ai-prd.md`
- **Spec**: `specs/infra/ai/spec.md`
- **ARD**: `docs/ard/ai-ard.md`
- **Architecture**: `ARCHITECTURE.md`

