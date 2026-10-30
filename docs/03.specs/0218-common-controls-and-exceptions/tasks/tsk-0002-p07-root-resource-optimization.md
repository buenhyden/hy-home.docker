---
title: "P07 Root Resource Optimization"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-30"
layer: "specs"
artifact_id: "SPEC-0218-TSK-0002"
parent_ids:
- "SPEC-0218-PLAN-0001"
created: "2026-10-11"
---

# P07 Root Resource Optimization

## Overview

### Objective

Continue existing common controls with measured root-service resource and
least-privilege optimization. Own criterion3's open HOME residual and
criteria6–10 through W9–W16. TSK-0001 and W1–W8 retain their original bytes,
criteria and historical source/LAB/initial-budget evidence. Admission and
source preparation do not close this Task or prove runtime savings.

## Inputs and Authorization

The user's P07 execution prompt and subsequent coordinator instructions
authorize public preparation, scoped implementation, and tests. Future delivery
uses one PR for its owning Spec; before merge, refresh it to the current target
head and obtain applicable current-head CI and an independent review. Do not
create a new Spec or repeat implemented controls v2,
DEV/MNG, Influx retirement, k6/OTLP or Wiki preparation. Learning apps and
actual Wiki engines, clients, collection, DB, schedules, model pulls and
external workspaces are excluded. LAB runtime, images, secrets and data are
excluded; P08 owns its document movement.

Admission input is `4c83f14b11a77e13e582eb85d0bf256685472a95`. On 2026-10-11,
the coordinator directly rechecked remote main, origin/main and local main
and found all three equal to that full SHA. Recheck exact remote main,
origin/main, HEAD, worktree/index state and ownership before implementation.
The reviewed issuance commit becomes the worker's baseline; record its full
SHA rather than guessing a commit that has not been created.

### Exclusive Writer and Reuse

One worker uses branch `codex/p07-root-resource-optimization` and worktree
`/home/hyunyoun/data/hy-home.docker/.worktrees/p07-root-resource-optimization`
from the reviewed issuance commit. Other writers are active: never reset,
stash, clean, stage or overwrite their changes. Initial exclusive files are:

- This Task and its execution evidence.
- `infra/09-platform-ops/resource-optimization/README.md`,
  `measurement.schema.json`, `fixtures/README.md` and synthetic JSON fixtures
  named `*.synthetic.json` in that fixture directory.
- `scripts/lib/ops/root_resource_assessment.py` and
  `scripts/operations/root-resource-assessment.py`.
- `tests/lib/ops/test_root_resource_assessment.py` and
  `tests/validation/test_root_resource_contract.py`.

Reuse `compose_controls.check` and `deviations`, controls/exception schema v2
and the existing inventory projection. Do not create another renderer,
registry, inventory or fixed service count. The current `compose_controls`
CLI renders root and LAB models and has no root-only CLI scope. Do not run
an invented root-scope flag; isolate/reuse pure APIs. Any CLI enhancement is
proposal-only to the coordinator.

The initial helper consumes explicitly selected, bounded, sanitized public
JSON and numeric facts. No Docker access, private `.env`, raw logs, secret
files, ambient API or actual host interrogation is allowed in that source
unit. Required unknown load values remain unknown and block optimization.
Every new folder and parent family gets Korean README navigation from its
owner; shared parent README edits are proposals.

### Shared Owners and Mutation Boundaries

After issuance, Spec/Plan edits, common controls and exceptions, shared
`compose_controls`/baseline tests, root/leaf Compose, environment, gateway,
Alloy, backup, catalog, Registry, manifest/workflow registration, m0021
inventory, version projections, parent indexes and POL-0001 are proposals.
Supply exact current base blobs, scoped hunks, consumers, tests and rollback;
one coordinator integrates each shared file once.

Prefer exact root leaf changes. Every proposed common-template change needs
a static comparison proving zero LAB effective-config delta and preservation
of existing LAB exception rows. This is a source comparison, with no LAB
runtime execution or ownership transfer.

SEC01 owns images; SMTP01 owns canonical SMTP and the COMM-003 executor;
CLN01 owns retirement assessment/deletion routing; P01 owns OpenBao; P03 owns
endpoint contracts; P04/P05 own workloads; P06 owns secret delivery. No P07
worker acquires their files or operating targets through this Task. Actual
benchmarking, observations and runtime changes require an exclusive window
for the named service and independent IaC/security review before mutation.

## Work Log

### W9 Admission and Blocking Facts

Prepare current root classification from the canonical include/service graph
and inventory. For each retained service, record consumer/data owner, role,
upstream/downstream, cadence, failure cost and idle/startup/steady/peak/
backfill/backup/recovery/GPU demand. Declared, running, healthy, used and
recovered are separate states. Use NO_CHANGE, IMPLEMENT, VERIFY_RUNTIME,
DELETE, BLOCKED_FACTS or OUT_OF_SCOPE; no traffic or disabled profile alone
proves absence. Refer deletion to CLN01 and its owning executor.

On 2026-10-11, the dedicated worktree was clean at entry: `git status --short`
produced no entries, `git branch --show-current` returned
`codex/p07-root-resource-optimization`, and `git rev-parse HEAD` returned
`88ecf9049ff0fc25675dce93fd21870266fbad18`. `git rev-parse main origin/main`
returned `4c83f14b11a77e13e582eb85d0bf256685472a95` for both references; direct
`git ls-remote origin refs/heads/main` exited 0 with that same SHA. This is a
baseline only. It ran no classification, Docker/native observation, load,
resource or privilege change, HOME action, or recovery.

W10 preparation is confined to its exclusive public schema, synthetic fixtures,
bounded assessment helper and two dedicated tests. Inputs remain sanitized,
bounded public JSON and numeric facts through existing pure `compose_controls`
APIs. Docker, private environment, raw logs, secret access, ambient-host access,
an invented root-only CLI flag, and all load/resource/permission/HOME changes
remain excluded or NOT_RUN pending the named service contracts and window.

