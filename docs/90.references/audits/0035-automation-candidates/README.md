---
profile_id: audit
status: superseded
artifact_id: AUD-0035
artifact_type: audit
parent_ids:
- AUD-0026
created: '2026-07-07'
updated: '2026-08-23'
observed_at: '2026-07-07'
superseded_by: AUD-0021
---

# Reference: Superseded Automation Candidate Mapping

## Overview

This leaf maps the former 14-candidate roadmap to verified canonical automation evidence.

## Purpose

Preserve useful themes while rejecting unverified IDs, priorities, and implied approvals.

## Repository Role

Superseded provenance only; not an active roadmap or current automation inventory.

## Scope

### In Scope

- Canonical destination and candidate-theme disposition.

### Out of Scope

- Authorizing scripts, CI, hooks, Graphify integration, scanners, release work, or agents.

## Definitions / Facts

| Field | Disposition |
| --- | --- |
| Canonical destination | [Canonical automation audit](ref-0021-automation-candidates.md). |
| Verified merged claims | Semantic eval, controlled all-files pre-commit, SBOM/provenance/signing, broader vulnerability scanning, instruction/provider compatibility, and release/deployment automation are valid bounded themes. |
| Rejected unsupported claims | `AEA-AUTO-014` through `027` as canonical IDs, High/Medium priorities, multi-agent orchestrator requirement, Graphify git-hook adoption, daemon requirements, chosen tool implementations, and immediate roadmap status. |
| Current-truth warning | Use AUT-01 through AUT-11 and the existing AEA-AUTO-001 through 013 disposition ledger; Task 9 owns the wrapper and Task 11 owns runtime/supply-chain/deployment follow-ups. |

## Source Rules

- Candidate status requires tracked evidence and one canonical owner.
- Security/runtime/remote automation requires a separate approved spec/plan.

## Sources

- [Canonical automation audit](ref-0021-automation-candidates.md) - current automation criteria and candidates.

## Maintenance

- **Owner**: Agentic Workflow Specialist / QA Engineer.
- **Review Cadence**: None for current status.
- **Update Trigger**: Supersession-route correction only.

## Related Documents

- [Superseded pack README](ref-0033-readme.md)
- [Canonical audit README](ref-0019-readme.md)

## Objective

This package preserves its existing audit evidence under the Stage 99 `audit` contract.

## Criteria

This package preserves its existing audit evidence under the Stage 99 `audit` contract.

## Evidence

This package preserves its existing audit evidence under the Stage 99 `audit` contract.

## Findings

This package preserves its existing audit evidence under the Stage 99 `audit` contract.

## Conformance

This package preserves its existing audit evidence under the Stage 99 `audit` contract.

## Actions

This package preserves its existing audit evidence under the Stage 99 `audit` contract.

## Traceability

This package preserves its existing audit evidence under the Stage 99 `audit` contract.
