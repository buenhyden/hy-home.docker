---
status: active
---
<!-- Target: docs/05.operations/runbooks/07-workflow/airflow.md -->

# Airflow Runbook

## Overview

이 런북은 Apache Airflow 서비스 장애 발생 시 운영자가 즉시 수행할 수 있는 복구 절차를 정의한다. 현재 서비스명은 Airflow 3의 `airflow-apiserver`를 기준으로 하며, root-included dev compose는 shared `mng-valkey`, service-local compose는 `airflow-valkey`를 사용한다.

## Airflow Recovery Procedure

> Scope: Apache Airflow (07-workflow)

---

### Purpose

- Airflow 서비스 가용성 즉각 복구
- 파이프라인 중단 시간 최소화
- 시스템 상태 검증 및 정상화 확인

### Canonical References

- ARD: [07-workflow Architecture](../../../02.architecture/requirements/0007-workflow-architecture.md)
- Usage: [Airflow System Usage](../../guides/07-workflow/airflow.md)
- Policy: [Airflow Operations Policy](../../policies/07-workflow/airflow.md)

## When to Use

- 태스크가 `Queued` 상태에서 장시간 머물러 있을 때.
- Web UI 접근 시 DB 연결 에러 또는 50x 에러가 발생할 때.
- 워커(Worker) 프로세스가 비정상 종료되거나 리소스 부족으로 경고가 발생할 때.

## Procedure

### Checklist

- [ ] `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`가 통과하는가?
- [ ] 현재 실행 환경이 root-included dev compose인지 service-local compose인지 식별했는가?
- [ ] 메타데이터 DB(PostgreSQL)가 정상 동작 중인가?

### Steps

#### 시나리오 1: 태스크 지연 (Task stuck in Queued)

1. Broker 상태 확인:
   - root-included dev compose: `docker compose exec mng-valkey sh -lc 'valkey-cli -a "$(cat /run/secrets/mng_valkey_password)" ping'`
   - service-local compose: `docker compose exec airflow-valkey sh -lc 'valkey-cli -a "$(cat /run/secrets/airflow_valkey_password)" ping'`
2. 워커 재배포: `docker compose restart airflow-worker`
3. Flower(`flower.${DEFAULT_URL}`)를 통해 큐에 쌓인 작업량 확인.

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
- **Evidence to Capture**: `docker compose logs --tail=100 airflow-scheduler`, `airflow-worker` 로그.

### Safe Rollback or Recovery Procedure

- [ ] 비정상 상태의 컨테이너를 강제 종료(`kill`)하기 전, 반드시 현재 실행 중인 태스크를 `Task Instance > Clear` 하여 재실행 가능하도록 조치하십시오.
- [ ] DB 마이그레이션 실패 시, `_AIRFLOW_DB_MIGRATE: 'false'`로 일시 전환 후 롤백을 고려하십시오.

---

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/07-workflow/airflow.md)
- [Operations policy](../../policies/07-workflow/airflow.md)
