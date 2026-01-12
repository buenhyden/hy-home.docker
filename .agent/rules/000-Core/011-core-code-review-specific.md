---
trigger: always_on
glob: "**/*"
description: "Code Review: Checklists, Feedback Tone, Performance Audits, and Blocking Criteria."
---
# Code Review Standards

## 1. Review Philosophy

- **Objective**: Improve code quality, share knowledge, and ensure maintainability.
- **Tone**: Be constructive. Critique the code, not the author. Ask questions ("Why did we choose X?") instead of making demands ("Change X").
- **Speed**: Prioritize reviews. A blocked PR halts the team.

## 2. Review Checklist (The "What")

- **Requirements (50%)**: Does code meet issue requirements/AC?
- **Standards (30%)**: Code style, security, naming conventions (see 05), and specific stack patterns.
- **Security (20%)**:
  - **SQL**: Parametrized queries ONLY.
  - **XSS**: Sanitization (Html::escape, {{ }}).
  - **Permissions**: Proper access control (IDOR).
  - **Secrets**: No hardcoded keys.
- **Performance**:
  - N+1 query issues?
  - Unnecessary loops or heavy computations in critical paths?
  - Pagination for large datasets?
- **Testability**: Coverage of new logic? Brittle tests?

### Example: Performance Feedback

**Good**
> "I see we are fetching user details inside the order loop. This might cause an N+1 problem. Can we prefetch users via 
epository.getUsersByIds()?"

**Bad**
> "This is slow. Fix it."

## 3. Feedback Types & Labeling

- **Nitpick**: Personal preference or minor style issue. Optional to fix. (Prefix with [NIT]).
- **Suggestion**: A recommendation for improvement, but not critical.
- **Blocker**: A critical bug, security flaw, or architectural violation. Must be fixed before merge.

### Agent Scoring Logic
- **Scores**:
  - ≥ 80%: code-review-approved (Green)
  - < 80%: code-review-changes (Orange)
  - Security Issues: code-review-security (Red)
- **Status**: 
equirements-met vs 
equirements-gap.

### Example: Feedback Categorization

**Good**
> "[NIT]: Extra whitespace here."
> "[BLOCKER]: This SQL query is vulnerable to injection. We must use parameters."

## 4. Automation First

- **Let Bots Complain**: Use linters/formatters for style. Humans should review logic/architecture.
- **CI Required**: Do not review broken builds. Push fixes first.

## 5. Output Format (Agent)

- **Line Comments**: Use GitHub Review API for specific feedback.
- **Freshdesk**: Update ticket with structured HTML summary (Score, findings, status).


## See Also

- [010-core-git-specific.md](./010-core-git-specific.md) - Git standards and commit patterns
- [012-core-pr-template-specific.md](./012-core-pr-template-specific.md) - PR template structure
- [005-core-naming-specific.md](./005-core-naming-specific.md) - Naming conventions for review
