---
title: "Service Integration, Security, and Operations Plan"
version: "1.8.3"
type: "sdlc/plan"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-11"
layer: "specs"
artifact_id: "SPEC-0204-PLAN-0001"
parent_ids:
- "SPEC-0204"
created: "2026-10-03"
---

# Service Integration, Security, and Operations Plan

## Overview

### Objective

Continue this package's residual integration acceptance in reversible Tasks.
The 2026-10-03 source slice and old prompt labels below are historical work
provenance. Current execution follows SPEC-0212's 2026-10-10 P00 routing,
exclusions and shared-writer order; completed Task bodies are preserved.

### Dependencies

- Local and remote `main` at `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`
  when drafting; fetch/recompare before source implementation.
- SPEC-0201 W5 exact handoff, SPEC-0202's dev data/backup contract, SPEC-0203's
  completed source and isolated synthetic quality/Alloy contract and current
  Requirement/Architecture. Real external-project/store/reader connections
  remain outside that completion receipt.
- User approval of this Plan and the listed Task source scopes on 2026-10-03.
- Kafka connector and backup-policy ownership transfer follows SPEC-0202 lifecycle
  closure, integrated locally before TSK-0003 source writing.
- Official n8n, Crawl4AI, Cassandra, backup and security references rechecked
  at implementation; image architecture/digest and secret consumer behavior
  remain runtime-unverified until bounded acceptance.
- A real consumer, native workflow target, credential subject and recovery
  boundary must be named before their dependent runtime lane. Learning-app
  planning and all actual LAB work are excluded. Source and this request's
  branch/PR/merge are authorized without repeated approval.

### Current execution routing — 2026-10-10

SPEC-0212-TSK-0003 owns the P00 baseline and documentation amendment; existing
SPEC-0204 Tasks retain their historical evidence. P03 owns port/endpoints,
P04 Airflow native integration, P05 n8n native import/execution and P01/P02/P06
secret classification/mapping/consumption under this package's acceptance.
SPEC-0213/0214/0218/0219/0220/0223/0224/0227 retain their delivered source;
no old prompt label creates duplicate work. LAB runtime and learning apps,
including planning, are out-of-scope. P08 may separately move typed LAB
documents; P09 now owns only offline Wiki preparation, and its future
application/workspace and runtime resources require a later exact Task. P10
retains its real input-to-recovery target.

Historical W7 CI retirement does not govern this pass: current quality policy
and workflow-contract route hosted PR candidate QA and independent review.
Historical source-only restrictions bind the old slice, not all future units.
Only a missing real target/tool permission stops its dependent action. Follow
current approval-boundaries and SPEC-0221; no policy/hook/validator rewrite is
needed when the current enforcer already meets the request.

