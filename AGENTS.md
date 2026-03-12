# Project Template Agent Guide

This repository uses layered agent documentation. Start here, then load only the linked material needed for the task.

## Core Contract

- Adopt the **Principal Agentic Architect** baseline and load task-specific rules from `.agent/rules/`.
- Follow spec-first execution: confirm or create a relevant spec and implementation plan before feature or refactor work.
- Discover and apply the best-matching skill before specialized work.
- Ground changes in terminal evidence and verify results before claiming completion.
- Use repository templates from `templates/` for new technical artifacts.
- Keep repository documentation links relative and prefer isolated work contexts when parallel work could collide.

## Load Order

- `[LOAD:INDEX]` [Documentation index](docs/README.md)
- `[LOAD:TACTICAL]` [Shared governance](.claude/agent-instructions/core-governance.md)
- `[LOAD:TACTICAL]` [Shared workflow](.claude/agent-instructions/workflow.md)

## Provider Directives

- [Claude directive](CLAUDE.md)
- [Gemini directive](GEMINI.md)

## Rule Map

- [Agent personas and standards](.agent/rules/0000-Agents/)
- [Documentation standards](.agent/rules/2100-Documentation/)
- [Security rules](.agent/rules/2200-Security/)
- [Performance rules](.agent/rules/2300-Performance/)
