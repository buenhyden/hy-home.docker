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
- `.gemini/` is the generated Gemini CLI native agent, settings, and hook
  adapter surface.
- GitHub-native instruction files are not part of this repository's active instruction hierarchy.

## 5. Runtime Surface

Per the Stage 00 Canonical Adapter Model (`providers/agents-md.md` §5), Gemini
uses generated `.gemini/` agents, settings, and one thin native event-name
adapter. Stage 00 remains canonical.

- `.agents/agents/<name>.md` are compatibility projections of the Stage 00 role catalog.
- `.agents/skills/<name>/SKILL.md` are shared skill projections of the Stage 00 function catalog.
- `.gemini/agents/*.md` use the native `name`, `description`, `kind`, `tools`,
  `model`, `max_turns`, and `timeout_mins` fields. Read-only roles have an
  explicit non-wildcard tool allowlist; Gemini agent files do not invent a
  per-agent sandbox field.
- `.gemini/settings.json` maps native events to
  `.gemini/hooks/agent-event-hook.sh`, which translates event names and delegates
  shared behavior to `scripts/hooks/agent-event-hook.sh` with recursion
  protection. The adapter also translates output schemas: `BeforeAgent` emits
  its native event name, `PreCompress` emits advisory `systemMessage` output
  only, and the other five events retain only their permitted native fields.
- Gemini model identifiers follow the typed work-profile policy: 3.5 Flash for
  supervision/complex work and 3.1 Flash-Lite for read-heavy/repetitive work.
- The `.agents/` directory is git-tracked.

## 6. Hook Parity Contract

- Gemini follows the shared `rules/output-style.md`, `rules/provider-capability-matrix.md`, and `rules/workflows.md` as behavioral contracts.
- `BeforeTool`/`AfterTool` use tool matchers. Lifecycle and agent hooks omit a
  default `*` matcher because matching behavior is event-specific.
- `AfterAgent` may deny a response and force a retry; it maps to the shared Stop
  gate as `deny-retry`, not as an irreversible session stop.
- `BeforeTool` and `BeforeAgent` expose native block capability, but the current
  repository dispatcher uses them only for advisory context. Capability and
  repository behavior are recorded separately in the typed event bindings.
- `PreCompress` is inherently asynchronous and advisory. No unsupported
  `async` configuration key is emitted. `SessionEnd` is best effort.
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
- `.gemini/README.md`
- `docs/00.agent-governance/contracts/provider-models.yaml`

## References

- <https://geminicli.com/docs/core/subagents/>
- <https://geminicli.com/docs/hooks/reference/>
- <https://geminicli.com/docs/get-started/configuration/>
