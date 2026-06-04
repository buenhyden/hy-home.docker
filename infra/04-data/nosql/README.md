# NoSQL Infrastructure (04-data/nosql)

> Distributed, Document-oriented, and Wide-column NoSQL databases.

## Overview

이 디렉터리는 `hy-home.docker` 에코시스템에서 선택적으로 사용할 수 있는 NoSQL 데이터베이스 인프라 구성을 포함한다. 현재 루트 compose에서는 Cassandra, CouchDB, MongoDB include가 주석 처리되어 있으며, 필요 시 각 서비스 compose를 명시적으로 포함해 실행한다.

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
- 각 엔진별 Docker Secret, 볼륨, `infra_net`, operations 문서 연결

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

1. **Selection**: 요구사항(단일 노드 wide-column, 문서 sync cluster, replica set)에 맞는 엔진을 선택한다.
2. **Deployment**: 루트 compose include 상태를 확인한 뒤 각 서브디렉터리의 `docker-compose.yml`을 함께 렌더링한다.
3. **Standards**: 각 엔진은 `common-optimizations.yml`을 확장하고, exporter가 선언된 Cassandra/MongoDB는 `obs` 프로파일 경계를 유지한다.
4. **Documentation**: 변경 사항 발생 시 하위 README와 상위 `docs/05.operations/{guides,policies,runbooks}/04-data/nosql/` 문서를 함께 업데이트한다.

## Related Documents

- **Architecture**: [Data Tier ARD](../../../docs/02.architecture/requirements/0004-data-architecture.md)
- **Guides**: [NoSQL Guides](../../../docs/05.operations/guides/04-data/nosql/README.md)
- **Policies**: [NoSQL Policies](../../../docs/05.operations/policies/04-data/nosql/README.md)
- **Runbooks**: [NoSQL Runbooks](../../../docs/05.operations/runbooks/04-data/nosql/README.md)
- **Source**: [Data Tier Root](../README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
