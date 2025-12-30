# Airflow Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 Apache Airflow를 Docker 환경에서 실행하기 위한 설정을 담고 있습니다. CeleryExecutor를 사용하여 분산 처리 환경을 구성하며, PostgreSQL(메타데이터 DB)과 Redis(Celery Broker)를 외부 서비스로 연동합니다. 또한 Traefik을 통해 외부 접근을 관리합니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **airflow-apiserver** | Webserver & API | Airflow UI 및 REST API를 제공합니다. Traefik을 통해 `airflow.${DEFAULT_URL}`로 접근 가능합니다. |
| **airflow-scheduler** | Scheduler | DAG 스케줄링 및 태스크 실행을 담당합니다. |
| **airflow-dag-processor** | DAG Processor | DAG 파일을 파싱하여 메타데이터 DB에 업데이트합니다. |
| **airflow-worker** | Worker | 실제 태스크를 실행하는 작업자입니다. CeleryExecutor를 사용합니다. |
| **airflow-triggerer** | Triggerer | 비동기 태스크(Deferrable Operators)를 관리합니다. |
| **flower** | Celery Monitor | Celery 워커 및 태스크 상태를 모니터링하는 웹 UI입니다. `flower.${DEFAULT_URL}`로 접근 가능합니다. |
| **airflow-statsd-exporter**| Metrics Exporter | Airflow 메트릭을 수집하여 Prometheus가 긁어갈 수 있는 형식으로 변환합니다. |
| **airflow-init** | Initialization | Airflow 실행 전 필요한 디렉토리 생성 및 DB 마이그레이션 등을 수행하는 초기화 컨테이너입니다. |

## 3. 구성 및 설정 (Configuration)

### 네트워크 및 의존성
- **Network**: `infra_net` (PostgreSQL, Redis 등 다른 인프라 서비스와 통신)
- **Database**: 외부 PostgreSQL 사용 (`POSTGRES_HOSTNAME`, `AIRFLOW_DB_USER` 등 환경변수 참조)
- **Broker**: 외부 Redis 사용 (`REDIS_NODE_NAME`, `REDIS_PASSWORD` 등 환경변수 참조)

### 환경 변수 (주요 설정)
`docker-compose.yml` 내 `x-airflow-common` 및 각 서비스에 정의되어 있습니다.
- `AIRFLOW__CORE__EXECUTOR`: CeleryExecutor
- `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN`: DB 연결 문자열
- `AIRFLOW__CELERY__BROKER_URL`: Celery Broker 연결 문자열
- `AIRFLOW_UID`: 호스트 사용자와의 권한 매핑을 위한 UID

### 볼륨 (Volumes)
- `airflow-dags`: DAG 파일 저장소 (`/opt/airflow/dags`)
- `airflow-plugins`: 플러그인 저장소 (`/opt/airflow/plugins`)
- `./config/statsd_mapping.yml`: StatsD 매핑 설정 파일

### 로드밸런싱 (Traefik)
- **Airflow UI**: `https://airflow.${DEFAULT_URL}`
- **Flower UI**: `https://flower.${DEFAULT_URL}`
- 선택적으로 Keycloak SSO 미들웨어 적용 가능 (`traefik.http.routers.airflow.middlewares=sso-auth@file` 주석 해제 시)
