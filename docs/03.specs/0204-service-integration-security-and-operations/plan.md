---
title: "Service Integration, Security, and Operations Plan"
version: "1.12.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-01"
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
  planning and LAB operations outside the 2026-10-12 source-relocation amendment
  are excluded. Source and this request's
  branch/PR/merge are authorized without repeated approval.

### Current execution routing — 2026-10-10

SPEC-0212-TSK-0003 owns the P00 baseline and documentation amendment; existing
SPEC-0204 Tasks retain their historical evidence. P03 owns port/endpoints,
P04 Airflow native integration, P05 n8n native import/execution and P01/P02/P06
secret classification/mapping/consumption under this package's acceptance.
SPEC-0213/0214/0218/0219/0220/0223/0224/0227 retain their delivered source;
no old prompt label creates duplicate work. Learning apps, including planning,
are out-of-scope. LAB runtime operations remain outside the source-relocation
amendment below. P08 may separately move typed LAB
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
LAB documents to their Stage05 family `labs/` destinations with required folder
and parent README navigation, Registry links and path checks. Existing merged
LAB service/source relocation is out of scope for future units and is neither
revalidated nor reversed; this documentation exception does not move live data
or secrets or start/stop a LAB resource.

The 2026-10-12 user clarification accepts the delivered SMTP01/CLN01 changes.
Actual LAB GoTrue SMTP connection configuration, activation and sending are
outside W24 and W26–W30; missing LAB readiness is not their completion gate.
Retain canonical source/wrapper and isolated fixture evidence without claiming
a fresh native result. A genuine later send uses the operator-supplied
designated sender/recipient mailbox in the bounded ROOT or P05 lane. This
clarification selects that mailbox but does not dispatch a message, provision
a LAB account or start a LAB service. Remaining ROOT/P05 operational receipts
and independently scoped material checks keep their existing owners.

### Current security-warning and delivery continuation — 2026-10-12

Use the existing latest-version and security gates plus independent ROOT include
authority; do not add a new gate, API, scanner or optional bypass. A root-image
version change or scanner correction is permitted only for an actual confirmed
current-image security warning. A successful current stable-channel lookup with
no newer release requires no version bump; absent/stale evidence remains
UNKNOWN. Existing feature/native/recovery Tasks retain exact scopes;
user-accepted SMTP01/CLN01 and completed P09 stay accepted. Version/source
acceptance is distinct from deployed-service acceptance. Each future delivery
uses the owning-Spec PR, exact-head CI and independent review before merge.

## Scope

