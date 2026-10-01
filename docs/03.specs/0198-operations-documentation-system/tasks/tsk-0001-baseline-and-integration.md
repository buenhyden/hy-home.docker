---
title: "Operations Audit Baseline and Integration"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0198-TSK-0001"
parent_ids:
- "SPEC-0198"
- "SPEC-0198-PLAN-0001"
created: "2026-10-01"
---

# Operations Audit Baseline and Integration

## Objective

Own W1 baseline, cross-wave integration and W8 acceptance evidence for
[the approved Plan](../plan.md) and [Spec](../spec.md).

## Inputs

User approved written Spec, then Plan and tier-scoped agents plus independent
review on 2026-10-01. Worktree: `/home/hyunyoun/.codex/worktrees/infra-tier-layout/hy-home.docker`;
branch `codex/infra-tier-layout`; Git base c26bc8026254dffd7d51fc45b4081a1f80f855f2.
SPEC-0197's source implementation is present and independently reviewed; its
final gate remains in progress. No merge or runtime deployment is implied.

## Work Log

On 2026-10-01 the user reaffirmed the existing Guide/Policy/Runbook authoring and language rules. The documentation protocol and all three registered templates were reread: Stage05 explanatory prose is Korean; structural headings, IDs, paths, commands, metadata and code retain their original form. W5 author notified; an independent read-only W2–W4 body-language/format audit is in progress. Numeric language checks do not replace semantic language review or authorize threshold gaming.

Preflight shared-boundary review:

| Units | Shared producer/consumer | Finding and resolution |
| --- | --- | --- |
| W1 -> W2-W7 | Exact document/service/version baseline | W1 manifest gates all implementation dispatches. |
| W2 -> W3-W7 | Shared owners and new system Guide | Finish/review W2 first; service writers link common owners. |
| W3-W6 | Disjoint subject bodies | Only the integrating owner edits role indexes/registry. |
| W2 -> W7 | Workspace/common owner bodies | W7 reconciles them after service waves; no concurrent writer. |
| W1-W7 -> W8 | Evidence and final joins | Review complete matrix and changes, not report assertions. |
| W1 | Baseline versus audit completion | Inventory is not semantic review; all body dispositions start pending. |
| W2 | New system documents versus duplicate registry | Navigation/knowledge only; no implementation_services claims. |
| W3 | Security discrepancy versus docs scope | Preserve controls; source defects require separate implementation. |
| W4 | Shared storage versus Analytics ownership | Keep named grouped identities and storage controls explicit. |
| W5 | Concurrent SPEC-0193 ownership | Check overlaps before edits; preserve concurrent changes. |
| W6 | Jobs versus persistent services | Explicit topic applicability; no generic HTTP/backup filler. |
| W7 | Concurrent SPEC-0182 RUN-0098 | Link existing procedure; coordinate needed body edits. |
| W8 | Static checks versus live evidence | Runtime/recovery remain NOT_RUN without separate execution. |

### User clarification: built services

The user explicitly required Dockerfile inspection for Compose-built services.
W1's 21 build-source baseline is discovery evidence; each owning wave must
inspect effective context/Dockerfile/args/target, FROM, installed packages, COPY
inputs and ENTRYPOINT/CMD, following referenced scripts/configuration needed to
explain behavior. Record effective overrides and unknown alternate selections.
No build execution or runtime observation is authorized by this clarification.

### Preparatory source findings awaiting wave resolution

Independent read-only recovery review `/root/ops_data_recovery_inputs` identified
W4 corrections in subjects 0021/0031/0032/0035: synthetic versus real HA recovery,
partial backup upload gating, capacity/schedule guarantees, restore selection,
isolation and secret-file permissions. Existing safeguards must be preserved;
no operational recovery contract or action was approved. W4 must record exact
source-to-final resolutions; independent security review covers permission gaps.
W5 version research additionally identified n8n core/runner version divergence
and Airflow native-auth versus proxy-auth wording; these remain pending W5
source/official-evidence reconciliation, not implemented fixes.

### W1 baseline receipt (2026-10-01)

The first W1 implementer stopped on a provider model-capacity error after
producing the inventory. The replacement resumed the preserved generator and
manifest, checked their joins, and completed build/package notes; it did not
restart the inventory. No secret, local `.env`, running service or external
package was read. Source is the current public worktree at the Inputs base,
including the reviewed but uncommitted SPEC-0197 layout, not committed main.

The dated counts reconcile: 225 role leaves = 77 Guides + 75 Policies +
73 Runbooks; 87 subjects = 68 triplets + 2 Guide/Policy pairs + 17 single roles.
There are 88 distinct filenames because Airflow lifecycle keeps GDE-0051 and
POL-0052 under one subject. Lifecycle totals are 184 active and 41 draft;
these values do not establish review completion. At baseline capture every body was
PENDING, including active documents. The tables preserve that initial capture;
subsequent wave Tasks own final dispositions and independent review receipts.

| Wave | Exact role leaves below | Bound service identities | Body/topic review |
| --- | ---: | ---: | --- |
| W3 | 18 | 8 | PENDING |
| W4 | 59 | 87 | PENDING |
| W5 | 60 | 34 | PENDING |
| W6 | 67 | 24 | PENDING |
| W7 | 21 | 0 | PENDING; applicable non-service subjects |
| Total | 225 | 153 | PENDING |

Each leaf has exactly one wave. Each service has exactly one Guide: 56 Guides
bind services; the other 21 Guides have no `implementation_services` binding.
The service table below expands every declared binding, including helpers and
provisioning jobs. Classification reconciles to HOME 45, DEV 12, OPTIONAL 55,
LAB 41; it is source classification, not evidence of deployed containers.

Shared W2/integrator ownership: `docs/05.operations/README.md`,
`docs/05.operations/guides/README.md`, `docs/05.operations/policies/README.md`,
`docs/05.operations/runbooks/README.md`, `docs/99.templates/registry.json`,
this package's Plan and Tasks. W2's candidate Guide is
`docs/05.operations/guides/0099-system-operations.md`; allocation was completed and independently reviewed in W2 after reconciling
the stale 0088 cursor against issued IDs through 0098. W2 added GDE-0099 and
RUN-0099 and advanced the cursor to 0100; no Policy was justified. No ID was
allocated in W1. W2 consumes AD-0031, RUN-0098, POL-0006,
POL-0078 and existing subjects 0021/0077/0086 by link; those leaves retain their
assigned wave owners. RUN-0098 remains coordinated with SPEC-0182.

This is a dated audit manifest, not a maintained runtime-version registry.
Exact literals below preserve the source baseline for later version matching;
Compose, Dockerfiles and package declarations remain their current authority.
The existing `infra/tech-stack.versions.json` projection is a discovery aid;
build source and inherited declarations below were inspected independently.
There are 143 mutable versioned/named image tags, one floating local label,
nine build-only identities and no image digest declarations. None establishes
installed runtime versions. Byte-pinned download inputs are listed separately.

### Role artifact manifest (baseline; body audit pending)

Paths are complete from repository root. Lifecycle is frontmatter status; every body review remains PENDING.

