---
title: "Kafka Messaging"
version: "1.1.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-18"
created: "2025-11-12"
---

# Kafka Messaging

> Kafka KRaft messaging stack with Schema Registry, Connect, REST Proxy, Kafbat UI, and exporter.

## Overview

`05-messaging/kafka`는 profile 기반 Kafka broker topology와 관련 관리 서비스를 제공한다.

Kafbat UI는 Keycloak application-native OAuth2/OIDC를 사용한다.
Traefik router에는 `gateway-standard-chain@file`만 적용하며 OAuth2 Proxy
ForwardAuth를 중복 적용하지 않는다.

## Audience

- Messaging Operators
- Developers
- Data Engineers
- AI Agents

## Scope

- Kafka broker(s)
- Schema Registry
- Kafka Connect
- Kafka REST Proxy
- Kafbat UI
- Kafka Exporter
- topic initialization

## Structure

```text
kafka/
├── docker-compose.yml
├── jmx-exporter/
├── kafbat-ui/
│   └── dynamic_config.template.yaml
└── README.md
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Single broker | `messaging`/`dev` -> `kafka-1` |
| Cluster | `messaging-cluster` adds `kafka-2`, `kafka-3` |
| Kafbat | `kafbat/kafka-ui:v1.5.0` |
| Kafbat auth | Keycloak Native OAuth2/OIDC |
| Kafbat secret | `kafbat_client_secret` |
| Kafbat health | `/actuator/health` |

## Kafbat Authentication

Client:
- `home-kafbat`

Issuer:
```text
https://keycloak.${DEFAULT_URL}/realms/hy-home.realm
```

Redirect:
```text
https://kafbat-ui.${DEFAULT_URL}/login/oauth2/code/keycloak
```

Roles field:
```text
groups
```

RBAC:
- `/admins` -> admin
- `/users` -> readonly

`rbac.roles[*].clusters`는 runtime `KAFKA_CLUSTERS_0_NAME`과 일치해야 한다.

## TLS Trust

Kafbat container는 JDK default `cacerts`를 `/tmp`로 복사하고 local
`rootCA.pem`을 import한다. 이 방식으로 public CA roots를 보존한다.

## How to Work in This Area

1. Kafka operations guide/runbook 확인.
2. root profile validation.
3. topic은 `kafka-init` contract 기준.
4. Kafbat auth 변경은 integration guide와 Keycloak client를 함께 확인.
5. Kafbat route에 `sso-auth@file`을 추가하지 않는다.

## Tech Stack

| Category | Technology |
| --- | --- |
| Kafka | Confluent CP-Kafka 8.3.x |
| Mode | KRaft |
| Registry | CP Schema Registry |
| Connect | CP Kafka Connect |
| UI | Kafbat UI |
| Exporter | Kafka Exporter |

## Testing

```bash
HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 05-messaging
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --list
```

Kafbat:
- `/actuator/health`
- login
- `/admins` admin
- `/users` readonly

## Change Impact

- broker topology 변경은 topic replication/ISR에 영향.
- Kafbat client/claim 변경은 UI access/RBAC에 영향.
- truststore 변경은 Keycloak 및 public HTTPS 연결에 영향.

## Troubleshooting

- broker health/listeners
- Schema Registry/Connect health
- Kafbat OAuth2 logs
- Kafbat cluster name exact match
- Keycloak group claim
- gateway-only route

## Related Documents

- **PRD**: `docs/01.requirements/0006-messaging.md`
- **Architecture**: `docs/02.architecture/descriptions/0005-messaging-architecture.md`
- **Guide**: `docs/05.operations/catalog/05-messaging/0036-kafka/guide.md`
- **Policy**: `docs/05.operations/catalog/05-messaging/0036-kafka/policy.md`
- **Runbook**: `docs/05.operations/catalog/05-messaging/0036-kafka/runbook.md`
- **Auth Integration**: `docs/05.operations/catalog/02-auth/0079-application-auth-integration/guide.md`
