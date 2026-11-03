---
title: "Role, Resource and Retirement Input Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0048"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-03"
---

# Role, Resource and Retirement Input Task

## Overview

### Objective

Implement the approved local P09 source and synthetic-checking work. Record
the fifteen requested role comparisons, preserve valid default and optional
composition, bind common-control and resource evidence to canonical public
inputs, reuse accepted storage placement, and reject unsafe retirement inputs.
This is not the historical SPEC-0204 P09 Wiki-preparation Task.

## Inputs and Authorization

The direct P09 plan authorizes public-source documentation, implementation,
synthetic fixtures and local checks. It excludes service recreation, host
configuration, storage movement, actual deletion, Secret access, external
repositories and remote integration. Host metadata and a short usage sample
are read-only observations only; they do not establish a new resource limit,
capacity, RPO/RTO, peak load, energy budget, recovery or operational PASS.

The observed clean starting HEAD was
`d2ff343d51809f9472e9e12a4d717956947a8d5b`. The supplied dependencies package
was unavailable, so a complete historical crosscheck is not claimed. Historical
SPEC-0204 P09 remains the Wiki-preparation record. SPEC-0218 common controls
and the SPEC-0246 C1–C6 acceptance, now summarized in the POL-0102
Traceability, remain authoritative at their recorded actor, environment and
criterion scope.

### Read-only host observation

At `2026-11-03T08:06:58+09:00`, a read-only Docker query reported Docker Root
Dir `/home/hyunyoun/storage/docker-root/docker` and one instantaneous selected
container sample: Prometheus 3.31% CPU, 445.4 MiB/2 GiB and 10 PIDs; Tempo
1.65%, 227.1 MiB/2 GiB and 11 PIDs; Loki 5.57%, 232.3 MiB/2 GiB and 12 PIDs;
Alloy 0.79%, 173.4 MiB/512 MiB and 11 PIDs; Pyroscope 0 B/0 B and 0 PIDs.
No raw log was retained. This is neither a complete host census nor evidence
of declared limit correctness, health, use, peak demand, storage placement,
RPO/RTO, energy cost or a runtime acceptance result.

## Work Log

### Single-writer leases

| Scope | Single writer | Independent review | Boundary |
| --- | --- | --- | --- |
| Current Task, SPEC/Plan, DATA-0096 and P09 policy clarifications | `/root/p09_docs` | independent document reviewer | This Task and explicitly listed public documentation only |
| Compose control and exception provenance | `/root/p09_controls` | independent IaC/security reviewer | `scripts/validation/compose_controls.py` and direct tests |
| Retirement input parser | `/root/p09_retire` | independent code/security reviewer | `scripts/lib/ops/retire_materials.py` and direct tests |
| Resource assessment binding | `/root/p09_resource` | independent code/IaC reviewer | `scripts/lib/ops/root_resource_assessment.py` and direct tests |
| QA and CI registration | named QA/CI writer | independent reviewer | No selector or protection weakening |

The public-document baseline fingerprints were SPEC
`88b17555311e04dbddc210ddeb473ad1a621c56223d1e6d155185dd52ee73d7b`, Plan
`00f2f65d77c36c0c3b7e8b91a1cd3863ceaf78d6169ea45cd4f0e154741266d4`, DATA
README `e7a80b0e7c922b28a76c2d8e4a8a0278e175c8865226a0589741a60d81061517` and
DATA payload `7638992aef2681af307ef36cf5db2276cdcf0d85fce2896d34bf2a65df2f663f`.
They identify source only and do not prove runtime state.

### Fifteen role dispositions

`DATA-0096` service and connection rows are the public declaration evidence;
the table does not upgrade a declaration, fixture, profile or historical record
into an operating consumer. An `UNKNOWN` owner, usage, cost or recovery row is
not a retirement candidate.

