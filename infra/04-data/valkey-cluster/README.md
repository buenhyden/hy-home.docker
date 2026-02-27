# Valkey Cluster

A high-performance, 6-node distributed Valkey (Redis-compatible) cluster.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `valkey-node-0..5` | `valkey/valkey:9.0.2-alpine`| Cluster nodes | 0.5 CPU / 512M |
| `valkey-cluster-init` | `valkey/valkey:9.0.2-alpine`| One-shot cluster bootstrap | 128MB RAM |
| `valkey-exporter` | `oliver006/redis_exporter:v1.80.1` | Metrics exporter | 128MB RAM |

## Networking

- **Nodes**: Internal ports `${VALKEY[0-5]_PORT}` and bus ports `${VALKEY[0-5]_BUS_PORT}`.
- **Exporter**: `${VALKEY_EXPORTER_HOST_PORT}` (Host).

## Initialization

Automated via `valkey-cluster-init.sh` which executes `valkey-cli --cluster create` with the 6 nodes.

## Persistence

- **Volumes**: `valkey-data-0` to `valkey-data-5`.
- **Mount Path**: `/data`.
- **Config**: Mounts local `./config/valkey.conf`.

## File Map

| Path                 | Description                                |
| -------------------- | ------------------------------------------ |
| `docker-compose.yml` | 6-node cluster definition and entrypoints. |
| `README.md`          | Cluster management and scaling notes.       |
