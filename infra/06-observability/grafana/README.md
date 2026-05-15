# Grafana Visualization & Dashboards

Unified visualization hub for metrics, logs, traces, and profiling.

## Scope

Grafana serves as the primary observability portal for the `hy-home.docker` ecosystem. It integrates multiple data sources including Prometheus, Loki, Tempo, and Pyroscope into cohesive dashboards, providing a single pane of glass for monitoring, alerting, and debugging.

- **Primary URL**: `https://grafana.${DEFAULT_URL}`
- **Authentication**: Keycloak SSO (OIDC) with automatic role mapping.

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Frontend | Grafana | v12.3.3 |
| Auth | Generic OAuth2 | Keycloak Integration |

## System Components

- **Dashboards**: 34+ provisioned JSON dashboards across domains.
  - **Infrastructure**: Node Exporter, cAdvisor, Docker, Linux Hosts.
  - **Middleware**: PostgreSQL, Redis, Kafka, MinIO.
  - **AI/ML**: Ollama, Qdrant.
  - **Services**: Application-specific metrics and SLI/SLO views.
- **Datasources**: Pre-integrated Prometheus (metrics), Loki (logs), Tempo (traces), and Pyroscope (profiles).
- **Provisioning**: Entirely code-based configuration for datasources and dashboards.

## Documentation

| Document | Description |
| :--- | :--- |
| [System Guide](../../../docs/05.operations/guides/06-observability/grafana.md) | Architecture, SSO mapping, and datasource integration details. |
| [Operational Policy](../../../docs/05.operations/guides/06-observability/grafana.md) | Dashboard provisioning, RBAC, and datasource maintenance. |
| [Recovery Runbook](../../../docs/05.operations/guides/06-observability/grafana.md) | Troubleshooting failing logins, dashboards, or service unavailability. |

## AI Agent Guidance

1. **Provisioning**: Dashboards MUST NOT be edit-locked in production. Always use code-based provisioning in the `dashboards/` directory.
2. **SSO Mapping**: Role mapping is managed via `GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH` in `docker-compose.yml`. Groups starting with `/admins` map to `Admin`.
3. **Variables**: Use Variables (Template tags) for cluster/node/service filtering to keep dashboards portable.
4. **Color Palette**: Adhere to the `hy-home.docker` visual standards for dashboard consistency.

---

## Overview

`infra/06-observability/grafana`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Structure

```text
infra/06-observability/grafana/
├── dashboards/  # 하위 구성 영역
├── provisioning/  # 하위 구성 영역
└── README.md  # This file
```

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Related Documents

- [infra/README.md](../../README.md)
- [docs/05.operations/README.md](../../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../../docs/05.operations/README.md)
