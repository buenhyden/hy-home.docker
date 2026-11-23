---
title: "P08 Native Brief Task"
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
artifact_id: "SPEC-0212-TSK-0106"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-24"
---

# P08 Native Brief Task

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

Own criterion162/W178 in the [Spec](../spec.md) and [Plan](../plan.md).
Make the request brief precede the first recognized workspace edit of an
observed session, and let the user see that a brief is bound.

##### Inputs and Authority

The direct P08-NATIVE-BRIEF1.2.0 request authorizes this workspace, scoped
implementation, bounded native observations and normal commit, push, PR and
merge. Inputs are the matching package README/P08, D08, D21, confirmed Q03 and
the Docker profile and findings; no other workspace is required. Start was
clean `main` 504795bc on branch `codex/p08-native-brief-1-2-0`. Brief
P08-NATIVE-BRIEF-docker-1.2.0 revisions 1 and 2 bound this scope before each
first edit. Direct user authorization is authority; this record is not.

#### Execution Log

##### Work Performed

Criterion134 (TSK-0078) already accepted BriefRecord 3.0.1 and native Codex
and Claude prompt binding and edit scope. Discovery found two D08 gaps: the
shared pre-tool hook checked edits only for sessions that had bound a brief
(AGENTIC-R63 treated other sessions as a coverage gap), and nothing showed the
user that a brief was bound. Q03 removes that exemption for supported routes.

`guard_edits` now refuses the first recognized workspace edit of a session
whose request was observed until a brief is bound; targets outside the
workspace and sessions with no observed request keep the reported gap.
`first_edit_notice` returns a notice for the first allowed edit of each bound
revision naming only the revision and action scope, and records the shown
revision in the prose-free private state. The dispatcher emits it as a
top-level `systemMessage`, which both providers surface in their UI, and keeps
model guidance in `additionalContext`. The prompt hook text states the gate.

The first native Claude run showed that a permission-restricted session could
not bind: the permission layer rejected a heredoc carrying JSON, a redirect
from `/tmp` and `python3 -c`. The gate made that a deadlock, because drafting
the record inside the workspace was itself an edit. The ignored
`.request-brief/` folder is now outside the first-edit check, so a session
writes the BriefRecord there and binds with `bind SESSION < FILE`. AGENTIC
4.1.0 records the gate, notice and draft route in R37, R63 and its prose.

##### Blockers and Decisions

