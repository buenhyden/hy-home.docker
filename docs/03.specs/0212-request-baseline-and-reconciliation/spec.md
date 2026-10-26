---
title: "Request Baseline and Reconciliation"
version: "1.5.2"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-26"
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

The earlier 11–30 request replaced P00's routing while preserving issued
IDs, created dates and completed Task bodies. The current coordination audit is
bound to main `262dc2dde6eea27195f7d8909e9453f5ccc97f66`, after PR #457 merged.
SEC01 delivery is prerequisite to the SMTP source transition, which precedes
CLN01 old-file deletion. Historical Tasks grant no current learning-app planning
or execution.

The r10 request dated 2026-10-15 extends this existing reconciliation owner
with P01–P08. Its starting HEAD is
`49f8dd661acf37bf292ee0aa59abfe1af16cde10`; TSK-0007 owns the new audit and
implementation evidence. Criteria 1–10 and their original decisions remain
historical facts. The direct r10 request authorizes this bounded local revision and
implementation; it does not establish WGOV-CORE/3.0.0 adoption or remote
authority. Independent implementation review and criterion acceptance remain
separate.

The direct infrastructure-audit request dated 2026-10-16 adds an independent
11–31 requirement namespace and the ordered `INFRA-P0` through `INFRA-P9`
coordination lane. Its requirement numbers 11–18 are not r10 criteria 11–18.
This package records cross-owner routing and P0 source evidence only; named
owners retain implementation and acceptance for their own leaf contracts.

The r13 request dated 2026-10-16 adds a follow-up current-source revalidation
criterion and Task. It began in a separate worktree while criterion 19/W24 was
issued; published main now preserves that allocation together with criterion
20/W25, without altering either Task's acceptance owner.

A follow-up request on the same date classifies the 2,870 links behind the
standing `historical-links-unrecorded` link warning. Criterion 21/W26 records
that classification in TSK-0010 without changing an archived body, the
retention catalog, or a checker.

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

### Current request scope (historical items 11–30)

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
| 20 | Template format | P08 | applied-excluded | P08 reuses SPEC-0227 criterion 1/W1/TSK-0001's accepted Stage05 template/schema/reader source; only changed-document/path checks remain |
| 21 | Incomplete Specs | SPEC01 | confirmed-gap | Current SPEC-0212 criterion 10 and TSK-0006 own lifecycle/source/evidence/merge/operation reconciliation; each existing Spec owns closure of its residuals |
| 22 | OpenBao migration and maintenance | P01 | consumer-dependent | SPEC-0204 owns per-consumer secret acceptance; P02 mapping and P06 consumption distinguish eligible, conditional, independent custody, unnecessary, candidate and excluded |
| 23 | Port distinctions | P03 | confirmed-gap | SPEC-0204 owns PORT_CONTRACT and port_inventory.py reconciliation; actual endpoint selection precedes runtime use |
| 24 | Active contract refresh | SPEC01 | confirmed-gap | Current SPEC-0212 criterion 9 and TSK-0006 own routing; SPEC-0204 owns its amended integration contract; other changed Specs amend their own acceptance |
| 25 | Separate common, domain and LAB documents | P08 | confirmed-gap | P08 moves LAB documents to typed `labs/` destinations with required READMEs and updated links/checks; LAB runtime remains excluded |
| 26 | Exclude learning applications | COORD | out-of-scope | Current SPEC-0212 criterion 9 and TSK-0006 own the global exclusion; every stage excludes planning, new files and resources for those applications |

Items 27–30 are execution constraints, not new numbered acceptance rows: use
the latest stable provider release, including compatible major/minor migrations
with recovery planning; delete legacy material only after source, runtime, jobs,
backup/restore and external consumers are confirmed absent. Disabled profiles
or absent traffic are not proof of no consumer.

That historical formulation predates the current infrastructure-audit route.
Criterion 9 records the historical numbered routes without changing the
accepted meaning of criteria 1–8. The direct current request supersedes its
restriction that an actual ROOT-image update needs a CVE, support end, or
required compatibility issue: every ROOT image is evaluated against its
official latest stable release. A compatibility, migration, consumer, or
recovery barrier may defer the update only when the owner records the exact
barrier, mitigation, review date, exit condition, and rollback boundary.
Latest-stable lookup does not itself prove a deployed, native, HOME, or
recovery result.

