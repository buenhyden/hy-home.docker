---
layer: infra
---
# Mail (MailHog + Stalwart)

**Overview (KR):** 개발용 SMTP 트랩(MailHog)과 프로덕션 메일 서버(Stalwart)를 함께 제공하는 서비스 정의입니다.

## Services

| Service | Image | Role | Profile |
| :--- | :--- | :--- | :--- |
| `mailhog` | `mailhog/mailhog:v1.0.1` | Dev SMTP trap — captures all mail in memory | `communication` |
| `stalwart` | `stalwartlabs/stalwart:v0.14` | Production SMTP/IMAP server with TLS and web admin | `communication` |

## Networking

### MailHog (dev)

- **SMTP**: `mailhog:1025` (internal `infra_net`)
- **Web UI**: `https://mailhog.${DEFAULT_URL}` (via Traefik, SSO-protected)

### Stalwart (production)

| Protocol | Internal Port | Host Port |
| :--- | :--- | :--- |
| SMTP | `25` | `${SMTP_HOST_PORT:-25}` |
| Submission | `587` | `${SUBMISSION_HOST_PORT:-587}` |
| SMTPS | `465` | `${SMTPS_HOST_PORT:-465}` |
| IMAPS | `993` | `${IMAPS_HOST_PORT:-993}` |
| ManageSieve | `4190` | `${MANAGESIEVE_HOST_PORT:-4190}` |
| Admin Web UI | `8080` | n/a (via Traefik) |

- **Admin UI**: `https://mail.${DEFAULT_URL}`

## Secrets

| Secret | File | Purpose |
| :--- | :--- | :--- |
| `stalwart_password` | `secrets/common/stalwart_password.txt` | Stalwart admin password |

## Persistence

| Volume | Host Path | Notes |
| :--- | :--- | :--- |
| `stalwart-data` | `${DEFAULT_COMMUNICATION_DIR}/stalwart/data` | Stalwart mail data and config |

> MailHog is stateless — all mail is stored in memory and lost on restart.

## Key Variables

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `SMTP_PORT` / `SMTP_HOST_PORT` | `25` | Stalwart SMTP port |
| `SUBMISSION_PORT` / `SUBMISSION_HOST_PORT` | `587` | Stalwart submission port |
| `SMTPS_PORT` / `SMTPS_HOST_PORT` | `465` | Stalwart SMTPS port |
| `IMAPS_PORT` / `IMAPS_HOST_PORT` | `993` | Stalwart IMAPS port |
| `MANAGESIEVE_PORT` / `MANAGESIEVE_HOST_PORT` | `4190` | Stalwart sieve port |
| `STALWART_PORT` | `8080` | Stalwart web admin port |
| `MAILHOG_UI_PORT` | `8025` | MailHog web UI port |
| `DEFAULT_COMMUNICATION_DIR` | `${DEFAULT_MOUNT_VOLUME_PATH}/comm` | Host path for Stalwart data |

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | MailHog and Stalwart service definitions. |
| `README.md` | Service overview (this file). |

## Documentation References

- [Mail Relay Guide](../../../docs/guides/10-communication/mail-relay-operations.md) — MailHog operational guide
- [Mail Server Guide](../../../docs/guides/10-communication/mail-server-operations.md) — Combined MailHog + Stalwart operations
- [Mail Context](../../../docs/guides/10-communication/mail-context.md) — Architecture, lifecycle, integration points