At the admission input, the earlier pure `validate_service_inventory` subset
returned 14 findings: seven P04 `compose.workflow.override.yml` Guide bindings
and seven inventory membership entries. Its wrapper exited0 but the findings
are a semantic FAIL. The coordinator's official operations catalog run then
failed with exit1 and 22 findings in 16.593 seconds: one include drift, seven
missing profile declarations, those seven Guide bindings and those seven
membership entries. These are BLOCKED_FACTS about the existing overlay, not
seven new services. P04/coordinator owns typed overlay projection repair;
blanket include/profile acceptance or P04 native changes are not that repair.
Public preparation may proceed; final inventory and full operations acceptance
wait for the repair and actual relevant gate results.

The official command was `/tmp/hy-home-p09-qa/bin/python
scripts/validation/check-operations-catalog.py`, bound to the admission SHA.
Its receipt is `.agent-work/p07-baseline-operations-catalog.json` and its
public log is `.agent-work/p07-baseline-operations-catalog.log`, SHA256
`1842a0016ac6e52c900fdcf6baadb4522a93068bafb8b539960aa699ccc09c35`.
These are SOURCE/STATIC facts; no Docker, private input or native action ran.

At the issuance HEAD, no P07 repair was attempted. The catalog command
`rtk proxy /tmp/hy-home-p09-qa/bin/python
scripts/validation/check-operations-catalog.py` first stopped on the sandbox
`bwrap` loopback environment error, then completed on the approved rerun with
exit1 and the same 22 P04-overlay findings (one include drift, seven missing
profiles, seven Guide bindings and seven inventory memberships). This remains a
SOURCE/STATIC BLOCKED_FACTS result owned by P04/coordinator, not seven new
services and not authorization for blanket include/profile acceptance.

Current dependent evidence remains bounded: SEC01 criterion15 is not ready;
SMTP's historical isolated snapshot restore proves only two-file usability,
not production send/authentication, external retirement or full recovery;
CLN01 has unresolved five-axis consumers and COMM-003 stays with SMTP;
P01 HOME/snapshot restore is held; P04/P05 native acceptance is NOT_RUN;
P06 criterion20 remains open. These are coordinator handoff facts, not
independent runtime observations by this Task. Relevant service readiness,
not an unqualified global completion claim, controls load and mutation in
W12–W15. W11 read-only baseline observation has its separate boundary below.

### W10 Public Assessment and Synthetic Tests

W9's recorded admission and ownership substep is sufficient to start W10;
final classification and inventory GREEN are not source-preparation
prerequisites. Their unresolved facts remain blocked without preventing
bounded public schema, synthetic fixtures or refusal tests.

Define measurement provenance, full source/image/config identity, environment,
workload, units, sample window, cadence, demand phase, numeric budgets and
unknowns. Record CPU throttling, RSS/application heap/work_mem/connections,
tmpfs/SHM/cache/off-heap, worker concurrency, PID peak, OOM/exit, latency,
throughput and recovery time where applicable. Validate bounded inputs,
unknown measurements, contradictory facts and refusal of private/raw data.
Witness focused RED before implementation, then GREEN and meaningful branch
coverage of at least 80%; fixture PASS proves only SOURCE/UNIT/STATIC.

### W11–W15 Measured Service Changes

For W11 read-only baseline observation, bind the exact host/service, deployed
image/platform/digest, read-only tool permission, Task-recorded observation
window and sanitization. Coordinate a lease against concurrent rollout;
record source target and deployed identity separately. SEC security acceptance
or successful restore is not required merely to observe currently running
services. Unreadable private inputs stay UNKNOWN. The initial W10 helper
still consumes public JSON only and gains no Docker access from this boundary.

Before benchmark/load, permission/configuration change or deployment in
W12–W15, bind the selected root model, accepted image/function/workload,
endpoint, fixtures, private input owner, budget, consumer, backup and verified
recovery boundary. Use sanitized numeric outputs; never print raw inspect,
logs, credentials or private paths.
Idle RSS alone cannot justify a lower memory limit. Measure application and
kernel overhead together and existing GPU workloads only; no Wiki model or
worker is introduced.

Distinguish actual runtime UID/GID from initialization chown/privilege drop.
Keep cap_drop ALL and prove exact required capabilities. Observe required
data/log/socket/cache/tmp write paths before selective read-only rootfs.
Check secret file UID/mode, parent traversal, inode replacement and reload;
grant no secret group to a service without a consumer. Restrict Docker socket
endpoints through the existing proxy; read-only mounts alone do not restrict
the administrative API. No recursive data chown, blanket rootfs conversion,
secret permission change or deployment occurs during admission.

Record each remaining root exception's exact scope/file/service/control/value,
reason, impact, mitigation, verification, owner, review deadline and release
condition. Refresh no date without actual evidence. A no-secret service or
one-shot restart policy is ordinary lifecycle, not a blanket exception.
Only changed services receive rollout; do not reuse TSK-0001's recreation list.
Use scoped functional/negative checks and before/after workload results with
the named backup, empty restore, rollback and cleanup boundaries. Preserve
data/outbox state; source revert alone is not recovery.

### W16 Verification and Delivery

Future checks use existing registered owners and the new modules only after
their files exist. The commands below remain verification inputs. Baseline
operations catalog and existing controls UNIT results are recorded separately
below; the other commands and new dedicated modules are NOT_RUN at admission:

```sh
python -m unittest tests.validation.test_compose_baseline_gates.ComposeControlsTests -v
python scripts/validation/check-script-manifest.py
python scripts/validation/check-github-workflow-contract.py
python scripts/validation/check-operations-catalog.py
python scripts/validation/run-ci-gate.py --profile changed --explain
```

The following coordinator-only proposal packet is reserved for the W10 source
freeze; it is not an authorization or a shared-file edit. The exact later
hunks must register the owned assessment CLI only where the current manifest
and workflow contracts require it, and add Korean navigation for the new
owned paths only in these parent READMEs. Rebase each hunk if its base blob
changes; do not stage or integrate it from this worktree.

