---
trigger: model_decision
glob: [".agent/workflows/*.md", "agents_settings/agent/workflows/*.md"]
description: "Workflow Standards: Guidelines for creating Agent Workflows and using Workflow Commands."
---

# 0860-Documentation-Workflow

- **Role**: Workflow Designer
- **Purpose**: standardized structure for Agent Workflows to ensure consistent execution.
- **Activates When**: Creating or editing `.agent/workflows/*.md` files.

## 1. Standards

### 1.1 Principles

- **[REQ-WKF-GEN-01] Sequential**: Steps MUST be ordered logically (1, 2, 3).
- **[REQ-WKF-GEN-02] Imperative**: Steps MUST use action verbs ("Run", "Create").
- **[REQ-WKF-GEN-03] Atomic**: Each step MUST be a distinct, verifiable action.

### 1.2 Scope

- **In-Scope**: Agent Workflows (`.md`), Workflow Slash Commands.
- **Out-of-Scope**: Task Rules (see 0010), Agent Skills (see 0870).

### 1.3 Inputs & Outputs

- **Inputs**: User intent, Repetitive task pattern.
- **Outputs**: Executable Markdown Workflow.

### 1.4 Must / Must Not

- **[REQ-WKF-STR-01] Header**: Workflows MUST include a description and `### Steps` section.
- **[BAN-WKF-CMP-01] No Ambiguity**: Steps MUST NOT be vague ("Make it look good").
- **[REQ-WKF-CMD-01] Slash Invocation**: Workflows MUST be invokable via `/[name]`.

## 2. Procedures

### 2.1 Creation

1. **Define**: What is the goal? (e.g., "Deploy to Staging").
2. **Draft**: List steps manually.
3. **Format**: Apply markdown structure.
4. **Test**: Run with Agent to verify behavior.

## 3. Examples

### 3.1 Standard Workflow

```markdown
---
description: Deploys the application to staging.
---

### Steps

1. Run `npm run test` to verify build.
2. Run `npm run build`.
3. Execute `deploy-script.sh staging`.
4. Verify HTTP 200 on staging URL.
```

## 4. Validation Criteria

- [ ] **[VAL-WKF-STR-01]** File is in `.agent/workflows/`.
- [ ] **[VAL-WKF-STR-02]** Contains `### Steps`.
- [ ] **[VAL-WKF-ACT-01]** Steps are numbered and imperative.

## 5. References

- Reference: [0003-core-task-workflow-standards.md](../0100-Standards/0003-core-task-workflow-standards.md)
