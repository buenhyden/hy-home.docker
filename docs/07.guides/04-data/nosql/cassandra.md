<!-- Target: docs/07.guides/04-data/nosql/cassandra.md -->

# Apache Cassandra System Guide

> Distributed wide-column NoSQL database for high-throughput, highly available workloads.

---

## Overview (KR)

이 문서는 Apache Cassandra 5.0의 시스템 아키텍처, 데이터 모델링 기본 원리 및 `hy-home.docker` 환경에서의 사용 가이드를 제공한다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- Operator
- Agent-tuner

## Purpose

애플리케이션 개발자와 운영자가 Cassandra의 분산 구조를 이해하고, 효율적인 데이터 스토리지 계층으로 활용할 수 있도록 돕는다.

## Prerequisites

- `infra/04-data/nosql/cassandra` 배포 환경 및 Docker 기반 지식
- CQL(Cassandra Query Language) 기본 문법 이해
- `${DEFAULT_DATA_DIR}/cassandra` 볼륨 접근 권한

## Step-by-step Instructions

### 1. Cassandra 서비스 상태 확인

Cassandra가 정상적으로 실행 중인지 `nodetool`을 통해 확인한다.

```bash
docker exec -it cassandra-node1 nodetool status
```

- `UN` (Up/Normal): 정상 상태
- `DN` (Down/Normal): 서비스는 살아있으나 노드 통신 불가

### 2. CQLSH를 통한 데이터베이스 접속

직접 쿼리를 수행하기 위해 `cqlsh` 인터페이스를 사용한다.

```bash
docker exec -it cassandra-node1 cqlsh -u ${CASSANDRA_USER} -p ${CASSANDRA_PASSWORD}
```

### 3. 데이터 모델링 가이드

Cassandra는 쿼리 기반 모델링(Query-driven modeling)이 권장된다.

- **Keyspace**: 데이터베이스 단위의 스키마 정의 (Replication Strategy 포함)
- **Table**: 기본 키(Partition Key + Clustering Column)를 신중히 설계하여 데이터 분산을 최적화한다.
- **SAI (Storage Attached Indexing)**: Cassandra 5.0의 신기능으로, 여러 컬럼에 대해 효율적인 인덱싱을 제공한다.

### 4. 메트릭 모니터링 연동

Prometheus는 `cassandra-exporter` (포트 8080/8081)를 통해 메트릭을 수집한다. Grafana에서 `Cassandra Overview` 대시보드를 통해 Read/Write Latency, Compaction 상태 등을 모니터링할 수 있다.

## Common Pitfalls

- **Single Node Limit**: 현재 단일 노드 구성이므로 클러스터 수준의 가용성(`QUORUM` 등) 테스트는 제한적이다.
- **Heavy Scan Queries**: `ALLOW FILTERING`을 사용하는 쿼리는 대규모 데이터 셋에서 성능 장애를 유발하므로 실무 환경에서는 지양한다.
- **Tombstone Accumulation**: 대량의 `DELETE` 작업은 데이터 조회 시 성능 저하를 일으키므로 TTL 기반의 자동 삭제를 권장한다.

## Related Documents

- **Spec**: [04-data Spec](../../../docs/04.specs/04-data/spec.md)
- **Operation**: [Cassandra Operations Policy](../../../docs/08.operations/04-data/nosql/cassandra.md)
- **Runbook**: [Cassandra Recovery Runbook](../../../docs/09.runbooks/04-data/nosql/cassandra.md)
