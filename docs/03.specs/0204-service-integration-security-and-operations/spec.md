---
title: "Service Integration, Security, and Operations Specification"
version: "1.9.2"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-31"
layer: "specs"
artifact_id: "SPEC-0204"
parent_ids:
- "REQ-0027"
- "AD-0031"
- "ADR-0046"
created: "2026-10-03"
---

# Service Integration, Security, and Operations Specification

## Overview

This package owns confirmed shared-service compatibility/security gaps and the
infrastructure side of external-project connection, signals and recovery.
Its 2026-10-03 implementation and PR358 activation are historical provenance;
current execution follows the 2026-10-10 request reconciled by SPEC-0212 P00 at
`d19fbfde605e257299aa2b39e25f2d7413a78221`. Re-read main and the worktree
before each unit. Existing delivery and runtime receipts remain in their Tasks.

Current owners are SPEC-0213 for development data/Influx retirement,
SPEC-0214 for quality/OTLP, SPEC-0218 for common controls,
SPEC-0219 for Storybook, SPEC-0220 for crawler egress,
SPEC-0223 for RedisInsight, SPEC-0224 for datastore observation and
SPEC-0227 for the Stage 05 body refresh. Applied source is NO_CHANGE;
old prompt numbers and draft labels never authorize reimplementation.
P03 routes endpoint/port integration, P04 Airflow, P05 n8n, P01/P02/P06
secret classification/mapping/consumption, P09 offline Wiki preparation and P10 the
named user vertical slice. Each residual stays with one existing acceptance
owner; the new stage labels do not reserve Spec IDs.

The direct 2026-10-16 request reopens ROOT latest-stable and security assessment
under the existing SEC01 authority. Task0017 prepares the newly confirmed n8n
source bundle; Task0018 corrects reproduced database CONNECT and ambiguous-send
lease/quarantine defects. These continuations supersede earlier blanket version
NO_CHANGE and security-warning-only restrictions for their current scope, while
preserving prior source, acceptance decisions and historical Task receipts.
They do not authorize HOME deployment, live ACL/data migration, secret use or
production recovery without the separate concrete target and recovery boundary.

### Technical Approach

Use four serial Tasks: confirmed compatibility/security corrections; an
external-project integration contract and bounded discovery; backup and
cross-tier operations; then whole-tree secret path and environment parity.
TSK-0004 records the user's subsequent explicit 2026-10-03 authorization,
including value-preserving path moves and incident disposition. Each Task owns exact files and focused regressions in
its Task ledger before source mutation. Shared root, Alloy, environment,
Registry and backup files have one writer at a time. If a named project or
consumer is missing, record a versioned contract and `BLOCKED` runtime result
instead of provisioning resources. P00 changes no HOME service or real data.
Follow-on native, host, credential, migration and recovery actions proceed only
when their concrete target, effects, validation and recovery boundary are
established in the owning Task. A historical source-only slice does not stop
other authorized work or require repeated delivery approval.

The approved maintenance slice reuses TSK-0001 for criterion 8. It removes the
completed SPEC-0153 migration-only gate after transferring the continuing
lifecycle topology to the current contract, hook, and corpus owners. General
archive preservation, current retired-authority guards, frozen bodies, and the
bounded npm acceptance remain under their existing owners. This maintenance
does not authorize archive disposition or change the package's blocked runtime
status.
The public metadata regression fixture uses coherent Git-baseline packages and
does not mix unrelated current-owner Tasks from a later live worktree.
A separately approved tenth path may correct only the timeout fixture's source
terminal-state stub before one final public revalidation.

W7's removal of hosted public validation was a historical maintenance slice,
preserved in the existing Task and Git history. Current CI responsibility comes
from the quality policy and `.github/workflow-contract.yml`: the remote PR
candidate owns aggregate changed QA, while main security is separate. Follow
actual remote checks and independent review for remote delivery; do not copy
W7's old CI disposition into current execution. For remaining future units,
the current request selects an owning-Spec PR after exact-head CI and
independent review; delivery is recorded only after that PR is merged. Preserve
logical commits, run the required local checks, and retain historical hosted
failures without relabeling them. SPEC-0221 already owns the request
precedence policy, hooks and validator. Change an enforcer with its regression
only when a current conflict is found; otherwise record NO_CHANGE.

### Interfaces and Data

- Input: reviewed current declarations, official release/security references,
  named service consumers, approved project metadata and secret **reference
  names**, and a Task-specific execution target.
- Output: matched source declarations, restricted integration metadata,
  contract fixtures, updated Korean READMEs and Stage 05 guide/policy/runbook
  owners, and Task evidence. Values of secrets and raw operational data are
  never outputs.
