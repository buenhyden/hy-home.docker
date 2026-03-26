---
layer: agentic
description: "Rule for explicit reasoning quality and safe autonomous execution behavior."
---

# Agentic — Reasoning Rule

## Case
- **[REQ-AGN-04]** Use structured reasoning before high-impact or irreversible operations.
- **[REQ-AGN-01]** Validate assumptions with repository/system evidence before implementation.
- **[REQ-AGN-10]** Prefer minimal solutions that satisfy explicit constraints.

## Style
- **[REQ-PRM-02]** Keep instruction flow deterministic: context, constraints, action, verification.
- **[REQ-AGN-11]** Use surgical edits that align with existing project style.
- **[BAN-REA-01]** Do not fabricate facts when evidence is unavailable.

## Validation
- [ ] High-risk actions include explicit rationale tied to evidence.
- [ ] Assumptions are either validated or documented as assumptions.
- [ ] Proposed changes are minimal and scoped to stated intent.
