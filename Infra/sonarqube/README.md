# SonarQube

## Overview

Automated code review and code quality analysis tool.

## Service Details

- **Image**: `sonarqube:26.1.0.118079-community`
- **Database**: Connects to the main `postgresql-cluster` or a dedicated DB (Env: `SONAR_JDBC_URL`).
- **Port**: `${SONARQUBE_PORT}` (9000).

## Network

Unlike other services in this infrastructure, SonarQube is configured with **Dynamic IP** assignment on the `infra_net` network.

| Service | IP Address |
| :--- | :--- |
| `sonarqube` | Dynamic (DHCP) |

## Environment Variables

- `SONAR_JDBC_URL`: Connection string for the database.
- `SONAR_JDBC_USERNAME`: Database user.
- `SONAR_JDBC_PASSWORD`: Database password.

## Traefik Configuration

- **Domain**: `sonarqube.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS enabled)
