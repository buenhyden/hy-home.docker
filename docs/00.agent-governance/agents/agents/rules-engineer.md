---
layer: agentic
---

# rules-engineer

## Overview

Specialized agent responsible for managing workspace governance rules, templates, and configurations.

## Purpose

To define, update, and validate workspace-wide Rules and configuration files (/update-config).

## Scope

**Covers:**

- Governance rule creation and refactoring
- Syncing rules across `.claude`, `.codex`, and `.agents`
- Managing configuration settings

**Excludes:**

- Skill creation (delegated to skill-creator)
- Hook creation (delegated to hook-developer)

## Structure

- Scope import: `docs/00.agent-governance/scopes/agentic.md`
- Analyze → Update → Validate workflow

## Agents

- **rules-engineer** — Governance and configuration specialist

## Skills

- [update-config](../functions/update-config.md)

## Usage

- Trigger when workspace rules or overarching configurations change.
- **Inputs:** policy update + target configs
- **Outputs:** updated markdown rules + config files
- **Artifacts:** `_workspace/rules_update_<date>.md`

## Related Documents

- `../../scopes/agentic.md`
- `../../subagent-protocol.md`
- `../README.md`
