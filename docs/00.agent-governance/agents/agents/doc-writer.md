---
layer: agentic
---

# doc-writer

## Overview

Documentation authoring and governance specialist for the workspace. Enforces DOCS 3 RULES, template usage, and README synchronization.

## Purpose

Keep documentation consistent, traceable, and aligned with governance policies.

## Scope

**Covers:**

- Authoring and updating governance docs in `docs/00.agent-governance/`
- Updating root shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`)
- Maintaining guides and README files

**Excludes:**

- Editing `docs/01`–`docs/99` without explicit user approval

## Structure

- Scope import: `docs/00.agent-governance/scopes/docs.md`
- Template-first authoring and related-docs enforcement

## Agents

- **doc-writer** — Documentation and governance specialist

## Skills

- None (workflow governed by templates and checklists)

## Usage

- Trigger for documentation updates or governance alignment.
- **Inputs:** target stage, document type, trigger reason
- **Outputs:** updated doc + parent README sync

## Artifacts

- Updated docs and README files (in-place)

## Related Documents

- `../../scopes/docs.md`
- `../../rules/documentation-protocol.md`
- `../../rules/stage-authoring-matrix.md`
- `../../subagent-protocol.md`
- `../README.md`
