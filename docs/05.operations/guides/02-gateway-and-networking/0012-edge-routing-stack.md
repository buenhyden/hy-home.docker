---
title: "Edge Routing Stack Operations"
version: "1.4.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-14"
layer: "operations"
artifact_id: "GDE-0012"
created: "2026-07-06"
next_review_at: "2027-05-13"
---

# Edge Routing Stack Operations

## Purpose

### Outcome

이 문서는 `01-gateway` 티어의 초기 설정 및 검증 가이드이다. 루트 stack은 Traefik 파일을 무조건 include하고 profile이 기동을 가른다. Traefik은 `core`/`dev`/`local`이 선택하며, 컨테이너 실행은 승인된 runtime context에서만 다룬다.

대상은 Infrastructure Operator, Backend Developer, Contributor다. `core`/`dev`/`local`이 선택하는 Traefik edge router를 검증하는 것이 목적이다.

사전 조건은 다음과 같다.

- Docker와 Docker Compose가 설치되어 있어야 한다.
- 유효한 domain name(`DEFAULT_URL` environment variable에 설정)이 있어야 한다.
- 승인된 secret owner가 준비한 기존 credential과 참조가 있어야 한다. 생성·회전은 이 Guide의 검증 절차에 포함하지 않는다.
- `DEFAULT_CERT_DIR`(`.env.example` 기본값 `${DEFAULT_DOCKER_PROJECT_PATH}/secrets/certs`)에 `cert.pem`, `key.pem`, `rootCA.pem`이 있어야 한다.

### Boundaries

- Governing authority: [Gateway Tier Architecture Description](../../../02.architecture/descriptions/0001-gateway-architecture.md) (`AD-0001`)
- Subject peers: none — `0012` 번호를 공유하는 Policy나 Runbook이 없다.

- Runtime pins: Compose/Dockerfile 선언이 authoritative이며, [curated version projection](../../../../infra/tech-stack.versions.json)은 drift 검증을 제공한다.

- [Operations index](../../README.md)
- [Gateway Traefik guide](0013-traefik.md)

## Prerequisites

### Environment

root [docker-compose.yml](../../../../docker-compose.yml)은 `infra/01-gateway/traefik/docker-compose.yml`을 include하고 flow-scoped network와 external network contract를 선언한다. Traefik은 `${HOST_LAN_BIND_IP}`의 80/443을 게시하며 OAuth2 Proxy·Keycloak 인증 경로를 ForwardAuth로 참조한다.

### Permissions

승인된 secret owner가 준비한 기존 credential과 참조가 필요하며 생성·회전은 이 Guide에 포함하지 않는다. `DEFAULT_CERT_DIR`의 `cert.pem`, `key.pem`, `rootCA.pem`이 있어야 하고, runtime 증거는 승인 후에만 확인한다.

## Procedure

### Actions

정상 사용 절차는 아래 항목에 정리한다.

#### Configure Traefik

1. `infra/01-gateway/traefik/config/traefik.yml`을 검토한다.
2. `infra/01-gateway/traefik/dynamic/`의 dynamic configuration(`middleware.yml`, `tls.yaml`, `blog-export.yml`, `hermes.yml`, `hermes-webhook.yml`)이 존재하는지 확인한다.
3. `tls.yaml`이 container 경로 `/certs/cert.pem`, `/certs/key.pem`을 기본 인증서로, `/openbao-ca/ca.pem`을 `openbao-tls` serversTransport CA로 가리키는지 확인한다.

### Exceptions

이 가이드는 별도 예외 절을 두지 않으며, 한계와 경계는 Environment와 Actions의 해당 본문과 Troubleshooting에 함께 적혀 있다.

## Verification

### Expected Result

network를 임의로 만들지 않고 root validator와 하드닝 검사로 static 증거를 얻는다.

```bash
HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 01-gateway
```

- 승인 후 runtime 증거는 실행 중인 root stack에서 Traefik dashboard와 `docker compose exec traefik traefik healthcheck --ping`을 확인한다.

runtime start/stop/reload action은 이 가이드의 범위가 아니다. Traefik chain의 limiter·401/403 차이는 [Traefik Guide](0013-traefik.md)에
명시되어 있다. 정적 검증만으로 이 한계가 해소되거나 인증·복구가 성공한 것은 아니다.
시스템 영향과 profile 공통 의미는 [System Guide](../01-common/0099-system-operations.md)를 따른다.

### Troubleshooting

- **Cert Name Mismatch**: `DEFAULT_CERT_DIR`에 `cert.pem`, `key.pem`, `rootCA.pem` 파일명이 정확히 있는지 확인한다. bind는 `create_host_path: false`라 파일이 없으면 기동이 실패한다.
- **Port Conflicts**: 호스트에서 port 80과 443을 사용할 수 있어야 한다.
- **Network Isolation**: backend service가 발견되려면 Traefik Docker provider network인 `edge_net`에 있어야 한다.
- **Service-local Compose**: 독립적인 `infra/01-gateway/*/docker-compose.yml` 렌더링은 root network/secret/dependency context가 없으므로 gateway readiness 증거가 아니다.

#### Runbook Handoff

runtime recovery는 [Traefik runbook](../../runbooks/02-gateway-and-networking/0013-traefik.md)이 처리한다.