No Q01-Q04 question is reopened. Codex 0.171.0 has persisted trust for the
unchanged `.codex/hooks.json`; its native run was refused before any turn by
the account usage limit, with a reset at 2026-11-27 12:53. That refusal is
recorded as blocked, not retried or bypassed. Codex hook behavior is covered
here only by the dispatcher regression with the Codex output shape.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 162 | W178 | method=review; tool=-; command=- | P08 1.2.0 package, D08, D21, Q03; current request_brief, dispatcher and AGENTIC R34-R63; TSK0078 criterion134 | PASS | Opt-in gate and missing user display identified; accepted 3.0.1 schema, store and native binding evidence reused | required | - |
| E02 | 162 | W178 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_request_brief | New refusal and notice regressions before the change | FAIL | Witnessed RED: an observed unbound session's first edit was allowed and `first_edit_notice` did not exist | required | - |
| E03 | 162 | W178 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_request_brief | Gate and notice, with the old opt-in assertion updated to the refusal | PASS | Exit0; 20 tests | required | E02 |
| E04 | 162 | W178 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_agent_governance_ci_routing.HookOutputAndMainPushTests.test_first_edit_waits_for_the_brief_then_shows_it_once | End-to-end hook for both provider shapes before the change | FAIL | Witnessed RED: no deny decision on the first edit for claude and codex | required | - |
| E05 | 162 | W178 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_agent_governance_ci_routing.HookOutputAndMainPushTests.test_first_edit_waits_for_the_brief_then_shows_it_once | Gate, notice and dispatcher output | PASS | Exit0; refusal, bind, one `systemMessage` naming revision 1 without the goal, and no repeat, for both providers | required | E04 |
| E06 | 162 | W178 | method=observation; tool=Claude CLI2.1.330 headless, existing first-party account, claude-sonnet-5-5; command=claude -p probe creating p08-brief-probe.txt with Read/Grep/Glob/Write and request_brief Bash only, max budget USD3 | Repository at 504795bc plus the candidate, user settings loaded | FAIL | The model could not bind: heredoc JSON was rejected as expansion obfuscation, a /tmp redirect was outside the working directories and `python3 -c` needed approval; user-global GateGuard hooks also intercepted. USD0.37, 10 turns; no edit attempted | required | - |
| E07 | 162 | W178 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_request_brief | New draft-folder regression before the exemption | FAIL | Witnessed RED: BRIEF_DRAFTS absent | required | - |
| E08 | 162 | W178 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_request_brief | Draft folder exempt and ignored | PASS | Exit0; 21 tests | required | E07 |
| E09 | 162 | W178 | method=observation; tool=Claude CLI2.1.330 headless, existing first-party account, claude-sonnet-5-5; command=claude -p probe creating p08-brief-probe.txt with Read/Grep/Glob/Write and request_brief Bash only, max budget USD3 | Same probe with --setting-sources project,local so only this repository's hooks load | PASS | Write refused with the gate message; status; draft written under .request-brief/; bind by redirect; retried Write allowed and the CLI showed the notice "Request brief revision 1 is bound ... (edit:p08-brief-probe.txt)". The model did not restate the brief in prose before binding. USD0.23, 12 turns, 37s. Probe file and draft deleted | required | E06 |
| E10 | 162 | W178 | method=observation; tool=Codex CLI0.171.0 exec, existing ChatGPT account, persisted hook trust; command=codex exec --json -s workspace-write probe | Same probe | NOT_RUN | Blocked before execution: the account usage limit refused the run before any turn; reset 2026-11-27 12:53. Not retried or bypassed | required | - |
| E11 | 162 | W178 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_agent_governance_ci_routing tests.lib.hooks.test_request_brief tests.lib.hooks.test_tool_payload tests.lib.hooks.test_folder_guides tests.lib.hooks.test_session_capture tests.validation.test_work_dispatch tests.lib.ops.test_dispatch_process | Final candidate | PASS | Exit0; 230 tests, 1 opt-in native test skipped and NOT_RUN | required | - |
| E12 | 162 | W178 | method=automated; tool=Python3.12.3; command=python3 scripts/validation/check-agent-governance-contract.py; python3 scripts/operations/provider_surface_renderer.py --check | AGENTIC 4.1.0 and unchanged provider surfaces | PASS | Governance contract failures0; renderer drift0 | required | - |
| E13 | 162 | W178 | method=automated; tool=GitHub Actions CI Quality Gates; command=candidate-core changed candidate validation | PR1147 head 37ffefd3, run45215197365 | FAIL | The new dispatcher test ran `request_brief status` against the hosted candidate checkout and it exited 1 for both providers; the child stderr was not captured. The refusal step had passed. candidate-quality failed only as the aggregate of this job | required | - |
| E14 | 162 | W178 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_agent_governance_ci_routing.HookOutputAndMainPushTests.test_first_edit_waits_for_the_brief_then_shows_it_once | Test isolated in a private Git fixture carrying the hook rules, child stderr asserted | PASS | Exit0 locally and under a simulated gate-root descriptor; RED again against the pre-change hook and library | required | - |
| E15 | 162 | W178 | method=automated; tool=GitHub Actions CI Quality Gates; command=candidate-core changed candidate validation | PR1147 head 78f2683b, run45216605394 | PASS | candidate-core, candidate-quality and candidate-routing passed with the isolated dispatcher test | required | E13 |

##### Resolution Links

E03, E05 and E08 resolve the witnessed failures E02, E04 and E07. E09
resolves E06 through the same native probe after the draft route and with only
repository settings loaded. E13 is the hosted failure of the first dispatcher test, which depended on the candidate
checkout; E14 isolates it, and E15 resolves E13 on the same hosted check. E10 is NOT_RUN: a pre-execution account refusal
is neither a pass nor an implementation failure.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 162 | pending | E01,E03,E05,E08,E09,E11,E12,E14,E15 | Implementation, focused regressions and the Claude native observation are recorded; the Codex native observation is blocked by the account usage limit and owner acceptance remains | @buenhyden |

##### Remaining Conditions

Run the same bounded Codex probe after the usage limit resets on 2026-11-27
12:53 and record it here; until then the Codex native route is unobserved.
Owner acceptance remains pending and may move to P16 once that observation is
recorded. Sessions with no observed request and writes the hook does not
recognize as edits remain the reported coverage gap.

#### Handoff

##### Promotion Receipt

`scripts/lib/hooks/request_brief.py` and the shared dispatcher own the gate and
notice; AGENTIC owns the rule. This Task owns execution evidence only.

##### Next Owner

The Codex observation stays with this Task. The next input for this workspace
is P09-MEMORY; it is not executed automatically. Keep the package through P17.

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
