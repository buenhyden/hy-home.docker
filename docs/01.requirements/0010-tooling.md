---
title: "Tooling Tier (09-tooling) Product Requirements"
version: "2.0.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "requirements"
artifact_id: "REQ-0010"
parent_ids: []
created: "2026-03-26"
---
# Tooling Tier (09-tooling) Product Requirements

## Problem and Goals

이 문서는 `09-tooling` 계층의 제품 요구사항을 정의한다. 이 계층은 개발 주기 전반에 걸친 보조 서비스를 제공하며, IaC(Infrastructure as Code) 자동화, 코드 품질 분석, 그리고 대규모 성능 테스트를 지원하여 안정적이고 효율적인 개발 환경을 구축하는 것을 목표로 한다.

### Problem Statement

인프라 변경 사항이 수동으로 관리되어 추적이 어렵고, 코드 품질 및 성능 검증이 파편화되어 있어 시스템의 전체적인 안정성을 보장하기 위한 중앙 집중식 도구가 필요하다.

## Stakeholders and User Needs

코드 품질 검사부터 인프라 프로비저닝 자동화까지 아우르는 통합 툴링 생태계를 구축하여, 수동 작업을 최소화하고 데이터 기반의 엔지니어링 의사결정을 지원한다.

### Personas

- **DevOps Engineer**: IaC 자동화를 통해 인프라를 일관되게 관리하고 배포 시간을 단축하고 싶어 한다.
- **Developer**: 작업 중인 코드의 품질 지표를 확인하고 내부 이미지 저장소를 통해 배포 산출물을 공유하고 싶어 한다.
- **QA/Performance Engineer**: 시스템의 한계 치를 측정하기 위해 대규모 부하 테스트를 쉽게 구성하고 실행하고 싶어 한다.

### Key Use Cases

- **STORY-01**: DevOps 엔지니어는 Terrakube를 통해 코드 변경 시마다 자동으로 인프라 계획(Plan)을 검토하고 배포한다.
- **STORY-02**: 개발자는 소스 코드 푸시 시 SonarQube를 통해 버그, 취약점, 코드 스멜을 자동으로 분석받는다.
- **STORY-03**: 성능 엔지니어는 Locust를 사용하여 분산 환경에서 수만 명의 동시 접속자를 시뮬레이션하고 병목 지점을 찾는다.

## Functional Requirements

- **REQ-0010-FR-0001**: IaC 실행 및 상태 관리를 위한 OpenTofu CLI helper와 중앙 집중식 오케스트레이션 지원 (Terrakube).
- **REQ-0010-FR-0002**: 다중 언어 정적 코드 분석 및 품질 게이트 적용 지원 (SonarQube).
- **REQ-0010-FR-0003**: Python 기반의 시나리오 정의 및 분산 부하 생성 지원 (Locust).
- **REQ-0010-FR-0004**: 내부 서비스 배포를 위한 단일 노드 사설 이미지 레지스트리 제공.

## Non-functional Requirements

No separately numbered non-functional requirement was identified in the source package.

## Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.

## Acceptance Criteria

- **REQ-0010-FR-0001**: 모든 인프라 변경의 IaC 수용률 100%.
- **REQ-0010-FR-0002**: 주요 서비스 코드의 테크니컬 데트(Technical Debt) 비율 5% 미만 유지.
- **REQ-0010-FR-0003**: 신규 환경 구축 시간 70% 이상 단축.

## Constraints

Syncthing runtime 제거에 따라 종전 functional allocation `0005`의 파일 동기화 의무는 2026-09-19에 철회되었다. 현재 제공 의무나 다른 기능으로 재할당하지 않는다. `REQ-0010.FR`의 high-water는 유지하고 번호 5는 Stage 99 Registry의 `reserved_history`에 영구 보존한다. 위 수용 기준은 검증 목표이며 현재 호스트에서 달성되었다는 증거를 뜻하지 않는다.

- **In Scope**:
  - 인프라 자동화 도구 및 관리 플랫폼.
  - 개발 생산성 및 품질 향상을 위한 보조 환경.
  - 내부 보안 통제 하의 리소스 공유 인프라.
- **Out of Scope**:
  - 실제 비즈니스 로직 구동 서버.
  - 서비스 모니터링 및 로깅 시스템 (06-observability 담당).
- **Non-goals**:
  - 범용 퍼블릭 클라우드 서비스 제공.

### AI Agent Requirements

N/A

## Risks

- **Risks**: Terrakube API 장애 시 인프라 변경 차단 위험.
- **Dependencies**: Terrakube/SonarQube 등 선택 서비스는 선언된 `04-data` backend와 `02-auth` 경계를 사용한다. Registry와 OpenTofu helper는 현재 local/bind-mount 중심이다. 단일 호스트의 volume 보존만으로 백업이나 호스트 장애 복구가 보장되지는 않는다.

## Traceability

- **Architecture Description**: [0009-tooling-architecture.md](../02.architecture/descriptions/0009-tooling-architecture.md)
- [Current convergence Spec](../03.specs/0180-home-dev-convergence/spec.md)
- [Current convergence Plan](../03.specs/0180-home-dev-convergence/plan.md)
- **ADR**: [0009-tooling-services.md](../02.architecture/decisions/0009-tooling-services.md)