- P09 preparation input/output: a future Project-Template-derived repository
  may later supply app Compose, business API/UI, migrations, collectors,
  workflow definitions, fixtures and E2E. P09 now produces only preparation
  contracts, synthetic fixtures and acceptance criteria. It creates no app,
  runtime resource, credential, workspace or blog-data write. Infra retains
  approved-engine, ingress/identity, telemetry and backup interface ownership;
  a manifest records planned scopes and owners but cannot provision or deploy.
  TSK-0008 records received schema, fixture and synthetic-helper source
  evidence separately from the coordinator-owned registration and final
  delivery gates. Replacement frozen source QA passed 35 tests with 99-percent
  coverage after Qdrant role-order parity correction; latest-head CI, review
  and delivery remain pending gates. It changes no operational resource.

### Open Questions

A real external project must identify its project ID, endpoint topology,
OIDC/S3/search scopes, operator and recovery boundary before a live connection
can pass. P04 needs its actual native Airflow DAG/DEV/S3 target; P05 needs
its actual n8n native import/execution target. P03/TSK-0011 owns the four-location
port contract and port_inventory.py preparation after the existing inventory/tool
reuse check. Their absence at assessment is not authority to duplicate the current
service inventory. Secret metadata, migration eligibility, reference
wiring, real consumption, rotation and recovery are separate completion states.
HOME PITR/offsite recovery and owner-held snapshot credentials remain with
their existing Tasks; historical isolated PASS is not a fresh HOME receipt.

### Operational Impact

Future source changes may alter native workflow execution, crawler rejection,
secret consumption and backup scheduling when deployed. The exact executing
stage binds target, impact and recovery before acting. P00 performs no such
runtime change; authorized delivery is independent of those unexecuted lanes.

## Scope

### Boundaries and Inputs

Use the current root include graph, service Compose/Dockerfiles/entrypoints,
tracked configuration and key-only environment contracts, current Stage 01/02/03
and Stage 05 owners, and official vendor documentation at implementation time.
SPEC-0201 supplies the source inventory and exclusive-writer handoff. SPEC-0202
supplies the dev-pg/dev-valkey source contract, synthetic restore result, and
operational exclusions. SPEC-0203 supplies completed source and historical
isolated synthetic quality/Alloy contract, including actual importer replay/concurrency/outage and metrics
temporality/retry/restart evidence. Its real application target, SeaweedFS
object handoff and live Grafana result reader remain unverified; synthetic
metrics acceptance is not a live external-project receipt. Archived
SPEC-0199/0200 provide no current approval.

No business project ID, external deployment topology, application endpoint,
OIDC client, S3 identity, search authority, traffic budget, or speech product
scope is approved here. Registering metadata is not a grant of network
access, credentials, runtime deployment, or storage. Civil-service exam, English
and Japanese learning applications are excluded, including planning, code,
databases, collection and resources. The current request does not reopen merged
LAB service/source relocation, image, secret, data or execution work; existing
pins and source remain untouched unless a separate request establishes a
concrete operational boundary. P08 may move typed LAB documents to their
Stage05 family `labs/` destinations with required folder and parent README
navigation, Registry links and path checks; that documentation exception
authorizes no LAB runtime action. Do not read secret values, private environment
files, authentication files, raw HOME logs, or user data.

## Contracts

### Behavior Contract

1. All changes are classified as confirmed source defects, consumer-dependent
   design, or runtime-unverified conditions. Each service row names the actual
   consumer, declaration owner, changed file, variable/secret reference,
   regression, rollback, and approval. Generated version/service projections
   are refreshed through their registered generators.
2. n8n main, worker, and both external task runners use one verified compatible
   stable version across Compose, Dockerfile defaults and image/update ownership.
   The instance consumes `N8N_RUNNERS_TASK_TIMEOUT` and the runner receives the
   supported timeout setting. Broker and runner authentication consume the
   selected secret files through verified entrypoints; empty/mismatched
   credentials fail closed without printing values or placing them in image
   layers or process arguments. Queue, manual, scheduled, webhook and Code
   execution paths are tested before reducing main runners. No DB upgrade
   occurs without matching metadata and encryption-key recovery evidence.
3. Crawl4AI's pinned image is checked against current official advisories,
   architecture and digest. Synthetic denied/allowed cases cover robots,
   link preview, redirect and untrusted configuration wrappers before a
   version change is accepted. Its separate bridge and inbound token gate
   do not prove egress isolation. Deny private, link-local and metadata
   destinations at each DNS resolution and redirect hop, including rebinding
   and caller-supplied proxy/browser flags, or require an approved egress
   enforcement layer. Its absent consumer remains absent until approved.
   LAB is excluded from this request; prior Cassandra evidence remains historical
   and authorizes no new LAB inspection, implementation or execution.
