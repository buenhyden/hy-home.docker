# 🔄 Automation Workflows Guide

복잡한 데이터 파이프라인과 비즈니스 프로세스 자동화를 위한 가이드입니다.

## 1. Engine Comparison

| 엔진 | 주 용도 | 특징 |
| :--- | :--- | :--- |
| **n8n** | 노드 기반 로우코드 자동화 | 시각적 워크플로우, 400+ 앱 연동, 간편한 API 통합 |
| **Apache Airflow** | 복잡한 데이터 엔지니어링 (DAG) | Python 코드로 정의, 엄격한 스케줄링, ETL 최적화 |

## 2. n8n (Visual Automation)

- **접속 주소**: `https://n8n.${DEFAULT_URL}`
- **Database**: `mng-pg`를 메타데이터 저장소로 사용합니다.
- **Queue Mode (Option)**: 대량의 태스크 처리를 위해 Redis를 브로커로 사용하는 Worker 모드 확장이 가능합니다.

### 💡 주요 패턴

- **Webhooks**: 외부 서비스로부터 신호를 받아 즉시 처리.
- **AI Integration**: AI 에이전트 노드를 통해 LLM과 연계된 워크플로우 구성.
- **Credentials**: 서비스 인증 정보는 n8n 내부에 안전하게 암호화되어 저장됩니다.

## 3. Apache Airflow (Data Pipeline)

- **접속 주소**: `https://airflow.${DEFAULT_URL}`
- **Structure**: Scheduler, Webserver, Worker, Triggerer로 구성됩니다.
- **DAGs Location**: `infra/airflow/dags/` 디렉토리에 Python 파일을 배치하면 자동 인식됩니다.

## 4. Operational Best Practices

### Error Handling & Monitoring

- 모든 워크플로우 장애 시 **Slack** 또는 **Email** 알림을 전송하도록 예외 처리 노드를 구성하십시오.
- **Observability**: `loki`를 통해 워크플로우 수행 로그를 통합 모니터링할 수 있습니다.

### Security

- n8n과 Airflow는 `Keycloak` 기반의 중앙 인증 또는 자체 배직 인증 레이어를 반드시 거치도록 설정되어 있습니다.
- 민감한 데이터는 환경 변수(`secrets`)를 통해 컨테이너에 전달하십시오.

## 5. Maintenance

- **Backup**: 워크플로우 정의(JSON/Python)는 정기적으로 Git 저장소에 백업하는 것을 권장합니다.
- **Version Update**: 워크플로우 엔진의 버전 업데이트 시, 데이터베이스 마이그레이션 호환성을 먼저 확인하십시오.