Shared root, gateway, Alloy, environment and backup files have one writer at a
time. Complete feature edits before the P08 document move writer starts, then
update references/checks and hand the destination SHA back. P08 may move typed
LAB documents to their `labs/` destinations with required folder and parent
README navigation, Registry links and path checks. LAB runtime changes remain
out of scope.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 8 | Freeze source and authority | None | TSK-0001 | Task evidence |
| W2 | 2, 3, 4 | Repair compatibility and security source | W1 | TSK-0001 | Task evidence |
| W3 | 4, 5 | Contract external connection | W1 | TSK-0002 | Task evidence |
| W4 | 6, 7 | Close backup and cross-tier handoffs | None | TSK-0003 | Task evidence |
| W5 | 1, 2, 3, 4, 5, 6, 7, 8 | Verify and hand off | W2, W3, W4 | TSK-0001, TSK-0004 | Task evidence |
| W6 | 8 | Retire completed migration-only QA while preserving current lifecycle and archive owners | None | TSK-0001 | Task evidence |
| W7 | 8 | Retire hosted public QA while preserving local changed/full selectors, main security, and historical evidence | W6 | TSK-0001 | Task evidence |
| W8 | 1, 9 | Second-round baseline, owner map and HOME observations | None | TSK-0005 | Task evidence |
| W9 | 7, 9 | Dev-valkey snapshot and isolated queue replay | W8 | TSK-0005 | Task evidence |
| W10 | 4, 9 | Secret file support matrix and wrapper refusal | W8 | TSK-0005 | Task evidence |
| W11 | 3, 6 | Image namespace residue and mail outcome states | W8 | TSK-0005 | Task evidence |
| W12 | 8, 9 | Validation and handoff | W9, W10, W11 | TSK-0005 | Task evidence |
| W13 | 7, 9 | OpenBao Raft snapshot with a snapshot-only token | W12 | TSK-0005 | Task evidence |
| W14 | 7, 9 | Open WebUI key kept in its backed-up volume | W12 | TSK-0005 | Task evidence |
| W15 | 6 | CDC stream rehearsal from dev-pg to decoded Avro | W12 | TSK-0005 | Task evidence |
| W16 | 4 | Gateway answers machine clients 401; SSO rehearsal | W12 | TSK-0005 | Task evidence |
| W17 | 4, 9 | SonarQube JDBC password from its secret | W12 | TSK-0005 | Task evidence |
| W18 | 8, 9 | Third-round validation | W13, W14, W15, W16, W17 | TSK-0005 | Task evidence |
| W19 | 1, 11 | Baseline, existing source exclusions, exact endpoint and recovery boundary | None | TSK-0006 | Tracked source/official tagged 2.6.2 docs; independent IaC design review |
| W20 | 4, 11 | TLS listener/Agent/metrics/Traefik and wrapped reissue/readiness | W19 | TSK-0006 | RED/GREEN failure, argv/redaction and endpoint tests |
| W21 | 7, 11 | Declarative HMAC audit, capacity/failure alerts, reuse snapshot flow | W20 | TSK-0006 | Exact image isolated audit and snapshot recovery cases |
| W22 | 8, 11 | Changed QA, independent IaC/security/code review, scoped commits/PR | W21 | TSK-0006 | Registered local/hosted candidate checks and actual delivery receipt |
| W23 | 11 | HOME cold boot, independent custody and selected real backup recovery | W22 | TSK-0006 | NOT_RUN until external facts, fixed runtime/cleanup proof and concrete boundary exist; HOME/P06 held |
| W24 | 12 | Assess consumers and implement the narrow private-unlink helper for material retired by another owner after SMTP01 evidence | W19 | TSK-0007 | Helper unit tests and document gates; private apply only after Task preflight |
| W25 | 13 | Prepare bounded LLM Wiki contracts, synthetic fixtures and future acceptance without provisioning | None | TSK-0008 | Frozen preparation QA: 35 PASS, 99-percent coverage; registration integrated. Historical candidate CI failure retained in Task 0008; current local-main source gates/review support delivery, resource changes 0 |
| W26 | 14 | SMTP01 baseline, consumer/source map and failing regressions | None | TSK-0005 | Source SHA and RED command receipts |
| W27 | 14 | Canonical root source and Supabase SMTP-only wrapper/target alias | W26 | TSK-0005 | Unit and synthetic selected Compose model |
| W28 | 14 | COMM-002 ownership, COMM-003 tombstone and guarded retirement helper | W27 | TSK-0005 | Equal/mismatch/idempotency/race/privacy tests; no HOME mutation |
| W29 | 14 | Exact-image synthetic SMTP authentication, capture and failure cases | W27 | TSK-0005 | Opt-in isolated native rehearsal, separate from HOME |
| W30 | 8, 14 | Current-source checks, independent review and coordinator handoff | W28, W29 | TSK-0005 | Preserve logical commits; reviewed local-main delivery under the superseding user instruction; HOME send/authentication and operational retirement acceptance remain separate |
| W31 | 15 | Integrate SEC01 stable/security ledger, source receipts and bounded repairs; continue exact operational validation | None | TSK-0009 | Source/common repairs, isolated datastore and current local leaf receipts integrated. Global latest/security evidence, HOME deployment and complete recovery remain pending/blocked; SOURCE delivery does not close SEC01 |
| W32 | 16, 8 | P02 single value-free catalog, classification, generated views and reissuance guards | W27, W28 | TSK-0010 | Existing source/schema reuse, alias and privacy RED/GREEN, scoped changed/staged checks and independent review; real migration/recovery are separate lanes |
| W33 | 1, 4, 6, 8, 17 | P03 current service/endpoint/environment and four-location port contracts; independent source preparation before consumer-specific runtime acceptance | W27, W28 | TSK-0011 | Existing inventory/tool reuse, synthetic RED/GREEN, privacy and DEV/MNG independence; final mappings and native/HOME checks follow their exact owning prerequisites |
| W34 | 1, 8, 18 | P04 baseline, source reuse, exclusive ownership and RED cases | None | TSK-0012 | Current SHA/consumer ledger; reference audit is not native acceptance |
| W35 | 18 | Strict manifest/parser/adapters, immutable inputs and byte-derived idempotency | W34 | TSK-0012 | RED/GREEN validation, privacy, replay and object/DB failure tests |
| W36 | 18 | Versioned DEV role/schema/publication/outbox contract; freeze the P05 interface | W35 | TSK-0012 | Reuse provisioning guards; migration/SQL security review and executable denial cases |
| W37 | 18 | Zero-I/O DAG parsing, compatible image and worker-only Compose proposal | W34, W35 | TSK-0012 | Exact-image import and rendered model; coordinator integrates shared hunks |
| W38 | 18 | Isolated then selected DEV/S3/Celery execution, concurrency/backfill and empty restoration | W36, W37 | TSK-0012 | Relevant image acceptance and exact resource/recovery boundary; no full-SEC or P06 global dependency |
| W39 | 8, 18 | Registered gates, independent review, logical commits, owning-Spec PR and handoffs | W38 | TSK-0012 | Current-head checks/review; preserve unexecuted lanes and actual delivery receipt |

