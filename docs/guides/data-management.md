# Data Management Guide

> Documentation for the persistent storage engines, specifically the PostgreSQL Patroni cluster and MinIO.

## 1. PostgreSQL High Availability (Patroni)

The PostgreSQL implementation utilizes Spilo (Zalando) to run a fully automated High-Availability Patroni Cluster.

### Topology

- **3x PostgreSQL Nodes** (`pg-0`, `pg-1`, `pg-2`).
- **3x Etcd Nodes** (`etcd-1`, `etcd-2`, `etcd-3`): Used as the Distributed Configuration Store (DCS) for leader election.
- **1x HAProxy Router** (`pg-router`): Balances read/write traffic.
  - Port 5000: Write (Primary Node)
  - Port 5001: Read (Replica Nodes)

### Initialization

The cluster is initialized using a temporary `pg-cluster-init` container which injects `init_users_dbs.sql` upon the first successful startup.

> [!NOTE]
> Database migrations should be executed against the HAProxy Writer endpoint (`pg-router:5000`).

## 2. MinIO Object Storage

MinIO acts as an S3-compatible object storage layer critical for the rest of the infrastructure (specifically Loki and Tempo object backends).

### Buckets

Required buckets (e.g., `loki-data`, `tempo-data`) must be automatically provisioned on startup or created via the MinIO UI before the observability stack boots. Note that credentials are encrypted away in the `/secrets` directory at the project root.

## 3. Storage Policies

Data is mapped recursively to the `$DEFAULT_DATA_DIR` directory on the host environment (WSL2 / Linux).

> [!CAUTION]
> Deleting the local directory at `$DEFAULT_DATA_DIR` will result in unrecoverable data loss across PostgreSQL, Redis, and MinIO. Implement cron-based snapshotting of this directory.
