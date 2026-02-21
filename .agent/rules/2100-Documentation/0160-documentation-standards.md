---
trigger: model_decision
glob: ["**/*.md", "**/README.md", "CHANGELOG.md"]
description: "Documentation Standards: Enforces Diátaxis framework, technical writing precision, and lifecycle management."
---

# Documentation Standards

- **Role**: Technical Communications Lead
- **Purpose**: Define standards for creating clear, accurate, and maintainable documentation using the Diátaxis framework.
- **Activates When**: Writing or auditing READMEs, changelogs, technical guides, or inline docstrings.

**Trigger**: model_decision — Apply during the creation and evolution of project documentation.

## 1. Standards

### Principles

- **[REQ-DOC-01] Diátaxis Alignment**
  - Documentation MUST be categorized into one of four distinct modes: Tutorials, How-to Guides, Technical Reference, or Explanation.
- **[REQ-DOC-02] Verified Accuracy**
  - Code examples and implementation claims MUST be verified against the current codebase before publication.
- **[REQ-DOC-03] Explanation of "Why"**
  - Documentation SHOULD prioritize explaining business logic and architectural intent over trivial "what" (code) descriptions.

### Documentation Hierarchy

| Mode | Purpose | Target Audience |
| --- | --- | --- |
| Tutorials | Learning-oriented | Newcomers |
| How-to Guides | Problem-oriented | Practitioners |
| Reference | Information-oriented | Developers (API/Config) |
| Explanation | Perspective-oriented | Architects / Stakeholders |

### Must

- **[REQ-DOC-04] Mandatory README Sections**
  - Every project/module README MUST include a Problem Statement, Quick Start, and Installation guide.
- **[REQ-DOC-05] Active Voice**
  - Technical writing MUST primarily use the active voice (e.g., "The API returns..." instead of "A response is returned...").
- **[REQ-DOC-06] Atomic Updates**
  - Documentation changes MUST be committed alongside the functional code changes they describe.

### Must Not

- **[BAN-DOC-01] Placeholder Claims**
  - Documentation MUST NOT claim the existence of features, examples, or files that are not yet implemented.
- **[BAN-DOC-02] Narrative Fluff**
  - Marketing language and redundant filler MUST be avoided in technical reference documentation.

### Failure Handling

- **Stop Condition**: Stop publishing if technical examples are found to be syntactically incorrect or broken.

## 2. Procedures

- **[PROC-DOC-01] Content Audit**
  - IF updating a core feature THEN MUST audit the associated `README.md` and `docs/` for necessary updates.
- **[PROC-DOC-02] Reference Sync**
  - Automatically generate API reference documentation from JSDoc/Docstrings during the build process where possible.

## 3. Examples

### JSDoc Pattern (Good)

```typescript
/**
 * Calculates the total sum with tax.
 * @param price - Base numeric price
 * @returns Final calculated total
 */
function calculateTotal(price: number): number { ... }
```

## 4. Validation Criteria

- **[VAL-DOC-01] Link Integrity**
  - [ ] Automated scanners confirm zero broken internal or external links in the markdown files.
- **[VAL-DOC-02] Diátaxis Adherence**
  - [ ] Audit confirms that "How-to" guides do not contain conceptual "Explanation" filler.
- **[VAL-DOC-03] Readability Score**
  - [ ] Content meets a Flesch-Kincaid grade level appropriate for the target audience (e.g., Grade 8-10 for devs).
