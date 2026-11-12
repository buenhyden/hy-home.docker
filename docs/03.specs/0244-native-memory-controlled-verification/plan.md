---
title: "Native Memory Controlled Verification Plan"
version: "0.1.2"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0244-PLAN-0001"
parent_ids:
- "SPEC-0244"
created: "2026-10-16"
---

# Native Memory Controlled Verification Plan

## Overview

### Goal and Boundary

Prepare and run a narrowly controlled native-session observation. The normal
session is evidence only for views it exposes without a mutating action; it is
not a substitute for a provider-wide trust or hook-delivery test.

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

Parent Spec:

- [Spec](spec.md)

### Assumptions

The plan works under the approved SPEC-0244; it assumes no authority beyond it. The normal session is evidence only for views it exposes without a mutating action.

## Dependencies

### Prerequisites

The plan needs only the approved Spec, an authorized normal Claude control query and the public Codex CLI feature observation named in its Goal and Boundary; it changes no persistent or provider-global state.

### Dependency Order

W1 has no dependency. W2 and W3 start after W1. W4 starts after W1 and W3, and W5 after W4. W6 starts after W2 to W5.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Record session target, action allowlist, redaction, and stop conditions | None | TSK-0001 | Task evidence review |
| W2 | 2 | Record and limit the public Codex CLI feature-boundary observation | W1 | TSK-0001 | Sanitized Task evidence |
| W3 | 3 | Perform an approved normal Claude control query using only initialize/get-memory-dialog/end-session and retain only a Boolean/enum classification; otherwise retain pending status | W1 | TSK-0001 | Sanitized Task evidence and independent security review |
| W4 | 4 | After W3 PASS, run only independently reviewed exact ignored-fixture provider attempts and record sanitized receipts for UserPromptSubmit, PreToolUse, PostToolUse, and Stop | W1, W3 | TSK-0001 | Sanitized Task evidence |
| W5 | 5 | For each W4 attempt, record the Task-reviewed two- or three-turn/USD 1 bound, strict MCP/tool denial, fixture hash, raw-output disposal, cleanup, and any session-only forced-memory or sandbox fallback proof class | W4 | TSK-0001 | Sanitized Task evidence |
| W6 | 6 | Privacy/security review and selected changed-document checks | W2, W3, W4, W5 | TSK-0001 | Review and gate evidence |

### Change and Rollback

- **Rollback.** This package changes no persistent or provider-global state.
  A documentation correction is a normal reviewed Git change; it does not
  alter any session.

## Verification Plan

### Verification Matrix

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

### Stage Placement

The Plan places no stage-specific checks beyond the Verification Matrix; the Task records each run.

## Risks

### Risks and Mitigations

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

### Escalation

Per Spec item 6 and its failure and edge cases, the execution owner stops and escalates before restricted content enters evidence, and a request to widen the fixture or tool boundary stops this package. An ambiguous view leaves the state unverified and the criterion pending.

## Promotion Map

### Durable Meaning

This package changes no persistent state. Its lasting meaning is the sanitized result classification and criterion status that TSK-0001 retains.

### Owner and Receipt

Owner @buenhyden. The receipt is the sanitized evidence recorded in TSK-0001.

- [Task](tasks/tsk-0001-native-memory-controlled-verification.md)
