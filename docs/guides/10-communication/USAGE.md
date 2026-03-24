---
layer: infra
---
# Mail Server Operations

**Overview (KR):** 메일 서버 시스템의 실행 상태 점검 및 통합 오퍼레이션 청사진입니다.

> Operational guide for the Communication tier's SMTP services: MailHog (dev) and Stalwart (production).

## 1. Description

The Communication stack (`infra/10-communication/mail/docker-compose.yml`) runs two mail services under the `communication` Docker Compose profile:

| Service | Role | Image |
| :--- | :--- | :--- |
| `mailhog` | Dev SMTP trap — captures all mail in memory, no external delivery | `mailhog/mailhog:v1.0.1` |
| `stalwart` | Production mail server — SMTP, IMAP, submission with TLS | `stalwartlabs/stalwart:v0.14` |

Only one should be the active relay at a time. For development, use MailHog. For production or staging with real delivery, switch to Stalwart.

## 2. SMTP Configurations

### Internal routing (MailHog — dev)

Services on `infra_net` should target MailHog during development:

- **Host**: `mailhog`
- **Port**: `1025`
- **TLS**: Disabled (trusted internal Docker network)
- **Auth**: None

### Internal routing (Stalwart — production)

- **Host**: `stalwart`
- **SMTP Port**: `25`
- **Submission Port**: `587` (STARTTLS)
- **SMTPS Port**: `465` (TLS)
- **IMAP Port**: `993` (TLS)
- **ManageSieve Port**: `4190`
- **Admin Web UI**: `https://mail.${DEFAULT_URL}` (port `${STALWART_PORT:-8080}`)
- **Auth**: Admin credentials via `stalwart_password` Docker secret

## 3. Web Dashboards

| Service | URL | Notes |
| :--- | :--- | :--- |
| MailHog UI | `https://mailhog.${DEFAULT_URL}` | SSO-protected |
| Stalwart Admin | `https://mail.${DEFAULT_URL}` | Web-based admin panel |

## 4. Secrets and Persistence

### Secrets

| Secret Name | Path | Used by |
| :--- | :--- | :--- |
| `stalwart_password` | `secrets/common/stalwart_password.txt` | Stalwart admin password |

### Volumes

| Volume | Host Path | Purpose |
| :--- | :--- | :--- |
| `stalwart-data` | `${DEFAULT_COMMUNICATION_DIR}/stalwart/data` | Stalwart mail data, config, certs |

MailHog stores mail in memory only — all messages are lost on container restart.

## 5. Troubleshooting

### Keycloak or Grafana cannot reach the SMTP server

1. Check that the `communication` profile is active and containers are running:

```bash
docker ps --filter name=mailhog
docker ps --filter name=stalwart
```

1. Verify `infra_net` visibility from the requesting container:

```bash
docker exec -it infra-alertmanager nc -zv mailhog 1025
```

1. Check mail container logs for connection or auth rejections:

```bash
docker logs mailhog
docker logs stalwart
```

1. Confirm the environment variable injected into the requesting container matches the correct port (MailHog uses `1025`, not `25`).

### Stalwart fails to start

- Check the `stalwart_password` secret exists at `secrets/common/stalwart_password.txt`.
- Ensure `${DEFAULT_COMMUNICATION_DIR}/stalwart/data` exists on the host with correct ownership.
- Review logs: `docker logs stalwart`.
