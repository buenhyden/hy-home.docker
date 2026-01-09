---
trigger: always_on
glob: "**/*"
description: "CLI Command Standards: Guidelines for creating custom agent commands."
---
# CLI Command Standards

## 1. Structure

- **Category**: Classify as `Planning`, `Implementation`, `Analysis`, `Testing`, or `Utility`.
- **Location**: Store in `.claude/commands/` or project equivalent.
- **Sections**: Include Title, Description, Usage, Process, Examples.

## 2. Design

- **Focused**: Single-purpose commands are better than monolithic ones.
- **Validation**: Always validate inputs and provide help text.

### Example: Command Template

#### Good

```markdown
# Generate Component

Creates a new UI component.

## Usage
`/gen-component <name>`

## Process
1. Create file.
2. Add boilerplate.
```