| Wave | Exact role path | Artifact ID | Lifecycle | Body audit |
| --- | --- | --- | --- | --- |
| W7 | docs/05.operations/guides/0002-developer-environment.md | GDE-0002 | active | PENDING |
| W7 | docs/05.operations/guides/0003-env-key-comparison.md | GDE-0003 | active | PENDING |
| W7 | docs/05.operations/guides/0004-harness-agent-first-engineering.md | GDE-0004 | active | PENDING |
| W7 | docs/05.operations/guides/0008-new-service-onboarding.md | GDE-0008 | active | PENDING |
| W7 | docs/05.operations/guides/0010-sensitive-env-vars-comparison.md | GDE-0010 | active | PENDING |
| W3 | docs/05.operations/guides/0011-nginx.md | GDE-0011 | active | PENDING |
| W3 | docs/05.operations/guides/0012-edge-routing-stack.md | GDE-0012 | active | PENDING |
| W3 | docs/05.operations/guides/0013-traefik.md | GDE-0013 | active | PENDING |
| W3 | docs/05.operations/guides/0014-keycloak.md | GDE-0014 | active | PENDING |
| W3 | docs/05.operations/guides/0015-oauth2-proxy.md | GDE-0015 | active | PENDING |
| W4 | docs/05.operations/guides/0017-influxdb.md | GDE-0017 | active | PENDING |
| W4 | docs/05.operations/guides/0019-opensearch.md | GDE-0019 | active | PENDING |
| W4 | docs/05.operations/guides/0021-backup-and-restore.md | GDE-0021 | draft | PENDING |
| W4 | docs/05.operations/guides/0022-valkey-cluster.md | GDE-0022 | active | PENDING |
| W4 | docs/05.operations/guides/0024-seaweedfs.md | GDE-0024 | active | PENDING |
| W4 | docs/05.operations/guides/0025-cassandra.md | GDE-0025 | active | PENDING |
| W4 | docs/05.operations/guides/0026-couchdb.md | GDE-0026 | active | PENDING |
| W4 | docs/05.operations/guides/0027-mongodb.md | GDE-0027 | active | PENDING |
| W4 | docs/05.operations/guides/0028-management-database.md | GDE-0028 | active | PENDING |
| W4 | docs/05.operations/guides/0029-supabase.md | GDE-0029 | active | PENDING |
| W4 | docs/05.operations/guides/0030-data-optimization-hardening.md | GDE-0030 | active | PENDING |
| W4 | docs/05.operations/guides/0031-postgresql-cluster.md | GDE-0031 | active | PENDING |
| W4 | docs/05.operations/guides/0033-neo4j.md | GDE-0033 | active | PENDING |
| W4 | docs/05.operations/guides/0034-qdrant.md | GDE-0034 | active | PENDING |
| W4 | docs/05.operations/guides/0036-kafka.md | GDE-0036 | active | PENDING |
| W4 | docs/05.operations/guides/0037-messaging-optimization-hardening.md | GDE-0037 | active | PENDING |
| W5 | docs/05.operations/guides/0039-alertmanager.md | GDE-0039 | active | PENDING |
| W5 | docs/05.operations/guides/0040-alloy.md | GDE-0040 | active | PENDING |
| W5 | docs/05.operations/guides/0041-grafana.md | GDE-0041 | active | PENDING |
| W5 | docs/05.operations/guides/0042-lgtm-stack.md | GDE-0042 | active | PENDING |
| W5 | docs/05.operations/guides/0043-loki.md | GDE-0043 | active | PENDING |
| W5 | docs/05.operations/guides/0044-observability-optimization-hardening.md | GDE-0044 | active | PENDING |
| W5 | docs/05.operations/guides/0045-prometheus.md | GDE-0045 | active | PENDING |
| W5 | docs/05.operations/guides/0046-pushgateway.md | GDE-0046 | active | PENDING |
| W5 | docs/05.operations/guides/0047-pyroscope.md | GDE-0047 | active | PENDING |
| W5 | docs/05.operations/guides/0049-tempo.md | GDE-0049 | active | PENDING |
| W5 | docs/05.operations/guides/0050-airflow.md | GDE-0050 | active | PENDING |
| W5 | docs/05.operations/guides/0051-airflow-dag-lifecycle.md | GDE-0051 | active | PENDING |
| W5 | docs/05.operations/guides/0053-n8n.md | GDE-0053 | active | PENDING |
| W5 | docs/05.operations/guides/0054-workflow-optimization-hardening.md | GDE-0054 | active | PENDING |
| W5 | docs/05.operations/guides/0056-ollama.md | GDE-0056 | active | PENDING |
| W5 | docs/05.operations/guides/0057-open-webui.md | GDE-0057 | active | PENDING |
| W5 | docs/05.operations/guides/0058-ai-optimization-hardening.md | GDE-0058 | active | PENDING |
| W5 | docs/05.operations/guides/0059-rag-workflow.md | GDE-0059 | active | PENDING |
| W6 | docs/05.operations/guides/0061-k6.md | GDE-0061 | active | PENDING |
| W6 | docs/05.operations/guides/0062-locust.md | GDE-0062 | active | PENDING |
| W6 | docs/05.operations/guides/0063-tooling-optimization-hardening.md | GDE-0063 | active | PENDING |
| W6 | docs/05.operations/guides/0064-performance-testing.md | GDE-0064 | active | PENDING |
| W6 | docs/05.operations/guides/0065-registry.md | GDE-0065 | active | PENDING |
| W6 | docs/05.operations/guides/0066-sonarqube.md | GDE-0066 | active | PENDING |
| W6 | docs/05.operations/guides/0068-terraform.md | GDE-0068 | active | PENDING |
| W6 | docs/05.operations/guides/0069-terrakube.md | GDE-0069 | active | PENDING |
| W6 | docs/05.operations/guides/0070-mail.md | GDE-0070 | active | PENDING |
| W6 | docs/05.operations/guides/0072-dozzle.md | GDE-0072 | active | PENDING |
| W6 | docs/05.operations/guides/0073-open-notebook.md | GDE-0073 | active | PENDING |
| W6 | docs/05.operations/guides/0074-laboratory-optimization-hardening.md | GDE-0074 | active | PENDING |
| W6 | docs/05.operations/guides/0076-redisinsight.md | GDE-0076 | active | PENDING |
| W7 | docs/05.operations/guides/0077-ip-address-management.md | GDE-0077 | active | PENDING |
| W3 | docs/05.operations/guides/0079-application-auth-integration.md | GDE-0079 | draft | PENDING |
| W6 | docs/05.operations/guides/0080-surrealdb.md | GDE-0080 | draft | PENDING |
| W5 | docs/05.operations/guides/0081-comfyui.md | GDE-0081 | draft | PENDING |
| W6 | docs/05.operations/guides/0082-opentofu.md | GDE-0082 | draft | PENDING |
| W6 | docs/05.operations/guides/0083-renovate.md | GDE-0083 | draft | PENDING |
| W6 | docs/05.operations/guides/0084-mailpit.md | GDE-0084 | draft | PENDING |
| W3 | docs/05.operations/guides/0085-openbao.md | GDE-0085 | draft | PENDING |
| W7 | docs/05.operations/guides/0086-dependency-version-management.md | GDE-0086 | draft | PENDING |
| W5 | docs/05.operations/guides/0087-gatus.md | GDE-0087 | draft | PENDING |
| W6 | docs/05.operations/guides/0088-mlflow.md | GDE-0088 | active | PENDING |
| W6 | docs/05.operations/guides/0089-jupyterlab.md | GDE-0089 | active | PENDING |
| W4 | docs/05.operations/guides/0090-dbt.md | GDE-0090 | active | PENDING |
| W5 | docs/05.operations/guides/0091-crawl4ai.md | GDE-0091 | active | PENDING |
| W6 | docs/05.operations/guides/0092-wiremock.md | GDE-0092 | active | PENDING |
| W6 | docs/05.operations/guides/0093-pact-broker.md | GDE-0093 | active | PENDING |
| W4 | docs/05.operations/guides/0094-lakehouse.md | GDE-0094 | draft | PENDING |
| W6 | docs/05.operations/guides/0095-conftest.md | GDE-0095 | draft | PENDING |
| W7 | docs/05.operations/guides/0096-k8s-integration.md | GDE-0096 | draft | PENDING |
| W4 | docs/05.operations/guides/0097-superset.md | GDE-0097 | draft | PENDING |
| W7 | docs/05.operations/policies/0001-common-optimizations-template-exceptions.md | POL-0001 | active | PENDING |
| W7 | docs/05.operations/policies/0004-harness-agent-first-engineering.md | POL-0004 | active | PENDING |
| W7 | docs/05.operations/policies/0006-infrastructure-optimization-governance.md | POL-0006 | active | PENDING |
| W3 | docs/05.operations/policies/0011-nginx.md | POL-0011 | active | PENDING |
| W3 | docs/05.operations/policies/0013-traefik.md | POL-0013 | active | PENDING |
| W3 | docs/05.operations/policies/0014-keycloak.md | POL-0014 | active | PENDING |
| W3 | docs/05.operations/policies/0015-oauth2-proxy.md | POL-0015 | active | PENDING |
| W4 | docs/05.operations/policies/0017-influxdb.md | POL-0017 | active | PENDING |
| W4 | docs/05.operations/policies/0019-opensearch.md | POL-0019 | active | PENDING |
| W4 | docs/05.operations/policies/0021-backup-and-restore.md | POL-0021 | active | PENDING |
| W4 | docs/05.operations/policies/0022-valkey-cluster.md | POL-0022 | active | PENDING |
| W4 | docs/05.operations/policies/0024-seaweedfs.md | POL-0024 | active | PENDING |
| W4 | docs/05.operations/policies/0025-cassandra.md | POL-0025 | active | PENDING |
| W4 | docs/05.operations/policies/0026-couchdb.md | POL-0026 | active | PENDING |
| W4 | docs/05.operations/policies/0027-mongodb.md | POL-0027 | active | PENDING |
| W4 | docs/05.operations/policies/0028-management-database.md | POL-0028 | active | PENDING |
| W4 | docs/05.operations/policies/0029-supabase.md | POL-0029 | active | PENDING |
| W4 | docs/05.operations/policies/0030-data-optimization-hardening.md | POL-0030 | active | PENDING |
| W4 | docs/05.operations/policies/0031-postgresql-cluster.md | POL-0031 | active | PENDING |
| W4 | docs/05.operations/policies/0033-neo4j.md | POL-0033 | active | PENDING |
| W4 | docs/05.operations/policies/0034-qdrant.md | POL-0034 | active | PENDING |
| W4 | docs/05.operations/policies/0036-kafka.md | POL-0036 | active | PENDING |
| W4 | docs/05.operations/policies/0037-messaging-optimization-hardening.md | POL-0037 | active | PENDING |
| W5 | docs/05.operations/policies/0039-alertmanager.md | POL-0039 | active | PENDING |
| W5 | docs/05.operations/policies/0040-alloy.md | POL-0040 | active | PENDING |
| W5 | docs/05.operations/policies/0041-grafana.md | POL-0041 | active | PENDING |
| W5 | docs/05.operations/policies/0043-loki.md | POL-0043 | active | PENDING |
| W5 | docs/05.operations/policies/0044-observability-optimization-hardening.md | POL-0044 | active | PENDING |
| W5 | docs/05.operations/policies/0045-prometheus.md | POL-0045 | active | PENDING |
| W5 | docs/05.operations/policies/0046-pushgateway.md | POL-0046 | active | PENDING |
| W5 | docs/05.operations/policies/0047-pyroscope.md | POL-0047 | active | PENDING |
| W5 | docs/05.operations/policies/0048-telemetry-retention.md | POL-0048 | active | PENDING |
| W5 | docs/05.operations/policies/0049-tempo.md | POL-0049 | active | PENDING |
| W5 | docs/05.operations/policies/0050-airflow.md | POL-0050 | active | PENDING |
| W5 | docs/05.operations/policies/0052-airflow-dag-lifecycle.md | POL-0052 | active | PENDING |
| W5 | docs/05.operations/policies/0053-n8n.md | POL-0053 | active | PENDING |
| W5 | docs/05.operations/policies/0054-workflow-optimization-hardening.md | POL-0054 | active | PENDING |
| W5 | docs/05.operations/policies/0056-ollama.md | POL-0056 | active | PENDING |
| W5 | docs/05.operations/policies/0057-open-webui.md | POL-0057 | active | PENDING |
| W5 | docs/05.operations/policies/0058-ai-optimization-hardening.md | POL-0058 | active | PENDING |
| W6 | docs/05.operations/policies/0060-iac-deployment.md | POL-0060 | active | PENDING |
| W6 | docs/05.operations/policies/0061-k6.md | POL-0061 | active | PENDING |
| W6 | docs/05.operations/policies/0062-locust.md | POL-0062 | active | PENDING |
| W6 | docs/05.operations/policies/0063-tooling-optimization-hardening.md | POL-0063 | active | PENDING |
| W6 | docs/05.operations/policies/0064-performance-testing.md | POL-0064 | active | PENDING |
| W6 | docs/05.operations/policies/0065-registry.md | POL-0065 | active | PENDING |
| W6 | docs/05.operations/policies/0066-sonarqube.md | POL-0066 | active | PENDING |
| W6 | docs/05.operations/policies/0068-terraform.md | POL-0068 | active | PENDING |
| W6 | docs/05.operations/policies/0069-terrakube.md | POL-0069 | active | PENDING |
| W6 | docs/05.operations/policies/0070-mail.md | POL-0070 | active | PENDING |
| W6 | docs/05.operations/policies/0072-dozzle.md | POL-0072 | active | PENDING |
| W6 | docs/05.operations/policies/0073-open-notebook.md | POL-0073 | active | PENDING |
| W6 | docs/05.operations/policies/0074-laboratory-optimization-hardening.md | POL-0074 | active | PENDING |
| W6 | docs/05.operations/policies/0076-redisinsight.md | POL-0076 | active | PENDING |
| W7 | docs/05.operations/policies/0077-ip-address-management.md | POL-0077 | active | PENDING |
| W7 | docs/05.operations/policies/0078-compose-profile-vocabulary.md | POL-0078 | active | PENDING |
| W3 | docs/05.operations/policies/0079-application-auth-integration.md | POL-0079 | draft | PENDING |
| W6 | docs/05.operations/policies/0080-surrealdb.md | POL-0080 | draft | PENDING |
| W5 | docs/05.operations/policies/0081-comfyui.md | POL-0081 | draft | PENDING |
| W6 | docs/05.operations/policies/0082-opentofu.md | POL-0082 | draft | PENDING |
| W6 | docs/05.operations/policies/0083-renovate.md | POL-0083 | draft | PENDING |
| W6 | docs/05.operations/policies/0084-mailpit.md | POL-0084 | draft | PENDING |
| W3 | docs/05.operations/policies/0085-openbao.md | POL-0085 | draft | PENDING |
| W7 | docs/05.operations/policies/0086-dependency-version-management.md | POL-0086 | draft | PENDING |
| W5 | docs/05.operations/policies/0087-gatus.md | POL-0087 | draft | PENDING |
| W6 | docs/05.operations/policies/0088-mlflow.md | POL-0088 | active | PENDING |
| W6 | docs/05.operations/policies/0089-jupyterlab.md | POL-0089 | active | PENDING |
| W4 | docs/05.operations/policies/0090-dbt.md | POL-0090 | active | PENDING |
| W5 | docs/05.operations/policies/0091-crawl4ai.md | POL-0091 | active | PENDING |
| W6 | docs/05.operations/policies/0092-wiremock.md | POL-0092 | active | PENDING |
| W6 | docs/05.operations/policies/0093-pact-broker.md | POL-0093 | active | PENDING |
| W4 | docs/05.operations/policies/0094-lakehouse.md | POL-0094 | draft | PENDING |
| W6 | docs/05.operations/policies/0095-conftest.md | POL-0095 | draft | PENDING |
| W7 | docs/05.operations/policies/0096-k8s-integration.md | POL-0096 | draft | PENDING |
| W4 | docs/05.operations/policies/0097-superset.md | POL-0097 | draft | PENDING |
| W7 | docs/05.operations/runbooks/0004-harness-agent-first-engineering.md | RUN-0004 | active | PENDING |
| W7 | docs/05.operations/runbooks/0009-release-management.md | RUN-0009 | active | PENDING |
| W3 | docs/05.operations/runbooks/0011-nginx.md | RUN-0011 | active | PENDING |
| W3 | docs/05.operations/runbooks/0013-traefik.md | RUN-0013 | active | PENDING |
| W3 | docs/05.operations/runbooks/0014-keycloak.md | RUN-0014 | active | PENDING |
| W3 | docs/05.operations/runbooks/0015-oauth2-proxy.md | RUN-0015 | active | PENDING |
| W4 | docs/05.operations/runbooks/0017-influxdb.md | RUN-0017 | active | PENDING |
| W4 | docs/05.operations/runbooks/0019-opensearch.md | RUN-0019 | active | PENDING |
| W4 | docs/05.operations/runbooks/0021-backup-and-restore.md | RUN-0021 | draft | PENDING |
| W4 | docs/05.operations/runbooks/0022-valkey-cluster.md | RUN-0022 | active | PENDING |
| W4 | docs/05.operations/runbooks/0024-seaweedfs.md | RUN-0024 | active | PENDING |
| W4 | docs/05.operations/runbooks/0025-cassandra.md | RUN-0025 | active | PENDING |
| W4 | docs/05.operations/runbooks/0026-couchdb.md | RUN-0026 | active | PENDING |
| W4 | docs/05.operations/runbooks/0027-mongodb.md | RUN-0027 | active | PENDING |
| W4 | docs/05.operations/runbooks/0028-management-database.md | RUN-0028 | active | PENDING |
| W4 | docs/05.operations/runbooks/0029-supabase.md | RUN-0029 | active | PENDING |
| W4 | docs/05.operations/runbooks/0030-data-optimization-hardening.md | RUN-0030 | active | PENDING |
| W4 | docs/05.operations/runbooks/0031-postgresql-cluster.md | RUN-0031 | active | PENDING |
| W4 | docs/05.operations/runbooks/0032-postgresql-logical-upgrade-restore-rehearsal.md | RUN-0032 | active | PENDING |
| W4 | docs/05.operations/runbooks/0033-neo4j.md | RUN-0033 | active | PENDING |
| W4 | docs/05.operations/runbooks/0034-qdrant.md | RUN-0034 | active | PENDING |
| W4 | docs/05.operations/runbooks/0035-storage-exhaustion.md | RUN-0035 | active | PENDING |
| W4 | docs/05.operations/runbooks/0036-kafka.md | RUN-0036 | active | PENDING |
| W4 | docs/05.operations/runbooks/0037-messaging-optimization-hardening.md | RUN-0037 | active | PENDING |
| W5 | docs/05.operations/runbooks/0039-alertmanager.md | RUN-0039 | active | PENDING |
| W5 | docs/05.operations/runbooks/0040-alloy.md | RUN-0040 | active | PENDING |
| W5 | docs/05.operations/runbooks/0041-grafana.md | RUN-0041 | active | PENDING |
| W5 | docs/05.operations/runbooks/0043-loki.md | RUN-0043 | active | PENDING |
| W5 | docs/05.operations/runbooks/0044-observability-optimization-hardening.md | RUN-0044 | active | PENDING |
| W5 | docs/05.operations/runbooks/0045-prometheus.md | RUN-0045 | active | PENDING |
| W5 | docs/05.operations/runbooks/0046-pushgateway.md | RUN-0046 | active | PENDING |
| W5 | docs/05.operations/runbooks/0047-pyroscope.md | RUN-0047 | active | PENDING |
| W5 | docs/05.operations/runbooks/0049-tempo.md | RUN-0049 | active | PENDING |
| W5 | docs/05.operations/runbooks/0050-airflow.md | RUN-0050 | active | PENDING |
| W5 | docs/05.operations/runbooks/0053-n8n.md | RUN-0053 | active | PENDING |
| W5 | docs/05.operations/runbooks/0054-workflow-optimization-hardening.md | RUN-0054 | active | PENDING |
| W5 | docs/05.operations/runbooks/0055-gpu-recovery.md | RUN-0055 | active | PENDING |
| W5 | docs/05.operations/runbooks/0056-ollama.md | RUN-0056 | active | PENDING |
| W5 | docs/05.operations/runbooks/0057-open-webui.md | RUN-0057 | active | PENDING |
| W5 | docs/05.operations/runbooks/0058-ai-optimization-hardening.md | RUN-0058 | active | PENDING |
| W6 | docs/05.operations/runbooks/0061-k6.md | RUN-0061 | active | PENDING |
| W6 | docs/05.operations/runbooks/0062-locust.md | RUN-0062 | active | PENDING |
| W6 | docs/05.operations/runbooks/0063-tooling-optimization-hardening.md | RUN-0063 | active | PENDING |
| W6 | docs/05.operations/runbooks/0064-performance-testing.md | RUN-0064 | active | PENDING |
| W6 | docs/05.operations/runbooks/0065-registry.md | RUN-0065 | active | PENDING |
| W6 | docs/05.operations/runbooks/0066-sonarqube.md | RUN-0066 | active | PENDING |
| W6 | docs/05.operations/runbooks/0068-terraform.md | RUN-0068 | active | PENDING |
| W6 | docs/05.operations/runbooks/0069-terrakube.md | RUN-0069 | active | PENDING |
| W6 | docs/05.operations/runbooks/0070-mail.md | RUN-0070 | active | PENDING |
| W6 | docs/05.operations/runbooks/0072-dozzle.md | RUN-0072 | active | PENDING |
| W6 | docs/05.operations/runbooks/0073-open-notebook.md | RUN-0073 | active | PENDING |
| W6 | docs/05.operations/runbooks/0074-laboratory-optimization-hardening.md | RUN-0074 | active | PENDING |
| W6 | docs/05.operations/runbooks/0076-redisinsight.md | RUN-0076 | active | PENDING |
| W7 | docs/05.operations/runbooks/0077-ip-address-management.md | RUN-0077 | active | PENDING |
| W6 | docs/05.operations/runbooks/0080-surrealdb.md | RUN-0080 | draft | PENDING |
| W5 | docs/05.operations/runbooks/0081-comfyui.md | RUN-0081 | draft | PENDING |
| W6 | docs/05.operations/runbooks/0082-opentofu.md | RUN-0082 | draft | PENDING |
| W6 | docs/05.operations/runbooks/0083-renovate.md | RUN-0083 | draft | PENDING |
| W6 | docs/05.operations/runbooks/0084-mailpit.md | RUN-0084 | draft | PENDING |
| W3 | docs/05.operations/runbooks/0085-openbao.md | RUN-0085 | draft | PENDING |
| W7 | docs/05.operations/runbooks/0086-dependency-version-management.md | RUN-0086 | draft | PENDING |
| W5 | docs/05.operations/runbooks/0087-gatus.md | RUN-0087 | draft | PENDING |
| W6 | docs/05.operations/runbooks/0088-mlflow.md | RUN-0088 | active | PENDING |
| W6 | docs/05.operations/runbooks/0089-jupyterlab.md | RUN-0089 | active | PENDING |
| W4 | docs/05.operations/runbooks/0090-dbt.md | RUN-0090 | active | PENDING |
| W5 | docs/05.operations/runbooks/0091-crawl4ai.md | RUN-0091 | active | PENDING |
| W6 | docs/05.operations/runbooks/0092-wiremock.md | RUN-0092 | active | PENDING |
| W6 | docs/05.operations/runbooks/0093-pact-broker.md | RUN-0093 | active | PENDING |
| W4 | docs/05.operations/runbooks/0094-lakehouse.md | RUN-0094 | draft | PENDING |
| W6 | docs/05.operations/runbooks/0095-conftest.md | RUN-0095 | draft | PENDING |
| W7 | docs/05.operations/runbooks/0096-k8s-integration.md | RUN-0096 | draft | PENDING |
| W4 | docs/05.operations/runbooks/0097-superset.md | RUN-0097 | draft | PENDING |
| W7 | docs/05.operations/runbooks/0098-cold-start-and-reboot.md | RUN-0098 | draft | PENDING |

