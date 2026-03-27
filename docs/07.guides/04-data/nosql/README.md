# NoSQL Data Tier Guides (04-data/nosql)

> NoSQL 데이터베이스(Cassandra 등) 기술 가이드.

## Resource Catalog

-   [Apache Cassandra](./cassandra.md): Wide-column distributed store.
-   [MongoDB](./mongodb.md): Document-based replica set cluster.
-   [README.md](./README.md): This file

## Overview

이 디렉터리는 `hy-home.docker` NoSQL 데이터 계층의 각 엔진별 사용 가이드와 시스템 아키텍처 설명을 포함한다. 개발자와 운영자가 각 데이터베이스의 특성을 이해하고 효율적으로 활용할 수 있도록 돕는다.

## Audience

이 README의 주요 독자:

- **Developers**: 데이터 모델링 및 쿼리 최적화 가이드 참조
- **Operators**: 시스템 구성 이해 및 성능 튜닝 참조
- **AI Agents**: 시스템 도메인 지식 습득 및 기술 지원 수행

## Scope

### In Scope

- Apache Cassandra System Guide
- CouchDB Cluster Guide
- MongoDB Replica Set Guide
- NoSQL 엔진별 연결 패턴 및 베스트 프랙티스

### Out of Scope

- 운영 정책 (08.operations/04-data/nosql 참조)
- 긴급 복구 런북 (09.runbooks/04-data/nosql 참조)
- 인프라 배포 코드 (infra/04-data/nosql 참조)

## Structure

```text
nosql/
├── README.md             # This file
├── cassandra.md          # Cassandra System Guide
├── couchdb.md            # CouchDB Cluster Guide
└── mongodb.md            # MongoDB Replica Set Guide
```

## How to Work in This Area

1.  **Templates**: 새 가이드 추가 시 `docs/99.templates/guide.template.md`를 사용한다.
2.  **SSoT**: 인프라 변경 사항이 가이드에 즉시 반영되도록 유지한다.
3.  **Traceability**: 각 가이드는 관련 `Spec`, `Operation`, `Runbook` 문서와 연결되어야 한다.

## Related References

- **Infrastructure**: [NoSQL Infrastructure](../../../../infra/04-data/nosql/README.md)
- **Operations**: [NoSQL Operations](../../../08.operations/04-data/nosql/README.md)
- **Runbooks**: [NoSQL Runbooks](../../../09.runbooks/04-data/nosql/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
