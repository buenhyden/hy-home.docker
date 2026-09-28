---
title: "Dozzle Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0072"
parent_ids:
- "POL-0072"
implementation_services:
  infra/11-laboratory/dozzle/docker-compose.yml:
  - dozzle
created: "2026-05-10"
---

# Dozzle Usage Guide

## Usage

### 목적과 분류

Dozzle은 `admin`과 `admin-logs` 하위의 OPTIONAL admin 로그 뷰어이다. 로그 아카이브가
아니다. 컨테이너 로그는 여전히 Docker/로깅 백엔드가 소유한다. Dozzle은
`${DEFAULT_MANAGEMENT_DIR}/dozzle`에 UI/사용자 설정을 영속화하지만, 조회한 로그의
두 번째 권위 사본을 보관하지는 않는다.

### 현재 구현과 위험

- [Dozzle Compose](../../../infra/11-laboratory/dozzle/docker-compose.yml)가
  profile, OIDC, 라우트, IP 허용목록, secret, health, 마운트를 정의한다.
- `DOZZLE_AUTH_*`와 `dozzle_client_secret`을 통해 Keycloak에 대한 네이티브 OIDC를
  사용한다. Traefik은 OAuth2 Proxy ForwardAuth가 아니라 게이트웨이 표준 체인과
  admin CIDR 허용목록을 적용한다.
- Docker socket은 `:ro`로 마운트되지만, 업스트림은 읽기 전용 파일 모드가 Docker
  API 메서드를 제한하지 않는다고 경고한다. 침해되면 root와 동등해질 수 있다.
  현재 소스는 socket proxy를 선언하지 않는다.
- `/data`는 설정을 영속화한다. CA 파일은 issuer 신뢰를 지원한다. health 명령은
  OIDC, socket 인가, 로그 커버리지가 아니라 Dozzle 프로세스 health만 증명한다.

### 일반적인 사용, 백업, 업그레이드

`docker compose --profile admin-logs config --quiet`로 검증하고, CIDR와 OIDC
client/claim을 확인한 다음 Dozzle만 시작한다. 최소 권한 테스트 identity로 로그인을
검증하고 명시적으로 설정하고 승인하지 않았다면 shell/actions가 비활성 상태로
유지되는지 확인한다. 증거를 캡처하기 전에 로그를 정제한다.

`/data`는 설정 연속성을 위해서만 백업한다. 컨테이너 로그는 백업하지 않는다. 일관된
복사를 위해 Dozzle을 중지한다. 프로덕션이 아닌 Docker endpoint에 연결되거나 socket이
없는 격리된 Dozzle에 설정 사본을 복원한다. 업그레이드 전에는 보안 권고/release
노트를 검토하고 OIDC와 필터링된 로그 접근을 테스트한다. 여기서는 백업, 복원,
업그레이드를 실행하지 않았다.

## Common Checks

- `docker compose --profile admin-logs config --quiet`
- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`

## Runbook Handoff

OIDC, socket, 로그 스트림, 설정, 업그레이드 복구에는
[runbook](../runbooks/0072-dozzle.md)을 사용한다.

## Traceability

- [Policy](../policies/0072-dozzle.md) (`POL-0072`)
- [Runbook](../runbooks/0072-dozzle.md) (`RUN-0072`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [Dozzle authentication and socket security](https://dozzle.dev/guide/authentication)
- [Dozzle getting started](https://dozzle.dev/guide/getting-started)
- [Dozzle MIT license](https://github.com/amir20/dozzle#license)
