---
profile_id: migration
status: completed
artifact_id: mig-0002
artifact_type: migration
parent_ids: [SPEC-0136]
created: 2026-08-13
updated: 2026-08-30
archived_from: docs/05.operations/README.md
archived_at: 2026-08-13T00:00:00+09:00
archive_reason: evidence-preserve
archive_disposition: evidence-preserve
archived_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
archived_blob: 8781b8031c541761e8f33bfce25df9856e2c02e8
preservation_class: git-history
---

# Operations Catalog Convergence Manifest

## Overview

This record freezes the exact Task 10B Operations inventory and the approved
structural and semantic dispositions. Approval authorizes the bounded later
execution tasks; this record itself does not move, rename, merge, or delete any
source document.

## Archive Metadata

- `migration_id`: `mig-0002`
- `baseline_commit`: `6f2703d8d245cf4e3576bece0bf247dd516b2bf3`
- `registration_commit`: `f9a010ccdc008a0265c5229631f918beaa484e1e`
- `inventory`: `77` subjects, `66` Guides, `64` Policies, `62` Runbooks, and
  `13` domain READMEs (`205` files total)
- `approval.status`: `approved`
- `approved_at`: `2026-08-13`
- `approved_by`: `user`
- `record_order`: source path ascending

## Proposed Subject Dispositions

The user explicitly approved every exact row below on 2026-08-13. `merge` means
that all four Spec criteria are recorded as proven in the machine block. Later
Tasks 10C-10G remain bounded by this exact approved map and their own gates.

| Current subject | Proposed domain/path | Action | Canonical owner | Roles retained / predecessor removed | Reason |
| :-- | :-- | :-- | :-- | :-- | :-- |
| `ops-0001` | `docs/05.operations/catalog/00-workspace/ops-0001-common-optimizations-template-exceptions` | `retain` | `ops-0001` | retain policy | Retain managed object or capability `common-optimizations-template-exceptions` as `ops-0001`; its policy evidence owns an independent operational boundary. |
| `ops-0002` | `docs/05.operations/catalog/00-workspace/ops-0002-developer-environment` | `rename` | `ops-0002` | retain guide | Replace generic setup wording with the developer-environment lifecycle this Guide actually owns. |
| `ops-0003` | `docs/05.operations/catalog/00-workspace/ops-0003-env-key-comparison` | `retain` | `ops-0003` | retain guide | Retain managed object or capability `env-key-comparison` as `ops-0003`; its guide evidence owns an independent operational boundary. |
| `ops-0004` | `docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering` | `retain` | `ops-0004` | retain guide, policy | Retain managed object or capability `harness-agent-first-engineering` as `ops-0004`; its guide, policy evidence owns an independent operational boundary. |
| `ops-0005` | `docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering` | `merge` | `ops-0004` | merge runbook; remove predecessor after approved semantic execution | The validation Runbook governs the same repository harness capability, owner, trigger, verification, and rollback boundary as ops-0004 and has no independent cadence or evidence owner. |
| `ops-0006` | `docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance` | `rename` | `ops-0006` | retain policy | Name the workspace-wide infrastructure optimization governance boundary and remove the catalog role word. |
| `ops-0007` | `docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance` | `retain` | `ops-0007` | retain guide, policy, runbook | Retain managed object or capability `llm-wiki-maintenance` as `ops-0007`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0008` | `docs/05.operations/catalog/00-workspace/ops-0008-new-service-onboarding` | `retain` | `ops-0008` | retain guide | Retain managed object or capability `new-service-onboarding` as `ops-0008`; its guide evidence owns an independent operational boundary. |
| `ops-0009` | `docs/05.operations/catalog/00-workspace/ops-0009-release-management` | `retain` | `ops-0009` | retain runbook | Retain managed object or capability `release-management` as `ops-0009`; its runbook evidence owns an independent operational boundary. |
| `ops-0010` | `docs/05.operations/catalog/00-workspace/ops-0010-sensitive-env-vars-comparison` | `retain` | `ops-0010` | retain guide | Retain managed object or capability `sensitive-env-vars-comparison` as `ops-0010`; its guide evidence owns an independent operational boundary. |
| `ops-0011` | `docs/05.operations/catalog/01-gateway/ops-0011-nginx` | `retain` | `ops-0011` | retain guide, policy, runbook | Retain managed object or capability `nginx` as `ops-0011`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0012` | `docs/05.operations/catalog/01-gateway/ops-0012-edge-routing-stack` | `rename` | `ops-0012` | retain guide | Replace generic setup wording with the Nginx and Traefik edge-routing stack boundary. |
| `ops-0013` | `docs/05.operations/catalog/01-gateway/ops-0013-traefik` | `retain` | `ops-0013` | retain guide, policy, runbook | Retain managed object or capability `traefik` as `ops-0013`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0014` | `docs/05.operations/catalog/02-auth/ops-0014-keycloak` | `retain` | `ops-0014` | retain guide, policy, runbook | Retain managed object or capability `keycloak` as `ops-0014`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0015` | `docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy` | `retain` | `ops-0015` | retain guide, policy, runbook | Retain managed object or capability `oauth2-proxy` as `ops-0015`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0016` | `docs/05.operations/catalog/03-security/ops-0016-vault` | `retain` | `ops-0016` | retain guide, policy, runbook | Retain managed object or capability `vault` as `ops-0016`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0017` | `docs/05.operations/catalog/04-data/ops-0017-influxdb` | `rename` | `ops-0017` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `analytics-influxdb` and name the managed `influxdb` object directly. |
| `ops-0018` | `docs/05.operations/catalog/04-data/ops-0018-ksqldb` | `rename` | `ops-0018` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `analytics-ksqldb` and name the managed `ksqldb` object directly. |
| `ops-0019` | `docs/05.operations/catalog/04-data/ops-0019-opensearch` | `rename` | `ops-0019` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `analytics-opensearch` and name the managed `opensearch` object directly. |
| `ops-0020` | `docs/05.operations/catalog/04-data/ops-0020-starrocks` | `rename` | `ops-0020` | retain guide, policy, runbook | Replace the analytics category alias with the actual managed StarRocks object. |
| `ops-0021` | `docs/05.operations/catalog/04-data/ops-0021-backup-and-restore` | `rename` | `ops-0021` | retain policy | Remove the repeated backup token and policy role word; name the backup-and-restore control boundary. |
| `ops-0022` | `docs/05.operations/catalog/04-data/ops-0022-valkey-cluster` | `rename` | `ops-0022` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `cache-and-kv-valkey-cluster` and name the managed `valkey-cluster` object directly. |
| `ops-0023` | `docs/05.operations/catalog/04-data/ops-0023-minio` | `rename` | `ops-0023` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `lake-and-object-minio` and name the managed `minio` object directly. |
| `ops-0024` | `docs/05.operations/catalog/04-data/ops-0024-seaweedfs` | `rename` | `ops-0024` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `lake-and-object-seaweedfs` and name the managed `seaweedfs` object directly. |
| `ops-0025` | `docs/05.operations/catalog/04-data/ops-0025-cassandra` | `rename` | `ops-0025` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `nosql-cassandra` and name the managed `cassandra` object directly. |
| `ops-0026` | `docs/05.operations/catalog/04-data/ops-0026-couchdb` | `rename` | `ops-0026` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `nosql-couchdb` and name the managed `couchdb` object directly. |
| `ops-0027` | `docs/05.operations/catalog/04-data/ops-0027-mongodb` | `rename` | `ops-0027` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `nosql-mongodb` and name the managed `mongodb` object directly. |
| `ops-0028` | `docs/05.operations/catalog/04-data/ops-0028-management-database` | `rename` | `ops-0028` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `operational-mng-db` and name the managed `management-database` object directly. |
| `ops-0029` | `docs/05.operations/catalog/04-data/ops-0029-supabase` | `rename` | `ops-0029` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `operational-supabase` and name the managed `supabase` object directly. |
| `ops-0030` | `docs/05.operations/catalog/04-data/ops-0030-optimization-hardening` | `rename` | `ops-0030` | retain guide, policy, runbook | Remove the repeated optimization token while retaining the data-domain hardening capability. |
| `ops-0031` | `docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster` | `rename` | `ops-0031` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `relational-postgresql-cluster` and name the managed `postgresql-cluster` object directly. |
| `ops-0032` | `docs/05.operations/catalog/04-data/ops-0032-postgresql-logical-upgrade-restore-rehearsal` | `rename` | `ops-0032` | retain runbook | Remove the relational taxonomy prefix while retaining the independent PostgreSQL upgrade rehearsal. |
| `ops-0033` | `docs/05.operations/catalog/04-data/ops-0033-neo4j` | `rename` | `ops-0033` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `specialized-neo4j` and name the managed `neo4j` object directly. |
| `ops-0034` | `docs/05.operations/catalog/04-data/ops-0034-qdrant` | `rename` | `ops-0034` | retain guide, policy, runbook | Remove the domain/category taxonomy prefix from `specialized-qdrant` and name the managed `qdrant` object directly. |
| `ops-0035` | `docs/05.operations/catalog/04-data/ops-0035-storage-exhaustion` | `rename` | `ops-0035` | retain runbook | Remove the repeated storage token while retaining the independent exhaustion recovery trigger. |
| `ops-0036` | `docs/05.operations/catalog/05-messaging/ops-0036-kafka` | `retain` | `ops-0036` | retain guide, policy, runbook | Retain managed object or capability `kafka` as `ops-0036`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0037` | `docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening` | `retain` | `ops-0037` | retain guide, policy, runbook | Retain managed object or capability `optimization-hardening` as `ops-0037`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0038` | `docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq` | `retain` | `ops-0038` | retain guide, policy, runbook | Retain managed object or capability `rabbitmq` as `ops-0038`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0039` | `docs/05.operations/catalog/06-observability/ops-0039-alertmanager` | `retain` | `ops-0039` | retain guide, policy, runbook | Retain managed object or capability `alertmanager` as `ops-0039`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0040` | `docs/05.operations/catalog/06-observability/ops-0040-alloy` | `retain` | `ops-0040` | retain guide, policy, runbook | Retain managed object or capability `alloy` as `ops-0040`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0041` | `docs/05.operations/catalog/06-observability/ops-0041-grafana` | `retain` | `ops-0041` | retain guide, policy, runbook | Retain managed object or capability `grafana` as `ops-0041`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0042` | `docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack` | `retain` | `ops-0042` | retain guide | Retain managed object or capability `lgtm-stack` as `ops-0042`; its guide evidence owns an independent operational boundary. |
| `ops-0043` | `docs/05.operations/catalog/06-observability/ops-0043-loki` | `retain` | `ops-0043` | retain guide, policy, runbook | Retain managed object or capability `loki` as `ops-0043`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0044` | `docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening` | `retain` | `ops-0044` | retain guide, policy, runbook | Retain managed object or capability `optimization-hardening` as `ops-0044`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0045` | `docs/05.operations/catalog/06-observability/ops-0045-prometheus` | `retain` | `ops-0045` | retain guide, policy, runbook | Retain managed object or capability `prometheus` as `ops-0045`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0046` | `docs/05.operations/catalog/06-observability/ops-0046-pushgateway` | `retain` | `ops-0046` | retain guide, policy, runbook | Retain managed object or capability `pushgateway` as `ops-0046`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0047` | `docs/05.operations/catalog/06-observability/ops-0047-pyroscope` | `retain` | `ops-0047` | retain guide, policy, runbook | Retain managed object or capability `pyroscope` as `ops-0047`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0048` | `docs/05.operations/catalog/06-observability/ops-0048-telemetry-retention` | `rename` | `ops-0048` | retain policy | Replace generic retention wording with the cross-backend telemetry retention control boundary. |
| `ops-0049` | `docs/05.operations/catalog/06-observability/ops-0049-tempo` | `retain` | `ops-0049` | retain guide, policy, runbook | Retain managed object or capability `tempo` as `ops-0049`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0050` | `docs/05.operations/catalog/07-workflow/ops-0050-airflow` | `retain` | `ops-0050` | retain guide, policy, runbook | Retain managed object or capability `airflow` as `ops-0050`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0051` | `docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle` | `rename` | `ops-0051` | retain guide | Replace unsupported basics wording with the independent Airflow DAG authoring and deployment lifecycle. |
| `ops-0052` | `docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle` | `merge` | `ops-0051` | merge policy; remove predecessor after approved semantic execution | The DAG deployment Policy governs the same Airflow DAG lifecycle, owner, lint and secret controls, dags-list verification, and ops-0050 recovery handoff as ops-0051 and has no independent evidence boundary. |
| `ops-0053` | `docs/05.operations/catalog/07-workflow/ops-0053-n8n` | `retain` | `ops-0053` | retain guide, policy, runbook | Retain managed object or capability `n8n` as `ops-0053`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0054` | `docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening` | `retain` | `ops-0054` | retain guide, policy, runbook | Retain managed object or capability `optimization-hardening` as `ops-0054`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0055` | `docs/05.operations/catalog/08-ai/ops-0055-gpu-recovery` | `retain` | `ops-0055` | retain runbook | Retain managed object or capability `gpu-recovery` as `ops-0055`; its runbook evidence owns an independent operational boundary. |
| `ops-0056` | `docs/05.operations/catalog/08-ai/ops-0056-ollama` | `retain` | `ops-0056` | retain guide, policy, runbook | Retain managed object or capability `ollama` as `ops-0056`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0057` | `docs/05.operations/catalog/08-ai/ops-0057-open-webui` | `retain` | `ops-0057` | retain guide, policy, runbook | Retain managed object or capability `open-webui` as `ops-0057`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0058` | `docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening` | `retain` | `ops-0058` | retain guide, policy, runbook | Retain managed object or capability `optimization-hardening` as `ops-0058`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0059` | `docs/05.operations/catalog/08-ai/ops-0059-rag-workflow` | `retain` | `ops-0059` | retain guide | Retain managed object or capability `rag-workflow` as `ops-0059`; its guide evidence owns an independent operational boundary. |
| `ops-0060` | `docs/05.operations/catalog/09-tooling/ops-0060-iac-deployment` | `rename` | `ops-0060` | retain policy | Remove the policy role word while retaining the cross-tool IaC deployment control boundary. |
| `ops-0061` | `docs/05.operations/catalog/09-tooling/ops-0061-k6` | `retain` | `ops-0061` | retain guide, policy, runbook | Retain managed object or capability `k6` as `ops-0061`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0062` | `docs/05.operations/catalog/09-tooling/ops-0062-locust` | `retain` | `ops-0062` | retain guide, policy, runbook | Retain managed object or capability `locust` as `ops-0062`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0063` | `docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening` | `retain` | `ops-0063` | retain guide, policy, runbook | Retain managed object or capability `optimization-hardening` as `ops-0063`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0064` | `docs/05.operations/catalog/09-tooling/ops-0064-performance-testing` | `retain` | `ops-0064` | retain guide, policy, runbook | Retain managed object or capability `performance-testing` as `ops-0064`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0065` | `docs/05.operations/catalog/09-tooling/ops-0065-registry` | `retain` | `ops-0065` | retain guide, policy, runbook | Retain managed object or capability `registry` as `ops-0065`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0066` | `docs/05.operations/catalog/09-tooling/ops-0066-sonarqube` | `retain` | `ops-0066` | retain guide, policy, runbook | Retain managed object or capability `sonarqube` as `ops-0066`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0067` | `docs/05.operations/catalog/09-tooling/ops-0067-syncthing` | `retain` | `ops-0067` | retain guide, policy, runbook | Retain managed object or capability `syncthing` as `ops-0067`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0068` | `docs/05.operations/catalog/09-tooling/ops-0068-terraform` | `retain` | `ops-0068` | retain guide, policy, runbook | Retain managed object or capability `terraform` as `ops-0068`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0069` | `docs/05.operations/catalog/09-tooling/ops-0069-terrakube` | `retain` | `ops-0069` | retain guide, policy, runbook | Retain managed object or capability `terrakube` as `ops-0069`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0070` | `docs/05.operations/catalog/10-communication/ops-0070-mail` | `retain` | `ops-0070` | retain guide, policy, runbook | Retain managed object or capability `mail` as `ops-0070`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0071` | `docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard` | `rename` | `ops-0071` | retain guide, policy, runbook | Name the actual managed Homer dashboard rather than the generic dashboard class. |
| `ops-0072` | `docs/05.operations/catalog/11-laboratory/ops-0072-dozzle` | `retain` | `ops-0072` | retain guide, policy, runbook | Retain managed object or capability `dozzle` as `ops-0072`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0073` | `docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook` | `retain` | `ops-0073` | retain guide, policy, runbook | Retain managed object or capability `open-notebook` as `ops-0073`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0074` | `docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening` | `retain` | `ops-0074` | retain guide, policy, runbook | Retain managed object or capability `optimization-hardening` as `ops-0074`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0075` | `docs/05.operations/catalog/11-laboratory/ops-0075-portainer` | `retain` | `ops-0075` | retain guide, policy, runbook | Retain managed object or capability `portainer` as `ops-0075`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0076` | `docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight` | `retain` | `ops-0076` | retain guide, policy, runbook | Retain managed object or capability `redisinsight` as `ops-0076`; its guide, policy, runbook evidence owns an independent operational boundary. |
| `ops-0077` | `docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management` | `rename` | `ops-0077` | retain guide, policy, runbook | Replace vague standardization and redundant domain wording with the IP address management capability. |

## Archive Ledger

```yaml
schema_version: 1
migration_id: mig-0002
baseline_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
subjects:
- legacy_subject_path: docs/05.operations/00-workspace/ops-0001-common-optimizations-template-exceptions
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: f3bac6681c5c13818c7c993c2ca46e5072861fb6
  current_ops_id: ops-0001
  catalog_domain: 00-workspace
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0001-common-optimizations-template-exceptions
  canonical_ops_id: ops-0001
  canonical_slug: common-optimizations-template-exceptions
  final_path: docs/05.operations/catalog/00-workspace/ops-0001-common-optimizations-template-exceptions
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `common-optimizations-template-exceptions` as `ops-0001`; its policy evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/00-workspace/ops-0002-developer-setup
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: aac0f2eea96249766d9eb45f5ebb9f989acd0516
  current_ops_id: ops-0002
  catalog_domain: 00-workspace
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0002-developer-setup
  canonical_ops_id: ops-0002
  canonical_slug: developer-environment
  final_path: docs/05.operations/catalog/00-workspace/ops-0002-developer-environment
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Replace generic setup wording with the developer-environment lifecycle this Guide actually owns.
- legacy_subject_path: docs/05.operations/00-workspace/ops-0003-env-key-comparison
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 5028486ba019d1ff503b38043a5d79302ed902c6
  current_ops_id: ops-0003
  catalog_domain: 00-workspace
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0003-env-key-comparison
  canonical_ops_id: ops-0003
  canonical_slug: env-key-comparison
  final_path: docs/05.operations/catalog/00-workspace/ops-0003-env-key-comparison
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `env-key-comparison` as `ops-0003`; its guide evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/00-workspace/ops-0004-harness-agent-first-engineering
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: a6f76c8850a4b1c2a5e97ead8a8e3f2138cc68b3
  current_ops_id: ops-0004
  catalog_domain: 00-workspace
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering
  canonical_ops_id: ops-0004
  canonical_slug: harness-agent-first-engineering
  final_path: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `harness-agent-first-engineering` as `ops-0004`; its guide, policy evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/00-workspace/ops-0005-harness-agent-first-engineering-validation
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: b4a75a3a5c4b136e3a978c5b438fc163f09c940a
  current_ops_id: ops-0005
  catalog_domain: 00-workspace
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0005-harness-agent-first-engineering-validation
  canonical_ops_id: ops-0004
  canonical_slug: harness-agent-first-engineering
  final_path: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering
  semantic_action: merge
  merge_into: ops-0004
  owner_match: true
  control_boundary_match: true
  trigger_and_recovery_match: true
  independent_evidence_boundary: false
  reason: The validation Runbook governs the same repository harness capability, owner, trigger, verification, and rollback boundary as ops-0004 and has no independent
    cadence or evidence owner.
- legacy_subject_path: docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 99bf57b99d401e9c3a7eaca25e8a8731eaf41073
  current_ops_id: ops-0006
  catalog_domain: 00-workspace
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0006-infra-service-optimization-catalog
  canonical_ops_id: ops-0006
  canonical_slug: infrastructure-optimization-governance
  final_path: docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Name the workspace-wide infrastructure optimization governance boundary and remove the catalog role word.
- legacy_subject_path: docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 87648ebace16b8261559ca7faf55d4e4cb84246b
  current_ops_id: ops-0007
  catalog_domain: 00-workspace
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance
  canonical_ops_id: ops-0007
  canonical_slug: llm-wiki-maintenance
  final_path: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `llm-wiki-maintenance` as `ops-0007`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/00-workspace/ops-0008-new-service-onboarding
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: bf92872d36adff7b071f33a166843c5ab16a34bb
  current_ops_id: ops-0008
  catalog_domain: 00-workspace
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0008-new-service-onboarding
  canonical_ops_id: ops-0008
  canonical_slug: new-service-onboarding
  final_path: docs/05.operations/catalog/00-workspace/ops-0008-new-service-onboarding
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `new-service-onboarding` as `ops-0008`; its guide evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/00-workspace/ops-0009-release-management
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: d8e89d649350bc7981bf6a82e16bbe432cbae47d
  current_ops_id: ops-0009
  catalog_domain: 00-workspace
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0009-release-management
  canonical_ops_id: ops-0009
  canonical_slug: release-management
  final_path: docs/05.operations/catalog/00-workspace/ops-0009-release-management
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `release-management` as `ops-0009`; its runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/00-workspace/ops-0010-sensitive-env-vars-comparison
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 0796c94f7448f0d0430d26c466e176e090fb8933
  current_ops_id: ops-0010
  catalog_domain: 00-workspace
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0010-sensitive-env-vars-comparison
  canonical_ops_id: ops-0010
  canonical_slug: sensitive-env-vars-comparison
  final_path: docs/05.operations/catalog/00-workspace/ops-0010-sensitive-env-vars-comparison
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `sensitive-env-vars-comparison` as `ops-0010`; its guide evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/01-gateway/ops-0011-nginx
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: b192520c725f5e5608f972d9e1ecee7b8480f206
  current_ops_id: ops-0011
  catalog_domain: 01-gateway
  catalog_path: docs/05.operations/catalog/01-gateway/ops-0011-nginx
  canonical_ops_id: ops-0011
  canonical_slug: nginx
  final_path: docs/05.operations/catalog/01-gateway/ops-0011-nginx
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `nginx` as `ops-0011`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/01-gateway/ops-0012-setup
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 3534455e2756f24c396d5d558bc2d0e2460db654
  current_ops_id: ops-0012
  catalog_domain: 01-gateway
  catalog_path: docs/05.operations/catalog/01-gateway/ops-0012-setup
  canonical_ops_id: ops-0012
  canonical_slug: edge-routing-stack
  final_path: docs/05.operations/catalog/01-gateway/ops-0012-edge-routing-stack
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Replace generic setup wording with the Nginx and Traefik edge-routing stack boundary.
- legacy_subject_path: docs/05.operations/01-gateway/ops-0013-traefik
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 93c83aeccb6205e733ce3cc4b6f44ec04eb06a21
  current_ops_id: ops-0013
  catalog_domain: 01-gateway
  catalog_path: docs/05.operations/catalog/01-gateway/ops-0013-traefik
  canonical_ops_id: ops-0013
  canonical_slug: traefik
  final_path: docs/05.operations/catalog/01-gateway/ops-0013-traefik
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `traefik` as `ops-0013`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/02-auth/ops-0014-keycloak
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 0bac23bd3d404fdaadb1df2db03d5f2124cc3f3e
  current_ops_id: ops-0014
  catalog_domain: 02-auth
  catalog_path: docs/05.operations/catalog/02-auth/ops-0014-keycloak
  canonical_ops_id: ops-0014
  canonical_slug: keycloak
  final_path: docs/05.operations/catalog/02-auth/ops-0014-keycloak
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `keycloak` as `ops-0014`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/02-auth/ops-0015-oauth2-proxy
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 7e3da83592924fc440a2a5626d8f7b1e215727f2
  current_ops_id: ops-0015
  catalog_domain: 02-auth
  catalog_path: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy
  canonical_ops_id: ops-0015
  canonical_slug: oauth2-proxy
  final_path: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `oauth2-proxy` as `ops-0015`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/03-security/ops-0016-vault
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 0ca62a70aca9b81877d8e65c6cf6bb199d4ff39c
  current_ops_id: ops-0016
  catalog_domain: 03-security
  catalog_path: docs/05.operations/catalog/03-security/ops-0016-vault
  canonical_ops_id: ops-0016
  canonical_slug: vault
  final_path: docs/05.operations/catalog/03-security/ops-0016-vault
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `vault` as `ops-0016`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/04-data/ops-0017-analytics-influxdb
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 15a5513ff9770e60cd2938ff72bc710d65c296fd
  current_ops_id: ops-0017
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0017-analytics-influxdb
  canonical_ops_id: ops-0017
  canonical_slug: influxdb
  final_path: docs/05.operations/catalog/04-data/ops-0017-influxdb
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `analytics-influxdb` and name the managed `influxdb` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0018-analytics-ksqldb
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 99ae67f29e76a322c23428a185b0618bc5f806ca
  current_ops_id: ops-0018
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0018-analytics-ksqldb
  canonical_ops_id: ops-0018
  canonical_slug: ksqldb
  final_path: docs/05.operations/catalog/04-data/ops-0018-ksqldb
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `analytics-ksqldb` and name the managed `ksqldb` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0019-analytics-opensearch
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: d05448fcd8a3c667b9cfc5be622b0a96c6a95572
  current_ops_id: ops-0019
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0019-analytics-opensearch
  canonical_ops_id: ops-0019
  canonical_slug: opensearch
  final_path: docs/05.operations/catalog/04-data/ops-0019-opensearch
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `analytics-opensearch` and name the managed `opensearch` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0020-analytics-warehouses
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: ae3d0739a86fc392ffe57145a38b1c2f25bc5ab8
  current_ops_id: ops-0020
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0020-analytics-warehouses
  canonical_ops_id: ops-0020
  canonical_slug: starrocks
  final_path: docs/05.operations/catalog/04-data/ops-0020-starrocks
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Replace the analytics category alias with the actual managed StarRocks object.
- legacy_subject_path: docs/05.operations/04-data/ops-0021-backup-backup-policy
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 3c76dc739edb983846172127a3da1465a1557684
  current_ops_id: ops-0021
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0021-backup-backup-policy
  canonical_ops_id: ops-0021
  canonical_slug: backup-and-restore
  final_path: docs/05.operations/catalog/04-data/ops-0021-backup-and-restore
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the repeated backup token and policy role word; name the backup-and-restore control boundary.
- legacy_subject_path: docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: d17705dcf8788529e5a94df6e471ecd028b0c474
  current_ops_id: ops-0022
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0022-cache-and-kv-valkey-cluster
  canonical_ops_id: ops-0022
  canonical_slug: valkey-cluster
  final_path: docs/05.operations/catalog/04-data/ops-0022-valkey-cluster
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `cache-and-kv-valkey-cluster` and name the managed `valkey-cluster` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0023-lake-and-object-minio
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 16ba4b4a750d8569233ff9872b30a69ce9c91240
  current_ops_id: ops-0023
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0023-lake-and-object-minio
  canonical_ops_id: ops-0023
  canonical_slug: minio
  final_path: docs/05.operations/catalog/04-data/ops-0023-minio
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `lake-and-object-minio` and name the managed `minio` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 572c2a7bce3b6b4bfafcc0ca46f860c064b0c2e5
  current_ops_id: ops-0024
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0024-lake-and-object-seaweedfs
  canonical_ops_id: ops-0024
  canonical_slug: seaweedfs
  final_path: docs/05.operations/catalog/04-data/ops-0024-seaweedfs
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `lake-and-object-seaweedfs` and name the managed `seaweedfs` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0025-nosql-cassandra
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: cdf61966b92f5342cb5f8d033b8181cdd9189251
  current_ops_id: ops-0025
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0025-nosql-cassandra
  canonical_ops_id: ops-0025
  canonical_slug: cassandra
  final_path: docs/05.operations/catalog/04-data/ops-0025-cassandra
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `nosql-cassandra` and name the managed `cassandra` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0026-nosql-couchdb
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 407124d285a4dd01ca083194245a996f0fbd63a2
  current_ops_id: ops-0026
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0026-nosql-couchdb
  canonical_ops_id: ops-0026
  canonical_slug: couchdb
  final_path: docs/05.operations/catalog/04-data/ops-0026-couchdb
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `nosql-couchdb` and name the managed `couchdb` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0027-nosql-mongodb
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: bb04e8c88d2a22f48c94ab01c52c7a8b561953b8
  current_ops_id: ops-0027
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0027-nosql-mongodb
  canonical_ops_id: ops-0027
  canonical_slug: mongodb
  final_path: docs/05.operations/catalog/04-data/ops-0027-mongodb
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `nosql-mongodb` and name the managed `mongodb` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0028-operational-mng-db
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: fb12f6989fafb6719226082c1478e2d37fb0a1d1
  current_ops_id: ops-0028
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0028-operational-mng-db
  canonical_ops_id: ops-0028
  canonical_slug: management-database
  final_path: docs/05.operations/catalog/04-data/ops-0028-management-database
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `operational-mng-db` and name the managed `management-database` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0029-operational-supabase
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: bd742e6eaa48f221f85c26c661abb2350d185609
  current_ops_id: ops-0029
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0029-operational-supabase
  canonical_ops_id: ops-0029
  canonical_slug: supabase
  final_path: docs/05.operations/catalog/04-data/ops-0029-supabase
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `operational-supabase` and name the managed `supabase` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0030-optimization-optimization-hardening
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: c195d1d4c64be3cc275e78c9a657a09a20cecd55
  current_ops_id: ops-0030
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0030-optimization-optimization-hardening
  canonical_ops_id: ops-0030
  canonical_slug: optimization-hardening
  final_path: docs/05.operations/catalog/04-data/ops-0030-optimization-hardening
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the repeated optimization token while retaining the data-domain hardening capability.
- legacy_subject_path: docs/05.operations/04-data/ops-0031-relational-postgresql-cluster
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 3d7cbd2dfff0b16e135042e364145c1c734bb194
  current_ops_id: ops-0031
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0031-relational-postgresql-cluster
  canonical_ops_id: ops-0031
  canonical_slug: postgresql-cluster
  final_path: docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `relational-postgresql-cluster` and name the managed `postgresql-cluster` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0032-relational-postgresql-logical-upgrade-restore-rehearsal
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 8bc004b32fbb7ad451114ab59879529ddd89a738
  current_ops_id: ops-0032
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0032-relational-postgresql-logical-upgrade-restore-rehearsal
  canonical_ops_id: ops-0032
  canonical_slug: postgresql-logical-upgrade-restore-rehearsal
  final_path: docs/05.operations/catalog/04-data/ops-0032-postgresql-logical-upgrade-restore-rehearsal
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the relational taxonomy prefix while retaining the independent PostgreSQL upgrade rehearsal.
- legacy_subject_path: docs/05.operations/04-data/ops-0033-specialized-neo4j
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 5b78f1f2316200fa383d46c21e84e5847d3c36db
  current_ops_id: ops-0033
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0033-specialized-neo4j
  canonical_ops_id: ops-0033
  canonical_slug: neo4j
  final_path: docs/05.operations/catalog/04-data/ops-0033-neo4j
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `specialized-neo4j` and name the managed `neo4j` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0034-specialized-qdrant
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 16f9b4aaf22ece4312e8401ecc54151c931126d0
  current_ops_id: ops-0034
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0034-specialized-qdrant
  canonical_ops_id: ops-0034
  canonical_slug: qdrant
  final_path: docs/05.operations/catalog/04-data/ops-0034-qdrant
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the domain/category taxonomy prefix from `specialized-qdrant` and name the managed `qdrant` object directly.
- legacy_subject_path: docs/05.operations/04-data/ops-0035-storage-storage-exhaustion
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 5ad9f3eefecdec95c7c1cfc7a1addfef015b8e9d
  current_ops_id: ops-0035
  catalog_domain: 04-data
  catalog_path: docs/05.operations/catalog/04-data/ops-0035-storage-storage-exhaustion
  canonical_ops_id: ops-0035
  canonical_slug: storage-exhaustion
  final_path: docs/05.operations/catalog/04-data/ops-0035-storage-exhaustion
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the repeated storage token while retaining the independent exhaustion recovery trigger.
- legacy_subject_path: docs/05.operations/05-messaging/ops-0036-kafka
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 7975f25d6cc185fa56674f2f69f6440742904698
  current_ops_id: ops-0036
  catalog_domain: 05-messaging
  catalog_path: docs/05.operations/catalog/05-messaging/ops-0036-kafka
  canonical_ops_id: ops-0036
  canonical_slug: kafka
  final_path: docs/05.operations/catalog/05-messaging/ops-0036-kafka
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `kafka` as `ops-0036`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/05-messaging/ops-0037-optimization-hardening
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: bbd3e8ebf632f899538becf2d4c28c5210c12e7d
  current_ops_id: ops-0037
  catalog_domain: 05-messaging
  catalog_path: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening
  canonical_ops_id: ops-0037
  canonical_slug: optimization-hardening
  final_path: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `optimization-hardening` as `ops-0037`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/05-messaging/ops-0038-rabbitmq
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 50137e193f24467f0f427ab5d470ff541b8d8fb2
  current_ops_id: ops-0038
  catalog_domain: 05-messaging
  catalog_path: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq
  canonical_ops_id: ops-0038
  canonical_slug: rabbitmq
  final_path: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `rabbitmq` as `ops-0038`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/06-observability/ops-0039-alertmanager
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 158aa7b620e9331b3d8e1eb0e51d0b7cf03490df
  current_ops_id: ops-0039
  catalog_domain: 06-observability
  catalog_path: docs/05.operations/catalog/06-observability/ops-0039-alertmanager
  canonical_ops_id: ops-0039
  canonical_slug: alertmanager
  final_path: docs/05.operations/catalog/06-observability/ops-0039-alertmanager
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `alertmanager` as `ops-0039`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/06-observability/ops-0040-alloy
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: d6b4bf249708276c8e77c300d2cc40ea3e0f8c20
  current_ops_id: ops-0040
  catalog_domain: 06-observability
  catalog_path: docs/05.operations/catalog/06-observability/ops-0040-alloy
  canonical_ops_id: ops-0040
  canonical_slug: alloy
  final_path: docs/05.operations/catalog/06-observability/ops-0040-alloy
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `alloy` as `ops-0040`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/06-observability/ops-0041-grafana
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 17ee44c27101f6f438c6357d83e47564a900222b
  current_ops_id: ops-0041
  catalog_domain: 06-observability
  catalog_path: docs/05.operations/catalog/06-observability/ops-0041-grafana
  canonical_ops_id: ops-0041
  canonical_slug: grafana
  final_path: docs/05.operations/catalog/06-observability/ops-0041-grafana
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `grafana` as `ops-0041`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/06-observability/ops-0042-lgtm-stack
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 3534aac953b0f17210e77d5959704e9786ab0ad0
  current_ops_id: ops-0042
  catalog_domain: 06-observability
  catalog_path: docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack
  canonical_ops_id: ops-0042
  canonical_slug: lgtm-stack
  final_path: docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `lgtm-stack` as `ops-0042`; its guide evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/06-observability/ops-0043-loki
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: d933588975822498561a8e978bed574a4b3f0c5a
  current_ops_id: ops-0043
  catalog_domain: 06-observability
  catalog_path: docs/05.operations/catalog/06-observability/ops-0043-loki
  canonical_ops_id: ops-0043
  canonical_slug: loki
  final_path: docs/05.operations/catalog/06-observability/ops-0043-loki
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `loki` as `ops-0043`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/06-observability/ops-0044-optimization-hardening
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 3c758695c718049c60e94dfdeeff9ab34b68388e
  current_ops_id: ops-0044
  catalog_domain: 06-observability
  catalog_path: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening
  canonical_ops_id: ops-0044
  canonical_slug: optimization-hardening
  final_path: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `optimization-hardening` as `ops-0044`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/06-observability/ops-0045-prometheus
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 6ace48cb8f0d47b589b098f99ca00eeae2f801e3
  current_ops_id: ops-0045
  catalog_domain: 06-observability
  catalog_path: docs/05.operations/catalog/06-observability/ops-0045-prometheus
  canonical_ops_id: ops-0045
  canonical_slug: prometheus
  final_path: docs/05.operations/catalog/06-observability/ops-0045-prometheus
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `prometheus` as `ops-0045`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/06-observability/ops-0046-pushgateway
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 4bfc4740d2911299f2b4a0dd25ec84685db1caad
  current_ops_id: ops-0046
  catalog_domain: 06-observability
  catalog_path: docs/05.operations/catalog/06-observability/ops-0046-pushgateway
  canonical_ops_id: ops-0046
  canonical_slug: pushgateway
  final_path: docs/05.operations/catalog/06-observability/ops-0046-pushgateway
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `pushgateway` as `ops-0046`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/06-observability/ops-0047-pyroscope
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: bd01290e9929cbfa2ac1597b34567d7717201486
  current_ops_id: ops-0047
  catalog_domain: 06-observability
  catalog_path: docs/05.operations/catalog/06-observability/ops-0047-pyroscope
  canonical_ops_id: ops-0047
  canonical_slug: pyroscope
  final_path: docs/05.operations/catalog/06-observability/ops-0047-pyroscope
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `pyroscope` as `ops-0047`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/06-observability/ops-0048-retention
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 3282e5772d68ab964202f9eaf68a12526be27f34
  current_ops_id: ops-0048
  catalog_domain: 06-observability
  catalog_path: docs/05.operations/catalog/06-observability/ops-0048-retention
  canonical_ops_id: ops-0048
  canonical_slug: telemetry-retention
  final_path: docs/05.operations/catalog/06-observability/ops-0048-telemetry-retention
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Replace generic retention wording with the cross-backend telemetry retention control boundary.
- legacy_subject_path: docs/05.operations/06-observability/ops-0049-tempo
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 8fdb73d56929f801899a85fb6fdc965e7c387301
  current_ops_id: ops-0049
  catalog_domain: 06-observability
  catalog_path: docs/05.operations/catalog/06-observability/ops-0049-tempo
  canonical_ops_id: ops-0049
  canonical_slug: tempo
  final_path: docs/05.operations/catalog/06-observability/ops-0049-tempo
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `tempo` as `ops-0049`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/07-workflow/ops-0050-airflow
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 63f04dd5bad73844163fc5706068adfc8d6f2bbe
  current_ops_id: ops-0050
  catalog_domain: 07-workflow
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0050-airflow
  canonical_ops_id: ops-0050
  canonical_slug: airflow
  final_path: docs/05.operations/catalog/07-workflow/ops-0050-airflow
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `airflow` as `ops-0050`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/07-workflow/ops-0051-airflow-dag-basics
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 6d9c540da0d4437b0d8001d0c4a020d7605f0948
  current_ops_id: ops-0051
  catalog_domain: 07-workflow
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-basics
  canonical_ops_id: ops-0051
  canonical_slug: airflow-dag-lifecycle
  final_path: docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Replace unsupported basics wording with the independent Airflow DAG authoring and deployment lifecycle.
- legacy_subject_path: docs/05.operations/07-workflow/ops-0052-dag-deployment
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 859e0c2a44210873cfbad77c242fdfd8599e114c
  current_ops_id: ops-0052
  catalog_domain: 07-workflow
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0052-dag-deployment
  canonical_ops_id: ops-0051
  canonical_slug: airflow-dag-lifecycle
  final_path: docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle
  semantic_action: merge
  merge_into: ops-0051
  owner_match: true
  control_boundary_match: true
  trigger_and_recovery_match: true
  independent_evidence_boundary: false
  reason: The DAG deployment Policy governs the same Airflow DAG lifecycle, owner, lint and secret controls, dags-list verification, and ops-0050 recovery handoff
    as ops-0051 and has no independent evidence boundary.
- legacy_subject_path: docs/05.operations/07-workflow/ops-0053-n8n
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 73cb74c4f661111b54d17318c1d286177ede2473
  current_ops_id: ops-0053
  catalog_domain: 07-workflow
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0053-n8n
  canonical_ops_id: ops-0053
  canonical_slug: n8n
  final_path: docs/05.operations/catalog/07-workflow/ops-0053-n8n
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `n8n` as `ops-0053`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/07-workflow/ops-0054-optimization-hardening
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 390d732c2fbe77adb88f34053bb58c535f23e068
  current_ops_id: ops-0054
  catalog_domain: 07-workflow
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening
  canonical_ops_id: ops-0054
  canonical_slug: optimization-hardening
  final_path: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `optimization-hardening` as `ops-0054`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/08-ai/ops-0055-gpu-recovery
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 83cc368f853d4353c0d59b9fb414a3ec15173bbb
  current_ops_id: ops-0055
  catalog_domain: 08-ai
  catalog_path: docs/05.operations/catalog/08-ai/ops-0055-gpu-recovery
  canonical_ops_id: ops-0055
  canonical_slug: gpu-recovery
  final_path: docs/05.operations/catalog/08-ai/ops-0055-gpu-recovery
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `gpu-recovery` as `ops-0055`; its runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/08-ai/ops-0056-ollama
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 6f889fefef78d2000080ed99886b53ef40eda5bf
  current_ops_id: ops-0056
  catalog_domain: 08-ai
  catalog_path: docs/05.operations/catalog/08-ai/ops-0056-ollama
  canonical_ops_id: ops-0056
  canonical_slug: ollama
  final_path: docs/05.operations/catalog/08-ai/ops-0056-ollama
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `ollama` as `ops-0056`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/08-ai/ops-0057-open-webui
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 2cdeaa9bcd238a9ddab662457807de540d7a17b2
  current_ops_id: ops-0057
  catalog_domain: 08-ai
  catalog_path: docs/05.operations/catalog/08-ai/ops-0057-open-webui
  canonical_ops_id: ops-0057
  canonical_slug: open-webui
  final_path: docs/05.operations/catalog/08-ai/ops-0057-open-webui
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `open-webui` as `ops-0057`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/08-ai/ops-0058-optimization-hardening
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: ed3eb86a028b5fa1ae50f7f3a0a8a284754727a5
  current_ops_id: ops-0058
  catalog_domain: 08-ai
  catalog_path: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening
  canonical_ops_id: ops-0058
  canonical_slug: optimization-hardening
  final_path: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `optimization-hardening` as `ops-0058`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/08-ai/ops-0059-rag-workflow
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 771ac95066af19770f3defd849bfc12eee7760e6
  current_ops_id: ops-0059
  catalog_domain: 08-ai
  catalog_path: docs/05.operations/catalog/08-ai/ops-0059-rag-workflow
  canonical_ops_id: ops-0059
  canonical_slug: rag-workflow
  final_path: docs/05.operations/catalog/08-ai/ops-0059-rag-workflow
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `rag-workflow` as `ops-0059`; its guide evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/09-tooling/ops-0060-iac-deployment-policy
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 401eb15223232bfad2768cd7f51998f759edb8e8
  current_ops_id: ops-0060
  catalog_domain: 09-tooling
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0060-iac-deployment-policy
  canonical_ops_id: ops-0060
  canonical_slug: iac-deployment
  final_path: docs/05.operations/catalog/09-tooling/ops-0060-iac-deployment
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Remove the policy role word while retaining the cross-tool IaC deployment control boundary.
- legacy_subject_path: docs/05.operations/09-tooling/ops-0061-k6
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: ee6b588bdb321d5f18a10ddd083c8b88a9258383
  current_ops_id: ops-0061
  catalog_domain: 09-tooling
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0061-k6
  canonical_ops_id: ops-0061
  canonical_slug: k6
  final_path: docs/05.operations/catalog/09-tooling/ops-0061-k6
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `k6` as `ops-0061`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/09-tooling/ops-0062-locust
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 388fb0ad848a7eb1aed313cc7f122b58cf5a51f7
  current_ops_id: ops-0062
  catalog_domain: 09-tooling
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0062-locust
  canonical_ops_id: ops-0062
  canonical_slug: locust
  final_path: docs/05.operations/catalog/09-tooling/ops-0062-locust
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `locust` as `ops-0062`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/09-tooling/ops-0063-optimization-hardening
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 9bb2fcbe6a37f7660ac4c5b6386da8d33d8e9c18
  current_ops_id: ops-0063
  catalog_domain: 09-tooling
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening
  canonical_ops_id: ops-0063
  canonical_slug: optimization-hardening
  final_path: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `optimization-hardening` as `ops-0063`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/09-tooling/ops-0064-performance-testing
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: f2a89ff06d069649bd3a8843ebd8460431046a65
  current_ops_id: ops-0064
  catalog_domain: 09-tooling
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing
  canonical_ops_id: ops-0064
  canonical_slug: performance-testing
  final_path: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `performance-testing` as `ops-0064`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/09-tooling/ops-0065-registry
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 1abed58aaee14315d7a12bbc15096352f08934a1
  current_ops_id: ops-0065
  catalog_domain: 09-tooling
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0065-registry
  canonical_ops_id: ops-0065
  canonical_slug: registry
  final_path: docs/05.operations/catalog/09-tooling/ops-0065-registry
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `registry` as `ops-0065`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/09-tooling/ops-0066-sonarqube
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 87bd5bbe45ebaba9a3eab9c30fa3587d79c9e3b6
  current_ops_id: ops-0066
  catalog_domain: 09-tooling
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube
  canonical_ops_id: ops-0066
  canonical_slug: sonarqube
  final_path: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `sonarqube` as `ops-0066`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/09-tooling/ops-0067-syncthing
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: a6f11cf3215aec9c927e74b03d0ed7645e2a15b7
  current_ops_id: ops-0067
  catalog_domain: 09-tooling
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0067-syncthing
  canonical_ops_id: ops-0067
  canonical_slug: syncthing
  final_path: docs/05.operations/catalog/09-tooling/ops-0067-syncthing
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `syncthing` as `ops-0067`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/09-tooling/ops-0068-terraform
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 366ac9c6f90b3a2b673bc2e40e39edb503ce52c8
  current_ops_id: ops-0068
  catalog_domain: 09-tooling
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0068-terraform
  canonical_ops_id: ops-0068
  canonical_slug: terraform
  final_path: docs/05.operations/catalog/09-tooling/ops-0068-terraform
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `terraform` as `ops-0068`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/09-tooling/ops-0069-terrakube
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 175d7c6e23d7cd7b162cc643f5819270260651ba
  current_ops_id: ops-0069
  catalog_domain: 09-tooling
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0069-terrakube
  canonical_ops_id: ops-0069
  canonical_slug: terrakube
  final_path: docs/05.operations/catalog/09-tooling/ops-0069-terrakube
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `terrakube` as `ops-0069`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/10-communication/ops-0070-mail
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: db6c875fac32542b52df4155861ff99baad5d9a7
  current_ops_id: ops-0070
  catalog_domain: 10-communication
  catalog_path: docs/05.operations/catalog/10-communication/ops-0070-mail
  canonical_ops_id: ops-0070
  canonical_slug: mail
  final_path: docs/05.operations/catalog/10-communication/ops-0070-mail
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `mail` as `ops-0070`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/11-laboratory/ops-0071-dashboard
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 008c6a11bdae8889dae1fb840d2da800add659ad
  current_ops_id: ops-0071
  catalog_domain: 11-laboratory
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0071-dashboard
  canonical_ops_id: ops-0071
  canonical_slug: homer-dashboard
  final_path: docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Name the actual managed Homer dashboard rather than the generic dashboard class.
- legacy_subject_path: docs/05.operations/11-laboratory/ops-0072-dozzle
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: a4a25cb196be6060f9df28e7c62f18fed7e8dfca
  current_ops_id: ops-0072
  catalog_domain: 11-laboratory
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle
  canonical_ops_id: ops-0072
  canonical_slug: dozzle
  final_path: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `dozzle` as `ops-0072`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/11-laboratory/ops-0073-open-notebook
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 29792454851f1e24b31451644272376f3ba26e4e
  current_ops_id: ops-0073
  catalog_domain: 11-laboratory
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook
  canonical_ops_id: ops-0073
  canonical_slug: open-notebook
  final_path: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `open-notebook` as `ops-0073`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/11-laboratory/ops-0074-optimization-hardening
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 107bd7ef0672de42550b1275bb8372af38c4fa9a
  current_ops_id: ops-0074
  catalog_domain: 11-laboratory
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening
  canonical_ops_id: ops-0074
  canonical_slug: optimization-hardening
  final_path: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `optimization-hardening` as `ops-0074`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/11-laboratory/ops-0075-portainer
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: d2afc00b648cd64716571aa928bb6ceba6ccc9ad
  current_ops_id: ops-0075
  catalog_domain: 11-laboratory
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0075-portainer
  canonical_ops_id: ops-0075
  canonical_slug: portainer
  final_path: docs/05.operations/catalog/11-laboratory/ops-0075-portainer
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `portainer` as `ops-0075`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/11-laboratory/ops-0076-redisinsight
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: ab07b7373e95d244a1e00afcffef4554b9539eeb
  current_ops_id: ops-0076
  catalog_domain: 11-laboratory
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight
  canonical_ops_id: ops-0076
  canonical_slug: redisinsight
  final_path: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight
  semantic_action: retain
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Retain managed object or capability `redisinsight` as `ops-0076`; its guide, policy, runbook evidence owns an independent operational boundary.
- legacy_subject_path: docs/05.operations/12-infra-net/ops-0077-standardize-infra-net
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_tree: 39f32636d7c3e3ada8844b1903f2b502b58ca468
  current_ops_id: ops-0077
  catalog_domain: 12-infra-net
  catalog_path: docs/05.operations/catalog/12-infra-net/ops-0077-standardize-infra-net
  canonical_ops_id: ops-0077
  canonical_slug: ip-address-management
  final_path: docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management
  semantic_action: rename
  merge_into: null
  owner_match: false
  control_boundary_match: false
  trigger_and_recovery_match: false
  independent_evidence_boundary: true
  reason: Replace vague standardization and redundant domain wording with the IP address management capability.
files:
- legacy_path: docs/05.operations/00-workspace/README.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d0c376e84ec0dcc1604be9773bf19024c3929f2f
  role: domain-readme
  catalog_path: docs/05.operations/catalog/00-workspace/README.md
  final_path: docs/05.operations/catalog/00-workspace/README.md
  semantic_action: retain
  canonical_role_owner: null
  preserved_semantics:
  - section:audience:b643009c3d36
  - section:how-to-work-in-this-area:384f700b86fa
  - section:operations-00-workspace:1b43eaa06b92
  - section:overview:497f87daf4df
  - section:related-documents:82f5d5269530
  - section:scope:aa946ea5f051
  - section:structure:9f0262b84e45
  removed_semantics: []
  active_consumers:
  - docs/05.operations/README.md
  - docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  final_consumers:
  - docs/05.operations/README.md
  - docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
- legacy_path: docs/05.operations/00-workspace/ops-0001-common-optimizations-template-exceptions/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 9ef8acdbb3ab5ab8fad8c9025f8b04c8416a84b9
  role: policy
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0001-common-optimizations-template-exceptions/policy.md
  final_path: docs/05.operations/catalog/00-workspace/ops-0001-common-optimizations-template-exceptions/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/00-workspace/ops-0001-common-optimizations-template-exceptions/policy.md
  preserved_semantics:
  - section:ai-agent-policy-section-if-applicable:32e7cda86953
  - section:common-optimizations-template-exceptions-policy:fc92a4e9f17f
  - section:controls:be0e52ec86d9
  - section:exceptions:5e477fc07945
  - section:overview:3e687e913d2c
  - section:policy-scope:11b9152c5f7c
  - section:related-documents:0782f6735ddf
  - section:review-cadence:7866ea0133f9
  - section:verification:c1f21ad4808c
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md
  - docs/05.operations/00-workspace/README.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
  - tests/validation/test_document_metadata.py
  final_consumers:
  - docs/03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md
  - docs/05.operations/catalog/00-workspace/README.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
  - tests/validation/test_document_metadata.py
- legacy_path: docs/05.operations/00-workspace/ops-0002-developer-setup/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d855614727f0b6b6a39ce3d0e3fdaa3d87ae797c
  role: guide
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0002-developer-setup/guide.md
  final_path: docs/05.operations/catalog/00-workspace/ops-0002-developer-environment/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/00-workspace/ops-0002-developer-environment/guide.md
  preserved_semantics:
  - section:1-context-objective:2d5450a189c4
  - section:2-recommended-permissions-claude-code:833ba3bafe01
  - section:3-tool-configuration:315b37707a84
  - section:4-operational-procedures:385169630a06
  - section:5-maintenance-safety:c0f4e4077c32
  - section:common-checks:1e2eeeea0f4d
  - section:common-pitfalls:6b9c048b7fb9
  - section:developer-environment-setup-usage:1fdedccc733f
  - section:developer-setup-operations:46830256abf5
  - section:development-tools:9956b2b1421b
  - section:file-system-access:a5a9a40928df
  - section:infrastructure-validation:deb8ce9961a2
  - section:initial-setup:7163d335d37d
  - section:local-settings-pruning:d6a28327d929
  - section:overview:f765f1129f28
  - section:prerequisites:4b12c47a8708
  - section:purpose:b80f9001cc4a
  - section:related-documents:0782f6735ddf
  - section:runbook-handoff:364a2499eda1
  - section:shell-environment:b32bae7cc041
  - section:step-by-step-instructions:bd16deab7ff6
  - section:target-audience:d44908ce17ef
  - section:usage-type:e426b518bdf2
  - section:usage:63bfd61a0561
  - text:baseline-body:관련 인프라 서비스나 문서 영역을 이해하고 안전하게 변경 또는 운영할 수 있도록 돕는다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0002-developer-setup
  active_consumers:
  - docs/05.operations/00-workspace/README.md
  - docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - secrets/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/README.md
  - docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - secrets/README.md
- legacy_path: docs/05.operations/00-workspace/ops-0003-env-key-comparison/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 77d07adf4f0c2e1c3999c269c8bdc12c14c53340
  role: guide
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0003-env-key-comparison/guide.md
  final_path: docs/05.operations/catalog/00-workspace/ops-0003-env-key-comparison/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/00-workspace/ops-0003-env-key-comparison/guide.md
  preserved_semantics:
  - section::0bef3edba74c
  - section::5455b1a87854
  - section::5476d3c6891f
  - section::59c3ede92b07
  - section::84974cf41b76
  - section::98d526bcf772
  - section::c074652f77cc
  - section::c96abf3c8d0d
  - section:common-checks:7afed2b3c26a
  - section:common-pitfalls:d44786157825
  - section:env-example-vs-env-key-comparison:b8f7d55a7377
  - section:env:8944d934dd13
  - section:overview:3e5671ae6336
  - section:prerequisites:8e6eddc948d2
  - section:purpose:92bc2f4430e2
  - section:related-documents:95f1fc8506da
  - section:runbook-handoff:364a2499eda1
  - section:step-by-step-instructions:33aaaee7e276
  - section:target-audience:90accb0a25c5
  - section:usage-type:d59449ab6f5b
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 `.env.example`과 `.env`의 환경변수 키 일관성을 확인하는 운영 참조 문서다. 키셋 동기화 여부, 순서 차이, 누락·추가·deprecated 키를 기록한다.
  removed_semantics:
  - contradiction:env-key-diff-count
  active_consumers:
  - docs/03.specs/spec-0090-workspace-audit-2026-05/spec.md
  - docs/05.operations/00-workspace/README.md
  - docs/05.operations/00-workspace/ops-0010-sensitive-env-vars-comparison/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/03.specs/spec-0090-workspace-audit-2026-05/spec.md
  - docs/05.operations/catalog/00-workspace/README.md
  - docs/05.operations/catalog/00-workspace/ops-0010-sensitive-env-vars-comparison/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/00-workspace/ops-0004-harness-agent-first-engineering/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 37831f733648aa5a38e0b9da1945878838d00b95
  role: guide
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/guide.md
  final_path: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/guide.md
  preserved_semantics:
  - section:audience-and-prerequisites:568bc40a6d4e
  - section:common-checks:47aab11faa68
  - section:harness-agent-first-engineering-usage-guide:f52c0a8336c8
  - section:overview:da6faf3d1b92
  - section:prerequisites:2a629a6b8aea
  - section:purpose:600c1f431056
  - section:related-documents:7e79195e9bbe
  - section:runbook-handoff:364a2499eda1
  - section:target-audience:4d7f295336e9
  - section:troubleshooting:bfe5e4f95750
  - section:usage-type:9150504bfdd7
  - section:usage:83e43c585d19
  - text:baseline-body:이 가이드는 `hy-home.docker`에서 하네스 엔지니어링과 Agent-first Engineering 상태를 다시 조사하거나 보완할 때 따라야 할 절차를 설명한다.
  removed_semantics:
  - stale:no-runbook-handoff
  active_consumers:
  - docs/03.specs/spec-0094-harness-agent-first-engineering/spec.md
  - docs/05.operations/00-workspace/README.md
  - docs/05.operations/00-workspace/ops-0004-harness-agent-first-engineering/policy.md
  - docs/05.operations/00-workspace/ops-0005-harness-agent-first-engineering-validation/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
  final_consumers:
  - docs/03.specs/spec-0094-harness-agent-first-engineering/spec.md
  - docs/05.operations/catalog/00-workspace/README.md
  - docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/policy.md
  - docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
- legacy_path: docs/05.operations/00-workspace/ops-0004-harness-agent-first-engineering/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d9733c220219efe23881f81fa3c785582fd33448
  role: policy
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/policy.md
  final_path: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/policy.md
  preserved_semantics:
  - section:controls:f378701b33cc
  - section:exceptions:e2ddad2f1c46
  - section:harness-agent-first-engineering-operations-policy:4de233e64854
  - section:overview:42a27204059b
  - section:policy-scope:78a8b09e20ee
  - section:related-documents:f25a88a3e12b
  - section:review-cadence:83e28c2b6882
  - section:verification:acea358dd49d
  - text:baseline-body:Governance rules and scopes.
  removed_semantics:
  - stale:stage-04-execution-routes
  active_consumers:
  - docs/03.specs/spec-0093-docs-taxonomy-agent-first-migration/spec.md
  - docs/03.specs/spec-0094-harness-agent-first-engineering/spec.md
  - docs/05.operations/00-workspace/README.md
  - docs/05.operations/00-workspace/ops-0004-harness-agent-first-engineering/guide.md
  - docs/05.operations/00-workspace/ops-0005-harness-agent-first-engineering-validation/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
  final_consumers:
  - docs/03.specs/spec-0093-docs-taxonomy-agent-first-migration/spec.md
  - docs/03.specs/spec-0094-harness-agent-first-engineering/spec.md
  - docs/05.operations/catalog/00-workspace/README.md
  - docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/guide.md
  - docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
- legacy_path: docs/05.operations/00-workspace/ops-0005-harness-agent-first-engineering-validation/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d3da293e44cfc19e47af7169bdd146ae381202a8
  role: runbook
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0005-harness-agent-first-engineering-validation/runbook.md
  final_path: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/runbook.md
  semantic_action: merge
  canonical_role_owner: docs/05.operations/catalog/00-workspace/ops-0004-harness-agent-first-engineering/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:agent-operations-if-applicable:48c1585987ef
  - section:canonical-references:a5849018c762
  - section:checklist:49d108719342
  - section:checklist:8718b2d8ac11
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:harness-agent-first-engineering-validation-operations:87146f0ba1cf
  - section:harness-agent-first-engineering-validation-procedure:41805de4e77d
  - section:observability-and-evidence-sources:14a6d7a51dc2
  - section:observability-and-evidence-sources:3c533d420833
  - section:overview:f265bb534370
  - section:procedure-or-checklist:b8a664d6bfa3
  - section:procedure:5da93bd3e257
  - section:procedure:bea1753b676d
  - section:purpose:6ca6271767ae
  - section:related-documents:0782f6735ddf
  - section:related-operational-documents:f7187beb5565
  - section:rollback-or-recovery:5ac18bc4e65f
  - section:safe-rollback-or-recovery-procedure:808566b787da
  - section:safe-rollback-or-recovery-procedure:97b21e8c1a6c
  - section:steps:9967c3592c53
  - section:verification-steps:0d62e67a380a
  - section:verification-steps:70472f7e622f
  - section:when-to-use:52d50801f899
  - text:graphify-advisory-corroboration:bash scripts/knowledge/report-graphify-health.sh
  - text:hafe-validation-trigger:New stage docs are added.
  - text:provider-hook-payload-simulation:Run hook payload simulations.
  removed_semantics:
  - duplicate:hafe-overview-and-validator-list
  active_consumers:
  - docs/03.specs/spec-0094-harness-agent-first-engineering/spec.md
  - docs/05.operations/00-workspace/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
  final_consumers:
  - docs/03.specs/spec-0094-harness-agent-first-engineering/spec.md
  - docs/05.operations/catalog/00-workspace/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
- legacy_path: docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: a8c80a8b101aa917d34cf856cf317daa34f1d8a5
  role: policy
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  final_path: docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  preserved_semantics:
  - section:01-gateway:ef43e46bf8b1
  - section:02-auth:3289173c47f6
  - section:03-security:36c7c308b15d
  - section:04-data:328964334772
  - section:05-messaging:4a19920d3993
  - section:06-observability:5dcbc3fc6524
  - section:07-workflow:a2c3ea23475f
  - section:08-ai:edc6edcbf623
  - section:09-tooling:c5608d3e9bf4
  - section:10-communication:926de372132a
  - section:11-laboratory:50fe2b63a8a8
  - section:ai-agent-policy-section-if-applicable:79dd88693ce0
  - section:baseline-audit-snapshot-2026-03-27:d51e6049af0b
  - section:common-template-coverage-snapshot-2026-03-28:8f086c357dca
  - section:controls:b7046292faf7
  - section:exceptions:7d58997bb3ca
  - section:infra-service-optimization-expansion-policy:9233b586fc50
  - section:overview:e9005e38119a
  - section:policy-scope:a9a498c93698
  - section:priority-model:7d1221bac0bd
  - section:quick-win-enforcement-snapshot-2026-03-28:3d7f3467b1e5
  - section:related-documents:0782f6735ddf
  - section:review-cadence:dfe3db40e261
  - section:roadmap-disposition:9c90c302f1e7
  - section:roadmap-status-and-priority-boundary:32546c3ef564
  - section:tier-by-tier-optimization-expansion-catalog:cc4d817e02bf
  - section:verification:ed3cf0b2c45d
  - text:baseline-body:모든 장기 실행 서비스에 `healthcheck`, `restart`, `no-new-privileges`, 자원 제한(`cpus`/`memory`)을 기본 적용
  removed_semantics:
  - stale:legacy-subject-path:ops-0006-infra-service-optimization-catalog
  active_consumers:
  - docs/03.specs/spec-0006-messaging/spec.md
  - docs/03.specs/spec-0007-observability/spec.md
  - docs/03.specs/spec-0008-workflow/spec.md
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/03.specs/spec-0010-tooling/spec.md
  - docs/03.specs/spec-0012-laboratory/spec.md
  - docs/05.operations/00-workspace/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/lib/document_governance/links.py
  - tests/validation/test_document_corpus_lifecycle.py
  - tests/validation/test_document_links.py
  final_consumers:
  - docs/03.specs/spec-0006-messaging/spec.md
  - docs/03.specs/spec-0007-observability/spec.md
  - docs/03.specs/spec-0008-workflow/spec.md
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/03.specs/spec-0010-tooling/spec.md
  - docs/03.specs/spec-0012-laboratory/spec.md
  - docs/05.operations/catalog/00-workspace/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/lib/document_governance/links.py
  - tests/validation/test_document_corpus_lifecycle.py
  - tests/validation/test_document_links.py
- legacy_path: docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 8a49e9192957fc6e18ff10c0bdf81144450f8505
  role: guide
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/guide.md
  final_path: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/guide.md
  preserved_semantics:
  - section:common-checks:8b4cfcb5af6d
  - section:common-pitfalls:d44786157825
  - section:llm-wiki-maintenance-usage-guide:0418fd4a815a
  - section:overview:c056d9be92d4
  - section:prerequisites:8e6eddc948d2
  - section:purpose:2750e599b4c0
  - section:related-documents:388b526e351d
  - section:runbook-handoff:47c1a4674d38
  - section:step-by-step-instructions:33aaaee7e276
  - section:target-audience:90accb0a25c5
  - section:usage-type:d59449ab6f5b
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 LLM Wiki를 언제 확인하거나 갱신해야 하는지 판단할 때 사용한다. 반복 실행 절차는 runbook으로 넘기고, 운영 통제 기준은 policy로 넘긴다.
  removed_semantics:
  - stale:parallel-guide-root
  active_consumers:
  - docs/03.specs/spec-0096-llm-wiki-agent-first-completion/spec.md
  - docs/05.operations/00-workspace/README.md
  - docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/policy.md
  - docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/runbook.md
  - docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/README.md
  - scripts/knowledge/generate-llm-wiki.py
  - scripts/validation/check-repo-contracts.sh
  final_consumers:
  - docs/03.specs/spec-0096-llm-wiki-agent-first-completion/spec.md
  - docs/05.operations/catalog/00-workspace/README.md
  - docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/policy.md
  - docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/runbook.md
  - docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/README.md
  - scripts/knowledge/generate-llm-wiki.py
  - scripts/validation/check-repo-contracts.sh
- legacy_path: docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 7026b98a4245d5f61a885a65eeaef55a278ca61b
  role: policy
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/policy.md
  final_path: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/policy.md
  preserved_semantics:
  - section:controls:027c151eeb74
  - section:exceptions:289483a377e7
  - section:llm-wiki-maintenance-operations-policy:2deb67a5675c
  - section:overview:2696c969e09f
  - section:policy-scope:311eb7de3b0d
  - section:related-documents:7f099c0be7f0
  - section:review-cadence:5326037d314e
  - section:verification:b30d9d21cff3
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/README.md
  - docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/guide.md
  - docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
  - tests/validation/test_agent_governance_contract.py
  final_consumers:
  - docs/05.operations/catalog/00-workspace/README.md
  - docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/guide.md
  - docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
  - tests/validation/test_agent_governance_contract.py
- legacy_path: docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 4a176c23237d6a3f57d2e5149deb4cf1d2cfd9b2
  role: runbook
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/runbook.md
  final_path: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:ai-agent-controls:0d28bacc3223
  - section:automation-handoff:3b8a1c15c0f7
  - section:canonical-references:a63cb6a5e708
  - section:checklist:66ace343eb5a
  - section:escalation:1b7f53a2b9c9
  - section:evidence:aea1a3bdbbfe
  - section:llm-wiki-maintenance-runbook:da4f1b9cd804
  - section:observability-and-evidence-sources:14a6d7a51dc2
  - section:overview:cf1d53f89104
  - section:procedure:5da93bd3e257
  - section:purpose:7567e321168d
  - section:related-documents:4e027d04de9d
  - section:rollback-or-recovery:5ac18bc4e65f
  - section:safe-rollback-or-recovery-procedure:808566b787da
  - section:steps:9967c3592c53
  - section:verification-record:fa3429a98d7b
  - section:verification-steps:70472f7e622f
  - section:when-to-use:59776a4b606e
  - section:when-to-use:bd9d5ee8722b
  - 'text:baseline-body:> Scope: LLM Wiki Maintenance Runbook operational execution'
  removed_semantics:
  - stale:parallel-runbook-root
  active_consumers:
  - docs/05.operations/00-workspace/README.md
  - docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/guide.md
  - docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/policy.md
  - docs/05.operations/00-workspace/ops-0009-release-management/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
  - tests/validation/test_agent_governance_contract.py
  final_consumers:
  - docs/05.operations/catalog/00-workspace/README.md
  - docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/guide.md
  - docs/05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/policy.md
  - docs/05.operations/catalog/00-workspace/ops-0009-release-management/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
  - tests/validation/test_agent_governance_contract.py
- legacy_path: docs/05.operations/00-workspace/ops-0008-new-service-onboarding/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b1cfbce90244bec55b6f82a71c044b819c91f48c
  role: guide
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0008-new-service-onboarding/guide.md
  final_path: docs/05.operations/catalog/00-workspace/ops-0008-new-service-onboarding/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/00-workspace/ops-0008-new-service-onboarding/guide.md
  preserved_semantics:
  - section:common-checks:a2d6d437a156
  - section:common-pitfalls:9fa0937eccc4
  - section:new-service-onboarding-guide:29c1d3305a43
  - section:overview:bdea000a7fee
  - section:prerequisites:8ed03988d929
  - section:purpose:6a5b41762591
  - section:related-documents:4979e3c5de43
  - section:runbook-handoff:e210b2cdfd92
  - section:step-by-step-instructions:979cf22d4f7f
  - section:target-audience:770730927283
  - section:usage-type:c0c66eb4b009
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - examples/sample-web-service/README.md
  - examples/sample-web-service/service.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - examples/sample-web-service/README.md
  - examples/sample-web-service/service.md
- legacy_path: docs/05.operations/00-workspace/ops-0009-release-management/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 1920f2ba528b9d48f0776afcf55ee3e99de10428
  role: runbook
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0009-release-management/runbook.md
  final_path: docs/05.operations/catalog/00-workspace/ops-0009-release-management/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/00-workspace/ops-0009-release-management/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:canonical-references:567d72bba115
  - section:checklist:d4476c1531c3
  - section:escalation:dc660de4527e
  - section:evidence:c4f517685339
  - section:observability-and-evidence-sources:14a6d7a51dc2
  - section:overview:d5bdaeb984aa
  - section:procedure:5da93bd3e257
  - section:purpose:bb3546c11f77
  - section:related-documents:4453cb630c08
  - section:release-management-runbook-procedure:8b5d1974958a
  - section:release-management-runbook:30dde600479b
  - section:rollback-or-recovery:96bcd8bab1c5
  - section:safe-rollback-or-recovery-procedure:808566b787da
  - section:steps:9967c3592c53
  - section:verification-steps:70472f7e622f
  - section:when-to-use:38de6a96d3e1
  - text:baseline-body:Release 또는 tag 생성 전에 local documentation, validation, changelog readiness를 확인해야 할 때.
  removed_semantics:
  - stale:stage-04-execution-route
  active_consumers:
  - docs/03.specs/spec-0097-home-docker-revalidation-deferred-follow-up/spec.md
  - docs/05.operations/00-workspace/README.md
  - docs/05.operations/00-workspace/ops-0008-new-service-onboarding/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - examples/sample-web-service/README.md
  - examples/sample-web-service/service.md
  - scripts/manifest.yaml
  final_consumers:
  - docs/03.specs/spec-0097-home-docker-revalidation-deferred-follow-up/spec.md
  - docs/05.operations/catalog/00-workspace/README.md
  - docs/05.operations/catalog/00-workspace/ops-0008-new-service-onboarding/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - examples/sample-web-service/README.md
  - examples/sample-web-service/service.md
  - scripts/manifest.yaml
- legacy_path: docs/05.operations/00-workspace/ops-0010-sensitive-env-vars-comparison/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: a56f53355f528d8e935bdc915cb02a4554e72d70
  role: guide
  catalog_path: docs/05.operations/catalog/00-workspace/ops-0010-sensitive-env-vars-comparison/guide.md
  final_path: docs/05.operations/catalog/00-workspace/ops-0010-sensitive-env-vars-comparison/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/00-workspace/ops-0010-sensitive-env-vars-comparison/guide.md
  preserved_semantics:
  - section::98d526bcf772
  - section::b38674cf67ab
  - section::c074652f77cc
  - section::ff17df739fbd
  - section:common-checks:fef388c5c4f0
  - section:common-pitfalls:d44786157825
  - section:example:adf2fcd28753
  - section:overview:c2c4c147e10f
  - section:prerequisites:8e6eddc948d2
  - section:purpose:b025eeae74cf
  - section:related-documents:5b5ef73c2299
  - section:runbook-handoff:364a2499eda1
  - section:secrets:ec7c5864acb3
  - section:sensitive-env-vars-md-example-vs-sensitive-env-vars-md-comparison:8d1285600148
  - section:step-by-step-instructions:33aaaee7e276
  - section:target-audience:90accb0a25c5
  - section:usage-type:d59449ab6f5b
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 `secrets/SENSITIVE_ENV_VARS.md.example`과 `secrets/SENSITIVE_ENV_VARS.md`의 카테고리 및 항목 수 일관성을 확인하는 운영 참조 문서다. 실제 파일은 mode 600의 operator-owned
    파일이므로 값 열람 없이 라인 수와 구조 비교만 수행한다.
  removed_semantics:
  - contradiction:sensitive-env-var-count
  active_consumers:
  - docs/03.specs/spec-0090-workspace-audit-2026-05/spec.md
  - docs/05.operations/00-workspace/README.md
  - docs/05.operations/00-workspace/ops-0003-env-key-comparison/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/03.specs/spec-0090-workspace-audit-2026-05/spec.md
  - docs/05.operations/catalog/00-workspace/README.md
  - docs/05.operations/catalog/00-workspace/ops-0003-env-key-comparison/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/01-gateway/README.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d2d77b963b8d34410e3f96a7cef3e330907a5d22
  role: domain-readme
  catalog_path: docs/05.operations/catalog/01-gateway/README.md
  final_path: docs/05.operations/catalog/01-gateway/README.md
  semantic_action: retain
  canonical_role_owner: null
  preserved_semantics:
  - section:audience:e2588f2409d1
  - section:how-to-work-in-this-area:c1a8e3a2fd5b
  - section:operations-01-gateway:259d1e30576a
  - section:overview:f0ef5c662a71
  - section:related-documents:b2cec8fcbe63
  - section:scope:18a27edbf2b1
  - section:structure:a7fff9c4136c
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0001-gateway/spec.md
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/03.specs/spec-0135-target-surface-delta-convergence/task.md
  - docs/05.operations/11-laboratory/ops-0072-dozzle/guide.md
  - docs/05.operations/README.md
  - docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/01-gateway/README.md
  - infra/01-gateway/traefik/config/README.md
  - infra/01-gateway/traefik/dynamic/README.md
  - infra/02-auth/README.md
  - infra/02-auth/oauth2-proxy/README.md
  - infra/03-security/README.md
  - infra/05-messaging/README.md
  - infra/06-observability/README.md
  - infra/06-observability/pushgateway/README.md
  - infra/07-workflow/README.md
  - tests/validation/test_target_surface_delta_contracts.py
  - tests/validation/test_tech_stack_version_contract.py
  final_consumers:
  - docs/03.specs/spec-0001-gateway/spec.md
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/03.specs/spec-0135-target-surface-delta-convergence/task.md
  - docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/guide.md
  - docs/05.operations/README.md
  - docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/01-gateway/README.md
  - infra/01-gateway/traefik/config/README.md
  - infra/01-gateway/traefik/dynamic/README.md
  - infra/02-auth/README.md
  - infra/02-auth/oauth2-proxy/README.md
  - infra/03-security/README.md
  - infra/05-messaging/README.md
  - infra/06-observability/README.md
  - infra/06-observability/pushgateway/README.md
  - infra/07-workflow/README.md
  - tests/validation/test_target_surface_delta_contracts.py
  - tests/validation/test_tech_stack_version_contract.py
- legacy_path: docs/05.operations/01-gateway/ops-0011-nginx/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 52eec39d0198dfcb024cc31fa637bfc084710b34
  role: guide
  catalog_path: docs/05.operations/catalog/01-gateway/ops-0011-nginx/guide.md
  final_path: docs/05.operations/catalog/01-gateway/ops-0011-nginx/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/01-gateway/ops-0011-nginx/guide.md
  preserved_semantics:
  - section:01-gateway-nginx-usage-guide:338c15b54522
  - section:common-checks:ca2bae75a9c0
  - section:common-pitfalls:d9dd00171d51
  - section:overview:0fee11c3fbd3
  - section:prerequisites:8d25ab84199d
  - section:purpose:83a5a0a50c2c
  - section:related-documents:388b526e351d
  - section:runbook-handoff:47c1a4674d38
  - section:step-by-step-instructions:fee89fdf8343
  - section:target-audience:88b6319d983f
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/01-gateway/README.md
  - docs/05.operations/01-gateway/ops-0011-nginx/policy.md
  - docs/05.operations/01-gateway/ops-0011-nginx/runbook.md
  - docs/05.operations/01-gateway/ops-0012-setup/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/nginx/README.md
  - scripts/manifest.yaml
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/01-gateway/README.md
  - docs/05.operations/catalog/01-gateway/ops-0011-nginx/policy.md
  - docs/05.operations/catalog/01-gateway/ops-0011-nginx/runbook.md
  - docs/05.operations/catalog/01-gateway/ops-0012-edge-routing-stack/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/nginx/README.md
  - scripts/manifest.yaml
- legacy_path: docs/05.operations/01-gateway/ops-0011-nginx/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 95cf02aaa74244c467192cfa08d30324a7d8b840
  role: policy
  catalog_path: docs/05.operations/catalog/01-gateway/ops-0011-nginx/policy.md
  final_path: docs/05.operations/catalog/01-gateway/ops-0011-nginx/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/01-gateway/ops-0011-nginx/policy.md
  preserved_semantics:
  - section:01-gateway-nginx-operations-policy:e1c3cd0db4c5
  - section:ai-agent-policy-section-if-applicable:e8e50df972b2
  - section:controls:a0cda8afce91
  - section:exceptions:feec9be9dfbd
  - section:overview:ae014242753f
  - section:policy-scope:31d616953ddc
  - section:related-documents:7f099c0be7f0
  - section:review-cadence:05a2c1cc0283
  - section:verification:c79aaf033c30
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0092-workspace-consistency-2026-05b/spec.md
  - docs/05.operations/01-gateway/README.md
  - docs/05.operations/01-gateway/ops-0011-nginx/guide.md
  - docs/05.operations/01-gateway/ops-0011-nginx/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/nginx/README.md
  final_consumers:
  - docs/03.specs/spec-0092-workspace-consistency-2026-05b/spec.md
  - docs/05.operations/catalog/01-gateway/README.md
  - docs/05.operations/catalog/01-gateway/ops-0011-nginx/guide.md
  - docs/05.operations/catalog/01-gateway/ops-0011-nginx/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/nginx/README.md
- legacy_path: docs/05.operations/01-gateway/ops-0011-nginx/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: ffc500a4282ef1e1e788fb665bab52781dfc862a
  role: runbook
  catalog_path: docs/05.operations/catalog/01-gateway/ops-0011-nginx/runbook.md
  final_path: docs/05.operations/catalog/01-gateway/ops-0011-nginx/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/01-gateway/ops-0011-nginx/runbook.md
  preserved_semantics:
  - section:01-gateway-nginx-procedure:e79590700e89
  - section:01-gateway-nginx-runbook:d8ac7317f9fa
  - section:agent-operations-if-applicable:de7dc827d0e9
  - section:canonical-references:06d2bd9c2683
  - section:checklist:cd9ee8215133
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:observability-and-evidence-sources:e26906cdd4b9
  - section:overview:c5528de94c0e
  - section:procedure:5da93bd3e257
  - section:purpose:87bb0e3d1206
  - section:related-documents:4e027d04de9d
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:1119b29e68b6
  - section:steps:cf6b90881cdd
  - section:verification-steps:ef81852c32ff
  - section:when-to-use:ef1323689337
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/01-gateway/README.md
  - docs/05.operations/01-gateway/ops-0011-nginx/guide.md
  - docs/05.operations/01-gateway/ops-0011-nginx/policy.md
  - docs/05.operations/01-gateway/ops-0012-setup/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/nginx/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/01-gateway/README.md
  - docs/05.operations/catalog/01-gateway/ops-0011-nginx/guide.md
  - docs/05.operations/catalog/01-gateway/ops-0011-nginx/policy.md
  - docs/05.operations/catalog/01-gateway/ops-0012-edge-routing-stack/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/nginx/README.md
- legacy_path: docs/05.operations/01-gateway/ops-0012-setup/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d9e3b438bdae318bcb7571643edc5f9267cbeaef
  role: guide
  catalog_path: docs/05.operations/catalog/01-gateway/ops-0012-setup/guide.md
  final_path: docs/05.operations/catalog/01-gateway/ops-0012-edge-routing-stack/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/01-gateway/ops-0012-edge-routing-stack/guide.md
  preserved_semantics:
  - section:01-gateway-setup-usage:8762b9cc7ef2
  - section:01-setup-operations:051e99665a45
  - section:1-verify-network-contract:ee207d610ebb
  - section:2-configure-traefik:2425c8bac53b
  - section:3-validate-gateway-stack:5167fb919b71
  - section:4-verify-functionality:86e2fdb5cb88
  - section:common-checks:1e2eeeea0f4d
  - section:common-pitfalls:f2403995dbcf
  - section:overview:27527b2a8813
  - section:prerequisites:34c0076cca20
  - section:purpose:3912b71934b2
  - section:related-documents:42d844df14e9
  - section:runbook-handoff:801b2302af8b
  - section:step-by-step-instructions:7a3b95dc4bed
  - section:target-audience:c4938c4794eb
  - section:usage-type:e426b518bdf2
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 `01-gateway` 티어의 초기 설정 및 검증 가이드이다. 현재 root stack은 Traefik을 active include로 사용하고, Nginx는 profile-only leaf로 유지하므로 컨테이너 실행은 승인된 runtime
    context에서만 다룬다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0012-setup
  active_consumers:
  - docs/05.operations/01-gateway/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/README.md
  - scripts/manifest.yaml
  final_consumers:
  - docs/05.operations/catalog/01-gateway/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/README.md
  - scripts/manifest.yaml
- legacy_path: docs/05.operations/01-gateway/ops-0013-traefik/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: ee1b8ca03adb5d0cd54502ed1541ae3576fb6c5e
  role: guide
  catalog_path: docs/05.operations/catalog/01-gateway/ops-0013-traefik/guide.md
  final_path: docs/05.operations/catalog/01-gateway/ops-0013-traefik/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/01-gateway/ops-0013-traefik/guide.md
  preserved_semantics:
  - section:01-gateway-traefik-usage-guide:04ece111e9f0
  - section:common-checks:fb28c543bc94
  - section:common-pitfalls:3c30c14674fa
  - section:overview:51e0ab6e151a
  - section:prerequisites:7f742cc9c009
  - section:purpose:46ccdb02e6e7
  - section:related-documents:388b526e351d
  - section:runbook-handoff:47c1a4674d38
  - section:step-by-step-instructions:9e188ec0c714
  - section:target-audience:88b6319d983f
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/01-gateway/README.md
  - docs/05.operations/01-gateway/ops-0012-setup/guide.md
  - docs/05.operations/01-gateway/ops-0013-traefik/policy.md
  - docs/05.operations/01-gateway/ops-0013-traefik/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/traefik/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/01-gateway/README.md
  - docs/05.operations/catalog/01-gateway/ops-0012-edge-routing-stack/guide.md
  - docs/05.operations/catalog/01-gateway/ops-0013-traefik/policy.md
  - docs/05.operations/catalog/01-gateway/ops-0013-traefik/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/traefik/README.md
- legacy_path: docs/05.operations/01-gateway/ops-0013-traefik/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: baa69b481fbab45ce0694c601ac2a5e3789601f7
  role: policy
  catalog_path: docs/05.operations/catalog/01-gateway/ops-0013-traefik/policy.md
  final_path: docs/05.operations/catalog/01-gateway/ops-0013-traefik/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/01-gateway/ops-0013-traefik/policy.md
  preserved_semantics:
  - section:01-gateway-traefik-operations-policy:3c3768435e28
  - section:ai-agent-policy-section-if-applicable:bd5273f310cc
  - section:controls:775310ce6e3e
  - section:exceptions:ac1aca60c1e0
  - section:overview:96471600b58b
  - section:policy-scope:0811dd72dcf8
  - section:related-documents:7f099c0be7f0
  - section:review-cadence:154af7424ef8
  - section:verification:4d96eab1b7ee
  removed_semantics: []
  active_consumers:
  - docs/05.operations/01-gateway/README.md
  - docs/05.operations/01-gateway/ops-0013-traefik/guide.md
  - docs/05.operations/01-gateway/ops-0013-traefik/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/traefik/README.md
  final_consumers:
  - docs/05.operations/catalog/01-gateway/README.md
  - docs/05.operations/catalog/01-gateway/ops-0013-traefik/guide.md
  - docs/05.operations/catalog/01-gateway/ops-0013-traefik/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/traefik/README.md
- legacy_path: docs/05.operations/01-gateway/ops-0013-traefik/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: f11bb3858c773fde4d7908a3cbbd4614dfcb25b4
  role: runbook
  catalog_path: docs/05.operations/catalog/01-gateway/ops-0013-traefik/runbook.md
  final_path: docs/05.operations/catalog/01-gateway/ops-0013-traefik/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/01-gateway/ops-0013-traefik/runbook.md
  preserved_semantics:
  - section:01-gateway-traefik-procedure:91e95ccc8b90
  - section:01-gateway-traefik-runbook:73f1e2a7abd7
  - section:agent-operations-if-applicable:9e700f0f969d
  - section:canonical-references:06d2bd9c2683
  - section:checklist:3b0d88e9ebcd
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:observability-and-evidence-sources:f980d312fd7a
  - section:overview:65536210bc28
  - section:procedure:5da93bd3e257
  - section:purpose:b02a1ca4dea4
  - section:related-documents:4e027d04de9d
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:686f2880c48e
  - section:steps:6dc2dfbf4886
  - section:verification-steps:f98082be9a86
  - section:when-to-use:85846bceb980
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/01-gateway/README.md
  - docs/05.operations/01-gateway/ops-0012-setup/guide.md
  - docs/05.operations/01-gateway/ops-0013-traefik/guide.md
  - docs/05.operations/01-gateway/ops-0013-traefik/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/traefik/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/01-gateway/README.md
  - docs/05.operations/catalog/01-gateway/ops-0012-edge-routing-stack/guide.md
  - docs/05.operations/catalog/01-gateway/ops-0013-traefik/guide.md
  - docs/05.operations/catalog/01-gateway/ops-0013-traefik/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/01-gateway/traefik/README.md
- legacy_path: docs/05.operations/02-auth/README.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: adc37ae1436cb6e268d31539622b09cd6f44b6d2
  role: domain-readme
  catalog_path: docs/05.operations/catalog/02-auth/README.md
  final_path: docs/05.operations/catalog/02-auth/README.md
  semantic_action: retain
  canonical_role_owner: null
  preserved_semantics:
  - section:audience:0cd22378cae3
  - section:how-to-work-in-this-area:dfa73a201218
  - section:operations-02-auth:8c08d3b66289
  - section:overview:0938a5e6f103
  - section:related-documents:9624e149b57d
  - section:scope:83575bfbab6a
  - section:structure:0e33218e53c5
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0002-auth/spec.md
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/11-laboratory/ops-0072-dozzle/guide.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/01-gateway/nginx/README.md
  - infra/02-auth/README.md
  - infra/02-auth/oauth2-proxy/README.md
  - infra/03-security/README.md
  - infra/06-observability/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
  final_consumers:
  - docs/03.specs/spec-0002-auth/spec.md
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/guide.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/01-gateway/nginx/README.md
  - infra/02-auth/README.md
  - infra/02-auth/oauth2-proxy/README.md
  - infra/03-security/README.md
  - infra/06-observability/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
- legacy_path: docs/05.operations/02-auth/ops-0014-keycloak/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 8ce2ccaae385442189679b42fe40f7acea3b4085
  role: guide
  catalog_path: docs/05.operations/catalog/02-auth/ops-0014-keycloak/guide.md
  final_path: docs/05.operations/catalog/02-auth/ops-0014-keycloak/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/02-auth/ops-0014-keycloak/guide.md
  preserved_semantics:
  - section:02-auth-keycloak-usage-guide:b8c33d660a82
  - section:common-checks:2549cd224bb0
  - section:common-pitfalls:d382950786c7
  - section:overview:02297406a431
  - section:prerequisites:c47e456f8b98
  - section:purpose:0767cccf253e
  - section:related-documents:388b526e351d
  - section:runbook-handoff:47c1a4674d38
  - section:step-by-step-instructions:53766dc22f77
  - section:target-audience:88b6319d983f
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/02-auth/README.md
  - docs/05.operations/02-auth/ops-0014-keycloak/policy.md
  - docs/05.operations/02-auth/ops-0014-keycloak/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/02-auth/keycloak/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/02-auth/README.md
  - docs/05.operations/catalog/02-auth/ops-0014-keycloak/policy.md
  - docs/05.operations/catalog/02-auth/ops-0014-keycloak/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/02-auth/keycloak/README.md
- legacy_path: docs/05.operations/02-auth/ops-0014-keycloak/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: ffad906845d2e84de0a4c52eb88b8c63162bd025
  role: policy
  catalog_path: docs/05.operations/catalog/02-auth/ops-0014-keycloak/policy.md
  final_path: docs/05.operations/catalog/02-auth/ops-0014-keycloak/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/02-auth/ops-0014-keycloak/policy.md
  preserved_semantics:
  - section:02-auth-keycloak-operations-policy:f177308ce8cf
  - section:ai-agent-policy-section-if-applicable:d5e7d63e1c93
  - section:controls:559af842f2c9
  - section:exceptions:643d8e484a05
  - section:overview:40b3f9ab49e8
  - section:policy-scope:3801ee4271fe
  - section:related-documents:7f099c0be7f0
  - section:review-cadence:0f1d28ee4cbd
  - section:verification:77fa33fae4c5
  removed_semantics: []
  active_consumers:
  - docs/05.operations/02-auth/README.md
  - docs/05.operations/02-auth/ops-0014-keycloak/guide.md
  - docs/05.operations/02-auth/ops-0014-keycloak/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/02-auth/keycloak/README.md
  final_consumers:
  - docs/05.operations/catalog/02-auth/README.md
  - docs/05.operations/catalog/02-auth/ops-0014-keycloak/guide.md
  - docs/05.operations/catalog/02-auth/ops-0014-keycloak/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/02-auth/keycloak/README.md
- legacy_path: docs/05.operations/02-auth/ops-0014-keycloak/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: ecd717e99940d5e28e95d2f53f8e88b647894458
  role: runbook
  catalog_path: docs/05.operations/catalog/02-auth/ops-0014-keycloak/runbook.md
  final_path: docs/05.operations/catalog/02-auth/ops-0014-keycloak/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/02-auth/ops-0014-keycloak/runbook.md
  preserved_semantics:
  - section:02-auth-keycloak-procedure:c3d3714e014f
  - section:02-auth-keycloak-runbook:445f2bc9f6e5
  - section:agent-operations-if-applicable:bf7794834f9c
  - section:canonical-references:06d2bd9c2683
  - section:checklist:a43d4aaee5fb
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:observability-and-evidence-sources:83d7b88a70bc
  - section:overview:526b61dfe51d
  - section:procedure:5da93bd3e257
  - section:purpose:f5238a55378a
  - section:related-documents:4e027d04de9d
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:6f2e84db4bd2
  - section:steps:57d8efdb9128
  - section:verification-steps:29271da8275d
  - section:when-to-use:44c7dd635c8d
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/02-auth/README.md
  - docs/05.operations/02-auth/ops-0014-keycloak/guide.md
  - docs/05.operations/02-auth/ops-0014-keycloak/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/02-auth/keycloak/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/02-auth/README.md
  - docs/05.operations/catalog/02-auth/ops-0014-keycloak/guide.md
  - docs/05.operations/catalog/02-auth/ops-0014-keycloak/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/02-auth/keycloak/README.md
- legacy_path: docs/05.operations/02-auth/ops-0015-oauth2-proxy/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: f8b1459be56f5077763bcaa629818a1f285fc0f0
  role: guide
  catalog_path: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/guide.md
  final_path: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/guide.md
  preserved_semantics:
  - section:02-auth-oauth2-proxy-usage-guide:e3c7f2d00184
  - section:common-checks:2549cd224bb0
  - section:common-pitfalls:ebbb25b4f830
  - section:overview:f1d00ea5b41d
  - section:prerequisites:60f1e35ba8a9
  - section:purpose:d9e04c125051
  - section:related-documents:388b526e351d
  - section:runbook-handoff:47c1a4674d38
  - section:step-by-step-instructions:e53b277c43d6
  - section:target-audience:88b6319d983f
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/02-auth/README.md
  - docs/05.operations/02-auth/ops-0015-oauth2-proxy/policy.md
  - docs/05.operations/02-auth/ops-0015-oauth2-proxy/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/02-auth/oauth2-proxy/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/02-auth/README.md
  - docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/policy.md
  - docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/02-auth/oauth2-proxy/README.md
- legacy_path: docs/05.operations/02-auth/ops-0015-oauth2-proxy/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b4ea05ce54cca7672cb969592b3cc2b6c118b6f4
  role: policy
  catalog_path: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/policy.md
  final_path: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/policy.md
  preserved_semantics:
  - section:02-auth-oauth2-proxy-operations-policy:55e4a0b559ae
  - section:ai-agent-policy-section-if-applicable:b46f2a17597f
  - section:controls:8463dc0fd1b5
  - section:exceptions:090744b40c08
  - section:overview:6ee70664ec0d
  - section:policy-scope:a7906cddaef6
  - section:related-documents:7f099c0be7f0
  - section:review-cadence:bb554e41a8be
  - section:verification:7db7ead0700e
  removed_semantics: []
  active_consumers:
  - docs/05.operations/02-auth/README.md
  - docs/05.operations/02-auth/ops-0015-oauth2-proxy/guide.md
  - docs/05.operations/02-auth/ops-0015-oauth2-proxy/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/02-auth/oauth2-proxy/README.md
  final_consumers:
  - docs/05.operations/catalog/02-auth/README.md
  - docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/guide.md
  - docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/02-auth/oauth2-proxy/README.md
- legacy_path: docs/05.operations/02-auth/ops-0015-oauth2-proxy/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: c7dc7dc51059f649618098d53e3ba46e289285d6
  role: runbook
  catalog_path: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/runbook.md
  final_path: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/runbook.md
  preserved_semantics:
  - section:02-auth-oauth2-proxy-procedure:d468d0018aea
  - section:02-auth-oauth2-proxy-runbook:03245fb0c146
  - section:agent-operations-if-applicable:963166d2dcdb
  - section:canonical-references:06d2bd9c2683
  - section:checklist:c2927993bead
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:observability-and-evidence-sources:dbd0d64df8aa
  - section:overview:c0d4a67976cf
  - section:procedure:5da93bd3e257
  - section:purpose:bcdf86a61001
  - section:related-documents:4e027d04de9d
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:c3a7b9e04ad4
  - section:steps:c0fa5d05214a
  - section:verification-steps:8102319edb86
  - section:when-to-use:8b0c178ef033
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/02-auth/README.md
  - docs/05.operations/02-auth/ops-0015-oauth2-proxy/guide.md
  - docs/05.operations/02-auth/ops-0015-oauth2-proxy/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/02-auth/oauth2-proxy/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/02-auth/README.md
  - docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/guide.md
  - docs/05.operations/catalog/02-auth/ops-0015-oauth2-proxy/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/02-auth/oauth2-proxy/README.md
- legacy_path: docs/05.operations/03-security/README.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 297f6b7fd5a0a89552e5023017d3daf11444a034
  role: domain-readme
  catalog_path: docs/05.operations/catalog/03-security/README.md
  final_path: docs/05.operations/catalog/03-security/README.md
  semantic_action: retain
  canonical_role_owner: null
  preserved_semantics:
  - section:audience:0640f3c5c541
  - section:how-to-work-in-this-area:3de09750bf33
  - section:operations-03-security:c9df8068029b
  - section:overview:63b330249f5b
  - section:related-documents:2cefc8aa3461
  - section:scope:c6ba29712c1b
  - section:structure:6d858db6bafa
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/03-security/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
  final_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/03-security/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
- legacy_path: docs/05.operations/03-security/ops-0016-vault/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: a30ec4bd8516fc74d4ff69803976d262bfa8da65
  role: guide
  catalog_path: docs/05.operations/catalog/03-security/ops-0016-vault/guide.md
  final_path: docs/05.operations/catalog/03-security/ops-0016-vault/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/03-security/ops-0016-vault/guide.md
  preserved_semantics:
  - section:03-security-vault-usage-guide:6bd580bc60d1
  - section:common-checks:754ff49ca261
  - section:common-pitfalls:e3c4b2390a73
  - section:overview:8cf0a25f75e2
  - section:prerequisites:c066dbbcee2e
  - section:purpose:2e3ceeaf89ae
  - section:related-documents:388b526e351d
  - section:runbook-handoff:47c1a4674d38
  - section:step-by-step-instructions:025e517783fd
  - section:target-audience:429b12f53180
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0015-security-optimization-hardening.md
  - docs/03.specs/spec-0003-security/spec.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/03-security/README.md
  - docs/05.operations/03-security/ops-0016-vault/policy.md
  - docs/05.operations/03-security/ops-0016-vault/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/03-security/README.md
  - infra/03-security/vault/README.md
  - scripts/manifest.yaml
  - tests/validation/test_script_manifest.py
  final_consumers:
  - docs/01.requirements/prd-0015-security-optimization-hardening.md
  - docs/03.specs/spec-0003-security/spec.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/03-security/README.md
  - docs/05.operations/catalog/03-security/ops-0016-vault/policy.md
  - docs/05.operations/catalog/03-security/ops-0016-vault/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/03-security/README.md
  - infra/03-security/vault/README.md
  - scripts/manifest.yaml
  - tests/validation/test_script_manifest.py
- legacy_path: docs/05.operations/03-security/ops-0016-vault/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 62f2d6420bc87090aeb14fcc42d2307480bfbce4
  role: policy
  catalog_path: docs/05.operations/catalog/03-security/ops-0016-vault/policy.md
  final_path: docs/05.operations/catalog/03-security/ops-0016-vault/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/03-security/ops-0016-vault/policy.md
  preserved_semantics:
  - section:03-security-vault-operations-policy:00f1f6400a8f
  - section:ai-agent-policy-section-if-applicable:b35ca80d2014
  - section:auto-unseal-remote-audit-adoption-gate:18b659b61e02
  - section:controls:043df3a04ff2
  - section:exceptions:10c36a8f584e
  - section:overview:29eb7458c37e
  - section:policy-scope:ae90f7b799cf
  - section:related-documents:7f099c0be7f0
  - section:review-cadence:2aee39356baa
  - section:verification:1f11019735f8
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0015-security-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0018-security-optimization-hardening-architecture.md
  - docs/03.specs/spec-0003-security/spec.md
  - docs/05.operations/03-security/README.md
  - docs/05.operations/03-security/ops-0016-vault/guide.md
  - docs/05.operations/03-security/ops-0016-vault/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/03-security/vault/README.md
  final_consumers:
  - docs/01.requirements/prd-0015-security-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0018-security-optimization-hardening-architecture.md
  - docs/03.specs/spec-0003-security/spec.md
  - docs/05.operations/catalog/03-security/README.md
  - docs/05.operations/catalog/03-security/ops-0016-vault/guide.md
  - docs/05.operations/catalog/03-security/ops-0016-vault/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/03-security/vault/README.md
- legacy_path: docs/05.operations/03-security/ops-0016-vault/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 162f1774d9463fcff84a289bc80a192b04db1dca
  role: runbook
  catalog_path: docs/05.operations/catalog/03-security/ops-0016-vault/runbook.md
  final_path: docs/05.operations/catalog/03-security/ops-0016-vault/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/03-security/ops-0016-vault/runbook.md
  preserved_semantics:
  - section:03-security-vault-procedure:92538d8298c1
  - section:03-security-vault-runbook:3782747680f8
  - section:agent-operations-if-applicable:65f85916431e
  - section:canonical-references:655e51316f4a
  - section:checklist:971e7da29b04
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:observability-and-evidence-sources:9b0a62463956
  - section:overview:4933a229d60e
  - section:procedure:5da93bd3e257
  - section:purpose:4526780eb263
  - section:related-documents:4e027d04de9d
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:328594e01fd4
  - section:steps:fae8c604ef3a
  - section:verification-steps:b334584dbc25
  - section:when-to-use:4ed169b6fd05
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0015-security-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0018-security-optimization-hardening-architecture.md
  - docs/03.specs/spec-0003-security/spec.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/03-security/README.md
  - docs/05.operations/03-security/ops-0016-vault/guide.md
  - docs/05.operations/03-security/ops-0016-vault/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/03-security/vault/README.md
  final_consumers:
  - docs/01.requirements/prd-0015-security-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0018-security-optimization-hardening-architecture.md
  - docs/03.specs/spec-0003-security/spec.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/03-security/README.md
  - docs/05.operations/catalog/03-security/ops-0016-vault/guide.md
  - docs/05.operations/catalog/03-security/ops-0016-vault/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/03-security/vault/README.md
- legacy_path: docs/05.operations/04-data/README.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: e4fab4b77d5ad7a249eac8116b336edc78c6d379
  role: domain-readme
  catalog_path: docs/05.operations/catalog/04-data/README.md
  final_path: docs/05.operations/catalog/04-data/README.md
  semantic_action: retain
  canonical_role_owner: null
  preserved_semantics:
  - section:audience:45e61f379e99
  - section:how-to-work-in-this-area:337b67e34061
  - section:operations-04-data:941b8e862c70
  - section:overview:2796720f0739
  - section:related-documents:392d2881011a
  - section:scope:9a1f4a6a566e
  - section:structure:d024e3e74ab6
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0005-data-analytics.md
  - docs/02.architecture/decisions/adr-0015-analytics-engine-selection.md
  - docs/02.architecture/descriptions/ad-0012-data-analytics-architecture.md
  - docs/03.specs/spec-0005-data-analytics/spec.md
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/03.specs/spec-0135-target-surface-delta-convergence/spec.md
  - docs/03.specs/spec-0135-target-surface-delta-convergence/task.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/02-auth/README.md
  - infra/04-data/analytics/README.md
  - infra/04-data/lake-and-object/README.md
  - infra/04-data/nosql/README.md
  - infra/04-data/operational/README.md
  - infra/04-data/relational/README.md
  - infra/04-data/specialized/README.md
  - infra/04-data/specialized/neo4j/README.md
  - infra/04-data/specialized/qdrant/README.md
  - infra/05-messaging/README.md
  - infra/06-observability/README.md
  - infra/07-workflow/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
  final_consumers:
  - docs/01.requirements/prd-0005-data-analytics.md
  - docs/02.architecture/decisions/adr-0015-analytics-engine-selection.md
  - docs/02.architecture/descriptions/ad-0012-data-analytics-architecture.md
  - docs/03.specs/spec-0005-data-analytics/spec.md
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/03.specs/spec-0135-target-surface-delta-convergence/spec.md
  - docs/03.specs/spec-0135-target-surface-delta-convergence/task.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/02-auth/README.md
  - infra/04-data/analytics/README.md
  - infra/04-data/lake-and-object/README.md
  - infra/04-data/nosql/README.md
  - infra/04-data/operational/README.md
  - infra/04-data/relational/README.md
  - infra/04-data/specialized/README.md
  - infra/04-data/specialized/neo4j/README.md
  - infra/04-data/specialized/qdrant/README.md
  - infra/05-messaging/README.md
  - infra/06-observability/README.md
  - infra/07-workflow/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
- legacy_path: docs/05.operations/04-data/ops-0017-analytics-influxdb/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b299574d4266581af44a9dc50964b0d1bd3540be
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0017-analytics-influxdb/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0017-influxdb/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0017-influxdb/guide.md
  preserved_semantics:
  - section:common-checks:ae862266107b
  - section:common-pitfalls:ebc7a244c4a7
  - section:influxdb-usage-guide:fee2dd87184f
  - section:overview:36fc08da9e5b
  - section:prerequisites:35cfd942a8ed
  - section:purpose:c5f6ededad05
  - section:related-documents:c149799bd1ce
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:096d2f5987ff
  - section:target-audience:089658ef5a70
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 `infra/04-data/analytics/influxdb`의 InfluxDB 사용 가이드다. 현재 구현은 InfluxDB 3 Core 단일 compose이며 database와 HTTP line-protocol endpoint/schema
    source contract를 정의한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0017-analytics-influxdb
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0017-analytics-influxdb/policy.md
  - docs/05.operations/04-data/ops-0017-analytics-influxdb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/influxdb/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0017-influxdb/policy.md
  - docs/05.operations/catalog/04-data/ops-0017-influxdb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/influxdb/README.md
- legacy_path: docs/05.operations/04-data/ops-0017-analytics-influxdb/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 3ec95196abb60fd2d058c508250d80af3cea231f
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0017-analytics-influxdb/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0017-influxdb/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0017-influxdb/policy.md
  preserved_semantics:
  - section:controls:ec636898fb08
  - section:exceptions:041c2677ad31
  - section:influxdb-operations-policy:c7c150337645
  - section:overview:fe4eabfb3381
  - section:policy-scope:3f75788b0ec4
  - section:related-documents:871ec253ddb2
  - section:review-cadence:3b4ffea6708a
  - section:verification:22a501d6eacb
  - 'text:baseline-body:**Required**: operations use `docker-compose.yml`, `INFLUXDB_DB_NAME`, port `8181`, and `/api/v3/write_lp` for line-protocol writes.'
  removed_semantics:
  - stale:legacy-subject-path:ops-0017-analytics-influxdb
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0017-analytics-influxdb/guide.md
  - docs/05.operations/04-data/ops-0017-analytics-influxdb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/influxdb/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0017-influxdb/guide.md
  - docs/05.operations/catalog/04-data/ops-0017-influxdb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/influxdb/README.md
- legacy_path: docs/05.operations/04-data/ops-0017-analytics-influxdb/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 0655d2a4d697f505b5dd268dcc8fd8c915164cfa
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0017-analytics-influxdb/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0017-influxdb/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0017-influxdb/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:e81231f106b2
  - section:canonical-references:2baec816b955
  - section:checklist:7544573b522a
  - section:escalation:1b86ed84c904
  - section:evidence:909c41c4b3ff
  - section:influxdb-recovery-procedure:fc69c1f8ab6b
  - section:influxdb-recovery-runbook:33cf814dc92b
  - section:observability-and-evidence-sources:f1b2d7ea5a34
  - section:overview:24af99585738
  - section:procedure:5da93bd3e257
  - section:purpose:00332840594a
  - section:related-documents:9f28eaeb0b4d
  - section:rollback-or-recovery:5d26144a4f6b
  - section:safe-rollback-or-recovery-procedure:58dda717e966
  - section:steps:63ac350268e3
  - section:verification-steps:a74b4a74d791
  - section:when-to-use:e3997d82e77b
  - text:baseline-body:`influxdb` container healthcheck가 실패할 때
  removed_semantics:
  - stale:legacy-subject-path:ops-0017-analytics-influxdb
  active_consumers:
  - docs/03.specs/spec-0005-data-analytics/spec.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0017-analytics-influxdb/guide.md
  - docs/05.operations/04-data/ops-0017-analytics-influxdb/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/influxdb/README.md
  final_consumers:
  - docs/03.specs/spec-0005-data-analytics/spec.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0017-influxdb/guide.md
  - docs/05.operations/catalog/04-data/ops-0017-influxdb/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/influxdb/README.md
- legacy_path: docs/05.operations/04-data/ops-0018-analytics-ksqldb/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b1cd43379f5b67a9c23c5509a886c8a8ce21d4e7
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0018-analytics-ksqldb/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0018-ksqldb/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0018-ksqldb/guide.md
  preserved_semantics:
  - section:common-checks:a5f4c2e45476
  - section:common-pitfalls:5365ad182d6b
  - section:ksqldb-usage-guide:aef3ebbcc819
  - section:overview:379291d44e30
  - section:prerequisites:24aa6b508bc2
  - section:purpose:7ecd9c61c9ca
  - section:related-documents:92f182b096fa
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:18ad8e169ca8
  - section:target-audience:32c3fcf09427
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 `infra/04-data/analytics/ksql`의 ksqlDB 사용 가이드다. 현재 compose는 `ksqldb-server`를 `data` profile로 실행하고, `ksqldb-cli`와 `ksql-datagen`은 `ksql`
    profile의 보조 job/tooling service로 유지한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0018-analytics-ksqldb
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0018-analytics-ksqldb/policy.md
  - docs/05.operations/04-data/ops-0018-analytics-ksqldb/runbook.md
  - docs/05.operations/05-messaging/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/ksql/README.md
  - tests/validation/test_script_manifest.py
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0018-ksqldb/policy.md
  - docs/05.operations/catalog/04-data/ops-0018-ksqldb/runbook.md
  - docs/05.operations/catalog/05-messaging/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/ksql/README.md
  - tests/validation/test_script_manifest.py
- legacy_path: docs/05.operations/04-data/ops-0018-analytics-ksqldb/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: c29fd832fcdefc51a145d5e45a8f4a0293fc10f4
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0018-analytics-ksqldb/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0018-ksqldb/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0018-ksqldb/policy.md
  preserved_semantics:
  - section:controls:022bfaf5eb72
  - section:exceptions:5b3bb984a177
  - section:ksqldb-operations-policy:e4560c1ff42b
  - section:overview:6189a1218b49
  - section:policy-scope:572849604b11
  - section:related-documents:85299051664a
  - section:review-cadence:9222aa08f849
  - section:verification:81ca43fcb030
  - 'text:baseline-body:**Required**: server changes must preserve Kafka bootstrap server, Schema Registry URL, Kafka Connect URL, and `KSQL_HEAP_OPTS` evidence in
    compose.'
  removed_semantics:
  - stale:legacy-subject-path:ops-0018-analytics-ksqldb
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0018-analytics-ksqldb/guide.md
  - docs/05.operations/04-data/ops-0018-analytics-ksqldb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/ksql/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0018-ksqldb/guide.md
  - docs/05.operations/catalog/04-data/ops-0018-ksqldb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/ksql/README.md
- legacy_path: docs/05.operations/04-data/ops-0018-analytics-ksqldb/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: e5f62638cc79b7bf09ba47716cdb5a515dcc8373
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0018-analytics-ksqldb/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0018-ksqldb/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0018-ksqldb/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:1ea69cc6a5b0
  - section:canonical-references:363281122f05
  - section:checklist:f1ace4d40ce5
  - section:escalation:43b4965df33f
  - section:evidence:6a0a082e64a6
  - section:ksqldb-recovery-procedure:33b206384637
  - section:ksqldb-recovery-runbook:38cb9c3b2f4d
  - section:observability-and-evidence-sources:33c26c8cbc0d
  - section:overview:329e7715aab1
  - section:procedure:5da93bd3e257
  - section:purpose:bfe02e2fd060
  - section:related-documents:9f28eaeb0b4d
  - section:rollback-or-recovery:f8a7ec9571fb
  - section:safe-rollback-or-recovery-procedure:827f654c4922
  - section:steps:9b6b327f7c9e
  - section:verification-steps:36966e7dc89e
  - section:when-to-use:7e91b42d0848
  - text:baseline-body:`ksqldb-server` `/info` endpoint가 실패할 때
  removed_semantics:
  - stale:legacy-subject-path:ops-0018-analytics-ksqldb
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0018-analytics-ksqldb/guide.md
  - docs/05.operations/04-data/ops-0018-analytics-ksqldb/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/ksql/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0018-ksqldb/guide.md
  - docs/05.operations/catalog/04-data/ops-0018-ksqldb/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/ksql/README.md
- legacy_path: docs/05.operations/04-data/ops-0019-analytics-opensearch/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 5f98f7140a252cbe3abf65d563b0e299b300d8f5
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0019-analytics-opensearch/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0019-opensearch/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0019-opensearch/guide.md
  preserved_semantics:
  - section:common-checks:6da8897c640c
  - section:common-pitfalls:88de9145e525
  - section:opensearch-usage-guide:d93866c70905
  - section:overview:57f58ffdcbc2
  - section:prerequisites:9235d781d327
  - section:purpose:f5fea39205c3
  - section:related-documents:809c1d2a1a21
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:5f9f7fbb0382
  - section:target-audience:f7dad154b372
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 `infra/04-data/analytics/opensearch`의 OpenSearch 사용 가이드다. 현재 primary compose는 `opensearch`와 `opensearch-dashboards`를 제공하며, `docker-compose.cluster.yml`은
    optional cluster variant로 별도 검증한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0019-analytics-opensearch
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0019-analytics-opensearch/policy.md
  - docs/05.operations/04-data/ops-0019-analytics-opensearch/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/opensearch/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0019-opensearch/policy.md
  - docs/05.operations/catalog/04-data/ops-0019-opensearch/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/opensearch/README.md
- legacy_path: docs/05.operations/04-data/ops-0019-analytics-opensearch/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 04e0d9deab2ae1ea1c67109ef43720f0de9eafa4
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0019-analytics-opensearch/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0019-opensearch/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0019-opensearch/policy.md
  preserved_semantics:
  - section:controls:e9725258239e
  - section:exceptions:3efce0dfaeb4
  - section:opensearch-operations-policy:21fd577f1f0c
  - section:overview:cc2331c5343d
  - section:policy-scope:5ba5cdd7c0ad
  - section:related-documents:c5292f2f2361
  - section:review-cadence:4fa32ef8488b
  - section:verification:cc181be64ab1
  - 'text:baseline-body:**Required**: OpenSearch API checks must use HTTPS and secret-backed admin authentication.'
  removed_semantics:
  - stale:legacy-subject-path:ops-0019-analytics-opensearch
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0019-analytics-opensearch/guide.md
  - docs/05.operations/04-data/ops-0019-analytics-opensearch/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/opensearch/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0019-opensearch/guide.md
  - docs/05.operations/catalog/04-data/ops-0019-opensearch/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/opensearch/README.md
- legacy_path: docs/05.operations/04-data/ops-0019-analytics-opensearch/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 03c0212e7bcd4adb04c835a80fa5b3392fc03548
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0019-analytics-opensearch/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0019-opensearch/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0019-opensearch/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:29ca04795a8d
  - section:canonical-references:bf6a6e6986a5
  - section:checklist:497b756fd3bb
  - section:escalation:894aefde1054
  - section:evidence:2f037103c7fc
  - section:observability-and-evidence-sources:4651745e5bca
  - section:opensearch-recovery-procedure:1e1d90efbf43
  - section:opensearch-recovery-runbook:8cb8a9c6dcd9
  - section:overview:5d533a1bedab
  - section:procedure:5da93bd3e257
  - section:purpose:729e3066c9be
  - section:related-documents:9f28eaeb0b4d
  - section:rollback-or-recovery:eaa4f61bcc99
  - section:safe-rollback-or-recovery-procedure:ee0a4e4ec491
  - section:steps:ae308bce5a54
  - section:verification-steps:5447e043e22d
  - section:when-to-use:7e4bf7ca154a
  - text:baseline-body:primary `opensearch` healthcheck fails
  removed_semantics:
  - stale:legacy-subject-path:ops-0019-analytics-opensearch
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0019-analytics-opensearch/guide.md
  - docs/05.operations/04-data/ops-0019-analytics-opensearch/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/opensearch/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0019-opensearch/guide.md
  - docs/05.operations/catalog/04-data/ops-0019-opensearch/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/opensearch/README.md
- legacy_path: docs/05.operations/04-data/ops-0020-analytics-warehouses/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 4f96585e89a84ab9b4b9d9e64033acde6b3a85d4
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0020-analytics-warehouses/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0020-starrocks/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0020-starrocks/guide.md
  preserved_semantics:
  - section:common-checks:b890929cfca3
  - section:common-pitfalls:72c1ba82250f
  - section:overview:d5613ebeefab
  - section:prerequisites:e56df1a3ebbf
  - section:purpose:f233c7abd55e
  - section:related-documents:7c435fcfb59b
  - section:runbook-handoff:a6f4d9784508
  - section:starrocks-usage-guide:35d46adc7331
  - section:step-by-step-instructions:450dfcf8109c
  - section:target-audience:0f260d12f89e
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 `infra/04-data/analytics/warehouses`의 StarRocks 사용 가이드다. 현재 compose는 `starrocks-fe`와 `starrocks-be` 단일 pair를 제공하고, BE는 FE에 `ALTER SYSTEM
    ADD BACKEND "starrocks-be:9050"` 명령으로 등록된다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0020-analytics-warehouses
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0020-analytics-warehouses/policy.md
  - docs/05.operations/04-data/ops-0020-analytics-warehouses/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/warehouses/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0020-starrocks/policy.md
  - docs/05.operations/catalog/04-data/ops-0020-starrocks/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/warehouses/README.md
- legacy_path: docs/05.operations/04-data/ops-0020-analytics-warehouses/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 18aa5a8cb7ef8ceaca051f168d3a2ca99fc4e9a0
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0020-analytics-warehouses/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0020-starrocks/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0020-starrocks/policy.md
  preserved_semantics:
  - section:controls:d6b5fdc99220
  - section:exceptions:da48da8c246b
  - section:overview:b642c6f6d83c
  - section:policy-scope:2f9fb9ad7e57
  - section:related-documents:a1093a3cf0d1
  - section:review-cadence:bf7d01a10a65
  - section:starrocks-operations-policy:bd26b38612f9
  - section:verification:cadd82c8b6ca
  - 'text:baseline-body:**Required**: BE registration must preserve the compose command that adds `starrocks-be:9050` to FE before starting BE.'
  removed_semantics:
  - stale:legacy-subject-path:ops-0020-analytics-warehouses
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0020-analytics-warehouses/guide.md
  - docs/05.operations/04-data/ops-0020-analytics-warehouses/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/warehouses/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0020-starrocks/guide.md
  - docs/05.operations/catalog/04-data/ops-0020-starrocks/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/warehouses/README.md
- legacy_path: docs/05.operations/04-data/ops-0020-analytics-warehouses/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 5a0c38397f62024c7c3816b5a27cb9926990c9b1
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0020-analytics-warehouses/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0020-starrocks/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0020-starrocks/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:1ea69cc6a5b0
  - section:canonical-references:d0a39c718b5e
  - section:checklist:201c548d723e
  - section:escalation:5df4a413ca3a
  - section:evidence:4ad89dd8ea19
  - section:observability-and-evidence-sources:8cdb156a1e65
  - section:overview:db9fc5b24d1f
  - section:procedure:5da93bd3e257
  - section:purpose:8c8668b40e07
  - section:related-documents:9f28eaeb0b4d
  - section:rollback-or-recovery:d486a328a5f7
  - section:safe-rollback-or-recovery-procedure:c896bdba9b62
  - section:starrocks-recovery-procedure:172804763e06
  - section:starrocks-recovery-runbook:816b33c79635
  - section:steps:fb57dde620d1
  - section:verification-steps:da8c1ddd555b
  - section:when-to-use:8d7ce19ddee9
  - text:baseline-body:`SHOW FRONTENDS` or `SHOW BACKENDS` health evidence fails
  removed_semantics:
  - stale:legacy-subject-path:ops-0020-analytics-warehouses
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0020-analytics-warehouses/guide.md
  - docs/05.operations/04-data/ops-0020-analytics-warehouses/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/warehouses/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0020-starrocks/guide.md
  - docs/05.operations/catalog/04-data/ops-0020-starrocks/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/analytics/warehouses/README.md
- legacy_path: docs/05.operations/04-data/ops-0021-backup-backup-policy/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 0184cad19940e50d4efb9c7aad44f088f6df7c4a
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0021-backup-backup-policy/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0021-backup-and-restore/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0021-backup-and-restore/policy.md
  preserved_semantics:
  - section:04-data-backup-policy:1e557d57907f
  - section:controls:d77b8075c812
  - section:exceptions:957e9fd9f2f7
  - section:overview:cc68df87693a
  - section:policy-scope:42b397a00e90
  - section:related-documents:b39d2e53a35d
  - section:review-cadence:88b9ee5be1cd
  - section:verification:53a0cec4297e
  - 'text:baseline-body:**Required**: critical relational and Supabase data must have daily backups with 30-day retention and monthly verification evidence.'
  removed_semantics:
  - stale:legacy-subject-path:ops-0021-backup-backup-policy
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0035-storage-storage-exhaustion/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0035-storage-exhaustion/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: e268e1c87bbd863a2f8717eb700890f1962d5338
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0022-cache-and-kv-valkey-cluster/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/guide.md
  preserved_semantics:
  - section:common-checks:2b57dc6f0cf1
  - section:common-pitfalls:debdfbc48e72
  - section:overview:c67e05f49507
  - section:prerequisites:7c44de35946e
  - section:purpose:99b8240cd324
  - section:related-documents:c162211f2a93
  - section:runbook-handoff:641266e98c03
  - section:step-by-step-instructions:9e35b8d06d2c
  - section:target-audience:4b38006ca81a
  - section:usage-type:9740efe86c23
  - section:usage:63bfd61a0561
  - section:valkey-cluster-usage-guide:7748e0c008d3
  - text:baseline-body:`valkey-cluster`는 `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml`에 선언된 6-node Valkey cache/kv cluster다. 현재 구현은 `data` 및 `service`
    profile에서 `valkey-node-0`부터 `valkey-node-5`, `valkey-cluster-init`, `valkey-cluster-exporter`를 실행하고, 모든 runtime credential은 Docker Secret `service_valkey_password`로
    주입한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0022-cache-and-kv-valkey-cluster
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/policy.md
  - docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/cache-and-kv/README.md
  - infra/04-data/cache-and-kv/valkey-cluster/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/policy.md
  - docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/cache-and-kv/README.md
  - infra/04-data/cache-and-kv/valkey-cluster/README.md
- legacy_path: docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 411d35bd8140007f76adb09ae0cbaa85e5a06f4f
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0022-cache-and-kv-valkey-cluster/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/policy.md
  preserved_semantics:
  - section:controls:a1d23d838190
  - section:exceptions:1d87aa3f3b3c
  - section:overview:f3f612704307
  - section:policy-scope:c748d307269d
  - section:related-documents:1321344a5d70
  - section:review-cadence:e5f88821780c
  - section:valkey-cluster-operations-policy:db213cb9e435
  - section:verification:32f70483b907
  - text:baseline-body:Authentication and node-to-node `masterauth` use Docker Secret `service_valkey_password`.
  removed_semantics:
  - stale:legacy-subject-path:ops-0022-cache-and-kv-valkey-cluster
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/guide.md
  - docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/cache-and-kv/README.md
  - infra/04-data/cache-and-kv/valkey-cluster/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/guide.md
  - docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/cache-and-kv/README.md
  - infra/04-data/cache-and-kv/valkey-cluster/README.md
- legacy_path: docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 1362cd4cddee31d4dd9ae76653307a2e7aaae145
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0022-cache-and-kv-valkey-cluster/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:f664ad9fdfca
  - section:canonical-references:fc3df506a891
  - section:checklist:35cc41b21ff6
  - section:escalation:79ca9360c465
  - section:evidence:b056e6a0592e
  - section:observability-and-evidence-sources:e08d6937d3be
  - section:overview:a2392050840a
  - section:procedure:5da93bd3e257
  - section:purpose:ca5d70b3962a
  - section:related-documents:060bd99a5a55
  - section:rollback-or-recovery:e72da5f3dd83
  - section:safe-rollback-or-recovery-procedure:45b23015a592
  - section:steps:6dbb392a855a
  - section:valkey-cluster-health-procedure:276ea4f4d2ea
  - section:valkey-cluster-health-runbook:da6184d93bc4
  - section:verification-steps:fd9034b474ff
  - section:when-to-use:8b516120e8d8
  - text:baseline-body:One or more `valkey-node-*` services are missing or unhealthy.
  removed_semantics:
  - stale:legacy-subject-path:ops-0022-cache-and-kv-valkey-cluster
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/guide.md
  - docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/cache-and-kv/README.md
  - infra/04-data/cache-and-kv/valkey-cluster/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/guide.md
  - docs/05.operations/catalog/04-data/ops-0022-valkey-cluster/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/cache-and-kv/README.md
  - infra/04-data/cache-and-kv/valkey-cluster/README.md
- legacy_path: docs/05.operations/04-data/ops-0023-lake-and-object-minio/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 966b1a6486c1550936ff8ffd6a709ea4f3197756
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0023-lake-and-object-minio/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0023-minio/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0023-minio/guide.md
  preserved_semantics:
  - section:common-checks:2c93e84c7fb1
  - section:common-pitfalls:605a0e24ad03
  - section:minio-object-storage-usage-guide:50259b7ce0be
  - section:overview:a1061db9b49d
  - section:prerequisites:9513ce8bb7d6
  - section:purpose:43418aba7789
  - section:related-documents:2616949f8a69
  - section:runbook-handoff:641266e98c03
  - section:step-by-step-instructions:859a5dd14dff
  - section:target-audience:4b38006ca81a
  - section:usage-type:9740efe86c23
  - section:usage:63bfd61a0561
  - text:baseline-body:MinIO는 `infra/04-data/lake-and-object/minio/docker-compose.yml`에 선언된 S3-compatible object storage다. 현재 root-active compose path는 단일 `minio`
    service와 bucket/bootstrap job `minio-create-buckets`를 실행하며, optional `docker-compose.cluster.yaml`은 root include에 포함되지 않은 별도 cluster variant다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0023-lake-and-object-minio
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0023-lake-and-object-minio/policy.md
  - docs/05.operations/04-data/ops-0023-lake-and-object-minio/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/lake-and-object/minio/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0023-minio/policy.md
  - docs/05.operations/catalog/04-data/ops-0023-minio/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/lake-and-object/minio/README.md
- legacy_path: docs/05.operations/04-data/ops-0023-lake-and-object-minio/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b949b1ac9cde4e3b9585d23af02d7c8744779eda
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0023-lake-and-object-minio/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0023-minio/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0023-minio/policy.md
  preserved_semantics:
  - section:controls:fd964b443a96
  - section:exceptions:39b17478de20
  - section:minio-object-storage-operations-policy:374dd354f1c8
  - section:overview:8fe221affb95
  - section:policy-scope:855fa63cc9f5
  - section:related-documents:eb362b89fdb4
  - section:review-cadence:d8b3722ea82e
  - section:verification:88e108d149e7
  - text:baseline-body:Root and app credentials are injected through Docker Secrets under `/run/secrets/`.
  removed_semantics:
  - stale:legacy-subject-path:ops-0023-lake-and-object-minio
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0023-lake-and-object-minio/guide.md
  - docs/05.operations/04-data/ops-0023-lake-and-object-minio/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/lake-and-object/minio/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0023-minio/guide.md
  - docs/05.operations/catalog/04-data/ops-0023-minio/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/lake-and-object/minio/README.md
- legacy_path: docs/05.operations/04-data/ops-0023-lake-and-object-minio/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 4b253d6e07a67cab529108280a7aab8780d28e16
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0023-lake-and-object-minio/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0023-minio/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0023-minio/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:f664ad9fdfca
  - section:canonical-references:e714b7932036
  - section:checklist:935e87709281
  - section:escalation:37a2e17ff035
  - section:evidence:01cf37a1827e
  - section:minio-object-storage-health-procedure:bf3877e31a5b
  - section:minio-object-storage-health-runbook:ef5234dc9d52
  - section:observability-and-evidence-sources:d19b649eae54
  - section:overview:1ae07ecc4242
  - section:procedure:5da93bd3e257
  - section:purpose:0a70f59a5485
  - section:related-documents:af4302ad0b56
  - section:rollback-or-recovery:a0b3aec2c39e
  - section:safe-rollback-or-recovery-procedure:f96cbc832348
  - section:steps:6bcfee435c92
  - section:verification-steps:d2d647361049
  - section:when-to-use:20a0cb37472b
  - text:baseline-body:`minio` is missing, unhealthy, or unavailable through the Traefik route.
  removed_semantics:
  - stale:legacy-subject-path:ops-0023-lake-and-object-minio
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0023-lake-and-object-minio/guide.md
  - docs/05.operations/04-data/ops-0023-lake-and-object-minio/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/lake-and-object/minio/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0023-minio/guide.md
  - docs/05.operations/catalog/04-data/ops-0023-minio/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/lake-and-object/minio/README.md
- legacy_path: docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 63ea9f701e74d4f7cb84f76e641b441ed9325be4
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0024-lake-and-object-seaweedfs/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0024-seaweedfs/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0024-seaweedfs/guide.md
  preserved_semantics:
  - section:common-checks:7f01f249b921
  - section:common-pitfalls:cd95bfabf5df
  - section:overview:0f693bb6c99c
  - section:prerequisites:5dcd32441bad
  - section:purpose:8f26a5f25d81
  - section:related-documents:f3962c11edc0
  - section:runbook-handoff:641266e98c03
  - section:seaweedfs-usage-guide:4af57d6daa9c
  - section:step-by-step-instructions:5f46890bef2f
  - section:target-audience:4b38006ca81a
  - section:usage-type:9740efe86c23
  - section:usage:63bfd61a0561
  - text:baseline-body:SeaweedFS는 `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`에 선언된 distributed file/object storage stack이다. 현재 구현은 `data` profile에서
    `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-mount`를 실행하며, all services use `infra_net` and image `chrislusf/seaweedfs:4.38`.
  removed_semantics:
  - stale:legacy-subject-path:ops-0024-lake-and-object-seaweedfs
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/policy.md
  - docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/lake-and-object/seaweedfs/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0024-seaweedfs/policy.md
  - docs/05.operations/catalog/04-data/ops-0024-seaweedfs/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/lake-and-object/seaweedfs/README.md
- legacy_path: docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 1ddbb9058d16800f54fd030584b6c5104ad37095
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0024-lake-and-object-seaweedfs/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0024-seaweedfs/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0024-seaweedfs/policy.md
  preserved_semantics:
  - section:controls:9037bec37a78
  - section:exceptions:fca566d8551b
  - section:overview:8d9ff17b7799
  - section:policy-scope:4d7f7789e878
  - section:related-documents:f88d21195344
  - section:review-cadence:2e08247534cc
  - section:seaweedfs-operations-policy:e18ceba13c0b
  - section:verification:3b04c4ff7d28
  - text:baseline-body:Compose-facing documentation must list image `chrislusf/seaweedfs:4.38` and the current five-service set.
  removed_semantics:
  - stale:legacy-subject-path:ops-0024-lake-and-object-seaweedfs
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/guide.md
  - docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/lake-and-object/seaweedfs/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0024-seaweedfs/guide.md
  - docs/05.operations/catalog/04-data/ops-0024-seaweedfs/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/lake-and-object/seaweedfs/README.md
- legacy_path: docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 119df17aa8af7cd198d0d2d53327a43afc74c765
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0024-lake-and-object-seaweedfs/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0024-seaweedfs/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0024-seaweedfs/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:63f3c1bc2740
  - section:canonical-references:49407bc0e165
  - section:checklist:50ccb4713d2c
  - section:escalation:f8cabbf5812d
  - section:evidence:ecc96b4f82d6
  - section:observability-and-evidence-sources:d6094f850e44
  - section:overview:94bd776b18eb
  - section:procedure:5da93bd3e257
  - section:purpose:09a6ea5995fc
  - section:related-documents:5d985beb2337
  - section:rollback-or-recovery:db378adc7823
  - section:safe-rollback-or-recovery-procedure:6b965d089bc1
  - section:seaweedfs-stack-health-procedure:23d8e381aaa3
  - section:seaweedfs-stack-health-runbook:44f48b1247ff
  - section:steps:fafcbb20c781
  - section:verification-steps:e47610d931d5
  - section:when-to-use:c51106895420
  - text:baseline-body:`seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, or `seaweedfs-s3` is missing or unhealthy.
  removed_semantics:
  - stale:legacy-subject-path:ops-0024-lake-and-object-seaweedfs
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/guide.md
  - docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/lake-and-object/seaweedfs/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0024-seaweedfs/guide.md
  - docs/05.operations/catalog/04-data/ops-0024-seaweedfs/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/lake-and-object/seaweedfs/README.md
- legacy_path: docs/05.operations/04-data/ops-0025-nosql-cassandra/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 4bd6b0c75e51e046dcf2c8eb09d77e8fb47eb64d
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0025-nosql-cassandra/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0025-cassandra/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0025-cassandra/guide.md
  preserved_semantics:
  - section:cassandra-usage-guide:4277f9a39cf4
  - section:common-checks:9f618313a504
  - section:common-pitfalls:8321dac83b81
  - section:overview:51c72fdef021
  - section:prerequisites:4b61e87449c7
  - section:purpose:7d4dbec8057a
  - section:related-documents:9c43c8631c84
  - section:runbook-handoff:6403829c7a07
  - section:step-by-step-instructions:295b81c7b3ed
  - section:target-audience:9abee23c6211
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 `infra/04-data/nosql/cassandra/docker-compose.yml`에 정의된 Cassandra 단일 노드와 `cassandra-exporter`를 기준으로 사용 맥락, 접속 방식, 일반 점검 방법을 설명한다. 현재
    루트 compose에서는 Cassandra include가 주석 처리된 선택 서비스이며, 활성화 시 `data` 프로파일의 `cassandra-node1`과 `data`/`obs` 프로파일의 `cassandra-exporter`가 `infra_net`에서 동작한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0025-nosql-cassandra
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0025-nosql-cassandra/policy.md
  - docs/05.operations/04-data/ops-0025-nosql-cassandra/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/cassandra/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0025-cassandra/policy.md
  - docs/05.operations/catalog/04-data/ops-0025-cassandra/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/cassandra/README.md
- legacy_path: docs/05.operations/04-data/ops-0025-nosql-cassandra/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 3bb28fc0d16cb13d5bccebee198a29f04c433514
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0025-nosql-cassandra/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0025-cassandra/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0025-cassandra/policy.md
  preserved_semantics:
  - section:cassandra-operations-policy:a1ee1659f04c
  - section:controls:dd3aa3cf9039
  - section:exceptions:1c46a9a63e45
  - section:overview:2c092b464bc4
  - section:policy-scope:fb2526e4d340
  - section:related-documents:e6e6ae3f7f7d
  - section:review-cadence:fc29ce40e527
  - section:verification:ba7a8b35db62
  - 'text:baseline-body:**Required**: Cassandra documentation must identify the current implementation as a single-node optional include, not as an active multi-node
    high-availability cluster.'
  removed_semantics:
  - stale:legacy-subject-path:ops-0025-nosql-cassandra
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0025-nosql-cassandra/guide.md
  - docs/05.operations/04-data/ops-0025-nosql-cassandra/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/cassandra/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0025-cassandra/guide.md
  - docs/05.operations/catalog/04-data/ops-0025-cassandra/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/cassandra/README.md
- legacy_path: docs/05.operations/04-data/ops-0025-nosql-cassandra/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 33489c68f57f58e2e51205de70342a651814e850
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0025-nosql-cassandra/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0025-cassandra/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0025-cassandra/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:b29d583bcd8e
  - section:canonical-references:813f2de23b4e
  - section:cassandra-health-and-recovery-triage-procedure:e4142d97ef7e
  - section:cassandra-health-and-recovery-triage-runbook:f135f8620954
  - section:checklist:cca699f13d5d
  - section:escalation:dcb7dd02e630
  - section:evidence:b25089afc950
  - section:observability-and-evidence-sources:f242814d0e6e
  - section:overview:17e1c6820a4b
  - section:procedure:5da93bd3e257
  - section:purpose:11c2573813f6
  - section:related-documents:9f54b8f7e94b
  - section:rollback-or-recovery:7e4f6d6f661c
  - section:safe-rollback-or-recovery-procedure:8ceaef852db0
  - section:steps:abaa8c5eddc1
  - section:verification-steps:0b46d9e349b5
  - section:when-to-use:7781a2b61c9c
  - text:baseline-body:`cassandra-node1`가 unhealthy, stopped, or missing 상태일 때
  removed_semantics:
  - stale:legacy-subject-path:ops-0025-nosql-cassandra
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0025-nosql-cassandra/guide.md
  - docs/05.operations/04-data/ops-0025-nosql-cassandra/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/cassandra/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0025-cassandra/guide.md
  - docs/05.operations/catalog/04-data/ops-0025-cassandra/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/cassandra/README.md
- legacy_path: docs/05.operations/04-data/ops-0026-nosql-couchdb/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 7c4e685944b7fd86271d2d894c5540d2528c4897
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0026-nosql-couchdb/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0026-couchdb/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0026-couchdb/guide.md
  preserved_semantics:
  - section:common-checks:1986da8f7688
  - section:common-pitfalls:3808a6eabec7
  - section:couchdb-usage-guide:64dd146a2710
  - section:overview:5364074127ab
  - section:prerequisites:4676a0e2fe68
  - section:purpose:c6f5c6bcc0f5
  - section:related-documents:b6d89cfc4eb1
  - section:runbook-handoff:0f930b8d0bd1
  - section:step-by-step-instructions:0f3ff0ff464d
  - section:target-audience:9abee23c6211
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 `infra/04-data/nosql/couchdb/docker-compose.yml`에 정의된 CouchDB 3노드 클러스터 사용 기준을 설명한다. 현재 루트 compose에서는 CouchDB include가 주석 처리된 선택 서비스이며,
    활성화 시 `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`가 `data` 프로파일과 `infra_net`에서 동작한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0026-nosql-couchdb
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0026-nosql-couchdb/policy.md
  - docs/05.operations/04-data/ops-0026-nosql-couchdb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/couchdb/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0026-couchdb/policy.md
  - docs/05.operations/catalog/04-data/ops-0026-couchdb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/couchdb/README.md
- legacy_path: docs/05.operations/04-data/ops-0026-nosql-couchdb/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 48997ded6ca18def5ba16dcda3fbfcc0ee544341
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0026-nosql-couchdb/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0026-couchdb/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0026-couchdb/policy.md
  preserved_semantics:
  - section:controls:83c9cfb60b35
  - section:couchdb-operations-policy:61ab65cb9b91
  - section:exceptions:1c46a9a63e45
  - section:overview:945d5eb7ac1e
  - section:policy-scope:214e16a2a7d8
  - section:related-documents:7d5696d436d6
  - section:review-cadence:e3090b3deede
  - section:verification:3eb95c331f54
  - 'text:baseline-body:**Required**: Documentation must use current service names `couchdb-1`, `couchdb-2`, `couchdb-3`, and `couchdb-cluster-init`.'
  removed_semantics:
  - stale:legacy-subject-path:ops-0026-nosql-couchdb
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0026-nosql-couchdb/guide.md
  - docs/05.operations/04-data/ops-0026-nosql-couchdb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/couchdb/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0026-couchdb/guide.md
  - docs/05.operations/catalog/04-data/ops-0026-couchdb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/couchdb/README.md
- legacy_path: docs/05.operations/04-data/ops-0026-nosql-couchdb/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: a79e9c1989fd144ae7e7a85312eb5c63d209a4b2
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0026-nosql-couchdb/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0026-couchdb/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0026-couchdb/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:b29d583bcd8e
  - section:canonical-references:a31b096f61c7
  - section:checklist:c6802a41a798
  - section:couchdb-cluster-triage-procedure:e8cd5010c6f1
  - section:couchdb-cluster-triage-runbook:cc5769a81c8b
  - section:escalation:5dab350020cb
  - section:evidence:f64b4c529f57
  - section:observability-and-evidence-sources:3efbd00daa26
  - section:overview:df44df4da5ce
  - section:procedure:5da93bd3e257
  - section:purpose:d3761a6e67ea
  - section:related-documents:de5f0db15ee8
  - section:rollback-or-recovery:0ef0ed29e039
  - section:safe-rollback-or-recovery-procedure:aa421e1846af
  - section:steps:0de1a5d679ed
  - section:verification-steps:71b7c1757c5d
  - section:when-to-use:c2fea86bbb5f
  - text:baseline-body:한 개 이상의 CouchDB 노드가 unhealthy, stopped, or missing 상태일 때
  removed_semantics:
  - stale:legacy-subject-path:ops-0026-nosql-couchdb
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0026-nosql-couchdb/guide.md
  - docs/05.operations/04-data/ops-0026-nosql-couchdb/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/couchdb/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0026-couchdb/guide.md
  - docs/05.operations/catalog/04-data/ops-0026-couchdb/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/couchdb/README.md
- legacy_path: docs/05.operations/04-data/ops-0027-nosql-mongodb/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 8be37ebcf123dee585fcb80b6df915eaf9653db1
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0027-nosql-mongodb/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0027-mongodb/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0027-mongodb/guide.md
  preserved_semantics:
  - section:common-checks:f68be04ad46e
  - section:common-pitfalls:f4889f8cf240
  - section:mongodb-usage-guide:aca423365ab7
  - section:overview:b7094cd9c134
  - section:prerequisites:ec5cdbaaa784
  - section:purpose:e2fba7ee95df
  - section:related-documents:eaa6feddd60b
  - section:runbook-handoff:fc4f662172fa
  - section:step-by-step-instructions:7519f70723ef
  - section:target-audience:9abee23c6211
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 `infra/04-data/nosql/mongodb/docker-compose.yml`에 정의된 MongoDB replica set 사용 기준을 설명한다. 현재 루트 compose에서는 MongoDB include가 주석 처리된 선택 서비스이며,
    활성화 시 `mongo-key-generator`, `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter`가 `data`/`obs` 프로파일과 `infra_net`에서
    동작한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0027-nosql-mongodb
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0027-nosql-mongodb/policy.md
  - docs/05.operations/04-data/ops-0027-nosql-mongodb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/mongodb/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0027-mongodb/policy.md
  - docs/05.operations/catalog/04-data/ops-0027-mongodb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/mongodb/README.md
- legacy_path: docs/05.operations/04-data/ops-0027-nosql-mongodb/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: a43a2a7cf31ff6b3923b2ed87661341a9e05e902
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0027-nosql-mongodb/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0027-mongodb/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0027-mongodb/policy.md
  preserved_semantics:
  - section:controls:d7bf247ef63c
  - section:exceptions:1c46a9a63e45
  - section:mongodb-operations-policy:4d5f4537916e
  - section:overview:0e7c215ebee9
  - section:policy-scope:c6529cae1357
  - section:related-documents:a703ffb0b71c
  - section:review-cadence:af382ea646c9
  - section:verification:82a081add005
  - 'text:baseline-body:**Required**: Documentation must describe the current replica set as two data-bearing nodes plus one arbiter, initialized by `mongo-init`.'
  removed_semantics:
  - stale:legacy-subject-path:ops-0027-nosql-mongodb
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0027-nosql-mongodb/guide.md
  - docs/05.operations/04-data/ops-0027-nosql-mongodb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/mongodb/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0027-mongodb/guide.md
  - docs/05.operations/catalog/04-data/ops-0027-mongodb/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/mongodb/README.md
- legacy_path: docs/05.operations/04-data/ops-0027-nosql-mongodb/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: e748d9e21684d5731e622a33c556c828edf27f20
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0027-nosql-mongodb/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0027-mongodb/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0027-mongodb/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:b29d583bcd8e
  - section:canonical-references:f064c6dbac8e
  - section:checklist:695afe3c7633
  - section:escalation:97ea5ad395a3
  - section:evidence:ded095b19530
  - section:mongodb-replica-set-triage-procedure:edead786b0f8
  - section:mongodb-replica-set-triage-runbook:e6279db35aaa
  - section:observability-and-evidence-sources:d5403b9d044f
  - section:overview:13652ef11658
  - section:procedure:5da93bd3e257
  - section:purpose:7fbd3be58cad
  - section:related-documents:3bdb0193e53c
  - section:rollback-or-recovery:a8eea7a83cb7
  - section:safe-rollback-or-recovery-procedure:d133ec0951a9
  - section:steps:b8e61bf3a498
  - section:verification-steps:5db96c6db15b
  - section:when-to-use:7f7c0463fdda
  - text:baseline-body:`mongodb-rep1` 또는 `mongodb-rep2`가 unhealthy, stopped, or missing 상태일 때
  removed_semantics:
  - stale:legacy-subject-path:ops-0027-nosql-mongodb
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0027-nosql-mongodb/guide.md
  - docs/05.operations/04-data/ops-0027-nosql-mongodb/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/mongodb/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0027-mongodb/guide.md
  - docs/05.operations/catalog/04-data/ops-0027-mongodb/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/nosql/mongodb/README.md
- legacy_path: docs/05.operations/04-data/ops-0028-operational-mng-db/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 95f2678496aa0aaacd2b55218a9994bcd8e03c70
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0028-operational-mng-db/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0028-management-database/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0028-management-database/guide.md
  preserved_semantics:
  - section:common-checks:5f3e3f412fd6
  - section:common-pitfalls:b857be62d834
  - section:management-database-usage-guide:853db5bd2c5c
  - section:overview:392deeee614a
  - section:prerequisites:e80316703750
  - section:purpose:48fa368830aa
  - section:related-documents:711f3374661f
  - section:runbook-handoff:641266e98c03
  - section:step-by-step-instructions:012b84090605
  - section:target-audience:4b38006ca81a
  - section:usage-type:9740efe86c23
  - section:usage:63bfd61a0561
  - text:baseline-body:`mng-db`는 플랫폼 관리 서비스가 공유하는 PostgreSQL/Valkey 운영 데이터 계층이다. 현재 구현은 `infra/04-data/operational/mng-db/docker-compose.yml`의 `mng` 및 `dev` profile로
    선언되며, Keycloak, n8n, Airflow, Terrakube, SonarQube, 기본 service DB를 위한 PostgreSQL role/database와 Valkey cache를 제공한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0028-operational-mng-db
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0028-operational-mng-db/policy.md
  - docs/05.operations/04-data/ops-0028-operational-mng-db/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/operational/mng-db/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0028-management-database/policy.md
  - docs/05.operations/catalog/04-data/ops-0028-management-database/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/operational/mng-db/README.md
- legacy_path: docs/05.operations/04-data/ops-0028-operational-mng-db/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 3b664e51f4a0ecd3c34ca2e0cc542bbc0b7467fd
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0028-operational-mng-db/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0028-management-database/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0028-management-database/policy.md
  preserved_semantics:
  - section:controls:534bacf69f37
  - section:exceptions:080eab87e728
  - section:management-database-operations-policy:1ade86145d1a
  - section:overview:ce250053766a
  - section:policy-scope:6bdf900f093e
  - section:related-documents:bbbd468b0dff
  - section:review-cadence:55ae0c9d2052
  - section:verification:95ff09bdfc16
  - text:baseline-body:Passwords and service credentials are injected through Docker Secrets under `/run/secrets/`.
  removed_semantics:
  - stale:legacy-subject-path:ops-0028-operational-mng-db
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0028-operational-mng-db/guide.md
  - docs/05.operations/04-data/ops-0028-operational-mng-db/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/operational/mng-db/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0028-management-database/guide.md
  - docs/05.operations/catalog/04-data/ops-0028-management-database/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/operational/mng-db/README.md
- legacy_path: docs/05.operations/04-data/ops-0028-operational-mng-db/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 09854c811e8b214657acb3b1c61315c21d5169e1
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0028-operational-mng-db/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0028-management-database/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0028-management-database/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:f3f5d4a7f4e7
  - section:canonical-references:f945618a5e04
  - section:checklist:c349533d7bbd
  - section:escalation:07b69eed7135
  - section:evidence:fbd1b40fff5e
  - section:management-database-health-and-init-procedure:d0ce8fddf020
  - section:management-database-health-and-init-runbook:bbce5822d3d7
  - section:observability-and-evidence-sources:42ec20ac9264
  - section:overview:d8a6ae1c7d37
  - section:procedure:5da93bd3e257
  - section:purpose:c7fbc82d97e9
  - section:related-documents:2b80feb7ba2f
  - section:rollback-or-recovery:78b4e02332e6
  - section:safe-rollback-or-recovery-procedure:b8b00dd634d0
  - section:steps:97cf5474219a
  - section:verification-steps:14538e934865
  - section:when-to-use:5f5a559e788f
  - text:baseline-body:`mng-pg`, `mng-valkey`, or exporter services are missing or unhealthy.
  removed_semantics:
  - stale:legacy-subject-path:ops-0028-operational-mng-db
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0028-operational-mng-db/guide.md
  - docs/05.operations/04-data/ops-0028-operational-mng-db/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/operational/mng-db/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0028-management-database/guide.md
  - docs/05.operations/catalog/04-data/ops-0028-management-database/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/operational/mng-db/README.md
- legacy_path: docs/05.operations/04-data/ops-0029-operational-supabase/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 92a7339a97ee7b9b93788e301c43496948169d84
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0029-operational-supabase/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0029-supabase/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0029-supabase/guide.md
  preserved_semantics:
  - section:common-checks:131ce5de3bb1
  - section:common-pitfalls:0c823eaf1759
  - section:overview:5ff7a915f732
  - section:prerequisites:3832b396748a
  - section:purpose:54fe1ca886e4
  - section:related-documents:6c6d8272f290
  - section:runbook-handoff:641266e98c03
  - section:step-by-step-instructions:b04a9a19914c
  - section:supabase-usage-guide:dd967eef560a
  - section:target-audience:4b38006ca81a
  - section:usage-type:9740efe86c23
  - section:usage:63bfd61a0561
  - text:baseline-body:`supabase`는 `infra/04-data/operational/supabase/docker-compose.yml`에 선언된 `data` profile 기반의 통합 백엔드 플랫폼이다. 현재 구현은 PostgreSQL, Kong Gateway,
    Auth, REST, Realtime, Storage, Studio, Edge Functions, analytics/logging, pooler를 `infra_net` 안에서 구성하고, 외부 접근은 compose에 선언된 Kong 및 일부 관리 포트를 통해 제한한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0029-operational-supabase
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0029-operational-supabase/policy.md
  - docs/05.operations/04-data/ops-0029-operational-supabase/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/operational/supabase/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0029-supabase/policy.md
  - docs/05.operations/catalog/04-data/ops-0029-supabase/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/operational/supabase/README.md
- legacy_path: docs/05.operations/04-data/ops-0029-operational-supabase/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: ed7e4b6755c41956c74a20ff8436e7613d87aec2
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0029-operational-supabase/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0029-supabase/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0029-supabase/policy.md
  preserved_semantics:
  - section:controls:4c0cf881c843
  - section:exceptions:2021400de9c3
  - section:overview:820e76eefa07
  - section:policy-scope:85d6f0531ba1
  - section:related-documents:5dd73eced7ce
  - section:review-cadence:1e35305d69a4
  - section:supabase-operations-policy:36d28b39776e
  - section:verification:cce6bed27d06
  - text:baseline-body:Supabase secrets are injected through Docker Secrets under `/run/secrets/`.
  removed_semantics:
  - stale:legacy-subject-path:ops-0029-operational-supabase
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0029-operational-supabase/guide.md
  - docs/05.operations/04-data/ops-0029-operational-supabase/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/operational/supabase/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0029-supabase/guide.md
  - docs/05.operations/catalog/04-data/ops-0029-supabase/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/operational/supabase/README.md
- legacy_path: docs/05.operations/04-data/ops-0029-operational-supabase/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: c9cbd009642a1006d9eefb5222057cc3856e6c5c
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0029-operational-supabase/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0029-supabase/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0029-supabase/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:f664ad9fdfca
  - section:canonical-references:473a370aa828
  - section:checklist:1a0ac6b07981
  - section:escalation:83948029ed1b
  - section:evidence:a748035d5a13
  - section:observability-and-evidence-sources:974a4ba1ca51
  - section:overview:a354c676c7a2
  - section:procedure:5da93bd3e257
  - section:purpose:9e42c642a69b
  - section:related-documents:763fe897ed9d
  - section:rollback-or-recovery:652a14987508
  - section:safe-rollback-or-recovery-procedure:0e24cd8745aa
  - section:steps:efa9b44a8a20
  - section:supabase-stack-health-procedure:011222448b8d
  - section:supabase-stack-health-runbook:41d2a6c6650d
  - section:verification-steps:219cffa0b4be
  - section:when-to-use:5a0b64c86969
  - text:baseline-body:`studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `db`, `analytics`, or `supavisor` is unhealthy or missing.
  removed_semantics:
  - stale:legacy-subject-path:ops-0029-operational-supabase
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0029-operational-supabase/guide.md
  - docs/05.operations/04-data/ops-0029-operational-supabase/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/operational/supabase/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0029-supabase/guide.md
  - docs/05.operations/catalog/04-data/ops-0029-supabase/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/operational/supabase/README.md
- legacy_path: docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 328adb7880797f8c2eadfd8daed76ba0eeb01855
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0030-optimization-optimization-hardening/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/guide.md
  preserved_semantics:
  - section:04-data-optimization-hardening-usage-guide:c6198fb08c7e
  - section:common-checks:c841f8ae9206
  - section:common-pitfalls:fdc385025bcb
  - section:overview:895b121c6a42
  - section:prerequisites:411c8c9d21a8
  - section:purpose:a86e8275aa2f
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:0d70f41b0e3b
  - section:target-audience:6341d3e3050c
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 `04-data` 계층의 즉시 하드닝 항목을 운영자/개발자가 재현 가능하게 적용하기 위한 가이드다. `supabase` healthcheck 보강, `valkey` 시크릿 경로 정합화, `seaweedfs` compose 정합화, `ksql`
    라벨 정규화 절차를 제공한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0030-optimization-optimization-hardening
  active_consumers:
  - docs/01.requirements/prd-0016-data-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0019-data-optimization-hardening-architecture.md
  - docs/03.specs/spec-0004-data/spec.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/policy.md
  - docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0016-data-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0019-data-optimization-hardening-architecture.md
  - docs/03.specs/spec-0004-data/spec.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/policy.md
  - docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: a9ad8bdda281fcf21f66f8e62ee0d5adf56cb1d2
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0030-optimization-optimization-hardening/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/policy.md
  preserved_semantics:
  - section:04-data-optimization-hardening-operations-policy:12067d9e2116
  - section:ai-agent-policy-section-if-applicable:e62ba53557ca
  - section:catalog-expansion-approval-gates:fd3c977e43d9
  - section:controls:11e89198d0eb
  - section:exceptions:62cb0aab3050
  - section:overview:140756171251
  - section:policy-scope:6b5d3f828254
  - section:related-documents:b7726adff5a9
  - section:review-cadence:8ae77604f09c
  - section:verification:65131a6a5cc5
  - text:baseline-body:04-data 구성 변경은 `infrastructure-hardening` CI 게이트를 통과해야 한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0030-optimization-optimization-hardening
  active_consumers:
  - docs/01.requirements/prd-0016-data-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0019-data-optimization-hardening-architecture.md
  - docs/03.specs/spec-0004-data/spec.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/guide.md
  - docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0016-data-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0019-data-optimization-hardening-architecture.md
  - docs/03.specs/spec-0004-data/spec.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/guide.md
  - docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 4170913c9c96bf1554cd711c0d659e4d5c65fb42
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0030-optimization-optimization-hardening/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/runbook.md
  preserved_semantics:
  - section:04-data-optimization-hardening-procedure:9dd65d926017
  - section:04-data-optimization-hardening-runbook:0c003a6fb613
  - section:agent-operations-if-applicable:0a385eb3b9f7
  - section:canonical-references:55285a740918
  - section:checklist:a1d6021725a2
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:observability-and-evidence-sources:5f426f6656da
  - section:overview:23922f9068bd
  - section:procedure:5da93bd3e257
  - section:purpose:2a8d52cb0913
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:38b10e33fb35
  - section:steps:6cfcac2deb27
  - section:verification-steps:d56fadc4c565
  - section:when-to-use:6e28bd0c4ace
  - text:baseline-body:`infrastructure-hardening` CI가 실패할 때
  removed_semantics:
  - stale:legacy-subject-path:ops-0030-optimization-optimization-hardening
  active_consumers:
  - docs/01.requirements/prd-0016-data-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0019-data-optimization-hardening-architecture.md
  - docs/03.specs/spec-0004-data/spec.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/guide.md
  - docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0016-data-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0019-data-optimization-hardening-architecture.md
  - docs/03.specs/spec-0004-data/spec.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/guide.md
  - docs/05.operations/catalog/04-data/ops-0030-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 7d0625becd6aea550d5a5a9cbaaa3e82b42fc31d
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0031-relational-postgresql-cluster/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/guide.md
  preserved_semantics:
  - section:common-checks:8ac9b34065ea
  - section:common-pitfalls:accb0fc395cf
  - section:overview:631357a4190d
  - section:postgresql-cluster-usage-guide:fbaacf81a457
  - section:prerequisites:2b9f9287f5ea
  - section:purpose:739a01c71f25
  - section:related-documents:3bfee1a5d18d
  - section:runbook-handoff:bcff1a30f158
  - section:step-by-step-instructions:2707fbacd2b7
  - section:target-audience:9abee23c6211
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 `infra/04-data/relational/postgresql-cluster/docker-compose.yml`에 정의된 PostgreSQL HA cluster 사용 기준을 설명한다. 현재 루트 compose에서는 `postgresql-cluster`
    include가 주석 처리된 선택 서비스이며, 활성화 시 etcd 3노드, Spilo/Patroni PostgreSQL 3노드, `pg-router`, `pg-cluster-init`, per-node postgres exporter가 `data`/`service` 프로파일에서 동작한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0031-relational-postgresql-cluster
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/policy.md
  - docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/relational/README.md
  - infra/04-data/relational/postgresql-cluster/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/policy.md
  - docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/relational/README.md
  - infra/04-data/relational/postgresql-cluster/README.md
- legacy_path: docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 706657c0ef1441c189652c6cb08e8fe8688a83b5
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0031-relational-postgresql-cluster/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/policy.md
  preserved_semantics:
  - section:controls:3cec1b62c613
  - section:exceptions:1c46a9a63e45
  - section:overview:bd81a4d4b938
  - section:policy-scope:ccc5e90a63b9
  - section:postgresql-cluster-operations-policy:bfab04fd01a7
  - section:related-documents:7c0389b43935
  - section:review-cadence:7e470fcbdb1e
  - section:verification:b969d9356131
  - 'text:baseline-body:**Required**: Documentation must identify the cluster as an optional/commented root include unless root compose changes.'
  removed_semantics:
  - stale:legacy-subject-path:ops-0031-relational-postgresql-cluster
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/guide.md
  - docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/relational/postgresql-cluster/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/guide.md
  - docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/relational/postgresql-cluster/README.md
- legacy_path: docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 985f9fc7b648d0fa741599b92502cde6c14e045f
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0031-relational-postgresql-cluster/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:b29d583bcd8e
  - section:canonical-references:4a676bac8afb
  - section:checklist:d2a47ebc4183
  - section:escalation:1e0ed2732844
  - section:evidence:dea42bab8f8d
  - section:observability-and-evidence-sources:d78b84ee3122
  - section:overview:4b1b43117580
  - section:postgresql-cluster-health-and-recovery-triage-procedure:5a89d8ef992f
  - section:postgresql-cluster-health-and-recovery-triage-runbook:31e38ef6e8d0
  - section:procedure:5da93bd3e257
  - section:purpose:5f44b3238ccd
  - section:related-documents:61097959383e
  - section:rollback-or-recovery:a87c0ab87a1b
  - section:safe-rollback-or-recovery-procedure:1b398915f68c
  - section:steps:29e996731cd3
  - section:verification-steps:b4b3f687d98a
  - section:when-to-use:b4b3453da77e
  - text:baseline-body:`pg-router` write/read endpoint가 응답하지 않을 때
  removed_semantics:
  - stale:legacy-subject-path:ops-0031-relational-postgresql-cluster
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/guide.md
  - docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/policy.md
  - docs/05.operations/04-data/ops-0032-relational-postgresql-logical-upgrade-restore-rehearsal/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/relational/postgresql-cluster/README.md
  - tests/validation/test_script_manifest.py
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/guide.md
  - docs/05.operations/catalog/04-data/ops-0031-postgresql-cluster/policy.md
  - docs/05.operations/catalog/04-data/ops-0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/relational/postgresql-cluster/README.md
  - tests/validation/test_script_manifest.py
- legacy_path: docs/05.operations/04-data/ops-0032-relational-postgresql-logical-upgrade-restore-rehearsal/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 1016242af1ee811fe899e47b1a4b1acc624dd5f5
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0032-relational-postgresql-logical-upgrade-restore-rehearsal/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md
  preserved_semantics:
  - section:automation-handoff:8dcad8ca29de
  - section:escalation:f80781873ed3
  - section:evidence:5a971c805a45
  - section:overview:5dbfc2182590
  - section:postgresql-logical-upgrade-and-restore-rehearsal-runbook:227be530e11b
  - section:procedure:a99606dbdca2
  - section:related-documents:3e8ccaf62461
  - section:rollback-or-recovery:663ab02a3ae9
  - section:trigger-and-preconditions:ad4985903e04
  - section:verification-record:0a7d1e256977
  - section:when-to-use:57f78049ee1b
  - text:baseline-body:PostgreSQL source/target image pin, fixture, oracle, wrapper, or recovery boundary가 바뀐 뒤 local representative evidence를 갱신할 때
  removed_semantics:
  - stale:legacy-subject-path:ops-0032-relational-postgresql-logical-upgrade-restore-rehearsal
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
  - tests/validation/test_script_manifest.py
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/manifest.yaml
  - tests/validation/test_script_manifest.py
- legacy_path: docs/05.operations/04-data/ops-0033-specialized-neo4j/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d9f2ba55eea69e09820f5ef844667853ac112c15
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0033-specialized-neo4j/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0033-neo4j/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0033-neo4j/guide.md
  preserved_semantics:
  - section:common-checks:e887f2002764
  - section:common-pitfalls:2a28d1372c0a
  - section:neo4j-usage-guide:9e703735cbc3
  - section:overview:9c8e95cfa5de
  - section:prerequisites:aba37801a72a
  - section:purpose:f9227ec1d53d
  - section:related-documents:b054dab5f4e9
  - section:runbook-handoff:e6124cbce3b7
  - section:step-by-step-instructions:75e7f9f4eefd
  - section:target-audience:9abee23c6211
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 root compose에 active include된 `infra/04-data/specialized/neo4j/docker-compose.yml` 기준으로 Neo4j graph database의 사용 맥락과 일반 점검 방법을 설명한다.
    현재 구현은 `neo4j:5.26.26-community`, 단일 `neo4j` 서비스, `data`/`graph` 프로파일, `infra_net`, `neo4j_password` Docker Secret, secret-aware entrypoint, Traefik HTTP Browser
    route를 사용한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0033-specialized-neo4j
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0033-specialized-neo4j/policy.md
  - docs/05.operations/04-data/ops-0033-specialized-neo4j/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/specialized/neo4j/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0033-neo4j/policy.md
  - docs/05.operations/catalog/04-data/ops-0033-neo4j/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/specialized/neo4j/README.md
- legacy_path: docs/05.operations/04-data/ops-0033-specialized-neo4j/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 849f5d668820024f2e353a35f635f6e9f32b0ed6
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0033-specialized-neo4j/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0033-neo4j/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0033-neo4j/policy.md
  preserved_semantics:
  - section:controls:87762600fe8e
  - section:exceptions:1c46a9a63e45
  - section:neo4j-operations-policy:c3cc81d263af
  - section:overview:6eadbdfdcbba
  - section:policy-scope:2d501a425b47
  - section:related-documents:b9d128b28957
  - section:review-cadence:dfceb73754ce
  - section:verification:5a724552905c
  - 'text:baseline-body:**Required**: Documentation must describe Neo4j as a root-active single Community service, not as a cluster or Enterprise deployment.'
  removed_semantics:
  - stale:legacy-subject-path:ops-0033-specialized-neo4j
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0033-specialized-neo4j/guide.md
  - docs/05.operations/04-data/ops-0033-specialized-neo4j/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/specialized/neo4j/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0033-neo4j/guide.md
  - docs/05.operations/catalog/04-data/ops-0033-neo4j/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/specialized/neo4j/README.md
- legacy_path: docs/05.operations/04-data/ops-0033-specialized-neo4j/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 5d29dd8754ac97c0a65f80ac6fefae8ce6980c3c
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0033-specialized-neo4j/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0033-neo4j/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0033-neo4j/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:b29d583bcd8e
  - section:canonical-references:6a11ab967a83
  - section:checklist:a47a2ef454bd
  - section:escalation:96ddbc5c4785
  - section:evidence:1c0dd49b6f68
  - section:neo4j-health-and-recovery-triage-procedure:8461df3c60a2
  - section:neo4j-health-and-recovery-triage-runbook:093708c92dda
  - section:observability-and-evidence-sources:e9638778f605
  - section:overview:f703bcd42436
  - section:procedure:5da93bd3e257
  - section:purpose:cb24a081b987
  - section:related-documents:b0f1e6d567ee
  - section:rollback-or-recovery:05dde4d8e995
  - section:safe-rollback-or-recovery-procedure:6ca911ab01d1
  - section:steps:c59f93e4f817
  - section:verification-steps:1573f8305467
  - section:when-to-use:fcdd414a2a6b
  - text:baseline-body:`neo4j`가 unhealthy, stopped, or missing 상태일 때
  removed_semantics:
  - stale:legacy-subject-path:ops-0033-specialized-neo4j
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0033-specialized-neo4j/guide.md
  - docs/05.operations/04-data/ops-0033-specialized-neo4j/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/specialized/neo4j/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0033-neo4j/guide.md
  - docs/05.operations/catalog/04-data/ops-0033-neo4j/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/specialized/neo4j/README.md
- legacy_path: docs/05.operations/04-data/ops-0034-specialized-qdrant/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 8107e3842c5db769f0d184c0121f3022ad3ab6db
  role: guide
  catalog_path: docs/05.operations/catalog/04-data/ops-0034-specialized-qdrant/guide.md
  final_path: docs/05.operations/catalog/04-data/ops-0034-qdrant/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0034-qdrant/guide.md
  preserved_semantics:
  - section:common-checks:fb79b28432d0
  - section:common-pitfalls:2098edf07cb4
  - section:overview:c68f2d5911b8
  - section:prerequisites:35d358cd81e3
  - section:purpose:cc4ac59a4241
  - section:qdrant-usage-guide:6aeb07064041
  - section:related-documents:bd7ce5726410
  - section:runbook-handoff:f2826849bcf2
  - section:step-by-step-instructions:0f607495f64b
  - section:target-audience:9abee23c6211
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 root compose에 active include된 `infra/04-data/specialized/qdrant/docker-compose.yml` 기준으로 Qdrant vector database의 사용 맥락과 일반 점검 방법을 설명한다.
    현재 구현은 `qdrant/qdrant:v1.18.1-unprivileged`, 단일 `qdrant` 서비스, `ai`/`data`/`dev` 프로파일, `infra_net`, REST route, gRPC TCP route, `/readyz` healthcheck를 사용한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0034-specialized-qdrant
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0034-specialized-qdrant/policy.md
  - docs/05.operations/04-data/ops-0034-specialized-qdrant/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/specialized/qdrant/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0034-qdrant/policy.md
  - docs/05.operations/catalog/04-data/ops-0034-qdrant/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/specialized/qdrant/README.md
- legacy_path: docs/05.operations/04-data/ops-0034-specialized-qdrant/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: f9e4ab314f349e1ada7e8cb360be37fa4943168e
  role: policy
  catalog_path: docs/05.operations/catalog/04-data/ops-0034-specialized-qdrant/policy.md
  final_path: docs/05.operations/catalog/04-data/ops-0034-qdrant/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0034-qdrant/policy.md
  preserved_semantics:
  - section:controls:d6ea609df6ef
  - section:exceptions:1c46a9a63e45
  - section:overview:59dc71df8e0d
  - section:policy-scope:b0a9cd19b1c6
  - section:qdrant-operations-policy:8121dc83d79b
  - section:related-documents:4b38c8b46eec
  - section:review-cadence:5fa9064a152b
  - section:verification:d4c5401adae9
  - 'text:baseline-body:**Required**: Documentation must describe Qdrant as a root-active single unprivileged service, not as a cluster.'
  removed_semantics:
  - stale:legacy-subject-path:ops-0034-specialized-qdrant
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0034-specialized-qdrant/guide.md
  - docs/05.operations/04-data/ops-0034-specialized-qdrant/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/specialized/qdrant/README.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0034-qdrant/guide.md
  - docs/05.operations/catalog/04-data/ops-0034-qdrant/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/specialized/qdrant/README.md
- legacy_path: docs/05.operations/04-data/ops-0034-specialized-qdrant/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 007018cd3a56ad793a73b2122feca09635ce1827
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0034-specialized-qdrant/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0034-qdrant/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0034-qdrant/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:75c7f3b87af8
  - section:canonical-references:1b4ed8457dd0
  - section:checklist:4e0c2d39eda8
  - section:escalation:f1aaec099920
  - section:evidence:6deaa178ff88
  - section:observability-and-evidence-sources:561631dd50b4
  - section:overview:1987c75c6839
  - section:procedure:5da93bd3e257
  - section:purpose:3c2ad2cf6392
  - section:qdrant-health-and-recovery-triage-procedure:58b8577d8a01
  - section:qdrant-health-and-recovery-triage-runbook:21f2630369a6
  - section:related-documents:11c7ee35f325
  - section:rollback-or-recovery:a23971f40244
  - section:safe-rollback-or-recovery-procedure:f26c1a0a8831
  - section:steps:0a91fb2cca52
  - section:verification-steps:a4fbe2350941
  - section:when-to-use:ce819c0a4e6d
  - text:baseline-body:`qdrant`가 unhealthy, stopped, or missing 상태일 때
  removed_semantics:
  - stale:legacy-subject-path:ops-0034-specialized-qdrant
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0034-specialized-qdrant/guide.md
  - docs/05.operations/04-data/ops-0034-specialized-qdrant/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/specialized/qdrant/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0034-qdrant/guide.md
  - docs/05.operations/catalog/04-data/ops-0034-qdrant/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/04-data/specialized/qdrant/README.md
- legacy_path: docs/05.operations/04-data/ops-0035-storage-storage-exhaustion/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d29a762a70c5f196f8d6555dd0300897089b180e
  role: runbook
  catalog_path: docs/05.operations/catalog/04-data/ops-0035-storage-storage-exhaustion/runbook.md
  final_path: docs/05.operations/catalog/04-data/ops-0035-storage-exhaustion/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/04-data/ops-0035-storage-exhaustion/runbook.md
  preserved_semantics:
  - section:04-data-storage-exhaustion-procedure:732b15841110
  - section:04-data-storage-exhaustion-runbook:fbf6dd086df8
  - section:agent-operations-if-applicable:99cf3563eedd
  - section:canonical-references:9c953dc92ae5
  - section:checklist:c40abb124667
  - section:escalation:0ba9d19dbf99
  - section:evidence:b14536787a2a
  - section:observability-and-evidence-sources:5440a4dba171
  - section:overview:635040650f75
  - section:procedure:5da93bd3e257
  - section:purpose:c31cfeab1524
  - section:related-documents:aec06512cbf1
  - section:rollback-or-recovery:35e2e7465088
  - section:safe-rollback-or-recovery-procedure:8173b125794f
  - section:steps:49774e70cf67
  - section:verification-steps:0acef34b814f
  - section:when-to-use:ff9d0c6a4ebc
  - text:baseline-body:데이터 서비스가 `No space left on device` 오류로 중단되거나 write operation이 실패할 때
  removed_semantics:
  - stale:legacy-subject-path:ops-0035-storage-storage-exhaustion
  active_consumers:
  - docs/05.operations/04-data/README.md
  - docs/05.operations/04-data/ops-0021-backup-backup-policy/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/05.operations/catalog/04-data/README.md
  - docs/05.operations/catalog/04-data/ops-0021-backup-and-restore/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/05-messaging/README.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 4217a7e2efd1671c3f2674953b212650f4c82d06
  role: domain-readme
  catalog_path: docs/05.operations/catalog/05-messaging/README.md
  final_path: docs/05.operations/catalog/05-messaging/README.md
  semantic_action: retain
  canonical_role_owner: null
  preserved_semantics:
  - section:audience:d76c2efde4a1
  - section:how-to-work-in-this-area:337b67e34061
  - section:operations-05-messaging:79bf5b0bceb6
  - section:overview:36d1aad85b9b
  - section:related-documents:2439de2a7e2f
  - section:scope:a1e7ba265630
  - section:structure:76e702f89a50
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/05-messaging/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
  final_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/05-messaging/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
- legacy_path: docs/05.operations/05-messaging/ops-0036-kafka/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 21ac38b1ab137de4c0adacce69e9a805f298af57
  role: guide
  catalog_path: docs/05.operations/catalog/05-messaging/ops-0036-kafka/guide.md
  final_path: docs/05.operations/catalog/05-messaging/ops-0036-kafka/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/05-messaging/ops-0036-kafka/guide.md
  preserved_semantics:
  - section:common-checks:7dc59cf510ed
  - section:common-pitfalls:098c98453c42
  - section:kafka-usage-guide:5448a16ccad8
  - section:overview:af37ef273000
  - section:prerequisites:4018cc67ce3d
  - section:purpose:25ff46d54d16
  - section:related-documents:8b259b0cf928
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:0a245d11bd05
  - section:target-audience:363b821b0b30
  - section:usage-type:c1852d6a7314
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/05-messaging/README.md
  - docs/05.operations/05-messaging/ops-0036-kafka/policy.md
  - docs/05.operations/05-messaging/ops-0036-kafka/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/05-messaging/README.md
  - infra/05-messaging/kafka/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/05-messaging/README.md
  - docs/05.operations/catalog/05-messaging/ops-0036-kafka/policy.md
  - docs/05.operations/catalog/05-messaging/ops-0036-kafka/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/05-messaging/README.md
  - infra/05-messaging/kafka/README.md
- legacy_path: docs/05.operations/05-messaging/ops-0036-kafka/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 3fea7d12795f5b36623e81d496a588362e85b0bf
  role: policy
  catalog_path: docs/05.operations/catalog/05-messaging/ops-0036-kafka/policy.md
  final_path: docs/05.operations/catalog/05-messaging/ops-0036-kafka/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/05-messaging/ops-0036-kafka/policy.md
  preserved_semantics:
  - section:ai-agent-policy-section:df72328571a5
  - section:controls:a033b1b1e3a9
  - section:exceptions:a9071e3915ba
  - section:kafka-operations-policy:7059aead5d82
  - section:overview:3fbf85e7aa28
  - section:policy-scope:67dd5fcbfd40
  - section:related-documents:b7726adff5a9
  - section:review-cadence:229924f1b393
  - section:verification:0c8c10ec7e04
  removed_semantics: []
  active_consumers:
  - docs/05.operations/05-messaging/README.md
  - docs/05.operations/05-messaging/ops-0036-kafka/guide.md
  - docs/05.operations/05-messaging/ops-0036-kafka/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/05-messaging/kafka/README.md
  final_consumers:
  - docs/05.operations/catalog/05-messaging/README.md
  - docs/05.operations/catalog/05-messaging/ops-0036-kafka/guide.md
  - docs/05.operations/catalog/05-messaging/ops-0036-kafka/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/05-messaging/kafka/README.md
- legacy_path: docs/05.operations/05-messaging/ops-0036-kafka/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: df4dbe0904cf4e48b01303f7cb86a16154ddd43e
  role: runbook
  catalog_path: docs/05.operations/catalog/05-messaging/ops-0036-kafka/runbook.md
  final_path: docs/05.operations/catalog/05-messaging/ops-0036-kafka/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/05-messaging/ops-0036-kafka/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:agent-operations:7d8d87a96a09
  - section:canonical-references:072a3b4fd0bf
  - section:checklist:6728b9e7d4b6
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:kafka-cluster-runbook:6606ac9d5bdb
  - section:kafka-recovery-maintenance-procedure-05-messaging:25265da5f979
  - section:observability-and-evidence-sources:15e4f75dc311
  - section:overview:df875ea778cb
  - section:procedure:5da93bd3e257
  - section:purpose:de6ef82dfadc
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:f32022b014d7
  - section:safe-rollback-or-recovery-procedure:8c7957459a89
  - section:steps:6614b6d81094
  - section:verification-steps:aa3ccf1c5971
  - section:when-to-use:51bde36655fb
  - text:baseline-body:broker health가 `unhealthy` 또는 `starting` 상태에 오래 머물 때
  removed_semantics:
  - stale:parallel-policy-label
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/05-messaging/README.md
  - docs/05.operations/05-messaging/ops-0036-kafka/guide.md
  - docs/05.operations/05-messaging/ops-0036-kafka/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/05-messaging/kafka/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/05-messaging/README.md
  - docs/05.operations/catalog/05-messaging/ops-0036-kafka/guide.md
  - docs/05.operations/catalog/05-messaging/ops-0036-kafka/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/05-messaging/kafka/README.md
- legacy_path: docs/05.operations/05-messaging/ops-0037-optimization-hardening/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: ed3f563087c6b005a86139cb82d1ad8f765c3d85
  role: guide
  catalog_path: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/guide.md
  final_path: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/guide.md
  preserved_semantics:
  - section:05-messaging-optimization-hardening-usage-guide:6584f0d8c2f5
  - section:common-checks:124197df8e16
  - section:common-pitfalls:d8dedf77c087
  - section:overview:746897a768a5
  - section:prerequisites:da95a1275a14
  - section:purpose:5a04f2ae91c7
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:754831c9dffc
  - section:target-audience:4cf4a88bbcca
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0017-messaging-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0020-messaging-optimization-hardening-architecture.md
  - docs/03.specs/spec-0006-messaging/spec.md
  - docs/05.operations/05-messaging/README.md
  - docs/05.operations/05-messaging/ops-0037-optimization-hardening/policy.md
  - docs/05.operations/05-messaging/ops-0037-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0017-messaging-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0020-messaging-optimization-hardening-architecture.md
  - docs/03.specs/spec-0006-messaging/spec.md
  - docs/05.operations/catalog/05-messaging/README.md
  - docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/policy.md
  - docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/05-messaging/ops-0037-optimization-hardening/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b5c3974760f08ac83ce81eb8b6284d2b3d9120d0
  role: policy
  catalog_path: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/policy.md
  final_path: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/policy.md
  preserved_semantics:
  - section:05-messaging-optimization-hardening-operations-policy:02fd6632259f
  - section:ai-agent-policy-section-if-applicable:1dc02a4380ba
  - section:catalog-expansion-approval-gates:1a749cc4c8cf
  - section:controls:87fa6d223268
  - section:exceptions:5ac7a83a712f
  - section:overview:3ca6182fc708
  - section:policy-scope:5ab95e70ef2c
  - section:related-documents:b7726adff5a9
  - section:review-cadence:9e5f51a52d8c
  - section:verification:6057a30f941e
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0017-messaging-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0020-messaging-optimization-hardening-architecture.md
  - docs/03.specs/spec-0006-messaging/spec.md
  - docs/05.operations/05-messaging/README.md
  - docs/05.operations/05-messaging/ops-0037-optimization-hardening/guide.md
  - docs/05.operations/05-messaging/ops-0037-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0017-messaging-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0020-messaging-optimization-hardening-architecture.md
  - docs/03.specs/spec-0006-messaging/spec.md
  - docs/05.operations/catalog/05-messaging/README.md
  - docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/guide.md
  - docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/05-messaging/ops-0037-optimization-hardening/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 3cd01e4d91eb311d8c83ec572d69ed29fbbf4925
  role: runbook
  catalog_path: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/runbook.md
  final_path: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/runbook.md
  preserved_semantics:
  - section:05-messaging-optimization-hardening-procedure:239e73cc9b71
  - section:05-messaging-optimization-hardening-runbook:74c4506dc1e9
  - section:agent-operations-if-applicable:e3d8589c4525
  - section:canonical-references:e74977e9fb40
  - section:checklist:c59313017679
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:observability-and-evidence-sources:f4afedb9c569
  - section:overview:8ef0403cc22d
  - section:procedure:5da93bd3e257
  - section:purpose:291297904c2e
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:a38893840438
  - section:safe-rollback-or-recovery-procedure:b23502b87f4c
  - section:steps:b4a63fcc5772
  - section:verification-steps:591d0242eca1
  - section:when-to-use:482b636cdd15
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0017-messaging-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0020-messaging-optimization-hardening-architecture.md
  - docs/03.specs/spec-0006-messaging/spec.md
  - docs/05.operations/05-messaging/README.md
  - docs/05.operations/05-messaging/ops-0037-optimization-hardening/guide.md
  - docs/05.operations/05-messaging/ops-0037-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0017-messaging-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0020-messaging-optimization-hardening-architecture.md
  - docs/03.specs/spec-0006-messaging/spec.md
  - docs/05.operations/catalog/05-messaging/README.md
  - docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/guide.md
  - docs/05.operations/catalog/05-messaging/ops-0037-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/05-messaging/ops-0038-rabbitmq/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 07a67d3d67fc350733937fa5ff182ae74482e7aa
  role: guide
  catalog_path: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/guide.md
  final_path: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/guide.md
  preserved_semantics:
  - section:1:31b1d085b8b3
  - section:2-management-ui:c755a72cbf18
  - section:3:95334e5b130c
  - section:4-python-pika:18f4f9a83f06
  - section:common-checks:56279a171b9a
  - section:common-pitfalls:3d7a569dfdf9
  - section:overview:26a183d8631f
  - section:prerequisites:f8994ff23568
  - section:purpose:477ee8ff6ec6
  - section:rabbitmq-usage-guide:3c1c9fd3dea1
  - section:related-documents:803dbdf99499
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:9c20e5ca273f
  - section:target-audience:b08fa52d7af2
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/05-messaging/README.md
  - docs/05.operations/05-messaging/ops-0038-rabbitmq/policy.md
  - docs/05.operations/05-messaging/ops-0038-rabbitmq/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/05-messaging/README.md
  - infra/05-messaging/rabbitmq/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/05-messaging/README.md
  - docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/policy.md
  - docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/05-messaging/README.md
  - infra/05-messaging/rabbitmq/README.md
- legacy_path: docs/05.operations/05-messaging/ops-0038-rabbitmq/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 14c84dbc3cfeb78cd82e8b10954c68345ac83bc9
  role: policy
  catalog_path: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/policy.md
  final_path: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/policy.md
  preserved_semantics:
  - section:controls:69b1da597fd3
  - section:exceptions:3e93186266b0
  - section:overview:86019af4c1d7
  - section:policy-scope:c9e75e6ed42a
  - section:rabbitmq-operations-policy:e75e4745c814
  - section:related-documents:b7726adff5a9
  - section:review-cadence:3d28bac958c2
  - section:verification:59475b888cc7
  removed_semantics: []
  active_consumers:
  - docs/05.operations/05-messaging/README.md
  - docs/05.operations/05-messaging/ops-0038-rabbitmq/guide.md
  - docs/05.operations/05-messaging/ops-0038-rabbitmq/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/05-messaging/rabbitmq/README.md
  final_consumers:
  - docs/05.operations/catalog/05-messaging/README.md
  - docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/guide.md
  - docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/05-messaging/rabbitmq/README.md
- legacy_path: docs/05.operations/05-messaging/ops-0038-rabbitmq/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d2a1e0d042db44efec6982c384e3996fdcbf50ba
  role: runbook
  catalog_path: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/runbook.md
  final_path: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:canonical-references:74b58ae63d45
  - section:checklist:78bf6cc8b487
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:observability-and-evidence-sources:14a6d7a51dc2
  - section:overview:2fa679cbc8a6
  - section:procedure:5da93bd3e257
  - section:purpose:0d7511ae6c42
  - section:rabbitmq-recovery-procedure:aafafb99431b
  - section:rabbitmq-runbook:4e2f712fa778
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:4b42c6217d22
  - section:safe-rollback-or-recovery-procedure:4e8ce93c828a
  - section:steps:d1b57b21be80
  - section:verification-steps:6efc4fa56b3b
  - section:when-to-use:5a17f2004870
  - 'text:baseline-body:"Message Backlog": 큐에 메시지가 수만 개 이상 쌓여 처리가 지연될 때.'
  removed_semantics:
  - stale:parallel-policy-label
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/05-messaging/README.md
  - docs/05.operations/05-messaging/ops-0038-rabbitmq/guide.md
  - docs/05.operations/05-messaging/ops-0038-rabbitmq/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/05-messaging/rabbitmq/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/05-messaging/README.md
  - docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/guide.md
  - docs/05.operations/catalog/05-messaging/ops-0038-rabbitmq/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/05-messaging/rabbitmq/README.md
- legacy_path: docs/05.operations/06-observability/README.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 7e67ed192fbd5f713c39fc3bb983ca3c18902874
  role: domain-readme
  catalog_path: docs/05.operations/catalog/06-observability/README.md
  final_path: docs/05.operations/catalog/06-observability/README.md
  semantic_action: retain
  canonical_role_owner: null
  preserved_semantics:
  - section:audience:20a8102f04d8
  - section:how-to-work-in-this-area:337b67e34061
  - section:operations-06-observability:056197476377
  - section:overview:ab305e4dbcc4
  - section:related-documents:e0bbbdfac753
  - section:scope:813c796c1092
  - section:structure:734aa6a608fa
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/06-observability/README.md
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.k8s.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.auth.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.datastores.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.gateway.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.infra.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.messaging.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.observability.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.prometheus.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.search.yml
  - infra/07-workflow/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
  - tests/validation/test_tech_stack_version_contract.py
  final_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/06-observability/README.md
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.k8s.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.auth.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.datastores.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.gateway.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.infra.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.messaging.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.observability.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.prometheus.yml
  - infra/06-observability/prometheus/config/alert_rules/alert_rules.local.search.yml
  - infra/07-workflow/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
  - tests/validation/test_tech_stack_version_contract.py
- legacy_path: docs/05.operations/06-observability/ops-0039-alertmanager/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: e70b389835b2eacbccc22fb1314da57c8b63d217
  role: guide
  catalog_path: docs/05.operations/catalog/06-observability/ops-0039-alertmanager/guide.md
  final_path: docs/05.operations/catalog/06-observability/ops-0039-alertmanager/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0039-alertmanager/guide.md
  preserved_semantics:
  - section:alertmanager-usage-guide:c512b8a41c28
  - section:common-checks:ea5006341728
  - section:common-pitfalls:480cdf72431c
  - section:overview:68dce7d7661b
  - section:prerequisites:a8614b00243f
  - section:purpose:48763a21d644
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:b738aea13358
  - section:target-audience:ca0be8dac2f4
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0039-alertmanager/policy.md
  - docs/05.operations/06-observability/ops-0039-alertmanager/runbook.md
  - docs/05.operations/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/alertmanager/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0039-alertmanager/policy.md
  - docs/05.operations/catalog/06-observability/ops-0039-alertmanager/runbook.md
  - docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/alertmanager/README.md
- legacy_path: docs/05.operations/06-observability/ops-0039-alertmanager/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b0302f4f90bffb38982370111e35208ed00aa3e7
  role: policy
  catalog_path: docs/05.operations/catalog/06-observability/ops-0039-alertmanager/policy.md
  final_path: docs/05.operations/catalog/06-observability/ops-0039-alertmanager/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0039-alertmanager/policy.md
  preserved_semantics:
  - section:alertmanager-operations-policy:969f44783eb0
  - section:controls:1f6df7cd8e16
  - section:exceptions:816111ea031e
  - section:overview:c932a14b2439
  - section:policy-scope:9f52b1967968
  - section:related-documents:b7726adff5a9
  - section:review-cadence:e65ee84b3791
  - section:verification:52d8af1035c0
  removed_semantics: []
  active_consumers:
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0039-alertmanager/guide.md
  - docs/05.operations/06-observability/ops-0039-alertmanager/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/alertmanager/README.md
  final_consumers:
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0039-alertmanager/guide.md
  - docs/05.operations/catalog/06-observability/ops-0039-alertmanager/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/alertmanager/README.md
- legacy_path: docs/05.operations/06-observability/ops-0039-alertmanager/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 0156cdb38feb180b96d468b35dd483d1309a9f71
  role: runbook
  catalog_path: docs/05.operations/catalog/06-observability/ops-0039-alertmanager/runbook.md
  final_path: docs/05.operations/catalog/06-observability/ops-0039-alertmanager/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0039-alertmanager/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:alertmanager-notification-recovery-procedure:52c90c6177c7
  - section:alertmanager-notification-recovery-runbook:b372660ea266
  - section:canonical-references:bcc7a3bc4f5e
  - section:checklist:b4d99d2841b5
  - section:escalation:798128d0dfd2
  - section:evidence:79ead1d6d6f6
  - section:observability-and-evidence-sources:500e61449032
  - section:overview:08191ecf4b69
  - section:procedure:5da93bd3e257
  - section:purpose:d730e5fdc5d1
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:8b39f89ebab7
  - section:safe-rollback-or-recovery-procedure:7437c504d34b
  - section:steps:22721b0c08f3
  - section:verification-steps:ff975ccd7420
  - section:when-to-use:3f259a56a364
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0039-alertmanager/guide.md
  - docs/05.operations/06-observability/ops-0039-alertmanager/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/alertmanager/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0039-alertmanager/guide.md
  - docs/05.operations/catalog/06-observability/ops-0039-alertmanager/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/alertmanager/README.md
- legacy_path: docs/05.operations/06-observability/ops-0040-alloy/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 7699709479d1aaf44864782f119871f883ba4f7a
  role: guide
  catalog_path: docs/05.operations/catalog/06-observability/ops-0040-alloy/guide.md
  final_path: docs/05.operations/catalog/06-observability/ops-0040-alloy/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0040-alloy/guide.md
  preserved_semantics:
  - section:alloy-usage-guide:6650760c5ec1
  - section:common-checks:bf755a651cec
  - section:common-pitfalls:3682e26561bc
  - section:overview:f525ee4d2012
  - section:prerequisites:d167f4b2261d
  - section:purpose:009e93fe59cb
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:e5244d3d7615
  - section:target-audience:ca0be8dac2f4
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0040-alloy/policy.md
  - docs/05.operations/06-observability/ops-0040-alloy/runbook.md
  - docs/05.operations/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/06-observability/ops-0047-pyroscope/guide.md
  - docs/05.operations/06-observability/ops-0049-tempo/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/README.md
  - infra/06-observability/alloy/README.md
  final_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0040-alloy/policy.md
  - docs/05.operations/catalog/06-observability/ops-0040-alloy/runbook.md
  - docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/catalog/06-observability/ops-0047-pyroscope/guide.md
  - docs/05.operations/catalog/06-observability/ops-0049-tempo/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/README.md
  - infra/06-observability/alloy/README.md
- legacy_path: docs/05.operations/06-observability/ops-0040-alloy/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 029f0989ccfc0aba1aac42133b8ba3a7f18bd984
  role: policy
  catalog_path: docs/05.operations/catalog/06-observability/ops-0040-alloy/policy.md
  final_path: docs/05.operations/catalog/06-observability/ops-0040-alloy/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0040-alloy/policy.md
  preserved_semantics:
  - section:alloy-operations-policy:121f7a261553
  - section:controls:e2a6b541cccf
  - section:exceptions:1c7d3acec641
  - section:overview:231aa0a80a5a
  - section:policy-scope:061fb703ae90
  - section:related-documents:b7726adff5a9
  - section:review-cadence:ba235d9de2d4
  - section:verification:69941cdc878b
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0040-alloy/guide.md
  - docs/05.operations/06-observability/ops-0040-alloy/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/alloy/README.md
  final_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0040-alloy/guide.md
  - docs/05.operations/catalog/06-observability/ops-0040-alloy/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/alloy/README.md
- legacy_path: docs/05.operations/06-observability/ops-0040-alloy/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 1562a52857bac311e09be8c6d3d2cadd12b713b5
  role: runbook
  catalog_path: docs/05.operations/catalog/06-observability/ops-0040-alloy/runbook.md
  final_path: docs/05.operations/catalog/06-observability/ops-0040-alloy/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0040-alloy/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:alloy-readiness-and-pipeline-recovery-procedure:aa2b359c8f7b
  - section:alloy-readiness-and-pipeline-recovery-runbook:1c71ee62bc95
  - section:canonical-references:ac1e873066be
  - section:checklist:0366525afd3b
  - section:escalation:d6eed7bc6b6a
  - section:evidence:a40de2ce862e
  - section:observability-and-evidence-sources:a2e023597662
  - section:overview:e98944b09824
  - section:procedure:5da93bd3e257
  - section:purpose:d8f6bf52cf22
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:61d75fb62faa
  - section:safe-rollback-or-recovery-procedure:a99aad7aef04
  - section:steps:116463f6918b
  - section:verification-steps:200fef2728fb
  - section:when-to-use:04a125804234
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0040-alloy/guide.md
  - docs/05.operations/06-observability/ops-0040-alloy/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/alloy/README.md
  final_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0040-alloy/guide.md
  - docs/05.operations/catalog/06-observability/ops-0040-alloy/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/alloy/README.md
- legacy_path: docs/05.operations/06-observability/ops-0041-grafana/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 95f77069d9e7e9db9114b97248e3aa03eeb8660a
  role: guide
  catalog_path: docs/05.operations/catalog/06-observability/ops-0041-grafana/guide.md
  final_path: docs/05.operations/catalog/06-observability/ops-0041-grafana/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0041-grafana/guide.md
  preserved_semantics:
  - section:common-checks:96af51c96819
  - section:common-pitfalls:5e25db9ca520
  - section:grafana-usage-guide:2cbedfead5f8
  - section:overview:dec5d5fa2f07
  - section:prerequisites:488d8feac26d
  - section:purpose:4c4cf41a9fa9
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:13f6900e0fd6
  - section:target-audience:ca0be8dac2f4
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0041-grafana/policy.md
  - docs/05.operations/06-observability/ops-0041-grafana/runbook.md
  - docs/05.operations/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/06-observability/ops-0047-pyroscope/guide.md
  - docs/05.operations/06-observability/ops-0049-tempo/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/grafana/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0041-grafana/policy.md
  - docs/05.operations/catalog/06-observability/ops-0041-grafana/runbook.md
  - docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/catalog/06-observability/ops-0047-pyroscope/guide.md
  - docs/05.operations/catalog/06-observability/ops-0049-tempo/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/grafana/README.md
- legacy_path: docs/05.operations/06-observability/ops-0041-grafana/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 94feb1feef9a25e67f3ebea900332f10d0d8a6e8
  role: policy
  catalog_path: docs/05.operations/catalog/06-observability/ops-0041-grafana/policy.md
  final_path: docs/05.operations/catalog/06-observability/ops-0041-grafana/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0041-grafana/policy.md
  preserved_semantics:
  - section:controls:1bf773a372b0
  - section:exceptions:c2c4596bf6ce
  - section:grafana-operations-policy:04271882bae5
  - section:overview:27030089217e
  - section:policy-scope:930fd460827b
  - section:related-documents:b7726adff5a9
  - section:review-cadence:32c1f3073934
  - section:verification:f52eede2da23
  removed_semantics: []
  active_consumers:
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0041-grafana/guide.md
  - docs/05.operations/06-observability/ops-0041-grafana/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/grafana/README.md
  final_consumers:
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0041-grafana/guide.md
  - docs/05.operations/catalog/06-observability/ops-0041-grafana/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/grafana/README.md
- legacy_path: docs/05.operations/06-observability/ops-0041-grafana/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 3992e3f7765e8e2b82f032d61b71dd380dc13888
  role: runbook
  catalog_path: docs/05.operations/catalog/06-observability/ops-0041-grafana/runbook.md
  final_path: docs/05.operations/catalog/06-observability/ops-0041-grafana/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0041-grafana/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:canonical-references:561c31d7d612
  - section:checklist:52e4d5c6fd77
  - section:escalation:0d4292e286ca
  - section:evidence:c79cf0ff5260
  - section:grafana-provisioning-and-access-recovery-procedure:6abb68a08776
  - section:grafana-provisioning-and-access-recovery-runbook:03f401024358
  - section:observability-and-evidence-sources:4e8ff564bd36
  - section:overview:835e1ebed14d
  - section:procedure:5da93bd3e257
  - section:purpose:f7bfc15eace6
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:fbcc55024d71
  - section:safe-rollback-or-recovery-procedure:891d238aec54
  - section:steps:b4694af5dd16
  - section:verification-steps:5827701f87b8
  - section:when-to-use:7a9c98024a33
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0041-grafana/guide.md
  - docs/05.operations/06-observability/ops-0041-grafana/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/grafana/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0041-grafana/guide.md
  - docs/05.operations/catalog/06-observability/ops-0041-grafana/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/grafana/README.md
- legacy_path: docs/05.operations/06-observability/ops-0042-lgtm-stack/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 5505c46af7b799e45dfbaaace2ac9f2cb1b0bd5c
  role: guide
  catalog_path: docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack/guide.md
  final_path: docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack/guide.md
  preserved_semantics:
  - section:common-checks:1f5c44a34a55
  - section:common-pitfalls:df79cbd5265a
  - section:lgtm-stack-usage-guide:b59a5c8ab155
  - section:overview:edb210c0c69e
  - section:prerequisites:758706614739
  - section:purpose:04c64477fb5a
  - section:related-documents:325bb6748b94
  - section:runbook-handoff:e9f159d1c4af
  - section:step-by-step-instructions:64de11b4d172
  - section:target-audience:ca0be8dac2f4
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/06-observability/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/README.md
  final_consumers:
  - docs/05.operations/catalog/06-observability/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/README.md
- legacy_path: docs/05.operations/06-observability/ops-0043-loki/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 139d0372974f9c819326e7f062915d51eb3034be
  role: guide
  catalog_path: docs/05.operations/catalog/06-observability/ops-0043-loki/guide.md
  final_path: docs/05.operations/catalog/06-observability/ops-0043-loki/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0043-loki/guide.md
  preserved_semantics:
  - section:common-checks:e7a177925b1f
  - section:common-pitfalls:5038735fb911
  - section:loki-usage-guide:8230bfd3d58f
  - section:overview:652cc73061b5
  - section:prerequisites:fdd36db29c2c
  - section:purpose:99146bffafca
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:cdd7b0f1dc09
  - section:target-audience:ca0be8dac2f4
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/06-observability/ops-0043-loki/policy.md
  - docs/05.operations/06-observability/ops-0043-loki/runbook.md
  - docs/05.operations/06-observability/ops-0048-retention/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/loki/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/catalog/06-observability/ops-0043-loki/policy.md
  - docs/05.operations/catalog/06-observability/ops-0043-loki/runbook.md
  - docs/05.operations/catalog/06-observability/ops-0048-telemetry-retention/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/loki/README.md
- legacy_path: docs/05.operations/06-observability/ops-0043-loki/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b4281b55e9ceef79021ac5a50d3925946b7dfc97
  role: policy
  catalog_path: docs/05.operations/catalog/06-observability/ops-0043-loki/policy.md
  final_path: docs/05.operations/catalog/06-observability/ops-0043-loki/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0043-loki/policy.md
  preserved_semantics:
  - section:controls:2ef5cc8f185f
  - section:exceptions:a0cefced2181
  - section:loki-operations-policy:80f6ea451c79
  - section:overview:a377833821f1
  - section:policy-scope:c8d920df5e38
  - section:related-documents:ab0f2087e5a8
  - section:review-cadence:28b839a6aa52
  - section:verification:599bba53a311
  - text:baseline-body:Loki storage는 MinIO S3 backend와 `loki-bucket`을 사용한다.
  removed_semantics:
  - stale:stage-04-execution-route
  active_consumers:
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0043-loki/guide.md
  - docs/05.operations/06-observability/ops-0043-loki/runbook.md
  - docs/05.operations/06-observability/ops-0048-retention/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/loki/README.md
  final_consumers:
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0043-loki/guide.md
  - docs/05.operations/catalog/06-observability/ops-0043-loki/runbook.md
  - docs/05.operations/catalog/06-observability/ops-0048-telemetry-retention/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/loki/README.md
- legacy_path: docs/05.operations/06-observability/ops-0043-loki/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 73f9916fc6f5b6c64ed2a0563330633aa78e7a58
  role: runbook
  catalog_path: docs/05.operations/catalog/06-observability/ops-0043-loki/runbook.md
  final_path: docs/05.operations/catalog/06-observability/ops-0043-loki/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0043-loki/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:canonical-references:4b11157576d4
  - section:checklist:26eaabb88998
  - section:escalation:a9b2d2c7befc
  - section:evidence:f5a1fa515ca5
  - section:loki-readiness-and-storage-recovery-procedure:f52727525a4f
  - section:loki-readiness-and-storage-recovery-runbook:3db47b4686b7
  - section:observability-and-evidence-sources:de8b525ad63b
  - section:overview:f558a98cd723
  - section:procedure:5da93bd3e257
  - section:purpose:173cba745d4e
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:cc96ac8e535e
  - section:safe-rollback-or-recovery-procedure:dcdba82e0420
  - section:steps:61ad04973612
  - section:verification-steps:008bed296e50
  - section:when-to-use:dd8b962a897a
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0043-loki/guide.md
  - docs/05.operations/06-observability/ops-0043-loki/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/loki/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0043-loki/guide.md
  - docs/05.operations/catalog/06-observability/ops-0043-loki/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/loki/README.md
- legacy_path: docs/05.operations/06-observability/ops-0044-optimization-hardening/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 0818296bfdd0bd52ca56e97b0eddd2c7cbcef3bc
  role: guide
  catalog_path: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/guide.md
  final_path: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/guide.md
  preserved_semantics:
  - section:06-observability-optimization-hardening-usage-guide:0a3941cb6985
  - section:common-checks:f61dd5b14fa4
  - section:common-pitfalls:af1395afc7e9
  - section:overview:c4a56f3da96b
  - section:prerequisites:032e1cef490c
  - section:purpose:2ac5e802fabe
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:76a0797e9a33
  - section:target-audience:21e1658fe25d
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0018-observability-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0021-observability-optimization-hardening-architecture.md
  - docs/03.specs/spec-0007-observability/spec.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0044-optimization-hardening/policy.md
  - docs/05.operations/06-observability/ops-0044-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0018-observability-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0021-observability-optimization-hardening-architecture.md
  - docs/03.specs/spec-0007-observability/spec.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/policy.md
  - docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/06-observability/ops-0044-optimization-hardening/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 9c7d7b5a85c5d4e801e2c397c19b225c9cb0b49b
  role: policy
  catalog_path: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/policy.md
  final_path: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/policy.md
  preserved_semantics:
  - section:catalog-expansion-approval-gates:7e2fd86a8e90
  - section:controls:80c058205e3e
  - section:exceptions:21a9e5b5102b
  - section:observability-optimization-hardening-policy:44c28bef6c0c
  - section:overview:0984d41f65ff
  - section:policy-scope:fd5b772ffdbf
  - section:related-documents:ab0f2087e5a8
  - section:review-cadence:d273aea1e528
  - section:verification:908d0afefbc1
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0018-observability-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0021-observability-optimization-hardening-architecture.md
  - docs/03.specs/spec-0007-observability/spec.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0044-optimization-hardening/guide.md
  - docs/05.operations/06-observability/ops-0044-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0018-observability-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0021-observability-optimization-hardening-architecture.md
  - docs/03.specs/spec-0007-observability/spec.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/guide.md
  - docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/06-observability/ops-0044-optimization-hardening/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 3d091c93034ea1ce8d339a58d942ccb1225dc2b2
  role: runbook
  catalog_path: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/runbook.md
  final_path: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/runbook.md
  preserved_semantics:
  - section:06-observability-optimization-hardening-procedure:6f40ee27803d
  - section:06-observability-optimization-hardening-runbook:13fbd0abcd91
  - section:agent-operations-if-applicable:0e839e8a53a3
  - section:canonical-references:1e58b85fdd8b
  - section:checklist:2f299a448ac3
  - section:escalation:65d1b9bb1b9d
  - section:evidence:7a1b0d0017ff
  - section:observability-and-evidence-sources:a14e8930c542
  - section:overview:79a7c9363e29
  - section:procedure:5da93bd3e257
  - section:purpose:090e9658902b
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:ec96a75d4a73
  - section:safe-rollback-or-recovery-procedure:cacf76d89151
  - section:steps:edeab6e7d1e0
  - section:verification-steps:0ebbd5190ab6
  - section:when-to-use:4c235b842888
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0018-observability-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0021-observability-optimization-hardening-architecture.md
  - docs/03.specs/spec-0007-observability/spec.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0044-optimization-hardening/guide.md
  - docs/05.operations/06-observability/ops-0044-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0018-observability-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0021-observability-optimization-hardening-architecture.md
  - docs/03.specs/spec-0007-observability/spec.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/guide.md
  - docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/06-observability/ops-0045-prometheus/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 6ce65e760d5df3e9ae916cf02b7fd5e32afd8c4a
  role: guide
  catalog_path: docs/05.operations/catalog/06-observability/ops-0045-prometheus/guide.md
  final_path: docs/05.operations/catalog/06-observability/ops-0045-prometheus/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0045-prometheus/guide.md
  preserved_semantics:
  - section:1-scrape-configurations:db76eb02b3ea
  - section:2-alerting-rule-system:bb58af055aff
  - section:3-storage-tsdb:711f4b9e6e35
  - section:alertmanager-integration:701aa01024b0
  - section:architecture:634ac39c6bab
  - section:common-checks:80c220c7b909
  - section:common-pitfalls:b05dba1bbf21
  - section:grafana-datasource:482dd9ee955e
  - section:integration-patterns:a4381dafb74f
  - section:key-components:312886950bc6
  - section:keycloak-observation:8d1778775934
  - section:overview:e50fdcc9e703
  - section:prerequisites:e7b096a62a5f
  - section:prometheus-usage-guide:504509cf8ade
  - section:purpose:316381b0afac
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:f464eaa0ac6c
  - section:target-audience:682ca9239150
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/06-observability/ops-0045-prometheus/policy.md
  - docs/05.operations/06-observability/ops-0045-prometheus/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/prometheus/README.md
  final_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/catalog/06-observability/ops-0045-prometheus/policy.md
  - docs/05.operations/catalog/06-observability/ops-0045-prometheus/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/prometheus/README.md
- legacy_path: docs/05.operations/06-observability/ops-0045-prometheus/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 136ddcbcf3bd0f559aa43fca04fe83107d27cf9c
  role: policy
  catalog_path: docs/05.operations/catalog/06-observability/ops-0045-prometheus/policy.md
  final_path: docs/05.operations/catalog/06-observability/ops-0045-prometheus/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0045-prometheus/policy.md
  preserved_semantics:
  - section:controls:ab6e10853a8c
  - section:exceptions:d13568c94f08
  - section:overview:26601f8d7a47
  - section:policy-scope:6b31394716b2
  - section:prometheus-operations-policy:89303ad0b87d
  - section:related-documents:ab0f2087e5a8
  - section:review-cadence:494b5c6cdb4a
  - section:verification:94d7c828fa1b
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0045-prometheus/guide.md
  - docs/05.operations/06-observability/ops-0045-prometheus/runbook.md
  - docs/05.operations/06-observability/ops-0048-retention/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/prometheus/README.md
  final_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0045-prometheus/guide.md
  - docs/05.operations/catalog/06-observability/ops-0045-prometheus/runbook.md
  - docs/05.operations/catalog/06-observability/ops-0048-telemetry-retention/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/prometheus/README.md
- legacy_path: docs/05.operations/06-observability/ops-0045-prometheus/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: a0001b737a8874b45f87270e72c03813f56bcd1b
  role: runbook
  catalog_path: docs/05.operations/catalog/06-observability/ops-0045-prometheus/runbook.md
  final_path: docs/05.operations/catalog/06-observability/ops-0045-prometheus/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0045-prometheus/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:canonical-references:1eb996699d6d
  - section:checklist:954a2ad25748
  - section:escalation:d15e3358cb68
  - section:evidence:43539ffb7c94
  - section:observability-and-evidence-sources:de3835fd0387
  - section:overview:308ac03ed43e
  - section:procedure:5da93bd3e257
  - section:prometheus-readiness-and-recovery-procedure:cf07beb305a4
  - section:prometheus-readiness-and-recovery-runbook:54f32821ac10
  - section:purpose:e9925be0e17e
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:0bf5c37ae6f8
  - section:safe-rollback-or-recovery-procedure:587f95d0bf21
  - section:steps:a23bb712dbd4
  - section:verification-steps:f126033c71d3
  - section:when-to-use:996b95dcbd24
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0045-prometheus/guide.md
  - docs/05.operations/06-observability/ops-0045-prometheus/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/prometheus/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0045-prometheus/guide.md
  - docs/05.operations/catalog/06-observability/ops-0045-prometheus/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/prometheus/README.md
- legacy_path: docs/05.operations/06-observability/ops-0046-pushgateway/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 7f42cfa85293a3b2b9d96f9f147a918fbce0404c
  role: guide
  catalog_path: docs/05.operations/catalog/06-observability/ops-0046-pushgateway/guide.md
  final_path: docs/05.operations/catalog/06-observability/ops-0046-pushgateway/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0046-pushgateway/guide.md
  preserved_semantics:
  - section:1:5358076cb050
  - section:2:794651f5ffbd
  - section:3-prometheus-scrape:1c2e72c129c9
  - section:4:5d94c0d32a1d
  - section:common-checks:c96b0f4bd1e4
  - section:common-pitfalls:57bcc914e9fe
  - section:help-batch-process-items-total-items-processed-by-batch:899c50282b63
  - section:overview:acc352f1e196
  - section:prerequisites:271046a569c2
  - section:purpose:e34d9e35287a
  - section:pushgateway-usage-guide:d2241954db53
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:9c20e5ca273f
  - section:target-audience:5bd8940e51d5
  - section:type-batch-process-items-counter:a0539b4b91e4
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/06-observability/ops-0046-pushgateway/policy.md
  - docs/05.operations/06-observability/ops-0046-pushgateway/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/pushgateway/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/catalog/06-observability/ops-0046-pushgateway/policy.md
  - docs/05.operations/catalog/06-observability/ops-0046-pushgateway/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/pushgateway/README.md
- legacy_path: docs/05.operations/06-observability/ops-0046-pushgateway/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d649ecff51f0aa8794695cb701cac0ac996d4811
  role: policy
  catalog_path: docs/05.operations/catalog/06-observability/ops-0046-pushgateway/policy.md
  final_path: docs/05.operations/catalog/06-observability/ops-0046-pushgateway/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0046-pushgateway/policy.md
  preserved_semantics:
  - section:controls:c3ca4aa5ecbd
  - section:exceptions:5588f315cd7c
  - section:overview:71d3b723403c
  - section:policy-scope:b6cfd31786e3
  - section:pushgateway-operations-policy:ee6680436f57
  - section:related-documents:b7726adff5a9
  - section:review-cadence:9c168b1bb2fe
  - section:verification:38f1e85d6f78
  removed_semantics: []
  active_consumers:
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0046-pushgateway/guide.md
  - docs/05.operations/06-observability/ops-0046-pushgateway/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/pushgateway/README.md
  final_consumers:
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0046-pushgateway/guide.md
  - docs/05.operations/catalog/06-observability/ops-0046-pushgateway/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/pushgateway/README.md
- legacy_path: docs/05.operations/06-observability/ops-0046-pushgateway/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d14307d8944b63078da6bedd672d7e875282d5e9
  role: runbook
  catalog_path: docs/05.operations/catalog/06-observability/ops-0046-pushgateway/runbook.md
  final_path: docs/05.operations/catalog/06-observability/ops-0046-pushgateway/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0046-pushgateway/runbook.md
  preserved_semantics:
  - section:canonical-references:5ac2f6ca3cdc
  - section:checklist:587dd066b353
  - section:escalation:1faf4dc04d85
  - section:evidence:d486ae50e356
  - section:observability-and-evidence-sources:395777edc2cd
  - section:overview:c0eaaeaf0294
  - section:procedure:5da93bd3e257
  - section:purpose:420f7195c305
  - section:pushgateway-metrics-buffer-recovery-procedure:17323afd9b28
  - section:pushgateway-metrics-buffer-recovery-runbook:3c74490e63a6
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:f609f0b1b982
  - section:safe-rollback-or-recovery-procedure:8add5a24c857
  - section:steps:41040f9b6494
  - section:verification-steps:1d9fa3ff894a
  - section:when-to-use:f1ea9ab9987d
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0046-pushgateway/guide.md
  - docs/05.operations/06-observability/ops-0046-pushgateway/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/pushgateway/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0046-pushgateway/guide.md
  - docs/05.operations/catalog/06-observability/ops-0046-pushgateway/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/pushgateway/README.md
- legacy_path: docs/05.operations/06-observability/ops-0047-pyroscope/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d3dbdafd24121c292df53e76fd63d3dbdcadb4d3
  role: guide
  catalog_path: docs/05.operations/catalog/06-observability/ops-0047-pyroscope/guide.md
  final_path: docs/05.operations/catalog/06-observability/ops-0047-pyroscope/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0047-pyroscope/guide.md
  preserved_semantics:
  - section:common-checks:17a447489d79
  - section:common-pitfalls:66adbc1254b9
  - section:overview:bedaea0e45b9
  - section:prerequisites:c86c08d25f22
  - section:purpose:dece30b29ef9
  - section:pyroscope-usage-guide:41a0c2217488
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:287b9501817a
  - section:target-audience:9e4d422119d4
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/06-observability/ops-0047-pyroscope/policy.md
  - docs/05.operations/06-observability/ops-0047-pyroscope/runbook.md
  - docs/05.operations/06-observability/ops-0048-retention/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/pyroscope/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/catalog/06-observability/ops-0047-pyroscope/policy.md
  - docs/05.operations/catalog/06-observability/ops-0047-pyroscope/runbook.md
  - docs/05.operations/catalog/06-observability/ops-0048-telemetry-retention/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/pyroscope/README.md
- legacy_path: docs/05.operations/06-observability/ops-0047-pyroscope/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: cce88527e471a341222c1eba1ce5d0003dbee169
  role: policy
  catalog_path: docs/05.operations/catalog/06-observability/ops-0047-pyroscope/policy.md
  final_path: docs/05.operations/catalog/06-observability/ops-0047-pyroscope/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0047-pyroscope/policy.md
  preserved_semantics:
  - section:controls:476d436ea5a7
  - section:exceptions:89333ee402d6
  - section:overview:9c6e4f4d3f2d
  - section:policy-scope:92bb94a9295d
  - section:pyroscope-operations-policy:4ce862dac2c0
  - section:related-documents:ab0f2087e5a8
  - section:review-cadence:edec14387085
  - section:verification:64d8ef2bef00
  removed_semantics: []
  active_consumers:
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0047-pyroscope/guide.md
  - docs/05.operations/06-observability/ops-0047-pyroscope/runbook.md
  - docs/05.operations/06-observability/ops-0048-retention/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/pyroscope/README.md
  final_consumers:
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0047-pyroscope/guide.md
  - docs/05.operations/catalog/06-observability/ops-0047-pyroscope/runbook.md
  - docs/05.operations/catalog/06-observability/ops-0048-telemetry-retention/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/pyroscope/README.md
- legacy_path: docs/05.operations/06-observability/ops-0047-pyroscope/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 238b6ac1e62016b5d5c8a0fba467e1ab13f202ba
  role: runbook
  catalog_path: docs/05.operations/catalog/06-observability/ops-0047-pyroscope/runbook.md
  final_path: docs/05.operations/catalog/06-observability/ops-0047-pyroscope/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0047-pyroscope/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:canonical-references:2b4244eaec06
  - section:checklist:9d51d48affbe
  - section:escalation:8490c96987a7
  - section:evidence:427583fee0b2
  - section:observability-and-evidence-sources:6b1c7f45d7c1
  - section:overview:0de37aedbb42
  - section:procedure:5da93bd3e257
  - section:purpose:8577a8f14d3c
  - section:pyroscope-readiness-and-recovery-procedure:c882fcd4ae28
  - section:pyroscope-readiness-and-recovery-runbook:0def33623c09
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:829dc2254c93
  - section:safe-rollback-or-recovery-procedure:1aaed2ef75cd
  - section:steps:e466e2768f6c
  - section:verification-steps:27255e1ec96c
  - section:when-to-use:6c759ea4ef11
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0047-pyroscope/guide.md
  - docs/05.operations/06-observability/ops-0047-pyroscope/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/pyroscope/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0047-pyroscope/guide.md
  - docs/05.operations/catalog/06-observability/ops-0047-pyroscope/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/pyroscope/README.md
- legacy_path: docs/05.operations/06-observability/ops-0048-retention/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: e81e0265b7c1f1516a11f150e5ab79708d275972
  role: policy
  catalog_path: docs/05.operations/catalog/06-observability/ops-0048-retention/policy.md
  final_path: docs/05.operations/catalog/06-observability/ops-0048-telemetry-retention/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0048-telemetry-retention/policy.md
  preserved_semantics:
  - section:controls:b1110f25cdea
  - section:exceptions:c969b9b14902
  - section:overview:5410e503a2aa
  - section:policy-scope:3a9b63337365
  - section:related-documents:790361e1d283
  - section:retention-and-performance-policies:70666d280e25
  - section:review-cadence:c84cd58158bd
  - section:verification:8e2fb4f243ed
  - text:baseline-body:Prometheus metrics는 local TSDB와 Prometheus policy의 retention/volume
  removed_semantics:
  - stale:legacy-subject-path:ops-0048-retention
  active_consumers:
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0043-loki/policy.md
  - docs/05.operations/06-observability/ops-0044-optimization-hardening/policy.md
  - docs/05.operations/06-observability/ops-0045-prometheus/policy.md
  - docs/05.operations/06-observability/ops-0047-pyroscope/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0043-loki/policy.md
  - docs/05.operations/catalog/06-observability/ops-0044-optimization-hardening/policy.md
  - docs/05.operations/catalog/06-observability/ops-0045-prometheus/policy.md
  - docs/05.operations/catalog/06-observability/ops-0047-pyroscope/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/06-observability/ops-0049-tempo/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: fe7e6292116656f865abeae220b4dddbef2df341
  role: guide
  catalog_path: docs/05.operations/catalog/06-observability/ops-0049-tempo/guide.md
  final_path: docs/05.operations/catalog/06-observability/ops-0049-tempo/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0049-tempo/guide.md
  preserved_semantics:
  - section:common-checks:c113385d45c8
  - section:common-pitfalls:057561897db6
  - section:overview:b72d108e6172
  - section:prerequisites:650a2661f44f
  - section:purpose:e4b96b233a17
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:990299a18001
  - section:target-audience:578140b77cc0
  - section:tempo-usage-guide:8a4b3c0f53ad
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/06-observability/ops-0049-tempo/policy.md
  - docs/05.operations/06-observability/ops-0049-tempo/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/tempo/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0042-lgtm-stack/guide.md
  - docs/05.operations/catalog/06-observability/ops-0049-tempo/policy.md
  - docs/05.operations/catalog/06-observability/ops-0049-tempo/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/tempo/README.md
- legacy_path: docs/05.operations/06-observability/ops-0049-tempo/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 1f5ce783f5611dedf1df3f8dc1267971a966bfbf
  role: policy
  catalog_path: docs/05.operations/catalog/06-observability/ops-0049-tempo/policy.md
  final_path: docs/05.operations/catalog/06-observability/ops-0049-tempo/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0049-tempo/policy.md
  preserved_semantics:
  - section:controls:1c4ed7159b66
  - section:exceptions:13ab28cdb6d5
  - section:overview:10fe3be1cf45
  - section:policy-scope:cefc0bfc6267
  - section:related-documents:b7726adff5a9
  - section:review-cadence:dc4b0a4ab3a5
  - section:tempo-operations-policy:b0200f759a40
  - section:verification:50d16cc7fc0a
  removed_semantics: []
  active_consumers:
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0048-retention/policy.md
  - docs/05.operations/06-observability/ops-0049-tempo/guide.md
  - docs/05.operations/06-observability/ops-0049-tempo/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/tempo/README.md
  final_consumers:
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0048-telemetry-retention/policy.md
  - docs/05.operations/catalog/06-observability/ops-0049-tempo/guide.md
  - docs/05.operations/catalog/06-observability/ops-0049-tempo/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/tempo/README.md
- legacy_path: docs/05.operations/06-observability/ops-0049-tempo/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 393f8fb6d1496dff9c121a60fb0e4114bfbffef8
  role: runbook
  catalog_path: docs/05.operations/catalog/06-observability/ops-0049-tempo/runbook.md
  final_path: docs/05.operations/catalog/06-observability/ops-0049-tempo/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/06-observability/ops-0049-tempo/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:canonical-references:51602cfb5c81
  - section:checklist:dacf052f314e
  - section:escalation:68277ac71599
  - section:evidence:d601b91b1d29
  - section:observability-and-evidence-sources:ced26cea18dd
  - section:overview:a2d8438f4e7e
  - section:procedure:5da93bd3e257
  - section:purpose:f9b4bc5fcf11
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:c7c742a3d2d8
  - section:safe-rollback-or-recovery-procedure:ef62689a630c
  - section:steps:5189092886bb
  - section:tempo-readiness-and-recovery-procedure:4f8200874ed3
  - section:tempo-readiness-and-recovery-runbook:195afa0c28ba
  - section:verification-steps:c5a13e9bab76
  - section:when-to-use:ff4e18dade6f
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/06-observability/README.md
  - docs/05.operations/06-observability/ops-0048-retention/policy.md
  - docs/05.operations/06-observability/ops-0049-tempo/guide.md
  - docs/05.operations/06-observability/ops-0049-tempo/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/tempo/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/06-observability/README.md
  - docs/05.operations/catalog/06-observability/ops-0048-telemetry-retention/policy.md
  - docs/05.operations/catalog/06-observability/ops-0049-tempo/guide.md
  - docs/05.operations/catalog/06-observability/ops-0049-tempo/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/06-observability/tempo/README.md
- legacy_path: docs/05.operations/07-workflow/README.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 4fa148c3211d2916e05e61f2b7ae7594fd18f737
  role: domain-readme
  catalog_path: docs/05.operations/catalog/07-workflow/README.md
  final_path: docs/05.operations/catalog/07-workflow/README.md
  semantic_action: retain
  canonical_role_owner: null
  preserved_semantics:
  - section:audience:6737cba13c69
  - section:how-to-work-in-this-area:337b67e34061
  - section:operations-07-workflow:1322e8bd8aef
  - section:overview:6baf4e72fd6b
  - section:related-documents:a9de645d676c
  - section:scope:3ae98b35e707
  - section:structure:f4a8f7da6417
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/07-workflow/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
  final_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/07-workflow/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
- legacy_path: docs/05.operations/07-workflow/ops-0050-airflow/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: cc8e0e3dacd6b9191c4e10fc552ed1c74e637e66
  role: guide
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0050-airflow/guide.md
  final_path: docs/05.operations/catalog/07-workflow/ops-0050-airflow/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/07-workflow/ops-0050-airflow/guide.md
  preserved_semantics:
  - section:1:accf060f2b5f
  - section:2-ui:0da16ade90f2
  - section:3:e4d857bfb488
  - section:airflow-usage-guide:68232e0d16a1
  - section:common-checks:7d9c261ced3b
  - section:common-pitfalls:4440548b889c
  - section:common-pitfalls:d44786157825
  - section:dag:a5c0fedb3529
  - section:overview:6db46bbe63ce
  - section:prerequisites:4f9a313c9dc3
  - section:purpose:e6a2d452c533
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:9c20e5ca273f
  - section:target-audience:e08c54cd166b
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  - section:workflow-root-compose-static-validation:7f94beb21c78
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0008-workflow.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/07-workflow/README.md
  - docs/05.operations/07-workflow/ops-0050-airflow/policy.md
  - docs/05.operations/07-workflow/ops-0050-airflow/runbook.md
  - docs/05.operations/07-workflow/ops-0051-airflow-dag-basics/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/airflow/README.md
  final_consumers:
  - docs/01.requirements/prd-0008-workflow.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/07-workflow/README.md
  - docs/05.operations/catalog/07-workflow/ops-0050-airflow/policy.md
  - docs/05.operations/catalog/07-workflow/ops-0050-airflow/runbook.md
  - docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/airflow/README.md
- legacy_path: docs/05.operations/07-workflow/ops-0050-airflow/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 25879d7e3ff0b76f355542a7c5c21fd5cd2d81c7
  role: policy
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0050-airflow/policy.md
  final_path: docs/05.operations/catalog/07-workflow/ops-0050-airflow/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/07-workflow/ops-0050-airflow/policy.md
  preserved_semantics:
  - section:airflow-operations-policy:5e7b457f1a0e
  - section:controls:897e8bab9987
  - section:exceptions:5df8fbdebb4e
  - section:overview:1dc09a0c5e7d
  - section:policy-scope:b73652f7aae9
  - section:related-documents:b7726adff5a9
  - section:review-cadence:f05174bf6489
  - section:verification:5bace4ae5f0b
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0008-workflow.md
  - docs/05.operations/07-workflow/README.md
  - docs/05.operations/07-workflow/ops-0050-airflow/guide.md
  - docs/05.operations/07-workflow/ops-0050-airflow/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/airflow/README.md
  final_consumers:
  - docs/01.requirements/prd-0008-workflow.md
  - docs/05.operations/catalog/07-workflow/README.md
  - docs/05.operations/catalog/07-workflow/ops-0050-airflow/guide.md
  - docs/05.operations/catalog/07-workflow/ops-0050-airflow/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/airflow/README.md
- legacy_path: docs/05.operations/07-workflow/ops-0050-airflow/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b1e4f8997037df5f6a50bba74f884af51d2724ea
  role: runbook
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0050-airflow/runbook.md
  final_path: docs/05.operations/catalog/07-workflow/ops-0050-airflow/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/07-workflow/ops-0050-airflow/runbook.md
  preserved_semantics:
  - section:1-task-stuck-in-queued:bb2a5de40c80
  - section:2-db:4a093a0fbf03
  - section:3:105cd1020a0c
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:airflow-recovery-procedure:f09f2fc3ec9c
  - section:airflow-runbook:594438a60945
  - section:canonical-references:257570a62246
  - section:checklist:16b9ce7703d8
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:observability-and-evidence-sources:d6dcc3191fdb
  - section:overview:af02a48d336b
  - section:procedure:5da93bd3e257
  - section:purpose:dfe34c7f231b
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:8f5400c3c766
  - section:steps:a0d2dd907944
  - section:verification-steps:555944b7da94
  - section:when-to-use:c9dea4535bc6
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0008-workflow.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/07-workflow/README.md
  - docs/05.operations/07-workflow/ops-0050-airflow/guide.md
  - docs/05.operations/07-workflow/ops-0050-airflow/policy.md
  - docs/05.operations/07-workflow/ops-0051-airflow-dag-basics/guide.md
  - docs/05.operations/07-workflow/ops-0052-dag-deployment/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/airflow/README.md
  final_consumers:
  - docs/01.requirements/prd-0008-workflow.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/07-workflow/README.md
  - docs/05.operations/catalog/07-workflow/ops-0050-airflow/guide.md
  - docs/05.operations/catalog/07-workflow/ops-0050-airflow/policy.md
  - docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle/guide.md
  - docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/airflow/README.md
- legacy_path: docs/05.operations/07-workflow/ops-0051-airflow-dag-basics/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 932c72d30b427bc70e12b92c50acb83ce088b309
  role: guide
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-basics/guide.md
  final_path: docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle/guide.md
  preserved_semantics:
  - section:1-dag-definition-pattern:3c1e5e3934f2
  - section:2-file-placement:9c90e8352d45
  - section:airflow-dag-basics-operations:9f1252f6ff6c
  - section:airflow-dag-basics-usage:520e8cd02c56
  - section:common-checks:8233383538aa
  - section:common-pitfalls:35d720584e73
  - section:overview:9f32d12d36ae
  - section:prerequisites:292c2516d0e2
  - section:purpose:25c6dc396044
  - section:related-documents:9745d5337275
  - section:runbook-handoff:364a2499eda1
  - section:step-by-step-instructions:7a3b95dc4bed
  - section:target-audience:3384a0fd8b00
  - section:usage-type:4200e5f9457b
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 `hy-home.docker` 환경에서 Airflow DAG를 작성하는 기본 방법과 권장 패턴을 설명합니다. 현재 compose는 DAG 파일을 repo 내부 Airflow 하위 경로가 아니라 `${DEFAULT_WORKFLOW_DIR}/airflow/dags`에서
    bind mount합니다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0051-airflow-dag-basics
  active_consumers:
  - docs/05.operations/07-workflow/README.md
  - docs/05.operations/07-workflow/ops-0052-dag-deployment/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/README.md
  - infra/07-workflow/airflow/README.md
  - tests/validation/test_script_manifest.py
  final_consumers:
  - docs/05.operations/catalog/07-workflow/README.md
  - docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/README.md
  - infra/07-workflow/airflow/README.md
  - tests/validation/test_script_manifest.py
- legacy_path: docs/05.operations/07-workflow/ops-0052-dag-deployment/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 2ef693b98a0cd0ff7fd9aba08adf2163bb486063
  role: policy
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0052-dag-deployment/policy.md
  final_path: docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle/policy.md
  semantic_action: merge
  canonical_role_owner: docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle/policy.md
  preserved_semantics:
  - section:controls:ac8dfc123590
  - section:dag-deployment-operations-policy:0881e0fbec39
  - section:exceptions:df3af92d469d
  - section:overview:56615cb9b737
  - section:policy-scope:b21627993a52
  - section:related-documents:345966a07c33
  - section:review-cadence:07e4c9f7604f
  - section:verification:449218f5c88f
  - text:airflow-dag-lint-control:All DAGs must pass `ruff` or `flake8` linting.
  - text:airflow-dag-secret-control:Hardcoded credentials (use Airflow Connections).
  removed_semantics:
  - duplicate:airflow-dag-validation-and-recovery-handoff
  active_consumers:
  - docs/05.operations/07-workflow/README.md
  - docs/05.operations/07-workflow/ops-0051-airflow-dag-basics/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/05.operations/catalog/07-workflow/README.md
  - docs/05.operations/catalog/07-workflow/ops-0051-airflow-dag-lifecycle/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/07-workflow/ops-0053-n8n/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 4b049909baeeb6a05013df7fefc1b6ac4c0ed747
  role: guide
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0053-n8n/guide.md
  final_path: docs/05.operations/catalog/07-workflow/ops-0053-n8n/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/07-workflow/ops-0053-n8n/guide.md
  preserved_semantics:
  - section:1-architecture-and-components:e7a318d30c98
  - section:2-access-and-integration:6b5398334d6f
  - section:3-workflow-authoring-and-activation:9a732f025177
  - section:4-credential-and-secret-boundary:e632674d481e
  - section:5-custom-node-extension:2c970a7df1cb
  - section:6-development-and-verification:8462dbcb1d25
  - section:common-checks:bbdaa4dd4b19
  - section:common-pitfalls:94dea7ef1993
  - section:n8n-usage-guide:854fe31dd948
  - section:overview:657dc79482a0
  - section:prerequisites:8cc2dac301d0
  - section:purpose:5ce9a9ef39d4
  - section:related-documents:723579e3249a
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:9c20e5ca273f
  - section:target-audience:86cb2f76a705
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0008-workflow.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/07-workflow/README.md
  - docs/05.operations/07-workflow/ops-0053-n8n/policy.md
  - docs/05.operations/07-workflow/ops-0053-n8n/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/README.md
  - infra/07-workflow/n8n/README.md
  final_consumers:
  - docs/01.requirements/prd-0008-workflow.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/07-workflow/README.md
  - docs/05.operations/catalog/07-workflow/ops-0053-n8n/policy.md
  - docs/05.operations/catalog/07-workflow/ops-0053-n8n/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/README.md
  - infra/07-workflow/n8n/README.md
- legacy_path: docs/05.operations/07-workflow/ops-0053-n8n/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: ab3575abf67ff620cde12b28049884fa2b841878
  role: policy
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0053-n8n/policy.md
  final_path: docs/05.operations/catalog/07-workflow/ops-0053-n8n/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/07-workflow/ops-0053-n8n/policy.md
  preserved_semantics:
  - section:controls:81aee359b560
  - section:exceptions:4e37e6f37046
  - section:n8n-operations-policy:dfea2c58efaf
  - section:overview:e0e9256581a4
  - section:policy-scope:86f3dbf5605a
  - section:related-documents:b7726adff5a9
  - section:review-cadence:8268b6138f53
  - section:verification:798564203150
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0008-workflow.md
  - docs/05.operations/07-workflow/README.md
  - docs/05.operations/07-workflow/ops-0053-n8n/guide.md
  - docs/05.operations/07-workflow/ops-0053-n8n/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/n8n/README.md
  final_consumers:
  - docs/01.requirements/prd-0008-workflow.md
  - docs/05.operations/catalog/07-workflow/README.md
  - docs/05.operations/catalog/07-workflow/ops-0053-n8n/guide.md
  - docs/05.operations/catalog/07-workflow/ops-0053-n8n/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/n8n/README.md
- legacy_path: docs/05.operations/07-workflow/ops-0053-n8n/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b81e798d988bf8166ff844c0bd2437da7258a778
  role: runbook
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0053-n8n/runbook.md
  final_path: docs/05.operations/catalog/07-workflow/ops-0053-n8n/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/07-workflow/ops-0053-n8n/runbook.md
  preserved_semantics:
  - section:1-worker-down:152e6a8d0fae
  - section:2:93bafbebfd9c
  - section:3-task-runner:111a04f45ce4
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:canonical-references:76b1247ba7ff
  - section:checklist:7262d3989785
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:n8n-recovery-procedure:5f1fbd176d8c
  - section:n8n-runbook:29648d101910
  - section:observability-and-evidence-sources:bda635c9ad09
  - section:overview:88a7b3a5c8f1
  - section:procedure:5da93bd3e257
  - section:purpose:4a0a0dabaee8
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:a8eabd2e3538
  - section:steps:a0d2dd907944
  - section:verification-steps:e37016cb74aa
  - section:when-to-use:f66b2a0192fc
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0008-workflow.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/07-workflow/README.md
  - docs/05.operations/07-workflow/ops-0053-n8n/guide.md
  - docs/05.operations/07-workflow/ops-0053-n8n/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/n8n/README.md
  final_consumers:
  - docs/01.requirements/prd-0008-workflow.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/07-workflow/README.md
  - docs/05.operations/catalog/07-workflow/ops-0053-n8n/guide.md
  - docs/05.operations/catalog/07-workflow/ops-0053-n8n/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/07-workflow/n8n/README.md
- legacy_path: docs/05.operations/07-workflow/ops-0054-optimization-hardening/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: e07e2af4fc6ee786d410c069977bab1e503d4c47
  role: guide
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/guide.md
  final_path: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/guide.md
  preserved_semantics:
  - section:07-workflow-optimization-hardening-usage-guide:dee902615dec
  - section:common-checks:1591745729c8
  - section:common-pitfalls:d9b603f6028e
  - section:overview:c93b7ce61f2b
  - section:prerequisites:9da6340d0c49
  - section:purpose:dc927f95587b
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:cc604cda7ae2
  - section:target-audience:42dd3527cb2b
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0019-workflow-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0022-workflow-optimization-hardening-architecture.md
  - docs/03.specs/spec-0008-workflow/spec.md
  - docs/05.operations/07-workflow/README.md
  - docs/05.operations/07-workflow/ops-0054-optimization-hardening/policy.md
  - docs/05.operations/07-workflow/ops-0054-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0019-workflow-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0022-workflow-optimization-hardening-architecture.md
  - docs/03.specs/spec-0008-workflow/spec.md
  - docs/05.operations/catalog/07-workflow/README.md
  - docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/policy.md
  - docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/07-workflow/ops-0054-optimization-hardening/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: f79807b7c611dfed83fcb7a18c7ba4aebca789d0
  role: policy
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/policy.md
  final_path: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/policy.md
  preserved_semantics:
  - section:07-workflow-optimization-hardening-operations-policy:e348b660ea3a
  - section:catalog-expansion-approval-gates:a6af44af11c1
  - section:controls:6f03906df031
  - section:exceptions:06fa74146d80
  - section:overview:fbb1df41e66b
  - section:policy-scope:6f0cb1db07a1
  - section:related-documents:b7726adff5a9
  - section:review-cadence:80295002652d
  - section:verification:04d466baeb27
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0019-workflow-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0022-workflow-optimization-hardening-architecture.md
  - docs/03.specs/spec-0008-workflow/spec.md
  - docs/05.operations/07-workflow/README.md
  - docs/05.operations/07-workflow/ops-0054-optimization-hardening/guide.md
  - docs/05.operations/07-workflow/ops-0054-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0019-workflow-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0022-workflow-optimization-hardening-architecture.md
  - docs/03.specs/spec-0008-workflow/spec.md
  - docs/05.operations/catalog/07-workflow/README.md
  - docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/guide.md
  - docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/07-workflow/ops-0054-optimization-hardening/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 11fdd4277e2f49baa4a34e1c7970fe949c3abd14
  role: runbook
  catalog_path: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/runbook.md
  final_path: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/runbook.md
  preserved_semantics:
  - section:07-workflow-optimization-hardening-procedure:8dcf2ea9962a
  - section:07-workflow-optimization-hardening-runbook:a54ba5a92dea
  - section:agent-operations-if-applicable:974fe3b8a8d5
  - section:canonical-references:be1ff53ed022
  - section:checklist:d93b28e4f77d
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:observability-and-evidence-sources:042ad71e89eb
  - section:overview:0e23bd7b9948
  - section:procedure:5da93bd3e257
  - section:purpose:38ad14754053
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:c33205b3b756
  - section:steps:f91bf51e09e8
  - section:verification-steps:a5e4bd61b144
  - section:when-to-use:55f000ab713b
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0019-workflow-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0022-workflow-optimization-hardening-architecture.md
  - docs/03.specs/spec-0008-workflow/spec.md
  - docs/05.operations/07-workflow/README.md
  - docs/05.operations/07-workflow/ops-0054-optimization-hardening/guide.md
  - docs/05.operations/07-workflow/ops-0054-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0019-workflow-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0022-workflow-optimization-hardening-architecture.md
  - docs/03.specs/spec-0008-workflow/spec.md
  - docs/05.operations/catalog/07-workflow/README.md
  - docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/guide.md
  - docs/05.operations/catalog/07-workflow/ops-0054-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/08-ai/README.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 3a85c8af98e1d75150edb1e1fed28024556aa553
  role: domain-readme
  catalog_path: docs/05.operations/catalog/08-ai/README.md
  final_path: docs/05.operations/catalog/08-ai/README.md
  semantic_action: retain
  canonical_role_owner: null
  preserved_semantics:
  - section:audience:d15b1a36c252
  - section:how-to-work-in-this-area:337b67e34061
  - section:operations-08-ai:e16ab803a6b7
  - section:overview:ae25293de39b
  - section:related-documents:8d9aa5b8ffb5
  - section:scope:27295ba98835
  - section:structure:9565c73617a5
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/08-ai/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
  - tests/validation/test_tech_stack_version_contract.py
  final_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/08-ai/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
  - tests/validation/test_tech_stack_version_contract.py
- legacy_path: docs/05.operations/08-ai/ops-0055-gpu-recovery/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: c2adb1aa9f9ff9882306857b2206fc62aae233c8
  role: runbook
  catalog_path: docs/05.operations/catalog/08-ai/ops-0055-gpu-recovery/runbook.md
  final_path: docs/05.operations/catalog/08-ai/ops-0055-gpu-recovery/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/08-ai/ops-0055-gpu-recovery/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:188b8d9b7e46
  - section:ai-gpu-recovery-procedure:83abbe4e8942
  - section:ai-gpu-recovery-runbook:9d5cc7400037
  - section:canonical-references:13b7f72770ed
  - section:checklist:1a0906c0f198
  - section:escalation:25efa37b431d
  - section:evidence:473fbed583e1
  - section:observability-and-evidence-sources:622a1a0b1b0e
  - section:overview:a5ddd36fb3be
  - section:procedure:5da93bd3e257
  - section:purpose:edaa26ae0bc8
  - section:related-documents:df10b4cae73c
  - section:rollback-or-recovery:ce5ec6011b66
  - section:safe-rollback-or-recovery-procedure:94512732aa1c
  - section:steps:21e651bd21fc
  - section:verification-steps:8f74181c8cb9
  - section:when-to-use:a9afcc69746b
  - text:baseline-body:Ollama 로그에 GPU driver load failure 또는 CPU-only fallback이 나타난다.
  removed_semantics:
  - stale:parallel-role-labels
  active_consumers:
  - docs/05.operations/08-ai/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/05.operations/catalog/08-ai/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/08-ai/ops-0056-ollama/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: c9f18b1f8835a7947ba71a74b32b21fdaf39a325
  role: guide
  catalog_path: docs/05.operations/catalog/08-ai/ops-0056-ollama/guide.md
  final_path: docs/05.operations/catalog/08-ai/ops-0056-ollama/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/08-ai/ops-0056-ollama/guide.md
  preserved_semantics:
  - section:1-service-gpu-health-check:4cc018e4db4e
  - section:2-model-lifecycle-cli:65716a31b64b
  - section:3-inference-api-check:74b6640da91d
  - section:4-open-webui-integration-check:35a061227438
  - section:5-exporter-observability-check:23d9ae139500
  - section::1c851a4dbce6
  - section::2ef1f2f54119
  - section:common-checks:74025399c672
  - section:common-pitfalls:6353f404b622
  - section:exporter-exposes-metrics-inside-infra-net-it-is-not-published-to-host:5a34f88513a1
  - section:gpu:ce70a2451bc2
  - section:gpu:dda03cbce9d3
  - section:ollama-api-health-via-host-port:77a384d962eb
  - section:ollama-usage-guide:3250e44a1a3e
  - section:overview:9da658fb923c
  - section:prerequisites:a7d1e54deb50
  - section:purpose:0dae1ea6d7b1
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:9c20e5ca273f
  - section:target-audience:fa7f489cd7c2
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/08-ai/README.md
  - docs/05.operations/08-ai/ops-0055-gpu-recovery/runbook.md
  - docs/05.operations/08-ai/ops-0056-ollama/policy.md
  - docs/05.operations/08-ai/ops-0056-ollama/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/README.md
  - infra/08-ai/ollama/README.md
  - tests/validation/test_script_manifest.py
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/08-ai/README.md
  - docs/05.operations/catalog/08-ai/ops-0055-gpu-recovery/runbook.md
  - docs/05.operations/catalog/08-ai/ops-0056-ollama/policy.md
  - docs/05.operations/catalog/08-ai/ops-0056-ollama/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/README.md
  - infra/08-ai/ollama/README.md
  - tests/validation/test_script_manifest.py
- legacy_path: docs/05.operations/08-ai/ops-0056-ollama/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 66366aab7588ed53a69db853ef89e7ff79b3c382
  role: policy
  catalog_path: docs/05.operations/catalog/08-ai/ops-0056-ollama/policy.md
  final_path: docs/05.operations/catalog/08-ai/ops-0056-ollama/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/08-ai/ops-0056-ollama/policy.md
  preserved_semantics:
  - section:controls:527fbb859788
  - section:exceptions:6d2399ffba2e
  - section:ollama-operations-policy:814701caa09d
  - section:overview:0890e1a0e291
  - section:policy-scope:8fc09d321f93
  - section:related-documents:b7726adff5a9
  - section:review-cadence:3290500acce8
  - section:verification:a187d2738a41
  removed_semantics: []
  active_consumers:
  - docs/05.operations/08-ai/README.md
  - docs/05.operations/08-ai/ops-0055-gpu-recovery/runbook.md
  - docs/05.operations/08-ai/ops-0056-ollama/guide.md
  - docs/05.operations/08-ai/ops-0056-ollama/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/ollama/README.md
  final_consumers:
  - docs/05.operations/catalog/08-ai/README.md
  - docs/05.operations/catalog/08-ai/ops-0055-gpu-recovery/runbook.md
  - docs/05.operations/catalog/08-ai/ops-0056-ollama/guide.md
  - docs/05.operations/catalog/08-ai/ops-0056-ollama/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/ollama/README.md
- legacy_path: docs/05.operations/08-ai/ops-0056-ollama/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 3b995d2476d18afd0d9d26bc15642ec4718fab92
  role: runbook
  catalog_path: docs/05.operations/catalog/08-ai/ops-0056-ollama/runbook.md
  final_path: docs/05.operations/catalog/08-ai/ops-0056-ollama/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/08-ai/ops-0056-ollama/runbook.md
  preserved_semantics:
  - section:1-initial-health-api-check:eb14c992535b
  - section:2-gpu-recognition-recovery:3bcf099de6c3
  - section:3-vram-oom-mitigation:cf3ede61f915
  - section:4-model-integrity-check:48f2e0bb68c5
  - section:5-open-webui-dependency-recheck:2a5f2a614f48
  - section::5143d90ce512
  - section:agent-operations-if-applicable:c82af396f795
  - section:canonical-references:f0128c9b9d2a
  - section:checklist:ae4df9b2f72d
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:gpu:1ddc6b34cbe0
  - section:gpu:b15a11f385c5
  - section:keep-alive-0:3f19d2a72427
  - section:observability-and-evidence-sources:799349b5ac0f
  - section:ollama-maintenance-recovery-procedure:b89b330fff2c
  - section:ollama-runbook:5fc1b5d5709f
  - section:open-webui-ollama:991114151f11
  - section:overview:3ee80bed6bf6
  - section:procedure:5da93bd3e257
  - section:purpose:bc8f5d5f134c
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:8a0c1fb7a0e5
  - section:steps:a0d2dd907944
  - section:verification-steps:e93e10e4041f
  - section:when-to-use:500f60baf4cd
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/08-ai/README.md
  - docs/05.operations/08-ai/ops-0055-gpu-recovery/runbook.md
  - docs/05.operations/08-ai/ops-0056-ollama/guide.md
  - docs/05.operations/08-ai/ops-0056-ollama/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/ollama/README.md
  - scripts/validation/check-repo-contracts.sh
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/08-ai/README.md
  - docs/05.operations/catalog/08-ai/ops-0055-gpu-recovery/runbook.md
  - docs/05.operations/catalog/08-ai/ops-0056-ollama/guide.md
  - docs/05.operations/catalog/08-ai/ops-0056-ollama/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/ollama/README.md
  - scripts/validation/check-repo-contracts.sh
- legacy_path: docs/05.operations/08-ai/ops-0057-open-webui/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: e973d9c4ecffa5697e6beb867c1d1e2b4542b86d
  role: guide
  catalog_path: docs/05.operations/catalog/08-ai/ops-0057-open-webui/guide.md
  final_path: docs/05.operations/catalog/08-ai/ops-0057-open-webui/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/08-ai/ops-0057-open-webui/guide.md
  preserved_semantics:
  - section:1-access-authentication:b950fe0e10ed
  - section:2-model-selection-chat:845427532381
  - section:3-rag-document-indexing:d038ef194368
  - section:4-quick-connectivity-checks:7fbe8c8b3b3e
  - section:5-advanced-settings:afe27726a86a
  - section:common-checks:507b734a5bb0
  - section:common-pitfalls:7e62f81cd4ef
  - section:open-webui-health-is-internal-unless-a-host-port-is-explicitly-published:2aa881b517a7
  - section:open-webui-ollama-connectivity:3d16eeff42ef
  - section:open-webui-qdrant-connectivity:77cbfa5e68d6
  - section:open-webui-usage-guide:71039e690ba7
  - section:overview:191d7d00d6bb
  - section:prerequisites:b0d27c0d0cf2
  - section:purpose:647ce0762e29
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:9c20e5ca273f
  - section:target-audience:c07b6d5acf25
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/08-ai/README.md
  - docs/05.operations/08-ai/ops-0057-open-webui/policy.md
  - docs/05.operations/08-ai/ops-0057-open-webui/runbook.md
  - docs/05.operations/08-ai/ops-0059-rag-workflow/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/README.md
  - infra/08-ai/open-webui/README.md
  final_consumers:
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/08-ai/README.md
  - docs/05.operations/catalog/08-ai/ops-0057-open-webui/policy.md
  - docs/05.operations/catalog/08-ai/ops-0057-open-webui/runbook.md
  - docs/05.operations/catalog/08-ai/ops-0059-rag-workflow/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/README.md
  - infra/08-ai/open-webui/README.md
- legacy_path: docs/05.operations/08-ai/ops-0057-open-webui/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b64359a293381ca079f86c2eb791ede4b5863fad
  role: policy
  catalog_path: docs/05.operations/catalog/08-ai/ops-0057-open-webui/policy.md
  final_path: docs/05.operations/catalog/08-ai/ops-0057-open-webui/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/08-ai/ops-0057-open-webui/policy.md
  preserved_semantics:
  - section:controls:bd3f427ec265
  - section:exceptions:d70800cbab3e
  - section:open-webui-operations-policy:c0840f4216d8
  - section:overview:e07adaa2cfed
  - section:policy-scope:2844f1d21c8f
  - section:related-documents:b7726adff5a9
  - section:review-cadence:945eab4c9c47
  - section:verification:fd6e1897d0be
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/05.operations/08-ai/README.md
  - docs/05.operations/08-ai/ops-0057-open-webui/guide.md
  - docs/05.operations/08-ai/ops-0057-open-webui/runbook.md
  - docs/05.operations/08-ai/ops-0059-rag-workflow/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/open-webui/README.md
  final_consumers:
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/05.operations/catalog/08-ai/README.md
  - docs/05.operations/catalog/08-ai/ops-0057-open-webui/guide.md
  - docs/05.operations/catalog/08-ai/ops-0057-open-webui/runbook.md
  - docs/05.operations/catalog/08-ai/ops-0059-rag-workflow/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/open-webui/README.md
- legacy_path: docs/05.operations/08-ai/ops-0057-open-webui/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: f1dea9c6d8f5a4b36a4ee0b1deeb082f38033d94
  role: runbook
  catalog_path: docs/05.operations/catalog/08-ai/ops-0057-open-webui/runbook.md
  final_path: docs/05.operations/catalog/08-ai/ops-0057-open-webui/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/08-ai/ops-0057-open-webui/runbook.md
  preserved_semantics:
  - section:1-initial-triage:ece4e63605a9
  - section:1:1ec045b3e7e8
  - section:2-dependency-connectivity-check:19c0c217840c
  - section:2:411f0833d088
  - section:3-sqlite-backup-and-recovery:d11999d89eb6
  - section:4-rag-index-re-sync:ebfcfcc351f5
  - section:5-service-restart-path:e55be95a79a7
  - section:agent-operations-if-applicable:4deb18fa12c0
  - section:canonical-references:6e79a7217229
  - section:checklist:79aad5837e53
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:observability-and-evidence-sources:e97375abde50
  - section:open-webui-maintenance-recovery-procedure:f26362059195
  - section:open-webui-ollama:f5aaf219fb7c
  - section:open-webui-qdrant:03f38ea9d322
  - section:open-webui-runbook:68b51bfa47b9
  - section:overview:eefb317997ef
  - section:procedure:5da93bd3e257
  - section:purpose:a8eb4ef79ed2
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:92b2c2b6250f
  - section:steps:a0d2dd907944
  - section:verification-steps:9ce0e5a59369
  - section:when-to-use:0a4a52bde4e8
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/08-ai/README.md
  - docs/05.operations/08-ai/ops-0057-open-webui/guide.md
  - docs/05.operations/08-ai/ops-0057-open-webui/policy.md
  - docs/05.operations/08-ai/ops-0059-rag-workflow/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/open-webui/README.md
  - scripts/validation/check-repo-contracts.sh
  final_consumers:
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/08-ai/README.md
  - docs/05.operations/catalog/08-ai/ops-0057-open-webui/guide.md
  - docs/05.operations/catalog/08-ai/ops-0057-open-webui/policy.md
  - docs/05.operations/catalog/08-ai/ops-0059-rag-workflow/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/open-webui/README.md
  - scripts/validation/check-repo-contracts.sh
- legacy_path: docs/05.operations/08-ai/ops-0058-optimization-hardening/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b97b250e6605986ce088a089b8ea33de3bb4aed1
  role: guide
  catalog_path: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/guide.md
  final_path: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/guide.md
  preserved_semantics:
  - section:08-ai-optimization-hardening-usage-guide:7717aa01b3b5
  - section:common-checks:c38771e5c13e
  - section:common-pitfalls:83e7f4df67d5
  - section:overview:0733057ecc66
  - section:prerequisites:d17bbc3c3323
  - section:purpose:d7c7489d4797
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:6da940acaa13
  - section:target-audience:0ba171d314b6
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0020-ai-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0023-ai-optimization-hardening-architecture.md
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/05.operations/08-ai/README.md
  - docs/05.operations/08-ai/ops-0058-optimization-hardening/policy.md
  - docs/05.operations/08-ai/ops-0058-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0020-ai-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0023-ai-optimization-hardening-architecture.md
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/05.operations/catalog/08-ai/README.md
  - docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/policy.md
  - docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/08-ai/ops-0058-optimization-hardening/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 4d8f918bfa71d86dbc267e17aa325efd7c974593
  role: policy
  catalog_path: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/policy.md
  final_path: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/policy.md
  preserved_semantics:
  - section:08-ai-optimization-hardening-operations-policy:6d238d124671
  - section:catalog-expansion-approval-gates:a930d3912ed7
  - section:controls:045f93ffe7f7
  - section:exceptions:2d610d189d0e
  - section:overview:21615649b8e2
  - section:policy-scope:49098da2e51c
  - section:related-documents:b7726adff5a9
  - section:review-cadence:3c60f7fc884a
  - section:verification:c8c8029fa462
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0020-ai-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0023-ai-optimization-hardening-architecture.md
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/05.operations/08-ai/README.md
  - docs/05.operations/08-ai/ops-0058-optimization-hardening/guide.md
  - docs/05.operations/08-ai/ops-0058-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0020-ai-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0023-ai-optimization-hardening-architecture.md
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/05.operations/catalog/08-ai/README.md
  - docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/guide.md
  - docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/08-ai/ops-0058-optimization-hardening/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 147ba00617294bb1b1e554b83e30fb795ada9ccb
  role: runbook
  catalog_path: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/runbook.md
  final_path: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/runbook.md
  preserved_semantics:
  - section:08-ai-optimization-hardening-procedure:9d734798a4c2
  - section:08-ai-optimization-hardening-runbook:95e5ca259891
  - section:agent-operations-if-applicable:9366335099ca
  - section:canonical-references:7b2fd6dc9483
  - section:checklist:8b7410ac4519
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:observability-and-evidence-sources:f758474d7380
  - section:overview:fbc415971d7b
  - section:procedure:5da93bd3e257
  - section:purpose:144c57514d04
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:d0a3b0e23111
  - section:steps:651ae3be330b
  - section:verification-steps:c8570f14e514
  - section:when-to-use:7256c2375ac9
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0020-ai-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0023-ai-optimization-hardening-architecture.md
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/05.operations/08-ai/README.md
  - docs/05.operations/08-ai/ops-0058-optimization-hardening/guide.md
  - docs/05.operations/08-ai/ops-0058-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0020-ai-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0023-ai-optimization-hardening-architecture.md
  - docs/03.specs/spec-0009-ai/spec.md
  - docs/05.operations/catalog/08-ai/README.md
  - docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/guide.md
  - docs/05.operations/catalog/08-ai/ops-0058-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/08-ai/ops-0059-rag-workflow/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: ca67cd6b2c8d2ce314b61dd41830e9df4f49ed92
  role: guide
  catalog_path: docs/05.operations/catalog/08-ai/ops-0059-rag-workflow/guide.md
  final_path: docs/05.operations/catalog/08-ai/ops-0059-rag-workflow/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/08-ai/ops-0059-rag-workflow/guide.md
  preserved_semantics:
  - section:common-checks:e22250cd7744
  - section:common-pitfalls:b0aca1ba753a
  - section:overview:e441f2d7f470
  - section:prerequisites:cc5c42e3a464
  - section:purpose:5faca96d82cb
  - section:rag-workflow-usage-guide:5704997c330c
  - section:related-documents:200195b1f6c6
  - section:runbook-handoff:56435c525641
  - section:step-by-step-instructions:fe3465ccf498
  - section:target-audience:c2d5bf1b424d
  - section:usage-type:845f70d8ac2b
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/08-ai/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/README.md
  final_consumers:
  - docs/05.operations/catalog/08-ai/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/08-ai/README.md
- legacy_path: docs/05.operations/09-tooling/README.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: aaf7234053ecbf7a8b4fba66064603e357603c52
  role: domain-readme
  catalog_path: docs/05.operations/catalog/09-tooling/README.md
  final_path: docs/05.operations/catalog/09-tooling/README.md
  semantic_action: retain
  canonical_role_owner: null
  preserved_semantics:
  - section:audience:8ed0837451b9
  - section:how-to-work-in-this-area:337b67e34061
  - section:operations-09-tooling:4640233a990c
  - section:overview:19caea9fcc1c
  - section:related-documents:50ff9790de47
  - section:scope:ae0f13d926bd
  - section:structure:7e06d8793747
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/09-tooling/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
  final_consumers:
  - docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/09-tooling/README.md
  - tests/validation/test_target_surface_contracts.py
  - tests/validation/test_target_surface_delta_contracts.py
- legacy_path: docs/05.operations/09-tooling/ops-0060-iac-deployment-policy/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d65f46a1301035c7b083ea700322cce1591a7137
  role: policy
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0060-iac-deployment-policy/policy.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0060-iac-deployment/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0060-iac-deployment/policy.md
  preserved_semantics:
  - section:controls:1757df1f168a
  - section:exceptions:df3af92d469d
  - section:iac-deployment-policy:0d1fbdf633b6
  - section:overview:76a5a6d0fb3c
  - section:policy-scope:3e0ee8c08074
  - section:related-documents:133ca40b5146
  - section:review-cadence:c9368c7c5e1a
  - section:verification:53503a3e8f27
  - 'text:baseline-body:**Required**: IaC 변경은 PR review, plan evidence, apply approval, state backend boundary 기록을 거친다.'
  removed_semantics:
  - stale:legacy-subject-path:ops-0060-iac-deployment-policy
  active_consumers:
  - docs/05.operations/09-tooling/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/09-tooling/ops-0061-k6/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 7748b6ed0f6aa824b30b448ae34021a80d847527
  role: guide
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0061-k6/guide.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0061-k6/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0061-k6/guide.md
  preserved_semantics:
  - section:common-checks:58d1e473697e
  - section:common-pitfalls:0a3396c7c733
  - section:k6-usage-guide:8fe8b14d6664
  - section:overview:5edc7b75a7af
  - section:prerequisites:7b303f7880e1
  - section:purpose:015acad92176
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:4ce2989b128a
  - section:target-audience:d043be9c31cc
  - section:usage-type:5a9d8aca9b1a
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0061-k6/policy.md
  - docs/05.operations/09-tooling/ops-0061-k6/runbook.md
  - docs/05.operations/09-tooling/ops-0064-performance-testing/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/k6/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0061-k6/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0061-k6/runbook.md
  - docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/k6/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0061-k6/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: ccaced42ca333509adee3031ae7daa29f062cf2c
  role: policy
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0061-k6/policy.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0061-k6/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0061-k6/policy.md
  preserved_semantics:
  - section:1:9e9ce8632a1c
  - section:2:0ef8c17317b7
  - section:3:dcd53a253108
  - section:controls:f3fb6d793df0
  - section:exceptions:4db2d9e28b64
  - section:k6-operations-policy:f1f3abc145d9
  - section:monitoring-requirements:5ffb2c257005
  - section:operational-standards:48e0a4dc6873
  - section:overview:8c55f1088ea7
  - section:policy-goals:41123bde2a16
  - section:policy-scope:c6e04cf79656
  - section:related-documents:b7726adff5a9
  - section:review-cadence:5326037d314e
  - section:target-audience:320b2738b735
  - section:verification:5d2a8eede829
  removed_semantics: []
  active_consumers:
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0061-k6/guide.md
  - docs/05.operations/09-tooling/ops-0061-k6/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/k6/README.md
  final_consumers:
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0061-k6/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0061-k6/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/k6/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0061-k6/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d526777820d3482c75e53554957765586882a2d4
  role: runbook
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0061-k6/runbook.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0061-k6/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0061-k6/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:7f0d798478c9
  - section:canonical-references:414e8e2a5382
  - section:checklist:a77bbdb4ff2a
  - section:escalation:7b3565109fdb
  - section:evidence:afd8558f1b74
  - section:k6-wrapper-recovery-procedure:81b407bc2ba5
  - section:k6-wrapper-recovery-runbook:95d18dc267c9
  - section:observability-and-evidence-sources:68b024267fbb
  - section:overview:c1443aabdad2
  - section:procedure:5da93bd3e257
  - section:purpose:10652176c64a
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:5078e79ef016
  - section:safe-rollback-or-recovery-procedure:e0680c5d3ecb
  - section:steps:2fa58ad07da5
  - section:verification-steps:2cb0602746b4
  - section:when-to-use:0b0a462d0a33
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0061-k6/guide.md
  - docs/05.operations/09-tooling/ops-0061-k6/policy.md
  - docs/05.operations/09-tooling/ops-0064-performance-testing/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/k6/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0061-k6/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0061-k6/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/k6/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0062-locust/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: da4cecf3c8310b148d6b6529c10335722f6c8c74
  role: guide
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0062-locust/guide.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0062-locust/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0062-locust/guide.md
  preserved_semantics:
  - section:common-checks:9f2c7875cae8
  - section:common-pitfalls:07fa2c2dcb26
  - section:locust-usage-guide:f0017da67f38
  - section:overview:7c127ba5900a
  - section:prerequisites:409dbcb402e9
  - section:purpose:c330cd13188d
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:c32ddd5f9c13
  - section:target-audience:19248fb2e0a5
  - section:usage-type:ec86ac615264
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0062-locust/policy.md
  - docs/05.operations/09-tooling/ops-0062-locust/runbook.md
  - docs/05.operations/09-tooling/ops-0064-performance-testing/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/locust/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0062-locust/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0062-locust/runbook.md
  - docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/guide.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/locust/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0062-locust/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: e03852cf337c63727166f1828b10ad6f71a5b7c4
  role: policy
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0062-locust/policy.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0062-locust/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0062-locust/policy.md
  preserved_semantics:
  - section:1-governance:c621948734a0
  - section:2-scaling:4fc9da84ffe2
  - section:3-data-security:d92fb120e214
  - section:controls:f3fb6d793df0
  - section:exceptions:4db2d9e28b64
  - section:locust-operations-policy:a1cf3e2c1b2e
  - section:operational-standards:48e0a4dc6873
  - section:overview:92124a8627f4
  - section:policy-goals:a17639d76c74
  - section:policy-scope:c6e04cf79656
  - section:related-documents:b7726adff5a9
  - section:review-cadence:5326037d314e
  - section:security-controls:a77bf6c71beb
  - section:target-audience:9d7413144d4c
  - section:verification:5d2a8eede829
  removed_semantics: []
  active_consumers:
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0062-locust/guide.md
  - docs/05.operations/09-tooling/ops-0062-locust/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/locust/README.md
  final_consumers:
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0062-locust/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0062-locust/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/locust/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0062-locust/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 9f94745ea68f1b6dc751b49315d42a0dbd5ca55a
  role: runbook
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0062-locust/runbook.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0062-locust/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0062-locust/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:7f0d798478c9
  - section:canonical-references:66b5c391a8d7
  - section:checklist:b22b9133e219
  - section:escalation:a2ce5dc1f4cf
  - section:evidence:577b9eac3a20
  - section:locust-recovery-procedure:234416d338dc
  - section:locust-recovery-runbook:1f5590e0ddc7
  - section:observability-and-evidence-sources:df87c40d21d5
  - section:overview:2fe40b17c10e
  - section:procedure:5da93bd3e257
  - section:purpose:61485c230ea6
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:cbf46c180d92
  - section:safe-rollback-or-recovery-procedure:d6c1377157dc
  - section:steps:ebf2f1d4eb11
  - section:verification-steps:eed576cdd07e
  - section:when-to-use:2e2d408ea599
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0062-locust/guide.md
  - docs/05.operations/09-tooling/ops-0062-locust/policy.md
  - docs/05.operations/09-tooling/ops-0064-performance-testing/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/locust/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0062-locust/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0062-locust/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/locust/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0063-optimization-hardening/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 11171673ed83245b5a16dc0eb77e146b13da5fee
  role: guide
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/guide.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/guide.md
  preserved_semantics:
  - section:09-tooling-optimization-hardening-usage-guide:6871c125e6b4
  - section:common-checks:aa73d2e75c54
  - section:common-pitfalls:007f07b98d59
  - section:overview:175d13582b07
  - section:prerequisites:0081e3ff6ce6
  - section:purpose:ba97e04a8fd4
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:b160c8e69b4d
  - section:target-audience:27c66bbd1dbf
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0021-tooling-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0024-tooling-optimization-hardening-architecture.md
  - docs/03.specs/spec-0010-tooling/spec.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0063-optimization-hardening/policy.md
  - docs/05.operations/09-tooling/ops-0063-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0021-tooling-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0024-tooling-optimization-hardening-architecture.md
  - docs/03.specs/spec-0010-tooling/spec.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/09-tooling/ops-0063-optimization-hardening/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: ae7d9bcca7f1cbe8fd73e3adacd9234c26ba45d9
  role: policy
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/policy.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/policy.md
  preserved_semantics:
  - section:09-tooling-optimization-hardening-operations-policy:ad8db9f6a07e
  - section:catalog-expansion-approval-gates:e0b9c7c31ca0
  - section:controls:4d64d6c57dc2
  - section:exceptions:c39b7b94117a
  - section:overview:40a7a5a0c827
  - section:policy-scope:c8d33647dcd7
  - section:related-documents:b7726adff5a9
  - section:review-cadence:c66fbe41b2b5
  - section:verification:59831dd820d3
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0021-tooling-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0024-tooling-optimization-hardening-architecture.md
  - docs/03.specs/spec-0010-tooling/spec.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0063-optimization-hardening/guide.md
  - docs/05.operations/09-tooling/ops-0063-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0021-tooling-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0024-tooling-optimization-hardening-architecture.md
  - docs/03.specs/spec-0010-tooling/spec.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/09-tooling/ops-0063-optimization-hardening/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 88ebc04b2b8221c3341534bbb778172126f1e426
  role: runbook
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/runbook.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/runbook.md
  preserved_semantics:
  - section:09-tooling-optimization-hardening-procedure:8455a4778b00
  - section:09-tooling-optimization-hardening-runbook:b7a308c5e1db
  - section:agent-operations-if-applicable:63333e40ffd3
  - section:canonical-references:0c2e95a2ecce
  - section:checklist:89c89a5216c7
  - section:escalation:629d18d11406
  - section:evidence:281de110c3b6
  - section:observability-and-evidence-sources:57cc84c94a27
  - section:overview:d38f679c7977
  - section:procedure:5da93bd3e257
  - section:purpose:488aa4a006a4
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:68184abaca10
  - section:safe-rollback-or-recovery-procedure:b4474c293b93
  - section:steps:7c894265fb86
  - section:verification-steps:5fb9216fa2be
  - section:when-to-use:a088cc6049c0
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0021-tooling-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0024-tooling-optimization-hardening-architecture.md
  - docs/03.specs/spec-0010-tooling/spec.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0063-optimization-hardening/guide.md
  - docs/05.operations/09-tooling/ops-0063-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0021-tooling-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0024-tooling-optimization-hardening-architecture.md
  - docs/03.specs/spec-0010-tooling/spec.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0063-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/09-tooling/ops-0064-performance-testing/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b8cd40d6cb3824d8119da201b38fdea4d3591ea5
  role: guide
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/guide.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/guide.md
  preserved_semantics:
  - section:common-checks:89ba96d04924
  - section:common-pitfalls:0cafa3d5f5c2
  - section:overview:2293b6a3c5dd
  - section:performance-testing-usage-guide:b87932126ac0
  - section:prerequisites:55149c958256
  - section:purpose:9acabd649c04
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:fd741d7ca252
  - section:target-audience:09b7a7577578
  - section:usage-type:5a9d8aca9b1a
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0064-performance-testing/policy.md
  - docs/05.operations/09-tooling/ops-0064-performance-testing/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/09-tooling/ops-0064-performance-testing/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: e5f9efdda7eaf0696c856ff1fc9e71e94ab5611e
  role: policy
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/policy.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/policy.md
  preserved_semantics:
  - section:1-pre-testing:d1a609d448d9
  - section:2-environment-isolation:1b003b1e3a98
  - section:3-retention:0c235dc5a197
  - section:controls:f3fb6d793df0
  - section:exceptions:4db2d9e28b64
  - section:governance-compliance:e00ab637e894
  - section:operational-standards:48e0a4dc6873
  - section:overview:5664d5e806fa
  - section:performance-testing-operations-policy:1fe533ca72f7
  - section:policy-goals:5d1b020779ec
  - section:policy-scope:1355c945b302
  - section:related-documents:b7726adff5a9
  - section:review-cadence:5326037d314e
  - section:security-controls:ce3c26ef9ef5
  - section:target-audience:d24e4c964704
  - section:verification:5d2a8eede829
  removed_semantics: []
  active_consumers:
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0064-performance-testing/guide.md
  - docs/05.operations/09-tooling/ops-0064-performance-testing/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/09-tooling/ops-0064-performance-testing/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: cabe77d4df35eb4da59d955ece03511ba167b454
  role: runbook
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/runbook.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:7f0d798478c9
  - section:canonical-references:1b81f50234bc
  - section:checklist:5d0fed3bd6bc
  - section:escalation:8274027e4432
  - section:evidence:6565cce30406
  - section:observability-and-evidence-sources:97dda51705e8
  - section:overview:467217821c94
  - section:performance-testing-incident-procedure:9617a9f3fbe6
  - section:performance-testing-incident-runbook:af6a646b5c7d
  - section:procedure:5da93bd3e257
  - section:purpose:a32f64a6989f
  - section:related-documents:718cb2f86f88
  - section:rollback-or-recovery:e83977b2abe9
  - section:safe-rollback-or-recovery-procedure:75d6cf51fc87
  - section:steps:24b2ae5b137d
  - section:verification-steps:60104651e064
  - section:when-to-use:1fc9c0e5ce2a
  removed_semantics: []
  active_consumers:
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0064-performance-testing/guide.md
  - docs/05.operations/09-tooling/ops-0064-performance-testing/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0064-performance-testing/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/09-tooling/ops-0065-registry/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 1ddf1967319ddee6923eee0a1eed96376a454155
  role: guide
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0065-registry/guide.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0065-registry/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0065-registry/guide.md
  preserved_semantics:
  - section:1-registry-login-if-auth-is-configured:c75d053cd6df
  - section:2-image-tagging:6caa5e724b43
  - section:3-image-push:10087b9fa695
  - section:4-image-pull:07e08e713661
  - section:common-checks:5f5af99d9672
  - section:common-pitfalls:a5f8ac7b1dcd
  - section:docker-registry-usage-guide:6fcfafc48f15
  - section:overview:107f889b63a3
  - section:prerequisites:ae1b2da3a616
  - section:purpose:3351416e37bb
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:9c20e5ca273f
  - section:target-audience:389f62f62ac3
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0065-registry/policy.md
  - docs/05.operations/09-tooling/ops-0065-registry/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/registry/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0065-registry/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0065-registry/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/registry/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0065-registry/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 94740ed0cf32716274500684be0fd32c1386e4fa
  role: policy
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0065-registry/policy.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0065-registry/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0065-registry/policy.md
  preserved_semantics:
  - section:controls:ff3fe643b29e
  - section:docker-registry-operations-policy:e1ae3ddf7fee
  - section:exceptions:75f6f1504818
  - section:overview:5d90e8b0eb7b
  - section:policy-scope:81038932a262
  - section:related-documents:b7726adff5a9
  - section:review-cadence:031a3f9f3d2e
  - section:verification:c3cc51f65a89
  removed_semantics: []
  active_consumers:
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0065-registry/guide.md
  - docs/05.operations/09-tooling/ops-0065-registry/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/registry/README.md
  final_consumers:
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0065-registry/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0065-registry/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/registry/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0065-registry/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: a30da7e2e613a425ce1ef8078d37d454f348f2ad
  role: runbook
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0065-registry/runbook.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0065-registry/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0065-registry/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:canonical-references:c184b02b818e
  - section:checklist:2857c78ed50d
  - section:docker-registry-runbook:c00ab680aaa5
  - section:escalation:5370d9ef6273
  - section:evidence:a22cebabc0e9
  - section:observability-and-evidence-sources:14a6d7a51dc2
  - section:overview:5fb6ba96ac2b
  - section:procedure:5da93bd3e257
  - section:purpose:81f00196a13f
  - section:recovery-steps:9c226a894bd1
  - section:registry-recovery-procedure:23780c6e3fe1
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:0c072582b820
  - section:steps:175102b44a8c
  - section:symptoms:a1bacabf1e0f
  - section:verification-steps:21eddcb34a65
  - section:when-to-use:23437a89c76a
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0065-registry/guide.md
  - docs/05.operations/09-tooling/ops-0065-registry/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/registry/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0065-registry/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0065-registry/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/registry/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0066-sonarqube/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 50234605bc296754d0b542b70ac7004caa93f2a0
  role: guide
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/guide.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/guide.md
  preserved_semantics:
  - section:1-access-and-authentication:2807e55819e5
  - section:2-creating-a-new-project:1cf3a72a31a2
  - section:3-running-a-local-scan:8573f695f4cc
  - section:architecture-context:96f30df3ce42
  - section:common-checks:bc6c4c1c43a3
  - section:common-pitfalls:d44786157825
  - section:elasticsearch-max-map-count:3c2eb4f62f70
  - section:execute-scan:345c02ef8557
  - section:how-to-procedures:e1b6a5b45a9a
  - section:memory-exhaustion:b046b1b5809f
  - section:overview:5b8073430c21
  - section:overview:90934a297651
  - section:prerequisites:8e6eddc948d2
  - section:purpose:83b4f82f9760
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:set-environment-variables:a52b65443ed3
  - section:sonarqube-usage-guide:982d7060fd50
  - section:step-by-step-instructions:33aaaee7e276
  - section:target-audience:90accb0a25c5
  - section:troubleshooting-pitfalls:f2d72a988065
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0066-sonarqube/policy.md
  - docs/05.operations/09-tooling/ops-0066-sonarqube/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/sonarqube/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/sonarqube/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0066-sonarqube/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 28cc06832386c9a598f31ff2e1b2ae6ac0d15120
  role: policy
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/policy.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/policy.md
  preserved_semantics:
  - section:1-quality-gate-enforcement:6dacf7b1250d
  - section:2-routine-maintenance:c210b2b90ecb
  - section:3-backup-and-persistence:372e2f06b070
  - section:controls:f3fb6d793df0
  - section:exceptions:4db2d9e28b64
  - section:monitoring-strategy:099e4a0f413a
  - section:operational-standards:48e0a4dc6873
  - section:overview:02675d385e5a
  - section:policy-scope:328dee8d5ea4
  - section:related-documents:b7726adff5a9
  - section:review-cadence:5326037d314e
  - section:sonarqube-operations-policy:1d88ea37dbd5
  - section:verification:5d2a8eede829
  removed_semantics: []
  active_consumers:
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0066-sonarqube/guide.md
  - docs/05.operations/09-tooling/ops-0066-sonarqube/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/sonarqube/README.md
  final_consumers:
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/sonarqube/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0066-sonarqube/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 2bae3ba58e48b475320c96b9ba328c6bad9d25d2
  role: runbook
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/runbook.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/runbook.md
  preserved_semantics:
  - section:1-check-service-status:b2443d03b08c
  - section:1-elasticsearch-index-reconstruction:3e9e9a681a95
  - section:1-stop-the-service:88ab94821dd1
  - section:2-clear-es-data-requires-root-to-delete-es-lock-files:97a420dda8e5
  - section:2-jvm-memory-adjustment:0c4836cd223f
  - section:2-verify-database-connectivity:4b8e538c957c
  - section:3-log-inspection:b22ce43781a3
  - section:3-restart-service:c9e339666d2f
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:canonical-references:c184b02b818e
  - section:checklist:2857c78ed50d
  - section:diagnostic-steps:66bb727fb152
  - section:escalation-policy:0013b0d92362
  - section:escalation:31d1967cf9fc
  - section:evidence:a22cebabc0e9
  - section:observability-and-evidence-sources:14a6d7a51dc2
  - section:overview:91b15bfdb417
  - section:procedure-sonarqube-service-recovery-p2:6e2c2f9302d3
  - section:procedure:5da93bd3e257
  - section:purpose:81f00196a13f
  - section:recovery-procedures:c878d8ea6b73
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:0c072582b820
  - section:sonarqube-runbook:796fd8cee34d
  - section:steps:175102b44a8c
  - section:symptoms:8f3e106d6940
  - section:update-these-values-in-docker-compose-yml:e531701d9e89
  - section:verification-steps:21eddcb34a65
  - section:when-to-use:23437a89c76a
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0066-sonarqube/guide.md
  - docs/05.operations/09-tooling/ops-0066-sonarqube/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/sonarqube/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0066-sonarqube/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/sonarqube/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0067-syncthing/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 8743f27b608537cfb47a75e0767e66bd13a60ae9
  role: guide
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0067-syncthing/guide.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0067-syncthing/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0067-syncthing/guide.md
  preserved_semantics:
  - section:1-accessing-the-gui:aba831d01455
  - section:2-pairing-a-new-device:90f29e903afd
  - section:3-sharing-the-sync-folder:0507aec0d1dd
  - section:architecture-context:16a46896ed90
  - section:common-checks:9f6eb55998b4
  - section:common-pitfalls:74d413976b14
  - section:connection-failures:faeeed54c4dd
  - section:how-to-procedures:e1b6a5b45a9a
  - section:out-of-sync-state:89f56a2335a9
  - section:overview:2048a485a0d1
  - section:overview:3382df0f0f90
  - section:prerequisites:872b84f8fb8b
  - section:purpose:3a77c36a08bf
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:6dc2f16483bb
  - section:syncthing-usage-guide:0ccc7b269a7a
  - section:target-audience:089658ef5a70
  - section:troubleshooting-pitfalls:f2d72a988065
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0067-syncthing/policy.md
  - docs/05.operations/09-tooling/ops-0067-syncthing/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/syncthing/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0067-syncthing/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0067-syncthing/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/syncthing/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0067-syncthing/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: f809a1771ecc6085426653330dbd715983225276
  role: policy
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0067-syncthing/policy.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0067-syncthing/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0067-syncthing/policy.md
  preserved_semantics:
  - section:1-data-integrity-and-conflicts:040063f67f64
  - section:2-routine-maintenance:f486dc925280
  - section:3-resource-optimization:ec7b04827b89
  - section:controls:f3fb6d793df0
  - section:exceptions:4db2d9e28b64
  - section:monitoring-strategy:50cc1cf231eb
  - section:operational-standards:48e0a4dc6873
  - section:overview:92d8615315bb
  - section:policy-scope:c2fe796b7a74
  - section:related-documents:b7726adff5a9
  - section:review-cadence:5326037d314e
  - section:syncthing-operations-policy:c28381f9ccbe
  - section:verification:5d2a8eede829
  removed_semantics: []
  active_consumers:
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0067-syncthing/guide.md
  - docs/05.operations/09-tooling/ops-0067-syncthing/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/syncthing/README.md
  final_consumers:
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0067-syncthing/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0067-syncthing/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/syncthing/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0067-syncthing/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 7423f828a8a193bab5188cb34db1377d65a2ebb4
  role: runbook
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0067-syncthing/runbook.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0067-syncthing/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0067-syncthing/runbook.md
  preserved_semantics:
  - section:1-check-service-status:4bc01ebdc016
  - section:1-resolving-out-of-sync-items:1675e72c1bee
  - section:2-repairing-corrupted-database:77ab5b41fb4c
  - section:2-verify-port-connectivity:6fc7146a85af
  - section:3-resetting-gui-password:f06c5bb4adde
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:alternative-manual-removal-of-the-index-directory:dde99f0dfd34
  - section:canonical-references:c184b02b818e
  - section:checklist:2857c78ed50d
  - section:diagnostic-steps:66bb727fb152
  - section:escalation-policy:71b9f89dc372
  - section:escalation:31d1967cf9fc
  - section:evidence:a22cebabc0e9
  - section:from-another-node:887f489c9054
  - section:observability-and-evidence-sources:14a6d7a51dc2
  - section:overview:759b22b242c1
  - section:procedure-syncthing-service-recovery-p2:79487e54c7d4
  - section:procedure:5da93bd3e257
  - section:purpose:81f00196a13f
  - section:recovery-procedures:c878d8ea6b73
  - section:related-documents:295cb48a66e8
  - section:restart-service:0f6e43f87844
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:0c072582b820
  - section:start-with-delta-reset-requires-editing-compose-or-temporary-exec:8f56889f48a0
  - section:steps:175102b44a8c
  - section:stop-the-service:7bb7c6b4c0d1
  - section:symptoms:5fa0997a45cc
  - section:syncthing-runbook:1d7d013b9f7c
  - section:verification-steps:21eddcb34a65
  - section:when-to-use:23437a89c76a
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0067-syncthing/guide.md
  - docs/05.operations/09-tooling/ops-0067-syncthing/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/syncthing/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0067-syncthing/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0067-syncthing/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/syncthing/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0068-terraform/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 7062bd601317fc83dd09abdbea67d4076dd4335f
  role: guide
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0068-terraform/guide.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0068-terraform/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0068-terraform/guide.md
  preserved_semantics:
  - section:1-generate-plan:58caf04b8f91
  - section:1-job-based-execution:6a83775b29a7
  - section:2-review-the-plan:77e0e9ad8461
  - section:2-state-management:960373cee9d4
  - section:3-apply-the-plan:91c7d1c50d5f
  - section:3-credential-handling:efc2f0d894a0
  - section:common-checks:16658467f269
  - section:common-pitfalls:d44786157825
  - section:common-workflows:4eac290fa0c6
  - section:formatting-and-validation:33f4e97d465b
  - section:implementation-context-kr:3657c33baf1f
  - section:initializing-a-project:f58bc6d5c0ea
  - section:key-concepts:99e34c284eca
  - section:lock-file-issues:fcac88c1012d
  - section:network-connectivity:08c97918233c
  - section:operations-terraform-policy-usage-guide:d64691818582
  - section:overview:99179a3504ac
  - section:overview:e2b77f51b03b
  - section:prerequisites:8e6eddc948d2
  - section:purpose:95a6c80ea958
  - section:related-documents:864fe5dd05d8
  - section:resource-provisioning-plan-apply:da23e091a162
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:33aaaee7e276
  - section:target-audience:90accb0a25c5
  - section:terraform-system-usage:b30a3b473f43
  - section:troubleshooting:c6b72ab43705
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0060-iac-deployment-policy/policy.md
  - docs/05.operations/09-tooling/ops-0068-terraform/policy.md
  - docs/05.operations/09-tooling/ops-0068-terraform/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/terraform/README.md
  - tests/validation/test_script_manifest.py
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0060-iac-deployment/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0068-terraform/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0068-terraform/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/terraform/README.md
  - tests/validation/test_script_manifest.py
- legacy_path: docs/05.operations/09-tooling/ops-0068-terraform/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 611987cfa39677aab64478d1f523ee2d32be62b1
  role: policy
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0068-terraform/policy.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0068-terraform/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0068-terraform/policy.md
  preserved_semantics:
  - section:1-remote-state-requirement:c02ff3fff5a6
  - section:2-state-backups:cd2c62da8712
  - section:compliance-security:786251d059e4
  - section:controls:f3fb6d793df0
  - section:credential-rotation:d4979373c370
  - section:deployment-workflow:ee2698b998e0
  - section:exceptions:4db2d9e28b64
  - section:maintenance-cycles:98fe5da75236
  - section:overview:22c87c8ba29c
  - section:policy-scope:68ef2acd995e
  - section:provider-updates:830c142d2cbb
  - section:related-documents:b7726adff5a9
  - section:review-cadence:5326037d314e
  - section:state-management-policy:0c60510f7494
  - section:terraform-operations-policy:b0153ed14f41
  - section:verification:5d2a8eede829
  removed_semantics: []
  active_consumers:
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0068-terraform/guide.md
  - docs/05.operations/09-tooling/ops-0068-terraform/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/terraform/README.md
  final_consumers:
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0068-terraform/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0068-terraform/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/terraform/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0068-terraform/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 5e53fe6f3f41c3faec5c86759d1dec3dc504a8ed
  role: runbook
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0068-terraform/runbook.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0068-terraform/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0068-terraform/runbook.md
  preserved_semantics:
  - section:1-confirm-execution-context:df8429bb6a0d
  - section:2-verify-remote-backend-access:66a1cb87b06b
  - section:3-force-unlocking-state:bb527fdeb2ea
  - section:4-restore-corrupted-local-state:fe468cd9d523
  - section:5-refresh-provider-credentials:e62f7f71b659
  - section:6-verify-terraform-health:7fb966abf670
  - section:escalation:781f8ab2da53
  - section:evidence:ea9a6881bbfd
  - section:overview:694af694fc31
  - section:procedure:5da93bd3e257
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:97dff023fc15
  - section:terraform-runbook:323d181df94f
  - section:when-to-use:76b3abeb4722
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0060-iac-deployment-policy/policy.md
  - docs/05.operations/09-tooling/ops-0068-terraform/guide.md
  - docs/05.operations/09-tooling/ops-0068-terraform/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/terraform/README.md
  - scripts/manifest.yaml
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0060-iac-deployment/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0068-terraform/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0068-terraform/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/terraform/README.md
  - scripts/manifest.yaml
- legacy_path: docs/05.operations/09-tooling/ops-0069-terrakube/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 95b296bcd02356a14a9ce8ab403b16043973d41f
  role: guide
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0069-terrakube/guide.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0069-terrakube/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0069-terrakube/guide.md
  preserved_semantics:
  - section:1-initial-login:74617bf8a595
  - section:2-organizations-and-workspaces:40149144e870
  - section:common-checks:b528e4104193
  - section:common-pitfalls:d44786157825
  - section:executor-model:e79694e5c44a
  - section:executor-timeout:ae6c0d1b8c6d
  - section:feature-breakdown:fe12188bdde2
  - section:getting-started:4467215509db
  - section:implementation-context-kr:126036bc3a8d
  - section:integration-details:75a111fcc83e
  - section:operations-terrakube-policy-usage-guide:6bc011afd2fd
  - section:overview:db87fcd6ebc9
  - section:overview:ffafd2714b88
  - section:prerequisites:8e6eddc948d2
  - section:private-module-registry:7087cc26b835
  - section:purpose:78fc6a38f20b
  - section:related-documents:864fe5dd05d8
  - section:remote-state-minio:febd8b0596ed
  - section:runbook-handoff:a6f4d9784508
  - section:sso-failures:378cc1592743
  - section:step-by-step-instructions:33aaaee7e276
  - section:target-audience:90accb0a25c5
  - section:troubleshooting:c6b72ab43705
  - section:ui-driven-workflows:dbb2ceff850b
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  - section:variable-management:f4fdce2b9729
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0060-iac-deployment-policy/policy.md
  - docs/05.operations/09-tooling/ops-0069-terrakube/policy.md
  - docs/05.operations/09-tooling/ops-0069-terrakube/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/terrakube/README.md
  - tests/validation/test_script_manifest.py
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0060-iac-deployment/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0069-terrakube/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0069-terrakube/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/terrakube/README.md
  - tests/validation/test_script_manifest.py
- legacy_path: docs/05.operations/09-tooling/ops-0069-terrakube/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 1693800cf4e67ca9f403f14323147961f00f7923
  role: policy
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0069-terrakube/policy.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0069-terrakube/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0069-terrakube/policy.md
  preserved_semantics:
  - section:1-workspace-rbac:916c868bcc90
  - section:2-sso-authentication:3560c6040dc5
  - section:access-control-policy:0409d6912f2c
  - section:controls:f3fb6d793df0
  - section:exceptions:4db2d9e28b64
  - section:monthly:cb22d08d71d2
  - section:overview:867f23c36714
  - section:policy-scope:b773fac9ebf6
  - section:registry-maintenance:082e852d4465
  - section:related-documents:b7726adff5a9
  - section:resource-execution-policy:c60a5f8f9355
  - section:review-cadence:5326037d314e
  - section:routine-maintenance:1fab1ee98927
  - section:security-standards:6bdad2e51e58
  - section:terrakube-operations-policy:30b07e2dfd28
  - section:verification:5d2a8eede829
  - section:weekly:c2540c00c724
  removed_semantics: []
  active_consumers:
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0069-terrakube/guide.md
  - docs/05.operations/09-tooling/ops-0069-terrakube/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/terrakube/README.md
  final_consumers:
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0069-terrakube/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0069-terrakube/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/terrakube/README.md
- legacy_path: docs/05.operations/09-tooling/ops-0069-terrakube/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 89308a56ccee4d30bd0f9cae45bb7653e3109f90
  role: runbook
  catalog_path: docs/05.operations/catalog/09-tooling/ops-0069-terrakube/runbook.md
  final_path: docs/05.operations/catalog/09-tooling/ops-0069-terrakube/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/09-tooling/ops-0069-terrakube/runbook.md
  preserved_semantics:
  - section:1-check-api-and-executor-health:3fefa951d9e2
  - section:1-cleaning-up-hung-executors:18825fa3609d
  - section:2-resolving-oidc-dex-auth-loops:542a6708f95d
  - section:2-verify-docker-socket-access:da53be5ab110
  - section:3-manual-workspace-unlock:8cb4566d3dce
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:canonical-references:c184b02b818e
  - section:checklist:2857c78ed50d
  - section:diagnostic-steps:66bb727fb152
  - section:escalation-policy:6c3d5a77dbf2
  - section:escalation:31d1967cf9fc
  - section:evidence:a22cebabc0e9
  - section:observability-and-evidence-sources:14a6d7a51dc2
  - section:overview:bf2fdc347225
  - section:procedure-terrakube-recovery-p2:8b0bd0934cab
  - section:procedure:5da93bd3e257
  - section:purpose:81f00196a13f
  - section:recovery-procedures:c878d8ea6b73
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:0c072582b820
  - section:steps:175102b44a8c
  - section:symptoms:3f9a24e53d41
  - section:terrakube-runbook:6516a2ddc4f9
  - section:verification-steps:21eddcb34a65
  - section:when-to-use:23437a89c76a
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/09-tooling/README.md
  - docs/05.operations/09-tooling/ops-0060-iac-deployment-policy/policy.md
  - docs/05.operations/09-tooling/ops-0069-terrakube/guide.md
  - docs/05.operations/09-tooling/ops-0069-terrakube/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/terrakube/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/09-tooling/README.md
  - docs/05.operations/catalog/09-tooling/ops-0060-iac-deployment/policy.md
  - docs/05.operations/catalog/09-tooling/ops-0069-terrakube/guide.md
  - docs/05.operations/catalog/09-tooling/ops-0069-terrakube/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/09-tooling/terrakube/README.md
- legacy_path: docs/05.operations/10-communication/README.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 819dc0bbc9f25e56ac53ab7c2acef8f6510378ef
  role: domain-readme
  catalog_path: docs/05.operations/catalog/10-communication/README.md
  final_path: docs/05.operations/catalog/10-communication/README.md
  semantic_action: retain
  canonical_role_owner: null
  preserved_semantics:
  - section:audience:8ed0837451b9
  - section:how-to-work-in-this-area:f88be1343bc9
  - section:operations-10-communication:b1722974549b
  - section:overview:d606158a8c3b
  - section:related-documents:b23f6dcf828c
  - section:scope:2f66a7fd47ad
  - section:structure:dd4c73cd8a24
  removed_semantics: []
  active_consumers:
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  final_consumers:
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
- legacy_path: docs/05.operations/10-communication/ops-0070-mail/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 3279fb8524211f6bf289c6e87ccd612fe46de914
  role: guide
  catalog_path: docs/05.operations/catalog/10-communication/ops-0070-mail/guide.md
  final_path: docs/05.operations/catalog/10-communication/ops-0070-mail/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/10-communication/ops-0070-mail/guide.md
  preserved_semantics:
  - section:1-compose:2e83d68f9951
  - section:2-stalwart:2e8422097c32
  - section:3-mailhog:cc62ec73e6a3
  - section:client-configuration-stalwart:5e43231e8dae
  - section:common-checks:fece244ac6a6
  - section:common-pitfalls:c4a20578928d
  - section:mail-usage-guide:a9b1e60033a4
  - section:overview:abc901cadb3d
  - section:prerequisites:82cdb0cb49e1
  - section:purpose:0bcdecbd8594
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:9c20e5ca273f
  - section:target-audience:089658ef5a70
  - section:usage-type:36d6db90c9bc
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0011-communication/spec.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/10-communication/README.md
  - docs/05.operations/10-communication/ops-0070-mail/policy.md
  - docs/05.operations/10-communication/ops-0070-mail/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/10-communication/README.md
  - infra/10-communication/mail/README.md
  - tests/validation/test_operations_taxonomy.py
  final_consumers:
  - docs/03.specs/spec-0011-communication/spec.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/10-communication/README.md
  - docs/05.operations/catalog/10-communication/ops-0070-mail/policy.md
  - docs/05.operations/catalog/10-communication/ops-0070-mail/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/10-communication/README.md
  - infra/10-communication/mail/README.md
  - tests/validation/test_operations_taxonomy.py
- legacy_path: docs/05.operations/10-communication/ops-0070-mail/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: b4c526e25c04d8abdac64339bd170ea206eef669
  role: policy
  catalog_path: docs/05.operations/catalog/10-communication/ops-0070-mail/policy.md
  final_path: docs/05.operations/catalog/10-communication/ops-0070-mail/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/10-communication/ops-0070-mail/policy.md
  preserved_semantics:
  - section:controls:23a209de9878
  - section:exceptions:4db2d9e28b64
  - section:mail-operations-policy:a737670d3881
  - section:overview:17b65f6a654f
  - section:persistence-backups:b383a1e22de5
  - section:policy-scope:e8cad662b572
  - section:related-documents:b7726adff5a9
  - section:review-cadence:ce2baac61c06
  - section:verification:ae64ec4e355e
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0011-communication/spec.md
  - docs/05.operations/10-communication/README.md
  - docs/05.operations/10-communication/ops-0070-mail/guide.md
  - docs/05.operations/10-communication/ops-0070-mail/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/10-communication/README.md
  - infra/10-communication/mail/README.md
  - tests/validation/test_operations_taxonomy.py
  final_consumers:
  - docs/03.specs/spec-0011-communication/spec.md
  - docs/05.operations/catalog/10-communication/README.md
  - docs/05.operations/catalog/10-communication/ops-0070-mail/guide.md
  - docs/05.operations/catalog/10-communication/ops-0070-mail/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/10-communication/README.md
  - infra/10-communication/mail/README.md
  - tests/validation/test_operations_taxonomy.py
- legacy_path: docs/05.operations/10-communication/ops-0070-mail/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 6836b76d14488435352f7f9e18d07d57f57b9b61
  role: runbook
  catalog_path: docs/05.operations/catalog/10-communication/ops-0070-mail/runbook.md
  final_path: docs/05.operations/catalog/10-communication/ops-0070-mail/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/10-communication/ops-0070-mail/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:c78af42d3c4e
  - section:canonical-references:a357b08a2d8a
  - section:checklist:a3d36ad1bc97
  - section:escalation:8a6dea00d440
  - section:evidence:823414ed55aa
  - section:mail-recovery-procedure:d6eff50e08d4
  - section:mail-recovery-runbook:23008baf9f7b
  - section:observability-and-evidence-sources:f78c15a72784
  - section:overview:18afff02c4a2
  - section:procedure:5da93bd3e257
  - section:purpose:dce0162df005
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:fd95e100bc52
  - section:safe-rollback-or-recovery-procedure:5d5b43a84d10
  - section:steps:275efd326643
  - section:verification-steps:24ae2c334768
  - section:when-to-use:e7fcb33894a6
  removed_semantics: []
  active_consumers:
  - docs/03.specs/spec-0011-communication/spec.md
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/10-communication/README.md
  - docs/05.operations/10-communication/ops-0070-mail/guide.md
  - docs/05.operations/10-communication/ops-0070-mail/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/10-communication/README.md
  - infra/10-communication/mail/README.md
  - tests/validation/test_operations_taxonomy.py
  final_consumers:
  - docs/03.specs/spec-0011-communication/spec.md
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/10-communication/README.md
  - docs/05.operations/catalog/10-communication/ops-0070-mail/guide.md
  - docs/05.operations/catalog/10-communication/ops-0070-mail/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/10-communication/README.md
  - infra/10-communication/mail/README.md
  - tests/validation/test_operations_taxonomy.py
- legacy_path: docs/05.operations/11-laboratory/README.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 10f69cff196fb2bd555d4f98e2c8dad15d9d7800
  role: domain-readme
  catalog_path: docs/05.operations/catalog/11-laboratory/README.md
  final_path: docs/05.operations/catalog/11-laboratory/README.md
  semantic_action: retain
  canonical_role_owner: null
  preserved_semantics:
  - section:audience:8ed0837451b9
  - section:how-to-work-in-this-area:1b78ec50d4e0
  - section:operations-11-laboratory:e43085748983
  - section:overview:cb92dda5969c
  - section:related-documents:2b050cc40989
  - section:scope:4924be894626
  - section:structure:1cc2fa0a8238
  removed_semantics: []
  active_consumers:
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/11-laboratory/README.md
  - infra/11-laboratory/open-notebook/README.md
  final_consumers:
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  - infra/11-laboratory/README.md
  - infra/11-laboratory/open-notebook/README.md
- legacy_path: docs/05.operations/11-laboratory/ops-0071-dashboard/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 454c71f20dbcc093169e3ace1d563f9db6e79ff8
  role: guide
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0071-dashboard/guide.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/guide.md
  preserved_semantics:
  - section:1-adding-new-services:3af2f873a8cc
  - section:2-customizing-icons-and-logos:8322d63b42cd
  - section:3-layout-and-theming:c061de519f89
  - section:common-checks:5415d418eba3
  - section:common-pitfalls:f467505f093f
  - section:laboratory-dashboard-usage-guide:688413774b48
  - section:overview:d508c7a0d5f1
  - section:prerequisites:05cd49f8e08e
  - section:purpose:f315932bd01f
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:9c20e5ca273f
  - section:target-audience:3738451fbe57
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 Homer 대시보드의 서비스 링크 관리, 테마 커스터마이징, 레이아웃 변경 방법을 설명한다. 하이홈 인프라의 모든 도구에 대한 접근성을 유지하고 관리하는 중앙 관리 지침을 제공한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0071-dashboard
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0071-dashboard/policy.md
  - docs/05.operations/11-laboratory/ops-0071-dashboard/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/dashboard/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/policy.md
  - docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/dashboard/README.md
- legacy_path: docs/05.operations/11-laboratory/ops-0071-dashboard/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 8732b12de647184a32ab62328d6e4db60b7b0355
  role: policy
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0071-dashboard/policy.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/policy.md
  preserved_semantics:
  - section:controls:83dcd117bf09
  - section:exceptions:48bd658abf5d
  - section:laboratory-dashboard-operations-policy:c4d669224cf5
  - section:overview:b31311924caf
  - section:policy-scope:f1d2899f9b9a
  - section:related-documents:b7726adff5a9
  - section:review-cadence:12551ecad78b
  - section:verification:fbf3dab22b98
  - text:baseline-body:모든 대시보드 접근은 Traefik `gateway-standard-chain@file,homer-admin-ip@docker,sso-errors@file,sso-auth@file` 미들웨어 체인을 통해 인증되어야 한다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0071-dashboard
  active_consumers:
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0071-dashboard/guide.md
  - docs/05.operations/11-laboratory/ops-0071-dashboard/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/dashboard/README.md
  final_consumers:
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/guide.md
  - docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/dashboard/README.md
- legacy_path: docs/05.operations/11-laboratory/ops-0071-dashboard/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: d207b8173aa5c9a5d413714b00bcaa94aed94f6c
  role: runbook
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0071-dashboard/runbook.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:08f9e8821952
  - section:canonical-references:d3fb09914dc1
  - section:checklist:99e93eba346f
  - section:escalation:cab3fb3d8cfc
  - section:evidence:0aa966493deb
  - section:laboratory-dashboard-recovery-procedure:d6ee34b00ab7
  - section:laboratory-dashboard-recovery-runbook:ec0fa618437a
  - section:observability-and-evidence-sources:2dc8b9a3e1bb
  - section:overview:a1a8ee390a3b
  - section:procedure:5da93bd3e257
  - section:purpose:68e4a8370430
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:994413d68fb8
  - section:safe-rollback-or-recovery-procedure:b3bf6d26161d
  - section:steps:811ca346bf09
  - section:verification-steps:81fbff29c845
  - section:when-to-use:1db8a749483f
  - text:baseline-body:`homer.${DEFAULT_URL}` 접속이 실패하거나 빈 화면이 표시될 때.
  removed_semantics:
  - stale:legacy-subject-path:ops-0071-dashboard
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0071-dashboard/guide.md
  - docs/05.operations/11-laboratory/ops-0071-dashboard/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/dashboard/README.md
  - scripts/validation/check-repo-contracts.sh
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/guide.md
  - docs/05.operations/catalog/11-laboratory/ops-0071-homer-dashboard/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/dashboard/README.md
  - scripts/validation/check-repo-contracts.sh
- legacy_path: docs/05.operations/11-laboratory/ops-0072-dozzle/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 6297880b149be96929e203c45078d903711208f8
  role: guide
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/guide.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/guide.md
  preserved_semantics:
  - section:common-checks:9a38e1d65e8d
  - section:common-pitfalls:780657fecd92
  - section:dozzle-usage-guide:f0476df5714f
  - section:overview:12c6a6ea8715
  - section:prerequisites:aab9d3238535
  - section:purpose:59a3799ce976
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:3628868d85ec
  - section:target-audience:f138b329cd22
  - section:usage-type:4d29c40edb03
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0072-dozzle/policy.md
  - docs/05.operations/11-laboratory/ops-0072-dozzle/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/dozzle/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/policy.md
  - docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/dozzle/README.md
- legacy_path: docs/05.operations/11-laboratory/ops-0072-dozzle/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 7a050ceea03710ab94556de08acc9991dddf67e3
  role: policy
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/policy.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/policy.md
  preserved_semantics:
  - section:controls:e0085e43b61d
  - section:dozzle-operations-policy:d9727a9c3352
  - section:exceptions:3b99eddcde43
  - section:overview:551a4a445758
  - section:policy-scope:fae4cfac7f97
  - section:related-documents:b7726adff5a9
  - section:review-cadence:96979f37cd70
  - section:verification:fb861cb52104
  removed_semantics: []
  active_consumers:
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0072-dozzle/guide.md
  - docs/05.operations/11-laboratory/ops-0072-dozzle/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/dozzle/README.md
  final_consumers:
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/guide.md
  - docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/dozzle/README.md
- legacy_path: docs/05.operations/11-laboratory/ops-0072-dozzle/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 8a8d402ea6f497e75750788b0171eacb1fcffac7
  role: runbook
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/runbook.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:08f9e8821952
  - section:canonical-references:7e3a8226ec07
  - section:checklist:0d71d856fdd8
  - section:dozzle-recovery-procedure:84c5185804f6
  - section:dozzle-recovery-runbook:da5d33b2668c
  - section:escalation:0e04cab97229
  - section:evidence:789ebe107614
  - section:observability-and-evidence-sources:fbc01deb61d0
  - section:overview:f94d277f5db3
  - section:procedure:5da93bd3e257
  - section:purpose:d280419be6b4
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:46a3423cf064
  - section:safe-rollback-or-recovery-procedure:7e312250ccf4
  - section:steps:18a8fa2ca5fe
  - section:verification-steps:a82e9a5d0a1e
  - section:when-to-use:a75ffe240ca9
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0072-dozzle/guide.md
  - docs/05.operations/11-laboratory/ops-0072-dozzle/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/dozzle/README.md
  - scripts/validation/check-repo-contracts.sh
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/guide.md
  - docs/05.operations/catalog/11-laboratory/ops-0072-dozzle/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/dozzle/README.md
  - scripts/validation/check-repo-contracts.sh
- legacy_path: docs/05.operations/11-laboratory/ops-0073-open-notebook/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 91003926f3731991e66b5fcef9d298e75d28c302
  role: guide
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/guide.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/guide.md
  preserved_semantics:
  - section:common-checks:c7cd979b4e8c
  - section:common-pitfalls:4aba310e547b
  - section:open-notebook-usage-guide:32f4f95c48d4
  - section:overview:a4191b210c36
  - section:prerequisites:cf57927c8101
  - section:purpose:e4f12be1f5cc
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:29427e9cf12d
  - section:target-audience:9abee23c6211
  - section:usage-type:4d29c40edb03
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0073-open-notebook/policy.md
  - docs/05.operations/11-laboratory/ops-0073-open-notebook/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/open-notebook/README.md
  final_consumers:
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/policy.md
  - docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/open-notebook/README.md
- legacy_path: docs/05.operations/11-laboratory/ops-0073-open-notebook/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 2927db07261530cee7decd6b917c93695b916502
  role: policy
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/policy.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/policy.md
  preserved_semantics:
  - section:controls:5f38cbdc2ac1
  - section:exceptions:94c394f27079
  - section:open-notebook-operations-policy:65acc8f7fc24
  - section:overview:22058d8997cf
  - section:policy-scope:22e8a97995a0
  - section:related-documents:b7726adff5a9
  - section:review-cadence:d5e1dc44d9e8
  - section:verification:cae6436a4e46
  removed_semantics: []
  active_consumers:
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0073-open-notebook/guide.md
  - docs/05.operations/11-laboratory/ops-0073-open-notebook/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/open-notebook/README.md
  final_consumers:
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/guide.md
  - docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/open-notebook/README.md
- legacy_path: docs/05.operations/11-laboratory/ops-0073-open-notebook/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: ced5de65c75fd43287c2c75d3361f50646c25a80
  role: runbook
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/runbook.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:76a81bcb935d
  - section:canonical-references:b12c1a5f1c53
  - section:checklist:e69323cada9e
  - section:escalation:a1caa8dd22b5
  - section:evidence:927baabc5b75
  - section:observability-and-evidence-sources:ff7ea975e5b2
  - section:open-notebook-recovery-procedure:5f4b4358288f
  - section:open-notebook-recovery-runbook:ec4e083f1087
  - section:overview:c59890fe7748
  - section:procedure:5da93bd3e257
  - section:purpose:241a008ead57
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:3c7fcd4212df
  - section:safe-rollback-or-recovery-procedure:cc1662416138
  - section:steps:90d66527254a
  - section:verification-steps:ac37e2e7ad5c
  - section:when-to-use:741257cd0402
  removed_semantics: []
  active_consumers:
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0073-open-notebook/guide.md
  - docs/05.operations/11-laboratory/ops-0073-open-notebook/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/open-notebook/README.md
  final_consumers:
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/guide.md
  - docs/05.operations/catalog/11-laboratory/ops-0073-open-notebook/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/open-notebook/README.md
- legacy_path: docs/05.operations/11-laboratory/ops-0074-optimization-hardening/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 3ba070199ac162521b4e4464b45b83e12e6416b4
  role: guide
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/guide.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/guide.md
  preserved_semantics:
  - section:11-laboratory-optimization-hardening-usage-guide:d9ed7cd7443f
  - section:common-checks:23daa4e37962
  - section:common-pitfalls:f5de19770bb4
  - section:overview:19f7283ec27b
  - section:prerequisites:24c643a56520
  - section:purpose:e6b426e87ff9
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:6184a15407e1
  - section:target-audience:e73f11b8bb7b
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0022-laboratory-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0025-laboratory-optimization-hardening-architecture.md
  - docs/03.specs/spec-0012-laboratory/spec.md
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0074-optimization-hardening/policy.md
  - docs/05.operations/11-laboratory/ops-0074-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0022-laboratory-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0025-laboratory-optimization-hardening-architecture.md
  - docs/03.specs/spec-0012-laboratory/spec.md
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/policy.md
  - docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/11-laboratory/ops-0074-optimization-hardening/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 0379a04b5e333dc5735089ffbc05d718679ee70d
  role: policy
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/policy.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/policy.md
  preserved_semantics:
  - section:11-laboratory-optimization-hardening-operations-policy:619cf10f7c8f
  - section:catalog-expansion-approval-gates:c512e511e47d
  - section:controls:1a3fe2a411b2
  - section:exceptions:5458c81684cd
  - section:overview:f802a9729933
  - section:policy-scope:8ef14f7af45a
  - section:related-documents:b7726adff5a9
  - section:review-cadence:cc52cf38347f
  - section:verification:82003c60e54e
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0022-laboratory-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0025-laboratory-optimization-hardening-architecture.md
  - docs/03.specs/spec-0012-laboratory/spec.md
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0074-optimization-hardening/guide.md
  - docs/05.operations/11-laboratory/ops-0074-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0022-laboratory-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0025-laboratory-optimization-hardening-architecture.md
  - docs/03.specs/spec-0012-laboratory/spec.md
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/guide.md
  - docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/11-laboratory/ops-0074-optimization-hardening/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 59de2e2f9218a1e90bf331d0c12c68ed55e7ace3
  role: runbook
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/runbook.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/runbook.md
  preserved_semantics:
  - section:11-laboratory-optimization-hardening-procedure:0e8dc78738e8
  - section:11-laboratory-optimization-hardening-runbook:154ee4b89d43
  - section:agent-operations-if-applicable:0c9c1dc00061
  - section:canonical-references:b62cd5e97be4
  - section:checklist:177be37b38e5
  - section:escalation:5370d9ef6273
  - section:evidence:f6f9d3228b3b
  - section:observability-and-evidence-sources:4eae19b6fe1f
  - section:overview:22121908f8ce
  - section:procedure:5da93bd3e257
  - section:purpose:4bb6e3d15432
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:42697566aa9a
  - section:safe-rollback-or-recovery-procedure:d306c894c769
  - section:steps:760713c1e459
  - section:verification-steps:a45c479ffa42
  - section:when-to-use:cee88dc81288
  removed_semantics: []
  active_consumers:
  - docs/01.requirements/prd-0022-laboratory-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0025-laboratory-optimization-hardening-architecture.md
  - docs/03.specs/spec-0012-laboratory/spec.md
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0074-optimization-hardening/guide.md
  - docs/05.operations/11-laboratory/ops-0074-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/01.requirements/prd-0022-laboratory-optimization-hardening.md
  - docs/02.architecture/descriptions/ad-0025-laboratory-optimization-hardening-architecture.md
  - docs/03.specs/spec-0012-laboratory/spec.md
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/guide.md
  - docs/05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/11-laboratory/ops-0075-portainer/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 9b1f42805e42c392967502a9f1dd3b1c8a3e641f
  role: guide
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0075-portainer/guide.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0075-portainer/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0075-portainer/guide.md
  preserved_semantics:
  - section:1-initial-admin-setup:17b8d3fc43af
  - section:2-managing-containers:1f55e2c7afe2
  - section:3-stack-deployment:122d2024af58
  - section:best-practices:9046e0c40597
  - section:common-checks:e6f61182278d
  - section:common-pitfalls:685e01e06f28
  - section:overview:8f7c12a347fc
  - section:portainer-usage-guide:cfab5ac385e3
  - section:prerequisites:872b84f8fb8b
  - section:purpose:3a77c36a08bf
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:9c20e5ca273f
  - section:target-audience:089658ef5a70
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0075-portainer/policy.md
  - docs/05.operations/11-laboratory/ops-0075-portainer/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/portainer/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0075-portainer/policy.md
  - docs/05.operations/catalog/11-laboratory/ops-0075-portainer/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/portainer/README.md
- legacy_path: docs/05.operations/11-laboratory/ops-0075-portainer/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: c3f2887dcf39ea30b20c16de71d52ce0292712a7
  role: policy
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0075-portainer/policy.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0075-portainer/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0075-portainer/policy.md
  preserved_semantics:
  - section:controls:6b8cc1501ffe
  - section:disallowed-actions:e1725d84bea1
  - section:exceptions:4db2d9e28b64
  - section:overview:28257067f45f
  - section:policy-scope:d059000e4cc0
  - section:portainer-operations-policy:5a5475c2137d
  - section:related-documents:b7726adff5a9
  - section:review-cadence:a383dba6076f
  - section:verification:6a7940cdb430
  removed_semantics: []
  active_consumers:
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0075-portainer/guide.md
  - docs/05.operations/11-laboratory/ops-0075-portainer/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/portainer/README.md
  final_consumers:
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0075-portainer/guide.md
  - docs/05.operations/catalog/11-laboratory/ops-0075-portainer/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/portainer/README.md
- legacy_path: docs/05.operations/11-laboratory/ops-0075-portainer/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 12dc5069b626babb7c6fc701548ba19d250bc7b0
  role: runbook
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0075-portainer/runbook.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0075-portainer/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0075-portainer/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:6c3ae3db7570
  - section:canonical-references:2ca048d9be93
  - section:checklist:b04166107f1d
  - section:escalation:0681b7d19a66
  - section:evidence:aaf52d7938c6
  - section:observability-and-evidence-sources:d08fdaf96b90
  - section:overview:d7464f3c10af
  - section:portainer-recovery-procedure:47072b561f45
  - section:portainer-recovery-runbook:e127ad0cd91b
  - section:procedure:5da93bd3e257
  - section:purpose:357282323620
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:736c444ae10c
  - section:safe-rollback-or-recovery-procedure:bd1e27327dad
  - section:steps:8352a80535de
  - section:verification-steps:85fa28783ec0
  - section:when-to-use:e787714c3c43
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0075-portainer/guide.md
  - docs/05.operations/11-laboratory/ops-0075-portainer/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/portainer/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0075-portainer/guide.md
  - docs/05.operations/catalog/11-laboratory/ops-0075-portainer/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/portainer/README.md
- legacy_path: docs/05.operations/11-laboratory/ops-0076-redisinsight/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: e9c4ea5585fddae76a53a28786453ada2e6687cf
  role: guide
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/guide.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/guide.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/guide.md
  preserved_semantics:
  - section:1-connection-setup:9fc0b3185c23
  - section:2-key-analysis-browser:059a3af5bf0f
  - section:3-using-profiler:590cac81b4a1
  - section:best-practices:20e14389242f
  - section:common-checks:746e42cb933e
  - section:common-pitfalls:7f7c44e8f41a
  - section:overview:bbda3be01336
  - section:prerequisites:872b84f8fb8b
  - section:purpose:3a77c36a08bf
  - section:redisinsight-usage-guide:1b9c59656aee
  - section:related-documents:864fe5dd05d8
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:9c20e5ca273f
  - section:target-audience:089658ef5a70
  - section:usage-type:d7a49acb2eb4
  - section:usage:63bfd61a0561
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0076-redisinsight/policy.md
  - docs/05.operations/11-laboratory/ops-0076-redisinsight/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/redisinsight/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/policy.md
  - docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/redisinsight/README.md
- legacy_path: docs/05.operations/11-laboratory/ops-0076-redisinsight/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 86ff0844c24068595cce97d8290f129bf5529ce6
  role: policy
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/policy.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/policy.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/policy.md
  preserved_semantics:
  - section:controls:7ad10f328022
  - section:disallowed-actions:1b6120ff8983
  - section:exceptions:4db2d9e28b64
  - section:overview:07f4e8cb345b
  - section:policy-scope:650266be1b89
  - section:redisinsight-operations-policy:afad142614b7
  - section:related-documents:b7726adff5a9
  - section:review-cadence:5317cf08eac8
  - section:verification:fa9541d0361c
  removed_semantics: []
  active_consumers:
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0076-redisinsight/guide.md
  - docs/05.operations/11-laboratory/ops-0076-redisinsight/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/redisinsight/README.md
  final_consumers:
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/guide.md
  - docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/redisinsight/README.md
- legacy_path: docs/05.operations/11-laboratory/ops-0076-redisinsight/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: a9304bc10226117b672b09ef4aad9e003935197c
  role: runbook
  catalog_path: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/runbook.md
  final_path: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/runbook.md
  semantic_action: retain
  canonical_role_owner: docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/runbook.md
  preserved_semantics:
  - section:agent-operations-if-applicable:6fb71d1e4276
  - section:canonical-references:a5396e3361cb
  - section:checklist:22938158bf27
  - section:escalation:479677f0ca3c
  - section:evidence:eac12fc2718a
  - section:observability-and-evidence-sources:3c2b1d20d341
  - section:overview:909a2f6f0397
  - section:procedure:5da93bd3e257
  - section:purpose:186e36411aa5
  - section:redisinsight-recovery-procedure:5b1b98a77b1f
  - section:redisinsight-recovery-runbook:f6384854bf00
  - section:related-documents:295cb48a66e8
  - section:rollback-or-recovery:d1a08e6c0272
  - section:safe-rollback-or-recovery-procedure:d888d7243f7d
  - section:steps:129cd7400d11
  - section:verification-steps:90622ba17e84
  - section:when-to-use:0a8252ef1216
  removed_semantics: []
  active_consumers:
  - docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  - docs/05.operations/11-laboratory/README.md
  - docs/05.operations/11-laboratory/ops-0076-redisinsight/guide.md
  - docs/05.operations/11-laboratory/ops-0076-redisinsight/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/redisinsight/README.md
  final_consumers:
  - docs/05.operations/catalog/00-workspace/ops-0006-infrastructure-optimization-governance/policy.md
  - docs/05.operations/catalog/11-laboratory/README.md
  - docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/guide.md
  - docs/05.operations/catalog/11-laboratory/ops-0076-redisinsight/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - infra/11-laboratory/redisinsight/README.md
- legacy_path: docs/05.operations/12-infra-net/README.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 1df8b720bf4d85f5de6ad73d2c57a6bc7f2f22a7
  role: domain-readme
  catalog_path: docs/05.operations/catalog/12-infra-net/README.md
  final_path: docs/05.operations/catalog/12-infra-net/README.md
  semantic_action: retain
  canonical_role_owner: null
  preserved_semantics:
  - section:audience:8ed0837451b9
  - section:how-to-work-in-this-area:bf17b61b3f43
  - section:operations-12-infra-net:b84a6c0603ec
  - section:overview:77563932d188
  - section:related-documents:2b840419baf3
  - section:scope:9806d2f2be78
  - section:structure:421d077d8bbe
  removed_semantics: []
  active_consumers:
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
  final_consumers:
  - docs/05.operations/README.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - docs/99.templates/support/document-metadata-profiles.yaml
- legacy_path: docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/guide.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 8dd211dd61f54a9743a70d973a73f4830d6f7f00
  role: guide
  catalog_path: docs/05.operations/catalog/12-infra-net/ops-0077-standardize-infra-net/guide.md
  final_path: docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/guide.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/guide.md
  preserved_semantics:
  - section:0012-standardize-infra-net-usage-guide:6d1596ed7d6a
  - section:common-checks:047f21e77568
  - section:common-pitfalls:399f9b11debb
  - section:overview:7a31be3a925b
  - section:prerequisites:b6dc46b5b72e
  - section:purpose:77506b7c68e1
  - section:related-documents:81f307214b3e
  - section:runbook-handoff:a6f4d9784508
  - section:step-by-step-instructions:68e25b224d80
  - section:target-audience:089658ef5a70
  - section:usage-type:4d29c40edb03
  - section:usage:63bfd61a0561
  - text:baseline-body:이 문서는 모든 인프라 서비스에 `infra_net` 공통 네트워크와 고정 IP를 할당하는 가이드다. 프로젝트의 일관성을 유지하기 위해 표준 딕셔너리 기반의 네트워크 정의 방식을 따른다.
  removed_semantics:
  - stale:legacy-subject-path:ops-0077-standardize-infra-net
  active_consumers:
  - docs/03.specs/spec-0098-standardize-infra-net/spec.md
  - docs/05.operations/12-infra-net/README.md
  - docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/policy.md
  - docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/03.specs/spec-0098-standardize-infra-net/spec.md
  - docs/05.operations/catalog/12-infra-net/README.md
  - docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/policy.md
  - docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/policy.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: 4e32e8521e7ab4ea2e70c7c9b5eeb69ef81319f5
  role: policy
  catalog_path: docs/05.operations/catalog/12-infra-net/ops-0077-standardize-infra-net/policy.md
  final_path: docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/policy.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/policy.md
  preserved_semantics:
  - section:controls:68ba560854a9
  - section:exceptions:3f9ae9a7a107
  - section:infra-net-ip-management-operations-policy:82d73fa970ac
  - section:overview:c63b4a75ff4b
  - section:policy-scope:b0d32df5e961
  - section:related-documents:93013220ad0f
  - section:review-cadence:b562d599d317
  - section:verification:7837b6a780c4
  - text:baseline-body:모든 서비스의 `networks` 항목에 `ipv4_address` 속성 필수 부여.
  removed_semantics:
  - stale:legacy-subject-path:ops-0077-standardize-infra-net
  active_consumers:
  - docs/03.specs/spec-0098-standardize-infra-net/spec.md
  - docs/05.operations/12-infra-net/README.md
  - docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/guide.md
  - docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  final_consumers:
  - docs/03.specs/spec-0098-standardize-infra-net/spec.md
  - docs/05.operations/catalog/12-infra-net/README.md
  - docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/guide.md
  - docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/runbook.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
- legacy_path: docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/runbook.md
  source_commit: 6f2703d8d245cf4e3576bece0bf247dd516b2bf3
  source_blob: eddd2a26741411b6fc0cfeabce4cd2049827ec40
  role: runbook
  catalog_path: docs/05.operations/catalog/12-infra-net/ops-0077-standardize-infra-net/runbook.md
  final_path: docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/runbook.md
  semantic_action: rewrite
  canonical_role_owner: docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/runbook.md
  preserved_semantics:
  - section:0012-standardize-infra-net-runbook:73c0f5f9190f
  - section:agent-operations-if-applicable:8905ad971519
  - section:canonical-references:9a062bf77140
  - section:checklist:274daad81c0b
  - section:escalation:5370d9ef6273
  - section:evidence:483a83285c03
  - section:evidence:8e5d5bf07275
  - section:infra-net-ip-mapping-validation-and-update-procedure:2e66cff4d1ad
  - section:overview:012e30121efd
  - section:procedure:5da93bd3e257
  - section:purpose:7e368d3082b0
  - section:related-documents:ecafca2dbb78
  - section:rollback-or-recovery:036fa8c1a203
  - section:safe-rollback-or-recovery-procedure:7be608cb5840
  - section:steps:8522e628bcf8
  - section:verification-steps:283ef387e2bf
  - section:when-to-use:6319a6c9858e
  - text:baseline-body:서비스의 `networks` 설정을 표준 딕셔너리 포맷으로 전환할 때.
  removed_semantics:
  - stale:legacy-subject-path:ops-0077-standardize-infra-net
  active_consumers:
  - docs/03.specs/spec-0098-standardize-infra-net/spec.md
  - docs/05.operations/12-infra-net/README.md
  - docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/guide.md
  - docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/validation/check-repo-contracts.sh
  final_consumers:
  - docs/03.specs/spec-0098-standardize-infra-net/spec.md
  - docs/05.operations/catalog/12-infra-net/README.md
  - docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/guide.md
  - docs/05.operations/catalog/12-infra-net/ops-0077-ip-address-management/policy.md
  - docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  - scripts/validation/check-repo-contracts.sh
approval:
  status: approved
  approved_at: '2026-08-13'
  approved_by: user
```

## Preserved Evidence

- Each subject row pins its exact source commit and tree object.
- Each file row pins its exact source commit and blob object, role, structural
  path, proposed final owner, section-level preservation tokens, removed
  predecessor-boundary tokens, and resolved active Markdown consumers.
- Recovery is `git show <source_commit>:<legacy_path>` for files and
  `git archive <source_commit> <legacy_subject_path>` for subject trees.
- The user approved this exact 77-row table on 2026-08-13. Structural and
  semantic execution remains limited to the subsequent Plan tasks and must pass
  the corresponding `structure`, `executed`, or `complete` validation mode.

## Structural Execution Evidence

Task 10C executed the approved structure boundary on 2026-08-13. The manifest
approval remains `approved`; no `legacy_*`, `source_*`, `final_path`,
`semantic_action`, merge, or semantic-preservation field in the frozen YAML
ledger changed.

- RED: the three live-topology tests produced 14 assertion failures: one absent
  `catalog/` root and all 13 legacy domain roots still present. The Incident and
  Release sibling assertion already passed.
- Move: exactly 13 native `git mv` commands moved `00-workspace` through
  `12-infra-net` in numeric order beneath `docs/05.operations/catalog/`.
- Structural inventory: 13 catalog domains, the same 77 subject IDs and
  structural names, 192 role files, and zero Incident or Release roots beneath
  `catalog/`.
- Consumer boundary: the approved rows select 342 unique active/final consumer
  routes. The structural rewrite updated 753 explicit legacy-prefix occurrences
  across 271 non-test, non-generated current files; moved Markdown required 784
  relative-link rebases across 205 files. Path-aware tests were migrated
  separately, and the two registered LLM Wiki outputs were regenerated from
  their canonical owner.
- Immutable exclusions: `archived_from`, legacy/source paths and Git objects in
  migration ledgers, completed Stage 98 evidence and tombstone provenance,
  immutable Stage 90 manifests/summaries, and Stage 00 progress history were not
  rewritten. Only the two manifest-declared current Stage 90 generated outputs
  changed.
- Initial GREEN: the three structural tests pass, structure mode reports
  `subjects=77 files=205 approval=approved`, and alignment reports 335 documents,
  2,349 links, and zero failures.
- Final structural equivalence: complete Operations catalog validation passes
  `37/37` in `305.262s`; Operations taxonomy passes `12/12`; traceability and
  alignment each report 335 documents, 2,349 links, and zero failures. An exact
  role-body comparison found all 192 current role files byte-identical to their
  pinned predecessors after neutralizing only approved path and Markdown-link
  destination rebases.
- Metadata and owner gates: changed metadata reports `selected=251
  violations=0`; metadata contracts report `violations=0`; the focused
  script-manifest consumers pass `2/2`; both registered LLM Wiki outputs are
  fresh. The single full metadata run reached `244/245`; its only failure was a
  root README Release-link label changed during routing reduction. Restoring the
  preserved label made the exact failure plus the three structural metadata
  regressions pass `4/4`. Ruff, `py_compile`, and diff hygiene pass.
- Review round 1: the initial general review reported `C0/I2/M0` for the catalog
  Runbook authority classifier and immutable Stage 98 tombstone expectations.
  The mandatory Python review reported `C0/I3/M0` for structure-body
  preservation, unsafe semantic normalization, and the two active governance
  publications. There was no overlap: five unique Important findings. RED reproduced the full
  script-manifest suite at `40` tests / `10` failures and eight focused failures:
  three structural body mutations, four unsafe Markdown targets, and the active
  publication scan naming exactly `git-workflow.md` and
  `github-governance.md`.
- Remediation GREEN: runtime authority accepts only the canonical
  `catalog/<domain>/ops-####-<slug>/runbook.md` leaf shape; the seven predecessor-era
  target values across six affected tombstone rows retain immutable equality;
  structure mode now compares
  every pinned source body exactly after only the approved 13 domain-prefix and
  safe link rebases; arbitrary addition, removal, and rewrite fail; absolute,
  traversal, backslash, and encoded-control targets fail closed. The two active
  Stage 00 publications use `catalog/00-workspace`. Focused remediation is `6/6`,
  full script manifest is `41/41` in `31.970s`, full Operations catalog is
  `40/40` in `378.385s`, and structure mode remains `77` subjects / `205` files /
  `approved`.
- Final remediation gates: Operations taxonomy `12/12`; traceability and
  alignment each 335 documents / 2,349 links / zero failures; changed metadata
  `253/0`; metadata contracts `0`; Ruff, `py_compile`, and all diff checks pass.
  The independent general reviewer reran full metadata after the Release-label
  restoration and reported `245/245` GREEN; remediation did not rerun that long
  suite because no metadata behavior changed.
- Round 1 partial re-review: general review reported all general findings
  addressed (`C0/I0/M0`); Python re-review reported `C0/I1/M0` because
  executed/complete `_semantic_section_tokens` still canonicalized unsafe
  Markdown targets.
- Round 2 RED/GREEN: the original executed fixture replaced its real relative
  Operations README link with four unsafe variants. Absolute `/docs/...`
  produced zero findings; traversal, backslash, and encoded-C0 destinations
  produced only a generic preservation mismatch and no deterministic unsafe
  finding. Shared semantic normalization now returns an unsafe-target flag,
  emits `semantic-link-invalid`, and also fails preservation for unsafe source or
  target links while retaining the valid relative approved rebase. Focused
  final executed/complete semantic coverage passes `4/4` in `77.810s`; Ruff,
  `py_compile`, and all diff checks pass.
- Final review and commit: general and Python re-reviews are both FINAL APPROVED
  (`C0/I0/M0`); all five unique Important findings are addressed. The controller
  recorded logical commit `548154b878ae62b50fddc4b2b4aea7b1b78f9176`
  (`docs: move operations domains under catalog`). Task 10D is the next bounded
  handoff and may execute only the approved semantic slice for catalog domains
  `00-workspace` through `03-security`.

## Semantic Execution Evidence: Domains 00 Through 03

Task 10D executed only the user-approved manifest slice for `00-workspace`
through `03-security` on 2026-08-14. The frozen YAML ledger, approval,
provenance objects, and semantic dispositions above remain unchanged.

- Slice boundary: 16 subjects and 33 role/index files; subject dispositions are
  12 retain, 3 rename, and 1 merge. File dispositions are 22 retain, 10
  evidence-bounded rewrite, and 1 merge. Eleven file rows declare approved
  removed semantics.
- RED: the exact live-slice test initially reported 11 findings: 3 missing final
  subjects, 4 missing final role files, 3 missing final consumers, and 1 stale
  consumer. Separate mutation REDs showed that executed mode did not reject a
  structural catalog predecessor and did not enforce `removed_semantics`.
- Native moves: `ops-0002-developer-setup` became
  `ops-0002-developer-environment`; `ops-0006-infra-service-optimization-catalog`
  became `ops-0006-infrastructure-optimization-governance`; `ops-0012-setup`
  became `ops-0012-edge-routing-stack`; and the `ops-0005` Runbook moved into
  canonical subject `ops-0004-harness-agent-first-engineering`. No copy/delete
  emulation or separate `git rm` was used.
- Merge preservation: the sole moved source role was captured before canonical
  normalization at `/tmp/task10d-ops0005-merge-source.tar`; it contains exactly
  `docs/05.operations/catalog/00-workspace/ops-0005-harness-agent-first-engineering-validation/runbook.md`
  and has SHA-256
  `12d12f52c15a4535ceedf23de835426acf72658d3e8204d13ab5fc6399bc8672`.
  The canonical Runbook retains the source trigger-through-escalation procedure
  while removing the approved duplicate overview and validator boilerplate.
- Semantic convergence: all 11 approved retained/merged role rewrites were
  applied, including current non-secret evidence for the two comparison guides,
  co-located Plan/Task routing, canonical Guide/Policy/Runbook handoffs, and the
  approved legacy-role/root removals. Incident and Release packets were not
  touched.
- Consumers and generated evidence: 86 distinct manifest-declared final
  consumer paths were reconciled for the slice. The two registered current LLM
  Wiki outputs were regenerated by their canonical generator and pass freshness.
  Immutable Stage 90/98 evidence and the predecessor-era tombstone replacement
  fixture remain unchanged; the Operations validator excludes only that named
  immutable fixture block from active stale-path scanning.
- Validator conflict repair: executed mode now rejects both legacy and
  structural predecessors, proves every non-removed frozen section, and rejects
  each explicitly approved removed semantic when it remains. The Operations
  taxonomy derives current paths from the typed Task 10B manifest instead of a
  Task 10C-only hard-coded subject list.
- GREEN: executed mode passes for domains 00--03; Operations taxonomy first
  passed `12/12`, and the later canonical merged-role ID correction passes its
  exact focused regression `1/1`; alignment and traceability each report 335
  documents, 2,350 links, and zero failures; changed metadata reports `24/0`;
  metadata contracts report zero; script manifest passes `41/41`; both generated
  outputs are fresh; and Ruff, `py_compile`, and staged/unstaged diff hygiene
  pass.
- Review remediation: initial independent review reported general `C0/I1` and
  Python `C0/I2`, with the non-ASCII/whole-section preservation defect
  overlapping and the paraphrased contradiction bypass distinct (`I2` unique).
  Exact RED mutations removed the Korean `## 키 카테고리 현황` section, the
  valid tracked-key statement, the renamed `ops-0002` H1, and canonical Runbook
  observability evidence, then added an English 325-key/three-key contradiction;
  all five initially escaped. GREEN replaces ASCII-only identities and broad
  section exemptions with Unicode-preserving exact section tokens, typed
  per-label source rewrites, required final witnesses, paraphrase-resistant
  forbidden invariants, canonical renamed H1 enforcement, and unknown-label
  fail-closed validation.
- Validator publication-guard remediation: a second strict RED proved the new
  exact source witnesses themselves matched the active legacy-publication scan.
  GREEN represents the frozen paths as structured immutable `PurePosixPath`
  components; an appended active legacy route in the same validator file still
  fails, so no file- or section-wide scan exclusion was introduced.
- Full Operations evidence: an intermediate full run passed 45 of 46 tests and
  isolated only that validator-source publication false positive. After its
  focused RED/GREEN repair, the one authorized final authoritative run passes
  `47/47` in `335.595s`. Executed mode passes for domains 00--03; taxonomy passes
  `12/12`; traceability and alignment each report 335 documents, 2,350 links,
  and zero failures; changed metadata is `24/0`; metadata contracts are zero;
  script manifest is `41/41`; direct registered LLM Wiki output freshness,
  Ruff, `py_compile`, and diff hygiene pass.
- Bounded generator aggregate: the registered all-generator check remained
  silent through the exact 12-minute cutoff. It was interrupted once with exit
  `130`; its aggregate result is unverified and it was not restarted. The
  direct owner check for both Task 10D-generated LLM Wiki outputs is GREEN.
- Round 1 scoped re-review: general review is APPROVED (`C0/I0`); Python review
  retained one Important (`C0/I1`) because a known approved semantic label with
  no implemented exact rewrite rule was silently skipped. That gap is distinct
  from the manifest-level unknown-label rejection.
- Round 2 RED/GREEN: a selected synthetic `04-data` execution initially
  produced no findings despite its later-slice labels having no exact Task 10E
  rules. The persistent RED expected `semantic-rewrite-rule-missing`. GREEN
  returns each missing known non-`remove-text` label from the exact dispatcher,
  marks preservation invalid, and emits the dedicated deterministic finding. Focused missing-rule,
  unknown-label, prior semantic-mutation, and approved 00--03 coverage passes
  `4/4` in `26.508s`; no Task 10E rule or corpus file was changed.
- Round 2 Python re-review: one Important remained (`C0/I1`). The dispatcher
  skipped `remove-text:` before exact-rule resolution, while semantic
  tokenization removed its fragment. Replacing 40 of 51 `04-data` rewrite
  labels with `remove-text:approved:<exact source H1>` therefore let those 40
  rows escape missing-rule and preservation findings.
- Round 3 RED/GREEN: the approved manifest has zero `remove-text:` labels. A
  persistent path-scoped RED reproduced all 40 reviewer mutations; manifest
  REDs additionally covered heading, full-section, path-only, and metadata
  fragments. GREEN removes the unconditional skip, requires an exact
  disposition-bound typed handler for every removal, emits
  `semantic-rewrite-rule-missing` for absent executed rules, and rejects
  unbound/structural `remove-text:` mutations with `remove-text-rule-missing`
  and `remove-text-fragment-invalid`. Final focused coverage passes `6/6` in
  `18.670s`; executed 00--03, Ruff, `py_compile`, and diff hygiene pass. No Task
  10E rule or corpus file was changed.
- Final review: general review is FINAL APPROVED (`C0/I0/M0`) and Python review
  is FINAL APPROVED (`C0/I0/M0`) after three remediation rounds. The unique
  initial `I2` and both later Python fail-open `I1` carries are resolved. The
  authoritative Operations result remains `47/47` in `335.595s`; the registered
  all-generator aggregate remains explicitly unverified after its exact
  12-minute cutoff and single interruption with exit `130`.
- Logical commit: `cb117edd109a217d89e4e97a0640b5c9c00b7492`
  (`docs: converge operations catalog domains 00 through 03`). The frozen YAML
  ledger, provenance objects, approval, and semantic dispositions remain
  unchanged. Recovery remains the one-entry archive
  `/tmp/task10d-ops0005-merge-source.tar` with SHA-256
  `12d12f52c15a4535ceedf23de835426acf72658d3e8204d13ab5fc6399bc8672`.
- Handoff status: `FINAL APPROVED AND COMMITTED`. Task 10E is the next bounded
  semantic slice and may consume only approved domains 04--06 rows.

## Related Documents

- [Stage authoring matrix](../../00.agent-governance/policies/stage-authoring-matrix.md)
