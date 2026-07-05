---
status: active
---

<!-- Target: docs/90.references/data/docker/compose-profile-service-coverage.md -->

# Reference: Docker Compose Profile Service Coverage

## Overview

This generated reference maps tracked Docker Compose services to declared
Compose profiles and infrastructure stages. It is a static repository
snapshot; runtime truth remains in `infra/**/docker-compose*.yml` and the
root Compose entrypoint.

## Purpose

This reference supports audit reports and documentation reviews that need a
quick view of which services are included by default and which services are
gated behind Compose profiles.

## Repository Role

Use this document as derived inventory context only. Do not edit it by hand;
regenerate it with `bash scripts/operations/generate-compose-profile-service-coverage.sh`.
It does not replace Compose files, operations runbooks, or runtime validation.

## Scope

### In Scope

- Tracked root and `infra/**/docker-compose*.yml` / `.yaml` files.
- Compose service names, declared `profiles`, source file paths, and top-level
  infrastructure stage folders.
- Services without a `profiles` key, represented as `default`.

### Out of Scope

- Running `docker compose config` or resolving profile-specific includes.
- Runtime service health, container state, secrets, or environment values.
- Deployment guidance or rollback procedures.

## Definitions / Facts

- **default**: service has no Compose `profiles` key and is active whenever its
  Compose file is included.
- **profile-gated service**: service declares one or more Compose profiles.
- **stage**: first directory under `infra/`, such as `04-data` or `09-tooling`.
- **snapshot**: deterministic parse of tracked Compose files, not live runtime
  evidence.

## Snapshot Summary

| Metric | Value |
| --- | ---: |
| Compose files scanned | 49 |
| Compose files with services | 48 |
| Services discovered | 169 |
| Distinct profiles including `default` | 25 |
| Default services | 9 |
| Profile-gated service entries | 160 |

## Profile Coverage

