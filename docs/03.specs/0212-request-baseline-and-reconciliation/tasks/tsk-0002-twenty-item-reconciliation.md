---
title: "Twenty-Item Reconciliation Task"
version: "0.1.3"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0002"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-08"
---

# Twenty-Item Reconciliation Task

## Objective

Revise the SPEC-0212 baseline for the twenty-item request, assign one primary
owner to each item, replace the fixed inventory counts with set equality, and
dispose of every open Spec.

## Inputs and Authorization

The user request on 2026-10-08 asks to execute prompt 00 of the revised
analysis pack: twenty items, items 16 to 19 linked to prompts 13 to 16, and
item 20 asking for a review of the draft, in-progress and blocked Specs. The
pack's twenty-item table arrived in the request body; its other files were not
available locally, so this Task uses only facts re-observed on 2026-10-08.
TSK-0001 stays as the 2026-10-07 record.

## Work Log

### Baseline

| Item | Observed |
| --- | --- |
| Pack baseline | `a56ab4e5bac84623735975e9ed79801fd874b9e4` |
| `main` when this Task was written | `3d90aa653` (PR #378), after PRs #372 to #378 |
| Project-Template `main` | `6b1c7394f1e08c0ce566f76b4644c2cad9c89891` (2026-10-07T13:29:37Z), equal to the pack baseline |

Spec states were read from each `spec.md` and Task frontmatter with a YAML
parser, not from the Stage 03 README.

### Item State

Owner columns are in SPEC-0212 Contract 1. State is what `main` and HOME
showed on 2026-10-08; it is not an acceptance of the owning prompt.

| Item | Owner Spec | State | Remaining for the owner |
| --- | --- | --- | --- |
| 01 | SPEC-0213 | DEV TimescaleDB and MNG PostgreSQL kept; DEV WAL archive, first full backup and restore canary on HOME | HOME PITR and R2 restore |
| 02 | SPEC-0214 | k6 default, Locust LAB, authenticated OTLP relay merged (#371); SPEC-0214 TSK-0002 adds the relay controller, `quality_otlp_net`, an isolated target-to-dashboard run and the supervised Locust lifecycle (#384); a HOME relay canary reached HOME Prometheus and the live Grafana dashboard | Real-target load; per-project producer credentials and quota |
| 03 | SPEC-0215 | Root `lab_net` retired, LAB lease controller merged (#376) | HOME LAB runs; persistent LAB inventory check |
| 04 | new at execution, reusing SPEC-0204 Crawl4AI lanes | Not started this round | All |
| 05 | new at execution | Existing Storybook static origin and MCP preserved | All |
| 06 | SPEC-0212 | Root inventory equals the rendered set (W7) | Role, cost and duplication review per service key |
| 07 | new at execution, reusing SPEC-0204 | Not started this round | All |
| 08 | new at execution | DEV consumers no longer read MNG variables (SPEC-0213) | Image `_FILE` support and address/permission review |
| 09 | new at execution | Not started this round | All |
| 10 | new at execution | Not started this round | External application vertical slice |
| 11 | new at execution | Project-Template baseline confirmed | External workspace and API budget |
| 12 | new at execution | Not started this round | All |
| 13 | new at execution | Not started this round | All |
| 14 | new at execution | `naming_exceptions` added to the exceptions file (SPEC-0216) | Exact exception scope with parser, generator and Rego |
| 15 | SPEC-0213 | No active InfluxDB surface; HOME has no InfluxDB container | Data directory disposal by the owner |
| 16 | new at execution | RedisInsight joins `dev_data_net` and reaches `dev-valkey` on HOME; the connection uses the `devadmin` ACL user | Inspector ACL and UI health |
| 17 | SPEC-0213 W5 | `dev_pg_monitor` and `devmonitor` accounts; Prometheus scrapes both on HOME | `db_scope` label and DB failure alerts |
| 18 | new at execution | Pins merged (#374); HOME runs `ollama/ollama:0.40.0` and `open-webui:v0.11.4-cuda`, both healthy | Manifest digest, wrapper, OIDC, CUDA/VRAM and rollback evidence |
| 19 | new at execution | Not started this round | All |
| 20 | SPEC-0212 | This Task | — |

### W7 Inventory Set Check

The rendered root model (`.env.example`, `--profile '*'`) has 121 services and
the m0021 inventory has 121 rows; the sets are equal, which the
`service-inventory-membership` check in `check-operations-catalog.py`
enforces. The eight `labs/*.yml` files hold 42 services, the same set as the
TSK-0001 table, and share no name with the root. Since TSK-0001 the root added
`dev-pg-exporter`, `dev-pg-monitor-provision` and `dev-valkey-exporter` and
removed `influxdb`. No tracked check enforces the LAB set yet; that belongs to
the item 03 owner.

### W8 Open Spec Disposition

| Spec | State | Disposition | Reason |
| --- | --- | --- | --- |
| SPEC-0182 | blocked; TSK-0003 blocked | keep | Recovery, SSO and R2 evidence waits for owner-held material |
| SPEC-0204 | blocked; TSK-0001 blocked | keep | Runtime lanes stay; items 04 and 07 reuse its ownership |
| SPEC-0207 | in-progress; Tasks completed | keep | Pending rows belong to the governance owner (prompt 12) |
| SPEC-0211 | in-progress | keep | QA rationalization continues under prompt 11 |
| SPEC-0212 | draft | revise | This Task |
| SPEC-0213 | draft | proceed | Source, isolated and HOME work done; PITR and R2 open |
| SPEC-0214 | draft | proceed | Merged source; HOME runs open |
| SPEC-0215 | draft | proceed | Merged source; HOME LAB runs open |
| SPEC-0216 | draft | proceed | OpenBao waits for the owner's unseal; then `openbao-agent` |

No Spec is superseded. Completed SPEC-0208, SPEC-0209 and SPEC-0210 are not
reopened.

### Handoff

Next order: prompt 13 (item 16) and prompt 14 (item 17 remainder) reuse the
DEV data owner; prompt 15 (item 18) verifies the running pins; prompts 04, 05,
06 and 07 follow; prompt 16 (item 19) runs after the document owners settle.
Prompts 09 and 10 stay discovery-only. Each takes its Spec number from the
Registry when it starts. One writer at a time owns the Registry, the Stage 03
README and `.github/workflow-contract.yml`.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline and item owners | 1, 2 | W6 | `gh api` commit reads; frontmatter parse | `main` `3d90aa653` | PASS | Baseline; Item State | accepted |
| Inventory set equality | 3 | W7 | Rendered root and LAB service sets against inventory rows | `.env.example`; `labs/*.yml` | PASS | W7 Inventory Set Check | accepted |
| Open Spec disposition | 7 | W8 | Spec and Task frontmatter and completion sections | `main` `3d90aa653` | PASS | W8 Open Spec Disposition | accepted |

## Review and Completion

The twenty-item baseline, inventory check and Spec dispositions are recorded.
Implementation stays with each owning prompt.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Task 0001](tsk-0001-request-baseline-and-inventory.md)
