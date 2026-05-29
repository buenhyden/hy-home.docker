---
name: style-validation
description: >
  Style validation reference for hy-home.docker. Normalizes and validates changed text,
  documentation, and shell files against the Output Style Contract and repository contracts.
  Use for 'style check', 'format', 'lint docs', 'normalize whitespace', 'contract style'.
  Backs the style-enforcer agent.
---

# Style Validation — hy-home.docker

## When to Use

Use after edits to normalize and validate style before completion.

## Procedure

1. Normalize changed-file style (whitespace/newline, shell formatting) — this runs automatically
   via the PostToolUse hook (`scripts/hooks/post-tool-validate.sh`); invoke manually only when
   editing outside the hooked tools.
2. Validate documentation/profile and template contracts:

   ```bash
   bash scripts/validation/check-repo-contracts.sh
   ```

3. Confirm output conforms to `rules/output-style.md` (structured findings, `file:line`
   citations, active voice, English governance / Korean human-facing docs).
4. Report residual blocking issues; never mark complete while style/contract checks fail.

## Rules

- Style normalization is deterministic — prefer the hook/script over manual reformatting.
- Do not change document content or policy under the guise of style.

## Related Documents

- `docs/00.agent-governance/agents/functions/style-validation.md`
- `docs/00.agent-governance/rules/output-style.md`
- `scripts/hooks/post-tool-validate.sh`
