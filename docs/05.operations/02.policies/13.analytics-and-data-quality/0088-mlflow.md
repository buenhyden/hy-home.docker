---
title: "MLflow Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0088"
parent_ids:
- "AD-0011"
created: "2026-09-21"
next_review_at: "2027-05-13"
---

# MLflow Operations Policy

## Purpose and Scope

### Objective

MLflow는 OPTIONAL tracking 서비스다. MLflow의 데이터베이스와 artifact store는 공유
인프라 위의 feature-owned 자원이며 공유 인프라의 권한을 절대 넓혀서는 안 된다.

#### Authority

- [Laboratory architecture](../../../02.architecture/01.descriptions/0011-laboratory-architecture.md)
- [Image Dockerfile](../../../../infra/08-ai/mlflow/Dockerfile) and [derived version projection](../../../../infra/tech-stack.versions.json)
- [MLflow Compose source](../../../../infra/08-ai/mlflow/docker-compose.yml)

### Applies To

MLflow tracking server의 활성화, 데이터베이스와 artifact 프로비저닝, 인증, credential
처리, backup/restore, 업그레이드, 제거.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0088-R1 | MLflow 선택 시 | 필수: `mlops` 또는 `data-science`를 통해서만 선택한다 | none | none |
| POL-0088-R2 | 항상 | 금지: 명시적 결정 없이 HOME이나 현재 운영 명령에 추가 | none | none |
| POL-0088-R3 | 항상 | 필수: MLflow SQL은 feature provisioning 파일에 둔다 | none | none |
| POL-0088-R4 | 항상 | 금지: 공유 `mng-pg-init` job이 MLflow secret을 읽음 | none | none |
| POL-0088-R5 | 항상 | 금지: 공유 `mng-pg-init` job이 MLflow DDL 실행 | none | none |
| POL-0088-R6 | 항상 | 필수: MLflow 데이터베이스 role은 `LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS`로 한다 | none | none |
| POL-0088-R7 | provisioning 시 | 필수: administrator role과 다른 role이 소유한 데이터베이스의 인수를 거부한다 | none | none |
| POL-0088-R8 | 항상 | 필수: 서버는 bucket-scoped SeaweedFS identity만 사용한다 | 런타임 검증(MLflow SeaweedFS user의 다른 bucket 거부) | none |
| POL-0088-R9 | 항상 | 금지: MLflow나 SDK에 SeaweedFS admin credential이나 다른 consumer의 identity 제공 | none | none |
| POL-0088-R10 | 항상 | 필수: credential은 argv나 backend URI를 거치지 않고 환경 변수로만 프로세스에 전달한다 | none | none |
| POL-0088-R11 | 항상 | 필수: route에서 gateway SSO를 유지한다 | 런타임 검증(세션 없는 gateway 요청의 거부/로그인 redirect와 인가 거부 403 유지) | none |
| POL-0088-R12 | 커뮤니티 OIDC plugin이나 `basic-auth` 채택 시 | 필수: UI·API·SDK 수용이 필요한 별도의 검토된 변경으로 다룬다 | 수동 | none |
| POL-0088-R13 | 업그레이드 전 | 필수: 데이터베이스와 bucket을 함께 백업한다 | none | none |
| POL-0088-R14 | 업그레이드 전 | 필수: 격리 환경에서 restore를 검증한다 | 런타임 검증(restore 리허설) | none |
| POL-0088-R15 | artifact 정리 시 | 필수: 참조·보존·복구본을 확인하고 별도로 승인한다 | 수동 | none |
| POL-0088-R16 | 항상 | 금지: `--allowed-hosts`나 gateway `/admins` 검사로 직접 peer 경로의 권한 통제가 완료되었다고 주장 | none | none |
| POL-0088-R17 | 기존 DB migration 시 | 필수: 서버 재시작과 별도 변경으로 다룬다 | none | none |

- `mlops` 또는 `data-science`를 통해서만 선택한다. 명시적 결정 없이는 HOME이나 현재
  운영 명령에 절대 추가하지 않는다.
- MLflow SQL은 feature provisioning 파일에 있다. 공유 `mng-pg-init` job은 MLflow
  secret을 읽거나 MLflow DDL을 실행해서는 안 된다.
