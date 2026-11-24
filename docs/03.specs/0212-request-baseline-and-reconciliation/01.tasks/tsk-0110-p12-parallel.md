---
title: "P12 Parallel Provider Task"
version: "0.1.2"
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
installed, so that needs an owner decision. A second review noted that byte
matching alone can be evaded and that a path rule is weaker than keeping the
file out of reach. Restricted mode is the primary confinement: a decoy run
showed it refuses a file outside the working directory and a symlink inside
it that points out (E10). The rules now also deny `/tmp`, `/proc` and `/run`,
a provider patch with binary content or a link is rejected, and the scan
covers base64, hex, URL- and JSON-escaped forms. The credential stays
readable by the CLI process inside the sandbox; a brokered short-lived token
would remove it and needs a token the owner issues. A first real run from the worktree code was
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
| E10 | 166 | W182 | method=observation; tool=Claude Code 2.1.331; command=claude --print --safe-mode --restricted with Read, Glob and Grep, asked to read a decoy outside the working directory, then a symlink to it inside | A synthetic decoy file in the session scratchpad, 2026-11-24; deleted afterwards | PASS | Both refused: the file tools are restricted to the working directory and the link points outside it; the decoy value never appeared; cost 0.0015 USD | required | - |
| E11 | 166 | W182 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.ops.test_dispatch_providers tests.validation.test_work_dispatch tests.lib.ops.test_dispatch_process tests.lib.test_surface_ownership | Encoded-scan and binary-or-link rejection added | PASS | Exit0; 80 tests, one opt-in skipped (NOT_RUN); these two cases were written after their code and carry no witnessed RED | required | - |
| E12 | 166 | W182 | method=observation; tool=Python3.12.3 CLI; command=work_dispatch.py run PLAN with two Claude units | Merged dispatcher 6c105ce5 from the primary checkout, brief revision 3 granting dispatch only, run 20261124T095324-6f261e | FAIL | The brief check refused both units before any spawn: "This action exceeds the bound request brief scope", since `check ... dispatch` needs both the edit and dispatch actions per path; no worker, cost or lease | required | - |
| E13 | 166 | W182 | method=observation; tool=Python3.12.3 CLI; command=work_dispatch.py run PLAN with two Claude units | Brief revision 4 with edit and dispatch, default 1-CPU budgets, run 20261124T095349-af1abe | FAIL | Unit a ran in the sandbox and succeeded (session 7f65135c, 0.0045 USD, 3 turns); unit b was refused by aggregate admission, `cpus_budget_exceeded`: the live Docker services already reserve 9.0 of the 10 host CPUs | required | - |
| E14 | 166 | W182 | method=observation; tool=Python3.12.3 CLI; command=work_dispatch.py run PLAN with two Claude units | Brief revision 4, 0.3-CPU budgets, model claude-haiku-5-5, 0.3 USD cap each, run 20261124T095454-d83d81 | PASS | Both succeeded: a active 5.16-22.08 s (session 83aad322, 0.0045 USD), b 9.25-22.72 s (session ff670873, 0.0034 USD), 12.8 s of overlap, elapsed 27.8 s against 30.4 s of unit time; each changed only its owned file with five accurate bullets on its module; integration passed (sha256 cef99563); main checkout clean, no worker scope or live lease left | required | E07,E12,E13 |
| E15 | 166 | W182 | method=observation; tool=Python3.12.3 CLI; command=work_dispatch.py run with one long Claude unit, then work_dispatch.py cancel | Run 20261124T095544-7c297c | PASS | Cancel 4 s after the scope appeared; the unit ended cancelled at 10.9 s, its scope was gone, no provider process remained and its worktree was removed | required | - |
| E16 | 166 | W182 | method=observation; tool=Python3.12.3 CLI; command=task_forecast.py observe SPEC-0212-TSK-0110 --status completed; score --type harness-change --time-basis elapsed | Real store, 2026-11-24T00:15:14Z to 00:56:10Z | PASS | 40.9 elapsed minutes against P30 25, P50 45, P80 90; two completed harness-change tasks, insufficient sample | optional | - |
| E17 | 166 | W182 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.ops.test_dispatch_providers | Leading-dash regressions on 0fb55d55, after an automated review found that a prompt or model starting with a dash could be read as a CLI option | FAIL | Witnessed RED: 3 subtests accepted `--dangerously-skip-permissions`, `-p x` after leading spaces and `--settings` | required | - |
| E18 | 166 | W182 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.ops.test_dispatch_providers | Guard in validate | PASS | Exit0; the three values are refused before any argv is built; the dispatcher suite also passes | required | E17 |

##### Resolution Links

E03 resolves the witnessed failures in E02 and E09 those in E08. E14 resolves E07, E12 and E13. E18 resolves E17. E07 was refused by admission from the
linked worktree.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 166 | pending | E01,E03,E04,E05,E06,E09,E10,E11,E14,E15,E18 | Implementation, focused regressions, a real overlapping two-worker Claude run with integration and a real cancellation are recorded; a Codex worker and owner acceptance in P16 remain | @buenhyden |

##### Remaining Conditions

A Codex worker needs an egress-limited network namespace (slirp4netns or
pasta, not installed: an owner decision) and its account limit lifted after
2026-11-27 12:53; until then the Codex adapter is refused, not complete. A
provider worker needs a CPU budget that fits beside the live services, about
0.3 CPU each on this host.

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