### Service identity and declared-version manifest (baseline; topic audit pending)

Each identity is Compose source plus service; sole Guide is from its implementation_services binding. tag means a mutable versioned or named image tag, including major-only tags; floating means unversioned/latest/local; digest means content-addressed; build-only means no image declaration. Every runtime version is UNVERIFIED. Local image labels do not establish upstream bytes.

| Compose source | Service | Sole Guide | Class | Image declaration | Build source | Certainty | Topic audit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| infra/01-gateway/nginx/docker-compose.yml | nginx | docs/05.operations/guides/0011-nginx.md | OPTIONAL | nginx:alpine | none | tag | PENDING |
| infra/01-gateway/traefik/docker-compose.yml | traefik | docs/05.operations/guides/0013-traefik.md | HOME | traefik:v3.7.13 | none | tag | PENDING |
| infra/02-auth/keycloak/docker-compose.yml | keycloak | docs/05.operations/guides/0014-keycloak.md | HOME | quay.io/keycloak/keycloak:26.7.4-0 | none | tag | PENDING |
| infra/02-auth/oauth2-proxy/docker-compose.yml | oauth2-proxy | docs/05.operations/guides/0015-oauth2-proxy.md | HOME | none | infra/02-auth/oauth2-proxy/dev.Dockerfile (default from ${OAUTH2_PROXY_DOCKERFILE:-dev.Dockerfile}) | build-only | PENDING |
| infra/02-auth/oauth2-proxy/docker-compose.yml | oauth2-proxy-valkey | docs/05.operations/guides/0015-oauth2-proxy.md | OPTIONAL | valkey/valkey:9.1.2-alpine | none | tag | PENDING |
| infra/02-auth/oauth2-proxy/docker-compose.yml | oauth2-proxy-valkey-exporter | docs/05.operations/guides/0015-oauth2-proxy.md | OPTIONAL | oliver006/redis_exporter:v1.91.1-alpine | none | tag | PENDING |
| infra/03-security/openbao/docker-compose.yml | openbao | docs/05.operations/guides/0085-openbao.md | HOME | openbao/openbao:2.6.2 | none | tag | PENDING |
| infra/03-security/openbao/docker-compose.yml | openbao-agent | docs/05.operations/guides/0085-openbao.md | HOME | openbao/openbao:2.6.2 | none | tag | PENDING |
| infra/04-data/cassandra/docker-compose.yml | cassandra-exporter | docs/05.operations/guides/0025-cassandra.md | LAB | bitnami/cassandra-exporter:2.3.11 | none | tag | PENDING |
| infra/04-data/cassandra/docker-compose.yml | cassandra-node1 | docs/05.operations/guides/0025-cassandra.md | LAB | cassandra:5.0.9 | none | tag | PENDING |
| infra/04-data/couchdb/docker-compose.yml | couchdb-1 | docs/05.operations/guides/0026-couchdb.md | LAB | couchdb:3.5.2 | none | tag | PENDING |
| infra/04-data/couchdb/docker-compose.yml | couchdb-2 | docs/05.operations/guides/0026-couchdb.md | LAB | couchdb:3.5.2 | none | tag | PENDING |
| infra/04-data/couchdb/docker-compose.yml | couchdb-3 | docs/05.operations/guides/0026-couchdb.md | LAB | couchdb:3.5.2 | none | tag | PENDING |
| infra/04-data/couchdb/docker-compose.yml | couchdb-cluster-init | docs/05.operations/guides/0026-couchdb.md | LAB | curlimages/curl:8.22.0 | none | tag | PENDING |
| infra/04-data/influxdb/docker-compose.yml | influxdb | docs/05.operations/guides/0017-influxdb.md | OPTIONAL | influxdb:3.11.5-core | none | tag | PENDING |
| infra/04-data/mng-db/docker-compose.yml | mng-pg | docs/05.operations/guides/0028-management-database.md | HOME | hy-home/mng-pg:18.6-pgbackrest | infra/04-data/mng-db/pg/backup/Dockerfile | tag | PENDING |
| infra/04-data/mng-db/docker-compose.yml | mng-pg-exporter | docs/05.operations/guides/0028-management-database.md | HOME | prometheuscommunity/postgres-exporter:v0.20.1 | none | tag | PENDING |
| infra/04-data/mng-db/docker-compose.yml | mng-pg-init | docs/05.operations/guides/0028-management-database.md | HOME | postgres:18.6-alpine | none | tag | PENDING |
| infra/04-data/mng-db/docker-compose.yml | mng-valkey | docs/05.operations/guides/0028-management-database.md | HOME | valkey/valkey:9.1.2-alpine | none | tag | PENDING |
| infra/04-data/mng-db/docker-compose.yml | mng-valkey-exporter | docs/05.operations/guides/0028-management-database.md | HOME | oliver006/redis_exporter:v1.91.1-alpine | none | tag | PENDING |
| infra/04-data/mongodb/docker-compose.yml | mongo-express | docs/05.operations/guides/0027-mongodb.md | LAB | mongo-express:1-18-alpine3.19 | none | tag | PENDING |
| infra/04-data/mongodb/docker-compose.yml | mongo-init | docs/05.operations/guides/0027-mongodb.md | LAB | mongo:8.3.11-noble | none | tag | PENDING |
| infra/04-data/mongodb/docker-compose.yml | mongo-key-generator | docs/05.operations/guides/0027-mongodb.md | LAB | alpine:3.24.2 | none | tag | PENDING |
| infra/04-data/mongodb/docker-compose.yml | mongodb-arbiter | docs/05.operations/guides/0027-mongodb.md | LAB | mongo:8.3.11-noble | none | tag | PENDING |
| infra/04-data/mongodb/docker-compose.yml | mongodb-exporter | docs/05.operations/guides/0027-mongodb.md | LAB | percona/mongodb_exporter:2.37 | none | tag | PENDING |
| infra/04-data/mongodb/docker-compose.yml | mongodb-rep1 | docs/05.operations/guides/0027-mongodb.md | LAB | mongo:8.3.11-noble | none | tag | PENDING |
| infra/04-data/mongodb/docker-compose.yml | mongodb-rep2 | docs/05.operations/guides/0027-mongodb.md | LAB | mongo:8.3.11-noble | none | tag | PENDING |
| infra/04-data/neo4j/docker-compose.yml | neo4j | docs/05.operations/guides/0033-neo4j.md | OPTIONAL | neo4j:5.26.30-community | none | tag | PENDING |
| infra/04-data/opensearch/docker-compose.yml | opensearch | docs/05.operations/guides/0019-opensearch.md | OPTIONAL | none | infra/04-data/opensearch/Dockerfile | build-only | PENDING |
| infra/04-data/opensearch/docker-compose.yml | opensearch-dashboards | docs/05.operations/guides/0019-opensearch.md | LAB | opensearchproject/opensearch-dashboards:3.8.0 | none | tag | PENDING |
| infra/04-data/opensearch/docker-compose.yml | opensearch-node1 | docs/05.operations/guides/0019-opensearch.md | LAB | none | infra/04-data/opensearch/Dockerfile | build-only | PENDING |
| infra/04-data/opensearch/docker-compose.yml | opensearch-node2 | docs/05.operations/guides/0019-opensearch.md | LAB | none | infra/04-data/opensearch/Dockerfile | build-only | PENDING |
| infra/04-data/opensearch/docker-compose.yml | opensearch-node3 | docs/05.operations/guides/0019-opensearch.md | LAB | none | infra/04-data/opensearch/Dockerfile | build-only | PENDING |
| infra/04-data/postgresql-cluster/docker-compose.yml | etcd-1 | docs/05.operations/guides/0031-postgresql-cluster.md | LAB | quay.io/coreos/etcd:v3.7.1 | none | tag | PENDING |
| infra/04-data/postgresql-cluster/docker-compose.yml | etcd-2 | docs/05.operations/guides/0031-postgresql-cluster.md | LAB | quay.io/coreos/etcd:v3.7.1 | none | tag | PENDING |
| infra/04-data/postgresql-cluster/docker-compose.yml | etcd-3 | docs/05.operations/guides/0031-postgresql-cluster.md | LAB | quay.io/coreos/etcd:v3.7.1 | none | tag | PENDING |
| infra/04-data/postgresql-cluster/docker-compose.yml | pg-0 | docs/05.operations/guides/0031-postgresql-cluster.md | LAB | ghcr.io/zalando/spilo-17:4.0-p3 | none | tag | PENDING |
| infra/04-data/postgresql-cluster/docker-compose.yml | pg-0-exporter | docs/05.operations/guides/0031-postgresql-cluster.md | LAB | prometheuscommunity/postgres-exporter:v0.20.1 | none | tag | PENDING |
| infra/04-data/postgresql-cluster/docker-compose.yml | pg-1 | docs/05.operations/guides/0031-postgresql-cluster.md | LAB | ghcr.io/zalando/spilo-17:4.0-p3 | none | tag | PENDING |
| infra/04-data/postgresql-cluster/docker-compose.yml | pg-1-exporter | docs/05.operations/guides/0031-postgresql-cluster.md | LAB | prometheuscommunity/postgres-exporter:v0.20.1 | none | tag | PENDING |
| infra/04-data/postgresql-cluster/docker-compose.yml | pg-2 | docs/05.operations/guides/0031-postgresql-cluster.md | LAB | ghcr.io/zalando/spilo-17:4.0-p3 | none | tag | PENDING |
| infra/04-data/postgresql-cluster/docker-compose.yml | pg-2-exporter | docs/05.operations/guides/0031-postgresql-cluster.md | LAB | prometheuscommunity/postgres-exporter:v0.20.1 | none | tag | PENDING |
| infra/04-data/postgresql-cluster/docker-compose.yml | pg-cluster-init | docs/05.operations/guides/0031-postgresql-cluster.md | LAB | postgres:18.6-alpine | none | tag | PENDING |
| infra/04-data/postgresql-cluster/docker-compose.yml | pg-router | docs/05.operations/guides/0031-postgresql-cluster.md | LAB | haproxy:3.4.4 | none | tag | PENDING |
| infra/04-data/qdrant/docker-compose.yml | qdrant | docs/05.operations/guides/0034-qdrant.md | HOME | qdrant/qdrant:v1.19.1-unprivileged | none | tag | PENDING |
| infra/04-data/seaweedfs/docker-compose.yml | seaweedfs-buckets | docs/05.operations/guides/0024-seaweedfs.md | HOME | amazon/aws-cli:2.36.50 | none | tag | PENDING |
| infra/04-data/seaweedfs/docker-compose.yml | seaweedfs-filer | docs/05.operations/guides/0024-seaweedfs.md | HOME | chrislusf/seaweedfs:4.47 | none | tag | PENDING |
| infra/04-data/seaweedfs/docker-compose.yml | seaweedfs-master | docs/05.operations/guides/0024-seaweedfs.md | HOME | chrislusf/seaweedfs:4.47 | none | tag | PENDING |
| infra/04-data/seaweedfs/docker-compose.yml | seaweedfs-s3 | docs/05.operations/guides/0024-seaweedfs.md | HOME | chrislusf/seaweedfs:4.47 | none | tag | PENDING |
| infra/04-data/seaweedfs/docker-compose.yml | seaweedfs-table-bucket | docs/05.operations/guides/0094-lakehouse.md | OPTIONAL | amazon/aws-cli:2.36.50 | none | tag | PENDING |
| infra/04-data/seaweedfs/docker-compose.yml | seaweedfs-volume | docs/05.operations/guides/0024-seaweedfs.md | HOME | chrislusf/seaweedfs:4.47 | none | tag | PENDING |
| infra/04-data/supabase/docker-compose.yml | analytics | docs/05.operations/guides/0029-supabase.md | OPTIONAL | supabase/logflare:1.50.15 | none | tag | PENDING |
| infra/04-data/supabase/docker-compose.yml | auth | docs/05.operations/guides/0029-supabase.md | OPTIONAL | supabase/gotrue:v2.197.0 | none | tag | PENDING |
| infra/04-data/supabase/docker-compose.yml | db | docs/05.operations/guides/0029-supabase.md | OPTIONAL | supabase/postgres:17.6.1.173 | none | tag | PENDING |
| infra/04-data/supabase/docker-compose.yml | functions | docs/05.operations/guides/0029-supabase.md | OPTIONAL | supabase/edge-runtime:v1.76.2 | none | tag | PENDING |
| infra/04-data/supabase/docker-compose.yml | imgproxy | docs/05.operations/guides/0029-supabase.md | OPTIONAL | darthsim/imgproxy:v4.0.15 | none | tag | PENDING |
| infra/04-data/supabase/docker-compose.yml | kong | docs/05.operations/guides/0029-supabase.md | OPTIONAL | kong:3.9.3 | none | tag | PENDING |
| infra/04-data/supabase/docker-compose.yml | meta | docs/05.operations/guides/0029-supabase.md | OPTIONAL | supabase/postgres-meta:v0.99.0 | none | tag | PENDING |
| infra/04-data/supabase/docker-compose.yml | realtime | docs/05.operations/guides/0029-supabase.md | OPTIONAL | supabase/realtime:v2.138.1 | none | tag | PENDING |
| infra/04-data/supabase/docker-compose.yml | rest | docs/05.operations/guides/0029-supabase.md | OPTIONAL | postgrest/postgrest:v16.3 | none | tag | PENDING |
| infra/04-data/supabase/docker-compose.yml | storage | docs/05.operations/guides/0029-supabase.md | OPTIONAL | supabase/storage-api:v1.79.4 | none | tag | PENDING |
| infra/04-data/supabase/docker-compose.yml | studio | docs/05.operations/guides/0029-supabase.md | OPTIONAL | supabase/studio:2026.09.14-sha-4dd8a95 | none | tag | PENDING |
| infra/04-data/supabase/docker-compose.yml | supavisor | docs/05.operations/guides/0029-supabase.md | OPTIONAL | supabase/supavisor:2.9.13 | none | tag | PENDING |
| infra/04-data/supabase/docker-compose.yml | vector | docs/05.operations/guides/0029-supabase.md | OPTIONAL | timberio/vector:0.58.0-alpine | none | tag | PENDING |
| infra/04-data/valkey-cluster/docker-compose.yml | valkey-cluster-exporter | docs/05.operations/guides/0022-valkey-cluster.md | LAB | oliver006/redis_exporter:v1.91.1-alpine | none | tag | PENDING |
| infra/04-data/valkey-cluster/docker-compose.yml | valkey-cluster-init | docs/05.operations/guides/0022-valkey-cluster.md | LAB | valkey/valkey:9.1.2-alpine | none | tag | PENDING |
| infra/04-data/valkey-cluster/docker-compose.yml | valkey-node-0 | docs/05.operations/guides/0022-valkey-cluster.md | LAB | valkey/valkey:9.1.2-alpine | none | tag | PENDING |
| infra/04-data/valkey-cluster/docker-compose.yml | valkey-node-1 | docs/05.operations/guides/0022-valkey-cluster.md | LAB | valkey/valkey:9.1.2-alpine | none | tag | PENDING |
| infra/04-data/valkey-cluster/docker-compose.yml | valkey-node-2 | docs/05.operations/guides/0022-valkey-cluster.md | LAB | valkey/valkey:9.1.2-alpine | none | tag | PENDING |
| infra/04-data/valkey-cluster/docker-compose.yml | valkey-node-3 | docs/05.operations/guides/0022-valkey-cluster.md | LAB | valkey/valkey:9.1.2-alpine | none | tag | PENDING |
| infra/04-data/valkey-cluster/docker-compose.yml | valkey-node-4 | docs/05.operations/guides/0022-valkey-cluster.md | LAB | valkey/valkey:9.1.2-alpine | none | tag | PENDING |
| infra/04-data/valkey-cluster/docker-compose.yml | valkey-node-5 | docs/05.operations/guides/0022-valkey-cluster.md | LAB | valkey/valkey:9.1.2-alpine | none | tag | PENDING |
| infra/05-messaging/kafka/docker-compose.yml | debezium-db-provision | docs/05.operations/guides/0036-kafka.md | OPTIONAL | postgres:18.6-alpine | none | tag | PENDING |
| infra/05-messaging/kafka/docker-compose.yml | kafbat-ui | docs/05.operations/guides/0036-kafka.md | OPTIONAL | kafbat/kafka-ui:v1.5.0 | none | tag | PENDING |
| infra/05-messaging/kafka/docker-compose.yml | kafka-1 | docs/05.operations/guides/0036-kafka.md | LAB | confluentinc/cp-kafka:8.3.2 | none | tag | PENDING |
| infra/05-messaging/kafka/docker-compose.yml | kafka-2 | docs/05.operations/guides/0036-kafka.md | LAB | confluentinc/cp-kafka:8.3.2 | none | tag | PENDING |
| infra/05-messaging/kafka/docker-compose.yml | kafka-3 | docs/05.operations/guides/0036-kafka.md | LAB | confluentinc/cp-kafka:8.3.2 | none | tag | PENDING |
| infra/05-messaging/kafka/docker-compose.yml | kafka-connect | docs/05.operations/guides/0036-kafka.md | OPTIONAL | hy-home/kafka-connect:8.3.2-debezium-3.6.3 | infra/05-messaging/kafka/Dockerfile.connect | tag | PENDING |
| infra/05-messaging/kafka/docker-compose.yml | kafka-exporter | docs/05.operations/guides/0036-kafka.md | LAB | danielqsj/kafka-exporter:v1.10.0 | none | tag | PENDING |
| infra/05-messaging/kafka/docker-compose.yml | kafka-init | docs/05.operations/guides/0036-kafka.md | LAB | confluentinc/cp-kafka:8.3.2 | none | tag | PENDING |
| infra/05-messaging/kafka/docker-compose.yml | kafka-rest-proxy | docs/05.operations/guides/0036-kafka.md | OPTIONAL | confluentinc/cp-kafka-rest:8.3.2 | none | tag | PENDING |
| infra/05-messaging/kafka/docker-compose.yml | schema-registry | docs/05.operations/guides/0036-kafka.md | OPTIONAL | confluentinc/cp-schema-registry:8.3.2 | none | tag | PENDING |
| infra/06-observability/docker-compose.yml | alertmanager | docs/05.operations/guides/0039-alertmanager.md | HOME | prom/alertmanager:v0.34.1 | none | tag | PENDING |
| infra/06-observability/docker-compose.yml | alloy | docs/05.operations/guides/0040-alloy.md | HOME | grafana/alloy:v1.19.2 | none | tag | PENDING |
| infra/06-observability/docker-compose.yml | cadvisor | docs/05.operations/guides/0044-observability-optimization-hardening.md | HOME | gcr.io/cadvisor/cadvisor:v0.55.1 | none | tag | PENDING |
| infra/06-observability/docker-compose.yml | dcgm-exporter | docs/05.operations/guides/0045-prometheus.md | HOME | nvcr.io/nvidia/k8s/dcgm-exporter:4.8.4 | none | tag | PENDING |
| infra/06-observability/docker-compose.yml | gatus | docs/05.operations/guides/0087-gatus.md | HOME | hy/gatus:local | infra/06-observability/gatus/Dockerfile | floating | PENDING |
| infra/06-observability/docker-compose.yml | grafana | docs/05.operations/guides/0041-grafana.md | HOME | grafana/grafana:13.2.2 | none | tag | PENDING |
| infra/06-observability/docker-compose.yml | grafana-db-provision | docs/05.operations/guides/0041-grafana.md | HOME | postgres:18.6-alpine | none | tag | PENDING |
| infra/06-observability/docker-compose.yml | loki | docs/05.operations/guides/0043-loki.md | HOME | hy/loki:3.7.8-seaweedfs | infra/06-observability/loki/Dockerfile | tag | PENDING |
| infra/06-observability/docker-compose.yml | node-exporter | docs/05.operations/guides/0045-prometheus.md | HOME | quay.io/prometheus/node-exporter:v1.12.1 | none | tag | PENDING |
| infra/06-observability/docker-compose.yml | prometheus | docs/05.operations/guides/0045-prometheus.md | HOME | prom/prometheus:v3.14.0 | none | tag | PENDING |
| infra/06-observability/docker-compose.yml | pushgateway | docs/05.operations/guides/0046-pushgateway.md | OPTIONAL | prom/pushgateway:v1.11.3 | none | tag | PENDING |
| infra/06-observability/docker-compose.yml | pyroscope | docs/05.operations/guides/0047-pyroscope.md | HOME | grafana/pyroscope:2.3.1 | none | tag | PENDING |
| infra/06-observability/docker-compose.yml | tempo | docs/05.operations/guides/0049-tempo.md | HOME | hy/tempo:3.0.3-seaweedfs | infra/06-observability/tempo/Dockerfile | tag | PENDING |
| infra/07-workflow/airflow/docker-compose.yml | airflow-apiserver | docs/05.operations/guides/0050-airflow.md | HOME | hy-home/airflow:3.3.1-keycloak | infra/07-workflow/airflow/Dockerfile | tag | PENDING |
| infra/07-workflow/airflow/docker-compose.yml | airflow-dag-processor | docs/05.operations/guides/0050-airflow.md | HOME | hy-home/airflow:3.3.1-keycloak | infra/07-workflow/airflow/Dockerfile | tag | PENDING |
| infra/07-workflow/airflow/docker-compose.yml | airflow-init | docs/05.operations/guides/0050-airflow.md | HOME | hy-home/airflow:3.3.1-keycloak | infra/07-workflow/airflow/Dockerfile | tag | PENDING |
| infra/07-workflow/airflow/docker-compose.yml | airflow-scheduler | docs/05.operations/guides/0050-airflow.md | HOME | hy-home/airflow:3.3.1-keycloak | infra/07-workflow/airflow/Dockerfile | tag | PENDING |
| infra/07-workflow/airflow/docker-compose.yml | airflow-statsd-exporter | docs/05.operations/guides/0050-airflow.md | HOME | prom/statsd-exporter:v0.31.0 | none | tag | PENDING |
| infra/07-workflow/airflow/docker-compose.yml | airflow-triggerer | docs/05.operations/guides/0050-airflow.md | HOME | hy-home/airflow:3.3.1-keycloak | infra/07-workflow/airflow/Dockerfile | tag | PENDING |
| infra/07-workflow/airflow/docker-compose.yml | airflow-valkey | docs/05.operations/guides/0050-airflow.md | OPTIONAL | valkey/valkey:9.1.2-alpine | none | tag | PENDING |
| infra/07-workflow/airflow/docker-compose.yml | airflow-valkey-exporter | docs/05.operations/guides/0050-airflow.md | OPTIONAL | oliver006/redis_exporter:v1.91.1-alpine | none | tag | PENDING |
| infra/07-workflow/airflow/docker-compose.yml | airflow-worker | docs/05.operations/guides/0050-airflow.md | HOME | hy-home/airflow:3.3.1-keycloak | infra/07-workflow/airflow/Dockerfile | tag | PENDING |
| infra/07-workflow/airflow/docker-compose.yml | flower | docs/05.operations/guides/0050-airflow.md | HOME | hy-home/airflow:3.3.1-keycloak | infra/07-workflow/airflow/Dockerfile | tag | PENDING |
| infra/07-workflow/n8n/docker-compose.yml | n8n | docs/05.operations/guides/0053-n8n.md | HOME | hyhome/n8n:2.29.5-local | infra/07-workflow/n8n/dev.Dockerfile (default from ${N8N_DOCKERFILE:-dev.Dockerfile}) | tag | PENDING |
| infra/07-workflow/n8n/docker-compose.yml | n8n-task-runner | docs/05.operations/guides/0053-n8n.md | HOME | n8nio/runners:2.41.3 | none | tag | PENDING |
| infra/07-workflow/n8n/docker-compose.yml | n8n-task-runner-worker | docs/05.operations/guides/0053-n8n.md | HOME | n8nio/runners:2.41.3 | none | tag | PENDING |
| infra/07-workflow/n8n/docker-compose.yml | n8n-valkey | docs/05.operations/guides/0053-n8n.md | OPTIONAL | valkey/valkey:9.1.2-alpine | none | tag | PENDING |
| infra/07-workflow/n8n/docker-compose.yml | n8n-valkey-exporter | docs/05.operations/guides/0053-n8n.md | OPTIONAL | oliver006/redis_exporter:v1.91.1-alpine | none | tag | PENDING |
| infra/07-workflow/n8n/docker-compose.yml | n8n-worker | docs/05.operations/guides/0053-n8n.md | HOME | hyhome/n8n:2.29.5-local | infra/07-workflow/n8n/dev.Dockerfile (default from ${N8N_DOCKERFILE:-dev.Dockerfile}) | tag | PENDING |
| infra/08-ai/comfyui/docker-compose.yml | comfyui | docs/05.operations/guides/0081-comfyui.md | HOME | yanwk/comfyui-boot:cu126-slim | none | tag | PENDING |
| infra/08-ai/crawl4ai/docker-compose.yml | crawl4ai | docs/05.operations/guides/0091-crawl4ai.md | OPTIONAL | unclecode/crawl4ai:0.9.3 | none | tag | PENDING |
| infra/08-ai/ollama/docker-compose.yml | ollama | docs/05.operations/guides/0056-ollama.md | HOME | ollama/ollama:0.35.0 | none | tag | PENDING |
| infra/08-ai/ollama/docker-compose.yml | ollama-exporter | docs/05.operations/guides/0056-ollama.md | HOME | lucabecker42/ollama-exporter:1.0.3 | none | tag | PENDING |
| infra/08-ai/open-webui/docker-compose.yml | open-webui | docs/05.operations/guides/0057-open-webui.md | HOME | ghcr.io/open-webui/open-webui:v0.11.3-cuda | none | tag | PENDING |
| infra/09-tooling/conftest/docker-compose.yml | conftest | docs/05.operations/guides/0095-conftest.md | OPTIONAL | openpolicyagent/conftest:v0.70.1 | none | tag | PENDING |
| infra/09-tooling/k6/docker-compose.yml | k6 | docs/05.operations/guides/0061-k6.md | DEV | none | infra/09-tooling/k6/Dockerfile | build-only | PENDING |
| infra/09-tooling/locust/docker-compose.yml | locust-master | docs/05.operations/guides/0062-locust.md | DEV | none | infra/09-tooling/locust/Dockerfile | build-only | PENDING |
| infra/09-tooling/locust/docker-compose.yml | locust-worker | docs/05.operations/guides/0062-locust.md | DEV | none | infra/09-tooling/locust/Dockerfile | build-only | PENDING |
| infra/09-tooling/opentofu/docker-compose.yml | opentofu | docs/05.operations/guides/0082-opentofu.md | DEV | hy-home/opentofu:1.12.6-local | infra/09-tooling/opentofu/docker-compose.yml#dockerfile_inline:opentofu | tag | PENDING |
| infra/09-tooling/pact-broker/docker-compose.yml | pact-broker | docs/05.operations/guides/0093-pact-broker.md | OPTIONAL | pactfoundation/pact-broker:3.0.0-pactbroker2.121.2 | none | tag | PENDING |
| infra/09-tooling/pact-broker/docker-compose.yml | pact-broker-db-provision | docs/05.operations/guides/0093-pact-broker.md | OPTIONAL | postgres:18.6-alpine | none | tag | PENDING |
| infra/09-tooling/registry/docker-compose.yml | registry | docs/05.operations/guides/0065-registry.md | HOME | registry:3 | none | tag | PENDING |
| infra/09-tooling/renovate/docker-compose.yml | renovate | docs/05.operations/guides/0083-renovate.md | DEV | renovate/renovate:44.115.12-full | none | tag | PENDING |
| infra/09-tooling/restic/docker-compose.yml | backup-sqlite-export | docs/05.operations/guides/0021-backup-and-restore.md | DEV | python:3.13.15-alpine | none | tag | PENDING |
| infra/09-tooling/restic/docker-compose.yml | restic | docs/05.operations/guides/0021-backup-and-restore.md | DEV | restic/restic:0.19.1 | none | tag | PENDING |
| infra/09-tooling/restic/docker-compose.yml | restic-offsite | docs/05.operations/guides/0021-backup-and-restore.md | DEV | restic/restic:0.19.1 | none | tag | PENDING |
| infra/09-tooling/sonarqube/docker-compose.yml | sonarqube | docs/05.operations/guides/0066-sonarqube.md | OPTIONAL | sonarqube:26.9.0.129388-community | none | tag | PENDING |
| infra/09-tooling/terrakube/docker-compose.yml | terrakube-api | docs/05.operations/guides/0069-terrakube.md | DEV | azbuilder/api-server:2.33.2 | none | tag | PENDING |
| infra/09-tooling/terrakube/docker-compose.yml | terrakube-executor | docs/05.operations/guides/0069-terrakube.md | DEV | azbuilder/executor:2.33.2 | none | tag | PENDING |
| infra/09-tooling/terrakube/docker-compose.yml | terrakube-ui | docs/05.operations/guides/0069-terrakube.md | DEV | azbuilder/terrakube-ui:2.33.2 | none | tag | PENDING |
| infra/09-tooling/wiremock/docker-compose.yml | wiremock | docs/05.operations/guides/0092-wiremock.md | OPTIONAL | wiremock/wiremock:3.13.2-alpine | none | tag | PENDING |
| infra/10-communication/mailpit/docker-compose.yml | mailpit | docs/05.operations/guides/0084-mailpit.md | DEV | axllent/mailpit:v1.31.2 | none | tag | PENDING |
| infra/10-communication/stalwart/docker-compose.yml | stalwart | docs/05.operations/guides/0070-mail.md | OPTIONAL | stalwartlabs/stalwart:v0.16.22 | none | tag | PENDING |
| infra/10-communication/stalwart/docker-compose.yml | stalwart-config | docs/05.operations/guides/0070-mail.md | OPTIONAL | hy-home/stalwart-config:0.16.22-cli1.0.12-local | infra/10-communication/stalwart/config/Dockerfile | tag | PENDING |
| infra/11-laboratory/dozzle/docker-compose.yml | dozzle | docs/05.operations/guides/0072-dozzle.md | OPTIONAL | amir20/dozzle:v11.1.1 | none | tag | PENDING |
| infra/11-laboratory/jupyterlab/docker-compose.yml | jupyterlab | docs/05.operations/guides/0089-jupyterlab.md | OPTIONAL | hy-home/jupyterlab:scipy-local | infra/11-laboratory/jupyterlab/Dockerfile | tag | PENDING |
| infra/11-laboratory/mlflow/docker-compose.yml | mlflow | docs/05.operations/guides/0088-mlflow.md | OPTIONAL | hy-home/mlflow:3.16.1-local | infra/11-laboratory/mlflow/Dockerfile | tag | PENDING |
| infra/11-laboratory/mlflow/docker-compose.yml | mlflow-db-provision | docs/05.operations/guides/0088-mlflow.md | OPTIONAL | postgres:18.6-alpine | none | tag | PENDING |
| infra/11-laboratory/open-notebook/docker-compose.yml | open_notebook | docs/05.operations/guides/0073-open-notebook.md | OPTIONAL | lfnovo/open_notebook:v1-latest-single | none | tag | PENDING |
| infra/11-laboratory/open-notebook/docker-compose.yml | surrealdb | docs/05.operations/guides/0080-surrealdb.md | OPTIONAL | none | infra/11-laboratory/open-notebook/surrealdb/Dockerfile | build-only | PENDING |
| infra/11-laboratory/redisinsight/docker-compose.yml | redisinsight | docs/05.operations/guides/0076-redisinsight.md | OPTIONAL | redis/redisinsight:3.8.0 | none | tag | PENDING |
| infra/12-analytics/dbt/docker-compose.yml | dbt | docs/05.operations/guides/0090-dbt.md | OPTIONAL | hy-home/dbt-postgres:1.11-local | infra/12-analytics/dbt/Dockerfile | tag | PENDING |
| infra/12-analytics/dbt/docker-compose.yml | dbt-db-provision | docs/05.operations/guides/0090-dbt.md | OPTIONAL | postgres:18.6-alpine | none | tag | PENDING |
| infra/12-analytics/flink/docker-compose.yml | flink-jobmanager | docs/05.operations/guides/0094-lakehouse.md | OPTIONAL | hy-home/flink-iceberg:2.1.3-iceberg1.11.0-local | infra/12-analytics/flink/Dockerfile | tag | PENDING |
| infra/12-analytics/flink/docker-compose.yml | flink-taskmanager | docs/05.operations/guides/0094-lakehouse.md | OPTIONAL | hy-home/flink-iceberg:2.1.3-iceberg1.11.0-local | infra/12-analytics/flink/Dockerfile | tag | PENDING |
| infra/12-analytics/great-expectations/docker-compose.yml | great-expectations | docs/05.operations/guides/0094-lakehouse.md | OPTIONAL | hy-home/great-expectations:1.23.1-local | infra/12-analytics/great-expectations/Dockerfile | tag | PENDING |
| infra/12-analytics/spark/docker-compose.yml | spark | docs/05.operations/guides/0094-lakehouse.md | OPTIONAL | hy-home/spark-iceberg:4.1.3-iceberg1.11.0-local | infra/12-analytics/spark/Dockerfile | tag | PENDING |
| infra/12-analytics/superset/docker-compose.yml | superset | docs/05.operations/guides/0097-superset.md | OPTIONAL | hy-home/superset:6.1.0-local | infra/12-analytics/superset/Dockerfile | tag | PENDING |
| infra/12-analytics/superset/docker-compose.yml | superset-db-provision | docs/05.operations/guides/0097-superset.md | OPTIONAL | postgres:18.6-alpine | none | tag | PENDING |
| infra/12-analytics/superset/docker-compose.yml | superset-init | docs/05.operations/guides/0097-superset.md | OPTIONAL | hy-home/superset:6.1.0-local | infra/12-analytics/superset/Dockerfile | tag | PENDING |
| infra/12-analytics/trino/docker-compose.yml | trino | docs/05.operations/guides/0094-lakehouse.md | OPTIONAL | trinodb/trino:483 | none | tag | PENDING |

