# postgresql-cluster

> Patroni 및 etcd를 이용한 고가용성(HA) PostgreSQL 17 관계형 데이터베이스 클러스터
> High-Availability (HA) PostgreSQL 17 Relational Database Cluster using Patroni and etcd

---

## Overview (KR/EN)

### KR

`postgresql-cluster`는 지속성과 가용성이 핵심인 서비스들을 위한 관계형 데이터베이스 인프라입니다. Spilo(Zalando) 이미지를 기반으로 Patroni가 클러스터 생명주기를 관리하며, etcd를 DCS(Distributed Configuration Store)로 사용하여 리더 선출 및 장애 복구를 자동화합니다. HAProxy(`pg-router`)를 통해 애플리케이션에 단일 접속 지점 및 읽기/쓰기 분산 기능을 제공합니다.

### EN

`postgresql-cluster` is a relational database infrastructure for services where durability and availability are critical. Based on the Spilo (Zalando) image, Patroni manages the cluster lifecycle, and etcd is used as the DCS (Distributed Configuration Store) to automate leader election and failover. It provides a single point of access and read/write distribution to applications through HAProxy (`pg-router`).

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
- 외부망 직접 노출 (반드시 `infra_net` 내부망 사용)
- 클러스터 외부 수동 백업 저장소 관리

## Structure

