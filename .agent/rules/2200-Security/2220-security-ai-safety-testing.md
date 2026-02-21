---
trigger: always_on
glob: ["**/*"]
description: "Security AI Safety Testing: Enforces OWASP LLM Top 10 mitigation, adversarial testing, and bias detection standards."
---

# Security AI Safety Testing & Response

- **Role**: AI Red Team Lead
- **Purpose**: Define standards for proactively testing AI integrations against common vulnerabilities and performance failures.
- **Activates When**: Performing quality assurance, red teaming prompts, or reviewing AI-generated outputs.

**Trigger**: always_on — Apply during the testing and validation phases of AI-integrated systems.

## 1. Standards

### Principles

- **[REQ-AI_TEST-01] Adversarial Verification**
  - Prompts MUST be stress-tested against the OWASP LLM Top 10 (Injection, Output Handling, Agency, etc.).
- **[REQ-AI_TEST-02] Multi-Category Bias Detection**
  - AI responses MUST be audited for bias across Gender, Racial, Cultural, Socioeconomic, Ability, and Age categories.
- **[REQ-AI_TEST-03] Deterministic Validations**
  - Output handling MUST prioritize strictly validated JSON/data structures over raw, unparsed text streams.

### OWASP LLM Top 10 Mapping

| Vulnerability | REQ ID | Critical Mitigation |
| --- | --- | --- |
| LLM01: Prompt Injection | [REQ-AI_TEST-04] | Input Sanitization / Delimiters |
| LLM02: Output Handling | [REQ-AI_TEST-05] | Validation & Parameterization |
| LLM06: Info Disclosure | [REQ-AI_TEST-06] | PII Filter / Output Scrubbing |
| LLM08: Excessive Agency | [REQ-AI_TEST-07] | Human-in-the-Loop Approval |

### Must

- **[REQ-AI_TEST-08] Baseline Test Coverage**
  - Every prompt MUST have at least 15 test cases (Happy Path, Edge Case, Error, Adversarial, Bias, Multilingual).
- **[REQ-AI_TEST-09] Explicit Error Summaries**
  - System-level errors (e.g., token limits, tool timeouts) MUST be handled gracefully with generic user feedback.
- **[REQ-AI_TEST-10] Token Usage Monitoring**
  - Requests MUST be rate-limited and capped by token usage to prevent Denial of Service (LLM04).

### Must Not

- **[BAN-AI_TEST-01] Unchecked Output Execution**
  - Model outputs MUST NOT be passed directly to execution sinks (e.g., `eval()`, `db.execute()`) without parameterization.
- **[BAN-AI_TEST-02] Single-Point Decisions**
  - AI MUST NOT make high-stakes final decisions (e.g., loan approval, account deletion) without human review (LLM09).

### Failure Handling

- **Stop Condition**: Stop feature activation if the bias detection audit identifies a consistent demographic discrepancy.

## 2. Procedures

- **[PROC-AI_TEST-01] Bias Audit Routine**
  - IF updating a core prompt THEN MUST run the formal 6-dimension bias test suite.
- **[PROC-AI_TEST-02] Regression Testing**
  - Maintain a "Reputation" dataset of known good/bad outputs to verify model performance consistency.

## 3. Examples

### Secure Output Handling

```python
# Good: Sanitizing LLM output before use in a database
llm_output = llm.complete(prompt)
validated_output = validate_and_sanitize(llm_output)
db.execute("INSERT INTO logs VALUES (%s)", (validated_output,))
```

## 4. Validation Criteria

- **[VAL-AI_TEST-01] Top 10 Compliance**
  - [ ] Prompt fails safely under standard LLM01 and LLM06 attack vectors.
- **[VAL-AI_TEST-02] Pass Rate Threshold**
  - [ ] Automated benchmarks show > 95% pass rate for functional accuracy across the test suite.
- **[VAL-AI_TEST-03] Rate-Limit Efficacy**
  - [ ] Simulated error surge proves that token caps and rate limits prevent budget exhaustion.