### Current infrastructure-audit routing (requirements 11–32)

`INFRA-P0` fixes common source boundaries before any variable source change;
`INFRA-P1` then protects data, secrets, backups, and recovery prerequisites.
The remaining phases are sequenced by the Plan. The source-evidence ladder is
`SOURCE_APPLIED`, `STATIC_PASS`, `ISOLATED_PASS`, `NATIVE_PASS`, `HOME_PASS`,
`RECOVERY_PASS`, `BLOCKED`, `OUT_OF_SCOPE`, `SUPERSEDED`, and `NOT_RUN`.
Lower-stage PASS never satisfies a higher-stage result.

| Requirement | Current primary owner | Current route and boundary |
| --- | --- | --- |
| 11 | SPEC-0218 / P07 | Consumer-backed root-leaf acceptance; SPEC-0212/P0 supplies the bounded inventory and route. |
| 12 | SPEC-0204 / P03 | Existing integration route; P0 maps the caller, contract, and verification leaf. |
| 13 | SPEC-0204 / P02 | Compose, secret, config, and consumer ownership reconciliation. |
| 14 | SPEC-0204 / P03 | Endpoint, ACL, S3, OIDC, resource, health, and upgrade prerequisites. |
| 15 | SPEC-0204 / P10 | Named input-to-recovery vertical acceptance; no P0 runtime claim. |
| 16 | SPEC-0204 / P04 | Existing Airflow DEV database/S3/DAG owner. |
| 17 | SPEC-0204 / P05 | Existing n8n outbox/SMTP owner. |
| 18 | SPEC-0218 / P07 | Measurement-backed resources, permissions, common controls, and exceptions. |
| 19 | SPEC-0218 / P07 | Existing v2 common-control owner; P0 only maps consumers and validation. |
| 20 | SPEC-0227 | Stage 05 template authority; SPEC-0204/P08 supports allowed document moves and LAB runtime remains excluded. |
| 21 | SPEC-0212 / P0 | Current lifecycle and acceptance inventory; each package retains residual closure. |
| 22 | SPEC-0204 / P01 | OpenBao classification; P02/P06 support mapping and consumer migration with rotation/recovery prerequisites. |
| 23 | SPEC-0204 / P03 | Listener, DNS, host, backend, and route-port contract owner. |
| 24 | SPEC-0212 / P0 | One-owner active-contract, consumer, and validation-route reconciliation. |
| 25 | SPEC-0204 / P08 | Operations-document layout and links; SPEC-0227 remains the template authority. |
| 26 | SPEC-0212 / P0 | Learning applications remain excluded from plans, code, data, and resources. |
| 27 | SEC01 | Official latest-stable, OCI identity, security, compatibility, migration, rollback, and evidence route; image owners implement approved changes. |
| 28 | SPEC-0204 / P09 criterion 13 / TSK-0008 | Offline Wiki preparation only; no Wiki service, database, API, UI, client, collector, or external workspace. |
| 29 | SMTP01 | Canonical SMTP source and real-consumer verification; retirement remains separate. |
| 30 | CLN01 | Retirement only after consumer, backup, external dependency, authorization, and recovery evidence. |
| 31 | SPEC-0204 / SEC01 (TSK-0009) image owner | Every actual ROOT-image change carries matching configuration, tests, templates, Guide, Policy, Runbook, and README updates in its logical unit; P08 checks documentation structure. Owner rerouted from P09 on 2026-10-21. |
| 32 | SPEC-0246 / TSK-0001 | Reuse accepted storage moves and measurements; criterion 6 owner acceptance, retained HDD-copy disposition, and dependent W6 policy promotion remain separate. |

The direct v30 request of 2026-10-26 extends existing criterion 19/W24 in
TSK-0008 to requirement 32 and the F01–F29 audit namespace. Completed
TSK-0006 criteria 9–10 and all other completed Task bodies remain unchanged.
The existing packaged requirements/crosswalk are source inputs; this Task
records current execution and hands each residual to its existing owner.
Prompt coverage, source implementation, actual verification and acceptance
remain four independent observations. A classified source survey may admit
an exact reversible source/test unit after its required review; missing
Native/HOME, private facts or operational authority block only dependent work.