The work units cover shared-service compatibility and integration,
OpenBao maintenance and secret catalog/migration interfaces, SMTP, independent
Airflow/n8n opsflow jobs, common endpoint contracts and the named recovery
slice. Offline Wiki preparation and typed Stage 05 document moves keep their
separate boundaries; missing consumer or operational targets do not authorize
provisioning, LAB runtime or learning-application work.

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
| W20 | 4, 11 | TLS listener/Agent/metrics/Traefik, protected root ceremony, restricted issuance/revocation and wrapped reissue/readiness; RUN-0105 owns maintenance and RUN-0021 links to it | W19 | TSK-0006 | RED/GREEN failure, argv/redaction, authenticated recovery access and endpoint tests |
| W21 | 7, 11 | Declarative HMAC audit, capacity/failure alerts, protected bounded snapshot and host rotation; reuse existing backup ownership | W20 | TSK-0006 | Exact image isolated audit and snapshot recovery cases; atomic artifact and native rotation evidence |
| W22 | 8, 11 | Changed QA, independent IaC/security/code review, scoped commits/PR | W21 | TSK-0006 | Registered local/hosted candidate checks and actual delivery receipt |
| W23 | 11 | HOME cold boot, independent custody and selected real backup recovery | W22 | TSK-0006 | NOT_RUN until external facts, fixed runtime/cleanup proof and concrete boundary exist; HOME/P06 held |
| W24 | 12 | Assess consumers and implement the narrow private-unlink helper for material retired by another owner after SMTP01 evidence | W19 | TSK-0007 | Helper unit tests and document gates; private apply only after Task preflight |
| W25 | 13 | Prepare bounded LLM Wiki contracts, synthetic fixtures and future acceptance without provisioning | None | TSK-0008 | Frozen preparation QA: 35 PASS, 99-percent coverage; registration integrated. Historical candidate CI failure retained in Task 0008; current local-main source gates/review support delivery, resource changes 0 |
| W26 | 14 | SMTP01 baseline, consumer/source map and failing regressions | None | TSK-0005 | Source SHA and RED command receipts |
| W27 | 14 | Canonical root source and Supabase SMTP-only wrapper/target alias | W26 | TSK-0005 | Unit and synthetic selected Compose model |
| W28 | 14 | COMM-002 ownership, COMM-003 tombstone and guarded retirement helper | W27 | TSK-0005 | Equal/mismatch/idempotency/race/privacy tests; no HOME mutation |
| W29 | 14 | Exact-image synthetic SMTP authentication, capture and failure cases | W27 | TSK-0005 | Opt-in isolated native rehearsal, separate from HOME |
| W30 | 8, 14 | Current-source checks, independent review and coordinator handoff | W28, W29 | TSK-0005 | Preserve logical commits; reviewed local-main delivery under the superseding user instruction; user-accepted delivered SMTP01/CLN01 scope; LAB GoTrue connection/activation excluded; any separately scoped ROOT/P05 operational receipt remains distinct |
| W31 | 15 | Integrate SEC01 stable/security ledger, source receipts and bounded repairs; continue exact operational validation | None | TSK-0009 | Source/common repairs, isolated datastore and current local leaf receipts integrated. Current ROOT stable-version and reviewed security evidence; successful no-newer lookup needs no bump; HOME/recovery retain exact owner prerequisites; unknown evidence is not a clean PASS |
| W32 | 16, 8 | P02 single value-free catalog, classification, generated views and reissuance guards | W27, W28 | TSK-0010 | Existing source/schema reuse, alias and privacy RED/GREEN, scoped changed/staged checks and independent review; real migration/recovery are separate lanes |
| W33 | 1, 4, 6, 8, 17 | P03 current service/endpoint/environment, opt-in dedicated broker observer identities with minimal ACLs, and four-location port contracts; independent source preparation before consumer-specific runtime acceptance | W27, W28 | TSK-0011 | Existing inventory/tool reuse, synthetic RED/GREEN, privacy and DEV/MNG independence; final mappings and native/HOME checks follow their exact owning prerequisites |
| W34 | 1, 8, 18 | P04 baseline, source reuse, exclusive ownership and RED cases | None | TSK-0012 | Current SHA/consumer ledger; reference audit is not native acceptance |
| W35 | 18 | Strict manifest/parser/adapters, immutable inputs and byte-derived idempotency | W34 | TSK-0012 | RED/GREEN validation, privacy, replay and object/DB failure tests |
| W36 | 18 | Versioned DEV role/schema/publication/outbox contract; freeze the P05 interface | W35 | TSK-0012 | Reuse provisioning guards; migration/SQL security review and executable denial cases |
| W37 | 18 | Zero-I/O DAG parsing, compatible image and worker-only Compose proposal | W34, W35 | TSK-0012 | Exact-image import and rendered model; coordinator integrates shared hunks |
| W38 | 18 | Isolated then selected DEV/S3/Celery execution, concurrency/backfill and empty restoration | W36, W37 | TSK-0012 | Relevant image acceptance and exact resource/recovery boundary; no full-SEC or P06 global dependency |
| W39 | 8, 18 | Registered gates, independent review, logical commits, owning-Spec PR and handoffs | W38 | TSK-0012 | Current-head checks/review; preserve unexecuted lanes and actual delivery receipt |
| W40 | 1, 8, 19 | P05 baseline, source/reference reuse, exact writer ledger and RED cases | None | TSK-0013 | Fresh Git and public metadata; reference static results are not native proof |
| W41 | 19 | Deterministic inactive workflow and bounded SMTP implementation with synthetic privacy/state tests | W40 | TSK-0013 | Closed inputs, graph/credential placeholders, Message-ID and checked ack/retry; no import side effects |
| W42 | 22 | Consume and freeze P04's reviewed SQL/outbox version and interface hash | W41, W36 | TSK-0013 | P04 owns SQL; publication/view/claim/ack/retry/state/lease and least-privilege contract |
| W43 | 22 | Exact-image inactive native import, credential binding and manual queue-worker Mailpit capture | W42, W38 | TSK-0013 | Relevant image/node/security receipt plus exact DEV/mail target, network, credential and recovery review |
| W44 | 22 | One-minute polling, concurrency/failures/dead/requeue, restart/rotation and empty restoration | W43 | TSK-0013 | Actual captured acceptance, duplicate uncertainty, stale-token denial and paired metadata/key recovery |
| W45 | 8, 22 | Shared registration/docs integration, final QA/review, logical commits and owning-Spec PR | W44 | TSK-0013 | Current-head required checks/review, actual merge and versioned downstream handoffs |
| W46 | 1, 8, 20 | P06 baseline, existing authority and exact consumer/ownership ledger; RED cases | None | TSK-0014 | Fresh SHA/clean state and prompt audit; no private value I/O |
| W47 | 20 | Closed value-free wave/receipt schemas and catalog-bound selection tests | W46 | TSK-0014 | Synthetic rejection of aliases, unknown IDs, unsafe paths, destinations and classifications |
| W48 | 20 | Bounded same-byte KV-v2 copy executor/CLI and failure reconciliation | W47, W32 | TSK-0014 | Reuse integrated P02 API; CAS=0, equal/conflict/ambiguous-readback, TLS/privacy and file safety tests |
| W49 | 20 | Reuse P01 renderer and freeze actual delivery/readiness contract | W48, W20, W33 | TSK-0014 | Exact version, UID/GID/mode, inode/reload, LKG/TTL, auth/freshness denials; shared proposals only |
| W50 | 20 | First real existing opsflow DEV ingest/S3 copy-render-consume pilot | W49, W23, W38 | TSK-0014 | Selected SEC artifact acceptance, actual catalog IDs/destinations and named native canary/recovery boundary |
| W51 | 20 | Pilot rollback, independent snapshot/empty restore and consumer reauthentication; authority transition | W50 | TSK-0014 | Actual recovery plus integrated generator guards; byte preservation and failure stop |
| W52 | 20 | Sequential additional selected consumer waves | W51 | TSK-0014 | Per-consumer evidence, exact writer and recovery; no global bulk import |
| W53 | 12, 20 | Remove accepted waves' obsolete plaintext/private rows/temp copies through owning executors | W51 | TSK-0014 | Fresh source/runtime/job/backup/external proof and recoverable boundary; SMTP retains COMM-003 execution |
| W54 | 20 | Separate selected provider/server credential rotation | W51 | TSK-0014 | Old-credential denial, session/pool/native-copy refresh and tested rollback; preserve stable/bootstrap material |
| W55 | 8, 20 | Registered current-head gates, independent review, owning-Spec PR and downstream handoffs | W52, W53, W54 | TSK-0014 | Preserve logical commits and actual versus NOT_RUN lanes; source delivery does not close criterion20 |
| W56 | 8 | Admit P08 ownership and audit existing move/discovery tooling and exact source inputs | None | TSK-0015 | Main/worktree observation; reuse and writer map |
| W57 | 8 | Read every tracked operations document and review exact semantic move map and populated README coverage | W56 | TSK-0015 | Per-document ID/type/body/link/LAB classification; collision checks |
| W58 | 8 | Test and integrate nested path/profile/discovery/catalog/link/changed-CI contracts before rename | W57 | TSK-0015 | RED/GREEN boundary fixtures; scoped source/security review |
| W59 | 8 | Freeze feature-owner leases and preservation/rollback proofs for exact move inputs | W57, W58 | TSK-0015 | Source SHA256, anchors, command/evidence and inverse mapping |
| W60 | 8 | Apply exact reviewed document renames and coupled references under one writer | W59 | TSK-0015 | One active document location; semantic preservation; no running-resource, secret-value or persisted-data changes |
| W61 | 8 | Complete Korean READMEs for populated domains and parent families | W60 | TSK-0015 | Actual descriptions, direct-child navigation and metadata selection |
| W62 | 8 | Validate document paths, links, bindings, lifecycle and delivery; hand new paths back to owners | W61 | TSK-0015 | Exact-head gates, independent review, logical commits and hash-bound document handoff |
| W63 | 1, 8, 21 | Issue P10, freeze current source/owner receipts and audit existing acceptance tools | None | TSK-0016 | Actual local/remote refs and public dependency evidence; no duplicate inventory |
| W64 | 21 | Prepare synthetic vertical-slice cases and evidence-bound integration tests | W63 | TSK-0016 | Reuse P04/P05 contracts; scoped RED/GREEN before behavior changes |
| W65 | 10, 21 | Run relevant exact-image isolated input/publication/outbox/capture/replay chain | W64 | TSK-0016 | P04 publication proof precedes P05 native claim/ack; exact relevant contracts and bounded resources |
| W66 | 21 | Selected HOME rollout and consumer authorization/readiness verification | W65 | TSK-0016 | Named host, accepted relevant images, connection/credential/backup/recovery facts and exclusive runtime lease |
| W67 | 7, 11, 12, 14, 20, 21 | Reconcile bounded failures and verify complete backup set and empty-target restoration | W65 | TSK-0016 | Isolated faults use synthetic targets; HOME recovery requires W66 facts; feature owners retain migration/deletion/rotation/recovery execution |
| W68 | 8, 21 | Consume final P08 paths and revalidate manual working directories and README coverage | W62 | TSK-0016 | Final path/hash handoff and actual dry-run receipts; no concurrent moves |
| W69 | 8, 21 | Final requirement 11–30 report, required checks/review and owning-Spec delivery | W66, W67, W68 | TSK-0016 | Actual evidence from all relevant owners; no duplicated test counts or inferred runtime PASS |
| W70 | 8 | Keep existing merged LAB service/source relocation out of this request; limit P08 to typed Stage05 LAB-document moves, README and path contracts | W56 | TSK-0015 | Exact writer path/hash handoff, profile/link/navigation checks; no LAB runtime, service-source, image, secret or data change |
| W71 | 2 | Prepare one compatible n8n stable source bundle | None | TSK-0017 | Exact pins, locked package, compile/tests; native separately |
| W72 | 18 | Reject cross-database CONNECT before workload login | None | TSK-0018 | Shared provision guard, operator bootstrap, isolated native denials/restore |
| W73 | 19 | Quarantine ambiguous sends and reject expired SMTP leases | W72 | TSK-0018 | Versioned SQL004, closed consumer contract, deadline and native quarantine tests |
| W74 | 19 | Execute the existing n8n notifier through an actual isolated queue worker, external runner and SMTP capture, then perform serial empty restoration | W73 | TSK-0019 | Exact reviewed images, terminal execution and Code-node proof, capture/unknown/reconciliation/no-resend and separate metadata/DEV restore; no accepted-response-loss or HOME claim |
| W75 | 18 | Execute existing Airflow manifest DAG through actual isolated Celery publication, retry, replay and serial empty restoration | None | TSK-0020 | Exact cached-image driver/UID preflight, terminal DagRun/task/Celery identity, real S3 readback and separate DEV/metadata PG18.6 restore |
| W76 | 15 | Adopt the fixed Traefik v3.7.16 and Prometheus v3.15.1 image pins, supersede the lapsed SEC01 acceptances in POL-0013 and POL-0045, and record the owner pull, scan, config-check, HOME recreation and rollback steps | None | TSK-0021 | Registry digests and latest releases verified, pins, tech-stack projection and ledger refreshed; pull, scan, boot, recreation and rollback `NOT_RUN` |
| W79 | 23 | Freeze runtime/source inventory, duplicate-workflow and validator dependencies | None | TSK-0022 | Redacted identities, roots, digests and owner exclusions |
| W80 | 23 | Implement narrow discovery, lossless snapshots and private local Outbox | W79 | TSK-0022 | RED/GREEN replay, restart, multiple ideas, paths/hashes, conflict and permissions |
| W81 | 23 | Implement adapter-independent delivery and reconciliation | W80 | TSK-0022 | Fake adapters prove bounded retry, response loss, strict durable receipt and request binding |
| W82 | 23 | Prepare bounded generic transport; adopt exact Gateway fixtures and inactive n8n forwarding | W81 | TSK-0022 | Fixed PR620 dev contract/fixture pinned and source reviewed; actual conversion BLOCKED on article collection time; Native operation NOT_RUN |
| W83 | 8, 23 | Document recovery/metrics/MCP, independently review and admit approved Native checks | W80-W82 | TSK-0022 | Source/synthetic and actual worker-to-Gateway evidence separated |