```text
postgresql-cluster/
├── config/
│   └── haproxy.cfg           # HAProxy 라우팅 설정
├── init-scripts/
│   └── init_users_dbs.sql    # 초기 데이터베이스 및 사용자 생성 스크립트
├── scripts/
│   └── spilo-entrypoint-with-secrets.sh # Secret-aware Spilo entrypoint
├── docker-compose.yml        # 클러스터 오케스트레이션 정의
└── README.md                 # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | postgresql-cluster service leaf in `04-data`; services: `etcd-1`, `etcd-2`, `etcd-3`, `pg-router`, `pg-cluster-init`, `pg-0`, plus 5 more; root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/relational/postgresql-cluster/docker-compose.yml` |
| Config files | `docker-compose.yml`, `config`, `config/haproxy.cfg.tpl` |
| Config values | env keys: `POSTGRES_ROUTER_HOSTNAME`, `POSTGRES_WRITE_PORT`, `POSTGRES_READ_PORT`, `POSTGRES_USER`, `POSTGRES_DB`, `PATRONI_EXPORTER_USERNAME`, `SERVICE_POSTGRES_USERNAME`, `SERVICE_POSTGRES_DB`, plus 10 more; profiles: `data`, `service` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/relational/postgresql-cluster/docker-compose.yml` |
| Networks | `infra_net`, `k3d-hyhome` |
| Volumes | `etcd1-data:/etcd-data:rw`, `etcd2-data:/etcd-data:rw`, `etcd3-data:/etcd-data:rw`, `./config/haproxy.cfg.tpl:/tmp/haproxy.cfg.tpl:ro`, `./init-scripts/init_users_dbs.sql:/work/init_users_dbs.sql:ro`, `pg0-data:/home/postgres/pgdata:rw`, `./scripts/spilo-entrypoint-with-secrets.sh:/usr/local/bin/spilo-entrypoint-with-secrets.sh:ro`, `pg1-data:/home/postgres/pgdata:rw`, plus 7 more |
| Ports | `${POSTGRES_WRITE_HOST_PORT:-15432}:${POSTGRES_WRITE_PORT:-15432}`, `${POSTGRES_READ_HOST_PORT:-15433}:${POSTGRES_READ_PORT:-15433}`, `${HAPROXY_METRICS_PORT:-8404}`, `${POSTGRES_EXPORTER_PORT:-9187}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.haproxy-stats.rule`, `traefik.http.routers.haproxy-stats.entrypoints`, `traefik.http.routers.haproxy-stats.tls`, `traefik.http.services.haproxy-stats.loadbalancer.server.port`, `traefik.http.routers.haproxy-stats.middlewares` |
| Secret refs | names: `pg_haproxy_stats_password`, `patroni_superuser_password`, `patroni_exporter_password`, `service_postgres_password`, `patroni_replication_password`; mounts: `/run/secrets/pg_haproxy_stats_password`, `/run/secrets/patroni_superuser_password`, `/run/secrets/patroni_exporter_password`, `/run/secrets/service_postgres_password`, `/run/secrets/patroni_replication_password` |
| Healthcheck | Compose healthcheck declared for `etcd-1`, `etcd-2`, `etcd-3`, `pg-router`, `pg-0`, plus 5 more; not declared for `pg-cluster-init` |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/relational/postgresql-cluster.md), [Policy](../../../../docs/05.operations/policies/04-data/relational/postgresql-cluster.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/relational/postgresql-cluster.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. 클러스터 아키텍처 및 연결 방법은 [Technical Guide](../../../../docs/05.operations/guides/04-data/relational/postgresql-cluster.md)를 먼저 확인합니다.
2. 루트 compose include 상태를 확인하고 `docker compose -f docker-compose.yml -f infra/04-data/relational/postgresql-cluster/docker-compose.yml --profile data --profile service config`로 렌더링합니다.
3. 운영 변경 사항은 반드시 [Operations Policy](../../../../docs/05.operations/policies/04-data/relational/postgresql-cluster.md) 준수 여부를 확인합니다.
4. 장애 대응 절차는 [Recovery Runbook](../../../../docs/05.operations/runbooks/04-data/relational/postgresql-cluster.md)를 참조합니다.

## Available Scripts

| Command                               | Description               |
| ------------------------------------- | ------------------------- |
| `docker compose -f docker-compose.yml -f infra/04-data/relational/postgresql-cluster/docker-compose.yml --profile data --profile service config` | 선택 클러스터 렌더링 |
| `docker exec pg-0 patronictl -c /home/postgres/postgres.yml list` | 클러스터 상태 및 역할 확인 |
| `docker compose logs --tail=120 pg-router pg-cluster-init pg-0 pg-1 pg-2` | 핵심 로그 확인 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :--- | :--- |
| `SCOPE` | Yes | 클러스터 이름 (Default: `pg-ha`) |
| `PATRONI_SUPERUSER_USERNAME` | Yes | 슈퍼유저 계정명 (Default: `postgres`) |
| `ETCD3_HOSTS` | Yes | etcd 엔드포인트 리스트 |
| `POSTGRES_WRITE_PORT` | No | HAProxy write endpoint (Default: 15432) |
| `POSTGRES_READ_PORT` | No | HAProxy read endpoint (Default: 15433) |
| `SERVICE_POSTGRES_DB` | Yes | `pg-cluster-init`가 생성/동기화하는 service database |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect PostgreSQL cluster services.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking PostgreSQL cluster documentation ready.

## Troubleshooting

- Start with `docker compose config` from this service directory to verify Patroni, etcd, HAProxy, exporter, network, volume, and secret references render.
- If leader election or routing fails, inspect `docker compose logs pg-router` and the Patroni node logs, then check `patronictl list` before changing DCS or HAProxy settings.

## Related Documents

- **Guide**: [docs/05.operations/guides/04-data/relational/postgresql-cluster.md](../../../../docs/05.operations/guides/04-data/relational/postgresql-cluster.md)
- **Policy**: [docs/05.operations/policies/04-data/relational/postgresql-cluster.md](../../../../docs/05.operations/policies/04-data/relational/postgresql-cluster.md)
- **Runbook**: [docs/05.operations/runbooks/04-data/relational/postgresql-cluster.md](../../../../docs/05.operations/runbooks/04-data/relational/postgresql-cluster.md)
- **ARD**: [docs/02.architecture/requirements/0004-data-architecture.md](../../../../docs/02.architecture/requirements/0004-data-architecture.md)

---
Copyright (c) 2026. Licensed under the MIT License.
