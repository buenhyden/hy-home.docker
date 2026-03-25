<!-- [ID:09-tooling:locust] -->
# Locust Cluster

> Scalable, distributed user load testing tool.

## 1. Overview (KR)

이 서비스는 수천 명의 동시 사용자를 시뮬레이션하여 시스템 성능을 측정하는 **분산 부하 테스트 도구**입니다. Python 스크립트를 통해 복잡한 시나리오를 자동화할 수 있습니다.

## 2. Overview

The `locust` stack enables performance benchmarking and stress testing for `hy-home.docker`. Running in a master-worker configuration, it provides real-time user simulation and exports performance metrics to InfluxDB for long-term analysis.

## 3. Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **locust-master** | Python 3 / Locust 2.43 | Test Orchestrator |
| **locust-worker** | Python 3 / Locust 2.43 | Load generator |

## 4. Networking

| Service | Port | Description |
| :--- | :--- | :--- |
| **Web UI** | `8089` | Test controller dashboard (`locust.${DEFAULT_URL}`). |
| **Master-Worker** | `5557` | Internal node communication. |

## 5. Persistence & Integration

- **Volumes**: `locust-data` → `${DEFAULT_TOOLING_DIR}/locust`.
- **Integration**: Exports to `influxdb` (04-data) via `influxdb_api_token`.
- **Secrets**: `influxdb_api_token`.

## 6. File Map

| Path | Description |
| :--- | :--- |
| `Dockerfile` | Custom image built on `locustio/locust:2.43.2`. |
| `docker-compose.yml` | Master and worker service definitions. |
| `locustfile.py` | Load test scenario scripts. |
| `README.md` | Service overview (this file). |

---

## Documentation References

- [Load Testing Guide](../../../docs/07.guides/09-tooling/load-testing-guide.md)
- [Observability Guide](../../../docs/07.guides/06-observability/README.md)
