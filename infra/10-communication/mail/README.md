<!-- [ID:10-communication:mail] -->
# Mail Services (Stalwart + MailHog)

> Combined mail infrastructure providing both production-grade services and development traps.

## 1. Overview (KR)

이 서비스는 시스템의 이메일 송수신을 담당합니다. **Stalwart**는 실제 운영 및 사용자 메일 서비스를 위한 SMTP/IMAP 서버이며, **MailHog**는 개발 및 테스트 중 외부로 메일이 발송되지 않도록 모든 메일을 캡처하는 안전한 트랩 역할을 합니다.

## 2. Overview

The `mail` services manage the full lifecycle of electronic correspondence in `hy-home.docker`. Stalwart provides a modern, high-performance mail server implementation, while MailHog ensures a "no-leak" development environment by capturing all SMTP traffic in memory for inspection.

## 3. Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **stalwart** | Stalwart Mail v0.14 | Production SMTP/IMAP/JMAP Server |
| **mailhog** | MailHog v1.0.1 | Dev SMTP Trap & Web UI |

## 4. Networking

### External Access (Web UI)

| Service | Rule | Entrypoint |
| :--- | :--- | :--- |
| **stalwart-ui** | `mail.${DEFAULT_URL}` | `websecure` |
| **mailhog** | `mailhog.${DEFAULT_URL}` | `websecure` |

### Protocol Ports (Stalwart)

| Protocol | Port | Description |
| :--- | :--- | :--- |
| **SMTP** | `25` | Standard mail exchange |
| **Submission** | `587` | Message submission (STARTTLS) |
| **SMTPS** | `465` | Secure SMTP (TLS) |
| **IMAPS** | `993` | Secure IMAP access |

### Dev Access (MailHog)

- **SMTP Trap**: `mailhog:1025` (internal `infra_net`)
- **API/UI**: `http://mailhog:8025`

## 5. Persistence & Secrets

- **Volumes**: `stalwart-data` -> `${DEFAULT_COMMUNICATION_DIR}/stalwart/data`.
- **Secrets**: `stalwart_password` (Admin password management).
- **Statelessness**: MailHog is stateless; no persistent volume is attached.
- **Certificates**: Mounted from `../../../../secrets/certs`.

## 6. File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Service definitions for Stalwart and MailHog. |
| `README.md` | This overview file. |

---

## Documentation References

- [Mail Services Setup Guide](../../../docs/07.guides/10-communication/mail-services-guide.md)
- [Mail Operations Policy](../../../docs/08.operations/10-communication/mail-ops-policy.md)
- [Stalwart Recovery Runbook](../../../docs/09.runbooks/10-communication/stalwart-recovery.md)

Copyright (c) 2026. Licensed under the MIT License.
