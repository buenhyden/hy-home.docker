---
title: "Request Baseline and Reconciliation"
version: "0.2.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
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

Reconcile the user request with current `main` and name one owner for each
item. The 2026-10-07 baseline covered fifteen items at
`23b0e6959d4f37e8dde6d7d33ffcc0589be32657`. The 2026-10-08 revision covers
twenty items against `a56ab4e5bac84623735975e9ed79801fd874b9e4` and
Project-Template `6b1c7394f1e08c0ce566f76b4644c2cad9c89891`, re-read when the
revision ran. Existing DEV TimescaleDB, MNG PostgreSQL, the k6 result
contract, standalone LAB files and Storybook are preserved and extended;
InfluxDB is retired, not kept optional.

## Scope

Included: the source baseline, a requirement disposition, a per-service-key
inventory of the rendered root model and each standalone LAB file, profile
selection probes, a conflict map from current rules to follow-on work, the
QA and remote-protection baseline, work dependencies, and ADR-0047.

Excluded: implementing the dispositions, HOME runtime observation, container
recreation, data migration or purge, secret reads, and the external
Project-Template workspace. Each belongs to the follow-on owner named below.

## Contracts

1. Every numbered request item and additional condition has exactly one
   disposition from `existing`, `complete`, `new`, `retire` or
   `discovery-only`, exactly one primary owning prompt, and any supporting
   prompts. The request item "retain InfluxDB as optional" is not a valid
   disposition.

   | Item | Request | Disposition | Primary | Supporting |
   | --- | --- | --- | --- | --- |
   | 01 | TimescaleDB replacement; DEV/MNG need | complete + retire | 01 | 04 |
   | 02 | k6/Locust selection and result series | complete | 02 | 04 |
   | 03 | HA/replica sets out of residence; Compose isolation | existing + complete | 03 | 05 |
   | 04 | Crawl4AI use | complete | 07 | 04 |
   | 05 | Storybook Docker, Traefik, Codex/Claude Design | complete | 06 | — |
   | 06 | duplicate roles and missing services | complete | 00 | 03, 04 |
   | 07 | cross-tier service integration | complete | 04 | — |
   | 08 | configuration, environment and secrets | complete | 04 | 01, 05 |
   | 09 | additional configuration needs | new | 04 | 05 |
   | 10 | complete user function from input to recovery | new | 08 | — |
   | 11 | public-data and public-API project | new | 08 | — |
   | 12 | Storybook retention and improvement | existing + complete | 06 | — |
   | 13 | service resource and permission optimization | complete | 05 | — |
   | 14 | the two common-optimizations files | complete | 05 | 12 |
   | 15 | every active InfluxDB reference | retire | 01 | — |
   | 16 | RedisInsight access to `dev-valkey` | new | 13 | 05 |
   | 17 | DEV PostgreSQL/Valkey exporters distinct from MNG | complete | 14 | 01 |
   | 18 | Ollama 0.40.0 and Open WebUI v0.11.4-cuda | complete | 15 | 05 |
   | 19 | Stage 05 operations document templates | complete | 16 | 12 |
   | 20 | review of draft, in-progress and blocked Specs | complete | 00 | 11 |
   | A1 | request precedence over workspace rules | existing + complete | 12 | — |
   | A2 | civil-service exam study app | discovery-only | 09 | — |
   | A3 | reading/speaking language app | discovery-only | 10 | — |
   | A4 | per-unit commit and per-Spec merge | existing | 11 | — |

2. The inventory has one row per service key with its owning Compose file,
   scope (`root` or `lab`), profiles, user and read-only state, capabilities,
   networks, host ports, secret count, forward and reverse dependencies,
   health check, CPU/memory/PID limits, Traefik routers, backup owner and one
   disposition from `keep`, `preserve+complete`, `optional`, `lab` or
   `retire`. Values come from a rendered model, never from private files.
3. Root and LAB stay separate: no LAB service key or network appears in the
   root `--profile '*'` model, and every LAB file renders standalone.
   Inventory size is an observation, not a contract: the root inventory rows
   equal the rendered root service set, which `check-operations-catalog.py`
   enforces, and the LAB rows equal the services of `labs/*.yml`.
4. Every conflict between a current rule and the request maps to a follow-on
   work unit that changes the rule, its enforcer and its regression together.
   A conflict is never recorded as a permanent block. Only missing tool
   permission or an unconfirmed real data target limits a single lane.
5. Follow-on Spec Packages take their numbers from the Registry when each one
   starts. This package reserves no future number.
6. Each draft, in-progress or blocked Spec has one disposition from `keep`,
   `revise`, `proceed` or `supersede`, read from its frontmatter and Task, not
   from the Stage 03 README. A merge is not an acceptance, and a source result
   is not a HOME result.

## Acceptance Criteria

1. The Task records the local and remote `main` SHA, the Project-Template SHA,
   the observation time and the difference from the pack's assumed baseline.
2. Every item in Contract 1 has a disposition and owner, and the Influx
   disposition is retirement.
3. The Task holds an inventory whose rows equal the rendered root service
   set plus the services of the standalone LAB files, with zero root/LAB name
   or network overlap and with synthetic inputs labelled. The 2026-10-07 count
   (119 root, 42 LAB) is a recorded observation.
4. The Task records profile probes, including no-profile, unknown-profile and
   explicit-service selection, with their exit codes.
5. The Task's conflict map links each conflicting rule to a follow-on owner,
   and ADR-0047 records the data, load-tool and LAB selection.
6. The Task records the QA selection baseline and the actual remote
   protection read, keeping missing evidence visible as `NOT_RUN`.
7. TSK-0002 records the twenty-item disposition with each item's current
   state and evidence, and the disposition of every open Spec.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-request-baseline-and-inventory.md)
- [Task 0002](tasks/tsk-0002-twenty-item-reconciliation.md)
- [ADR-0047](../../02.architecture/decisions/0047-dev-timescale-influx-retirement-and-load-tools.md)
- [Data requirement](../../01.requirements/0004-data.md)
- [Analytics requirement](../../01.requirements/0005-data-analytics.md)
- [Governance requirement](../../01.requirements/0024-agent-governance-standardization.md)
- [Home host requirement](../../01.requirements/0027-home-development-host.md)
- [Data architecture](../../02.architecture/descriptions/0004-data-architecture.md)
- [Home host architecture](../../02.architecture/descriptions/0031-home-development-host.md)
