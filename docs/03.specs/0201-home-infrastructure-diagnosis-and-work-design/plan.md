---
title: "Home Infrastructure Diagnosis and Work Design Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0201-PLAN-0001"
parent_ids:
- "SPEC-0201"
created: "2026-10-02"
---

# Home Infrastructure Diagnosis and Work Design Plan

## Objective

W1-W6 produced the source diagnosis, service-role rulings, integration
manifest proposal, and handoffs. W7.1-W7.3 close the runtime facts required
before Prompt 02 source work. The owner deferred W7.4's isolated restore
measurement to a later operational Task without treating it as PASS. This Plan changes neither Compose nor HOME
infrastructure and never migrates data. W7 is separate from the prior W1-W6 approval. The user approved W7.1-W7.3
read-only observation on 2026-10-02; W7.4 isolated restore still requires
its own exact preflight and execution approval.

## Dependencies

- Approved SPEC-0201 at the recorded baseline. W1-W6 and W7.1-W7.3 have
  explicit execution approval recorded in their Tasks despite initial draft
  frontmatter; W7.4 restore has no execution approval.
- The latest main and work-branch SHA, checked before evidence is used.
- Current tracked source, active lifecycle documents, and official vendor
  material current on the inspection date.
- W1-W6 used tracked source only. W7 may use approved, sanitized aggregate
  live metadata and host capacity numbers; actual .env values, credentials,
  auth files, raw operational logs, row contents, and traffic payloads remain
  excluded. Its data source and isolated restore scope require explicit approval.

## Execution Sequence

1. W1: **establish baseline and document authority.** Record main and work
   SHA, compare the baseline across infra/, policies, .github/, scripts,
   tests, and docs, and classify Requirement, Architecture, Spec, Plan, Task,
   and registered IDs as active, draft, or archive. Do not reuse archived
   SPEC-0199 or SPEC-0200 as authority. Maps acceptance criterion 1.

2. W2: **derive the source inventory.** Enumerate the current root Compose
   include graph, services, and one-shot jobs. Trace each inventory field
   through declared Compose, Dockerfiles, entrypoints, tracked mount
   configuration, environment-variable consumers, policy, backup/runbook, and
   regression owners. Mark missing runtime facts unverified. Identify generated
   projections, their authored source, generator, and the limit of any
   semantic check. Maps criteria 2 and 3.

3. W3: **make role and engine rulings.** Establish actual source consumers
   before deciding each required overlap. Record unique function, learning
   purpose, resident and recovery cost, license, alternative, disposition, and
   residual uncertainty. Compare TimescaleDB Community, InfluxDB Core, QuestDB
   OSS, PostgreSQL, and ClickHouse on SQL, transactions, authorization,
   resource use, recovery, and license using current official sources; record
   no unmeasured performance conclusion. Retain the gateway, quality-tool, and
   shared-stack choices in SPEC-0201. Maps criteria 4 and 5.

4. W4: **draft the external-project boundary.** Define the manifest fields,
   connection locations, ownership division, approval state, and metadata-only
   resource registration. Keep external application Compose and business source
   in Project-Template-derived workspaces. Keep 07 and 08 separate
   planning-only tracks; do not derive speech, crawler, GPU, network, secret,
   or runtime authority from either. Maps criterion 6.

5. W5: **prepare the change and approval ledger.** Trace Prompt 01 requests
   1-12, named environment-variable contracts, learning domains, and duplicate
   conditions to source evidence and a later implementation Task or
   planning-only track. Define exact file ownership, current and target state,
   focused regression, rollback, and approval for 02-06. Assign a single
   future writer for shared root, Alloy, environment-variable, and Registry
   surfaces. Maps criteria 7 and 8.

6. W6: **verify the documentation package and report boundaries.** Run the
   smallest Stage 03 documentation gates, perform an independent read-only
   review of the exact revision, and record commands, exit codes, evidence,
   skipped checks, and residual uncertainty in the Task. Report source
   implementation, static validation, isolated execution, HOME rollout, and
   data migration separately. Maps criterion 9.