### Build and package source index

The baseline contains 34 Compose service identities selecting 21 distinct build
sources, including the inline OpenTofu Dockerfile. W3 owns one built identity,
W4 thirteen, W5 twelve and W6 eight. Shared Dockerfiles do not waive each
identity's Compose command, build-argument and mounted-input reconciliation.

FROM tags and ARG defaults are declared inputs, not immutable bytes. Checksummed ADD inputs are byte-pinned. Requirements entries are source package declarations, not installed versions.

| Dockerfile | FROM declaration | ARG defaults | Checksummed ADD count | Adjacent requirements declarations |
| --- | --- | --- | ---: | --- |
| infra/02-auth/oauth2-proxy/dev.Dockerfile | quay.io/oauth2-proxy/oauth2-proxy:v7.15.4, alpine:3.24.2 | none | 0 | none |
| infra/04-data/mng-db/pg/backup/Dockerfile | postgres:18.6-alpine | none | 0 | none |
| infra/04-data/opensearch/Dockerfile | opensearchproject/opensearch:3.8.0 | none | 0 | none |
| infra/05-messaging/kafka/Dockerfile.connect | quay.io/debezium/connect:3.6.3.Final, confluentinc/cp-kafka-connect:8.3.2 | none | 0 | none |
| infra/06-observability/gatus/Dockerfile | golang:1.26.4-alpine3.22, alpine:3.24 | none | 0 | none |
| infra/06-observability/loki/Dockerfile | grafana/loki:3.7.8, alpine:3.24.2 | none | 0 | none |
| infra/06-observability/tempo/Dockerfile | grafana/tempo:3.0.3, alpine:3.24.2 | none | 0 | none |
| infra/07-workflow/airflow/Dockerfile | apache/airflow:${AIRFLOW_VERSION} | AIRFLOW_VERSION=3.3.2, AIRFLOW_VERSION=3.3.1, PYTHON_VERSION=3.13, KEYCLOAK_PROVIDER_VERSION=0.9.0 | 0 | none |
| infra/07-workflow/n8n/dev.Dockerfile | alpine:3.24.2, n8nio/n8n:${N8N_VERSION} | N8N_VERSION=2.41.3 | 0 | none |
| infra/09-tooling/k6/Dockerfile | grafana/k6:2.2.0 | none | 0 | none |
| infra/09-tooling/locust/Dockerfile | locustio/locust:2.46.6 | none | 0 | none |
| infra/09-tooling/opentofu/docker-compose.yml#dockerfile_inline:opentofu | ghcr.io/opentofu/opentofu:1.12.6-minimal, alpine:3.24 | none | 0 | none |
| infra/10-communication/stalwart/config/Dockerfile | ghcr.io/stalwartlabs/cli:1.0.12, stalwartlabs/stalwart:v0.16.22 | none | 0 | none |
| infra/11-laboratory/jupyterlab/Dockerfile | quay.io/jupyter/scipy-notebook:${JUPYTER_BASE_TAG} | JUPYTER_BASE_TAG=2026-07-28 | 0 | infra/11-laboratory/jupyterlab/requirements.txt: mlflow==3.16.1, polars==1.44.2, pyarrow==23.0.1, duckdb==1.5.5, psycopg[binary]==3.3.6, boto3==1.43.75, s3fs==2026.7.0, confluent-kafka==2.15.1, jupysql==0.11.1, optuna==4.6.0 |
| infra/11-laboratory/mlflow/Dockerfile | ghcr.io/mlflow/mlflow:v3.16.1 | none | 0 | infra/11-laboratory/mlflow/requirements.txt: psycopg2-binary==2.9.10, boto3==1.36.26 |
| infra/11-laboratory/open-notebook/surrealdb/Dockerfile | surrealdb/surrealdb:v2, debian:bookworm-slim | none | 0 | none |
| infra/12-analytics/dbt/Dockerfile | python:3.12-slim-bookworm | none | 0 | infra/12-analytics/dbt/requirements.txt: dbt-core==1.11.15, dbt-postgres==1.11.0 |
| infra/12-analytics/flink/Dockerfile | flink:2.1.3-scala_2.12-java21 | none | 5 | none |
| infra/12-analytics/great-expectations/Dockerfile | python:3.12-slim-bookworm | none | 0 | infra/12-analytics/great-expectations/requirements.txt: great-expectations==1.23.1, trino[sqlalchemy]==0.340.0 |
| infra/12-analytics/spark/Dockerfile | apache/spark:4.1.3-scala2.13-java21-python3-ubuntu | none | 2 | none |
| infra/12-analytics/superset/Dockerfile | apache/superset:6.1.0 | none | 0 | infra/12-analytics/superset/requirements.txt: authlib==1.8.0, psycopg2-binary==2.9.13, trino[sqlalchemy]==0.340.0 |

