---
title: "01-Gateway Nginx Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0011"
parent_ids:
- "POL-0011"
implementation_services:
  infra/01-gateway/nginx/docker-compose.yml:
  - nginx
created: "2026-05-10"
---

# 01-Gateway Nginx Usage Guide

## Usage

### Implementation Sources

- [infra/01-gateway/nginx/docker-compose.yml](../../../infra/01-gateway/nginx/docker-compose.yml)

### Overview

이 문서는 01-gateway의 Nginx 특수 경로 프록시 구성과 하드닝 포인트를 설명한다. Nginx의 lifecycle class는 **OPTIONAL** alternative gateway다. readonly/tmpfs 운영, timeout/failover, 정적 캐시 정책의 의도를 중심으로 다룬다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

### Purpose

- Nginx를 `template-infra-readonly-low` 기반으로 안정적으로 운영한다.
- `/oauth2/`, `/keycloak/`, `/cdn/` 경로 흐름을 유지하면서 하드닝 변경을 적용한다.

### Prerequisites

- Docker/Docker Compose 사용 가능
- `infra/01-gateway/nginx` 구성 파일 접근 가능
- `scripts/hardening/check-all-hardening.sh 01-gateway` 실행 가능
- Nginx runtime 검증 시 명시적 root network/dependency context 승인 필요

### Source, activation and route limits

