# Incident Runbook: Patroni Split-Brain

**Issue:** `PatroniMissingLeader` alert triggered, or multiple nodes claim leadership simultaneously.

## Definition

A split-brain scenario occurs in a Patroni cluster when network partitions cause Etcd to lose consensus, or when two database variants believe they are the primary node but WAL logs have diverged.

## Resolution Steps

### 1. Identify the current State

Execute a shell into one of the Pg instances to view the topology.

```bash
docker exec -it pg-0 patronictl -c /home/postgres/postgres0.yml topology
```

### 2. Verify Etcd Health

If Etcd itself is down, Patroni falls back to a read-only state.

```bash
docker exec -it etcd-1 etcdctl endpoint health --endpoints=http://localhost:2379
```

If Etcd nodes are failing, restart the `etcd` services.

```bash
docker compose -f infra/04-data/postgresql-cluster/docker-compose.yml restart etcd-1 etcd-2 etcd-3
```

### 3. Re-initialize the Replica (Sync Failure)

If a primary is determined, but a replica is stuck in a diverging state (Split-Brain on data):

```bash
docker exec -it pg-0 patronictl -c /home/postgres/postgres0.yml reinit pg-ha <stuck_node_name>
```

### 4. Forcing a Failover

If the primary is deadlocked and you need to force a replica to take over without consensus (Dangerous - potential data loss):

```bash
docker exec -it pg-1 patronictl -c /home/postgres/postgres1.yml failover --force
```

## Post-Mortem

Check the `/var/log/postgresql` directories to see if OOM (Out Of Memory) killer killed the primary resulting in a miscommunicated state shift.
