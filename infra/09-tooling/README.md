# 09-tooling: Tooling Tier

> Developer, quality, performance, registry, and IaC automation services.

## Overview (KR)

`09-tooling` 계층은 개발 주기 전반에 걸친 보조 서비스를 제공하는 인프라 계층이다. 인프라 자동화(Terrakube/Terraform), 코드 품질 분석(SonarQube), 성능 테스트(Locust 및 k6 leaf의 Locust wrapper), 컨테이너 이미지 저장소(Registry), 파일 동기화(Syncthing)를 포함한다. 현재 root `docker-compose.yml`에서는 대부분 선택 include로 주석 처리되어 있으므로, 운영 문서는 optional root context와 service-local compose 경계를 구분한다.

## Audience

이 README의 주요 독자:

- Platform Operators
- Developers using tooling services
- AI Agents

## Scope

### In Scope

- Tooling tier service index and high-level integration map
- Terrakube, SonarQube, Locust, Registry, Syncthing, Terraform, and k6 service boundaries
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

본 계층은 서비스별로 독립된 컨테이너 환경을 가지며, 필요한 경우 `04-data` 계층의 PostgreSQL, MinIO, Valkey, InfluxDB와 연동한다.

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
| **k6** | Performance | Current Locust-wrapper `k6-master` leaf | InfluxDB |
| **Registry** | Cont. Storage | Private OCI Registry | Bind mount `${DEFAULT_REGISTRY_DIR}` |
| **Syncthing** | Data Sync | P2P File Synchronization | Local Storage |
| **Terraform** | IaC CLI | Containerized Terraform helper | Local workspace |

## Operational Governance

- **Manual Approval**: Production 인프라 변경 시 Terrakube에서의 수동 승인 필수.
- **Quality Gates**: SonarQube 분석 결과가 'Passed'인 경우에만 배포 추진 권장.
- **Clean-up**: Registry의 테스트 이미지는 주기적으로 정리(GC 수행).
- **Validation Boundary**: `bash scripts/hardening/check-all-hardening.sh 09-tooling` is the static hardening gate; optional runtime rendering must include root network/secret/dependency context.

## How to Work in This Area

1. Treat this README as a folder index; service-specific runtime details belong in each service leaf README.
2. Review the linked tooling guide, policy, and runbook indexes before changing service configuration.
3. Keep CI credentials, registry credentials, and provider tokens out of README content.
4. After adding, moving, or removing a tooling service, update this index and the matching operations index.

## Related Documents

- **PRD**: [010-tooling.md](../../docs/01.requirements/010-tooling.md)
- **ARD**: [0009-tooling-architecture.md](../../docs/02.architecture/requirements/0009-tooling-architecture.md)
- **Spec**: [09-tooling/spec.md](../../docs/03.specs/09-tooling/spec.md)
- **Guide**: [09-tooling guide index](../../docs/05.operations/guides/09-tooling/README.md)
- **Policy**: [09-tooling policy index](../../docs/05.operations/policies/09-tooling/README.md)
- **Runbook**: [09-tooling runbooks](../../docs/05.operations/runbooks/09-tooling/README.md)
