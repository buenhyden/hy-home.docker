---
trigger: model_decision
glob: [".agent/workflows/**/*.md", "**/*workflow*"]
description: "Workflows Pillar Standards: Enforces declarative structure, Turbofan execution, and re-runnable (idempotent) automation steps."
---

# Workflows Pillar Standards

- **Role**: Workflow Governance Architect
- **Purpose**: Define standards for the creation, organization, and execution of automated agent workflows, ensuring they are reproducible, safe, and transparent.
- **Activates When**: Creating or modifying `.md` workflow files in the `.agent/workflows/` directory or executing automated task sequences.

**Trigger**: model_decision — Apply during all phases of workflow design and execution.

## 1. Standards

### Principles

- **[REQ-WKP-01] Declarative Location Identity**
  - All agent workflows MUST reside within the `.agent/workflows/` directory to ensure discoverability and governance.
- **[REQ-WKP-02] Transparent Step Logic**
  - Workflow steps MUST be numbered, actionable, and explicitly defined with clear prerequisite context for the agent.
- **[REQ-WKP-03] Idempotent Execution Path**
  - Workflows SHOULD be designed for re-runnability. Intermediate state checks MUST be implemented to ensure the workflow can be resumed or restarted without corruption.

### Workflow Execution Matrix

| Attribute | Requirement ID | Critical Control |
| --- | --- | --- |
| Metadata | [REQ-WKP-04] | Mandatory Frontmatter with `description` |
| Safety | [REQ-WKP-05] | `// turbo` for non-destructive commands |
| Sequence | [REQ-WKP-06] | Ordered numerical stepping (1, 2, 3...) |
| Visibility | [REQ-WKP-07] | Concise summary of each step's outcome |

### Must

- **[REQ-WKP-08] Mandatory Turbo Annotation**
  - Utilize the `// turbo` (or `// turbo-all`) annotation exclusively for commands that have been verified as safe to run without user approval.
- **[REQ-WKP-09] Explicit Post-Step Verification**
  - Critical workflow steps MUST include a verification action (e.g., `ls`, `grep`) to confirm the successful transition to the next state.
- **[REQ-WKP-10] Atomic Command Granularity**
  - Each workflow step SHOULD contain a single logical command to maintain high observability and failure granularity.

### Must Not

- **[BAN-WKP-01] Opaque Logic Bundling**
  - DO NOT bundle multiple complex operations into a single workflow step without clear, intermediate verification points.
- **[BAN-WKP-02] Hardcoded Path Dependencies**
  - Avoid hardcoding absolute local paths inside workflow commands; utilize project-relative paths or environment variables.

### Failure Handling

- **Stop Condition**: Stop workflow execution if a step identifies an unexpected state that makes subsequent re-runnable steps invalid or dangerous.

## 2. Procedures

- **[PROC-WKP-01] Safe-to-Run Audit**
  - IF a command is identified as having potential side-effects THEN MUST NOT utilize the `// turbo` annotation; user approval is mandatory.
- **[PROC-WKP-02] Lineage Impact review**
  - Upon completion of a workflow, conduct a manual verification of the workspace state to confirm alignment with the workflow's intended goal.

## 3. Examples

### Standard Workflow Template (Good)

```markdown
---
description: "Build and Test Asset"
---
1. Check for directory existence
// turbo
2. Run `npm run build`
```

## 4. Validation Criteria

- **[VAL-WKP-01] Frontmatter Compliance**
  - [ ] Verification confirms that 100% of files in `.agent/workflows/` possess the required YAML frontmatter.
- **[VAL-WKP-02] Idempotency Pass**
  - [ ] Manual verification confirms that the workflow can be restarted after a simulated failure in step 2 without duplicate side-effects.
- **[VAL-WKP-03] Turbo Integrity**
  - [ ] Audit confirms that no commands with destructive side-effects (e.g., `rm -rf /`) are marked with `// turbo`.
