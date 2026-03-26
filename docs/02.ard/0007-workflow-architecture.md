<!-- Target: docs/02.ard/0007-workflow-architecture.md -->

# Workflow Tier (07-workflow) Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 `07-workflow` 계층의 참조 아키텍처를 정의한다. 이 계층은 상이한 요구사항을 가진 두 가지 엔진(Airflow, n8n)을 하이이브리드 방식으로 운영하며, 공통 인프라(Valkey, PostgreSQL)를 공유하여 운영 효율성을 도모한다.

## Summary

`07-workflow` 계층은 시서비스 및 인프라 간의 워크플로우를 제어하고 자동화하는 통합 오케스트레이션 계층이다.

- **Airflow**: 프로그래밍 프레임워크 기반의 복잡한 데이터 파이프라인 관리.
- **n8n**: 빠른 연동, API 중심 자동화, 비개발자 친화적인 워크플로 전용.

## Boundaries & Non-goals

- **Owns**:
  - Airflow Cluster (Scheduler, Webserver, Worker, Triggerer).
  - n8n Server & Task Runner.
  - Workflow 전용 Message Broker (Valkey).
- **Consumes**:
  - `04-data`: PostgreSQL Management Cluster (Airflow & n8n DB).
  - `06-observability`: Prometheus, Loki (Monitoring & Logging).
- **Does Not Own**:
  - 개별 서비스의 API 서버.
  - 영구적인 비즈니스 데이터 저장소 (04-data 소유).
- **Non-goals**:
  - 실시간 채팅 서버 기능.
  - 대용량 파일의 직접 저장.

## Quality Attributes

- **Performance**: CeleryExecutor를 통한 수평 확장으로 동시 태스크 처리량 확보.
- **Security**: RBAC(Role-Based Access Control)를 통한 UI 접근 제어, 시크릿 정보는 Vault/Secrets 관리.
- **Reliability**: Postgres HA 연동을 통한 워크플로 메타데이터 영속성 보장.
- **Scalability**: CeleryExecutor 및 n8n worker 확장을 통한 병렬 처리 능력 확보.
- **Reliability**: Valkey 기반의 메시지 큐 시스템을 통한 작업 유실 방지.
- **Observability**: Flower를 통한 Celery 워커 모니터링, Prometheus 메트릭 수집.

## System Overview & Context

시스템은 크게 두 가지 영역으로 나뉜다.

1. **Programmatic Orchestration (Airflow)**: CeleryExecutor 기반의 분산 구조. Redis 프로토콜의 Valkey를 브로커로 사용하여 태스크를 분배한다.
2. **Visual Automation (n8n)**: Queue 모드로 실행되어 대량의 자동화 요청을 안정적으로 처리하며, 로컬 Python Runner를 통해 스크립트 실행 기능을 보완한다.

## Data Architecture

- **Key Entities / Flows**:
  - DAG/Workflow Definitions: 버전 관리되는 파일 시스템 또는 내부 DB.
  - Execution Metrics: StatsD/Prometheus를 통해 외부로 전송.
- **Storage Strategy**:
  - Metadata: PostgreSQL (`mng-db`) 내 독립된 스키마/데이터베이스 사용.
  - Task Logs: Persistent Volume (NFS/Local) 또는 S3 호환 저장소.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Compose / Docker Swarm (Infrastructure Profile: `workflow`).
- **Deployment Model**: Infrastructure-as-code 기반의 컨테이너화된 배포.
- **Operational Evidence**: `docker-compose ps` 및 각 서비스별 Healthcheck 엔드포인트.

## Related Documents

- **PRD**: [2026-03-26-07-workflow.md](../01.prd/2026-03-26-07-workflow.md)
- **Spec**: [07-workflow/spec.md](../04.specs/07-workflow/spec.md)
- **Plan**: [2026-03-26-07-workflow-standardization.md](../05.plans/2026-03-26-07-workflow-standardization.md)
- **ADR**: [0007-airflow-n8n-hybrid-workflow.md](../03.adr/0007-airflow-n8n-hybrid-workflow.md)