### P04 start, ownership and ordered native acceptance

TSK-0012 is issued from clean local main
`74feff9429d302233d2475b31beed3dbf2ac07c9`; fresh fetch confirmed remote main
`6da5e3bf380d5002e0e28181136fde8c016e49ce` with no open PRs and successful
remote quality checks. Those checks do not certify SEC01 security/HOME or a
P04 workload. The worker branch is `codex/p04-airflow-manifest-pipeline` in
`.worktrees/p04-airflow-manifest-pipeline`, from the issuance commit. This
assessment launches no implementation chat and preserves other dirty worktrees.

W34-W37 public source, synthetic tests and draft SQL/outbox design may begin
independently of full W31/SEC01 and W33/P03 completion. There is no current P04
workload to reimplement. TSK-0012 lists the exact new workload/test files; one
canonical workload owns its SQL and P05 later consumes its versioned contract
read-only. Existing DEV provisioning and database policies are reused through
a reviewed narrow extension, not a second provisioner with conflicting grants.
P04 submits base-blob-bound proposals for the existing provisioner, Dockerfile/
constraints, Compose/environment/networks, S3 policy, catalogs, Stage05/README
indexes, Registry and manifest/workflow registration. The current named owner
or coordinator writes each shared file once.

Before W38, SEC01 supplies the relevant Airflow image/core/Python/provider/
constraint and security receipt; P03 supplies the selected DEV/object endpoints,
worker identity and network contract; P02 supplies reviewed secret references.
Bound the exact synthetic or DEV resources, migration, credential delivery,
budget, operator, backup/empty-restore target, cleanup and rollback. Protected
worker-only files may support DEV proof before OpenBao migration; P01/P06 are
needed for subsequent OpenBao delivery, not all P04 tests. Shared native
execution is sequential: P04 provisions/publishes and verifies outbox first;
P05 uses its frozen SQL/lease contract to notify afterward. No n8n writer edits
P04 SQL or silently changes outbox semantics.

P04's full prompt selects logical commits and an owning-Spec PR with actual
latest-head CI and independent review. Reconcile the local documentation
prefix with fresh remote main before that PR. This issuance performs no remote
write or deployment; SEC01/SMTP01/CLN01 keep their local-main delivery. Do not
close Task-0012 or the broader P04/P05 workflow acceptance on unit tests alone.

### P03 parallel start and dependency boundaries

TSK-0011 is issued from clean local main
`6da5e3bf380d5002e0e28181136fde8c016e49ce`; read-only remote verification
returned `2b9f5ec82cb73ea148fb27bfbd2d35c10e328e51` and no open PRs. Local main
contains three unpublished documentation commits. The worker starts at the
Task issuance commit in its own `codex/p03-service-integration-contracts`
branch and `.worktrees/p03-service-integration-contracts` worktree. This
issuance creates no second implementation session. Completed TSK-0002/0003
and TSK-0005's historical/SMTP work are not reopened or overwritten.

