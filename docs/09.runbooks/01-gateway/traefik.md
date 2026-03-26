# Traefik Runbook

: Gateway Routing & TLS Management

> Runbook for immediate operational tasks and troubleshooting for Traefik.

---

## Overview (KR)

이 런북은 Traefik 에지 라우터의 운영 절차를 정의한다. 인증서 갱신, 서비스 장애 발생 시의 문제 해결 절차, 그리고 비상 복구 단계를 제공한다.

## Purpose

Traefik 서비스 가용성 확보 및 SSL/TLS 관련 운영 이슈 해결.

## Canonical References

- **ARD**: `[../../02.ard/README.md]`
- **Ops Policy**: `[../../08.operations/01-gateway/traefik.md]`
- **Guide**: `[../../07.guides/01-gateway/traefik.md]`

## When to Use

- Traefik 컨테이너 중단 또는 재시작 필요 시.
- SSL 인증서 만료 임박 및 수동 갱신 시.
- 특정 도메인으로의 접근이 불가능할 경우(502/504 Bad Gateway).

## Procedure or Checklist

### Procedure: Recovery from Healthcheck Failure

Traefik 헬스체크 실패(Ping 응답 없음) 시:

1. `config/traefik.yml` 내 `ping` 엔드포인트 설정 확인.
2. `metrics` 엔드포인트(Port 8082) 리스닝 상태 확인.
3. Docker Socket 접근 권한 (`traefik.yml`의 `endpoint`) 확인.

### Procedure: Debugging ForwardAuth SSO

SSO 인증 중단 시 체크리스트:

1. OAuth2 Proxy 서비스 상태 확인 (`docker compose ps oauth2-proxy`).
2. `dynamic/middleware.yml`의 `address` 오타 여부 확인.
3. 브라우저 개발자 도구의 `Authorization` 헤더 포함 여부 확인.

## Verification Steps

- [ ] `docker exec traefik traefik healthcheck --ping` 결과가 `OK`인지 확인.
- [ ] 브라우저에서 `https://dashboard.${DEFAULT_URL}` 접속 및 인증서 유효성 확인.
- [ ] 특정 보호 경로 진입 시 Keycloak 로그인 창으로 리다이렉트되는지 확인.

## Observability and Evidence Sources

- **Signals**: Traefik Dashboard, Prometheus Metrics (`:8082/metrics`).
- **Evidence**: `docker compose logs --tail=100 traefik`.

## Safe Rollback

- `/infra/01-gateway/traefik` 폴더에서 Git 커밋을 이전 상태로 되돌리고 `docker compose up -d --force-recreate`를 실행한다.

## Related Operational Documents

- **Incident examples**: `[../../10.incidents/README.md]`
- **Postmortem examples**: `[../../11.postmortems/README.md]`
