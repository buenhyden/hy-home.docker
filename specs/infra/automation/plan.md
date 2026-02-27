---
goal: 'Create a deterministic, spec-compliant implementation path for init/sidecar automation (idempotent provisioning containers) across the Docker Compose stack.'
version: '1.0'
date_created: '2026-02-27'
last_updated: '2026-02-27'
owner: 'Platform Architect'
status: 'Planned'
tags: ['implementation', 'planning', 'infra', 'automation', 'init', 'sidecar', 'docker-compose']
stack: 'docker'
---

# Infrastructure Automation Implementation Plan

_Target Directory: `specs/infra/automation/plan.md`_

## 1. Context & Introduction

This plan operationalizes `specs/infra/automation/spec.md` aligned with `docs/prd/infra-automation-prd.md`.

The goal is deterministic Day-0 bootstrap via one-shot init/sidecar containers that provision dependencies (buckets, users, topics, schemas) safely and repeatably.

## 2. Goals & In-Scope

- **Goals:**
  - Ensure init/sidecar containers are idempotent and safe to rerun.
  - Ensure init/sidecar containers fail fast with non-zero exit on readiness failures.
  - Ensure credentials are passed only via Docker secrets (`/run/secrets/*`).
- **In-Scope (Scope of this Plan):**
  - Existing init containers in the repo (Kafka, MinIO, Postgres, Valkey).
  - Compose ordering via `depends_on: { condition: service_healthy }`.
  - Documentation drift fixes to keep spec and implementation aligned.

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Terraform-managed provisioning for the local stack (explicitly deferred in PRD).
  - Vault-based rotation or dynamic credential issuance.
- **Out-of-Scope:**
  - Application schema migrations beyond infra readiness (unless explicitly adopted later).

## 4. Requirements & Constraints

_Note: Use Machine-Readable Identifiers (e.g., `[REQ-...]`) for traceability._

- **Requirements:**
  - `[REQ-AUTO-001]`: Init containers MUST be idempotent and safe to rerun (maps to `REQ-SPC-AUTO-001`).
  - `[REQ-AUTO-002]`: Init containers MUST fail fast with non-zero exit on readiness failure (maps to `REQ-SPC-AUTO-002`).
  - `[SEC-AUTO-001]`: Credentials MUST be provided via Docker secrets (maps to `SEC-SPC-AUTO-001`).
  - `[REQ-AUTO-003]`: Provisioning MUST use Docker DNS (maps to `REQ-SPC-AUTO-003`).
  - `[AC-AUTO-001]`: (from `STORY-AUTO-01`) Given Kafka is healthy, when `kafka-init` runs, then baseline topics are created automatically.
- **Constraints:**
  - Init containers MUST NOT echo secret values.
  - Init container ordering MUST rely on healthchecks/readiness, not sleeps alone.

## 5. Work Breakdown (Tasks & Traceability)

| Task     | Description | Files Affected | Target REQ | Validation Criteria |
| -------- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Inventory and document all init/sidecar containers and their provisioned resources. | `docker-compose.yml`, `infra/04-data/minio/docker-compose.yml`, `infra/05-messaging/kafka/docker-compose.yml`, `infra/04-data/postgresql-cluster/docker-compose.yml`, `infra/04-data/valkey-cluster/docker-compose.yml` | [REQ-AUTO-001] | Every init container is listed with its deterministic output (topics/buckets/users). |
| TASK-002 | Enforce idempotency semantics for each init container (use `--if-not-exists`, `--ignore-existing`, or safe rerun patterns). | `infra/04-data/minio/docker-compose.yml`, `infra/05-messaging/kafka/docker-compose.yml` | [REQ-AUTO-001] | Re-running init containers does not fail due to “already exists” errors. |
| TASK-003 | Ensure readiness gating and fail-fast behavior using `depends_on` + healthchecks and timeouts. | `infra/04-data/minio/docker-compose.yml`, `infra/05-messaging/kafka/docker-compose.yml`, related dependent compose files | [REQ-AUTO-002] | If a dependency never becomes healthy, the init container exits non-zero within a bounded time. |
| TASK-004 | Ensure all credentials used by init containers are read from `/run/secrets/*` and not passed as plaintext env. | `docker-compose.yml`, `infra/04-data/minio/docker-compose.yml`, `infra/06-observability/docker-compose.yml` | [SEC-AUTO-001] | No credentials are introduced via plaintext env; all are defined as secrets and mounted. |
| TASK-005 | Ensure all provisioning uses Docker DNS endpoints (no hard-coded IPs). | `infra/**/docker-compose*.yml` (init containers only) | [REQ-AUTO-003] | `rg -n "172\\.|ipv4_address" infra` finds no provisioning endpoints using fixed IPs. |

**Traceability Matrix**

| Spec / PRD Item | Plan Task(s) | Verification(s) |
| --------------- | ------------ | --------------- |
| `REQ-SPC-AUTO-001` | `TASK-001`, `TASK-002` | `VAL-AUTO-PLN-001`, `VAL-AUTO-PLN-003` |
| `REQ-SPC-AUTO-002` | `TASK-003` | `VAL-AUTO-PLN-002` |
| `SEC-SPC-AUTO-001` | `TASK-004` | `VAL-AUTO-PLN-001` |
| `REQ-SPC-AUTO-003` | `TASK-005` | `VAL-AUTO-PLN-001` |
| `STORY-AUTO-01` | `TASK-002`, `TASK-003` | `VAL-AUTO-PLN-004` |

**Estimates**

| Task | Priority | Points |
| ---- | -------- | ------ |
| TASK-001 | P1 | 2 |
| TASK-002 | P0 | 3 |
| TASK-003 | P0 | 3 |
| TASK-004 | P0 | 2 |
| TASK-005 | P1 | 2 |

## 6. Verification Plan

| ID             | Level       | Description | Command / How to Run | Pass Criteria |
| -------------- | ----------- | ----------- | -------------------- | ------------- |
| VAL-AUTO-PLN-001 | Lint/Build | Static config validation. | `docker compose --env-file .env.example config -q` | Exit `0` |
| VAL-AUTO-PLN-002 | Integration | Runtime behavior: init containers succeed when deps are healthy. | `docker compose --env-file .env.example up -d && docker compose ps -a` | All init containers reach `exited (0)` |
| VAL-AUTO-PLN-003 | Integration | Idempotency: re-run does not fail. | Run `docker compose --env-file .env.example up -d` twice | Second run yields no init failures |
| VAL-AUTO-PLN-004 | Integration | PRD AC: `kafka-init` creates baseline topics. | `COMPOSE_PROFILES=messaging docker compose --env-file .env.example up -d && docker exec kafka-1 kafka-topics --bootstrap-server kafka-1:19092 --list | rg -q \"^(infra-events|application-logs)$\"` | Exit `0` |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Dependency never becomes ready (init stuck) | High | Use healthchecks + bounded retries/timeouts and exit non-zero with actionable logs. |
| Drift between init behavior and docs/spec | Medium | Keep init responsibilities documented and verified via deterministic commands. |

## 8. Completion Criteria

- [ ] All tasks completed
- [ ] Verification checks passed
- [ ] Documentation updated

## 9. References

- **PRD**: `docs/prd/infra-automation-prd.md`
- **Spec**: `specs/infra/automation/spec.md`
- **ARD**: `docs/ard/infra-automation-ard.md`
- **Architecture**: `ARCHITECTURE.md`

