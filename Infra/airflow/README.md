# Apache Airflow

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 워크플로우를 프로그래밍 방식으로 작성, 예약 및 모니터링하는 플랫폼입니다 (Workflow as Code).  
복잡한 데이터 파이프라인을 Python 코드로 정의하여 관리, 예약, 실행할 수 있습니다.

## 2. 주요 기능 (Key Features)
- **Workflow as Code**: Python을 사용하여 파이프라인(DAG)을 동적으로 생성.
- **Scalable**: Celery Executor와 Worker를 통한 분산 처리 지원.
- **Extensible**: 다양한 외부 시스템(DB, Cloud Service 등)과 연동 가능한 방대한 Provider 생태계.
- **Monitoring**: 직관적인 Web UI를 통한 파이프라인 상태 모니터링 및 관리.

## 3. 기술 스택 (Tech Stack)
- **Image**: `apache/airflow:3.1.3`
- **Executor**: `CeleryExecutor` (분산 처리를 위한 실행기)
- **Metadata DB**: PostgreSQL
- **Broker**: Redis (Celery 작업 큐 관리)

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 주요 컴포넌트 및 역할
1.  **Scheduler**: 모든 DAG와 Task를 모니터링하고, 종속성이 충족되면 실행을 예약합니다.
2.  **Webserver (API Server)**: 사용자가 DAG 상태를 확인하고 관리할 수 있는 UI 및 REST API를 제공합니다.
3.  **Worker**: 실제 예약된 Task를 실행하는 노드입니다. Celery Executor를 통해 분산 처리가 가능합니다.
4.  **Triggerer**: 비동기 작업(Deferred Operator)을 효율적으로 처리하여 Worker 슬롯 낭비를 줄입니다.
5.  **Dag Processor**: DAG 파일을 지속적으로 파싱하여 메타데이터 DB를 업데이트합니다.
6.  **StatsD Exporter**: Airflow 메트릭을 수집하여 Prometheus 포맷으로 변환합니다.

### 워크플로우
1.  사용자가 `dags/` 폴더에 Python 파일로 DAG 작성.
2.  **Dag Processor**가 파일을 파싱하여 DB에 메타데이터 저장.
3.  **Scheduler**가 실행 조건(시간, 의존성)을 확인하고 태스크를 **Redis**(Broker)에 큐잉.
4.  **Worker**가 Redis에서 태스크를 가져와 실행.
5.  실행 상태 및 로그는 **PostgreSQL**(DB)에 저장되고 **Webserver**를 통해 시각화.

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **참고**: 최초 실행 시 `airflow-init` 서비스가 데이터베이스 마이그레이션과 초기 사용자 생성을 수행합니다.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 CLI 사용법
컨테이너 내부에서 Airflow CLI를 통해 다양한 관리 작업을 수행할 수 있습니다.

```bash
# Scheduler 컨테이너 접속 및 DAG 목록 확인
docker exec -it airflow-scheduler airflow dags list

# 특정 DAG의 태스크 테스트 (실제 실행 없이 드라이 런)
# usage: airflow tasks test <dag_id> <task_id> <execution_date>
docker exec -it airflow-worker airflow tasks test example_bash_operator runme_0 2024-01-01
```

### 6.2 API 사용법
Airflow 2.0+ 버전은 강력한 REST API를 제공합니다.

**DAG 목록 조회**:
```bash
curl -X GET "http://localhost:8080/api/v1/dags" \
  --user "airflow:airflow"
```

**DAG 실행 트리거 (Trigger DAG)**:
```bash
curl -X POST "http://localhost:8080/api/v1/dags/example_bash_operator/dagRuns" \
  --user "airflow:airflow" \
  -H "Content-Type: application/json" \
  -d '{"conf": {"custom_param": "value"}}'
```

### 6.3 Web UI 사용법
1.  **접속**: 브라우저에서 `https://airflow.${DEFAULT_URL}` (또는 `http://localhost:8080`) 접속.
2.  **로그인**: 기본 계정 `airflow` / `airflow` 사용.
3.  **DAG 활성화**: 메인 화면에서 DAG 이름 왼쪽의 **Toggle 스위치**를 `On`으로 변경.
4.  **수동 실행**: `Actions` 열의 **Play 버튼**(`▶`) -> `Trigger DAG` 클릭.

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `AIRFLOW__CORE__EXECUTOR`: `CeleryExecutor` (실행 모드 설정)
- `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN`: 메타데이터 DB 연결 정보.
- `AIRFLOW__CELERY__BROKER_URL`: Redis Broker 연결 정보.
- `AIRFLOW__WEBSERVER__BASE_URL`: 외부 접속 도메인 설정 (`https://airflow.${DEFAULT_URL}`).

### 볼륨 마운트 (Volumes)
- `airflow-dags`: `/opt/airflow/dags` (DAG 파일 저장 경로)
- `airflow-plugins`: `/opt/airflow/plugins` (커스텀 플러그인 저장 경로)

### 네트워크 포트 (Ports)
- **Airflow Web UI**: 8080 (`https://airflow.${DEFAULT_URL}`)
- **Flower UI**: 5555 (`https://flower.${DEFAULT_URL}`) - Celery 모니터링

## 8. 통합 및 API 가이드 (Integration Guide)
**API 명세**:
- **Base URL**: `/api/v1`
- **Authentication**: Basic Auth (ID/PW). `airflow-init`에서 생성된 계정 사용.
- **Documentation**: UI 접속 후 하단 `API Documentation` 링크 참조.

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- 각 서비스(`scheduler`, `webserver` 등)는 `curl` 기반의 Docker Health Check가 구성되어 있습니다.

**Monitoring**:
- `AIRFLOW__METRICS__STATSD_ON=true` 설정으로 메트릭 수집이 활성화되어 있습니다.
- `airflow-statsd-exporter` 컨테이너가 StatsD 메트릭을 받아 Prometheus가 수집 가능한 형태로 변환합니다.

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**필수 백업 대상**:
1.  **Metadata DB**: PostgreSQL의 `airflow` 데이터베이스 (모든 실행 이력, 연결 정보 등).
2.  **DAG Files**: `airflow-dags` 볼륨의 소스 코드.
3.  **Plugins**: `airflow-plugins` 볼륨의 소스 코드.
4.  **Variables/Connections**: 코드 외에 UI로 설정한 값들은 DB 백업에 포함되지만, JSON으로 별도 에크스포트 권장.

## 11. 보안 및 강화 (Security Hardening)
- **Proxy Support**: `AIRFLOW__WEBSERVER__ENABLE_PROXY_FIX=true` 설정을 통해 프록시 뒤에서도 올바른 IP와 Scheme을 인식합니다.
- **Authentication**: 기본적으로 활성화되어 있으며, Keycloak과 같은 SSO 연동도 가능합니다 (주석 처리된 설정 참조).

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제 및 해결**:
- **Task Stuck(작업 멈춤)**: Celery Worker의 리소스 부족이나 Redis 연결 문제를 확인하세요. Flower UI(`localhost:5555`)에서 Worker 상태를 점검할 수 있습니다.
- **DAG Not Found**: `airflow-dags` 볼륨이 호스트의 올바른 경로와 마운트되었는지 확인하세요.
- **Permission Denied**: `AIRFLOW_UID` 환경 변수가 호스트 사용자와 일치하는지 확인하세요.

---
**공식 문서**: [https://airflow.apache.org/docs/](https://airflow.apache.org/docs/)
