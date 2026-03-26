<!-- [ID:10-communication:mail] -->
# ✉️ Mail Infrastructure (mail)

> Production-grade mail server (Stalwart) and development-safe SMTP interceptor (MailHog).

## Overview

이 서비스 유닛은 이메일 송수신을 위한 핵심 인프라를 제공합니다. **Stalwart**는 실제 메일 서비스를 위한 엔터프라이즈급 기능을 제공하며, **MailHog**는 개발 과정에서 외부로 메일이 발송되는 것을 차단하고 로컬에서 확인할 수 있도록 돕습니다.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- **Stalwart Mail Server**: SMTP, IMAP, JMAP 프로토콜 지원 및 관리 UI.
- **MailHog**: 개발용 SMTP 트랩 및 메일 뷰어 UI.
- **Secrets Management**: 관리자 패스워드 주입 로직.
- **Network Configuration**: `infra_net` 연동 및 포트 매핑.

### Out of Scope

- **Domain DNS Management**: DNS 레코드(A, MX) 자체 관리 (클라우드/DNS 공급자 담당).
- **SSL/TLS Certificates Production**: 인증서 발급 프로세스 (Certbot/ZeroSSL 담당).
- **Application Level SMTP Client Logic**: 개별 앱 내의 SMTP 발송 로직.

## Structure

```text
mail/
├── docker-compose.yml    # 서비스 정의 (Stalwart, MailHog)
└── README.md             # This file
```

## Available Scripts

| Command                                        | Description                |
| ---------------------------------------------- | -------------------------- |
| `docker-compose --profile communication up -d` | 통신 티어 서비스 전체 시작 |
| `docker-compose logs -f stalwart`              | Stalwart 로그 모니터링     |
| `docker-compose restart mailhog`               | MailHog 큐 초기화 및 재시작 |

## Configuration

### Environment Variables

| Variable                | Required | Description                                  |
| ----------------------- | -------- | -------------------------------------------- |
| `DEFAULT_URL`           | Yes      | 서비스 접속 주소 베이스 도메인               |
| `DEFAULT_COMMUNICATION_DIR` | Yes  | Stalwart 데이터 저장을 위한 호스트 경로      |
| `SMTP_HOST_PORT`        | No       | 외부 SMTP 수신 포트 (기본: 25)               |
| `STALWART_PORT`         | No       | Stalwart 관리 UI 내부 포트 (기본: 8080)       |

## Related References

- **Guide**: [Mail Services Guide](../../../docs/07.guides/10-communication/mail.md)
- **Operation**: [Mail Operations Policy](../../../docs/08.operations/10-communication/mail.md)
- **Runbook**: [Mail Recovery Runbook](../../../docs/09.runbooks/10-communication/mail.md)

---

Copyright (c) 2026. Licensed under the MIT License.
