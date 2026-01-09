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

- **Correctness**: Does it meet the requirements? Are there edge cases?
- **Readability**: Is the intent clear? Are naming conventions followed (see `005`)?
- **Performance**:
  - Are there N+1 query issues?
  - Are there unnecessary loops or heavy computations in the critical path?
  - Are large datasets paginated?
- **Security**:
  - Are inputs validated/sanitized?
  - Are secrets exposed?
  - Is authorization checked (IDOR)?
- **Testability**: Are there tests coverage new logic? Are the tests brittle?

### Example: Performance Feedback

**Good**
> "I see we are fetching user details inside the order loop. This might cause an N+1 problem. Can we prefetch users via `repository.getUsersByIds()`?"

**Bad**
> "This is slow. Fix it."

## 3. Feedback Types

- **Nitpick**: Personal preference or minor style issue. Optional to fix. (Prefix with `[NIT]`).
- **Suggestion**: A recommendation for improvement, but not critical.
- **Blocker**: A critical bug, security flaw, or architectural violation. Must be fixed before merge.

### Example: Feedback Categorization

**Good**
> "[NIT]: Extra whitespace here."
> "[BLOCKER]: This SQL query is vulnerable to injection. We must use parameters."

## 4. Automation First

- **Let Bots Complain**: Use linters/formatters for style. Humans should review logic/architecture.
- **CI Required**: Do not review broken builds. Push fixes first.
