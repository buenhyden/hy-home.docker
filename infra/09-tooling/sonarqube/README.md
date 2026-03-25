# SonarQube Code Quality

> Continuous code quality inspection and security scanning.

## Overview

SonarQube provides static application security testing (SAST) and code quality metrics. It integrates with the platform's PostgreSQL management database for persistence.

## Audience

- Developers (PR analysis)
- Security Engineers (Vulnerability scanning)

## Structure

```text
sonarqube/
├── docker-compose.yml  # SonarQube service configuration
└── README.md           # This file
```

## How to Work in This Area

1. Access the UI at `https://sonarqube.${DEFAULT_URL}`.
2. Login using Keycloak SSO.

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Quality | SonarQube Community | v10.7.0 |
| DB | PostgreSQL | Management Cluster |

## AI Agent Guidance

1. The `sonarqube` service requires `vm.max_map_count` to be at least 262144 on the host.
2. Database credentials are securely passed via Docker secrets (`sonarqube_db_password`).
3. Use the integrated SonarLint tools in IDEs for pre-commit feedback.
