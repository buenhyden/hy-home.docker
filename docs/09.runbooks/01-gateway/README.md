# 01-gateway Runbook

: Gateway Tier Maintenance & Recovery

---

## Overview (KR)

이 런북은 `01-gateway` 티어의 유지보수 및 즉각적인 장애 대응을 위한 실행 절차를 정의한다. 서비스 재시작, 로그 분석, 상태 점검 절차를 포함한다.

## Purpose

This runbook addresses common operational tasks and emergency recovery for the Traefik/Nginx gateway stack.

## When to Use

- System start/stop/restart.
- SSL/TLS certificate updates.
- Unexpected 502/504 Bad Gateway errors.
- High latency observations at the edge.

## Procedure or Checklist

### Daily Checklist

- [ ] Check Traefik container status.
- [ ] Verify Prometheus metric scrape health.

### SSL Certificate Renewal

1. Place new certs in `secrets/certs/`.
2. Reload Traefik (Dynamic config usually picks up changes, if not):

   ```bash
   docker exec traefik kill -HUP 1
   ```

3. Verify expiration date via browser.

### Troubleshooting 502 Errors

1. Check if the backend service is running.
2. Verify backend service is in `infra_net`.
3. Check Traefik logs for upstream resolution errors:

   ```bash
   docker compose logs -f traefik
   ```

## Verification Steps

- [ ] `docker exec traefik traefik healthcheck --ping` should return success.
- [ ] `curl -vI https://your-domain.com` should show valid cert and 200/302.

## Observability and Evidence Sources

- **Signals**: Traefik dashboard, Grafana dashboard (Traefik metrics).
- **Evidence to Capture**: `docker compose logs traefik > traefik_crash.log`.

## Safe Rollback

- Revert `traefik.yml` or `dynamic/*.yml` to the previous git version and restart.

## Related Operational Documents

- **Operations Policy**: [../../docs/08.operations/01-gateway/README.md]
- **Setup Guide**: [../../docs/07.guides/01-gateway/01.setup.md]
