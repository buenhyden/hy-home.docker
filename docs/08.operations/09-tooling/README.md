# Tooling Operations Policy (09-tooling)

> Toolchain Lifecycle, Database Maintenance & CI/CD Governance

## Overview

이 정책은 `hy-home.docker` 도구 계층(09-tooling)의 안정적인 운영과 데이터 관리를 위한 기준을 정의한다.

## Toolchain Maintenance

- **SonarQube Upgrades**: 코드 품질 규칙 업데이트를 위해 주기적으로 최신 Community 버전을 유지한다. 엘라스틱서치(Elasticsearch) 인덱스 재구축이 필요한 경우 무중단 업데이트가 불가능할 수 있음을 인지한다.
- **Terrakube Backups**: Terraform 상태(tfstate)는 MinIO에서 버전 관리를 수행하며, Terrakube 메타데이터 DB는 매일 백업을 수행한다.

## Operational Standards

### 1. 성능 및 리소스 관리

- [Performance Testing Operations Policy](./performance-testing.md) - General benchmarking and scaling policies.
- [Locust Operations Policy](./locust.md) - Specific governance for Locust service units.
- [k6 Operations Policy](./k6.md) - Specific governance for k6 infrastructure units.
- [Registry Operations Policy](./registry.md) - Governance for internal OCI image distribution.
- [SonarQube Operations Policy](./sonarqube.md) - Governance for code quality and security scanning.
- [07. Syncthing Operations](./syncthing.md) - P2P sync integrity and conflict management.
- [08. Terraform Operations](./terraform.md) - IaC state policy and deployment workflow.
- [09. Terrakube Operations](./terrakube.md) - Collaborative IaC governance and registry policy.chronization.
- **Memory Limits**: SonarQube는 높은 메모리 할당을 요구하므로, `common-optimizations.yml`의 `high` 최적화 템플릿을 준수한다.

### 2. 접근 제어 (Access Control)

- 모든 도구(SonarQube, Terrakube)는 Keycloak SSO를 기반으로 한 RBAC 정책을 적용한다.
- `registry`는 [Registry Operations Policy](./registry.md)에 따라 내부 네트워크에서 관리한다.

## Database & Persistence

- 도구별 전용 데이터베이스 스키마는 `04-data`의 매니지먼트 PostgreSQL 클러스터에서 독립적으로 관리한다.
- 불필요한 테스트 실행 기록은 60일 경과 시 자동 아카이빙 처리한다.

## Related Documents

- [07. Guides](../../07.guides/09-tooling/README.md)
- [09. Runbooks](../../09.runbooks/09-tooling/README.md)
