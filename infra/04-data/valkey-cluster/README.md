# Valkey Cluster

A high-performance, 6-node distributed Valkey (Redis-compatible) cluster.

## Services

| Service | Image | Role | Resources | IP Range |
| :--- | :--- | :--- | :--- | :--- |
| `valkey-node-0..5` | `valkey/valkey:9.0.2-alpine`| Cluster Nodes | 0.5 CPU / 512M | `172.19.0.60..65`|
| `valkey-init` | `valkey/valkey:9.0.2-alpine`| Setup Assistant | 128MB RAM | `172.19.0.66` |
| `exporter` | `redis_exporter:v1.80.1` | Metrics | 128MB RAM | `172.19.0.67` |

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
