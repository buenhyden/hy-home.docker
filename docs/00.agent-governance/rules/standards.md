---
layer: agentic
---

# AI Agent Standards

Shared standards for instruction design, token efficiency, and task execution.

## 1. Token Optimization & Lazy Loading

- Keep `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` as thin entry shims.
- Store detailed governance only in `docs/00.agent-governance/`.
- Load context in this order:
  1. `rules/bootstrap.md`
  2. `rules/persona.md`
  3. one primary `scopes/<layer>.md`
  4. JIT stage documents (`docs/01` to `docs/11`, then `docs/90` or `docs/99` if required)
- Avoid duplicated instructions across root files and rules.

## 2. Language Standard

- Governance and runtime policy files in `docs/00.agent-governance/` must be English.
- Human-facing documentation (README, operational narratives, reports) should be Korean.
- User-facing assistant responses should be Korean unless explicitly requested otherwise.

## 3. Stage-Gate Compliance

- Treat `docs/01` to `docs/99` as SSoT for project intent, specs, plans, and templates.
- Do not bypass `docs/01.prd` and `docs/04.specs` for implementation work.
- Maintain reciprocal links across PRD, ARD, ADR, Spec, Plan, Task, and Runbook artifacts.

## 4. Execution Discipline

- Use programmatic validation commands whenever they exist.
- Prefer small, isolated changes and explicit verification evidence.
- Remove stale commands or obsolete policy text when discovered.
