---
title: "02-Auth OAuth2 Proxy Runbook"
version: "1.2.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0015"
parent_ids:
- "GDE-0015"
created: "2026-05-17"
---

# 02-Auth OAuth2 Proxy Runbook

## Overview

이 런북은 OAuth2 Proxy 인증 루프, OIDC 장애, CA/issuer/callback 불일치, Redis/Valkey session 장애, logout 경계 혼동, readonly/tmpfs 관련 오류, 설정 검증 실패 상황에 대한 복구 절차를 정의한다.

> Scope: OAuth2 Proxy ForwardAuth Recovery

### Purpose

- 인증 경로 장애를 신속히 복구한다.
- degraded-mode 수행/종료를 통제한다.
- config lint 실패 시 안전하게 롤백한다.

## When to Use

- 로그인 루프(무한 redirect)
- OIDC issuer 접근 실패
- callback `https://auth.${DEFAULT_URL}/oauth2/callback` 거부 또는 state/CSRF 오류
- Keycloak login 후 OAuth2 Proxy cookie/session 생성 실패
- logout 후 Keycloak SSO가 남아 즉시 재로그인되는 현상
- `/ping` healthcheck 실패
- readonly/tmpfs 관련 쓰기 오류
- compose/config 변경 후 런타임 부팅 실패

## Procedure

### Target, approval and safe evidence

저장소 루트의 승인된 Docker context에서 아래에 명시한 서비스만 다룬다.
명령이 runtime을 변경하는 단계는 대상, 영향받는 사용자·소비자, 이전 image/config,
중단 조건이 확인된 별도 승인 뒤에만 수행한다. 원문 로그나 전체 환경·inspect는
출력하지 않는다. 필요한 오류 유형과 횟수는 승인된 운영자가 로컬에서 정제해 전달하며
token, code, cookie, session ID, 사용자·비공개 주소를 증거에서 제외한다.
여러 앱 공통 장애는 [RUN-0099](0099-system-operations.md), cold-start는
[RUN-0098](0098-cold-start-and-reboot.md)이 소유한다.

### Checklist

- [ ] `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh` 성공
- [ ] `bash scripts/hardening/check-all-hardening.sh 02-auth` 실행
- [ ] Proxy의 정제된 인증/backend 오류 요약 오류 패턴 확인

### Steps

1. 기본 진단
   - `/ping` 확인: `docker compose --profile auth exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping`
   - `/ready` 확인: `docker compose --profile auth exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ready`
   - OIDC issuer 확인: `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm`
   - 로그 확인: Proxy의 정제된 인증/backend 오류 요약; 로컬 운영 화면 밖으로 공유하기 전에는 token, authorization code, session id, cookie, email, IP 등 식별자와 credential 후보를 redaction한다.
2. issuer/CA/JWKS 대응
   - tracked issuer는 `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm`이다.
   - root CA mount는 `/etc/ssl/certs/rootCA.pem`, `SSL_CERT_FILE`과 `ssl_insecure_skip_verify=false`를 확인한다.
   - CA 오류를 `ssl_insecure_skip_verify=true`로 우회하지 않는다.
3. callback/state/PKCE 대응
   - Keycloak client `home-proxy-client`의 Valid Redirect URI가 `https://auth.${DEFAULT_URL}/oauth2/callback`인지 확인한다.
   - OAuth2 Proxy config의 `code_challenge_method = "S256"`와 Keycloak client flow가 호환되는지 확인한다.
   - state/CSRF 오류가 있으면 `cookie_domains=.${DEFAULT_URL}`, `cookie_secure=true`, HTTPS 진입, browser stale cookie를 함께 확인한다.
4. session store 대응
   - tracked default는 `OAUTH2_PROXY_SESSION_STORE_TYPE=redis`, `OAUTH2_PROXY_REDIS_CONNECTION_URL=redis://${OAUTH2_PROXY_VALKEY_HOST:-mng-valkey}:6379`이다.
   - shared path는 `mng-valkey`; `dedicated-valkey` profile은 `oauth2-proxy-valkey`를 추가할 뿐이다. 실제 proxy backend 전환은 `OAUTH2_PROXY_VALKEY_HOST`, selected image, entrypoint secret path가 함께 맞을 때만 성립한다.
   - `/ping`은 process health이고 `/ready`는 Redis/Valkey 연결까지 확인한다.
   - Valkey credential rotation 후 기존 sessions는 무효화될 수 있으며 secret 값은 출력하지 않는다.
5. logout 진단
   - `/oauth2/sign_out`만 호출하면 OAuth2 Proxy cookie만 제거된다.
   - Keycloak SSO까지 종료하려면 provider `end_session_endpoint`로 redirect해야 하며, `rd` 대상 domain이 `OAUTH2_PROXY_WHITELIST_DOMAINS=.${DEFAULT_URL}`에 맞아야 한다.
   - 현재 tracked config만으로 모든 app logout이 Keycloak SSO를 끝낸다고 기록하지 않는다.
