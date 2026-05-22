<!-- [ID:09-tooling:sonarqube] -->
# SonarQube Code Quality

> Continuous code quality inspection and security scanning.

## Overview

SonarQube provides static application security testing (SAST) and code quality metrics. It integrates with the platform's PostgreSQL management database for persistence and uses Traefik for secure external access.

## Audience

이 README의 주요 독자:

- Developers (PR analysis)
- Security Engineers (Vulnerability scanning)
- Operators
- AI Agents

## Scope

### In Scope

- SonarQube Community Edition service.
- Integration with external management PostgreSQL.
- ElasticSearch-based search index management.
- Traefik routing configuration.

### Out of Scope

- CI/CD pipeline implementation (managed in individual project repositories).
- Management Database lifecycle (managed in `04-data`).
- SonarLint IDE configuration (client-side).

## Structure

```text
sonarqube/
├── README.md           # This file
└── docker-compose.yml  # Service definition
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Service** | SonarQube Community | v10.7.0 |
| **Database** | PostgreSQL | Management Cluster |
| **Network** | Traefik | SSL termination |
| **Storage** | Bind Mount | `${DEFAULT_TOOLING_DIR}/sonarqube` |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `SONARQUBE_PORT` | No | Listening port (default: 9000). |
| `SONARQUBE_DBNAME` | Yes | Target database name. |
| `SONARQUBE_DB_USER` | Yes | Database username. |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose up -d` | Start the SonarQube service. |
| `docker compose logs -f` | View real-time service logs. |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect SonarQube.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking SonarQube documentation ready.

## Troubleshooting

- Start with `docker compose config` to confirm SonarQube DB, network, and secret references render.
- Check SonarQube logs and the linked runbook before changing database or quality-gate settings.

## Related Documents

- **Guide**: [SonarQube Guide](../../../docs/05.operations/guides/09-tooling/sonarqube.md)
- **Operation**: [SonarQube Operations](../../../docs/05.operations/guides/09-tooling/sonarqube.md)
- **Runbook**: [SonarQube Runbook](../../../docs/05.operations/guides/09-tooling/sonarqube.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | SonarQube Code Quality service leaf in `09-tooling`; services: `sonarqube`; root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/sonarqube/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `SONAR_JDBC_URL`, `SONAR_JDBC_USERNAME`, `SONAR_JDBC_PASSWORD_FILE`, `SONAR_WEB_JAVAOPTS`, `SONAR_SEARCH_JAVAOPTS`; profiles: `tooling`, `sast` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/sonarqube/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `sonarqube-data-volume:/opt/sonarqube/data:rw`, `sonarqube-logs-volume:/opt/sonarqube/logs:rw`, `sonarqube-data-volume`, `sonarqube-logs-volume` |
| Ports | `${SONARQUBE_PORT:-9000}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.sonarqube.rule`, `traefik.http.routers.sonarqube.entrypoints`, `traefik.http.routers.sonarqube.tls`, `traefik.http.routers.sonarqube.middlewares`, `traefik.http.services.sonarqube.loadbalancer.server.port` |
| Secret refs | names: `sonarqube_db_password`; mounts: `/run/secrets/sonarqube_db_password` |
| Healthcheck | Compose healthcheck declared for `sonarqube` |
| Operations | [Guide](../../../docs/05.operations/guides/09-tooling/sonarqube.md), [Policy](../../../docs/05.operations/policies/09-tooling/sonarqube.md), [Runbook](../../../docs/05.operations/runbooks/09-tooling/sonarqube.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
