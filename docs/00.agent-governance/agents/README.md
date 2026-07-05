---
layer: agentic
---

# Agent and Function Catalog

## Overview

This catalog documents the agents and orchestration functions used in the current workspace. It consolidates responsibilities, inputs and outputs, and linkage to governance rules without referencing any source example set.

## Audience

This README is for:

- AI Agents
- Documentation Writers
- Repository Maintainers

## Purpose

Provide a single, English-only source of truth for agent roles and reusable orchestration functions so that governance, routing, and documentation stay consistent.

## Scope

**Covers:**

- Agent definitions used in this workspace
- Orchestration function catalog entries corresponding to runtime skills
- Links to governing scopes and rules

**Excludes:**

- Product, architecture, or implementation details (see `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/99.templates`)
- External harness references or identifiers

## Structure

- `agents/` — per-agent role documentation
- `functions/` — per-function catalog entries corresponding to runtime skill implementations across providers

## Agents

- [workflow-supervisor](./agents/workflow-supervisor.md)
- [ci-cd-engineer](./agents/ci-cd-engineer.md)
- [code-reviewer](./agents/code-reviewer.md)
- [doc-writer](./agents/doc-writer.md)
- [drift-detector](./agents/drift-detector.md)
- [hook-developer](./agents/hook-developer.md)
- [iac-reviewer](./agents/iac-reviewer.md)
- [incident-responder](./agents/incident-responder.md)
- [infra-implementer](./agents/infra-implementer.md)
- [qa-engineer](./agents/qa-engineer.md)
- [rules-engineer](./agents/rules-engineer.md)
- [security-auditor](./agents/security-auditor.md)
- [skill-creator](./agents/skill-creator.md)
- [style-enforcer](./agents/style-enforcer.md)
- [wiki-curator](./agents/wiki-curator.md)

## Functions

- [code-reviewer](./functions/code-reviewer.md)
- [security-audit](./functions/security-audit.md)
- [infra-validate](./functions/infra-validate.md)
- [infra-cross-validate](./functions/infra-cross-validate.md)
- [incident-response](./functions/incident-response.md)
- [docker-compose-patterns](./functions/docker-compose-patterns.md)
- [container-threat-modeling](./functions/container-threat-modeling.md)
- [code-review-dimensions](./functions/code-review-dimensions.md)
- [adr-writing](./functions/adr-writing.md)
- [ci-cd-patterns](./functions/ci-cd-patterns.md)
- [deployment-pipeline-design](./functions/deployment-pipeline-design.md)
- [e2e-testing](./functions/e2e-testing.md)
- [workspace-audit-revalidation](./functions/workspace-audit-revalidation.md)
- [compose-stack-agent](./functions/compose-stack-agent.md)
- [execution-plan-agent](./functions/execution-plan-agent.md)
- [knowledge-map-agent](./functions/knowledge-map-agent.md)
- [policy-gate-agent](./functions/policy-gate-agent.md)
- [requirements-to-design-agent](./functions/requirements-to-design-agent.md)
- [task-breakdown-agent](./functions/task-breakdown-agent.md)
- [ops-runbook-agent](./functions/ops-runbook-agent.md)
- [style-validation](./functions/style-validation.md)
- [test-automator](./functions/test-automator.md)

## Function / Skill Lifecycle

Workspace functions and provider skill adapters use the same lifecycle terms:

1. **Discovery**: identify requested or applicable functions/skills before mutation.
2. **Applicability**: decide whether the function/skill changes the workflow,
   artifact, or validation scope.
3. **Provider loading**: load the runtime-specific skill or adapter instructions
   needed for the task.
4. **Canonical artifact**: write outputs to the repository's canonical stage or
   runtime surface.
5. **Validation evidence**: record commands, outcomes, CI-only gates, and
   skipped-check rationale.

Provider-local `skill.md` or `SKILL.md` files may describe runtime mechanics;
the lifecycle policy remains in Stage 00.

## How to Work in This Area

- Use this catalog when updating `.claude/agents/`, `.agents/agents/`, `.codex/agents/*.toml`, or provider runtime notes.
- Note that `.agents/skills/` is the Gemini-compatible surface, `.claude/skills/` is the Claude runtime surface, and `.codex/skills/` is the Codex runtime surface.
- Keep agent docs aligned with their scope files under `docs/00.agent-governance/scopes/`.
- Keep this catalog free of external harness identifiers.
- Update links here when agent or function files are added, moved, or removed.

## Related Documents

- `../README.md`
- `../subagent-protocol.md`
- `../rules/documentation-protocol.md`
- `../scopes/`
- `../../../.claude/CLAUDE.md`