| Profile | Service Count | Services |
| --- | ---: | --- |
| `admin` | 6 | `homer` (infra/11-laboratory/dashboard/docker-compose.yml), `dozzle` (infra/11-laboratory/dozzle/docker-compose.yml), `open_notebook` (infra/11-laboratory/open-notebook/docker-compose.yml), `surrealdb` (infra/11-laboratory/open-notebook/docker-compose.yml), `portainer` (infra/11-laboratory/portainer/docker-compose.yml), `redisinsight` (infra/11-laboratory/redisinsight/docker-compose.yml) |
| `ai` | 4 | `qdrant` (infra/04-data/specialized/qdrant/docker-compose.yml), `ollama` (infra/08-ai/ollama/docker-compose.yml), `ollama-exporter` (infra/08-ai/ollama/docker-compose.yml), `open-webui` (infra/08-ai/open-webui/docker-compose.yml) |
| `auth` | 5 | `keycloak` (infra/02-auth/keycloak/docker-compose.yml), `oauth2-proxy` (infra/02-auth/oauth2-proxy/docker-compose.dev.yml), `oauth2-proxy` (infra/02-auth/oauth2-proxy/docker-compose.yml), `oauth2-proxy-valkey` (infra/02-auth/oauth2-proxy/docker-compose.yml), `oauth2-proxy-valkey-exporter` (infra/02-auth/oauth2-proxy/docker-compose.yml) |
| `communication` | 2 | `mailhog` (infra/10-communication/mail/docker-compose.yml), `stalwart` (infra/10-communication/mail/docker-compose.yml) |
| `core` | 8 | `traefik` (infra/01-gateway/traefik/docker-compose.yml), `keycloak` (infra/02-auth/keycloak/docker-compose.yml), `oauth2-proxy` (infra/02-auth/oauth2-proxy/docker-compose.dev.yml), `oauth2-proxy` (infra/02-auth/oauth2-proxy/docker-compose.yml), `oauth2-proxy-valkey` (infra/02-auth/oauth2-proxy/docker-compose.yml), `oauth2-proxy-valkey-exporter` (infra/02-auth/oauth2-proxy/docker-compose.yml), `vault` (infra/03-security/vault/docker-compose.yml), `vault-agent` (infra/03-security/vault/docker-compose.yml) |
| `data` | 58 | `influxdb` (infra/04-data/analytics/influxdb/docker-compose.yml), `ksqldb-server` (infra/04-data/analytics/ksql/docker-compose.yml), `opensearch` (infra/04-data/analytics/opensearch/docker-compose.yml), `opensearch-dashboards` (infra/04-data/analytics/opensearch/docker-compose.yml), `starrocks-be` (infra/04-data/analytics/warehouses/docker-compose.yml), `starrocks-fe` (infra/04-data/analytics/warehouses/docker-compose.yml), `valkey-cluster-exporter` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-cluster-init` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-node-0` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-node-1` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-node-2` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-node-3` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-node-4` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-node-5` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `seaweedfs-filer` (infra/04-data/lake-and-object/seaweedfs/docker-compose.yml), `seaweedfs-master` (infra/04-data/lake-and-object/seaweedfs/docker-compose.yml), `seaweedfs-mount` (infra/04-data/lake-and-object/seaweedfs/docker-compose.yml), `seaweedfs-s3` (infra/04-data/lake-and-object/seaweedfs/docker-compose.yml), ... +40 more |
| `default` | 9 | `influxdb` (infra/04-data/analytics/influxdb/docker-compose.v2.yml), `opensearch-dashboards` (infra/04-data/analytics/opensearch/docker-compose.cluster.yml), `opensearch-node1` (infra/04-data/analytics/opensearch/docker-compose.cluster.yml), `opensearch-node2` (infra/04-data/analytics/opensearch/docker-compose.cluster.yml), `opensearch-node3` (infra/04-data/analytics/opensearch/docker-compose.cluster.yml), `minio1` (infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml), `minio2` (infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml), `minio3` (infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml), `minio4` (infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml) |
| `dev` | 48 | `traefik` (infra/01-gateway/traefik/docker-compose.yml), `keycloak` (infra/02-auth/keycloak/docker-compose.yml), `oauth2-proxy` (infra/02-auth/oauth2-proxy/docker-compose.dev.yml), `oauth2-proxy` (infra/02-auth/oauth2-proxy/docker-compose.yml), `vault` (infra/03-security/vault/docker-compose.yml), `vault-agent` (infra/03-security/vault/docker-compose.yml), `minio` (infra/04-data/lake-and-object/minio/docker-compose.yml), `minio-create-buckets` (infra/04-data/lake-and-object/minio/docker-compose.yml), `mng-pg` (infra/04-data/operational/mng-db/docker-compose.yml), `mng-pg-exporter` (infra/04-data/operational/mng-db/docker-compose.yml), `mng-pg-init` (infra/04-data/operational/mng-db/docker-compose.yml), `mng-valkey` (infra/04-data/operational/mng-db/docker-compose.yml), `mng-valkey-exporter` (infra/04-data/operational/mng-db/docker-compose.yml), `qdrant` (infra/04-data/specialized/qdrant/docker-compose.yml), `kafbat-ui` (infra/05-messaging/kafka/docker-compose.dev.yml), `kafka-1` (infra/05-messaging/kafka/docker-compose.dev.yml), `kafka-connect` (infra/05-messaging/kafka/docker-compose.dev.yml), `kafka-exporter` (infra/05-messaging/kafka/docker-compose.dev.yml), ... +30 more |
| `graph` | 1 | `neo4j` (infra/04-data/specialized/neo4j/docker-compose.yml) |
| `iac` | 4 | `terraform` (infra/09-tooling/terraform/docker-compose.yml), `terrakube-api` (infra/09-tooling/terrakube/docker-compose.yml), `terrakube-executor` (infra/09-tooling/terrakube/docker-compose.yml), `terrakube-ui` (infra/09-tooling/terrakube/docker-compose.yml) |
| `ksql` | 2 | `ksql-datagen` (infra/04-data/analytics/ksql/docker-compose.yml), `ksqldb-cli` (infra/04-data/analytics/ksql/docker-compose.yml) |
| `messaging` | 17 | `kafbat-ui` (infra/05-messaging/kafka/docker-compose.dev.yml), `kafka-1` (infra/05-messaging/kafka/docker-compose.dev.yml), `kafka-connect` (infra/05-messaging/kafka/docker-compose.dev.yml), `kafka-exporter` (infra/05-messaging/kafka/docker-compose.dev.yml), `kafka-init` (infra/05-messaging/kafka/docker-compose.dev.yml), `kafka-rest-proxy` (infra/05-messaging/kafka/docker-compose.dev.yml), `schema-registry` (infra/05-messaging/kafka/docker-compose.dev.yml), `kafbat-ui` (infra/05-messaging/kafka/docker-compose.yml), `kafka-1` (infra/05-messaging/kafka/docker-compose.yml), `kafka-2` (infra/05-messaging/kafka/docker-compose.yml), `kafka-3` (infra/05-messaging/kafka/docker-compose.yml), `kafka-connect` (infra/05-messaging/kafka/docker-compose.yml), `kafka-exporter` (infra/05-messaging/kafka/docker-compose.yml), `kafka-init` (infra/05-messaging/kafka/docker-compose.yml), `kafka-rest-proxy` (infra/05-messaging/kafka/docker-compose.yml), `schema-registry` (infra/05-messaging/kafka/docker-compose.yml), `rabbitmq` (infra/05-messaging/rabbitmq/docker-compose.yml) |
| `messaging-option` | 1 | `rabbitmq` (infra/05-messaging/rabbitmq/docker-compose.yml) |
| `mng` | 5 | `mng-pg` (infra/04-data/operational/mng-db/docker-compose.yml), `mng-pg-exporter` (infra/04-data/operational/mng-db/docker-compose.yml), `mng-pg-init` (infra/04-data/operational/mng-db/docker-compose.yml), `mng-valkey` (infra/04-data/operational/mng-db/docker-compose.yml), `mng-valkey-exporter` (infra/04-data/operational/mng-db/docker-compose.yml) |
| `nginx` | 1 | `nginx` (infra/01-gateway/nginx/docker-compose.yml) |
| `obs` | 22 | `minio` (infra/04-data/lake-and-object/minio/docker-compose.yml), `minio-create-buckets` (infra/04-data/lake-and-object/minio/docker-compose.yml), `cassandra-exporter` (infra/04-data/nosql/cassandra/docker-compose.yml), `mongodb-exporter` (infra/04-data/nosql/mongodb/docker-compose.yml), `alertmanager` (infra/06-observability/docker-compose.dev.yml), `alloy` (infra/06-observability/docker-compose.dev.yml), `cadvisor` (infra/06-observability/docker-compose.dev.yml), `grafana` (infra/06-observability/docker-compose.dev.yml), `loki` (infra/06-observability/docker-compose.dev.yml), `prometheus` (infra/06-observability/docker-compose.dev.yml), `pushgateway` (infra/06-observability/docker-compose.dev.yml), `pyroscope` (infra/06-observability/docker-compose.dev.yml), `tempo` (infra/06-observability/docker-compose.dev.yml), `alertmanager` (infra/06-observability/docker-compose.yml), `alloy` (infra/06-observability/docker-compose.yml), `cadvisor` (infra/06-observability/docker-compose.yml), `grafana` (infra/06-observability/docker-compose.yml), `loki` (infra/06-observability/docker-compose.yml), ... +4 more |
| `registry` | 1 | `registry` (infra/09-tooling/registry/docker-compose.yml) |
| `sast` | 1 | `sonarqube` (infra/09-tooling/sonarqube/docker-compose.yml) |
| `security` | 2 | `vault` (infra/03-security/vault/docker-compose.yml), `vault-agent` (infra/03-security/vault/docker-compose.yml) |
| `service` | 19 | `valkey-cluster-exporter` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-cluster-init` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-node-0` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-node-1` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-node-2` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-node-3` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-node-4` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `valkey-node-5` (infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml), `etcd-1` (infra/04-data/relational/postgresql-cluster/docker-compose.yml), `etcd-2` (infra/04-data/relational/postgresql-cluster/docker-compose.yml), `etcd-3` (infra/04-data/relational/postgresql-cluster/docker-compose.yml), `pg-0` (infra/04-data/relational/postgresql-cluster/docker-compose.yml), `pg-0-exporter` (infra/04-data/relational/postgresql-cluster/docker-compose.yml), `pg-1` (infra/04-data/relational/postgresql-cluster/docker-compose.yml), `pg-1-exporter` (infra/04-data/relational/postgresql-cluster/docker-compose.yml), `pg-2` (infra/04-data/relational/postgresql-cluster/docker-compose.yml), `pg-2-exporter` (infra/04-data/relational/postgresql-cluster/docker-compose.yml), `pg-cluster-init` (infra/04-data/relational/postgresql-cluster/docker-compose.yml), ... +1 more |
| `storage` | 2 | `minio` (infra/04-data/lake-and-object/minio/docker-compose.yml), `minio-create-buckets` (infra/04-data/lake-and-object/minio/docker-compose.yml) |
| `sync` | 1 | `syncthing` (infra/09-tooling/syncthing/docker-compose.yml) |
| `testing` | 2 | `k6-master` (infra/09-tooling/k6/docker-compose.yml), `locust-master` (infra/09-tooling/locust/docker-compose.yml) |
| `tooling` | 10 | `k6-master` (infra/09-tooling/k6/docker-compose.yml), `locust-master` (infra/09-tooling/locust/docker-compose.yml), `locust-worker` (infra/09-tooling/locust/docker-compose.yml), `registry` (infra/09-tooling/registry/docker-compose.yml), `sonarqube` (infra/09-tooling/sonarqube/docker-compose.yml), `syncthing` (infra/09-tooling/syncthing/docker-compose.yml), `terraform` (infra/09-tooling/terraform/docker-compose.yml), `terrakube-api` (infra/09-tooling/terrakube/docker-compose.yml), `terrakube-executor` (infra/09-tooling/terrakube/docker-compose.yml), `terrakube-ui` (infra/09-tooling/terrakube/docker-compose.yml) |
| `workflow` | 28 | `airflow-apiserver` (infra/07-workflow/airflow/docker-compose.dev.yml), `airflow-dag-processor` (infra/07-workflow/airflow/docker-compose.dev.yml), `airflow-init` (infra/07-workflow/airflow/docker-compose.dev.yml), `airflow-scheduler` (infra/07-workflow/airflow/docker-compose.dev.yml), `airflow-statsd-exporter` (infra/07-workflow/airflow/docker-compose.dev.yml), `airflow-triggerer` (infra/07-workflow/airflow/docker-compose.dev.yml), `airflow-worker` (infra/07-workflow/airflow/docker-compose.dev.yml), `flower` (infra/07-workflow/airflow/docker-compose.dev.yml), `airflow-apiserver` (infra/07-workflow/airflow/docker-compose.yml), `airflow-dag-processor` (infra/07-workflow/airflow/docker-compose.yml), `airflow-init` (infra/07-workflow/airflow/docker-compose.yml), `airflow-scheduler` (infra/07-workflow/airflow/docker-compose.yml), `airflow-statsd-exporter` (infra/07-workflow/airflow/docker-compose.yml), `airflow-triggerer` (infra/07-workflow/airflow/docker-compose.yml), `airflow-valkey` (infra/07-workflow/airflow/docker-compose.yml), `airflow-valkey-exporter` (infra/07-workflow/airflow/docker-compose.yml), `airflow-worker` (infra/07-workflow/airflow/docker-compose.yml), `flower` (infra/07-workflow/airflow/docker-compose.yml), ... +10 more |

## Stage Coverage

| Stage | Service Count | Profiles Seen |
| --- | ---: | --- |
| `01-gateway` | 2 | `core`, `dev`, `nginx` |
| `02-auth` | 5 | `auth`, `core`, `dev` |
| `03-security` | 2 | `core`, `dev`, `security` |
| `04-data` | 76 | `ai`, `data`, `default`, `dev`, `graph`, `ksql`, `mng`, `obs`, `service`, `storage` |
| `05-messaging` | 17 | `dev`, `messaging`, `messaging-option` |
| `06-observability` | 18 | `dev`, `obs` |
| `07-workflow` | 28 | `dev`, `workflow` |
| `08-ai` | 3 | `ai`, `dev` |
| `09-tooling` | 10 | `iac`, `registry`, `sast`, `sync`, `testing`, `tooling` |
| `10-communication` | 2 | `communication` |
| `11-laboratory` | 6 | `admin`, `dev` |

## Compose File Coverage

| Compose File | Service Count | Profiles Seen |
| --- | ---: | --- |
| `infra/01-gateway/nginx/docker-compose.yml` | 1 | `nginx` |
| `infra/01-gateway/traefik/docker-compose.yml` | 1 | `core`, `dev` |
| `infra/02-auth/keycloak/docker-compose.yml` | 1 | `auth`, `core`, `dev` |
| `infra/02-auth/oauth2-proxy/docker-compose.dev.yml` | 1 | `auth`, `core`, `dev` |
| `infra/02-auth/oauth2-proxy/docker-compose.yml` | 3 | `auth`, `core`, `dev` |
| `infra/03-security/vault/docker-compose.yml` | 2 | `core`, `dev`, `security` |
| `infra/04-data/analytics/influxdb/docker-compose.v2.yml` | 1 | `default` |
| `infra/04-data/analytics/influxdb/docker-compose.yml` | 1 | `data` |
| `infra/04-data/analytics/ksql/docker-compose.yml` | 3 | `data`, `ksql` |
| `infra/04-data/analytics/opensearch/docker-compose.cluster.yml` | 4 | `default` |
| `infra/04-data/analytics/opensearch/docker-compose.yml` | 2 | `data` |
| `infra/04-data/analytics/warehouses/docker-compose.yml` | 2 | `data` |
| `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml` | 8 | `data`, `service` |
| `infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml` | 4 | `default` |
| `infra/04-data/lake-and-object/minio/docker-compose.yml` | 2 | `dev`, `obs`, `storage` |
| `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml` | 5 | `data` |
| `infra/04-data/nosql/cassandra/docker-compose.yml` | 2 | `data`, `obs` |
| `infra/04-data/nosql/couchdb/docker-compose.yml` | 4 | `data` |
| `infra/04-data/nosql/mongodb/docker-compose.yml` | 7 | `data`, `obs` |
| `infra/04-data/operational/mng-db/docker-compose.yml` | 5 | `dev`, `mng` |
| `infra/04-data/operational/supabase/docker-compose.yml` | 13 | `data` |
| `infra/04-data/relational/postgresql-cluster/docker-compose.yml` | 11 | `data`, `service` |
| `infra/04-data/specialized/neo4j/docker-compose.yml` | 1 | `data`, `graph` |
| `infra/04-data/specialized/qdrant/docker-compose.yml` | 1 | `ai`, `data`, `dev` |
| `infra/05-messaging/kafka/docker-compose.dev.yml` | 7 | `dev`, `messaging` |
| `infra/05-messaging/kafka/docker-compose.yml` | 9 | `messaging` |
| `infra/05-messaging/rabbitmq/docker-compose.yml` | 1 | `messaging`, `messaging-option` |
| `infra/06-observability/docker-compose.dev.yml` | 9 | `dev`, `obs` |
| `infra/06-observability/docker-compose.yml` | 9 | `obs` |
| `infra/07-workflow/airflow/docker-compose.dev.yml` | 8 | `dev`, `workflow` |
| `infra/07-workflow/airflow/docker-compose.yml` | 10 | `workflow` |
| `infra/07-workflow/n8n/docker-compose.dev.yml` | 4 | `dev`, `workflow` |
| `infra/07-workflow/n8n/docker-compose.yml` | 6 | `workflow` |
| `infra/08-ai/ollama/docker-compose.yml` | 2 | `ai`, `dev` |
| `infra/08-ai/open-webui/docker-compose.yml` | 1 | `ai` |
| `infra/09-tooling/k6/docker-compose.yml` | 1 | `testing`, `tooling` |
| `infra/09-tooling/locust/docker-compose.yml` | 2 | `testing`, `tooling` |
| `infra/09-tooling/registry/docker-compose.yml` | 1 | `registry`, `tooling` |
| `infra/09-tooling/sonarqube/docker-compose.yml` | 1 | `sast`, `tooling` |
| `infra/09-tooling/syncthing/docker-compose.yml` | 1 | `sync`, `tooling` |
| `infra/09-tooling/terraform/docker-compose.yml` | 1 | `iac`, `tooling` |
| `infra/09-tooling/terrakube/docker-compose.yml` | 3 | `iac`, `tooling` |
| `infra/10-communication/mail/docker-compose.yml` | 2 | `communication` |
| `infra/11-laboratory/dashboard/docker-compose.yml` | 1 | `admin` |
| `infra/11-laboratory/dozzle/docker-compose.yml` | 1 | `admin`, `dev` |
| `infra/11-laboratory/open-notebook/docker-compose.yml` | 2 | `admin`, `dev` |
| `infra/11-laboratory/portainer/docker-compose.yml` | 1 | `admin` |
| `infra/11-laboratory/redisinsight/docker-compose.yml` | 1 | `admin`, `dev` |

## Source Rules

- Regenerate this file after adding, removing, or changing tracked Compose
  services or profiles.
- Treat this reference as advisory inventory; use Compose files for current
  implementation truth.
- Do not include secret values, `.env` values, container logs, or runtime
  inspection output.

## Sources

- [root Compose entrypoint](../../../../docker-compose.yml) - root Compose
  include boundary when tracked.
- [infra directory](../../../../infra/) - tracked service-local Compose files.
- [coverage generator](../../../../scripts/operations/generate-compose-profile-service-coverage.sh) - deterministic snapshot generator.

## Maintenance

- **Owner**: Infra/DevOps Engineer / Documentation Specialist.
- **Review Cadence**: Review after Compose service/profile changes.
- **Update Trigger**: Run the generator after tracked Compose files change.

## Related Documents

- **Docker data index**: [README.md](./README.md)
- **Docker image/version interpretation**: [image-version-interpretation.md](./image-version-interpretation.md)
- **Automation candidates**: [../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
- **Compose validation script**: [../../../../scripts/validation/validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh)
