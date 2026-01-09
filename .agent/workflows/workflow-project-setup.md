---
description: Standard workflow for project setup and context understanding
---

# Project Setup Workflow

Based on `003-core-context-prime-specific.md`.

1. **Read README**
   - Understand project goals and architecture.

2. **Check AI Guidelines**
   - Look for `.agent/rules`, `CLAUDE.md`, `.cursorrules`.

3. **Analyze Structure**

   ```bash
   git ls-files | head -50
   ```

4. **Identify Dependencies**
   - Check `package.json`, `pyproject.toml`, `Cargo.toml`.

5. **Identify Test Framework**
   - Look for `pytest`, `jest`, `vitest` configuration.

6. **Output**
   - Document project constraints and architecture understanding.
