---
title: "Home Infrastructure Diagnosis and Work Design Specification"
version: "1.0.0"
type: "sdlc/spec"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0201"
parent_ids:
- "REQ-0027"
- "AD-0004"
- "AD-0031"
- "ADR-0045"
- "ADR-0046"
created: "2026-10-02"
---

# Home Infrastructure Diagnosis and Work Design Specification

## Overview

This package contracts Prompt 01: diagnose the current `hy-home.docker` source,
select retained service roles, define the external-project integration boundary,
and produce an approval-ready work design. Its output is evidence and a staged
plan, not a change to running infrastructure. Prompt 02's database/LAB source
implementation follows this package and needs its own approved Spec, Plan, and
Task. The independently planned learning applications in Prompts 07 and 08
provide no current provisioning authority.

The inspected baseline is `main` at
`e2c841eb9ef5086d0fbd6cc2ccd43ea35d89e26d` on 2026-10-02. At execution,
compare the latest main and branch with that baseline before using a finding.
`REQ-0027` and `AD-0031` are draft inputs; `AD-0004`, `ADR-0045`, and
`ADR-0046` describe current accepted boundaries. Archived SPEC-0199 and
SPEC-0200 are historical records, not active Tasks or approval.

## Boundaries and Inputs

Read tracked `AGENTS.md`, canonical bootstrap/provider and applicable approval,
quality, documentation, and Git policies. Inspect the active Requirements,
Architecture, Specs, Plans, Tasks, and registered IDs. Use the root Compose
include graph, its leaf Compose files, Dockerfiles, entry scripts, tracked mount
configuration, environment-variable consumers, policies, `.github/`, scripts,
tests, and current docs. Treat generated projections as outputs of identified
authored sources and generators. Record any absent named document without
inventing its content.

The approved W1-W6 diagnosis covered tracked source and official material. It
did not read actual `.env` values, credentials, keys, auth files, raw operational
logs, untracked host mounts, or live traffic. Source findings, plausible risks,
and unverified runtime conditions remain separate. The user approved the amended follow-up Task TSK-0002 for W7.1-W7.3
read-only observation on 2026-10-02. It collects sanitized aggregate metadata
through approved tools, without exposing secret values, row contents, raw
queries, addresses, or logs. The owner later approved W7.4 Phase A
preflight/verify, then directed it and later recovery work to be deferred
before verify, scratch creation, or restore. W7.4 remains NOT_RUN; its future
execution requires a fresh exact Docker context, project, ports, networks,
volumes, resources, data source, and cleanup approval.

Out of scope are Compose/infra implementation, application code, DB/schema/role
creation, crawler or speech services, GPU/network reservation, HOME service
start/stop/restart/deployment, real-data migration/deletion, credential
rotation, remote push/PR/merge, and DNS/firewall changes. The proposed isolated
restore rehearsal writes only to newly created disposable test state after
separate execution approval; it never attaches HOME PGDATA or changes a HOME
backup repository. Public-data and the
07/08 learning applications belong to workspaces derived from the consumer
main of `buenhyden/Project-Template`, outside this repository. The existing
shared Storybook project is unaffected.

## Behavior Contract

1. The inventory is derived from the current root include graph and separates
   long-running services from one-shot jobs. Each row connects role, actual
   consumer, image/version owner, profile, dependencies, networks, ports,
   authentication, secret reference names, UID/GID, persistence, resource
   limits, health/readiness, backup, runbook, and regression check. Unknown
   runtime fields remain unknown rather than guessed.
2. A baseline comparison covers `infra/`, policies, `.github/`, scripts,
   tests, and docs. It distinguishes current active documents from Stage 98
   archives and records which findings were already implemented. Source
   defects, inferred risks, and environment-unverified conditions have
   different labels and evidence.
3. Role dispositions use confirmed consumers, unique capability, learning
   purpose, resident cost, recovery burden, license, and replacement path.
   An optional definition alone is not waste. Every required overlap pair in
   Prompt 01 receives a keep, improve, optional, LAB, or retire decision with
   rationale and any required follow-up evidence.
4. Traefik stays the default gateway. The proposed development data pair is
   one TimescaleDB Community `dev-pg` and one `dev-valkey`; `mng-pg` and
   `mng-valkey` retain management metadata, sessions, and queues. No
   management TimescaleDB is added without a named consumer. Current
   `app_db` has no business-app consumer per owner confirmation;
   only its observed infrastructure-owned objects are a later migration or
   retirement candidate. Future projects use dev-db, not `app_db`. `perf_db` holds test results with project-scoped
   read, ingest, and verdict authority, not raw samples in management DB.
5. The data-engine decision compares TimescaleDB Community with InfluxDB
   Core, QuestDB OSS, ordinary PostgreSQL, and ClickHouse for SQL,
   transactions, access control, resource use, recovery, and license. It
   distinguishes free self-hosting from open-source license terms and claims
   no performance rank without measurement. Image/digest and compatibility
   pins are rechecked against official sources at implementation time.
6. k6 is the default load generator, WireMock the HTTP stub, and Locust an
   isolated optional practice tool. Prometheus, Grafana, SeaweedFS, and
   Qdrant are reused. The design does not add a duplicate example stack or
   another HTTP mock server without a consumer need.
