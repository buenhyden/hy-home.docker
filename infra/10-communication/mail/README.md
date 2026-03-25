<!-- [ID:10-communication:mail] -->
# ✉️ Mail Infrastructure (mail)

> Production-grade mail server (Stalwart) and development-safe SMTP interceptor (MailHog).

## 1. 개요 (KR)
이 서비스 유닛은 이메일 송수신을 위한 핵심 인프라를 제공합니다. **Stalwart**는 실제 메일 서비스를 위한 엔터프라이즈급 기능을 제공하며, **MailHog**는 개발 과정에서 외부로 메일이 발송되는 것을 차단하고 로컬에서 확인할 수 있도록 돕습니다.

## 2. Implementation Details

| Service | Image | Internal Ports | External Access |
| :--- | :--- | :--- | :--- |
| **Stalwart** | `stalwartlabs/stalwart:v0.14` | 8080 (UI), 25, 587, 465, 993 | `mail.${DEFAULT_URL}` |
| **MailHog** | `mailhog/mailhog:v1.0.1` | 8025 (UI), 1025 (SMTP) | `mailhog.${DEFAULT_URL}` |

## 3. Key Configurations

### Stalwart (Production)
- **Auth**: Docker Secret(`stalwart_password`)을 통해 관리자 패스워드를 주입합니다.
- **Storage**: `/opt/stalwart` 볼륨을 통해 메일 데이터 및 구성을 유지합니다.
- **Security**: SPF, DKIM, DMARC 설정이 필요하며 포트 25 차단 여부를 ISP에서 확인해야 합니다.

### MailHog (Development)
- **Trap**: 모든 앱의 SMTP 설정을 `mailhog:1025`로 설정하여 실발송을 방지합니다.
- **SSO**: 배포된 환경의 UI는 Keycloak/DEX를 통해 보호됩니다.
- **Ephemeral**: 메모리 기반 저장소를 사용하여 재시작 시 모든 데이터가 휘발됩니다 (보안/청소 용이).

## 4. Quick Start
```bash
# Start communication tier
docker-compose --profile communication up -d
```

---

## 🔗 Internal References
- [Guide: Mail Server Setup](../../../docs/07.guides/10-communication/01.mail-server-setup.md)
- [Runbook: Delivery Troubleshooting](../../../docs/09.runbooks/10-communication/README.md)

Copyright (c) 2026. Licensed under the MIT License.
