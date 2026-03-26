---
layer: agentic
---

# Documentation Protocol

This protocol defines how agents maintain documentation consistency across the repository.

## 1. Context & Objective

- Preserve Stage-Gate integrity.
- Keep documentation synchronized with implementation state.
- Ensure language and template policies are applied consistently.

## 2. Requirements & Constraints

- Use templates from `docs/99.templates/` for new stage documents.
- Maintain relative links only; do not use absolute `file://` links.
- Keep `docs/00.agent-governance/` English-only.
- Keep human-facing docs in Korean unless technical interoperability requires English terms.

## 3. Implementation Flow

1. Identify target stage and corresponding template.
2. Draft or update the document with required metadata and references.
3. Cross-link related PRD/ARD/ADR/Spec/Plan/Task/Runbook artifacts.
4. Verify links and command examples.

## 4. Operational Procedures

- Trigger documentation updates when:
  - service topology changes
  - commands or workflow steps change
  - ownership/scope of a module changes
- For task completion, ensure affected README files remain accurate.

## 5. Maintenance & Safety

- Remove obsolete instructions quickly.
- Do not modify `docs/01` to `docs/99` unless explicitly requested.
- If policy and reality diverge, update policy references in `docs/00.agent-governance`.
