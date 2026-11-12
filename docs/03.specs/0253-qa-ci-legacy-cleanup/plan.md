---
title: "QA and CI Legacy Cleanup Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0253-PLAN-0001"
parent_ids:
- "SPEC-0253"
created: "2026-11-04"
---

# QA and CI Legacy Cleanup Plan

## Overview

### Goal and Boundary

Remove the empty frozen boundary, repoint the evidence owner, fix the command
block and stale wording, and inventory one-off and legacy items.

The files named in the Spec; no runtime or remote state changes.

Parent Spec: [Spec](spec.md)

### Assumptions

The plan works under the approved Spec and assumes no authority beyond it.

## Dependencies

### Prerequisites

The approved Spec.

### Dependency Order

W1 and W2 have no dependency; W3 starts after W1 and W2; W4 records the results after W1 to W3.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Remove the pre-commit frozen boundary and the hook code and tests that read it | None | TSK-0001 | CI routing tests |
| W2 | 1 | Repoint the CI gate evidence owner in the workflow contract and its readers | None | TSK-0001 | gate evidence and workflow contract tests |
| W3 | 1, 2 | Fix the DATA-0096 command block and stale wording; inventory one-off and legacy items | W1, W2 | TSK-0001 | links alignment and commands; Script Manifest |
| W4 | 3 | Record local results | W1–W3 | TSK-0001 | the checks above |

### Change and Rollback

Revert the branch to restore the boundary and the label; no outside state changes.

## Verification Plan

### Verification Matrix

Run the gate evidence, workflow contract, CI routing, CI gate plan and Script
Manifest unit suites, `check-script-manifest.py`, `check-document-metadata.py
--mode check-changed`, `check-document-corpus-lifecycle.py`,
`check-document-links.py` in `alignment` and `commands` modes,
`provider_surface_renderer.py --check` and
`check-agent-governance-contract.py`.

### Stage Placement

The Plan places no stage-specific checks beyond the Verification Matrix; the Task records each run.

## Risks

### Risks and Mitigations

A hook test that relied on the boundary fails in W1.

### Escalation

The Spec states: "This Task pushes and merges nothing."

## Promotion Map

### Durable Meaning

The removed boundary, the repointed CI gate evidence owner and the cleaned command block live in the workflow contract, its readers and the documents named in the Spec.

### Owner and Receipt

The owner is @buenhyden; the receipt is the Task named in the Work Breakdown.

- [Task](tasks/tsk-0001-qa-ci-legacy-cleanup.md)
