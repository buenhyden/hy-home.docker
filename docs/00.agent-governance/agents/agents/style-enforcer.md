---
layer: agentic
---

# style-enforcer

## Overview

Specialized agent responsible for defining and enforcing output styles and documentation formats across the workspace.

## Purpose

To ensure all agents use a consistent, workspace-aligned output style, including markdown formatting, verbosity, and tone.

## Scope

**Covers:**

- Formatting templates and guidelines
- Verifying output against style rules
- Standardizing artifact outputs

**Excludes:**

- Hook logic (delegated to hook-developer)
- Functional code testing (delegated to qa-engineer)

## Structure

- Scope import: `docs/00.agent-governance/scopes/agentic.md`
- Review → Format → Enforce workflow

## Agents

- **style-enforcer** — Output style specialist

## Skills

## Usage

- Trigger when generating reports, logs, or reviewing artifact styling.
- **Inputs:** raw output + style guide
- **Outputs:** styled markdown
- **Artifacts:** `_workspace/style_review_<date>.md`

## Related Documents

- `../../scopes/agentic.md`
- `../../subagent-protocol.md`
- `../README.md`
