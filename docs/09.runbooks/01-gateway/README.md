<!-- Target: docs/09.runbooks/01-gateway/README.md -->

# 01-gateway Runbook

: Gateway Tier Maintenance & Recovery

---

## Overview (KR)

이 런북은 `01-gateway` 티어의 유지보수 및 즉각적인 장애 대응을 위한 실행 절차를 정의한다. 서비스 재시작, 로그 분석, 상태 점검 절차를 포함한다.

## Purpose

This runbook addresses common operational problems and provides emergency recovery steps for the Traefik/Nginx gateway stack.

## Canonical References

- **ARD**: [../../02.ard/README.md](../../02.ard/README.md)
- **Ops Policy**: [../../08.operations/01-gateway/README.md](../../08.operations/01-gateway/README.md)
- **Setup Guide**: [../../07.guides/01-gateway/01.setup.md](../../07.guides/01-gateway/01.setup.md)

## When to Use

- System start/stop/restart.
- SSL/TLS certificate updates.
- Unexpected 502/504 Bad Gateway errors.
- High latency observations at the edge.

## Procedure or Checklist

### Daily Checklist

- [ ] Check Traefik container status (`docker compose ps traefik`).
- [ ] Verify Prometheus metric scrape health via Traefik metrics endpoint.

### SSL Certificate Renewal

1. Place new certs (`cert.pem`, `key.pem`) in `secrets/certs/`.
2. Reload Traefik configuration:
   ```bash
   docker exec traefik kill -HUP 1
   ```

3. Verify expiration date via browser or `openssl s_client`.

### Troubleshooting 502 Errors

1. Check if the backend service is running.
2. Verify backend service is in `infra_net`.
3. Check Traefik logs for upstream resolution errors:

   ```bash
   docker compose logs -f traefik
   ```

## Verification Steps

- [ ] `docker exec traefik traefik healthcheck --ping` returns success.
- [ ] `curl -vI https://your-domain.com` shows valid certificate and 200/302 OK.

## Observability and Evidence Sources

- **Signals**: Traefik dashboard, Grafana (Traefik metrics).
- **Evidence to Capture**: `docker compose logs traefik > traefik_crash.log`.

## Safe Rollback

- Revert `traefik.yml` or `dynamic/*.yml` to the previous git version and restart.

## Related Operational Documents

- **Incident examples**: [../../10.incidents/README.md](../../10.incidents/README.md)
- **Postmortem examples**: [../../11.postmortems/README.md](../../11.postmortems/README.md)
