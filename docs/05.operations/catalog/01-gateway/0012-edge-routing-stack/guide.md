---
profile_id: guide
status: active
artifact_id: guide-0012
artifact_type: guide
parent_ids: []
created: 2026-07-06
updated: 2026-08-14
---
# Edge Routing Stack Operations

## Usage

### Overview

이 문서는 `01-gateway` 티어의 초기 설정 및 검증 가이드이다. 현재 root stack은 Traefik을 active include로 사용하고, Nginx는 profile-only leaf로 유지하므로 컨테이너 실행은 승인된 runtime context에서만 다룬다.

### Edge Routing Stack Usage

> Step-by-step procedure for deploying and configuring the entry point infrastructure.

---

#### Usage Type

`system-guide`

#### Target Audience

- Infrastructure Operator
- Backend Developer
- Contributor

#### Purpose

This guide helps the reader validate the root-active Traefik edge router and understand the profile-only Nginx path-proxy boundary.

#### Prerequisites

- Docker & Docker Compose installed.
- Valid domain name (configured in `DEFAULT_URL` environment variable).
- Secrets generated via `scripts/operations/gen-secrets.sh`.
- Certificates available in `secrets/certs/`.

#### Step-by-step Instructions

##### 1. Verify Network Contract

Use the root compose validator instead of creating networks ad hoc. The root compose declares `infra_net` and the external network contracts.

```bash
HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh
```

##### 2. Configure Traefik

1. Review `infra/01-gateway/traefik/config/traefik.yml`.
2. Ensure dynamic configuration in `infra/01-gateway/traefik/dynamic/` is present.
3. Verify TLS certificates are mapped correctly in `tls.yaml`.

##### 3. Validate Gateway Stack

Validate the current gateway contract before any runtime action:

```bash
bash scripts/hardening/check-all-hardening.sh 01-gateway
```

Runtime start/stop/reload actions are not part of this guide. Traefik runtime work must use the approved root compose context. Nginx runtime work requires an explicit root network/dependency context because `infra/01-gateway/nginx/docker-compose.yml` is not root-included by default and depends on backend services.

#### 4. Verify Functionality

- For static evidence, use `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh` and `bash scripts/hardening/check-all-hardening.sh 01-gateway`.
- For runtime evidence after approval, check the Traefik dashboard and `docker compose exec traefik traefik healthcheck --ping` in the running root stack.
- For Nginx runtime evidence after approval, run `docker compose exec nginx nginx -t` only in the explicitly provisioned Nginx context.

#### Common Pitfalls

- **Cert Name Mismatch**: Ensure `tls.yaml` points to the correct filenames in `secrets/certs/`.
- **Port Conflicts**: Port 80 and 443 must be available on the host.
- **Network Isolation**: Backend services must be on `infra_net` to be discovered by Traefik.
- **Service-local Compose**: Standalone `infra/01-gateway/*/docker-compose.yml` rendering is not gateway readiness evidence because it lacks the root network/secret/dependency context.

## Common Checks

- Step-by-step Instructions 의 검증 단계를 따른다.

## Runbook Handoff

Runtime recovery is handled by [Traefik runbook](../0013-traefik/runbook.md) and [Nginx runbook](../0011-nginx/runbook.md).

## Related Documents

- [Operations index](../../../README.md)
- [Gateway Traefik guide](../0013-traefik/guide.md)
- [Gateway Nginx guide](../0011-nginx/guide.md)
