---
title: "Host Logrotate Failure Alert Task"
version: "0.1.1"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0023"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-11-28"
---

# Host Logrotate Failure Alert Task

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

Own criterion 24/W84 in the [Spec](../spec.md) and [Plan](../plan.md): a
failure alert for the host audit rotation, the W6 item that
[TSK-0006](tsk-0006-openbao-trust-bootstrap-and-recovery.md) owns and SPEC-0212
TSK-0128 left open (its E09 saw the 2026-11-27 reopening only by hand).

##### Inputs and Authority

On 2026-11-28 the user asked in this chat to review and handle the OpenBao
rotation failure alert. Work ran in the primary checkout on branch
`feat/logrotate-result-alert` from `main` `ae9ab478e`; brief
`logrotate-alert` bound the changed files. TSK-0006's Evidence table is frozen in
the pre-generation-7 form, so this Task and criterion 24 record this part of
W6; criterion 11 keeps the rest. No secret or audit content was read. Direct user authorization is
authority; this record is not.

#### Execution Log

##### Work Performed

###### Changes

| Area | Change |
| --- | --- |
| Gap | `logrotate.service` leaves no result anyone scrapes: node-exporter runs no systemd collector and the textfile directory had no logrotate file. A failed postrotate HUP leaves OpenBao writing to `audit.json.1`, which the next daily rotation compresses (`delaycompress`), so audit lines would be lost unseen |
| Drop-in | `infra/03-security/openbao/config/systemd/logrotate-result.conf`: `ExecStopPost` writes `hyhome_logrotate_last_run_success` (1 when `SERVICE_RESULT=success`) and `hyhome_logrotate_last_run_timestamp_seconds` to `~/backups/metrics/hyhome_logrotate.prom` after every run, atomically. It runs inside the unit's own sandbox, where `ProtectSystem=full` leaves home writable |
| Alerts | `host_logrotate_alerts` in `alert_rules.local.infra.yml`: `HostLogrotateFailed` (success == 0, at once, critical) and `HostLogrotateNotRunning` (no run for 3 h or no metric, 15 m, warning; covers a missing drop-in, a `ConditionACPower` skip and a dead timer) |
| Tests | Drop-in contract test runs the unescaped command for success and exit-code in a temporary directory; `logrotate-alerts.test.yml` promtool cases join the cached-promtool test |
| Docs | RUN-0105 Rotation Failure Alert (install, check, rollback, order against the rule reload); OpenBao README file list |

##### Blockers and Decisions

The owner installed the drop-in and reloaded the Prometheus rules on
2026-11-28; nothing blocks acceptance.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 24 | W84 | method=automated; tool=Python3 venv, cached promtool image; command=python -m unittest tests.validation.test_openbao_window_overrides tests.validation.test_compose_baseline_gates.ContainerThrottleAlertNativeTests | Tests and fixture before the drop-in and rules | FAIL | 1 error (no drop-in), 1 failure (no logrotate alerts) | required | - |
| E02 | 24 | W84 | method=automated; tool=Python3 venv, cached promtool image; command=python -m unittest tests.validation.test_openbao_window_overrides tests.validation.test_compose_baseline_gates.ContainerThrottleAlertNativeTests | With the drop-in and rules | PASS | 14 tests OK; a first fixture sampled every 15 m went stale under the 5 m lookback and was resampled every minute | required | E01 |
| E03 | 24 | W84 | method=observation; tool=systemd user manager; command=temporary user unit files with ExecStart /bin/true and /bin/false plus the drop-in ExecStopPost line, writing to a job scratch directory | HOME, 2026-11-28 | PASS | Result success wrote 1, exit-code wrote 0, no temporary file left; probe units removed. A `systemd-run -p` attempt does not expand `%%` like a unit file and was not used as evidence | required | - |
| E04 | 24 | W84 | method=observation; tool=-; command=owner installs the drop-in, Prometheus reloads the rules, the next hourly run writes hyhome_logrotate.prom with success 1 and both alerts read inactive | HOME | NOT_RUN | Owner sudo install and rule reload pending | required | - |
| E05 | 24 | W84 | method=observation; tool=-; command=owner installs the drop-in, Prometheus reloads the rules, the next hourly run writes hyhome_logrotate.prom with success 1 and both alerts read inactive | HOME, 2026-11-28 after the owner installed the drop-in and reloaded Prometheus (21:02 KST) | PASS | Drop-in root 0644, identical to the source, listed in DropInPaths; the 21:00 run ended success and wrote success 1 with its timestamp (root 0644, no temporary file); Prometheus reads hyhome_logrotate_last_run_success 1, reloadConfigSuccess true, and `host_logrotate_alerts` evaluates HostLogrotateFailed and HostLogrotateNotRunning as inactive with health ok | required | E04 |

##### Resolution Links

E02 resolves E01. E05 resolves E04.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 24 | pending | E01,E02,E03,E04,E05 | Awaiting owner acceptance | @buenhyden |

##### Remaining Conditions

None; owner acceptance only.

#### Handoff

##### Promotion Receipt

The procedure is promoted to RUN-0105 and the file to the OpenBao README.

##### Next Owner

@buenhyden decides acceptance of criterion 24.

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