7. Infra owns engines, shared ingress/identity, observability, backup, and
   limited resource provisioning. An external project owns its business API,
   UI, migrations, collection adapters, workflow definitions, fixtures, E2E,
   and app Compose. The root never includes an external application's source
   path. Metadata registration does not approve runtime deployment or secret
   issuance.
8. A proposed integration manifest records `project_id`, `environment`,
   `infra_ref`, `template_ref`, `project_ref`, endpoints by connection
   location, allowed networks, database and role names, Valkey ACL prefix,
   S3 bucket/prefix, OIDC client, search collection and permission path,
   telemetry `service.name`, backup/restore owners, secret reference names,
   quota, schema/interface version, and approval/verification state.
9. Tier work covers gateway routing/auth/rate limits/retries; OIDC/PKCE and
   admin separation; OpenBao lifecycle; management/development data and LAB;
   CDC/Avro; telemetry discovery/capacity/alerts; Airflow/n8n; AI document
   security/evaluation/GPU contention; platform image/IaC/registry/backup;
   development capture versus delivery; load/mock/contract/accessibility and
   result verdicts; and analytics metadata/business readers and checkpoints.
   Shared Storybook/MCP may become 13-experience only with a real common
   capability. LAB is a separate execution area, not a tier.
10. Voice feature work begins only after product approval and inspection of
    existing Open WebUI/Ollama support, public APIs, and stored configuration.
    ASR, TTS, and pronunciation evaluation are separate capabilities. Real
    voice retention, deletion, capacity, and processing location need their
    own contract; the language-app idea alone establishes no current defect.
11. The work design maps requests 1-12, environment variables, learning
    domains, and overlap decisions to exact source owners, current/target
    state, focused regressions, rollback, and approval. One Task writes each
    shared root, Alloy, environment, and Registry surface; other Tasks consume
    the contract. Existing path-aware validation ownership is preserved.

## Technical Approach

The diagnosis first captures baseline SHA, source inventory, current document
and ID state, and root include/service/job enumeration. It traces consumers
through declared Compose, Dockerfiles, entrypoints, tracked mounts, and env
references. It then records role decisions, unresolved runtime questions, and
the engine comparison. Finally it drafts the external-project manifest and
file-level change ledger. A grep hit is only a lead; semantic claims require
the owning source and a consumer path.

Required overlap review: PostgreSQL HA/single dev PG; Valkey cluster/single
dev Valkey; Kafka multi/single broker and real Avro/Schema Registry consumers;
NoSQL replicas/project data models; Traefik/Nginx and Storybook static server;
k6/Locust/WireMock; Airflow/n8n; Spark/Flink/Trino; Grafana/Superset;
Loki/OpenSearch/Dozzle; Open WebUI/Open Notebook; OpenTofu/Terrakube;
Mailpit/Stalwart; and Supabase/direct business API. Existing services are
not removed merely because their profile is optional.

The approval work breakdown is sequential: 02 database, migration, and LAB
isolation; 03 quality tooling and `perf_db`; 04 common integration and
operations; 05 shared Storybook; 06 the external project's consumed manifest;
07 civil-service learning and 08 language speaking/reading as independent
planning-only tracks. Each later package records its own exact file ownership,
regression checks, rollback, and implementation/operational approval gate.
The data/observability/Registry/root shared surfaces get one writer at a time.

## Interfaces and Data

| Output | Input | Consumer and boundary |
| --- | --- | --- |
| Service/job inventory | Current root include and tracked consumer paths | Role review and later Tasks; no live-state claim |
| Disposition ledger | Consumer, unique function, cost, recovery, license, alternative | 02-06 plans; removals need separate approval |
| Engine decision | Current official license/features and source constraints | 02 data Spec; no unmeasured performance claim |
| Integration manifest proposal | Approved project identity and reference names, never secret values | 06 external project and 04/06 infra provision contract |
| Change/approval ledger | Exact files, current/target, regression, rollback, owner | Later Spec/Plan/Task review; no runtime authorization |

Project-owned DB and Valkey identities are granted only after a concrete
external-project approval. The owner reports no current app uses `app_db` and no data is stored
there. The live catalog did find one technical heartbeat row and a dbt view;
no business dataset was observed. DBeaver connects by SSH to management
PostgreSQL, but whether its session selected `app_db` and the origin of
observed transactions remain unverified. The public-data application uses an external Project-Template-derived workspace; the template itself is
not an app implementation target.

## Failure Modes and Guardrails

| Failure | Guard |
| --- | --- |
| Old inventory count or archived Spec is treated as current | Re-enumerate latest root includes and current Stage 03 IDs; label archive evidence. |
| Source health or test count is reported as deployment evidence | Report static, isolated, HOME, and migration states separately with commands and exit codes. |
| Secret or host data is inferred from tracked metadata | Record reference names only and mark actual values/traffic unknown. |
| Optional definition is retired without consumer analysis | Apply the full disposition criteria and preserve a rollback path. |
| Generated projection is hand-edited | Find authored source and registered generator; validate output against both. |
| Shared files receive concurrent writers | Assign one Task owner and contract consumers before execution. |
| Plan is mistaken for approval to run services or migrate data | Require separately scoped runtime, data, credential, remote, and network approvals. |

