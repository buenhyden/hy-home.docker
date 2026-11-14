---
title: "PostgreSQL HA LAB"
version: "1.0.7"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2025-11-12"
---

# PostgreSQL HA LAB

## Purpose

### Service Role

이 문서는 root Compose에서 분리된 PostgreSQL HA LAB topology의 source 계약을
설명한다. normal HOME 또는 development stack의 상태·network·secret을 공유하지
않으며, LAB 학습과 정적 render에만 사용한다.

#### Audience

- 개발자: 이 실습 topology의 연결과 상태 경계를 확인합니다.
- 운영자: 격리된 LAB 렌더링과 복구 전제만 확인합니다.
- Agent: root Compose와 분리된 보조 자산 경로를 추적합니다.

#### In Scope

- Patroni/etcd/HAProxy와 exporter/init topology의 학습·render 계약
- 보조 config·init SQL: `./postgresql-ha/`

#### Out of Scope

- HOME 서비스, 관리 DB, root Compose, 운영 데이터와 credential 값
- 실제 기동, 중지, 데이터 이관·삭제, credential rotation

#### Structure

```text
labs/postgresql-ha/
├── README.md          # 서비스 README
├── docker-compose.yml # 독립 LAB entrypoint
├── promotion.yaml     # SPEC-0263 승격 manifest
├── config/            # HAProxy template
├── dashboards/        # LAB 전용 Grafana 대시보드
├── init-scripts/      # 초기화 SQL
└── scripts/           # Spilo secret-file wrapper
```

| Dashboard | UID | Source |
| --- | --- | --- |
| [`etcd-cluster.json`](./dashboards/etcd-cluster.json) | `hyhome-etcd` | monitoring-mixins etcd/etcd.json (2026-09-24) |
| [`haproxy-overview.json`](./dashboards/haproxy-overview.json) | `hyhome-haproxy` | grafana.com dashboard 12693 revision 14 (2026-04-11) |

HOME Grafana는 `infra/06-observability/grafana/dashboards/`만 provisioning하므로
이 대시보드는 HOME에 표시되지 않고, HOME Prometheus는 LAB 서비스를 수집하지
않습니다. LAB 관측을 연결하는 별도 계약이 승인되면 그 LAB의 Prometheus·Grafana가
이 파일을 읽도록 구성하며, HOME provisioning 경로로 옮기지 않습니다.

### Supported Environment

| Category | Source of truth | Boundary |
| --- | --- | --- |
| Compose | [docker-compose.yml](./docker-compose.yml) | 독립 LAB project |
| State | `${LAB_DATA_DIR:?set isolated LAB data root}` bind | HOME 상태와 미공유 |
| Secrets | `${LAB_SECRET_DIR:-../secrets/labs}` 아래 LAB 전용 reference | 값은 문서화하지 않음 |
| Networks | LAB 전용 network declarations | root network와 미공유 |

## Interfaces

### Inputs and Outputs

상태는 `${LAB_DATA_DIR}/postgresql-ha/` 아래에 bind하고 network는 `lab_pg_core_net`, `lab_pg_edge_net`, `lab_pg_obs_net`을 사용한다. 환경 변수는 아래 표와 같다.

#### Environment Variables

| Variable | Required | Description |
| --- | ---: | --- |
| `LAB_DATA_DIR` | Yes for bind-backed LAB state | isolated LAB data root; unset이면 fail fast |
| `LAB_SECRET_DIR` | No | unset이면 `../secrets/labs` reference path 사용 |
| LAB-specific port/network keys | No | Compose의 LAB default만 사용하며 root key와 공유하지 않음 |

### Security Boundary

secret은 `lab_pg_haproxy_stats_password`, `lab_pg_superuser_password`, `lab_pg_replication_password`, `lab_pg_exporter_password`, `lab_pg_service_password`를 참조하며 값은 문서에 쓰지 않는다. 호스트 노출은 `${LAB_HOST_BIND_IP}`와 `LAB_PG_*_HOST_PORT`만 사용한다.

## Development

### Local Workflow