W33's declared prerequisites W27/W28 have integrated source; full SEC01/HOME
completion is not a prerequisite to offline preparation. P03 reuses the bounded
`current-service-inventory` in m0021 and its existing operations-catalog
renderer. It owns only its Task, new port schema/README, library/CLI and dedicated
synthetic tests. It audits other current root services read-only and submits
service-specific fixes with exact file leases before writing them. The supplied
reference parser is partial: it does not establish actual listeners, complete
short/IPv6/range forms, aliases, authentication or recovery.

P01 owns OpenBao helpers/configuration and subject-0085/README; P02 now prepares
catalog paragraphs as proposals to that writer, superseding the earlier P02
subject-0085 assignment below. SEC01 owns image/version/security decisions;
SMTP01 owns COMM-002/COMM-003 and its executor; CLN01 owns consumer/deletion
assessment. Root/leaf Compose, environment, gateway, Keycloak configuration,
Alloy, backup, inventory, Registry, manifest/workflow and shared tests are
proposal-only to the P03 worker until a named exclusive lease is recorded.
The coordinator combines reviewed hunks rather than replacing whole files.

Final secret mappings await P02 catalog and P01 auth/recovery contracts;
relevant exact-image security acceptance precedes HOME activation. Legacy
`SERVICE_POSTGRES_*` deletion awaits CLN01 consumer evidence. P03 supplies the
connection boundary to P04/P05; their future native workers are not assumed
present. P06 migration waits on P01/P02/P03 and real consumer proof. A missing
runtime target defers that lane, not the offline source unit. Each selected
runtime action binds target, operational writer, resource/recovery bounds and
independent review; no whole-stack restart or private-state mutation occurs
in Task issuance.

The supplied P03 prompt requests its owning-Spec PR after implementation,
current-head CI and independent review. First reconcile the local-only
preparation prefix with the fresh remote base; do not include unrelated worker
commits or publish main implicitly. SEC01/SMTP01/CLN01 keep their authorized
local-main delivery. Dev remains unused. Task 0011 carries the executable
worker handoff and exact acceptance/evidence map.

### P02 parallel start and shared ownership

TSK-0010 is issued from clean local main `2b9f5ec82cb73ea148fb27bfbd2d35c10e328e51`.
The first remote observation was `a31a38ca`; a later `ls-remote` and fetch
confirmed remote main at the same `2b9f5ec82` integration revision. P02 uses its own worktree and
`codex/p02-secret-catalog` branch from the Task issuance commit. Integrated
SMTP01 permits public classification and provisional mapping now; P01's final
OpenBao image, authentication and recovery evidence still gate final runtime
destinations and P06 migration. This narrows the historical P01-before-P02
dependency to those final mappings; it does not assert a P01 runtime PASS.

P02 is the sole implementation writer for its new catalog/schema/view tooling,
focused tests and subject-0085 secret documentation. SEC01 owns images and
exact-image support verdicts; SMTP01 owns canonical source and retirement;
CLN01 owns consumer/delete assessment. Existing shared generator, public view
and support-matrix changes are proposals until the coordinator serially
integrates them against the current head. Root Compose, environment, Registry,
workflow/manifest registration, backup and other active Tasks are read-only to
the P02 writer. The SEC01/SMTP01/CLN01 integration retains its local-main
delivery instruction. The newly supplied P02 execution prompt instead requests
an owning-Spec PR after implementation, current-head CI and independent review.
P02's PR must contain only its own logical units against a fresh remote baseline;
this assessment/issuance performs no remote push or PR creation. Dev remains
unused. Current remote synchronization does not certify operational acceptance.

### SMTP01 sequence and private-operation boundary

SMTP01 starts at `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`. Work is isolated
in `/tmp/hy-home-smtp01` on `codex/smtp01-canonical`; concurrent root edits are
preserved. The integration order is SEC01, SMTP01, then CLN01, subject to actual
owning-Spec dependencies. Current implementation and tests do not change HOME,
private metadata or either real SMTP file. Image tags/projections remain SEC01
ownership; exact digests belong only to the isolated test fixture here.

