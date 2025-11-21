# Apache Airflow

**Apache Airflow**는 복잡한 데이터 파이프라인을 프로그래밍 방식으로 작성, 예약 및 모니터링하기 위한 오픈 소스 플랫폼입니다.
이 구성은 **CeleryExecutor**를 사용하여 분산 처리가 가능한 구조로 설정되어 있습니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **airflow-apiserver** | 웹 UI 및 API 서버 | `8080` |
| **airflow-scheduler** | 작업 예약 및 실행 관리 | - |
| **airflow-worker** | 실제 작업(Task)을 실행 (Celery) | - |
| **airflow-triggerer** | 비동기 작업(Deferrable Operators) 관리 | - |
| **flower** | Celery 워커 모니터링 대시보드 | `5555` |

## 🛠 설정 및 환경 변수

- **Executor**: `CeleryExecutor` (Redis를 브로커로, PostgreSQL을 백엔드로 사용)
- **DB 연결**: `postgresql+psycopg2://...` (PostgreSQL 서비스 의존)
- **Broker 연결**: `redis://...` (Redis 서비스 의존)
- **DAGs 폴더**: `./dags` (호스트 볼륨 마운트)

## 📦 볼륨 마운트

- `airflow-dags`: DAG 파일 저장소 (`/opt/airflow/dags`)
- `airflow-logs`: 실행 로그 (`/opt/airflow/logs`)
- `airflow-config`: 설정 파일 (`/opt/airflow/config`)
- `airflow-plugins`: 커스텀 플러그인 (`/opt/airflow/plugins`)

## 🏃‍♂️ 실행 방법

```bash
# 실행
docker compose up -d

# 초기화 (최초 1회 필요 시)
docker compose up airflow-init
```

## ⚠️ 주의사항
- **리소스**: Airflow는 메모리를 많이 소모할 수 있습니다. `airflow-init` 컨테이너가 리소스를 체크하여 경고를 줄 수 있습니다.
- **사용자 ID**: 리눅스 환경에서는 `AIRFLOW_UID` 설정이 필요할 수 있습니다.
