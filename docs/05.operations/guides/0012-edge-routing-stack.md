---
title: "Edge Routing Stack Operations"
version: "1.2.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0012"
parent_ids: []
created: "2026-07-06"
---
# Edge Routing Stack Operations

## Usage

### Overview

이 문서는 `01-gateway` 티어의 초기 설정 및 검증 가이드이다. 루트 stack은 두 파일을 모두 무조건 include하고 profile이 기동을 가른다. Traefik은 `core`/`dev`가, Nginx는 전용 `nginx` profile이 선택하며, 컨테이너 실행은 승인된 runtime context에서만 다룬다.

### Edge Routing Stack Usage

> entry point infrastructure를 배포하고 구성하기 위한 단계별 절차.

---

#### Usage Type

`system-guide`

#### Target Audience

- Infrastructure Operator
- Backend Developer
- Contributor

#### Purpose

이 가이드는 `core`/`dev`가 선택하는 Traefik edge router를 검증하고, `nginx` profile이 그리는 Nginx path-proxy boundary를 이해하도록 돕는다.

#### Prerequisites

- Docker와 Docker Compose가 설치되어 있어야 한다.
- 유효한 domain name(`DEFAULT_URL` environment variable에 설정)이 있어야 한다.
- `scripts/operations/gen-secrets.sh`로 생성한 secret이 있어야 한다.
- `secrets/certs/`에 certificate가 있어야 한다.

#### Step-by-step Instructions

##### 1. Verify Network Contract

network를 임의로 만드는 대신 root compose validator를 사용한다. root compose는 flow-scoped network와 external network contract를 선언한다.

```bash
HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh
```

##### 2. Configure Traefik

1. `infra/01-gateway/traefik/config/traefik.yml`을 검토한다.
2. `infra/01-gateway/traefik/dynamic/`의 dynamic configuration이 존재하는지 확인한다.
3. `tls.yaml`에서 TLS certificate가 올바르게 매핑되어 있는지 확인한다.

##### 3. Validate Gateway Stack

runtime action 전에 현재 gateway contract를 검증한다.

```bash
bash scripts/hardening/check-all-hardening.sh 01-gateway
```

runtime start/stop/reload action은 이 가이드의 범위가 아니다. Traefik runtime 작업은 승인된 root compose context를 사용해야 한다. Nginx runtime 작업은 명시적인 root network/dependency context가 필요하다. root는 `infra/01-gateway/nginx/docker-compose.yml`을 무조건 include하지만, service는 `nginx` profile이 선택하며 backend service에 의존한다.

#### 4. Verify Functionality

- static 증거는 `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`와 `bash scripts/hardening/check-all-hardening.sh 01-gateway`를 사용한다.
- 승인 후 runtime 증거는 실행 중인 root stack에서 Traefik dashboard와 `docker compose exec traefik traefik healthcheck --ping`을 확인한다.
- 승인 후 Nginx runtime 증거는 명시적으로 provision된 Nginx context에서만 `docker compose exec nginx nginx -t`를 실행한다.

#### Common Pitfalls

- **Cert Name Mismatch**: `tls.yaml`이 `secrets/certs/`의 올바른 파일명을 가리키는지 확인한다.
- **Port Conflicts**: 호스트에서 port 80과 443을 사용할 수 있어야 한다.
- **Network Isolation**: backend service가 발견되려면 Traefik Docker provider network인 `edge_net`에 있어야 한다.
- **Service-local Compose**: 독립적인 `infra/01-gateway/*/docker-compose.yml` 렌더링은 root network/secret/dependency context가 없으므로 gateway readiness 증거가 아니다.

## Common Checks

- Step-by-step Instructions 의 검증 단계를 따른다.

## Runbook Handoff

runtime recovery는 [Traefik runbook](../runbooks/0013-traefik.md)과 [Nginx runbook](../runbooks/0011-nginx.md)이 처리한다.

## Traceability

- Governing authority: [Gateway Tier Architecture Description](../../02.architecture/descriptions/0001-gateway-architecture.md) (`AD-0001`)
- Subject peers: none — `0012` 번호를 공유하는 Policy나 Runbook이 없다.

## Related Documents

- Runtime pins: Compose/Dockerfile 선언이 authoritative이며, [curated version projection](../../../infra/tech-stack.versions.json)은 drift 검증을 제공한다.

- [Operations index](../README.md)
- [Gateway Traefik guide](0013-traefik.md)
- [Gateway Nginx guide](0011-nginx.md)
