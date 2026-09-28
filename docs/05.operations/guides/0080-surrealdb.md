---
title: "SurrealDB Guide"
version: "0.2.2"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0080"
parent_ids:
- "POL-0080"
implementation_services:
  infra/11-laboratory/open-notebook/docker-compose.yml:
  - 'surrealdb'
created: "2026-09-19"
---

# SurrealDB Guide

## Usage

### Overview

SurrealDB는 Open Notebook을 위한 `OPTIONAL` 데이터베이스로, 업스트림 호환성을 위해
SurrealDB v2에 고정되어 있다.
[Compose 구현](../../../infra/11-laboratory/open-notebook/docker-compose.yml)은
정확히 `surrealdb`와 `notebook` profile 아래에 `surrealdb` 서비스 하나를 정의한다.
`admin`은 더 이상 이를 선택하지 않는다. 커스텀 Dockerfile과 entrypoint가 서버
프로세스를 소유하고, `surrealdb-data`가 `/mydata`를 영속화하며,
`surreal_db_password`가 Compose에 리터럴 없이 root 인증을 제공한다.

### 현재 구현

| Field | Repository-specific decision |
| --- | --- |
| 소비자와 데이터 근거 | Open Notebook을 위한 OPTIONAL 영속 다중 모델 데이터베이스이며, 업스트림 호환성 제약으로 SurrealDB v2에 고정되어 있다. |
| 소스 / 업데이터 | [Compose](../../../infra/11-laboratory/open-notebook/docker-compose.yml), [Dockerfile](../../../infra/11-laboratory/open-notebook/surrealdb/Dockerfile), entrypoint가 프로세스를 소유한다. base 이미지는 SurrealDB v2에 고정되어 있다. |
| 서비스 / profile | 단일 `surrealdb`; 정확히 `surrealdb`, `notebook`. |
| 흐름 / 노출 | Open Notebook은 `ai_net`에서 연결한다. 호스트 접근은 Compose 노출을 통한 내부 포트 8000이다. |
| 영속성 / 환경 | bind 기반 `surrealdb-data:/mydata`; 호스트 포트와 경로 입력은 Compose가 소유한다. |
| Secret / 보안 | `surreal_db_password`; root/namespace/database 인증 범위는 각 작업과 일치해야 한다. |
| Health / 리소스 | `surreal is-ready`는 도달 가능성만 증명한다. 커스텀 서비스는 Compose에 선언된 템플릿을 사용한다. |
| 백업 / 업그레이드 | 새로 호환되는 대상으로의 명시적 namespace/database export/import; 부분적으로 실패한 import는 대상 폐기가 필요하다; v2 내에서 업스트림 스토리지 형식 순서를 따른다. |
| 라이선스 / edition | SurrealDB 사용은 현재 공식 라이선스 조건을 준수해야 한다. 이 문서는 프로덕션이나 상업적 권리를 확장하지 않는다. |

### Usage Type

`system-guide | operational-reference`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

라이브 복구 테스트를 주장하지 않으면서 현재 profile, 노출, 영속성, 인증,
namespace/database 범위, 버전 제약(v2 전용), 복원 계약을 설명한다.

### Prerequisites

- 저장소 루트에서 작업한다. root Compose가 포함 여부를 소유한다.
- 값을 출력하거나 복사하지 않고 `surreal_db_password` Docker Secret을 준비한다.
- 의도한 SurrealDB namespace와 database를 기록한다. 이 범위 없는 export/import는
  허용 가능한 복구 아티팩트가 아니다.
- Compose/Dockerfile 선언을 런타임 버전 권한으로 취급한다(SurrealDB v2에 고정됨).
  Open Notebook은 v3 업그레이드를 지원하지 않는다.

### Step-by-step Instructions

1. 선택된 surface를 렌더링한다: `docker compose --profile surrealdb config --quiet`.
2. 선언된 서비스를 확인한다: `docker compose --profile surrealdb ps surrealdb`.
3. credential이나 데이터 없이 준비 상태를 확인한다:
   `docker compose exec -T surrealdb /usr/local/bin/surreal is-ready --endpoint http://127.0.0.1:8000`.
4. `ai_net`의 애플리케이션은 `ws://surrealdb:8000/rpc`로 연결한다.
5. 복구 인벤토리를 위해 모든 export를 엔진 버전, namespace, database, 인증 수준,
   스키마/데이터 범위, checksum, 보존 기간, 격리된 복원 결과와 연결한다.

### Common Pitfalls

- 준비 상태는 도달 가능성만 증명한다. 인증, namespace, database, 스키마, 영속성은
  검증하지 않는다.
- Open Notebook 업스트림은 SurrealDB v3를 지원하지 않는다. 이 컨테이너를
  SurrealDB v3로 업그레이드하면 프로토콜과 쿼리 실패가 발생한다.
- root, namespace, database 사용자는 서로 다른 인증 범위를 갖는다. 복원
  credential은 선택된 namespace/database와 `OPTION IMPORT` 동작에 대한 인가를 받아야
  한다.
- import는 오류가 나기 전에 일부만 적용될 수 있다. 실패한 격리 대상은 폐기하고 빈
  상태로 다시 만들어야 한다.
- 라이브 `/mydata` 디렉터리를 복사하지 않는다. 승인된 export나 별도로 승인된
  정지 상태 스토리지 절차를 사용한다.

## Common Checks

- `docker compose --profile surrealdb config --quiet`
- `docker compose --profile surrealdb ps surrealdb`
- `docker compose exec -T surrealdb /usr/local/bin/surreal is-ready --endpoint http://127.0.0.1:8000`

## Runbook Handoff

[Runbook](../runbooks/0080-surrealdb.md)이 health triage와 계획된 격리 export/import
리허설을 소유한다. [Policy](../policies/0080-surrealdb.md)가 백업, 인증, 보존,
업그레이드, 제거 통제를 소유한다.

## Traceability

- 선언된 상위 문서: [SurrealDB Policy](../policies/0080-surrealdb.md) (`POL-0080`)
- 관장 아키텍처: [AD-0011](../../02.architecture/descriptions/0011-laboratory-architecture.md)
- 관련 대상 문서: [Policy](../policies/0080-surrealdb.md), [Runbook](../runbooks/0080-surrealdb.md)

## Related Documents

- [SurrealDB export](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/export)
- [SurrealDB import](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/import)
- [SurrealDB upgrades and patching](https://surrealdb.com/docs/manage/self-hosted/upgrades-and-patching)
- [SurrealDB authentication](https://surrealdb.com/docs/learn/security/authentication/summary)
- [SurrealDB licensing](https://surrealdb.com/license)
- [Operations index](../README.md)
- [Infrastructure README](../../../infra/11-laboratory/open-notebook/README.md)
