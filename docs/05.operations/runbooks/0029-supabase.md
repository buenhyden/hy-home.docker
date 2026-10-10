---
title: "Supabase Stack Health Runbook"
version: "1.2.0"
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

### SMTP 전환 확인과 중복 퇴역

1. SMTP01의 root 단일 source, Auth source/target, COMM-002/003 alias와 파일 소비
   증거를 확인합니다. 공용 username·host·account와 Alertmanager는 변경하지 않습니다.
2. 실제 정확한 호스트 checkout에서 old path의 source, 모든 container mount,
   정기 job, backup/restore 및 외부 소비를 확인해 owning Task에 기록합니다.
   비선택 profile이나 최근 무트래픽만으로 소비자 부재를 판단하지 않습니다.
3. 제한된 로컬 비교는 다음 check mode를 사용합니다. 값·hash·길이는 출력하지 않으며
   exit 0은 이미 퇴역, 1은 변경 대기, 2는 불안전/불일치입니다. 실제 비밀 접근은
   정확한 대상에 대한 현재 사용자 권한과 owning Task 기록이 있어야 합니다.

   ```bash
   bash scripts/operations/gen-secrets.sh --retire-supabase-smtp-check
   ```

4. 총괄이 선행 전환을 수용하고 CLN01의 폐기·복구 검토를 마친 뒤에만 현재 호스트,
   Git SHA, 공개 Compose source hash, 동일 root identity, old mount 부재,
   job/backup/external 확인, canonical restore mapping과 아래 두 quiescence
   사실을 담은 값 없는 audit receipt로 적용합니다.
   receipt 자체는 권한을 발급하지 않습니다. 다음 명령은 현재 SMTP01에서 실행하지 않습니다.

   ```bash
   bash scripts/operations/gen-secrets.sh --retire-supabase-smtp --smtp-audit-proof /tmp/smtp01-audit.json
   ```

5. helper는 canonical 파일을 보존하고 COMM-003 private 값 행과 정확한 중복 파일만
   처리합니다. 동시 변경·불일치·불명확한 mount는 거부합니다. `.env`와 LAB은 읽거나
   수정하지 않습니다. 퇴역 marker 제거와 빈 folder 정리는 CLN01이 소유하며 다른 entry가
   있으면 보존합니다. 재실행으로 idempotency와 활성 old source/path 참조 0을 확인합니다.

복구는 canonical 파일과 Auth mount alias, 특정 소비자의 source 설정만 복원합니다.
기존 암호화 Restic host snapshot은 비밀 자료의 보관이지 old path의 live 소비자가
아닙니다. snapshot에서 옛 layout을 복원할 때 현재 canonical mapping을 다시 적용하며
평문 중복을 영구 유지하지 않습니다. 실제 backup/restore 검증은 별도 Task 증거이고,
source revert나 격리 SMTP 성공으로 HOME 복구를 PASS로 기록하지 않습니다. 전체 up/down,
volume 초기화와 일괄 credential 회전은 이 절차에 포함되지 않습니다.

### SMTP01과 CLN01의 root·lock·증거 계약

receipt의 필수 필드는 `host`, `git_sha`, `source_sha256`,
`root_identity: {st_dev, st_ino}`, `old_mount_consumers: []`,
`job_backup_external_verified: true`, `canonical_restore_mapping_verified: true`,
`consumer_creation_quiesced: true`, `source_private_mutation_quiesced: true`입니다.
이는 값 없는 사실 확인이며 실행 권한을 대신하지 않습니다. 현재 HOME 사실과
receipt 발급은 NOT_RUN입니다.

실제 운영 root는 `/home/hyunyoun/data/hy-home.docker`입니다. apply와 CLN01은
그 root의 device/inode를 확인하고 `secrets/.smtp01-retirement.lock`의 동일 inode에
exclusive nonblocking lock을 사용합니다. lock은 nofollow·단일 regular file·0600이며
사용 후 지우지 않습니다. 다른 worktree의 같은 상대 경로는 동일 lock이 아닙니다.
읽기 전용 check는 lock 파일을 생성하거나 변경하지 않습니다. 퇴역 CLI는 lock을
스스로 획득하므로 다른 executor가 같은 lock을 잡은 채 CLI를 중첩 호출하지 않습니다.
CLN01의 별도 writer는 동일 protocol로 직렬화하고 lock을 반납한 뒤 전용 CLI를 호출합니다.

총괄은 해당 host의 정확한 consumer recreate/start 경로와 source/private metadata
writer를 일시 정지시키고, 어떤 경로를 어떻게 멈췄는지 owning Task에 기록해야
합니다. 동일 lock은 협력하는 executor만 직렬화합니다. Docker daemon이나 다른
프로세스의 쓰기를 강제로 막지 않으므로, 두 quiescence 사실을 확인하지 못하면
apply를 실행하지 않습니다. 본 문서만으로 stop 명령이나 대상 부재를 가정하지 않습니다.

helper는 공개 source와 mount 증거를 반복 검사하고 metadata/old file을 atomic
quarantine으로 옮겨 identity와 내용을 확인합니다. 다른 writer의 새 파일을 덮어쓰지
않습니다. 성공 전 old pathname 부재와 private metadata postcondition을 검사합니다.
변경 이후 실패는 `unsafe_after_mutation`, `applied: true`, `completed: false`, exit 2로
보고합니다. 이를 무변경 실패나 퇴역 성공으로 취급하지 않고 현재 pathname과 보존된
quarantine을 제한된 로컬 프로세스에서 확인합니다. 평문 복제본을 영구 보관하지 않으며
필요한 custody·정리·복구는 정확한 대상에 대한 CLN01/총괄 지시로 처리합니다.

퇴역 실행 코드는 `scripts/lib/ops/smtp_contract.py`입니다. 생성기의 전용 모드만
이 모듈을 호출합니다. SMTP01이 source·consumer·generator 계약을 수용하기 전에는
CLN01이 중복 파일을 삭제하지 않습니다. 과거 CLN01 초안의 target 변경이나 SMTP
verdict 고정은 자동 적용하지 않고 이 계약과 실제 native 결과에 맞춰 검토합니다.

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
