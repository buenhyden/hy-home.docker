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
and SPEC-0246 C1–C6 remain authoritative at their recorded source, actor,
environment and criterion scope.

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

SPEC-0246 C1–C6 is `REUSE_ACCEPTED`: the recorded owner acceptance places
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

| Evidence | Criteria | Result | Boundary |
| --- | --- | --- | --- |
| Current public role mapping | 90 | SOURCE_READY | Declaration/consumer evidence only; actual use and owner remain explicit UNKNOWN where unobserved |
| Resource assessment binding | 91 | PASS: independent 35/35 rerun in 23.509 s through the QA-owned dependency bridge; new execution trace 81/82 (98.8%) | Canonical registry/service/Compose/HEAD bindings reject caller projections. `control_deviations` remains a caller projection, not measured settings. Effective runtime controls and the receipt itself remain `EFFECTIVE_CONTROLS_UNVERIFIED`/`RECEIPT_UNVERIFIED`, therefore BLOCKED for runtime or mutation acceptance |
| Common-control overlay helper | 91 | PASS: latest direct 30/30, skip 0, exit 0 (0.037 s); independent security 18/18; public-copy root+8 overlays+9 LAB CLI 18 scopes/1,062 instances/0 findings; stdlib trace 335/364 added executable lines (92.0%, subprocess excluded) | Frozen source `d9e901e08f7f037d70e8b692902f5f60363c4d6417f6b3ce49bb273dc2a5fbdb`, direct-test source `2b53691ac5cde8f5795635f4e6ce84beb4a82e17a85b200f8f9d518e431e68c8`. Owned volatile trace counts were `/tmp/p09-controls-final.tSZlDh/counts`, not a retained test log. The earlier 26/26 and security14 packets remain history, not the latest source result. Base/overlay provenance source behavior only; no runtime limit or host change |
| C1–C6 historical placement | 92 | REUSE_ACCEPTED | Recorded criterion acceptance only; no current migration or restore is claimed |
| Retirement parser | 93 | PASS: final 135 focused tests, changed executable-line trace 86/88 (97.7%) | Independent security review passed 66 focused checks. Earlier 133-test/77-of-79 trace packet remains prior-fingerprint history. Trusted `/usr/bin/git` with a minimal environment rejects PATH shim bypass. This proves only rejected/synthetic input behavior; no apply/deletion evidence |
| P09 routing and contract checks | 90–93 | PASS: final 28/28, exit 0, skip 0, 1.243 s; workflow contract (5 workflows/7 jobs/9 actions) PASS | The temporary alternate-index script manifest PASS (26.185 s); actual final staged manifest remains required |
| Broad CI plan | 90–93 | NOT_PASS: 7 failures/323 errors | Existing `leaf.p03-hermes` public-execution parity residual; preserve separate P03/CI ownership |
| Workflow expected-list residual | 90–93 | TEST_RESIDUAL: 6 expected-list registration differences | P04/P05 registration ownership, distinct from the P03 execution-parity residual |
| P09 DATA review refresh | 90 | PASS: post-controls-freeze local `scan` then `validate` using 98 retained review receipts | 42,018/42,018 files listed; whole review 6/2,322 and partial 78/2,322; render 0/17, runtime 0/112 and restore 0/112. This is metadata/listing only, not a body, configuration, operational or restore acceptance |
| Service operation, storage move, credential use, external deletion, remote CI | 90–93 | NOT_RUN | Not authorized in this Task |

## Criterion Acceptance

| Criterion | Decision | Current owner / resume condition |
| --- | --- | --- |
| 90 | SOURCE_READY | TSK-0048: keep all 15 public-source rows and unknowns current after source freeze |
| 91 | SOURCE_READY | Controls and resource source tests pass; runtime/mutation remains BLOCKED because effective controls and receipt are unverified |
| 92 | REUSE_ACCEPTED | SPEC-0246 owner evidence remains scoped; reopen only for measured drift plus approved recovery plan |
| 93 | SOURCE_READY | Parser rejection tests pass; apply remains blocked pending exact owner, writer stop and target approval |

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
- [SPEC-0246 storage Task](../../0246-host-storage-tiering/tasks/tsk-0001-host-storage-tiering.md)