### Build inputs beyond image labels (source observations; semantic audit PENDING)

Compose build arguments take precedence over Dockerfile defaults for the
corresponding declared build. Operator overrides and alternate Dockerfiles
remain UNVERIFIED; no private interpolation or Compose rendering was needed.

| Source / exact identities | Additional declared source evidence | Certainty / follow-up owner |
| --- | --- | --- |
| `infra/07-workflow/airflow/docker-compose.yml`: airflow-apiserver, airflow-dag-processor, airflow-init, airflow-scheduler, airflow-triggerer, airflow-worker, flower | Shared build args: AIRFLOW_VERSION=3.3.1, PYTHON_VERSION=3.13, KEYCLOAK_PROVIDER_VERSION=0.9.0. Dockerfile's pre-FROM default is 3.3.2 and in-stage default 3.3.1; Compose overrides both. pip declares common-compat>=1.18.0 and python-keycloak>=5.0.0 under the constraints-3.3.1/constraints-3.13.txt URL, then keycloak provider==0.9.0 with --no-deps. | Declared Compose base/constraint selection 3.3.1; mutable image/constraint URL and uninspected transitive resolution. W5 compatibility review PENDING. |
| `infra/07-workflow/n8n/docker-compose.yml`: n8n, n8n-worker | Both declare N8N_VERSION=2.29.5, overriding dev.Dockerfile default 2.41.3; `${N8N_DOCKERFILE:-dev.Dockerfile}` permits another Dockerfile. | Default Compose build selects 2.29.5; image labels/defaults and task-runner declarations must be reconciled by W5, PENDING. |
| `infra/11-laboratory/jupyterlab/Dockerfile` | JUPYTER_BASE_TAG=2026-07-28 has no Compose build-arg override; ten direct requirements are shown above. | Date tag and requirements are mutable/version-selected inputs, no package hashes; transitive/runtime versions UNVERIFIED. W6 PENDING. |
| `infra/04-data/mng-db/pg/backup/Dockerfile` | apk explicitly selects pgbackrest=2.58.0-r0. | Package release pin, no artifact checksum; installed bytes UNVERIFIED. W4 PENDING. |
| `infra/04-data/opensearch/Dockerfile` | Five built-in plugins have no separate version; prometheus-exporter URL selects 3.5.0.0 while FROM selects 3.8.0 and LABEL still describes 3.5. | Release URL without checksum; compatibility and stale label assessment W4 PENDING. |
| `infra/06-observability/gatus/Dockerfile` | Source archive selects commit ed1107b41a30e22047eecfb6dbc3be5e39829d5a, verified during build by declared SHA-256 5638de42703fc6a936b9820920c3e07d1b1e017f1aabea94808155ed9953433a; local patches/oidc-hardening.patch applies before go mod tidy -diff and source tests. | Byte-pinned archive plus local patch; no local go.mod/go.sum declaration to inspect, transitive/build results UNVERIFIED. W5 PENDING. |
| `infra/12-analytics/flink/Dockerfile` | Five SHA-256 ADD inputs select Iceberg runtime and AWS bundle 1.11.0, Kafka SQL connector 5.0.0-2.1, Hadoop client API/runtime 3.5.0; exact URLs/checksums remain in this Dockerfile. | Byte-pinned downloads; base image is mutable. W4 compatibility/runtime audit PENDING. |
| `infra/12-analytics/spark/Dockerfile` | Two SHA-256 ADD inputs select Iceberg Spark runtime and AWS bundle 1.11.0; exact URLs/checksums remain in this Dockerfile. | Byte-pinned downloads; base image is mutable. W4 compatibility/runtime audit PENDING. |
| `infra/11-laboratory/mlflow/requirements.txt`, `infra/12-analytics/{dbt,great-expectations,superset}/requirements.txt` | Direct equality pins are expanded above; these and JupyterLab are all five tracked infra requirements files. | No package hashes or complete transitive lock; installed versions UNVERIFIED. W4/W6 PENDING. |
| Gatus, Loki, Tempo, n8n dev and OpenTofu inline Dockerfiles; open-notebook/surrealdb and dbt Dockerfiles | apk/apt packages are selected by name without release pins (CA certificates, shell/network tools, fonts, patch/wget or git as applicable). | Repository-resolved package versions UNVERIFIED. Applicable W4/W5/W6 audits PENDING. |

