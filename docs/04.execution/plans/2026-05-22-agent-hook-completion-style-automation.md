---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-22-agent-hook-completion-style-automation.md -->

# Agent Hook Completion and Style Automation Plan

> Bounded plan for strengthening logical commit completion, code style validation, and post-edit formatting hooks.

## Overview

This document is the completion plan for strengthening hook and Hookify guidance so AI Agents leave logical-unit commits when finishing repository-modifying work and run automatic formatting plus code-style validation after file edits.

## Context

The existing hook surface ran basic post-edit formatting and repository validators, but logical commit guidance was closer to a reminder. This change blocks completion at Stop when task-owned changes remain and adds shell/YAML style validation to the post-edit path.

## Goals & In-Scope

- **Goals**:
  - `G-HOOK-AUTO-001`: Stop hook detects task-owned uncommitted changes and requires logical commit completion.
  - `G-HOOK-AUTO-002`: PostToolUse hook performs style validation for changed shell/YAML files.
  - `G-HOOK-AUTO-003`: Document the safe default formatting contract after file edits in provider docs and Hookify rules.
- **In Scope**:
  - `scripts/hooks/agent-event-hook.sh`
  - `scripts/hooks/post-tool-validate.sh`
  - `.claude/hookify.*.local.md`
  - provider docs and `.codex/README.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not run automatic commits inside hook scripts.
  - Do not automate `--no-verify`, force push, rebase, or reset.
  - Do not modify user-global Claude/Codex settings.
- **Out of Scope**:
  - deployment, Docker runtime mutation, secret values, shell history, or personal settings
  - unrelated untracked `projects/storybook/mcp/`

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-HOOK-AUTO-001 | Add Stop gate for uncommitted task-owned changes | `scripts/hooks/agent-event-hook.sh` | G-HOOK-AUTO-001 | Stop smoke blocks owned changes and ignores `projects/storybook/mcp/` |
| PLN-HOOK-AUTO-002 | Add changed-file style validation | `scripts/hooks/post-tool-validate.sh` | G-HOOK-AUTO-002 | Bash syntax passes; optional `shellcheck`/`yamllint` run when available |
| PLN-HOOK-AUTO-003 | Update Hookify rules and provider docs | `.claude/hookify.*.local.md`, provider docs, `.codex/README.md` | G-HOOK-AUTO-003 | docs describe commit, formatting, and style behavior |
| PLN-HOOK-AUTO-004 | Record task evidence and validate | task doc and validators | all | repository checks pass |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-HOOK-AUTO-001 | Syntax | Check hook shell syntax | `bash -n scripts/hooks/agent-event-hook.sh scripts/hooks/post-tool-validate.sh .claude/hooks/*.sh` | no syntax errors |
| VAL-HOOK-AUTO-002 | JSON | Check hook config JSON | `python3 -m json.tool .claude/settings.json`; `python3 -m json.tool .codex/hooks.json` | JSON parses |
| VAL-HOOK-AUTO-003 | Stop Smoke | Simulate Stop with owned changes and unrelated Storybook MCP left untouched | `printf ... \| bash scripts/hooks/agent-event-hook.sh Stop` | hook blocks owned changes before commit; does not list `projects/storybook/mcp/` |
| VAL-HOOK-AUTO-004 | Post-edit Smoke | Simulate PostToolUse payload for changed hook/script files | `printf ... \| bash scripts/hooks/agent-event-hook.sh PostToolUse` | post-edit script exits successfully or reports concrete style failure |
| VAL-HOOK-AUTO-005 | Repository Contracts | Run repository docs/governance validators | `bash scripts/validation/check-repo-contracts.sh`; `bash scripts/validation/check-doc-traceability.sh` | failures=0 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Stop hook blocks intentional incomplete handoff | Medium | Provide explicit `AGENT_ALLOW_UNCOMMITTED_STOP=1` override with reason requirement |
| Style tools unavailable in a sandbox | Low | Run `shellcheck` and `yamllint` only when the command exists |
| Hook script performs unwanted commits | High | Keep commit action agent-driven; hook only blocks/reminds |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: syntax, JSON, Stop smoke, post-edit smoke, and repository validators pass.
- **Sandbox / Canary Rollout**: local hook simulations only.
- **Human Approval Gate**: user explicitly requested hook and Hookify improvements.
- **Rollback Trigger**: Stop hook blocks unrelated untracked Storybook MCP path or post-edit validation fails on unchanged files.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] Logical commit Stop gate implemented.
- [x] Code style validation added to post-edit validation path.
- [x] File edit formatting behavior documented.
- [x] Hookify and provider docs updated.
- [x] Verification evidence recorded in the task document.

## Related Documents

- **Task**: [Agent hook completion and style automation task](../tasks/2026-05-22-agent-hook-completion-style-automation.md)
- **Claude Provider Notes**: [Claude provider notes](../../00.agent-governance/providers/claude.md)
- **Codex Provider Notes**: [Codex provider notes](../../00.agent-governance/providers/codex.md)
- **Codex Runtime README**: [Codex runtime README](../../../.codex/README.md)
- **Hook Dispatcher**: [Agent event hook](../../../scripts/hooks/agent-event-hook.sh)
- **Post Tool Validation**: [Post tool validation](../../../scripts/hooks/post-tool-validate.sh)