6. 로그인 루프 대응
   - `OAUTH2_PROXY_COOKIE_DOMAINS`, `OAUTH2_PROXY_WHITELIST_DOMAINS`, `OAUTH2_PROXY_REDIRECT_URL` 정합성 확인
   - `reverse_proxy=true`, trusted proxy/header 설정을 검토한다. Forwarded header spoofing을 허용하는 네트워크 경로가 있으면 중단하고 gateway boundary를 먼저 고친다.
7. readonly/tmpfs 장애 복구
   - 쓰기 대상 경로가 `/tmp`, `/run` 내인지 점검
   - 엔트리포인트/인증서 마운트 경로 권한 확인
8. degraded-mode 절차(승인 필요)
   - 현재 구현에는 자동 fail-open/degraded-mode 전환 명령이 없다. OIDC 장기 장애 시 대상별 대체 관리 경로·인가·rollback이 별도 승인되기 전에는 fail-closed를 유지한다
   - 적용 시간/범위/종료 조건을 티켓에 기록
   - Keycloak 정상화 즉시 기본 fail-closed로 복귀
9. config lint 실패 롤백
   - 직전 정상 커밋으로 compose/config 복원
   - 재기동 후 `/ping`, `/ready`, 인증 플로우 재검증

### Lifecycle, helpers and change acceptance

Proxy의 issuer·CA와 선택 Valkey가 준비되어야 한다. 기본 공유 경로에서 `auth`
선택이 DB/Valkey readiness를 기다린다고 가정하지 않는다. 기존 로컬 image를
사용하는 승인된 대상 기동·중지는 다음과 같다.

```bash
docker compose --profile auth up -d --no-deps --no-build --pull never oauth2-proxy
docker compose stop oauth2-proxy
```

기동 후 `/ping`과 `/ready`, 로그인 callback, 비허용 그룹 거부, logout 범위를
각각 확인한다. Proxy 중지는 ForwardAuth 소비자에 영향을 준다. cfg/CA/secret
파일 변경은 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)에
따른 대상 재생성과 hash 검사로 반영한다. 코드/Dockerfile 변경은 restart로
반영되지 않는다. image가 없거나 build 선택이 불명확하면 [RUN-0086](0086-dependency-version-management.md)의
별도 검토·build 절차로 넘기고 여기서 임의 build/pull하지 않는다.

전용 대안을 승인받은 경우 먼저 Valkey bind 경로의 존재·UID999 권한·용량,
전용 Secret 참조, exporter 포트, Proxy Dockerfile/host/credential 일치를 확인한다.
이미지와 volume 입력이 준비된 뒤에만 아래 순서로 수행한다.

```bash
docker compose --profile dedicated-valkey up -d --no-deps --no-build --pull never oauth2-proxy-valkey
# Valkey healthy를 확인한 다음 실행한다.
docker compose --profile dedicated-valkey up -d --no-deps --no-build --pull never oauth2-proxy-valkey-exporter
docker compose ps oauth2-proxy-valkey oauth2-proxy-valkey-exporter
```

첫 서비스 healthy가 아니면 exporter로 진행하지 않는다. exporter에는 healthcheck가
없으므로 실행 여부와 수집기의 target UP/`redis_up`을 별도로 확인한다. 값·세션
본문·password 인자가 포함될 수 있는 원문 health/inspect/process 출력은 금지한다.
접속 전환은 일치하는 Proxy image·설정·Secret을 별도 승인된 재생성으로 적용한
뒤 `/ready`와 신규 login으로 확인한다. 재시작만으로 build 선택이 바뀌지 않는다.
중지는 Proxy 소비자 영향 확인 → exporter → 전용 Valkey 순서로 대상만 정하며
공유 `mng-valkey`는 이 절차로 중지/flush하지 않는다.

전용 Valkey AOF 손실 시 세션 재로그인이 기본 복구다. exporter는 state가 없으므로
동일 선언으로 재생성하며 DB backup/credential 발급 기능이 없다. 전용 volume
삭제는 소비자 전환·재로그인 영향·보존 disposition이 승인되기 전에는 수행하지
않는다. cleanup을 위해 `down -v`나 `FLUSHALL`을 사용하지 않는다.

### Verification Steps

- [ ] `bash scripts/hardening/check-all-hardening.sh 02-auth` 통과
- [ ] `docker compose --profile auth exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping` 성공
- [ ] 인증 콜백(`/oauth2/callback`) 정상 동작
- [ ] `/ready`가 session store 연결까지 성공
- [ ] `/oauth2/sign_out`과 Keycloak end-session redirect의 효과를 구분해서 기록

### Observability and Evidence Sources

- **Signals**: `/ping`, oauth2-proxy 로그, Keycloak 연결 오류율
- **Evidence to Capture**:
  - Proxy의 정제된 인증/backend 오류 요약
  - Keycloak의 정제된 OIDC 오류 요약
  - check-all-hardening.sh 02-auth 출력

### Safe Rollback or Recovery Procedure

