# Keycloak Runbook

> Step-by-step procedures for troubleshooting and maintaining the Keycloak security layer.

---

## Overview (KR)

이 런북은 Keycloak 서비스의 장애 상황(Healthcheck Failure, OIDC Redirect Mismatch, IdP Sync Error)에 대한 대응 절차와 복구 방법을 다룬다.

## Runbook Type

`incident-response | maintenance`

## Target Audience

- SRE / Platform Engineers
- Auth Feature Developers
- On-call Responders

## Incident Response

### 1. Health Readiness Failure
- **Problem**: Keycloak이 `9000/health/ready`에서 `Down` 상태를 반환함.
- **Diagnosis**: 
  ```bash
  docker logs keycloak
  # Check PostgreSQL connection status
  docker exec keycloak curl -f http://localhost:9000/health/live
  ```
- **Solution**: 
  - DB 연결 문제 시 `mng-pg` 상태 확인.
  - OOM 또는 리소스 부족 시 컨테이너 재시작.

### 2. OIDC Redirect Mismatch
- **Problem**: 로그인 시도 시 `Invalid parameter: redirect_uri` 오류 발생.
- **Diagnosis**: 브라우저 주소창의 `redirect_uri`와 Keycloak Client 설정 비교.
- **Solution**: Keycloak 콘솔 -> Clients -> 해당 Client -> **Valid Redirect URIs**에 정확한 도메인(와일드카드 주의) 추가.

### 3. External IdP Reconciliation
- **Problem**: Google 로그인 등이 작동하지 않음.
- **Diagnosis**: 
  - Keycloak 서버 로그에서 401/403 오류 확인.
  - IdP 제공자(Google Cloud)의 Client ID/Secret 유효성 확인.
- **Solution**: Identity Providers 메뉴에서 IdP 재연동 및 시크릿 업데이트.

## Maintenance Tasks

### 1. Realm Configuration Export/Import
데이터 백업 및 레이아웃 동기화를 위해 수동 엑스포트를 권장함:
```bash
# Export Realm with Users
docker exec keycloak /opt/keycloak/bin/kc.sh export --realm hy-home --file /tmp/hy-home-realm.json --users same_file
```

### 2. Theme & Provider Update
신규 테마 또는 JAR 파일을 반영하려면 볼륨 마운트 확인 후 서비스를 재시작함:
```bash
docker compose restart keycloak
```

## Related Documents

- **Guide**: `[../../07.guides/02-auth/keycloak.md]`
- **Operation**: `[../../08.operations/02-auth/keycloak.md]`
- **Spec**: `[../../04.specs/02-auth/keycloak.md]`
