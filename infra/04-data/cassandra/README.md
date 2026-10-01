---
title: "Apache Cassandra"
version: "1.0.4"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2025-11-12"
---

<!-- [ID:04-data:nosql:cassandra] -->
# Apache Cassandra

> 높은 처리량 워크로드를 위한 분산 wide-column NoSQL 데이터베이스입니다.

## Overview

Apache Cassandra는 고가용성과 선형 확장성을 갖춘 NoSQL 데이터베이스로 대규모 데이터 세트와 빠른 쓰기 성능이 필요한 환경에 최적화되어 있다. `hy-home.docker`에서는 제로 다운타임이 요구되는 시계열 데이터와 실시간 처리 요구사항의 저장 계층으로 쓴다.

## Audience

이 README의 주요 독자:

- **Developers**: 애플리케이션 연결 및 CQL 작업 수행
- **Operators**: 인프라 배포, 백업 및 클러스터 관리
- **AI Agents**: 시스템 구조 분석 및 자동화 작업 수행

## Scope

### In Scope

- Cassandra 단일 노드 컨테이너 구성(정확한 버전은 `docker-compose.yml` 참조)
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
| Engine     | Compose에 선언된 Cassandra 이미지       | 메인 데이터 노드             |
| Monitoring | Compose에 선언된 Cassandra exporter 이미지 | 메트릭 수집    |
| Network    | `lab_net`, `obs_net` | 내부 트래픽 격리 |
| Resource   | `template-stateful-high`             | 고성능 profile   |

## Structure

```text
cassandra/
├── README.md             # 이 파일
└── docker-compose.yml    # 주 배포 파일
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `04-data`의 Apache Cassandra 서비스 leaf; 무조건 root include, profile로 선택됨; services: `cassandra-node1`, `cassandra-exporter` |
| Config files | `docker-compose.yml` |
| Config values | 환경 키는 Compose가 소유함; node/exporter의 exact profile: `cassandra` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/04-data/cassandra/docker-compose.yml` |
| Networks | `lab_net`, `obs_net` |
| Volumes | `cassandra-exporter-volume:/opt/bitnami/cassandra-exporter/conf:rw`, `cassandra-node1-volume:/bitnami/cassandra:rw`, `cassandra-node1-volume`, `cassandra-exporter-volume` |
| Ports | `${CASSANDRA_EXPORTER_PORT:-8080}`, `${CASSANDRA_EXPORTER_LISTEN_PORT:-8081}`, `${CASSANDRA_INTER_NODE_PORT:-7000}`, `${CASSANDRA_CLIENT_PORT:-9042}` |
| Labels | `hy-home.tier` |
| Secret refs | names: `cassandra_password`; mounts: `/run/secrets/cassandra_password` |
| Healthcheck | `cassandra-node1`에 Compose healthcheck 선언됨; `cassandra-exporter`에는 선언되지 않음 |
| Operations | Guide (`docs/05.operations/guides/0025-cassandra.md`), Policy (`docs/05.operations/policies/0025-cassandra.md`), Runbook (`docs/05.operations/runbooks/0025-cassandra.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `docker compose config --quiet`부터 시작한 뒤 서비스 로그와 연결된 운영/runbook 증거를 확인함 |

## How to Work in This Area

1. **Deployment**: 루트 compose include 상태를 확인하고 `docker compose --profile cassandra config --quiet`로 렌더링한다.
2. **Configuration**: 환경 변수, Docker Secret, 볼륨 경로는 `docker-compose.yml`을 기준으로 한다.
3. **Verification**: `docker exec cassandra-node1 nodetool status` 명령으로 서비스 상태를 확인한다.
4. **Documentation**: 상세 운영 지침 및 복구 절차는 상위 `docs/05.operations` 경로의 산출물을 확인한다.

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose --profile cassandra config --quiet` | Cassandra 선택 스택 렌더링 |
| `docker exec cassandra-node1 nodetool status` | Cassandra 노드 상태 확인 |
| `docker exec cassandra-node1 sh -lc 'cqlsh -u "$CASSANDRA_USER" -p "$(cat /run/secrets/cassandra_password)" -e "SELECT cluster_name FROM system.local;"'` | Secret mount 기반 read-only CQL 확인 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `DEFAULT_DATA_DIR` | Yes | 호스트 시스템의 데이터 저장 루트 경로 |
| `CASSANDRA_USERNAME` | Yes | 관리자 계정 이름 |
| `CASSANDRA_CLIENT_PORT` | No | CQL 접속 포트 (Default: 9042) |
| `CASSANDRA_EXPORTER_PORT` | No | exporter metrics 포트 (Default: 8080) |
| `CASSANDRA_EXPORTER_LISTEN_PORT` | No | exporter listen 포트 (Default: 8081) |

## Validation

Classification은 `LAB`입니다. 단일 데이터 노드이며 quorum이나 HA cluster가
아닙니다. 복구는 tagged snapshot을 schema, keyspace/replication,
topology/token, 버전, SSTable, checksum과 묶은 뒤 `sstableloader`나
`nodetool refresh`로 비어 있는 호환 노드에 복원합니다. 소유 artifact는
`GDE-0025`, `POL-0025`, `RUN-0025`입니다.

- Cassandra에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- Cassandra 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.

## Troubleshooting

- `docker compose config --quiet`로 Cassandra 네트워크, volume, secret 참조가 정상 렌더링되는지 먼저 확인합니다.
- cluster나 persistence 설정을 변경하기 전에 Cassandra 로그와 `nodetool` 상태를 확인합니다.

## Related Documents

- **Guide**: Cassandra Guide (`docs/05.operations/guides/0025-cassandra.md`)
- **Policy**: Cassandra Operation (`docs/05.operations/policies/0025-cassandra.md`)
- **Runbook**: Cassandra Runbook (`docs/05.operations/runbooks/0025-cassandra.md`)
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [derived Compose 이미지 투영](../../tech-stack.versions.json)으로 drift를 검증합니다.
