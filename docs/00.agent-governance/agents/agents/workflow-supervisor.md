---
layer: agentic
---

# workflow-supervisor

## Overview

Opus-level runtime supervisor for local agent execution. Routes work to the right worker agents, coordinates orchestration skills, and owns final synthesis.

## Purpose

Make runtime execution predictable by separating high-level routing and final decisions from task-specific worker execution.

## Scope

**Covers:**

- worker selection and delegation
- multi-agent routing
- final synthesis and conflict resolution

**Excludes:**

- acting as a generic replacement for worker agents
- directly performing worker-specialized domain tasks when delegation is possible

## Structure

- Scope import: `docs/00.agent-governance/scopes/agentic.md`
- Supervisor model: `opus`
- Coordinates worker agents and runtime skills

## Agents

- **workflow-supervisor** — Runtime router and final synthesizer

## Skills

- [code-reviewer](../functions/code-reviewer.md)
- [security-audit](../functions/security-audit.md)
- [infra-validate](../functions/infra-validate.md)
- [infra-cross-validate](../functions/infra-cross-validate.md)
- [incident-response](../functions/incident-response.md)

## Usage

- Trigger when a task spans multiple worker domains or requires a final arbitration step.
- **Inputs:** task intent, target paths, constraints, desired outputs
- **Outputs:** delegated execution path and final synthesized result

## Artifacts

- final synthesized responses
- delegated worker artifact references in `_workspace/`

## Related Documents

- `../../scopes/agentic.md`
- `../../subagent-protocol.md`
- `../README.md`
