# Apache Airflow

## 개요

이 디렉토리는 워크플로우 오케스트레이션을 위한 Apache Airflow의 Docker Compose 구성을 포함합니다. CeleryExecutor를 사용하며, Redis(브로커)와 PostgreSQL(메타데이터 DB)을 백엔드로 사용합니다. 또한 StatsD를 통한 메트릭 수집과 Flower를 통한 Celery 모니터링을 포함합니다.

## 서비스

- **airflow-apiserver**: Airflow API 서버 및 웹 인터페이스.
- **airflow-scheduler**: 작업 스케줄러.
- **airflow-dag-processor**: DAG 파일 처리기.
- **airflow-worker**: Celery 워커 (작업 실행).
- **airflow-triggerer**: 지연된 작업(Deferrable Operators) 처리.
- **airflow-init**: 초기화 작업 (DB 마이그레이션, 사용자 생성).
- **airflow-cli**: CLI 명령 실행을 위한 컨테이너.
- **flower**: Celery 워커 모니터링 도구.
- **airflow-statsd-exporter**: StatsD 메트릭을 Prometheus 형식으로 변환.

## 필수 조건

- Docker 및 Docker Compose 설치.
- `Docker/Infra` 루트 디렉토리에 `.env` 파일.
- 외부 PostgreSQL 및 Redis 서비스 실행 필요.

## 설정

이 서비스는 다음 환경 변수(`.env`에 정의됨)를 사용합니다:

- `AIRFLOW_UID`: Airflow 프로세스 실행 사용자 ID.
- `AIRFLOW_DB_USER`, `AIRFLOW_DB_PASSWORD`: 메타데이터 DB 자격 증명.
- `REDIS_PASSWORD`: Redis 인증 비밀번호.
- `AIRFLOW_PORT`: 웹 UI 포트.
- `FLOWER_PORT`: Flower UI 포트.
- `STATSD_AIRFLOW_PORT`, `STATSD_PROMETHEUS_PORT`: 메트릭 포트.

## 사용법

서비스 시작:

```bash
docker-compose up -d
```

로그 확인:

```bash
docker-compose logs -f
```

## 접속

- **Airflow UI**: `http://localhost:${AIRFLOW_HOST_PORT}` (`.env` 파일의 실제 포트 확인)
- **Flower UI**: `http://localhost:${FLOWER_HOST_PORT}`

## 볼륨

- `airflow-dags`: DAG 파일 저장.
- `airflow-logs`: 실행 로그 저장.
- `airflow-config`: 설정 파일 저장.
- `airflow-plugins`: 커스텀 플러그인 저장.
