<!-- Target: docs/07.guides/10-communication-user-guide.md -->

# User Guide - 10-communication

## Overview (KR)
이 문서는 `10-communication` 계층의 서비스를 사용하는 사용자를 위한 가이드이다. 개발용 SMTP 트랩(MailHog)과 운영용 메일 서버(Stalwart) 접속 방법을 설명한다.

## Getting Started

### 1. 개발 환경 메일 테스트 (MailHog)
애플리케이션 개발 중에는 모든 메일이 MailHog로 트랩되어 실제 외부로 발송되지 않는다.
- **SMTP Host**: `mailhog` (Internal) / `localhost` (Port Forwarding)
- **SMTP Port**: `1025`
- **Authentication**: 필요 없음 (None)
- **Web UI**: `http://localhost:8025` 또는 Traefik을 통한 설정된 도메인.

### 2. 운영 환경 메일 설정 (Stalwart)
운영 환경에서는 인증된 SMTP 서버를 사용해야 한다.
- **SMTP Host**: `mail.yourdomain.com`
- **Ports**: 
    - `465` (SSL/TLS 강제)
    - `587` (STARTTLS 강제)
- **Username**: 전체 이메일 주소 (예: `user@yourdomain.com`)
- **Password**: Keycloak 또는 Stalwart 계정 비밀번호.

## Key Features

- **JMAP Support**: 현대적인 JMAP 프로토콜을 지원하여 빠른 동기화 가능.
- **Web Interface**: Stalwart 관리 인터페이스를 통해 도메인 및 별칭 설정 가능.

## Troubleshooting

- **메일 수신 불가**: MX 레코드가 올바른 서버 IP를 가리키고 있는지 확인한다.
- **발송 실패**: 포트 25번이 호스트 서버에서 개방되어 있는지 확인한다.
- **인증 오류**: TLS 설정을 '강제(Required)'로 설정했는지 확인한다.
