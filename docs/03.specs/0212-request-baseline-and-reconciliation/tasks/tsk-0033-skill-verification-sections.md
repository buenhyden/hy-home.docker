---
title: "Skill Verification Sections Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0033"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Skill Verification Sections Task

## Overview

### Objective

Execute W49: give every canonical skill a `Verification` section that states
how success is checked (request line L340), and require it for new skills.
This Task owns criterion 44 only.

## Inputs and Authorization

On 2026-10-29 the owner asked for every gap offered after TSK-0029 to be
done, and then directed that governance documents be written in English. The
input is `main` at merged PR #629. The authorization covers these edits, this
branch, its pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0033 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0033 | ready | in-progress | #objective |
| SPEC-0212-TSK-0033 | in-progress | completed | #evidence |

### Changes

- Each of the 24 `.agents/skills/*/SKILL.md` files gains `## Verification`
  between `## Outputs` and `## Failure Handling`. It has three observable
  success conditions, drawn from that skill's own Procedure, Gates, and
  Outputs. Each skill's minor version goes up by one.
- The conditions name only commands and assets that exist:
  `check-document-metadata.py`, `check-document-links.py`,
  `check-github-workflow-contract.py`, `validate-docker-compose.sh`,
  `run-ci-precommit.sh`, and each skill's own `scripts/` and `assets/` files.
- The Registry `governance-skill` profile lists `Verification` as a required
  section after `Outputs`.
- `skill.template.md` gains the same section with a
  `{{OBSERVABLE_SUCCESS_CONDITIONS}}` placeholder.
- The new prose is English, under the language rule of TSK-0032.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Section coverage | 44 | W49 | `grep -c '^## Verification' .agents/skills/*/SKILL.md` | This branch | PASS | 24 files, one section each | required | - |
| Metadata contracts | 44 | W49 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations with `Verification` required | required | - |
| Registry and heading tests | 44 | W49 | `python3 -m unittest tests.lib.document_governance.test_registry tests.lib.document_governance.test_language tests.lib.document_governance.metadata.test_heading` | This branch | PASS | 223 tests OK | required | - |
| Language check | 44 | W49 | `check-document-links.py --mode language` | This branch | PASS | 0 failures | required | - |
| Provider projections | 44 | W49 | `provider_surface_renderer.py --check` | This branch | PASS | 2 providers, 0 drift | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 44 | accepted | Section coverage, Metadata contracts, Registry and heading tests, Language check, Provider projections | Every skill states its observable success conditions, and the Registry requires the section for new skills. | SPEC-0212 TSK-0033 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Request line meaning audit](tsk-0029-request-line-meaning-audit.md)
