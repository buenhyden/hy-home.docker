---
title: "NoSQL Infrastructure (04-data/nosql)"
version: "1.0.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2026-03-27"
---

# NoSQL Infrastructure (04-data/nosql)

> Distributed, Document-oriented, and Wide-column NoSQL databases.

## Overview

이 디렉터리는 `hy-home.docker`의 `LAB` NoSQL 구성을 포함한다. 루트 compose는 세 leaf를 include하며 exact profiles `cassandra`, `couchdb`, `mongodb`가 각각의 전체 service set을 선택한다. 같은 host의 복수 member는 host-level HA가 아니다.

## Audience

이 README의 주요 독자:

- **Developers**: NoSQL 엔진 선택 및 데이터 모델링 참조
- **Operators**: 클러스터 배포, 배정 및 리소스 관리
- **Documentation Writers**: 가이드 및 운영 문서 동기화
- **AI Agents**: 인프라 구조 분석 및 자동화 작업 수행

## Scope

### In Scope

- Apache Cassandra 단일 노드와 exporter
- CouchDB 3노드 cluster-init 구성
- MongoDB replica set, Mongo Express, exporter 구성
- 각 엔진별 Docker Secret, 볼륨, network 소속, operations 문서 연결

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

| Package | Classification | Exact profile | Stage 05 subject |
| --- | --- | --- | --- |
| [Cassandra](cassandra/README.md) | `LAB` | `cassandra` | `0025-cassandra` |
| [CouchDB](couchdb/README.md) | `LAB` | `couchdb` | `0026-couchdb` |
| [MongoDB](mongodb/README.md) | `LAB` | `mongodb` | `0027-mongodb` |

1. **Selection**: 요구사항(단일 노드 wide-column, 문서 sync cluster, replica set)에 맞는 엔진을 선택한다.
2. **Deployment**: 루트 compose include 상태를 확인한 뒤 각 서브디렉터리의 `docker-compose.yml`을 함께 렌더링한다.
3. **Standards**: 각 엔진은 `common-optimizations.yml`의 source-declared template을 확장하며 exporter도 해당 engine의 exact profile에 속한다.
4. **Documentation**: 변경 사항 발생 시 하위 README와 상위 `docs/05.operations/catalog/04-data/` 문서를 함께 업데이트한다.

## Related Documents

- **Architecture**: Data Tier Architecture Description (`docs/02.architecture/descriptions/0004-data-architecture.md`)
- **Guides**: NoSQL Guides (`docs/05.operations/catalog/04-data/README.md`)
- **Policies**: NoSQL Policies (`docs/05.operations/catalog/04-data/README.md`)
- Stage 05 subjects: `docs/05.operations/catalog/04-data/<subject>/`
- **Source**: [Data Tier Root](../README.md)
- [Documentation index](../../../docs/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
