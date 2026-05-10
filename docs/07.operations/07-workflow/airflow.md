# Airflow Operations Policy

> Airflow 시스템의 안정적 운영을 위한 정책, 통제 기준 및 관리 절차 정의.

---

## Overview (KR)

이 문서는 `hy-home.docker` 플랫폼의 Apache Airflow 운영 정책을 정의한다. 시스템의 가용성, 보안, 리소스 관리 및 변경 제어 절차를 규정하여 안정적인 워크플로 실행 환경을 보장한다.

## Policy Scope

- Airflow 코어 컴포넌트 (`scheduler`, `worker`, `webserver` 등) 관리
- 메타데이터 DB 및 브로커(Valkey) 백업 및 복구 정책
- DAG 배포 및 운영 환경 보안 통제

## Applies To

- **Systems**: Apache Airflow v2.10.x, CeleryExecutor
- **Agents**: CI/CD 배포 에이전트, 모니터링 에이전트
- **Environments**: Production ( workflow 티어)

## Controls

- **Required**:
  - 모든 DAG은 `Idempotent`(멱등성)를 유지해야 함.
  - 민감 정보는 반드시 Secret Backend(Docker Secrets/Vault) 및 Airflow Connections를 통해 관리함.
  - `AIRFLOW__CORE__LOAD_EXAMPLES`는 운영 환경에서 반드시 `false`여야 함.
- **Allowed**:
  - 워커 노드의 동적 확장 (부하에 따른 Replica 조정).
  - 읽기 전용 UI 접근 (GUEST 권한).
- **Disallowed**:
  - Scheduler 노드에서의 직접적인 대용량 외부 API 호출 또는 파일 입출력.
  - 사용자 인증(FAB)이 비활성화된 상태에서의 Web UI 노출.

## Exceptions

- **Emergency Hotfix**: 중대한 파이프라인 중단 시, 사후 보고를 조건으로 수동 DB 수정 또는 워커 강제 재시작 가능 (관리자 승인 필요).

## Verification

- **Compliance Check**: `docker compose run --rm airflow-cli config list` 명령을 통해 설정값 준수 여부 확인.
- **Health Check**: Traefik 및 Docker Healthcheck 로그를 통한 실시간 상태 검증.

## Review Cadence

- **Quarterly**: 매 분기별 리소스 사용량 분석 및 쿼터 조정.
- **Per Release**: 새로운 Airflow 버전 또는 Provider 업데이트 시 정책 재검토.

## Related Documents

- **ARD**: [07-workflow Architecture](../../02.ard/0007-workflow-architecture.md)
- **Procedure**: [Airflow Recovery Procedure](../../07.operations/07-workflow/airflow.md)

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/07.operations/07-workflow/airflow.md` during the 2026-05-10 operations taxonomy consolidation.

### Airflow System Usage

> Apache Airflow 워크플로 엔진 시스템 환경 및 운영 전반에 대한 종합 안내서.

---

#### Overview (KR)

이 문서는 `hy-home.docker` 플랫폼의 Apache Airflow 시스템에 대한 가이드다. 개발자와 운영자가 시스템 아키텍처를 이해하고, 서비스 상태를 확인하며, 기본적인 파이프라인 운영을 수행할 수 있도록 돕는다.

#### Usage Type

`system-guide`

#### Target Audience

- **Developers**: DAG 개발 및 시스템 통합
- **Operators**: 서버 상태 모니터링 및 리소스 관리
- **AI Agents**: 자동화된 스케줄링 환경 분석

#### Purpose

- Airflow 분산 아키텍처 (CeleryExecutor) 이해
- 웹 UI 및 모니터링 도구 접근 방법 확인
- 기본 개발 환경 설정 및 검증 절차 습득

#### Prerequisites

- **Docker/Compose**: 로컬 실행 환경
- **Secrets**: `airflow_www_password` 등 서비스 접근 권한
- **Network**: `infra_net` 외부 통신 가능 상태

#### Step-by-step Instructions

##### 1. 시스템 아키텍처 이해

Airflow는 다음과 같은 분산 컴포넌트로 구성됩니다:

- **Scheduler & DAG Processor**: 작업 예약 및 DAG 파일 해석 (독립 실행으로 안정성 확보)
- **Celery Workers**: 실제 태스크가 실행되는 동적 확장 노드
- **Valkey Broker**: 스케줄러와 워커 간의 메시지 교환 (Redis 호환)
- **API Server**: UI 및 외부 통합을 위한 통합 엔드포인트

##### 2. UI 접근 및 모니터링

- **Main UI**: `https://airflow.${DEFAULT_URL}` (작업 모니터링, 로그 확인)
- **Flower Dashboard**: `https://flower.${DEFAULT_URL}` (Celery 워커 부하 상태 확인)
- **Metrics**: Prometheus/Grafana를 통해 StatsD 지표 확인 가능

##### 3. 개발 환경 검증

