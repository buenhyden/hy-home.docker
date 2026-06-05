---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-06-04-docs-implementation-audit.md -->

# Task: docs/01-05 Content-vs-Implementation Audit

## Overview

This document is an audit report that compares the **authored content** in
`docs/01.requirements` through `docs/05.operations` against tracked `infra/**`
implementation at a semantic unit level. The decision criterion is whether
"document content vs current implementation" matches, not whether link,
governance, or chain validation passes. This report is Phase B
(archive/correction) execution and verification evidence, and it references
governance documents instead of a parent Spec because this is cross-cutting
governance work (`documentation-protocol.md` §8.5).

## Inputs

- **Plan**: Approved plan-mode plan (docs/01-05 content-vs-implementation reconciliation)
- **Implementation SoT**: tracked `infra/**` (compose, configs, scripts, `infra/tech-stack.versions.json`)
- **Existing signals**: `scripts/validation/check-doc-implementation-alignment.sh`, `docs/98.archive/README.md` ledger

## Working Rules

- The criterion is content vs implementation. Passing automated checks is a
  necessary condition, not the success criterion.
- Do not artificially inflate accurately completed documents into archive
  candidates (honest reporting).
- Destructive actions (archive/delete) run only when whole-document evidence
  confirms a conflict with the current implementation.

## Methodology & Coverage

- **Structural mapping (100%)**: Inventoried Stage 01-05 documents by
  stage/tier/service and mapped them to 40 compose-bearing implementation roots,
  tier-level compose service documents, and governance surfaces.
- **Implementation reconciliation**: candidate status/lifecycle groups, Stage 05 structure, and every implemented
  service/tier current-truth pass from `01-gateway` through `11-laboratory` were compared against tracked
  `infra/**`, scripts, compose profile validators, hardening checks, and service READMEs.
- **Signal scans**: frontmatter status distribution, legacy/deprecated terms,
  operations-infra coverage,
  runtime version literals, service-local compose proof drift, archive links, stage taxonomy shorthand, and
  stale command/control literals.
- **Coverage closure**: unresolved active-doc current-truth blockers are 0. Runtime-only live rehearsals that
  need a running local environment remain explicitly scoped as future evidence, not active documentation drift.

## Key Finding

The 2026-06-02 reconciliation already archived documents that conflicted
globally with implementation (unimplemented Airbyte, conflicting Codex
Markdown/HADS chains, and similar cases). In this continuation, the misplaced
ksqlDB guide in `05-messaging`, duplicate Airflow DAG guide in `07-workflow`,
duplicate Ollama setup/inference guides in `08-ai`, duplicate IaC automation
guide in `09-tooling`, and duplicate Vault setup guide in `03-security` were
moved to archive tombstones. In `01-gateway`, `10-communication`, and
`11-laboratory`, mismatches between documentation criteria and implementation
also exposed real compose/hardening gaps, so the tracked implementation was
corrected as well.
`02-auth`, `03-security`, `04-data`, `05-messaging`, `06-observability`, `07-workflow`, `08-ai`, and
`09-tooling` closed current-truth mismatches in implemented service documents,
service-local validation boundaries, runtime version/control literal drift, and
active taxonomy shorthand drift with in-place corrections and repo-contract
guards.

## Verdict Summary (by stage)

| Stage           | Docs | KEEP (matches impl)                    | FIX (status/content)                       | ARCHIVE candidate   | Notes                                                                         |
| --------------- | ---- | -------------------------------------- | ------------------------------------------ | ------------------- | ----------------------------------------------------------------------------- |
| 01.requirements | 25   | 25 active                              | 23 (status: draft->active)                 | 0                   | 23 tier PRDs have tracked implementation surfaces and remain active requirements |
| 02.architecture | 51   | 51                                     | 0                                          | 0                   | All ADR/ARD docs map to current infra (real traefik/keycloak/vault/kafka/patroni/lgtm, etc.) |
| 03.specs        | 43   | 15 active / 9 completed / 19 README-like missing status | 7 process specs (status active->completed) | 0                   | tier spec mapping OK; process specs are completed one-time work |
| 04.execution    | 125  | 120 completed / 3 active / 2 README-like missing status | stale `active` Open WebUI plan/task -> completed; hardening runtime rows deferred | 0 | infra-opt-priority-plan remains active as an ongoing roadmap |
| 05.operations   | 267  | 197 active / 70 README-like missing status | open-notebook draft->active; duplicate policy/guide profiles cleaned; bucket-root leaf documents moved into purpose folders; `05-messaging`/`07-workflow`/`08-ai`/`09-tooling`/`10-communication`/`11-laboratory` current truth corrected | 9 archived | Airbyte guide/policy/runbook, misplaced ksqlDB guide, duplicate Airflow DAG guide, duplicate AI setup/inference guides, duplicate tooling IaC guide, and duplicate Vault setup guide are in `docs/98.archive`; no remaining orphans (`failures=0`) |

## Task Table

### Findings and Disposition