### P10 staged admission and acceptance ownership

TSK-0016 is issued from local main
`43917df47f94f0ddd7e1dbbf7bb7cc87701a56c8`; actual remote main and origin/main
are `c26c3b93f4e73034ddad4d08ba9da8eaa9fec0c7` at assessment. GitHub has no
open PR at that observation. The two local P08 commits are not remote delivery.
The worker uses `codex/p10-opsflow-acceptance` and its independent worktree from
this reviewed issuance. No new Spec is allocated, and dev remains excluded.

W63/W64 may start now: current public receipt inventory, acceptance scenarios,
synthetic fixtures and one dedicated integration test. The sole worker owns
Task16, `tests/validation/test_opsflow_e2e_acceptance.py` and the public
`tests/fixtures/opsflow-acceptance/{README.md,manifest.valid.json,cases.json}`.
A new helper requires a proven reuse gap and an explicit file lease. Parent
fixture navigation, manifest/workflow/Registry, Compose/environment/gateway/
Alloy/backup/catalog and Stage05 indexes remain coordinator-written proposals.
P04 retains SQL/DAG/adapter ownership; P05 retains workflow/node ownership;
P01 retains issuer/renderer/custody, P02 catalog, P03 connection contracts,
P06 migration, P07 controls and P08 document moves. P10 proposes owner fixes.

