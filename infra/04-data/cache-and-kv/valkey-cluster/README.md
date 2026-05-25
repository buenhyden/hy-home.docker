# Valkey Distributed Cluster

> 고성능, 6노드 분산 캐시 클러스터 (Redis 호환 가능) / High-performance, 6-node Distributed Cache Cluster

## Overview

`valkey-cluster`는 `hy-home.docker` 에코시스템을 위한 고처리량, 저지연 캐싱 및 상태 저장소 계층을 제공한다. 3개의 프라이머리 노드와 3개의 복제본(Replica) 노드로 구성되어 자동 파티셔닝과 고가용성을 보장하도록 설계되었다.

`valkey-cluster` provides a high-throughput, low-latency caching and state storage layer for the `hy-home.docker` ecosystem. It is designed with 3 primary nodes and 3 replica nodes to ensure automatic partitioning and high availability.

## Audience

이 README의 주요 독자:

- 인프라를 배포하고 관리하는 **Operators**
- 클러스터와 연결되는 서비스를 개발하는 **Developers**
- 자동화된 운영 작업을 수행하는 **AI Agents**

## Scope

### In Scope

- 6노드 Valkey 클러스터 구성 및 관리
- Docker Compose 기반 배포 및 헬스체크
- 클러스터 초기화 및 상태 검증 스크립트

### Out of Scope

- 클러스터 외부의 개별 Valkey 인스턴스 (`mng-valkey`)
- 애플리케이션 레벨의 데이터 모델링 설계
- 다중 리전 복제 및 재해 복구 구성

## Structure

```text
valkey-cluster/
├── config/                  # Configuration files
├── scripts/                 # Initialization and management scripts
├── docker-compose.yml       # Cluster orchestration
└── README.md                # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Valkey Distributed Cluster service leaf in `04-data`; services: `valkey-node-0`, `valkey-node-1`, `valkey-node-2`, `valkey-node-3`, `valkey-node-4`, `valkey-node-5`, plus 2 more; root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml` |
| Config files | `docker-compose.yml`, `config`, `config/valkey.conf` |
| Config values | env keys: `PORT`, `NODE_NAME`; profiles: `data`, `service` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `valkey0-data:/data:rw`, `./config/valkey.conf:/usr/local/etc/valkey/valkey.conf:ro`, `./scripts/valkey-start.sh:/usr/local/bin/valkey-start.sh:ro`, `valkey1-data:/data:rw`, `valkey2-data:/data:rw`, `valkey3-data:/data:rw`, `valkey4-data:/data:rw`, `valkey5-data:/data:rw`, plus 7 more |
| Ports | `${VALKEY0_PORT:-6379}:${VALKEY0_PORT:-6379}`, `${VALKEY0_BUS_PORT:-16379}`, `${VALKEY1_PORT:-6380}:${VALKEY1_PORT:-6380}`, `${VALKEY1_BUS_PORT:-16380}`, `${VALKEY2_PORT:-6381}:${VALKEY2_PORT:-6381}`, `${VALKEY2_BUS_PORT:-16381}`, `${VALKEY3_PORT:-6382}:${VALKEY3_PORT:-6382}`, `${VALKEY3_BUS_PORT:-16382}`, plus 5 more |
| Labels | `hy-home.tier` |
| Secret refs | names: `service_valkey_password`; mounts: `/run/secrets/service_valkey_password` |
| Healthcheck | Compose healthcheck declared for `valkey-node-0`, `valkey-node-1`, `valkey-node-2`, `valkey-node-3`, `valkey-node-4`, plus 2 more; not declared for `valkey-cluster-init` |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/cache-and-kv/valkey-cluster.md), [Policy](../../../../docs/05.operations/policies/04-data/cache-and-kv/valkey-cluster.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/cache-and-kv/valkey-cluster.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. [docker-compose.yml](./docker-compose.yml)을 통해 클러스터 노드 구성을 확인한다.
2. [scripts/valkey-cluster-init.sh](./scripts/valkey-cluster-init.sh)를 통해 초기화 로직을 이해한다.
3. 가이드 문서는 [docs/05.operations/04-data/cache-and-kv/valkey-cluster.md](../../../../docs/05.operations/guides/04-data/cache-and-kv/valkey-cluster.md)를 참조한다.
4. 운영 정책은 [docs/05.operations/04-data/cache-and-kv/valkey-cluster.md](../../../../docs/05.operations/guides/04-data/cache-and-kv/valkey-cluster.md)를 확인한다.
5. 장애 조치 지침은 [docs/05.operations/04-data/cache-and-kv/valkey-cluster.md](../../../../docs/05.operations/guides/04-data/cache-and-kv/valkey-cluster.md)를 따른다.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Verify cluster connectivity by running `docker exec valkey-cluster valkey-cli cluster info` and confirming `cluster_state:ok`.
- Confirm replication health by checking `docker logs valkey-cluster | grep -i 'error\|warn'` after config changes.

## Troubleshooting

- Start with `docker compose config` to confirm network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For cluster connectivity errors: verify all cluster nodes can reach each other on the gossip port and confirm `cluster-enabled yes` in the config.
- For replication errors: check node roles with `cluster nodes` command and verify the replica count matches the configuration.
- For persistence issues: confirm the Valkey data volume is mounted and `appendonly` or `save` settings are correct.

## Related Documents

- **Guide**: [Valkey Cluster Guide](../../../../docs/05.operations/guides/04-data/cache-and-kv/valkey-cluster.md)
- **Policy**: [Valkey Operations Policy](../../../../docs/05.operations/policies/04-data/cache-and-kv/valkey-cluster.md)
- **Runbook**: [Valkey Recovery Runbook](../../../../docs/05.operations/runbooks/04-data/cache-and-kv/valkey-cluster.md)

## Tech Stack

| Category   | Technology   | Notes                     |
| ---------- | ------------ | ------------------------- |
| Image      | valkey/valkey| v9.0.2-alpine             |
| Interface  | valkey-cli   | Cluster protocol          |
| Clustering | 3P + 3R      | 6 nodes architecture      |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose up -d` | 클러스터 전체 노드 시작 |
| `docker compose ps` | 노드별 상태 및 헬스체크 확인 |
| `docker compose logs -f` | 실시간 로그 모니터링 |
| `docker exec -it valkey-node-0 valkey-cli -a $PASS cluster info` | 클러스터 상태 확인 |
