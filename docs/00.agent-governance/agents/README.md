---
layer: agentic
---

# Agent and Function Catalog

## Overview

This catalog documents the agents and orchestration functions used in the current workspace. It consolidates responsibilities, inputs/outputs, and linkage to governance rules without referencing external harness sources.

## Purpose

Provide a single, English-only source of truth for agent roles and reusable orchestration functions so that governance, routing, and documentation stay consistent.

## Scope

**Covers:**

- Agent definitions used in this workspace
- Orchestration functions (skills) used by agents
- Links to governing scopes and rules

**Excludes:**

- Product, architecture, or implementation details (see `docs/01`–`docs/11`)
- External harness references or identifiers

## Structure

- `agents/` — per-agent role documentation
- `functions/` — per-function (skill) documentation

## Agents

- [code-reviewer](agents/code-reviewer.md)
- [doc-writer](agents/doc-writer.md)
- [iac-reviewer](agents/iac-reviewer.md)
- [incident-responder](agents/incident-responder.md)
- [infra-implementer](agents/infra-implementer.md)
- [security-auditor](agents/security-auditor.md)

## Functions

- [infra-validate](functions/infra-validate.md)
- [infra-cross-validate](functions/infra-cross-validate.md)
- [incident-response](functions/incident-response.md)

## Usage

- Use this catalog when updating `.claude/agents/` or `.claude/skills/`.
- Keep agent docs aligned with their scope files under `docs/00.agent-governance/scopes/`.

## Artifacts

- `_workspace/` (agent- and function-specific outputs)

## Related Documents

- `../README.md`
- `../subagent-protocol.md`
- `../rules/documentation-protocol.md`
- `../scopes/`
