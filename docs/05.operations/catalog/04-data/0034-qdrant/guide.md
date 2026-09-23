---
title: "Qdrant Usage Guide"
version: "1.0.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0034"
parent_ids:
- "POL-0034"
implementation_services:
  infra/04-data/specialized/qdrant/docker-compose.yml:
  - 'qdrant'
created: "2026-05-10"
---

# Qdrant Usage Guide

## Usage

### Overview

이 문서는 root compose에 active include된 [Qdrant Compose 구현](../../../../../infra/04-data/specialized/qdrant/docker-compose.yml)을 설명한다. 현재 구현은 frozen `HOME` 단일 `qdrant` 서비스, exact `ai`/`ai-llm`/`qdrant` profiles, `ai_net`, SSO 뒤의 REST route와 `/readyz` healthcheck를 사용한다. gRPC는 network 안의 `qdrant:6334`로만 쓴다.

### Current implementation

| Field | Repository-specific decision |
| --- | --- |
| Consumer and data rationale | HOME vector storage for AI/RAG consumers under `ai` and `ai-llm`; `qdrant` supports direct selection. |
| Source / updater | [Compose](../../../../../infra/04-data/specialized/qdrant/docker-compose.yml) owns the image source; compatibility review owns snapshot/version changes. |
| Services / profiles | Single `qdrant`; exact `ai`, `ai-llm`, `qdrant`. |
| Flow / exposure | REST through Traefik HTTPS behind SSO; gRPC only in-network on `qdrant:6334`; no host publication. |
| Persistence / environment | `qdrant-data:/qdrant/storage`, snapshots under `/qdrant/storage/snapshots`; service ports/path are Compose environment keys. |
| Secrets / security | No API-key secret is declared; authentication requirements require an implementation change. |
| Health / resources | `/readyz`; `template-stateful-med`. |
| Backup / upgrade | snapshot restore to same minor or next minor target with approximately 2x disk; verify collections/aliases/counts before promotion. |
| License / edition | Qdrant source is Apache-2.0; managed-cloud features are outside this self-hosted single-node contract. |

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

Qdrant를 vector storage로 사용할 때 현재 repository의 service name, route, protocol, persistence, snapshot path, no-secret state를 compose와 맞춰 이해하도록 한다.

### Prerequisites

- 루트 [docker-compose.yml](../../../../../docker-compose.yml)에 `infra/04-data/specialized/qdrant/docker-compose.yml`가 active include인지 확인한다.
- `DEFAULT_DATA_DIR`, `DEFAULT_URL`, `QDRANT_PORT`, `QDRANT_GRPC_PORT` 값이 로컬 환경과 맞아야 한다. 아래 명령의 `6333`은 기본 `QDRANT_PORT`이며, 바꿨다면 그 값으로 바꿔 쓴다.
- 현재 compose에는 Qdrant API-key secret이 선언되어 있지 않다. 인증 정책을 추가하려면 compose, policy, guide, runbook을 같은 변경 단위로 갱신한다.

### Step-by-step Instructions

1. root-active compose 구성을 렌더링한다.

   ```bash
   docker compose --profile qdrant config --quiet
   ```

2. 서비스 상태를 확인한다.

   ```bash
   docker compose ps qdrant
   ```

3. REST health route를 확인한다.

   ```bash
   docker compose exec qdrant bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333; printf "GET /readyz HTTP/1.0\r\n\r\n" >&3; cat <&3'
   ```

4. collection inventory 같은 read-only API만 일반 점검에 사용한다.

   ```bash
   docker compose exec qdrant bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333; printf "GET /collections HTTP/1.0\r\n\r\n" >&3; cat <&3'
   ```

5. `qdrant.${DEFAULT_URL}` 경로는 SSO 뒤에 있고(Qdrant에 API key 없음) gRPC route는 없다. 컨테이너는 `ai_net`에서 `qdrant:6333`(REST)·`qdrant:6334`(gRPC)를 쓴다.

### Common Pitfalls

- 현재 compose는 host port publish가 아니라 SSO 뒤의 Traefik REST route와 internal expose를 사용한다.
- Qdrant API-key secret은 현재 선언되어 있지 않다. 인증이 필요한 요구사항은 compose와 operations 문서를 함께 변경해야 한다.
- create/search/delete collection 예시는 데이터 mutation 또는 application workflow이므로 일반 usage check가 아니라 application guide 또는 승인된 runbook에서 다룬다.
- snapshot restore compatibility는 same minor 또는 next minor로 제한하고 target collection 부재/force semantics와 약 2배 disk headroom을 사전 확인한다.

## Common Checks

- `docker compose --profile qdrant config --quiet`
- `docker compose ps qdrant`
- `docker compose exec qdrant bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333; printf "GET /readyz HTTP/1.0\r\n\r\n" >&3; cat <&3'`
- `docker compose exec qdrant bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333; printf "GET /collections HTTP/1.0\r\n\r\n" >&3; cat <&3'`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [Qdrant runbook](runbook.md)을 따른다.

## Traceability

- Declared parent: [Qdrant Operations Policy](policy.md) (`POL-0034`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Policy](policy.md) (`POL-0034`), [Runbook](runbook.md) (`RUN-0034`)

## Related Documents

- [Qdrant snapshots](https://qdrant.tech/documentation/operations/snapshots/)
- [Qdrant migration and recovery](https://qdrant.tech/documentation/migration-recovery-options/)
- [Qdrant source and license](https://github.com/qdrant/qdrant)

- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/specialized/qdrant/README.md)
