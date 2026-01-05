# Apache Airflow

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 워크플로우를 프로그래밍 방식으로 작성, 예약 및 모니터링하는 플랫폼입니다 (Workflow as Code).

**주요 기능 (Key Features)**:
- **Celery Executor**: 분산 작업 처리를 위해 Redis와 Worker 노드 사용.
- **DAG Processor**: DAG 파일 파싱 및 스케줄링 최적화.
- **Flower UI**: Celery 워커 상태 모니터링.

**기술 스택 (Tech Stack)**:
- **Image**: `apache/airflow:3.1.3`
- **Executor**: CeleryExecutor
- **Backend**: PostgreSQL (`airflow` DB) + Redis (`celery` Broker)

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
**컴포넌트**:
- **Scheduler**: 작업 예약 및 트리거.
- **Webserver (API Server)**: UI 및 API 제공.
- **Worker**: 실제 Task 실행.
- **Triggerer**: Async 작업(Deferred Operator) 처리.
- **StatsD Exporter**: 메트릭 변환 (StatsD -> Prometheus).

## 3. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
(`airflow-init` 서비스가 DB 마이그레이션과 초기 계정 생성을 수행합니다.)

## 4. 환경 설정 명세 (Configuration Reference)
**볼륨 마운트**:
- `airflow-dags`: DAG 파일 저장소.
- `airflow-plugins`: 커스텀 플러그인.

**네트워크 포트**:
- **UI**: 8080 (`https://airflow.${DEFAULT_URL}`)
- **Flower**: 5555 (`https://flower.${DEFAULT_URL}`)

## 5. 통합 및 API 가이드 (Integration Guide)
**API 명세**:
- Base URL: `/api/v1`
- 인증: Basic Auth (초기 계정: `airflow` / `airflow`)

## 6. 가용성 및 관측성 (Availability & Observability)
**상태 확인**:
- 각 컴포넌트(`scheduler`, `webserver` 등)별 전용 Health Check 명령 수행.

**모니터링**:
- StatsD 메트릭이 활성화되어 `airflow-statsd-exporter`로 전송됩니다.

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- PostgreSQL의 `airflow` 데이터베이스 백업 필수.
- DAG 파일과 플러그인 소스 코드(Git 관리) 백업.

## 8. 보안 및 강화 (Security Hardening)
- **Webserver Proxy Fix**: `AIRFLOW__WEBSERVER__ENABLE_PROXY_FIX=true`를 통해 역방향 프록시 환경의 IP/Scheme 인식.

## 9. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Task Stuck**: Celery Worker 리소스 부족 확인 또는 Flower에서 상태 확인.
- **DAG Not Found**: `airflow-dags` 볼륨 마운트 경로 및 권한 확인.

**진단 명령어**:
```bash
docker exec -it airflow-scheduler airflow dags list
```
