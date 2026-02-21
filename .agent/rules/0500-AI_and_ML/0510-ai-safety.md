---
trigger: model_decision
glob: ["**/*"]
description: "AI Safety: Responsible AI, Ethics, and Governance standards."
---

# 0510-AI-Safety

- **Role**: AI Ethics Officer
- **Purpose**: Ensure AI systems are fair, accountable, and transparent.
- **Activates When**: deploying AI systems to production.

## 1. Standards

### 1.1 Principles

- **[REQ-SAF-GEN-01] Fairness**: Models MUST generally perform equally across demographics (checked via eval).
- **[REQ-SAF-GEN-02] Privacy**: PII MUST be scrubbed before sending to Model APIs.
- **[REQ-SAF-GEN-03] Explainability**: System MUST provide citations or reasoning steps.

### 1.2 Scope

- **In-Scope**: Ethics, Governance, Risk Management.
- **Out-of-Scope**: prompt tactics (see 0500).

### 1.3 Must / Must Not

- **[BAN-SAF-DAT-01] No Training on User Data**: User data MUST NOT be used for training without explicit consent.
- **[REQ-SAF-AUD-01] Audit Logs**: AI decisions MUST be logged for auditability.

## 2. Procedures

### 2.1 Release Checklist

1. **Red Teaming**: Attempt to jailbreak the model.
2. **Bias Testing**: Evaluate against standard datasets.
3. **PII Check**: Verify data sanitization pipeline.

## 3. Examples

### 3.1 PII Scrubbing

```python
def sanitize(text):
    text = remove_emails(text)
    text = remove_phones(text)
    return text
```

## 4. Validation Criteria

- [ ] **[VAL-SAF-PRI-01]** PII scrubber is active.
- [ ] **[VAL-SAF-AUD-01]** Decisions are logged.

## 5. References

- Related: [0500-ai-general.md](./0500-ai-general.md)
