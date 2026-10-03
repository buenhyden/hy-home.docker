---
title: "Service Integration, Security, and Operations Specification"
version: "0.1.5"
type: "sdlc/spec"
status: "active"
owner: "@buenhyden"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0204"
parent_ids:
- "REQ-0027"
- "AD-0031"
- "ADR-0046"
- "SPEC-0201"
- "SPEC-0202"
- "SPEC-0203"
created: "2026-10-03"
---

# Service Integration, Security, and Operations Specification

## Overview

Prompt 04 closes confirmed shared-service compatibility and security gaps,
then defines the infrastructure side of external-project connection, signals,
and recovery. The implementation baseline is remote and local `main` at
`d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7` on 2026-10-03. Recheck it
before any source edit. SPEC-0202 owns development engines and migration;
SPEC-0203 owns performance results and its Alloy metrics path; Prompt 05 owns
Storybook; Prompt 06 owns an external application's consumed manifest and
application Compose. This package must not reimplement those owners.

The user approved Prompt 04 on 2026-10-03. This review transition records the
source contract before activation. HOME changes, credential actions, external
publication, and protected-branch merge remain separate approvals.

## Boundaries and Inputs

Use the current root include graph, service Compose/Dockerfiles/entrypoints,
tracked configuration and key-only environment contracts, current Stage 01/02/03
and Stage 05 owners, and official vendor documentation at implementation time.
SPEC-0201 supplies the source inventory and exclusive-writer handoff. SPEC-0202
supplies the dev-pg/dev-valkey source contract, synthetic restore result, and
operational exclusions. SPEC-0203 supplies a source-only quality/Alloy contract;
its live target, object handoff, Grafana result reader, and end-to-end metrics
remain unverified. Archived SPEC-0199/0200 provide no current approval.

No business project ID, external deployment topology, application endpoint,
OIDC client, S3 identity, search authority, traffic budget, or speech product
scope is approved here. Registering metadata is not a grant of network
access, credentials, runtime deployment, or storage. Do not create learning
application code, DBs, crawlers, ASR/TTS services, or GPU reservations for
planning-only Prompts 07 and 08. Do not read secret values, private environment
files, authentication files, raw HOME logs, or user data.

## Behavior Contract

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
   Cassandra remains in LAB on the official image path; an image/path search
   alone neither migrates old data nor establishes authentication or safe UID.
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

## Technical Approach

Use four serial Tasks: confirmed compatibility/security corrections; an
external-project integration contract and bounded discovery; backup and
cross-tier operations; then whole-tree secret path and environment parity.
TSK-0004 records the user's subsequent explicit 2026-10-03 authorization,
including value-preserving path moves and incident disposition. Each Task owns exact files and focused regressions in
its Task ledger before source mutation. Shared root, Alloy, environment,
Registry and backup files have one writer at a time. If a named project or
consumer is missing, record a versioned contract and `BLOCKED` runtime result
instead of provisioning resources. No Task changes HOME services or real data.

## Interfaces and Data

- Input: reviewed current declarations, official release/security references,
  named service consumers, approved project metadata and secret **reference
  names**, and a Task-specific execution target.
- Output: matched source declarations, restricted integration metadata,
  contract fixtures, updated Korean READMEs and Stage 05 guide/policy/runbook
  owners, and Task evidence. Values of secrets and raw operational data are
  never outputs.
- External application input/output: Prompt 06's Project-Template-derived
  repository supplies app Compose, business API/UI, migrations, collectors,
  workflow definitions, fixtures and E2E. Infra supplies approved engines,
  ingress/identity, telemetry and backup interfaces; the manifest records
  scopes and owners but cannot deploy the app.

## Failure Modes and Guardrails

Reject version mismatch, unsupported `_FILE` variables, missing selected
secret, unsafe redirect, public unauthenticated machine API, unknown project
label, cross-project read/write, unbounded crawler egress, sealed-is-healthy
claims, missing WAL/backups, and projection drift. Preserve unrelated worker
changes; no reset, stash, broad clean, full-stack `up`, `down -v`, volume prune,
remote push/PR/merge, credential rotation, DNS/firewall edit or HOME restart
without its separate exact approval.

## Acceptance Contract

1. Current service evidence and owner/file/variable/consumer/regression/
   rollback/approval ledger is complete, and no Prompt 02/03/05/06 owner is
   overwritten.
2. n8n version, runner timeout and secret-consumption source contracts pass
   focused static and isolated functional checks without a HOME upgrade.
3. Crawl4AI security and Cassandra LAB contracts are checked against current
   official sources; changed behavior passes DNS/redirect/private-destination
   allow/deny tests, with real egress enforcement separately verified.
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

## Traceability

- [REQ-0027](../../01.requirements/0027-home-development-host.md)
- [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md)
- [ADR-0046](../../02.architecture/decisions/0046-capability-tiers-and-quality-boundary.md)
- [SPEC-0201](../../98.archive/completed/03.specs/0201-home-infrastructure-diagnosis-and-work-design/spec.md)
- [SPEC-0202](../../98.archive/completed/03.specs/0202-development-data-and-lab-isolation/spec.md)
- [SPEC-0203](../../98.archive/completed/03.specs/0203-quality-results-and-isolated-load-testing/spec.md)

## Open Questions

The user approved the listed Task source scopes on 2026-10-03; a new path
requires an exact Task amendment. Any HOME upgrade,
backup execution, restore, credential issuance or network publication. A real
external project must separately identify its project ID, endpoint topology,
OIDC/S3/search scopes and operator before a live connection can pass. A
verified dev-pg recovery target and capacity budget are still absent.

## Operational Impact

Source changes may alter n8n workflow execution, crawler rejection, OpenBao
health dependency and future backup scheduling when deployed. Each requires
its own staged rollback and HOME change window; this package does not exercise
those effects.