| ID   | Doc(s)                                                                                                                                                                                                                                     | Evidence                                                                                     | Disposition |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | ----------- |
| F-01 | `docs/05.operations/{guides,policies}/11-laboratory/open-notebook.md` | `infra/11-laboratory/open-notebook` implementation exists and content matches | Applied status `draft`->`active` |
| F-02 | `docs/04.execution/plans/2026-03-27-08-ai-open-webui-plan.md`, `.../tasks/2026-03-27-08-ai-open-webui-tasks.md` | Open WebUI implementation surface exists (`infra/08-ai/open-webui`); live RAG indexing requires runtime evidence | Applied plan/task status `active`->`completed`; corrected the task-internal live RAG row to `Deferred` |
| F-03 | `docs/03.specs/{workspace-consistency-2026-05b,workspace-doc-consistency-2026-05,docs-taxonomy-agent-first-migration,harness-agent-first-engineering,llm-wiki-agent-first-completion,home-docker-revalidation-deferred-follow-up}/spec.md` | Described work is reflected in current implementation (R4/R5 rules, CI taxonomy, LLM Wiki generator, docs taxonomy, etc.) | Applied status `active`->`completed`; not archived because it does not conflict with current implementation |
| F-04 | `docs/04.execution/plans/2026-03-27-infra-service-optimization-priority-plan.md` | Quick Wins were implemented, but the 2026 Q2/Q3 quarterly roadmap and operations-standard codification items remain planned work | Kept `active` |
| F-05 | `docs/01.requirements/2026-03-26-*` and related tier PRDs | tracked tier implementation exists under `infra/**`; requirements remain current inputs rather than completed task evidence | Applied status `draft`->`active` |
| F-06 | README and governance documents in changed folders | folder-level content/status changes require README/governance alignment | Updated `docs/01.requirements/README.md`, QA/GitHub/script governance, and progress log |
| F-07 | `docs/05.operations/policies/**/*.md` | Several policy leaves retained duplicate `## Policy Scope` headings that differed from current `policy.template.md` | Removed `## Policy Scope` headings after the first one, preserved bullets, added an exactly-one gate to `check-repo-contracts.sh`, and updated the `policies/README.md` contract |
| F-08 | `docs/05.operations/guides/{05-messaging/kafka,06-observability/{alertmanager,grafana,prometheus},09-tooling/{sonarqube,terraform,terrakube}}.md`, `docs/05.operations/runbooks/09-tooling/terraform.md` | 7 guide leaves retained duplicate `### Usage Type` profile blocks, and the Terraform runbook retained a `<your-profile>` placeholder | Removed duplicate guide profiles, preserved service content, added a duplicate Usage Type gate to the repo contract, and cleaned the Terraform runbook to env-var based credential refresh |
| F-09 | `docs/05.operations/{guides,policies}/09-tooling/{sonarqube,syncthing}.md` | Documents belong to the `09-tooling` path/implementation, but ID comments pointed to old `07-tooling` or `08-tooling` tiers | Corrected ID comments to `09-tooling:<service>`, added an operations ID tier/path match gate to `check-repo-contracts.sh`, and reflected the rule in 09-tooling guide/policy README files |
| F-10 | `docs/02.architecture/requirements/0013-open-webui-architecture.md`, `docs/03.specs/{01-gateway,02-auth,03-security,05-messaging,08-ai}`, selected `docs/04.execution/tasks`, selected `docs/05.operations/{guides,policies,runbooks}` | Current image tags in compose and `infra/tech-stack.versions.json` diverged from runtime version literals retained in document bodies | Corrected Traefik, Keycloak, OAuth2 Proxy, Vault, Kafka, RabbitMQ, Kafbat UI, Open WebUI, Grafana, Airflow, Pushgateway, Pyroscope, Qdrant, and Neo4j document versions to match current implementation; added stale runtime version gate to `check-repo-contracts.sh` |
| F-11 | `docs/03.specs/standardize-infra-net/spec.md`, `docs/05.operations/{guides,runbooks}/12-infra-net/standardize-infra-net.md` | Active docs retained wildcard IPv4 examples that looked copyable despite differing from the authoritative mapping table | Corrected examples to use the registry's actual implementation IP (`172.19.0.7`) and strengthened steps to use authoritative table values for target services; added a stage docs IP placeholder gate to `check-repo-contracts.sh` |
| F-12 | `docs/03.specs/workspace-audit-2026-05/{spec.md,README.md}`, `docs/03.specs/README.md` | The completed 2026-05 audit spec gap table could read ambiguously as either the historical baseline or current implementation state | Marked the section as a historical snapshot and strengthened README/03.specs index wording for the completed historical spec |
| F-13 | `docs/05.operations/guides/00-workspace/{env-key-comparison,sensitive-env-vars-comparison}.md` | Metadata-only comparison document counts diverged from current `.env.example`, `.env`, and `secrets/SENSITIVE_ENV_VARS.md*` state | Corrected `.env.example`/`.env` key counts to 325/325 and sensitive registry line count to 184/184, clarified the no-value-comparison wording as metadata-only, and added a conditional metadata comparison guide drift gate to `check-repo-contracts.sh` |
| F-14 | `docs/02.architecture/{decisions/0015-analytics-engine-selection.md,requirements/0012-data-analytics-architecture.md}`, `docs/03.specs/04-data-analytics/{spec.md,README.md}` | Analytics engine selection/contract docs described InfluxDB primary, OpenSearch, and StarRocks families using old baselines that differed from the current `infra/04-data/analytics` compose version family | Corrected to InfluxDB 3.x Core primary + InfluxDB 2.x legacy compose, Confluent ksqlDB 8.x, OpenSearch 3.x, and StarRocks 4.x; corrected InfluxDB primary health check to `8181`; added stale analytics version-family gate |
| F-15 | `docs/05.operations/{guides/06-observability/prometheus.md,runbooks/11-laboratory/dozzle.md,runbooks/11-laboratory/README.md}`, `infra/11-laboratory/dozzle/README.md` | Prometheus guide and Dozzle runbook/infra README contained implementation values that did not match the current PostgreSQL image family and Dozzle compose tag | Corrected Prometheus scrape target description to PostgreSQL 17/18 family; aligned Dozzle baseline tag to `amir20/dozzle:v10.6.4` and changed rollback wording to record the previous verified tag evidence; added stale Dozzle/PostgreSQL literal gate |
| F-16 | `docs/05.operations/{guides,policies,runbooks}/README.md` and `00-workspace`, `12-infra-net`, `90-knowledge` purpose folders | Bucket roots mixed leaf documents and folder indexes, so Stage 05 operations structure did not match the purpose-based navigation contract | Kept only bucket `README.md` files at root, moved workspace, infra_net, and knowledge documents into purpose folders, refreshed parent/child README files and cross-links, and added operations bucket-root leaf prohibition plus target-path match gates to `check-repo-contracts.sh` |
| F-17 | `infra/04-data/operational/README.md`, `infra/04-data/operational/{mng-db,supabase}/README.md`, `docs/05.operations/{guides,policies,runbooks}/04-data/operational/{mng-db,supabase}.md` | `mng-db` docs retained obsolete network/old Compose CLI guidance and template remnants; Supabase docs assumed direct Studio host-port access and contained incomplete policy/runbook template residue; infra README listed a relational cluster under the operational folder and linked the guide index to policies | Corrected in place to current compose truth: `mng-db` services/profiles/networks/init DBs, Supabase data-profile services/Kong ports/runtime mounts, PostgreSQL image family, and operations guide/policy/runbook links; no archive because documents map to implemented services |
| F-18 | `infra/04-data/cache-and-kv/README.md`, `infra/04-data/cache-and-kv/valkey-cluster/README.md`, `docs/05.operations/{guides,policies,runbooks}/04-data/cache-and-kv/valkey-cluster.md` | Valkey docs referenced stale init/container names, direct password variables, stale image tag, unsupported `maxmemory-policy` control, and destructive restore guidance not proven by current runbook evidence | Corrected in place to current compose truth: six `valkey-node-*` services, `valkey-cluster-init`, `valkey-cluster-exporter`, `service_valkey_password`, `valkey/valkey:9.1.0-alpine`, current port/profile/network model, and non-destructive escalation boundary |
| F-19 | `infra/04-data/lake-and-object/{minio,seaweedfs}/README.md`, `docs/05.operations/{guides,policies,runbooks}/04-data/lake-and-object/{minio,seaweedfs}.md` | MinIO docs mixed root-active single-node compose with optional 4-node cluster recovery; SeaweedFS README contained duplicated old/new structures, an obsolete SeaweedFS version literal, unmounted `security.toml` claims, single-container log command, and unverified destructive restore/reshard procedures | Corrected in place to current compose truth: MinIO root-active `minio` + `minio-create-buckets` with optional cluster variant explicitly scoped; SeaweedFS `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-mount`, image `chrislusf/seaweedfs:4.31`, route/health/mount boundaries, and non-destructive escalation boundary |
| F-20 | `infra/04-data/nosql/{README.md,cassandra/README.md,couchdb/README.md,mongodb/README.md}`, `docs/05.operations/{guides,policies,runbooks}/04-data/nosql/{README.md,cassandra.md,couchdb.md,mongodb.md}` | NoSQL docs retained stale image tags, template/profile residue, old service/control names, unsupported replica-set variable guidance, direct secret-style commands, and destructive restore/resync steps not proven by current runbook evidence | Corrected in place to current compose truth: Cassandra optional single node `cassandra-node1` + `cassandra-exporter` (`cassandra:5.0.8`), CouchDB `couchdb-1..3` + `couchdb-cluster-init` (`couchdb:3.5.2`), MongoDB `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, init/UI/exporter (`mongo:8.2.9-noble`), Docker Secret boundaries, purpose-specific guide/policy/runbook separation, and non-destructive escalation boundary |
| F-21 | `infra/04-data/specialized/{README.md,neo4j/README.md,qdrant/README.md}`, `docs/05.operations/{guides,policies,runbooks}/04-data/specialized/{README.md,neo4j.md,qdrant.md}` | Specialized data docs retained stale image tags, a removed `05.analytical-specialized-dbs.md` link, external Bolt/API-key claims not declared by compose, data mutation guide examples, backup/restore schedules, and destructive recovery steps not proven by current runbook evidence | Corrected in place to current compose truth: root-active Neo4j `neo4j:5.26.26-community` with `neo4j_password` secret-aware entrypoint and HTTP Browser route only; root-active Qdrant `qdrant/qdrant:v1.18.1-unprivileged` with REST/gRPC Traefik routes, current no-secret state, snapshot path, purpose-specific guide/policy/runbook separation, and non-destructive escalation boundary |
| F-22 | `infra/04-data/relational/{README.md,postgresql-cluster/README.md}`, `docs/05.operations/{guides,policies,runbooks}/04-data/relational/{README.md,postgresql-cluster.md}` | Relational docs retained removed old relational index links, stale Spilo entrypoint filename, template/profile residue, unproven backup/archive controls, and destructive DCS/leadership guidance not proven by current runbook evidence | Corrected in place to current compose truth: optional/commented PostgreSQL HA cluster include; etcd `3.6.12`, HAProxy `3.3.10`, Spilo `spilo-17:4.0-p3`, init job `postgres:18-alpine`, exporters `v0.19.1`, Docker Secret boundaries, `pg-router` write/read endpoints, `pg-cluster-init` scope, and non-destructive escalation boundary |
| F-23 | `infra/06-observability/{README.md,docker-compose.yml,docker-compose.dev.yml,*/README.md}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**06-observability**` | Observability docs retained stale Mimir/version-family wording, generic README counts, service-local compose validation claims, stale Pushgateway/Pyroscope endpoints, and `docker-compose.dev.yml` referenced Pyroscope via Alloy/Grafana without declaring the service; cAdvisor labels used Pyroscope router/service names | Corrected in place to current compose truth: Prometheus `v3.12.0`, Loki `3.6.6-custom`, Tempo `2.10.1-custom`, Alloy `1.16.2`, Grafana `13.0.2`, cAdvisor `0.55.1`, Pyroscope `2.0.2`, Alertmanager `0.32.1`, Pushgateway `1.11.3`; restored Pyroscope in root-included dev compose; separated cAdvisor/Pyroscope Traefik labels; documented root/overlay compose validation boundary and current retention/storage facts |
| F-24 | `infra/05-messaging/{README.md,kafka/README.md,rabbitmq/README.md}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**05-messaging**`, `docs/05.operations/guides/05-messaging/ksql-streaming.md` | Messaging docs retained ksqlDB as a 05-messaging-owned service, old Kafka/RabbitMQ version literals, nonexistent `ksql/` structure, service-local compose validation claims without root context, stale `schema-registry.localhost`, wrong RabbitMQ AMQP route guidance, destructive queue purge guidance, and Guide/Policy/Runbook links that all pointed at policy docs | Archived misplaced `ksql-streaming.md` as a central tombstone; redirected active ksqlDB references to `04-data/analytics/ksql`; corrected Kafka/RabbitMQ docs to current images, profiles, root dev vs service-local full compose boundary, Docker Secrets, Traefik route/AMQP separation, and non-destructive runbook escalation; removed the stale active validator exception so a future 05-messaging `ksql-streaming` guide maps to missing implementation and fails alignment |
| F-25 | `infra/07-workflow/{README.md,airflow/README.md,n8n/README.md}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**07-workflow**`, `docs/05.operations/guides/07-workflow/01.airflow-dag-dev.md` | Workflow docs retained Airflow 2 webserver-era service names, repo-local DAG path guidance, direct service-local compose validation claims that fail without root `infra_net`, incorrect n8n project ownership wording, duplicate policy/runbook profile residue, and links that pointed Guide/Runbook labels at policy docs | Archived duplicate `01.airflow-dag-dev.md` as a central tombstone; corrected active Airflow/n8n docs to current service names, Airflow 3.2.2, n8n runner 2.23.2, root-included dev `mng-valkey` vs service-local `airflow-valkey`/`n8n-valkey` boundary, root validator commands, template-compliant guide/policy/runbook purpose separation, and stale-literal repo-contract guards |
| F-26 | `infra/08-ai/{README.md,ollama/README.md,open-webui/README.md}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**08-ai**`, `docs/05.operations/guides/08-ai/{01.llm-inference.md,local-llm-setup.md}` | AI docs retained stale Ollama/Open WebUI image guidance, duplicate Ollama setup/inference guides with generic template residue, service-local compose validation claims that fail without root `infra_net`, host-local Open WebUI/exporter health checks despite internal-only exposure, a typoed Open WebUI port env var, and Guide/Runbook labels that pointed at policy docs | Archived duplicate setup/inference guides as central tombstones; corrected active Ollama/Open WebUI/RAG docs to current compose image tags, root optional include boundary, `.env.example` exporter port vs compose fallback, container-internal health checks, current embedding model tag, template-compliant guide/policy/runbook separation, and stale-literal repo-contract guards |
| F-27 | `infra/09-tooling/{README.md,*/README.md}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**09-tooling**`, duplicate tooling IaC guide | Tooling docs retained stale service image/version guidance, optional compose leaves described as direct standalone config targets, unavailable performance-tool worker/route claims, registry storage/backend mismatch, Terraform/Terrakube service-context drift, and a duplicate IaC guide with generic template residue | Archived duplicate IaC guide as a central tombstone; corrected active tooling docs to current compose truth: root optional include boundary, SonarQube/Syncthing/Terraform/Terrakube current images, registry bind mount storage, `k6-master` Locust-wrapper service, Locust host-port UI boundary, root-context runtime commands, template-compliant guide/policy/runbook separation, and stale-literal repo-contract guards |
| F-28 | `infra/10-communication/{README.md,mail/{README.md,docker-compose.yml}}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**10-communication**`, `docs/03.specs/standardize-infra-net/spec.md`, hardening/repo-contract scripts | Communication docs retained standalone compose validation claims, an invalid old high-range `infra_net` allocation, a MailHog host-port claim, unproven encrypted-volume/automatic deliverability assertions, direct Keycloak/OIDC wording, incomplete historical task status, and stale legacy Compose operational commands; compose also used invalid IPv4 addresses and left Stalwart UI without the SSO middleware chain required by policy | Corrected implementation and docs in place: Stalwart/MailHog static IPs now use `172.19.0.228-229`, Stalwart and MailHog UI routes use the SSO middleware chain, `10-communication` is covered by `check-all-hardening.sh`, PRD/ARD/spec/ADR/plan/task and operations guide/policy/runbook now reflect root optional include plus promotion-readiness evidence, and repo-contract stale guards block the old IPs, MailHog host-port claim, legacy compose command, and standalone config proof |
| F-29 | `infra/11-laboratory/{README.md,*/README.md,open-notebook/docker-compose.yml,redisinsight/docker-compose.yml}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**11-laboratory**`, `docs/03.specs/standardize-infra-net/spec.md`, hardening/repo-contract scripts | Laboratory docs retained root-active/optional service confusion, omitted root-active Open Notebook/SurrealDB from hardening scope, service-local compose validation claims that fail without root `infra_net`, stale RedisInsight tag guidance, stale Homer host-port and container-log names, weak SSO-only snippets, underscore volume names, and destructive/unverified runbook actions such as generic down/restart/reset guidance; implementation left Open Notebook UI without the required SSO/allowlist chain and left RedisInsight static route unprotected | Corrected implementation and docs in place: Open Notebook route now uses gateway+allowlist+large-body+SSO and has a healthcheck; RedisInsight static route now uses the protected chain; `11-laboratory` hardening checks dashboard/dozzle/open-notebook/portainer/redisinsight, static IPs, images, healthchecks, secret-file boundaries, and socket permissions; docs now distinguish root-active Dozzle/RedisInsight/Open Notebook/SurrealDB from optional Homer/Portainer, update infra_net mapping for `172.19.0.122-123`, replace service-local config proof with root `admin` profile validation, rewrite service runbooks as non-destructive evidence/escalation procedures, and add repo-contract stale guards |
| F-30 | `infra/01-gateway/{README.md,traefik/**,nginx/**}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**01-gateway**`, hardening/repo-contract scripts | Gateway docs retained root-active/profile-only confusion, old Traefik version guidance, stale gateway-owned TCP/dashboard port claims, tier-local compose start/config proof, runtime lint commands without an approved context, and a rate-limit value mismatch between hardening policy and implementation | Corrected implementation and docs in place: Traefik remains root-active on `web`, `websecure`, and `metrics`; Nginx is documented as profile-only and not root-included by default; service-local standalone compose proof was replaced with root `core` profile validation, hardening checks, and runtime-only approved-context commands; `req-rate-limit` now matches the 100/50 policy and hardening script enforces it; repo-contract guards block the stale gateway version, entrypoint, command, and rate-limit literals |
| F-31 | `infra/02-auth/{README.md,keycloak/**,oauth2-proxy/**}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**02-auth**`, hardening/repo-contract scripts | Auth docs retained older Keycloak/OAuth2 Proxy version guidance, a lower Keycloak template baseline than the current compose, root-active dev leaf vs local/full OAuth2 Proxy leaf confusion, leaf-local compose validation claims that fail without root `infra_net`, and direct container log/exec runtime checks | Corrected implementation and docs in place: Keycloak is documented against the current high template and image; OAuth2 Proxy docs distinguish root-active dev leaf using `mng-valkey` from local/full leaf using dedicated Valkey/exporter services; validation now routes through root `auth`/`core` profile scripts plus `check-all-hardening.sh 02-auth`; hardening checks cover Keycloak, both OAuth2 Proxy compose leaves, Dockerfiles, entrypoints, cookie/secret config, IPs, images, middleware, and healthchecks; repo-contract guards block stale auth literals and leaf-local validation/runtime command drift |
| F-32 | `infra/03-security/{README.md,vault/**}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**03-security**`, `docs/05.operations/guides/03-security/01.setup.md`, hardening/repo-contract scripts | Security docs retained older Vault version guidance, single-node Vault described as current HA, service-local compose validation/startup proof, direct container log/exec runtime checks, duplicate setup guide residue, and policy/runbook links pointing back to the guide | Archived duplicate setup guide as a central tombstone; corrected active Vault docs to current image, single-node Raft + planned HA boundary, root `security`/`core` profile validation, runtime-only root compose commands, correct guide/policy/runbook links, mlock config comment, and strengthened hardening/repo-contract checks for Vault image, networks/IPs, Agent templates, output volume, healthchecks, and stale command reintroduction |
| F-33 | Active Stage 01-05 optimization-hardening PRD/ARD/ADR/spec/plan leaves for `04-data`, `05-messaging`, `06-observability`, `07-workflow`, `08-ai`, and `09-tooling` | Several active documents still described the old nine-stage documentation chain even though the current taxonomy is Stage 01-05 plus Stage 90/98/99 support areas | Rewrote those references in place to the current Stage 01-05 PRD/ARD/ADR/Spec/Plan/Task and Guide/Policy/Runbook chain; strengthened `check-repo-contracts.sh` so old bare shorthand cannot re-enter active docs |

## Archive Decision

Completed one-time **process specs/plans** (F-03/F-04: workspace-audit,
docs-taxonomy-migration, harness-agent-first, llm-wiki-completion, and similar
items) match the current implementation exactly and do **not** conflict with it.
Therefore the archive criterion is not whether a document is "historical", but
whether it **conflicts with the current implementation**.

Whole-document residue that conflicted with implementation is tombstoned in the
`docs/98.archive/README.md` ledger, including Airbyte, misplaced ksqlDB,
duplicate Airflow/AI/tooling/Vault guides, and the old conflicting Codex/HADS
chain. Stage 05 bucket-root structure drift (F-16) did not conflict with current
implementation content; only the location/navigation contract was stale, so it
was handled by in-place moves and reference refresh rather than archive.

`04-data/operational` drift (F-17) was a current-truth mismatch in implemented
`mng-db` and `supabase` service documents, so it was handled by
template-compliant in-place rewrites and README reference refresh rather than
archive. `04-data/cache-and-kv` drift (F-18) was also a service-name,
command, and control mismatch in implemented Valkey cluster documents, so it was
handled the same way.

`04-data/lake-and-object` drift (F-19) was active-vs-optional compose confusion
and stale runtime/control guidance in implemented MinIO and SeaweedFS documents,
so it was handled by template-compliant in-place rewrites and README reference
refresh rather than archive. `04-data/nosql` drift (F-20) was service-name,
image, and control mismatch plus unverified destructive recovery guidance in
implemented Cassandra, CouchDB, and MongoDB documents, so it was handled by
template-compliant in-place rewrites and README reference refresh.

`04-data/specialized` drift (F-21) was mismatch in active compose truth, route,
secret/no-secret control, stale links, and unverified destructive recovery
guidance in implemented Neo4j and Qdrant documents, so it was handled by
template-compliant in-place rewrites and README reference refresh rather than
archive. `04-data/relational` drift (F-22) was mismatch in optional compose
truth, stale links, secret-aware entrypoint filename, and unverified
backup/DR/destructive recovery guidance in implemented PostgreSQL HA cluster
documents, so it was handled by template-compliant in-place rewrites and README
reference refresh.

`06-observability` drift (F-23) was route/service/version/storage mismatch
between implemented observability compose and documentation, and some compose
label/service declarations were clear current-truth defects. It was handled by
in-place compose correction, template-aligned documentation correction, and
README reference refresh instead of archive.

`05-messaging` drift (F-24) mixed current-truth mismatch in implemented
Kafka/RabbitMQ documents with a misplaced ksqlDB guide. Kafka/RabbitMQ documents
map to implemented services, so they were handled by in-place correction.
`docs/05.operations/guides/05-messaging/ksql-streaming.md` does not correspond
to current `infra/05-messaging` implementation and conflicts with the
`04-data/analytics/ksql` document, so it moved to a `docs/98.archive` tombstone.

`07-workflow` drift (F-25) mixed current-truth mismatch in implemented
Airflow/n8n documents with a duplicate Airflow DAG guide. Airflow/n8n documents
map to implemented services, so they were handled by in-place correction.
`docs/05.operations/guides/07-workflow/01.airflow-dag-dev.md` conflicts with the
current `${DEFAULT_WORKFLOW_DIR}/airflow/dags` bind-mount baseline and
duplicates `airflow-dag-basics.md`, so it moved to a `docs/98.archive`
tombstone.

`08-ai` drift (F-26) mixed current-truth mismatch in implemented Ollama/Open
WebUI documents with duplicate Ollama setup/inference guides. Ollama/Open
WebUI/RAG/hardening documents map to implemented services, so they were handled
by in-place correction. The duplicate setup/inference guides duplicate active
`ollama.md` and have incomplete runbook handoff, so they moved to
`docs/98.archive` tombstones.

`09-tooling` drift (F-27) mixed current-truth mismatch in implemented tooling
service documents with a duplicate IaC automation guide. Terraform/Terrakube/
Registry/SonarQube/Syncthing/Locust/k6 documents map to implemented services,
so they were handled by in-place correction. The duplicate tooling IaC guide
duplicates active `terraform.md`/`terrakube.md` and has incomplete runbook
handoff, so it moved to a `docs/98.archive` tombstone.

`10-communication` drift (F-28) mixed current-truth mismatch in implemented mail
service documents with compose hardening gaps. Stalwart/MailHog documents map to
implemented services, so they were handled by in-place correction rather than
archive. The invalid IPv4 static allocation and Stalwart UI SSO middleware gap
were corrected in tracked compose and hardening scripts so current
implementation matches the documentation criteria.

`11-laboratory` drift (F-29) mixed current-truth mismatch in implemented
laboratory service documents with root-active service hardening gaps.
Dashboard/Dozzle/Open Notebook/Portainer/RedisInsight documents map to
implemented services, so they were handled by in-place correction rather than
archive. The Open Notebook route and RedisInsight static route middleware gaps
were corrected in tracked compose and hardening scripts so current
implementation matches the documentation criteria.

`01-gateway` drift (F-30) mixed current-truth mismatch in implemented
Traefik/Nginx gateway documents with a rate-limit hardening gap. Traefik/Nginx
documents map to implemented services, so they were handled by in-place
correction rather than archive. The gateway rate-limit mismatch was corrected in
tracked dynamic config and hardening scripts so current implementation matches
the policy criteria.

`02-auth` drift (F-31) mixed current-truth mismatch in implemented
Keycloak/OAuth2 Proxy documents with root-active/local-full validation-boundary
gaps. Keycloak/OAuth2 Proxy documents map to implemented services, so they were
handled by in-place correction rather than archive. Both the OAuth2 Proxy
root-active dev leaf and local/full leaf were included in hardening and
repo-contract guards so current implementation matches the QA criteria.

`03-security` drift (F-32) mixed current-truth mismatch in implemented
Vault/Vault Agent documents with a duplicate setup guide. Vault/Vault Agent
documents map to implemented services, so they were handled by in-place
correction. `docs/05.operations/guides/03-security/01.setup.md` duplicates
active `vault.md` and conflicts with the root compose validation boundary, so it
moved to a `docs/98.archive` tombstone.

Stage taxonomy drift (F-33) did not mean whole document content conflicted with
implementation; only active-chain wording remained on the old taxonomy. It was
handled by in-place correction and repo-contract guard strengthening without
archive.

## Verification Summary

- Stage 01-05 inventory: `docs/01.requirements=25`, `docs/02.architecture=51`, `docs/03.specs=43`, `docs/04.execution=125`, `docs/05.operations=267`, total `511`.
- operations service coverage: `check-doc-implementation-alignment.sh` -> `operations_service_docs_checked=143`, `failures=0`.
- operations bucket-root scan: only each bucket `README.md` remains at the root of `docs/05.operations/{guides,policies,runbooks}`.
- stale operations root-path scan: 0 old bucket-root leaf forms (`guides/<leaf>.md`, `runbooks/<leaf>.md`, `policies/<leaf>.md`).
- legacy/orphan scan: no new unimplemented-service documents; Patroni/Spilo/HADS are classified as current implementation or historical evidence.
- policy profile scan: 0 duplicate `## Policy Scope` headings in `docs/05.operations/policies/**/*.md` leaves; repo contract enforces exactly one heading per policy leaf.
- guide profile scan: 0 duplicate `### Usage Type` blocks; remaining TODO/TBD/placeholder-like hits are classified as historical evidence or scan command literals.
- operations ID tier scan: 0 mismatches between ID comments and path tiers under `docs/05.operations/{guides,policies,runbooks}`; repo contract blocks mismatches.
- runtime version drift scan: 0 stale runtime version literals; repo contract blocks reintroduction of document versions that diverge from current compose/tech-stack registry.
- IP placeholder scan: 0 wildcard infra/k3d IPv4 placeholders; repo contract blocks concrete-network placeholder reintroduction.
- Stage taxonomy shorthand scan: 0 old nine-stage shorthand hits in active Stage 01-05 docs; repo contract blocks bare shorthand and path-style shorthand reintroduction.
- metadata comparison scan: `.env.example`/`.env` key count 325/325, sensitive registry line count 184/184, secret ID count 107; repo contract blocks metadata-only number drift when local files exist.
- analytics/laboratory version-family scan: analytics primary/decision stale phrases, Dozzle old tag, and PostgreSQL old scrape family phrase 0 hits; repo contract blocks exact stale literal reintroduction.
- 04-data operational scan: 0 old Compose CLI command spelling, direct Studio host-port literal, template copyright residue, and obsolete shared-network literal hits in `mng-db`/`supabase` guide, policy, and runbook documents.
- 04-data operational implementation mapping: `mng-db` docs now match compose services `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-exporter`; Supabase docs now match data-profile services `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `imgproxy`, `meta`, `functions`, `analytics`, `db`, `vector`, `supavisor`.
- 04-data cache-and-kv scan: 0 stale init/container names, stale image tag, direct password variable command, unsupported maxmemory policy, and single-container command assumptions in Valkey guide, policy, runbook, and infra README.
- 04-data cache-and-kv implementation mapping: Valkey docs now match compose services `valkey-node-0` through `valkey-node-5`, `valkey-cluster-init`, `valkey-cluster-exporter`, profiles `data`/`service`, network `infra_net`, and secret `service_valkey_password`.
- 04-data lake-and-object scan: 0 stale SeaweedFS version, single-container SeaweedFS log target, unverified reshard command, direct MinIO root credential env references, and root-active/optional cluster confusion in MinIO/SeaweedFS guide, policy, runbook, and infra README outside the explicitly optional MinIO cluster compose file.
- 04-data lake-and-object implementation mapping: MinIO docs now match root-active `minio` + `minio-create-buckets` and optional `docker-compose.cluster.yaml`; SeaweedFS docs now match services `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-mount`, image `chrislusf/seaweedfs:4.31`, network `infra_net`, and mount privilege boundary.
- 04-data nosql scan: 0 stale image tags, old service names, old secret-control names, unsupported replica-set variable guidance, direct password examples, and destructive restore/resync commands in Cassandra/CouchDB/MongoDB guide, policy, runbook, and infra README.
- 04-data nosql implementation mapping: Cassandra docs now match optional `cassandra-node1` + `cassandra-exporter`, image `cassandra:5.0.8`, profiles `data`/`obs`, secret `cassandra_password`; CouchDB docs now match `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`, image `couchdb:3.5.2`, secrets `couchdb_password`/`couchdb_cookie`; MongoDB docs now match `mongo-key-generator`, `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter`, image `mongo:8.2.9-noble`, replica set `MyReplicaSet`, and non-destructive escalation boundary.
- 04-data specialized scan: 0 stale image tags, removed guide link, unsupported external Bolt/API-key claims, mutation guide examples, backup/restore schedules, and destructive recovery commands in Neo4j/Qdrant guide, policy, runbook, and infra README.
- 04-data specialized implementation mapping: Neo4j docs now match root-active `neo4j`, image `neo4j:5.26.26-community`, profiles `data`/`graph`, secret `neo4j_password`, secret-aware entrypoint, healthcheck, and HTTP Browser route; Qdrant docs now match root-active `qdrant`, image `qdrant/qdrant:v1.18.1-unprivileged`, profiles `ai`/`data`/`dev`, no-secret state, REST/gRPC Traefik routes, `/readyz` healthcheck, and non-destructive escalation boundary.
- 04-data relational scan: 0 removed old relational index links, stale entrypoint filename, unproven backup/archive controls, manual leadership-mutation instructions, destructive DCS reset command, and old template residue in PostgreSQL cluster guide, policy, runbook, and infra README.
- 04-data relational implementation mapping: PostgreSQL cluster docs now match optional/commented root include services `etcd-1..3`, `pg-router`, `pg-cluster-init`, `pg-0..2`, `pg-0-exporter..pg-2-exporter`, image families/tags etcd `3.6.12`, HAProxy `3.3.10`, Spilo `spilo-17:4.0-p3`, init job `postgres:18-alpine`, postgres exporter `v0.19.1`, Docker Secret boundaries, `pg-router` write/read endpoints, and non-destructive escalation boundary.
- 06-observability stale scan: 0 old Prometheus/Grafana/Alloy/Pyroscope/Alertmanager/Pushgateway version literals, old Mimir wording, `pushgateway.local`, stale Pyroscope `/health`, and generated `plus N more` README evidence hits in active observability scope.
- 06-observability implementation mapping: root-included `docker-compose.dev.yml` and local `docker-compose.yml` now both render `prometheus`, `loki`, `tempo`, `alloy`, `grafana`, `cadvisor`, `pyroscope`, `alertmanager`, and `pushgateway`; cAdvisor uses `cadvisor` Traefik labels and `${CADVISOR_PORT:-8080}`, Pyroscope uses `pyroscope` Traefik labels and `${PYROSCOPE_PORT:-4040}`.
- 06-observability validation boundary: root profile validation passes with `HYHOME_COMPOSE_PROFILES=obs`; service-local compose validation requires root network/secret context or an explicit temporary validation overlay.
- 05-messaging implementation mapping: root messaging profile renders `kafka-1`, `schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`, `kafka-exporter`, `kafka-init`, and `rabbitmq`; `HYHOME_COMPOSE_PROFILES=messaging` validation passes with `services_total=8`, while `HYHOME_COMPOSE_PROFILES='messaging dev'` validation passes with `services_total=46`.
- 05-messaging service-local boundary: direct service-local `--profile messaging config --services` for Kafka full, Kafka dev, and RabbitMQ compose fails without root `infra_net` context (`undefined network infra_net`), so active docs now route normal validation through root profile scripts or explicit overlay context.
- 05-messaging stale scan: outside this audit evidence, archive tombstones, generated indexes, and the current `04-data/analytics` ksqlDB owner docs, active messaging docs no longer retain the old ksql streaming guide path, old Kafka/RabbitMQ version literals, stale Schema Registry host example, destructive queue purge command, or unrelated MinIO CLI definition export command.
- 07-workflow implementation mapping: root workflow profile renders `airflow-init`, `airflow-apiserver`, `airflow-dag-processor`, `airflow-scheduler`, `airflow-statsd-exporter`, `airflow-triggerer`, `flower`, `airflow-worker`, `n8n`, `n8n-worker`, `n8n-task-runner`, and `n8n-task-runner-worker`; `HYHOME_COMPOSE_PROFILES=workflow` validation passes with `services_total=12`, while `HYHOME_COMPOSE_PROFILES='workflow dev'` validation passes with `services_total=45`.
- 07-workflow service-local boundary: direct service-local `--profile workflow config --services` for Airflow and n8n compose fails without root `infra_net` context (`undefined network infra_net`), so active docs now route normal validation through root profile scripts or explicit overlay context.
- 07-workflow stale scan: active workflow docs no longer retain old Airflow webserver service names, incorrect n8n project ownership wording, or repo-local DAG placement guidance; repo contract blocks those exact stale literals in Stage 01-05 docs.
- 08-ai implementation mapping: current tracked AI implementation is optional/commented at root for `ollama`, `ollama-exporter`, and `open-webui`; Qdrant remains root-included under `04-data/specialized` with `ai`/`data`/`dev` profiles.
- 08-ai validation boundary: AI hardening baseline passes, and root-active `core ai` profile validation passes with `services_total=6`; service-local AI compose files fail as standalone checks without root `infra_net` context, so active docs route static validation through the hardening script and root profile validator.
- 08-ai stale scan: active AI docs no longer retain old Ollama/Open WebUI image guidance, typoed Open WebUI port env variable, duplicate setup/inference guide links, host-local Open WebUI/exporter health assumptions, or Guide/Runbook labels that point at policy docs; repo contract blocks exact stale literals and direct service-local AI compose validation commands in Stage 01-05 docs.
- 10-communication implementation mapping: optional/commented root mail include now defines valid `infra_net` static IPs `172.19.0.228` for Stalwart and `172.19.0.229` for MailHog; both Stalwart and MailHog UI routes use `gateway-standard-chain@file,sso-errors@file,sso-auth@file`; hardening supports `10-communication` explicitly.
- 10-communication stale scan: active 01-05/infra communication docs no longer retain the invalid old high-range allocation, MailHog host-port claim, service-local standalone config proof, legacy Compose communication-profile command, unproven encrypted-volume/automatic deliverability assertions, or direct Keycloak/OIDC management wording.
- 11-laboratory implementation mapping: root `admin` profile renders active services `dozzle`, `redisinsight`, `surrealdb`, and `open_notebook`; optional/commented root includes remain `homer` and `portainer`; hardening now checks all five laboratory service leaves plus Open Notebook/SurrealDB secret and health boundaries.
- 11-laboratory stale scan: active 01-05/infra laboratory docs no longer retain service-local standalone config proof, old RedisInsight tag guidance, nonexistent Homer host-port/log-target wording, underscore Portainer/RedisInsight volume naming, weak SSO-only middleware snippets, or destructive generic service recovery instructions in 11-laboratory runbooks.
- 01-gateway implementation mapping: root `core` profile renders active `traefik`; `nginx` remains a profile-only leaf that is not root-included by default and needs explicit root network/backend context for runtime use; Traefik static entrypoints are `web`, `websecure`, and `metrics`.
- 01-gateway stale scan: active 01-05/infra gateway docs no longer retain old Traefik version guidance, stale gateway-owned TCP/dashboard port claims, tier-local compose start/config proof, standalone Nginx config proof, or runtime lint commands outside an approved context. Repo contract now blocks exact stale gateway literals across Stage 01-05 and `infra/01-gateway`.
- 02-auth implementation mapping: root `auth` profile renders `keycloak` and root-active `oauth2-proxy`; root `core` profile renders the auth pair plus core dependencies; local/full OAuth2 Proxy compose remains distinct with dedicated Valkey/exporter services.
- 02-auth validation boundary: `bash scripts/hardening/check-all-hardening.sh 02-auth`, `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`, and `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh` pass; leaf-local auth compose validation requires root network/secret context and is no longer active documentation proof.
- 02-auth stale scan: active 01-05/infra auth docs no longer retain old runtime version guidance, lower Keycloak template guidance, leaf-local compose proof, or direct container log/exec checks. Repo contract now blocks exact stale auth literals across Stage 01-05 auth docs and `infra/02-auth`.
- 03-security implementation mapping: root `security` profile renders `vault` and `vault-agent`; root `core` profile renders the security pair plus core dependencies; Vault uses single-node Raft, `vault-agent` uses AppRole files and renders configured templates to `/vault/out`.
- 03-security validation boundary: `bash scripts/hardening/check-all-hardening.sh 03-security`, `HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh`, and `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh` pass; leaf-local Vault compose validation requires root network context and is no longer active documentation proof.
- 03-security stale scan: active 01-05/infra security docs no longer retain old Vault version guidance, duplicate setup guide references, service-local compose proof, direct container log/exec checks, or current-HA wording. Repo contract now blocks exact stale security literals across Stage 01-05 security/Vault docs and `infra/03-security`.
- reference.template.md archive mention: 0 hits (constraint already satisfied).
- Local QA gate: `bash scripts/validation/run-local-qa-gates.sh` -> PASS, repo contracts `failures=0`, generated LLM Wiki fresh.

## Related Documents

- **Archive index/ledger**: [98.archive README](../../98.archive/README.md)
- **Alignment check**: [check-doc-implementation-alignment.sh](../../../scripts/validation/check-doc-implementation-alignment.sh)
- **Documentation protocol**: [documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Progress Log**: [progress.md](../../00.agent-governance/memory/progress.md)
