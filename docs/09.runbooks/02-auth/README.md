# Auth Runbook (02-auth)

> Identity & Access Management Maintenance & Recovery (02-auth)

## Overview

이 런북은 `hy-home.docker`의 인증 시스템(02-auth)에서 발생할 수 있는 주요 장애 대응 및 점검 절차를 단계별로 설명한다.

## Target Audience

- System Administrators
- SRE / DevOps Engineers
- On-call Operators

---

## Recovery Procedures

### 1. Keycloak 관리자 계정 복구

관리자 비밀번호를 분실했거나 계정이 잠긴 경우 다음 단계를 거친다.

1. **임시 관리자 생성**:
   ```bash
   docker exec -it keycloak /opt/keycloak/bin/kc.sh bootstrap-admin --user new-admin --password temp-password
   ```
2. **관리자 로그인**: `https://keycloak.${DEFAULT_URL}`에 `new-admin`으로 접속.
3. **기존 계정 수정**: `master` 렐름에서 기존 관리자 계정의 비밀번호를 재설정한다.

### 2. OAuth2 Proxy Cookie Secret 교체

보안 사고가 의심되거나 정기 교체 주기가 도래한 경우.

1. **Secret 생성**: 32바이트 랜덤 문자열 생성.
2. **Secret 업데이트**: `secrets/oauth2_proxy_cookie_secret` 파일 내용 수정.
3. **서비스 재시작**:
   ```bash
   cd infra/02-auth/oauth2-proxy
   docker compose restart oauth2-proxy
   ```
   > [!WARNING]
   > 이 작업은 모든 활성 세션을 즉시 무효화하며 사용자는 다시 로그인해야 함.

### 3. Keycloak 렐름 설정 백업 (Export)

1. **익스포트 실행**:
   ```bash
   docker exec keycloak /opt/keycloak/bin/kc.sh export --dir /opt/keycloak/conf/backups --realm hy-home.realm
   ```
2. **백업 파일 확인**: `/opt/keycloak/conf/backups` 폴더에 JSON 파일이 생성되었는지 확인.

---

## Maintenance Tasks

### 정기 점검 항목

- **로그 확인**: `docker logs keycloak` 및 `docker logs oauth2-proxy`를 통해 오류 발생 여부 확인.
- **인증서 만료**: Traefik에서 관리하는 SSL 인증서의 유효 기간을 확인.
- **데이터베이스 인덱싱**: PostgreSQL의 성능 저하 여부 확인.

## Verification

- [ ] `keycloak/health/ready` 엔드포인트가 `UP`인지 확인.
- [ ] 보호 대상 서비스 접속 시 SSO 흐름이 정상 작동하는지 확인.
- [ ] `mng-valkey` 세션 데이터가 정상적으로 쌓이는지 확인.

## Related Documents

- **Setup Guide**: `[../07.guides/02-auth/01.setup.md]`
- **Operation Policy**: `[../08.operations/02-auth/README.md]`
