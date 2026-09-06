---
title: "Output Style"
version: "1.1.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
---

# Output Style

Claude and Codex communicate outcomes first, use plain language, cite concrete
repository evidence, and distinguish verified facts from assumptions. Long-work
updates are concise. Final reports include changed scope, validation, residual
risks, and blockers without copying sensitive output.

## Language

Conversational responses follow the user's active language. Artifact language is
not a presentation choice: it is routed by document role through
[documentation protocol](documentation-protocol.md#authoring-rules). A provider
surface may not set either rule.

## Findings

State a finding as a claim plus its evidence, not as narrative. Cite evidence by
repository path and line so a reader can verify it directly. Tag a review issue
with one severity: `blocker`, `high`, `medium`, or `low`. State an assumption
explicitly and surface a tradeoff rather than resolving it silently.

## Procedures

Write an instruction in the active voice with one action per step and one
expected result. Keep a command runnable as written; mark a non-executable
snippet explicitly.

## Completion Reporting

Report outcomes faithfully. Show failing output rather than summarizing it, name
a skipped step, and state completion only after the check that proves it has
run. Completion obligations themselves belong to
[task checklists](task-checklists.md); this policy owns only how the result is
reported.

Provider-native presentation may adapt rendering but may not change governance
authority, language routing, or acceptance criteria.

## Related Documents

- [Documentation protocol](documentation-protocol.md)
- [Task checklists](task-checklists.md)
- [Provider capability matrix](provider-capability-matrix.md)
- [AI agent standards](standards.md)
