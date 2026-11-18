---
title: "W08 Shared Memory Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0082"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-18"
---

# W08 Shared Memory Task

## Scope

### Objective and Parent

Own criterion 138 and work units W148 to W151 under the [Spec](../spec.md)
and [Plan](../plan.md). Bring the shared agent memory to the 4.2.0
W08-MEMORY design: restore capacity admission for the daily memory
snapshots that D-11 in [TSK-0067](tsk-0067-w00-delta-gap-closure.md#new-items)
assigned here, and add the D06 record semantics the store lacks.

### Inputs and Authority

The direct 2026-11-18 request runs W08-MEMORY from the git-ignored 4.2.0
package, with designs D06 and D16. On 2026-11-18 the owner chose to charge
each snapshot its actual memory export size, and to implement the full D06
record semantics with an explicit migration. Live backup runs, a reconcile
of the real ledger and changes to the real store each need their own
approval of that exact target.

## Execution Log

### Work Performed

#### Gap analysis

`scripts/operations/agent_memory.py` (SPEC-0236) already keeps one store per
clone at the Git common directory, refuses another repository's CLI, writes
immutable revisions under a compare-and-swap expected revision, records
conflicts, binds a request key to a digest of the whole request, separates
busy, full and capacity errors, and pins sources with a reuse state. It
holds no Task approval or status. It uses a rollback journal because the
linked SQLite is 3.45.1 in both the system and controller Python, which has
neither the WAL-reset fix of 3.51.3 nor a listed backport; Node links 3.53.4
but does not write the store.

D06 items it lacks: a baseline identity with default exclusion of other
baselines, a record kind separate from the time tier, validity times,
supersession and invalidation links, and selective export and erase. The
`usage` command reports the read-only connection's default page limit
instead of the enforced write limit.

D-11 is an accepted requirement left unmet. The capacity ledger charged
every snapshot and local copy 64 MiB against the 1 GiB allocation. A
read-only `usage` on 2026-11-18 showed 60 external snapshots charged
4,026,531,840 bytes, generation 1 and zero available bytes, so each daily
memory export was refused with exit 4 and dropped with a warning since
2026-11-11, and memory was missing from the daily snapshots.

#### W148 design

The backup inventory already reads the memory export size of each snapshot
from `restic ls --json` and bounds it to 64 MiB. Pass that size into the
inventory and charge it: an external allocation now requires
`memory_bytes` from 1 byte to 64 MiB and charges exactly that. Reservations
keep 64 MiB per new snapshot, local copies keep their 64 MiB charge, and
compression or deduplication still earns no credit. Settlement may never
lower an existing charge; only a reconciliation from a complete inventory
recalculates charges, and it replaces every allocation, so earlier 64 MiB
rows convert on the next reconcile without a separate migration. The daily
orchestrator reconciles before admitting the export, and any refused or
failed export now fails the run. Reverting the change restores the fixed
charge and the warning path.

ENVIRONMENT-CONSTRAINTS-R98, its prose, RUN-0021 and the Restic README
state the new charge. The daily `backup.sh backup` and `offsite.sh copy`
still create snapshots without admission; W149 owns that part.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0082 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0082 | ready | in-progress | #w148-design |

### Blockers and Decisions

No live Docker, Restic or ledger operation ran. The real ledger converts on
the first reconcile after delivery, which a daily run or an approved manual
`capacity reconcile` performs. W148 is high risk; on 2026-11-18 the owner
chose to deliver it without the Q08 independent review, on the local tests
and the hosted candidate checks.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Memory baseline | 138 | W148 | memory unittest suites | Capacity, backup, local copy, store, CLI capacity and backup contract modules at `320b17bdd` | PASS | 106 tests, 11 s | required | - |
| Real ledger observation | 138 | W148 | read-only `agent_memory.py usage` | Real store and ledger on 2026-11-18 | PASS | 60 external snapshots at 64 MiB each, 0 bytes available | optional | - |
| Size charge RED | 138 | W148 | capacity and backup charging tests | New size, settlement and inventory cases on the earlier code | FAIL | Six errors and two failures: `memory_bytes` refused, 64 MiB charged, no lower-charge guard | required | - |
| Size charge GREEN | 138 | W148 | capacity and backup charging tests | Size-charged allocations and the settlement guard | PASS | 55 tests; 40 snapshots of 50,000 bytes leave room for a new reservation | required | Size charge RED |
| Daily export RED | 138 | W148 | orchestrator memory step contract | Reconcile, capacity and reconcile-failure cases on the earlier orchestrator | FAIL | Three cases failed: no reconcile, capacity refusal passed | required | - |
| Daily export GREEN | 138 | W148 | orchestrator memory step contract | Reconcile before export; refusal fails the run | PASS | Backup contract tests passed; shellcheck clean | required | Daily export RED |
| Memory regression | 138 | W148 | memory, offsite and backup contract suites | Changed capacity, backup and orchestrator sources | PASS | 119 tests, seven opt-in Docker rehearsals skipped | required | - |

### Resolution Links

Size charge GREEN resolves Size charge RED and Daily export GREEN resolves
Daily export RED.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 138 | pending | Size charge GREEN, Daily export GREEN, Memory regression | Awaits W149 to W151 and the owner's decision | @buenhyden |

### Remaining Conditions

W149 routes the daily snapshots through admission, W150 adds the D06 record
semantics, and W151 needs a native Claude and Codex observation. A live
daily run and the real ledger reconcile remain unobserved.

## Handoff

### Promotion Receipt

`memory_capacity.py`, `memory_backup.py`, the daily orchestrator,
ENVIRONMENT-CONSTRAINTS-R98 and RUN-0021 hold the W148 behavior.

### Next Owner

The implementer owns W149 to W151. The owner decides criterion 138.
