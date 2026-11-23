---
title: "P10 Session Capture and Analysis Task"
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
artifact_id: "SPEC-0212-TSK-0108"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-24"
---

# P10 Session Capture and Analysis Task

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

Own criterion164/W180 in the [Spec](../spec.md) and [Plan](../plan.md).
Apply the D10 session capture and analysis delta to the existing Docker
capture and analysis stores without rebuilding what TSK-0084 and TSK-0107
already observed.

##### Inputs and Authority

The direct P10-SESSIONS1.2.0 request authorizes this workspace, scoped
implementation, bounded observations and normal commit, push, PR and merge.
Inputs are the matching package README/P10, D10, the session retention
policy, decision Q-02, the requirements matrix rows U48, U50, U56 and U57,
and the Docker profile and findings D23-11 and D23-12; no other workspace is
required. Start was clean `main` 4b9d6e41 on branch
`codex/p10-sessions-1-2-0` in the linked worktree `.worktrees/p10-sessions`,
because the live hooks run this checkout's capture module on every turn and
an intermediate edit must not migrate the real store. Brief p10-sessions
revision 1 bound this scope before the first edit. Direct user authorization
is authority; this record is not.

#### Execution Log

##### Work Performed

Retained without rework: the hook enqueue and its failure log, the Claude
transcript cursor reconcile and Codex limit, lease fencing, the deterministic
local rules and the TSK-0107 promotion outbox. Discovery against D10 found
these gaps. Analysis read `captured_at > window_end`, so an event captured in
the same second after a run was never read; the real store holds 56 seconds
with more than one event. A pending candidate's `source_event_ids` was
replaced by the latest run's events and cut to 50. A prompt was cut to 64 KiB
before redaction, so a secret on the cut could keep its prefix, and its
digest covered the unredacted text for 90 days; the real store holds a
21,032-byte prompt. Everything expired together at 90 days. The visible final
response that Q-02 selects was not captured and R137 forbade it. The timer
had one fixed name for every clone, with no bound store, and a linked
worktree could install it. A run had no input bound or backlog report, and
candidates never expired.

`session_capture` now redacts each selected text whole, cuts it to 16 KiB of
UTF-8 and redacts again, marking a cut `truncated`. It stores the visible
final response from `Stop`, takes a never-reused ingest sequence per insert,
keeps the fingerprint over the stored redacted text and clears text and
fingerprint 30 days after the event while metadata stays 90 days. Past a
256 MiB store only metadata and the `quota` gap are kept. The first
connection migrates an older store once. `session_analysis` reads at most
5,000 events after its ingest-sequence cursor and the failure log after its
byte offset, with rotation detected by the first line, and commits both with
the candidates. Repeated prompts are matched against the 30-day content
history, so a repetition split across runs is found. A new correction rule
groups three or more correction prompts with the response before each.
Source events form a union, and a redelivery counts once. `candidates`
reports `source_expired`. A pattern clears with its content, and candidates
expire 90 days after creation or 30 days after a decision. The timer name
carries the checkout's workspace key and its service names the capture store.
A linked worktree is refused, and this checkout's old fixed-name unit is
moved, while another checkout's is kept. `observe.py` follows the new unit
name. ENVIRONMENT-CONSTRAINTS 2.3.0 changes R136-R138 and R144-R146, and
the harness maintenance guide 2.3.0 documents the behaviour.

##### Blockers and Decisions

No Q01-Q04 question is reopened. R137 forbade copying replies; Q-02 selects
the visible final response, so the requirement prevails and R137 now
forbids hidden reasoning, intermediate replies and tool input or output
only. Tool results are not captured: D10 adds no field without a consumer,
and no deterministic rule here reads them. The 4 KiB summary limit has no
producer here, because no wider original is captured to summarize. The
event ID still includes the content fingerprint, as before, so a retried
hook without a turn ID stays one event; for an event before this change the
ID was derived from an unredacted digest and expires with its 90-day record.
The analysis budget stays local and deterministic at 0 USD; no text leaves
the host.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 164 | W180 | method=review; tool=-; command=- | P10 1.2.0 package, D10, retention policy, Q-02, D23-11, D23-12; current session_capture, session_analysis, observe and ENVIRONMENT-CONSTRAINTS R136-R148; real stores read only | PASS | Gaps listed in Work Performed; hooks, reconcile, fencing, rules and outbox retained | required | - |
| E02 | 164 | W180 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_session_capture tests.validation.test_session_analysis | New regressions on the pre-change code at 4b9d6e41 | FAIL | Witnessed RED: capture 1 failure and 5 errors over 6 new tests; analysis 2 failures and 7 errors, including the same-second event, the provenance union, the backlog, expiry and the bound timer | required | - |
| E03 | 164 | W180 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_session_capture tests.validation.test_session_analysis | Change | PASS | Exit0; 43 tests, with the migration, correction, expired-provenance and earlier-cursor cases added | required | E02 |
| E04 | 164 | W180 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_agent_memory tests.validation.test_session_analysis tests.lib.hooks.test_session_capture tests.validation.test_observe tests.validation.test_task_forecast tests.validation.test_work_dispatch tests.validation.test_agent_governance_ci_routing | Change | PASS | Exit0; 224 tests | required | - |
| E05 | 164 | W180 | method=automated; tool=ruff; command=ruff check and ruff format --check on the changed Python files | Change | PASS | Exit0 | required | - |
| E06 | 164 | W180 | method=observation; tool=Python3.12.3 CLI; command=session_capture hook Stop and UserPromptSubmit; session_analysis.py run twice and candidates; session_capture status | A scratch capture directory through HY_HOME_CAPTURE_DIR with three synthetic sessions | PASS | Cursor 0 to 6, backlog 0, 3 candidates; second run read nothing; correction candidate with 6 sources; no stored text holds the masked value; 3 responses stored; status reports 30 and 90 days; the scratch store was deleted | required | - |

##### Resolution Links

E03 resolves the witnessed failures in E02.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 164 | pending | E01,E03,E04,E05,E06,E07 | Implementation, focused regressions and a synthetic CLI run are recorded; the real store migration, the timer move and owner acceptance remain | @buenhyden |

##### Remaining Conditions

The real capture and analysis stores migrate on their first connection after
the merge, and this checkout's timer moves to its named unit with
`install-timer` from the primary checkout. Both are observed after the merge
and recorded here. A scheduled run of the new unit is observed at its next
03:00 run. A native Codex capture of the final response waits for the Codex
usage limit to lift on 2026-11-27 12:53.

#### Handoff

##### Promotion Receipt

`session_capture.py`, `session_analysis.py` and `observe.py` own the
behavior; ENVIRONMENT-CONSTRAINTS R136-R138 and R144-R146 own the rules; the
harness maintenance guide owns the commands. This Task owns execution
evidence only.

##### Next Owner

The owner decides criterion164. The next input for this workspace is
P11-FORECAST; it is not executed automatically. Keep the package through P17.

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
