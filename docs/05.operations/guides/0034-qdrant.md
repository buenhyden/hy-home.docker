---
title: "Qdrant Usage Guide"
version: "1.2.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0034"
parent_ids:
- "POL-0034"
implementation_services:
  infra/04-data/qdrant/docker-compose.yml:
  - 'qdrant'
created: "2026-05-10"
---

# Qdrant Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Overview

이 문서는 root compose에 active include된 [Qdrant Compose 구현](../../../infra/04-data/qdrant/docker-compose.yml)을 설명한다. 현재 구현은 frozen `HOME` 단일 `qdrant` 서비스, exact `ai`/`ai-llm`/`qdrant` profiles, `ai_net`, SSO 뒤의 REST route와 `/readyz` healthcheck를 사용한다. gRPC는 network 안의 `qdrant:6334`로만 쓴다.

### Current implementation

| 항목 | 이 저장소의 구현 결정 |
| --- | --- |
| Consumer와 data 근거 | `ai`와 `ai-llm`의 AI/RAG consumer를 위한 HOME vector storage이며 `qdrant`로 직접 선택할 수도 있다. |
| Source·update 책임 | [Compose](../../../infra/04-data/qdrant/docker-compose.yml)가 image source를 소유한다. snapshot/version 변경은 호환성 검토가 소유한다. |
| 서비스·profile | 단일 `qdrant`; 정확한 profile은 `ai`, `ai-llm`, `qdrant`. |
| 흐름·노출 | REST는 SSO 뒤의 Traefik HTTPS를 통한다. gRPC는 network 내부의 `qdrant:6334`에서만 사용하며 host에는 공개하지 않는다. |
| 영속성·환경 설정 | `qdrant-data:/qdrant/storage`에 저장하고 snapshot은 `/qdrant/storage/snapshots` 아래에 둔다. service port/path는 Compose 환경 key이다. |
| Secret·보안 | API key는 `qdrant_api_key` secret(AI-008)에서 가져온다. `/readyz`, `/livez`, `/healthz`를 제외한 모든 REST/gRPC 호출에는 이 key 또는 읽기 전용 key가 필요하다. Prometheus는 읽기 전용 key `qdrant_read_only_api_key`(AI-009)만 보유한다. |
| Health·자원 | `/readyz`와 `template-stateful-med`를 사용한다. |
| Backup·upgrade | 약 2x의 disk 용량으로 같은 minor 또는 다음 minor 대상에 snapshot을 복구한다. 승격 전에 collection/alias/count를 검증한다. |
| License·edition | Qdrant source에는 Apache-2.0이 적용된다. managed-cloud 기능은 이 self-hosted single-node 계약에 포함되지 않는다. |

### Identity-specific behavior

Qdrant1.19.1 unprivileged 는 API key/read-only key 파일 참조를 사용한다. `/readyz`는 health-only 이며 collection authorization/search correctness 가 아니다. snapshot 은 `/qdrant/storage`와 같은 data disk 에 있으므로 별도 암호화 사본이 필요하다. 같은/다음 minor 복원과약 2 배 여유라는 upstream 범위도 original collection/version/config/alias 검토를 대신하지 않는다. snapshot/force overwrite·key rotation·collection 삭제는 승인된 target 에만 수행한다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `qdrant` | vector collections; local snapshot은 off-disk backup 아님 | readyz; API key/collection query 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/qdrant/docker-compose.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../98.archive/completed/03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

Qdrant를 vector storage로 사용할 때 현재 repository의 service name, route, protocol, persistence, snapshot path, API key를 compose와 맞춰 이해하도록 한다.

### Prerequisites

- 루트 [docker-compose.yml](../../../docker-compose.yml)에 `infra/04-data/qdrant/docker-compose.yml`가 active include인지 확인한다.
- `DEFAULT_DATA_DIR`, `DEFAULT_URL`, `QDRANT_PORT`, `QDRANT_GRPC_PORT` 값이 로컬 환경과 맞아야 한다. 아래 명령의 `6333`은 기본 `QDRANT_PORT`이며, 바꿨다면 그 값으로 바꿔 쓴다.
- Qdrant는 `qdrant_api_key` secret(AI-008)을 시작 스크립트가 `QDRANT__SERVICE__API_KEY`로 넘겨 API key를 요구한다. 클라이언트는 `api-key` 또는 `Authorization: Bearer` header로 보낸다. 읽기 전용 key `qdrant_read_only_api_key`(AI-009)는 `QDRANT__SERVICE__READ_ONLY_API_KEY`로 넘어가며, 16자 이상이고 전체 key와 달라야 시작한다. Prometheus는 이 읽기 전용 key만 받아 `bearer_token_file`로 보낸다.

### Step-by-step Instructions

정상 운영 중 점검은 compose profile 렌더링, 서비스 상태, REST `/readyz` health route, API key 기반 read-only `/collections` inventory 확인으로 구성된다. `qdrant.${DEFAULT_URL}` 경로는 SSO 뒤에 있고 그 뒤에서도 API key가 필요하며, gRPC route는 없다. 컨테이너는 `ai_net`에서 `qdrant:6333`(REST)·`qdrant:6334`(gRPC)를 쓴다. 실행 가능한 명령 순서와 기대 결과는 [Qdrant runbook](../runbooks/0034-qdrant.md#steps)을 따른다.

### Common Pitfalls

- 현재 compose는 host port publish가 아니라 SSO 뒤의 Traefik REST route와 internal expose를 사용한다.
- 새 클라이언트는 key를 secret file로 받아야 한다. 컨테이너 환경변수나 로그에 key 값을 남기지 않는다. Open WebUI는 Qdrant를 쓰지 않는다(`VECTOR_DB` 미설정, 로컬 저장소 사용).
- create/search/delete collection 예시는 데이터 mutation 또는 application workflow이므로 일반 usage check가 아니라 application guide 또는 승인된 runbook에서 다룬다.
- snapshot restore compatibility는 same minor 또는 next minor로 제한하고 target collection 부재/force semantics와 약 2배 disk headroom을 사전 확인한다.

### Common Checks

- `docker compose --profile qdrant config --quiet`
- `docker compose ps qdrant`
- `docker compose exec qdrant bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333; printf "GET /readyz HTTP/1.0\r\n\r\n" >&3; cat <&3'`
- `docker compose exec qdrant bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333; printf "GET /collections HTTP/1.0\r\napi-key: %s\r\n\r\n" "$(tr -d "\r\n" </run/secrets/qdrant_api_key)" >&3; cat <&3'`

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [Qdrant runbook](../runbooks/0034-qdrant.md)을 따른다.

### Traceability

- Declared parent: [Qdrant Operations Policy](../policies/0034-qdrant.md) (`POL-0034`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Policy](../policies/0034-qdrant.md) (`POL-0034`), [Runbook](../runbooks/0034-qdrant.md) (`RUN-0034`)

## Related Documents

- [Qdrant snapshots](https://qdrant.tech/documentation/operations/snapshots/)
- [Qdrant migration and recovery](https://qdrant.tech/documentation/migration-recovery-options/)
- [Qdrant source and license](https://github.com/qdrant/qdrant)

- [Operations index](../README.md)
- [Operations policy](../policies/0034-qdrant.md)
- [Recovery runbook](../runbooks/0034-qdrant.md)
- [Infra README](../../../infra/04-data/qdrant/README.md)
