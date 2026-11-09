---
title: "02-Auth OAuth2 Proxy Operations Policy"
version: "1.2.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-09"
layer: "operations"
artifact_id: "POL-0015"
parent_ids:
- "AD-0002"
created: "2026-05-17"
---

# 02-Auth OAuth2 Proxy Operations Policy

## Overview

이 문서는 `02-auth` OAuth2 Proxy 운영 정책을 정의한다. 시크릿 주입 경로, 세션/쿠키 표준, fail-closed 및 degraded-mode 운영 통제를 명시한다.

## Scope

- `infra/02-auth/oauth2-proxy/docker-compose.yml`
- `infra/02-auth/oauth2-proxy/docker-entrypoint.sh`
- `infra/02-auth/oauth2-proxy/docker-entrypoint.dev.sh`
- `infra/02-auth/oauth2-proxy/Dockerfile`
- `infra/02-auth/oauth2-proxy/dev.Dockerfile`
- `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg`

- **Systems**: OAuth2 Proxy ForwardAuth gateway
- **Environments**: Local, Dev, Stage, Production-like

## Rules

- **필수**:
  - `check-all-hardening.sh 02-auth` 실패 0건을 유지해야 한다.
  - 로그인 루프, 콜백 실패 급증, `/ping` 실패 지속 시 런북 절차를 수행해야 한다.
  - 서비스는 `template-infra-readonly-med`를 사용해야 한다.
  - 세션 저장소 password는 엔트리포인트 스크립트가 `/run/secrets` 파일에서 주입한다.
    client/cookie secret은 cfg의 `*_secret_file`로 읽고, client secret은
    `OAUTH2_PROXY_CLIENT_SECRET_FILE`로 OpenBao Agent 출력(`/run/openbao/oauth2-proxy`)을
    지정할 수 있다. 값을 환경 변수 리터럴로 두지 않는다.
  - SSO route 통과는 Keycloak group `/admins`(`allowed_groups`)로 제한하고,
    `trusted_ips`는 두지 않으며 `trusted_proxy_ips`는 Traefik `edge_net` 주소로 한정한다.
  - 세션 저장소는 공유 `mng-valkey`다. 앱별 전용 Valkey와 exporter는 ADR-0062 결정 10으로
    제거되었고, `OAUTH2_PROXY_VALKEY_HOST`는 `mng-valkey`를 가리켜야 한다. 선택한
    이미지의 entrypoint가 읽는 세션 시크릿도 해당 저장소와 일치해야 한다.
  - 이미지 실행 계정은 non-root여야 한다(`dev.Dockerfile`은 `oauth2proxy`, `Dockerfile`은 UID 100/GID 101).
  - 세션 정책은 `cookie_secure=true`, `cookie_httponly=true`, `cookie_samesite=lax`, `cookie_refresh=1h`, `cookie_expire=12h`를 유지한다.
  - 기본 운영 모드는 fail-closed다.
- **허용**:
  - 운영 승인 하에 degraded-mode를 제한적으로 수행(원복 절차 필수)
  - 환경별 도메인 변수(`DEFAULT_URL`) 조정
- **금지**:
  - fail-open 상시 운영
  - 시크릿을 Compose/문서에 평문으로 저장

### Session boundaries

Valkey AOF는 세션 persistence이며 백업을 대신하지 않는다. 세션 손실 시 재로그인
영향을 고지하고 공유 `mng-valkey`를 Proxy 복구만을 위해 비우거나 삭제하지 않는다.

### Credential exposure boundary

Proxy는 entrypoint가 Secret 파일에서 읽어 `OAUTH2_PROXY_REDIS_PASSWORD` 환경 변수로
password를 소비한다. Docker daemon/host process 접근도 credential 신뢰 경계다. full
`docker inspect`, `docker top`/process `ps`, `/proc/*/cmdline`·`environ`, 원문
`.State.Health.Log`는 기록하지 않는다. 서비스명·image identity·health 상태·재시작
횟수·시각처럼 허용된 필드만 사용한다. 실제 유출은 관찰하지 않았다.

### Shared controls and accountability

운영 책임자는 @buenhyden이다. 변경·재시작·credential 작업의 대상과 영향, 승인,
종료 조건을 기록하며 예외는 위험·만료·원복 책임까지 명시한다. 공통 자원 상한과
mount 적용은 [POL-0006](../01-common/0006-infrastructure-optimization-governance.md), profile·
상호 배제는 [POL-0078](../01-common/0078-compose-profile-vocabulary.md), image 변경과 검토는
[POL-0086](../10-platform-and-backup/0086-dependency-version-management.md)을 적용한다. OOM·반복 재시작·
인증 실패 증가 또는 이미지·노출·mount 변경 시 정기 주기를 기다리지 않고 검토한다.
보존할 상태와 private credential은 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의
접근·암호화·retention을 적용한다. 제거 전에 소비자와 복구 입력을 확인하고,
volume·인증서·secret 삭제는 서비스 중지와 분리된 승인 대상으로 한다.

### Session and Upgrade Controls

- Cookie, client, Valkey credential 값은 각각의 secret 소유자가 관리한다.
  회전할 때는 모든 활성 session이 무효화되는지 명시해야 한다.
- Session-store 내용은 단기 인증 상태이며 영속 business-data backup 대상이 아니다.
  store 손실 후에는 fail-closed와 재인증을 우선하며, session을 유지하기 위해
  cookie 보안을 약화하지 않는다.
- 격리된 OIDC/PKCE/ForwardAuth/logout test 후에만 upgrade한다.
  이전 image 선언을 보존하고 session 무효화 계획을 기록한다.

## Exceptions

- OIDC 공급자 장애가 장기화될 때 한시적 degraded-mode 허용 가능.
- 단, 승인자 기록과 종료 조건(원복 기준)을 사전에 명시해야 한다.

### Review Cadence

- 월 1회 정기 점검
- OAuth2 Proxy/Keycloak 버전 변경 시 수시 점검

### Traceability

- Declared parent: [02-Auth Architecture Description](../../../02.architecture/descriptions/0002-auth-architecture.md) (`AD-0002`)
- Subject peers: [Guide](../../guides/03-identity-and-access/0015-oauth2-proxy.md) (`GDE-0015`), [Runbook](../../runbooks/03-identity-and-access/0015-oauth2-proxy.md) (`RUN-0015`)

## Verification

- `bash scripts/hardening/check-all-hardening.sh 02-auth`
- `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
- Runtime-only: `docker compose --profile auth exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping`(기본 `OAUTH2_PROXY_PORT` 기준)

## Related Documents

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../../README.md)
- [Usage guide](../../guides/03-identity-and-access/0015-oauth2-proxy.md)
- [Recovery runbook](../../runbooks/03-identity-and-access/0015-oauth2-proxy.md)