For this v30 execution, delivery is local logical commits and per-Spec review
drafts. Remote push, PR mutation, merge, release and deployment require separate
direct authorization. Earlier remote-delivery instructions below retain their
historical scope and grant no current remote action. The two external app
planning instructions are reused outside tracked implementation; neither they
nor Template readiness authorizes application or sibling-repository changes.

### Current coordination audit

The current audit is a source-routing and handoff record, not a replacement for
the named owners' source, native, HOME, migration, rotation, recovery or
delivery evidence. Its classifications are prose results: `SOURCE_APPLIED`
means the reviewed source is already present; `CONFIRMED_GAP` names a concrete
source/document discrepancy; `RUNTIME_UNVERIFIED` retains a required target or
recovery boundary; `COMPLETE_FOR_SCOPE` closes only the stated coordination
scope; and `OUT_OF_SCOPE` records an excluded lane. They do not alter document
metadata or acceptance domains.

The coordinator owns this package's routing, source identity and handoff only.
SEC01 owns image/digest/build evidence; P01 owns OpenBao TLS, custody and
maintenance boundaries; P02 owns the value-free catalog; SMTP01 owns the
canonical SMTP source and alias; CLN01 owns the exact deletion assessment; P03
owns endpoint/port contracts; P04 owns SQL/DAG; P05 owns workflow/SMTP node;
P06 owns value migration; P07 owns root-leaf measurement; P08 owns Stage05
document moves; P10 owns the vertical acceptance; and SPEC01 owns active
contract reconciliation. `docker-compose.yml`, the Stage 99 Registry, shared
indexes and shared Tasks require an explicit single-writer lease before change.
Existing worktrees show activity but do not prove a writer is active; unknown
activity remains a handoff fact rather than an inferred lock release.

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

### R10 reconciliation boundaries

P01–P08 are purposes within this package, not eight new Specs. Preserve
existing feature owners, issued IDs, historical failures and acceptance.
Reversible source, documentation, governance and scoped checker changes are
authorized by the direct request. Remote push, PR, merge, publication,
deployment, credentials, managed/global settings and actual data removal
retain their action-specific authorization boundary. Unknown execution and
approval evidence remain unknown; a local source PASS does not replace them.

The current local Stage 99 Registry remains the executable input while the
r10 target changes are made concrete. Record the proposed Evidence `Required`
column and result-domain changes, Criterion Acceptance `Current Owner`,
Execution Items columns, lifecycle edges and role headings as a coupled
Registry/schema/template/reader/test amendment. No revised shared meaning is
silently issued as an already approved WGOV-CORE/3.0.0 contract. Existing
records retain their original generation and acceptance meaning.

P02 also reconciles the language owner for new common agent explanations
with the request's Korean default; it does not bulk-translate old instructions
or frozen records. Existing memory source, physical store and backup remain
in place; no repeat native-memory migration or private-body audit is implied.
P04 retires an asset only after its current consumers, retained assurance,
hold, authorization and recovery requirements have been established.

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
9. A current Task maps requirements 11–30 to one existing owner, criterion,
   Plan unit, Task, state/evidence location, source target, verification leaf,
   unresolved lane and prose classification. It also records writer/lock
   ownership, open-worktree uncertainty, unsafe-resource and recovery
   boundaries, and the sequencing before shared files, migrations, rotations,
   deletions or document moves. The audit uses the current main identity and
   never treats source or historical evidence as a runtime result.
10. A current Task inventories every tracked package with a draft or in-review
    Spec or Plan, a ready, in-progress or blocked Task or Execution Item, and
    every approved parent with a nonterminal Task or item. It treats Spec/Plan
    state as approval and Task/item state as execution, records the actual
    source/static checks it ran, and hands the exact next input to the owner
    without creating a duplicate acceptance record.

11. P01 binds the actual branch, HEAD, index/worktree, historical delta,
    request identity and available authority to a classified finding map;
    recorded shared approval and local adoption are separate claims.
