---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-03-28-01-gateway-optimization-hardening-plan.md -->

# 01-Gateway Optimization Hardening Implementation Plan

## Overview

This document is the implementation plan for optimizing `infra/01-gateway` Traefik/Nginx against the `Traefik Primary, Balanced Hardening` baseline. It includes configuration changes, validation automation, CI gates, and documentation traceability synchronization across `04.execution/plans` and `05.operations/{guides,policies,runbooks}`.

## Context

- Baseline catalog: [infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
- Baseline plan: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- Scope decisions:
  - Scope: `Config+Docs`
  - Runtime model: `Traefik Primary`
  - Hardening level: `Balanced`
  - Validation gate: `Strict CI Gate`
  - Traefik scope: `Gateway-owned routers only`

## Goals & In-Scope

- **Goals**:
  - Apply the Traefik standard middleware chain (`rate-limit/retry/circuit-breaker`) to routers owned by 01-gateway.
  - Harden Nginx with a readonly operations model and explicit failover/timeout policy.
  - Enforce 01-gateway changes through automated CI validation.
  - Synchronize plan, operations policy, runbook, and guide documents through cross-links and indexes.
- **In Scope**:
  - `infra/01-gateway/traefik/**`, `infra/01-gateway/nginx/**`
  - `scripts/hardening/check-all-hardening.sh 01-gateway`, `.github/workflows/ci-quality.yml`
  - `docs/04.execution/plans`, `docs/04.execution/tasks`, `docs/05.operations/{guides,policies,runbooks}/01-gateway`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Bulk-changing router labels across tiers 02 through 11
  - Changing authentication or business logic
- **Out of Scope**:
  - Adding new external ports or services
  - Changing APIs, types, or schemas

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-GW-001 | Define the Traefik standard middleware chain | `infra/01-gateway/traefik/dynamic/middleware.yml` | REQ-GW-TRAEFIK-CHAIN | `req-rate-limit/retry/circuit-breaker/gateway-standard-chain` exists |
| PLN-GW-002 | Apply the chain to the dashboard router | `infra/01-gateway/traefik/docker-compose.yml` | REQ-GW-TRAEFIK-ROUTER | `dashboard-auth@file,gateway-standard-chain@file` is applied |
| PLN-GW-003 | Convert Nginx to a readonly template plus tmpfs | `infra/01-gateway/nginx/docker-compose.yml` | REQ-GW-NGINX-READONLY | Readonly template, required tmpfs entries, and `/ping` healthcheck exist |
| PLN-GW-004 | Harden Nginx timeout/failover/cache policy | `infra/01-gateway/nginx/config/nginx.conf` | REQ-GW-NGINX-HARDEN | `server_tokens`, timeout, upstream fail params, `proxy_next_upstream`, and static cache policy are applied |
| PLN-GW-005 | Add Gateway hardening validation script coverage | `scripts/hardening/check-all-hardening.sh 01-gateway`, `scripts/README.md` | REQ-GW-VERIFY-AUTO | Script returns non-zero on failure and zero on pass |
| PLN-GW-006 | Connect the CI Strict Gate | `.github/workflows/ci-quality.yml` | REQ-GW-CI-GATE | `infrastructure-hardening` job runs as required |
| PLN-GW-007 | Synchronize document traceability | `docs/04.execution/plans/**`, `docs/04.execution/tasks/**`, `docs/05.operations/{guides,policies,runbooks}/01-gateway/**` | REQ-GW-DOC-TRACE | Cross-links and README indexes are reflected |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-GW-001 | Structural | Static Gateway hardening policy validation | `bash scripts/hardening/check-all-hardening.sh 01-gateway` | 0 failures |
| VAL-GW-002 | Compliance | Template/security baseline validation | `bash scripts/validation/check-template-security-baseline.sh` | 0 failures |
| VAL-GW-003 | Traceability | Execution/operations document traceability validation | `bash scripts/validation/check-doc-traceability.sh` | 0 failures |
| VAL-GW-004 | Compose | root-active Traefik compose resolution validation | `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh` | Output without errors |
| VAL-GW-005 | Runtime lint | Nginx configuration syntax validation | `docker compose exec nginx nginx -t` in the approved Nginx runtime context | `syntax is ok`; standalone service-local compose is not used as readiness evidence |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Dashboard requests return more 429 responses | Medium | Keep current `req-rate-limit` values (100/50), observe, then tune |
| retry/circuit-breaker changes abnormal response patterns | Medium | Limit application scope to gateway-owned routers |
| Write path errors occur after readonly conversion | High | Declare tmpfs for `/var/cache/nginx`, `/var/log/nginx`, and `/var/run` |
| An nginx.conf mistake blocks reload | High | Pre-validate with `nginx -t` and provide runbook rollback procedures |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Pass three static checks: `infrastructure-hardening`, `template-security`, and `doc-traceability`.
- **Sandbox / Canary Rollout**: Apply Traefik first, then Nginx.
- **Human Approval Gate**: Merge after Infra/Ops reviewer approval.
- **Rollback Trigger**: Restore the previous commit if authentication loops, large-scale 429 responses, or `/ping` failures occur.
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] Traefik/Nginx configuration changes reflected
- [x] Gateway hardening script and CI gate added
- [x] Plan/Task/Operation/Runbook/Guide documents synchronized
- [x] Related README indexes refreshed
- [x] Verification commands VAL-GW-001 through VAL-GW-004 passed

## Related Documents

- **Operations Catalog**: [infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
- **Parent Priority Plan**: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- **Task**: [2026-03-28-01-gateway-optimization-hardening-tasks.md](../tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)
- **Gateway Operations**: [01-gateway/README.md](../../05.operations/guides/01-gateway/README.md)
- **Gateway Runbooks**: [01-gateway/README.md](../../05.operations/runbooks/01-gateway/README.md)
