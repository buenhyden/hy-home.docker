# Keycloak IAM

> Identity and Access Management (IAM) provider based on Quarkus for the `hy-home.docker` ecosystem.

---

## Overview (KR)

Keycloak은 `hy-home.docker` 생태계의 중앙 ID 제공자(IdP)이다. 사용자 인증, 세션 관리, OIDC/SAML 토큰 발행을 처리하며, Quarkus 기반 배포판(v26.5.4)을 인프라망 내에서 컨테이너 환경에 최적화하여 운영한다.

## Service Type

`infra-service | auth-provider`

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Platform   | Keycloak (Quarkus)             | V26.5.4 (quay.io)         |
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

## Related Documents

- **Guide**: `[../../../docs/07.operations/02-auth/keycloak.md]`
- **Operation**: `[../../../docs/07.operations/02-auth/keycloak.md]`
- **Runbook**: `[../../../docs/07.operations/02-auth/keycloak.md]`
- **Spec**: `[../../../docs/04.specs/02-auth/spec.md]`

## AI Agent Guidance

1. **Realm Provisioning**: 모든 신규 서비스 연동 시 `hy-home-core` 제품군에 속한 경우 `hy-home` 렐름을 공유하여 SSO를 달성하시오.
2. **Secret Injection**: `KC_DB_PASSWORD_FILE` 및 `KC_BOOTSTRAP_ADMIN_PASSWORD`는 반드시 `/run/secrets` 경로의 시크릿 파일을 참조해야 함.
3. **Health Check**: 서비스 기동 시 `9000/health/ready` 엔드포인트가 `UP` 상태가 될 때까지 의존성 서비스를 대기시키시오.

---

## Overview

`infra/02-auth/keycloak`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Compose 서비스 정의와 관련 설정 설명
- 서비스별 README와 운영 문서 연결
- 검증 시 참고해야 할 구성 파일 인벤토리

### Out of Scope

- secret 값 원문
- 사용자 승인 없는 runtime 동작 변경
- 다른 tier의 서비스 정책 중복 정의

## Structure

```text
infra/02-auth/keycloak/
├── docker-compose.yml  # Docker Compose 정의
├── Dockerfile  # 구성 파일
└── README.md  # This file
```

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
