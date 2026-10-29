---
title: "Partial Gap Rules Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0035"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Partial Gap Rules Task

## Overview

### Objective

Execute W51: write the missing rule text behind the partly met request lines
that TSK-0029 recorded, and record the lines already closed by later Tasks.
This Task owns criterion 46 only.

## Inputs and Authorization

On 2026-10-29 the owner asked for the remaining partly met lines to be
handled the same way and chose all four groups: rule text, investigation
records, open Spec reconciliation, and owner decisions. This Task is the rule
text group. The input is `main` at merged PR #631. The authorization covers
these policy edits, this branch, its pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0035 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0035 | ready | in-progress | #objective |
| SPEC-0212-TSK-0035 | in-progress | completed | #evidence |

### Rules added

| Line | CR | Rule | Owner |
| --- | --- | --- | --- |
| L059 | CR-08.06 | Archive work is a disposition inside the current Task, never a new Spec project, and a closed Spec gets no new standing pipeline | `documentation-protocol.md` 3.7.0 |
| L084 | CR-13.01 | A pull request carries one Spec Package's work, possibly several of its Tasks as separate commits, and never mixes Specs | `git-workflow.md` 1.6.0 |
| L117 | CR-11.04 | QA optimization order, with a reproducible before-and-after measure and no new global cache or gate first | `quality-standards.md` 1.8.0 |
| L159, L316 | CR-15.01 | `AGENTS.md` and `CLAUDE.md` are entry shims and tool-neutral rules live in `.agents/governance/`; provider names appear under `.agents/` only as Registry translation facts and the capability matrix | `bootstrap.md` 1.7.0 |
| L176 | CR-18.04 | No paid model API is called, so no repository rate-limit, token, or retry policy applies; adding one needs a Spec stating those limits first | `agentic.md` 1.7.0 |
| L177 | CR-15.08 | No automatic PR reviewer or test generator; both would call a model API | `agentic.md` 1.7.0 |
| L179, L180 | CR-20.03 | A non-functional requirement names one ISO/IEC 25010 characteristic and an ISO/IEC 25023 measure; a characteristic left out states why; no separate gate | `quality-standards.md` 1.8.0 |
| L223, L224 | CR-13.01 | Start a new branch or worktree from the latest committed state; never stash, reset, discard, or force-commit user work | `git-workflow.md` 1.6.0 |
| L242, L243 | CR-17.02 | The `short-term`, `long-term`, and `domain` memory tiers are a use classification and never a deletion deadline | `environment-constraints.md` 1.8.0 |
| L250 | CR-21.03 | Codex keeps its default approval mode with no tracked `approval_policy`; in-scope edits are authorized by the request, matching Claude's `autoMode` | `.codex/provider.md` 1.3.0 |
| L265 | CR-17.02 | A memory record body states the reason, what failed and how it was fixed, and the reuse condition | `environment-constraints.md` 1.8.0 |
| L272 | CR-03.04 | Research, drafts, and isolated trials never require a future approval, commit, or digest; activating a shared norm needs its approval first, and a valid earlier approval is reused | `sdlc.md` 1.5.0 |
| L294 | CR-07.03 | Inside `docs/`, link to Stage 99 templates and Stage 05 operations for shape and procedure; write everything else in the document | `documentation-protocol.md` 3.7.0 |

### Lines already closed by later Tasks

| Line | Closed by |
| --- | --- |
| L112 | TSK-0034 moved the Migration 0003 constants out of the general archive module |
| L152 | TSK-0031 added the no-progress and cancellation loop exits |
| L155, L156, L158 | TSK-0029 corrected the `_workspace` statement in `environment-constraints.md` |
| L283, L383 | TSK-0031 recorded why skills are adapters and not symlinks |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Agent governance | 46 | W51 | `check-agent-governance-contract.py` | This branch | PASS | 0 failures | required | - |
| Provider projections | 46 | W51 | `provider_surface_renderer.py --check` | This branch | PASS | 2 providers, 0 drift | required | - |
| Language check | 46 | W51 | `check-document-links.py --mode language` | This branch | PASS | 0 failures | required | - |
| Routing tests | 46 | W51 | `python3 -m unittest tests.validation.test_agent_governance_ci_routing` | This branch | PASS | OK | required | - |
| Metadata contracts | 46 | W51 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 46 | accepted | Agent governance, Provider projections, Language check, Routing tests, Metadata contracts | Every rule-text gap in the partly met lines now has its rule in one canonical owner. | SPEC-0212 TSK-0035 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Request line meaning audit](tsk-0029-request-line-meaning-audit.md)
