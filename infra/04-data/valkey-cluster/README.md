<!-- [ID:04-data:valkey-cluster] -->
# Valkey Cluster

> High-performance, 6-node distributed Valkey cluster.

## 1. Context (SSoT)

The `valkey-cluster` provides a distributed caching and session management layer. It uses a 3-master/3-replica configuration to ensure high throughput and fault tolerance.

- **Status**: Production / Distributed
- **SSoT Documentation**: [docs/07.guides/04-data/01.core-dbs.md](../../../docs/07.guides/04-data/01.core-dbs.md)
- **Compatibility**: Redis OSS CLI compatible

## 2. Structure

```text
valkey-cluster/
├── docker-compose.yml   # Cluster definition
├── config/              # Node configuration
└── scripts/             # Bootstrap scripts
```

## 3. Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **valkey-node-0..5** | Valkey 9.0 | Cluster nodes |
| **cluster-init** | Valkey CLI | 3M/3R Bootstrap |
| **exporter** | Redis Exporter | Metrics collection |

## 4. Configuration (Secrets & Env)

- **Bootstrap**: Automated via `valkey-cluster-init.sh`.
- **Passwords**: Managed via `VALKEY_PASSWORD_FILE`.
- **Ports**: Client (`6379`), Bus (`16379`).

## 5. Persistence

- **Volumes**: `valkey-data-0..5`.
- **Path**: `${DEFAULT_DATA_DIR}/valkey/...`

## 6. Operational Status

- **Status**: Distributed HA
- **Monitoring**: `http://pg-router:9121/metrics` (Exporter)
- **Check**: `valkey-cli -c -a "$PASSWORD" -h valkey-node-0 cluster info`

---
Copyright (c) 2026. Licensed under the MIT License.
