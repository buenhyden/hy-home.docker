---
title: "Development Data and LAB Isolation Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0202-PLAN-0001"
parent_ids:
- "SPEC-0202"
created: "2026-10-02"
---

# Development Data and LAB Isolation Plan

## Objective

Implement Prompt 02's authored source without deploying HOME, moving real
data, or performing deferred recovery. The user authorized source progression
after accepting SPEC-0201 W7.1-W7.3 and explicitly deferred W7.4 and later
operational work. Each runtime-dependent acceptance remains NOT_RUN.

## Dependencies

- Current main/worktree and exact SPEC-0201 handoff; archived SPEC-0199/0200
  are not authority.
- Official Timescale, PostgreSQL, pgBackRest, Valkey and Influx sources at
  implementation; an image digest is a current registry observation, not a
  local build/restore result.
- Canonical governance and an approved Task for state-changing source files.
- No app-specific provision without approved project metadata. No access to
  live secret values or untracked application data.

## Execution Sequence

1. **W1: baseline and source contract.** Recheck main/branch, registered
   IDs, current root graph and consumers; fix exact ownership of root/env,
   projection, DB, CDC, LAB and migration files in TSK-0001. Bind current
   image digest/platform/PGDATA/license to official evidence.
2. **W2: dev engines and role boundary.** Add dev-pg Timescale and dev-valkey
   source, explicit resource/health/persistence/backup interfaces and a
   fail-closed project provisioner. Keep mng metadata/queues and existing
   state intact. Add focused privilege tests before provisioning code.
3. **W3: consumer transition.** Move future business `SERVICE_POSTGRES_*`
   responsibility from mng init and retarget dbt/CDC source, preserving
   management metadata and Avro Schema Registry. Record current `app_db`
   technical objects and the future cutover/LSN/rollback steps as NOT_RUN.
4. **W4: migration and backup source.** Add strict Influx mapping
   validation and no-data handling. Defer actual export/import adapters until
   source measurement/writer inventory and precision are known. Define
   separate dev-pg WAL/pgBackRest repository/stanza/key references, globals,
   role/extension/migration revision and separate-volume restore steps;
   key issuance, real migration and recovery stay deferred.
5. **W5: LAB isolation.** Move complete HA/cluster/replica closures behind
   separate LAB entrypoints and distinct state; keep a normal single Kafka
   broker and approved management/development pair in root. Revise the
   operations catalog's all-infra-in-root rule, its focused tests, and
   POL-0078 profile guidance to model separate LAB entrypoints. Check render
   without starting all profiles.
6. **W6: source verification and handoff.** Update `.env.example`, image
   projection/Renovate, path-aware tests, docs and 03/04/06 contracts. Run
   focused static checks and independent correctness/security review. Mark
   Docker/restore/HOME/data tests NOT_RUN where authorization is absent.

7. **W7: scoped issuance and isolated acceptance (TSK-0002).** Under the
   owner's 2026-10-03 follow-up, issue only the 20 previously absent dev/LAB
   secret paths with fresh independent values and no rotation. Record path-only
   inventory, mode, ownership and custody. Preflight Docker context, unique
   project, ports, networks, volumes, source image, resources and exact cleanup
   before isolated execution. Exercise bounded dev engine and LAB contracts
   without touching HOME services; distinguish every unrun runtime criterion.
   Reconcile public/private metadata without exposing values, run selected
   path-aware checks, then fast-forward local `main` only from a clean verified
   branch. Remote publication, HOME start/restart and real data operations remain
   outside this work unit.

## Risk and Rollback

A source rollback reverts only Task-owned files before deployment; it cannot
reverse a real schema/data/credential change. Existing HOME/LAB containers
are not stopped by an include removal. A later operational Task must identify
exact service stop/restart/reboot behavior and rollback before deployment.
Unknown Influx types/precision or CDC offsets stop their dependent source
promotion rather than guess. Retention deletion needs separate owner approval.

## Verification

Use existing path-aware owners: focused SQL/Compose/CDC tests, scoped Compose
render, version projection check, document metadata/links and `git diff
--check`. Before any container test verify Docker context, project, ports,
networks, volumes, resources and exact cleanup; actual runtime execution is
deferred unless newly approved. Do not run whole-stack `up`, `down -v`, volume
prune or an all-files gate by default.

## Rulings

TSK-0001 is the sole writer of root `docker-compose.yml`, `.env.example`,
image projection and Stage 99 registry in this serial wave. Other tasks
consume the resulting contract. Prompt 03 owns `perf_db`; Prompt 04 owns
later shared Alloy/Registry integration, after this wave closes. Product 07
and 08 planning has no source authority here.
