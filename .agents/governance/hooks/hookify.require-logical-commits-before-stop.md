---
title: "BLOCKED: incomplete logical commits"
version: "1.0.7"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
action: "block"
enabled: true
event: "stop"
name: "require-logical-commits-before-stop"
pattern: ".*"
---

# BLOCKED: incomplete logical commits

## Overview

Apply the declared `block` action for require-logical-commits-before-stop.

## Scope

The `require-logical-commits-before-stop` rule applies on the `stop` event and matches the end of an agent turn, ("BLOCKED: incomplete logical commits"). The frontmatter owns the exact matcher.

## Rules

**Logical commit completion check**

Before the final response for completed repository-modifying work:

- Inspect `git status --short` and the relevant diffs.
- Stage only files or hunks that belong to the current task.
- Create small Conventional Commits by logical unit after required checks pass.
- Leave unrelated untracked files untouched.
- If commits are intentionally skipped, state the reason clearly.

The shared Stop hook conservatively blocks on Git-visible uncommitted
changes. Git status does not establish which task or person owns a path,
nor does it grant permission to stage or commit it. Inspect ownership and
scope before acting, preserve unrelated changes, and use the applicable
incomplete-handoff route if completion cannot be established. The gate
does not replace review of the staged diff or waive required checks.

A repeated Stop payload (`stop_hook_active: true`) returns without another
block or verification run. The first attempt retains the uncommitted-change
check; a retry does not certify completion.

## Exceptions

No exception is declared by this rule.

## Verification

`scripts/hooks/hook_rules.py` does not evaluate `event: stop` rules; their `pattern: .*` is a placeholder. The enforcing code is `logical_commit_stop_gate` in `scripts/hooks/agent-event-hook.sh`. Native event delivery remains a separate observation.

## Related Documents

- `.agents/README.md`