7. W7: **close the approved runtime evidence gaps.** TSK-0002 owns this
   proposed unit. W7.1 maps live `app_db` existence and project ownership;
   W7.2 maps external consumers and bounded aggregate traffic; W7.3 measures
   host capacity against existing policy floors and hands off the snapshot for
   Prompt 02 sizing; W7.4 rehearses
   restore from the approved backup into an isolated disposable target. These
   map the original criterion 10; the owner later deferred W7.4 and revised
   Prompt 02's source-work gate to W7.1-W7.3. W7.5 records the Prompt 02 implementation-time image,
   architecture, extension, backup-tool, and license recheck handoff for
   criterion 11. W7.1-W7.3 were approved as read-only observations on 2026-10-02; W7.4
   remains unapproved and NOT_RUN. The owner confirmed no current business
   app uses `app_db` and reports no stored data; the catalog found one
   technical heartbeat row and a dbt view but no business dataset. Future
   projects will use dev-db. W7.1 records the no-business-owner finding.
   DBeaver connects by SSH to management PostgreSQL, while its `app_db`
   selection and each transaction origin remain unverified. W7.2 passes
   only the consumer inventory and bounded aggregate traffic requirement;
   this origin uncertainty remains a handoff risk. Prompt 02 must calculate
   the new dev/LAB margin from its approved resource budget.

## Risk and Rollback

| Risk | Guard and recovery |
| --- | --- |
| Baseline drift invalidates an inference | Recompare latest main and work SHA before execution; stop and reconcile the Task if they differ from its handoff. |
| Source metadata is mistaken for live state | Keep W1-W6 source claims separate from W7 sanitized observation; no secret values, raw logs, row contents, or traffic payloads. |
| Archive or generated output becomes authority | Use current owners, preserve archive labels, and locate the authored source and generator before a conclusion. |
| A later task receives an ambiguous shared-file owner | Record one writer and named consumer tasks in W5; return an unresolved conflict to this package. |
| Plan is read as implementation authority | W7.1-W7.3 used their written read-only approval; W7.4 restore needs separate written execution approval and exact isolation preflight. HOME service, migration, credential, remote, and DNS/firewall actions remain outside this Task. |
| Documentation conclusion is unsupported | Correct or withdraw only the Task-owned draft documents after a reviewed disposition; preserve unrelated worktree state and do not alter infrastructure or runtime state. |

## Verification

W1-W6 results are recorded in TSK-0001. W7.1-W7.3 read-only observations
are recorded in TSK-0002; W7.1 owner closure, W7.2 consumer inventory and
aggregate traffic, and W7.3 capacity are scoped PASS. Transaction origin
remains unverified. W7.4
restore has not run and no restore result is claimed. On 2026-10-02 the
owner changed the Prompt 02 source-work gate: W7.4 is deferred, while W7.1-W7.3
scoped PASS and W7.5's implementation-time checks allow Prompt 02's own
Spec/Plan/Task to proceed. Runtime recovery and data migration remain gated. The changed-path
Gate can select a one-shot Conftest Docker job when the Registry changes; it is
therefore not a no-container check. Before running it, verify Docker context,
project name hyhome-conftest-gate, no host ports or shared network, read-only
infra bind, CPU/memory limit, and cleanup limited to
Docker Compose down --remove-orphans without volumes. If any preflight item is
unavailable, record the Gate as NOT_RUN rather than starting a container.
After that preflight and approval, run:

    python3 scripts/validation/run-ci-gate.py --profile changed
    git diff --check

The Task records their actual exit codes and affected revision. Domain tests, image pulls, HOME service changes, and data migration remain
NOT_RUN in W1-W6. TSK-0002 records the approved read-only observations and defines the separate
isolated restore preflight; restore remains NOT_RUN. Prompt 02 selects
its own path-aware checks and revalidates image compatibility at execution.

## Rulings

SPEC-0201's body was approved by the user on 2026-10-02. Its initial
frontmatter was draft under the Registry; the recorded lifecycle transitions
subsequently brought this Spec, Plan, and its Tasks to completed. The scoped
approvals covered the documented source and read-only work, not operational
execution beyond those bounds.

- The earlier Plan approval covered W1-W6. The user subsequently approved
  W7.1-W7.3 read-only observation. The owner subsequently approved W7.4
  Phase A, then directed all later recovery work to be deferred before any
  verify or scratch creation. Prompt 02 source work may proceed under its own
  Spec/Plan/Task; W7.4 is not marked PASS.
- TimescaleDB Community is the proposed development time-series choice; image
  digest, architecture, compatibility, backup method, and license revision are
  rechecked in the subsequent implementation package.
- mng-pg and mng-valkey remain management services. The owner confirmed
  no current business-app consumer of `app_db`; only retained infra objects
  need a later migration or retirement decision. Future projects use dev-db.
  Neither conclusion grants a schema, role, secret, or data action.
- LAB is an execution area rather than a capability tier. Its relocation or
  removal is a later approved configuration change.
