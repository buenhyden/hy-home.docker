# Prometheus

Prometheus is the core metrics collection and time-series database.

## Services

| Service      | Image                       | Role         | Resources       |
| :----------- | :-------------------------- | :----------- | :-------------- |
| `prometheus` | `prom/prometheus:v3.2.1`    | Metrics DB   | 1 CPU / 2GB RAM |

## Networking

| Endpoint                   | Port | Purpose                |
| :------------------------- | :--- | :--------------------- |
| `prometheus.${DEFAULT_URL}`| 9090 | Web UI / Query API     |

## Persistence

- **Data**: `/prometheus` (mounted to `prometheus-data` volume).
- **Retention**: 15 days (default).

## Configuration

- **Scrape Config**: Defined in `config/prometheus.yml`.
- **Rules**: Alerting and recording rules in `config/rules.yml`.

## File Map

| Path                 | Description                    |
| -------------------- | ------------------------------ |
| `config/prometheus.yml` | Master scrape configuration. |
| `config/rules.yml`   | Alerting/Recording rules.      |
| `README.md`          | Service notes.                 |
