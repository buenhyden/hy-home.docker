---
title: "Subagent Model and Routing Text"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0217"
parent_ids:
- "REQ-0024"
- "AD-0027"
created: "2026-10-08"
---

# Subagent Model and Routing Text

## Overview

The generated Claude subagents run on the current Claude generation, and each
subagent description tells the delegating model when to use that role. Before
this package the Provider Registry pinned `claude-opus-5` and `claude-sonnet-5`,
and every generated description read "Canonical {scope} role for {id}; owned by
canonical agent governance.", which carries no routing signal.

## Scope

Included: the Claude `work_profiles` and `models` entries in the Provider
Registry, the renderer's description function and its generated-file check,
the regenerated `.claude/agents/` and `.codex/agents/` projections, and a
regression test.

Excluded: the Haiku `routine-validation` profile, Codex model selections,
effort values, role sources under `.agents/roles/`, and Stage 90 research that
cites the earlier models.

## Contracts

1. The Claude `adversarial-review` and `long-horizon-supervision` profiles use
   `claude-opus-5-5`; `complex-implementation` and `evidence-research` use
   `claude-sonnet-5-5`. Effort values are unchanged.
2. A generated subagent description is the role's `## Overview` paragraph
   followed by `Use when:` and the role's `### Use When` cases, for Claude and
   Codex alike.
3. The renderer fails when a role lacks either section, instead of emitting a
   description without routing text.

## Acceptance Criteria

1. The description test fails for every role before the renderer change and
   passes after it.
2. `provider_surface_renderer.py --check` reports no drift and the agent
   governance contract check passes.
3. No authored surface outside Stage 90 and Stage 98 still names
   `claude-opus-5` or `claude-sonnet-5`.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-subagent-model-and-routing-text.md)
- [Provider Registry](../../../.agents/governance/providers/registry.yaml)
