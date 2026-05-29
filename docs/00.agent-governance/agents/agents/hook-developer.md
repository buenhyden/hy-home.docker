---
layer: agentic
---

# hook-developer

## Overview

Specialized agent responsible for defining and managing hookify rules to enforce workspace behaviors.

## Purpose

To write hook rules (/writing-hookify-rules, /hook-development) that intercept tool calls and ensure compliance with governance.

## Scope

**Covers:**

- Hookify rule (`hookify.*.local.md`) creation
- Event pattern matching (bash, file, stop, prompt)
- Warning and block message formatting

**Excludes:**

- Skill creation (delegated to skill-creator)
- Output styling (delegated to style-enforcer)

## Structure

- Scope import: `docs/00.agent-governance/scopes/agentic.md`
- Intercept → Pattern Match → Warn/Block workflow

## Agents

- **hook-developer** — Hook rules developer

## Skills

- [writing-hookify-rules](../functions/writing-hookify-rules.md)
- [hook-development](../functions/hook-development.md)

## Usage

- Trigger when governance requires programmatic enforcement via hooks.
- **Inputs:** governance policy + trigger condition
- **Outputs:** `.claude/hookify.<rule>.local.md`
- **Artifacts:** `_workspace/hook_development_<date>.md`

## Related Documents

- `../../scopes/agentic.md`
- `../../subagent-protocol.md`
- `../README.md`
