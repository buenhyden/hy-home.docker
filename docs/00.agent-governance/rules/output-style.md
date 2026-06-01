---
layer: agentic
---

# Output Style Contract

Provider-neutral output-style contract for all runtimes (Claude, Codex/GPT, Gemini).
This is the single source of truth for how agents format their responses and
artifacts in `hy-home.docker`. Claude exposes it natively via
`.claude/output-styles/*.md`; Codex and Gemini follow it as a behavioral contract.

## 1. Language

- `docs/00.agent-governance/` content and all governance artifacts: English only.
- Human-facing stage docs (`docs/01`–`docs/05`, `docs/90`): Korean, except where
  interoperability requires English technical terms or code identifiers.
- Conversational replies follow the user's active language preference.

## 2. Findings and Reports

- Report findings as structured, scannable output (tables or bulleted lists), not prose walls.
- Cite evidence with `file:line` references so claims are verifiable.
- Tag issues with severity (`blocker` / `high` / `medium` / `low`) when reviewing.
- State assumptions explicitly; surface tradeoffs instead of silently choosing.

## 3. Instructions and Procedures

- Use active voice and single-action steps ("Configure the service", not "The service should be configured").
- Every procedure step has one action and one expected result.
- Code blocks must be runnable as-is; mark non-executable snippets explicitly.

## 4. Documentation Output

- Author target-stage documents template-first per `rules/documentation-protocol.md`
  (load the mapped `docs/99.templates/*` template before writing).
- Every document ends with one `## Related Documents` section (R3).
- Keep root shims thin; route detail into governance.
- Keep human-facing documents direct and specific. Avoid promotional tone,
  vague significance claims, formulaic "future outlook" endings, and chatbot
  filler; use plain claims backed by repository evidence.
- Use HADS block labels only when a document type or approved plan explicitly
  asks for them. Do not add `[SPEC]`, `[NOTE]`, `[BUG]`, or `[?]` tags to active
  templates as an incidental style change.

## 5. Honesty and Completion

- Report outcomes faithfully: failing checks are reported with their output; skipped
  steps are named; completion is stated plainly only when verified.
- Do not fabricate results or mark work complete while contract checks fail.

## Related Documents

- `docs/00.agent-governance/rules/provider-capability-matrix.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/rules/quality-standards.md`
- `docs/00.agent-governance/rules/persona.md`
