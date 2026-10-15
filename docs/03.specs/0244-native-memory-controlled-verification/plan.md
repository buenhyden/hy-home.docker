---
title: "Native Memory Controlled Verification Plan"
version: "0.1.0"
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
W3 performs only an authorized normal Claude session under W1 and requires a
non-mutating effective-memory-off view to accept criterion 3. W4 separates a
hooks-menu result from actual event receipts through one conditional exact
fixture prompt, after W3 passes. W5 records its boundary and cleanup. W6
obtains review and runs document checks. No work unit reads memory, changes
configuration or global/provider state, or changes completed Task records.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Record session target, action allowlist, redaction, and stop conditions | None | TSK-0001 | Task evidence review |
| W2 | 2 | Record and limit the public Codex CLI feature-boundary observation | W1 | TSK-0001 | Sanitized Task evidence |
| W3 | 3 | Perform one approved normal Claude session using only W1 actions and obtain a non-mutating effective-memory-off view; otherwise retain pending status | W1 | TSK-0001 | Sanitized Task evidence |
| W4 | 4 | After W3 PASS, run one exact ignored-fixture provider prompt and record only sanitized receipts for UserPromptSubmit, PreToolUse, PostToolUse, and Stop | W1, W3 | TSK-0001 | Sanitized Task evidence |
| W5 | 5 | Record the three-turn/USD 0.10 bound, empty MCP/tool denial, fixture hash, raw-output disposal, and wrapper cleanup | W4 | TSK-0001 | Sanitized Task evidence |
| W6 | 6 | Privacy/security review and selected changed-document checks | W2, W3, W4, W5 | TSK-0001 | Review and gate evidence |

## Verification Plan

- Review the action allowlist before the normal session and the conditional
  fixture probe. The probe is one prompt only, at most three turns and USD
  0.10, with strict empty MCP and no Chrome, Bash, or network tools.
- Record only result categories, timestamps, provider/session category, and
  value-free observed state; do not retain memory, authentication, prompt, or
  tool content.
- Run the selected changed-document metadata, link, and Task-evidence checks.
- Obtain an independent privacy/security review before criterion acceptance.

## Risks and Recovery

### Risks and Rollback

- **Ambiguous provider view.** A menu may not expose effective memory state.
  Record it as unverified, leave criterion 3 pending, and do not explore hidden
  or mutating controls. The fixture probe then remains NOT_RUN.
- **Fixture side effect.** The one prompt may read and write only the exact
  ignored fixture after memory-off is proved. A changed fixture path, missing
  strict tool boundary, exceeded turn/cost limit, or incomplete cleanup stops
  the probe and keeps criteria 4 and 5 pending.
- **Sensitive output.** Stop before capture; retain no raw output and escalate
  the need for a redacted collection plan.
- **Session side effect.** The allowlist excludes actions with side effects.
  If an interface does not offer a safe view, stop the session and make no
  setting change.
- **Rollback.** This package changes no provider state. A documentation
  correction is a normal reviewed Git change; it does not alter any session.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-native-memory-controlled-verification.md)
