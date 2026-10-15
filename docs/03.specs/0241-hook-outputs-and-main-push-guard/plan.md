---
title: "Hook Outputs and Main Push Guard Plan"
version: "0.1.2"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-15"
layer: "specs"
artifact_id: "SPEC-0241-PLAN-0001"
parent_ids:
- "SPEC-0241"
created: "2026-10-13"
---

# Hook Outputs and Main Push Guard Plan

## Overview

Fix the hook outputs, align the Codex bindings, close the main-push routes an
agent can reach and add a push-time guard for the rest, then tighten the Claude
permissions the owner chose.

## Scope

W1–W4 align provider hook outputs/bindings, main-push denial and protected
read settings; W5 validates and reviews that source. The later installed-hook
and protection observations remain in the Task, while r10 push-stage repair
belongs to SPEC-0212 W20; global provider settings and unchosen denials are
excluded.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | PreCompact, SessionStart and PreToolUse outputs | None | TSK-0001 | Task evidence |
| W2 | 2 | Codex hook bindings, sandbox and memory notes, Storybook guide | None | TSK-0001 | Task evidence |
| W3 | 3 | Main-push rule, implicit-target check, pre-push guard, protection record | None | TSK-0001 | Task evidence |
| W4 | 4 | Settings permissions and PreToolUse fail-closed | W3 | TSK-0001 | Task evidence |
| W5 | 5, 6 | Checks, review and candidate | W1, W2, W3, W4 | TSK-0001 | Task evidence |

## Verification Plan

New tests in `tests/validation/test_agent_governance_ci_routing.py` run against
`main` first and then the branch; the routing suite, hook tests, renderer
check, governance contract, script manifest, workflow contract, shellcheck,
changed metadata, corpus lifecycle, links, markdownlint, an independent review
and the hosted candidate.

## Risks and Recovery

### Risks and Rollback

- **Fail-closed PreToolUse.** With `onFailure: block`, a hook slower than 30 s
  denies the tool, per the documentation; this is not observed. The timeout was raised from 10 s to 30 s for that reason.
- **Stricter reads.** Denying `.env` stops agents reading it through file
  tools and, per the documentation, the Bash file commands Claude Code
  recognizes; a key-only
  comparison then needs the owner's approval for that read.
- **Push-time guard.** The Task records installation on 2026-10-14 with
  `pre-commit install --hook-type pre-push` (alongside the other hook types).
  A blocked push through that installed hook has not been observed. Static
  guard tests and installation do not establish that live observation.
- **Rollback.** Reverting tracked source affects the implementation only.
  The later installed hooks and remote `enforce_admins` change recorded by the
  Task have their own target and authorization boundary; this source Plan
  does not authorize changing them.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-hook-outputs-and-main-push-guard.md)
