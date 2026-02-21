---
trigger: model_decision
glob: ["docs/**/*.md","README.md"]
description: "Documentation Pillar Standard: Enforces the Diátaxis framework and Style Guidelines."
---
# Documentation Pillar Standard

## Activation
- [ ] Apply when Writing docs, READMEs, or architectural records..
- [ ] Apply when editing files matching: `docs/**/*.md, README.md`.

## Rules
- **Role**: Technical Writer
- **Purpose**: Enforce clarity, usability, and maintainability of internal and external documentation.
- **Activates When**: Writing docs, READMEs, or architectural records.

**Trigger**: model_decision — Apply when writing documentation.

---

### 1. Standards

### 1.1 Diátaxis Framework
- **[REQ-DOC-DIA-01] Tutorial**: Learning-oriented. Step-by-step strictly for beginners. (e.g., "Zero to Hero").
- **[REQ-DOC-DIA-02] How-To**: Task-oriented. "How do I...?" focused on specific outcome. (e.g., "How to configure OAuth").
- **[REQ-DOC-DIA-03] Reference**: Information-oriented. Dry facts, APIs, configs. (e.g., "API Spec").
- **[REQ-DOC-DIA-04] Explanation**: Understanding-oriented. Background, alternatives, trade-offs. (e.g., "Why we chose Rust").

### 1.2 Writing Style
- **[REQ-DOC-STYLE-01] Clarity**: Use Active Voice. Avoid jargon without definition.
- **[REQ-DOC-STYLE-02] Structure**: Use Headings (H1-H3) and Bullet points for scannability.
- **[REQ-DOC-STYLE-03] Links**: Links MUST work relative to the file location.

---

### 2. Procedures

### 2.1 Documentation Lifecycle
1. **Draft**: Create file in `docs/` mapped to a quadrant.
2. **Review**: Check against Style Guide.
3. **Publish**: Merge to main.
4. **Update**: Update on every code change that affects behavior.

---

### 3. Examples

### 3.1 How-To Structure
> **Goal**: Rotate API Keys
> 1. Go to settings.
> 2. Click "Revoke".
> 3. Generate New Key.

---

### 4. Validation Criteria
- [ ] Is Active Voice used?
- [ ] Is Diátaxis quadrant clear?
- [ ] Are links valid?

## References
- None.
