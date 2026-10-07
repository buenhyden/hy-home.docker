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

### W3 Budget, Selection and Disposition Rules

POL-0078 gains two sections. "LAB lifecycle and budget" states the following:

- A profile is a selection, not a security boundary, and naming a root service
  selects it regardless of profile (0212 conflict C10). A LAB cannot be
  selected that way.
- LABs on one host do not give host fault tolerance.
- `lab.py` is the only start and stop path, and the policy lists its
  collision, budget, concurrency and lease rules.
- Declared HOME ceilings already exceed the host, so operators set an explicit
  overcommit budget.
- GPU is not in declared limits. ComfyUI and Ollama concurrency follows the
  DCGM VRAM headroom.
- No savings figure is published without measurement.
- AI and workflow residency is kept.

"Optional service disposition" assigns each optional, DEV and LAB group a
role, consumer, decision and the host state from one read-only `docker ps`
on 2026-10-08:

- Loki and Dozzle, Airflow and n8n, and Mailpit and Stalwart are judged
  separately rather than as duplicates.
- Schema Registry stays because the Debezium Avro connector uses it.
- Crawl4AI has no consumer and is marked for retirement review, not deleted.
- No `hy-home-lab-*` project was running.

The `lab-kafka` companion row now distinguishes the HOME single broker
(replication factor 1, no fault tolerance) from the LAB (three brokers,
replication factor 3, `min.insync.replicas=2`, one broker loss on the same
host).

### W4 HA Wording, Handoffs and Final Validation

The following documents were corrected:

- REQ-0004-FR-0001 no longer requires HA for core databases. HOME and DEV
  databases are single nodes recovered by backup and restore, and replication
  and failover are exercised only in the LABs, which share one host.
- ADR-0004 keeps Spilo and Patroni for the HA topology but limits it to the
  LAB.
- RUN-0036 became the "Kafka Runbook" and states the single broker's
  replication factor 1.
- REQ-0006 names the single-broker Kafka and the LAB topology.
- POL-0031 calls the PostgreSQL topology a LAB that is not host HA.

Handoff to prompt 05: `infra/common-optimizations.exceptions.json` and
`infra/image-tag-policy.exceptions.json` name no `labs/` path or LAB service,
so no exception has to move with the LAB boundary. Every LAB still extends
`infra/common-optimizations.yml`, so template changes there reach the LABs.

New blocker, found by a real run: `lab.py up mongodb` with synthetic roots
exited 1 because `percona/mongodb_exporter:2.37`, pinned in `labs/mongodb.yml`
and `infra/tech-stack.versions.json`, does not exist on Docker Hub. `docker
manifest inspect` confirms that `2.37` is missing while `mongo:8.3.11-noble`
and `percona/mongodb_exporter:0.47.1` exist. The ledger recorded `failed`;
`lab.py down mongodb` exited 0 and left no container or network. The pin is
not changed here because another worker is editing
`infra/tech-stack.versions.json`. The bind-volume ownership of the MongoDB
LAB therefore stays unverified at runtime.

### Independent Review and Fixes

A read-only review of the branch found eight important and eight minor
items. Each change below has a test that failed against the previous code
(RED) and passes now, except where stated:

| Item | Change |
| --- | --- |
| Tier test passed a missing label | The test now requires `hy-home.tier: lab`; four labelless services (`mongo-key-generator`, `mongo-init`, `mongodb-exporter`, `couchdb-cluster-init`) got the label |
| `min.insync.replicas=2` was documented but unset | `KAFKA_MIN_INSYNC_REPLICAS: 2` on the LAB brokers; a test pins it and HOME replication factor 1 |
| MongoDB guide said no host port | Names the Mongo Express loopback port |
| Symlinks defeated the HOME overlap check | `footprint` resolves real paths; the mkdir guard compares with the resolved data root |
| mkdir guard was untested | A volume outside `LAB_DATA_DIR` is not created |
| `reap` skipped `stop-failed` | `reap` retries it |
| A read-only input was a cleanup target | Only volumes mounted read-write and writable binds enter the ledger cleanup list; read-only inputs still count for collisions |
| REQ-0004 use case still promised an HA cluster | STORY-01/02, scope and risks now describe single nodes recovered by backup |
| Ledger could name any project | `down` refuses a non-`hy-home-lab-` project |
| Replica names stopped at `-1` | Every replica name is listed |
| Valkey ignored `LAB_HOST_BIND_IP` | All six ports use it |
| Bad env or ledger values crashed | Exit 2 |
| `down` re-rendered the LAB | `down` stops by project label, so lost inputs cannot block it |
| Ledger-before-start and own-project budget exclusion were untested | Both are pinned |
| Bind ownership for MongoDB and OpenSearch | Recorded as unverified in both LAB guides with the uid each process writes as |

Not changed: port ranges are compared as strings (no LAB or root service
publishes a range), the manifest names one consumer (one proving reference
is required), and the `$(` in `labs/postgresql-ha.yml` predates this change
and renders.

The Valkey LAB was run again with the fixed controller: `up` exit 0,
`cluster_state:ok`, ledger with 6 state paths and 8 containers, `down` by
project label exit 0, no container or network left, 6 data directories kept.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Root closure | 1 | W1 | Root render test RED then GREEN; clean-worktree gate | Working tree at `a5aecc629` | PASS | W1 Root Closure and `lab_net` Retirement | accepted |
| LAB boundary | 2 | W2 | Boundary tests RED then GREEN; LAB renders | Working tree | PASS | W2 LAB Boundaries and Lease Controller | accepted |
| Controller | 3 | W2 | Unit tests, mutations, real Docker run of `valkey-cluster` | Synthetic LAB roots | PASS | W2 LAB Boundaries and Lease Controller | accepted |
| Selection rules | 4 | W3 | Policy text; catalog and link checks; changed-profile gate | Working tree | PASS | W3 Budget, Selection and Disposition Rules | accepted |
| Records | 5 | W4 | Clean-worktree changed-profile gate and staged lint per unit; independent review; HOME, data moves and MongoDB runtime stay `NOT_RUN` | Working tree at each unit | PASS | W4 HA Wording, Handoffs and Final Validation | accepted |

## Review and Completion

Not complete.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
