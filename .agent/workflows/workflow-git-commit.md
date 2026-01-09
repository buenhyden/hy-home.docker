---
description: Standard workflow for git commits
---

# Git Commit Workflow

Based on `010-core-git-specific.md` and `035-core-workflow-slash-commands.md`.

1. **Check Status**

   ```bash
   git status
   ```

2. **Analyze Changes**
   - Review file diffs.
   - Identify the scope (feat, fix, docs, style, refactor, perf, test, chore).

3. **Generate Message**
   - Format: `type(scope): description`
   - Example: `feat(auth): add login endpoint validation`

4. **Commit**

   ```bash
   git add .
   git commit -m "type(scope): description"
   ```
