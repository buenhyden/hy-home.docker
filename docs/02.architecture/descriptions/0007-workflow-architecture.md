---
profile_id: architecture-description
status: active
artifact_id: AD-0007
artifact_type: architecture-description
parent_ids:
  - REQ-0008
created: 2026-03-26
updated: 2026-08-10
---
# Workflow Tier (07-workflow) Architecture Description

## Context and Stakeholders

이 문서는 `07-workflow` 계층의 참조 아키텍처를 정의한다. 이 계층은 상이한 요구사항을 가진 두 가지 엔진(Airflow, n8n)을 하이브리드 방식으로 운영하며, root-included dev compose와 service-local compose의 broker 경계를 명확히 분리한다.

## Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

`07-workflow` 계층은 서비스 및 인프라 간의 워크플로우를 제어하고 자동화하는 통합 오케스트레이션 계층이다.

- **Airflow**: 프로그래밍 프레임워크 기반의 복잡한 데이터 파이프라인 관리.
- **n8n**: 빠른 연동, API 중심 자동화, 비개발자 친화적인 워크플로 전용.

## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owns**:
  - Airflow services (`airflow-apiserver`, scheduler, dag-processor, worker, triggerer, Flower).
  - n8n Server & Task Runner.
  - Workflow broker wiring: root dev uses shared `mng-valkey`; service-local compose declares dedicated Airflow/n8n Valkey services.
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

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: CeleryExecutor를 통한 수평 확장으로 동시 태스크 처리량 확보.
- **Security**: RBAC(Role-Based Access Control)를 통한 UI 접근 제어, 시크릿 정보는 Vault/Secrets 관리.
- **Reliability**: Management PostgreSQL 연동을 통한 워크플로 메타데이터 영속성 보장.
- **Scalability**: CeleryExecutor 및 n8n worker 확장을 통한 병렬 처리 능력 확보.
- **Reliability**: Valkey 기반의 메시지 큐 시스템을 통한 작업 유실 방지.
- **Observability**: Flower를 통한 Celery 워커 모니터링, Prometheus 메트릭 수집.

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

시스템은 크게 두 가지 영역으로 나뉜다.

1. **Programmatic Orchestration (Airflow)**: CeleryExecutor 기반의 분산 구조. Redis 프로토콜의 Valkey를 브로커로 사용하여 태스크를 분배한다.
2. **Visual Automation (n8n)**: Queue 모드로 실행되어 대량의 자동화 요청을 안정적으로 처리하며, 로컬 Python Runner를 통해 스크립트 실행 기능을 보완한다.

## Data Flow

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

- **Key Entities / Flows**:
  - DAG/Workflow Definitions: 버전 관리되는 파일 시스템 또는 내부 DB.
  - Execution Metrics: StatsD/Prometheus를 통해 외부로 전송.
- **Storage Strategy**:
  - Metadata: PostgreSQL (`mng-db`) 내 독립된 스키마/데이터베이스 사용.
  - Task Logs: Persistent Volume (NFS/Local) 또는 S3 호환 저장소.

## Deployment View

- **Runtime / Platform**: Docker Compose (Infrastructure Profile: `workflow`).
- **Deployment Model**: Infrastructure-as-code 기반의 컨테이너화된 배포.
- **Operational Evidence**: `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`, hardening gate, and runtime service health.

## Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [008-workflow.md](../../01.requirements/0008-workflow.md)
- **Spec**: [008-workflow/spec.md](../../03.specs/0008-workflow/spec.md)
- **Plan**: 2026-03-26-07-workflow-standardization.md
- **ADR**: [0007-airflow-n8n-hybrid-workflow.md](../decisions/0007-airflow-n8n-hybrid-workflow.md)
