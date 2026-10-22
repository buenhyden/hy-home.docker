---
title: "LAB Closure and HOME LAB Run Task"
version: "0.2.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-22"
layer: "specs"
artifact_id: "SPEC-0215-TSK-0002"
parent_ids:
- "SPEC-0215-PLAN-0001"
created: "2026-10-08"
---

# LAB Closure and HOME LAB Run Task

## Overview

### Objective

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
| opensearch-cluster | 1 (200 s); 0 (141 s) on the rerun | First `FAIL` on host disk; rerun green, 3 nodes, 14 active shards, Dashboards healthy | 0 | 0 / 0 |

The HOME project held 54 containers before and after every run.

OpenSearch formed a three-node cluster and elected a cluster manager, but
the host disk is 90% used. That is OpenSearch's default high disk watermark,
so the cluster put an index-create block on and could not allocate the
`.opendistro_security` primary shard. Security stayed uninitialized and the
nodes stayed unhealthy. The watermark is not disabled, because that would
hide a real capacity risk.

After the owner freed the disk to 66%, the rerun showed that the disk was not
the only cause. Two LAB defects surfaced, both fixed in `e0e19cdcf`:

- The node healthcheck refused an admin password with any character outside
  a short allowlist, so a green cluster stayed unhealthy. It now escapes the
  value for curl's config syntax and refuses only an empty value or a line
  break.
- Dashboards execs its binary directly, which skips the image's
  env-to-option mapping, so it connected to `127.0.0.1:9200`. A tracked
  config file (`labs/opensearch-cluster-dashboards.config`) now names the
  three nodes and reads its passwords from the environment, so none reaches
  argv.

The rerun on 2026-10-08 exited 0 after 141 s with the cluster green, three
nodes and 14 active shards; `down` left no container or network, and the HOME
project held 55 containers before and after. A new test fails against the
previous LAB file and passes now.

The first Valkey attempt on the final code exited 3 on the stale-volume
check, because its volume records point at an earlier scratch data root.
That is the W8 guard working. Removing those records with `docker volume rm`
was denied to this session, so the rerun used the recorded data root.

### Validation

The changed-profile local gate ran in a throwaway worktree holding the
branch diff against `f88eb6601` as staged changes, because the local gate
selects only uncommitted paths. Its first run failed three tests: two
permission tests failed only because that checkout was made under umask 002,
and `test_lab_credential_argv` still required the retired exporter's
`MONGODB_PASSWORD`. The second run failed on the LAB public key count, which
the retirement had lowered, and showed that `LAB_READY_TIMEOUT_SECONDS` was
not declared. After commits `d341b75c8` and `137650df8` the gate exited 0
(161 tests). `pre-commit run --from-ref origin/main --to-ref HEAD` exited 0.

### W6 Follow-up: Single Collection and Exact Path List

The request on 2026-10-13 (prompt v9, findings F31 to F33) asked to compare
this test module with the current guides and its callers. The baseline is
`main` `5bf0e9479`.

- F31 is already resolved on `main`: `LAB_GUIDE_PATHS` reads the moved
  Supabase guide, and the operations catalog reader checks its
  `implementation_services` against the LAB source. The other eight guides
  have no frontmatter binding, so the Project and Services assertion stays as
  their only render check.
- F32: `LabBoundaryTests` and `LabInventoryAndSelectionTests` inherited
  `RootClosureTests`, so its three tests ran three times and every class
  rendered the root and all nine LABs again. A test-free `RenderedModels`
  fixture now gives each class the models from one `functools.cache` render
  per process. The cache does not keep a failed render, so a render failure
  still fails every class that needs it.
- F33: the tracked-file scan split `git ls-files` output on whitespace, which
  broke paths that hold a space. It now reads `-z` output split on NUL. A
  scratch repository with `a b.md` and `한글 문서.md` showed the old split
  breaking both names and the new one keeping them.

Measured with a counting `docker` wrapper on `PATH`: 12 tests in 50 s and 20
`docker` calls, against 18 collected tests in 105 s on `main`. The main run's
call count was not measured; the code implies 58 (three class setups of ten
renders, three times nine target probes, one HOME render).