The remaining build entries above copy binaries/plugins from mutable FROM
images or add local scripts, without a separate package release declaration.
The seven checksummed ADDs and Gatus archive checksum bind only those inputs,
not a whole image. No download, package install, build or runtime probe ran.

### Shared wave evidence format

W3-W7 record evidence in their own Task. Each actual evidence row has all fields
below; a PENDING field is an unresolved audit item, not a satisfied criterion.
Named shared service sets are permitted only after checking their differences.

| Artifact ID + exact service identity | Required topic | Implementation path/section | Declared version + certainty | Official URL + release/section | Finding | Original document/section | Final owner/section | Applicability/exception | Action | Check/result | Reviewer disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

The Spec's nine required-topic rows are authoritative. The Plan's former
reference to ten was a counting error, not an extra or omitted requirement.
For compact service-topic tracking, waves may map ten columns to the same rows:
T1 purpose/users/class/limits (row 1); T2 source/version/profile/dependency/
readiness (2); T3 access/auth/credentials (3); T4 configuration inputs and T5
mounts/data ownership/persistence (both 4); T6 normal use/signals/resources (5);
T7 controls/approvals/exceptions/accountability (6); T8 provisioning/start/stop/
changes/upgrades (7); T9 diagnosis/results/stops/escalation (8); T10 backup/
restore/rollback/credential maintenance/deletion/cleanup (9). At baseline capture all ten cells for
each of the 153 identities were PENDING; wave Tasks record subsequent results. Non-service subjects use applicable
Spec content and record concrete non-applicability reasons.

