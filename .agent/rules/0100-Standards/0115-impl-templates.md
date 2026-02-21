---
trigger: model_decision
glob: ["**/templates/project/*.md", "specs/**/plan.md", "specs/**/plan/**/*.md", "**/plan/**/*.md"]
description: "Implementation plan templates: provides canonical structures for stories, features, and epics to ensure data consistency and parseability."
---

# Implementation Plan Templates

- **Role**: Software Design Architect
- **Purpose**: Provide the canonical markdown structures for all levels of implementation planning.
- **Activates When**: Using or validating implementation plan templates in `specs/**/plan.md`, `**/plan/**/*.md`, or `templates/project/`.

**Trigger**: model_decision — Automatically apply these templates when creating new plan files.

## 1. Standards

### Principles

- **[REQ-IMPL_TPL-01] Structural Consistency**
  - All plans MUST adhere to the structural hierarchy defined in the templates.
- **[REQ-IMPL_TPL-02] No Placeholder Content**
  - Finalized plans MUST NOT contain template placeholders (e.g., `[TBD]`).

### Scope

- **In-Scope**: YAML front matter, header hierarchy, and mandatory sections for all plan types.
- **Out-of-Scope**: Logic specific to features or bug fixes.

### Outputs

- **Plan File**: A markdown file containing YAML front matter and structured implementation sections.

### Must

- **[REQ-IMPL_TPL-03] Front Matter Fields**
  - Every plan MUST include: `goal`, `version`, `date_created`, `last_updated`, `owner`, `status`, `tags`.
- **[REQ-IMPL_TPL-04] Verification Tables**
  - Task lists MUST use tables with: `Task`, `Description`, `Files Affected`, `Validation Criteria`.

### Must Not

- **[BAN-IMPL_TPL-01] Section Modification**
  - Level 1 headers defined in the canonical templates MUST NOT be renamed or omitted.

### Failure Handling

- **Stop Condition**: Stop processing if a plan is missing mandatory sections.
- **Resolution**: Prompt to re-generate the plan using the correct template.

### Style

- Use standard Github Flavored Markdown.

## 2. Procedures

- **[PROC-IMPL_TPL-01] Template Selection**
  - Choose the template (Story/Feature/Epic) based on the estimated scope and points.

## 3. Examples

### Standard Task Table

| Task | Description | Files Affected | Validation Criteria |
| --- | --- | --- | --- |
| TASK-001 | Init auth | `auth.ts` | No build errors |

## 4. Validation Criteria

- **[VAL-IMPL_TPL-01] Mandatory Headers**
  - [ ] Introduction, Requirements & Constraints, Implementation Steps exist.
- **[VAL-IMPL_TPL-02] Front Matter Schema**
  - [ ] All mandatory YAML keys are present and correctly typed.
