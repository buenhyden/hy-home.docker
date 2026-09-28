---
title: "Terrakube Usage Guide"
version: "1.1.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0069"
parent_ids:
- "POL-0069"
implementation_services:
  infra/09-tooling/terrakube/docker-compose.yml:
  - terrakube-api
  - terrakube-executor
  - terrakube-ui
created: "2026-05-10"
---

# Terrakube Usage Guide

## Usage

### 목적과 분류

Terrakube는 온디맨드 DEV IaC 자동화/제어 플레인이다. API, UI, executor는
`iac`에만 속한다. 광범위한 `tooling`과 HOME은 이를 시작하지 않는다. 검토된 협업
실행과 private module/registry 워크플로 용도로 유지한다. 추적되는 토폴로지는
각 컴포넌트를 하나의 복제본으로만 두고 외부 의존성도 단일 호스트로 구성한다.
고가용성을 제공하거나 주장하지 않는다.

### 구현과 데이터 흐름

- [Terrakube Compose](../../../infra/09-tooling/terrakube/docker-compose.yml)가
  서비스, profile, 이미지, secret, healthcheck, 라우트, executor의 Docker socket
  접근을 정의한다. 파생된 이미지 프로젝션은 런타임 pin을 소유하지 않는다.
- 브라우저 -> Traefik -> `terrakube-ui`; UI -> `terrakube-api`; API는
  `terrakube-executor`로 작업을 전달한다. 기존 라우트는 게이트웨이 ForwardAuth를
  적용하며 UI/API 설정도 Keycloak/Dex 방식 OIDC를 사용한다. 두 계층 모두 테스트가
  필요하다. 정적 설정만으로는 네이티브 로그인이나 role 매핑을 증명하지 못한다.
- PostgreSQL(`mng-pg`)이 Terrakube 메타데이터를 보관한다. SeaweedFS 버킷
  `tfstate`가 state와 출력을 보관한다. Management Valkey가 작업을 조정한다. 이들은
  의존성이며 Terrakube leaf에 선언된 서비스가 아니다.
- Secret은 `terrakube_db_password`, `seaweedfs_s3_terrakube_secret_key`,
  `terrakube_valkey_password`, `terrakube_pat_secret`,
  `terrakube_internal_secret`이며 값은 절대 증거에 들어가지 않는다.
- executor는 `/var/run/docker.sock`을 읽기-쓰기로 마운트한다. 호스트와
  동등한 실행 권한이므로 로컬 Docker 관리와 같은 수준의 신뢰가 필요하다.
- health endpoint는 컴포넌트 프로세스 준비 상태만 증명한다. DB, object-state,
  VCS, OIDC, executor의 end-to-end 수용을 증명하지 않는다.

### 일반적인 사용

1. organization/workspace, VCS repository/ref, provider credential, 예상
   리소스, state key, 승인 경계를 식별한다.
2. 루트에서 `docker compose --profile iac config --quiet`를 실행하고 Terrakube
   서비스 세 개와 별도로 선택된 의존성을 모두 확인한다.
3. credential이나 state를 출력하지 않고 PostgreSQL, SeaweedFS `tfstate`,
   Valkey, Keycloak, 게이트웨이 준비 상태를 검증한다.
4. 의존성과 Docker socket 권한 검토 후에만 Terrakube 서비스를 시작한다. UI
   로그인, API 인가, executor 등록, 적용하지 않는 plan을 별도로 검증한다.
5. 인프라를 apply하거나 destroy하려면 별도의 원격 변경 승인이 필요하다.

### 상태, 백업, 업그레이드

복구에는 일관된 세트가 필요하다. Terrakube PostgreSQL 데이터베이스, SeaweedFS
`tfstate` object/버전, 관련 Keycloak client/role 설정, 추적되는 Compose, secret
메타데이터/보관 정보. Valkey는 조정 상태이므로 비어 있거나 정지된 제어 플레인과
일관되어야 한다. 조정된 데이터베이스/object 스냅샷을 찍기 전에 새 실행을 중지하고
API/executor를 정지한다. provider와 webhook egress를 비활성화한 격리 환경에서만
복원하고, DB/state-key 참조 일관성과 적용하지 않는 plan을 검증한다. SeaweedFS
사본 하나나 DB 덤프 하나만으로 복구 가능성을 추정하지 않는다.

업그레이드 전에는 이 조정된 백업을 확보하고, Terrakube release/마이그레이션
노트를 읽고, 복원된 사본에 대해 테스트하고, 컴포넌트 세트 하나를 함께 롤포워드한다.
마이그레이션 이후 데이터베이스/state 롤백 없이 이미지만 롤백하는 것은 안전하지
않다. 이 문서 작업에서는 백업/복원과 업그레이드 리허설을 실행하지 않았다.

## Common Checks

- `docker compose --profile iac config --quiet`
- `docker compose --profile iac config --services`
- `bash scripts/hardening/check-all-hardening.sh 09-tooling`

## Runbook Handoff

실행 실패, 조정된 백업/복원, OIDC 진단, 업그레이드에는
[runbook](../runbooks/0069-terrakube.md)을 사용한다.

## Traceability

- [Policy](../policies/0069-terrakube.md) (`POL-0069`)
- [Runbook](../runbooks/0069-terrakube.md) (`RUN-0069`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Terrakube architecture](https://docs.terrakube.io/architecture)
- [Terrakube Amazon-compatible storage](https://docs.terrakube.io/getting-started/deployment/storage-backend/amazon-cloud-storage)
- [Terrakube project and Apache-2.0 license](https://github.com/terrakube-io/terrakube)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- [Operations index](../README.md)
