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

## Related References

- **Guide**: [SonarQube Guide](../../../docs/07.guides/09-tooling/sonarqube.md)
- **Operation**: [SonarQube Operations](../../../docs/08.operations/09-tooling/sonarqube.md)
- **Runbook**: [SonarQube Runbook](../../../docs/09.runbooks/09-tooling/sonarqube.md)