4. Browser administrator SSO, application OIDC, webhook signatures and machine
   service authentication have separate routes and tests. Removing ForwardAuth
   requires the target API's own issuer, audience and authorization checks.
   Project OIDC clients use approved redirect, PKCE, cookie and logout rules;
   user ownership is enforced by the app/API. Management client secrets,
   superuser credentials and OpenBao admin tokens are never shared with an
   external project. A login HTML response is not machine API success.
5. Traefik retains `exposedByDefault: false`, explicit service/network names,
   and distinct browser/machine routes. Any shared connection network has a
   named owner and approved project allowlist. Same-daemon projects use
   project/service-specific networks with only the gateway and target service,
   or backend mTLS/service authentication that also rejects direct peers and
   project A-to-B access. Another host needs explicit DNS, TLS and access
   control. Cross-Compose `depends_on` is not readiness;
   consumers use bounded startup retry and operational disconnect handling.
   Rate limits and retries apply only where safe for method and idempotency.
6. Infra-owned integration metadata records project/environment and source
   refs, location-specific endpoints, allowed networks, DB/role, Valkey prefix,
   object bucket/prefix, OIDC client ID, search collection plus authorization
   path, telemetry identity, backup/restore owner, secret reference names,
   quota, schema/interface version and approval/verification state. No secret
   bytes, implicit project provisioning or app source enter root Compose.
   Alloy discovers only approved project labels/allowlist, not all Docker
   containers. OTLP producer identity is authenticated at the receiver and
   mapped to server-controlled project labels; untrusted resource and trace
   attributes are scrubbed and quotas bound the stream. Preserve
   SPEC-0203's existing metrics path until these controls are verified.
7. OpenBao sealed, live and Agent-template-current states are observed
   separately; a sealed status is not application readiness. Secret `_FILE`
   support is verified per image/entrypoint, including empty file, renewal,
   reload and DSN special-character cases. External-project secrets require
   a project-specific AppRole, token sink, policy, output directory and exact
   file mount; the management renderer and its output volume are not shared.
   Docker socket read-only mounts
   remain full API access unless a proven authorization boundary limits calls.
8. Existing service roles remain distinct: management metadata stays in
   mng-pg/mng-valkey, business data in approved dev project roles, test results
   in perf_db, original objects in restricted storage, and recreatable search
   indexes behind project authorization. Real Avro consumers retain Schema
   Registry; CDC source/slot/lag/replay, analytics reader/writer, checkpoint
   restore, and workflow payload retention are accepted only through named
   synthetic or approved operational fixtures. No new engine or duplicate
   quality/observability stack is inferred.
9. The development PostgreSQL pgBackRest repository is included in the
   existing Restic state set only through a complete source path: bounded
   scheduler, globals/extension/migration metadata, repository mount,
   allowlist, offsite copy and alert accounting. A live PGDATA copy or a file's
   existence is not a recovery claim. Restore acceptance uses a separate
   project and volume with a selected backup/WAL range and compatible image;
   HOME backup, restore, key rotation, retention deletion and RPO/RTO claims
   require separate approval and measurement.
10. Every long-running service distinguishes liveness from functional
    readiness. Observability reports freshness, data gaps, collector failure,
    backup capacity and user-visible completion without LAB false positives.
    Mailpit remains development capture; Stalwart distinguishes accepted,
    failed and uncertain delivery. AI/GPU and Flink checkpoint settings are
    budgeted or left unverified rather than asserted from configuration alone.
11. Every stateful engine is captured by its own consistent method, never a
    live file copy: pgBackRest for PostgreSQL, a bounded RDB export for each
    Valkey whose queues matter, the SQLite online backup API, and the
    engine's snapshot API for OpenBao and OpenSearch. An engine without a
    tested method is named as a recovery gap. A restored queue replays
    pending entries at least once, so its consumers stay idempotent.
12. Every `*_FILE` and `*_CMD` key in the rendered root has a recorded
    verdict for its exact image: native, repository wrapper or unsupported,
    with upstream source or runtime evidence. A service whose image ignores
    a key stays out of the HOME selection until it is fixed.

### P08 operations-document layout contract

