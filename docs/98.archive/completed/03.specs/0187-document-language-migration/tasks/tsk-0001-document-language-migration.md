---
title: "Document Language Migration"
version: "0.4.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-29"
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
- 2026-09-29: W2-W7 ran as 27 translation batches (B01-B27) with doc-writer
  subagents, then 36 humanize-korean monolith runs (2026-09-29-001..036) over
  the Korean-target batches.
- 2026-09-29: The PreToolUse hook denied every Write to the session
  scratchpad, which blocked humanize output. The owner fixed the hook and added
  scratchpad allow rules (`54741b2d5`).
- 2026-09-29: A scan for English sentences in the Korean-target set and for
  Hangul in the English-target set found remnants; a cleanup pass translated
  them.
- 2026-09-29: W8 widened `--mode language` to the corpus and removed the
  lifecycle body filter. W9 reran the gate members and both unit suites.

## Verification Evidence

Structure tokens were compared per document against `main` with a scratch
script outside the repository: frontmatter other than `version` and `updated`,
a patch `version` bump, fenced blocks, inline code (multi-line spans
normalized), link targets, bare URLs, identifiers (ASCII-bounded, so a Korean
particle glued to an ID still counts), heading levels, registered headings, and
table shapes. Every one of the 200 documents passed, except GDE-0087, whose one
link target was corrected on purpose. W1 and W9 ran the twelve changed-profile
members except `check-conftest-policy.sh`, which runs `docker compose` and is
outside this request.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: 200 documents recorded under Inputs before any translation (`31f6921ef`) | N/A: the measured set is a one-time scope record |
| 5 | W1 | PASS: twelve members returned 0 at baseline | N/A: baseline run evidence |
| 2 | W2 | PASS: 17 Requirements packages read in English; token comparison and language check ok (`1ee018334`, `bf26f7a56`) | [Stage 01](../../../../docs/01.requirements/README.md) |
| 5 | W2 | PASS: metadata `check-changed` 0 violations after the batch | [Stage 01](../../../../docs/01.requirements/README.md) |
| 2 | W3 | PASS: 29 ADRs read in English; ADR-0038 takes a same-line history exception for evaluated versions (`d98f31ff2`, `bf26f7a56`) | [Stage 02](../../../../docs/02.architecture/README.md) |
| 5 | W3 | PASS: metadata `check-changed` 0 violations after the batch | [Stage 02](../../../../docs/02.architecture/README.md) |
| 2 | W4 | PASS: 20 architecture descriptions read in English (`ec78e49cd`, `bf26f7a56`) | [Stage 02](../../../../docs/02.architecture/README.md) |
| 5 | W4 | PASS: links `--mode all` PASS after the batch | [Stage 02](../../../../docs/02.architecture/README.md) |
| 2 | W5 | PASS: 45 guides read in Korean (`fcc256bd3`, `464dbb2f2`, `90b07dc9f`, `35a9b2232`, `c0b6f80c0`) | [Stage 05](../../../../docs/05.operations/README.md) |
| 3 | W5 | PASS: humanize runs 002-013, gates OK or WARN; every WARN was a numbered-item `heading_lost` or a split-sentence modality false positive | [Stage 05](../../../../docs/05.operations/README.md) |
| 5 | W5 | PASS: token comparison and language check ok for every guide | [Stage 05](../../../../docs/05.operations/README.md) |
| 2 | W6 | PASS: 47 policies read in Korean (`8904193b5`, `679d1292a`, `c0b6f80c0`) | [Stage 05](../../../../docs/05.operations/README.md) |
| 3 | W6 | PASS: humanize runs 014-024, gates OK | [Stage 05](../../../../docs/05.operations/README.md) |
| 5 | W6 | PASS: token comparison and language check ok for every policy | [Stage 05](../../../../docs/05.operations/README.md) |
| 2 | W7 | PASS: 41 runbooks and `.github/repository-surface.md` read in Korean (`fcc256bd3`, `1e3faef73`, `90b07dc9f`, `c0b6f80c0`) | [Stage 05](../../../../docs/05.operations/README.md) |
| 3 | W7 | PASS: humanize runs 001 and 025-036, gates OK or numbered-item WARN | [Stage 05](../../../../docs/05.operations/README.md) |
| 5 | W7 | PASS: token comparison and language check ok for every runbook | [Stage 05](../../../../docs/05.operations/README.md) |
| 4 | W8 | PASS: `LanguageModeTests` judged-profile case failed before the change and passes after; `--mode language` 971 documents, failures 0; lifecycle filter removed (`9dc9d01d0`) | [links.py](../../../../scripts/lib/document_governance/links.py) |
| 5 | W8 | PASS: lifecycle `violations=0`, metadata `check-changed` 0 violations | [documentation protocol](../../../../.agents/governance/documentation-protocol.md) |
| 6 | W8 | PASS: `test_links` and `test_heading` 156 tests OK | [links.py](../../../../scripts/lib/document_governance/links.py) |
| 5 | W9 | PASS: twelve members returned 0 (`gate fail=0`) | N/A: run evidence for this change |
| 6 | W9 | PASS: `tests/validation` 675 tests OK, 23 skipped; `tests/lib` 945 tests, one failure: `test_requirements` pinned the Korean REQ-0001-FR-0004 line; the fixture now pins the English line and the module reruns OK | N/A: run evidence for this change |

