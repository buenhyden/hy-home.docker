---
title: "Specialized Data Services (04-data/specialized)"
version: "1.1.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-05-15"
---

# Specialized Data Services (04-data/specialized)

> 특수 목적 데이터 서비스 / Specialized Data Services

## Overview

이 디렉터리는 `hy-home.docker` 인프라의 루트가 무조건 include하는 specialized data 서비스 구성을 포함한다. 현재 루트 compose는 Neo4j graph database와 Qdrant vector database를 active include로 참조한다.

## Audience

이 README의 주요 독자:

- 인프라를 배포하고 관리하는 **Operators**
- 특수 데이터 서비스를 연동하는 **Developers**
- 자동화된 운영 작업을 수행하는 **AI Agents**

## Scope

### In Scope

- Neo4j graph database 구성과 `neo4j_password` Docker Secret 경계
- Qdrant vector database 구성과 현재 no-secret route 경계
- Traefik route, network 소속, persistent volume, linked operations docs

### Out of Scope

- 관계형·NoSQL·캐시 서비스 (`../relational/`, `../nosql/`, `../cache-and-kv/` 담당)
- 벡터 검색 애플리케이션 로직

## Structure

```text
specialized/
├── neo4j/        # Neo4j 그래프 데이터베이스
├── qdrant/       # Qdrant 벡터 데이터베이스
└── README.md     # 이 파일
```

## How to Work in This Area

| Package | Classification | Exact profiles | Stage 05 subject |
| --- | --- | --- | --- |
| [Neo4j](neo4j/README.md) | `OPTIONAL` | `graph` | `0033-neo4j` |
| [Qdrant](qdrant/README.md) | `HOME` | `ai`, `ai-llm`, `qdrant` | `0034-qdrant` |

1. 이 README를 폴더 인덱스로 취급하십시오. 서비스별 runtime 세부 사항은 각 서비스 leaf README에 있습니다.
2. 서비스를 변경하기 전에 [neo4j/README.md](./neo4j/README.md) 또는 [qdrant/README.md](./qdrant/README.md)를 검토하십시오.
3. 벡터 검색, 그래프 모델링, 애플리케이션 로직 결정은 이 infra 인덱스가 아니라 spec이나 애플리케이션 문서에 두십시오.
4. 특수 데이터 서비스를 추가, 이동, 제거한 뒤에는 이 인덱스와 관련 guide/policy/runbook 링크를 갱신하십시오.

## Related Documents

- [infra/04-data/README.md](../README.md)
- Stage 05 documents: `docs/05.operations/{guides,policies,runbooks}/####-<slug>.md`
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [derived Compose 이미지 투영](../../tech-stack.versions.json)은 drift를 검증합니다.
