---
title: "P14 Docker Task"
version: "0.1.3"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0112"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-24"
---

# P14 Docker Task

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

Own criterion168/W184 in the [Spec](../spec.md) and [Plan](../plan.md).
Apply the D14 delta to the HOME Compose selection and start path without
rebuilding the selector, the shared admission or the whole-stack refusal.

##### Inputs and Authority

The direct P14-DOCKER1.2.0 request authorizes this workspace, scoped
implementation, read-only observation of the real HOME model and normal
commit, push, PR and merge. Inputs are the matching package README/P14,
D14, D21, the Docker profile and findings D23-03. On 2026-11-24 the owner
chose the Compose label over a separate registry or keeping
`restart: "no"` as the role, knowing that the next HOME `up` recreates the
labelled job containers and reruns their initialization. Start was clean
`main` de588ad0 on branch `codex/p14-docker-1-2-0` in the linked worktree
`.worktrees/p14`; brief p14-docker bound this scope before the first edit
and was rebound to add the selector and controls tests. This Task's
forecast was recorded before the start (revision 1, P30 40, P50 60, P80 100
elapsed minutes). Direct user authorization is authority; this record is
not.

#### Execution Log

##### Work Performed

Retained without rework: the HOME selector's `depends_on` closure and its
refusal of an empty, every-profile or whole-stack start; the operating
start's admission of its targets against the 89-service product inventory,
which also refuses a union of active runs that covers every service; the
`block-whole-stack-compose-start` hook; and the LAB role contract from P07.
Discovery found the remaining P07 meaning gap in HOME: `compose_start`
recorded and released one-shot services by `restart: "no"`, and the
common-controls check exempted a service from a healthcheck by the same
policy, while D21 keeps the restart policy as Docker restart behavior only.
P07 had left this open (TSK-0105) because labelling HOME jobs recreates
their containers; the owner accepted that cost.

`lab.home_roles` reads `hy-home.role` (`job` or `service`, default
`service`) and reports any other value. `lab.py select` lists the closure's
`jobs`, which must exit 0, apart from the services, which must run and pass
any declared healthcheck. `compose_start` records and releases one-shot
services by that role and refuses an invalid one. `compose_controls.is_job`
reads the same label for root and LAB scopes. `template-job-low` and
`template-job-med` carry the label, so all 18 HOME jobs that extend them and
every LAB job inherit it, and `k6` declares it directly. POL-0001 2.1.0
(R20, R21), SPEC-0218 and GDE-0099 state the role contract.

###### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0112 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0112 | ready | in-progress | #work-performed |
| SPEC-0212-TSK-0112 | in-progress | completed | #criterion-decisions |

##### Blockers and Decisions

