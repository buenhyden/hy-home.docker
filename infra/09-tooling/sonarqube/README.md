# SonarQube

SonarQube is a self-managed, automatic code review tool that systematically helps you deliver Clean Code.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `sonarqube` | `sonarqube:10.7.0-community` | Code Quality Analysis | 1.0 CPU / 1 GB RAM |

## Networking

- **URL**: `sonarqube.${DEFAULT_URL}` via Traefik.
- **Internal Port**: `${SONARQUBE_PORT}` (9000).

## Persistence

- **Data**: `sonarqube-data-volume` mapped to `/opt/sonarqube/data`.
- **Logs**: `sonarqube-logs-volume` mapped to `/opt/sonarqube/logs`.

## Configuration

- **Database**: External PostgreSQL (`mng-pg`) in `infra/04-data/mng-db`. Database name: `${SONARQUBE_DBNAME}`, user: `${SONARQUBE_DB_USER}`.
- **Java**: `-Xmx512m -Xms512m` for both Web and Search processes.
- **Authentication**: Default credentials `admin` / `admin`. **Change immediately on first login.**
- **Host Requirement**: Requires `vm.max_map_count >= 524288` on the Docker host for Elasticsearch.

## Secrets

| Secret | Description |
| :--- | :--- |
| `sonarqube_db_password` | PostgreSQL database password for the `sonarqube` user. |

## File Map

| Path                | Description                                    |
| ------------------- | ---------------------------------------------- |
| `docker-compose.yml`| Service definition with volumes and Traefik.   |
| `README.md`         | Service overview and analysis docs.            |
