---
trigger: always_on
glob: ".agent/rules/*.md"
description: "AI Agent Rules Meta Guide: Standards for creating and maintaining AI coding rules."
---
# AI Agent Rules Standards

## 1. Rule Structure

All AI agent rules must follow this exact Markdown structure to ensure consistent parsing and application.

- **File Format**: Markdown (`.md`).
- **Naming Convention**: `XXX-category-subcategory-topic-specific.md` (e.g., `211-backend-python-fastapi-specific.md`).

### Frontmatter

Must include valid YAML frontmatter:

- `trigger`: When to apply the rule (e.g., `always_on`).
- `glob`: File patterns to match (e.g., `**/*.py`).
- `description`: A clear, one-line summary.

```yaml
---
trigger: always_on
glob: "**/*.ts"
description: "TypeScript Best Practices: Typing and interfaces."
---
```

## 2. Content Guidelines

### Sections

Use clear, numbered headers for major topics.

```markdown
## 1. Topic Name
```

### Directives

- **Be Declarative**: Use strong verbs ("Use", "Avoid", "Prefer").
- **Be Specific**: Avoid vague advice like "Make it clean." explain *how*.
- **Bold Key Points**: Use bold text for the main directive.

### Examples

Always provide **Good** and **Bad** examples. You may use headers or in-code comments with emojis (`✅ DO`, `❌ DON'T`).

#### Good

```typescript
interface User {
  id: string;
  name: string;
}
```

#### Bad

```typescript
// ❌ DON'T: Don't use 'any'
function process(user: any) { ... }
```

## 3. Best Practices

- **Actionable**: Rules must be specific and actionable, avoiding vague philosophies.
- **DRY**: Reference other rules or documentation instead of duplicating content.
- **Atomic**: Each rule should focus on a single concept or technology.

## 4. File References

- **Syntax**: Use standard Markdown links `[filename](./path/to/file)` to reference other files contextually.
- **Cross-Referencing**: Link to related rules to build a knowledge graph.

## 5. Maintenance

- **Conflicts**: Ensure new rules do not contradict existing specific rules.

## 6. Continuous Improvement

### Triggers for Updates

- **New Patterns**: If a pattern appears in 3+ files, create a rule.
- **Recurring Bugs**: If a bug type repeats, create a preventative rule.
- **Security/Perf**: New frameworks or vulnerabilities require immediate updates.

### Evolution Workflow

1. **Collection**: Note repeated manual corrections during dev.
2. **Analysis**: Assess impact (time saved vs. maintenance cost).
3. **Documentation**: Draft > Verify > Publish > Monitor.
