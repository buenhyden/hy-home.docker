---
trigger: always_on
glob: "**/*.md"
description: "Core Documentation Standard: Master index for Diátaxis framework, technical writing, and lifecycle management."
---

# Core Documentation Standard

- **Role**: Knowledge Architect
- **Purpose**: Provide a master authority and index for all documentation-related standards within the workspace.
- **Activates When**: Writing, updating, or auditing project documentation, READMEs, or LLM-facing metadata.

**Trigger**: always_on — Apply as the primary standard for knowledge management.

## 1. Standards

### Principles

- **[REQ-DOC_CORE-01] Authoritative Threading**
  - This rule MUST serve as the master index. All specific documentation sub-domains (Technical Writing, Formatting) MUST be linked here.
- **[REQ-DOC_CORE-02] Intentful Structure**
  - Documentation MUST adhere to the Diátaxis mode (Tutorial vs Reference) as defined in the master content standard.
- **[REQ-DOC_CORE-03] Self-Documenting Repository**
  - The repository root MUST contain an `llms.txt` file and a primary `README.md` that serves as a functional entry point.

### Domain Index

| Domain | Requirement ID | Authority File |
| --- | --- | --- |
| Content & Mode | [REQ-DOC_CORE-04] | `0160-documentation-standards.md` |
| Technical Writing | [REQ-DOC_CORE-05] | `2102-doc-technical.md` |
| Formatting Rules | [REQ-DOC_CORE-06] | `2103-doc-formatting.md` |
| Lifecycle Mgmt | [REQ-DOC_CORE-07] | `2104-doc-lifecycle.md` |

### Must

- **[REQ-DOC_CORE-08] Standard README Header**
  - Every `README.md` MUST include standard metadata Badges (Build, Version) and a concise one-line value proposition.
- **[REQ-DOC_CORE-09] GFM Compliance**
  - All markdown content MUST follow GitHub Flavored Markdown (GFM) and utilize standard alerts (e.g., `[!NOTE]`).
- **[REQ-DOC_CORE-10] Truth Verification**
  - Documentation MUST NOT describe features or implementation details that are not currently present in the codebase.

### Must Not

- **[BAN-DOC_CORE-01] Cross-Repository Duplication**
  - Standards MUST NOT be duplicated across directories; reference the authoritative file via relative markdown links.
- **[BAN-DOC_CORE-02] Placeholder Documentation**
  - Internal links to "Coming Soon" or non-existent files are PROHIBITED in the production documentation set.

### Failure Handling

- **Stop Condition**: Stop documentation updates if the generated `llms.txt` index contains broken relative links.

## 2. Procedures

- **[PROC-DOC_CORE-01] Standards Extraction**
  - IF starting a new project THEN MUST run the standards extraction workflow to define naming and formatting conventions.
- **[PROC-DOC_CORE-02] Quality Review**
  - Perform a self-verification check against the "Documentation Quality Checklist" for every document PR.

## 3. Examples

### Standard README Header

```markdown
# Project Name
![Build](badge_url) ![Version](badge_url)
> Concise description of the project's purpose.
```

## 4. Validation Criteria

- **[VAL-DOC_CORE-01] Index Integrity**
  - [ ] All relative links in this index point to valid, existing rule files.
- **[VAL-DOC_CORE-02] Format Adherence**
  - [ ] All `.md` files in the repository pass the internal markdown-lint checks.
- **[VAL-DOC_CORE-03] Truth Audit**
  - [ ] Manual review confirms that documented "Quick Start" commands work as intended.
