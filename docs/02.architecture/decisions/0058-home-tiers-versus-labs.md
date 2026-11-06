---
title: "HOME Tiers versus LABs"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "ADR-0058"
parent_ids:
- "AD-0004"
- "AD-0009"
- "AD-0011"
- "AD-0012"
- "AD-0019"
- "AD-0024"
- "AD-0025"
created: "2026-11-06"
---

# ADR-0058: HOME Tiers versus LABs

## Context

HOME is the set of services the root `docker-compose.yml` includes; they are
the always-on tier members. A LAB is a standalone package under `labs/<name>/`
with its own entrypoint, README and `promotion.yaml` (SPEC-0263); it is never
root-included, uses `lab-*` profiles and the isolated `${LAB_DATA_DIR}` root,
and becomes HOME only through the LAB promotion policy (POL-0107). SPEC-0262
moved the analytics engines into LABs.

HOME members by tier, from the root includes:

| Tier | HOME members |
| --- | --- |
| `04-data` | dev-db, mng-db, neo4j, opensearch, qdrant, redisinsight, seaweedfs |
| `05-messaging` | kafka |
| `06-observability` | LGTM stack, Alloy and the other observability services; dozzle |
| `07-workflow` | airflow, n8n |
| `08-ai` | comfyui, crawl4ai, mlflow, ollama, open-notebook, open-webui |
| `09-platform-ops` | opentofu, registry, renovate, restic, terrakube |
| `10-communication` | none |
| `11-quality` | conftest, k6, mailpit, pact-broker, wiremock |
| `12-analytics` | none |
| `13-experience` | storybook |

LABs: cassandra, couchdb, dbt, jupyterlab, kafka-cluster, lakehouse (Flink,
Spark, Trino, Great Expectations), locust, mongodb, opensearch-cluster,
postgresql-ha, sonarqube, stalwart, superset and valkey-cluster.

### Traceability

This record replaces seven accepted ADRs, deleted in the same change
(ADR-0051). Each one's still-valid decisions carry forward below.

- ADR-0009 selected the tooling stack: OpenTofu with Terrakube for IaC,
  SonarQube for code quality, k6 as the default load tool with Locust as an
  optional LAB (after ADR-0047), an OCI Distribution registry, and the
  withdrawal of Syncthing; admin UIs behind gateway and SSO, not assumed for CLI
  or registry protocols; persistence not counted as backup. It named no
  rejected candidates. SonarQube is now a LAB.
- ADR-0024 ordered the tooling hardening: the gateway and SSO chain on the
  SonarQube and Terrakube routers, an explicit `infra_net` boundary, a
  locust-worker healthcheck, k6 volume alignment, and the
  `check-all-hardening.sh 09-platform-ops 11-quality` gate, with OpenTofu drift
  detection, Terrakube audit, registry signing, a SonarQube quality gate and
  k6/Locust standardization in phases. Locust and SonarQube are now LABs, and
  `infra_net` is replaced by segmented networks
  ([ADR-0055](0055-segmented-per-flow-networks.md)).
- ADR-0025 ordered the laboratory hardening: no direct host ports for admin
  dashboards, `gateway-standard-chain + ipAllowList + sso-errors + sso-auth` on
  every laboratory router, a read-only Docker socket for Dozzle, an
  allowlist, large-body and SSO boundary for Open Notebook with Docker Secret
  credentials, the `check-all-hardening.sh 04-data 06-observability 08-ai`
  gate, and phased dashboard expiry, Dozzle scope, admin session and
  RedisInsight audit policies. The laboratory tier no longer exists; Dozzle
  and Open Notebook do not use `sso-auth` (native OIDC and an application
  password instead).
- ADR-0039 replaced ADR-0015's specialized engines after the lakehouse
  acceptance of 2026-09-24: OpenSearch for log and search, Flink for SQL stream
  processing between Kafka and Iceberg, Trino for SQL over Iceberg on
  SeaweedFS, no ksqlDB or StarRocks, time series handed to DEV TimescaleDB by
  ADR-0047. It rejected keeping ksqlDB and StarRocks beside Flink and Trino, and
  Spark alone. The engines now run in the lakehouse LAB (`lab-lakehouse`
  profile, checkpoints under `${LAB_DATA_DIR}`), not in a `lakehouse` HOME
  profile.
- ADR-0040 replaced ADR-0019's 04-data hardening: Compose contracts protected
  by `check-all-hardening.sh 04-data` and CI, new services adding their own
  checks, HA, lifecycle and recovery drills through approved procedures, and the
  `template-stateful-*` / `template-infra-*` inheritance model. It rejected an
  all-at-once HA expansion and documentation-only changes. Its items for
  supabase healthchecks, the `valkey-cluster-exporter` secret path and a
  SeaweedFS expose-token check no longer match: supabase was a LAB removed by
  owner decision on 2026-11-06, the Valkey cluster is a LAB with its own
  `lab_valkey_password`, and the gate has no expose-token check.
- ADR-0045 (SPEC-0197) split storage from processing: Data kept the stores,
  Analytics took Flink, Spark, Trino, Great Expectations, Superset and dbt,
  SeaweedFS stayed shared, dbt stayed on PostgreSQL, and tier numbering is a
  namespace, not start order or isolation. It rejected keeping eight Data
  categories and flattening all seventeen packages. Its Data list included
  supabase, the PostgreSQL and Valkey clusters, Cassandra, CouchDB and MongoDB;
  those are LABs now (supabase is being removed), and Analytics has no HOME
  member.
