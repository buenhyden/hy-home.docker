---
title: "Request Baseline and Reconciliation"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-07"
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

Reconcile the 2026-10-07 user request (fifteen numbered items plus additional
conditions) with `main` at `23b0e6959d4f37e8dde6d7d33ffcc0589be32657`. Record
what already exists, what each item still needs, which current rules conflict
with it, and which follow-on Spec Package owns each change. Existing DEV
TimescaleDB, MNG PostgreSQL, the k6 result contract, standalone LAB files and
Storybook are preserved and extended; InfluxDB is retired, not kept optional.

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
   `discovery-only`, plus one owning execution prompt. The request item
   "retain InfluxDB as optional" is not a valid disposition.

   | Item | Request | Disposition | Owner |
   | --- | --- | --- | --- |
   | 01 | Influx to Timescale; DEV/MNG need | complete + retire | 01 |
   | 02 | k6/Locust selection, series, results | complete | 02 |
   | 03 | HA/replica/multi-broker isolation | existing + complete | 03 |
   | 04 | Crawl4AI project and ingestion | complete | 07 |
   | 05 | Storybook Docker, Traefik, Codex, Design | complete | 06 |
   | 06 | infra duplicate roles and gaps | complete | 00, 03, 04 |
   | 07 | service-to-service connections | complete | 04 |
   | 08 | configuration, env and secrets | complete | 01, 04, 05 |
   | 09 | additional capability readiness | new | 04, 05 |
   | 10 | input-to-recovery user function | new | 08 |
   | 11 | public-data external project | new | 08 |
   | 12 | Storybook retention and improvement | existing + complete | 06 |
   | 13 | service resource and permission | complete | 05 |
   | 14 | two common files and validators | complete | 05, 12 |
   | 15 | remove every active Influx reference | retire | 01 |
   | A1 | request precedence over workspace rules | existing + complete | 12 |
   | A2 | civil-service exam study app | discovery-only | 09 |
   | A3 | reading/speaking language app | discovery-only | 10 |
   | A4 | per-unit commit and per-Spec merge | existing | 11 |

2. The inventory has one row per service key with its owning Compose file,
   scope (`root` or `lab`), profiles, user and read-only state, capabilities,
   networks, host ports, secret count, forward and reverse dependencies,
   health check, CPU/memory/PID limits, Traefik routers, backup owner and one
   disposition from `keep`, `preserve+complete`, `optional`, `lab` or
   `retire`. Values come from a rendered model, never from private files.
3. Root and LAB stay separate: no LAB service key or network appears in the
   root `--profile '*'` model, and every LAB file renders standalone.
4. Every conflict between a current rule and the request maps to a follow-on
   work unit that changes the rule, its enforcer and its regression together.
   A conflict is never recorded as a permanent block. Only missing tool
   permission or an unconfirmed real data target limits a single lane.
5. Follow-on Spec Packages take their numbers from the Registry when each one
   starts. This package reserves no future number.

## Acceptance Criteria

1. The Task records the local and remote `main` SHA, the Project-Template SHA,
   the observation time and the difference from the pack's assumed baseline.
2. Every item in Contract 1 has a disposition and owner, and the Influx
   disposition is retirement.
3. The Task holds a 161-row inventory equal to the rendered root model (119)
   plus the eight standalone LAB models (42), with zero root/LAB name or
   network overlap and with synthetic inputs labelled.
4. The Task records profile probes, including no-profile, unknown-profile and
   explicit-service selection, with their exit codes.
5. The Task's conflict map links each conflicting rule to a follow-on owner,
   and ADR-0047 records the data, load-tool and LAB selection.
6. The Task records the QA selection baseline and the actual remote
   protection read, keeping missing evidence visible as `NOT_RUN`.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-request-baseline-and-inventory.md)
- [ADR-0047](../../02.architecture/decisions/0047-dev-timescale-influx-retirement-and-load-tools.md)
- [Data requirement](../../01.requirements/0004-data.md)
- [Analytics requirement](../../01.requirements/0005-data-analytics.md)
- [Governance requirement](../../01.requirements/0024-agent-governance-standardization.md)
- [Home host requirement](../../01.requirements/0027-home-development-host.md)
- [Data architecture](../../02.architecture/descriptions/0004-data-architecture.md)
- [Home host architecture](../../02.architecture/descriptions/0031-home-development-host.md)
