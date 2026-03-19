# Prometheus

Prometheus is the core metrics collection and time-series database.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `prometheus` | `prom/prometheus:v3.9.0`| Time-Series DB | 2.0 CPU / 2GB RAM |

## Networking

| Endpoint                   | Port | Purpose                |
| :------------------------- | :--- | :--------------------- |
| `prometheus.${DEFAULT_URL}`| 9090 | Web UI / Query API     |

## Persistence

- **Data**: `/prometheus` (mounted to `prometheus-data` volume).
- **Retention**: 15 days (default).

## Configuration

- **Scrape Config**: Defined in `config/prometheus.yml`. Secrets are injected at startup via template substitution (`prometheus.yml.template`).
- **Rules**: Alerting and recording rules in `config/alert_rules/` (directory with multiple YAML files).

## File Map

| Path                       | Description                             |
| -------------------------- | --------------------------------------- |
| `config/prometheus.yml`    | Master scrape configuration (template). |
| `config/alert_rules/`      | Alerting/Recording rules (directory).   |
| `README.md`                | Service notes.                          |
