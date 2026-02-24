# Runbook: PostgreSQL HA Re-initialization

> **Component**: `postgresql-cluster`
> **Profile**: `mng-db`
> **Severity**: CRITICAL (Destructive)

## 1. Description

This runbook describes how to completely wipe and re-initialize a PostgreSQL Patroni cluster. This is typically required if the Etcd quorum and Patroni state are hopelessly desynchronized or if you wish to reset the environment.

> [!CAUTION]
> This procedure DESTROYS all data in the database cluster. Ensure you have backups if the data is valuable.

## 2. Steps

1. **Stop the Cluster**:

   ```bash
   docker compose -f infra/04-data/postgresql-cluster/docker-compose.yml down
   ```

2. **Wipe Persistent Data**:
   Remove the local data directories mapped to the containers.

   ```bash
   # Caution: Destructive
   sudo rm -rf ${DEFAULT_DATA_DIR}/pg/*
   sudo rm -rf ${DEFAULT_DATA_DIR}/etcd/*
   ```

3. **Verify Volume Cleanliness**:
   Ensure no Docker volumes are lingering with stale state.

   ```bash
   docker volume ls | grep pg-ha
   ```

4. **Boot Strategy**:
   Bring up the nodes. Patroni will detect the empty data directory and initialize a fresh leader.

   ```bash
   docker compose -f infra/04-data/postgresql-cluster/docker-compose.yml up -d
   ```

5. **Verify Initialization**:
   Check the topology to ensure nodes have re-joined.

   ```bash
   docker exec -it pg-0 patronictl -c /home/postgres/postgres0.yml topology
   ```

## 3. Rollback

There is no rollback for data deletion. You must restore from a previous filesystem or pg_dump backup if accidental deletion occurred.
