---
title: "Request Baseline and Reconciliation"
version: "1.0.1"
type: "sdlc/spec"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0212"
parent_ids:
- "REQ-0004"
- "REQ-0005"
- "REQ-0024"
- "REQ-0027"
- "AD-0004"
- "AD-0031"
created: "2026-10-07"
---

# Request Baseline and Reconciliation

## Overview

P00 reconciles requirements 11–26 supplied by the user on 2026-10-10 against
`d19fbfde605e257299aa2b39e25f2d7413a78221`. This package owns the baseline,
requirement routing and exclusions. Feature acceptance stays in its existing
owning Spec; P00 does not duplicate implementation. TSK-0001 and TSK-0002
preserve the earlier fifteen/twenty-item observations and prompt numbering.
Their historical learning-app routes grant no current planning or execution.

## Scope

Included: inspect root includes and service keys against the existing bounded
current inventory; parse actual open Spec/Plan/Task frontmatter; separate
source, evidence, merge and operation states; refresh this package and
SPEC-0204's active routing; assign serial shared writers and downstream order.

Excluded: all LAB code, configuration, data, secrets, execution, deletion and
document moves; civil-service exam, English and Japanese learning applications,
including planning; unrelated agent model updates. LAB may receive only a
separate document classification and prospective `separate_target` route in
P08. Influx retirement, n8n version alignment, DEV/MNG exporters, RedisInsight,
common controls v2 and the complete Stage 05 body refresh are `NO_CHANGE`
when existing evidence proves they are applied.

## Contracts

### Requirements 11–26

Each row has one primary execution owner and one disposition. Supporting
stages do not own the same acceptance criterion. The Task records evidence,
input revision and concrete residual targets; these rows are routing rather
than feature completion claims. A mixed request's primary disposition describes
its remaining work; applied sub-items are separately excluded in the Task.

| Requirement | Request | Primary | Disposition | Acceptance owner and supporting stages |
| --- | --- | --- | --- | --- |
| 11 | Service duplication and gaps | P07 | consumer-dependent | SPEC-0218 owns consumer-backed root leaf/control review; P00 reuses the supplied SERVICE_MATRIX and m0021 for SPEC-0212 source-set reconciliation, with no duplicate inventory |
| 12 | Service integration | P03 | consumer-dependent | SPEC-0204 owns integration; P04 Airflow, P05 n8n and P09 external Wiki provide consumed interfaces |
| 13 | Files, configuration and environment | P02 | confirmed-gap | SPEC-0204 owns secret/layout parity; P03 endpoint contracts and P06 actual consumption use the same owner |
| 14 | Additional configuration | P03 | consumer-dependent | SPEC-0204 owns named-consumer integration; P01 secret prerequisites and P07 resource prerequisites support it |
| 15 | User function from input through recovery | P10 | consumer-dependent | SPEC-0204 owns infrastructure recovery boundaries; P04, P05 and P09 own their native/app evidence, with the vertical slice assigned only after its real consumer is named |
| 16 | Airflow DEV/S3/DAG implementation | P04 | confirmed-gap | SPEC-0204 owns native Airflow acceptance for reference/dags, workflow_lib, sql and provision |
| 17 | n8n use and implementation | P05 | confirmed-gap | SPEC-0204 owns native import/execution for reference/n8n JSON and builder; existing version work is excluded |
| 18 | Resources and permissions | P07 | confirmed-gap | SPEC-0218 owns common controls; incremental root leaf work requires observed demand and no guessed limits or LAB edits |
| 19 | Both common controls files | P07 | applied-excluded | SPEC-0218 owns existing v2 and any proven root-leaf/exception increment; preserve both common files |
| 20 | Template format | P08 | applied-excluded | SPEC-0227 owns completed full Stage 05 body refresh; only changed-document/path checks remain |
| 21 | Incomplete Specs | P00 | confirmed-gap | SPEC-0212 owns lifecycle/source/evidence/merge/operation reconciliation; each existing Spec owns closure of its residuals |
| 22 | OpenBao migration and maintenance | P01 | consumer-dependent | SPEC-0204 owns per-consumer secret acceptance; P02 mapping and P06 consumption distinguish eligible, conditional, independent custody, unnecessary, candidate and excluded |
| 23 | Port distinctions | P03 | confirmed-gap | SPEC-0204 owns PORT_CONTRACT and port_inventory.py reconciliation; actual endpoint selection precedes runtime use |
| 24 | Active contract refresh | P00 | confirmed-gap | SPEC-0212 owns current routing; SPEC-0204 owns its amended integration contract; other changed Specs amend their own acceptance |
| 25 | Separate common, domain and LAB documents | P08 | confirmed-gap | SPEC-0212 owns the writer handoff; P08 selects exact Registry-compliant moves in its owning package; LAB is separate_target only |
| 26 | Exclude learning applications | P00 | out-of-scope | SPEC-0212 owns the global exclusion; every stage excludes planning, new files and resources for those applications |

