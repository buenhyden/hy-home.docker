# Service Runbook: Gateway 502 Troubleshooting

_Target Directory: `runbooks/01-gateway/gateway-502-errors.md`_
_Note: Procedure for resolving "Bad Gateway" responses from Traefik ingress._

---

## 1. Service Overview & Ownership

- **Description**: Handles Ingress traffic and edge routing via Traefik.
- **Owner Team**: Gateway / Platform
- **Primary Contact**: #infra-gateway (Slack)

## 2. Dependencies

| Dependency | Type | Impact if Down | Link to Runbook |
| ---------- | ---- | -------------- | --------------- |
| Traefik Proxy | Hub | Gateway failure | [Traefik Recovery](traefik-proxy-recovery.md) |
| infra_net | Network | Routing lost | [Bootstrap](../core/infra-bootstrap-runbook.md) |

## 3. Observability & Dashboards

- **Primary Dashboard**: [Traefik HTTP Routers](https://dashboard.${DEFAULT_URL}/#http/routers)
- **Error Trends**: [Grafana Edge Metrics](https://grafana.${DEFAULT_URL}/d/traefik-overview)

## 4. Operational Scenarios

### Scenario A: Target Container Unreachable

- **Given**: End user receives `502 Bad Gateway`.
- **When**: Traefik access logs show "service unreachable".
- **Then**:
  1. [ ] Check Target Service status: `docker compose ps <service_name>`
  2. [ ] Verify Network membership: `docker network inspect infra_net | grep <service_name>`
- **Expected Outcome**: Container status is `Up` and has an internal IP on `infra_net`.

### Scenario B: Load Balancer Port Mismatch

- **Given**: Container is healthy but 502 persists.
- **When**: Application listens on dynamic port (e.g. 8080) but label refers to default.
- **Then**:
  1. [ ] Check labels: `docker inspect <service_name> --format '{{.Config.Labels}}'`
  2. [ ] Verify `traefik.http.services.<name>.loadbalancer.server.port` matches internal app port.
- **Expected Outcome**: Port label matches `EXPOSE` or binary listen port.

## 5. Safe Rollback Procedure

- [ ] Revert any recent `labels:` changes in `docker-compose.yml`.
- [ ] Run `docker compose up -d <service_name>` to re-apply.

## 6. Data Safety Notes

- **Configuration**: Traefik dynamic configs in `infra/01-gateway/traefik/dynamic/` are auto-reloaded.

## 7. Escalation Path

1. **On-Call**: Gateway Engineer
2. **Secondary**: Platform Lead

## 8. Verification Steps (Post-Fix)

- [ ] `curl -I https://<service>.${DEFAULT_URL}` returns `200 OK` or `302 Found`.
- [ ] Traefik Dashboard shows router state as `success` (green).
