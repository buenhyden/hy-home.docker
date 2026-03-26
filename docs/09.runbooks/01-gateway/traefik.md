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

### Procedure: Manual Config Reload
정적 설정이 아닌 동적 설정(`dynamic/`) 변경 시 Traefik은 자동으로 감지하지만, 강제 적용이 필요한 경우 다음을 실행한다.

1. 컨테이너 내부로 재시그널 전송:
   ```bash
   docker exec traefik kill -HUP 1
   ```
2. 대시보드에서 규칙이 정상적으로 로드되었는지 확인.

### Procedure: SSL Certificate Renewal
1. 새로운 인증서 파일(`cert.pem`, `key.pem`)을 `secrets/certs/` 폴더에 복사한다.
2. Traefik이 파일을 다시 읽게 하거나 컨테이너를 재시작한다.
   ```bash
   docker compose restart traefik
   ```
3. `openssl` 명령으로 갱신 여부를 확인한다:
   ```bash
   echo | openssl s_client -connect dashboard.${DEFAULT_URL}:443 2>/dev/null | openssl x509 -noout -dates
   ```

## Verification Steps

- [ ] `docker exec traefik traefik healthcheck --ping` 결과가 `OK`인지 확인.
- [ ] 브라우저에서 `https://dashboard.${DEFAULT_URL}` 접속 및 인증서 유효성 확인.

## Observability and Evidence Sources

- **Signals**: Traefik Dashboard, Prometheus Metrics (`:8082/metrics`).
- **Evidence**: `docker compose logs --tail=100 traefik`.

## Safe Rollback

- `/infra/01-gateway/traefik` 폴더에서 Git 커밋을 이전 상태로 되돌리고 `docker compose up -d --force-recreate`를 실행한다.

## Related Operational Documents

- **Incident examples**: `[../../10.incidents/README.md]`
- **Postmortem examples**: `[../../11.postmortems/README.md]`
