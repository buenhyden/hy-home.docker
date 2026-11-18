---
title: "W10 Parallel Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0090"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-18"
---

# W10 Parallel Task

## Scope

### Objective and Parent

Own criterion 146 and work unit W162 under the [Spec](../spec.md) and
[Plan](../plan.md). Bring parallel work to the 4.2.0 W10-PARALLEL design
with D10: dependent work units dispatched to real workers, with resource
ownership, fencing, cancellation and checked integration.

### Inputs and Authority

The direct 2026-11-18 request runs W10-PARALLEL from the git-ignored 4.2.0
package. Asked which worker runs the acceptance test, the owner chose shell
workers only, so no Claude or Codex worker is started and the provider
worker run stays NOT_RUN. W09-ENV supplies the whole-stack Compose ban and
W07-BRIEF the brief revision passed to each worker. W10-FORECAST owns the
rule against summing per-task P80 values.

## Execution Log

### Work Performed

#### Gap analysis

Before this Task the repository had delegation envelope rules
(AGENTIC-R65 and R67) and a fenced lease for session analysis, but no
dispatcher: nothing started workers from a dependency graph, locked
resources, refused late or out-of-scope results, cancelled workers or
reran checks after integration.

#### W162 design

`scripts/operations/work_dispatch.py` reads a plan whose units name a
command, dependencies, owned paths, shared resources and a timeout, and
refuses a cycle, an unknown dependency, a duplicate id or a path outside
the repository. A unit starts when its dependencies succeeded, the worker
ceiling (the plan's value, at most the CPU count) allows, and it acquires,
in one SQLite transaction, a lease on every owned path and shared resource;
path leases conflict by prefix. Each lease gets the next generation for its
resource. The worker runs in its own detached worktree at the base commit
with its ancestors' patches applied, in a new process group, and receives
`HY_TASK`, `HY_BRIEF_REVISION`, `HY_WORK_UNIT` and `HY_FENCE`. When it ends
the dispatcher refuses a change outside the owned paths and a result whose
leases are no longer held at the same generation, saves the patch, releases
the leases and removes the worktree. A failure, timeout or refusal blocks
only downstream units. `cancel`, or SIGINT or SIGTERM to the dispatcher,
kills each running process group and blocks pending units. After a full
success the integrator applies every patch on the base in a fresh worktree
and reruns the integration checks; the combined patch stays in the run
folder for a person or integrator to apply. `cleanup` stops workers and
removes worktrees left by a dispatcher that died. A worktree separates
files only; ports, volumes and processes are guarded by declared shared
resources, not confined. ENVIRONMENT-CONSTRAINTS-R156 to R160 and RUN-0021
state the behavior.

#### Real runs

The same plan ran on this repository at `7807dcf62` with two workers and
then one: `forecast-tests` and `registry-conflict` each ran the forecast
tests and shared `registry:writer`, and `manifest-check` ran the script
manifest check. With two workers the shared-resource unit started at 1.88 s,
after the first ended at 1.28 s, at generation 2 against 1; the run took
36.7 s and the integration checks passed. With one worker it took 40.9 s,
so the parallel run was 4.2 s, about 10%, faster in one sample of each,
setup and integration included; the manifest check, about 34 to 36 s,
bounds both runs. A third run received SIGTERM after 4 s: the running
manifest check was cancelled, integration did not run, and no worktree or
check process remained.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0090 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0090 | ready | in-progress | #w162-design |

### Blockers and Decisions

No Claude or Codex worker was run, by the owner's choice. Docker and
Kubernetes resources are only lock names here; no worker started a service.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dispatch RED | 146 | W162 | `test_work_dispatch` | New tests before the module | FAIL | Import error: no dispatch module | required | - |
| Dispatch GREEN | 146 | W162 | `test_work_dispatch` | Dispatch module | PASS | 14 tests: concurrency, brief and fence handoff, shared and overlapping locks, ownership, downstream blocking, timeout, cancel, takeover fencing, generations, integration failure, upstream patch, dispatcher death cleanup, bad plans | required | Dispatch RED |
| Real parallel run | 146 | W162 | `work_dispatch.py run` | Three-unit plan on `7807dcf62`, two workers and one | PASS | 36.7 s against 40.9 s, N 1 each; shared resource serialised; integration passed both times | required | - |
| Real cancel | 146 | W162 | `work_dispatch.py run` and SIGTERM | Same plan, two workers | PASS | Status cancelled, integration not run, one worktree and no check process left | required | - |
| Provider worker run | 146 | W162 | Claude or Codex worker | none | NOT_RUN | The owner chose shell workers only | optional | - |

### Resolution Links

Dispatch GREEN resolves Dispatch RED.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 146 | pending | Dispatch GREEN, Real parallel run, Real cancel | Awaits the owner's decision | @buenhyden |

### Remaining Conditions

A provider worker run and a larger sample of parallel gains remain open.

## Handoff

### Promotion Receipt

`work_dispatch.py`, ENVIRONMENT-CONSTRAINTS-R156 to R160 and RUN-0021 hold
the W162 behavior.

### Next Owner

The owner decides criterion 146.
