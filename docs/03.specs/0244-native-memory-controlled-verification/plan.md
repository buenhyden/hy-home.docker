---
title: "Native Memory Controlled Verification Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0244-PLAN-0001"
parent_ids:
- "SPEC-0244"
created: "2026-10-16"
---

# Native Memory Controlled Verification Plan

## Overview

Prepare and run a narrowly controlled native-session observation. The normal
session is evidence only for views it exposes without a mutating action; it is
not a substitute for a provider-wide trust or hook-delivery test.

## Scope

W1 writes the allowlist and redaction boundary. W2 records the already
available public Codex CLI feature observation without broadening its meaning.
W3 performs an authorized normal Claude control query using only
initialize/get-memory-dialog/end-session and requires a non-mutating
effective-memory-off view to accept criterion 3. W4 separates a hooks-menu
result from actual event receipts through independently reviewed, conditional
exact-fixture attempts after W3 passes. W5 records each attempt's boundary and
cleanup. W6 obtains review and runs document checks. No work unit reads a
memory body, changes persistent/global configuration or provider state, or
changes completed Task records.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Record session target, action allowlist, redaction, and stop conditions | None | TSK-0001 | Task evidence review |
| W2 | 2 | Record and limit the public Codex CLI feature-boundary observation | W1 | TSK-0001 | Sanitized Task evidence |
| W3 | 3 | Perform an approved normal Claude control query using only initialize/get-memory-dialog/end-session and retain only a Boolean/enum classification; otherwise retain pending status | W1 | TSK-0001 | Sanitized Task evidence and independent security review |
| W4 | 4 | After W3 PASS, run only independently reviewed exact ignored-fixture provider attempts and record sanitized receipts for UserPromptSubmit, PreToolUse, PostToolUse, and Stop | W1, W3 | TSK-0001 | Sanitized Task evidence |
| W5 | 5 | For each W4 attempt, record the Task-reviewed two- or three-turn/USD 1 bound, strict MCP/tool denial, fixture hash, raw-output disposal, cleanup, and any session-only forced-memory or sandbox fallback proof class | W4 | TSK-0001 | Sanitized Task evidence |
| W6 | 6 | Privacy/security review and selected changed-document checks | W2, W3, W4, W5 | TSK-0001 | Review and gate evidence |

## Verification Plan

- Review the action allowlist before the normal control query and every
  conditional fixture attempt. Each fixture attempt is limited to its
  Task-reviewed two- or three-turn/USD 1 bound, strict empty MCP, and no
  Chrome, Bash, or network tools.
- Record only result categories, timestamps, provider/session category, and
  value-free observed state. The approved normal control query may transiently
  read provider metadata but retains only its Boolean or enum classification;
  it never retains a memory body, authentication, prompt, or tool content.
- Run the selected changed-document metadata, link, and Task-evidence checks.
- Obtain an independent privacy/security review before criterion acceptance.

## Risks and Recovery

### Risks and Rollback

- **Ambiguous provider view.** A menu may not expose effective memory state.
  Record it as unverified, leave criterion 3 pending, and do not explore hidden
  or mutating controls. The fixture probe then remains NOT_RUN.
- **Fixture side effect.** Each independently reviewed attempt may use only
  the exact ignored fixture after memory-off is proved. A changed fixture path,
  missing strict tool boundary, exceeded Task-bound turn/cost limit, or
  incomplete cleanup stops that attempt and keeps criteria 4 and 5 pending.
- **Sensitive output.** Stop before capture; retain no raw output and escalate
  the need for a redacted collection plan.
- **Session side effect.** The normal control query cannot change settings. A
  session-only forced-memory flag or `sandbox=false` fallback requires a
  separately reviewed Task plan, is classified separately from normal merged
  state, and does not alter persistent settings.
- **Rollback.** This package changes no persistent or provider-global state.
  A documentation correction is a normal reviewed Git change; it does not
  alter any session.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-native-memory-controlled-verification.md)
