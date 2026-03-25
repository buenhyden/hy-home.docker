<!-- [ID:10-communication:root] -->
# 📬 Communication Tier (10-communication)

> Centralized communication infrastructure providing development-safe SMTP trapping and production-grade mail services.

## 1. 개요 (KR)
이 티어는 시스템의 외부 통신 인프라를 관리합니다. 개발 및 테스트를 위한 이메일 캡처 서비스인 **MailHog**와 실운영 환경을 위한 고성능 메일 서버인 **Stalwart**를 제공합니다. 모든 통신은 중앙 집중식 인증서와 보안 정책을 따르도록 설계되었습니다.

## 2. Infrastructure Overview
The `10-communication` tier balances high-fidelity mail processing with testing safety. It ensures that outgoing notifications are either trapped for inspection (Dev) or securely delivered to external recipients (Prod) via modern authenticated protocols.

## 3. Technology Stack

| Component | Technology | Role | Persistence |
| :--- | :--- | :--- | :--- |
| **SMTP Trap** | `MailHog v1.0.1` | Dev SMTP Interface | Stateless (In-memory) |
| **Mail Server** | `Stalwart v0.14` | IMAP/SMTP/JMAP | Local Bind Mount |
| **Security** | `SSO / TLS` | Auth & Encryption | secrets/certs |

## 4. Implementation Snippet

```yaml
# 10-communication core services
services:
  stalwart:
    image: stalwartlabs/stalwart:v0.14
    volumes:
      - stalwart-data:/opt/stalwart
      - ../../../secrets/certs:/opt/stalwart/certs:ro
    # Port 25 for SMTP, 587/465 for Submission, 993 for IMAPS
  
  mailhog:
    image: mailhog/mailhog:v1.0.1
    # SSO protected UI for dev testing
```

## 5. Directory Structure
```text
10-communication/
├── mail/             # Core mail services (docker-compose)
└── README.md         # This entry point
```

## 6. Persistence & Security
- **Stateless Debugging**: MailHog captures are lost on restart, preventing sensitive data accumulation.
- **Encrypted Storage**: Stalwart volumes store encrypted mail data and account configurations.
- **Edge Protection**: MailHog is protected by Traefik SSO middleware; Stalwart exposes native SSL ports.

---

## 🔗 Documentation Links
- **Guides**: [Mail Setup & Logic](../../docs/07.guides/10-communication/README.md)
- **Operations**: [SPF/DKIM/DMARC Policy](../../docs/08.operations/10-communication/README.md)
- **Runbooks**: [Delivery Recovery](../../docs/09.runbooks/10-communication/README.md)

Copyright (c) 2026. Licensed under the MIT License.
