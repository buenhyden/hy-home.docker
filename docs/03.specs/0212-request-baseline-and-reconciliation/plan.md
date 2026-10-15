---
title: "Request Baseline and Reconciliation Plan"
version: "1.3.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-15"
layer: "specs"
artifact_id: "SPEC-0212-PLAN-0001"
parent_ids:
- "SPEC-0212"
created: "2026-10-07"
---

# Request Baseline and Reconciliation Plan

## Overview

The current 11–30 request preserves completed P00 Tasks. SEC01 delivers first,
SMTP01 owns the source transition second, and CLN01 deletes the old file third.

R10 adds W16–W23 in TSK-0007 from the 2026-10-15 source baseline. Existing
W1–W15 and completed bodies retain their earlier scope and evidence. The direct user request authorizes this bounded local contract and Plan;
that authority is not inferred from historical acceptance and does not approve
a shared edition or remote action.

## Scope

W9–W15 reconcile the request baseline, owner routes, shared-file leases
and SEC01 → SMTP01 → CLN01 handoffs; W1–W8 retain their historical receipts.
R10 W16–W23 add the current authority, document, lifecycle, retention,
hook/release, memory and OpenBao source corrections in TSK-0007 without
reopening completed Tasks or assigning new downstream acceptance owners.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Historical local/remote and Project-Template baseline read; retained evidence only | None | TSK-0001 | Preserved Task evidence |
| W2 | 2 | Historical fifteen-item ownership; superseded for current routing | W1 | TSK-0001 | Preserved Task evidence |
| W3 | 3, 4 | Historical root/LAB inventory and profile probes; LAB excluded from current execution | W1 | TSK-0001 | Preserved Task evidence |
| W4 | 5 | Historical conflict map and ADR-0047 | W2, W3 | TSK-0001 | Preserved Task evidence |
| W5 | 6 | Historical QA/protection read and validation | W4 | TSK-0001 | Preserved Task evidence |
| W6 | 1, 2 | Historical twenty-item main/template baseline | W5 | TSK-0002 | Preserved Task evidence |
| W7 | 3 | Historical inventory comparison; no fresh LAB run | W6 | TSK-0002 | Preserved Task evidence |
| W8 | 7 | Historical open-Spec disposition | W6 | TSK-0002 | Preserved Task evidence |
| W9 | 1 | Compare local/origin/remote main, dirty state and named baseline; parse root service keys and current inventory only | None | TSK-0003 | Value-free baseline and source-set evidence |
| W10 | 2, 3, 6, 7 | Read open Spec/Plan/Task frontmatter, latest tracked source and PR state; classify residuals and exclusions | W9 | TSK-0003 | Requirement table and owning evidence paths |
| W11 | 2, 4 | Observe contract RED; update SPEC-0212 Spec/Plan and SPEC-0204 Spec/Plan current routing | W10 | TSK-0003 | Contract GREEN; current authority checker |
| W12 | 4, 5 | Record writers/order/rollback, validate final documents, independent review, logical commits and protected PR delivery | W11 | TSK-0003 | Document checks; staged checks; actual hosted observations |
| W13 | 8 | Record current routing and SEC01 → SMTP01 → CLN01 ordering | W12 | TSK-0005 | Value-free contract probe; Stage 99 checks |
| W14 | 10 | Bind current main, supplied COORD input, observed worktree/PR state and active-package inventory; retain PR #457's merged receipt as input only | None | TSK-0006 | Value-free Git/source and lifecycle audit |
| W15 | 9 | Map requirements 11–30, reconcile active routing conflicts, record writer locks/recovery boundaries, run Stage99 selectors and hand off exact current inputs | W14 | TSK-0006 | Cross-package source, Task and document audit |
| W16 | 11 | P01 source/permission/delta baseline, attachment identity and classified finding map | None | TSK-0007 | Read-only Git and canonical-owner audit |
| W17 | 12 | P02 role, language, section and link correction; coupled Stage99 target amendment design | W16 | TSK-0007 | Changed metadata/links and affected contract regressions |
| W18 | 13 | P03 distinguish existing approval, Task state, acceptance, integration and observations | W16 | TSK-0007 | Generation-6 reader and exact lifecycle/acceptance evidence |
| W19 | 14 | P04 consumer/assurance/hold assessment and authorized retention or retirement | W16 | TSK-0007 | Direct consumer trace and applicable archive integrity checks |
| W20 | 15 | P05 hook/CI call graph and reproduced push-stage or duplicate assurance correction | W16 | TSK-0007 | Focused hook/routing tests and isolated installed-stage probe |
| W21 | 16 | P06 branch/release/CHANGELOG/rollback producer audit and concrete source corrections | W16 | TSK-0007 | Current producer/config trace and scoped contracts |
| W22 | 17 | P07 shared-memory/native-off/Restic reuse and justified missing assurance design or implementation | W16 | TSK-0007 | Existing receipts plus synthetic memory/backup regressions |
| W23 | 18 | P08 OpenBao optional-skip and CA-overlay discrepancies, operations promotion and quality limits | W16 | TSK-0007 | Focused OpenBao synthetic tests and changed document checks |

