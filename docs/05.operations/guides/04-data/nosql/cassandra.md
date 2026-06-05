---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/nosql/cassandra.md -->

# Cassandra Usage Guide

## Usage

### Overview

이 문서는 `infra/04-data/nosql/cassandra/docker-compose.yml`에 정의된 Cassandra 단일 노드와 `cassandra-exporter`를 기준으로 사용 맥락, 접속 방식, 일반 점검 방법을 설명한다. 현재 루트 compose에서는 Cassandra include가 주석 처리된 선택 서비스이며, 활성화 시 `data` 프로파일의 `cassandra-node1`과 `data`/`obs` 프로파일의 `cassandra-exporter`가 `infra_net`에서 동작한다.

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

Cassandra를 wide-column 저장소로 사용할 때 현재 repository의 서비스명, secret mount, 볼륨 경계, 메트릭 exporter 경로를 오해하지 않도록 한다.

### Prerequisites

- `infra/04-data/nosql/cassandra/docker-compose.yml`와 루트 [docker-compose.yml](../../../../../docker-compose.yml)의 선택 include 상태를 확인한다.
- `DEFAULT_DATA_DIR`, `CASSANDRA_USERNAME`, `cassandra_password` secret 파일이 로컬 환경에서 준비되어 있어야 한다.
- 런타임 점검은 container 내부 secret 파일을 읽는 방식으로 수행하고, secret 값을 문서나 로그에 남기지 않는다.

### Step-by-step Instructions

1. 서비스 구성을 렌더링한다.

   ```bash
   docker compose -f docker-compose.yml -f infra/04-data/nosql/cassandra/docker-compose.yml --profile data config
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

- 현재 구현은 `cassandra:5.0.8` 단일 노드다. 다중 노드 quorum, repair 자동화, zero-downtime node rotation을 구현된 기능처럼 문서화하지 않는다.
- 데이터 볼륨은 `${DEFAULT_DATA_DIR}/cassandra/node1`에 bind되고 container에는 `/bitnami/cassandra`로 mount된다. `/var/lib/cassandra` 기준 설명은 현재 compose와 맞지 않는다.
- 평문 password 환경 변수를 전제로 한 명령을 사용하지 않는다. compose는 `/run/secrets/cassandra_password`를 사용한다.

## Common Checks

- `docker compose -f docker-compose.yml -f infra/04-data/nosql/cassandra/docker-compose.yml --profile data config`
- `docker exec cassandra-node1 nodetool status`에서 `cassandra-node1` 상태가 `UN`인지 확인한다.
- `docker compose ps cassandra-node1 cassandra-exporter`에서 Cassandra가 healthy이고 exporter가 실행 중인지 확인한다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [Cassandra runbook](../../../runbooks/04-data/nosql/cassandra.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/nosql/cassandra.md)
- [Recovery runbook](../../../runbooks/04-data/nosql/cassandra.md)
- [Infra README](../../../../../infra/04-data/nosql/cassandra/README.md)
