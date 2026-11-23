---
title: "P10 Session Capture and Analysis Task"
version: "0.1.5"
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

On 2026-11-24 the owner decided to capture tool results, remove the
text-derived event IDs and close the P09 leftovers. A failed tool call now
keeps its tool name and failure text, redacted and cut to 4 KiB. Claude sends
it through a new `PostToolUseFailure` binding in the Registry, the wrapper and
the settings; Codex sends a shell failure through `PostToolUse`, kept only
when the exit is not 0. A new `tool-failure` rule groups three or more
failures with the same tool and first line. Event IDs now come from provider,
session, event and a stored marker only. Each connection checks the prompt
rows past a watermark and rekeys any whose ID came from its text, mapping the
old ID until the next analysis run rewrites candidate and outbox references.
`promote --include-earlier` records intents for candidates accepted before
the outbox. ENVIRONMENT-CONSTRAINTS 2.4.0 changes R136, R137 and R139, and the
harness maintenance guide is 2.4.0.

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

The worktree did not isolate the real store. `capture_dir()` maps every
linked worktree to the primary checkout's shared store, and a hook runs the
`scripts` package of its working directory. A hook run while this session
worked in the worktree migrated the real store before the merge. Later hooks
from the primary checkout, still on the old code, wrote 4 `Stop` rows with no
ingest sequence, which the cursor would never read. Checkouts on different
code can always share one store, so the fix is in the shared `connect`: any
row without a sequence is adopted on the next connection. It gets the next
sequence, redacted-then-cut text, a replaced digest and a normalized time.
An audit-hook probe found why the real store moved before each merge. A hook
test without a captured event still started a detached reconcile
(`--session None`), and that reconcile, without `HY_HOME_CAPTURE_DIR`,
resolved the shared real store and migrated it with the tested checkout's
code; during this follow-up it took the real store to schema 3 with 209 IDs
rekeyed. `hook()` now starts a reconcile only after it stored an event, and
`tests/__init__.py` gives every test process a temporary capture directory;
the probe then found no access to the real store. Rows written meanwhile by
the merged schema 2 code are caught by the ID watermark. A Claude or Codex
tool failure has not yet reached the real store; the next failing tool call
observes the native route.

