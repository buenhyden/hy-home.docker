---
title: "npm Risk Acceptance Extension Task"
version: "0.2.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-22"
layer: "specs"
artifact_id: "SPEC-0222-TSK-0001"
parent_ids:
- "SPEC-0222-PLAN-0001"
created: "2026-10-09"
---

# npm Risk Acceptance Extension Task

## Overview

### Objective

Extend the GHSA-vfj7-8cjw-p6xm acceptance by the owner's approval and let a
future approval extend it without a code or governance change.

## Inputs and Authorization

On 2026-10-09 the owner asked to upgrade to a patched version after SPEC-0221.
The official advisory (`GET /advisories/GHSA-vfj7-8cjw-p6xm`) lists
`braces <= 3.0.3` with no patched version; npm lists `braces` 3.0.3 (2024-05),
`eslint-config-next` and `@next/eslint-plugin-next` 16.4.0, and `fast-glob`
3.3.3, which still depends on `micromatch`. Offered an extension, removal of
the Next lint chain, or expiry, the owner chose a 30-day extension and asked to
replace the dated text in the quality standard with a rule that lets an
approval extend the window.

## Work Log

### W1 Contract Window

`_parse_npm_audit_acceptance` keeps the advisory, owner, project, chain and
URL pinned and accepts `approved_at` and `expires_at` as UTC timestamps with
`approved_at < expires_at <= approved_at + 30 days`. The record carries
`approved_at` `2026-10-09T07:00:00Z` and `expires_at` `2026-11-08T07:00:00Z`.
The window is counted from the approval, so it ends on 2026-11-08 rather than
30 days after the old expiry. Contract and adapter tests: 68 pass.

### W2 Quality Standard Rule

The bounded acceptance section no longer restates SPEC-0205 and SPEC-0219
dates. It names the record fields the workflow contract owns, keeps the
identity pinned, and lets the owner extend by up to 30 days from approval while
the advisory lists no patch, with no governance amendment. The owner applied
the copy prepared under the ignored `_workspace/ghsa/` after the auto-mode
safety check refused it to the agent (`ad12a1a6d`); the agent-governance contract
and markdownlint pass.

### Review

The independent review found that a future `approved_at` passed the 30-day
bound while the audit accepted the risk from the current time, and that the
contract tests named the current dates, so an extension would also have needed
a test edit. `921d2f6a8` makes the audit require `approved_at <= now < expires_at`
at both expiry checks, adds a future-approval adapter case, and derives the
30-day, over-limit, equal and reversed cases from the live record; offset,
non-string and impossible timestamps are covered. The quality standard lists
the pinned identity without `advisory_url`; kept, because the code is the
stricter side. Contract and adapter tests: 69 pass.

### W3 Validation

SPEC-0221 merged as PR #396 (`40dcfb349`) and this branch was rebased onto it.
In a throwaway worktree with the branch staged on `40dcfb349`, the changed
gate, which includes the candidate preflight, and the staged style check ran on
the final head. `candidate-quality` and the merge are recorded in the pull
request.

### Current Contract Approval 2026-10-22

The user's current request on 2026-10-22 explicitly authorizes status and lifecycle
processing for implemented Specs, Plans and Tasks. The earlier audit was compared
with the current Spec and Plan, and this package's public implementation at
`bd4168e20` was confirmed unchanged since the audit input `d7bec9a9a`.
The current contracts and assignments remain valid, so the Spec and Plan are each
approved through `draft → approved`, with their first stable version `1.0.0`.
This present decision neither backdates approval of the original implementation
nor grants new operational authorization or risk acceptance.

### Current Readiness Review 2026-10-22

The currently approved parent Spec and Plan, assigned Work Units, existing
implementation, and this Task's Evidence and Criterion Acceptance were secured
as closure-review inputs. Preparation for the document closure requested today
is complete, so the Task transitions `draft → ready` today. No execution status
is inferred for the time of the historical source or runtime work.

### Current Closure Review 2026-10-22

The prepared document closure review was performed, transitioning the Task
`ready → in-progress`. The canonical package reader and the assignment, evidence
and acceptance rows confirm PASS for all 3 criterion/Work Unit pairs assigned
to this Task, accepted decisions for all criteria it owns, and no unresolved FAIL.
Existing checks and decisions are reused; observation and acceptance rows are unchanged.
Completion covers delivery of the existing window, parser and rule. It neither changes `expires_at=2026-11-08T07:00:00Z` nor extends risk acceptance. No fresh external advisory patch-status check is claimed.

### Current Completion Decision 2026-10-22

Today's readiness and closure reviews, including assigned-pair PASS and existing
accepted decisions, are complete, so the Task transitions `in-progress → completed`.
Completion is limited to this Task's assigned scope. The lifecycle rows below
record the document transitions actually performed today; they do not replace
historical execution evidence. Archive readiness is derived by the canonical
reader, and this change performs no Stage 98 move.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0222 | draft | approved | #current-contract-approval-2026-10-22 |
| SPEC-0222-PLAN-0001 | draft | approved | #current-contract-approval-2026-10-22 |
| SPEC-0222-TSK-0001 | draft | ready | #current-readiness-review-2026-10-22 |
| SPEC-0222-TSK-0001 | ready | in-progress | #current-closure-review-2026-10-22 |
| SPEC-0222-TSK-0001 | in-progress | completed | #current-completion-decision-2026-10-22 |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Contract window | 1 | W1 | Contract and adapter tests | `7258d2bfb` | PASS | W1 Contract Window | - |
| Extension rule | 2 | W2 | Agent-governance contract; markdownlint | `ad12a1a6d` | PASS | W2 Quality Standard Rule | - |
| Review fixes | 1 | W1 | Contract and adapter tests | `921d2f6a8` | PASS | Review | - |
| Local validation | 3 | W3 | Changed gate with preflight; staged style check | final branch head | PASS | W3 Validation | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | accepted | Contract window, Review fixes | Generation 5 row acceptance |
| 2 | accepted | Extension rule | Generation 5 row acceptance |
| 3 | accepted | Local validation | Generation 5 row acceptance |

## Review and Completion

The current status is `completed`. Today's
[completion decision](#current-completion-decision-2026-10-22) owns the current
lifecycle; the existing completion, observation and limitation records below
are preserved as history for their dated inputs.

Complete. `candidate-quality` passed on head `751821989` against base
`40dcfb349`, and PR #397 merged as `0df98f405` before the earlier acceptance
expired.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
