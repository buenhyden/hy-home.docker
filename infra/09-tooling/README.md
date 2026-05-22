# 09-tooling: Tooling Tier

> Developer, quality, performance, registry, and IaC automation services.

## Overview (KR)

`09-tooling` 계층은 개발 주기 전반에 걸친 보조 서비스를 제공하는 인프라 계층이다. 인프라 자동화(Terrakube), 코드 품질 분석(SonarQube), 성능 테스트(Locust), 컨테이너 이미지 저장소(Registry), 파일 동기화(Syncthing) 등을 포함하며, 모든 서비스는 표준 인증(Keycloak) 및 데이터(PostgreSQL, MinIO) 계층과 통합되어 운영된다.

## Audience

이 README의 주요 독자:

- Platform Operators
- Developers using tooling services
- AI Agents

## Scope

### In Scope

- Tooling tier service index and high-level integration map
- Terrakube, SonarQube, Locust, Registry, Syncthing, Terraform, and k6 service routing
- Links to canonical tooling guide, policy, runbooks, and specs

### Out of Scope

- Service-specific runtime procedures that belong in leaf README or operations runbooks
- Secret values, CI tokens, registry credentials, or SaaS credentials
- Application code quality decisions outside the tooling infrastructure boundary

## Structure

```text
09-tooling/
├── k6/          # k6 load-testing service assets
├── locust/      # Locust distributed load-testing service
├── registry/    # Private OCI registry
├── sonarqube/   # Code quality service
├── syncthing/   # File synchronization service
├── terraform/   # Terraform helper/runtime area
├── terrakube/   # IaC automation service
└── README.md    # This file
```

## Architecture

![Tooling Architecture](https://img.shields.io/badge/Architecture-Tooling_Tier-blue)

본 계층은 서비스별로 독립된 컨테이너 환경을 가지며, `04-data` 계층을 영구 저장소로 활용한다.

- **IaC Engine**: Terrakube를 통한 Terraform 상태 관리 및 자동화.
- **Analysis Engine**: SonarQube를 통한 정적 코드 분석 및 품질 게이트 적용.
- **Load Generator**: Locust를 통한 분산 부하 테스트 환경 제공.
- **Storage**: OCI Registry 및 Syncthing을 통한 리소스 배포 및 공유.

## Services

| Service | Category | Key Feature | Integration |
| :--- | :--- | :--- | :--- |
| **Terrakube** | IaC Automation | TF State Management, API-driven Infra | PostgreSQL, MinIO |
| **SonarQube** | Code Quality | Static Analysis, Security Hotspots | PostgreSQL |
| **Locust** | Performance | Python-based Load Testing | Distributed Workers |
| **Registry** | Cont. Storage | Private OCI Registry | MinIO (S3 Backend) |
| **Syncthing** | Data Sync | P2P File Synchronization | Local Storage |

## Operational Governance

- **Manual Approval**: Production 인프라 변경 시 Terrakube에서의 수동 승인 필수.
- **Quality Gates**: SonarQube 분석 결과가 'Passed'인 경우에만 배포 추진 권장.
- **Clean-up**: Registry의 테스트 이미지는 주기적으로 정리(GC 수행).

## How to Work in This Area

1. Treat this README as a folder index; service-specific runtime details belong in each service leaf README.
2. Review the linked tooling guide, policy, and runbook indexes before changing service configuration.
3. Keep CI credentials, registry credentials, and provider tokens out of README content.
4. After adding, moving, or removing a tooling service, update this index and the matching operations index.

## Related Documents

- **PRD**: [2026-03-26-09-tooling.md](../../docs/01.requirements/2026-03-26-09-tooling.md)
- **ARD**: [0009-tooling-architecture.md](../../docs/02.architecture/requirements/0009-tooling-architecture.md)
- **Spec**: [09-tooling/spec.md](../../docs/03.specs/09-tooling/spec.md)
- **User Guide**: [09-tooling README](../../docs/05.operations/guides/09-tooling/README.md)
- **Operational Policy**: [09-tooling policies](../../docs/05.operations/policies/09-tooling/README.md)
- **Runbook**: [09-tooling runbooks](../../docs/05.operations/runbooks/09-tooling/README.md)
