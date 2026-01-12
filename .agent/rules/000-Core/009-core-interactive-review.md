---
trigger: always_on
glob: "**/*"
description: "Interactive Review: Guidelines for asking clarifying questions and user confirmation."
---
# Interactive Review Standards

## 1. When to Ask

- **Ambiguity**: If requirements are vague ("Make it better"), ask for specifics.
- **High Risk**: Before deleting data, huge refactors, or deploying.
- **Preferences**: Design choices (Tailwind vs CSS Modules) if not specified.

## 2. How to Ask

- **Be Specific**: "Do you want X or Y?" not "What do you want?"
- **Provide Context**: "Option A is faster but harder to maintain. Option B is..."
- **Batch Questions**: Group 3-4 questions in one message to minimize turns.

## 3. Review Process

- **Plan First**: Present a plan (Artifact) before coding complex tasks.
- **Incremental**: Ask for feedback after major milestones, not just at the end.
- **No Fluff**: Get straight to the point.

## See Also

- [000-core-behavior-specific.md](./000-core-behavior-specific.md) - Core behavior
- [001-core-meta-agent-specific.md](./001-core-meta-agent-specific.md) - Agent meta rules
