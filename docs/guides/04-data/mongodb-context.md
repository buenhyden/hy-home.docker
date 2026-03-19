---
layer: infra
---
# MongoDB Replica Set Context

**Overview (KR):** MongoDB 레플리카 셋 아키텍처와 고가용성 문서 데이터베이스 운영을 위한 컨텍스트 가이드입니다.

> **Component**: `mongodb`
> **Profile**: `standalone` (Optional)
> **Internal Port**: `27017` (MongoDB Wire Protocol)
> **Replica Set Name**: `MyReplicaSet`

## 1. System Role

MongoDB serves as the document-oriented NoSQL backend for applications requiring flexible JSON/BSON schemas, geospatial queries, real-time analytics, and CMS content management. The replica set topology ensures automatic failover and data durability.

- **Internal DNS**: `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`
- **Web UI**: `https://mongo-express.${DEFAULT_URL}`

## 2. Topology

The deployment consists of a **Primary + Secondary + Arbiter** (PSA) replica set:

| Container | Role | Priority | Data |
| :--- | :--- | :--- | :--- |
| `mongodb-rep1` | Primary (preferred) | 2 | Yes |
| `mongodb-rep2` | Secondary | 1 | Yes |
| `mongodb-arbiter` | Arbiter (vote-only) | 0 | No |

The arbiter maintains an odd quorum for leader election without storing user data.

## 3. Bootstrapping

A one-shot `mongo-init` container executes `rs.initiate()` after all nodes are healthy. A `mongo-key-generator` container creates the inter-node authentication KeyFile (`/data/configdb/mongodb.key`) idempotently on first start.

## 4. Secrets & Configuration

| Variable / Secret | Description |
| :--- | :--- |
| `MONGODB_ROOT_USERNAME` | Admin username (from `.env`) |
| `mongodb_root_password` | Docker secret at `secrets/db/mongodb/mongodb_root_password.txt` |
| `mongo_express_basicauth_password` | Mongo Express basic auth password |

## 5. Connection Strings

**Replica Set connection (recommended):**

```text
mongodb://<user>:<pass>@mongodb-rep1:27017,mongodb-rep2:27017/admin?replicaSet=MyReplicaSet&authSource=admin
```

**Primary-only (admin tasks):**

```bash
docker exec -it mongodb-rep1 mongosh -u admin -p <password>
```

## 6. Persistence

| Volume | Container | Path |
| :--- | :--- | :--- |
| `mongo-key` | All nodes | `/data/configdb` (KeyFile) |
| `mongodb1-data` | `mongodb-rep1` | `/data/db` |
| `mongodb2-data` | `mongodb-rep2` | `/data/db` |
