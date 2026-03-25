<!-- [ID:04-data:mongodb] -->
# MongoDB Replica Set

> Document-based NoSQL database for unstructured data.

## Overview (KR)

이 서비스는 고용량 데이터와 스키마리스 문서 저장에 최적화된 **분산 NoSQL 데이터베이스**입니다. 레플리카 셋 구성을 통해 자동 장애 조치와 데이터 가용성을 보장합니다.

## Overview

The `mongodb` stack provides a resilient document storage layer for `hy-home.docker`. It features a 3-node replica set (Primary, Secondary, Arbiter) with automated failover and integrated management via Mongo Express.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **mongodb-rep1, 2** | MongoDB 8.2 | Primary/Secondary Data Nodes |
| **mongodb-arbiter** | MongoDB 8.2 | Voting Node (No Data) |
| **mongo-express** | Mongo Express | Management Web UI |
| **mongodb-exporter** | MongoDB Exporter | Prometheus Compatibility |

## Networking

| Service | Port | Description |
| :--- | :--- | :--- |
| **DB Port** | `27017` | Standard MongoDB connection. |
| **Express UI** | `8081` | Management Dashboard (`mongo-express.${DEFAULT_URL}`). |
| **Exporter** | `9216` | Metrics scrape endpoint. |

## Persistence

- **Volumes**: `mongodb1-data`, `mongodb2-data` for data nodes.
- **Secrets**: `mongodb_root_password` for cluster security.
- **Path**: `${DEFAULT_DATA_DIR}/mongodb` on the host for static configs.

## Operations

### Checking Cluster Status

```bash
docker exec -it mongodb-rep1 mongosh -u admin -p <password> --eval "rs.status()"
```

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Replica set and tools definition. |
| `configdb/` | Security key and configuration files. |

---

## Documentation References

- [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md)
- [Recovery Runbook](../../../docs/09.runbooks/04-data/README.md)
