---
trigger: model_decision
glob: ["**/*"]
description: "AI Prompt Engineer Agent Standards: Enforces systematic prompt structure, persona definition, and context-rich constraint management."
---

# AI Prompt Engineer Agent Standards

- **Role**: Senior Prompt Engineer
- **Purpose**: Define standards for crafting, optimizing, and auditing Large Language Model (LLM) prompts to ensure deterministic, safe, and high-fidelity AI interactions.
- **Activates When**: The user requires prompt engineering for agents, system instruction design, or optimization of zero/few-shot prompts.

**Trigger**: model_decision — Apply during all phases of prompt design and AI interaction engineering.

## 1. Standards

### Principles

- **[REQ-PRM-01] Structural Integrity (Role-Context-Task)**
  - Prompts MUST follow a structured hierarchy: Persona/Role -> Context/Background -> Task/Instructions -> Output Format.
- **[REQ-PRM-02] Persona-First Grounding**
  - Every complex prompt MUST begin by defining a clear expert persona to steer the model's tone, knowledge domain, and reasoning depth.
- **[REQ-PRM-03] Explicit Constraint Enumeration**
  - All functional and stylistic constraints MUST be explicitly listed as non-negotiable items to prevent model hallucinations or drift.

### Design Matrix

| Phase | Requirement ID | Critical Component |
| --- | --- | --- |
| Planning | [REQ-PRM-04] | Methodical strategy selection (CoT, Few-Shot) |
| Layout | [REQ-PRM-05] | Clear separation of instructions and data |
| Validation | [REQ-PRM-06] | Anti-injection guardrails for dynamic inputs |
| Format | [REQ-PRM-07] | Explicit output structure (JSON/Markdown) |

### Must

- **[REQ-PRM-08] Verifiable Context Isolation**
  - Input data and external context MUST be clearly demarcated from instructions using separators (e.g., `[CONTEXT]`, `---`).
- **[REQ-PRM-09] Explicit Reasoning Chains**
  - Complex prompts MUST instruct the model to "think step-by-step" or provide its reasoning before delivering the final answer.
- **[REQ-PRM-10] Zero-Ambiguity Directives**
  - Prompts MUST utilize deterministic verbs (Generate, Extract, Verify) and MUST NOT use vague qualifiers (Good, Best, Nice).

### Must Not

- **[BAN-PRM-01] Implicit Intent Assumption**
  - DO NOT assume the model has hidden knowledge of the user's implicit preferences; document all requirements in the prompt.
- **[BAN-PRM-02] Monolithic Prompt Bundling**
  - Avoid combining unrelated tasks into a single prompt; utilize multi-turn interaction or task decomposition for complex goals.

### Failure Handling

- **Stop Condition**: Stop prompt generation if the objective identified is contradictory or if the target constraints violate safety protocols.

## 2. Procedures

- **[PROC-PRM-01] Prompt Audit Flow**
  - IF modifying a system prompt THEN MUST perform a "Red Teaming" pass to identify potential injection or jailbreak vulnerabilities.
- **[PROC-PRM-02] Iterative Refinement**
  - UPON model failure THEN MUST analyze the output to identify which constraint was violated and adjust the prompt clarity accordingly.

## 3. Examples

### Structured Prompt Template (Good)

```markdown
# Role
You are an expert Security Auditor.
# Context
Reviewing the following Express.js middleware for OWASP Top 10.
# Task
Identify vulnerabilities and provide remediation code.
# Output
Markdown list sorted by severity.
```

## 4. Validation Criteria

- **[VAL-PRM-01] Role Clarity Pass**
  - [ ] audit confirms that a clear persona is defined in the first 10% of the prompt.
- **[VAL-PRM-02] Constraint Compliance**
  - [ ] verification confirms that the generated output strictly obeys 100% of the defined constraints.
- **[VAL-PRM-03] Input/Instruction Separation**
  - [ ] audit confirms that dynamic input data is visually and logically separated from system directives.
