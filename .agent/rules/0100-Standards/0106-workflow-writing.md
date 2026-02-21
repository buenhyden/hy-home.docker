---
trigger: model_decision
glob: [".agent/workflows/**/*.md", ".agent/workflows/**/*.md"]
description: "Workflow Writing Standards: Master authority for creating deterministic, repeatable, and safe automation workflows."
---

# Workflow Writing Standards

- **Role**: Automation Workflow Architect
- **Purpose**: Define deterministic standards for creating and managing Workflows as repeatable execution scripts.
- **Activates When**: Creating or modifying any Workflow stored under workspace workflow stores.

**Trigger**: model_decision — Apply this standard whenever a Workflow is created or changed.

## 1. Standards

### Principles

- **[REQ-WF-01] Scripted Determinism**
  - Workflows MUST be repeatable execution scripts with ordered, numbered steps.
- **[REQ-WF-02] Safety Gating**
  - Each Workflow MUST declare exactly one safety level (Level 1: Read-only, Level 2: Plan-first, Level 3: Manual review).
- **[REQ-WF-03] Modular Composition**
  - Workflows MUST be composable, using explicit chaining syntax: `Call /<workflow-name> with <context>`.

### Safety Levels

| Level | Permission | Action Required |
| --- | --- | --- |
| Level 1 | Read-Only | None (Safe to auto-run with `// turbo`) |
| Level 2 | Destructive | Mandatory Plan-First Checkpoint |
| Level 3 | High Risk | Mandatory Manual Review |

### Must

- **[REQ-WF-04] Mandatory Sections**
  - Every Workflow MUST include: Goal, Scope, Steps, Quality Checks, and Completion Criteria.
- **[REQ-WF-05] Targeted Steps**
  - Every step MUST explicitly name a target (file, directory, or command).
- **[REQ-WF-06] Turbo Protocol**
  - `// turbo` MUST only be used in Level 1 (Read-Only) workflows.

### Must Not

- **[BAN-WF-01] Vague Instructions**
  - Steps MUST NOT use ambiguous phrases like "as appropriate" or "be careful".
- **[BAN-WF-02] Hidden Dependencies**
  - Workflows MUST NOT depend on other scripts without an explicit call step.

### Failure Handling

- **Stop Condition**: Subsequent modifying steps MUST stop if a prior step fails a quality check.

## 2. Procedures

- **[PROC-WF-01] Workflow Creation**
  - IF creating a new workflow THEN MUST use the kebab-case naming convention and store in a designated store.
- **[PROC-WF-02] Level Classification**
  - IF a workflow contains destructive commands (e.g., `rm`, `git push`) THEN Safety Level MUST be Level 2 or 3.

## 3. Examples

### Standard Level 1 Step

1. // turbo
   git status

### Workflow Call

1. Call /generate-manifest with context="production"

## 4. Validation Criteria

- **[VAL-WF-01] Safety Declaration**
  - [ ] Exactly one Safety Level is documented in the workflow.
- **[VAL-WF-02] Structural Integrity**
  - [ ] All mandatory sections (Goal/Scope/Steps/QC) are present.
- **[VAL-WF-03] Turbo Compliance**
  - [ ] `// turbo` is NOT used on destructive commands.
