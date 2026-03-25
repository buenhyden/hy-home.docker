---
layer: agentic
title: 'Agentic Behavior Engineering Scope'
---

# Agentic Behavior Engineering Scope

**Protocols and instructions for AI agents to ensure predictable and high-quality autonomous work.**

## 1. Context & Objective

- **Goal**: Standardize how AI agents plan, execute, and communicate to minimize errors and maximize efficiency.
- **Standards**: Priority on JIT context loading, explicit reasoning, and `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements & Constraints

- **Thinking Process**: ALWAYS use `<thinking>` tags for planning and internal logic (Claude-specific).
- **Communication**: All user-facing interaction MUST be in **Korean**. Internal governance is in **English**.
- **Execution**: Use the `writing-plans` and `executing-plans` workflows for multi-step tasks.

## 3. Implementation Flow

1. **Context Discovery**: Start by reading the root shims (`AGENTS.md`) and identifying the target layer.
2. **Permission Check**: Verify tool availability and permission boundaries before execution.
3. **Step-by-Step**: Execute work in bite-sized, verifiable tasks.

## 4. Operational Procedures

- **Status Updates**: Provide regular task boundary updates and summaries.
- **Error Handling**: Stop and ask for clarification when hitting blockers or ambiguous requirements.

## 5. Maintenance & Safety

- **Self-Correction**: Proactively identify and fix formatting or linting issues in own output.
- **Human-in-the-Loop**: Request review for high-impact architectural changes or implementation plans.