W65 is admitted per selected consumer: exact accepted image/package/UID/TLS
contract, frozen P04 SQL/outbox interface, least-privilege functions/object
policy and a reviewed unique synthetic Docker project/network/volume/port/
resource/cleanup boundary. P04 publication precedes P05 native notification.
Full SEC01/P01/P06 completion is not a blanket prerequisite for a bounded
pre-migration isolated or DEV consumer; an unresolved relevant fact blocks
that lane only. OpenBao/P06 acceptance still requires its owning prerequisites.

W66 and actual W67 recovery wait for the named host/context, exclusive runtime
lease, accepted relevant images, backup contents and exact snapshot identifier,
independent custody and empty restore target. SMTP01 is COMM-003's sole
proposed unlink executor after CLN01's fresh assessment; P10 never duplicates
it. Actual restore, migration, deletion and rotation executors stay with their
feature owners unless an exact runtime lease is transferred; P10 owns bounded
acceptance faults/reconciliation and receipt collection. Current private cutover/deletion/restore and global SEC01 acceptance remain
unverified. W68 waits for final P08 W62 paths and hashes; typed LAB document
moves belong under `docs/05.operations/{guides,policies,runbooks}/labs/`.

Preserve logical source/test, public contract, actual native receipt and final
acceptance commits. Run current registered changed/staged gates and independent
code/security/recovery review on their exact inputs before the owning-Spec PR,
exact-head CI and merge. Never infer remote CI.
Rollback of issuance reverts only these three owned documents; future runtime
rollback needs its reviewed data-aware recovery contract. No private value,
service, DB, object, credential, schedule or document path changes on issuance.

### P08 single-writer continuation

TSK-0015 owns W56–W62 under criterion 8 and SPEC-0212 requirement 25; completed
0212/P00 and 0227 records remain unchanged. Initial branch
`codex/p08-operations-document-layout` starts at observed main
`4c83f14b11a77e13e582eb85d0bf256685472a95`. The separate source candidate's
ongoing gates are not a PASS or P08 baseline; adopt its reviewed final main SHA
only after delivery and re-read inputs before every move lease.

Initial public preparation owns only the Task and, if semantic reuse analysis
establishes the gap, `scripts/lib/document_governance/operations_moves.py`,
dedicated unit tests and public operations-moves fixtures with family READMEs.
Registry/schema/discovery/profile/heading, operations catalog/Guide binding,
manifest/workflow/CI and indexes remain coordinator proposals until the exact
writer lease transfers. Actual edits and moves wait for fixed feature-owner
SHAs; old/new paths never have concurrent independent writers.

