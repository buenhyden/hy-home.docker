---
layer: ai-ml
description: "Rule for prompt engineering safety, injection resistance, and output control."
---

# AI/ML — Prompt Safety Rule

## Case
- **[REQ-PRM-STR-01]** Use structured prompts with explicit delimiters and intent.
- **[REQ-PRM-SEC-01]** Defend against prompt injection and instruction override patterns.
- **[REQ-SAF-GEN-01]** Apply safety checks before executing or publishing generated content.

## Style
- **[REQ-PRM-PER-01]** Keep prompts concise, deterministic, and role-consistent.
- **[REQ-SAF-AUD-01]** Keep security/audit context around critical model actions.
- **[BAN-SAF-DAT-01]** Do not expose sensitive data in prompts or model logs.

## Validation
- [ ] Prompt structure and guardrails are documented.
- [ ] Injection-risk paths include mitigation controls.
- [ ] Output validation occurs before downstream execution.
