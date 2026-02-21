---
trigger: model_decision
glob: ["AGENTS.md", "README.md"]
description: "AGENTS.md Generator Agent Standards: Enforces standardized, copy-paste ready, and verified technical documentation for AI agent consumption."
---

# AGENTS.md Generator Agent Standards

- **Role**: AI-Optimization Documentation Specialist
- **Purpose**: Define standards for creating and maintaining `AGENTS.md` and high-level project documentation that enables autonomous discovery and operation by AI agents.
- **Activates When**: The user requests documentation generation, specifically for the "Agentic" audience or during project initialization.

**Trigger**: model_decision — Apply during all documentation generation and technical walkthrough creation phases.

## 1. Standards

### Principles

- **[REQ-GEN-01] copy-Paste Functional Integrity**
  - All commands and code blocks MUST be directly executable in the project environment without manual placeholder replacement.
- **[REQ-GEN-02] Verification-First Evidence**
  - Documentation MUST provide the expected output for critical setup and verification commands to enable agentive self-correction.
- **[REQ-GEN-03] Machine-Optimized Layout**
  - documentation MUST prioritize structured data (Tables, Mermaid, Coded IDs) over marketing prose to facilitate rapid context ingestion by LLMs.

### Documentation Matrix

| Section | Requirement ID | Critical Action |
| --- | --- | --- |
| Setup | [REQ-GEN-04] | list all prerequisites with version pins |
| Workflow | [REQ-GEN-05] | Document "Day 1" commands (Build/Test) |
| Personas | [REQ-GEN-06] | link to standardized rule files |
| Glossary | [REQ-GEN-07] | Define non-standard project terminology |

### Must

- **[REQ-GEN-08] Absolute Path Awareness**
  - Reference files and directories using relative paths from the project root to ensure portability across different local environments.
- **[REQ-GEN-09] Explicit Version Identity**
  - Documentation MUST specify mandatory tool versions (e.g., Node.js >= 20) and verify them using the provided commands.
- **[REQ-GEN-10] Standardized 8-Section Alignment**
  - When documenting project standards, MUST follow the mandatory 8-section skeleton established in the project governance.

### Must Not

- **[BAN-GEN-01] Opaque Placeholders**
  - DO NOT use placeholders like `<your-key>` or `[name]`. utilize environment variable references (e.g., `process.env.KEY`) or concrete examples.
- **[BAN-GEN-02] Narrative Fluff**
  - Avoid purely stylistic or marketing-focused descriptions; maintain a direct, technical, and objective tone.

### Failure Handling

- **Stop Condition**: Stop documentation generation if a required setup command fails verification or if the target persona cannot be definitively linked to a rule file.

## 2. Procedures

- **[PROC-GEN-01] Command Verification Flow**
  - IF documenting a new setup command THEN MUST run the command in the current environment and capture its success output for the documentation.
- **[PROC-GEN-02] Cross-Link Audit**
  - verify that all links within `AGENTS.md` pointing to internal project files or rule sets are functional and accurate.

## 3. Examples

### Clean Setup Block (Good)

```markdown
### Installation
```bash
npm install
cp .env.example .env # Set your API keys here
```

```

## 4. Validation Criteria

- **[VAL-GEN-01] Command Executability**
  - [ ] manual verification confirms that 100% of code blocks can be run without modification.
- **[VAL-GEN-02] Skeleton Compliance**
  - [ ] audit confirms that documentation for standards follows the mandatory 8-section breakdown.
- **[VAL-GEN-03] Persona Linkage**
  - [ ] Verification confirms that 100% of mentioned agent roles map to a valid rule file in `0000-Agents`.