TSK-0015 continues criterion 8 and SPEC-0212 requirement 25 without reopening
completed SPEC-0212/P00 or SPEC-0227 body-refresh evidence. Inspect every tracked
Guide, Policy and Runbook's actual type, artifact ID, title, service bindings,
body and links before selecting one exact meaningful destination. Numeric IDs
alone do not identify a subject or LAB membership. Populated domains belong
within `docs/05.operations/{guides,policies,runbooks}/`; LAB documents go only
to each family's `labs/`. Repository-root `labs/` owns the separately authorized
2026-10-12 service-source relocation; it is not a destination for Stage05 documents.

Each populated domain and parent family requires a Korean, profile-valid README
with exact links, roles, scope, owners and verification. Create no empty domain
or duplicate active document. Bind old/new exact paths, source SHA256, ID/created
date, anchors, relative working-directory assumptions and generated owner before
moving. Preserve command/warning/recovery/evidence content except reviewed
relative-path or changed-document structure adjustments; do not repeat the
completed whole-corpus refresh or rewrite sealed history.

Test nested path/profile/discovery/catalog/binding/link/changed-CI consumers
together, rejecting unsafe paths, unknown domains, duplicate IDs and case
collisions. Historical old-path resolution, if needed, is bounded metadata and
never a second active copy. Source preparation can proceed while feature
delivery is pending; actual rename/link integration requires exact single-writer
leases and fixed feature-owner SHAs. Future delivery requires an owning-Spec PR,
exact-head CI and independent review before merge; operational acceptance is not
inferred from document relocation.

### Hermes ingestion transport contract

The direct 2026-10-30 request adds the bounded TSK-0022 continuation. Existing
Hermes Cron jobs and email remain producers. The active structured exporter
`84d3f689378b` remains the sole exporter; consume completed
`out/<job_id>/<run_id>.json` files without a duplicate exporter or Cron.

A restricted host Publisher reads only the three approved job identities and
approved report/idea roots. It verifies the reviewed SPEC-0247 validator by exact
path/SHA-256 and fails closed if unavailable or changed; do not copy or weaken
that validator. Snapshot candidate, original report and per-idea bytes losslessly
in a private SQLite Outbox (directory 0700, files 0600). Reject path/symlink
escapes, incomplete artifacts, hash mismatch and private-infrastructure inputs.
No LLM summary, source deletion, whole Hermes home, credentials, browser session,
Hermes database or Docker socket exposure is authorized.

Outbox identity is `(job_id, run_id)` with immutable candidate, report, idea and
prepared-request digests. Exact replay deduplicates; changed bytes with the same
identity preserve original snapshots and conflict history. States distinguish
pending, sending, uncertain, delivered, failed and conflict; the delivery processor converts interrupted sending to uncertain after acquiring its lock. Bounded retries require provable no-send or contract-defined
reconciliation. Only an authenticated, identity/digest-bound receipt proving
Gateway durable persistence permits delivered. A queue/webhook acknowledgement
is insufficient. Lost responses remain uncertain until duplicate-safe reconciliation.

Adapter-independent source and synthetic tests may proceed while Blog-data's
Gateway API develops. Its exact approved contract and fixtures must define
request/authentication/status/receipt/reconciliation before any live adapter or
forwarding workflow is authored. An inactive preparation stub may contain only
authenticated Webhook → StopAndError `GATEWAY_CONTRACT_NOT_BOUND`, with no
HTTP node, Gateway endpoint or body mapping. The supplied public web build manifest is not
an ingestion contract. Never infer Gateway JSON/status codes from it. Each
repository's adoption remains with the common owner and exact approved revision.

Start with a restricted host process, requiring no Compose change. A later
approved non-root container may use existing `n8n_net` after overlay/network
review and exact read-only artifact mounts. Public Traefik SSO and ports remain
unchanged. Reuse queue workers, PostgreSQL metadata, selected Valkey and OpenBao
ownership. Do not repurpose Manifest Outbox Notifier or duplicate `hy-home.n8n`
news crawling. Actual server-B DNS/TCP/TLS/authentication/timeout evidence must
originate from the actual n8n worker; host probes prove a different path.

## Acceptance Criteria

### Acceptance Contract

1. Current service evidence and owner/file/variable/consumer/regression/
   rollback/approval ledger is complete, and no existing feature acceptance
   owner in the current SPEC-0212 routing is overwritten.
2. n8n version, runner timeout and secret-consumption source contracts pass
   focused static and isolated functional checks without a HOME upgrade.
3. Existing Crawl4AI security/egress acceptance belongs to SPEC-0220 and is
   NO_CHANGE when applied. Any consumer-dependent increment uses its named
   target and DNS/redirect/private-destination checks; LAB is out-of-scope.
4. Gateway, OIDC, machine auth, secret and socket boundaries have explicit
   route/identity/readiness and direct-backend/project A-to-B denial tests or
   named `BLOCKED` evidence.
