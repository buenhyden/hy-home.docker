<!-- [ID:04-data:valkey-cluster] -->
# Valkey Cluster

> High-performance, 6-node distributed Valkey cluster.

## Overview (KR)

이 스택은 6개의 노드로 구성된 고성능 분산 Valkey(Redis 호환) 클러스터를 제공합니다. 확장성과 고가용성을 위해 설계되었습니다.

## Overview

The `valkey-cluster` provides a distributed caching and session management layer for applications requiring high throughput and low latency. It uses a standard 3-master/3-replica configuration to ensure fault tolerance.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **valkey-node-0..5** | Valkey 9.0 | Cluster nodes |
| **valkey-cluster-init** | Valkey CLI | One-shot bootstrap |
| **valkey-exporter** | Redis Exporter | Metrics |

## Networking

- **Client Access**: Port `6379` (Internal) on each node.
- **Cluster Bus**: Port `16379` (Internal) for inter-node communication.

## Initialization

Automated via `valkey-cluster-init.sh` which executes `valkey-cli --cluster create` including all 6 nodes on first deployment.

## Persistence

- **Volumes**: Individual `valkey-data-0` to `valkey-data-5` volumes.
- **Config**: Mounts local `./config/valkey.conf` for shared cluster behavior.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Cluster definition. |
| `scripts/` | Initialization and management scripts. |
| `config/` | Node configuration templates. |

---

## Documentation References

- [Core DB Guide](../../../docs/07.guides/04-data/01.core-dbs.md)
- [Backup Operations](../../../docs/08.operations/04-data/README.md)
