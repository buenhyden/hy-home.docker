---
title: "Service Integration, Security, and Operations Specification"
version: "1.6.0"
type: "sdlc/spec"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-10"
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
access, credentials, runtime deployment, or storage. Civil-service exam, English and Japanese learning applications are excluded,
including planning, code, databases, collection and resources. All LAB-specific
runtime code, configuration, data, secrets and execution are excluded. P08 may
move typed LAB documents to their `labs/` destinations with required folder and
parent README navigation, Registry links and path checks; that documentation
work authorizes no LAB runtime action. Do not read secret values, private environment
files, authentication files, raw HOME logs, or user data.

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
actual remote checks and independent review before merge; do not copy W7's
old CI disposition into current execution. SPEC-0221 already owns the request
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

### Failure Modes and Guardrails

Reject version mismatch, unsupported `_FILE` variables, missing selected
secret, unsafe redirect, public unauthenticated machine API, unknown project
label, cross-project read/write, unbounded crawler egress, sealed-is-healthy
claims, missing WAL/backups, and projection drift. Preserve unrelated worker
changes; no reset, stash, broad clean, full-stack `up`, `down -v`, volume prune,
credential rotation, DNS/firewall edit or HOME restart without the named target
and recovery boundary. The current request authorizes its source/docs/tests,
logical commits, branch push, PR and merge after required checks and review;
missing permission or target defers only the dependent operation.

### Open Questions

A real external project must identify its project ID, endpoint topology,
OIDC/S3/search scopes, operator and recovery boundary before a live connection
can pass. P04 needs its actual native Airflow DAG/DEV/S3 target; P05 needs
its actual n8n native import/execution target. P03 confirms PORT_CONTRACT and
port_inventory.py ownership before creating them; they are not assumed to
exist in this repository. Secret metadata, migration eligibility, reference
wiring, real consumption, rotation and recovery are separate completion states.
HOME PITR/offsite recovery and owner-held snapshot credentials remain with
their existing Tasks; historical isolated PASS is not a fresh HOME receipt.

### Operational Impact

Future source changes may alter native workflow execution, crawler rejection,
secret consumption and backup scheduling when deployed. The exact executing
stage binds target, impact and recovery before acting. P00 performs no such
runtime change; authorized delivery is independent of those unexecuted lanes.

## Scope

### Scope

## Contracts

### Contracts

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

## Acceptance Criteria

### Acceptance Criteria

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
9. The second round (TSK-0005) closes contracts 11 and 12 in source with
   tests that fail against the previous source, records HOME observations
   for authentication, CDC, workflow and backup without changing HOME
   data, and names each remaining gap with its owner action.
10. The current P04/P05 native integration increment separately proves the
    selected Airflow DEV/S3/DAG and n8n JSON/import/execution flow from input
    through its recovery fixture. Source creation, reference wiring, secret
    consumption and native results have separate evidence; missing exact
    consumer/target defers only that lane. Existing version work is NO_CHANGE.

11. P01 completes one coherent native TLS endpoint/CA contract for OpenBao,
    Agent, metrics, operational clients and Traefik backend; bootstrap trust
    and the server key are provisioned independently of that OpenBao. Exact
    2.6.2 isolated tests exercise wrong CA/SAN, expiry/denial, sealing, fresh
    Agent process/cold start, wrapped SecretID reissue, restricted snapshot
    issuance/renewal/save/empty Raft restore/unseal, HMAC audit and audit failure.
    HOME cold boot, custody and real snapshot acceptance require the named
    host, external unseal/offsite material and restore boundary; missing facts
    defer only that lane. P06 expansion remains blocked until those conditions
    pass, including known SecretID expiry and malformed-audit-input residuals on
    the selected runtime; fixed-version verification and abandoned wrapped
    issuance cleanup remain acceptance prerequisites. No new KMS/engine, LAB action or learning-app planning is included.
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

<!-- markdownlint-disable MD029 -->
15. SEC01 maintains a current stable/security integration ledger and its
    version projections without representing a candidate pin, isolated test or
    source merge as a deployed update. It preserves actual source/unit/static
    receipts and failures, integrates common validator, inventory, manifest
    and navigation changes through their single writer, and records a fresh
    latest/security gate and independent review at the final PR head. HOME,
    migration, rotation, real service recovery and deployment remain `NOT_RUN`
    until a named target, consumer, backup and recovery boundary exist. Image
    signature/SBOM/scan acceptance separately awaits the named tool, cache/DB
    and trust facts; it is not inferred from a missing HOME target. TSK-0009
    owns this increment; LAB runtime and
    learning applications remain out of scope.
<!-- markdownlint-enable MD029 -->

## Related Documents

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
