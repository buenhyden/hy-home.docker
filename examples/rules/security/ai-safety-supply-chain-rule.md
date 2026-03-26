---
layer: security
description: "Rule for AI safety controls and dependency/supply-chain risk governance."
---

# Security — AI Safety & Supply Chain Rule

## Case
- **[REQ-AI-SEC-01]** Defend model-facing surfaces against prompt injection and unsafe execution.
- **[REQ-AI-SEC-02]** Validate model output before trusted action.
- **[REQ-SEC-11]** Continuously audit dependency/supply-chain risk.
- **[REQ-SEC-12]** Preserve lockfile and dependency integrity controls.

## Style
- **[PROC-DSO-01]** Use repeatable dependency scanning and triage flow.
- **[REQ-SUP-01]** Keep supply-chain ownership and remediation workflow explicit.
- **[BAN-AI-SEC-01]** Avoid direct execution of unvalidated model outputs.
- **[BAN-DSO-01]** Do not ignore critical dependency vulnerabilities.

## Validation
- [ ] AI safety controls exist for model-driven critical paths.
- [ ] Dependency scan workflow is active and actionable.
- [ ] High-risk supply-chain findings have explicit remediation paths.
