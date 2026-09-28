---
title: "Document Language Migration"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0187-TSK-0001"
parent_ids:
- "SPEC-0187"
- "SPEC-0187-PLAN-0001"
created: "2026-09-28"
---

# Document Language Migration

## Objective

Execute W1 through W9 of the [Plan](../plan.md) and record the evidence for
every acceptance criterion of [SPEC-0187](../spec.md).

## Inputs

- The SPEC-0184 Task, Deferred Items, P2 entry.
- The owner's choice of 2026-09-28: P2 after P3, with Spec and Plan approval
  before any translation, subagent translation by area, and a humanize-korean
  pass for Korean output.
- Baseline: the local `main` at `a406430b2`.

### Measured Set

Measured on 2026-09-28 at `a406430b2` with `language_mismatch` over every
non-README document whose profile declares a language: 200 documents.

| Document | Profile | Direction | Unit |
| --- | --- | --- | --- |
| `.github/repository-surface.md` | `repository-readme` | English to Korean | W7 |
| `docs/01.requirements/0001-gateway.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0002-auth.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0003-security.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0004-data.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0005-data-analytics.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0006-messaging.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0007-observability.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0008-workflow.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0009-ai.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0010-tooling.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0011-communication.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0012-laboratory.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0013-ai-open-webui.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0023-standardize-infra-net.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0024-agent-governance-standardization.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0025-operational-readiness-closure.md` | `requirements-package` | Korean to English | W2 |
| `docs/01.requirements/0027-home-development-host.md` | `requirements-package` | Korean to English | W2 |
| `docs/02.architecture/decisions/0001-traefik-nginx-hybrid.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0003-vault-as-secrets-manager.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0004-postgresql-ha-patroni.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0006-lgtm-stack-selection.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0008-ollama-openwebui-local-ai.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0009-tooling-services.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0010-communication-services.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0011-laboratory-services.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0016-open-webui-implementation.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0017-auth-hardening-runtime-and-fail-closed.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0026-standardize-infra-net.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0028-local-isolated-readiness-evidence.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0032-canonical-agent-governance-home.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0038-selective-native-oidc-for-native-auth-apps.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0039-analytics-engines-after-lakehouse-convergence.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0040-data-hardening-gate-and-staged-expansion.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0041-offsite-backup-target.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0042-openbao-unseal-method.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/decisions/0043-operations-role-layout.md` | `adr` | Korean to English | W3 |
| `docs/02.architecture/descriptions/0001-gateway-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0002-auth-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0004-data-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0006-observability-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0007-workflow-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0008-ai-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0009-tooling-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0012-data-analytics-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0013-open-webui-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0018-security-optimization-hardening-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0019-data-optimization-hardening-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0020-messaging-optimization-hardening-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0021-observability-optimization-hardening-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0022-workflow-optimization-hardening-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0023-ai-optimization-hardening-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0024-tooling-optimization-hardening-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0025-laboratory-optimization-hardening-architecture.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0027-agent-governance-canonical-adapter.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0028-operational-readiness-closure.md` | `architecture-description` | Korean to English | W4 |
| `docs/02.architecture/descriptions/0031-home-development-host.md` | `architecture-description` | Korean to English | W4 |
| `docs/05.operations/guides/0004-harness-agent-first-engineering.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0012-edge-routing-stack.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0017-influxdb.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0019-opensearch.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0021-backup-and-restore.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0022-valkey-cluster.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0024-seaweedfs.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0028-management-database.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0029-supabase.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0030-data-optimization-hardening.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0036-kafka.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0037-messaging-optimization-hardening.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0041-grafana.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0042-lgtm-stack.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0043-loki.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0045-prometheus.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0047-pyroscope.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0049-tempo.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0051-airflow-dag-lifecycle.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0061-k6.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0062-locust.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0065-registry.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0066-sonarqube.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0069-terrakube.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0070-mail.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0072-dozzle.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0073-open-notebook.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0076-redisinsight.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0080-surrealdb.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0081-comfyui.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0082-opentofu.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0083-renovate.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0084-mailpit.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0085-openbao.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0087-gatus.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0088-mlflow.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0089-jupyterlab.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0090-dbt.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0091-crawl4ai.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0092-wiremock.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0093-pact-broker.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0094-lakehouse.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0095-conftest.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0096-k8s-integration.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/guides/0097-superset.md` | `guide` | English to Korean | W5 |
| `docs/05.operations/policies/0004-harness-agent-first-engineering.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0017-influxdb.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0019-opensearch.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0021-backup-and-restore.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0022-valkey-cluster.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0024-seaweedfs.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0025-cassandra.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0026-couchdb.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0027-mongodb.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0028-management-database.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0029-supabase.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0030-data-optimization-hardening.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0031-postgresql-cluster.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0033-neo4j.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0034-qdrant.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0036-kafka.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0037-messaging-optimization-hardening.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0045-prometheus.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0049-tempo.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0052-airflow-dag-lifecycle.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0061-k6.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0062-locust.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0065-registry.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0066-sonarqube.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0069-terrakube.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0070-mail.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0072-dozzle.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0073-open-notebook.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0076-redisinsight.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0080-surrealdb.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0081-comfyui.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0082-opentofu.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0083-renovate.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0084-mailpit.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0085-openbao.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0086-dependency-version-management.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0087-gatus.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0088-mlflow.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0089-jupyterlab.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0090-dbt.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0091-crawl4ai.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0092-wiremock.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0093-pact-broker.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0094-lakehouse.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0095-conftest.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0096-k8s-integration.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/policies/0097-superset.md` | `policy` | English to Korean | W6 |
| `docs/05.operations/runbooks/0004-harness-agent-first-engineering.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0017-influxdb.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0019-opensearch.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0021-backup-and-restore.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0022-valkey-cluster.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0024-seaweedfs.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0028-management-database.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0029-supabase.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0030-data-optimization-hardening.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0032-postgresql-logical-upgrade-restore-rehearsal.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0035-storage-exhaustion.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0036-kafka.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0037-messaging-optimization-hardening.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0041-grafana.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0061-k6.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0062-locust.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0065-registry.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0066-sonarqube.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0069-terrakube.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0070-mail.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0072-dozzle.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0073-open-notebook.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0076-redisinsight.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0080-surrealdb.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0081-comfyui.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0082-opentofu.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0083-renovate.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0084-mailpit.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0085-openbao.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0086-dependency-version-management.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0087-gatus.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0088-mlflow.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0089-jupyterlab.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0090-dbt.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0091-crawl4ai.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0092-wiremock.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0093-pact-broker.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0094-lakehouse.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0095-conftest.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0096-k8s-integration.md` | `runbook` | English to Korean | W7 |
| `docs/05.operations/runbooks/0097-superset.md` | `runbook` | English to Korean | W7 |

## Work Log

- 2026-09-28: Spec, Plan, and Task drafted on branch
  `docs/document-language-migration`.
- 2026-09-29: The owner approved the Spec and Plan. Execution runs on the
  branch while the package stays `draft` against `main`; promotion follows the
  local `main` merge.
- 2026-09-29: W1 recorded the measured set below Inputs and the pre-change
  gate summaries.

## Verification Evidence

Not started.

## Review Evidence

None yet.

## Commit Ledger

None yet.

## Rulings

- 2026-09-29: Owner approved the Spec and Plan ("승인").

## Deferred Items

None yet.
