---
title: "09-tooling: Tooling Tier"
version: "1.0.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
created: "2025-11-12"
---

# 09-tooling: Tooling Tier

> Developer, quality, performance, registry, and IaC automation services.

## Overview

`09-tooling`은 OpenTofu/Terrakube IaC, SonarQube 분석, Locust/k6 부하 테스트, OCI Registry와 Renovate dependency-update 작업을 제공한다. Root Compose가 leaf를 include하며 profile이 실행 대상을 선택한다. `tooling`은 OpenTofu, Terrakube API/UI/executor, SonarQube, Registry, Locust master/worker를 선택한다. `iac`, `sast`, `registry`는 해당 역할을 선택하고 `testing`은 Locust master와 k6를 선택한다. Locust worker는 `tooling`에만 포함된다. Renovate는 별도 `dependency-update` profile의 수동 작업이다.

Terraform과 Syncthing runtime은 제거되었다. 현재 IaC 실행은 OpenTofu를 사용하며 기존 Terraform workspace 이관은 문서 인덱스의 `0068-terraform` migration handoff를 따른다.

## Audience

이 README의 주요 독자:

- Platform Operators
- Developers using tooling services
- AI Agents

## Scope

### In Scope

- Tooling tier service index and high-level integration map
- OpenTofu, Terrakube, SonarQube, Locust, Registry, Renovate, and k6 service boundaries
- Links to canonical tooling guide, policy, runbooks, and specs

### Out of Scope

- Service-specific runtime procedures that belong in leaf README or operations runbooks
- Secret values, CI tokens, registry credentials, or SaaS credentials
- Application code quality decisions outside the tooling infrastructure boundary

## Structure

```text
09-tooling/
├── k6/          # k6 load-testing job assets
├── locust/      # Locust distributed load-testing service
├── registry/    # Private OCI registry
├── sonarqube/   # Code quality service
├── opentofu/    # OpenTofu CLI helper and workspace
├── renovate/    # Manual dependency-update job
├── terrakube/   # IaC automation service
└── README.md    # This file
```

## Architecture

![Tooling Architecture](https://img.shields.io/badge/Architecture-Tooling_Tier-blue)

본 계층은 서비스별로 독립된 컨테이너 환경을 가지며, 필요한 경우 `04-data` 계층의 PostgreSQL, MinIO, Valkey와 연동한다.

- **IaC Engine**: OpenTofu CLI helper 및 Terrakube workspace 실행 관리.
- **Analysis Engine**: SonarQube를 통한 정적 코드 분석 및 품질 게이트 적용.
- **Load Generator**: Locust를 통한 분산 부하 테스트 환경 제공.
- **Storage**: OCI Registry를 통한 컨테이너 이미지 보관.

## Services

| Service | Category | Key Feature | Integration |
| :--- | :--- | :--- | :--- |
| **Terrakube** | IaC Automation | TF State Management, API-driven Infra | PostgreSQL, MinIO |
| **SonarQube** | Code Quality | Static Analysis, Security Hotspots | PostgreSQL |
| **Locust** | Performance | Python-based Load Testing | Distributed Workers |
| **k6** | Performance | `k6` one-shot job; metrics via Prometheus remote write | Prometheus |
| **Registry** | Cont. Storage | Private OCI Registry | Bind mount `${DEFAULT_REGISTRY_DIR}` |
| **OpenTofu** | IaC CLI | Containerized `tofu` helper | Local workspace; read-only provider credential mounts |
| **Renovate** | Dependency Updates | Manual `dependency-update` job | GitHub; Docker Secret token; cache volume |

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

- **PRD**: 010-tooling.md (`docs/01.requirements/0010-tooling.md`)
- **ARD**: `docs/02.architecture/descriptions/0009-tooling-architecture.md`
- **Guide**: 09-tooling guide index (`docs/05.operations/catalog/09-tooling/README.md`)
- **Policy**: 09-tooling policy index (`docs/05.operations/catalog/09-tooling/README.md`)
- **Runbook**: 09-tooling runbooks (`docs/05.operations/catalog/09-tooling/README.md`)
- [Documentation index](../../docs/README.md)

Runtime pins are owned by the Compose/Dockerfile declarations; the [curated version projection](../tech-stack.versions.json) provides drift verification.