PR #439 head `58ae9cf6d`: `candidate-quality` passed in run `38344705466` (4m16s).

### W6 RED Proof for Contracts 11 and 12 — 2026-10-13

The owner asked on 2026-10-13 to check criterion 6 and proceed ("SPEC-0215 C6
점검후 진행"). The Evidence row "Inventory and selection tests" said "New tests
RED then GREEN", but the W6 table records that the contract 11 test and both
contract 12 tests passed on first run; only the contract 9 and 10 tests had a
witnessed RED. That row's wording overstated it and now names the split.

**Against the 0.1.0 source.** The three current tests, with
`tests/validation/test_lab_isolation.py` copied from `ec0877f10`, were run in
detached scratch worktrees of two earlier commits:

- `ba9bdd3f3` (2026-10-08, the commit that added the SPEC-0215 Spec): 3 tests,
  OK.
- `f88eb6601` (TSK-0002's baseline): `test_home_prometheus_scrapes_no_lab_container`
  and `test_no_document_or_script_starts_the_root_with_every_profile` OK.
  `test_home_selection_starts_no_lab_or_alternate_gateway` first errored only
  because POL-0078 lived at `docs/05.operations/policies/0078-compose-profile-vocabulary.md`
  before the 2026-10-12 renumbering; with that path it passed.

So the 0.1.0 source already met contracts 11 and 12. These three tests are
characterization tests; no RED against 0.1.0 exists, and criterion 6's clause
"fail against the 0.1.0 source or documents" cannot hold for them. That
clause needs an owner decision.

**Guard sensitivity.** In this worktree on `ec0877f10`, three temporary edits,
never committed:

- appended `# - targets: ['cassandra-node1:9100']` to
  `infra/06-observability/prometheus/config/prometheus.dev.yml`;
- appended `docker compose --profile '*' up -d` to `README.md`;
- put `` `nginx` `` first in POL-0078's `| HOME |` row.

```bash
T=tests.validation.test_lab_isolation.LabInventoryAndSelectionTests
python3 -m unittest $T.test_home_prometheus_scrapes_no_lab_container \
  $T.test_no_document_or_script_starts_the_root_with_every_profile \
  $T.test_home_selection_starts_no_lab_or_alternate_gateway
```

With the edits: 3 tests, `FAILED (failures=3)`, one failure per test. After
`git checkout --` of the three files: 3 tests, OK. Each guard fails when its
contract is broken.

### Owner Decisions

On 2026-10-13 the owner chose "Count mutation RED and accept" through
AskUserQuestion. SPEC-0215 criterion 6 (Spec 0.3.0) now counts a targeted
mutation that fails a guard as its RED when the 0.1.0 source already met the
contract. The "Contract 11 and 12 mutation" PASS row therefore resolves the
"Contract 11 and 12 at 0.1.0" FAIL, and the owner accepted criterion 6.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0215-TSK-0002 | draft | ready | #current-readiness-review-on-2026-10-22 |
| SPEC-0215-TSK-0002 | ready | in-progress | #current-execution-review-on-2026-10-22 |
| SPEC-0215-TSK-0002 | in-progress | completed | #current-completion-decision-on-2026-10-22 |

### Current bounded closure scope on 2026-10-22

The review covers only existing W5–W8, criteria 4–7 PASS evidence and criteria
6/7 acceptance. It reuses the owner's 2026-10-13 criterion 6 mutation RED decision
and the existing HOME/LAB execution records. Cleanup of the 27 volume records
under Owner actions remains a separate residual outside the accepted completion
criteria; no deletion or new observation of those records ran today.

### Current readiness review on 2026-10-22

The review checked the owner's current status/lifecycle request, the approved
parents, this Task's assigned criterion/Work Unit pairs and the existing
PASS/FAIL/acceptance records. Today's document closure review enters `ready`
without backdating historical execution.

### Current execution review on 2026-10-22

The document closure review actually compared the assigned criterion/Work Unit
pairs, existing PASS and FAIL resolution links, acceptance ownership and parent
approvals. Today's work is this document review; historical test and operational
dates and inputs remain as recorded in Evidence. No new runtime, cleanup or
token operation ran.

### Current completion decision on 2026-10-22

Every assigned W5–W8 pair has existing PASS evidence, and criteria 6/7 are
accepted. Mutation evidence and the owner's decision resolve criterion 6's
historical FAIL. Cleanup of the 27 volume records remains with the owner.
TSK-0001 still lacks the C4/W4 legacy-table linkage, so SPEC-0215 as a whole is
not ready for archive review.
Today's closure review marks this Task `completed` while preserving the
historical evidence and acceptance tables exactly. This status does not claim
new operational validation or an archive move.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Exporter retirement | 6 | W5 | Image tag check; renders; catalog and tech-stack sync | `3bc108834` | PASS | W5 MongoDB Exporter Retirement | - |
| Inventory and selection tests | 6 | W6 | Contract 9 and 10 tests RED then GREEN; contract 11 and 12 tests passed on first run; changed-profile gate | `5a16f1844` | PASS | W6 Inventory, Cluster ID, Observability and Selection Tests | - |
| Disposition columns | 4 | W7 | Policy text; HOME selection test; link and metadata checks | `add4cc598` | PASS | W7 Disposition Columns | - |
| HOME residue audit | 5 | W8 | Read-only `docker ps`, restart policies, systemd units, crontab | HOME host 2026-10-08 | PASS | W8 HOME Residue Audit and Real LAB Runs | - |
| Local gate | 6 | W6 | Changed-profile gate in a clean worktree; pre-commit over the range | `137650df8` | PASS | Validation | - |
| Real LAB runs | 7 | W8 | `lab.py up`, probe, `down`, leftover count for six LABs | Synthetic roots; `231e070ac` | PASS | W8 HOME Residue Audit and Real LAB Runs | - |
| OpenSearch LAB run | 7 | W8 | `lab.py up`, cluster health, `down`, leftover count | Synthetic roots; host disk 66%; `e0e19cdcf` | PASS | W8 HOME Residue Audit and Real LAB Runs | - |
| Contract 11 and 12 at 0.1.0 | 6 | W6 | Current contract 11 and 12 tests run against `ba9bdd3f3` and `f88eb6601`; all pass, so no RED against 0.1.0 | `ba9bdd3f3`, `f88eb6601` | FAIL | W6 RED Proof for Contracts 11 and 12 — 2026-10-13 | - |
| Contract 11 and 12 mutation | 6 | W6 | One uncommitted mutation per contract: 3 failures; restored: OK | `ec0877f10` | PASS | W6 RED Proof for Contracts 11 and 12 — 2026-10-13 | Contract 11 and 12 at 0.1.0 |
| Single collection and exact path list | 6 | W6 | Module run with a counting `docker` wrapper; scratch space-path check | `test_lab_isolation.py` on `5bf0e9479`, rebased on `4af41f1a8` | PASS | W6 Follow-up: Single Collection and Exact Path List | - |
| W6 follow-up remote candidate | 6 | W6 | `candidate-quality` on PR #439 | `58ae9cf6d` | PASS | W6 Follow-up: Single Collection and Exact Path List | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 6 | accepted | Exporter retirement, Inventory and selection tests, Local gate, Contract 11 and 12 mutation, Single collection and exact path list, W6 follow-up remote candidate | Owner accepted 2026-10-13 |
| 7 | accepted | Real LAB runs, OpenSearch LAB run | Generation 5 row acceptance |

## Review and Completion

Criteria 6 and 7 are accepted. Criterion 6 was accepted by the owner on 2026-10-13 after the contract 11 and 12 mutation RED proof (Owner Decisions). The volume cleanup below stays with the owner.

Owner actions, which this session may not take:

- Remove the 27 `hy-home-lab-*` volume records that point into session
  scratch directories, with `docker volume rm` on each name that
  `lab.py check` reports. They hold no HOME data.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [First Task](tsk-0001-lab-isolation-and-service-selection.md)
