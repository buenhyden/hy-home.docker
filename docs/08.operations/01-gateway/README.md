<!-- Target: docs/08.operations/01-gateway/README.md -->

# Gateway Operations Policy

> Governance and control rules for the edge routing infrastructure.

---

## Overview (KR)

이 문서는 `01-gateway` 티어의 운영 정책을 정의한다. 트래픽 인입 경로의 보안성, 가용성, 그리고 변경 관리 프로세스에 대한 통제 기준을 규정한다.

## Policy Scope

This policy governs all traffic ingress points, TLS termination strategies, and routing middleware configurations in the `hy-home.docker` cluster.

## Applies To

- **Systems**: Traefik, Nginx, OAuth2 Proxy.
- **Agents**: Infrastructure Maintenance Agents.
- **Environments**: Production, Staging, Development.

## Controls

### Security

- **Required**: All public endpoints MUST terminate TLS 1.2+ at Traefik.
- **Required**: Internal dashboards MUST be protected by Basic Auth as a secondary layer.
- **Disallowed**: Plaintext HTTP (Port 80) is allowed only for redirection to HTTPS.

### Availability

- **Required**: Health checks MUST be configured for both Traefik and Nginx.
- **Disallowed**: Manual modification of `traefik.yml` in production without a verified deployment plan.

## Verification

- **Compliance Check**: Weekly audit of SSL Labs score (target: A+).
- **Log Audit**: Monthly review of 4xx and 5xx error trends in Traefik access logs.

## Review Cadence

- Quarterly.

## Related Documents

- **ARD**: [../02.ard/README.md](../../02.ard/README.md)
- **Runbook**: [../09.runbooks/01-gateway/README.md](../../09.runbooks/01-gateway/README.md)
