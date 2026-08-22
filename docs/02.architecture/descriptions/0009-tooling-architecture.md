---
profile_id: architecture-description
status: active
artifact_id: AD-0009
artifact_type: architecture-description
parent_ids:
  - REQ-0010
created: 2026-03-26
updated: 2026-08-10
---
# Tooling Tier Architecture Description

## Tooling Tier Reference Document

## Context and Stakeholders

이 문서는 `09-tooling` 계층의 참조 아키텍처와 품질 속성을 정의한다. 인프라 자동화, 품질 분석, 성능 테스트 도구들의 시스템 경계, 책임, 그리고 공통 인프라와의 연동 구조를 제공한다.

## Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

`09-tooling` 계층은 프로젝트의 '운영 효율성'과 '품질 보증'을 담당하는 보조 계층이다. IaC 엔진, 분석 서버, 테스트 워커 등으로 구성되며, 공개 관리 UI가 있는 서비스는 gateway/SSO 경계를 사용하고, 필요한 서비스만 PostgreSQL, MinIO, Valkey, InfluxDB 같은 data tier backend와 연동한다.

## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owns**:
  - IaC 자동화 플랫폼 (`Terrakube`)
  - 정적 코드 분석 엔진 (`SonarQube`)
  - 분산 부하 테스트 시스템 (`Locust`)
  - 사설 패키지/이미지 스토리지 (`Registry`)
  - P2P 데이터 동기화 서비스 (`Syncthing`)
- **Consumes**:
  - 데이터 지속성 서비스 (`04-data` / PostgreSQL, MinIO, Valkey, InfluxDB)
  - 공통 인증 서비스 (`02-auth` / Keycloak)
  - 네트워크 리소스 (`infra_net`)
- **Does Not Own**:
  - 코어 비즈니스 애플리케이션 서비스
  - 전역 관제 및 로깅 스택 (06-observability)
- **Non-goals**:
  - 실서비스의 트래픽 라우팅 및 외부 노출 관리 (Gateway 계층 소유)

## Quality Attributes

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Scalability**: Locust 워커 및 Terrakube 실행기의 필요 시 유동적 스케일링 지원.
- **Security**: SonarQube/Terrakube/Syncthing 같은 공개 관리 UI에 gateway+SSO 체인 적용.
- **Reliability**: 상태 정보(Terraform state)를 MinIO에 보관하여 노드 장애 시에도 연속성 보장.
- **Operability**: 중앙 집중식 대시보드 및 API를 통한 통합 제어 환경 제공.

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

시스템은 '관리형 도구(Managed Tools)'와 '실행형 도구(Execution Tools)'로 나뉜다.

1. **Management**: SonarQube, Terrakube API 등은 지속적으로 구동되며 중앙 상태를 관리한다.
2. **Execution**: Terrakube Worker, Locust Worker 등은 작업 발생 시 리소스를 점유하며 실제 연산을 수행한다.

## Data Flow

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

- **Key Entities / Flows**: Source Code → SonarQube Scan → Quality Result / Terraform Script → Terrakube Plan → Deployment.
- **Storage Strategy**: Terrakube state/object data는 MinIO 호환 backend를 사용하고, SonarQube/Terrakube metadata는 management PostgreSQL을 사용한다. Registry와 Syncthing은 현재 bind mount 기반 local persistence를 사용한다.
- **Data Boundaries**: 각 도구는 별도의 데이터베이스 또는 스키마를 사용하여 데이터 간섭을 방지한다.

## Deployment View

- **Runtime / Platform**: Docker Compose v3.8+ 기반의 컨테이너 오케스트레이션.
- **Deployment Model**: `tooling` 프로필로 그룹화되어 있으나, root `docker-compose.yml`의 09-tooling includes는 현재 optional/commented 상태다.
- **Operational Evidence**: `bash scripts/hardening/check-all-hardening.sh 09-tooling`, service healthcheck, approved root-context runtime evidence.

## Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [010-tooling.md](../../01.requirements/0010-tooling.md)
- **Spec**: [010-tooling/spec.md](../../03.specs/0010-tooling/spec.md)
- **Plan**: 2026-03-26-09-tooling-standardization.md
- **ADR**: [0009-tooling-services.md](../decisions/0009-tooling-services.md)