### Exact writer map

The historical P00 doc-writer owned this Spec, this Plan and TSK-0003 for the
first reviewable current-contract unit. The current COORD writer owns only this
Spec, this Plan and TSK-0006. TSK-0001, TSK-0002, TSK-0003 and TSK-0005 are
completed historical bodies and remain immutable. Existing operations bodies,
inventory, Registry, runtime and governance sources are read-only here.
No new Spec number is issued. Independent reviewers do not edit the patch. A delivery-receipt unit after
actual P00 merge may reconcile the frontmatter of TSK-0001/TSK-0002 from their
already accepted historical criteria, preserving both bodies byte-for-byte.
The current Task records their lifecycle edges and actual delivery separately;
this is no fresh execution or downstream native acceptance.

For downstream work, each acceptance owner assigns one implementation writer
before touching a shared path. P01 owns secret classification/prerequisites;
P02 owns metadata/path mappings; P03 owns root gateway, endpoint and port
contracts; P04 owns Airflow source/native integration; P05 owns n8n source/native
integration; P06 owns per-image consumption; P07 owns root-leaf controls and
exact exceptions. SEC01 owns P09 preparation documents, schemas, synthetic
fixtures and future acceptance contracts. It creates no external workspace,
Wiki engine, native application or production consumer. SMTP01 provides only
the canonical secret/consumer/catalog interface and reviews related P09
contracts; it does not duplicate P09 files. P10 owns a named input-to-recovery
consumer. These stage labels allocate no new Spec IDs or unnamed live targets.

Only one writer at a time may own `docker-compose.yml`, public environment
contracts, `.github/workflow-contract.yml`, `scripts/manifest.yaml`, the
Stage 99 Registry, document indexes, shared Alloy/gateway/backup configuration,
and both `infra/common-optimizations.yml` and
`infra/common-optimizations.exceptions.json`. P00 owns none of their implementation.
P07 reuses SPEC-0218 v2; no full common-file rewrite follows from this Plan.

For W14–W15, the coordinator writes only this package's Spec, Plan and
TSK-0006. Existing worktrees are evidence of possible concurrent ownership, not
permission to edit their paths. The lock map is: SEC01 image/digest/build;
P01 OpenBao TLS/custody; P02 catalog; SMTP01 canonical SMTP/alias; CLN01 exact
retirement; P03 common connection/port contracts; P04 SQL/DAG; P05 workflow and
SMTP node; P06 migration; P07 measurements/root leaves; P08 Stage05 moves; P10
acceptance fixtures; SPEC01 active-contract documents. The coordinator may
propose a shared-file change, but the lease holder integrates it after the
preceding source identity and review are fixed.

### Dependency and P08 integration order

1. P00 fixes baseline, ownership and exclusions first. Applied work stays
   NO_CHANGE and genuine gaps keep their existing acceptance owner.
2. P01 classification precedes P02 mappings and P06 actual secret consumption.
   P03 endpoint/port contracts precede their P04/P05 consumers; P09 references
   these contracts only for preparation. P07 uses
   observed demand and consumer prerequisites, with no invented optimal limits.
3. P04 and P05 native runs require actual connection/secret/recovery targets.
   Wiki preparation has no external workspace, native/app or production-consumer
   assignment. A future canonical SMTP interface may later name a consumer; P10
   consumes only verified interfaces and its named recovery fixture.
