---
goal: 'Create a deterministic, spec-compliant implementation path for the local Kafka messaging stack gated by the `messaging` Compose profile.'
version: '1.0'
date_created: '2026-02-27'
last_updated: '2026-02-27'
owner: 'Infrastructure Architect'
status: 'Planned'
tags: ['implementation', 'planning', 'infra', 'messaging', 'kafka', 'docker-compose']
stack: 'docker'
---

# Messaging (Kafka) Implementation Plan

_Target Directory: `specs/infra/messaging/plan.md`_

## 1. Context & Introduction

This plan operationalizes `specs/infra/messaging/spec.md` aligned with `docs/prd/messaging-prd.md`.

The messaging stack is Kafka-based (KRaft mode) and MUST be enabled via the Compose profile `messaging` with DNS-only internal connectivity on `infra_net`.

## 2. Goals & In-Scope

- **Goals:**
  - Ensure Kafka stack is gated behind the `messaging` profile.
  - Ensure 3-broker topology is preserved for local HA testing.
  - Ensure all inter-service connectivity relies on Docker DNS (no static IPs).
- **In-Scope (Scope of this Plan):**
  - Kafka stack compose file and its included components (Schema Registry, Connect, REST Proxy, UI, exporters, init).
  - Documentation drift fixes if spec and implementation diverge.

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Implementing production-grade TLS and ACL policies (deferred per PRD).
- **Out-of-Scope:**
  - External cloud event bridges or tiered storage.

## 4. Requirements & Constraints

_Note: Use Machine-Readable Identifiers (e.g., `[REQ-...]`) for traceability._

- **Requirements:**
  - `[REQ-MSG-001]`: Kafka stack MUST be gated behind the `messaging` profile (maps to `REQ-SPC-MSG-001`).
  - `[REQ-MSG-002]`: Cluster MUST be multi-node (3 brokers) for local HA testing (maps to `REQ-SPC-MSG-002`).
  - `[REQ-MSG-003]`: Internal connectivity MUST use Docker DNS (maps to `REQ-SPC-MSG-003`).
  - `[AC-MSG-001]`: (from `STORY-MSG-01`) Given a Kafka cluster, when a message is sent to `events-topic`, then it is readable by a consumer.
- **Constraints:**
  - Root `docker-compose.yml` remains the single supported entrypoint.
  - Host ports must be configurable via `.env.example` to avoid conflicts.

## 5. Work Breakdown (Tasks & Traceability)

| Task     | Description | Files Affected | Target REQ | Validation Criteria |
| -------- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Validate profile gating and root include integration for the Kafka stack. | `docker-compose.yml`, `infra/05-messaging/kafka/docker-compose.yml` | [REQ-MSG-001] | `COMPOSE_PROFILES=core,data,obs,messaging docker compose --env-file .env.example config -q` exits `0`. |
| TASK-002 | Validate 3-broker topology and persistence mapping under `${DEFAULT_MESSAGE_BROKER_DIR}`. | `infra/05-messaging/kafka/docker-compose.yml`, `.env.example` | [REQ-MSG-002] | 3 brokers exist (`kafka-1..3`) with distinct volumes bound to `${DEFAULT_MESSAGE_BROKER_DIR}/kafka/*`. |
| TASK-003 | Validate DNS-only connectivity and absence of static IP pinning. | `infra/05-messaging/kafka/docker-compose.yml` | [REQ-MSG-003] | `rg -n \"ipv4_address\" infra/05-messaging/kafka` returns 0 matches; bootstrap uses `kafka-1..3` hostnames. |
| TASK-004 | Implement a deterministic smoke workflow (topic create + produce/consume) for PRD AC. | `infra/05-messaging/kafka/README.md` | [AC-MSG-001] | Commands in `VAL-MSG-PLN-003` succeed and consumer reads the produced message. |

**Traceability Matrix**

| Spec / PRD Item | Plan Task(s) | Verification(s) |
| --------------- | ------------ | --------------- |
| `REQ-SPC-MSG-001` | `TASK-001` | `VAL-MSG-PLN-001` |
| `REQ-SPC-MSG-002` | `TASK-002` | `VAL-MSG-PLN-002` |
| `REQ-SPC-MSG-003` | `TASK-003` | `VAL-MSG-PLN-001` |
| `STORY-MSG-01` | `TASK-004` | `VAL-MSG-PLN-003` |

**Estimates**

| Task | Priority | Points |
| ---- | -------- | ------ |
| TASK-001 | P0 | 2 |
| TASK-002 | P0 | 2 |
| TASK-003 | P0 | 1 |
| TASK-004 | P1 | 3 |

## 6. Verification Plan

| ID             | Level       | Description | Command / How to Run | Pass Criteria |
| -------------- | ----------- | ----------- | -------------------- | ------------- |
| VAL-MSG-PLN-001 | Lint/Build | Compose schema validation with messaging profile enabled. | `COMPOSE_PROFILES=core,data,obs,messaging docker compose --env-file .env.example config -q` | Exit `0` |
| VAL-MSG-PLN-002 | Integration | Runtime healthcheck for brokers. | `COMPOSE_PROFILES=messaging docker compose --env-file .env.example up -d && docker compose ps` | Brokers are `running`; healthchecks are `healthy` where defined |
| VAL-MSG-PLN-003 | Integration | PRD AC: topic smoke (create + produce + consume). | `COMPOSE_PROFILES=messaging docker compose --env-file .env.example up -d && docker exec kafka-1 kafka-topics --bootstrap-server kafka-1:19092 --create --if-not-exists --topic events-topic --partitions 1 --replication-factor 3 && echo \"hello\" | docker exec -i kafka-1 kafka-console-producer --bootstrap-server kafka-1:19092 --topic events-topic >/dev/null && docker exec kafka-1 kafka-console-consumer --bootstrap-server kafka-1:19092 --topic events-topic --from-beginning --max-messages 1 --timeout-ms 10000 | rg -q \"hello\"` | Exit `0` |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Host port conflicts | Medium | Keep all host port mappings configurable via `.env.example` and document expected defaults. |
| Disk growth from broker logs | Medium | Document storage location and retention expectations; ensure adequate disk under `${DEFAULT_MESSAGE_BROKER_DIR}`. |

## 8. Completion Criteria

- [ ] All tasks completed
- [ ] Verification checks passed
- [ ] Documentation updated

## 9. References

- **PRD**: `docs/prd/messaging-prd.md`
- **Spec**: `specs/infra/messaging/spec.md`
- **ARD**: `docs/ard/messaging-ard.md`
- **Architecture**: `ARCHITECTURE.md`