`nginx`는 OPTIONAL이며 `nginx` profile만 선택한다. 기본 host bind는
`${HOST_LAN_BIND_IP:-192.168.0.13}`, host 포트는 `HTTP_HOST_PORT`/`HTTPS_HOST_PORT`다.
실제 [nginx.conf](../../../infra/01-gateway/nginx/config/nginx.conf)는 80/443을
고정 청취하므로 Compose의 `HTTP_PORT`/`HTTPS_PORT`만 변경하면 불일치가 생긴다.
Traefik의 `core`/`dev`/`local`과 같은 호스트의 80/443을 함께 점유할 수 없다.
선택과 network 전제는 [POL-0078](../policies/0078-compose-profile-vocabulary.md),
공통 기동은 [시스템 Guide](0099-system-operations.md#selection-and-readiness)를 따른다.

Compose가 기다리는 것은 `seaweedfs-s3`의 `service_healthy`뿐이다. 설정은
`oauth2-proxy:4180`, `keycloak:8080`도 참조하므로 DNS·network·인증 의존성이
별도로 필요하다. `nginx` profile만으로 이 인증 서비스가 준비되지는 않는다.
현재 `/keycloak/`은 prefix를 제거하지 않고 전달하지만 Keycloak은 host 기반
issuer를 사용한다. 경로 호환성은 미검증이며 정상 OIDC 진입점으로 단정하지 않는다.

| 경로 | 소스의 실제 동작과 한계 |
| --- | --- |
| HTTP `/ping` | 서버 전체 301 HTTPS 전환을 거친다. Compose의 HTTP `wget`은 직접 200을 검사하지 않으며 redirect 뒤의 CA·hostname 검증 실패 가능성이 있다. |
| HTTPS `/ping` | `pong` 200인 process 응답이다. 인증·backend·failover 성공을 뜻하지 않는다. |
| `/oauth2/` | OAuth2 Proxy로 전달한다. issuer/callback은 [0015](0015-oauth2-proxy.md)의 host 기반 설정과 함께 확인한다. |
| `/app/` | `auth_request`와 limiter가 선언돼 있으나 `return 200`이 access 단계 전에 종료한다. backend `proxy_pass`는 주석이다. 인증된 앱 경로나 보호된 backend 노출로 설명하지 않는다. |
| `/cdn/` | `cdn-bucket`의 익명 GET/HEAD 전용이다. 루트 목록은 404, 쓰기·삭제는 거부한다. `^~`가 정적 확장자 location보다 우선한다. 객체 권한은 [POL-0024](../policies/0024-seaweedfs.md)도 적용한다. |
| 정적 확장자 | 7일 cache header가 있으나 자체 앱 content mount는 없다. `proxy_cache_path` 선언만으로 모든 route가 proxy cache를 사용하지는 않는다. |

각 upstream은 현재 한 서버뿐이다. retry/max_fails 설정을 다중 노드 failover나
단일 호스트 장애 격리 증거로 보지 않는다. placeholder의 처리 순서는
[Nginx request phases](https://nginx.org/en/docs/dev/development_guide.html)와
[return](https://nginx.org/en/docs/http/ngx_http_rewrite_module.html#return)에 근거한다.
이미지 `nginx:alpine`은 변경 가능한 tag로 정확한 릴리스가 고정되지 않았다.
이 문서의 소스 분석은 실행 버전 관측이 아니며, 이미지 확정·인증 경로 수정은
별도 구현 변경으로 @buenhyden에게 전달한다.

### Configuration, state and signals

필수 입력은 `DEFAULT_CERT_DIR`의 `cert.pem`, `key.pem`, `rootCA.pem`과
읽기 전용 설정 파일이다. 인증서 비밀값을 공개하지 않는다. 설정은 Git,
인증서는 private owner가 소유하고 cache/log/PID는 tmpfs로 재시작 시 사라질 수 있다.
자원은 공통 `template-infra-readonly-low`(CPU 0.5, 메모리 256 MiB)를 상속한다.
1 GiB cache 상한을 선언했다고 이 메모리 예산 안에서 그만큼 사용할 수 있다는
뜻은 아니다. worker 연결 상한·cache·무제한 Keycloak upload의 실제 사용량과
OOM을 함께 본다. Nginx 로그 경로는 tmpfs `/var/log/nginx`이며 Docker 로그에
모든 access 로그가 있다고 가정하지 않는다. 전용 metrics exporter는 없다.
정상 신호는 lint 성공, TLS 응답, 필요한 경로와 인증의 개별 수용 결과이며,
운영 절차는 Runbook이 소유한다.


### Step-by-step Instructions

1. Compose 하드닝 확인
   - `infra/01-gateway/nginx/docker-compose.yml`
   - readonly 템플릿/필수 tmpfs/`/ping` healthcheck 존재 확인
2. Nginx config 하드닝 확인
   - `infra/01-gateway/nginx/config/nginx.conf`
   - `server_tokens off`, timeout 3종, `proxy_next_upstream`, upstream `max_fails/fail_timeout`, 정적 캐시 location 확인
3. 설정 검증
   - 정적 검증: `bash scripts/hardening/check-all-hardening.sh 01-gateway`
   - runtime lint: approved Nginx runtime context에서 `docker compose exec nginx nginx -t`
4. 하드닝 검증
   - `bash scripts/hardening/check-all-hardening.sh 01-gateway`

### Common Pitfalls

- readonly 전환 후 `/var/cache/nginx`/`/var/log/nginx`/`/var/run` tmpfs 누락
- `proxy_pass` trailing slash 처리 실수로 경로 재작성 오류
- timeout 전역값/특정 location override 충돌

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 01-gateway`
- `docker compose exec nginx nginx -t`는 승인된 Nginx runtime context가 실행 중일 때만 사용한다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0011-nginx.md)을 따른다.

구성·인증서 복구, 변경 적용과 업그레이드는 [Runbook](../runbooks/0011-nginx.md#rollback-or-recovery)이 소유한다. tmpfs는 업무 데이터 백업 대상이 아니다.

## Traceability

- Declared parent: [01-Gateway Nginx Operations Policy](../policies/0011-nginx.md) (`POL-0011`)
- Governing authority: [Gateway Tier Architecture Description](../../02.architecture/descriptions/0001-gateway-architecture.md) (`AD-0001`)
- Subject peers: [Policy](../policies/0011-nginx.md) (`POL-0011`), [Runbook](../runbooks/0011-nginx.md) (`RUN-0011`)

## Related Documents

- [Official upstream operational documentation](https://nginx.org/en/docs/beginners_guide.html)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0011-nginx.md)
- [Recovery runbook](../runbooks/0011-nginx.md)
