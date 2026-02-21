---
trigger: model_decision
glob: ["**/*"]
description: "Responsible AI: Bias prevention, Accessibility compliance, and Safety guardrails."
---

# 0106-Responsible-AI

- **Role**: Ethics Compliance Officer
- **Purpose**: Ensure AI systems are safe, fair, accessible, and transparent.
- **Activates When**: Designing AI interactions or data processing pipelines.

## 1. Standards

### 1.1 Principles

- **[REQ-RAI-GEN-01] Fairness**: AI MUST not discriminate based on protected characteristics.
- **[REQ-RAI-GEN-02] Transparency**: Users MUST know they are interacting with AI.
- **[REQ-RAI-GEN-03] Privacy**: User PII MUST be protected (sanitized) before AI processing.

### 1.2 Scope

- **In-Scope**: AI Interactions, Generated Content, Accessiblity of AI UIs.
- **Out-of-Scope**: General Security (see 0750).

### 1.3 Must / Must Not

- **[REQ-RAI-ACC-01] Accessibility**: AI Interfaces MUST meet WCAG 2.1 AA (Keyboard, Screen Reader).
- **[BAN-RAI-SEC-01] No Secrets**: API Keys/Secrets MUST NOT be sent to LLMs.
- **[REQ-RAI-TST-01] Bias Testing**: Models MUST be tested against diverse inputs (names, cultures).

## 2. Procedures

### 2.1 Pre-Deployment Checklist

1. **Red Teaming**: Can you trick the AI into harmful output?
2. **Bias Check**: Does it treat "John" different from "Akira"?
3. **Accessibility**: Can you use it without a mouse?

### 2.2 Data Sanitization

1. **Identify**: Email, Phone, SSN, Credit Card.
2. **Action**: Replace with placeholders (`<EMAIL>`) or Redact.
3. **Log**: Record that redaction occurred (audit trail).

## 3. Examples

### 3.1 Output Sanitization Pattern

```javascript
// BAD
return `Welcome ${user.realName}, I see you live at ${user.address}`;

// GOOD
// PII is treated carefully
const safeName = sanitize(user.realName);
return `Welcome ${safeName}`;
```

## 4. Validation Criteria

- [ ] **[VAL-RAI-ACC-01]** UI passes automated accessibility scan (axe-core).
- [ ] **[VAL-RAI-PRI-01]** No PII detected in prompt logs.
- [ ] **[VAL-RAI-TSPA-01]** UI clearly labels content as "AI Generated".

## 5. References

- Related: [0105-prompt-engineering.md](./0105-prompt-engineering.md)
