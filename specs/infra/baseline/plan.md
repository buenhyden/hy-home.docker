---
goal: 'Create a deterministic, spec-compliant implementation path for the baseline infra invariants (pinned images, init, secrets-first) and its bootstrap prerequisites.'
version: '1.0'
date_created: '2026-02-27'
last_updated: '2026-02-27'
owner: 'Infrastructure Architect'
status: 'Planned'
tags: ['implementation', 'planning', 'infra', 'baseline', 'docker-compose']
stack: 'docker'
---

# Infrastructure Baseline Implementation Plan

_Target Directory: `specs/infra/baseline/plan.md`_

## 1. Context & Introduction

This plan operationalizes the baseline invariants defined in `specs/infra/baseline/spec.md`, aligned with `docs/prd/infra-baseline-prd.md`.

The baseline defines the minimum compliant state required for contributors to bootstrap and validate the root-only Compose stack deterministically.

## 2. Goals & In-Scope

- **Goals:**
  - Ensure infra images are pinned (no `latest` tags).
  - Ensure `init: true` is enforced by default (directly or via templates).
  - Ensure secrets-first handling via Docker secrets (`/run/secrets/*`).
  - Ensure contributors can detect missing bootstrap prerequisites via preflight.
- **In-Scope (Scope of this Plan):**
  - Root `docker-compose.yml` + included infra compose files.
  - Bootstrap tools under `scripts/` used for preflight and validation.
  - Documentation drift fixes if the implementation deviates from the spec.

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Re-architecting tiers, profiles, or service topology.
  - Introducing Kubernetes or non-Compose orchestration.
- **Out-of-Scope:**
  - Application-level feature development.

## 4. Requirements & Constraints

_Note: Use Machine-Readable Identifiers (e.g., `[REQ-...]`) for traceability._

- **Requirements:**
  - `[REQ-BSL-001]`: All images MUST use pinned version tags; `latest` is prohibited (maps to `SPEC-BASE-01`).
  - `[REQ-BSL-002]`: Every service SHALL utilize `init: true` for signal handling (maps to `SPEC-BASE-02`).
  - `[SEC-BSL-001]`: Sensitive data MUST be injected via `/run/secrets/` filesystem mounts (maps to `SPEC-BASE-03`).
  - `[AC-BSL-001]`: (from `STORY-BASE-01`) Given a clean Docker environment, when running `preflight-compose.sh`, then missing secrets are identified.
- **Constraints:**
  - Changes MUST preserve persistent data compatibility (do not break existing host volume layouts).

## 5. Work Breakdown (Tasks & Traceability)

| Task     | Description | Files Affected | Target REQ | Validation Criteria |
| -------- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Audit and enforce pinned image tags across root and included compose files (no `latest`). | `docker-compose.yml`, `infra/**/docker-compose*.yml` | [REQ-BSL-001] | `rg -n \"image:.*:latest\\b\" docker-compose.yml infra` returns 0 matches. |
| TASK-002 | Ensure `init: true` is present by default via `infra/common-optimizations.yml` templates or explicit service config. | `infra/common-optimizations.yml`, `infra/**/docker-compose*.yml` | [REQ-BSL-002] | `docker compose --env-file .env.example config` output includes `init: true` for services using baseline templates. |
| TASK-003 | Ensure all sensitive values are injected via Docker secrets mounted under `/run/secrets/*` (no plaintext secret env vars). | `docker-compose.yml`, `infra/**/docker-compose*.yml`, `secrets/**` | [SEC-BSL-001] | Secrets are referenced via `*_FILE=/run/secrets/*` or `cat /run/secrets/*`; no plaintext passwords/tokens introduced. |
| TASK-004 | Ensure contributors can identify missing bootstrap prerequisites (env/secrets/certs/dirs) via preflight script. | `scripts/preflight-compose.sh`, `scripts/README.md`, `runbooks/core/infra-bootstrap-runbook.md` | [AC-BSL-001] | Running `bash scripts/preflight-compose.sh` reports missing prerequisites with non-zero exit (or WARN where documented). |

**Traceability Matrix**

| Spec / PRD Item | Plan Task(s) | Verification(s) |
| --------------- | ------------ | --------------- |
| `SPEC-BASE-01` | `TASK-001` | `VAL-BSL-PLN-002` |
| `SPEC-BASE-02` | `TASK-002` | `VAL-BSL-PLN-001` |
| `SPEC-BASE-03` | `TASK-003` | `VAL-BSL-PLN-001` |
| `STORY-BASE-01` | `TASK-004` | `VAL-BSL-PLN-003` |

**Estimates**

| Task | Priority | Points |
| ---- | -------- | ------ |
| TASK-001 | P0 | 2 |
| TASK-002 | P0 | 3 |
| TASK-003 | P0 | 3 |
| TASK-004 | P1 | 2 |

## 6. Verification Plan

| ID             | Level       | Description | Command / How to Run | Pass Criteria |
| -------------- | ----------- | ----------- | -------------------- | ------------- |
| VAL-BSL-PLN-001 | Lint/Build | Baseline schema validation for default profile set. | `COMPOSE_PROFILES=core,data,obs docker compose --env-file .env.example config -q` | Exit `0` |
| VAL-BSL-PLN-002 | Lint/Build | Pinned-image audit (no `latest`). | `rg -n \"image:.*:latest\\b\" docker-compose.yml infra` | No matches |
| VAL-BSL-PLN-003 | Integration | PRD AC: preflight detects missing prerequisites. | `bash scripts/preflight-compose.sh` | Exit is non-zero when required files are missing; output lists missing secrets clearly |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Broad cross-file changes introduce YAML breakage | Medium | Validate incrementally with `docker compose ... config -q` after each change. |
| Over-hardening breaks some images | Medium | Use shared templates and document exceptions explicitly when required. |

## 8. Completion Criteria

- [ ] All tasks completed
- [ ] Verification checks passed
- [ ] Documentation updated

## 9. References

- **PRD**: `docs/prd/infra-baseline-prd.md`
- **Spec**: `specs/infra/baseline/spec.md`
- **ARD**: `docs/ard/infra-baseline-ard.md`
- **Architecture**: `ARCHITECTURE.md`

