---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/cache-and-kv/valkey-cluster.md -->

# Valkey Cluster Usage Guide

> Use this guide to understand and verify the current 6-node Valkey cluster implementation.

---

## Usage

### Overview (KR)

`valkey-cluster`는 `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml`에 선언된 6-node Valkey cache/kv cluster다. 현재 구현은 `data` 및 `service` profile에서 `valkey-node-0`부터 `valkey-node-5`, `valkey-cluster-init`, `valkey-cluster-exporter`를 실행하고, 모든 runtime credential은 Docker Secret `service_valkey_password`로 주입한다.

### Usage Type

`system-guide | operational-reference`

### Target Audience

- Operator
- Developer
- SRE
- AI Agent

### Purpose

이 가이드는 Valkey cluster의 현재 compose service set, port model, initialization job, secret boundary, 일반 확인 절차를 이해하고 애플리케이션 및 운영 문서가 실제 구현과 같은 surface를 참조하도록 돕는다.

### Prerequisites

- Repository checkout at the project root.
- Docker Compose access on the local or approved infrastructure host.
- `.env` or approved environment values for `VALKEY0_PORT` through `VALKEY5_PORT` and bus ports.
- Docker Secret file for `service_valkey_password`; secret values must not be copied into docs, logs, or commits.
- Runtime data directories under `${DEFAULT_DATA_DIR}/valkey/data-0` through `data-5`.

### Step-by-step Instructions

1. 현재 compose service set을 확인한다.

   ```bash
   docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml --profile data config --services
   ```

   Expected services: `valkey-node-0`, `valkey-node-1`, `valkey-node-2`, `valkey-node-3`, `valkey-node-4`, `valkey-node-5`, `valkey-cluster-init`, `valkey-cluster-exporter`.

2. 노드와 포트 모델을 확인한다.

   - Node ports: `${VALKEY0_PORT:-6379}` through `${VALKEY5_PORT:-6384}`
   - Cluster bus ports: `${VALKEY0_BUS_PORT:-16379}` through `${VALKEY5_BUS_PORT:-16384}`
   - Exporter: `${VALKEY_EXPORTER_PORT:-9121}`
   - Network: `infra_net`

3. 초기화 job 경계를 확인한다.

   `valkey-cluster-init` runs [valkey-cluster-init.sh](../../../../../infra/04-data/cache-and-kv/valkey-cluster/scripts/valkey-cluster-init.sh), waits for all six nodes to be healthy, checks `valkey-node-0`, and creates the cluster with `--cluster-replicas 1`. The script skips destructive re-initialization when nodes already contain data or cluster metadata.

4. 일반 상태를 확인한다.

   ```bash
   docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml --profile data ps valkey-node-0 valkey-node-1 valkey-node-2 valkey-node-3 valkey-node-4 valkey-node-5 valkey-cluster-exporter
   ```

### Common Pitfalls

- Referring to old init service names. The current init service is `valkey-cluster-init`.
- Referring to a single `valkey-cluster` container. The current implementation uses six node containers plus init/exporter services.
- Passing passwords through shell variables in docs or evidence. Use Docker Secrets inside the container boundary and avoid copying secret values.
- Assuming a memory eviction policy is configured when `config/valkey.conf` does not declare one.

## Common Checks

- `docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml --profile data config`
- `docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml --profile data ps`
- Search paired guide/policy/runbook and infra README for old service names, direct password variables, stale image tags, or single-container assumptions.
- Expected result: compose renders, documented services match the compose file, and no stale service/container name is used as an operational command target.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은
[recovery runbook](../../../runbooks/04-data/cache-and-kv/valkey-cluster.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/cache-and-kv/valkey-cluster.md)
- [Recovery runbook](../../../runbooks/04-data/cache-and-kv/valkey-cluster.md)
- [Infrastructure service README](../../../../../infra/04-data/cache-and-kv/valkey-cluster/README.md)
