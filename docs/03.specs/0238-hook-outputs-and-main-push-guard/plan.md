---
title: "Hook Outputs and Main Push Guard Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0238-PLAN-0001"
parent_ids:
- "SPEC-0238"
created: "2026-10-13"
---

# Hook Outputs and Main Push Guard Plan

## Overview

Fix the hook outputs, align the Codex bindings, close the main-push routes an
agent can reach and add a push-time guard for the rest, then tighten the Claude
permissions the owner chose.

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

## Risks and Rollback

- **Fail-closed PreToolUse.** With `onFailure: block`, a hook slower than 30 s
  denies the tool, per the documentation; this is not observed. The timeout was raised from 10 s to 30 s for that reason.
- **Stricter reads.** Denying `.env` stops agents reading it through file
  tools and, per the documentation, the Bash file commands Claude Code
  recognizes; a key-only
  comparison then needs the owner's approval for that read.
- **Push-time guard.** It runs only after the owner installs it with
  `pre-commit install --hook-type pre-push`.
- **Rollback.** Revert the commits; no remote setting changes.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-hook-outputs-and-main-push-guard.md)