A finding is missing, incomplete, duplicate, contradictory or consistent;
unsupported implementation and justified non-applicability are explicit
outcomes with a reason. Every original section maps to retained, corrected or
linked final content; no unexplained drop. Official evidence must match the
source-selected release; unavailable matching evidence stays PENDING or
UNVERIFIED. No official product page was fetched in W1, and none is implied
by an image tag or filename. Wave-specific review must fill this field.

### Language correction checkpoint

The user reaffirmed that Spec, Plan and Task prose is English. Stage05 role
prose and README prose remain Korean under the document-language contract.
SPEC0197's four package documents and SPEC0198 Spec/Plan/Tasks0001–0004 were
checked; two retained Korean heading lists in Tasks0003/0004 now use explicitly
labelled English glosses. At this checkpoint Task0005's Korean draft was being corrected before acceptance;
the final English-language acceptance is recorded below.

W2–W4 semantic language audit corrections:44 role files,116 exact replacement
blocks. Independent review found three minor meaning/tense ambiguities in
GDE0079; all three were corrected before applying unique/hash-matching blocks.
RUN0015's actual2026-09-22 observation now uses the required historical quotation
marker and verified source commit. Quoted payload SHA-256 remains
`ca16c759220f73d6ac267b77ffe933128770a7bcc7ff4518102bae5c88021704`.
Commands, links, IDs and mandatory headings are preserved. Focused metadata:
44 selected, zero violations. Global language mode:1,021 documents,10,680 links,
zero failures/warnings. Scoped independent final confirmation by
`/root/ops_w2_review`: CLEAR/APPROVED for all116 applied blocks, the three wording
fixes, historical payload preservation and the two English Task glosses.
Spec/Plan global constraints now state the user-confirmed language boundary
explicitly; this clarifies the existing authoring contract rather than expanding
implementation scope.

### Cross-document integration disposition

Ruling: source-package README statements that contradict the corrected W5
operating contract require bounded documentary reconciliation during W8. This
also serves the user's existing infra documentation-consistency request. Keep
versions/settings owned by source, preserve useful content, and change no
Compose, Dockerfile or runtime behavior. The independent reviewer identified
Crawl4AI route-auth exceptions, Ollama/Tempo profile summaries, Pyroscope's
image-compatible readiness command and Loki/Grafana restart-versus-recreate
wording. Earlier W5 source inputs additionally identify Alloy telemetry,
Grafana role fallback, Airflow build/interpreter claims, n8n profile/readiness
and ComfyUI network/persistence wording. Related AD0006/0008/0031 corrections
are coordinated with SPEC0197's already-approved current-description scope.
These integration items were pending at that checkpoint; twelve README fixes
were subsequently accepted in the receipt below. The risk of an omitted correction is a contradictory operator entrypoint.

W5 final receipt, 2026-10-01:60 leaves/34 identities/306 topic cells/12 built identities accepted by independent Spec/quality review. Integrating reviewer confirmed61/61 final hashes; earlier snapshots are superseded. README integration12/12 accepted, focused metadata12/0. Language corrections preserve all11 current Spec/Plan/Task documents in English. W6/W7 body work and W8 closure remain pending.

SPEC0197 handoff: the twelve additional source prefixes follow the exact crosswalk in SPEC0197 Task0002 W5.2–W5.3; immutable W1 source manifests retain their original dates/paths. W6/W7 must use final capability paths without rewriting baseline observations. OPTIONAL classification and153 identities remain unchanged.

### W8 partial integration checkpoint

Completed-wave independent audit reconfirmed225 baseline leaves,87 subjects and
153 identities. W3–W5 account for137 leaves,129 identities and1,161 topic cells;
the remaining88 baseline leaves belong exactly to W6/W7. W3 earlier/final link
counts and stale present-tense review labels are now distinguished without
removing initial FAIL/REQUEST_CHANGES evidence. Fifteen service README source
corrections are independently accepted; runtime behavior is unchanged.

Explicit-path metadata retry uncovered Task0005 heading deficits despite the
earlier author-reported scoped PASS. Existing content was relocated to registered
Task sections, with no change to its60 accepted leaves. Initial integration
check selected38 and failed only that Task; fix2 selected41 and passed with
zero violations/overrides. New-path initial draft rules also apply to relocated
READMEs; original active records remain in Git. This is a partial W8 receipt,
not final package acceptance; W6/W7 and the frozen combined gate remain open.

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: all 225 baseline leaves and 153 service identities are accounted for in the accepted audit | [Operations documentation](../../../05.operations/README.md) |
| 2 | W2 | PASS: issued identities and role paths are preserved and final navigation and ownership checks pass | [Operations navigation](../../../05.operations/README.md) |
| 3 | W7 | PASS: system operating routes and common owners were reconciled with explicit capability limits | [System operations guide](../../../05.operations/guides/0099-system-operations.md) |
| 4 | W3 | PASS: identity ownership and applicable role documents were checked across all accepted service waves | [Operations documentation](../../../05.operations/README.md) |
| 5 | W4 | PASS: the 59-leaf data audit preserved section mappings and resolved reviewed documentary conflicts | [Operations documentation](../../../05.operations/README.md) |
| 5 | W5 | PASS: the 60-leaf observability, workflow and AI audit reconciled source versions, topics and section mappings | [Operations documentation](../../../05.operations/README.md) |
| 5 | W6 | PASS: the 67-leaf tooling, communication and laboratory audit preserved historical payloads and closed review findings | [Operations documentation](../../../05.operations/README.md) |
| 6 | W8 | PASS: the final frozen changed gate and independent semantic review accepted the integrated source tree | N/A: Gate and independent review receipts remain in this execution Task. |
| 7 | W8 | PASS: source verification is distinguished from unperformed runtime and recovery observations | N/A: Execution boundaries and unperformed observations remain in the wave Tasks. |

