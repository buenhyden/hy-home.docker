---
title: "Tooling Tier Architecture Description"
version: "2.1.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "architecture"
artifact_id: "AD-0009"
parent_ids:
- "REQ-0010"
created: "2026-03-26"
---
# Tooling Tier Architecture Description

## Context and Stakeholders

이 문서는 `09-tooling` 계층의 참조 아키텍처와 품질 속성을 정의한다. 인프라 자동화, 품질 분석, 성능 테스트 도구들의 시스템 경계, 책임, 그리고 공통 인프라와의 연동 구조를 제공한다.

### Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

`09-tooling` 계층은 프로젝트의 '운영 효율성'과 '품질 보증'을 담당하는 보조 계층이다. IaC 엔진, 분석 서버, 테스트 워커 등으로 구성되며, 공개 관리 UI가 있는 서비스는 gateway/SSO 경계를 사용하고, 필요한 서비스만 PostgreSQL, SeaweedFS, Valkey 같은 data tier backend와 연동한다.

## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owns**:
  - IaC CLI helper (`OpenTofu`)와 자동화 플랫폼 (`Terrakube`)
  - 정적 코드 분석 엔진 (`SonarQube`)
  - 분산 부하 테스트 시스템 (`Locust`)과 명시적 부하 테스트 작업 (`k6`)
  - 사설 패키지/이미지 스토리지 (`Registry`)
  - 수동 의존성 업데이트 작업 (`Renovate`)
- **Consumes**:
  - 데이터 지속성 서비스 (`04-data` / PostgreSQL, SeaweedFS, Valkey)
  - 공통 인증 서비스 (`02-auth` / Keycloak)
  - 네트워크 리소스 (선언된 Compose network)
- **Does Not Own**:
  - 코어 비즈니스 애플리케이션 서비스
  - 전역 관제 및 로깅 스택 (06-observability)
- **Non-goals**:
  - 실서비스의 트래픽 라우팅 및 외부 노출 관리 (Gateway 계층 소유)

## Quality Attributes

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Scalability**: Locust 워커와 Terrakube 실행 용량은 승인된 구성 변경으로 조정한다. 현재 고정 Compose 서비스가 자동 확장을 구현하거나 검증했다는 뜻은 아니다.
- **Security**: SonarQube/Terrakube 같은 공개 관리 UI에 gateway+SSO 체인 적용.
- **Reliability**: IaC state/object persistence를 선언된 backend에 보관한다. 동일 호스트의 SeaweedFS와 PostgreSQL은 독립 장애 도메인이 아니므로 호스트 장애 시 연속성을 보장하지 않는다. 백업과 격리 복구 검증은 별도 운영 증거가 필요하다.
- **Operability**: 중앙 집중식 대시보드 및 API를 통한 통합 제어 환경 제공.

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

시스템은 '관리형 도구(Managed Tools)'와 '실행형 도구(Execution Tools)'로 나뉜다.

1. **Management**: SonarQube, Terrakube API 등은 해당 profile을 선택한 환경에서 중앙 상태를 관리한다. HOME 상시 기동 대상으로 자동 포함하지 않는다.
2. **Execution**: Terrakube Worker, Locust Worker 등은 작업 발생 시 리소스를 점유하며 실제 연산을 수행한다.

## Data Flow

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

- **Key Entities / Flows**: Source Code → SonarQube Scan → Quality Result / IaC Configuration → OpenTofu 또는 Terrakube Plan → 승인된 Apply.
- **Storage Strategy**: Terrakube state/object data는 SeaweedFS S3 backend를 사용하고, SonarQube/Terrakube metadata는 management PostgreSQL을 사용한다. Registry와 OpenTofu workspace는 현재 bind mount 기반 local persistence를 사용한다. Syncthing runtime은 제거되었으며 파일 동기화 경로를 소유하지 않는다.
- **Data Boundaries**: 각 도구는 별도의 데이터베이스 또는 스키마를 사용하여 데이터 간섭을 방지한다.

## Deployment View

- **Runtime / Platform**: 현재 root Compose include 및 profile 계약을 사용하는 Docker Compose.
- **Deployment Model**: root `docker-compose.yml`은 모든 leaf를 include하고
  profile이 서비스를 선택한다. `tooling`은 Registry와 SonarQube만,
  `testing`은 k6와 Locust master/worker 모두, `iac`은 OpenTofu와 Terrakube
  API/UI/executor 모두, `dependency-update`는 Renovate만 선택한다. `registry`
  와 `sast`는 해당 단일 역할을 선택한다. `analytics-engineering`은 dbt와 그
  DB provisioning 작업, `contract-testing`은 Pact Broker와 그 DB provisioning
  작업, `api-mock`은 WireMock, `backup`은 Restic과 SQLite export 작업,
  `policy-check`는 Conftest 작업만 선택한다. 이 도구들은 HOME에 포함되지 않는다.
- **Operational Evidence**: `bash scripts/hardening/check-all-hardening.sh 09-tooling`, service healthcheck, approved root-context runtime evidence.

## Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [010-tooling.md](../../01.requirements/0010-tooling.md)
- [Current convergence Spec](../../03.specs/0180-home-dev-convergence/spec.md)
- [OpenTofu operations](../../05.operations/catalog/09-tooling/0082-opentofu/guide.md)
- [Terraform migration handoff](../../05.operations/catalog/09-tooling/0068-terraform/guide.md)
- **ADR**: [0009-tooling-services.md](../decisions/0009-tooling-services.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
