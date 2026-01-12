# SonarQube

## Overview

SonarQube is a self-managed, automatic code review tool that systematically helps you deliver clean code.

## Services

- **sonarqube**: SonarQube Server.
  - URL: `https://sonarqube.${DEFAULT_URL}`

## Configuration

### Environment Variables

- `SONAR_JDBC_URL`: Postgres JDBC URL.
- `SONAR_JDBC_USERNAME`: DB User.
- `SONAR_JDBC_PASSWORD`: DB Password.

### Volumes

- `sonarqube-data-volume`: `/opt/sonarqube/data`
- `sonarqube-logs-volume`: `/opt/sonarqube/logs`

## Networks

- `infra_net`

## Traefik Routing

- **Domain**: `sonarqube.${DEFAULT_URL}`