5. A versioned infra-owned schema and validator reject malformed project
   metadata, unapproved reference names and credential-bearing endpoint
   syntax without provisioning resources. Closed fields and a separate secret
   scanner/review guard against secret bytes; schema validity alone cannot
   prove their absence. Live project connection and Alloy discovery require a named
   project and a later exact Task. That Task must authenticate OTLP
   producers, map identity to server labels, scrub traces and bound quota
   while preserving existing quality metrics.
6. Messaging, workflow, AI, mail and analytics roles have a consumer-backed
   source decision, regression or honest unverified status without duplicate
   services or speculative learning-app resources.
7. Dev-pg backup enters the existing Restic source chain with bounded failure
   handling, and a separately approved isolated restore is the only recovery
   PASS route; HOME and real data remain distinct.
8. Documentation, generated projections, focused checks and independent
   review match the exact diff. The final report separately records source,
   static, isolation, HOME and migration statuses with SHA and exit evidence.
   Future work is limited to typed Stage05 LAB-document moves, their READMEs
   and path contracts. Existing merged LAB service/source relocation is
   preserved as NO_CHANGE and is neither an acceptance target nor a reason to
   change LAB images, secrets, data or runtime resources.
9. The second round (TSK-0005) closes contracts 11 and 12 in source with
   tests that fail against the previous source, records HOME observations
   for authentication, CDC, workflow and backup without changing HOME
   data, and names each remaining gap with its owner action.
10. The current P04/P05 native integration increment separately proves the
    selected Airflow DEV/S3/DAG and n8n JSON/import/execution flow from input
    through its recovery fixture. Source creation, reference wiring, secret
    consumption and native results have separate evidence; missing exact
    consumer/target defers only that lane. Earlier version-work NO_CHANGE remains
    historical; Task0017 supports criterion 2 with the current stable source
    preparation, without accepting this criterion's native integration lane.

11. P01 completes one coherent native TLS endpoint/CA contract for OpenBao,
    Agent, metrics, operational clients and Traefik backend; bootstrap trust
    and the server key are provisioned independently of that OpenBao. Historical
    exact 2.6.2 isolated proof is preserved; final verification uses SEC01's
    current stable server/Agent/snapshot CLI contract (2.7.1 at the current
    assessment), with fresh input binding. The tests exercise wrong CA/SAN,
    expiry/denial, sealing, fresh
    Agent process/cold start, wrapped SecretID reissue, restricted snapshot
    issuance/renewal/save/empty Raft restore/unseal, HMAC audit and audit failure.
    HOME cold boot, custody and real snapshot acceptance require the named
    host, external unseal/offsite material and restore boundary; missing facts
    defer only that lane. P06 expansion remains blocked until those conditions
    pass, including known SecretID expiry and malformed-audit-input residuals on
    the selected runtime; fixed-version verification and abandoned wrapped
    issuance cleanup remain acceptance prerequisites. Existing nonce-based
    cleanup is reused; the requested issuance_id metadata contract requires
    explicit journal compatibility, never blind renaming of outstanding receipts.
    No new KMS/engine, LAB action or learning-app planning is included.
    TSK-0006 owns this increment; TSK-0005/0229's applied snapshot source is
    NO_CHANGE and their historical results are never a fresh P01 PASS.
12. CLN01 owns the consumer assessment and narrow private-unlink helper for
    material already retired by its owning source contract. It permits a
    `COMM-003` disposition only after SMTP01 has merged and its source
    and operational cutover evidence is recorded, then only after fresh source,
    runtime, jobs, backup/restore and external-consumer checks. SMTP01 proof
    cannot automatically translate into CLN01 manifest truth. The helper
    rejects tracked, protected, shared-inode, symlinked, identity-changed or
    unknown targets. `COMM-002` stays protected and `PG-020` remains retained
    for rollback. The generic helper refuses COMM-003 by ID and exact path;
    its sole proposed unlink executor is SMTP01's `smtp_contract --retire`,
    subject to supervisor release and integrated evidence/lock checks.
    CLN01 owns assessment and the hold, not a second executor. TSK-0007 owns this increment.
<!-- markdownlint-disable MD029 -->
13. P09 produces a bounded, offline LLM Wiki preparation package: product
    intake; future consumer, source/artifact, job/outbox/handoff and blog-data
    handoff contracts; valid and invalid synthetic fixtures; future user-flow
    acceptance; and a readiness matrix. The generic registration schema and
    validator are reused without weakening or duplication. The package rejects
    cross-project/path-escape, wildcard/admin and empty-required values. It
    does not create a Wiki Core/API/UI, source crawler, app database/role,
    collection/bucket, credential, external workspace, scheduled workflow,
    blog-data write, learning application or LAB runtime change. Actual source
    revision, ACL/revocation, retention, backup and recovery verification stay
    future acceptance conditions, not preparation PASS claims.
