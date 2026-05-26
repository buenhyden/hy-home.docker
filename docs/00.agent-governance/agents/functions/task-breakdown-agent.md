---
layer: agentic
---

# task-breakdown-agent

## Overview

Decomposes approved implementation plans into task evidence documents in
`docs/04.execution/tasks/` using `task.template.md`.

## Purpose

Maintain the audit trail of what was actually done, what was verified, and what
deviated from the plan. One task per plan; update in place.

## Scope

**Covers:**

- Per-step execution status tracking
- Actual command output and pass/fail recording
- Deviation and deferral notation

**Excludes:**

- New requirements, architecture decisions, or spec content
- Plan authoring (handled by execution-plan-agent)

## Structure

- Reads source plan from `docs/04.execution/plans/`
- Uses `docs/99.templates/task.template.md`
- Outputs to `docs/04.execution/tasks/YYYY-MM-DD-<topic>.md`

## Agents

- **doc-writer** — primary caller

## Skills

- `.claude/skills/task-breakdown-agent/skill.md`

## Usage

- **Inputs:** source plan, task template, verification commands from plan
- **Outputs:** new or updated task file, updated execution README entry

## Related Documents

- `../../scopes/docs.md`
- `../../rules/stage-authoring-matrix.md`
- `../README.md`
