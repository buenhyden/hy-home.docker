---
layer: agentic
---

# Agent and Function Catalog

## Overview

This catalog documents the agents and orchestration functions used in the current workspace. It consolidates responsibilities, inputs and outputs, and linkage to governance rules without referencing any source example set.

## Purpose

Provide a single, English-only source of truth for agent roles and reusable orchestration functions so that governance, routing, and documentation stay consistent.

## Scope

**Covers:**

- Agent definitions used in this workspace
- Orchestration functions mirrored from runtime skills
- Links to governing scopes and rules

**Excludes:**

- Product, architecture, or implementation details (see `docs/01`–`docs/11`)
- External harness references or identifiers

## Structure

- `agents/` — per-agent role documentation
- `functions/` — per-function documentation mirrored from `.claude/skills/<name>/skill.md`

## Agents

- [workflow-supervisor](agents/workflow-supervisor.md)
- [code-reviewer](agents/code-reviewer.md)
- [doc-writer](agents/doc-writer.md)
- [drift-detector](agents/drift-detector.md)
- [iac-reviewer](agents/iac-reviewer.md)
- [incident-responder](agents/incident-responder.md)
- [infra-implementer](agents/infra-implementer.md)
- [security-auditor](agents/security-auditor.md)

## Functions

- [code-reviewer](functions/code-reviewer.md)
- [security-audit](functions/security-audit.md)
- [infra-validate](functions/infra-validate.md)
- [infra-cross-validate](functions/infra-cross-validate.md)
- [incident-response](functions/incident-response.md)
- [docker-compose-patterns](functions/docker-compose-patterns.md)
- [container-threat-modeling](functions/container-threat-modeling.md)
- [code-review-dimensions](functions/code-review-dimensions.md)
- [adr-writing](functions/adr-writing.md)
- [ci-cd-patterns](functions/ci-cd-patterns.md)

## Usage

- Use this catalog when updating `.claude/agents/` or `.claude/skills/<name>/skill.md`.
- Keep agent docs aligned with their scope files under `docs/00.agent-governance/scopes/`.

## Artifacts

- `_workspace/` (agent- and function-specific outputs)

## Related Documents

- `../README.md`
- `../subagent-protocol.md`
- `../rules/documentation-protocol.md`
- `../scopes/`
- `../../../.claude/CLAUDE.md`
