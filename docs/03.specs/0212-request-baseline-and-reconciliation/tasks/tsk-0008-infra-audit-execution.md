---
title: "Infrastructure Audit Execution Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0008"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-16"
---

# Infrastructure Audit Execution Task

## Overview

### Objective

Execute `INFRA-P0` only: establish a current, value-free source snapshot and
single-owner routing for infrastructure requirements 11–31 before P1 or any
variable source change. This Task owns SPEC-0212 criterion 19. It does not
reopen historical Task bodies or r10 criteria 11–18, and it does not accept
leaf implementation, native, HOME, recovery, hosted delivery, or remote
protection results.

## Inputs and Authorization

The direct user supplied an independent infrastructure-audit prompt identified
by SHA-256 `ea9ddbdd8db5ea93b2e8858c477d223e2ea877cdccd99c7c1e86a22303cc4935`.
It authorizes source, tests, documentation, logical commits, a SPEC-0212
feature branch, and delivery after gates. It excludes remote-protection
changes, secret values and credential mutation, live destructive actions,
rotation, migration, deployment, and recovery until the owning operation
records concrete prerequisites. Value-free secret metadata checks remain in
scope.

The coordinator created `feature/spec-0212-infra-audit` from clean main
`e6807a7d16d8b9e180ff58456ab64e4ee721ca69` after `git fetch origin main`.
At that baseline, open pull requests were empty and no extra worktree or
unpublished commit was observed. The earlier r10 criteria 11–18 use another
namespace and do not prove infrastructure requirements 11–18.

At approximately 2026-10-16 00:49 KST, the tracked/index frontmatter census
at this base plus this staged Task found 36 Specs (13 approved, 23 draft), 36
Plans (13 approved, 23 draft), and 65 Tasks (16 completed, 3 blocked, 11
in-progress, 34 draft, and this Task in-progress). The approved package IDs
are `0182`, `0204`, `0207`–`0212`, `0230`–`0233`, and `0242`; every other
current package Spec is draft. This is a lifecycle/source inventory, not an
acceptance-PASS claim: each draft or nonterminal record retains its own
criteria, evidence, merge, and operation disposition under its primary owner.

## Work Log

### P0 execution state

W24 source preparation is active while this newly issued Task remains `draft`
under the lifecycle contract. Its scope is source inventory, owner routing,
shared leases, evidence ladder, QA/CI mapping, and P1–P9 handoff. Final P0
source findings and independent review remain pending; they do not block
unrelated, reversible owner source/test/document work. P1 blocks only live or
irreversible operations until its named prerequisites are met.

### Current P0 source snapshot

The bounded current-service inventory projection records 43 root Compose
includes, 13 infrastructure layers, and 111 services. Its service rows are
source inventory evidence, not native runtime proof: 83 consumer cells and 81
backup cells are explicitly unverified or `NOT_RUN`. Current source inventory
also records 84 secret declarations, 19 networks, 65 profiles, 71 image
strings, 30 build consumers, and 21 distinct build objects. No P0 operation
prints secret values, rendered private environment, or authentication headers.

The direct request replaces the historical "security warning only" update
restriction. Every ROOT image proceeds through official latest-stable,
OCI-identity, compatibility, migration, rollback, and consumer assessment.
For example, the current official n8n lookup is 2.43.6, published
2026-10-15T07:26:03Z, non-prerelease; it is a P2 candidate, not an update or
runtime-success claim. A real compatibility barrier must name its mitigation,
review date, exit condition, and rollback boundary.

P0 also preserves two current implementation blockers for their existing
owners: the n8n 2.42.7 bundle and related custom-node package/lock remain a
coupled P2 source change, and the P04/P05 outbox currently omits its SQL
`lease_until` contract while uncertain post-send outcomes can be retried. P04
owns the versioned SQL/manual-reconciliation correction and P05 owns its
consumer contract; neither is accepted here.

### Requirement routes and shared leases

