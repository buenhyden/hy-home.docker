<!-- [ID:04-data:cassandra] -->
# Apache Cassandra

> Distributed wide-column NoSQL database for high-throughput workloads.

## Overview

Apache Cassandra is a highly available, linearly scalable NoSQL database designed for large-scale data sets and fast write performance. In `hy-home.docker`, it serves as the storage layer for time-series data and real-time processing requirements that demand zero downtime.

## Audience

이 README의 주요 독자:

- **Developers**: 애플리케이션 연결 및 CQL 작업 수행
- **Operators**: 인프라 배포, 백업 및 클러스터 관리
- **Documentation Writers**: 기술 가이드 및 런북 유지보수
- **AI Agents**: 시스템 구조 분석 및 자동화 작업 수행

## Scope

### In Scope

- Cassandra 5.0 단일 노드 컨테이너 구성
- JMX 기반 Prometheus 메트릭 엑스포터
- 영속성 데이터 볼륨 관리(`${DEFAULT_DATA_DIR}/cassandra/node1`)
- Docker Secrets 기반 보안 설정

### Out of Scope

- 다중 노드 클러스터링(현재 단일 노드 기준)
- 애플리케이션 레벨의 데이터 모델링 상세(Docs Tier 참조)
- 외부 네트워크 직접 노출 관리

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Engine | `cassandra:5.0.6` | Main Data Node |
| Monitoring | `bitnami/cassandra-exporter:2.3.11` | Metrics Collection |
| Network | `infra_net` | Internal Traffic Isolation |
| Resource | `template-stateful-high` | High Performance Profile |

## Structure

```text
cassandra/
├── README.md             # This file
└── docker-compose.yml    # Main deployment file
```

## How to Work in This Area

1. **Deployment**: `docker compose up -d`를 사용하여 스택을 기동합니다.
2. **Configuration**: 환경 변수 및 볼륨 경로는 `docker-compose.yml`을 참조합니다.
3. **Verification**: `docker exec -it cassandra-node1 nodetool status` 명령으로 서비스 상태를 확인합니다.
4. **Documentation**: 상세 운영 지침 및 복구 절차는 상위 `docs/` 경로의 산출물을 확인합니다.

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose up -d` | Cassandra 스택 배포 |
| `docker exec -it cassandra-node1 cqlsh -u ${USER} -p ${PASS}` | CQL 셸 접속 |
| `docker exec -it cassandra-node1 nodetool <cmd>` | 운영 도구(Repair, Snapshot 등) 실행 |

## Configuration

### Environment Variables (Selected)

| Variable | Required | Description |
| :--- | :--- | :--- |
| `DEFAULT_DATA_DIR` | Yes | 호스트 시스템의 데이터 저장 루트 경로 |
| `CASSANDRA_USERNAME` | Yes | 관리자 계정 이름 |
| `CASSANDRA_CLIENT_PORT` | No | CQL 접속 포트 (Default: 9042) |

## Related References

- **Guide**: [Cassandra System Guide](../../../docs/07.guides/04-data/nosql/cassandra.md)
- **Operation**: [Cassandra Operations Policy](../../../docs/08.operations/04-data/nosql/cassandra.md)
- **Runbook**: [Cassandra Recovery Runbook](../../../docs/09.runbooks/04-data/nosql/cassandra.md)
- **Source**: [Infrastructure Source](../../../infra/04-data/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
