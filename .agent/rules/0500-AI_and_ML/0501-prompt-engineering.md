---
trigger: model_decision
glob: ["**/*.prompt", "**/*.md"]
description: "Prompt Engineering Standard. Research-driven creation, Persona validation, and Dual-Persona methodology."
---

# 0501-Prompt-Engineering-Standard

- **Role**: Lead Prompt Engineer
- **Purpose**: Create Deterministic, Safe, and High-Performance AI Prompts.
- **Activates When**: Designing System Prompts, deciding Agent Behavior, or writing Instruction Sets.

## 1. Standards

### 1.1 Core Principles

- **[REQ-PRM-DET-01] Deterministic**: Prompts MUST use imperative language ("You WILL", "You MUST"). Avoid "Please" or "Try".
- **[REQ-PRM-COT-01] Chain of Thought**: Complex reasoning tasks MUST require a "Thought" block before the "Action".
- **[REQ-PRM-STR-01] Structure**: Prompts MUST follow the `Role -> Context -> Task -> Constraints -> Examples` format.

### 1.2 Dual Persona Methodology

- **[REQ-PRM-PER-01] Builder**: The persona writing the prompt. Focus on constraints and edge cases.
- **[REQ-PRM-PER-02] Tester**: The persona validating the prompt. Focus on breaking the constraints (Red Teaming).

### 1.3 Safety

- **[REQ-PRM-SEC-01] Injection Defense**: Prompts MUST strictly separate Instructions from User Data (e.g., using XML tags `<user_input>`).

## 2. Procedures

### 2.1 Prompt Creation Flow

1. **Define Goal**: What is the single specific output?
2. **Select Persona**: "Act as a Senior Python Architect".
3. **Draft Context**: Provide necessary background (Stack, Constraints).
4. **Add Examples**: Few-Shot learning (Input -> Reasoning -> Output).
5. **Refine**: Remove ambiguity.

### 2.2 Optimization

1. **Token Reduction**: Remove polite filler words.
2. **Constraint Hardening**: Move negative constraints ("Do NOT") to the end or beginning for emphasis.

## 3. Examples

### 3.1 Standard Prompt Template

```markdown
# Role
You are a Security Auditor.

# Context
We are auditing a React application for XSS vulnerabilities.

# Task
Analyze the provided code snippet. Return a JSON list of vulnerabilities.

# Constraints
- You MUST only identify High/Critical issues.
- You MUST provide a fix for each issue.

# Input
<code_snippet>
{code}
</code_snippet>
```

## 4. Validation Criteria

- [ ] **[VAL-PRM-STR-01]** Prompt follows the RC-TCE structure.
- [ ] **[VAL-PRM-COT-01]** Complex tasks enforce Chain of Thought.
- [ ] **[VAL-PRM-SEC-01]** User input is delimited (XML/Markdown).