Classify actual artifact IDs and bodies, including distinct subjects sharing
one number across families. LAB destinations are exactly
`docs/05.operations/{guides,policies,runbooks}/labs/`, never root `labs/`.
Retain correctly arranged documents; ambiguities remain review-required rather
than being assigned to common. Corpus counts are observations, not constants.

Existing LAB service/source relocation is historical merged source and is
NO_CHANGE for this request. P08's remaining future unit is limited to typed
Stage05 LAB-document destinations, README navigation and path contracts.
Preserve shared common controls and live initialization/recovery inputs under
their real owner. Root includes exclude independent LAB projects; their
project/profile/network/dependency/data-path closure is validated with public
inputs. The existing LAB controller remains the sole runtime entrypoint owner.

One writer reconciles relative paths, root/LAB includes, catalog/support metadata,
environment examples, generators, validators and current navigation. Prior
source/runtime receipts remain bound to their old inputs. Moving a definition
does not prove that a running container, data directory or secret has moved.
Restore/activation retains a separate reviewed operational boundary. Record
canonical commands, input SHA, results and recovery rationale before removing
invocation-only tests/scripts/scratch during final development-worktree cleanup.

Use reversible logical units: path contracts/tests, coupled exact renames and
references, populated README content, then final validation/hash handoff. Every
unit preserves identity uniqueness and active links; no duplicate active copy
or indefinite mixed-path waiver. Reuse completed body refresh. Rollback is the
reviewed inverse exact rename/link/README/source-contract mapping and its
consumer checks, without runtime/secret/data operations or foreign reset/clean.

Final checks cover metadata selection of new READMEs, ID/profile/language/body/
lifecycle, active links/anchors, command working directories, catalog/service
bindings, changed-CI regressions and staged changes. Record failures and input
SHAs; future delivery needs an owning-Spec PR, exact-head CI and independent
review before merge. No native or operational acceptance follows from a move.

### P06 parallel preparation and per-consumer admission

TSK-0014 is issued against local main
`f7543e0697e2473cbbbeb254792e7a1d5b4b8423`; remote main is
`4e26a5a8022a7307c7461af60337442912955df1` at assessment. Neither fresh
remote CI success nor merged SMTP source is a real migration receipt. No
new Spec is created. One worker uses `codex/p06-openbao-consumer-migration`
and its separate worktree from the issuance commit. The Task fixes exact
new-file ownership, provenance, tests and native admission facts.

W46/W47 public schemas, provisional synthetic contracts, RED cases and
integration proposals may start immediately. W48 production binding reuses
the reviewed P02 catalog API after source integration; it does not copy the
reference classifier, table parser or catalog views. P01 remains the sole
issuer/renderer/journal/config and subject0085 writer. P04 owns opsflow SQL,
roles, adapters and DAGs; P05 owns notifier/native credential copies. P06
proposes their required changes and never creates duplicate authorities.

P01 has new source/diagnostic commits but remains blocked on current native,
HOME, restricted snapshot and independent custody/restore evidence. P02 has
committed source plus an uncommitted lifecycle/lock follow-up; the new ignored
lock-inheritance proposal reports synthetic PASS and independent review but
is not integrated generator acceptance. Its catalog has no opsflow entry or
approved KV destination. P03 source contracts and P04/P05 drafts do not prove
actual delivery or operational consumers. Preserve all these writers' changes.

W50 waits for the exact selected OpenBao artifact's SEC acceptance, P01 W23
authentication/recovery evidence, approved P02 opsflow IDs/paths/ACL/delivery,
P03 endpoint/UID/mode/reload facts and P04 W38's actual DEV/S3 consumer.
Full unrelated-image or P05 acceptance is not a global first-pilot gate.
The P04 restricted-file DEV lane can precede P06, avoiding a circular gate.
W51 authority changes and W53 removal additionally wait for coherent shared
generator guards, restored-key/consumer reconciliation and per-wave recovery.
W52 expands only the selected accepted consumer set, never all catalog rows.
W53 follows W52's evidence for each additional selected wave. W54 rotation
has its own exact target, owner, old-credential denial and rollback receipt;
same-value KV copy is not server rotation. Missing targets remain NOT_RUN.

Root/leaf Compose, environment, gateway, backup, Registry, indexes, generator
integration, Script Manifest and workflow registration have one coordinator
writer; P02/P01/P03 retain their owned contracts. COMM-003 has one SMTP
executor, CLN owns deletion eligibility and PG-020 stays retained for recovery.
Final source-only delivery may precede the blocked operational units with
criterion20 open. The P06-only owning-Spec PR requires integrated dependencies,
current-head registered checks and independent code/security/IaC/docs review;
do not push unrelated unpublished main commits as a P06 change. Task0014
records each downstream contract and exact final SHA.

### P05 parallel preparation and single SQL owner

TSK-0013 starts from assessed clean local main
`4e26a5a8022a7307c7461af60337442912955df1`. Remote main initially returned
`6da5e3bf380d5002e0e28181136fde8c016e49ce`, then advanced externally to
the same 4e26a5a80 with successful CI Quality Gates and no open PRs. P04 was
initially clean, then began its workload and dedicated tests; no frozen SQL
handoff or native producer acceptance was received. Use `codex/p05-n8n-outbox-notifier` and
`.worktrees/p05-n8n-outbox-notifier` from the reviewed issuance commit. No second
implementation chat or operational resource is created by issuance.