12. P02 corrects current role/language/template/link conflicts at their
    canonical owner and affected consumers; coupled contract changes preserve
    historical records and distinguish proposed shared meaning from approval.
13. P03 reconciles Task execution, criterion acceptance and parent authority
    against actual evidence, including SPEC-0241 and SPEC-0236/0237, without
    converting a merge, static PASS or old approval into a new acceptance.
14. P04 assesses completed/superseded units and temporary QA by direct
    consumers and required assurances, promotes durable meaning and performs
    only justified, authorized retention or retirement with source preserved.
15. P05 maps Git/native hooks and hosted jobs to actual inputs and leaf
    producers, fixes reproduced push-stage or duplicate-call defects, and
    distinguishes declared, installed, synthetic and real-push observations.
16. P06 identifies the actual branch/change/release/CHANGELOG producers and
    authorization boundary; source corrections preserve main protection,
    immutable history and separate release, deployment and recovery results.
17. P07 reuses SPEC-0236/0237 memory and backup records, assesses native-off,
    shared-store identity, freshness, conflict, capacity and secret boundaries,
    and implements justified gaps with synthetic data; private bodies and
    actual provider acceptance remain outside unobserved claims.
18. P08 corrects demonstrated OpenBao/operations source discrepancies while
    retaining service-specific security and recovery checks; purpose quality
    measures and durable owner promotion trace actual evidence and limits.
19. TSK-0008 records an `INFRA-P0` source snapshot for requirements 11–32:
    root/inventory scope, one current owner route per requirement, changed-file
    to test/gate/rollback mapping, shared-writer leases, evidence ladder, and
    the distinct F01–F29 audit routes, and explicit pending native, HOME,
    recovery, and delivery boundaries. It does
    not alter historical r10 criteria 11–18 or claim downstream execution.
20. TSK-0009 classifies current P01-P08 follow-up findings, removes a
    demonstrated same-input link-graph duplicate, and corrects memory-source
    revision trust and CLI shared-store identity only with scoped regression and
    CI-consumer checks. It keeps
    historical criteria 11-18 unchanged, records unavailable checks as
    NOT_RUN, and leaves runtime, remote, and named leaf-owner acceptance
    outside this criterion.
21. TSK-0010 classifies every link counted by the `historical-links-unrecorded`
    warning against its pre-archive Git origin, separates links proven to
    resolve historically from the residual set, and names the cause it can
    prove. It changes no archived body, retention-catalog row, or checker, and
    it does not convert the warning into a failure or a pass.

## Failure Conditions

Reconciliation fails when a request item has competing acceptance owners,
a source or historical receipt is presented as fresh runtime acceptance, or
shared paths change without the assigned writer. Learning-app work, actual
Wiki implementation, unproven consumer retirement and unnamed operational
targets remain outside the routed execution boundaries.

The infrastructure-audit coordination also fails if a ROOT-image result is
called current without an official release/source date and compatibility
assessment, a lower evidence stage is promoted, a shared path changes without
its lease, or a destructive/secret/live action proceeds without its named
target, backup, recovery boundary, and action-specific authorization.

## Related Documents

- [Plan](plan.md)
- [R10 reconciliation Task](tasks/tsk-0007-r10-reconciliation.md)
- [Infrastructure audit execution Task](tasks/tsk-0008-infra-audit-execution.md)
- [Historical link classification Task](tasks/tsk-0010-historical-link-classification.md)
- [SMTP01 request contract Task](tasks/tsk-0005-smtp01-request-contract.md)
- [Current coordination audit Task](tasks/tsk-0006-current-coordination-audit.md)
- [Completed P00 Task](tasks/tsk-0003-active-contract-and-exclusions.md)
- [Historical baseline Task](tasks/tsk-0001-request-baseline-and-inventory.md)
- [Historical twenty-item Task](tasks/tsk-0002-twenty-item-reconciliation.md)
- [Integration owner](../0204-service-integration-security-and-operations/spec.md)
- [Request precedence owner](../0221-request-precedence-and-enforcers/spec.md)
- [Home host requirement](../../01.requirements/0027-home-development-host.md)
- [Home host architecture](../../02.architecture/descriptions/0031-home-development-host.md)
