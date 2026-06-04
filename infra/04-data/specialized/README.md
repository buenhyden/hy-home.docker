# Specialized Data Services (04-data/specialized)

> 특수 목적 데이터 서비스 / Specialized Data Services

## Overview

이 디렉터리는 `hy-home.docker` 인프라의 root-active specialized data 서비스를 위한 구성을 포함한다. 현재 루트 compose는 Neo4j graph database와 Qdrant vector database를 active include로 참조한다.

## Audience

이 README의 주요 독자:

- 인프라를 배포하고 관리하는 **Operators**
- 특수 데이터 서비스를 연동하는 **Developers**
- 자동화된 운영 작업을 수행하는 **AI Agents**

## Scope

### In Scope

- Neo4j graph database 구성과 `neo4j_password` Docker Secret 경계
- Qdrant vector database 구성과 현재 no-secret route 경계
- Traefik route, `infra_net`, persistent volume, linked operations docs

### Out of Scope

- 관계형·NoSQL·캐시 서비스 (`../relational/`, `../nosql/`, `../cache-and-kv/` 담당)
- 벡터 검색 애플리케이션 로직

## Structure

```text
specialized/
├── neo4j/        # Neo4j graph database
├── qdrant/       # Qdrant vector database
└── README.md     # This file
```

## How to Work in This Area

1. Treat this README as a folder index; service-specific runtime details belong in each service leaf README.
2. Review [neo4j/README.md](./neo4j/README.md) or [qdrant/README.md](./qdrant/README.md) before changing a service.
3. Keep vector search, graph modeling, and application logic decisions in specs or application docs, not this infra index.
4. After adding, moving, or removing a specialized data service, update this index and related guide/policy/runbook links.

## Related Documents

- [infra/04-data/README.md](../README.md)
- [docs/03.specs/04-data/README.md](../../../docs/03.specs/04-data/README.md)
- [Operations Guides](../../../docs/05.operations/guides/04-data/specialized/README.md)
- [Operations Policies](../../../docs/05.operations/policies/04-data/specialized/README.md)
- [Operations Runbooks](../../../docs/05.operations/runbooks/04-data/specialized/README.md)
