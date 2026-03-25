# Tooling Operations Policy (09-tooling)

> Toolchain Lifecycle, Database Maintenance & CI/CD Governance

## Overview

이 정책은 `hy-home.docker` 도구 계층(09-tooling)의 안정적인 운영과 데이터 관리를 위한 기준을 정의한다.

## Toolchain Maintenance

- **SonarQube Upgrades**: 코드 품질 규칙 업데이트를 위해 주기적으로 최신 Community 버전을 유지한다. 엘라스틱서치(Elasticsearch) 인덱스 재구축이 필요한 경우 무중단 업데이트가 불가능할 수 있음을 인지한다.
- **Terrakube Backups**: Terraform 상태(tfstate)는 MinIO에서 버전 관리를 수행하며, Terrakube 메타데이터 DB는 매일 백업을 수행한다.

## Operational Standards

### 1. 성능 및 리소스 관리

- **Locust Benchmarking**: 대규모 부스트 테스트는 공식 유지보수 시간(Maintenance Window) 내에 수행하는 것을 원칙으로 한다.
- **Memory Limits**: SonarQube는 높은 메모리 할당을 요구하므로, `common-optimizations.yml`의 `high` 최적화 템플릿을 준수한다.

### 2. 접근 제어 (Access Control)

- 모든 도구(SonarQube, Terrakube)는 Keycloak SSO를 기반으로 한 RBAC 정책을 적용한다.
- `registry`는 개인 토큰(PAT) 또는 기본 인증을 통해 엄격히 관리한다.

## Database & Persistence

- 도구별 전용 데이터베이스 스키마는 `04-data`의 매니지먼트 PostgreSQL 클러스터에서 독립적으로 관리한다.
- 불필요한 테스트 실행 기록은 60일 경과 시 자동 아카이빙 처리한다.

## Related Documents

- [07. Guides](../../docs/07.guides/09-tooling/README.md)
- [09. Runbooks](../../docs/09.runbooks/09-tooling/README.md)