| Shared proposal target | Current base blob | Proposed purpose | Status |
| --- | --- | --- | --- |
| `.github/workflow-contract.yml` | `0788cfe0197a279660c4effb9d6f4d83ba8e17f9` | Route both owned W10 modules through the existing repository-integrity leaf and changed-root rule | unsubmitted, coordinator only |
| `scripts/manifest.yaml` | `0f2c2ac06382dc1d8da401431a4d4b9dfb0cb0da` | Register the owned library and operation paths with their consumers and tests | unsubmitted, coordinator only |
| `infra/09-platform-ops/README.md` | `d80d80c56b56f0222b35786fcbc0dacd110ba177` | Korean navigation for `resource-optimization/` | unsubmitted, coordinator only |
| `scripts/lib/ops/README.md` | `746a5399a34f4eac01a7281eeda7e7b5d5bd7ca7` | Korean navigation for the owned helper | unsubmitted, coordinator only |
| `tests/lib/ops/README.md` | `6d31046a967c340eba2a28b47556b3abe5015eda` | Korean navigation for the dedicated unit module | unsubmitted, coordinator only |
| `tests/validation/README.md` | `44cc4806c23baaee2a840b91bff77ebdf58e0cf1` | Korean navigation for the dedicated contract module | unsubmitted, coordinator only |

The exact intended manifest proposal, subject to the source-freeze diff, is
one `library` row for `scripts/lib/ops/root_resource_assessment.py` and one
`operations` row for `scripts/operations/root-resource-assessment.py`. Both
name `infra/09-platform-ops/resource-optimization/README.md` as authority,
`mutation: none`, `lifecycle: active`, `disposition: retain`, and no successor.
The library row names the CLI and both dedicated test modules as consumers;
the operations row names the resource-optimization README and contract test as
consumers. The rows cite the two dedicated test modules.

The exact workflow proposal reuses an existing typed route: in
`leaf.repository-integrity-regressions` (current lines 764–803), add
`tests.lib.ops.test_root_resource_assessment` and
`tests.validation.test_root_resource_contract` to `argv` immediately before
`-v`. Add one `changed_root_rules` sibling beside the existing Wiki rule
(current line 1768), with prefixes for
`infra/09-platform-ops/resource-optimization/`,
`scripts/lib/ops/root_resource_assessment.py`,
`scripts/operations/root-resource-assessment.py`,
`tests/lib/ops/test_root_resource_assessment.py`, and
`tests/validation/test_root_resource_contract.py`; its `root_gate_ids` are
`leaf.repository-integrity-regressions` and `leaf.local-script-manifest`.
This adds no new gate. Root `README.md`, `infra/README.md`, Registry and
catalog have no P07 hunk in this packet.

W11's next action is an input-binding request, not an invented runtime
command: record the exact host and service, deployed image/platform/digest,
read-only tool permission, sanitized output destination and observation window
coordinated against concurrent rollout. Only after those values and the
service-owner command contract are supplied may the Task record that exact
read-only command and result. W12–W15 additionally remain NOT_RUN until their
accepted image/function/workload/endpoint/budget/consumer/backup/recovery
inputs and exclusive service window are bound.

After new source/test creation, run its two dedicated modules, required
manifest/workflow registrations, selected metadata/links and the actual
changed-profile plan. Record exact commands, input/index/base/history hashes,
tools, timeout, exit codes, failures and independent code/security review.
Per-service IaC review precedes any mutation. All unexecuted operational
checks remain NOT_RUN with a concrete next command/input in this Task.

Keep logical commits by service/source unit. Future delivery uses one PR for
its owning Spec. Before that PR merges, refresh it to the current target head
and obtain applicable current-head CI and an independent review. Formal
issuance remains a logical commit on the isolated admission branch, and its
reviewed SHA can start public source/synthetic preparation, not delivery
acceptance. Do not merge before the P04/coordinator repair and relevant gates
and review. Run local-staged after staging the reviewed candidate.

### Scope Reconciliation Receipt — 2026-10-12

Baseline: `23e37362b72e98028a4675f282819c0346ae59dc` (the coordinator's
current main input). This receipt changes only the future delivery instruction:
an owning-Spec PR, current-target-head CI, and independent review are required
before merge. It does not rewrite prior issuance, validation, or delivery
receipts.

P07 common-control source and helpers are `NO_CHANGE`; no infra, image,
resource, LAB runtime/service/data/secret, or test change is authorized by this
receipt. Source demand classification, measurement, and native HOME observation
remain `NOT_RUN` pending their existing exact target, owner, permission,
window, workload, backup, and recovery bindings. The correction is reversible
by reverting its logical documentation commit; that revert does not change
runtime state, delivery state, data, secrets, or recovery evidence.

The coordinator's selected metadata check covered this Plan and Task with two
selected documents and zero violations, exit0. The changed-profile local-only
gate failed on two existing baseline image-projection pins, not a P07 resource
change. SPEC-0204 is the sole metadata writer for the prepared correction;
independent review is pending, and its approved metadata commit must be
fast-forwarded into P07 before final checks. This is neither a local-gate GREEN
result nor remote CI evidence.

After that approved metadata commit was fast-forwarded to
`854ccc249b05ae17a9eb650a091676cdcf7e87e0`, the changed-profile local-only
gate against base `23e37362b72e98028a4675f282819c0346ae59dc` passed. Two
independent reviewers approved the preceding P07 Plan/Task source and schema
diff with no findings. Re-review of this result-only receipt is APPROVE with
no findings. Their review covers neither HOME nor runtime, migration, recovery,
or remote CI acceptance.

Result-only validation receipt: candidate HEAD was
`854ccc249b05ae17a9eb650a091676cdcf7e87e0`; the exact two-file candidate
blobs were Plan `81b62987de551d7576e8845ddccf84801902b6e7` and Task
`907b5a507cd21e4466272677db8fbdfae39bafff`. The staged index contained only
those two paths and was observed unchanged after validation; its tree hash was
not recorded and is `UNKNOWN`. The commands below wrote no tracked receipt;
their terminal output and this Task are the evidence location:

