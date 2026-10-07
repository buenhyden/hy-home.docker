---
title: "LAB Isolation and Service Selection Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0215-TSK-0001"
parent_ids:
- "SPEC-0215-PLAN-0001"
created: "2026-10-08"
---

# LAB Isolation and Service Selection Task

## Objective

Keep HA and replica LABs out of the root, make their runs bounded and
self-cleaning, and record why each optional service is or is not resident.

## Inputs and Authorization

The current user request on 2026-10-08 asks to execute prompt 03 of the
analysis pack with per-unit commits and a per-Spec PR merge. It names no HOME
host run or data move, so those lanes stay `NOT_RUN`. Baseline `main`
`a56ab4e5b`. Registry issues SPEC-0215.

## Work Log

### Observed Baseline

The root renders 118 services with `--profile '*'`; none is a LAB service.
Seven LAB files refuse to render without their data, cluster or result roots.
`labs/mongodb.yml` renders without input because its state uses project
named volumes; `labs/opensearch-cluster.yml` does the same for node data.
The root still declares `lab_net` (10.250.9.0/24), which only RedisInsight
joins and which no LAB uses. CouchDB, MongoDB Express and the PostgreSQL
router register `Host(*.${LAB_BASE_DOMAIN})` routers with HOME middleware,
and `LAB_BASE_DOMAIN` equals the HOME domain. Six LABs label their services
`hy-home.tier: data`. No script starts or stops a LAB, and no aggregate HOME
budget exists. `infra/common-optimizations.exceptions.json` names no LAB.

### W1 Root Closure and `lab_net` Retirement

`tests/validation/test_lab_isolation.py` renders the root with `--profile '*'`
and each LAB with synthetic inputs. It fails if a LAB service, LAB network or
`secrets/labs` path appears in the root, or if a LAB service can be targeted
through the root. The test failed on `lab_net` (RED) and passed after the
root stopped allocating it. RedisInsight's `lab_net` attachment reached no LAB
service, because every LAB uses its own internal project network, so it was
removed with its hardening assertion and the stale network rows in AD-0026,
the RedisInsight README and GDE-0076.

The changed-profile gate ran in a clean worktree holding only this unit,
because another worker is editing `infra/04-data/dev-db` and the RedisInsight
compose file in the main tree. Two permission tests failed there only because
that checkout was made under umask 002; after `chmod g-w` they passed. Staged
lint passed. Commit `a5aecc629`.

### W2 LAB Boundaries and Lease Controller

Every LAB service is tiered `lab`. CouchDB, MongoDB Express and the
PostgreSQL router no longer carry HOME Traefik routers or middleware; each is
reachable only on a loopback port (`LAB_COUCHDB_HOST_PORT` 35984,
`LAB_MONGO_EXPRESS_HOST_PORT` 38081, `LAB_PG_HAPROXY_STATS_HOST_PORT` 37000).
`LAB_BASE_DOMAIN` is removed. MongoDB and the OpenSearch cluster keep state
under the required `LAB_DATA_DIR`; their previous project named volumes are
not moved or deleted. New boundary tests failed 39 times against the previous
LAB files (RED) and pass now. Default LAB host ports collide with no root port
or other LAB.

`scripts/operations/lab.py` adds `check`, `up`, `down`, `reap` and `status`.
`up` needs a purpose and a lease of at most `LAB_MAX_LEASE_MINUTES`, refuses
collisions of container names, networks, host ports or writable data paths
with the root, another selected LAB or a running container, refuses when the
declared limits of running containers plus the LAB exceed
`LAB_HOST_BUDGET_CPUS`/`LAB_HOST_BUDGET_MEMORY_MIB` or when more than
`LAB_MAX_CONCURRENT` LABs would run, records the ledger and starts the
project. `down` stops only that project without `-v`. Eleven unit tests pass;
three mutations (adding `-v`, removing the concurrency check, ignoring the own
project) each fail a test. The LAB env contract now counts the controller as a
consumer, so the lab public set is 55 keys (14 required, 41 optional).

Real Docker run on the HOME host, with synthetic data and secret roots in the
session scratch directory:

| Step | Result |
| --- | --- |
| `check valkey-cluster`, budget 12 CPUs / 32020 MiB (the host) | Exit 3: running HOME containers alone declare 61 CPUs and about 56 GiB |
| `check valkey-cluster`, explicit overcommit budget 80 / 70000 | Exit 0 |
| `up valkey-cluster --lease 30m` | Exit 0; 7 containers healthy; `cluster_state:ok`, 6 known nodes |
| `check mongodb` while it ran | Exit 3: `2 LABs would run; limit is 1` |
| `reap` after setting the lease to the past | Exit 0; 0 containers and 0 networks left; 6 data directories kept; ledger `stopped` |
| HOME project | 49 containers before and after |

The first row is a finding, not a defect of the check: declared HOME ceilings
already oversubscribe the host, so a ceiling budget equal to the host refuses
every LAB. Operators set the budget with an explicit overcommit. No measured
usage was taken.

The first full gate for this unit failed on two registrations: the new test
modules were not in the workflow contract plan (including
`test_lab_isolation`, which entered with W1 because the W1 gate did not select
that ownership check), and `lab.py` had no script manifest record. Both are
now registered, `labs/` became a selector prefix so a LAB-only change runs
these tests, and RUN-0022 names the controller as its runtime authority. The
earlier run also stopped on six links from `labs/*.md` to a stage policy; the
LAB guides now name `POL-0078` without linking it.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Root closure | 1 | W1 | Root render test RED then GREEN; clean-worktree gate | Working tree at `a5aecc629` | PASS | W1 Root Closure and `lab_net` Retirement | accepted |
| LAB boundary | 2 | W2 | Boundary tests RED then GREEN; LAB renders | Working tree | PASS | W2 LAB Boundaries and Lease Controller | accepted |
| Controller | 3 | W2 | Unit tests, mutations, real Docker run of `valkey-cluster` | Synthetic LAB roots | PASS | W2 LAB Boundaries and Lease Controller | accepted |
| Selection rules | 4 | W3 | Policy and catalog checks | Pending | NOT_RUN | Pending | pending |
| Records | 5 | W4 | Local gate and review | Pending | NOT_RUN | Pending | pending |

## Review and Completion

Not complete.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
