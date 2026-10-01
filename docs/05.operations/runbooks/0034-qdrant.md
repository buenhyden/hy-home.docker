---
title: "Qdrant Health and Recovery Triage Runbook"
version: "1.3.4"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0034"
parent_ids:
- "GDE-0034"
created: "2026-05-17"
---

# Qdrant Health and Recovery Triage Runbook

## Overview

> Scope: Triage root-active Qdrant service health, REST route (SSO) assumptions, persistence path, and evidence capture without destructive data actions.

이 런북은 health triage와 별도 승인 후 수행할 Qdrant snapshot의 격리 복원 rehearsal 계약을 제공한다. 이번 변경에서 snapshot create/recover API나 storage mutation은 실행하지 않았다.

### Purpose

Qdrant single unprivileged service의 상태, `/readyz` healthcheck, SSO 뒤의 REST Traefik route, snapshot path evidence를 수집하고 compose가 보장하는 범위 안에서만 비파괴 조치를 수행한다.

## When to Use

- `qdrant`가 unhealthy, stopped, or missing 상태일 때
- `/readyz`가 200 응답을 반환하지 않을 때
- REST route `qdrant.${DEFAULT_URL}`(SSO 뒤) 경계를 확인해야 할 때
- Qdrant operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

### Execution and stop boundary

대상: `qdrant`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Procedure

### Checklist

- [ ] 루트 compose에서 `infra/04-data/qdrant/docker-compose.yml`가 active include인지 확인한다.
- [ ] `secrets/data/qdrant_api_key.txt`와 `secrets/data/qdrant_read_only_api_key.txt`가 있고 비어 있지 않은지 값을 읽지 않고 확인한다(`test -s`).
- [ ] collection delete, snapshot recovery, volume replacement, cluster repair가 필요한 경우 이 런북을 중단하고 에스컬레이션한다.
- [ ] 모든 명령 출력은 요약으로 기록하고 application data payload는 기록하지 않는다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   docker compose --profile qdrant config --quiet
   ```

2. 서비스 상태를 확인한다.

   ```bash
   docker compose ps qdrant
   ```

3. 최근 로그를 확인한다.

   ```bash
   docker compose logs --tail=120 qdrant
   ```

4. REST readiness를 확인한다.

   ```bash
   # 6333 is the default QDRANT_PORT; substitute it if changed.
   docker compose exec qdrant bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333; printf "GET /readyz HTTP/1.0\r\n\r\n" >&3; cat <&3'
   ```

5. read-only collection inventory를 확인한다.

   ```bash
   docker compose exec qdrant bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333; printf "GET /collections HTTP/1.0\r\napi-key: %s\r\n\r\n" "$(tr -d "\r\n" </run/secrets/qdrant_api_key)" >&3; cat <&3'
   ```

6. 컨테이너가 stopped 상태이고 데이터 작업이 필요하지 않은 경우 compose로 재기동한다.

   ```bash
   docker compose --profile qdrant up -d --no-deps qdrant
   ```

### Verification Steps

- `docker compose ps qdrant`에서 `qdrant`가 running 또는 healthy 상태인지 확인한다.
- `/readyz`가 200 response evidence를 제공하는지 확인한다.
- `docker compose --profile qdrant config --quiet`가 통과하는지 확인하고, source Compose에서 `qdrant-data:/qdrant/storage:rw`와 `/qdrant/storage/snapshots`가 유지되는지 비교한다.

### Observability and Evidence Sources

- **Logs**: `docker compose logs --tail=120 qdrant`
- **Health**: `/readyz` and compose healthcheck
- **Route**: Traefik HTTP labels on `qdrant` with SSO; no gRPC route
- **Config**: `docker compose --profile qdrant config --quiet`

### Safe Rollback or Recovery Procedure

1. 이 Runbook의 runtime 복구는 evidence 수집 후 compose `up -d qdrant`를 실행하는 범위로 제한한다.
2. 실패한 isolated target과 전용 volume을 보존하고, 정확한 소유 target의 삭제는 별도 승인 후 수행한다. source service, snapshot과 tracked volume은 변경하지 않는다.

### Planned Isolated Restore Rehearsal

1. 사전 승인 후 source engine minor version, collection list/config/status, aliases, point-count invariants, snapshot scope/identifier와 free disk를 기록한다. API key가 켜져 있는지도 기록한다.
2. approved collection or full-storage snapshot을 생성하고 `/qdrant/storage/snapshots`에서 manifest/checksum과 함께 보호한다. snapshot API response나 vector payload를 evidence에 복사하지 않는다.
3. production network/route/volume을 공유하지 않는 fresh target을 same minor 또는 upstream이 허용하는 next minor로 준비한다. snapshot 크기의 약 2배 free disk와 absent target collection을 확인한다.
4. collection snapshot recovery API 또는 full-storage startup recovery 중 snapshot type에 맞는 upstream procedure 하나만 사용한다. `force`는 target collision이 명시적으로 검토된 경우에만 별도 승인한다.
5. `/readyz`, collection status/config, aliases, point counts와 representative search invariants를 검증한다. version, checksum 또는 count mismatch면 승격하지 않는다.
6. 실패하면 target을 보존하고, 정확한 소유 target의 삭제는 별도 승인 후 수행한다. production route switch, API key 교체, collection deletion과 volume replacement는 별도 승인 사항이다.

## Evidence

- 명령 이름, pass/fail 상태, service 상태, image tag, 민감 정보를 제거한 log, route label과 readiness 요약을 기록한다.
- vector payload, collection data, credential 또는 mutation API body는 기록하지 않는다.
- 문제가 container health, REST route, network 내부 gRPC, 영속성 또는 snapshot-path 증상 중 어디와 관련되는지 기록한다.

## Rollback or Recovery

데이터 복구는 위 planned isolated rehearsal로만 검증한다. 이번 변경에서는 snapshot mutation, collection restore/delete, volume replacement와 route change를 실행하지 않았다.

## Escalation

restart 후에도 `/readyz`가 실패하거나, log에 storage 손상이 나타나거나, route label이 예상한 compose와 다르거나, API key가 없어 client가 401을 받거나, data 작업이 필요하면 저장소 소유자 @buenhyden에게 에스컬레이션한다. 민감 정보를 제거한 log, 렌더링된 compose evidence, service 상태와 시도한 단계를 포함한다.

## Traceability

- Declared parent: [Qdrant Usage Guide](../guides/0034-qdrant.md) (`GDE-0034`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0034-qdrant.md) (`GDE-0034`), [Policy](../policies/0034-qdrant.md) (`POL-0034`)

## Related Documents

- [Compose implementation: infra/04-data/qdrant/docker-compose.yml](../../../infra/04-data/qdrant/docker-compose.yml)

- [Qdrant snapshots](https://qdrant.tech/documentation/operations/snapshots/)
- [Qdrant migration and recovery](https://qdrant.tech/documentation/migration-recovery-options/)

- [Operations index](../README.md)
- [Usage guide](../guides/0034-qdrant.md)
- [Operations policy](../policies/0034-qdrant.md)
- [Infra README](../../../infra/04-data/qdrant/README.md)
