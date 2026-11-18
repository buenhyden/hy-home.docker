---
title: "W08 Session Capture Task"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0084"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-18"
---

# W08 Session Capture Task

## Scope

### Objective and Parent

Own criterion 140 and work units W154 and W155 under the [Spec](../spec.md)
and [Plan](../plan.md). Bring session capture to the 4.2.0 W08-CAPTURE
design: actual capture, retention and gap recovery of visible prompts, with
completeness stated rather than assumed.

### Inputs and Authority

The direct 2026-11-18 request runs W08-CAPTURE from the git-ignored 4.2.0
package, with designs D07, D17 and D06. On 2026-11-18 the owner chose to
capture visible prompts and event metadata only, keep them 90 days, and
store them redacted in a private directory. Decision Q06 keeps collection
local. Reading another personal session file or changing what a provider
retains needs its own approval.

## Execution Log

### Work Performed

#### Gap analysis

No session capture existed. Both providers already route `SessionStart`,
`UserPromptSubmit`, `Stop` and `PreCompact` through
`scripts/hooks/agent-event-hook.sh`; no `SessionEnd` hook is registered.
No policy forbade capture outright: ENVIRONMENT-CONSTRAINTS-R55 to R57
keep native memory files unread and R79 keeps source pins away from
personal paths, and both stay. Claude Code 2.1.327 writes each visible
prompt as a `user` line with string content, a `uuid` and a `promptId`.
Codex 0.169 rollouts mix injected context into user-role messages and mark
no visible prompt, and a Codex hook may give a null transcript path.

#### W154 design

`scripts/lib/hooks/session_capture.py` keeps a rollback-journal SQLite store
at `.workspace-capture/capture.sqlite3`, 0700 and 0600, ignored by Git and
outside every backup include. The dispatcher calls `hook` for the four
events with all output discarded and its result ignored. The hook writes
one event: provider, version, session, a per-session sequence, kind,
transcript path and size, and for a prompt the text with secret shapes and
`password|secret|token|api_key` values replaced, a digest of the original
and the redaction count. The event ID binds provider, session, kind, turn
or source or transcript size, and the prompt digest, so a retried hook adds
nothing. A failure appends to `degraded.log` and never raises.

`Stop` and a `SessionStart` from `resume` or `compact` start a detached
reconcile under a non-blocking lock. For Claude it reads the transcript
from its cursor (inode, offset, head digest), leaves a partly flushed line
for the next run, rescans a replaced or truncated file, links each prompt
line to its hook event by digest and records a prompt the hooks missed by
its `promptId`, never twice. A session is complete only when every line
was readable, nothing is pending and every hook prompt appears in the
transcript; otherwise it is partial with the reason. Codex reports partial
(hook events only) or unavailable without a transcript path. A transcript
is read only when it is a regular, owned `.jsonl` file under the
provider's own session directory. Reconcile prunes records older than 90
days. Nothing is promoted to memory.

ENVIRONMENT-CONSTRAINTS-R136 to R142 and RUN-0021 state the behavior. The
hook entry starts in about 0.06 s on this host. A routing test forbids the
`Stop` path from calling an external `timeout`, so the bounds live in the
module: a 1 s SQLite busy wait, a non-blocking lock and a detached
reconcile.

#### Native Claude observation

Once the dispatcher change was in the main checkout, this session's own
hooks captured events, and a second Claude session in the workspace was
captured too. The first status showed two defects. Claude records provider
notifications as `user` lines and fires `UserPromptSubmit` for them, so 215
`<task-notification>` texts were stored as prompts; Claude 2.1.327 marks a
typed prompt with `origin.kind: human` and a notification with
`task-notification`, so capture now keeps only human turns, drops compact
summaries and lines starting with a notification, command output or system
reminder tag, and the hook ignores a notification prompt. And 48 failures
came from test runs that called the real dispatcher with payloads that had
no session ID; every provider event carries one, so such a call is now
ignored instead of counted. The 215 misclassified rows and the 48 log lines
were deleted from the real store, which the transcripts can rebuild, and a
reconcile then reported both sessions complete with 427 events and no
failure.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0084 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0084 | ready | in-progress | #w154-design |