The private duplicate deletion target is exactly
`/home/hyunyoun/data/hy-home.docker/secrets/communication/supabase/supabase_smtp_password.txt`.
Canonical `secrets/communication/smtp/smtp_password.txt`, username, host and
account remain protected. CLN01/the coordinator verifies all consumers and
backup/restore facts, records a sanitized audit receipt, switches any old inode
consumer by selected recreation and then releases SMTP01’s sole narrow retirement executor. Separate CLN01
and SMTP01 locks do not prove cross-executor exclusivity.
Unclear facts or mismatched values stop only that operation. RUN-0029 owns
exact check/apply commands and canonical-only recovery; SMTP01 does not execute
private comparison, unlink, broad sync/prune, rotation or HOME deployment.

### P01 current continuation ownership and sequence

The 2026-10-11 assessment continues existing blocked TSK-0006/W19-W23;
it allocates no new Task or Spec. Assessment input is clean local main
`728ec6379f193256cee342550e38479cf3ebfc56`, remote main `2b9f5ec82`.
Server/Agent declaration is SEC01's exact 2.7.1 contract; fresh HOME metadata
still reports both on 2.6.2. Historical source and isolated receipts are retained.
Task-0006's current continuation section owns the exact worker instructions.

One P01 writer owns OpenBao scripts/config except P02's catalog/schema,
its named Agent/issuance/candidate/rehearsal tests, Task-0006 and subject-0085
Guide/Policy/Runbook plus the OpenBao README. P02 retains catalog/schema,
classification/views and its own tooling/tests; its 0085/README paragraphs are
proposals to P01. SEC01 owns image selection, signature/SBOM/CVE decisions and
version projection; it does not concurrently edit P01 helpers/tests.
The coordinator alone integrates OpenBao Compose, root/environment, gateway,
Prometheus/Gatus/Alloy, backup, shared CI/manifest/validators, Registry/inventory
and Spec/Plan. Proposed shared changes bind exact base blob IDs and are reviewed
once; same-file writers never overwrite one another.

Reuse implemented TLS/wrapping/readiness/audit/snapshot and restricted cleanup.
Change only proven residuals, including issuance_id metadata/journal compatibility.
Current source preparation and needed synthetic isolation can proceed without
closing W23. The P01 operational contract must bind the exact HOME containers,
source runtime/image, credential and TLS paths, snapshot artifact, independent
custody, owned empty restore target, limits, operator/independent reviewer,
existing human authorization, rollback and retained result before any action.
No production fault injection, real consumer migration or P06 release occurs.
SEC01's image/security acceptance and actual backup/custody/empty-restore
preconditions gate only HOME activation; do not wait for unrelated images to
finish before doing P01 source/isolated work.

The later P01 prompt requests an owning-Spec PR after implementation. Preserve
logical commits and align preceding local-only coordinator documentation with
remote main before a P01-only diff is submitted; do not mix unrelated SEC/P02
implementation or bypass latest-head CI/review. This assessment creates no PR,
remote push or runtime change. P02 and P01 use separate clean worktrees; dev is
unused. The following original scope is historical, not a current writer lease.

### P01 historical source scope and sequence

The original source input was main/origin/main
`1ee5d6707e3b75b61222baad0c51050c64e1b10d`, clean at start. Compared with d19fbfde6, only P00 documentation changed;
OpenBao executable source is unchanged. This request authorizes source,
synthetic isolated 2.6.2 tests, documentation, commits and checked PR delivery.
The user's `ok` accepts isolation first and supplies no HOME host/CA/custody
facts. No HOME rollout, real credential use/rotation, host reboot, raw auth/log
inspection or real recovery is inferred. No LAB paths are inspected or changed.

The root implementer owns OpenBao Compose/HCL/TLS/audit source, both Prometheus
scrape configs and its start script/Compose mounts, Traefik backend transport,
OpenBao alert rules and only its existing root secrets-group exception row, the current service inventory fields for
only these five changed services, this package's Spec/Plan/new Task and Korean OpenBao
README/GDE/POL/RUN plus only changed RUN-0021/RUN-0098 passages. A bounded
worker owns only the three new OpenBao Agent/reissue shell scripts and their
unit test; another bounded worker may own only the isolated rehearsal test and its two _openbao_rehearsal helper modules.
Root serially integrates workflow test registration/script manifest if needed.
No completed Task body, common-v2 implementation, LAB exception, Registry allocation, image
pin, data/secret file, external application or LAB document is changed.
Shared gateway/Prometheus/backup files have one writer; P08 moves wait for this
feature input and remain a separate stage. Existing snapshot policy and backup
implementation are reused. Before HOME activation source rollback is a protected logical revert;
HOME rollback/recovery is a separate gate and is never inferred from Git.