<!-- markdownlint-enable MD029 -->

<!-- Criteria 12/13 are reserved by CLN01/P09; retain the owning IDs. -->
<!-- markdownlint-disable-next-line MD029 -->
14. SMTP01 leaves one root `smtp_password` source at the canonical communication
    SMTP path and maps the Supabase auth grant to its existing container target.
    COMM-002 owns the value; COMM-003 is a value-free retired-ID alias. Model,
    generator and wrapper regression tests reject drift, duplicate mounts,
    unsafe retirement and secret output. Fixed-image isolation separately
    proves SMTP authentication, capture, negative password/TLS cases and file
    readability without HOME activation. SEC01 owns image versions; the
    integration coordinator controls common-file delivery and HOME deployment.
    CLN01 assesses the exact duplicate; SMTP01 is its sole proposed unlink
    executor after source, runtime, jobs,
    backup/restore and external consumers are verified. Missing private facts
    defer migration/deletion alone. Rollback uses the canonical source mapping
    and only the affected consumer; no volume reset or broad rotation occurs.
    The 2026-10-12 user clarification accepts the delivered SMTP01/CLN01
    changes and excludes actual LAB GoTrue SMTP connection configuration,
    activation and sending from criteria 12 and 14. Missing LAB readiness
    cannot reopen that acceptance. Existing source mapping and isolated
    fixture evidence remain valid within their recorded scope; user acceptance
    is not a new provider authentication, send or recovery receipt. Any later
    genuine send uses the operator-supplied designated sender/recipient mailbox
    under its bounded ROOT or P05 lane, without publishing the address here.

<!-- markdownlint-disable MD029 -->
15. SEC01 maintains a current security integration ledger and its version
    projections without representing a candidate pin, isolated test or
    source merge as a deployed update. It preserves actual source/unit/static
    receipts and failures, integrates common validator, inventory, manifest
    and navigation changes through their single writer, and records a fresh
    latest/security gate and independent review at the final delivery head. Local
    source delivery preserves a blocked latest/security result as pending
    operational acceptance rather than claiming full SEC01 completion. HOME,
    migration, rotation, real service recovery and deployment remain `NOT_RUN`
    until a named target, consumer, backup and recovery boundary exist. Image
    signature/SBOM/scan acceptance separately awaits the named tool, cache/DB
    and trust facts; it is not inferred from a missing HOME target. TSK-0009
    owns this increment; LAB runtime and
    learning applications remain out of scope.
    The earlier warning-only version restriction is historical. The direct
    2026-10-16 request authorizes full ROOT stable/security investigation and
    compatible source updates; major/schema changes still require independent
    migration, native and recovery evidence. Task0017 owns the bounded current
    n8n preparation, while Task0009 retains this criterion's overall acceptance.
    Reuse the existing reviewed
    security-disposition gates; missing or stale evidence remains UNKNOWN,
    never a clean verdict. Do not invent a replacement scanner or optional gate.
    Bind current ROOT inputs independently and exclude relocated LAB
    Supabase/GoTrue rows. Existing completed source and baseline evidence is
    preserved. Native acceptance, migration and recovery retain their own
    Tasks; user-accepted SMTP01/CLN01 scope and P09 preparation are not reopened.
16. P02 provides one value-free secret catalog with preserved issued IDs,
    canonical COMM-002 and an alias/tombstone for COMM-003, explicit
    classification, consumers, delivery and independent recovery dependencies.
    Public/local views and generator rules reject sensitive fields, aliases
    without a canonical source and reissuance of migrated or retired identities.
    Source classification and provisional mappings may proceed from integrated
    SMTP01; P01's final authentication/recovery contract gates final destinations
    and P06 gates real KV copy and consumer delivery. Unknown consumers remain
    BLOCKED_FACTS and positive recovery consumers remain retained under CLN01.
    TSK-0010 owns catalog, schema, view tooling and focused regressions; shared
    Compose/environment/Registry/backup integration has one coordinator writer.
    No credential value is read, copied, rotated or deleted by Task issuance.