### Blockers and Decisions

After the Codex usage limit ended at 16:29 KST on 2026-11-18, three
`codex exec` sessions in this workspace each recorded SessionStart,
UserPromptSubmit and Stop through the shared dispatcher. Codex transcripts
stay unparsed, so those sessions report partial with the reason "transcript
format unsupported; hook events only", as designed.

The real store also held 25 sessions named `s` or `test-<32 hex>` with 60
events. `test_folder_guides` drove the real hooks from the repository root,
and capture resolves its store from that repository. `capture_dir` now
honors `HY_HOME_CAPTURE_DIR`, the hook tests point it at their temporary
state, and RUN-0021 says so. The 25 test sessions were deleted by exact
name from the real store, leaving 13 provider sessions; no pending analysis
candidate cited a deleted event.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Capture RED | 140 | W154 | `test_session_capture` | New tests on `0dcf8bc2f` | FAIL | Import error: no capture module | required | - |
| Capture GREEN | 140 | W154 | `test_session_capture` | Capture module and dispatcher change | PASS | 10 tests: idempotency, redaction, recovery, partial flush, rewrite, Codex, outside paths, retention, failure, lock | required | Capture RED |
| Contract checks | 140 | W154 | capture, script manifest, routing and surface suites | Capture change on `0dcf8bc2f` | PASS | 162 tests | required | - |
| System turn RED | 140 | W154 | `test_session_capture` notification and session cases | Real store status after native capture | FAIL | 215 notifications stored as prompts; 48 non-provider calls counted as failures | required | - |
| System turn GREEN | 140 | W154 | `test_session_capture` notification and session cases | Origin filter and session guard | PASS | 12 tests | required | System turn RED |
| Native Claude capture | 140 | W155 | `session_capture status` | Real capture store, two Claude sessions | PASS | Both complete, 427 events, no failure | required | - |
| Native Codex capture | 140 | W155 | `session_capture status` after a Codex session | Real capture store | NOT_RUN | Codex usage limit until 16:29 KST | required | - |
| Native Codex capture observed | 140 | W155 | `session_capture status` after a Codex session | Real capture store after three `codex exec` sessions | PASS | 3 sessions, each SessionStart, UserPromptSubmit and Stop by hook; partial, transcript format unsupported | required | Native Codex capture |
| Test isolation RED | 140 | W154 | `CaptureDirectoryTests` | New test before the override | FAIL | `capture_dir` ignored `HY_HOME_CAPTURE_DIR` and returned the real store | required | - |
| Test isolation GREEN | 140 | W154 | `CaptureDirectoryTests` | Override and hook test environment | PASS | 38 capture and folder-guide tests; the real store held 38 sessions before and after the run | required | Test isolation RED |
| Test session removal | 140 | W154 | exact-name delete in the real capture store | Sessions `s` and `test-<32 hex>` | PASS | 25 sessions and 60 events deleted; 13 provider sessions remain; no analysis candidate affected | required | - |

### Resolution Links

Capture GREEN resolves Capture RED, and System turn GREEN resolves System
turn RED. Native Codex capture observed resolves Native Codex capture, and
Test isolation GREEN resolves Test isolation RED.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 140 | pending | Capture GREEN, System turn GREEN, Native Claude capture, Native Codex capture observed, Test isolation GREEN | Awaits the owner's decision | @buenhyden |

### Remaining Conditions

None in W154 or W155. W08-ANALYSIS owns scheduled analysis of the captured
events.

## Handoff

### Promotion Receipt

`session_capture.py`, `agent-event-hook.sh`, ENVIRONMENT-CONSTRAINTS-R136 to
R142 and RUN-0021 hold the W154 behavior, including the test directory
override.

### Next Owner

The owner decides criterion 140.