The root writer also owns `scripts/hardening/check-all-hardening.sh` (retire
its internal-HTTP requirement), `infra/06-observability/gatus` endpoint/CA
entrypoint changes, the existing backup missing-token failure branch,
`tests/validation/test_service_runtime_compatibility.py`, affected Gatus unit
fixtures, `infra/03-security/openbao/scripts/start-server.sh`, renderer role
metadata/version templates, exact metadata reads, issuer policy and TLS material preflight. These are the same atomic TLS/
bootstrap change, not extra engines or downstream consumer migration.

### Work Details

1. **W1: freeze source and authority.** Recheck main, root include, current
   service consumers, lifecycle IDs and protected paths. Confirm the exact
   changed-file ledger and separate confirmed defects from runtime questions.
   Update the Task if a concurrent change has closed a finding. Maps
   acceptance 1 and 8.
2. **W2: repair priority compatibility and security source.** TSK-0001 owns
   n8n server/worker/runner version, timeout and secret-file consumption,
   Crawl4AI advisory response, Cassandra LAB verification and OpenBao sealed
   readiness. Select a current compatible pin only after official/image check;
   retain metadata/encryption-key recovery gate before HOME DB upgrade. Use
   isolated synthetic execution only after Docker preflight. Maps 2, 3, 4.
3. **W3: contract external connection and access.** TSK-0002 owns a
   generic infra-side registration schema, validator and synthetic fixtures.
   Traefik/auth/network/Alloy source stays read-only until a named project
   supplies approved values in a later exact Task. Preserve Traefik's opt-in
   Docker discovery and SPEC-0203's quality metrics. No project-specific
   account, bucket, OIDC client, network or secret is issued here. Maps 4 and 5.
4. **W4: close backup and cross-tier handoffs.** TSK-0003 owns dev-pg
   repository inclusion in Restic and the bounded scheduler source only after
   SPEC-0202 ownership handoff. Review CDC/Avro, workflow payload, AI GPU,
   mail delivery and analytics reader/checkpoint paths. Source modifications
   require confirmed consumers and contract fixtures; otherwise mark them
   `BLOCKED` with a named follow-up owner. Maps 6 and 7.
5. **W5: verify, document and hand off.** TSK-0004 serially owns the later
   whole-tree secret path, metadata and actual/public environment parity
   request. It preserves values and IDs, writes only its exact consumer
   ledger, and keeps credential rotation/HOME recreation separately approved. Run focused tests, scoped Compose
   render, registered projection generators/checks, relevant document and
   path-aware gates. Obtain independent code and security review. Record each
   command, exit, revision and unsupported environment separately; stage
   durable operations meaning in existing Stage 05 owners. Maps 1-8.
6. **W6: retire completed migration-only QA.** TSK-0001 removes the
   SPEC-0153-only leaf, its current gate callers, and its dedicated test module
   after a RED regression proves the lifecycle aggregate still has the obsolete
   fourth child. The contract, hook, and corpus lifecycle leaves remain the
   exact current owners. Preserve general archive tests, frozen source and
   recovery references, current retired-authority guards, and the bounded npm
   exception. The prerequisite is the approved current source baseline and
   frozen W6 writer ledger, not completion of runtime-blocked W5. Maps 8 without
   completing this blocked package.
   Keep the public metadata regression on a coherent Git baseline instead of
   copying unrelated live owner Tasks into its synthetic SPEC-0210 snapshot.
   If the final gate reaches the PostgreSQL timeout fixture, add only its
   source terminal-state stub and permit one fresh public revalidation.
7. **W7: retire hosted public QA.** TSK-0001 removes the quality workflow's
   pull-request and manual triggers with the `validation-changed` and
   `validation-full` jobs, then aligns the typed workflow contract, checker,
   regressions, current governance, and operations guidance. The public
   `changed` and `full` selectors remain available for exact local Task
   evidence, and `main-security` plus its channel-tag dependency remain on main
   pushes. W7 authorizes no remote control-plane mutation and does not complete
   the blocked runtime package. Task-bound local validation and independent
   review own W7 candidate acceptance. Remote integration follows its
   separately approved delivery boundary and actual readback; local success is
   not a merge receipt, and no hosted PASS is inferred. Maps 8.

