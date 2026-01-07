# Mail Service (MailHog)

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 개발 및 테스트 환경을 위한 이메일 테스팅 도구입니다.  
애플리케이션에서 발송하는 SMTP 트래픽을 가로채서 실제 외부 발송 없이 웹 UI에서 전송된 메일을 확인하고 검증할 수 있게 해줍니다.

## 2. 주요 기능 (Key Features)
- **SMTP Capture**: SMTP 프로토콜(1025 포트)로 들어오는 모든 메일을 수집하고 저장합니다.
- **Web UI**: 수신된 메일의 내용, 헤더, 첨부파일을 웹 브라우저에서 편리하게 열람할 수 있습니다.
- **Jim (Chaos Monkey)**: 네트워크 지연이나 전송 실패와 같은 장애 상황을 시뮬레이션하여 애플리케이션의 예외 처리를 테스트할 수 있습니다.
- **In-Memory Storage**: 별도의 DB 설정 없이 가볍게 실행 가능합니다 (컨테이너 재시작 시 데이터 초기화).

## 3. 기술 스택 (Tech Stack)
- **Image**: `mailhog/mailhog:latest`
- **Language**: Go
- **Protocol**: SMTP (ESMTP), HTTP

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 데이터 흐름
1.  **Application**: 메일 발송 로직 실행 (`Host: mailhog`, `Port: 1025`).
2.  **MailHog**: SMTP 요청을 수신하여 메모리에 저장.
3.  **User**: 웹 브라우저로 접속 (`https://mail.${DEFAULT_URL}`)하여 메일 확인.

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **참고**: `Stalwart Mail Server` 설정은 `docker-compose.yml` 파일 내에 주석으로 포함되어 있습니다. 실제 프로덕션 레벨의 메일 서버가 필요한 경우 해당 주석을 해제하여 사용하십시오.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 Web UI 사용
1.  **접속**: `https://mail.${DEFAULT_URL}`
2.  **기능**:
    - **Inbox**: 수신된 메일 리스트 확인.
    - **Search**: 제목, 보낸 사람, 내용 등으로 메일 검색.
    - **Delete All**: 테스트 메일 일괄 삭제.
    - **Release**: (설정 시) 실제 외부 SMTP 서버로 메일을 릴레이(Relay)하여 발송 시도.

### 6.2 Chaos Monkey (Jim) 설정
애플리케이션의 견고성을 테스트하기 위해 무작위 실패를 유발할 수 있습니다.
- **Enable**: 컨테이너 환경 변수로 `MH_JIM_ENABLE=true` 설정 (현재 기본값은 미설정).

## 7. 환경 설정 명세 (Configuration Reference)
### 네트워크 포트 (Ports)
- **SMTP**: 1025 (내부 서비스용, 인증 불필요).
- **HTTP**: 8025 (웹 UI용, Traefik을 통해 80/443으로 노출).

### 환경 변수 (Environment Variables)
- `MH_STORAGE`: `memory` (기본값) 또는 `mongodb` (영구 저장 시).
- `MH_SMTP_BIND_ADDR`: `0.0.0.0:1025`

## 8. 통합 및 API 가이드 (Integration Guide)
**애플리케이션 연동 설정**:
- **Host**: `mailhog`
- **Port**: `1025`
- **Username/Password**: 없음 (Null 또는 임의 값 입력)
- **TLS/SSL**: `None` (또는 `STARTTLS`, MailHog는 자체 인증서를 가짐)

**REST API**:
- **Get Messages**: `GET /api/v2/messages`
- **Delete Messages**: `DELETE /api/v1/messages`

## 9. 가용성 및 관측성 (Availability & Observability)
**상태 확인**:
- 웹 UI(`https://mail.${DEFAULT_URL}`) 접속이 가능하다면 정상 동작 중입니다.
- Health Check 명령: `wget -qO- http://localhost:8025/api/v2/messages > /dev/null`

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 보존**:
- 현재 설정은 **In-Memory** 모드이므로 컨테이너 재시작 시 모든 메일 데이터가 삭제됩니다.
- 테스트 목적의 도구이므로 별도의 백업은 권장되지 않으나, 필요시 MongoDB 백엔드를 구성해야 합니다.

## 11. 보안 및 강화 (Security Hardening)
- **Web UI Auth**: Traefik 미들웨어(`sso-auth`)가 적용되어 있어 Keycloak 로그인이 필요합니다.
- **SMTP Open Relay**: 1025 포트는 내부 네트워크(`infra_net`)에만 노출되어 외부 스팸 발송용으로 악용되는 것을 방지합니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **메일 미수신**: 애플리케이션과 MailHog가 동일한 Docker Network(`infra_net`)에 있는지 확인하세요.
- **포트 충돌**: 호스트의 1025, 8025 포트가 이미 사용 중인지 확인하세요.

---
**공식 저장소**: [https://github.com/mailhog/MailHog](https://github.com/mailhog/MailHog)
