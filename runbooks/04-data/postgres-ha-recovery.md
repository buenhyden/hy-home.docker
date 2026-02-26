# Service Runbook: PostgreSQL HA & Patroni Recovery

_Target Directory: `runbooks/04-data/postgres-ha-recovery.md`_
_Note: High-criticality data tier recovery procedure._

---

## 1. Service Overview & Ownership

- **Description**: High-Availability PostgreSQL cluster managed by Patroni and Etcd.
- **Owner Team**: Database Ops / Platform
- **Primary Contact**: #ops-database (Slack)

## 2. Dependencies

| Dependency | Type | Impact if Down | Link to Runbook |
| ---------- | ---- | -------------- | --------------- |
| Etcd Cluster | Quorum | No leader election | [Vault/Etcd Runbook](../03-security/vault-sealed.md) |
| Docker Engine | Runtime | Complete service failure | [Core Runbook](../core/infra-bootstrap-runbook.md) |

## 3. Observability & Dashboards

- **Primary Dashboard**: [Grafana DB Overview](https://grafana.${DEFAULT_URL}/d/postgres-ha)
- **SLOs/SLIs**: 99.99% Write availability, zero data loss.
- **Alert Definitions**: `PatroniMissingLeader`, `PostgresReplicaLag`

## 4. Alerts & Common Failures

### Scenario A: Split-Brain or No Leader Election

- **Symptoms**: `PatroniMissingLeader` alert; multiple nodes claiming leader.
- **Investigation Steps**:
  1. `docker exec -it pg-0 patronictl topology`
  2. Check Etcd logs: `docker logs etcd-1`
- **Remediation Action**:
  - [ ] Restart Etcd quorum: `docker compose restart etcd-1 etcd-2 etcd-3`
  - [ ] Forced Failover (if primary deadlocked): `docker exec -it pg-1 patronictl failover --force`
- **Expected Outcome**: Single "Leader" appears in `patronictl list`.

### Scenario B: Replica Out of Sync

- **Symptoms**: WAL recycling error in replica logs.
- **Investigation Steps**:
  1. `docker logs pg-1 | grep "requested WAL segment"`
- **Remediation Action**:
  - [ ] Rebuilt node: `docker exec -it pg-0 patronictl reinit pg-ha [stuck_node]`
- **Expected Outcome**: Node enters `streaming` state with 0 lag.

## 5. Safe Rollback Procedure

- [ ] **Step 1**: Check if data volume is intact.
- [ ] **Step 2**: Revert any recent `docker-compose.yml` config changes.
- [ ] **Step 3**: Restart stack: `docker compose up -d`.

## 6. Data Safety Notes (If Stateful)

- **WARNING**: Do NOT delete `${DEFAULT_DATA_DIR}/pg/` unless performing an Emergency Reset.
- **Backups**: Verified daily via PgBackRest sidecar.

## 7. Escalation Path

1. **Primary On-Call**: Database Engineer (Slack)
2. **Secondary Escalation**: Platform Architect
3. **Management Escalation (SEV-1)**: CTO / VP Eng

## 8. Verification Steps (Post-Fix)

- [ ] `patronictl list` shows one Leader and two Replicas in `running` state.
- [ ] Application logs show successful DB connections.
- [ ] Grafana "Postgres Connections" counts are > 0.
