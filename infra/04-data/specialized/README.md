# Specialized Data Services (04-data/specialized)

> 특수 목적 데이터 서비스 / Specialized Data Services

## Overview

이 디렉터리는 `hy-home.docker` 인프라의 특수 목적 데이터 서비스를 위한 구성을 포함합니다. 그래프 데이터베이스 및 벡터 데이터베이스 등 전문 데이터 스토어를 포함합니다.

## Audience

이 README의 주요 독자:

- 인프라를 배포하고 관리하는 **Operators**
- 특수 데이터 서비스를 연동하는 **Developers**
- 자동화된 운영 작업을 수행하는 **AI Agents**

## Scope

### In Scope

- Neo4j 그래프 데이터베이스 구성
- Qdrant 벡터 데이터베이스 구성
- 시크릿 마운트 및 접근 제어

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
4. After adding, moving, or removing a specialized data service, update this index and related operations links.

## Related Documents

- [infra/04-data/README.md](../README.md)
- [docs/03.specs/04-data/README.md](../../../docs/03.specs/04-data/README.md)
- [docs/05.operations/guides/04-data/](../../../docs/05.operations/guides/04-data/)
