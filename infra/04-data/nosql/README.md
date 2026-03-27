# NoSQL Infrastructure (04-data/nosql)

> Distributed, Document-oriented, and Wide-column NoSQL databases.

## Overview

이 디렉터리는 `hy-home.docker` 에코시스템에서 사용하는 NoSQL 데이터베이스 인프라 구성을 포함한다. 대규모 데이터 처리, 고가용성 문서 저장, 그리고 전역 분산 아키텍처를 지원하기 위한 다양한 NoSQL 엔진들을 관리한다.

## Audience

이 README의 주요 독자:

- **Developers**: NoSQL 엔진 선택 및 데이터 모델링 참조
- **Operators**: 클러스터 배포, 배정 및 리소스 관리
- **Documentation Writers**: 가이드 및 운영 문서 동기화
- **AI Agents**: 인프라 구조 분석 및 자동화 작업 수행

## Scope

### In Scope

- Apache Cassandra (Wide-column store)
- CouchDB (Document store with Sync)
- MongoDB (Document store with Replica Set)
- 각 엔진별 백업, 모니터링 및 인증 구성

### Out of Scope

- 관계형 데이터베이스 (04-data/relational 참조)
- 캐시 및 KV 저장소 (04-data/cache-and-kv 참조)
- 데이터 레이크 구성 (04-data/lake-and-object 참조)

## Structure

```text
nosql/
├── cassandra/            # Apache Cassandra configuration
├── couchdb/              # CouchDB Cluster configuration
├── mongodb/              # MongoDB Replica Set configuration
└── README.md             # This file
```

## How to Work in This Area

1. **Selection**: 요구사항(분산 성능, 동기화, 범용성)에 맞는 적절한 엔진을 선택한다.
2. **Deployment**: 각 서브디렉터리의 `docker-compose.yml`을 사용하여 서비스를 기동한다.
3. **Standards**: 모든 엔진은 `common-optimizations.yml`을 확장하며 Prometheus 익스포터를 포함해야 한다.
4. **Documentation**: 변경 사항 발생 시 상위 `docs/` 경로의 관련 가이드와 런북을 업데이트한다.

## Related References

- **Architecture**: [Data Tier ARD](../../docs/02.ard/0004-data-architecture.md)
- **Guides**: [NoSQL Guides](../../docs/07.guides/04-data/nosql/README.md)
- **Operations**: [NoSQL Operations](../../docs/08.operations/04-data/nosql/README.md)
- **Source**: [Data Tier Root](../README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
