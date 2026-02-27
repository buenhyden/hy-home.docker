---
goal: 'Create a deterministic, spec-compliant implementation path to enforce standardized service requirements (healthchecks, Traefik exposure, portability) across all infra compose files.'
version: '1.0'
date_created: '2026-02-27'
last_updated: '2026-02-27'
owner: 'Reliability & Security Engineer'
status: 'Planned'
tags: ['implementation', 'planning', 'infra', 'standards', 'service', 'docker-compose']
stack: 'docker'
---

# Service Standards Implementation Plan

_Target Directory: `specs/infra/service-standards/plan.md`_

## 1. Context & Introduction

This plan operationalizes `specs/infra/service-standards/spec.md` aligned with `docs/prd/system-optimization-prd.md`.

Service standards are cross-cutting: they apply to all long-running services in `infra/**/docker-compose*.yml` and aim to prevent drift (security defaults, readiness signaling, and consistent gateway exposure).

## 2. Goals & In-Scope

- **Goals:**
  - Ensure each long-running service defines a healthcheck for readiness signaling.
  - Ensure external exposure is intentionally controlled via Traefik labels (avoid unnecessary host port mappings).
  - Ensure portability conventions (env/path abstractions and templates) are consistently applied.
- **In-Scope (Scope of this Plan):**
  - Auditing and remediation across `infra/**/docker-compose*.yml`.
  - Adjusting shared templates in `infra/common-optimizations.yml` if needed to simplify compliance.
  - Documentation updates for contributors on how to add new services in a compliant way.

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Changing service business behavior or replacing components.
- **Out-of-Scope:**
  - Standards enforcement in other repositories (only this infra repo).

## 4. Requirements & Constraints

_Note: Use Machine-Readable Identifiers (e.g., `[REQ-...]`) for traceability._

- **Requirements:**
  - `[REQ-STD-001]`: Every service MUST define a `healthcheck` in the Compose file (maps to `SPEC-STD-01`).
  - `[REQ-STD-002]`: Services SHALL expose only required ports via Traefik labels (maps to `SPEC-STD-02`).
  - `[REQ-STD-003]`: Use of `${DEFAULT_ENV}` for environment file mapping is required where applicable (maps to `SPEC-STD-03`).
  - `[AC-STD-001]`: (from `STORY-SYS-01`) Given a new `docker-compose.yml`, when extending `base-security`, then `cap_drop: ALL` is applied automatically.
- **Constraints:**
  - Healthchecks MUST avoid false positives; they must validate readiness, not only liveness.
  - Any exceptions (missing healthcheck tooling, necessary host ports) must be explicit and documented.

## 5. Work Breakdown (Tasks & Traceability)

| Task     | Description | Files Affected | Target REQ | Validation Criteria |
| -------- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Audit all long-running services for `healthcheck` coverage and add missing healthchecks. | `infra/**/docker-compose*.yml` | [REQ-STD-001] | `docker compose --env-file .env.example config` output contains `healthcheck:` for all long-running services. |
| TASK-002 | Audit external exposure patterns; ensure Traefik labels are used for intended public endpoints and remove unnecessary host `ports:` where safe. | `infra/**/docker-compose*.yml`, `infra/01-gateway/traefik/**` | [REQ-STD-002] | Services intended for external access have `traefik.http.routers.*`; unnecessary host ports are removed without breaking documented workflows. |
| TASK-003 | Normalize env mapping conventions (where applicable) to `${DEFAULT_ENV}` and consistent `.env` usage patterns. | `.env.example`, `infra/**/docker-compose*.yml` | [REQ-STD-003] | No ad-hoc envfile paths; conventions documented and consistent. |
| TASK-004 | Validate security baseline propagation via `extends: base-security` (cap_drop/no-new-privileges). | `infra/common-optimizations.yml`, representative compose files using `base-security` (e.g. `infra/05-messaging/kafka/docker-compose.yml`) | [AC-STD-001] | `docker compose --env-file .env.example config | rg -q \"cap_drop:\\n\\s*- ALL\"` exits `0`. |

**Traceability Matrix**

| Spec / PRD Item | Plan Task(s) | Verification(s) |
| --------------- | ------------ | --------------- |
| `SPEC-STD-01` | `TASK-001` | `VAL-STD-PLN-001` |
| `SPEC-STD-02` | `TASK-002` | `VAL-STD-PLN-001` |
| `SPEC-STD-03` | `TASK-003` | `VAL-STD-PLN-001` |
| `STORY-SYS-01` | `TASK-004` | `VAL-STD-PLN-002` |

**Estimates**

| Task | Priority | Points |
| ---- | -------- | ------ |
| TASK-001 | P0 | 5 |
| TASK-002 | P1 | 5 |
| TASK-003 | P2 | 3 |
| TASK-004 | P0 | 2 |

## 6. Verification Plan

| ID             | Level       | Description | Command / How to Run | Pass Criteria |
| -------------- | ----------- | ----------- | -------------------- | ------------- |
| VAL-STD-PLN-001 | Lint/Build | Schema validation (ensures healthchecks and labels resolve). | `docker compose --env-file .env.example config -q` | Exit `0` |
| VAL-STD-PLN-002 | Lint/Build | Security baseline propagation (cap_drop). | `docker compose --env-file .env.example config | rg -q \"cap_drop:\\n\\s*- ALL\"` | Exit `0` |
| VAL-STD-PLN-003 | Integration | Runtime readiness behavior (spot-check). | `docker compose --env-file .env.example up -d && docker compose ps` | Services reach `healthy` where defined; unhealthy services investigated |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Some images lack `curl/wget` for healthchecks | Medium | Use protocol-level checks, app-provided endpoints, or minimal shell healthchecks without adding new tooling. |
| Removing host ports breaks local workflows | Medium | Remove ports only when Traefik exposure is intended and documented; keep ports when required for non-HTTP tooling. |

## 8. Completion Criteria

- [ ] All tasks completed
- [ ] Verification checks passed
- [ ] Documentation updated

## 9. References

- **PRD**: `docs/prd/system-optimization-prd.md`
- **Spec**: `specs/infra/service-standards/spec.md`
- **ARD**: `docs/ard/system-optimization-ard.md`
- **Architecture**: `ARCHITECTURE.md`