### Evidence and authority

1. Re-read `origin/main`, remote `main`, worktree state and differences from
   the baseline at the start of each unit. An equal main does not make an old
   success or failure a newly executed test. Do not reset, stash or clean user work.
2. Compare only the actual root include/service set to the bounded
   `current-service-inventory`. Historical tables and service counts are not
   current source authority. No new service-count constant is introduced.
3. Classify residuals as `confirmed-gap`, `consumer-dependent`,
   `runtime-unverified`, `applied-excluded` or `out-of-scope`, with evidence
   path, input revision and real execution target. `NO_CHANGE` is the action
   for applied-excluded work; a merged draft alone proves no runtime acceptance.
4. Current user scope takes precedence over old local source-only, CI and
   prompt contracts. Revise conflicting policy, Registry, hooks, validators
   and tests together when a real conflict exists. SPEC-0221's existing
   authority implementation is reused, not reimplemented.
5. Source authoring and delivery are authorized within this request. Actual
   credentials, host actions, migration and recovery require the named target,
   effects and recovery boundary at their owning stage. Missing target/tool
   permission stops only that dependent operation. Do not invent permissions,
   secret values or recovery material.
6. Keep `SOURCE`, `UNIT`, `STATIC`, `ISOLATED`, `HOME`, `MIGRATION`,
   `RECOVERY` and `DELIVERY` separate. Secret path migration, source creation,
   reference wiring, actual consumption, rotation, recovery and merge are
   distinct states. Local PASS never means native service or remote CI PASS.
7. Registry profiles and language rules govern authoring: repository README
   and Stage 05 bodies remain Korean; Spec/Plan/Task bodies remain English.
   Preserve issued IDs, created dates and historical completed Task bodies.
   Reuse an existing owner; allocate a new Spec only through the actual Registry
   when new acceptance ownership is necessary, never reserve future numbers.
8. Run applicable regressions before implementation, commit each logical
   unit, create one PR per owning Spec and merge only after actual required
   checks and independent review. Shared writers and P08 moves are serialized
   as specified in the Plan; permission already supplied is not requested again.

## Acceptance Criteria

1. The current Task records local/remote baseline and worktree evidence,
   root/inventory set equality or exact differences, and private/LAB exclusions.
2. Requirements 11–26 have exactly one primary owner and disposition, with
   evidence-backed NO_CHANGE actions and concrete residual targets.
3. Every draft, in-progress or blocked Spec found from frontmatter has a
   source/evidence/merge/operation disposition. Stale-record reconciliation
   and code work are distinguished without rewriting completed Tasks.
4. SPEC-0204 and this package use the current request, CI and ownership
   contracts; genuine enforcer conflicts are fixed together or recorded absent.
5. The Plan names shared writers, execution dependencies, verification and
   rollback; the Task records commands, input SHA, outcomes, review and delivery,
   with unavailable downstream operations explicitly NOT_RUN.
6. The original baseline, inventory/profile and QA/protection observations
   remain identifiable in TSK-0001 as dated evidence. They are not re-executed
   by this contract; old criterion numbering is retained for evidence integrity.
7. The earlier twenty-item and open-Spec disposition remains identifiable in
   TSK-0002. Its older request/prompt routes are superseded by this contract;
   preserved learning-app mentions grant no current planning authority.

## Related Documents

- [Plan](plan.md)
- [Current P00 Task](tasks/tsk-0003-active-contract-and-exclusions.md)
- [Historical baseline Task](tasks/tsk-0001-request-baseline-and-inventory.md)
- [Historical twenty-item Task](tasks/tsk-0002-twenty-item-reconciliation.md)
- [Integration owner](../0204-service-integration-security-and-operations/spec.md)
- [Request precedence owner](../0221-request-precedence-and-enforcers/spec.md)
- [Home host requirement](../../01.requirements/0027-home-development-host.md)
- [Home host architecture](../../02.architecture/descriptions/0031-home-development-host.md)
