---
title: "Hermes DevOps Daily Brief Recovery Task"
version: "0.2.1"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0054"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-11"
---

# Hermes DevOps Daily Brief Recovery Task

## Overview

### Objective

Restore the scheduled Hermes `devops` daily brief. Its last successful
submission was on 2026-11-08, so `HermesResearchNoSuccess` and
`HermesResearchBlocked` have fired since then while the `news` and
`business_ideas` topics keep submitting. The Task finds the cause, fixes what
belongs to this repository, and records any external cause as a residual.

## Inputs and Authorization

On 2026-11-11 the owner (@buenhyden) asked for this failure to run as its own
Task. That covers read-only diagnosis and a repository-side fix. Hermes agent
configuration under `~/.hermes`, a model or provider change, and any paid
model use stay owner decisions, under the
[approval boundaries](../../../../.agents/governance/approval-boundaries.md).

## Work Log

### Observed failures

| Date | Outcome | Observation |
| --- | --- | --- |
| 2026-11-08 | submitted | Last successful submission. |
| 2026-11-09 | blocked | `blocked_total` rose for `report_not_final` and `report_path_not_allowed`. |
| 2026-11-10 | gateway_error | The submission reached the Gateway and failed. |
| 2026-11-11 | no outcome | Cron job `devops-daily-brief` started at 08:00:33 KST on `claude-haiku-5-5`, while the other jobs ran on `gpt-6.1-terra`. After two API calls the turn ended with `reason=pending_tool_result`, and the scheduler logged "No reply: the turn stopped while a tool result was still pending". No outcome metric was written. |

The same morning `news` and `business_ideas` each logged one `gateway_error`
and one `source_quality` refusal, then submitted. Those topics are healthy and
are context only.

### Open questions

| Item | Question |
| --- | --- |
| H1 | Why does the `devops` job run on a different model from the other jobs, and is that intended? |
| H2 | Which tool result was pending when the turn ended, and does the same job stop the same way on a rerun? |
| H3 | Are `report_not_final` and `report_path_not_allowed` (2026-11-09) from the job's prompt or report path, or from the Gateway's validation? |
| H4 | What did the Gateway reject on 2026-11-10? |

### Diagnosis (2026-11-11)

Read-only sources: `~/.hermes/cron/jobs.json`, `~/.hermes/logs/agent.log*`,
the plugin outbox under `~/.hermes/data/research-report-outbox/`, and the
Prometheus `hermes_research_*` series.

| Item | Finding |
| --- | --- |
| H1 | The `devops` job pins no model, like the other jobs. At 08:00:48 the default `gpt-6.1-terra` (`openai-codex`) answered this job's first request with `HTTP 400 {"detail":"Bad Request"}`, which is not retried. The fallback chain then failed in turn: `openai-api` `gpt-5.6-sol` had no credits, the free Nous Beam model returned 404 (free period ended), and `ollama-cloud` refused for billing. Only `anthropic` `claude-haiku-5-5` accepted. The model difference is the fallback, not a job setting. Why the primary rejected this job's request is not visible in the log. |
| H2 | The turn ended with `pending_tool_result` two API calls after the switch to `claude-haiku-5-5`, so no report was written. The 09:13 manual rerun finished, but its `submit_research_report` returned `scheduled_instant_required`: manual runs cannot submit by design, so it cannot clear either alert. |
| H3 | `report_not_final` (2026-11-08) and `report_path_not_allowed` (2026-11-09 08:05:20) are the plugin's own report checks refusing the agent's report file. They work as designed; the agent retried in the same run. |
| H4 | The Gateway did not reject anything. On 2026-11-09 08:05:41 and 2026-11-10 08:08:23 and 08:15:45 the plugin's POST hit its 15 s per-attempt limit and returned `delivery_uncertain` (`timeout`); the outbox records stay `uncertain` and are never retried. The workload README nests the limits as Gateway 20 s < flow `executionTimeout` 30 s < submitter attempt 45 s, and the Publisher uses 45 s, but the direct plugin path still used 15 s. A Gateway answer that takes 15–30 s, which is plausible during the 08:00 burst of jobs, is therefore lost. The flow saves no execution data, so whether those two reports were stored is not recorded. |

### Repository fix

The direct plugin path now uses 45 s per attempt (`_HTTP_TIMEOUT` and
`MAX_REQUEST_TIMEOUT`), the same as the Publisher, inside the existing 60 s
total and three attempts. A new test keeps the attempt longer than the flow's
`executionTimeout`. The installed copy under `~/.hermes/plugins/research-report`
is owner-managed and needs the two changed files and a gateway restart.

### Host session kills during verification (2026-11-11)

While verifying the timeout change, three local runs of the transport tests
(12:28:52, 12:33:50 and 12:59:10 KST) each killed every UID 1000 process on
the HOME host: the systemd user manager, SSH sessions, the agent session, the
Hermes gateway and containers that run as UID 1000. Raising the limit to 45 s
made the test's over-limit case of 16 s valid, so a mocked `Popen` was called
and returned a `MagicMock` whose `pid` converts to 1. The cleanup then ran
`os.killpg(1, SIGKILL)`, which is `kill(-1, SIGKILL)`. The test case moved to
46 s before #943 merged, and `_kill_owned_process` now signals only a real
child group (`int` pid above 1), with a test that a mock, 0, 1 or -1 is
never signalled. The 12:35:57 suspend was a separate `sudo systemctl suspend`
sent over SSH from the owner's client, not from this work.

### Residual for the owner

The 2026-11-11 failure is a model-provider failure, not a repository defect:
the primary model's HTTP 400 for this job and a fallback chain where only one
entry still works. Choosing the fallback chain or pinning a model for the job
is the owner's decision under `~/.hermes`; no paid model is assumed.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DevOps brief failure observation | 107 | W112 | Prometheus Hermes metrics, scheduler and agent logs | HOME, 2026-11-11 08:31 KST | FAIL | No `devops` outcome on 2026-11-11; last success 2026-11-08; both alerts still firing. | required | - |
| DevOps brief diagnosis | 107 | W112 | Read-only Hermes cron, agent log, outbox and Prometheus readback | HOME, 2026-11-11 12:40 KST | PASS | H1–H4 answered in Diagnosis (2026-11-11). | optional | - |
| DevOps brief scheduled success | 107 | W112 | One scheduled `devops` run submitted and both alerts resolved | Next scheduled run after the fix | NOT_RUN | Waits for the diagnosis. | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 107 | pending | DevOps brief failure observation, DevOps brief diagnosis, DevOps brief scheduled success | Diagnosis done; the timeout fix waits for the owner's plugin install and the next scheduled run. | SPEC-0212 TSK-0054 |

## Review and Completion

Completion needs one scheduled `devops` run that submits a final report and
both alerts resolving for it, or the external cause recorded as a residual
with the owner's decision.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Hermes provenance Task](tsk-0050-hermes-provenance-trust-export.md)
- [Exporter observability Task](tsk-0046-exporter-observability.md)
