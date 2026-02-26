# Service Runbook: Core Infra Bootstrap

_Target Directory: `runbooks/core/infra-bootstrap-runbook.md`_
_Note: High-criticality bootstrap procedure for the combined Docker Compose infrastructure._

---

## 1. Service Overview & Ownership

- **Description**: Standard procedure to initialize the core infrastructure stack from a clean state.
- **Owner Team**: Platform / SRE
- **Primary Contact**: #infra-ops (Slack)

## 2. Dependencies

| Dependency | Type | Impact if Down | Link to Runbook |
| ---------- | ---- | -------------- | --------------- |
| Docker Engine | Tooling | Bootstrap impossible | [Deployment Runbook](deployment-runbook.md) |
| Docker Compose v2 | Tooling | Orchestration failure | [Deployment Runbook](deployment-runbook.md) |
| mkcert | Provisioning | No local TLS | N/A |

## 3. Observability & Dashboards

- **Primary Dashboards**:
  - Traefik Hub: `https://dashboard.${DEFAULT_URL}`
  - Metrics Hub: `https://grafana.${DEFAULT_URL}`
- **SLOs/SLIs**:
  - Uptime (Core): > 99.9%
  - Ready-to-Serve Latency: < 5m from start.

## 4. Alerts & Common Failures

### Scenario A: Missing Docker Secrets

- **Symptoms**: `docker compose up` fails with "secret file not found".
- **Remediation Action**:
  - [ ] Execute `bash scripts/preflight-compose.sh` to identify missing files.
  - [ ] Populate missing `.txt` files in `secrets/` using vault or baseline values.
- **Expected Outcome**: `docker compose config` returns clear YAML with zero errors.

### Scenario B: TLS Certificate Mismatch

- **Symptoms**: 502/SSL errors in browser when hitting `https`.
- **Remediation Action**:
  - [ ] `bash scripts/generate-local-certs.sh`
  - [ ] Restart Traefik: `docker compose restart traefik`
- **Expected Outcome**: Browser shows valid certificate for `*.${DEFAULT_URL}`.

## 5. Safe Rollback Procedure

- [ ] **Step 1**: Stop all containers: `docker compose down`
- [ ] **Step 2**: (Data Wipe - CAUTION) Only if corrupted: `docker compose down -v`
- [ ] **Step 3**: Re-render config: `docker compose config`
- [ ] **Step 4**: Perform clean start: `docker compose up -d`

## 6. Data Safety Notes (If Stateful)

- **WARNING**: `docker compose down -v` PERMANENTLY deletes local database volumes.
- **Backups**: Ensure `/mnt/backup/db/` has a valid snapshot before performing volume resets.

## 7. Escalation Path

1. **Primary On-Call**: Platform Engineer (@handle)
2. **Secondary Escalation**: SRE Lead (@handle)
3. **Management Escalation (SEV-1)**: VP Engineering (@handle)

## 8. Verification Steps (Post-Fix)

### Deterministic Bootstrap Checklist

1. **Validation Check**
   - [ ] Run `docker compose config -q`
2. **Execution**
   - [ ] Run `docker compose up -d`
3. **Health Verification**
   - [ ] `docker exec traefik traefik healthcheck --ping` -> SUCCESS
   - [ ] `curl -k https://grafana.${DEFAULT_URL}/api/health` -> 200 OK
   - [ ] `docker compose ps` shows all containers as `Up (healthy)`.