| Requirements | Primary owner | P0 route | Next boundary |
| --- | --- | --- | --- |
| 11 | SPEC-0218 / P07 | Consumer-backed root-leaf acceptance; P0 supplies bounded inventory | Existing leaf acceptance. |
| 12 | SPEC-0204 / P03 | Integration caller, contract, and verification route | P1 review, then named source/native Task. |
| 13 | SPEC-0204 / P02 | Compose, secret, config, and consumer route | P1 review, then named source/native Task. |
| 14 | SPEC-0204 / P03 | Endpoint, ACL, S3, OIDC, resource, health, and upgrade prerequisites | P1 review, then named source/native Task. |
| 15 | SPEC-0204 / P10 | Input-to-recovery vertical acceptance | Native/HOME/recovery remains pending. |
| 16 | SPEC-0204 / P04 | Airflow DEV database/S3/DAG | Existing source/native Task. |
| 17 | SPEC-0204 / P05 | n8n outbox/SMTP | Existing source/native Task. |
| 18 | SPEC-0218 / P07 | Resource and permission controls | Measured demand required. |
| 19 | SPEC-0218 / P07 | Common controls and exceptions | Measured demand required. |
| 20 | SPEC-0227 | Template authority; P08 supports layout paths | LAB runtime excluded. |
| 21 | SPEC-0212 / P0 | Lifecycle inventory | Package owners retain residual closure. |
| 22 | SPEC-0204 / P01 | OpenBao classification | P02/P06 support mapping and consumption. |
| 23 | SPEC-0204 / P03 | Listener, DNS, host, backend, and route ports | Existing contract owner. |
| 24 | SPEC-0212 / P0 | Active-contract and validation routing | Package owners retain residual closure. |
| 25 | SPEC-0204 / P08 | Operations-document layout and links | SPEC-0227 supports templates. |
| 26 | SPEC-0212 / P0 | Learning application exclusion | No app plan/code/data/resources. |
| 27 | SEC01 | Latest-stable and OCI/compatibility assessment | Image owner changes only after prerequisites. |
| 28 | SPEC-0204 / P09 criterion 13 / TSK-0008 | Offline Wiki preparation only | Wiki implementation and external workspace remain out of scope. |
| 29 | SMTP01 | Canonical source plus actual-consumer verification | Separate authorized retirement assessment. |
| 30 | CLN01 | Consumer, backup, external-dependency, authorization, recovery evidence | No deletion from profile-off or no-traffic observation. |
| 31 | SPEC-0204 / P09 | Same-unit Guide, Policy, Runbook, README, template, test, and configuration route | P08 supports layout; runs with each actual image change. |

### Requirement source, gate, and blocker trace

| Requirement | Current source / Task | Validator or gate | P0 state and blocker |
| --- | --- | --- | --- |
| 11 | `m0021` / SPEC-0218 P07 | Operations catalog and leaf contracts | SOURCE_APPLIED; consumer acceptance remains owner work. |
| 12 | SPEC-0204 P03 | Service-wiring and port contracts | NOT_RUN; named integration target required. |
| 13 | SPEC-0204 P02 | Secret catalog and Compose contracts | FAIL; catalog view drift is unresolved. |
| 14 | SPEC-0204 P03 | Endpoint/ACL/health contracts | NOT_RUN; target prerequisites pending. |
| 15 | SPEC-0204 P10 | Opsflow E2E acceptance | FAIL; lease/unknown-message correction pending. |
| 16 | SPEC-0204 P04 | Airflow contract/rehearsal tests | SOURCE_APPLIED; native target remains pending. |
| 17 | SPEC-0204 P05 | n8n outbox/rehearsal tests | FAIL; P04/P05 coupled lease handoff pending. |
| 18 | SPEC-0218 P07 | Root-resource contract | NOT_RUN; measured demand absent. |
| 19 | SPEC-0218 P07 | Common-control contract | NOT_RUN; measured demand absent. |
| 20 | SPEC-0227 | Metadata, catalog, and link checks | STATIC_PASS; no eligible move is leased. |
| 21 | Current Spec inventory | Metadata/lifecycle parser | SOURCE_APPLIED; package closures remain owner work. |
| 22 | SPEC-0204 P01 | OpenBao consumer-migration contract | NOT_RUN; secret/restore boundary absent. |
| 23 | SPEC-0204 P03 | `test_port_contract.py` | SOURCE_APPLIED; runtime listener proof pending. |
| 24 | SPEC-0212 P0 | Document/CI route checks | FAIL; CI routed regressions remain open. |
| 25 | SPEC-0204 P08 | Operations catalog, metadata, links | STATIC_PASS; document path freeze required. |
| 26 | SPEC-0212 P0 | Scope and changed-path review | SOURCE_APPLIED; no learning-app work admitted. |
| 27 | SEC01 | Version/security/OCI contracts | NOT_RUN; official lookup and compatibility ledger pending. |
| 28 | SPEC-0204 P09 TSK-0008 | Offline preparation contract | SOURCE_APPLIED; implementation excluded. |
| 29 | SMTP01 | SMTP contract/rehearsal | NOT_RUN; consumer verification pending. |
| 30 | CLN01 | Consumer/backup/retirement contract | NOT_RUN; consumer and recovery evidence absent. |
| 31 | SPEC-0204 P09 | Changed-image documentation and CI route | NOT_RUN; no image change is accepted. |

`docker-compose.yml`, `.env.example`, catalogs/exceptions, Stage 99 Registry,
Stage 05 indexes, shared scripts, and CI contracts require one named writer.
The coordinator (`/root/coordination_docs`) owns only this Spec, Plan, and Task
on `feature/spec-0212-infra-audit`. Read-only P0 contributors are
`/root/inventory_analysis`, `/root/ci_audit`, and `/root/workflow_analysis`;
they hold no write lease. No task-level token, time, or rate limit is known;
no ceiling is invented or used to release a lease.

