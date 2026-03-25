<!-- [ID:10-communication:root] -->
# Communication Tier (10-communication)

> External communication services: Dev SMTP trap (MailHog) and Production-capable mail server (Stalwart).

## 1. Overview (KR)

이 티어는 시스템의 외부 통신 인프라를 관리합니다. 개발용 SMTP 트랩 서비스를 제공하여 테스트 중 메일 유출을 방지하고, 운영 환경을 위한 Stalwart 메일 서버를 통해 실제 메일 송수신 기능을 지원합니다.

## 2. Overview

The `10-communication` tier provides robust email infrastructure for the `hy-home.docker` ecosystem. It balances the needs of local development (no-leaks testing) with production-grade SMTP/IMAP services, ensuring secure and reliable data exchange with external entities.

## 3. Structure

```text
10-communication/
├── mail/             # Mail services (MailHog & Stalwart)
└── README.md         # This file
```

## 4. Service Matrix

| Service | Category | Profile | Role |
| :--- | :--- | :--- | :--- |
| **mailhog** | Dev Tool | `communication` | Captures outgoing mail in memory for debugging |
| **stalwart** | Mail Server | `communication` | Multi-node SMTP, IMAP, JMAP, and Sieve server |

## 5. Governance & Persistence

- **Data Path**: Stalwart data is persisted in `${DEFAULT_COMMUNICATION_DIR}/stalwart/data`.
- **Statelessness**: MailHog is entirely stateless; all intercepted mail is lost on restart.
- **Certificates**: Services utilize centralized certificates from `secrets/certs`.
- **Secrets**: Stalwart admin password must be managed via Docker secrets.

---

## Documentation References

- [Mail Services Guide](../../docs/07.guides/10-communication/README.md)
- [Operations Policy](../../docs/08.operations/10-communication/README.md)
- [Recovery Runbook](../../docs/09.runbooks/10-communication/README.md)

Copyright (c) 2026. Licensed under the MIT License.