새로운 DAG를 추가하기 전에 다음 명령으로 시스템 상태를 확인합니다:

```bash
### 컨테이너 상태 확인
docker compose ps workflow

### DAG 목록 로드 확인
docker compose exec airflow-webserver airflow dags list
```

#### Common Pitfalls

- **Scheduler Heavy Load**: DAG 파일 내에서 DB 쿼리나 파일 시스템 접근을 직접 수행하면 스케줄러 성능이 저하됩니다.
- **Worker Timeout**: 리소스 부족으로 워커가 종료되면 태스크가 `Queued` 상태로 멈출 수 있습니다.
- **XCom Abuse**: XCom은 작은 데이터 교환용입니다. 대용량 데이터는 S3/MinIO 등 외부 저장소를 사용하십시오.

#### Related Documents

- **Spec**: [07-workflow Spec](../../04.specs/07-workflow/spec.md)
- **Operation**: [Airflow Operations Policy](../../07.operations/07-workflow/airflow.md)
- **Procedure**: [Airflow Recovery Procedure](../../07.operations/07-workflow/airflow.md)

## Procedure

> Migrated from `docs/07.operations/07-workflow/airflow.md` during the 2026-05-10 operations taxonomy consolidation.

### Airflow Recovery Procedure

: Apache Airflow (07-workflow)

---

#### Overview (KR)

이 런북은 Apache Airflow 서비스 장애 발생 시 운영자가 즉시 수행할 수 있는 복구 절차를 정의한다. 데이터베이스 연결 오류, 워커 중단, DAG 파싱 지연 등 주요 장애 시나리오별 대응 단계를 제공한다.

#### Purpose

- Airflow 서비스 가용성 즉각 복구
- 파이프라인 중단 시간 최소화
- 시스템 상태 검증 및 정상화 확인

#### Canonical References

- ARD: [07-workflow Architecture](../../02.ard/0007-workflow-architecture.md)
- Usage: [Airflow System Usage](../../07.operations/07-workflow/airflow.md)
- Policy: [Airflow Operations Policy](../../07.operations/07-workflow/airflow.md)

#### When to Use

- 태스크가 `Queued` 상태에서 장시간 머물러 있을 때.
- Web UI 접근 시 DB 연결 에러 또는 50x 에러가 발생할 때.
- 워커(Worker) 프로세스가 비정상 종료되거나 리소스 부족으로 경고가 발생할 때.

#### Procedure or Checklist

##### Checklist

- [ ] [ ] `docker compose ps workflow` 결과가 모두 `Up` 인가?
- [ ] [ ] `airflow-valkey` 브로커와 통신이 가능한가?
- [ ] [ ] 메타데이터 DB(PostgreSQL)가 정상 동작 중인가?

##### Procedure

###### 시나리오 1: 태스크 지연 (Task stuck in Queued)

1. Valkey 브로커 상태 확인: `docker compose exec airflow-valkey valkey-cli ping`
2. 워커 재배포: `docker compose restart airflow-worker`
3. Flower(`flower.${DEFAULT_URL}`)를 통해 큐에 쌓인 작업량 확인.

###### 시나리오 2: 메타데이터 DB 오류

1. DB 연결 정보 확인: `docker compose exec airflow-webserver airflow db check`
2. 비밀번호/시크릿 로드 여부 확인: `/run/secrets/airflow_db_password` 파일 존재 여부 확인.
3. 서비스 재시작: `docker compose restart airflow-apiserver airflow-scheduler`

###### 시나리오 3: 관리자 패스워드 분실

1. 사용자 재생성/업데이트:

   ```bash
   read -rsp "New Airflow admin password: " AIRFLOW_NEW_PASSWORD; echo
   docker compose run --rm airflow-cli users reset-password \
     --username admin \
     --password "$AIRFLOW_NEW_PASSWORD"
   unset AIRFLOW_NEW_PASSWORD
   ```

#### Verification Steps

- [ ] `docker compose exec airflow-webserver airflow dags report` 명령어로 정상 로드 여부 확인.
- [ ] Airflow Web UI 로그인 및 `Admin > Health` 페이지 확인.

#### Observability and Evidence Sources

- **Signals**: Grafana Alert (Worker Down), Flower (Queue Length).
- **Evidence to Capture**: `docker compose logs --tail=100 airflow-scheduler`, `airflow-worker` 로그.

#### Safe Rollback or Recovery Procedure

- [ ] 비정상 상태의 컨테이너를 강제 종료(`kill`)하기 전, 반드시 현재 실행 중인 태스크를 `Task Instance > Clear` 하여 재실행 가능하도록 조치하십시오.
- [ ] DB 마이그레이션 실패 시, `_AIRFLOW_DB_MIGRATE: 'false'`로 일시 전환 후 롤백을 고려하십시오.

---

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../README.md)
- [../../07.operations/README.md](../../07.operations/README.md)
- [../../10.incidents/README.md](../../10.incidents/README.md)