No Q01-Q04 question is reopened. The label change recreates the 19 HOME job
containers at the next owner `up` of their services, rerunning
initialization jobs such as `mng-pg-init` and `kafka-init`; no service was
started here. Backup and restore owners are unchanged: criterion148 stays
failing in TSK-0092 (the R2 copy is at its cap after a lock-refused remote
prune) and criterion138's locked R2 memory copies stay with TSK-0082 until
2026-12-10. Q01 is not read as permission to delete locked backups or
another host's data.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 168 | W184 | method=review; tool=-; command=- | P14 1.2.0 package, D14, D21, findings D23-03; current lab, compose_start, environment_admission, compose_controls and the rendered HOME model | PASS | Gap listed in Work Performed; selector, admission union and whole-stack refusal retained | required | - |
| E02 | 168 | W184 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.ops.test_compose_start tests.validation.test_lab_controller | Role regressions on de588ad0 | FAIL | Witnessed RED: an unlabelled `restart: "no"` service recorded as one-shot (['app', 'job']); `home_roles` and the selection `jobs` absent | required | - |
| E03 | 168 | W184 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.ops.test_compose_start tests.validation.test_lab_controller | Change | PASS | Exit0; 165 tests | required | E02 |
| E04 | 168 | W184 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_infra_tier_layout | Real root role test before the labels | FAIL | Witnessed RED: awaited jobs such as airflow-init, mng-pg-init and mlflow-db-provision declared no role | required | - |
| E05 | 168 | W184 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_infra_tier_layout | Labels on the job templates and k6 | PASS | Exit0; 12 tests; the rendered root has exactly the 19 jobs, each `restart: "no"`, and every awaited dependency is one | required | E04 |
| E06 | 168 | W184 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_p09_compose_controls | Controls role regression on de588ad0 | FAIL | Witnessed RED: an unlabelled `restart: "no"` service counted as a job | required | - |
| E07 | 168 | W184 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_p09_compose_controls | Change | PASS | Exit0; 19 tests | required | E06 |
| E08 | 168 | W184 | method=automated; tool=Python3.12.3; command=python3 scripts/validation/compose_controls.py | Change, every root and LAB scope | PASS | 18 scopes, 326 services, 0 findings | required | - |
| E09 | 168 | W184 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_lab_layout tests.validation.test_lab_isolation tests.validation.test_compose_baseline_gates tests.validation.test_infra_tier_layout tests.lib.ops.test_compose_start tests.validation.test_lab_controller | Change before the controls edit | PASS | Exit0; 337 tests, 29 opt-in skipped (NOT_RUN) | required | - |
| E10 | 168 | W184 | method=observation; tool=Docker Compose 5.6.1; command=lab.py select airflow-scheduler | Real HOME model and containers, read-only | PASS | Closure airflow-init and airflow-scheduler; jobs [airflow-init]; 58 of 89 services running after the start; no problem; nothing started | required | - |
| E11 | 168 | W184 | method=automated; tool=Python3.12.3; command=check-document-metadata.py --mode check-changed --base-ref origin/main; check-operations-catalog.py | Change | PASS | 0 violations; catalog PASS | required | - |
| E12 | 168 | W184 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest on the 13 other suites that read the templates or compose_controls | Change | NOT_RUN | 526 tests passed, 1 opt-in skipped; tests.lib.ops.test_root_resource_assessment could not import locally (no `referencing` package in this Python), left to hosted CI | required | - |
| E13 | 168 | W184 | method=automated; tool=GitHub Actions candidate-core, Python3.14.8; command=changed candidate validation | PR 1164 first push | FAIL | Two real failures: a compose-controls fixture still treated `restart: "no"` alone as a job, and the SEC01 ledger and release lookups held the old k6 Compose hash | required | - |
| E14 | 168 | W184 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_compose_baseline_gates tests.lib.supply_chain.test_update_gates | Fixture labelled; `ledger_rebind --write` re-bound the k6 row and include input (hash only); the k6 reviewed-subject hash in the ledger and release lookups follows the file, as in a0ec32eb1 | PASS | Exit0; baseline suite with an unlabelled restart-no case now reported, 43 supply-chain tests | required | - |
| E15 | 168 | W184 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest on the 13 other suites that read the templates or compose_controls | `main` 1b7e76aa with the repository `.venv` first on `PATH` (it carries `referencing`), 2026-11-24 (P16) | PASS | Exit0; 555 tests, 1 opt-in skipped (NOT_RUN); tests.lib.ops.test_root_resource_assessment imported and passed | required | E12 |
| E16 | 168 | W184 | method=automated; tool=GitHub Actions candidate-core, Python3.14.8; command=changed candidate validation | PR 1164 head a2d65816 after E14 | PASS | Every check passed and the PR merged clean as c001d125 | required | E13 |

##### Resolution Links

E03 resolves E02, E05 resolves E04 and E07 resolves E06. E15 resolves E12 and E16 resolves E13. E14 fixes the
hosted failures of E13; hosted CI on the fixed head is the gate.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 168 | accepted | E01,E03,E05,E07,E08,E09,E10,E11 | Owner @buenhyden accepted on 2026-11-24 in this chat during P16 (TSK-0114). The recreated HOME job containers are observed at the owner's next `up`. | @buenhyden |

##### Remaining Conditions

No HOME start was run, so the recreated job containers and their exit codes
under the new label are first observed at the owner's next `up` of their
services. Criterion148 (TSK-0092) and criterion138 (TSK-0082) keep their own
owners and open conditions.

#### Handoff

##### Promotion Receipt

`lab.py`, `compose_start.py` and `compose_controls.py` own the behavior;
`infra/common-optimizations.yml` and the k6 leaf own the labels; POL-0001,
SPEC-0218 and GDE-0099 own the rule. This Task owns execution evidence only.

##### Next Owner

The owner decides criterion168 in P16. The next input for this workspace is
P15-CLEANUP; it is not executed automatically. Keep the package through P17.

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
