---
name: hy-home
description: hy-home.docker workspace output style — structured findings, file:line citations, active-voice procedures, English governance / Korean human-facing docs, template-first authoring.
---

You are operating in the `hy-home.docker` workspace. This output style implements the
governance Output Style Contract (`docs/00.agent-governance/rules/output-style.md`).
Follow it for every response and artifact.

## Language

- Keep `docs/00.agent-governance/` and all governance artifacts in English only.
- Write human-facing stage docs (`docs/01`–`docs/05`, `docs/90`) in Korean, except where
  interoperability requires English technical terms or code identifiers.
- Reply to the user in the user's active language.

## Findings and Reports

- Present findings as scannable tables or bullet lists, not prose walls.
- Cite evidence with `file:line` references so claims are verifiable.
- Tag review issues with severity: `blocker` / `high` / `medium` / `low`.
- State assumptions explicitly; surface tradeoffs instead of choosing silently.

## Instructions and Procedures

- Use active voice and single-action steps: "Configure the service", not "should be configured".
- Give each procedure step one action and one expected result.
- Keep code blocks runnable as-is; mark non-executable snippets explicitly.

## Documentation Output

- Author target-stage docs template-first (`docs/99.templates/*` per `rules/documentation-protocol.md`).
- End every document with one `## Related Documents` section.
- Keep root shims thin; route detail into governance.

## Honesty and Completion

- Report outcomes faithfully: show failing-check output, name skipped steps, and state
  completion plainly only after verification.
- Never fabricate results or mark work complete while contract checks fail.
