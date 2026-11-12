---
title: "README and Agent Guide Split Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0251-PLAN-0001"
parent_ids:
- "SPEC-0251"
created: "2026-11-03"
---

# README and Agent Guide Split Plan

## Overview

### Goal and Boundary

Add the placement rule, register the folder guide profile, write the nine
guides, move agent-directed README sections into them, and let the stage
loaders accept the new file.

The files named in the Spec; no runtime or remote state changes.

Parent Spec: [Spec](spec.md)

### Assumptions

The plan works under the approved Spec and assumes no authority beyond it.

## Dependencies

### Prerequisites

The approved Spec.

### Dependency Order

W1 has no dependency; W2 starts after W1; W3 starts after W2; W4 records the results after W1 to W3.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Documentation protocol rule, language rule, bootstrap step, provider loading notes, stage authoring matrix kind | None | TSK-0001 | agent governance contract; renderer parity |
| W2 | 2, 4 | Registry `folder-agent-guide` profile, template and owned paths; stage loaders, operations catalog, Stage 90 corpus and navigation accept `AGENTS.md` | W1 | TSK-0001 | metadata check-changed; operations catalog; document-governance suites |
| W3 | 2, 3 | Write the nine AGENTS.md files; move README agent sections | W2 | TSK-0001 | links alignment, navigation, language |
| W4 | 4 | Record local results | W1–W3 | TSK-0001 | the checks above |

### Change and Rollback

Revert the branch to remove the guides and restore the READMEs; no outside state changes.

## Verification Plan

### Verification Matrix

Run `check-document-metadata.py` in `check-changed` and `check-active` modes,
`check-document-corpus-lifecycle.py`, `check-operations-catalog.py`,
`check-document-links.py` in `alignment`, `navigation`, `language`,
`entrypoint` and `commands` modes, `check-agent-governance-contract.py`,
`provider_surface_renderer.py --check`, `check-script-manifest.py`, and the
document-governance and CI routing unit suites.

### Stage Placement

The Plan places no stage-specific checks beyond the Verification Matrix; the Task records each run.

## Risks

### Risks and Mitigations

A loader that still rejects `AGENTS.md` fails its stage check, which W2 runs.

### Escalation

The Spec states: "This Task pushes nothing and merges nothing."

## Promotion Map

### Durable Meaning

The placement rule, the `folder-agent-guide` profile and the nine guides live in the documentation protocol, the Registry and the folder `AGENTS.md` files named in the Spec.

### Owner and Receipt

The owner is @buenhyden; the receipt is the Task named in the Work Breakdown.

- [Task](tasks/tsk-0001-readme-and-agents-guide-split.md)