W40/W41 may proceed on explicitly provisional interface fixtures. W42 waits
for P04 W36's reviewed SQL version/hash. P04 remains the only canonical SQL
and provisioning writer in `airflow/workloads/manifest-pipeline/sql`; P05 does
not copy the supplied DAG/SQL or create a second schema/provisioner. The prompt's
standalone provisioning fallback is routed through that existing writer; a
necessary reassignment requires a recorded exact handover, never concurrent
writing. P05 native W43 follows P04 W38's real publication/outbox proof.

Source selects n8n/core/runners2.42.6 and Mailpit1.31.4; read-only HOME metadata
still shows2.41.6 and1.31.2. SEC01 supplies the selected compatible immutable
images and security receipt, not a source-tag-only waiver. P03 supplies exact
DEV/Mailpit endpoints, worker execution/network and UID/mode boundaries; P02
reviews credential references. P05 uses only notifier credentials and encrypted
n8n execution copies; P01/P06 gate final OpenBao delivery, not all protected
DEV verification. No edition/native OpenBao support is assumed.

The stock EmailSend source lacks Message-ID and explicit transport-timeout
controls required by the P04 handoff. W41 may develop a narrow credential-aware
custom node inside its own workload with synthetic tests; runtime registration,
custom bind/image integration and dependency review remain coordinator/SEC01
proposals. Do not add unsupported options or enable unrestricted Code imports.
Current mail_net is shared with Stalwart and is not internal-only; network
attachment alone is not Mailpit-only acceptance. Review the dedicated capture
boundary with P03 and preserve existing unrelated networks and consumers.

Root/leaf Compose, public/private environment, both existing n8n Dockerfiles,
custom bind integration, existing README/subject0053 docs, backup, catalog,
Registry, inventory, manifest/workflow and shared tests remain single-writer
proposals. TSK-0013 fixes the exact new-file scope and evidence ladder. Preserve
other writers' dirty worktrees; no reset/stash/clean or dev branch is used.
The newer P05 prompt selects an owning-Spec PR after implementation, actual
latest-head CI and independent review. Reconcile the local preparation prefix
and P04 dependency with fresh remote main before a P05-only PR. This assessment
makes no remote write, workflow import, credential update or deployment.

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
assessment/hold. Integration must confirm that executor, resolve the currently failed cross-executor lock/order compatibility and
enforce receipt freshness before any private apply. The present user-integration
hold remains until the supervisor selects one route; no private execution is
authorized by either tool's source checks.

### Current safety and stable-source corrections — 2026-10-16

W71 belongs to Task0017 for n8n stable source preparation. W72 and W73 belong
to Task0018 for the reproduced DEV CONNECT and SMTP lease/quarantine defects.
These corrective units support existing criteria 2, 18 and 19 without changing
the durable acceptance owners or rewriting historical evidence. Each requires
its own logical commit, focused RED/GREEN, native evidence where executable,
changed/full gate routing, and independent review. HOME, live cluster ACLs,
real workflow activation and complete recovery remain separate blocked lanes.

### Hermes ingestion implementation plan — 2026-10-30

**Goal:** preserve Hermes execution/email and durably stage completed structured
exports for reliable authenticated n8n delivery. **Architecture:** a restricted
host Publisher reads approved files, invokes the reviewed external validator,
and stores immutable snapshots in SQLite; a separate adapter-independent state
machine accepts only Gateway durable-persistence receipts. **Tech stack:** Python
standard library, SQLite and existing Hermes/n8n. **Spec:** criterion 23 and the
Hermes transport contract. Existing Stage 03 ownership overrides the
writing-plans skill's default location. Execution uses subagent-driven-development.

#### Global constraints and ownership

TSK-0022 alone owns the new
`infra/07-workflow/n8n/workloads/hermes-blog-ingestion/` package. The staging
worker owns `publisher/{__init__,files,candidates,outbox,cli}.py` and staging tests;
the delivery worker owns `publisher/delivery.py` and delivery tests, consuming
the staging worker's actual interface handoff. The workflow writer owns only inactive `workflow.json`, `tests/test_workflow.py`,
workload READMEs and the workloads README link. Its initial stub was headerAuth
Webhook → StopAndError `GATEWAY_CONTRACT_NOT_BOUND`; the current source is a
contract-based inactive workflow. Native import and activation are not established.
The HTTP transport writer owns only `publisher/http_transport.py` and
`tests/test_http_transport.py`; the Task records its narrow source admission.
The Gateway adapter writer owns separate adapter source and its dedicated tests;
the n8n writer owns `workflow.json` and workflow-specific tests. Shared delivery
integration requires a serial handoff. Pin contract and fixture inputs to
Blog-data dev revision `a6d0957ad380f179f73bdd2a60ff23792d53f7ae`, as listed
in Task0022; verify retrieved content and digests before compatibility claims.
The doc-writer owns this
Spec/Plan, Task0022 and later implemented source-only RUN-0053 procedures.
The controller owns inventory, registered checks, independent review and final
evidence. Shared files require serial handoff and every worker preserves others'
changes. Exclude Task0013, Manifest Outbox Notifier, SPEC0247 source, other
worktrees, installed Cron, credentials and runtime resources from writes.

