---
title: "Request Baseline and Reconciliation Plan"
version: "1.0.1"
type: "sdlc/plan"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0212-PLAN-0001"
parent_ids:
- "SPEC-0212"
created: "2026-10-07"
---

# Request Baseline and Reconciliation Plan

## Overview

Execute the 2026-10-10 P00 contract in SPEC-0212-TSK-0003. The earlier W1–W8
baseline and twenty-item work remain preserved in TSK-0001/TSK-0002 and Git
history. This Plan supersedes their prompt order and LAB/application discovery
routes for current execution, without changing their recorded results.

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

### Exact writer map

The P00 doc-writer owns only this Spec, this Plan, TSK-0003, and
`../0204-service-integration-security-and-operations/{spec,plan}.md` and
`../0220-crawl4ai-collection-and-egress/plan.md` in the first reviewable
current-contract unit. The latter removes an active learning-app candidate. Existing Tasks, operations bodies,
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
exact exceptions. P09 owns the external Wiki in a Project-Template-derived
workspace; P10 owns a named input-to-recovery consumer. These stage labels do
not allocate new Spec IDs or authorize unnamed live targets.

Only one writer at a time may own `docker-compose.yml`, public environment
contracts, `.github/workflow-contract.yml`, `scripts/manifest.yaml`, the
Stage 99 Registry, document indexes, shared Alloy/gateway/backup configuration,
and both `infra/common-optimizations.yml` and
`infra/common-optimizations.exceptions.json`. P00 owns none of their implementation.
P07 reuses SPEC-0218 v2; no full common-file rewrite follows from this Plan.

### Dependency and P08 integration order

1. P00 fixes baseline, ownership and exclusions first. Applied work stays
   NO_CHANGE and genuine gaps keep their existing acceptance owner.
2. P01 classification precedes P02 mappings and P06 actual secret consumption.
   P03 endpoint/port contracts precede their P04/P05/P09 consumers. P07 uses
   observed demand and consumer prerequisites, with no invented optimal limits.
3. P04 and P05 native runs require actual connection/secret/recovery targets.
   P09 requires its external workspace; P10 consumes verified interfaces and
   its named recovery fixture. Missing targets defer only their dependent lane.
4. P08 selects exact current common/domain document destinations through the
   Registry. Finish a feature writer's edits and evidence before moving those
   paths; then one P08 writer moves documents and updates all references,
   indexes and applicable checks. Re-read SHA and hand the new paths back to
   the feature owner before any further edit. Do not edit old/new paths in
   parallel. LAB receives only `separate_target` classification and prospective
   path metadata; its actual documents, code, config and secrets are not moved.
5. Each feature owner completes its Task, independent review and per-Spec PR.
   P00's inventory or merge receipt cannot complete a downstream native run.

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

After independent review, validate the Conventional Commit message and run
`scripts/validation/run-ci-precommit.sh --mode local-staged` on the exact
staged set. Read actual branch protection and PR checks. Push this request's
branch, create its PR and attach it; merge only when its current review/check
conditions are satisfied. Record hosted results separately from local results.

## Risks and Rollback

Revert only the logical P00 documentation commits through a protected PR to
restore the prior active contract; preserve historical Tasks and issued IDs.
No service, credential, data, volume or host state changes, so no runtime/data
rollback is claimed. Equal baseline, merged draft and historical runtime PASS
must not be promoted to fresh validation. A concurrent shared-writer/path
change invalidates affected inputs and requires a fresh scoped check.

## Related Documents

- [Spec](spec.md)
- [Current P00 Task](tasks/tsk-0003-active-contract-and-exclusions.md)
- [Historical baseline Task](tasks/tsk-0001-request-baseline-and-inventory.md)
- [Historical twenty-item Task](tasks/tsk-0002-twenty-item-reconciliation.md)
- [Integration plan](../0204-service-integration-security-and-operations/plan.md)