Historical pre-acceptance checkpoint (subsequently resolved by the language and
wave receipts above): intermediate language check, 2026-10-01, during active W5 authoring: `python3 scripts/validation/check-document-links.py --mode language` reported18 Korean-language mismatches, all in W5-owned leaves. The author received the exact paths and must correct meaningful prose, not thresholds or padding. This is an in-progress FAIL, not final W5 acceptance. Separate manual W2–W4 audit also identified English explanatory prose despite earlier numeric checks; correction and independent language re-review remain required.

W1 inventory and source-index construction and independent W1 review are complete.
Current receipt status: W1–W8 are accepted. All wave and adjacent-owner reviews passed; the final frozen integrated changed gate exited0. All seven source/document acceptance criteria are complete, subject to the runtime and implementation limits retained below.

| Check | Result | Boundary |
| --- | --- | --- |
| Public-source manifest joins | PASS: 225 unique role paths, 87 subjects, 153 unique identities, unique Guide owner and exactly one wave per leaf | Frontmatter/source inventory only; no body audit |
| `python3 scripts/validation/check-operations-catalog.py` | PASS, exit 0 on W1 source state | No initial catalog failure observed; prior implementer also reported PASS |
| `python3 -m unittest tests.lib.document_governance.test_operations_catalog tests.lib.document_governance.test_operations_taxonomy` | PASS, exit 0: 99 tests in 116.056s | Existing tests only; no test/checker edit |
| Scoped Task metadata | PASS, exit 0: selected=1, violations=0, legacy_exceptions=0, transition_overrides=0 | check-changed with only this Task selected |
| `python3 scripts/validation/check-document-links.py --mode all` | PASS, exit 0: failures=0, warnings=1 | Existing warning: 2,870 legacy links lack capture source; historical resolution UNVERIFIED |
| `python3 scripts/validation/run-ci-gate.py --profile changed` | NOT_RUN by W1 during concurrent edits | Integrator owns final stable-tree run; concurrent Git mutation can invalidate mutation-sensitive tests; no relaxation authorized |
| Runtime, build, recovery and hosted CI | NOT_RUN | Outside W1 public-source scope |
| Domain-code coverage/new tests | N/A | Documentation-only change; no executable repository logic modified |

| Source acceptance mapping | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1, W3-W8 | W1 exact manifest and all W1–W7 receipts accepted | Existing role documents and wave Tasks |
| 2 | W2, W8 | PASS: navigation and153 identity-owner joins verified by final W8 checks | Operations indexes |
| 3 | W2, W7, W8 | PASS: system routes, W7 reconciliation and W8 final gate | System Guide and existing procedures |
| 4 | W3-W8 | 153 identities /1377 topic cells reviewed across W3–W6 | Service subjects and shared owners |
| 5 | W3-W8 | All225 baseline leaf mappings accepted across W3–W7; two new system leaves accepted | Role documents and section mappings |
| 6 | W8 | PASS: final registered changed gate exit0 and independent semantic review APPROVED | This Task |
| 7 | W1-W8 | PASS: source-only boundaries preserved; runtime/recovery NOT_RUN | This Task and wave evidence |

## Review Evidence

W4 complete (uncommitted scoped snapshot), 2026-10-01: `/root/ops_w4_independent_review` fix1 review Spec PASS / quality ACCEPT, I1–I3/M1–M3 addressed, no new finding. Exact59 leaves/87 identities/13 built identities/eight Dockerfiles; focused metadata14/0, catalog PASS, links10514/0 failures with one historical warning, scoped diff/static PASS. Reviewed Task receipt and full details reside in Task0004. At that W4 checkpoint W5–W8 remained pending.

Spec independent review CLEAR. Plan self-review: all 88 distinct baseline
filenames (225 role leaves) appear in its file map; acceptance criteria1-7 mapped.
W1 independent review by `/root/ops_w1_review` on 2026-10-01: specification
compliance CLEAR; quality CLEAR; no findings. Reviewer verified all 225 artifact
rows, 153 service-owner/image/build joins, 21 build sources, five requirements
files and effective overrides against source. Reviewed Task SHA-256 was
`368de4d27e1e83f588eabbc89b26d564ad0f470c2694a696929283c4a7f22014`.
At the W1–W5 checkpoint those waves were complete as independently reviewed,
uncommitted snapshots; W6/W7 and W8 were then pending and are accepted below.
Inventory/source inspection alone is not a review disposition for role bodies.

Final frozen gate attempt1: FAIL in two SPEC0197 hardening test fixtures, after628 document regression tests and the document/catalog/link checks passed. No documentary finding resulted. SPEC0197 Task0002 records the exact test-root/moved-fixture corrections and19 focused GREEN tests; complete integrated rerun is still required.

Frozen gate attempt2: the136-test quickwin batch passed (23 skips), closing both fixture failures. The next script-manifest check found four stale consumer paths after commands moved to Runbook owners. Parent changed only those consumer declarations: hook calls to RUN-0004, mount-hash check to RUN-0086, and generator use to RUN-0096; authority, mutation classification and test declarations remain unchanged. Independent integration review accepted all four substitutions against actual invocations. Focused manifest PASS; remaining GitHub workflow contract PASS (5 workflows/7 jobs/8 actions); Storybook contract exit0. The first focused manifest attempt additionally required its existing sorted-consumer rule; ordering was corrected. Full frozen gate attempt3 remains pending; prior failures are retained.

### W6/W7 and final navigation review receipts

On 2026-10-01, independent W6 final review accepted67 leaves/24 identities/216 topic cells, including683 original heading mappings and four historical payloads. Three initial findings were corrected and re-reviewed. Independent W7 fix-round1 review accepted21 common leaves, closed four findings, and verified71 profile memberships and the unchanged RUN-0098 historical payload. Exact wave evidence and review manifests reside in Tasks0006/0007.

The independent W8 navigation review accepted225 baseline to227 current leaves (78 Guides/75 Policies/74 Runbooks),153 unique current source/service bindings, stable IDs and all12 tier routes. No omission, duplicate owner or required sibling gap was found. Fifteen README integrations and the subsequent Stalwart ownership qualification were independently accepted. The final registered gate subsequently passed on the frozen source/index snapshot.

Final adjacent review accepted three public-document deltas: secrets README and RUN-0096 distinguish mode drift from rejected input; RUN-0085 uses the official accessor lookup form and requires authoritative revocation evidence with positive controls. The reviewer corrected its earlier F1 mode assessment explicitly. Task0007 records the superseding RUN-0096 hash; all other accepted wave bodies remain unchanged.

### Final W8 acceptance

On2026-10-01 the third frozen `python3 scripts/validation/run-ci-gate.py --profile changed` run exited0 across all13 selected public entrypoints. Active metadata417/0 violations; links1025 documents/10942 links/0 failures/1 existing warning (2870 uncaptured legacy links); operations catalog PASS;628 document regression tests PASS;136 quickwin tests OK with23 skips; supply-chain, Compose/security, Conftest376 assertions, script manifest, workflow and Storybook contracts PASS. Final log SHA-256 `4a3071ff1b9502e877bd96a439fe1912f2cd7b073d8f8448f8d98c557f886669`. Initial failures and their independently accepted corrections remain above; a failed attempt is not rewritten as PASS.

Independent final integration review: Spec PASS / quality APPROVED. All67 W6 bodies match their accepted hashes;20 W7 bodies match fix1 and RUN-0096 matches its accepted adjacent-fix hash; six navigation bodies remain unchanged. All225 baseline leaves plus two system leaves,153 identities and1377 service/topic cells are accounted for. Current source scope is complete. Registered Conftest used an isolated temporary policy container; application deployment, secret rotation, build/recovery rehearsal, installed-unit refresh and hosted CI remain NOT_RUN. Existing source nonconformances retain their controls and require separately scoped implementation.

## Commit Ledger

Integrated source commit: `0d42c5edf584fcae7cd78a26fee263492e193885`.
The following worker receipt records the earlier authoring checkpoint.

No SPEC-0198 implementation commit. Preserve current unrelated/staged work;
workers do not commit or mutate the shared index. Proposed delivery boundaries
are W1 baseline, reviewed W2 shared owners, independently reviewed W3-W7 batches,
then W8 integration evidence. These are planned boundaries, not recorded commits;
the integrating owner determines authorized staging/delivery after review.

## Rulings

Final naming handoff: SPEC0197 W6 source validation and independent review are
APPROVED; five retained packages now use09-platform-ops. W6/W7 may consume the
final map. Their exact leaf ownership is disjoint, so remaining body drafting
may run concurrently after the naming freeze; both still require independent
review before W8. No index mutation or combined gate while either writer runs.
RUN0098 retains the separate SPEC0182 ownership and historical-payload boundary.

- Ruling: canonical Tasks are the only execution ledger, overriding generic
  skill scratch progress files. Cost if wrong: evidence routing needs correction,
  but no user content is lost. Temporary briefs/diffs may exist under task-owned
  `/tmp` and do not replace these receipts.
- Ruling: use task-scoped before/after file snapshots for reviews while approved
  dependency work remains uncommitted. Cost if wrong: regenerate a scoped diff;
  never treat HEAD alone as the full implemented state.
- Ruling: serialize implementers under the selected subagent procedure; independent
  read-only reviews/research and ongoing gates may overlap. Cost if wrong: longer
  elapsed time, with explicit file ownership preserved.
- Ruling: no keyword-only semantic scoring or boilerplate generation. Every
  service/topic and existing instruction needs substantive source-backed review.

- Ruling: reconcile the ESO five-entry scope only against the later existing
  SPEC-0180/Task 0008 owner evidence and commits `e3d811870`/`5fb725b2a`, verified
  by independent security review; do not infer authorization from source alone.
  Preserve the restrictive unauthenticated-route policy for grafana-static,
  whose standing exception was not established, and document nonconformance.
  Cost if wrong: permission documentation would misstate the approved boundary;
  no ACL/runtime change is made, and W3 retains the exact provenance for review.

Initial W4 review checkpoint (superseded by fix1 acceptance above):
W4 independent review by `/root/ops_w4_independent_review` on 2026-10-01: specification FAIL, quality REQUEST_CHANGES; Critical0/Important3/Minor3. Exact59 leaves/87 service identities/nine topics/13 built identities/eight Dockerfiles inspected. Fix round1/5 dispatched to the original author: active Guide credential examples, diagnostic dependency side effects, and reversed WAL-drop warning. Three bounded Minor identity/process/profile corrections are included. No W4 completion claim; scoped re-review required before W5.

## Deferred Items

W3 source/content audit passed independent rules/specification/quality review.
Minor closed during W8 receipt reconciliation: Task0003 now distinguishes the
earlier10,285-link and final10,286-link PASS receipts; no content blocker existed.

Runtime changes, security implementation fixes, publication, merge and archival
disposition remain outside the approved documentation execution scope.
