# Load Testing Guide

Performance benchmarking procedures using Locust in `hy-home.docker`.

## 1. Environment Setup

The Locust stack is integrated with InfluxDB for metrics persistence.

- **URL**: `https://locust.${DEFAULT_URL}`
- **Auth**: Secured via Traefik/OIDC (where applicable).

## 2. Writing Test Scenarios

Locust scripts are written in Python (`locustfile.py`).

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index_page(self):
        self.client.get("/")
```

## 3. Distributed Execution

- **Scaling**: Increase workers via `docker compose up --scale locust-worker=N`.
- **Master Node**: Always view results on the master Web UI.

## 4. Analyzing Metrics

Metrics are exported to InfluxDB. Use the `Load Testing Dashboard` in Grafana for visualization.
