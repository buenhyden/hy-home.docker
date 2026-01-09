---
description: Standard workflow for reviewing Pull Requests
---

# Pull Request Review Workflow

Based on `017-core-pull-request-review-specific.md` and `011-core-code-review-specific.md`.

1. **Requirements Check (50%)**
   - Does code meet issue requirements?
   - Are acceptance criteria met?

2. **Standards Check (30%)**
   - Code Style & Naming (`005-core-naming-specific.md`).
   - Patterns (Framework specific rules).

3. **Security Check (20%)**
   - SQL Injection check.
   - XSS check.
   - Auth/Permissions check.
   - Secrets check.

4. **Feedback**
   - Use `[NIT]`, `[BLOCKER]`, `[SUGGESTION]` prefixes.
   - Approve if Score >= 80% and no Security Blockers.
