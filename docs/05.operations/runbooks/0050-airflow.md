---
title: "Airflow Runbook"
version: "1.3.3"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "RUN-0050"
parent_ids:
- "GDE-0050"
created: "2026-05-17"
---

# Airflow Runbook

## Overview

이 런북은 Apache Airflow 서비스 장애 발생 시 운영자가 즉시 수행할 수 있는 복구 절차를 정의한다. 현재 서비스명은 Airflow 3의 `airflow-apiserver`를 기준으로 한다. `dedicated-valkey` profile은 전용 broker를 기동할 뿐이며, `AIRFLOW_VALKEY_HOST`와 `AIRFLOW_VALKEY_SECRET`을 전용 pair로 바꾼 환경만 `airflow-valkey`를 사용한다.

> Scope: Apache Airflow (07-workflow)

---

### Purpose

- Airflow 서비스 가용성 즉각 복구
- 파이프라인 중단 시간 최소화
- 시스템 상태 검증 및 정상화 확인

## When to Use

- 태스크가 `Queued` 상태에서 장시간 머물러 있을 때.
- Web UI 접근 시 DB 연결 에러 또는 50x 에러가 발생할 때.
- 워커(Worker) 프로세스가 비정상 종료되거나 리소스 부족으로 경고가 발생할 때.
- Airflow UI 로그인, Keycloak token exchange, 또는 TLS verification이 실패할 때.
- Airflow token 또는 session이 노출되어 폐기해야 할 때.

## Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### Service lifecycle prerequisites

처음 기동하거나 이미지를 바꾸기 전에 DB·실제 선택 broker, CA, DAG/plugin/config/log host 경로와 비root 쓰기 권한을 확인한다. `airflow-init`은 migration 가능한 root 일회성 작업이므로 DB backup·schema 계획 승인 뒤에만 실행한다. init은 chown이나 사용자 역할 배정을 하지 않는다. init 완료 뒤 API·scheduler·processor·triggerer, API 준비 뒤 worker·Flower가 요구하는 조건을 각각 검증한다. StatsD exporter도 init 완료에 의존하지만 HTTP healthcheck는 없고 이벤트가 생긴 뒤 metric을 확인한다. 전용 Valkey·exporter를 선택하면 RUN-0028의 broker backup·인증 절차를 적용하되 workflow 이력 복원으로 간주하지 않는다. 중지는 예약·입력을 먼저 차단하고 실행 작업의 외부 효과를 대조한 뒤 한다.

### Checklist

