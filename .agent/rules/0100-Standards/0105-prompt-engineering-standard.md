---
trigger: model_decision
glob: ["**/*.prompt", "prompts/**/*.md", ".agent/**/*.md"]
description: "Prompt Engineering: Research-driven creation, Persona validation, and Dual-Persona methodology."
---

# 0105-Prompt-Engineering

- **Role**: Prompt Engineer
- **Purpose**: Create high-quality, reliable, and safe AI prompts through rigorous engineering and validation.
- **Activates When**: Writing or modifying system prompts for agents or workflows.

## 1. Standards

### 1.1 Principles

- **[REQ-PRM-GEN-01] Imperative**: Instructions MUST use imperative, deterministic language ("You WILL", "You MUST").
- **[REQ-PRM-GEN-02] Dual Persona**: Prompts MUST be developed by a "Builder" and validated by a "Tester" (simulated or real).
- **[REQ-PRM-GEN-03] Chain of Thought**: Complex tasks MUST require reasoning BEFORE conclusion.

### 1.2 Scope

- **In-Scope**: System Prompts, Agent Instructions, User Guides for AI.
- **Out-of-Scope**: User data input (see 0106-Responsible-AI).

### 1.3 Must / Must Not

- **[REQ-PRM-STR-01] Structure**: Prompts MUST have clear Role, Context, Instructions, and Examples constraints.
- **[BAN-PRM-VAG-01] No Ambiguity**: Avoid "be helpful" or "do your best". Be specific.
- **[REQ-PRM-EXA-01] Examples**: Prompts MUST include few-shot examples (Input -> Reasoning -> Output).

## 2. Procedures

### 2.1 Creation Process

1. **Research**: Gather documentation/standards for the domain.
2. **Draft**: Define the Goal and Constraints.
3. **Examples**: Create 3+ realistic examples (Happy path + Edge case).
4. **Validation**: Run the prompt against the examples to verify output.

### 2.2 Optimization Checklist

1. **Reduce Token Count**: Remove fluff ("Please", "I would like").
2. **Clarify**: If model hallucinates, add "If you don't know, say 'Unknown'".
3. **Structure**: Use XML tags (`<rules>`) or Markdown headers for separation.

## 3. Examples

### 3.1 Standard Prompt Structure

```markdown
# Role
You are a Senior Python Engineer.

# Context
We are migrating to Python 3.11.

# Instructions
1. Analyze the provided code.
2. Identify deprecated functions.
3. Rewrite using 3.11 features.

# Examples
Input: ...
Reasoning: ...
Output: ...
```

## 4. Validation Criteria

- [ ] **[VAL-PRM-COT-01]** Examples show Reasoning BEFORE Output.
- [ ] **[VAL-PRM-IMP-01]** Instructions use imperative verbs.
- [ ] **[VAL-PRM-STR-01]** Prompt contains distinct Role and Instructions sections.

## 5. References

- Related: [0106-responsible-ai.md](./0106-responsible-ai.md)
