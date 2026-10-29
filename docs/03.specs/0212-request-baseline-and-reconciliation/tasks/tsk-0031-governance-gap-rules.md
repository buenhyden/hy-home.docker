---
title: "Governance Gap Rules Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0031"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Governance Gap Rules Task

## Overview

### Objective

Execute W47: add the five missing rules that TSK-0029 found for request lines
L047, L171, L175, L292, and L369. This Task owns criterion 42 only.

## Inputs and Authorization

On 2026-10-29 the owner asked for every gap offered after TSK-0029 to be
done. The input is `main` at merged PR #627. The authorization covers these
policy edits, this branch, its pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0031 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0031 | ready | in-progress | #objective |
| SPEC-0212-TSK-0031 | in-progress | completed | #evidence |

### Rules added

| Line | CR | Rule | Owner |
| --- | --- | --- | --- |
| L047 | CR-03.02 | The owner, who owns all four repositories, is the one joint decision maker for a shared meaning; each repository records its own adoption | `.agents/governance/approval-boundaries.md` 1.3.0 |
| L171 | CR-18.05 | Every agent loop has five exits: success, failure, no progress, budget, and cancellation. Two iterations in a row with no change end it; a cancellation ends it at once | `.agents/governance/agentic.md` 1.6.0 |
| L175 | CR-15.07 | Editor shortcuts, code actions, and inline edit are personal IDE settings, not repository surfaces; no separate documentation hook, because the PostToolUse hook already checks documents | `.agents/governance/agentic.md` 1.6.0 |
| L292 | CR-21.02 | The single-developer review path is the required check, a fresh-context review of the final diff, and the owner's merge; it calls no AI-agent API | `.agents/governance/github-governance.md` 1.5.0 |
| L369 | CR-15.10 | Claude skills are generated adapters, not symlinks, so canonical skills stay explicitly invoked and provider-neutral; Codex reads `.agents/skills/` directly | `.claude/provider.md` 1.4.0 |

### Facts checked

- `git grep` finds no model-provider endpoint, API key name, or agent review
  action in `.github/`, `scripts/`, `.claude/hooks/`, `.codex/`, or
  `.agents/governance/hooks/`, so the no-API rule matches the code.
- `.vscode/` and `.idea/` are ignored and only `.editorconfig` is tracked.
- A generated `.claude/skills/*/SKILL.md` carries
  `disable-model-invocation: true`; the canonical `.agents/skills/*/SKILL.md`
  does not, which is why a symlink would change invocation.
- Whether Claude Code would follow a skill symlink was not tested; the
  decision rests on invocation, not on support.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Agent governance | 42 | W47 | `check-agent-governance-contract.py` | This branch | PASS | 0 failures | required | - |
| Provider projections | 42 | W47 | `provider_surface_renderer.py --check` | This branch | PASS | 2 providers, 0 drift | required | - |
| Routing tests | 42 | W47 | `python3 -m unittest tests.validation.test_agent_governance_ci_routing` | This branch | PASS | 82 tests OK | required | - |
| Metadata contracts | 42 | W47 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 42 | accepted | Agent governance, Provider projections, Routing tests, Metadata contracts | The five rules TSK-0029 found missing now exist, each in its canonical owner. | SPEC-0212 TSK-0031 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Request line meaning audit](tsk-0029-request-line-meaning-audit.md)
