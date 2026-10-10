---
title: "Service Integration, Security, and Operations Plan"
version: "1.4.2"
type: "sdlc/plan"
status: "blocked"
owner: "@buenhyden"
updated: "2026-10-10"
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
no old prompt label creates duplicate work. LAB and learning apps, including
planning, are out-of-scope. P09's external Wiki needs its actual derived
workspace and P10 its real input-to-recovery target.

Historical W7 CI retirement does not govern this pass: current quality policy
and workflow-contract route hosted PR candidate QA and independent review.
Historical source-only restrictions bind the old slice, not all future units.
Only a missing real target/tool permission stops its dependent action. Follow
current approval-boundaries and SPEC-0221; no policy/hook/validator rewrite is
needed when the current enforcer already meets the request.

Shared root, gateway, Alloy, environment and backup files have one writer at a
time. Complete feature edits before the P08 document move writer starts, then
update references/checks and hand the destination SHA back. P08 gives LAB only
a prospective separate_target classification; no LAB documents are moved.

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

### P01 exact scope and sequence

Current input is main/origin/main `1ee5d6707e3b75b61222baad0c51050c64e1b10d`,
clean at start. Compared with d19fbfde6, only P00 documentation changed;
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
closure branch before the backup source change. SPEC-0219 owns Storybook; P09's external workspace owns its application
manifest/deployment. Existing LAB evidence is excluded from new execution.
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
