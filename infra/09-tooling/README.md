# 09-tooling: Tooling Tier

## Overview (KR)

`09-tooling` 계층은 개발 주기 전반에 걸친 보조 서비스를 제공하는 인프라 계층이다. 인프라 자동화(Terrakube), 코드 품질 분석(SonarQube), 성능 테스트(Locust), 컨테이너 이미지 저장소(Registry), 파일 동기화(Syncthing) 등을 포함하며, 모든 서비스는 표준 인증(Keycloak) 및 데이터(PostgreSQL, MinIO) 계층과 통합되어 운영된다.

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

## Related Documents

- **PRD**: [2026-03-26-09-tooling.md](../../docs/01.prd/2026-03-26-09-tooling.md)
- **ARD**: [0009-tooling-architecture.md](../../docs/02.ard/0009-tooling-architecture.md)
- **Spec**: [09-tooling/spec.md](../../docs/04.specs/09-tooling/spec.md)
- **User Guide**: [09-tooling-user-guide.md](../../docs/07.guides/09-tooling-user-guide.md)
- **Operational Policy**: [09-tooling-operational-policy.md](../../docs/08.operations/09-tooling-operational-policy.md)
- **Runbook**: [09-tooling-maintenance.md](../../docs/09.runbooks/09-tooling-maintenance.md)
