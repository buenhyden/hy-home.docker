# Valkey Cluster

A high-performance, 6-node distributed Valkey (Redis-compatible) cluster.

## Services

| Service          | Role            | Instances | Resources         |
| :--------------- | :-------------- | :-------- | :---------------- |
| `valkey-cluster` | Distributed Cache| 6 Nodes   | 0.2 CPU / 256MB ea|

## Networking

- **Internal Ports**: 6379 (Client), 16379 (Bus).
- **Setup**: Nodes are automatically clustered using a startup script (Check `scripts/` or `docker-compose.yml`).

## Persistence

- **Data**: Each node has its own persistence directory in the `valkey-data` volume.

## File Map

| Path                 | Description                                |
| -------------------- | ------------------------------------------ |
| `docker-compose.yml` | 6-node cluster definition and entrypoints. |
| `README.md`          | Cluster management and scaling notes.       |