| Comparison | Current public source / named consumer | Disposition | Data owner / current use | Boundary and resume condition |
| --- | --- | --- | --- | --- |
| PostgreSQL cluster / DEV PostgreSQL | `infra/04-data/mng-db`, `infra/04-data/dev-db`; P04 Opsflow path | RETAIN_SEPARATE | actual owner/use UNKNOWN | P04/P02 retain management-versus-DEV contract; name owner and recovery target before a move |
| Valkey cluster / single | MNG Valkey and P02 named-ACL/dedicated-broker contract | RETAIN_SEPARATE | actual topology use UNKNOWN | P02/P06 own listener and credentials; no inferred cluster retirement |
| InfluxDB / business time-series | no corroborated current public consumer in this Task | UNKNOWN | UNKNOWN | require exact source, consumer and retention/recovery contract |
| Prometheus/Grafana variants | `infra/06-observability`; Grafana datasource declarations | RETAIN | runtime use UNKNOWN | P07 owns expected-target and backend evidence; no second monitoring source is created |
| Traefik / Nginx | `infra/01-gateway/traefik`, `infra/01-gateway/nginx` | RETAIN_SEPARATE | routed UI / named Nginx consumer UNKNOWN | Traefik remains default ingress; Nginx stays documented optional mode |
| k6 / Locust | `infra/11-quality/k6`; Locust current source/consumer UNKNOWN | RETAIN_K6_DEFER_LOCUST | UNKNOWN | do not create or remove a load tool without a named workload and budget |
| Schema Registry | Kafka source and Kafbat schema-registry declaration | RETAIN_OPTIONAL | historical CDC consumer scope only | P04 keeps current `platform_dev` evidence; Opsflow adoption needs an actual consumer |
| Airflow / n8n | `infra/07-workflow/airflow`, `infra/07-workflow/n8n` | RETAIN_SEPARATE | P04 batch/backfill; P05 event/notification source scope | distinct execution models; current operation remains NOT_RUN |
| Spark / Flink / Trino | `infra/12-analytics/{spark,flink,trino}` | DEFER_OPTIONAL | workload owner UNKNOWN | no always-on analytics service or new workload from declaration alone |
| Supabase / direct app | Supabase is LAB; direct app consumer UNKNOWN | RETAIN_LAB_DEFER_APP | UNKNOWN | LAB runtime and external project work stay excluded |
| Loki / OpenSearch / Dozzle | `infra/06-observability/dozzle`, storage/search source | RETAIN_SEPARATE | Grafana/Loki declaration; others UNKNOWN | logs, search and live UI are not interchangeable; no removal inference |
| Open WebUI / Open Notebook | `infra/08-ai/open-webui`, `infra/08-ai/open-notebook` | RETAIN_SEPARATE | actual model consumer UNKNOWN | P03 owns model registration; neither liveness nor route proves feature use |
| OpenTofu / Terrakube | `infra/09-platform-ops/{opentofu,terrakube}` | RETAIN_SEPARATE | operator use UNKNOWN | client tooling and optional server have distinct recovery/authority boundaries |
| Mailpit / Stalwart | `infra/11-quality/mailpit`, `infra/10-communication/stalwart` | RETAIN_SEPARATE | P05 isolated capture; actual Stalwart sender UNKNOWN | capture is not final delivery; P06 owns credentials and Secret lifecycle |
| NoSQL / graph stores | Neo4j, OpenSearch, SurrealDB/Qdrant declaration surfaces | DEFER_OPTIONAL | consumer/data owner UNKNOWN | no candidate removal until consumer, backup reader and recovery evidence are explicit |

### Historical/source reconciliation

Historical ADR bodies are preserved. ADR-0005 names RabbitMQ, ADR-0006 names
MinIO and ADR-0010 names MailHog, while current public sources use the relevant
Kafka/SeaweedFS/Mailpit paths. That is a documented source-versus-history
distinction, not evidence that packages, images, backups or external consumers
are absent.

SPEC-0246 C1–C6 is `REUSE_ACCEPTED`: the owner acceptance summarized in the
POL-0102 Traceability places
Prometheus and Tempo on SSD while Loki, Alloy, Pyroscope, containerd, Docker
and BuildKit remain on HDD. P09 does not re-run any migration, change C6 to
pending, or interpret an observational read-only mount as a host fault.

### Official applicability