- ADR-0046 (SPEC-0197 option C, SPEC-0198) set capability tiers: Quality for
  software verification (with Great Expectations staying data quality in
  Analytics), Platform Operations for lifecycle packages, Dozzle moved to
  Observability, RedisInsight to Data, Open Notebook and MLflow to AI, the
  laboratory directory removed, identities and profiles preserved, and
  `09-platform-ops` naming. It rejected keeping the directories (A) and a
  six-package move (B). It placed Locust and SonarQube in Quality, Stalwart in
  Communication and JupyterLab in Analytics; those four are LABs now.

Evidence is the root Compose includes, `labs/`, and
`scripts/hardening/check-all-hardening.sh`. No runtime state is claimed.

## Decision Drivers

- HOME should contain only services that run every day, so its security and
  operations surface stays small.
- Experimental, clustered or heavy services need a place that cannot change
  HOME by accident.
- Tier placement follows capability, not activation style.
- Hardening gates must protect what exists, at the path where it exists.

## Options

### Alternatives

- Keep heavy and alternative services as opt-in profiles inside HOME tiers:
  rejected; profiles share the root project, data root and networks, so an
  experiment can change HOME.
- One ADR per tier restating HOME and LAB membership: rejected; the rule is the
  same for every tier and would be repeated nine times.
- One boundary rule, HOME by root include and LAB by `labs/`, with tier
  capability ownership and promotion by policy: selected.

## Decision

1. HOME is exactly the root Compose includes. A tier owns its HOME members by
   capability; tier numbers are a namespace, not start order or an isolation
   guarantee.
2. A LAB lives in `labs/<name>/`, is never root-included, uses `lab-*`
   profiles and `${LAB_DATA_DIR}`, and joins HOME only through POL-0107.
3. Data owns storage: dev-db (with DEV TimescaleDB for time series, ADR-0047),
   mng-db, neo4j, opensearch, qdrant, redisinsight and the shared seaweedfs.
   Clustered and alternative stores (postgresql-ha, valkey-cluster,
   opensearch-cluster, cassandra, couchdb, mongodb) are LABs.
4. Analytics owns processing and has no HOME member. The engine choice stands:
   Flink for streaming, Trino for SQL over Iceberg on SeaweedFS, Spark for table
   maintenance and batch, Great Expectations for data quality, Superset, dbt on
   PostgreSQL and JupyterLab, all as LABs. ksqlDB and StarRocks are not adopted;
   adding an engine for the same role needs a new ADR. Unauthenticated engine
   APIs bind only to loopback (POL-0094).
5. Platform Operations owns OpenTofu with Terrakube (IaC), the OCI registry,
   Renovate and Restic. Syncthing stays withdrawn.
6. Quality owns software verification: conftest, k6 (the default load tool),
   Mailpit, Pact Broker and WireMock. Locust and SonarQube are LABs.
   Communication owns no HOME member; Stalwart is a LAB
   ([ADR-0054](0054-mailpit-home-stalwart-lab.md)).
7. Admin UIs are reached only through Traefik, never by direct host ports, and
   keep these boundaries: Terrakube and RedisInsight behind
   `gateway-standard-chain` with `sso-errors` and `sso-auth` (RedisInsight also
   with an admin `ipAllowList`); Dozzle behind the chain and an admin
   allowlist with its own Keycloak OIDC and a read-only Docker socket; Open
   Notebook behind the chain, an admin allowlist and `large-body`, with its
   application password and database credentials as Docker Secrets.
8. `scripts/hardening/check-all-hardening.sh` per tier and the CI
   `infrastructure-hardening` job guard HOME members. A new service adds its
   checks to its tier. A LAB's checks run against its `labs/` source; moving a
   service between HOME and LAB moves its checks in the same change.
9. HOME services keep the `template-stateful-*` and `template-infra-*`
   inheritance. HA, lifecycle and recovery drills, OpenTofu drift detection,
   Terrakube audit, registry signing, load-test standardization, Dozzle scope,
   admin session and RedisInsight audit policies proceed in phases through
   approved policy and runbook changes.

## Consequences

- Positive: HOME's surface is the root include list, readable in one file.
- Positive: experiments cannot reach HOME data or profiles by accident.
- Negative: an analytics or clustered workload needs a LAB start or a promotion
  before use.
- Negative: hardening checks for LAB sources still run in tier functions,
  which must follow each move.

### Compliance

The root include list, `labs/<name>/promotion.yaml`, POL-0107 and
`check-all-hardening.sh` enforce the boundary; `tests/validation/test_infra_tier_layout.py`
fails on a renamed or retired tier.

### Follow-up

Requirement and description text that still places a LAB in a HOME tier is
reconciled by its owners.

## Related Documents

- [AD-0004 Data architecture](../descriptions/0004-data-architecture.md)
- [AD-0009 Platform operations and verification](../descriptions/0009-tooling-architecture.md)
- [AD-0011 Administration and experimentation](../descriptions/0011-laboratory-architecture.md)
- [AD-0012 Data analytics](../descriptions/0012-data-analytics-architecture.md)
- [AD-0019 Data hardening](../descriptions/0019-data-optimization-hardening-architecture.md)
- [AD-0024 Platform operations and quality hardening](../descriptions/0024-tooling-optimization-hardening-architecture.md)
- [AD-0025 Admin and experiment tools hardening](../descriptions/0025-laboratory-optimization-hardening-architecture.md)
- [REQ-0005 Data analytics](../../01.requirements/0005-data-analytics.md)
- [ADR-0047 DEV TimescaleDB and load tools](0047-dev-timescale-influx-retirement-and-load-tools.md)
- [POL-0094 Lakehouse](../../05.operations/policies/15-labs/0094-lakehouse.md)
- [POL-0107 LAB promotion](../../05.operations/policies/15-labs/0107-lab-promotion.md)