```sh
env PATH=/tmp/hyhome-coord-qa/bin:$PATH python3 scripts/validation/run-ci-gate.py --profile changed --local-only
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD
git diff --check
env PATH=/tmp/hyhome-coord-qa/bin:$PATH bash scripts/validation/run-ci-precommit.sh --mode local-staged
git commit -m 'docs(p07): Align future delivery with reviewed PRs'
```

Each command exited0. The first used base
`23e37362b72e98028a4675f282819c0346ae59dc`; metadata used explicit `HEAD`
with merge base `854ccc249b05ae17a9eb650a091676cdcf7e87e0`. The commit created
`b84f7514590bd1889fc9c3e92fb831d58dd094fa` with the same two paths. No
`cz` message-file command was executed for that already-created commit.

The global Node `cz` inspected during the later result-only correction was not
the configured checker. The post-audit used the isolated QA environment's
Python checker and succeeded, exit0:

```sh
/tmp/hyhome-coord-qa/bin/cz check --message-length-limit 75 --rev-range 854ccc249b05ae17a9eb650a091676cdcf7e87e0..242ed0abe7037dc5dc5cda1b548666dc2a8d9aac
```

This validates the commit range after the fact; it does not assert an earlier
pre-commit `cz` invocation.

### Main Integration Continuation — 2026-10-12

