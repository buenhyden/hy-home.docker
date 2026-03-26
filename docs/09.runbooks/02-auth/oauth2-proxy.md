# OAuth2 Proxy Runbook

> Step-by-step procedures for troubleshooting and maintaining the OAuth2 Proxy service.

---

## Overview (KR)

이 문서는 OAuth2 Proxy 서비스의 장애 대응 및 복구를 위한 실행 지침서다. 세션 저장소 연결 오류, 인증 루프, 그리고 쿠키 유효성 문제에 대한 해결 방법을 다룬다.

## Runbook Type

`incident-response | maintenance`

## Target Audience

- Operator
- SRE
- Agent-tuner

## Incident Response

### 1. Internal Server Error (500)
- **Problem**: OAuth2 Proxy가 500 에러를 반환함.
- **Diagnosis**: `docker logs oauth2-proxy`를 통해 로그 확인.
- **Solution**:
  - Valkey 세션 저장소 연결 오류인 경우: `infra/04-data/valkey` 서비스 상태 확인 및 재시작.
  - OIDC Issuer (Keycloak) 연결 오류인 경우: Keycloak 서비스 가용성 확인.

### 2. Login Loop (Infinite Redirect)
- **Problem**: 로그인 후 계속해서 로그인 페이지로 리다이렉트됨.
- **Diagnosis**: 브라우저 개발자 도구의 Network 탭에서 쿠키 전송 여부 확인.
- **Solution**:
  - `cookie_domains` 설정이 현재 접근하는 도메인과 일치하는지 확인.
  - `cookie_secure`가 `true`인데 HTTP로 접근 중인지 확인 (HTTPS 필수).

### 3. Invalid Cookie / Session Expired
- **Problem**: 유효한 세션임에도 불구하고 인증이 거부됨.
- **Solution**:
  - `cookie_secret`이 변경되었는지 확인 (변경 시 기존 모든 세션 무효화됨).
  - 클라이언트 시스템 시계 동기화 여부 확인.

## Maintenance Tasks

### Session Clearing
Valkey에서 특정 유저의 세션을 강제로 만료시켜야 하는 경우:
```bash
docker exec -it mng-valkey valkey-cli
> KEYS "oauth2_proxy_session:*"
> DEL "oauth2_proxy_session:<session_id>"
```

## Related Documents

- **Guide**: `[../../07.guides/02-auth/oauth2-proxy.md]`
- **Operation**: `[../../08.operations/02-auth/oauth2-proxy.md]`
- **Spec**: `[../../04.specs/02-auth/oauth2-proxy.md]`