- [ ] `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`가 통과하는가?
- [ ] `AIRFLOW_VALKEY_HOST`/`AIRFLOW_VALKEY_SECRET`의 선택 이름과 일치 여부를 확인했는가? Profile만으로 broker를 추정하지 않는다.
- [ ] 메타데이터 DB(PostgreSQL)가 정상 동작 중인가?
- [ ] `apache-airflow-providers-keycloak` 버전이 바뀌었다면
  [Authorization bootstrap](../guides/0079-application-auth-integration.md#authorization-bootstrap)의
  `create-permissions`를 다시 실행하고, 로그인한 사용자로 Pools, DAGs, Assets,
  HITL 화면이 `403` 없이 열리는지 확인했는가? (inc-2026-0002)

### Steps

#### 시나리오 0: Keycloak 인증 또는 TLS 실패

1. `airflow-apiserver` 로그에서 auth manager, `401`, `403`, certificate 오류를
   확인한다. Secret 값 자체는 출력하지 않는다.
2. `KEYCLOAK_URL`, `KEYCLOAK_REALM`, `AIRFLOW_KEYCLOAK_CLIENT_ID`가 현재
   환경의 Keycloak client 설정과 일치하는지 값 노출 없이 확인한다.
3. `/run/secrets/airflow_keycloak_client_secret`와
   `/run/secrets/airflow_api_jwt_secret`가 컨테이너에 연결되어 있는지 경로만
   확인한다.
4. `${DEFAULT_CERT_DIR}/rootCA.pem` bind mount가 존재하고 API server가 임시
   CA bundle을 생성했는지 로그와 파일 존재 여부로 확인한다.
5. 이미지가 최신 Dockerfile 변경을 포함해야 하면 승인된 Compose build를
   수행하고, 이후 `airflow db check`와 UI 로그인 검증을 다시 실행한다.

#### 시나리오 1: 태스크 지연 (Task stuck in Queued)

1. 증거 캡처:
   - `docker compose logs --tail=100 airflow-worker airflow-scheduler airflow-apiserver`
   - `docker compose exec airflow-worker df -h /opt/airflow/logs`
2. 선택된 host/secret pair가 shared인지 dedicated인지 확인하고 [Valkey Runbook](0028-management-database.md)의 값 비노출 인증 점검을 따른다. DB/broker가 준비되지 않으면 중단한다. Profile은 선택 증거가 아니다.
3. Celery worker 응답 확인: `docker compose exec airflow-apiserver celery --app airflow.providers.celery.executors.celery_executor.app inspect ping`. Remote control이 허용된 worker의 응답이 없으면 실패로 기록하고 원인을 먼저 진단한다.
4. 스케줄을 pause하고 실행/예약 태스크와 외부 부작용을 조정한 뒤 승인된 worker 재시작만 수행한다: `docker compose restart airflow-worker`. 자동 재실행이나 task clear를 복구 전제로 삼지 않는다.

5. Flower(`flower.${DEFAULT_URL}`) 또는 worker 로그에서 heartbeat 회복 여부를 확인한다.

##### 시나리오 2: 메타데이터 DB 오류

1. DB 연결 정보 확인: `docker compose exec airflow-apiserver airflow db check`
2. 비밀번호/시크릿 로드 여부 확인: `/run/secrets/airflow_db_password` 파일 존재 여부 확인.
3. DB/secret 준비 문제가 남아 있으면 중단하고 소유자에게 넘긴다. 해당 준비가 회복되고 실행 작업의 외부 효과와 중단 영향이 승인된 경우에만 기존 설정의 서비스를 재시작한다: `docker compose restart airflow-apiserver airflow-scheduler`. Secret bind·환경변수·image 변경은 restart 대상이 아니며 R0085/R0086의 승인된 재생성 절차로 넘긴다.

##### 시나리오 3: 관리자 계정 접근 복구

Native Keycloak Auth Manager의 계정과 역할 소유자는 Keycloak이다.
[RUN-0014](0014-keycloak.md)의 승인된 계정 복구 절차로 넘긴다.
FAB `airflow users reset-password`나 CLI 인자에 password를 넣는 방식은
이 구현에 적용하지 않는다. 복구 뒤 native login과 필요한 권한을 확인한다.
Permission bootstrap 완료만으로 사용자 역할이 부여되지는 않는다.

##### 시나리오 4: 노출된 Airflow token/session 폐기

Keycloak으로 로그인한 UI는 Airflow 자체 JWT(`_token` cookie,
`airflow_api_jwt_secret`으로 서명)와 Keycloak access/refresh/id token cookie를
함께 쓴다. 아래 동작은 설치된 Airflow 3.3.1과 keycloak provider 0.9.0의 <!-- runtime-version-exception: history — SPEC-0193의 2026-09-30 장애·인증 검증에 적용된 버전 근거를 보존한다. -->
코드에서 확인했다. Keycloak session과 client secret은
[RUN-0014](0014-keycloak.md)의 "노출된 token/session 폐기" 단계가 다룬다.

1. 노출된 브라우저 session에 접근할 수 있으면 UI에서 Logout한다.
   `/api/v2/auth/logout`이 현재 Airflow JWT의 `jti`를 `revoked_token` table에
   기록한 뒤 Keycloak end-session으로 보내고, callback이 token cookie를 지운다.
   이 JWT는 만료 전이라도 거부된다.
2. token 사본이 따로 노출됐으면 로그아웃만으로는 부족하다. Airflow JWT는
   `[api_auth] jwt_expiration_time`(기본 86400초, 이 저장소는 값을 바꾸지
   않음)까지 유효하다. 모두 끊으려면 `airflow_api_jwt_secret`을 교체한다.
   - 실행 중인 task를 먼저 멈추거나 끝낸다. task execution token도 같은
     key로 서명되므로, 교체하면 실행 중인 task의 API 호출이 실패한다.
   - `secrets/automation/airflow/airflow_api_jwt_secret.txt`를 값 출력 없이 새 난수로
     교체하고 기존 소유자와 mode(`0640`)를 유지한다.
   - 이 secret을 읽는 `airflow-apiserver`, `airflow-scheduler`,
     `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`를 함께
     재생성한다. 파일을 바꾸기만 해서는 실행 중인 컨테이너에 반영되지 않는다.
   - 모든 사용자와 API client가 다시 로그인해야 한다.
3. 확인: 기존 cookie의 요청이 `401`을 받고, 새로 로그인하면 DAGs, Pools,
   Assets, HITL이 `403` 없이 열린다. 증거는 경로와 상태 코드만 남긴다.

### Verification Steps

- [ ] `docker compose exec airflow-apiserver airflow dags list` 명령어로 정상 로드 여부 확인.
- [ ] native Keycloak 로그인과 `/api/v2/monitor/health` JSON의 component status를 확인한다. HTTP 200만으로 정상 판정하지 않는다. Scheduler health, processor/triggerer job check, worker ping과 승인된 canary 결과도 확인한다.

### Observability and Evidence Sources

- **Signals**: Grafana의 worker 중단 alert와 Flower 큐 길이
- **Evidence to Capture**: `docker compose logs --tail=100 airflow-scheduler airflow-worker airflow-apiserver`, broker ping, `celery --app airflow.providers.celery.executors.celery_executor.app inspect ping`, DAG list 결과.
- **Metrics**: statsd exporter mapping은 DAG, task, pool, DAG 파일 이름을 `dag_id`, `task_id`, `pool_name`, `dag_file` label로 옮기고, 규칙에 없는 네 단계 이상 이름은 버린다(SPEC-0193). 이름 템플릿은 `${1}_${2}`로 쓴다. `$1_$2`로 쓰면 exporter가 `1_`이라는 변수로 읽어 이름이 `airflow_` 하나로 뭉개진다(2026-09-30 확인). DAG run·task 메트릭(`airflow_dagrun_*`, `airflow_task_finish_total`)은 DAG가 실행된 뒤에야 생긴다. Grafana `Applications/airflow`(mixin)와 `Applications/airflow-db`(`airflow-db` SQL datasource)가 이를 본다.
- **Traces**: Airflow는 trace를 보내지 않는다. SPEC-0193에서 OTLP tracing을 켰다가 모두 껐다(2026-09-30, owner 결정). Airflow 3.3.1에서 tracing을 켜면 fork하는 프로세스가 멈춘다. Airflow 쪽 신호는 statsd metric, `airflow-db` SQL datasource, 로그로 본다. 업그레이드 뒤 다시 켜려면 scheduler 하나에서 먼저 health와 DAG run을 확인한다. <!-- runtime-version-exception: history — SPEC-0193의 2026-09-30 장애·인증 검증에 적용된 버전 근거를 보존한다. -->
  - scheduler: 8974 health server가 뜨지 않아 unhealthy로 남는다. SIGUSR2 stack dump에 health thread가 없었다.
  - DAG processor: 파일마다 50 s parse timeout을 넘겨 kill되고, 모든 DAG가 `is_stale`이 되어 run이 `queued`에 머문다. 같은 파일을 프로세스 안에서 parse하면 4 s가 걸린다.
  - worker: prefork pool이 task를 reserve만 하고 실행하지 않는다.
  - 증상이 보이면 `airflow dags details <dag_id>`의 `is_stale`과 `celery inspect reserved`를 먼저 본다.

### Safe Rollback or Recovery Procedure

- [ ] 강제 종료 전 schedule을 pause하고 실행/예약 태스크와 외부 부작용을 조정한다. `Clear`는 재실행을 허가하므로 idempotency와 중복 출력 처리의 별도 승인 없이 실행하지 않는다.
- [ ] DB migration 실패 시 중단하고 DB 소유자와 일치하는 schema/image/artifact 복구 계획을 승인받는다. `_AIRFLOW_DB_MIGRATE: 'false'`는 후속 migration만 막으며 이미 바뀐 schema를 되돌리지 않는다.

---

### Planned isolated restore rehearsal

**Project 이름만 바꿔서는 실행할 수 없다.** Rehearsal 전에 고정 container name, host port, bind path, external network와 route 충돌을 제거하고 production 통지·workflow egress를 차단한 별도 Compose/storage 정의를 승인한다. 격리와 대상 backup 계약을 검토하기 전에는 NOT_RUN으로 유지한다. 임의 project에 production volume이나 credential을 연결하지 않는다.

상태: **계획됨·미실행**. 이 문서는 Airflow 복원 성공 증거를 주장하지 않는다.

1. 이미지 digest, profile·환경변수 이름(값 제외), Airflow 버전, 마이그레이션 수준, DAG 목록, 실행·대기 작업 목록, 백업 산출물 checksum을 기록한다. 예약과 입력 생산자를 일시 중지한 뒤 작업 완료를 기다리거나 상태를 명시적으로 대조한다.
2. PostgreSQL 소유자에게 `airflow` DB의 일관된 논리 백업을 요청한다. `airflow-dags`, `airflow-plugins`, `airflow-config`, 필요한 `airflow-logs`와 정확히 일치하는 `airflow_fernet_key`, JWT secret, Keycloak client secret, DB secret, 선택한 broker secret의 참조를 승인된 secret 절차로 보존한다. 실행 중인 Valkey 복사본에 정확한 복구를 의존하지 않는다.
3. 운영 경로·예약·webhook·외부 실행기가 없는 별도 Compose 프로젝트와 격리 네트워크에 복원 복사본을 준비한다. PostgreSQL을 먼저 복원하고 같은 Fernet 키와 마운트 산출물을 복원한 뒤 broker 호스트·secret 쌍을 일치시킨다.
4. 의존 서비스를 기동하고 지원되는 Airflow DB 점검·마이그레이션을 수행한 뒤 processor·scheduler·API·worker를 기동한다. DAG 파싱, DB 상태, 값을 출력하지 않는 Connections 복호화, worker ping, Keycloak 네이티브 로그인, 작업 로그 접근, 외부 효과가 없는 canary DAG를 확인한다.
5. 불일치하면 격리 프로젝트를 중지하고 로그·checksum을 보존한 뒤 변경하지 않은 원본 백업으로 돌아간다. 운영 교체나 DNS·경로 변경에는 별도 변경 승인이 필요하다.

## Evidence

- 실행 명령·결과·시각과 운영자 또는 agent 조치를 기록한다.
- 실패 검사, 관찰 증상과 최종 복구·에스컬레이션 상태를 관련 Task/Incident에 남긴다.

## Rollback or Recovery

- 이 Runbook에 기록된 복구·rollback 절차와 위의 `Safe Rollback or Recovery Procedure` 하위 절차만 사용한다.
- 위 격리 복원은 미실행 상태다. 상태를 변경하기 전에 날짜가 있는 출력과 산출물 checksum을 기록한다.
- 관찰한 장애가 문서화된 절차와 다르면 변경을 중지하고 증거를 보존한 뒤 `## Escalation`에 따라 보고한다.

## Escalation

검증 실패, secret 노출 위험, 파괴적 변경 필요 또는 예상 절차와 다른 상태이면 중단하고 @buenhyden에게 넘긴다. 정제된 증거, 시도한 단계와 현재 rollback/recovery 상태를 함께 전달한다.

## Traceability

- Declared parent: [Airflow Usage Guide](../guides/0050-airflow.md) (`GDE-0050`)
- Governing authority: [Workflow Tier (07-workflow) Architecture Description](../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)
- Subject peers: [Guide](../guides/0050-airflow.md) (`GDE-0050`), [Policy](../policies/0050-airflow.md) (`POL-0050`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0050-airflow.md)
- [Operations policy](../policies/0050-airflow.md)
