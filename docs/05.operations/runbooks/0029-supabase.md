---
title: "Supabase Stack Health Runbook"
version: "1.1.5"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "RUN-0029"
parent_ids:
- "GDE-0029"
created: "2026-05-17"
---

# Supabase Stack Health Runbook

## Overview

이 런북은 health triage와 별도 승인 후 수행할 coherent Supabase backup의 격리 복원 rehearsal 계약을 제공한다. Supabase data profile stack의 compose render, 서비스 상태, Kong 접근 경로, 주요 로그를 안전하게 확인하고, secret 노출이나 destructive recovery가 필요한 경우 빠르게 escalation한다. 아래 database/storage/config 복원은 이번 문서 변경에서 실행하지 않았다.

## Trigger and Preconditions

- `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `db`, `analytics`, 또는 `supavisor`가 unhealthy이거나 누락된 경우.
- Kong HTTP/HTTPS 접근이 compose가 선언한 host port에서 응답하지 않는 경우.
- JWT rotation, dashboard 비밀번호 재설정, storage 용량, 또는 DB restore를 검토 중이며 변경 전 evidence가 필요한 경우.
- 연결된 Supabase 운영 문서나 compose 참조가 변경되어 로컬 검증 evidence가 필요한 경우.

사전 확인:

- 이 task가 destructive restore나 secret rotation이 아니라 health/access 검증 task인지 확인한다.
- compose secret ref에 대응하는 Docker Secret 파일이 존재하는지 값을 출력하지 않고 확인한다.
- `${DEFAULT_DATA_DIR}/supabase/...` runtime mount가 승인된 호스트에 존재하는지 확인한다.
- 생성된 config 검사가 내장된 secret 값을 복사하지 않도록 확인한다.

### Execution and stop boundary

대상: `analytics`, `auth`, `db`, `functions`, `imgproxy`, `kong`, `meta`, `realtime`, `rest`, `storage`, `studio`, `supavisor`, `vector`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Procedure

1. 현재 compose configuration을 렌더링한다.

   ```bash
   docker compose --profile supabase config --quiet
   ```

2. 서비스 상태를 확인한다.

   ```bash
   docker compose --profile supabase ps studio kong auth rest realtime storage db analytics supavisor
   ```

3. 관련 서비스 로그를 검사한다. secret 값을 evidence에 복사하지 않는다.

   ```bash
   docker compose --profile supabase logs kong auth rest storage db analytics supavisor
   ```

4. compose가 선언한 공개 Kong 접근 경로를 검증한다.

   ```bash
   curl -fsS "http://localhost:${SUPABASE_KONG_HTTP_HOST_PORT:-8000}/" >/dev/null
   ```

5. dashboard 접근을 확인할 경우 승인된 Kong/stack route를 사용한다. Studio용 직접 local host port가 있다고 가정하지 않는다. 현재 compose 파일은 Studio를 직접 publish하지 않는다.

6. 최종 상태 스냅샷을 캡처한다.

   ```bash
   docker compose --profile supabase ps
   ```

### Planned Isolated Restore Rehearsal

1. 사전 승인 후 Compose image declarations, PostgreSQL version/extensions, roles and databases, Storage buckets/object counts, mounted config/functions, Auth providers, JWT issuer expectations와 free capacity를 inventory한다. secret values는 manifest에 넣지 않는다.
2. PostgreSQL globals/roles, schema and data를 protected logical artifacts로 export하고 checksum한다. Storage metadata tables와 `${DEFAULT_DATA_DIR}/supabase/storage` object files는 같은 recovery point로 보존한다. Kong, functions, pooler, DB init and analytics/vector config는 별도 configuration artifact로 보존한다.
3. JWT, anon/service-role keys, SMTP/provider credentials, database passwords, vault and crypto keys는 backup data와 분리된 approved secret store에서 동일 identifier/version으로 참조한다.
4. production network, ports and volumes를 공유하지 않는 compatible empty stack을 별도 test credentials로 준비한다. roles/globals, schema, data 순서로 PostgreSQL을 복원하고 Storage objects와 metadata를 함께 배치한 후 mounted configuration을 적용한다.
5. Kong API, Auth signup/login policy, REST read, Realtime subscription, Storage object read, Function invocation, Studio metadata, analytics ingestion과 Supavisor connection을 synthetic data로 확인한다. object-count/metadata mismatch나 missing key가 있으면 승격하지 않는다.
6. 실패 시 isolated stack과 전용 volumes를 보존하고, 정확한 소유 target의 삭제는 별도 승인 후 수행한다. production cutover, DNS/route switch, secret rotation은 별도 승인 절차이며 source stack은 변경하지 않는다.

## Verification

- `docker compose --profile supabase config --quiet`
- `docker compose --profile supabase ps`
- 기대 결과: compose가 렌더링되고, 서비스가 존재하며, Kong route 상태가 기록되고, secret 값이 캡처되지 않는다.

### Observability and Evidence Sources

- **Logs**: `docker compose --profile supabase logs ...`
- **Health**: Supabase 서비스 집합에 대한 compose `ps` 상태
- **Access**: compose 변수를 사용한 Kong HTTP/HTTPS host-port 확인
- **Evidence to Capture**: 명령 이름, timestamp, 서비스 상태 요약, Kong route 결과, 생략한 destructive action

### 증거 기록

- 실행한 compose 명령, 서비스 상태, Kong route 결과, destructive recovery나 credential rotation을 생략한 이유를 기록한다.
- 실패한 검증 출력이나 서비스 증상은 secret 값을 복사하지 않고 관련 task나 incident evidence에 첨부한다.

## Rollback and Escalation

### Rollback or Recovery

1. 문서 전용 변경이면 마지막 문서 diff를 되돌리고 검증을 다시 실행한다.
2. 문서화된 확인 이후에도 서비스가 unhealthy하면 로그를 보존하고 escalation한다. 이 runbook에서 database나 storage volume을 삭제하지 않는다.
3. secret 노출이 의심되면 출력 복사를 중단하고 최소한의 context만 보존한 뒤 `## Escalation`에 따라 escalation한다.

데이터 복구는 위 planned isolated rehearsal로만 검증한다. 이 변경에서는 backup/restore, storage mutation, JWT rotation이나 credential reset을 실행하지 않았다.

### Escalation

compose 렌더링이 실패하거나, 필요한 secret이나 mounted config가 누락되거나, 문서화된 확인 이후에도 서비스가 unhealthy하거나, Kong 접근이 계속 불가능하거나, secret 노출 위험이 나타나거나, destructive database/storage/credential 변경이 필요하면 담당 operator에게 escalation한다.

## Related Documents

### Traceability

- 선언된 parent: [Supabase Usage Guide](../guides/0029-supabase.md) (`GDE-0029`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peer: [Guide](../guides/0029-supabase.md) (`GDE-0029`), [Policy](../policies/0029-supabase.md) (`POL-0029`)

- [Compose implementation: infra/04-data/supabase/docker-compose.yml](../../../infra/04-data/supabase/docker-compose.yml)

- [Supabase self-hosted restore guidance](https://supabase.com/docs/guides/self-hosting/restore-from-platform)
- [Supabase self-hosted update guidance](https://supabase.com/docs/guides/self-hosting/updating)
- [Supabase source and licenses](https://github.com/supabase/supabase)

- [Operations index](../README.md)
- [Usage guide](../guides/0029-supabase.md)
- [Operations policy](../policies/0029-supabase.md)
- [Infrastructure service README](../../../infra/04-data/supabase/README.md)
