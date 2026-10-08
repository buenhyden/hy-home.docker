---
title: "Service Integration, Security, and Operations Plan"
version: "1.1.0"
type: "sdlc/plan"
status: "blocked"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0204-PLAN-0001"
parent_ids:
- "SPEC-0204"
created: "2026-10-03"
---

# Service Integration, Security, and Operations Plan

## Overview

### Objective

Implement Prompt 04 in reversible, reviewable Tasks. The user approved the
listed source scopes on 2026-10-03. The package established file ownership
and acceptance gates before any service declaration was changed.

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
- No current external project registration, real traffic target or product
  scope for Prompts 07/08. Runtime, secret issuance, data, remote and network
  operations need their own exact approvals.

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

### Rulings

SPEC-0203 already wrote the common Alloy metrics path; TSK-0002 may extend only
bounded external discovery after review. SPEC-0202 development DB source and lifecycle handoff are integrated in this
closure branch before the backup source change. Prompt 05 owns Storybook;
Prompt 06 owns the external application's consumed manifest and deployment.
Cassandra's current official-image LAB move is already implemented; no
Bitnami-wide replacement is planned. Crawl4AI has no confirmed consumer and
gets a security fix, not automatic HOME activation.

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
- [Task 0001](tasks/tsk-0001-runtime-compatibility-and-security.md)
- [Task 0002](tasks/tsk-0002-external-project-integration.md)
- [Task 0003](tasks/tsk-0003-backup-and-cross-tier-operations.md)
- [Task 0004](tasks/tsk-0004-secret-layout-and-environment-parity.md)
- [Task 0005](tasks/tsk-0005-cross-tier-contracts-second-round.md)
