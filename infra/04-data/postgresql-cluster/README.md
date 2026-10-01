---
title: "postgresql-cluster"
version: "1.0.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2026-03-27"
---

# postgresql-cluster

> Patroni와 etcd를 이용한 고가용성(HA) PostgreSQL 관계형 데이터베이스 클러스터입니다(정확한 버전은 `docker-compose.yml` 참조).

---

## Overview

`postgresql-cluster`는 지속성과 가용성이 핵심인 서비스들을 위한 관계형 데이터베이스 인프라입니다. Spilo(Zalando) 이미지를 기반으로 Patroni가 클러스터 생명주기를 관리하며 etcd를 DCS(Distributed Configuration Store)로 사용하여 리더 선출 및 장애 복구를 자동화합니다. HAProxy(`pg-router`)는 애플리케이션에 단일 접속 지점과 읽기/쓰기 분산 기능을 제공합니다.

## Audience

이 README의 주요 독자:

- 데이터베이스 연결이 필요한 **Developers**
- 클러스터 상태 및 백업을 관리하는 **Operators**
- 인프라 무결성을 확인하는 **AI Agents**

## Scope

### In Scope

- 3노드 PostgreSQL 하드웨어/소프트웨어 스택 구성
- etcd 기반의 분산 설정 및 리더 락(Leader Lock) 관리
- HAProxy 기반의 읽기(15433)/쓰기(15432) 가용성 라우팅
- Prometheus 엑스포터를 통한 노드 및 클러스터 메트릭 노출

### Out of Scope

- 개별 서비스 애플리케이션의 데이터 스키마(Schema) 정의
- 외부망 직접 노출 (반드시 선언된 내부 network 사용)
- 클러스터 외부 수동 백업 저장소 관리

## Structure

```text
postgresql-cluster/
├── config/
│   └── haproxy.cfg.tpl       # HAProxy 라우팅 설정 template
├── init-scripts/
│   └── init_users_dbs.sql    # 초기 데이터베이스 및 사용자 생성 스크립트
├── scripts/
│   └── spilo-entrypoint-with-secrets.sh # Secret-aware Spilo entrypoint
├── docker-compose.yml        # 클러스터 오케스트레이션 정의
└── README.md                 # 이 파일
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `04-data`의 postgresql-cluster 서비스 leaf; services: `etcd-1`, `etcd-2`, `etcd-3`, `pg-router`, `pg-cluster-init`, `pg-0` 등 5개 더; [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/04-data/postgresql-cluster/docker-compose.yml` |
| Config files | `docker-compose.yml`, `config --quiet`, `config/haproxy.cfg.tpl` |
| Config values | env keys: `POSTGRES_WRITE_PORT`, `POSTGRES_READ_PORT`, `POSTGRES_USER`, `POSTGRES_DB`, `PATRONI_EXPORTER_USERNAME`, `SERVICE_POSTGRES_USERNAME`, `SERVICE_POSTGRES_DB` 등 10개 더; profiles: `postgres-ha` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/04-data/postgresql-cluster/docker-compose.yml` |
| Networks | `edge_net`, `lab_net`, `obs_net` |
| Volumes | `etcd1-data:/etcd-data:rw`, `etcd2-data:/etcd-data:rw`, `etcd3-data:/etcd-data:rw`, `./config/haproxy.cfg.tpl:/tmp/haproxy.cfg.tpl:ro`, `./init-scripts/init_users_dbs.sql:/work/init_users_dbs.sql:ro`, `pg0-data:/home/postgres/pgdata:rw`, `./scripts/spilo-entrypoint-with-secrets.sh:/usr/local/bin/spilo-entrypoint-with-secrets.sh:ro`, `pg1-data:/home/postgres/pgdata:rw` 등 7개 더 |
| Ports | `${POSTGRES_WRITE_HOST_PORT:-15432}:${POSTGRES_WRITE_PORT:-15432}`, `${POSTGRES_READ_HOST_PORT:-15433}:${POSTGRES_READ_PORT:-15433}`, `${HAPROXY_METRICS_PORT:-8404}`, `${POSTGRES_EXPORTER_PORT:-9187}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.haproxy-stats.rule`, `traefik.http.routers.haproxy-stats.entrypoints`, `traefik.http.routers.haproxy-stats.tls`, `traefik.http.services.haproxy-stats.loadbalancer.server.port`, `traefik.http.routers.haproxy-stats.middlewares` |
| Secret refs | names: `pg_haproxy_stats_password`, `patroni_superuser_password`, `patroni_exporter_password`, `service_postgres_password`, `patroni_replication_password`; mounts: `/run/secrets/pg_haproxy_stats_password`, `/run/secrets/patroni_superuser_password`, `/run/secrets/patroni_exporter_password`, `/run/secrets/service_postgres_password`, `/run/secrets/patroni_replication_password` |
| Healthcheck | `etcd-1`, `etcd-2`, `etcd-3`, `pg-router`, `pg-0` 등 5개 더에 Compose healthcheck 선언됨; `pg-cluster-init`에는 선언되지 않음 |
| Operations | Guide (`docs/05.operations/guides/0031-postgresql-cluster.md`), Policy (`docs/05.operations/policies/0031-postgresql-cluster.md`), Runbook (`docs/05.operations/runbooks/0031-postgresql-cluster.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `docker compose config --quiet`부터 시작한 뒤 서비스 로그와 연결된 운영/runbook 증거를 확인함 |

