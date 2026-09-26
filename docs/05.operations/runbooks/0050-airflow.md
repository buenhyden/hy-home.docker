---
title: "Airflow Runbook"
version: "1.1.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-26"
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

## Procedure

### Checklist

- [ ] `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`가 통과하는가?
- [ ] 현재 실행 환경이 `dedicated-valkey` profile을 선택했는지 식별했는가?
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
2. Broker 상태 확인:
   - `dedicated-valkey` 미선택(공유 broker): `docker compose exec mng-valkey sh -lc 'valkey-cli -a "$(cat /run/secrets/mng_valkey_password)" ping'`
   - `dedicated-valkey` 선택(전용 broker): `docker compose exec airflow-valkey sh -lc 'valkey-cli -a "$(cat /run/secrets/airflow_valkey_password)" ping'`
3. Celery worker 응답 확인: `docker compose exec airflow-apiserver airflow celery inspect ping`
4. 워커만 재시작: `docker compose restart airflow-worker`
5. Flower(`flower.${DEFAULT_URL}`) 또는 worker 로그에서 heartbeat 회복 여부를 확인한다.

##### 시나리오 2: 메타데이터 DB 오류

1. DB 연결 정보 확인: `docker compose exec airflow-apiserver airflow db check`
2. 비밀번호/시크릿 로드 여부 확인: `/run/secrets/airflow_db_password` 파일 존재 여부 확인.
3. 서비스 재시작: `docker compose restart airflow-apiserver airflow-scheduler`

##### 시나리오 3: 관리자 패스워드 분실

1. 사용자 재생성/업데이트:

   ```bash
   read -rsp "New Airflow admin password: " AIRFLOW_NEW_PASSWORD; echo
   docker compose exec airflow-apiserver airflow users reset-password \
     --username admin \
     --password "$AIRFLOW_NEW_PASSWORD"
   unset AIRFLOW_NEW_PASSWORD
   ```

### Verification Steps

- [ ] `docker compose exec airflow-apiserver airflow dags list` 명령어로 정상 로드 여부 확인.
- [ ] Airflow Web UI 로그인 및 `Admin > Health` 페이지 확인.

### Observability and Evidence Sources

- **Signals**: Grafana Alert (Worker Down), Flower (Queue Length).
- **Evidence to Capture**: `docker compose logs --tail=100 airflow-scheduler airflow-worker airflow-apiserver`, broker ping, `airflow celery inspect ping`, DAG list 결과.

### Safe Rollback or Recovery Procedure

- [ ] 비정상 상태의 컨테이너를 강제 종료(`kill`)하기 전, 반드시 현재 실행 중인 태스크를 `Task Instance > Clear` 하여 재실행 가능하도록 조치하십시오.
- [ ] DB 마이그레이션 실패 시, `_AIRFLOW_DB_MIGRATE: 'false'`로 일시 전환 후 롤백을 고려하십시오.

---

### Planned isolated restore rehearsal

Status: **planned and not executed**. No successful Airflow restore evidence is claimed by this document.

1. Record image digests, profile/env names (not values), Airflow version, migration level, DAG inventory, running/queued task inventory, and checksums of the backup artifacts. Pause schedules and inbound producers, then wait for or explicitly reconcile tasks.
2. Ask the PostgreSQL owner to create a consistent logical backup of database `airflow`. Preserve `airflow-dags`, `airflow-plugins`, `airflow-config`, required `airflow-logs`, and the exact `airflow_fernet_key`, JWT secret, Keycloak client secret, DB secret, and selected broker secret references under the approved secret process. Do not depend on a live Valkey copy for exact recovery.
3. Create a separate Compose project and isolated network with restored copies and no production routes, schedules, webhooks, or external executors. Restore PostgreSQL first, then the same Fernet key and mounted artifacts; configure the broker host/secret pair consistently.
4. Start dependencies, run the supported Airflow DB check/migration, then start processor/scheduler/API/worker. Verify DAG parsing, DB health, Connections decryption without printing values, worker ping, native Keycloak login, task-log access, and a side-effect-free canary DAG.
5. On any mismatch, stop the isolated project, retain logs/checksums, and return to the untouched source backup. Production replacement or DNS/route changes require a separate approved change.

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- The isolated restore above remains unexecuted; capture dated outputs and artifact checksums before changing that status.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Traceability

- Declared parent: [Airflow Usage Guide](../guides/0050-airflow.md) (`GDE-0050`)
- Governing authority: [Workflow Tier (07-workflow) Architecture Description](../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)
- Subject peers: [Guide](../guides/0050-airflow.md) (`GDE-0050`), [Policy](../policies/0050-airflow.md) (`POL-0050`)

## Related Documents

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../README.md)
- [Usage guide](../guides/0050-airflow.md)
- [Operations policy](../policies/0050-airflow.md)
