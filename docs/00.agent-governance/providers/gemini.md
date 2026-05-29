---
layer: agentic
---

# Gemini / Antigravity Provider Notes

Antigravity 2.0 IDE & Gemini CLI-specific guidance for this repository.

## 1. Context and Objective

- Keep Gemini and Antigravity context loading predictable and token-efficient.
- Align behavior with the Universal SSOT in `docs/00.agent-governance/`.
- Embrace Antigravity 2.0 IDE's native features (Workspace Rules, Skills, Workflows) over legacy shim directories.

## 2. Provider-Specific Rules

- `GEMINI.md` delegates directly to shared governance.
- Antigravity 2.0 natively reads User Rules and Skills from `.gemini/config/skills/` and global configurations. For repository-specific logic, agents must consult `docs/00.agent-governance/rules/` directly.
- The legacy `.agents/` directory is deprecated as an execution surface in favor of native Antigravity integrations.

## 3. Recommended Loading Sequence

1. `@AGENTS.md`
2. `@docs/00.agent-governance/providers/agents-md.md`
3. `@docs/00.agent-governance/providers/gemini.md`
4. bootstrap -> persona -> checklists -> one scope -> JIT stage docs
5. `rules/github-governance.md` for PR / merge / review tasks

## 4. Instruction Precedence (Antigravity-Specific)

- `GEMINI.md` is the root shim; it delegates to `AGENTS.md` and provider overlays.
- `docs/00.agent-governance/` governance files are the policy SSOT.
- Antigravity's native `[RULE]` injections override legacy file contents where applicable.
- GitHub-native instruction files are not part of this repository's active instruction hierarchy.

## 5. Runtime Surface & Adapter Pattern

Per the Adapter Model (`providers/agents-md.md` §5), Antigravity acts as a platform adapter:

- Antigravity agents map the catalog in `docs/00.agent-governance/agents/` directly into their operational context.
- Gemini agent model identifiers follow the Model Policy in `subagent-protocol.md` (supervisor `gemini-3.1-pro`, worker `gemini-3.5-flash`).

## 6. Hook Parity Contract

- Antigravity/Gemini follows the shared `rules/output-style.md`, `rules/provider-capability-matrix.md`, and `rules/workflows.md` as behavioral contracts.
- Common rules are now defined in `docs/00.agent-governance/rules/hooks/hookify.*.md`. Antigravity agents MUST respect these rules during all Tool Uses (like Edit, Write, MultiEdit).
- **Pre-edit validation**: Review requirements and guardrails in the common hook definitions before mutating files.
- **Post-edit validation**: Validate style and run repository contract checks before declaring completion.
- **Template-first guidance**: Use `docs/99.templates/` before creating new target-stage documentation.
- **Commit discipline**: Create logical Conventional Commits for completed repository-modifying work.

## 7. Operational Practices

- Use Antigravity Planning Mode and Artifact generation for complex, multi-step tasks.
- Keep imports explicit and remove stale references quickly.

## Related Documents

- `docs/00.agent-governance/providers/agents-md.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/bootstrap.md`
