---
trigger: model_decision
glob: ["**/*.py", "**/*.ts"]
description: "AI Standards: Prompt Engineering, Model integration, and Responsible AI principles."
---

# 0500-AI-General

- **Role**: AI Engineer
- **Purpose**: Define standards for AI Integration, Prompt Engineering, and Safety.
- **Activates When**: Integrating LLMs, designing prompts, or building AI agents.

## 1. Standards

### 1.1 Principles

- **[REQ-AI-GEN-01] Safety First**: AI outputs MUST be treated as untrusted user input.
- **[REQ-AI-GEN-02] Transparency**: Users MUST be informed when interacting with AI.
- **[REQ-AI-GEN-03] Human in the Loop**: Critical actions MUST require human confirmation.

### 1.2 Scope

- **In-Scope**: LLM Integration, Prompt Engineering, RAG.
- **Out-of-Scope**: Model Training (MLOps).

### 1.3 Must / Must Not

- **[REQ-AI-PRM-01] System Prompts**: MUST define clear role, constraints, and format.
- **[BAN-AI-SEC-01] No Injection**: Prompts MUST protect against injection attacks (delimiters).
- **[REQ-AI-COS-01] Token Limits**: Inputs MUST be truncated to fit context windows.

## 2. Procedures

### 2.1 Prompt Engineering (CO-STAR)

1. **C**ontext: Background info.
2. **O**bjective: What to achieve.
3. **S**tyle: Tone/Role.
4. **T**one: Formal/Casual.
5. **A**udience: Who is reading.
6. **R**esponse: Format (JSON/Markdown).

### 2.2 Safety Guardrails

1. **Input**: Scan for PII/Injection.
2. **Processing**: Use separate context for user data.
3. **Output**: Validate against schema (JSON mode) and content policy.

## 3. Examples

### 3.1 Protected Prompt

```python
system_prompt = """
You are a helpful assistant.
Current Date: {date}

Instructions:
1. Answer the user question.
2. If unsure, say "I don't know".

User Input is delimited by triple quotes.
"""

user_message = f"""'''{user_input}'''"""
```

## 4. Validation Criteria

- [ ] **[VAL-AI-SEC-01]** User input is delimited in prompts.
- [ ] **[VAL-AI-HUM-01]** Critical tools require confirmation.

## 5. References

- Reference: [0510-ai-safety.md](./0510-ai-safety.md)