8. **W8: second-round baseline.** Recheck main, map which file each of
   SPEC-0213, 0214 and 0215 owns, and observe HOME authentication, CDC,
   workflow and backup state read-only. Maps 1 and 9.
9. **W9: dev-valkey snapshot.** Add the bounded RDB export to the nightly
   run and prove restore and queue replay in an isolated container. Maps 7
   and 9.
10. **W10: secret file support.** Record a verdict per rendered key and image,
    keep unsupported services out of HOME by test, and make the Keycloak
    wrapper refuse empty secrets. Maps 4 and 9.
11. **W11: residue and mail.** Refuse Bitnami images across active Compose
    and Dockerfiles, and separate mail outcome states in RUN-0070. Maps 3
    and 6.
12. **W12: validation and handoff.** Run the changed gate and record the
    remaining gaps with owner actions. Maps 8 and 9.
13. **W13: OpenBao snapshot.** Add a Raft snapshot to the nightly run with
    a periodic token limited to the snapshot path, and prove save, restore
    and unseal in isolation. Maps 7 and 9.
14. **W14: Open WebUI key.** Keep the generated key in the data volume and
    back it up with the uploads. Maps 7 and 9.
15. **W15: CDC rehearsal.** Run the tracked provisioning and connector end
    to end with decode, evolution, resume and heartbeat checks. Maps 6.
16. **W16: gateway machine path.** Answer an unauthenticated JSON client
    with 401 instead of a login page, proven by an SSO rehearsal before the
    HOME change. Maps 4.
17. **W17: SonarQube secret.** Replace the ignored `_FILE` key with a
    wrapper. Maps 4 and 9.
18. **W18: third-round validation.** Run the changed gate and record what
    stays open. Maps 8 and 9.

### Rulings

SPEC-0203 already wrote the common Alloy metrics path; TSK-0002 may extend only
bounded external discovery after review. SPEC-0202 development DB source and lifecycle handoff are integrated in this
closure branch before the backup source change. SPEC-0219 owns Storybook. P09
W25 prepares future application-manifest and deployment acceptance only; it
does not create an external workspace. Existing LAB evidence is excluded from
new execution.
SPEC-0220 already owns Crawl4AI security/egress and HOME receipts; its consumer
admission remains consumer-dependent rather than a repeat security fix.

### Historical closure-branch completion recheck — 2026-10-04

At closure source `451b1ec7e4c5509e088a17c9c0f33e3dab93ddd7`, W4's
Restic/dev-pg source chain and approved synthetic restore passed; TSK-0003 is completed with its exact selected-set/snapshot receipt.
TSK-0002 and TSK-0004 remain completed. W2's exact-image n8n/Crawl4AI runtime
and secret/egress security acceptance remain BLOCKED in TSK-0001, so this Plan
and Spec remain active. Image pulls and the reviewed isolated security fixture
require the pending scope approval; HOME and host policy changes remain held.

Protected PR358 activated the current Plan and Tasks; SPEC-0204-TSK-0001 now owns the
exclusive reintegration ledger and fresh validation. The historical Task
completion statements above are closure-branch receipts, not new execution
or current lifecycle transitions. Runtime gaps keep this Plan active.

### Current prerequisite routing — 2026-10-04

The owner requested prerequisite reconciliation; exact writers for this pass
are this Plan and [SPEC-0204-TSK-0001](tasks/tsk-0001-runtime-compatibility-and-security.md).
Protected baseline is
`ebeb83521c768fedc620380b0c2e92db10a6fcdc`; Task2/3/4 completed source and
private parity receipts are already delivered. This pass neither reopens them
nor duplicates their implementation. The current Task owns source, synthetic,
image-cache, runtime, and security evidence; its derived status is `blocked`.

Before separately authorized runtime work, the Task's recorded prerequisites
remain exact image digest and entrypoint review, isolated non-HOME context,
bounded network and resources, synthetic secrets, redaction, failure
preservation, and identity-bound cleanup. This Plan does not duplicate those
findings or authorize an image pull, container run, HOME change, live secret
use, or host/DNS/firewall mutation.

### CLN01 execution boundary

