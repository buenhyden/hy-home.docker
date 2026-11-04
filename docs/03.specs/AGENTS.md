---
title: "Specifications Agent Guide"
version: "0.2.0"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-04"
---

# Specifications Agent Guide

## Overview

Stage 03 holds Spec Packages: a Spec contracts the change, a Plan sequences
it, and Tasks record execution and evidence. This guide routes an agent that
creates or executes a package. The human guide is [README.md](README.md).

## Scope

`####-<slug>/spec.md`, `plan.md`, `tasks/tsk-####-<slug>.md`, `contracts/`
and this folder's README. Long-lived requirements, architecture and operating
procedures belong to Stage 01, Stage 02 and Stage 05.

## Working Rules

- Load the governing Spec, Plan and current Task before any repository change,
  and record progress, decisions and evidence in that Task.
- Create documents from
  [`spec.template.md`](../99.templates/templates/specs/spec.template.md),
  [`plan.template.md`](../99.templates/templates/specs/plan.template.md) and
  [`task.template.md`](../99.templates/templates/specs/task.template.md).
  Allocate the next Spec number from the Registry `spec` space and advance its
  high-water mark in the same change.
- Record each check as an Evidence row with an honest result from the
  Registry `result_domain` in [`registry.json`](../99.templates/registry.json)
  and the revision it examined. What a row may
  `Resolve` is defined by the [SDLC](../../.agents/governance/sdlc.md#sequence)
  and the Registry `evidence_columns` contract.
- Never edit the body of a terminal Task. Record a later correction in the
  current Task instead.
- Remove a package only as the
  [retirement preconditions](../../.agents/governance/documentation-protocol.md#retirement-preconditions)
  and the [SDLC](../../.agents/governance/sdlc.md#sequence) readiness and
  approval sequence define it.
- Write prose in English, per the profile `language`.

## Canonical References

- [Bootstrap](../../.agents/governance/bootstrap.md),
  [SDLC](../../.agents/governance/sdlc.md),
  [workflows](../../.agents/governance/workflows.md),
  [documentation protocol](../../.agents/governance/documentation-protocol.md),
  [task checklists](../../.agents/governance/task-checklists.md),
  [quality standards](../../.agents/governance/quality-standards.md).
- Roles: [`workflow-supervisor`](../../.agents/roles/workflow-supervisor.md),
  [`code-reviewer`](../../.agents/roles/code-reviewer.md).
- Skills: [`execution-plan-agent`](../../.agents/skills/execution-plan-agent/SKILL.md),
  [`task-breakdown-agent`](../../.agents/skills/task-breakdown-agent/SKILL.md),
  [`change-review-execution`](../../.agents/skills/change-review-execution/SKILL.md).
- Prompt: [handoff](../../.agents/prompts/handoff.md).
- Provider loading: [Claude adapter](../../.claude/provider.md),
  [Codex adapter](../../.codex/provider.md).

## Verification

- `python3 scripts/validation/check-document-corpus-lifecycle.py`
- `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main`
- `python3 scripts/validation/check-document-links.py --mode alignment`
- `python3 scripts/validation/check-document-links.py --mode commands`

## Related Documents

- [Specifications README](README.md)
- [Task template](../99.templates/templates/specs/task.template.md)