Redaction no longer counts a value that is exactly `[REDACTED]` again. A
first lookahead also skipped a value that only began with `[REDACTED]`; an
automated security review found it before merge (E13), and the lookahead now
needs the masked marker to end the value.

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
| E07 | 164 | W180 | method=automated; tool=Python3.12.3; command=check-agent-governance-contract.py --mode repository --section all; check-document-metadata.py --mode check-active and check-changed; check-document-links.py --mode all --changed; check-document-corpus-lifecycle.py; check-candidate-preflight.sh; provider_surface_renderer.py --check; check-script-manifest.py | Changed-profile selection on the candidate; run-ci-gate.py itself refuses locally because Python 3.12.3 differs from the hosted 3.14.8 | PASS | Governance failures0; metadata violations0; links failures0; lifecycle violations0; preflight exit0; renderer drift0; manifest valid | required | - |
| E08 | 164 | W180 | method=automated; tool=GitHub Actions CI Quality Gates; command=candidate-core changed candidate validation | PR1149 head 82349929, run45281460776 | PASS | candidate-core, candidate-quality and candidate-routing passed; CodeQL and GitGuardian passed | required | - |
| E09 | 164 | W180 | method=observation; tool=Python3.12.3 CLI; command=session_capture reconcile; read-only SQL counts; session_analysis.py run and candidates --all | Real stores after merge e9b64846 | FAIL | Schema 2; 1,019 events, 9 prompts cut to 16,384 bytes, times normalized; run read cursor 1009 to 1015, backlog 0; 14 candidates kept; but 4 Stop rows written by the pre-merge code had no ingest sequence and would never be read | required | - |
| E10 | 164 | W180 | method=observation; tool=systemd user manager; command=session_analysis.py install-timer from the primary checkout; systemctl --user list-timers and cat | This host after merge e9b64846 | PASS | Fixed-name unit disabled and removed; hy-home-session-analysis-40ae7a89c683.timer enabled for 03:00 with WorkingDirectory and HY_HOME_CAPTURE_DIR of this checkout; the k8s and template timers untouched; no scheduled run of the new unit yet | required | - |
| E11 | 164 | W180 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_session_capture | Adoption regression on e9b64846 | FAIL | Witnessed RED: a row written without a sequence kept ingest_seq NULL | required | - |
| E12 | 164 | W180 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_session_capture | Adoption fix | PASS | Exit0; 20 tests with the adoption case; the analysis and observe suites also pass | required | E11 |
| E13 | 164 | W180 | method=automated; tool=Python3.12.3; command=redact("token=[REDACTED]hunter2") on commit 15e68a5e, then python3 -m unittest tests.lib.hooks.test_session_capture | Masked-prefix value before and after the lookahead fix | PASS | Before: the value stayed unmasked with count 0; after: masked with count 1, an exact `[REDACTED]` still counts 0; 21 tests pass | required | - |
| E14 | 164 | W180 | method=observation; tool=Python3.12.3 CLI; command=session_capture reconcile; read-only SQL counts; session_analysis.py run and candidates --all | Real stores after merge 29f0bfc2 | PASS | 1,021 events, none without a sequence, 1,021 distinct sequences and counter 1,021; the run read cursor 1015 to 1021 with the 4 adopted rows, backlog 0 | required | E09 |
| E15 | 164 | W180 | method=observation; tool=Claude Code 2.1.331 Stop hook; command=read-only SQL on the real capture store | This session's Stop events after the merge | PASS | 2 claude Stop events stored the visible final response, 75 and 123 bytes, content_state stored; no Codex Stop observed | required | - |
| E16 | 164 | W180 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_session_capture tests.validation.test_session_analysis | New tool-failure, ID, rekey and earlier-promotion regressions on 6e252f6e | FAIL | Witnessed RED: 3 failures and 4 errors over 7 new tests | required | - |
| E17 | 164 | W180 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_session_capture tests.validation.test_session_analysis | Follow-up change | PASS | Exit0; with the dispatcher route and reconcile-start cases added | required | E16 |
| E18 | 164 | W180 | method=automated; tool=Python3.12.3 audit hook; command=sitecustomize audit hook on sqlite3.connect and open of the real capture path while running the routing, dispatch, forecast, observe, memory, folder-guide, capture and analysis suites | Before and after the reconcile-start and test-directory fix | PASS | Before: 12 accesses by reconcile --session None from hook tests; after: 0; suites exit0 | required | - |
| E19 | 164 | W180 | method=automated; tool=GitHub Actions CI Quality Gates; command=candidate-core changed candidate validation | PR1152 head 026d8e32, run45289346245 | PASS | candidate-core, candidate-quality and candidate-routing passed; CodeQL and GitGuardian passed | required | - |
| E20 | 164 | W180 | method=observation; tool=Python3.12.3 CLI; command=session_capture reconcile; read-only SQL; session_analysis.py run and candidates --all; ID formula check | Real stores after merge 1fc58dcb | PASS | Schema 4, watermark 1,027, no row without a sequence; the run applied the 209-entry map and cleared it; 14 candidates with 0 expired sources; 209 hook prompt rows, 0 with a text-derived ID | required | - |
| E21 | 164 | W180 | method=observation; tool=Python3.12.3 CLI; command=session_analysis.py promote --include-earlier, then promote; agent_memory.py list --all and list | Real stores after merge 1fc58dcb, owner decision 2026-11-24 | PASS | The 3 earlier accepted candidates became 3 unreviewed candidate records at revision 1; default reads 0; the second promote wrote nothing | required | - |

##### Resolution Links

E03 resolves the witnessed failures in E02.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 164 | pending | E01,E03,E04,E05,E06,E07,E08,E10,E12,E13,E14,E15,E17,E18,E19,E20,E21 | Implementation, focused regressions, a synthetic CLI run, the real migration and row adoption, native Claude response capture and the timer move are recorded; a scheduled run of the new unit, a Codex response capture and owner acceptance remain | @buenhyden |

##### Remaining Conditions

E14 records the adoption of the real store's 4 rows and resolves E09. A
scheduled run of the new unit is observed at its next 03:00 run. A native Codex capture of the final response waits for the Codex
usage limit to lift on 2026-11-27 12:53.

#### Handoff

##### Promotion Receipt

`session_capture.py`, `session_analysis.py` and `observe.py` own the
behavior; ENVIRONMENT-CONSTRAINTS R136-R138 and R144-R146 own the rules; the
harness maintenance guide owns the commands. This Task owns execution
evidence only.

##### Next Owner

The owner decides criterion164 in P16 (decision of 2026-11-24). The next input for this workspace is
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