## How to Work in This Area

1. 클러스터 아키텍처 및 연결 방법은 Technical Guide (`docs/05.operations/guides/0031-postgresql-cluster.md`)를 먼저 확인합니다.
2. 루트 compose include 상태를 확인하고 `docker compose --profile postgres-ha config --quiet`로 렌더링합니다.
3. 운영 변경 사항은 반드시 Operations Policy (`docs/05.operations/policies/0031-postgresql-cluster.md`) 준수 여부를 확인합니다.
4. 장애 대응 절차는 Recovery Runbook (`docs/05.operations/runbooks/0031-postgresql-cluster.md`)를 참조합니다.

## Available Scripts

| Command                               | Description               |
| ------------------------------------- | ------------------------- |
| `docker compose --profile postgres-ha config --quiet` | 선택 클러스터 렌더링 |
| `docker exec pg-0 patronictl -c /home/postgres/postgres.yml list` | 클러스터 상태 및 역할 확인 |
| `docker compose logs --tail=120 pg-router pg-cluster-init pg-0 pg-1 pg-2` | 핵심 로그 확인 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :--- | :--- |
| `SCOPE` | Yes | 클러스터 이름(기본값: `pg-ha`) |
| `PATRONI_SUPERUSER_USERNAME` | Yes | 슈퍼유저 계정명(기본값: `postgres`) |
| `ETCD3_HOSTS` | Yes | etcd 엔드포인트 리스트 |
| `POSTGRES_WRITE_PORT` | No | HAProxy write endpoint(기본값: 15432) |
| `POSTGRES_READ_PORT` | No | HAProxy read endpoint(기본값: 15433) |
| `SERVICE_POSTGRES_DB` | Yes | `pg-cluster-init`가 생성/동기화하는 service database |

## Validation

Classification은 `LAB`입니다. etcd와 Patroni member가 한 호스트를 공유하므로
이 토폴로지는 host-level 재해 복구가 아닙니다. Logical 복구는 새로운 호환
cluster에 database별 dump를 넣기 전에 `pg_dumpall --globals-only`의
role/privilege를 복원하고 DCS 상태를 재구축하며 `RUN-0032`를 따릅니다.
소유 artifact는 `GDE-0031`, `POL-0031`, `RUN-0031`입니다.

- PostgreSQL cluster 서비스에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- PostgreSQL cluster 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.

## Troubleshooting

- 이 서비스 디렉터리에서 `docker compose config --quiet`로 Patroni, etcd, HAProxy, exporter, 네트워크, volume, secret 참조가 정상 렌더링되는지 먼저 확인합니다.
- leader election이나 routing이 실패하면 `docker compose logs pg-router`와 Patroni 노드 로그를 확인하고 DCS나 HAProxy 설정을 변경하기 전에 `patronictl list`를 확인합니다.

## Related Documents

- **Guide**: `docs/05.operations/guides/0031-postgresql-cluster.md`
- **Policy**: `docs/05.operations/policies/0031-postgresql-cluster.md`
- **Runbook**: `docs/05.operations/runbooks/0031-postgresql-cluster.md`
- **ARD**: `docs/02.architecture/descriptions/0004-data-architecture.md`
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [derived Compose 이미지 투영](../../tech-stack.versions.json)은 drift를 검증합니다.