## Acceptance Contract

1. The Task records the latest main and branch SHA, the earlier baseline
delta across infra, policy, `.github/`, scripts, tests, and docs, and the
active versus archive document/ID status without using SPEC-0199/0200 as
authority.
2. An inventory derived from the current root include enumerates actual
services and one-shot jobs and provides every field in Behavior 1 or marks
it unverified with the owning evidence path; no historical count is forced.
3. Every finding is labeled confirmed source defect, contextual risk, or
unverified execution state; generated projections name their authored source,
generator, and semantic check limit.
4. The data-engine matrix covers all five candidates and all seven decision
axes in Behavior 5 using current official evidence; TimescaleDB Community is
selected for development business time series without an unmeasured speed
claim or an OSS-license claim.
5. Each overlap pair in Technical Approach has a consumer-based disposition,
unique function, resident/recovery cost, license where relevant, alternative,
and residual uncertainty. The baseline gateway, quality, and shared-stack
choices in Behaviors 4 and 6 remain explicit.
6. The external-project manifest contains every field in Behavior 8, assigns
infra and app ownership as in Behavior 7, and prevents app source paths or
unapproved 07/08 provision from entering this repository.
7. A trace table connects Prompt 01 requests 1-12, env variables, learning
fields, and duplication conditions to the evidence and a later Task or
planning-only track; all twelve tier concerns in Behavior 9 are represented.
8. The change ledger gives exact file owners, evidence, current and target
state, focused regressions, rollback, and approval for 02-06. It gives 07
and 08 separate planning-only scopes and a single writer for each shared
file. A later Plan/Task is not treated as already approved.
9. The final report names baseline/work SHA, changed files, input/output
contract, commands/exit codes/evidence, residual risks, and separate `source
implementation`, `static validation`, `isolated execution`, `HOME rollout`,
and `data migration` status. A skipped or blocked gate is not PASS.
10. Before Prompt 02 source work begins, TSK-0002 identifies the live
`app_db` owner through the owner's no-business-app attestation and catalog
corroboration, inventories external clients and bounded aggregate traffic,
and measures current host capacity against existing policy floors. W7.1-W7.3
are scoped PASS. The owner expressly deferred W7.4's current-backup isolated
restore result on 2026-10-02; W7.4 remains NOT_RUN and is not a Prompt 02
source-work prerequisite. This is a recorded acceptance change, not a restore
PASS. Prompt 02 owns fresh final dev/LAB sizing and margin. Any HOME service
change, real data migration, destructive retention change, or claim that the
current backup is restorable still needs its own evidence and approval.
Collection time, method, sanitized result, limits, and explicit status stay
recorded; a catalog owner or point-in-time connection count alone does not
prove business ownership or absence of external consumers.
11. Prompt 02 has a start gate to recheck the selected image digest, platform
architecture, PostgreSQL/Timescale/pgBackRest compatibility, and license at
its actual implementation time. A 2026-10-02 lookup is a dated observation,
not a future pin or proof of restored data.

## Traceability

- [REQ-0027](../../01.requirements/0027-home-development-host.md) (draft input)
- [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md) (draft input)
- [AD-0004](../../02.architecture/descriptions/0004-data-architecture.md)
- [ADR-0045](../../02.architecture/decisions/0045-data-storage-and-analytics-tier-boundary.md)
- [ADR-0046](../../02.architecture/decisions/0046-capability-tiers-and-quality-boundary.md)
- [Profile vocabulary](../../05.operations/policies/0078-compose-profile-vocabulary.md)
- [Backup policy](../../05.operations/policies/0021-backup-and-restore.md)

## Open Questions

- W7.1-W7.3 read-only observations found only a Debezium heartbeat row and a
  dbt connectivity view in `app_db`, observed transactions without attributable
  clients, and measured host capacity. The owner subsequently confirmed that
  no current app uses `app_db` and reports no stored data; future projects
  will use dev-db. The catalog nevertheless found one technical heartbeat
  row and a dbt view, without an observed business dataset. DBeaver connects
  by SSH to management PostgreSQL. The absence of a current business-app
  owner is resolved; DBeaver selection of `app_db` and the observed
  transaction origin remain unverified. InfluxDB live-data ownership was
  not in this survey.
- Host capacity passes existing policy floors as a snapshot; the proposed
  dev/LAB budget remains a Prompt 02 start gate. Isolated restore is NOT_RUN pending its separate
  approval and exact source/target preflight.
- Which exact image/digest, license revision, and compatibility facts are
  current when Prompt 02 implementation starts? This must be checked then.

## Operational Impact

W1-W6 had none. W7.1-W7.3 used approved, read-only sanitized live metadata
queries. W7.4 isolated restore requires separate execution approval and the
recorded Docker/data preflight. Neither action authorizes HOME
deployment, service stop/restart, real data migration/deletion, credential
changes, remote mutation, or DNS/firewall work. Prompt 02 source implementation
requires its own approved package.
