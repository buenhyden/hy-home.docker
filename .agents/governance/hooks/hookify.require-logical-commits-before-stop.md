---
title: "BLOCKED: incomplete logical commits"
version: "1.0.5"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-03"
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

Applies to the `require-logical-commits-before-stop` rule on the `stop` event. The frontmatter of this document owns the exact matcher.

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

The declared `stop` event and `pattern` define the matching scope; native event delivery remains a separate observation.

## Related Documents

- `.agents/README.md`
