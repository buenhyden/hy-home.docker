---
title: "Hermes DevOps Daily Brief Recovery Task"
version: "0.1.0"
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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DevOps brief failure observation | 107 | W112 | Prometheus Hermes metrics, scheduler and agent logs | HOME, 2026-11-11 08:31 KST | FAIL | No `devops` outcome on 2026-11-11; last success 2026-11-08; both alerts still firing. | required | - |
| DevOps brief scheduled success | 107 | W112 | One scheduled `devops` run submitted and both alerts resolved | Next scheduled run after the fix | NOT_RUN | Waits for the diagnosis. | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 107 | pending | DevOps brief failure observation, DevOps brief scheduled success | Diagnosis not started. | SPEC-0212 TSK-0054 |

## Review and Completion

Completion needs one scheduled `devops` run that submits a final report and
both alerts resolving for it, or the external cause recorded as a residual
with the owner's decision.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Hermes provenance Task](tsk-0050-hermes-provenance-trust-export.md)
- [Exporter observability Task](tsk-0046-exporter-observability.md)
