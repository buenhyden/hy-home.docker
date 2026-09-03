---
title: RedisInsight Recovery Runbook
version: 1.0.0
type: operation/runbook
layer: operations
status: active
owner: "@buenhyden"
artifact_id: RUN-0076
parent_ids:
  - GDE-0076
created: 2026-05-17
updated: 2026-08-11
---
<!-- Target: docs/05.operations/catalog/11-laboratory/0076-redisinsight/runbook.md -->

# RedisInsight Recovery Runbook

## Overview

> Scope: RedisInsight route hardening, root-active admin profile evidence, and non-destructive connection diagnosis.

이 런북은 RedisInsight UI 접속 실패, Redis/Valkey connection failure, route hardening drift를 진단하고 비파괴적 evidence를 남기는 절차를 정의한다.

### Purpose

RedisInsight의 current image/route/storage boundary를 유지하면서 운영 캐시 직접 수정이나 data reset을 승인 없는 복구 절차로 수행하지 않도록 한다.

## When to Use

- `redisinsight.${DEFAULT_URL}` UI가 응답하지 않을 때.
- Redis/Valkey 연결이 실패하거나 key browser가 비어 있을 때.
- hardening check에서 RedisInsight image, static route, middleware, healthcheck drift가 감지될 때.

## Procedure

### Checklist

- [ ] target Redis/Valkey endpoint와 권한 범위를 기록한다.
- [ ] RedisInsight data path 변경이나 EULA/connection config 변경 내역을 기록한다.
- [ ] cache mutation, data reset, volume deletion은 승인 필요 작업으로 분리한다.

### Steps

1. static hardening을 확인한다: `bash scripts/hardening/check-all-hardening.sh 11-laboratory`.
2. root-active admin profile을 확인한다: `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`.
3. 실행 중이면 상태와 로그를 기록한다: `docker ps --format '{{.Names}}\t{{.Status}}'`, `docker logs --tail 100 redisinsight`.
4. route drift가 있으면 normal/static router 모두 `gateway-standard-chain@file,redisinsight-admin-ip@docker,sso-errors@file,sso-auth@file`로 복구한다.
5. Redis/Valkey 연결 실패는 endpoint host/port와 승인된 credential reference만 확인한다. credential 값은 출력하지 않는다.

### Verification Steps

- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`
- `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
- 활성화된 runtime에서 UI 접속 및 read-only inspection evidence를 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail 100 redisinsight`
- **Static config**: [RedisInsight compose](../../../../../infra/11-laboratory/redisinsight/docker-compose.yml)

### Safe Rollback or Recovery Procedure

N/A — no verified config reset, volume deletion, or cache mutation procedure is documented for autonomous execution.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: stop if credential values or cache data values may be exposed.
- **Eval Re-run**: hardening, root profile validation, doc traceability.

## Evidence

- Record hardening output, root profile validation result, container status/log tail, and read-only connection diagnosis.

## Rollback or Recovery

If data reset, volume deletion, cache mutation, credential rotation, or broad restart is required, stop and escalate.

## Escalation

Escalate to the owning operator when cache mutation, connection credential changes, data reset/delete, or auth/allowlist changes are required.

## Traceability

- Declared parent: [RedisInsight Usage Guide](guide.md) (`GDE-0076`)
- Governing authority: [11-laboratory Architecture Description](../../../../02.architecture/descriptions/0011-laboratory-architecture.md) (`AD-0011`)
- Subject peers: [Guide](guide.md) (`GDE-0076`), [Policy](policy.md) (`POL-0076`)

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Operations policy](policy.md)
