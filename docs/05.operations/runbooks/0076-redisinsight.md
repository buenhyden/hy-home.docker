---
title: "RedisInsight Recovery Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0076"
parent_ids:
- "GDE-0076"
created: "2026-05-17"
---

# RedisInsight Recovery Runbook

## When to Use

gateway login failure, lost/corrupt settings, target auth failure, credential
exposure, settings restore, 또는 upgrade에 사용한다.

## Procedure

1. 루트에서 validate하고 점검한다.

   ```bash
   docker compose --profile admin-data config --quiet
   docker compose --profile admin-data ps redisinsight
   docker compose --profile admin-data logs --tail=200 redisinsight
   ```

2. gateway/CIDR, RedisInsight settings, target database 증상을 구분한다. 명시적으로
   승인되지 않는 한 administrator target credential로 테스트하지 않는다.
3. 저장된 credential이 노출되었을 수 있으면 RedisInsight를 중지하고, 각 target에서
   rotate하고, 복구 후 connection definition을 제거/재추가하고, sanitized evidence만
   보존한다.
4. `/data` ownership/free-space와 gateway control이 통과한 후에만 재시작한다.

### Settings restore and upgrade

1. RedisInsight를 중지하고 `/data` 전체를 protected storage로 복사한다. checksum과
   source commit을 기록하고 credential-bearing material로 보호한다.
2. production target network가 차단된 isolated instance로 복원한다. source
   deployment에 `RI_ENCRYPTION_KEY`가 있었다면 동일한 key를 사용한다. 현재 tracked
   configuration은 이를 선언하지 않는다.
3. live target에 연결하지 않고 settings/log count와 UI access를 확인한다.
4. upgrade 시에는 release/license note를 검토하고, 복사된 settings에서 target image를
   테스트하고, gateway access와 disposable test database connection을 확인한다.

## Evidence

exit, source commit, settings checksum/count, gateway/CIDR boolean,
credential-rotation receipt, target account scope, 최종 상태를 기록한다. password,
key, query history, data 값은 기록하지 않는다.

## Rollback or Recovery

settings restore와 upgrade rehearsal은 **계획되었으나 미실행** 상태이다. target
Redis/Valkey data의 restore는 target engine runbook 소관이다.

## Escalation

credential exposure, encrypted data의 encryption key 누락, 알 수 없는 target
authority, settings corruption, license 모호성, restore rehearsal 중 production
target reachability가 있으면 중단한다.

## Traceability

- [Guide](../guides/0076-redisinsight.md) (`GDE-0076`)
- [Policy](../policies/0076-redisinsight.md) (`POL-0076`)
- [RedisInsight Compose](../../../infra/11-laboratory/redisinsight/docker-compose.yml)

## Related Documents

- [RedisInsight configuration](https://redis.io/docs/latest/operate/redisinsight/configuration/)