1. `LAB_DATA_DIR`과 LAB secret reference directory를 독립 경로로 지정한다.
2. 실제 기동 없이 `LAB_DATA_DIR=/tmp/hyhome-postgresql-ha-static docker compose --env-file labs/.env.example -f labs/postgresql-ha/docker-compose.yml --profile '*' config --quiet`로 렌더링한다.
3. LAB Compose project, network, volume, port와 secret reference가 HOME 또는 management 경로와 겹치지 않는지 검토한다.
4. 기동은 `python3 scripts/operations/lab.py up postgresql-ha --purpose "<목적>" --lease <30m|4h>`로만 한다. 이 명령은 다른 LAB·HOME과의 이름·port·data 경로 충돌, 예산과 동시 LAB 수를 먼저 검사하고 `${LAB_DATA_DIR}/.ledger/postgresql-ha.json`에 정리 대상을 기록한다. 종료는 `lab.py down postgresql-ha`이며 volume과 data를 지우지 않는다. 만료 lease는 `lab.py reap`이 정지한다 (정책 `POL-0078`).

#### Available Scripts

| Command | Description |
| --- | --- |
| `LAB_DATA_DIR=/tmp/hyhome-postgresql-ha-static docker compose --env-file labs/.env.example -f labs/postgresql-ha/docker-compose.yml --profile '*' config --quiet` | LAB source render만 검증; 컨테이너를 만들지 않음 |

### Checks

Classification은 `LAB`입니다. 이 topology는 독립 Compose project, LAB 전용
network, secret reference, state path를 사용합니다. 같은 host의 여러 member는
host-level HA를 증명하지 않습니다. 정적 render 통과는 실행·인증·복구 증거가
아닙니다.

PostgreSQL init job은 비밀번호를 `psql` 인자가 아닌 `/tmp` tmpfs의
0600 psql 입력 파일로 전달하며 exporter는 파일 참조를 사용합니다.
HAProxy stats password는 설정 문자를 검증하고 `/tmp`에 렌더합니다.
실제 권한과 bootstrap 결과는 격리 실행 전까지 검증되지 않았습니다.

## Operations

### Runbook Links

- [Architecture index](../../docs/02.architecture/README.md)
- [Operations index](../../docs/05.operations/README.md)
- [15-labs runbooks](../../docs/05.operations/runbooks/15-labs/README.md): RUN-0031 postgresql-cluster, RUN-0107 lab-promotion

### Observability and Recovery

| Field | Evidence |
| --- | --- |
| Entry point | [docker-compose.yml](./docker-compose.yml) |
| Project | `hy-home-lab-postgresql-ha` |
| Services | `etcd-1`, `etcd-2`, `etcd-3`, `pg-0`, `pg-1`, `pg-2`, `pg-cluster-init`, `pg-router`, `pg-0-exporter`, `pg-1-exporter`, `pg-2-exporter` |
| State | `${LAB_DATA_DIR:?set isolated LAB data root}/postgresql-ha/...` |
| Networks | `lab_pg_core_net`, `lab_pg_edge_net`, `lab_pg_obs_net` |
| Secret refs | `lab_pg_haproxy_stats_password`, `lab_pg_superuser_password`, `lab_pg_replication_password`, `lab_pg_exporter_password`, `lab_pg_service_password` |
| Host exposure | `${LAB_HOST_BIND_IP}`와 `LAB_PG_*_HOST_PORT`만 사용 |
| Helper assets | [config](config/README.md), [init-scripts](init-scripts/README.md), [scripts](scripts/README.md), [dashboards](dashboards/README.md); LAB Compose에만 연결되며 HOME root Compose로 실행하지 않음 |
| Readiness | Compose healthcheck/one-shot dependency declarations only; runtime result is unverified |

#### Troubleshooting

- `LAB_DATA_DIR` unset 오류는 안전한 fail-fast 동작이다. HOME data path를 대입하지 않는다.
- secret file 누락은 LAB secret reference를 준비해야 하는 상태이며 값의 공개나 root secret 재사용 사유가 아니다.
- 실제 cluster 재초기화·volume 삭제·restore는 별도 승인 없이는 실행하지 않는다.