Input is delivered main `b70bc01b58ae35a486860377519155a882af3d76`, produced
through [SPEC-0204 PR #425](https://github.com/buenhyden/hy-home.docker/pull/425).
This P07 branch merges that main normally from `a69bda497c170d28416705e7656402f8774d7675`;
it retains delivered shared version and security-ledger content from main. Its
continuation owns only this Plan and Task, with the exceptions-policy reference
resolved under P08's numbered layout. P07 helpers/resources are `NO_CHANGE`;
no benchmark, native/HOME, runtime, deployment, LAB runtime/testing, secret or
data action ran. Delivery remains pending the owning SPEC-0218 PR, its
current-head CI, and independent review; reverting the later P07-only commit
removes this continuation record without rolling back delivered main.

### Remote Source Adoption Audit — 2026-10-13

At observation, the integration started from delivered main
`b70bc01b58ae35a486860377519155a882af3d76`; the current remote main is
`98144b2c0b5738f272b6a628246c901945ba15bf`, the same P07 integration. The
pre-audit source blobs are Plan `81b62987de551d7576e8845ddccf84801902b6e7`
and Task `721e373de619cf30e9dad3f8260dd5d46dfebc00`. The CI owner observed a
successful branch push and a `gh pr create` exit1 because there were no commits
between the feature branch and main; no P07 PR was observed. The source-adoption
route is therefore `UNVERIFIED`, not retroactive PR delivery or human approval.

This is a source-only audit: P07 source is `NO_CHANGE` on current main, with no
resource, image, native, LAB-testing, deployment, secret, or data action. The
observed main-security result is SOURCE/SARIF evidence, not a PR-candidate
acceptance. A new owning SPEC-0218 receipt PR is planned; its current-head CI
can validate only this receipt and current boundary, while original source-route
proof remains unproved. Native/HOME, runtime, migration, rotation and recovery
remain `NOT_RUN`.

### Admission Document Validation History

The initial selected metadata check failed with exit1 and 146 violations
after the new Plan Dependencies cells contained prose rather than Work Unit
identities. Correcting only those new cells to W9–W15 references or None
resolved the package error; no archive, validator or historical Task changed.
The corrected canonical package loader then parsed 25 Spec Packages, exit0.
The subsequent metadata check selected three admission documents with zero
violations, exit0. That PASS belongs to those prior document bytes, not to
later factual updates or the unimplemented assessment source. The final
Plan/Task selected check must be recorded against its actual input hashes.

The coordinator ran the existing
`tests.validation.test_compose_baseline_gates.ComposeControlsTests` at the
admission SHA: 11 tests passed in 0.042 seconds, exit0, with public output in
`.agent-work/p07-existing-controls-tests.log`. This is existing-control reuse
UNIT evidence only. No new P07 helper, schema or fixture exists; no Docker,
HOME, benchmark, permission, migration, rotation or recovery check ran.

### Segmented Local Source Validation — 2026-10-11

Frozen source input is `5b1a92db48fd508feff4cee0753b3b4468dd41dc`, following
common/worker integration `c7d56a383ad8b77dd615327d11605b3e15d2146e`.
The registered local execution plan has33 nodes; public explain exposes10.
The front-door run exited124 after nodes0–9 passed. First canonical continuation
exited1 at node18; nodes10–17 passed. Permission-corrected continuation exited1
at node26; nodes18–25 passed. Final continuation26–32 exited0 with ordinary
Python, debug true/optimization0 and clean unchanged post-input. Thus all33
nodes have segmented successful receipts; the original124 and both suffix1
failures remain failures. No fresh aggregate exit0 or hosted PASS is claimed.

Only two coordinator-checkout entrypoint modes changed775 to755, matching their
tracked100755 modes: Open WebUI and Gatus. File content hashes and index were
unchanged, with Git clean and no HOME/runtime effect. The only source delta
from c7d56a383 is the synthetic workflow fixture's canonical working directory,
seven changed lines in the existing test. RED: one test/four subcase failures,
exit1,1.769s; GREEN:39 tests,exit0,7.492s; Ruff/staged checks exit0 and independent
review ACCEPT. The registered workflow contract SHA256 remains
`bdb1941e522865a9a381b0913f4a8e266dfb613cbb832ca35889ff26ac3ecfc5`.

### Historical Local-Main Source-Preparation Receipt — 2026-10-11

Receipts are `.agent-work/p04-p07-registered-suffix-final-fixture-result.json`,
`.agent-work/p04-p07-checkout-permissions-repair.json` and
`.agent-work/p05-fixture-cwd-receipt.json`; final output is
`.agent-work/p04-p07-registered-suffix-final-fixture.log`. Earlier aggregate and
suffix logs remain preserved. These SOURCE/UNIT/STATIC checks do not complete
operational criteria. At this historical point, local-main source integration
awaited final documentation checks and review; its delivery SHA was not yet
known. The then-current direct-user local-main delivery lane used no dev,
remote push, PR, or hosted execution.

Worker source `8d3569b67e1283e9344f036854658ac0b9f53f15` is preserved; this
receipt keeps this Task's actual draft lifecycle and records source preparation
only. Coordinator P06/P07 four-module checks passed62 in16.592s, exit0; earlier
P04/P05 checks passed196 separately. The P07 manifest's two missing records and
workflow canonical-order failure were witnessed, then corrected common checks
exited0. Six-file common commit c7d56a383 was independently accepted; staged
check exited0, links1216/11727 had0 failures/1 historical warning, and metadata
with four provided paths actually selected1 document with0 violations, exit0.

P04 typed-overlay source repair resolved the earlier official catalog blocker
on its later accepted source; original4c83 inventory/catalog failures remain
historical failures, not new observations. P07's existing85.06percent branch
coverage is not remeasured here. The final repository leaf passed494 tests/
127.874s, exit0. No current deployed demand, performance, exception authority,
permission/read-only configuration, benchmark or HOME rollout is accepted.
W11–W15 and criteria3 HOME residual/6–10 remain open as recorded; no LAB runtime
change occurred. At this historical point, final documentation review and
local-main source delivery were pending and conferred no operational acceptance
or lifecycle closure.

### Availability and recovery targets — 2026-10-21

v22 §9.1 asks for per-function allowed outage and loss, RTO and RPO, restart
order and freshness alerts, without invented numbers. Options were derived
from the current configuration and presented; the owner chose "B 균형형"
(balanced): keep the current schedule and alerting, and measure recovery time
before setting any RTO.

Facts used: REQ-0027 FR-0002 keeps AI/workflow and their required
dependencies always on, with development and experiments opt-in; AD-0031 notes
that one host shares the power, storage, daemon and GPU failure domain and that
backup and restore are unproven. `hyhome-backup.timer` runs daily at 03:30 KST
with `Persistent=true`; pgBackRest takes a weekly full and daily differential
backups with WAL `archive_timeout=300`; Restic keeps 30 daily, 13 weekly and 12
monthly snapshots locally and copies to R2 under the 9 GB cap; the freshness
alert fires 26 hours after the last whole-run success.

| Tier | Members | Allowed outage while the PC is on | RPO | Restart order | Freshness alert |
| --- | --- | --- | --- | --- | --- |
| T1 core | OpenBao, Keycloak, gateway, mng-pg, mng-valkey | Until an operator restores or unseals | 24 h | 1 | 26 h (current) |
| T2 user apps | Open WebUI, n8n, Grafana, Airflow scheduler | Until T1 is back | 24 h | 2 | 26 h |
| T3 development data | dev-pg, SeaweedFS, Qdrant | Longer; development is opt-in | 24 h | 2 | 26 h |
| T4 batch | Airflow DAG runs | Re-run instead of restore | State follows T1 | 3 | Per-DAG SLA, not set |
| T5 observability | Prometheus, Loki, Tempo | Longest | Loss accepted; Loki and Tempo buckets are not backed up | 4 | None |
| T6 optional | ComfyUI, Ollama models | Unlimited | Re-download | 5 | None |

RPO 24 h holds only while the PC is on: when it is off, the loss window runs
back to the last run. After losing the host or its disk, recovery depends on the
R2 copy, which is not yet proven by a restore. The WAL archive gives a shorter
window for a logical PostgreSQL failure on a healthy disk, but B does not set
it as a target.

RTO is not set for any tier. Each is recorded after one measured restore per
tier into `recovery_seconds` of
`infra/09-platform-ops/resource-optimization/measurement.schema.json`; until
then RTO is unknown. Two items come before the measurements: the daily run
exits 1 because the OpenBao snapshot token does not exist until the SPEC-0243
window (W3), and that window's first daily run must exit 0. The B choice needs
no change to the backup schedule and does not affect the R2 cap. S9.1 status:
PARTIAL, targets chosen, RTO pending measurement.

First measured recovery, T5 observability — 2026-10-21: the isolated Prometheus
restore of the 2026-10-20 copy (SPEC-0245 TSK-0001) took 814.4 s to extract
6.7 GB and 55.4 s to `/-/ready`, about 14.5 minutes, while the host load average
was 9–15 and the archive hash read shared the disk. Gatus's SQLite copy
(4.5 MB) opened with `integrity_check` ok in under a second; its stop-copy-start
took 29 s. These are single measurements on a loaded host, not an RTO; T5's
RTO is set after a measurement on a quieter host or after the owner accepts
these figures.

### Current Registration Reconciliation — 2026-10-22

At `d7bec9a9a4318caa60cc0f5f99a1de6cfa71a580`, `scripts/manifest.yaml`
registers the assessment library and CLI with both dedicated test modules;
`.github/workflow-contract.yml` selects those modules and their changed/full
input paths. The two missing registrations and unselected tests in the W10
source-preparation receipt below describe its historical input, not the current
source blocker.

The coordinator's local `full` receipt at that same input records
`leaf.local-script-manifest` `PASS`, exit 0, from
`2026-10-22T07:51:36.547454Z` to `2026-10-22T07:51:58.493487Z`.
The directly read plan/result are under
`/tmp/hyhome-v28-full-d7bec9a9a-umask022-20261022/`; the result binds plan SHA-256
`a33caa34b12a80d030d0339a29d52635348989d2bd8228630cb86c124293a66a`.
The aggregate has 26 `PASS`, one `FAIL` and six `NOT_RUN`; it is not a full
gate PASS. This bounded registration result adds no criterion acceptance,
measurement, native proof or permission change. Canonical exception binding,
service workload and recovery evidence remain open. Historical receipts and
the acceptance tables below are preserved.

### v29 Source Readiness Review 2026-10-22

The current readiness review on 2026-10-22 confirms that SPEC-0218 and its
Plan are approved at version 1.0.0 following PR #559. The direct v29 request
and completed investigation gate bind the existing validator, regression
fixtures, official Python toolchain and exclusive source-writing scope for
the exception-date correction. These inputs are sufficient to start this
bounded public source work, so the Task moves from `draft` to `ready`.
This is today's readiness decision, not a backdated claim about the earlier
P07 implementation or its delivery route. Representative workload, exact
service observation, least privilege and recovery prerequisites remain
unmet for their dependent operational steps.

### v29 Source Execution Start 2026-10-22

The authorized v29 source work began after the investigation gate established
those inputs: exception-date regression tests, witnessed RED results and the
minimal shared validator correction are recorded below. Following the current
readiness decision, this state reconciliation records `ready` to
`in-progress` from that observed source execution. It does not claim that the
tests ran again or start W11–W15 runtime work,
accept criteria 6–10, complete P07, or authorize any host, native, credential
or remote action. Historical evidence and acceptance decisions remain intact.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0218-TSK-0002 | draft | ready | #v29-source-readiness-review-2026-10-22 |
| SPEC-0218-TSK-0002 | ready | in-progress | #v29-source-execution-start-2026-10-22 |

### v29 exception-date boundary correction — 2026-10-22

The direct v29 continuation and the completed investigation gate authorize this
bounded P07 source correction on baseline
`49fd95a6ed482d7194c840b43b73a030be6f3d5d`. The shared validator accepted both
a future `reviewed` date and a `review_by` before `reviewed`. It now rejects
both, while accepting today's deadline and the existing 366-day maximum.
No registry entry, service control, deadline, template, or LAB model changed.
POL-0001 states those exact date boundaries and clarifies that `--report`
does not inventory rootfs, UID, host namespaces or Docker socket authority.
The monthly cadence and existing 2027-04-07 deadlines are preserved; their
owner's scheduling interpretation is not replaced by a new 30-day rule.

TDD used the existing official Python 3.14.8/controller-lock environment at
`/tmp/hyhome-v28-toolchain-venv`. Before production edits,
`python -m unittest
 tests.validation.test_compose_baseline_gates.ComposeControlsTests
 tests.lib.ops.test_storage_write_rate -v` ran 28 tests and exited 1 with
22 failing subcases and three errors across the date and W7 regressions.
The focused corrected run passed all 28 in 0.599 s. A later finite-calculation
boundary test was included in the full affected-module run:

```sh
/tmp/hyhome-v28-toolchain-venv/bin/python -m unittest \
  tests.validation.test_compose_baseline_gates \
  tests.lib.ops.test_storage_write_rate \
  tests.lib.ops.test_root_resource_assessment \
  tests.validation.test_root_resource_contract -v
```

The run used umask 022, with all seven native-rehearsal opt-ins explicitly
unset (`HYHOME_PG_REHEARSAL`, `HYHOME_SSO_REHEARSAL`,
`HYHOME_STORYBOOK_REHEARSAL`, `HYHOME_CDC_REHEARSAL`,
`HYHOME_BACKUP_REHEARSAL`, `HYHOME_SEAWEEDFS_REHEARSAL`,
`HYHOME_MAIL_REHEARSAL`). It exited 0: 163 tests counted, 133 PASS and
30 declared native SKIP, in 31.727 s. This includes the resource evaluator's
shared-validator callers and synthetic CLI checks; static public Compose
rendering is not a runtime rollout. Scoped Ruff 0.15.12 check and format
passed for the five changed Python files.

The pinned environment has no installed `coverage` module; no dependency was
added. A requirement-scoped rerun of 29 tests under standard-library `trace`
exited 0 and measured `compose_controls.check` statement-line coverage at
58/59 (98.31%). This is selected-function statement-line coverage, not branch,
whole-module, deployed-service or runtime coverage. Its source SHA256 is
`4abaecd36d1c4ca98b989249e2b153b1b01f371016fcacfcce939b79f7089fc5`.

Mode-0600 retained receipts: `/tmp/hyhome-v29-resources-red.log` SHA256
`aea436b80bda67f1071266b6d697876dd80474f1b71cc7bffa9a15df24368b48`;
`/tmp/hyhome-v29-resources-green-focused.log` SHA256
`64db5032f078c851326737f1aec4766f7d2e795462fae269087d7ae4238c67c3`;
`/tmp/hyhome-v29-resources-green-full.log` SHA256
`8554f27583544e24a8fdf717c406b757dd42a7a3c3df3fad66926d3ec4c8a3bf`;
`/tmp/hyhome-v29-resources-coverage.json` SHA256
`eb8f1e6d66bcdd350c46a3a16ea0b37ed90985917f67fbfeb948bb40f926278d`.
The latter binds the exact measured source and names the coverage scope.

This source-only correction changes no Criterion Acceptance. The current
readiness and source-execution events above establish `in-progress` only.
Canonical exception binding, representative workloads, measured
budgets, least privilege, service recovery and HOME acceptance remain with
W11–W16 and their existing owners. No load, actual W7 collection, secret,
Docker runtime mutation, token action or remote write ran. Root retains final
registered gates, independent review and commit ownership.

### Handoff from SPEC-0204 TSK-0013 2026-10-30

SPEC-0204 TSK-0013 (P05 n8n notifier) is final at `main`
`c585c5244`. Its only measured facts that bear on P07 are timings from one
native fixture run on 2026-10-30. A scheduled delivery took 23 s from
activation, and the whole native class took 1,221.6 s. Fixture caps were
40 minutes total and per-container resource caps from `RESOURCE_CAPS`.
NOT_RUN: CPU, memory and polling-load measurement of the notifier. Next input:
measure the notifier's one-minute polling load on HOME when P07 W11 binds
its inputs.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Issuance baseline | 6 | W9 | Worktree and main-reference recheck | HEAD `88ecf9049ff0fc25675dce93fd21870266fbad18`; main/origin `4c83f14b11a77e13e582eb85d0bf256685472a95` | PASS | Clean branch; `git status --short`, `git branch --show-current`, `git rev-parse`, `git ls-remote` exit0; baseline only | - |
| Public classification | 6 | W9 | Current root consumer/demand classification | Reviewed issuance commit pending | NOT_RUN | W9 public preparation contract above | - |
| Inventory subset blocker | 6 | W9 | Coordinator-reported pure validate_service_inventory subset | Admission main 4c83f14b11a77e13e582eb85d0bf256685472a95 | FAIL | 14 overlay binding/membership findings; wrapper exit0 is not semantic PASS | - |
| Official operations blocker | 6 | W9 | check-operations-catalog.py | Admission main 4c83f14b11a77e13e582eb85d0bf256685472a95 | FAIL | .agent-work/p07-baseline-operations-catalog.json and .log; exit1, 22 findings, 16.593s; SOURCE/STATIC only | - |
| Current operations blocker | 6 | W9 | `rtk proxy /tmp/hy-home-p09-qa/bin/python scripts/validation/check-operations-catalog.py` | Issuance HEAD | FAIL | Sandbox `bwrap` environment error, then approved rerun exit1 with the same 22 P04-overlay findings; no repair | - |
| Public assessment RED | 7 | W10 | Dedicated unittest modules | Issuance HEAD; tests only | PASS | RED witnessed: initial sandbox artifact; escalated rerun exit1 with missing helper ImportError and four missing-schema FileNotFoundError | - |
| Public assessment GREEN | 7 | W10 | Dedicated assessment and contract modules with branch coverage | Final frozen public W10 source/fixture inputs below | PASS | exit0, 30 tests in 13.068s after security-token corrections; tracked fixture SHA256, exact blocker lists and CLI exit1 checked; SOURCE/UNIT/STATIC only | - |
| W10 source quality | 7 | W10 | Branch coverage and Ruff | Frozen owned helper/CLI and dedicated tests | PASS | 316 statements, 32 missing (89.87%); 154 branches, 23 missing (85.06%); combined 88.30%; Ruff check and format --check PASS | - |
| W10 workflow contract | 7 | W10 | Workflow-contract validator | Existing shared contract, unmodified | PASS | 5 workflows, 7 jobs, 8 actions; this does not route the new dedicated modules | - |
| W10 manifest integration | 7 | W10 | Script manifest validator | New helper and CLI staged; shared manifest unmodified | FAIL | exit1, exactly two missing records: `root_resource_assessment.py` and `root-resource-assessment.py`; coordinator-only proposal required | - |
| W10 document contracts | 7 | W10 | Selected metadata and document links | This Task and the two owned READMEs | PASS | metadata check-changed: selected3, violations0, exit0; links --mode all: failures0, warning1, exit0; official package loader: 25 packages, exit0 | W10 manifest integration |
| W10 staged style | 7 | W10 | Official local-staged check-only controller | Ten-file candidate tree c65338beaa6865f65871e481944c743c9cf93075 | PASS | exit0; applicable JSON/Markdown/Ruff/hardcoded-secret and generic checks passed; no candidate mutation; later result-only Task update requires final repetition | - |
| W10 independent code review | 7 | W10 | Read-only code-reviewer of exact staged diff and result-only Task delta | Issuance HEAD to frozen nine-source-file diff and Task evidence; source SHA256 below | PASS | approve; all reproduced platform/time/limits/provenance/path/fixture findings resolved; 28 tests, branch85.06%, Ruff and diff checks independently verified; main/operations acceptance excluded | - |
| W10 token correction and independent re-review | 7 | W10 | Malformed and conflicting security_opt regressions; code-reviewer and security-auditor | Schema, unit test and README affected delta; unchanged library/CLI slice reused | PASS | Both malformed substring and conflicting true/false inputs witnessed RED; exact enum plus maxItems1 fixed them. Code reviewer: 2 focused tests exit0, 0.309s, approve; security auditor: 2 focused tests exit0, 0.289s, approve; no remaining Critical/Important findings | - |
| Service observations | 6, 7, 8 | W11 | Sanitized read-only numeric/runtime facts | Exact service window not bound | NOT_RUN | Native prerequisite contract above | - |
| Measured resources | 7 | W12 | Representative application/GPU workload comparison | Workload and measurement values unknown | NOT_RUN | Initial budgets are not optimal measurements | - |
| Least privilege | 8 | W13 | UID/capability/rootfs/secret/socket functional and negative checks | Exact service/image/restore pending | NOT_RUN | No permission/runtime action at admission | - |
| Existing control reuse | 8 | W13 | Existing ComposeControlsTests | Admission main 4c83f14b11a77e13e582eb85d0bf256685472a95 | PASS | .agent-work/p07-existing-controls-tests.log; 11 tests, 0.042s, exit0; UNIT only, native acceptance open | - |
| Existing control reuse, issuance recheck | 8 | W13 | `rtk proxy /tmp/hy-home-p09-qa/bin/python -m unittest tests.validation.test_compose_baseline_gates.ComposeControlsTests -v` | Issuance HEAD | PASS | Initial sandbox `bwrap` artifact; rerun exit0, 11 tests, 0.010s; UNIT only and no Docker | - |
| Dependency audit | 7 | W10 | `uv tool run --no-config --cache-dir /tmp/p07-audit-cache pip-audit --path /tmp/hy-home-p09-qa/lib/python3.12/site-packages --cache-dir /tmp/p07-audit-http --progress-spinner off --strict` | Existing isolated QA environment | PASS | exit0, no known vulnerabilities; bounded to QA installed dependencies, not image/runtime or requirements-resolution. Earlier resolver attempts unavailable: missing `pip_audit`/ensurepip; unhashed requirements invocation was setup failure | - |
| Common integration | 9 | W14 | Effective root model and exact exceptions | Owner proposals not applied | NOT_RUN | Coordinator single-writer boundary | - |
| Scoped rollout and recovery | 3, 10 | W15 | Changed-service functionality, backup and empty restore | Exact target/image/workload/recovery pending | NOT_RUN | No HOME, migration, rotation or recovery execution | - |
| Projection and delivery | 9, 10 | W16 | Current-target-head CI and independent review before owning-Spec PR merge | P07 source/helpers present and `NO_CHANGE`; SPEC-0218 docs PR/CI/review/merge pending | NOT_RUN | Future delivery contract above; no SPEC-0218 PR/push/merge receipt | - |
| Segmented source checks | 9, 10 | W16 | Registered local nodes0–32 across preserved runs; final continuation26–32 exit0 | c7d56a383 then5b1a92db; unchanged registered contract | PASS | Segmented Local Source Validation; original aggregate124 and suffix1/1 preserved; final docs/delivery pending | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 6 | pending | - | - |
| 7 | pending | - | - |
| 8 | pending | - | - |
| 9 | pending | - | - |
| 10 | pending | - | - |

## Review and Completion

### W10 Source Preparation Receipt

The changed tracked paths are this Task, the resource-optimization README and
measurement schema, its fixtures README and two synthetic JSON files, the
assessment library and CLI, and the two dedicated test modules. Source-only
preparation adds no inventory copy, operational data, runtime configuration,
image change, secret consumer change or deletion decision. All shared
manifest/workflow/README edits above remain coordinator-only proposals.

The final dedicated command was
`rtk proxy env COVERAGE_FILE=.agent-work/p07-coverage-data
/tmp/hy-home-p09-qa/bin/python -m coverage run --branch
--source=scripts.lib.ops.root_resource_assessment -m unittest
tests.lib.ops.test_root_resource_assessment
tests.validation.test_root_resource_contract -v`, exit0, 30 tests in 13.068s.
Python 3.12 and Ruff 0.15.12 came from the existing isolated QA environment.
Coverage JSON is `.agent-work/p07-coverage-final.json`; its 85.06% branch
coverage applies to the assessment library, not to operating services.
The tests cover public schema/units, missing and nonfinite/deep/duplicate JSON,
private/traversal/symlink/hardlink/nonregular/oversized inputs, identity and
budget contradictions, control exception mismatch and sanitized CLI output.

Independent code-review reproductions added RED failures for required RSS
marked not-applicable, source/control path mismatch, null deployed platform,
future observation day, zero direct/deploy limits, missing/unknown provenance,
and non-normalized public paths. The owner corrected the bounded evaluator and
schema; synthetic provenance cannot be relabelled measurement. Complete
provenance is a declaration, not authenticated receipt or runtime proof.
Every result retains runtime_acceptance=false and mutation_authorized=false.

Frozen source SHA256 values:

| Path | SHA256 |
| --- | --- |
| `scripts/lib/ops/root_resource_assessment.py` | `d8b8ed0fae64932d44ccd9a9ef6b9028a82530fdcf89ff0b7ee27f7d99bcaf3a` |
| `scripts/operations/root-resource-assessment.py` | `1fe217bb088837bfd56efca87d374147bf2e1656558e0da5fe82eaec8f116198` |
| `infra/09-platform-ops/resource-optimization/measurement.schema.json` | `209a52a924f95360c55fa57a4c9fea70347d8731437dcb12ca8a5563fae12ce7` |
| `tests/lib/ops/test_root_resource_assessment.py` | `a3e31d7985917fcd8a3771eb1093c5f86ab9bd16a58e4a72c569cf474aef9a45` |
| `tests/validation/test_root_resource_contract.py` | `977fb43d1cbf73ee70aa7276d2bcf40e8896426f74ad51110aae063678976a49` |

The source-only staged check used
`rtk proxy env PATH=/tmp/hy-home-p09-qa/bin:$PATH bash
scripts/validation/run-ci-precommit.sh --mode local-staged`, exit0. JSON,
Markdown, Ruff and hardcoded-secret checks passed without changing the index
or candidate. The final Task-inclusive reviewed index must repeat this command
immediately before the logical commit. `git diff --cached --check` passed.
The document-link command `check-document-links.py --mode all` exited0 with
zero failures and one existing historical-capture warning (2870 legacy links).
The unchanged workflow validator passed; `run-ci-gate.py --profile changed
--explain` exited0 but did not select the new tests. Manifest registration
still fails with exactly two missing records. No full aggregate or remote
CI acceptance is claimed.

Two metadata runs failed before local corrections: the first reported 150
violations with an invalid criterion/Work Unit pair and README headings; the
next reported 147 with invalid Evidence Acceptance and one fixture table
header. Fixes preserve the canonical result/acceptance vocabulary and package
relations; archive findings from these failed package parses are not an
independently established baseline defect. The corrected official package
loader parsed 25 packages, exit0. The final metadata command selected this
Task and the two owned READMEs with --mode check-changed, --base-ref HEAD and
three explicit --changed-path arguments: selected3, violations0, exit0.
The earlier archive findings disappeared after the owned package corrections.
Independent code-reviewer disposition is approve with no remaining code
findings. It covers the nine frozen source files and the result-only Task
delta; main integration and native acceptance remain outside that disposition.
An Important security finding on arbitrary security_opt strings was corrected
inside the P07 schema: only one exact no-new-privileges true/false token is
supported. Both substring impersonation and conflicting exact tokens were
reproduced RED before the correction. Code and security affected-slice
re-reviews approved the schema/test/README delta and reused the unchanged
source slice; no Critical/Important finding remains. The caller-provided
exception projection is still not bound to the canonical registry. Later
acceptance requires canonical comparison/binding; SOURCE/STATIC preparation,
visible deviations and false runtime/mutation flags do not supply that proof.

Admission creates a draft Task and permits public preparation only. Keep
SOURCE / UNIT / STATIC / ISOLATED / HOME / MIGRATION / ROTATION / RECOVERY /
DELIVERY separate. This continuation remains unfinished while measurements,
native prerequisites, current inventory or assigned criteria lack actual
evidence. Source/schema checks cannot close HOME or recovery acceptance.
Preserve TSK-0001 and all other writers; record every changed file, exclusion,
criterion result, commit/delivery input and next actionable blocker here.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Earlier common-controls evidence](tsk-0001-common-controls-and-exceptions.md)
- [Shared-service integration package](../../0204-service-integration-security-and-operations/spec.md)
- [Canonical service inventory](../../../90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md)
- [Exceptions policy](../../../05.operations/policies/01-common/0001-common-optimizations-template-exceptions.md)
