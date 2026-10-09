---
title: "Edge Routing Stack Operations"
version: "1.3.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0012"
created: "2026-07-06"
---
# Edge Routing Stack Operations

## Overview

이 문서는 `01-gateway` 티어의 초기 설정 및 검증 가이드이다. 루트 stack은 두 파일을 모두 무조건 include하고 profile이 기동을 가른다. Traefik은 `core`/`dev`/`local`이, Nginx는 전용 `nginx` profile이 선택하며, 컨테이너 실행은 승인된 runtime context에서만 다룬다.

## Audience and Goal

대상은 Infrastructure Operator, Backend Developer, Contributor다. `core`/`dev`/`local`이 선택하는 Traefik edge router를 검증하고, `nginx` profile이 그리는 Nginx path-proxy boundary를 이해하는 것이 목적이다.

사전 조건은 다음과 같다.

- Docker와 Docker Compose가 설치되어 있어야 한다.
- 유효한 domain name(`DEFAULT_URL` environment variable에 설정)이 있어야 한다.
- 승인된 secret owner가 준비한 기존 credential과 참조가 있어야 한다. 생성·회전은 이 Guide의 검증 절차에 포함하지 않는다.
- `secrets/certs/`에 certificate가 있어야 한다.

## Usage

gateway 선택과 정적 검증 경계를 이해하기 위한 안내다.

### Verify the network contract

network를 임의로 만드는 대신 root compose validator를 사용한다. root compose는 flow-scoped network와 external network contract를 선언한다.

```bash
HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh
```

### Configure Traefik

1. `infra/01-gateway/traefik/config/traefik.yml`을 검토한다.
2. `infra/01-gateway/traefik/dynamic/`의 dynamic configuration이 존재하는지 확인한다.
3. `tls.yaml`에서 TLS certificate가 올바르게 매핑되어 있는지 확인한다.

### Validate the gateway stack

runtime action 전에 현재 gateway contract를 검증한다.

```bash
bash scripts/hardening/check-all-hardening.sh 01-gateway
```

runtime start/stop/reload action은 이 가이드의 범위가 아니다. Traefik runtime 작업은 승인된 root compose context를 사용해야 한다. Nginx runtime 작업은 명시적인 root network/dependency context가 필요하다. root는 `infra/01-gateway/nginx/docker-compose.yml`을 무조건 include하지만, service는 `nginx` profile이 선택하며 backend service에 의존한다.

### Verify functionality

- static 증거는 `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`와 `bash scripts/hardening/check-all-hardening.sh 01-gateway`를 사용한다.
- 승인 후 runtime 증거는 실행 중인 root stack에서 Traefik dashboard와 `docker compose exec traefik traefik healthcheck --ping`을 확인한다.
- 승인 후 Nginx runtime 증거는 명시적으로 provision된 Nginx context에서만 `docker compose exec nginx nginx -t`를 실행한다.

### Common Checks

- 위 "Verify functionality" 단계를 따른다.

Nginx health의 HTTP redirect·placeholder 인증 한계는 [Nginx Guide](0011-nginx.md),
Traefik chain의 limiter 미준수·401/403 차이는 [Traefik Guide](0013-traefik.md)에
명시되어 있다. 두 gateway가 같은 host bind를 점유하므로 동시 선택하지 않는다.
정적 검증만으로 이 한계가 해소되거나 인증·복구가 성공한 것은 아니다.
시스템 영향과 profile 공통 의미는 [System Guide](0099-system-operations.md)를 따른다.

### Runbook Handoff

runtime recovery는 [Traefik runbook](../runbooks/0013-traefik.md)과 [Nginx runbook](../runbooks/0011-nginx.md)이 처리한다.

### Traceability

- Governing authority: [Gateway Tier Architecture Description](../../02.architecture/descriptions/0001-gateway-architecture.md) (`AD-0001`)
- Subject peers: none — `0012` 번호를 공유하는 Policy나 Runbook이 없다.

## Troubleshooting

- **Cert Name Mismatch**: `tls.yaml`이 `secrets/certs/`의 올바른 파일명을 가리키는지 확인한다.
- **Port Conflicts**: 호스트에서 port 80과 443을 사용할 수 있어야 한다.
- **Network Isolation**: backend service가 발견되려면 Traefik Docker provider network인 `edge_net`에 있어야 한다.
- **Service-local Compose**: 독립적인 `infra/01-gateway/*/docker-compose.yml` 렌더링은 root network/secret/dependency context가 없으므로 gateway readiness 증거가 아니다.

## Related Documents

- Runtime pins: Compose/Dockerfile 선언이 authoritative이며, [curated version projection](../../../infra/tech-stack.versions.json)은 drift 검증을 제공한다.

- [Operations index](../README.md)
- [Gateway Traefik guide](0013-traefik.md)
- [Gateway Nginx guide](0011-nginx.md)
