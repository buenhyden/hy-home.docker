---
title: "Terrakube Usage Guide"
version: "1.1.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0069"
parent_ids:
- "POL-0069"
implementation_services:
  infra/09-platform-ops/terrakube/docker-compose.yml:
  - terrakube-api
  - terrakube-executor
  - terrakube-ui
created: "2026-05-10"
---

# Terrakube Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### 목적과 분류

Terrakube는 온디맨드 DEV IaC 자동화/제어 플레인이다. API, UI, executor는
`iac`에만 속한다. 광범위한 `tooling`과 HOME은 이를 시작하지 않는다. 검토된 협업
실행과 private module/registry 워크플로 용도로 유지한다. 추적되는 토폴로지는
각 컴포넌트를 하나의 복제본으로만 두고 외부 의존성도 단일 호스트로 구성한다.
고가용성을 제공하거나 주장하지 않는다.

### 구현과 데이터 흐름

- [Terrakube Compose](../../../infra/09-platform-ops/terrakube/docker-compose.yml)가
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
4. 현재 인증 경로 제한을 먼저 확인한다. 브라우저 로그인만으로 CLI/API와 executor
   실행이 가능하다고 판단하지 않는다. 아래 제한을 별도 구현 검토로 해소하고 승인을
   받은 뒤에만 서비스 기동·등록·비적용 plan 검증을 런북에 따라 수행한다.
5. 인프라를 apply하거나 destroy하려면 별도의 원격 변경 승인이 필요하다.

### 상태, 백업, 업그레이드

실행 순서와 실패·복구 판단은 [런북](../runbooks/0069-terrakube.md)의 `복구 세트와 버전 변경` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Common Checks

- `docker compose --profile iac config --quiet`
- `docker compose --profile iac config --services`
- `bash scripts/hardening/check-all-hardening.sh 09-platform-ops`

### Runbook Handoff

실행 실패, 조정된 백업/복원, OIDC 진단, 업그레이드에는
[runbook](../runbooks/0069-terrakube.md)을 사용한다.

### 현재 실행 경로의 제한

추적되는 Compose와 README는 cookie 기반 ForwardAuth가 Terraform CLI/API 토큰
요청 및 공개 API URL을 사용하는 executor 요청을 막는 상태임을 명시한다. 전용
`home-terrakube` client/audience와 RBAC 활성화는 별도 승인된 구현 변경이 필요하다.
현재 gateway 통제는 유지하며 로그인·health 성공을 실행 가능 증거로 기록하지 않는다.
인증 오류를 우회하거나 실제 plan/apply를 재시도하지 말고 `@buenhyden`에게 보고한다.

### 컴포넌트별 준비와 자원

UI와 executor는 API의 health를 기다린다. API/executor의 버킷 초기화 의존성은
선택적이며 PostgreSQL·Valkey readiness를 기다리는 선언은 없다. API/executor는
`edge_net`, `terrakube_net`, `mng_data_net`, `object_net`, UI는 앞의 두 네트워크에
연결된다. 각 자원 제한은 Compose·공통 템플릿이 소유한다. executor가 참조하는
외부 도구의 `main` 및 Terraform release 목록은 특정 workspace 엔진 버전의 증거가
아니다. 사용한 도구·엔진의 실제 식별자를 승인된 실행 근거에 남겨야 한다.

### Traceability

- [Policy](../policies/0069-terrakube.md) (`POL-0069`)
- [Runbook](../runbooks/0069-terrakube.md) (`RUN-0069`)
- [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Terrakube architecture](https://docs.terrakube.io/architecture)
- [Terrakube Amazon-compatible storage](https://docs.terrakube.io/getting-started/deployment/storage-backend/amazon-cloud-storage)
- [Terrakube project and Apache-2.0 license](https://github.com/terrakube-io/terrakube)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- [Operations index](../README.md)