17. P03 reconciles every current root service with the existing service inventory,
    keeping declared, running, healthy, used and recovered states separate. Its
    closed four-location contract distinguishes listener, internal DNS, host
    publication and Traefik backend, with lossless protocols/ranges/aliases and
    explicit unknown listener observations. Synthetic tests reject secret output,
    malformed endpoints and cross-tier/project drift. Native machine auth,
    CDC/workflow consumers, secret delivery and recovery require their exact
    targets and owning evidence; a declaration, HTTP 401 or fixture is not a
    HOME result. TSK-0011 owns criterion 17/W33 and new dedicated source/tests;
    common settings remain single-writer integration proposals. Applied source
    and historical Task acceptance are preserved; learning apps, LAB runtime
    and Wiki implementation are excluded.
    Opt-in dedicated broker observer identities use explicit minimal ACL commands,
    with source, synthetic, isolated, HOME, rotation and recovery evidence separate;
    criterion 16 retains catalog ownership and default application authority remains.
18. P04 implements the independent `opsflow_dev` manifest validation and
    publication batch, with one canonical Airflow workload, versioned
    `ops_flow` SQL and a frozen outbox interface for P05. Strict synthetic
    input validation, byte-derived identity, S3 readback, atomic PostgreSQL
    publication, replay/concurrency/backfill and failure recovery are tested.
    Native execution proves the selected Celery worker, DEV roles and restricted
    object identity, including direct-write/cross-database/object denials and
    separately targeted empty restoration. DAG parsing performs no workload
    file, database or object I/O. P04 creates no Wiki engine or real source
    collector and does not implement P05 notification. TSK-0012 owns W34-W39;
    shared provisioning, images, Compose, catalogs and QA registration retain
    their named single writers. Source preparation can proceed now; native
    actions require the relevant fixed image and exact resource/recovery
    contract. Restricted file delivery may support pre-migration DEV proof;
    P01/P06 completion is not a global prerequisite to that bounded lane.
19. P05 implements one independent DEV-only n8n notifier consuming P04's
    versioned `ops_flow` claim/ack/retry interface. A value-free workflow imports
    inactive, uses operator-resolved native credential references and proves
    manual execution on the actual queue worker and external runner. The
    notifier has function-only database access and a restricted Mailpit
    capture path. Run-derived Message-ID, bounded transports, checked ack,
    stale leases, uncertain SMTP isolation and reconciliation, restart and
    serial metadata and database restoration have genuine native evidence.
    Criterion 22 holds the scheduled, concurrent, retry/dead and rotation
    evidence. SMTP acceptance is not external delivery or exactly-once
    processing. TSK-0013 owns W40-W41; P04 retains SQL/provisioning,
    SEC01 images and the coordinator shared integration. Draft source tests may
    run in parallel; native P05 execution follows P04 publication/outbox proof.
    No Wiki schedule, Airflow mail duplicate, external SMTP or extra engine is
    created. Only the relevant image/resource/credential/recovery contracts gate
    its native lane; full SEC01/P01/P06 completion is not a global start gate.
    Task0018 supports the current safety correction: a server-issued deadline
    bounds SMTP work, and existing retry, expired sending or ambiguous SMTP/ack
    outcomes are quarantined pending evidence-backed reconciliation. Automatic
    retry requires proof that no send occurred; source tests and isolated SQL
    proof do not accept the actual n8n queue or HOME lane.
20. P06 migrates only catalog-approved existing static values in sequential
    consumer waves, preserving the exact bytes during the first copy. It
    consumes P01's accepted authentication, renderer and recovery contract,
    P02's single value-free catalog and P03's actual delivery facts; the first
    real pilot is one existing P04 opsflow DEV ingest/S3 consumer. KV-v2 CAS=0,
    equal-value no-op, different-value conflict and bounded reconciliation
    after ambiguous writes prevent blind overwrites. A separate least-privilege
    renderer proves versioned delivery and native consumption. Pilot rollback,
    snapshot/empty restoration and consumer reauthentication precede authority
    changes. Old plaintext and private metadata are removed only after a fresh
    five-axis zero-consumer proof through the named SMTP/CLN/service executor;
    server credential rotation is a separate unit. TSK-0014 owns W46-W55 and
    new migration-only schemas, executor and tests. Public schema and synthetic
    preparation can proceed now; real copy waits for the selected P01/SEC/P02/
    P03/P04 contracts, and cutover/removal also require integrated generator
    guards. Missing opsflow IDs or KV destinations are blocking facts, not
    invented bindings. No duplicate catalog, issuer, workflow, Wiki resource,
    LAB runtime or learning-app plan is created. Source-only delivery does not
    close the native migration, rotation or recovery criteria.
