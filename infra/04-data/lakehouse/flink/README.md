---
title: "Flink (Iceberg)"
version: "1.0.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2026-09-23"
---

<!-- [ID:04-data:lakehouse-flink] -->
# Flink (Iceberg)

> On-demand OPTIONAL Flink session cluster for streaming and batch SQL into Iceberg tables in the SeaweedFS REST catalog.

## Overview

Flink은 `lakehouse` profile로 선택되는 **OPTIONAL** stream processing engine입니다.
JobManager 하나와 TaskManager 하나(slot 2개)로 된 session cluster이며, catalog
`lakehouse`는 Spark·Trino와 같은 SeaweedFS Iceberg REST catalog와 `lakehouse`
S3 identity를 사용합니다. Kafka source와 sink는 `kafka_net`의 `kafka-1:19092`를
씁니다. REST API와 UI에 인증이 없으므로 `127.0.0.1`에만 게시하고 route는 없으며,
REST API로 JAR를 올릴 수 없습니다.

## Audience

이 README의 주요 독자:

- Data engineers
- Operators
- AI Agents

## Scope

### In Scope

- Session cluster (JobManager, TaskManager) with the Iceberg, AWS, Kafka and Hadoop client jars.
- The `lakehouse` catalog statement, the scoped S3 identity and file checkpoints.

### Out of Scope

- High availability, TLS, authentication and a Traefik route.
- Application mode and JAR submission through the REST API.
- Batch maintenance ([Spark](../spark/README.md)) and interactive SQL ([Trino](../trino/README.md)).

## Structure

```text
flink/
├── README.md           # This file
├── Dockerfile          # flink base plus checksum-pinned jars
├── docker-compose.yml  # flink-jobmanager, flink-taskmanager
└── hyhome-flink.sh     # Exports the secret, writes /tmp/lakehouse.sql, then runs the command
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Engine** | Apache Flink (base image in `Dockerfile`) | JobManager 1 CPU / 1.25 GiB, TaskManager 2 CPUs / 2 GiB, 2 slots |
| **Table format** | Iceberg Flink runtime | Same Iceberg version as Spark; SigV4 REST catalog, S3FileIO |
| **Streaming source** | Kafka SQL connector | `kafka-1:19092` on `kafka_net` |
| **State** | File checkpoints | `${DEFAULT_DATA_DIR}/flink/checkpoints`, shared by both containers |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `FLINK_HOST_PORT` | No | Loopback host port for the REST API and UI (default: 18091). |
| `SEAWEEDFS_ICEBERG_PORT` | No | REST catalog port on `seaweedfs-s3` (default: 8181). |
| `DEFAULT_DATA_DIR` | Yes | Parent of the checkpoint directory. |

The secret is `seaweedfs_s3_lakehouse_secret_key` (STRG-015); the access key ID
is `lakehouse`. Flink settings are `-D` arguments in `docker-compose.yml`; the
image configuration file is not edited.

## Available Scripts

Starting the service requires runtime approval. Create the checkpoint directory
first: `install -d -m 2770 -g "${SECRETS_GID:-1000}" "$DEFAULT_DATA_DIR/flink/checkpoints"`.

| Command | Description |
| :--- | :--- |
| `docker compose --profile lakehouse up -d flink-jobmanager flink-taskmanager` | Start the session cluster (writes nothing). |
| `docker compose exec flink-jobmanager bash /opt/hyhome/hyhome-flink.sh /opt/flink/bin/sql-client.sh -i /tmp/lakehouse.sql` | SQL client on the `lakehouse` catalog. |
| `docker compose exec flink-jobmanager /opt/flink/bin/flink list -a` | List jobs. |
| `docker compose exec flink-jobmanager /opt/flink/bin/flink cancel <job_id>` | Stop a job. |

## Validation

- `HYHOME_COMPOSE_PROFILES=lakehouse bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests.test_3_flink_writes_the_lakehouse_catalog`

## Troubleshooting

- Exit `64`: the `lakehouse` secret is missing or empty.
- `ClassNotFoundException: org.apache.hadoop.conf.Configuration`: a Hadoop client jar is missing from the image.
- No `lakehouse` catalog or an S3 `403` in the SQL client: it was started without the wrapper; run it through `hyhome-flink.sh` as above.
- A streaming `INSERT` that never commits: checkpointing is off; the wrapper sets a 60 s interval, and a session `SET` must not turn it off.
- Checkpoint `AccessDeniedException`: the host checkpoint directory is not group-writable; follow the lakehouse runbook.

## Related Documents

- **Guide**: Lakehouse Usage Guide (`docs/05.operations/catalog/04-data/0094-lakehouse/guide.md`)
- **Policy**: Lakehouse Operations Policy (`docs/05.operations/catalog/04-data/0094-lakehouse/policy.md`)
- **Runbook**: Lakehouse Recovery Runbook (`docs/05.operations/catalog/04-data/0094-lakehouse/runbook.md`)
- [Documentation index](../../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Flink leaf in `04-data/lakehouse`; services: `flink-jobmanager`, `flink-taskmanager`; unconditional root include, profile-selected, in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/lakehouse/flink/docker-compose.yml` |
| Config files | `Dockerfile`, `docker-compose.yml`, `hyhome-flink.sh` |
| Config values | profiles: `lakehouse` |
| Compose linkage | unconditional root include, profile-selected, in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/lakehouse/flink/docker-compose.yml` |
| Networks | `object_net`, `kafka_net` |
| Volumes | `./hyhome-flink.sh:/opt/hyhome/hyhome-flink.sh:ro`, `flink-checkpoints:/opt/flink/checkpoints` |
| Ports | `127.0.0.1:${FLINK_HOST_PORT:-18091}:8081` (JobManager) |
| Labels | `hy-home.tier` |
| Secret refs | `seaweedfs_s3_lakehouse_secret_key` |
| Healthcheck | JobManager `curl -fsS http://localhost:8081/overview`; TaskManager none (it waits for a healthy JobManager) |
| Operations | Guide (`docs/05.operations/catalog/04-data/0094-lakehouse/guide.md`), Policy (`docs/05.operations/catalog/04-data/0094-lakehouse/policy.md`), Runbook (`docs/05.operations/catalog/04-data/0094-lakehouse/runbook.md`) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Run `flink list -a`, then follow the runbook. |

## How to Work in This Area

1. Move the Iceberg version in the Flink and Spark Dockerfiles together; the Flink runtime jar name carries the Flink minor version.
2. Renovate updates only the `FROM` image; the jars are updated by hand with a new checksum. A Flink minor bump also needs the matching `iceberg-flink-runtime-<minor>` and Kafka connector jars.
3. A streaming `INSERT` runs until cancelled and commits on each checkpoint (60 s by default, from the wrapper); record the job ID and target table.

Runtime image authority is [docker-compose.yml](docker-compose.yml);
the [derived Compose image projection](../../../tech-stack.versions.json) is drift evidence.
