---
title: "Service Integration, Security, and Operations Plan"
version: "0.1.4"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0204-PLAN-0001"
parent_ids:
- "SPEC-0204"
created: "2026-10-03"
---

# Service Integration, Security, and Operations Plan

## Objective

Implement Prompt 04 in reversible, reviewable Tasks. The user approved the
listed source scopes on 2026-10-03. The package established file ownership
and acceptance gates before any service declaration was changed.

## Dependencies

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
- No current external project registration, real traffic target or product
  scope for Prompts 07/08. Runtime, secret issuance, data, remote and network
  operations need their own exact approvals.

## Execution Sequence

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

## Risk and Rollback

| Risk | Bound and recovery |
| --- | --- |
| n8n update mutates metadata or encryption compatibility | Back up compatible metadata and key before any separate HOME upgrade; source rollback alone cannot reverse DB migration. |
| Runner token or Valkey secret is not consumed | Test actual entrypoint with synthetic files; no plaintext arguments, shell tracing or unbounded environment export. Revert only Task-owned source on failure. |
| Crawler fix changes allowed URLs | Use pinned synthetic DNS/redirect/private-destination cases; a separate bridge is not egress enforcement. Preserve the prior image declaration until source acceptance. |
| External discovery widens collection or ingress | Require project/service network or backend auth, direct-peer denial, authenticated OTLP identity mapping, trace scrub and quotas; reject unregistered peers. Revert scoped source; do not delete project state. |
| Backup path is incomplete or data is deleted | Include mount, list, scheduler, offsite and alert as one reviewed source change; no live PGDATA copy, retention/prune or restore without separate approval. |
| Parallel writers change shared files | TSK-0001, then TSK-0002, then TSK-0003 write serially. Rebase against exact preceding diff; do not reset, stash or clean another worker's state. |
| Existing required CI is red | Keep source review and hosted gate results distinct; do not bypass branch protection or weaken a security audit. |

## Verification

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

## Rulings

SPEC-0203 already wrote the common Alloy metrics path; TSK-0002 may extend only
bounded external discovery after review. SPEC-0202 development DB source and lifecycle handoff are integrated in this
closure branch before the backup source change. Prompt 05 owns Storybook;
Prompt 06 owns the external application's consumed manifest and deployment.
Cassandra's current official-image LAB move is already implemented; no
Bitnami-wide replacement is planned. Crawl4AI has no confirmed consumer and
gets a security fix, not automatic HOME activation.

### Completion recheck — 2026-10-04

W4's current Restic/dev-pg source chain and freshly approved synthetic restore
passed; TSK-0003 is completed with its exact selected-set/snapshot receipt.
TSK-0002 and TSK-0004 remain completed. W2's exact-image n8n/Crawl4AI runtime
and secret/egress security acceptance remain BLOCKED in TSK-0001, so this Plan
and Spec remain active. Image pulls and the reviewed isolated security fixture
require the pending scope approval; HOME and host policy changes remain held.
