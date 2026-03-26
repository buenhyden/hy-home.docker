# Nginx Runbook

: Path-based Routing & SSO Integration Management

> Runbook for immediate operational tasks and troubleshooting for Nginx.

---

## Overview (KR)

이 런북은 Nginx 프록시의 운영 절차를 정의한다. 설정 오류로 인한 서비스 중단 대응, SSO 연동 문제 해결, 그리고 성능 최적화를 위한 튜닝 절차를 제공한다.

## Purpose

Nginx 서비스 가용성 유지 및 복잡한 라우팅 이슈의 신속한 해결.

## Canonical References

- **ARD**: `[../../02.ard/README.md]`
- **Ops Policy**: `[../../08.operations/01-gateway/nginx.md]`
- **Guide**: `[../../07.guides/01-gateway/nginx.md]`

## When to Use

- Nginx 설정 변경 후 즉시 반영이 필요할 때.
- SSO 인증 후 앱 접근 시 401/403/502 에러가 반복될 때.
- 대용량 파일 업로드 실패 시 (`413 Request Entity Too Large`).
- Healthcheck 실패로 인한 컨테이너 재시작 발생 시.

## Procedure or Checklist

### Checklist

- [ ] `docker exec nginx nginx -t` 성공 여부 확인
- [ ] `infra_net` 상의 타겟 업스트림 핑 응답 확인
- [ ] OAuth2 Proxy 서비스 상태 확인


### Procedure: Configuration Reload

설정 파일 수정 후 서비스 중단 없이 반영하는 단계:

1. 설정 파일 문법 검사:
   ```bash
   docker exec nginx nginx -t
   ```
2. 오류가 없을 경우 리로드 실행:
   ```bash
   docker exec nginx nginx -s reload
   ```


### Procedure: Debugging SSO Integration

인증 문제가 발생할 경우 다음을 순차적으로 확인:

1. Nginx 에러 로그 확인:
   ```bash
   docker compose logs -f nginx
   ```
2. `/_oauth2_auth_check` 내부 요청의 응답 코드 확인.
3. Upstream 서비스가 정상 작동 중인지 확인 (`docker compose ps`).
4. `X-Forwarded-Proto`가 `https`로 설정되어 있는지 확인.


### Procedure: Recovery from Healthcheck Failure

Healthcheck 실패 시(`wget` spider 에러):

1. `/ping` 로케이션 설정 확인 (`nginx.conf`).
2. 포트 바인딩 및 컨테이너 내부 80포트 리스닝 상태 확인.
3. `/etc/nginx/certs` 내 인증서 만료 여부 확인.

## Verification Steps

- [ ] `wget -q --spider http://localhost:80/ping` 명령 성공 확인.
- [ ] 브라우저에서 `/app/` 경로 진입 시 SSO 로그인 페이지로 리다이렉트되는지 확인.

## Observability and Evidence Sources

- **Signals**: Nginx Access/Error Logs (`/var/log/nginx/`).
- **Evidence**: `docker exec nginx nginx -V` (컴파일 옵션 및 모듈 확인).

## Safe Rollback

- `/infra/01-gateway/nginx/config/nginx.conf` 파일을 Git 이전 버전으로 복구 후 리로드.

## Agent Operations

- **Prompt Rollback**: `git checkout config/nginx.conf` 후 리로드 요청.
- **Trace Capture**: `docker logs nginx --since 5m` 덤프 생성.

## Related Operational Documents

- **Incident examples**: `[../../10.incidents/README.md]`
- **Postmortem examples**: `[../../11.postmortems/README.md]`
