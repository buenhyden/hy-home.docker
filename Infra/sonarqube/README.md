# SonarQube

## Overview

Automated code review and code quality analysis tool.

## Service Details

- **Image**: `sonarqube:26.1.0.118079-community`
- **Database**: Connects to the main `postgresql-cluster` or a dedicated DB (Env: `SONAR_JDBC_URL`).
- **Port**: `${SONARQUBE_PORT}` (9000).

## Environment Variables

- `SONAR_JDBC_URL`
- `SONAR_JDBC_USERNAME`
- `SONAR_JDBC_PASSWORD`

## Traefik Configuration

- **Domain**: `sonarqube.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS enabled)