- [ ] 아래 파일을 직전 정상 커밋으로 복원
  - `infra/02-auth/oauth2-proxy/docker-compose.yml`
  - `infra/02-auth/oauth2-proxy/docker-entrypoint.sh`
  - `infra/02-auth/oauth2-proxy/docker-entrypoint.dev.sh`
  - `infra/02-auth/oauth2-proxy/Dockerfile`
  - `infra/02-auth/oauth2-proxy/dev.Dockerfile`
  - `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg`
- [ ] 위 Lifecycle의 승인된 대상 재생성과 hash 점검 수행
- [ ] `/ping` + 로그인 시나리오 재검증

전용 Valkey server/exporter와 인증 health probe는 현재 password를 process 인자로
소비한다. Docker daemon/host process 접근도 credential 신뢰 경계다. full
`docker inspect`, `docker top`/process `ps`, `/proc/*/cmdline`·`environ`, 원문
`.State.Health.Log`는 기록하지 않는다. 서비스명·image identity·health 상태·재시작
횟수·시각처럼 허용된 필드만 사용한다. 실제 유출은 관찰하지 않았으며 credential
전달 방식 수정은 별도 구현 변경으로 검토한다.

## Evidence

- 원문을 제외한 명령 종료 상태·시각·승인 대상·조치와 미검증 항목만 기록한다.
- 실패한 점검, 관찰된 증상과 최종 복구 또는 에스컬레이션 상태를 관련 Task나 incident evidence에 기록한다.

### Shared Valkey outage rehearsal (2026-09-22, owner-approved)

> Historical evidence (not current authority; source: Git history):
> Source: `c26bc8026254`, `docs/05.operations/runbooks/0015-oauth2-proxy.md`, 2026-09-22 owner-approved rehearsal.
>
> `mng-valkey` was stopped for 68 seconds and recreated. Probes every five seconds:
> unauthenticated SSO route 401, `/oauth2/start` 302 and `/ping` OK throughout;
> oauth2-proxy logged no errors and did not restart. The Airflow Celery worker
> logged connection errors and reconnected four seconds after Valkey returned
> without a restart; n8n and its worker restarted twice and were healthy 37 seconds
> after Valkey returned. Not measured: an existing authenticated session during
> the outage, because oauth2-proxy rejects an unsigned cookie before it reaches
> Valkey and no test credentials were used.

위 outage 관찰은 당시 공유 backend와 unauthenticated 요청만 다룬다. 현재 선언
이미지에서 재실행한 결과도, 인증된 기존 세션의 fail-closed 검증도 아니다.

## Rollback or Recovery

이미지 upgrade는 [RUN-0086](0086-dependency-version-management.md)을 따라 release와
설정 변경을 검토한 뒤 격리된 issuer discovery, PKCE callback, ready, ForwardAuth
identity headers, logout와 session 만료를 확인한다. 이전 image로 돌아갈 때
cookie secret과 session-store endpoint를 동일하게 유지하거나 전 사용자 재로그인을
선언한다. config 복구만으로 image/build 내용이 되돌아가지 않는다.


Valkey session state를 잃었거나 호환되지 않으면 ForwardAuth를 fail-closed로 유지하고,
검토된 endpoint와 credential 참조를 복구한 뒤 사용자에게 재인증을 요구한다.
출처가 불명확한 시점의 오래된 session을 복구하거나 login을 유지하기 위해
cookie/client secret을 노출하지 않는다. cookie secret이 바뀌었다면 이전 cookie를
명시적으로 무효화하고 새 Keycloak login을 test한다. session-loss 복구와 upgrade
rollback 경로는 계획된 절차이며 2026-09-20 문서 수정 때 실행하지 않았다.

## Escalation

검증 실패, secret 노출 위험, 파괴적인 data 변경 필요, 또는 예상한 절차 결과와 관찰 상태의 불일치가 나타나면 중단하고 @buenhyden에게 에스컬레이션한다. 수집한 evidence, 시도한 단계와 현재 rollback/recovery 상태를 포함한다. evidence가 local 운영자 환경을 벗어나기 전에 credential, authorization code, token, cookie, session identifier, 필요한 경우 private IP, 개인 account 정보를 가린다.

## Traceability

- Declared parent: [02-Auth OAuth2 Proxy Usage Guide](../guides/0015-oauth2-proxy.md) (`GDE-0015`)
- Governing authority: [02-Auth Architecture Description](../../02.architecture/descriptions/0002-auth-architecture.md) (`AD-0002`)
- Subject peers: [Guide](../guides/0015-oauth2-proxy.md) (`GDE-0015`), [Policy](../policies/0015-oauth2-proxy.md) (`POL-0015`)

## Related Documents

- [Official OAuth2 Proxy Keycloak OIDC provider](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/keycloak_oidc/)
- [Official OAuth2 Proxy configuration overview](https://oauth2-proxy.github.io/oauth2-proxy/configuration/overview/)
- [Official OAuth2 Proxy session storage](https://oauth2-proxy.github.io/oauth2-proxy/configuration/session_storage/)
- [Official OAuth2 Proxy endpoints](https://oauth2-proxy.github.io/oauth2-proxy/features/endpoints/)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0015-oauth2-proxy.md)
- [Operations policy](../policies/0015-oauth2-proxy.md)
