---
title: "P07 Root Resource Optimization"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-11"
layer: "specs"
artifact_id: "SPEC-0218-TSK-0002"
parent_ids:
- "SPEC-0218-PLAN-0001"
created: "2026-10-11"
---

# P07 Root Resource Optimization

## Objective

Continue existing common controls with measured root-service resource and
least-privilege optimization. Own criterion3's open HOME residual and
criteria6–10 through W9–W16. TSK-0001 and W1–W8 retain their original bytes,
criteria and historical source/LAB/initial-budget evidence. Admission and
source preparation do not close this Task or prove runtime savings.

## Inputs and Authorization

The user's P07 execution prompt and subsequent coordinator instructions
authorize public preparation, scoped implementation, tests and local main
delivery. Do not create a new Spec or repeat implemented controls v2,
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

After new source/test creation, run its two dedicated modules, required
manifest/workflow registrations, selected metadata/links and the actual
changed-profile plan. Record exact commands, input/index/base/history hashes,
tools, timeout, exit codes, failures and independent code/security review.
Per-service IaC review precedes any mutation. All unexecuted operational
checks remain NOT_RUN with a concrete next command/input in this Task.

Keep logical commits by service/source unit. The current delivery lane is
reviewed local main, with no dev merge and no required PR, remote push or
remote merge. Formal issuance is a logical commit on the isolated admission
branch, and its reviewed SHA can start public source/synthetic preparation.
Do not merge admission to main before the P04/coordinator repair and relevant
current-head gates and independent review. Source admission does not mean full
main gate acceptance. Run local-staged after staging the reviewed candidate;
a later remote PR lane requires owning-Spec scope, current-head CI and
independent review. Do not create or push a PR at admission.

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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Public classification | 6 | W9 | Current root consumer/demand classification | Reviewed issuance commit pending | NOT_RUN | W9 public preparation contract above | pending |
| Inventory subset blocker | 6 | W9 | Coordinator-reported pure validate_service_inventory subset | Admission main 4c83f14b11a77e13e582eb85d0bf256685472a95 | FAIL | 14 overlay binding/membership findings; wrapper exit0 is not semantic PASS | pending |
| Official operations blocker | 6 | W9 | check-operations-catalog.py | Admission main 4c83f14b11a77e13e582eb85d0bf256685472a95 | FAIL | .agent-work/p07-baseline-operations-catalog.json and .log; exit1, 22 findings, 16.593s; SOURCE/STATIC only | pending |
| Public assessment source | 7 | W10 | RED/GREEN and bounded refusal fixtures | New source files not created | NOT_RUN | Dedicated source/test ownership above | pending |
| Service observations | 6, 7, 8 | W11 | Sanitized read-only numeric/runtime facts | Exact service window not bound | NOT_RUN | Native prerequisite contract above | pending |
| Measured resources | 7 | W12 | Representative application/GPU workload comparison | Workload and measurement values unknown | NOT_RUN | Initial budgets are not optimal measurements | pending |
| Least privilege | 8 | W13 | UID/capability/rootfs/secret/socket functional and negative checks | Exact service/image/restore pending | NOT_RUN | No permission/runtime action at admission | pending |
| Existing control reuse | 8 | W13 | Existing ComposeControlsTests | Admission main 4c83f14b11a77e13e582eb85d0bf256685472a95 | PASS | .agent-work/p07-existing-controls-tests.log; 11 tests, 0.042s, exit0; UNIT only, native acceptance open | pending |
| Common integration | 9 | W14 | Effective root model and exact exceptions | Owner proposals not applied | NOT_RUN | Coordinator single-writer boundary | pending |
| Scoped rollout and recovery | 3, 10 | W15 | Changed-service functionality, backup and empty restore | Exact target/image/workload/recovery pending | NOT_RUN | No HOME, migration, rotation or recovery execution | pending |
| Projection and delivery | 9, 10 | W16 | Current-head gates, local-staged and independent review | Issuance and source integration pending | NOT_RUN | Local-main delivery; no dev/PR/push at admission | pending |

## Review and Completion

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
- [Exceptions policy](../../../05.operations/policies/0001-common-optimizations-template-exceptions.md)
