---
title: "P12 Parallel Provider Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-24"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0110"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-24"
---

# P12 Parallel Provider Task

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Objective and Parent

Own criterion166/W182 in the [Spec](../spec.md) and [Plan](../plan.md).
Apply the D12 delta to the existing Docker work dispatcher without rebuilding
the DAG, leases, admission or sandbox that TSK-0090 and TSK-0105 built.

##### Inputs and Authority

The direct P12-PARALLEL1.2.0 request authorizes this workspace, scoped
implementation, a bounded real provider run within the existing accounts and
normal commit, push, PR and merge. Inputs are the matching package
README/P12, D12, the Docker profile and findings D23-03, D23-10 and D23-14;
no other workspace is required. Start was clean `main` 2a90d2f5 on branch
`codex/p12-parallel-1-2-0` in the linked worktree `.worktrees/p12`. Brief
p12-parallel revision 1 bound this scope, including dispatch to the two
worker output paths, before the first edit. This Task's forecast was recorded
before the start (revision 1, P30 25, P50 45, P80 90 elapsed minutes, one
comparable prior). Direct user authorization is authority; this record is
not.

#### Execution Log

##### Work Performed

Retained without rework: the plan DAG, fenced path and resource leases,
ownership checks, P07 numeric admission with owner intent and process
identity, the systemd scope that owns every worker process with CPU and
memory limits, the bubblewrap boundary with a read-only root and only the
worktree writable, cancellation, timeouts, integration in a temporary
worktree and recovery. Discovery against D12 found that a unit could only be
a shell command: no provider adapter, no brief check before spawn, no way
for a worker to reach its API or credentials inside the sandbox, and no
provider result in the report.

`scripts/lib/ops/dispatch_providers.py` adds the adapters. A unit names
`provider: {name, model, prompt, max_budget_usd}` (USD cap above 0 and at
most 5). Claude runs `--print --output-format json --safe-mode --restricted
--permission-mode acceptEdits` with the Read, Edit, Write, Glob and Grep
tools only, no MCP, no setting sources, no session persistence and
`--max-budget-usd`, and its file tools are denied the private HOME. A Codex
adapter (`exec --json`) exists but is refused at validation, see below. Each profile adds to the existing boundary only the
network, the provider binary, its credential file read-only at a private
HOME, and the DNS and TLS files. `work_dispatch.py` requires the plan's brief
`session` and `request_revision` for a provider unit, runs the brief's
`check ... dispatch` for the unit's owned paths right before spawn and fails
the unit if the brief does not allow it, and records the final JSON session,
cost and error; a provider error fails the unit. ENVIRONMENT-CONSTRAINTS
2.6.0 changes R156 and adds R168, and the harness maintenance guide 2.6.0
documents the plan fields.

##### Blockers and Decisions

No Q01-Q04 question is reopened. An automated security review of the first
push found two real exposures: the worker's Read tool could copy the bound
credential file into an accepted patch, and a Codex worker would get a shell
with the host network and its credentials. Claude's file tools are now
denied the private HOME, a result whose patch or log holds any credential
value is rejected and the log wiped, and Codex is refused until an
egress-limited network namespace exists; neither slirp4netns nor pasta is
installed, so that needs an owner decision. A first real run from the worktree code was
refused by admission ("execution admission must use this repository root"):
the dispatcher only runs against its own checkout, and the brief is bound to
the primary checkout, so the real run uses the merged dispatcher from the
primary checkout. Codex is also limited by its account until 2026-11-27
12:53. The network is open to a provider worker for its API, a
monitored boundary rather than a block. The adapter module's unit tests were
written after the module, so they carry no witnessed RED; the dispatcher
wiring has one.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 166 | W182 | method=review; tool=-; command=- | P12 1.2.0 package, D12, D23-03, D23-10, D23-14; current work_dispatch, dispatch_process, environment_admission and request_brief; installed claude 2.1.331 and codex 0.172.0 help | PASS | Gap listed in Work Performed; DAG, leases, admission, scope and sandbox retained | required | - |
| E02 | 166 | W182 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_work_dispatch | Provider regressions on 2a90d2f5 | FAIL | Witnessed RED: 1 failure and 3 errors over 4 new tests: overlap with session and cost, stale brief, provider error, plan validation | required | - |
| E03 | 166 | W182 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_work_dispatch | Change | PASS | Exit0; 35 tests | required | E02 |
| E04 | 166 | W182 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.test_surface_ownership tests.lib.ops.test_dispatch_providers tests.lib.ops.test_dispatch_process tests.validation.test_work_dispatch | Change | PASS | Exit0; one opt-in native shell boundary test skipped (NOT_RUN); adapter tests cover argv, profile, refusals, result parsing and the sandbox arguments | required | - |
| E05 | 166 | W182 | method=automated; tool=ruff; command=ruff check and ruff format on the changed Python files | Change | PASS | Exit0 | required | - |
| E06 | 166 | W182 | method=automated; tool=Python3.12.3; command=check-agent-governance-contract.py --mode repository --section all; check-script-manifest.py | Change | PASS | Governance failures0; manifest valid with the new library and its tests | required | - |
| E07 | 166 | W182 | method=observation; tool=Python3.12.3 CLI; command=work_dispatch.py run PLAN with two Claude units | Dispatcher code from the linked worktree against the primary checkout, 2026-11-24 | FAIL | Admission refused before any spawn: execution admission must use this repository root; no worker, cost or lease remained | required | - |
| E08 | 166 | W182 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.ops.test_dispatch_providers tests.validation.test_work_dispatch | Security regressions on e30f87ab | FAIL | Witnessed RED: 1 failure and 3 errors: Codex accepted, no HOME deny, no credential scan, a leaking result accepted | required | - |
| E09 | 166 | W182 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.ops.test_dispatch_providers tests.validation.test_work_dispatch | Security fix | PASS | Exit0; with the process and surface-ownership suites 79 tests, one opt-in skipped (NOT_RUN) | required | E08 |

##### Resolution Links

E03 resolves the witnessed failures in E02 and E09 those in E08. E07 is resolved by the real run
from the primary checkout after the merge.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 166 | pending | E01,E03,E04,E05,E06,E09 | Implementation and focused regressions are recorded; the real two-worker run, the Codex run after its limit and owner acceptance in P16 remain | @buenhyden |

##### Remaining Conditions

The real two-worker Claude run from the primary checkout follows the merge
and is recorded here with its overlap, sessions, costs and integration. The
Codex worker needs an egress-limited network namespace, an owner decision,
and runs after 2026-11-27 12:53.

#### Handoff

##### Promotion Receipt

`dispatch_providers.py`, `work_dispatch.py` and `dispatch_process.py` own the
behavior; ENVIRONMENT-CONSTRAINTS R156 and R168 own the rules; the harness
maintenance guide owns the commands. This Task owns execution evidence only.

##### Next Owner

The owner decides criterion166 in P16. The next input for this workspace is
P13-OBSERVABILITY; it is not executed automatically. Keep the package
through P17.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