- MLflow 데이터베이스 role은 `LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE
  NOREPLICATION NOBYPASSRLS`이다. Provisioning은 administrator role과 다른 role이 소유한
  데이터베이스를 인수하는 대신 거부한다.
- 서버는 bucket-scoped SeaweedFS identity만 사용한다. MLflow나 어떤 SDK에도
  SeaweedFS admin credential이나 다른 consumer의 identity를 주지 않는다.
- Credential은 argv나 backend URI를 거치지 않고 환경 변수로만
  프로세스에 전달한다.
- route에서 gateway SSO를 유지한다. 커뮤니티 OIDC plugin이나 `basic-auth`를 채택하는
  것은 UI, API, SDK 수용이 필요한 별도의 검토된 변경이다.
- 업그레이드 전에 데이터베이스와 bucket을 함께 백업하고 격리 환경에서 restore를
  검증한다.

#### 보존·삭제와 책임

책임자는 `@buenhyden`이다. run 삭제는 metadata soft-delete이며 bucket의 저장
공간 회수를 보장하지 않는다. artifact 정리는 참조·보존·복구본을 확인하고 별도로
승인한다. `--allowed-hosts`나 gateway `/admins` 검사로 직접 peer 경로의 권한 통제가
완료되었다고 주장하지 않는다. 기존 DB migration은 서버 재시작과 별도 변경이다.

### Exceptions

#### Exception Conditions

`edge_net`, `ai_net`, `mng_data_net`, `object_net`의 직접 SDK 접근에는
동등한 네이티브 사용자 인증이 선언되지 않았다. MLflow 레벨 인증
경로가 승인될 때까지 받아들이고 기록해 둔 gap일 뿐, 보증이 아니다. 어떤 예외도 gateway
SSO를 비활성화할 수 없다.

#### Approval and Review

MLflow 업그레이드, 인증 변경, bucket/데이터베이스 이름 변경, credential 회전 시 검토한다.

## Enforcement

### Mechanisms

정적 profile 렌더링, provisioning 계약 테스트, 일회성 PostgreSQL 리허설. 런타임 검증은
다음을 요구한다: 세션 없는 gateway 요청이 인증 경계에서 거부·로그인 redirect되고
인가 거부 403이 유지된다, artifact가 있는 run이 proxy를 통해
round-trip한다, MLflow SeaweedFS user가 다른 bucket에서 거부된다, restore 리허설이
수행된다.

### Limits

다음 규칙은 정책이 이름 있는 자동 검사를 연결하지 않았다.

- 이름 있는 검사 없음(선택): `POL-0088-R1`, `POL-0088-R2`
- 이름 있는 검사 없음(프로비저닝): `POL-0088-R3`, `POL-0088-R4`, `POL-0088-R5`
- 이름 있는 검사 없음(DB role): `POL-0088-R6`, `POL-0088-R7`
- 이름 있는 검사 없음(SeaweedFS): `POL-0088-R9`
- 이름 있는 검사 없음(credential): `POL-0088-R10`
- 이름 있는 검사 없음(업그레이드): `POL-0088-R13`
- 이름 있는 검사 없음(삭제·권한): `POL-0088-R16`, `POL-0088-R17`
- 수동 검토·승인에 의존(route): `POL-0088-R12`
- 수동 검토·승인에 의존(삭제·권한): `POL-0088-R15`
- 정책이 스스로 밝힌 한계: `edge_net`, `ai_net`, `mng_data_net`, `object_net`의 직접 SDK 접근에는 동등한 네이티브 사용자 인증이 선언되지 않았으며 승인될 때까지 받아들이고 기록한 gap이지 보증이 아니다.
- run 삭제는 metadata soft-delete이며 bucket의 저장 공간 회수를 보장하지 않는다.
- Mechanisms의 정적 profile 렌더링, provisioning 계약 테스트, 일회성 PostgreSQL 리허설은 어느 규칙에 대응하는지 정책이 연결하지 않았다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- [Guide](../../01.guides/13.analytics-and-data-quality/0088-mlflow.md) (`GDE-0088`)
- [Runbook](../../03.runbooks/13.analytics-and-data-quality/0088-mlflow.md) (`RUN-0088`)
- [Management database policy](../05.databases-and-storage/0028-management-database.md)
- [SeaweedFS policy](../05.databases-and-storage/0024-seaweedfs.md)