TSK-0007 owns the material-retirement manifest contract, helper source and
focused tests. SMTP01 owns canonical SMTP cutover and generator work; CLN01
does not implement or merge either shared surface. `COMM-003` can enter the
assessment lane only after SMTP01's merged delivery and recorded source and
operational cutover evidence; its dependent PR is TBD. SMTP01 proof cannot
populate CLN01 manifest truth automatically. CLN01 performs a fresh
five-axis consumer assessment before a private apply. The operator checkout is
`/home/hyunyoun/data/hy-home.docker`; host Docker observations still require a
mapping to that checkout. A manifest is under `/tmp/cln01-<run>/`, in an
operator-owned 0700 directory, and is a 0600 regular single-link file. No
manifest value or credential byte enters tracked evidence.

`PG-020` remains retained for rollback because its observed nlink is 2;
canonical `COMM-002` remains protected; `COMM-003` is pending SMTP01 evidence
and all five checks.
Optional stacks are `UNKNOWN_BLOCKED`; `owner@buenhyden` re-reviews them by
2026-10-17. LAB runtime, secrets, data, images and Compose remain excluded.
Source rollback is a logical owning-commit revert. Private recovery requires an
existing encrypted artifact or a proven reissue path and is not promised.

The generic CLN01 helper refuses COMM-003 by ID and exact path. The proposed
sole candidate executor is SMTP01's `smtp_contract --retire`; CLN01 owns the
assessment/hold. Integration must confirm that executor, use the shared retirement lock, and
enforce receipt freshness before any private apply. The present user-integration
hold remains until the supervisor selects one route; no private execution is
authorized by either tool's source checks.

## Verification Plan

### Verification

For each Task, select its current path-aware tests from the repository matrix.
Compose or Docker source requires synthetic env render, secret-ref/route checks
and scoped static validation. A container run requires exact Docker context,
project, ports, networks, volumes, resource budget and cleanup review before
execution. Generated version projection uses its registered generator, not
manual JSON edits. Stage 03 metadata/link checks and `git diff --check` apply
to changed documents. Protected PR checks are required for remote integration;
local success is not a merge receipt. HOME activation, real backup/restore,
data migration and real external-project
connection remain `NOT_RUN` here. The separately approved synthetic dev-pg
Restic restore passed in TSK-0003 and is not HOME recovery evidence.

## Risks and Rollback

### Risk and Rollback

| Risk | Bound and recovery |
| --- | --- |
| n8n update mutates metadata or encryption compatibility | Back up compatible metadata and key before any separate HOME upgrade; source rollback alone cannot reverse DB migration. |
| Runner token or Valkey secret is not consumed | Test actual entrypoint with synthetic files; no plaintext arguments, shell tracing or unbounded environment export. Revert only Task-owned source on failure. |
| Crawler fix changes allowed URLs | Use pinned synthetic DNS/redirect/private-destination cases; a separate bridge is not egress enforcement. Preserve the prior image declaration until source acceptance. |
| External discovery widens collection or ingress | Require project/service network or backend auth, direct-peer denial, authenticated OTLP identity mapping, trace scrub and quotas; reject unregistered peers. Revert scoped source; do not delete project state. |
| Backup path is incomplete or data is deleted | Include mount, list, scheduler, offsite and alert as one reviewed source change; no live PGDATA copy, retention/prune or restore without separate approval. |
| Parallel writers change shared files | TSK-0001, then TSK-0002, then TSK-0003 write serially. Rebase against exact preceding diff; do not reset, stash or clean another worker's state. |
| Observed protection still names a retired required context | Preserve the general no-bypass default. For W7 only, use the separately approved one-time Task delivery boundary and actual remote readback; do not infer a hosted PASS or weaken the post-merge security audit. |

## Related Documents

- [Specification](spec.md)
- [Current routing](../0212-request-baseline-and-reconciliation/plan.md)
- [Task 0001](tasks/tsk-0001-runtime-compatibility-and-security.md)
- [Task 0002](tasks/tsk-0002-external-project-integration.md)
- [Task 0003](tasks/tsk-0003-backup-and-cross-tier-operations.md)
- [Task 0004](tasks/tsk-0004-secret-layout-and-environment-parity.md)
- [Task 0005](tasks/tsk-0005-cross-tier-contracts-second-round.md)
- [CLN01 material retirement Task](tasks/tsk-0007-cln01-material-retirement.md)
- [Task 0006](tasks/tsk-0006-openbao-trust-bootstrap-and-recovery.md)
- [Task 0008](tasks/tsk-0008-llm-wiki-preparation.md)