The 2026-11-03 P09 research reread the official Docker documentation for
[Compose profiles](https://docs.docker.com/compose/how-tos/profiles/),
[resource constraints](https://docs.docker.com/engine/containers/resource_constraints/)
and [bind mounts](https://docs.docker.com/engine/storage/bind-mounts/), plus
[Restic restore](https://restic.readthedocs.io/en/stable/050_restore.html) and
[Debezium PostgreSQL](https://debezium.io/documentation/reference/stable/connectors/postgresql.html).
They support source-level selection, bounded-resource and recovery planning;
they do not prove this host's live use or authorize mutation. The dependencies
package was unavailable and is recorded as such.

### Retirement safety boundary

No new deletion target is confirmed. The retirement parser must reject malformed
or unsafe public manifests and preserve the existing external-owner directory,
no-follow and single-link contracts. Security review found that a hostile writer
can still race unlink after validation, so actual apply requires writer stop and
a separately approved exact target. Owner/evidence strings are not
authorization. If apply succeeds but stdout receipt output fails, retry treats
the target as `absent-unverified` and blocks automatic retry until an operator
checks the target; this is not a deletion success receipt. Secret copies,
SMTP-specific retirement and protected recovery material remain P06/existing
executor handoffs.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Current public role mapping | 90 | W95 | Declaration and consumer mapping | Public source rows | PASS | Declaration/consumer source evidence was read; actual use and owner remain explicit `UNKNOWN` where unobserved. | required | - |
| Current runtime role use | 90 | W95 | Service/consumer operation | Operating environment | NOT_RUN | Not authorized or observed; declaration evidence is not runtime use, owner or cost evidence. | required | - |
| Resource assessment binding | 91 | W96 | QA-owned dependency bridge | Canonical registry/service/Compose/HEAD bindings | PASS | Independent 35/35 rerun in 23.509 s; changed execution trace 81/82 (98.8%). Caller projections are rejected. Effective runtime controls and receipt remain unverified, so runtime/mutation acceptance is blocked. | required | - |
| Common-control overlay helper | 91 | W96 | Direct, security and public-copy overlay checks | Root plus documented overlays and LAB CLI | PASS | Direct 30/30, security 18/18, public-copy 18 scopes/1,062 instances/0 findings; trace 335/364 added lines. Recorded source fingerprints and earlier packets remain historical; no runtime limit or host change is claimed. | required | - |
| C1–C6 historical placement | 92 | W97 | Historical acceptance readback | POL-0102 Traceability | NOT_APPLICABLE | Recorded criterion acceptance only; no current migration or restore was run. | optional | - |
| Retirement parser | 93 | W98 | Focused parser rejection and security checks | Owned synthetic fixtures | PASS | Final 135 focused tests; trace 86/88 (97.7%); independent security review 66 checks. This proves rejected/synthetic input behavior only, not apply/deletion. | required | - |
| P09 routing and contract checks | 90 | W95 | Local routing and workflow contract checks | Current public P09 sources | PASS | Final 28/28, exit 0, skip 0, 1.243 s; workflow contract passed. Temporary alternate-index manifest result remains historical and is not a final staged-manifest result. | required | - |
| Broad CI plan | 91 | W96 | Public-plan execution | Existing CI plan | FAIL | 7 failures/323 errors from existing `leaf.p03-hermes` public-execution parity residual; separate P03/CI ownership remains. | required | - |
| Workflow expected-list residual | 93 | W98 | Expected-selector list comparison | Existing workflow test expectation | FAIL | Six P04/P05 registration expectation differences; distinct from P03 execution parity. | required | - |
| P09 DATA review refresh | 90 | W95 | Local inventory scan then validate | 98 retained public review receipts | PASS | 42,018/42,018 files listed; whole review 6/2,322; partial 78/2,322; render 0/17; runtime/restore 0/112. Metadata/listing only. | required | - |
| Service operation, storage move, credential use, external deletion, remote CI | 92 | W97 | Authorized-operation boundary | Current authorization | NOT_RUN | Not authorized in this Task. | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 90 | pending | Current public role mapping, P09 DATA review refresh | Source declaration scope is current; actual use and ownership remain unverified. | SPEC-0212 TSK-0048 |
| 91 | pending | Resource assessment binding, Common-control overlay helper | Source tests pass; runtime/mutation remains blocked because effective controls and receipt are unverified. | SPEC-0212 TSK-0048 |
| 92 | pending | C1–C6 historical placement | Existing SPEC-0246 acceptance, summarized in POL-0102, is reused at its recorded scope; measured drift plus an approved recovery plan is required to reopen. | @buenhyden |
| 93 | pending | Retirement parser | Parser rejection tests pass; apply remains blocked pending exact owner, writer stop and target approval. | SPEC-0212 TSK-0048 |

## Review and Completion

Run documentation, DATA, focused QA and CI-selector checks after source freeze;
record any timeout or unavailable tool as `NOT_RUN`. Run `graphify update .`
after final source changes. Independent code, security, IaC and document review
do not edit another writer's leased path. Current operation, independent restore,
actual deletion, credential rotation, remote CI and final operational acceptance
remain independent results.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Workspace inventory](../../../90.references/data/0096-workspace-inventory/README.md)
- [Common profile policy](../../../05.operations/policies/01-common/0078-compose-profile-vocabulary.md)
- [Host storage placement policy](../../../05.operations/policies/10-platform-and-backup/0102-host-storage-placement.md)
