# Mail Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 메일 관련 서비스를 정의합니다. 현재 개발 및 테스트 환경을 위한 SMTP 테스트 도구인 MailHog가 활성화되어 있으며, 운영용 메일 서버인 Stalwart Mail Server는 비활성화(주석 처리)되어 있습니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **mailhog** | SMTP Web Client | 개발용 가상 SMTP 서버입니다. 발송된 메일을 실제로 전송하지 않고 웹 UI에서 가로채 확인할 수 있습니다. |
| **stalwart** | Mail Server | (현재 비활성) 완전한 기능을 갖춘 Mail Server(SMTP, IMAP, JMAP 등) 솔루션입니다. |

## 3. 구성 및 설정 (Configuration)

### MailHog (Active)
- **SMTP Port**: 내부적으로 1025 포트를 사용하여 애플리케이션의 메일 발송 요청을 수신합니다.
- **Web UI**: Traefik을 통해 `https://mail.${DEFAULT_URL}` (또는 `mailhog` 라우터 규칙)로 접속하여 수신된 메일을 확인할 수 있습니다.
- **Access Control**: SSO 미들웨어(`sso-auth`)가 적용될 수 있도록 라벨이 설정되어 있습니다.

### Stalwart (Inactive)
- 활성화 시 SMTP, Submission, SMTPS, IMAPS 등 다양한 보안 메일 포트를 호스트에 직접 노출하도록 설정되어 있습니다.
- 관리자 UI는 Traefik을 통해 접속 가능합니다.
