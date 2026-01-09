---
trigger: always_on
glob: "**/*"
description: "Create Command: Guidelines for creating new Agent/CLI commands."
---
# Create Command Standard

## 1. Purpose

- **Goal**: Automate repetitive tasks via slash commands or CLI tools.
- **Categories**: Planning, Implementation, Analysis, Testing, Docs, Workflow.

## 2. Structure

- **Name**: Action-oriented, concise (e.g., `/bug-fix`, `/review`).
- **Description**: Single line summary.
- **Usage**: Arguments and examples.
- **Process**: Step-by-step logic the agent should follow.

## 3. Best Practices

- **Examples**: Provide concrete examples of input/output.
- **Robustness**: Handle missing arguments gracefully.
- **Efficiency**: Minimize round-trips; maximize context usage.
