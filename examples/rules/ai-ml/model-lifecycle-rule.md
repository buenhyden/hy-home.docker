---
layer: ai-ml
description: "Rule for AI/ML model lifecycle quality, grounding, and evaluation controls."
---

# AI/ML — Model Lifecycle Rule

## Case
- **[REQ-AI-GEN-01]** Ground generated outputs in explicit source context.
- **[REQ-AI-GEN-02]** Keep model behavior reproducible for engineering workflows.
- **[REQ-AI-GEN-03]** Define evaluation criteria before rollout.
- **[REQ-AI-IDX-01]** Preserve model/feature traceability for audits.

## Style
- **[PROC-AI-EVAL-01]** Use repeatable evaluation loops for critical outputs.
- **[REQ-AI-MUST-01]** Document assumptions and confidence boundaries.
- **[BAN-AI-COS-01]** Avoid cosmetic AI integration without measurable value.

## Validation
- [ ] Lifecycle stages (input, generation, evaluation, release) are explicit.
- [ ] Evaluation signals are defined and recorded.
- [ ] Output grounding requirements are enforceable.
