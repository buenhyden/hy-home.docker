---
layer: agentic
---

# style-validation

## Overview

Style validation function for the `hy-home.docker` workspace. Normalizes and validates changed
text, documentation, and shell files against the repository's style and contract profiles.

## Purpose

Keep output and documents consistent with the Output Style Contract and repository contracts so
completion gates pass deterministically.

## Scope

**Covers:**

- Changed-file style normalization via `scripts/hooks/post-tool-validate.sh`
- Markdown/doc profile and template-contract checks via `scripts/validation/check-repo-contracts.sh`
- Output Style Contract conformance (`rules/output-style.md`)

**Excludes:**

- Authoring document content (see `doc-writer` and the stage authoring matrix)
- Policy decisions (governance rules own policy)

## Structure

- Detect changed files → normalize style → run contract/profile checks → report residual issues

## Agents

- **style-enforcer** — primary caller

## Skills

- Runtime mirror: `.claude/skills/style-validation/skill.md`

## Usage

- Trigger after edits to normalize and validate style before completion.
- **Inputs:** changed file list
- **Outputs:** style report; blocking issues surfaced before Stop

## Related Documents

- `../../scopes/agentic.md`
- `../../rules/output-style.md`
- `../../rules/documentation-protocol.md`
- `../README.md`
