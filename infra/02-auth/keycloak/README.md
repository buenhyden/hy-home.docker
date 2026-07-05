# Keycloak IAM

> Identity and Access Management (IAM) provider based on Quarkus for the `hy-home.docker` ecosystem.

---

## Overview (KR)

Keycloak은 `hy-home.docker` 생태계의 중앙 ID 제공자(IdP)이다. 사용자 인증, 세션 관리, OIDC/SAML 토큰 발행을 처리하며, Quarkus 기반 배포판(`quay.io/keycloak/keycloak:26.6.4-1`)을 인프라망 내에서 컨테이너 환경에 최적화하여 운영한다.

## Audience

이 README의 주요 독자:

- Infrastructure Operators
- Security Reviewers
- AI Agents

## Scope

### In Scope

- Keycloak container runtime wiring under `infra/02-auth/keycloak/`
- Non-secret environment keys, healthcheck behavior, and compose references
- Links to canonical guide, policy, runbook, and auth spec

### Out of Scope

- Realm export contents, user credentials, token values, and secret file contents
- Application-specific RBAC policy design
- OAuth2 Proxy runtime configuration

## Structure

```text
keycloak/
├── docker-compose.yml  # Keycloak service definition and routing labels
└── README.md           # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Keycloak IAM service leaf in `02-auth`; services: `keycloak`; root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/02-auth/keycloak/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `KC_DB`, `KC_DB_URL`, `KC_DB_USERNAME`, `KC_DB_PASSWORD_FILE`, `KC_BOOTSTRAP_ADMIN_USERNAME`, `KC_HOSTNAME`, `KC_HTTP_ENABLED`, `KC_PROXY_HEADERS`, plus 6 more; profiles: `core`, `auth`, `dev` |
| Compose linkage | root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/02-auth/keycloak/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `keycloak-themes:/opt/keycloak/themes:ro`, `keycloak-config:/opt/keycloak/conf:ro`, `keycloak-providers:/opt/keycloak/providers:ro`, `keycloak-config`, `keycloak-providers`, `keycloak-themes` |
| Ports | `${KEYCLOAK_MANAGEMENT_PORT:-9000}`, `${KEYCLOAK_PORT:-8080}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.keycloak.rule`, `traefik.http.routers.keycloak.entrypoints`, `traefik.http.routers.keycloak.tls`, `traefik.http.routers.keycloak.middlewares`, `traefik.http.services.keycloak.loadbalancer.server.port` |
| Secret refs | names: `keycloak_db_password`, `keycloak_admin_password`; mounts: `/run/secrets/keycloak_db_password`, `/run/secrets/keycloak_admin_password` |
| Healthcheck | Compose healthcheck declared for `keycloak` |
| Operations | [Guide](../../../docs/05.operations/guides/02-auth/keycloak.md), [Policy](../../../docs/05.operations/policies/02-auth/keycloak.md), [Runbook](../../../docs/05.operations/runbooks/02-auth/keycloak.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. Read the linked operations guide, policy, and runbook before changing Keycloak configuration.
2. Keep all sensitive values behind Docker Secrets or mounted secret files.
3. After compose or config reference changes, run the validation commands listed below.

## Service Type

`infra-service | auth-provider`

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Platform   | Keycloak (Quarkus)             | `quay.io/keycloak/keycloak:26.6.4-1` |
| Database   | PostgreSQL                     | Identity Persistence      |
| Networking | Traefik                        | ForwardAuth/OIDC Ingress  |

## Configuration (Environment Variables)

- **KC_HOSTNAME**: `keycloak.${DEFAULT_URL}` (Public access URL)
- **KC_DB**: `postgres` (Database vendor)
- **KC_DB_URL**: `jdbc:postgresql://mng-pg:${POSTGRES_PORT:-5432}/${KEYCLOAK_DBNAME}`
- **KC_BOOTSTRAP_ADMIN_USERNAME**: `${KEYCLOAK_ADMIN_USER}` (Initial bootstrap user)
- **KC_PROXY_HEADERS**: `xforwarded` (Trusting reverse proxy)

## Healthcheck Strategy

Keycloak은 관리 포트(9000)를 통해 헬스체크를 수행하며, 인프라 부트스트래핑을 위해 `/dev/tcp` 소켓 방식을 사용하여 상태를 감지한다.

```yaml
healthcheck:
  test: ["CMD-SHELL", "exec 3<>/dev/tcp/127.0.0.1/9000; printf 'GET /health/ready HTTP/1.1\\r\\nHost: localhost\\r\\nConnection: close\\r\\n\\r\\n' >&3; cat <&3 | grep -Eq '\"status\"[[:space:]]*:[[:space:]]*\"UP\"'"]
  interval: 15s
  timeout: 30s
  retries: 5
```

## Validation

- Run `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh 02-auth` before marking documentation ready.
- Verify realm and client configuration by logging into the Keycloak admin console and confirming OIDC client settings match dependent services.
- Confirm OIDC discovery by checking `docker compose --profile auth logs keycloak --tail=200 | grep -i 'error\|warn'` after config changes.
- Verify admin credentials and database connectivity before declaring the service ready.

## Troubleshooting

- Start with `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh` to confirm root-context DB, secret, and Traefik label wiring.
- Check the `keycloak` container health endpoint and logs before changing realm, client, or secret references.

## Related Documents

- **Guide**: [Keycloak Operations Guide](../../../docs/05.operations/guides/02-auth/keycloak.md)
- **Operation**: [Keycloak Operations Policy](../../../docs/05.operations/policies/02-auth/keycloak.md)
- **Runbook**: [Keycloak Recovery Runbook](../../../docs/05.operations/runbooks/02-auth/keycloak.md)
- **Spec**: [02-auth Spec](../../../docs/03.specs/002-auth/spec.md)

## AI Agent Guidance

1. **Realm Provisioning**: 모든 신규 서비스 연동 시 `hy-home-core` 제품군에 속한 경우 `hy-home` 렐름을 공유하여 SSO를 달성하시오.
2. **Secret Injection**: `KC_DB_PASSWORD_FILE` 및 `KC_BOOTSTRAP_ADMIN_PASSWORD`는 반드시 `/run/secrets` 경로의 시크릿 파일을 참조해야 함.
3. **Health Check**: 서비스 기동 시 `9000/health/ready` 엔드포인트가 `UP` 상태가 될 때까지 의존성 서비스를 대기시키시오.
