---
trigger: always_on (when creating commands)
glob: "**/*"
description: "CLI/Slash Command Standards: Guidelines for creating custom agent commands."
---
# CLI & Command Creation Standards

## 1. Purpose & Categories

- **Goal**: Automate repetitive tasks via slash commands or CLI tools.
- **Categories**: `Planning`, `Implementation`, `Analysis`, `Testing`, `Docs`, `Utility`.

## 2. Structure & Design

- **Name**: Action-oriented, concise (e.g., `/bug-fix`, `/review`).
- **Location**: Store in `.agent/commands/` or `.claude/commands/`.
- **Focused**: Single-purpose commands are better than monolithic ones.
- **Validation**: Always validate inputs and provide help text.

## 3. Command Template

### Example: Good Structure

```markdown
# Generate Component

Creates a new UI component.

## Usage
`/gen-component <name>`

## Process
1. Validate input name.
2. Create component file.
3. Add boilerplate code.
4. Verify file existence.
```

## See Also

- [035-core-workflow-slash-commands.md](./035-core-workflow-slash-commands.md) - Workflow patterns
