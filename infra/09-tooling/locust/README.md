# Locust Load Testing

> Distributed performance benchmarking and user simulation.

## Overview

Locust is used for load testing the platform's services. It supports distributed execution with a master node orchestrating multiple workers to simulate high concurrent traffic.

## Audience

- QA Engineers (Load testing)
- SREs (Capacity planning)

## Structure

```text
locust/
├── locustfile.py       # Default test script
├── Dockerfile          # Custom Locust build
├── docker-compose.yml  # Master/Worker orchestration
└── README.md           # This file
```

## How to Work in This Area

1. Read the [Performance Testing Guide](../../../docs/07.guides/09-tooling/02.performance-testing.md).
2. Access the UI at `http://${INTERNAL_IP}:18089`.

## Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| Testing | Locust | Distributed testing engine |
| Reporting | InfluxDB | Metrics backend |

## AI Agent Guidance

1. Scale workers using `docker compose up --scale locust-worker=N`.
2. Metrics are automatically pushed to InfluxDB if the API token is correctly mounted.
3. Custom Python dependencies for `locustfile.py` should be added to the local `Dockerfile`.
