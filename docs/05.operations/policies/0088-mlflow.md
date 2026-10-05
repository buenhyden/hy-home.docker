---
title: "MLflow Operations Policy"
version: "1.0.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0088"
parent_ids:
- "AD-0011"
created: "2026-09-21"
---

# MLflow Operations Policy

## Overview

### Overview

MLflow는 OPTIONAL tracking 서비스다. MLflow의 데이터베이스와 artifact store는 공유
인프라 위의 feature-owned 자원이며 공유 인프라의 권한을 절대 넓혀서는 안 된다.

## Scope

### Policy Scope

MLflow tracking server의 활성화, 데이터베이스와 artifact 프로비저닝, 인증, credential
처리, backup/restore, 업그레이드, 제거.

### Traceability

- [Guide](../guides/0088-mlflow.md) (`GDE-0088`)
- [Runbook](../runbooks/0088-mlflow.md) (`RUN-0088`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Rules

### Controls

- `mlops` 또는 `data-science`를 통해서만 선택한다. 명시적 결정 없이는 HOME이나 현재
  운영 명령에 절대 추가하지 않는다.
- MLflow SQL은 feature provisioning 파일에 있다. 공유 `mng-pg-init` job은 MLflow
  secret을 읽거나 MLflow DDL을 실행해서는 안 된다.
- MLflow 데이터베이스 role은 `LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE
  NOREPLICATION`이다. Provisioning은 administrator role과 다른 role이 소유한
  데이터베이스를 인수하는 대신 거부한다.
- 서버는 bucket-scoped SeaweedFS identity만 사용한다. MLflow나 어떤 SDK에도
  SeaweedFS admin credential이나 다른 consumer의 identity를 주지 않는다.
- Credential은 argv나 backend URI를 거치지 않고 환경 변수로만
  프로세스에 전달한다.
- route에서 gateway SSO를 유지한다. 커뮤니티 OIDC plugin이나 `basic-auth`를 채택하는
  것은 UI, API, SDK 수용이 필요한 별도의 검토된 변경이다.
- 업그레이드 전에 데이터베이스와 bucket을 함께 백업하고 격리 환경에서 restore를
  검증한다.

### Verification

정적 profile 렌더링, provisioning 계약 테스트, 일회성 PostgreSQL 리허설. 런타임 검증은
다음을 요구한다: 세션 없는 gateway 요청이 인증 경계에서 거부·로그인 redirect되고
인가 거부 403이 유지된다, artifact가 있는 run이 proxy를 통해
round-trip한다, MLflow SeaweedFS user가 다른 bucket에서 거부된다, restore 리허설이
수행된다.

### Review Cadence

MLflow 업그레이드, 인증 변경, bucket/데이터베이스 이름 변경, credential 회전 시 검토한다.

### 보존·삭제와 책임

책임자는 `@buenhyden`이다. run 삭제는 metadata soft-delete이며 bucket의 저장
공간 회수를 보장하지 않는다. artifact 정리는 참조·보존·복구본을 확인하고 별도로
승인한다. `--allowed-hosts`나 gateway `/admins` 검사로 직접 peer 경로의 권한 통제가
완료되었다고 주장하지 않는다. 기존 DB migration은 서버 재시작과 별도 변경이다.

## Exceptions

### Exceptions

`edge_net`, `ai_net`, `mng_data_net`, `object_net`의 직접 SDK 접근에는
동등한 네이티브 사용자 인증이 선언되지 않았다. MLflow 레벨 인증
경로가 승인될 때까지 받아들이고 기록해 둔 gap일 뿐, 보증이 아니다. 어떤 예외도 gateway
SSO를 비활성화할 수 없다.

## Related Documents

- [Image Dockerfile](../../../infra/08-ai/mlflow/Dockerfile) and [derived version projection](../../../infra/tech-stack.versions.json)
- [MLflow Compose source](../../../infra/08-ai/mlflow/docker-compose.yml)
- [Management database policy](0028-management-database.md)
- [SeaweedFS policy](0024-seaweedfs.md)
