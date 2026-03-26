<!-- Target: docs/02.ard/0009-tooling-architecture.md -->

# Tooling Tier Architecture Reference Document (ARD)

## Tooling Tier Reference Document

## Overview (KR)

이 문서는 `09-tooling` 계층의 참조 아키텍처와 품질 속성을 정의한다. 인프라 자동화, 품질 분석, 성능 테스트 도구들의 시스템 경계, 책임, 그리고 공통 인프라와의 연동 구조를 제공한다.

## Summary

`09-tooling` 계층은 프로젝트의 '운영 효율성'과 '품질 보증'을 담당하는 보조 계층이다. IaC 엔진, 분석 서버, 테스트 워커 등으로 구성되며, 프로젝트의 표준 인증(SSO) 및 데이터 저장소(MinIO/DB)를 공유하여 일관된 관리 경험을 제공한다.

## Boundaries & Non-goals

- **Owns**:
  - IaC 자동화 플랫폼 (`Terrakube`)
  - 정적 코드 분석 엔진 (`SonarQube`)
  - 분산 부하 테스트 시스템 (`Locust`)
  - 사설 패키지/이미지 스토리지 (`Registry`)
  - P2P 데이터 동기화 서비스 (`Syncthing`)
- **Consumes**:
  - 데이터 지속성 서비스 (`04-data` / PostgreSQL, MinIO)
  - 공통 인증 서비스 (`02-auth` / Keycloak)
  - 네트워크 리소스 (`infra_net`)
- **Does Not Own**:
  - 코어 비즈니스 애플리케이션 서비스
  - 전역 관제 및 로깅 스택 (06-observability)
- **Non-goals**:
  - 실서비스의 트래픽 라우팅 및 외부 노출 관리 (Gateway 계층 소유)

## Quality Attributes

- **Scalability**: Locust 워커 및 Terrakube 실행기의 필요 시 유동적 스케일링 지원.
- **Security**: 모든 UI 서비스에 대한 Keycloak 기반 SSO 강제 적용.
- **Reliability**: 상태 정보(Terraform state)를 MinIO에 보관하여 노드 장애 시에도 연속성 보장.
- **Operability**: 중앙 집중식 대시보드 및 API를 통한 통합 제어 환경 제공.

## System Overview & Context

시스템은 '관리형 도구(Managed Tools)'와 '실행형 도구(Execution Tools)'로 나뉜다.
1. **Management**: SonarQube, Terrakube API 등은 지속적으로 구동되며 중앙 상태를 관리한다.
2. **Execution**: Terrakube Worker, Locust Worker 등은 작업 발생 시 리소스를 점유하며 실제 연산을 수행한다.

## Data Architecture

- **Key Entities / Flows**: Source Code → SonarQube Scan → Quality Result / Terraform Script → Terrakube Plan → Deployment.
- **Storage Strategy**: 대용량 바이너리(이미지, 아티팩트)는 MinIO를 활용하며, 메타데이터는 PostgreSQL 관리형 클러스터에 저장한다.
- **Data Boundaries**: 각 도구는 별도의 데이터베이스 또는 스키마를 사용하여 데이터 간섭을 방지한다.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Compose v3.8+ 기반의 컨테이너 오케스트레이션.
- **Deployment Model**: `tooling` 프로필로 그룹화되어 있으며, 필요에 따라 개별 서비스별 배포 가능.
- **Operational Evidence**: 컨테이너 헬스체크 및 각 서비스의 `/health` 엔드포인트를 통한 상태 모니터링.

## Related Documents

- **PRD**: [2026-03-26-09-tooling.md](../01.prd/2026-03-26-09-tooling.md)
- **Spec**: [09-tooling/spec.md](../04.specs/09-tooling/spec.md)
- **Plan**: [2026-03-26-09-tooling-standardization.md](../05.plans/2026-03-26-09-tooling-standardization.md)
- **ADR**: [0009-tooling-services.md](../03.adr/0009-tooling-services.md)
