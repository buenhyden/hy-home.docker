---
goal: 'Create a deterministic, spec-compliant implementation path for global infrastructure invariants (extends templates, path abstraction, default hardening) across all tiers.'
version: '1.0'
date_created: '2026-02-27'
last_updated: '2026-02-27'
owner: 'Platform Architect'
status: 'Planned'
tags: ['implementation', 'planning', 'infra', 'global-baseline', 'docker-compose', 'standards']
stack: 'docker'
---

# Infrastructure Global Baseline Implementation Plan

_Target Directory: `specs/infra/global-baseline/plan.md`_

## 1. Context & Introduction

This plan operationalizes the global baseline invariants defined in `specs/infra/global-baseline/spec.md` aligned with `docs/prd/system-architecture-prd.md` and `docs/ard/system-architecture-ard.md`.

These invariants apply repository-wide and are foundational to a predictable root-only Compose system using profiles and shared templates.

## 2. Goals & In-Scope

- **Goals:**
  - Ensure services extend from `infra/common-optimizations.yml` where required by the spec.
  - Ensure bind mounts use `${DEFAULT_*_DIR}` abstractions for portability.
  - Ensure hardened defaults are applied consistently via shared templates.
  - Ensure profiles allow starting only the required tiers (core/data/obs/etc.).
- **In-Scope (Scope of this Plan):**
  - `infra/common-optimizations.yml` template usage across `infra/**/docker-compose*.yml`.
  - Root `docker-compose.yml` include orchestration and profile behavior.
  - Documentation drift fixes if the implementation deviates from the spec.

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Switching orchestrators (Kubernetes, Nomad, Swarm).
  - Introducing new tiers or major topology changes.
- **Out-of-Scope:**
  - Per-service feature enhancements not related to baseline invariants.

## 4. Requirements & Constraints

_Note: Use Machine-Readable Identifiers (e.g., `[REQ-...]`) for traceability._

- **Requirements:**
  - `[REQ-GLOB-001]`: All services MUST extend from `infra/common-optimizations.yml` where applicable (maps to `SPEC-GLOB-01`).
  - `[REQ-GLOB-002]`: Bind mounts SHALL use `${DEFAULT_DATA_DIR}` (or tier-specific `${DEFAULT_*_DIR}`) variables (maps to `SPEC-GLOB-02`).
  - `[SEC-GLOB-001]`: Runtime filesystems SHALL be `read_only: true` by default (maps to `SPEC-GLOB-03`).
  - `[AC-GLOB-001]`: (from `STORY-01`) Given a multi-tier infra, when I run `docker compose --profile core up`, then only core services start.
- **Constraints:**
  - Exceptions to hardening must be explicit and justified (prefer ADR/spec updates if persistent).

## 5. Work Breakdown (Tasks & Traceability)

| Task     | Description | Files Affected | Target REQ | Validation Criteria |
| -------- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Audit and normalize `extends` usage to shared templates. | `infra/common-optimizations.yml`, `infra/**/docker-compose*.yml` | [REQ-GLOB-001] | `rg -n \"extends:\\n\\s+file:\" infra` references valid template files and `docker compose ... config -q` passes. |
| TASK-002 | Audit bind mounts and normalize to `${DEFAULT_*_DIR}` path abstractions. | `.env.example`, `infra/**/docker-compose*.yml` | [REQ-GLOB-002] | No unexpected hard-coded bind paths under `device:` outside defined defaults. |
| TASK-003 | Enforce hardened defaults via templates (read-only filesystem by default where feasible). | `infra/common-optimizations.yml`, `infra/**/docker-compose*.yml` | [SEC-GLOB-001] | Services intended to be hardened extend hardened templates; exceptions documented and minimal. |
| TASK-004 | Validate profile behavior supports starting only core services. | `infra/01-gateway/traefik/docker-compose.yml`, `infra/02-auth/keycloak/docker-compose.yml`, `infra/02-auth/oauth2-proxy/docker-compose.yml`, `docker-compose.yml` | [AC-GLOB-001] | `COMPOSE_PROFILES=core docker compose --env-file .env.example config --services | sort` output is exactly `keycloak`, `oauth2-proxy`, `traefik`. |

**Traceability Matrix**

| Spec / PRD Item | Plan Task(s) | Verification(s) |
| --------------- | ------------ | --------------- |
| `SPEC-GLOB-01` | `TASK-001` | `VAL-GLOB-PLN-001` |
| `SPEC-GLOB-02` | `TASK-002` | `VAL-GLOB-PLN-002` |
| `SPEC-GLOB-03` | `TASK-003` | `VAL-GLOB-PLN-001` |
| `STORY-01` | `TASK-004` | `VAL-GLOB-PLN-003` |

**Estimates**

| Task | Priority | Points |
| ---- | -------- | ------ |
| TASK-001 | P0 | 3 |
| TASK-002 | P0 | 3 |
| TASK-003 | P1 | 2 |
| TASK-004 | P1 | 2 |

## 6. Verification Plan

| ID                | Level       | Description | Command / How to Run | Pass Criteria |
| ----------------- | ----------- | ----------- | -------------------- | ------------- |
| VAL-GLOB-PLN-001 | Lint/Build | Global schema validation (root-only orchestration). | `docker compose --env-file .env.example config -q` | Exit `0` |
| VAL-GLOB-PLN-002 | Lint/Build | Bind-mount abstraction audit. | `rg -n \"device:\\s*/\" infra` | No unexpected hard-coded paths (only documented exceptions) |
| VAL-GLOB-PLN-003 | Integration | PRD AC: core profile isolates core services. | `COMPOSE_PROFILES=core docker compose --env-file .env.example config --services | sort` | Output is exactly: `keycloak`, `oauth2-proxy`, `traefik` |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Over-standardization breaks special-case services | Medium | Allow explicit exceptions with documentation and minimal changes. |
| Ambiguous “where applicable” for extends usage | Medium | Define and document a consistent rule: all long-running services extend a template unless explicitly excluded. |

## 8. Completion Criteria

- [ ] All tasks completed
- [ ] Verification checks passed
- [ ] Documentation updated

## 9. References

- **PRD**: `docs/prd/system-architecture-prd.md`
- **Spec**: `specs/infra/global-baseline/spec.md`
- **ARD**: `docs/ard/system-architecture-ard.md`
- **Architecture**: `ARCHITECTURE.md`
