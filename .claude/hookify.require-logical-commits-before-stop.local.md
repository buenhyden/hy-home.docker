---
name: require-logical-commits-before-stop
enabled: true
event: stop
pattern: .*
action: block
---

**Logical commit completion check**

Before the final response for completed repository-modifying work:

- Inspect `git status --short` and the relevant diffs.
- Stage only files or hunks that belong to the current task.
- Create small Conventional Commits by logical unit after required checks pass.
- Leave unrelated untracked files untouched.
- If commits are intentionally skipped, state the reason clearly.

The shared Stop hook blocks when task-owned repository changes remain
uncommitted. Use this as a completion gate, not as a substitute for reviewing
the staged diff.
