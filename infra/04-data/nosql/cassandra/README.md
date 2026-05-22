<!-- [ID:04-data:nosql:cassandra] -->
# Apache Cassandra

> Distributed wide-column NoSQL database for high-throughput workloads.

## Overview

Apache Cassandra는 고가용성과 선형 확장성을 제공하는 NoSQL 데이터베이스로, 대규모 데이터 세트와 빠른 쓰기 성능이 필요한 환경에 최적화되어 있다. `hy-home.docker`에서는 제로 다운타임이 요구되는 시계열 데이터 및 실시간 처리 요구사항을 위한 저장 계층으로 사용된다.

## Audience

이 README의 주요 독자:

- **Developers**: 애플리케이션 연결 및 CQL 작업 수행
- **Operators**: 인프라 배포, 백업 및 클러스터 관리
- **AI Agents**: 시스템 구조 분석 및 자동화 작업 수행

## Scope

### In Scope

- Cassandra 5.0 단일 노드 컨테이너 구성
- JMX 기반 Prometheus 메트릭 엑스포터 (`cassandra-exporter`)
- 영속성 데이터 볼륨 관리 (`${DEFAULT_DATA_DIR}/cassandra/node1`)
- Docker Secrets 기반 보안 설정 (`cassandra_password`)

### Out of Scope

- 다중 노드 클러스터링 (현재 단일 노드 기준)
- 애플리케이션 레벨의 데이터 모델링 상세 (Docs Tier 참조)
- 외부 네트워크 직접 노출 관리

## Tech Stack

| Category   | Technology                           | Notes                      |
| :--------- | :----------------------------------- | :------------------------- |
| Engine     | `cassandra:5.0.6`                    | Main Data Node             |
| Monitoring | `bitnami/cassandra-exporter:2.3.11` | Metrics Collection         |
| Network    | `infra_net`                          | Internal Traffic Isolation |
| Resource   | `template-stateful-high`             | High Performance Profile   |

## Structure

```text
cassandra/
├── README.md             # This file
└── docker-compose.yml    # Main deployment file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Apache Cassandra service leaf in `04-data`; services: `cassandra-exporter`, `cassandra-node1`; root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/nosql/cassandra/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `CASSANDRA_SEEDS`, `CASSANDRA_PASSWORD_SEEDER`, `CASSANDRA_USER`, `CASSANDRA_PASSWORD_FILE`, `MAX_HEAP_SIZE`, `HEAP_NEWSIZE`; profiles: `data`, `obs` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/nosql/cassandra/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `cassandra-exporter-volume:/opt/bitnami/cassandra-exporter/conf:rw`, `cassandra-node1-volume:/bitnami/cassandra:rw`, `cassandra-node1-volume`, `cassandra-exporter-volume` |
| Ports | `${CASSANDRA_EXPORTER_PORT:-8080}`, `${CASSANDRA_EXPORTER_LISTEN_PORT:-8081}`, `${CASSANDRA_INTER_NODE_PORT:-7000}`, `${CASSANDRA_CLIENT_PORT:-9042}` |
| Labels | `hy-home.tier` |
| Secret refs | names: `cassandra_password`; mounts: `/run/secrets/cassandra_password` |
| Healthcheck | Compose healthcheck declared for `cassandra-node1`; not declared for `cassandra-exporter` |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/nosql/cassandra.md), [Policy](../../../../docs/05.operations/policies/04-data/nosql/cassandra.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/nosql/cassandra.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. **Deployment**: `docker compose up -d`를 사용하여 스택을 기동한다.
2. **Configuration**: 환경 변수 및 볼륨 경로는 `docker-compose.yml`을 참조한다.
3. **Verification**: `docker exec -it cassandra-node1 nodetool status` 명령으로 서비스 상태를 확인한다.
4. **Documentation**: 상세 운영 지침 및 복구 절차는 상위 `docs/` 경로의 산출물을 확인한다.

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose up -d` | Cassandra 스택 배포 |
| `docker exec -it cassandra-node1 cqlsh -u ${USER} -p ${PASS}` | CQL 셸 접속 |
| `docker exec -it cassandra-node1 nodetool <cmd>` | 운영 도구(Repair, Snapshot 등) 실행 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `DEFAULT_DATA_DIR` | Yes | 호스트 시스템의 데이터 저장 루트 경로 |
| `CASSANDRA_USERNAME` | Yes | 관리자 계정 이름 |
| `CASSANDRA_CLIENT_PORT` | No | CQL 접속 포트 (Default: 9042) |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect Cassandra.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking Cassandra documentation ready.

## Troubleshooting

- Start with `docker compose config` to confirm Cassandra network, volume, and secret references render.
- Check Cassandra logs and `nodetool` status before changing cluster or persistence settings.

## Related Documents

- **Guide**: [Cassandra Guide](../../../../docs/05.operations/guides/04-data/nosql/cassandra.md)
- **Operation**: [Cassandra Operation](../../../../docs/05.operations/guides/04-data/nosql/cassandra.md)
- **Runbook**: [Cassandra Runbook](../../../../docs/05.operations/guides/04-data/nosql/cassandra.md)

---
Copyright (c) 2026. Licensed under the MIT License.