#### Review focus

- W80: parent symlinks/path escapes/source replacement fail without source logs.
- W80: same execution identity with changed bytes preserves first snapshots and
  conflict evidence, including multiple-idea references and hashes.
- W81: death after send or lost acknowledgement recovers uncertain, not pending.
- W81: unrelated or generic success receipts never mark durable delivery.
- W82-W83: unknown Gateway schema/authentication/TLS fails closed; fake outcomes
  cannot establish actual worker networking or Gateway persistence.

#### W79: input and ownership admission

- [ ] Record fresh remote main, HEAD, worktree and runtime inventory in Task0022.
- [ ] Bind the three approved job IDs, actual output/idea roots and run IDs.
- [ ] Bind the stronger SPEC0247 validator path/SHA; missing dependency blocks
  staging. Compare actual workflow identities with `hy-home.n8n` before adding
  workflow source; active exporter is reused without a new Cron.

#### W80: candidate staging and Outbox

- [ ] Write failing tests: one export, multiple ideas, exact replay, changed
  identity contents, missing/changed validator, path escape/symlink, hash drift,
  excluded private job, permissions, restart and original retention.
- [ ] Run workload unittest discovery and record RED in Task0022.
- [ ] Implement bounded approved-root reads, reviewed validator invocation,
  immutable snapshots, identity uniqueness and transactional conflict history
  in staging-owned files. CLI supports safe staging/status without secret use.
- [ ] Re-run the same tests GREEN and measure coverage. Hand off the actual
  Outbox record/transaction API to W81; never duplicate the candidate validator.

#### W81: delivery/reconciliation

- [ ] Write failing fake-adapter tests for durable receipt, response loss,
  proven-no-send retry, n8n/Gateway outage, timeout/auth/TLS rejection, restart,
  conflict and immutable prepared-request/destination binding.
- [ ] Record RED, implement the agreed Outbox consumer and bounded protocol,
  then run GREEN and the complete suite. Retain failed/uncertain evidence;
  reconciliation never replaces snapshots. Fake adapters are synthetic only.
  No live HTTP adapter, guessed endpoint, Gateway JSON or status enters this unit.

#### W82: exact Gateway and inactive n8n source

- [x] Implement and test bounded generic HTTP transport independently of a
  Gateway protocol, using isolated loopback tests and fake credentials only.
  Follow the exact HTTPS, TLS, redirect, ambiguity and reconciliation limits
  in Task0022; no CLI dispatch or runtime resource changes are included.
  The first experiment was removed after independent review found idle timeouts
  did not bound the complete request. Its replacement bounds DNS, TLS, request,
  headers and body after subprocess startup; input acquisition and subprocess
  creation are outside that deadline. Timeout kills and reaps the child and
  remains ambiguous. After a correction to pre-send connect failure classification,
  independent security re-review passed. The final suite reported 74 PASS and
  one optional validator SKIP out of 75, with Ruff check and format passing.
  A separately approved synthetic localhost HTTP/TLS run passed 11/11 on the
  final revision; the 93% measured coverage excludes its child subprocess.
  Fixed-validator focused tests passed 14/14. Private CA and live operational
  connectivity remain unverified.
- [x] Prepare and test the initial inactive authenticated fail-closed stub;
  this historical step does not establish Gateway compatibility.
- [ ] Retrieve and verify the Gateway API and fixture at the fixed Blog-data dev
  revision recorded in Task0022. Bind tests to its exact requests, authentication,
  idempotency/conflict, durable receipt and reconciliation semantics. Establish
  authoritative producer timestamp provenance before mapping required fields:
  `collected_at` is the actual Hermes article collection time, `generated_at`
  the execution finish and `scheduled_at` the exact execution `scheduled_instant`.
  Existing eight candidates and database records lack actual article collection
  time; actual conversion and delivery are blocked until that source exists.
- [ ] Implement the adapter and its tests independently from the inactive n8n
  workflow and its tests, then review their integration through explicit handoff.
  Source includes receipt/Outbox handling, pinned fixture and schema, content
  type, explicit offline replay and adapter/Outbox response loss. Synthetic
  adapter/replay tests passed 6/6; independent code and security reviews were
  performed. The inactive workflow uses a reserved domain, screens input and
  returns a fixed 400 on invalid input, stricter than the Gateway contract.
  Native import, Queue execution, credentials, TLS, actual logs and alerts, URL
  runner and runtime operation remain NOT_RUN. The 105-test full suite with one
  skip predates the final IF test change and does not prove that later revision.
  The latest source removes the URL global, delegates authority validation to
  the Gateway to retain valid IDN/IPv6, applies a stricter 24-hour prefilter,
  fixed fail-safe 400 IF branch and success MIME check. Empty-VM Node tests
  passed 13/13. Its URL preprocessing admits only a subset of Gateway-valid
  inputs. Independent final adapter, replay and workflow correctness/security
  reviews found no remaining Critical or Important findings. The replacement
  checkout's full suite passed 107 tests using the pinned validator and
  synthetic localhost tests; this is not Native or hosted acceptance.
