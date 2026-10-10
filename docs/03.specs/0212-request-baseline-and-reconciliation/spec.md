---
title: "Request Baseline and Reconciliation"
version: "1.1.0"
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

The current 11–30 request replaces P00's active routing while preserving issued
IDs, created dates and completed Task bodies. SEC01 delivery is prerequisite to
the SMTP source transition, which precedes CLN01 old-file deletion. Historical
Tasks grant no current learning-app planning or execution.

## Scope

LLM Wiki work is preparation only: documentation, schema, connection contract,
synthetic fixtures and future acceptance criteria are allowed. Wiki Core/API/UI,
search, embeddings, collectors, application databases, production clients,
n8n Wiki reservations, blog-data writes and external workspace creation are
excluded. Requirements 16 and 17 are independent `opsflow_dev` manifest
validation, publication and notification jobs, not a Wiki engine or database.
LAB runtime is excluded; P08 may make actual typed `labs/` document moves with
required READMEs, links, Registry and path checks. Learning applications remain
excluded, including planning.

## Contracts

### Current request scope (items 11–30)

Each row has one primary execution owner and one disposition. Supporting
stages do not own the same acceptance criterion. The Task records evidence,
input revision and concrete residual targets; these rows are routing rather
than feature completion claims. A mixed request's primary disposition describes
its remaining work; applied sub-items are separately excluded in the Task.

| Requirement | Request | Primary | Disposition | Acceptance owner and supporting stages |
| --- | --- | --- | --- | --- |
| 11 | Service duplication and gaps | P07 | consumer-dependent | SPEC-0218 owns consumer-backed root leaf/control review; P00 reuses the supplied SERVICE_MATRIX and m0021 for SPEC-0212 source-set reconciliation, with no duplicate inventory |
| 12 | Service integration | P03 | consumer-dependent | SPEC-0204 owns integration; P04/P05 own independent `opsflow_dev` jobs; Wiki preparation has no external workspace, native/app assignment or production consumer |
| 13 | Files, configuration and environment | P02 | confirmed-gap | SPEC-0204 owns secret/layout parity; P03 endpoint contracts and P06 actual consumption use the same owner |
| 14 | Additional configuration | P03 | consumer-dependent | SPEC-0204 owns named-consumer integration; P01 secret prerequisites and P07 resource prerequisites support it |
| 15 | User function from input through recovery | P10 | consumer-dependent | SPEC-0204 owns infrastructure recovery boundaries; a future canonical SMTP interface may supply a named consumer, but no Wiki native/app assignment exists here |
| 16 | Airflow DEV/S3/DAG implementation | P04 | confirmed-gap | SPEC-0204 owns an independent `opsflow_dev` manifest validation, publication and notification job; it is not Wiki implementation |
| 17 | n8n use and implementation | P05 | confirmed-gap | SPEC-0204 owns an independent `opsflow_dev` manifest validation, publication and notification job; it is not Wiki implementation |
| 18 | Resources and permissions | P07 | confirmed-gap | SPEC-0218 owns common controls; incremental root leaf work requires observed demand and no guessed limits or LAB edits |
| 19 | Both common controls files | P07 | applied-excluded | SPEC-0218 owns existing v2 and any proven root-leaf/exception increment; preserve both common files |
| 20 | Template format | P08 | applied-excluded | SPEC-0227 owns completed full Stage 05 body refresh; only changed-document/path checks remain |
| 21 | Incomplete Specs | P00 | confirmed-gap | SPEC-0212 owns lifecycle/source/evidence/merge/operation reconciliation; each existing Spec owns closure of its residuals |
| 22 | OpenBao migration and maintenance | P01 | consumer-dependent | SPEC-0204 owns per-consumer secret acceptance; P02 mapping and P06 consumption distinguish eligible, conditional, independent custody, unnecessary, candidate and excluded |
| 23 | Port distinctions | P03 | confirmed-gap | SPEC-0204 owns PORT_CONTRACT and port_inventory.py reconciliation; actual endpoint selection precedes runtime use |
| 24 | Active contract refresh | P00 | confirmed-gap | SPEC-0212 owns current routing; SPEC-0204 owns its amended integration contract; other changed Specs amend their own acceptance |
| 25 | Separate common, domain and LAB documents | P08 | confirmed-gap | P08 moves LAB documents to typed `labs/` destinations with required READMEs and updated links/checks; LAB runtime remains excluded |
| 26 | Exclude learning applications | P00 | out-of-scope | SPEC-0212 owns the global exclusion; every stage excludes planning, new files and resources for those applications |

Items 27–30 are execution constraints, not new numbered acceptance rows: use
the latest stable provider release, including compatible major/minor migrations
with recovery planning; delete legacy material only after source, runtime, jobs,
backup/restore and external consumers are confirmed absent. Disabled profiles
or absent traffic are not proof of no consumer.

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
9. Preserve OpenBao TLS, wrapped reauthentication, functional readiness, audit
   and snapshot work delivered by PRs #409/#410; residual HOME and migration/
   recovery verification remains separate work.

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
8. The active routing records Wiki preparation, independent `opsflow_dev` jobs,
   P08 LAB document moves, latest-stable planning, consumer-confirmed deletion,
   and the SEC01 → SMTP source transition → CLN01 sequence.

## Related Documents

- [Plan](plan.md)
- [SMTP01 request contract Task](tasks/tsk-0005-smtp01-request-contract.md)
- [Completed P00 Task](tasks/tsk-0003-active-contract-and-exclusions.md)
- [Historical baseline Task](tasks/tsk-0001-request-baseline-and-inventory.md)
- [Historical twenty-item Task](tasks/tsk-0002-twenty-item-reconciliation.md)
- [Integration owner](../0204-service-integration-security-and-operations/spec.md)
- [Request precedence owner](../0221-request-precedence-and-enforcers/spec.md)
- [Home host requirement](../../01.requirements/0027-home-development-host.md)
- [Home host architecture](../../02.architecture/descriptions/0031-home-development-host.md)
