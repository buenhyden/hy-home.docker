<!-- Target: docs/09.runbooks/10-communication-maintenance-runbook.md -->

# Maintenance Runbook - 10-communication

## Overview (KR)
이 문서는 `10-communication` 티어 유지보수 및 장애 대응을 위한 실행 절차를 정의한다.

## Maintenance Procedures

### 1. 메일 서버 재시작 및 상태 확인
```bash
# Docker Compose 서비스 재시작
docker compose -f infra/10-communication/docker-compose.yml restart stalwart

# 서비스 로그 확인
docker compose -f infra/10-communication/docker-compose.yml logs -f stalwart
```

### 2. 저장 공간 확장
- Stalwart 데이터 볼륨의 사용률이 80%를 초과할 경우 호스트 디스크 확장을 검토한다.

## Incident Response

### Case 1: 메일 발송 지연 (Queue Backlog)
- **증상**: 메일 발송 요청 후 수신측에 도착하지 않음.
- **조치**:
    1. Stalwart 관리 UI에서 송신 큐(Outgoing Queue) 상태 조회.
    2. 수신측 메일 서버의 거부 이유(SMTP 5xx) 확인.
    3. SPF/DKIM 설정 누락 여부 점검.

### Case 2: 인증 오류 (Authentication Failure)
- **증상**: 클라이언트 로그인 실패.
- **조치**:
    1. Keycloak SSO 서버 가동 여부 확인.
    2. OIDC 연동 설정(Client Secret 등) 만료 여부 확인.
    3. Stalwart 로그에서 인증 프로바이더 연결 상태 확인.

## Backup & Recovery

- **Backup**: `docker exec`를 사용하여 Stalwart 데이터베이스 덤프 및 파일 시스템 스냅샷 수행.
- **Recovery**: 새 호스트에서 볼륨을 복구한 후 컨테이너를 실행하여 서비스 복구.