4. P08 selects exact current common/domain document destinations through the
   Registry. Finish a feature writer's edits and evidence before moving those
   paths; then one P08 writer moves documents and updates all references,
   indexes and applicable checks. Re-read SHA and hand the new paths back to
   the feature owner before any further edit. Do not edit old/new paths in
   parallel. P08 may move LAB documents to typed `labs/` destinations; LAB code,
   config, secrets and runtime are not moved.
5. Each feature owner completes its Task, independent review and per-Spec PR.
   P00's inventory or merge receipt cannot complete a downstream native run.

### R10 ownership and integration

The coordinator assigns one writer per slice. The documentation writer owns
this Spec, Plan and TSK-0007. Hook/CI implementation, Stage 99 and governance
contracts, and OpenBao source each have a distinct writer; the controller
integrates shared files and releases their lease before another writer edits.
No worktree path alone proves a lease released. Do not rewrite earlier Tasks.

Start with the Stage 99 stale authority prose and empty REQ-0024/AD-0030
scaffolding. Align new common-guidance language at its policy owner. Reproduce
pre-push multiple-ref/deletion behavior in an isolated repository. Independently
fix the OpenBao optional-skip contract and SPEC-0243 CA-overlay source wording.
The controller sequences any table/lifecycle/memory amendment after its exact
consumer impact and compatibility are reviewable; unimplemented targets stay
pending in TSK-0007 rather than being treated as completed by this Plan.

## Verification Plan

Run a value-free source-set audit, actual frontmatter parse and read-only PR
metadata before authoring. Observe the requirement-coverage/exclusion contract
probe fail on the baseline, then pass after the active-contract edits. Its
input SHA and result are recorded in the Task; no persistent snapshot test or
new service-count constant is added for this documentation change.

On the final source run document metadata/relationship/lifecycle checks,
local document links and `git diff --check`; select through the current changed
profile with `--explain`, without substituting a local aggregate candidate
run for the hosted PR. Run the existing agent-authority checker to establish
whether SPEC-0221 already meets the request. No public full/private env render,
LAB check, container run or secret read is part of P00.

W14–W15 add no live validation. They use tracked source and public Git metadata
only. HOME, migration, rotation, deletion, native workflow execution and empty
target restoration remain NOT_RUN until their owning Task identifies the exact
resource, approved operator/window, backup set and recovery boundary. A P08
document move waits for the feature-owner path freeze and a single move writer;
the confirmed duplicate README headings and stale domain wording are source
findings, not permission to move LAB runtime assets.

After independent review, validate the Conventional Commit message and run
`scripts/validation/run-ci-precommit.sh --mode local-staged` on the exact
staged set. Read actual branch protection and PR checks. Push this request's
branch, create its PR and attach it; merge only when its current review/check
conditions are satisfied. Record hosted results separately from local results.

For r10, select the smallest checks that establish each changed guarantee.
Content-only edits use changed metadata, relationships, links and diff checks;
Registry/parser/permission/workflow changes add their directly affected
regressions. Use synthetic repositories and DBs for failure probes. Record
actual commands, revisions, result and elapsed observations once. Hosted CI,
real provider effectiveness, HOME backup/restore and remote main protection
remain separate observations. Never create credentials or change managed
settings to make a source check pass.

## Risks and Recovery

### Risks and Rollback

Revert only the logical W13 documentation commit through a protected PR to
restore the prior active contract; preserve historical Tasks and issued IDs.
No service, credential, data, volume or host state changes, so no runtime/data
rollback is claimed. Equal baseline, merged draft and historical runtime PASS
must not be promoted to fresh validation. A concurrent shared-writer/path
change invalidates affected inputs and requires a fresh scoped check.

## Related Documents

- [Spec](spec.md)
- [R10 reconciliation Task](tasks/tsk-0007-r10-reconciliation.md)
- [SMTP01 request contract Task](tasks/tsk-0005-smtp01-request-contract.md)
- [Current coordination audit Task](tasks/tsk-0006-current-coordination-audit.md)
- [Completed P00 Task](tasks/tsk-0003-active-contract-and-exclusions.md)
- [Historical baseline Task](tasks/tsk-0001-request-baseline-and-inventory.md)
- [Historical twenty-item Task](tasks/tsk-0002-twenty-item-reconciliation.md)
- [Integration plan](../0204-service-integration-security-and-operations/plan.md)
