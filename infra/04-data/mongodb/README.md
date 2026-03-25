<!-- [ID:04-data:mongodb] -->
# MongoDB Replica Set

> Document-based NoSQL database for unstructured data.

## Overview (KR)

이 서비스는 고가용성과 데이터 내구성을 보장하는 **문서 기반 NoSQL 데이터베이스**입니다. 레플리카 셋 구성을 통해 자동 장애 조치와 데이터 복제를 지원합니다.

## Overview

The `mongodb` stack provides a resilient document storage layer for `hy-home.docker`. It features a 3-node replica set (Primary, Secondary, Arbiter) with automated failover and a management Web UI.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **mongodb-rep1, 2** | MongoDB 8.2 | Data Nodes |
| **mongodb-arbiter** | MongoDB 8.2 | Arbiter (Voting) |
| **mongo-express** | Mongo Express | Management UI |
| **mongodb-exporter**| Percona Exporter | Metrics |

## Networking

| Service | Access | Description |
| :--- | :--- | :--- |
| **DB Port** | `27017` | Standard MongoDB connection. |
| **Express UI** | `mongo-express.${DEFAULT_URL}` | Management Dashboard (Internal). |
| **Exporter** | `9216` | Prometheus metrics scrape. |

## Persistence

- **Volumes**: `mongodb1-data`, `mongodb2-data` for member nodes.
- **KeyFile**: `mongo-key` volume for internal cluster authentication.
- **Path**: `${DEFAULT_DATA_DIR}/mongodb` on the host.

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
| `init/` | Initialization scripts for automated setup. |

---

## Documentation References

- [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md)
- [Recovery Runbook](../../../docs/09.runbooks/04-data/README.md)