## Review Evidence

- Meaning review: each batch report listed passages the humanize pass
  reworded; the controller checked the flagged ones. The Valkey "may be absent"
  line keeps its permissive-possibility reading.
- Heading house style: Korean-target documents keep their English template
  headings, as GDE-0008 already did, so no anchor changed.

## Commit Ledger

| Commit | Unit | Change |
| --- | --- | --- |
| `0b77e6097` | Package | Spec, Plan, and Task drafted |
| `31f6921ef` | W1 | Measured set and baseline |
| `1ee018334` | W2 | 17 Requirements packages |
| `d98f31ff2` | W3 | 29 ADRs |
| `ec78e49cd` | W4 | 20 architecture descriptions |
| `54741b2d5` | Hook | Owner-applied scratchpad fix for the edit-target hook |
| `fcc256bd3` | W5, W7 | Seven guides and the repository surface |
| `464dbb2f2` | W5 | 38 guides; GDE-0087 link corrected |
| `8904193b5` | W6 | 22 policies |
| `90b07dc9f` | W5, W7 | GDE-0089 code span; also swept in the six B22 runbook translations before their humanize runs |
| `679d1292a` | W6 | 25 policies; stray closing tags removed |
| `1e3faef73` | W7 | 35 runbooks |
| `35a9b2232` | W5 | GDE-0070 remnant |
| `bf26f7a56` | W2-W4 | Korean remnants in five English documents |
| `9dc9d01d0` | W8 | Corpus-wide language enforcement |
| `c0b6f80c0` | W7 | B22 humanize output and English remnant cleanup |
| (this commit) | W9 | Requirement fixture follows the translated text; evidence recorded |

## Rulings

- 2026-09-29: Owner approved the Spec and Plan ("승인").
- 2026-09-29: Korean-target documents keep all headings unchanged, not only
  registered ones — house style (GDE-0008) keeps English template headings,
  and it avoids anchor churn. This narrows Spec behavior rule 3 to the
  English-target set.
- 2026-09-29: One humanize run per batch of at most 25,000 characters, without
  a diagnosis call — cost control, as in SPEC-0184.
- 2026-09-29: The owner fixed the scratchpad Write hook and added allow rules,
  and approved the metadata, link, and language checks on translated files.
- 2026-09-29: `check-conftest-policy.sh` was not run; the request forbids
  `docker compose` run/down.

## Deferred Items

- Short English labels (`> Scope:`, `**Systems**:`-style lead-ins) and comma
  lists of technical nouns remain in Korean-target documents as house style.