- [ ] Test those exact fixtures RED/GREEN, then prepare versioned inactive n8n
  source: authenticated event, schema and file/report identity checks, Gateway
  request, durable receipt validation, state recording and bounded error alerting.
  Never record real credential IDs/values in workflow JSON.
- [ ] Preserve the existing PR and prepare the user-selected replacement PR to
  address the candidate failure caused by a malformed merge commit message.
  The replacement branch integrates `6a` without rewriting existing history;
  its draft PR is not yet published. Run applicable hosted checks on it.
- [ ] Review existing network/overlay policy before restricted host transport
  or non-root container membership in `n8n_net`. No new public path or port;
  any later Compose source gets scoped validation and independent review.

#### W83: docs, review and Native admission

- [x] Realign the Publisher validator pin from the pre-merge draft to the
  main-tracked validator bytes after diff, corpus and independent review; add
  Companion Evidence v1 structural verification and the bounded `dispatch`
  entry point over existing delivery components. All three Hermes jobs stay
  fail-closed until a producer trust anchor is admitted (TSK-0022, 2026-10-31).
- [x] Decide one producer authentication design (restricted account, Ed25519
  detached signature over Companion v1, tracked public key store with job scope,
  validity and retroactive revocation), implement `trust.authorize` as the single
  decision for dispatch, processing, request binding and replay, align timeouts
  and record the producer contract cross-check. The tracked key store stays empty
  until a real producer key is reviewed (TSK-0022, 2026-10-31).
- [x] Close the protected-install gap: declare and hash-lock `cryptography`,
  install one immutable root-owned release per commit, require root ownership
  without group/other write for interpreter, import paths, loaded modules and
  key store, add `verify-install` and a separate-account container check, count
  rejections by value-free reason, correct the Traefik timeout meaning and record
  the ingest-only server-B contract. Server-A account, install and service stay
  separate approval units (TSK-0022, 2026-10-31).
- [x] Redirect to the Hermes host direct path: point the inactive workflow at
  the production webhook path and the internal Gateway, host the Blog-data
  Gateway on server A as an opt-in pinned service on an internal isolated
  network shared only with `n8n-worker`, propose the exact-path Traefik router
  outside the live directory, and prove host → Traefik → native n8n → Gateway →
  SQLite in a disposable E2E. Export/ACK stays blocked on Blog-data; every
  deployment step stays a separate approval unit (TSK-0022, 2026-10-31).
- [x] Connect attestation and Resource Export: pin the Gateway to Blog-data
  `dev` with Resource Export, add a Traefik-only isolated export network,
  propose exact-path export and attestation routes, add a separately run
  `attest` command that signs only producer-verified requests, and prove
  attestation → ready export → pull → ACK, the schema-3 upgrade and backup
  restore in disposable E2Es. Production signer, Windows receiver and every
  deployment step stay separate approval units (TSK-0022, 2026-11-01).

- [ ] Update Korean workload README and existing RUN-0053 only with implemented
  safe commands and recovery/uncertainty limits. Record metrics design for
  success/failure, pending/uncertain, retries and oldest pending age without
  source, credentials or report-ID labels; reuse Grafana/Prometheus ownership.
- [ ] Design later read-only n8n MCP Server Trigger tools
  `list_review_candidates`, `get_ingestion_status` and `get_ingestion_summary`
  over Gateway `GET /v1/candidates`, `GET /v1/ingestions/{id}` and
  `GET /v1/summary` on a separate read path and token, never server A's
  ingest-only token. The Gateway has no full-text search, so the earlier
  `search_collected_news`/`search_business_ideas` names are withdrawn rather
  than implied. HTTP delivery stability precedes implementation; verify the
  actual client, authentication and Queue-mode connections first. Exclude
  project management, arbitrary HTTP, capture/review/delete and GitHub writes.
  Never change Blog-data MCP or treat retrieval as Vault-change/publication
  approval.
- [ ] Run measured source tests, required documentation/static checks,
  `git diff --check` and independent review. Logical local commits follow
  repository gates; remote Git remains excluded by the current request.
- [ ] Admit operational checks only after the separately approved server-A
  Gateway image, paths, start, credentials, workflow publication and Traefik
  route (RUN-0053), measuring the host source address first. Probe the
  worker-to-Gateway path from the actual n8n worker. Approve
  bounded outage/response-loss/replay and email/workflow regressions separately;
  never interrupt shared services just to simulate a fault. Keep all unexecuted
  lanes visible and criterion 23 pending.

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

## Risks and Recovery

### Risks and Rollback

#### Risk and Rollback

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

- [Hermes transport Task](tasks/tsk-0022-hermes-blog-ingestion.md)

- [W74 n8n native notification Task](tasks/tsk-0019-n8n-native-notification.md)
- [W76 Traefik and Prometheus fixed image pins Task](tasks/tsk-0021-traefik-prometheus-fixed-image-pins.md)
- [W75 Airflow native publication Task](tasks/tsk-0020-airflow-native-publication.md)
- [P10 opsflow acceptance Task](tasks/tsk-0016-p10-opsflow-acceptance.md)

- [P08 operations-document layout Task](tasks/tsk-0015-p08-operations-document-layout.md)

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
