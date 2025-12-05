# 메일 서버 (MailHog)

## 시스템 아키텍처에서의 역할

MailHog는 **개발/테스트용 SMTP 서버 및 메일함**으로 실제 이메일을 발송하지 않고 테스트할 수 있는 환경을 제공합니다.

**핵심 역할:**

- 📧 **테스트 메일 수신**: 개발 중 이메일 테스트
- 🔍 **메일함 UI**: 웹 기반 메일 뷰어
- 🚫 **실제 발송 방지**: 안전한 테스트 환경

## 주요 구성 요소

### MailHog

- **컨테이너**: `mailhog`
- **이미지**: `mailhog/mailhog`
- **SMTP**: 1025 (내부)
- **WebUI**: `${MAILHOG_UI_PORT}` (기본 8025)
- **Traefik**: `https://mail.${DEFAULT_URL}`

## 환경 변수

```bash
MAILHOG_UI_PORT=8025
DEFAULT_URL=127.0.0.1.nip.io
```

## 사용 방법

### 애플리케이션 설정

```yaml
SMTP_HOST: mailhog
SMTP_PORT: 1025
SMTP_USER: (none)
SMTP_PASSWORD: (none)
```

### 메일 확인

- **URL**: `https://mail.127.0.0.1.nip.io`

## 참고 자료

- [MailHog GitHub](https://github.com/mailhog/MailHog)