### Evidence domains, stop, and recovery boundaries

The evidence ladder is `SOURCE_APPLIED`, `STATIC_PASS`, `ISOLATED_PASS`,
`NATIVE_PASS`, `HOME_PASS`, `RECOVERY_PASS`, `BLOCKED`, `OUT_OF_SCOPE`,
`SUPERSEDED`, and `NOT_RUN`. A lower stage never closes a higher stage. P0
stops the dependent operation when its resource, operator/window, backup
identity, restore boundary, compatibility result, or action-specific approval
is missing. Secret rotation, data migration, retirement, and live upgrades
require their owner’s rollback plan; an isolated documentation rollback does
not restore runtime data.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| main-baseline | 19 | W24 | `git fetch origin main`; source/branch/worktree/open-PR observation | `e6807a7d16d8b9e180ff58456ab64e4ee721ca69` | PASS | Task inputs and coordinator observation | required | - |
| document-baseline | 19 | W24 | Active metadata, operations catalog, and all-link checks before P0 edits | baseline `e6807a7` | PASS | Metadata 576 selected/0 violations; catalog PASS; links 1,310 documents/11,677 links/0 failures and 1 historical warning (2,870 links lack capture source) | required | - |
| current-service-inventory | 19 | W24 | Bounded source projection and `scripts/lib/ops/port_inventory.py` | baseline `e6807a7` | PASS | `docs/90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md`; generated temporary output is not durable evidence | required | - |
| secret-catalog-views | 19 | W24 | Value-free secret-catalog public validation and view check | baseline `e6807a7` | FAIL | Prepared dependency environment: metadata valid for 145 entries/1 alias; `check-views` exits 2 with `P02_VIEW_DRIFT` in ignored operator staging, not runtime evidence or a source repair | required | - |
| ci-local-context | 19 | W24 | `python3 scripts/validation/run-ci-gate.py --profile changed --requirements` without invented PR context | baseline `e6807a7` | FAIL | Exit 1: hosted prerequisites require a pull-request context; no fake CI variables used | required | - |
| remote-protection | 19 | W24 | Authenticated branch-protection/rules readback | baseline `e6807a7` | PASS | `strict=true`, empty required contexts/checks, admin enforcement and conversation resolution observed; no mutation | required | - |
| root-hardening-coverage | 19 | W24 | Existing hardening script tier coverage | baseline `e6807a7` | FAIL | Script passes its 01–12 list but omits `infra/13-experience`; owner must add P8 route and regression | required | - |
| ci-routing-regressions | 19 | W24 | Registered CI gate and SMTP routing unit suites | baseline `e6807a7` | FAIL | CI contract expected-route drift and SMTP optional-runtime count drift; QA/CI owner routes fixes before P8 acceptance | required | - |
| workflow-source-suite | 19 | W24 | Focused Airflow/n8n/P10 source suites | baseline `e6807a7` | PASS | `python3 -m unittest` focused suite: 108 tests, exit 0; no source mutation | required | - |
| workflow-isolated-denial | 19 | W24 | `env OPSFLOW_PG_REHEARSAL_IMAGE=sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873 OPSFLOW_PG_REHEARSAL_CONTEXT=default python3 -m unittest tests.validation.test_opsflow_database_rehearsal.OpsflowDatabaseNativeRehearsal -v` | baseline `e6807a7` | FAIL | 2 tests: restore/ACL PASS; cross-database denial failed; three owned containers cleaned up | required | - |
| native-home-recovery | 19 | W24 | Native service, HOME flow, and isolated restore result | No named live target in P0 | NOT_RUN | Deferred to owning P1–P10 Tasks | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 19 | pending | main-baseline, document-baseline, current-service-inventory, secret-catalog-views, ci-local-context, remote-protection, root-hardening-coverage, ci-routing-regressions, workflow-source-suite, workflow-isolated-denial, native-home-recovery | P0 routing is in progress; required failures and unrun higher evidence domains remain open. | SPEC-0212 coordinator for routing; named primary owners for execution. |

## Review and Completion

Independent review must verify that every requirement 11–31 has exactly one
primary owner, all shared-file leases are explicit, and the P0 snapshot does
not promote source/static observations into native, HOME, recovery, hosted, or
remote-protection acceptance. The coordinator then runs the document checks and
changed selector for this exact diff, records command/result/input revision,
and makes one logical documentation commit. No push, PR, merge, remote setting,
or live operation is performed by this Task record.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [R10 reconciliation Task](tsk-0007-r10-reconciliation.md)
- [Current coordination audit Task](tsk-0006-current-coordination-audit.md)
- [Bounded service inventory](../../../90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md)
- [Integration owner](../../0204-service-integration-security-and-operations/spec.md)
