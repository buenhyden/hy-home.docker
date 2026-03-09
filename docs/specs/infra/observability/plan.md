---
goal: 'Create a deterministic, spec-compliant implementation path for the LGTM observability stack gated by the `obs` Compose profile and configured via secrets-first inputs.'
version: '1.0'
date_created: '2026-02-27'
last_updated: '2026-02-27'
owner: 'Reliability Engineer'
status: 'Planned'
tags: ['implementation', 'planning', 'infra', 'observability', 'lgtm', 'grafana', 'loki', 'tempo', 'prometheus', 'docker-compose']
stack: 'docker'
---

# Observability (LGTM) Implementation Plan

_Target Directory: `specs/infra/observability/plan.md`_

## 1. Context & Introduction

This plan operationalizes `specs/infra/observability/spec.md` aligned with `docs/prd/observability-prd.md`.

The observability stack (LGTM) MUST be enabled via Compose profile `obs`, and MUST inject sensitive values using Docker secrets (`/run/secrets/*`).

## 2. Goals & In-Scope

- **Goals:**
  - Ensure observability stack is gated behind `obs` profile.
  - Ensure Grafana and related sensitive configuration uses Docker secrets.
  - Ensure the shared logging driver/template strategy is applied consistently where supported.
- **In-Scope (Scope of this Plan):**
  - `infra/06-observability/docker-compose.yml` and referenced config files.
  - Root secrets registry in `docker-compose.yml` as required for obs services.
  - Documentation drift fixes if spec and implementation diverge.

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Managed SaaS observability (Datadog/NewRelic).
- **Out-of-Scope:**
  - Application business KPI dashboards.

## 4. Requirements & Constraints

_Note: Use Machine-Readable Identifiers (e.g., `[REQ-...]`) for traceability._

- **Requirements:**
  - `[REQ-OBS-001]`: Observability stack MUST be gated behind `obs` profile (maps to `REQ-SPC-OBS-001`).
  - `[SEC-OBS-001]`: Secrets (Grafana admin, SMTP, etc.) MUST be injected via Docker secrets (maps to `REQ-SPC-OBS-002`).
  - `[REQ-OBS-002]`: Containers SHOULD use Loki logging driver via shared templates where supported (maps to `REQ-SPC-OBS-003`).
  - `[AC-OBS-001]`: (from `STORY-OBS-01`) Given a trace ID, when searching in Grafana, then the complete request span tree is displayed.
- **Constraints:**
  - Secrets MUST NOT be printed in logs.
  - Root `docker-compose.yml` remains the single supported entrypoint.

## 5. Work Breakdown (Tasks & Traceability)

| Task     | Description | Files Affected | Target REQ | Validation Criteria |
| -------- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Validate profile gating and root include integration for the obs stack. | `docker-compose.yml`, `infra/06-observability/docker-compose.yml` | [REQ-OBS-001] | `COMPOSE_PROFILES=core,data,obs docker compose --env-file .env.example config -q` exits `0`. |
| TASK-002 | Validate secrets-first configuration in Grafana/Prometheus/etc. | `infra/06-observability/docker-compose.yml`, `docker-compose.yml` | [SEC-OBS-001] | Secrets are passed via `*_FILE` or `cat /run/secrets/*`; no plaintext password env introduced. |
| TASK-003 | Validate template inheritance and logging driver consistency where supported. | `infra/common-optimizations.yml`, `infra/06-observability/docker-compose.yml` | [REQ-OBS-002] | Services extend shared templates and `docker compose ... config` resolves cleanly. |
| TASK-004 | Define and document a minimal trace UX smoke workflow for PRD AC. | `infra/06-observability/README.md` | [AC-OBS-001] | Grafana health endpoint is reachable; trace UI smoke steps are documented and reproducible. |

**Traceability Matrix**

| Spec / PRD Item | Plan Task(s) | Verification(s) |
| --------------- | ------------ | --------------- |
| `REQ-SPC-OBS-001` | `TASK-001` | `VAL-OBS-PLN-001` |
| `REQ-SPC-OBS-002` | `TASK-002` | `VAL-OBS-PLN-001` |
| `REQ-SPC-OBS-003` | `TASK-003` | `VAL-OBS-PLN-001` |
| `STORY-OBS-01` | `TASK-004` | `VAL-OBS-PLN-003` |

**Estimates**

| Task | Priority | Points |
| ---- | -------- | ------ |
| TASK-001 | P0 | 2 |
| TASK-002 | P0 | 3 |
| TASK-003 | P1 | 2 |
| TASK-004 | P2 | 2 |

## 6. Verification Plan

| ID             | Level       | Description | Command / How to Run | Pass Criteria |
| -------------- | ----------- | ----------- | -------------------- | ------------- |
| VAL-OBS-PLN-001 | Lint/Build | Compose schema validation with obs profile enabled. | `COMPOSE_PROFILES=core,data,obs docker compose --env-file .env.example config -q` | Exit `0` |
| VAL-OBS-PLN-002 | Integration | Runtime healthchecks for obs services (where defined). | `COMPOSE_PROFILES=obs docker compose --env-file .env.example up -d && docker compose ps` | Services are `running`; healthchecks are `healthy` where defined |
| VAL-OBS-PLN-003 | Integration | PRD acceptance proxy: Grafana API health endpoint reachable. | `curl -fk https://grafana.${DEFAULT_URL}/api/health >/dev/null` | Exit `0` |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Loki driver/plugin unavailable on host | High | Document host prerequisites; treat missing plugin as a hard dependency for stacks using Loki driver. |
| High-cardinality labels overload Loki | Medium | Document label hygiene rules and avoid unbounded label values. |

## 8. Completion Criteria

- [ ] All tasks completed
- [ ] Verification checks passed
- [ ] Documentation updated

## 9. References

- **PRD**: `docs/prd/observability-prd.md`
- **Spec**: `specs/infra/observability/spec.md`
- **ARD**: `docs/ard/observability-ard.md`
- **Architecture**: `ARCHITECTURE.md`

