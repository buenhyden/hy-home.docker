# SonarQube

## Overview

Automated code review and code quality analysis tool.

## Services

| Service | Image | Role |
| :--- | :--- | :--- |
| `sonarqube` | `sonarqube:26.1.0.118079-community` | Code Quality Server |

## Networking

Service runs on `infra_net` using **Dynamic** IP assignment (DHCP), unlike most other services in this stack.

| Service | IP Address | Internal Port | Traefik Domain |
| :--- | :--- | :--- | :--- |
| `sonarqube` | *(Dynamic)* | `${SONARQUBE_PORT}` | `sonarqube.${DEFAULT_URL}` |

## Persistence

- **Data**: `sonarqube-data-volume` → `/opt/sonarqube/data`
- **Logs**: `sonarqube-logs-volume` → `/opt/sonarqube/logs`

## Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SONAR_JDBC_URL` | JDBC Connection String | `jdbc:postgresql://...` |
| `SONAR_JDBC_USERNAME` | Database Username | `${SONARQUBE_DB_USER}` |
| `SONAR_JDBC_PASSWORD` | Database Password | `${SONARQUBE_DB_PASSWORD}` |

## Traefik Integration

Services are exposed via Traefik with TLS enabled (`websecure`).

- **Dashboard**: `sonarqube.${DEFAULT_URL}`

## Usage

1. **Dashboard**: Access `https://sonarqube.${DEFAULT_URL}`.
2. **First Login**: Default credentials `admin` / `admin`. You will be prompted to change these immediately.
