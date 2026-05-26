---
layer: agentic
---

# ops-runbook-agent

## Overview

Authors and maintains Stage 05 runbook documents in
`docs/05.operations/runbooks/`. Runbooks define ordered procedures, expected
output, failure-stop criteria, rollback steps, and escalation paths.

## Purpose

Produce runbook documents that an operator can follow step-by-step during
incidents or routine operations.

## Scope

**Covers:**

- Ordered procedure authoring with expected output per step
- Failure-stop and rollback criteria
- Escalation path documentation

**Excludes:**

- Secret values, tokens, or credential content
- Incident timeline recording (handled by incidents/ bucket)

## Structure

- Reads service spec from `docs/03.specs/<tier>/spec.md`
- Uses `docs/99.templates/operation.template.md`
- Outputs to `docs/05.operations/runbooks/<tier>/<topic>.md`

## Agents

- **doc-writer** — primary caller

## Skills

- `.claude/skills/ops-runbook-agent/skill.md`

## Usage

- **Inputs:** service spec, operations template, existing runbooks
- **Outputs:** new or updated runbook, updated runbooks README index

## Related Documents

- `../../scopes/docs.md`
- `../../rules/stage-authoring-matrix.md`
- `../README.md`
