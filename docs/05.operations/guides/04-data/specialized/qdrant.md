---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/specialized/qdrant.md -->

# Qdrant Usage Guide

## Usage

### Overview

이 문서는 root compose에 active include된 `infra/04-data/specialized/qdrant/docker-compose.yml` 기준으로 Qdrant vector database의 사용 맥락과 일반 점검 방법을 설명한다. 현재 구현은 `qdrant/qdrant:v1.18.1-unprivileged`, 단일 `qdrant` 서비스, `ai`/`data`/`dev` 프로파일, `infra_net`, REST route, gRPC TCP route, `/readyz` healthcheck를 사용한다.

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
- `DEFAULT_DATA_DIR`, `DEFAULT_URL`, `QDRANT_PORT`, `QDRANT_GRPC_PORT` 값이 로컬 환경과 맞아야 한다.
- 현재 compose에는 Qdrant API-key secret이 선언되어 있지 않다. 인증 정책을 추가하려면 compose, policy, guide, runbook을 같은 변경 단위로 갱신한다.

### Step-by-step Instructions

1. root-active compose 구성을 렌더링한다.

   ```bash
   docker compose --profile data --profile ai config qdrant
   ```

2. 서비스 상태를 확인한다.

   ```bash
   docker compose ps qdrant
   ```

3. REST health route를 확인한다.

   ```bash
   curl -fsS "https://qdrant.${DEFAULT_URL}/readyz"
   ```

4. collection inventory 같은 read-only API만 일반 점검에 사용한다.

   ```bash
   curl -fsS "https://qdrant.${DEFAULT_URL}/collections"
   ```

5. gRPC는 Traefik TCP route `qdrant-grpc.${DEFAULT_URL}`와 `${QDRANT_GRPC_PORT:-6334}` 기준이다. gRPC client 설정은 application 문서에서 관리한다.

### Common Pitfalls

- 현재 compose는 host port publish가 아니라 Traefik REST/TCP route와 internal expose를 사용한다.
- Qdrant API-key secret은 현재 선언되어 있지 않다. 인증이 필요한 요구사항은 compose와 operations 문서를 함께 변경해야 한다.
- create/search/delete collection 예시는 데이터 mutation 또는 application workflow이므로 일반 usage check가 아니라 application guide 또는 승인된 runbook에서 다룬다.

## Common Checks

- `docker compose --profile data --profile ai config qdrant`
- `docker compose ps qdrant`
- `curl -fsS "https://qdrant.${DEFAULT_URL}/readyz"`
- `curl -fsS "https://qdrant.${DEFAULT_URL}/collections"`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [Qdrant runbook](../../../runbooks/04-data/specialized/qdrant.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/specialized/qdrant.md)
- [Recovery runbook](../../../runbooks/04-data/specialized/qdrant.md)
- [Infra README](../../../../../infra/04-data/specialized/qdrant/README.md)