21. P10 binds the independent opsflow manifest-to-recovery vertical slice to
    exact current source, image and interface revisions. It reuses P04's
    Airflow/SQL/publication and P05's outbox/notifier implementation and retains
    each feature's acceptance owner. Offline preparation may proceed now;
    isolated native admission needs the relevant fixed artifacts, least-privilege
    connection contract and bounded synthetic resources. Selected HOME and real
    deletion/migration/rotation/recovery need their own exact target, backup set,
    custody and reversible boundary; global completion is never inferred from
    one consumer or isolated success. P10 verifies replay, concurrent claims,
    negative authorization, fault reconciliation and restoration to an empty
    separate target, then consumes P08's final path/hash handoff for manual
    working-directory checks. Its requirement 11–30 report separates SOURCE,
    UNIT, STATIC, ISOLATED, HOME, MIGRATION, ROTATION, RECOVERY and DELIVERY,
    preserves failures and NOT_RUN lanes, and excludes Wiki implementation,
    learning applications and LAB runtime. TSK-0016 owns W63–W69 and dedicated
    acceptance-only fixtures/tests; shared registration and feature fixes remain
    single-writer proposals. Local source delivery cannot close this criterion.
22. The P05 notifier proves one-minute scheduled execution on the actual queue
    worker, concurrent claims, retry and dead-letter handling, an empty queue,
    credential rotation with stale-credential denial, and paired metadata and
    encryption-key restoration with genuine native evidence, building on the
    criterion 19 notifier. TSK-0013 owns W42-W45. On 2026-10-29 the owner moved
    these obligations out of criterion 19, whose native evidence covers manual
    execution only.
23. Hermes transport preserves Cron/exporter/email and proves a bounded,
    lossless Publisher/Outbox with immutable execution identity, reviewed
    candidate validation, duplicate/conflict handling, restart recovery,
    bounded retry and durable-receipt reconciliation. TSK-0022 owns W79-W83
    and reports SOURCE, SYNTHETIC, API_COMPATIBILITY, N8N_NATIVE,
    SERVER_B_NATIVE and DELIVERY separately. Dispatch additionally requires
    producer-authenticated collection evidence, reported as PRODUCER_AUTH; a
    structural evidence check alone never authorizes delivery. The verifier
    runs only from a hash-locked, root-owned release under a dedicated
    non-root account with `python3 -I`; server A holds an ingest-only token
    for `POST /v1/ingestions` and no read permission. Exact Gateway contract/fixtures,
    native worker networking/authentication and actual durable persistence
    remain required blocked lanes until supplied and approved. Source-only
    Publisher or simulated adapter evidence does not close this criterion.
<!-- markdownlint-enable MD029 -->

## Failure Conditions

### Failure Modes and Guardrails

Reject version mismatch, unsupported `_FILE` variables, missing selected
secret, unsafe redirect, public unauthenticated machine API, unknown project
label, cross-project read/write, unbounded crawler egress, sealed-is-healthy
claims, missing WAL/backups, and projection drift. Preserve unrelated worker
changes; no reset, stash, broad clean, full-stack `up`, `down -v`, volume prune,
credential rotation, DNS/firewall edit or HOME restart without the named target
and recovery boundary. The current request authorizes source/docs/tests and
logical commits; each remaining owning-Spec delivery uses its PR, exact-head CI
and independent review before merge. `dev` is excluded throughout. This does
not reclassify historical local-main receipts or absorb unrelated
integration/runtime commits.
Missing permission or target defers only the dependent operation.

## Related Documents

- [Hermes transport Task](tasks/tsk-0022-hermes-blog-ingestion.md)

- [P10 opsflow acceptance Task](tasks/tsk-0016-p10-opsflow-acceptance.md)

- [P08 operations-document layout Task](tasks/tsk-0015-p08-operations-document-layout.md)

### Traceability

- [Current request reconciliation](../0212-request-baseline-and-reconciliation/spec.md)
- [REQ-0027](../../01.requirements/0027-home-development-host.md)
- [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md)
- [ADR-0046](../../02.architecture/decisions/0046-capability-tiers-and-quality-boundary.md)
- [REQ-0026](../../01.requirements/0026-document-retention-and-retirement.md)
- [AD-0030](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- [ADR-0037](../../02.architecture/decisions/0037-package-disposition-wait-and-task-cancellation.md)
- [CLN01 material retirement Task](tasks/tsk-0007-cln01-material-retirement.md)
- [SPEC-0201](../../98.archive/completed/03.specs/0201-home-infrastructure-diagnosis-and-work-design/spec.md)
- [SPEC-0202](../../98.archive/completed/03.specs/0202-development-data-and-lab-isolation/spec.md)
- [SPEC-0203](../../98.archive/completed/03.specs/0203-quality-results-and-isolated-load-testing/spec.md)
