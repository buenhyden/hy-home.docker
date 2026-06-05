---
status: active
---
<!-- Target: docs/02.architecture/requirements/0009-tooling-architecture.md -->

# Tooling Tier Architecture Reference Document (ARD)

## Tooling Tier Reference Document

## Overview

이 문서는 `09-tooling` 계층의 참조 아키텍처와 품질 속성을 정의한다. 인프라 자동화, 품질 분석, 성능 테스트 도구들의 시스템 경계, 책임, 그리고 공통 인프라와의 연동 구조를 제공한다.

## Summary

`09-tooling` 계층은 프로젝트의 '운영 효율성'과 '품질 보증'을 담당하는 보조 계층이다. IaC 엔진, 분석 서버, 테스트 워커 등으로 구성되며, 공개 관리 UI가 있는 서비스는 gateway/SSO 경계를 사용하고, 필요한 서비스만 PostgreSQL, MinIO, Valkey, InfluxDB 같은 data tier backend와 연동한다.

## Boundaries & Non-goals

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

- **Scalability**: Locust 워커 및 Terrakube 실행기의 필요 시 유동적 스케일링 지원.
- **Security**: SonarQube/Terrakube/Syncthing 같은 공개 관리 UI에 gateway+SSO 체인 적용.
- **Reliability**: 상태 정보(Terraform state)를 MinIO에 보관하여 노드 장애 시에도 연속성 보장.
- **Operability**: 중앙 집중식 대시보드 및 API를 통한 통합 제어 환경 제공.

## System Overview & Context

시스템은 '관리형 도구(Managed Tools)'와 '실행형 도구(Execution Tools)'로 나뉜다.

1. **Management**: SonarQube, Terrakube API 등은 지속적으로 구동되며 중앙 상태를 관리한다.
2. **Execution**: Terrakube Worker, Locust Worker 등은 작업 발생 시 리소스를 점유하며 실제 연산을 수행한다.

## Data Architecture

- **Key Entities / Flows**: Source Code → SonarQube Scan → Quality Result / Terraform Script → Terrakube Plan → Deployment.
- **Storage Strategy**: Terrakube state/object data는 MinIO 호환 backend를 사용하고, SonarQube/Terrakube metadata는 management PostgreSQL을 사용한다. Registry와 Syncthing은 현재 bind mount 기반 local persistence를 사용한다.
- **Data Boundaries**: 각 도구는 별도의 데이터베이스 또는 스키마를 사용하여 데이터 간섭을 방지한다.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Compose v3.8+ 기반의 컨테이너 오케스트레이션.
- **Deployment Model**: `tooling` 프로필로 그룹화되어 있으나, root `docker-compose.yml`의 09-tooling includes는 현재 optional/commented 상태다.
- **Operational Evidence**: `bash scripts/hardening/check-all-hardening.sh 09-tooling`, service healthcheck, approved root-context runtime evidence.

## Related Documents

- **PRD**: [2026-03-26-09-tooling.md](../../01.requirements/2026-03-26-09-tooling.md)
- **Spec**: [09-tooling/spec.md](../../03.specs/09-tooling/spec.md)
- **Plan**: [2026-03-26-09-tooling-standardization.md](../../04.execution/plans/2026-03-26-09-tooling-standardization.md)
- **ADR**: [0009-tooling-services.md](../decisions/0009-tooling-services.md)
