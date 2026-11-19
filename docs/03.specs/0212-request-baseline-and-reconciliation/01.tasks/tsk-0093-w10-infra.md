---
title: "W10 Infrastructure Task"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-19"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0093"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-19"
---

# W10 Infrastructure Task

## Scope

### Objective and Parent

Own criterion 149 and work unit W165 under the [Spec](../spec.md) and
[Plan](../plan.md). Bring the Docker workspace to the 4.2.0 W10-INFRA
design with D20 and D11: a HOME start is checked against its dependency
closure and the services already running, and static, LAB and operating
results are reported apart. D19 (Kubernetes) does not apply here: this
workspace owns Compose services, and the cluster's desired state belongs
to the separate Kubernetes repository.

### Inputs and Authority

The direct 2026-11-19 request runs W10-INFRA from the git-ignored 4.2.0
package. On 2026-11-19 the owner chose no live LAB acceptance run and no
sandbox claim for LABs that run on the operating Docker daemon. W09-ENV
(TSK-0087) supplies R149, R150 and the whole-stack hook rule; SPEC-0215 and
SPEC-0263 supply `lab.py` and its LAB lease, collision and budget checks.

## Execution Log

### Work Performed

#### Survey on 2026-11-19

The root project `hy-home-infra` renders 89 services, every one behind a
profile, and 57 of them run; no other Compose project runs. Compose selects
0 services without a profile flag. A scratch project proved Compose reads
`COMPOSE_PROFILES` from `.env` (0 services without the key, 1 with it), so
the operating `.env` preselects no profile; this answers the TSK-0087 open
question without reading the file. The 15 LABs under `labs/` run as their
own projects through `lab.py`, which checks port, path and network
collisions with HOME and running LABs, the declared reservation budget and
a limit of one running LAB; `lab.py check jupyterlab couchdb` refused with
"2 LABs would run; limit is 1". Seven LABs ran one at a time under leases on
2026-11-05 and 06 and are recorded stopped. LABs share the operating daemon,
so a LAB result is an operating-host result, never a sandbox one.

The kubeconfig on this host has no context and no current context. The one
cluster script, `infra/03-security/openbao/scripts/k8s-writers.sh`, pins
`--context k3d-hyhome`, reads no Secret data and runs only in the RUN-0105
window for the external cluster operator, so nothing here reaches a cluster
by default.

#### Gap and design

R149 named no check: nothing computed what a named start pulls in through
`depends_on` or whether the result, with the services already running,
would leave every HOME service up. `lab.py select [SERVICE...] [--profile
P]` now renders every profile once, expands named services through
`depends_on` (or, for profiles alone, their members and every profile-less
service), joins the running containers of the HOME project only, and
prints the closure, the services it adds, those already running and the
union against the total. It refuses with exit 3 an empty selection, an
unknown service or profile, `*` and a start that would leave every HOME
service running. It reads only and starts nothing. Alternatives not taken:
a new script (the render and container survey already live in `lab.py`)
and a dry-run `up` (it stops at the first image not present locally).

#### Review

`lab.py` is operations code, so R123 asks for one fresh-context primary
review; on 2026-11-19 the owner asked for one `code-reviewer` agent. It was
dispatched at 2026-11-18T23:23:58Z with the diff, tests, rules and recorded
checks, read files only (it had no shell), and returned after 62 s with 11
tool calls: approve with follow-up, no critical or important finding. It
confirmed the closure, the profile semantics, the error exits and that
nothing starts or changes a container, and found three minor items: a
running container of a service no longer declared raised the union above
the total, tests did not cover running services, services with profiles,
a mixed unknown name or a cycle, and the help text did not say the closure
is an upper bound. The union now counts declared services only, the tests
cover each input, and the help text says so; the follow-up closed with an
author check. Its suggestion that a shell `COMPOSE_PROFILES` is not
modelled stays recorded: the operating `.env` sets none (Profile control).
Queue wait and context loading were not observed.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0093 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0093 | ready | in-progress | #gap-and-design |

### Blockers and Decisions

A live LAB run, its own-resource cleanup after an expired lease and a
separate test daemon are not exercised by the owner's choice; they stay
runtime-only. The union check reads the moment it runs; two workers that
start HOME services at once must serialize on a shared resource lease.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Host survey | 149 | W165 | `docker compose config --services`, `docker ps` by project | This server on 2026-11-19 | PASS | 89 services, 57 running, 0 selected without a profile, one project | required | - |
| Profile control | 149 | W165 | `docker compose config --services` in a scratch project | `.env` without and with `COMPOSE_PROFILES` | PASS | 0 and 1 service: Compose applies the key, so the operating `.env` sets none | required | - |
| LAB concurrency | 149 | W165 | `lab.py check jupyterlab couchdb` | Owner `labs/.env` | PASS | Refused, exit 3: 2 LABs would run, limit 1 | required | - |
| Kubernetes boundary | 149 | W165 | `kubectl config get-contexts`, source read of `k8s-writers.sh` | This server | PASS | No context; the script pins `k3d-hyhome` and runs only in the owner window | required | - |
| Select RED | 149 | W165 | `test_lab_controller.HomeSelectionTests` | New tests before the command | FAIL | 7 errors: no `home_selection` | required | - |
| Select GREEN | 149 | W165 | `test_lab_controller.HomeSelectionTests` | `lab.py select` | PASS | 107 lab controller tests | required | Select RED |
| Real select | 149 | W165 | `lab.py select` | `pact-broker`, `--profile '*'`, no argument | PASS | 4-service closure, 1 running, union 60 of 89; the other two refused with exit 3 | required | - |
| Closure oracle | 149 | W165 | `home_selection` against `docker compose --profile '*' config SERVICE` | All 89 HOME services, one render, `1cd0bf484` | PASS | 89 of 89 closures equal Compose's own; 212.9 s | required | - |
| Select review | 149 | W165 | Fresh-context `code-reviewer` review | `1cd0bf484` | PASS | Approve with follow-up: three minor items, all fixed; 62 s, 1 round | required | - |
| Follow-up RED | 149 | W165 | `test_lab_controller.HomeSelectionTests` | New follow-up test on `1cd0bf484` | FAIL | 1 failure: an undeclared running service counted in the union | required | - |
| Follow-up GREEN | 149 | W165 | `test_lab_controller.HomeSelectionTests` | Union over declared services | PASS | 108 lab controller tests | required | Follow-up RED |
| Live LAB run | 149 | W165 | `lab.py up`, lease expiry, `lab.py reap` | One LAB | NOT_RUN | The owner chose no live run on 2026-11-19 | optional | - |

### Resolution Links

Select GREEN resolves Select RED, and Follow-up GREEN resolves Follow-up RED.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 149 | accepted | Host survey, Profile control, LAB concurrency, Kubernetes boundary, Select GREEN, Real select, Closure oracle, Select review, Follow-up GREEN | Owner @buenhyden accepted on 2026-11-19 in this chat (W11-ACCEPT) | @buenhyden |

### Remaining Conditions

The owner accepted criterion 149 on 2026-11-19.

The live LAB run stays runtime-only by the owner's choice.

## Handoff

### Promotion Receipt

`lab.py select`, ENVIRONMENT-CONSTRAINTS-R149 and R163 hold the W165 rules.

### Next Owner

The owner decides criterion 149.
