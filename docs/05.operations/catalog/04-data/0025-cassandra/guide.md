---
title: "Cassandra Usage Guide"
version: "1.0.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0025"
parent_ids:
- "POL-0025"
implementation_services:
  infra/04-data/nosql/cassandra/docker-compose.yml:
  - 'cassandra-exporter'
  - 'cassandra-node1'
created: "2026-05-10"
---

# Cassandra Usage Guide

## Usage

### Overview

이 문서는 [Cassandra Compose 구현](../../../../../infra/04-data/nosql/cassandra/docker-compose.yml)의 단일 `cassandra-node1`과 `cassandra-exporter`를 설명한다. 두 서비스는 모두 정확히 `cassandra` profile에 속하며 `lab_net`에서 동작한다. frozen service classification은 `LAB`이고, 한 호스트의 단일 데이터 노드이므로 quorum이나 host-level HA를 제공하지 않는다.

### Current implementation

| Field | Repository-specific decision |
| --- | --- |
| Consumer and data rationale | No confirmed HOME consumer; LAB wide-column evaluation for high-write/keyspace workloads. |
| Source / updater | [Compose](../../../../../infra/04-data/nosql/cassandra/docker-compose.yml) owns image sources; dependency automation may propose changes, but operator review owns upgrades. |
| Services / profile | `cassandra-node1`, `cassandra-exporter`; exact `cassandra`. |
| Flow / dependency | CQL clients use the node on `lab_net`; exporter starts after node health. |
| Exposure / persistence | Database is internal; exporter ports are Compose-declared; `${DEFAULT_DATA_DIR}/cassandra/node1` mounts at `/bitnami/cassandra`. |
| Environment / secrets | `CASSANDRA_USERNAME` and Compose-owned tuning keys; `cassandra_password` at `/run/secrets`. |
| Health / resources | `nodetool status` and CQL health; node `template-stateful-high`, exporter `template-infra-low`. |
| Security | Secret-backed password; no claim of network encryption or multi-node authorization beyond source configuration. |
| Backup / upgrade | Tagged SSTable snapshot plus schema/topology inventory; isolated compatible restore before any version change or removal. |
| License / edition | Apache Cassandra source is Apache-2.0; this repository runs the source-declared single-node distribution with no commercial feature claim. |

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

Cassandra를 wide-column 저장소로 사용할 때 현재 repository의 서비스명, secret mount, 볼륨 경계, 메트릭 exporter 경로를 오해하지 않도록 한다.

### Prerequisites

- 루트 [docker-compose.yml](../../../../../docker-compose.yml)는 Cassandra 파일을 include하며, 두 서비스의 정확한 profile은 `cassandra`다.
- `DEFAULT_DATA_DIR`, `CASSANDRA_USERNAME`, `cassandra_password` secret 파일이 로컬 환경에서 준비되어 있어야 한다.
- 런타임 점검은 container 내부 secret 파일을 읽는 방식으로 수행하고, secret 값을 문서나 로그에 남기지 않는다.

### Step-by-step Instructions

1. 서비스 구성을 렌더링한다.

   ```bash
   docker compose --profile cassandra config --quiet
   ```

2. Cassandra 서비스가 활성화된 런타임에서 컨테이너 상태를 확인한다.

   ```bash
   docker compose ps cassandra-node1 cassandra-exporter
   ```

3. 노드 상태는 `nodetool`로 확인한다.

   ```bash
   docker exec cassandra-node1 nodetool status
   ```

4. CQL 점검은 container 내부 secret mount를 사용한다.

   ```bash
   docker exec cassandra-node1 sh -lc 'cqlsh -u "$CASSANDRA_USER" -p "$(cat /run/secrets/cassandra_password)" -e "SELECT cluster_name, release_version FROM system.local;"'
   ```

5. 메트릭 연동은 `cassandra-exporter`가 노드 health 이후 시작되는지 확인한다. exporter 포트는 compose의 `${CASSANDRA_EXPORTER_PORT:-8080}` 및 `${CASSANDRA_EXPORTER_LISTEN_PORT:-8081}` 기준이다.

### Common Pitfalls

- 현재 구현은 단일 노드다. image tag는 Compose declaration이 소유하며, 다중 노드 quorum, repair 자동화, zero-downtime node rotation을 구현된 기능처럼 문서화하지 않는다.
- 데이터 볼륨은 `${DEFAULT_DATA_DIR}/cassandra/node1`에 bind되고 container에는 `/bitnami/cassandra`로 mount된다. `/var/lib/cassandra` 기준 설명은 현재 compose와 맞지 않는다.
- 평문 password 환경 변수를 전제로 한 명령을 사용하지 않는다. compose는 `/run/secrets/cassandra_password`를 사용한다.
- restore 전에 Cassandra release/schema, keyspace 목록, replication 설정, snapshot tag, token/topology를 기록한다. snapshot은 schema와 모든 table SSTable을 함께 보존하고 빈 격리 target에서만 검증한다.

## Common Checks

- `docker compose --profile cassandra config --quiet`
- `docker exec cassandra-node1 nodetool status`에서 `cassandra-node1` 상태가 `UN`인지 확인한다.
- `docker compose ps cassandra-node1 cassandra-exporter`에서 Cassandra가 healthy이고 exporter가 실행 중인지 확인한다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [Cassandra runbook](runbook.md)을 따른다.

## Traceability

- Declared parent: [Cassandra Operations Policy](policy.md) (`POL-0025`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Policy](policy.md) (`POL-0025`), [Runbook](runbook.md) (`RUN-0025`)

## Related Documents

- [Cassandra backup and restore](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/backups.html)
- [Cassandra security](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/security.html)
- [Apache Cassandra source and license](https://github.com/apache/cassandra)

- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/nosql/cassandra/README.md)
- [Compose implementation: infra/04-data/nosql/cassandra/docker-compose.yml](../../../../../infra/04-data/nosql/cassandra/docker-compose.yml)
