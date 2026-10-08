---
title: "LAB Closure and HOME LAB Run Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0215-TSK-0002"
parent_ids:
- "SPEC-0215-PLAN-0001"
created: "2026-10-08"
---

# LAB Closure and HOME LAB Run Task

## Objective

Close what TSK-0001 left open: pin the LAB inventory and selection rules with
tests, give every optional service a cost and retirement condition, audit the
HOME host for LAB residue, and start each LAB on the HOME host.

## Inputs and Authorization

The current user request on 2026-10-08 asks to execute prompt 03 of the
analysis pack ("separate the normal Compose from the HA and replica LABs")
with per-unit commits and a per-Spec PR merge. It asks for real selection
behavior to be verified and for HOME residue to be audited without `down -v`
or prune. Baseline `main` `f88eb6601`. No HOME data move is requested.

## Work Log

### Starting State

TSK-0001 left these items open:

- The MongoDB LAB never started, because its exporter pin did not exist.
- The LAB guides did not name their services.
- `lab.py` did not compare cluster IDs.
- No test kept HOME Prometheus away from LAB containers or kept wildcard
  profile starts out of documents.
- The disposition table had no cost, retained data or retirement column.
- No LAB other than Valkey had been started on the HOME host.

### W5 MongoDB Exporter Retirement

`percona/mongodb_exporter:2.37` never existed, every later tag lacks
`/bin/sh` for the secret wrapper, and no Prometheus job reads it.
`mongodb-exporter`, its `lab_mongodb_obs_net` network, the two env keys and
the tech-stack row were removed. The MongoDB guide, runbook, policy and the
POL-0078 row record the retirement. Commit `3bc108834`.

### W6 Inventory, Cluster ID, Observability and Selection Tests

`tests/validation/test_lab_isolation.py` gains `LabInventoryAndSelectionTests`:

| Test | Contract | RED evidence |
| --- | --- | --- |
| Guide Project and Services rows equal the render | 9 | Failed for 7 guides before the rows were added |
| HOME Prometheus targets contain no LAB host | 11 | Passed on first run; kept as a regression guard |
| No tracked document, script or unit starts the root with `--profile '*'` | 12 | Passed on first run; config renders are allowed |
| POL-0078 HOME selection holds no LAB service and no `nginx` | 12 | Passed on first run |

`lab.py` collects each service's `CLUSTER_ID` and refuses a LAB whose ID
equals the root's or another selected LAB's. The new controller test failed
before the change and passes now. Commit `5a16f1844`.

### W7 Disposition Columns

POL-0078 "Optional service disposition" gains declared cost (CPU and MiB from
the rendered root), retained data and retirement condition columns. Traefik is
the default gateway. Nginx is an alternate gateway kept for practice: it
shares 80/443 with Traefik and is not in the HOME selection. Supabase is
13 services at 14.5 CPUs and 10496 MiB. LAB exporters are not scraped by
HOME. Commit `add4cc598`.

### W8 HOME Residue Audit and Real LAB Runs

The HOME audit was read-only:

- Only the k3d cluster runs outside `hy-home-infra`; it is the Kubernetes
  integration, not a LAB.
- No stopped LAB or orphan container exists.
- The systemd units `hyhome-backup` and `hyhome-renovate` select the
  `backup` and `dependency-update` profiles only. No crontab binary is
  installed.
- `COMPOSE_PROFILES` is unset; HOME selection comes from the POL-0078 row.

Nothing was stopped or removed.

Every LAB was then started through `lab.py up` on the HOME host with
synthetic data, secret and certificate roots in the session scratch
directory. The runs exposed these defects, each fixed and committed:

| Defect | Fix | Commit |
| --- | --- | --- |
| `compose up --wait` fails when a one-shot init job exits 0 | `lab.py` polls the project itself: a non-zero exit or `unhealthy` fails, a finished init passes, a running one-shot is pending; `LAB_READY_TIMEOUT_SECONDS` default 600, now in `labs/.env.example` (LAB public set 54 keys: 15 required, 39 optional) | `c9b544451` |
| Cassandra, CouchDB and MongoDB entrypoints chown and `gosu`, which `cap_drop: ALL` forbids | The data nodes use the stateful DB templates; MongoDB nodes run as `999:999` because `gosu` drops the secret group; the key generator runs `mongosh` with `CHOWN`, `DAC_OVERRIDE` and `FOWNER` | `1e9ed644c` |
| CouchDB `finish_cluster` returns 500 "unable to sync admin passwords" and a rerun returns 409 | The init accepts 2xx or 409, treats 3 cluster members as done and creates the system databases | `1e9ed644c` |
| OpenSearch image build fails on the exporter plugin | Plugin `3.8.0.0` to match the `3.8.0` base | `1e9ed644c` |
| OpenSearch nodes reject each other's certificates | `plugins.security.nodes_dn: CN=opensearch-node*`; transport hostname verification off for IP SAN certificates | `1e9ed644c` |
| A changed `LAB_DATA_DIR` made Compose prompt on stdin and hang | Children get `stdin=DEVNULL`; `check` reports a stale volume record and names the `docker volume rm` | `4c87bc09e` |
| MongoDB init reported failed authentication on every run | mongosh returns `{ ok: 1 }`, not `1`; the check reads `.ok` | `231e070ac` |

Final run on the fixed code (`results6`, `results7` and the Valkey rerun):

| LAB | `up` | Readiness signal | `down` | Left containers / networks |
| --- | --- | --- | --- | --- |
| postgresql-ha | 0 (39 s) | 3 members, 1 leader, 3 running | 0 | 0 / 0 |
| kafka-cluster | 0 (56 s) | Topic `lab-events` RF 3, `min.insync.replicas=2`, 3 brokers | 0 | 0 / 0 |
| mongodb | 0 (21 s) | `PRIMARY,SECONDARY,ARBITER` | 0 | 0 / 0 |
| couchdb | 0 (18 s) | 3 of 3 cluster nodes | 0 | 0 / 0 |
| cassandra | 0 (20 s) | 1 node `UN` | 0 | 0 / 0 |
| valkey-cluster | 0 | `cluster_state:ok`, 6 nodes | 0 | 0 / 0 |
| opensearch-cluster | 1 (200 s) | `FAIL`, blocked by host disk, see below | 0 | 0 / 0 |

The HOME project held 54 containers before and after every run.

OpenSearch formed a three-node cluster and elected a cluster manager, but
the host disk is 90% used. That is OpenSearch's default high disk watermark,
so the cluster put an index-create block on and could not allocate the
`.opendistro_security` primary shard. Security stayed uninitialized and the
nodes stayed unhealthy. The watermark is not disabled, because that would
hide a real capacity risk. The LAB needs free disk first; this is a HOME
capacity condition, not a LAB configuration defect.

The first Valkey attempt on the final code exited 3 on the stale-volume
check, because its volume records point at an earlier scratch data root.
That is the W8 guard working. Removing those records with `docker volume rm`
was denied to this session, so the rerun used the recorded data root.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Exporter retirement | 6 | W5 | Image tag check; renders; catalog and tech-stack sync | `3bc108834` | PASS | W5 MongoDB Exporter Retirement | accepted |
| Inventory and selection tests | 6 | W6 | New tests RED then GREEN; changed-profile gate | `5a16f1844` | PASS | W6 Inventory, Cluster ID, Observability and Selection Tests | accepted |
| Disposition columns | 4 | W7 | Policy text; HOME selection test; link and metadata checks | `add4cc598` | PASS | W7 Disposition Columns | accepted |
| HOME residue audit | 5 | W8 | Read-only `docker ps`, restart policies, systemd units, crontab | HOME host 2026-10-08 | PASS | W8 HOME Residue Audit and Real LAB Runs | accepted |
| Real LAB runs | 7 | W8 | `lab.py up`, probe, `down`, leftover count for six LABs | Synthetic roots; `231e070ac` | PASS | W8 HOME Residue Audit and Real LAB Runs | accepted |
| OpenSearch LAB run | 7 | W8 | `lab.py up`, cluster health, `down`, leftover count | Synthetic roots; host disk 90% | FAIL | W8 HOME Residue Audit and Real LAB Runs | pending |

## Review and Completion

Not complete. The OpenSearch row stays pending until the host has free disk.

Owner actions, which this session may not take:

- Remove the 27 `hy-home-lab-*` volume records that point into session
  scratch directories, with `docker volume rm` on each name that
  `lab.py check` reports. They hold no HOME data.
- Free host disk below 90% before starting the OpenSearch LAB again. HOME
  OpenSearch is subject to the same watermark.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [First Task](tsk-0001-lab-isolation-and-service-selection.md)
