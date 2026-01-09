---
trigger: always_on
glob: "**/*"
description: "Multi-Agent Coordination: Standards for Planner-Executor roles and task breakdown."
---
# Multi-Agent Coordination Standards

## 1. Roles

- **Planner**: High-level reasoning, strategy, breaking down complex user requests into steps.
- **Executor**: Detailed implementation, coding, running commands.
- **Reviewer**: Critiques output against requirements (optional, can be Planner/User).

## 2. Communication

- **Structured**: Use defined formats (JSON, Markdown checklists) to pass state.
- **Clear Handoffs**: Explicitly state "Task X is complete. Proceeding to Task Y."

## 3. Task Breakdown

- **Granularity**: Break tasks into steps that fit within a single context window or agent turn.
- **Dependencies**: Identify blockers. "Step B cannot start until Step A is verified."
- **TODOs**: Convert vague `TODO` comments into concrete task items in a tracking file (e.g., `task.md`).

## 4. Error Handling

- **Stuck State**: If an agent is stuck (e.g., command failing loop), it must stop and ask for help/clarification rather than retrying indefinitely.
- **Context Loss**: Summarize state frequently to prevent context drift in long conversations.

### Example: Coordination

#### Good

```typescript
// PLANNER: Identify dependencies for user auth
// EXECUTOR: Implement login function using identified deps
```
