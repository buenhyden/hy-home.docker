---
title: Formatting Authority Convergence Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0166
parent_ids: [REQ-0024, REQ-0026, AD-0030, ADR-0029]
created: 2026-09-03
updated: 2026-09-03
---

# Formatting Authority Convergence Specification

## Overview

Formatting was decided outside this repository. An agent editor hook ran
`ruff format` on every Python write and `npx prettier` on every Markdown write,
while `.pre-commit-config.yaml` held no formatter at all, so nothing in CI
agreed with or observed what that hook did.

88 of 106 Python files disagreed with the formatter that was silently applying
itself, and 18 already matched it -- the ones agents had touched. The corpus was
splitting into two styles at random.

## Boundaries and Inputs

Owned here: which tool owns each file type, where its settings are pinned, and
the validator coupling that made any reformatting break the gate.

Not owned here: the editor hook itself, which lives outside this repository and
is met with a boundary rather than edited.

Inputs: the tracked corpus, `.pre-commit-config.yaml`, and the measured
disagreement between corpus and tools.

## Behavior Contract

- Each tracked file type has exactly one formatting owner, named in
  `.pre-commit-config.yaml`.
- Formatting settings are pinned in the repository, not taken from a tool
  default or a machine's installed version.
- A tool with no tracked invocation does not govern the repository, and states
  so in its own ignore file where it cannot be registered.
- No validator depends on where a line breaks.

## Technical Approach

Measure the disagreement before choosing. Prefer the configuration that already
matches most of the corpus; where none does, adopt the tool that actually runs
and reformat once. Remove configuration that governs nothing rather than leaving
it to be mistaken for policy.

Fix every check the reformatting would break before reformatting, so the
adoption commit lands green instead of dragging a red gate.

## Interfaces and Data

| Surface | Change |
| :--- | :--- |
| `ruff.toml` | added; pins Python formatting |
| `.pre-commit-config.yaml` | `ruff-format` section; headers renumbered and in English |
| `.prettierrc.json` | deleted |
| `.prettierignore` | ignores everything and names each type's owner |
| `scripts/lib/document_governance/operations_catalog.py` | scan honours a stated marker |
| 88 Python files | reformatted once |
| `docs/00.agent-governance/policies/quality-standards.md` | ownership rules |

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| Reformatting breaks a check that depended on line breaks | Decouple the check first, in its own commit |
| An exemption marker becomes a blanket bypass | Verify it exempts only the line it is on |
| Removing a config unleashes the tool it configured | Verify the tool is a no-op afterwards, not merely unconfigured |
| A style is chosen by preference | Measure each candidate against the corpus |

## Acceptance Contract

1. `ruff format --check` reports every tracked Python file already formatted.
2. Prettier is a no-op on this repository.
3. The retired-route scan still reports an unmarked reference.
4. `run-ci-gate.py --profile full` exits 0 after every commit.

## Traceability

- Enabled by SPEC-0165, which is unrelated in subject but shares the branch;
  the ordering constraint here is internal to this package.

## Related Documents

- [Quality standards](../../../../00.agent-governance/policies/quality-standards.md)
- [Documentation protocol](../../../../00.agent-governance/policies/documentation-protocol.md)
