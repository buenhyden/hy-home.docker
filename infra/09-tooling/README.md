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
- **User Guide**: [09-tooling README](../../docs/07.operations/09-tooling/README.md)
- **Operational Policy**: [09-tooling operations](../../docs/07.operations/09-tooling/README.md)
- **Runbook**: [09-tooling runbooks](../../docs/07.operations/09-tooling/README.md)

---

## Overview

`infra/09-tooling`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Compose 서비스 정의와 관련 설정 설명
- 서비스별 README와 운영 문서 연결
- 검증 시 참고해야 할 구성 파일 인벤토리

### Out of Scope

- secret 값 원문
- 사용자 승인 없는 runtime 동작 변경
- 다른 tier의 서비스 정책 중복 정의

## Structure

```text
infra/09-tooling/
├── k6/  # 하위 구성 영역
├── locust/  # 하위 구성 영역
├── registry/  # 하위 구성 영역
├── sonarqube/  # 하위 구성 영역
├── syncthing/  # 하위 구성 영역
├── terraform/  # 하위 구성 영역
├── terrakube/  # 하위 구성 영역
└── README.md  # This file
```

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
