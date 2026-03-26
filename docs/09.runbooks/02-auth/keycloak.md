# Keycloak Runbook

: Identity and Access Management (IAM)

---

## Overview (KR)

이 런북은 Keycloak 서비스의 일상적인 운영 작업, 유지보수, 그리고 긴급 복구 절차를 정의한다. 시스템 관리자와 운영자가 즉시 실행할 수 있는 명령형 가이드를 제공한다.

## Purpose

- Keycloak 서비스 가동 및 중지 절차 확립
- 관리자 계정 분실 및 잠금 해제 등 긴급 대응
- 렐름 데이터 백업 및 복구 프로세스 표준화

## Canonical References

- ARD: `[../../docs/02.ard/02-auth-architecture.md]`
- Setup Guide: `[../../docs/07.guides/02-auth/keycloak.md]`
- Operations Policy: `[../../docs/08.operations/02-auth/keycloak.md]`

## When to Use

- 서비스 초기 기동 및 재시작 시
- 관리자 패스워드 재설정이 필요한 경우
- 시스템 업그레이드 전후 데이터 백업 시

## Procedure or Checklist

### Checklist

- [ ] `infra/04-data/mng-db` (PostgreSQL) 정상 상태 확인
- [ ] `keycloak` 컨테이너 로그의 에러 메세지 유무 확인
- [ ] 관리 콘솔(`https://keycloak.${DEFAULT_URL}`) 접속 가능 여부

### Procedure

#### 1. 서비스 재시작 및 상태 확인

```bash
cd infra/02-auth/keycloak
docker compose restart keycloak
docker logs -f keycloak
```

#### 2. 임시 관리자 계정 생성 (Password Lost)

```bash
# Keycloak 컨테이너 내에서 임시 관리자 생성 (Quarkus distribution)
docker exec -it keycloak /opt/keycloak/bin/kc.sh bootstrap-admin --user emergency-admin --password temp-password-123
```

> 생성 후 브라우저에서 로그인하여 기존 계정 복구 후 임시 계정 삭제 권장.

#### 3. 렐름 데이터 익스포트 (Backup)

```bash
docker exec keycloak /opt/keycloak/bin/kc.sh export --dir /opt/keycloak/conf/backups --realm hy-home.realm
```

## Verification Steps

- [ ] `docker exec keycloak /opt/keycloak/bin/kc.sh show-config` 실행 시 오류 없음 확인.
- [ ] `curl -f https://keycloak.${DEFAULT_URL}/health/live` 응답 확인.

## Safe Rollback or Recovery Procedure

- **DB Recovery**: Keycloak 데이터 정합성 오류 시 `infra/04-data/mng-db`의 PostgreSQL 스냅샷으로 복구.
- **Config Rollback**: `infra/02-auth/keycloak/conf/`의 이전 설정 파일 복원 후 재시작.

## Related Operational Documents

- **Incident Table**: `[../../docs/10.incidents/README.md]`
- **Postmortem**: `[../../docs/11.postmortems/README.md]`
