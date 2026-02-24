# SonarQube

SonarQube is a self-managed, automatic code review tool that systematically helps you deliver Clean Code.

## Services

| Service     | Image                      | Role           | Resources       |
| :---------- | :----------------------- | :------------- | :-------------- |
| `sonarqube` | `sonarqube:9.9-community`  | Code Analysis  | 2 CPU / 4GB RAM |

## Persistence

- **Data**: `/opt/sonarqube/data` (mounted to `sonarqube-data` volume).
- **PostgreSQL**: Uses an internal or shared database for state.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and analysis docs. |
