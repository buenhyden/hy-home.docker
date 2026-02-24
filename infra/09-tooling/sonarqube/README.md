# SonarQube

SonarQube is a self-managed, automatic code review tool that systematically helps you deliver Clean Code.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `sonarqube` | `sonarqube:26.1.0...` | Code Quality | 1.0 CPU / 1GB RAM |

## Networking

- **URL**: `sonarqube.${DEFAULT_URL}` via Traefik.
- **Internal Port**: `${SONARQUBE_PORT}` (9000).

## Persistence

- **Data**: `sonarqube-data-volume` mapped to `/opt/sonarqube/data`.
- **Logs**: `sonarqube-logs-volume` mapped to `/opt/sonarqube/logs`.

## Configuration

- **Database**: External PostgreSQL (`mng-pg`) in `infra/04-data/mng-db`.
- **Java**: `-Xmx512m -Xms512m` for both Web and Search processes.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and analysis docs. |
