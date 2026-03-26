# Airflow Recovery Runbook

: Apache Airflow (07-workflow)

---

## Overview (KR)

이 런북은 Apache Airflow 서비스 장애 발생 시 운영자가 즉시 수행할 수 있는 복구 절차를 정의한다. 데이터베이스 연결 오류, 워커 중단, DAG 파싱 지연 등 주요 장애 시나리오별 대응 단계를 제공한다.

## Purpose

- Airflow 서비스 가용성 즉각 복구
- 파이프라인 중단 시간 최소화
- 시스템 상태 검증 및 정상화 확인

## Canonical References

- ARD: [07-workflow Architecture](../../02.ard/07-workflow.md)
- Guide: [Airflow System Guide](../../07.guides/07-workflow/airflow.md)
- Policy: [Airflow Operations Policy](../../08.operations/07-workflow/airflow.md)

## When to Use

- 태스크가 `Queued` 상태에서 장시간 머물러 있을 때.
- Web UI 접근 시 DB 연결 에러 또는 50x 에러가 발생할 때.
- 워커(Worker) 프로세스가 비정상 종료되거나 리소스 부족으로 경고가 발생할 때.

## Procedure or Checklist

### Checklist

- [ ] [ ] `docker compose ps workflow` 결과가 모두 `Up` 인가?
- [ ] [ ] `airflow-valkey` 브로커와 통신이 가능한가?
- [ ] [ ] 메타데이터 DB(PostgreSQL)가 정상 동작 중인가?

### Procedure

#### 시나리오 1: 태스크 지연 (Task stuck in Queued)
1. Valkey 브로커 상태 확인: `docker compose exec airflow-valkey valkey-cli ping`
2. 워커 재배포: `docker compose restart airflow-worker`
3. Flower(`flower.${DEFAULT_URL}`)를 통해 큐에 쌓인 작업량 확인.

#### 시나리오 2: 메타데이터 DB 오류
1. DB 연결 정보 확인: `docker compose exec airflow-webserver airflow db check`
2. 비밀번호/시크릿 로드 여부 확인: `/run/secrets/airflow_db_password` 파일 존재 여부 확인.
3. 서비스 재시작: `docker compose restart airflow-apiserver airflow-scheduler`

#### 시나리오 3: 관리자 패스워드 분실
1. 사용자 재생성/업데이트:
   ```bash
   docker compose run --rm airflow-cli users reset-password \
     --username admin \
     --password <new_password>
   ```

## Verification Steps

- [ ] `docker compose exec airflow-webserver airflow dags report` 명령어로 정상 로드 여부 확인.
- [ ] Airflow Web UI 로그인 및 `Admin > Health` 페이지 확인.

## Observability and Evidence Sources

- **Signals**: Grafana Alert (Worker Down), Flower (Queue Length).
- **Evidence to Capture**: `docker compose logs --tail=100 airflow-scheduler`, `airflow-worker` 로그.

## Safe Rollback or Recovery Procedure

- [ ] 비정상 상태의 컨테이너를 강제 종료(`kill`)하기 전, 반드시 현재 실행 중인 태스크를 `Task Instance > Clear` 하여 재실행 가능하도록 조치하십시오.
- [ ] DB 마이그레이션 실패 시, `_AIRFLOW_DB_MIGRATE: 'false'`로 일시 전환 후 롤백을 고려하십시오.
