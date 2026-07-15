---
layer: agentic
runtime: gemini
---

# Gemini Provider Notes

Gemini CLI-specific guidance for this repository.

## 1. Context and Objective

- Keep Gemini context loading predictable and token-efficient.
- Align Gemini behavior with shared governance in `AGENTS.md` and `docs/00.agent-governance`.

## 2. Provider-Specific Rules

- Keep root `GEMINI.md` thin and import shared governance.
- Prefer hierarchical context loading over broad static context.
- Recommended `.gemini/settings.json` configuration:
  - `"context.fileName": ["GEMINI.md", "AGENTS.md"]`

## 3. Root Import Boundary

The root `GEMINI.md` owns the executable import list. It loads bootstrap, this
provider overlay, the memory index, and progress in that order; do not copy the
list into another governance surface.

## 4. Instruction Precedence (Gemini-Specific)

Gemini merges context from multiple files. Within this repository:

- `GEMINI.md` is the root shim; it imports bootstrap, this overlay, and memory.
- `docs/00.agent-governance/` governance files are the policy SSOT and override Gemini defaults.
- `.agents/` is the provider-neutral compatibility and shared-skill surface.
- GitHub-native instruction files are not part of this repository's active instruction hierarchy.

## 5. Runtime Surface

Per the Stage 00 Canonical Adapter Model (`providers/agents-md.md` §5), Gemini
uses `.gemini/` for native adapters and hooks when those generated surfaces are
present. Until the provider projection task creates them, native workspace
adoption is not claimed.

- `.agents/agents/<name>.md` are compatibility projections of the Stage 00 role catalog.
- `.agents/skills/<name>/SKILL.md` are shared skill projections of the Stage 00 function catalog.
- `.gemini/agents/` and `.gemini/settings.json` are the reserved Gemini-native
  surfaces; their absence means adoption is pending, not behaviorally complete.
- Gemini agent model identifiers follow the Model Policy in `subagent-protocol.md` (supervisor `gemini-3.1-pro`, worker `gemini-3.5-flash`).
- The `.agents/` directory is git-tracked.

## 6. Hook Parity Contract

- Gemini follows the shared `rules/output-style.md`, `rules/provider-capability-matrix.md`, and `rules/workflows.md` as behavioral contracts.
- Current Gemini CLI releases expose provider-native hooks, but no adoption is
  claimed until tracked `.gemini/` artifacts are rendered and validated.
- **Pre-edit validation**: Review requirements and guardrails before mutating files.
- **Post-edit validation**: Validate style (formatting, trimming), run repository
  contracts, and for changed or new target Markdown run
  `python3 scripts/validation/check-document-metadata.py --mode check-changed`
  with a safe comparison base before declaring completion.
- **Template-first guidance**: Use `docs/99.templates/` before creating new target-stage documentation.
- **Commit discipline**: Create logical Conventional Commits for completed repository-modifying work.
- **README guidance**: Follow the provider-neutral README readiness rules.
- **Controlled all-files QA**: Direct agent execution of all-files pre-commit is
  prohibited. At an approved final QA gate, invoke only
  `scripts/validation/run-agent-precommit-all-files.sh` and record the reviewed
  Git-visible, non-ignored repository paths in Stage 04 evidence.

## 7. Operational Practices

- Use `/memory list` to inspect loaded context files.
- Use `/memory show` to inspect merged effective context.
- Use `/memory refresh` after editing instruction files.
- Keep imports explicit and remove stale references quickly.

## Related Documents

- `docs/00.agent-governance/providers/agents-md.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `.agents/README.md`

## References

- <https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html>
- <https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html>
- <https://google-gemini.github.io/gemini-cli/docs/cli/commands.html>
