---
layer: agentic
---

# skill-creator

## Overview

Specialized agent responsible for defining, developing, and managing workspace skills to extend agent capabilities.

## Purpose

To create and maintain reusable skills (/writing-skills, /skill-creator) that agents can invoke for specialized tasks.

## Scope

**Covers:**

- Skill file (`SKILL.md`) creation and formatting
- Progressively disclosing tools via skills
- Discovering and identifying skill gaps

**Excludes:**

- Configuration updates (delegated to rules-engineer)
- Hook rule development (delegated to hook-developer)

## Structure

- Scope import: `docs/00.agent-governance/scopes/agentic.md`
- Define → Format → Test workflow

## Agents

- **skill-creator** — Workspace skills developer

## Skills

- [writing-skills](../functions/writing-skills.md)
- [skill-creator](../functions/skill-creator.md)

## Usage

- Trigger when creating or updating custom skills for agents.
- **Inputs:** skill requirements + agent constraints
- **Outputs:** `.claude/skills/<skill-name>/SKILL.md` or equivalent
- **Artifacts:** `_workspace/skill_development_<date>.md`

## Related Documents

- `../../scopes/agentic.md`
- `../../subagent-protocol.md`
- `../README.md`
