# Mail Service (MailHog)

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 개발 및 테스트 환경을 위한 이메일 테스팅 도구입니다. 애플리케이션에서 발송하는 SMTP 메일을 가로채서 웹 UI로 보여줍니다. 실제 외부로 메일을 발송하지 않습니다.

**주요 기능 (Key Features)**:
- **SMTP Capture**: 모든 발송 메일 수신.
- **Web UI**: 수신된 메일 열람 및 검색.
- **Chaos Monkey**: 무작위 지연/실패 시뮬레이션 기능(Jim).

**기술 스택 (Tech Stack)**:
- **Tool**: MailHog (Go 기반)

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
- **App** -> **SMTP (1025)** -> **MailHog** (In-memory Storage) -> **Web UI (8025)**

## 3. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```

## 4. 환경 설정 명세 (Configuration Reference)
**네트워크 포트**:
- **SMTP**: 1025 (내부 서비스용, `mailhog:1025`)
- **HTTP**: 8025 (`https://mail.${DEFAULT_URL}`)

## 5. 통합 및 API 가이드 (Integration Guide)
**애플리케이션 설정 (예: Django/Spring)**:
- Host: `mailhog`
- Port: `1025`
- Auth: None (인증 불필요)

**API**:
- `/api/v2/messages`: 수신된 메시지 JSON 목록.

## 6. 가용성 및 관측성 (Availability & Observability)
**상태 확인**: 웹 UI 접속 가능 여부(`https://mail.${DEFAULT_URL}`).

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 보존**:
- 기본 설정상 **인메모리** 저장소이므로 컨테이너 재시작 시 **메일이 모두 삭제**됩니다.
- 영구 보존이 필요하다면 `MongoDB` 등을 백엔드로 연결해야 합니다.

## 8. 보안 및 강화 (Security Hardening)
- **SSO**: 웹 UI (`/`) 접근 시 `sso-auth` 미들웨어를 통해 Keycloak 인증을 거치도록 설정되어 있습니다.

## 9. 트러블슈팅 (Troubleshooting)
**참고 사항**:
- `Stalwart Mail Server` 설정은 `docker-compose.yml` 내에 주석 처리되어 있습니다. 상용 수준의 메일 서버가 필요한 경우 주석을 해제하여 사용하십시오.
