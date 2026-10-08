---
title: "01-Gateway Traefik Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "operations"
artifact_id: "GDE-0013"
parent_ids:
- "POL-0013"
implementation_services:
  infra/01-gateway/traefik/docker-compose.yml:
  - traefik
created: "2026-05-10"
---

# 01-Gateway Traefik Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Implementation Sources

- [infra/01-gateway/traefik/docker-compose.yml](../../../infra/01-gateway/traefik/docker-compose.yml)

### Overview

이 문서는 `Traefik Primary` 모델에서 01-gateway 소유 라우터를 운영하는 방법을 설명한다. Traefik의 lifecycle class는 **HOME**이다. 표준 미들웨어 체인 적용과 검증 흐름을 중심으로 다룬다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

### Purpose

- Traefik dashboard 라우터 하드닝 정책을 일관되게 적용한다.
- `gateway-standard-chain` 구성요소와 적용 범위를 이해한다.

### Prerequisites

- Docker/Docker Compose 사용 가능
- `infra/01-gateway/traefik` 구성 파일 접근 가능
- `scripts/hardening/check-all-hardening.sh 01-gateway` 실행 가능
- root `core` profile compose validation 실행 가능

### Source, activation and middleware behavior

`traefik`은 HOME이며 `core`/`dev`/`local`로 선택한다. host bind는
`HOST_LAN_BIND_IP`, host 포트는 `HTTP_HOST_PORT`/`HTTPS_HOST_PORT`에서 정한다.
[정적 설정](../../../infra/01-gateway/traefik/config/traefik.yml)의 내부 80/443과
Compose의 `HTTP_PORT`/`HTTPS_PORT`는 일치해야 한다. OPTIONAL Nginx와 동시에
같은 host 포트를 사용하지 않는다. Compose `depends_on`은 없지만 실제 요청은
대상 앱·OAuth2 Proxy·Keycloak과 공유 DB/Valkey readiness에 의존한다.

[동적 middleware](../../../infra/01-gateway/traefik/dynamic/middleware.yml)의
`gateway-standard-chain` 실제 멤버는 `req-retry`, `req-circuit-breaker`다.
`req-rate-limit` 선언이 있어도 이 chain에는 연결되지 않았다. 세 멤버를 요구하는
[POL-0013](../policies/0013-traefik.md#controls)의 **구현 미준수**이며 문서 변경으로
rate limit이 적용된 것은 아니다. route에 chain 이름이 있다는 사실이나 하드닝
문자열 검사 통과로 준수를 주장하지 않는다. 근거는 소스와
[선언 릴리스 계열의 Chain 동작](https://doc.traefik.io/traefik/v3.7/reference/routing-configuration/http/middlewares/chain/)이다.

`sso-auth`는 `http://oauth2-proxy:4180/`(static upstream)을 호출하며 성공 시 사용자·
이메일·preferred username 헤더만 앱에 전달한다. 공통 체인은 Authorization이나
access token을 전달하지 않는다. session이 없으면 브라우저는 Keycloak으로 가는
302를, `Accept: application/json` 요청은 401을 받는다. `sso-errors`는 **403만**
sign-in 서비스의 응답으로 바꾸며 401은 machine client에게 그대로 간다.
[Errors statusRewrites](https://doc.traefik.io/traefik/v3.7/reference/routing-configuration/http/middlewares/errorpages/#statusrewrites)와
[인증 통합 Guide](0079-application-auth-integration.md)를 함께 확인한다.

### Configuration, state and signals

필수 입력은 `DEFAULT_URL`, `DEFAULT_CERT_DIR`, `CERT_GROUP_GID`, root network와
세 Docker Secret 참조(`traefik_basicauth_password`,
`traefik_opensearch_basicauth_password`, `traefik_prometheus_api_htpasswd`)다.
`edge_net` 고정 주소와 Keycloak/auth alias는 Proxy의 trust 설정과 연결된다.
설정·인증서는 읽기 전용이고 ACME state 선언은 없다. Docker socket의 읽기 전용
mount는 Docker API를 저권한으로 만들지 않으므로 host 제어 경계로 취급한다.

Docker provider는 기본 노출을 끄고 `edge_net`을 사용한다. dashboard는 HTTPS
`dashboard.${DEFAULT_URL}`에서 BasicAuth를 요구한다. 내부 8082의 ping·Prometheus
metrics는 host에 게시하지 않으며, OTLP는 `tempo:4317`로 전달한다. Docker access/error
로그는 공통 rotation을 상속한다. `template-infra-readonly-med`의 CPU 1,
메모리 512 MiB와 요청·재시도·오류·OOM을 함께 관찰한다. ping은 라우터 인가나
backend 성공을 보장하지 않는다. directory mount `/dynamic`은 file watch 대상이고,
정적 단일 파일 변경은 [POL-0006 적용 통제](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)를 따른다.

### Step-by-step Instructions

1. 미들웨어 파일 확인
   - `infra/01-gateway/traefik/dynamic/middleware.yml`
   - 필수 블록과 실제 chain 멤버십을 별도로 확인: `req-rate-limit`, `req-retry`, `req-circuit-breaker`, `gateway-standard-chain`
2. 라우터 라벨 확인
   - `infra/01-gateway/traefik/docker-compose.yml`
   - dashboard 라우터에 `dashboard-auth@file,gateway-standard-chain@file` 적용 확인
3. 설정 정적 검증
   - `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
4. 하드닝 검증
   - `bash scripts/hardening/check-all-hardening.sh 01-gateway`

### Common Pitfalls

- `gateway-standard-chain` 이름 오타로 middleware resolve 실패
- dashboard middleware 순서/구분자(`,`) 오류
- 비게이트웨이 소유 라우터까지 무분별하게 체인 확장 적용

### Common Checks

- `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 01-gateway`
- `docker compose exec traefik traefik healthcheck --ping`은 승인된 root stack이 실행 중일 때만 사용한다.

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0013-traefik.md)을 따른다.

구성·private 인증서 복구, upgrade 수용 검증과 prior-image rollback은 [Runbook](../runbooks/0013-traefik.md#rollback-or-recovery)이 소유한다. 공통 변경 흐름은 [RUN-0086](../runbooks/0086-dependency-version-management.md), 여러 서비스 장애는 [RUN-0099](../runbooks/0099-system-operations.md)로 연결한다.

### Traceability

- Declared parent: [01-Gateway Traefik Operations Policy](../policies/0013-traefik.md) (`POL-0013`)
- Governing authority: [Gateway Tier Architecture Description](../../02.architecture/descriptions/0001-gateway-architecture.md) (`AD-0001`)
- Subject peers: [Policy](../policies/0013-traefik.md) (`POL-0013`), [Runbook](../runbooks/0013-traefik.md) (`RUN-0013`)

## Related Documents

- [Official upstream operational documentation](https://doc.traefik.io/traefik/)
- [Traefik Docker API security guidance](https://doc.traefik.io/traefik/providers/docker/)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0013-traefik.md)
- [Recovery runbook](../runbooks/0013-traefik.md)
