---
title: "Folder Guide Delivery Plan"
version: "0.4.2"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0264-PLAN-0001"
parent_ids:
- "SPEC-0264"
created: "2026-11-06"
---

# Folder Guide Delivery Plan

## Overview

### Goal and Boundary

The change is already implemented on branch `feat/folder-agents-guide-hook`.
This Plan records the work units and the evidence that closes them.

The scope and exclusions are those of SPEC-0264.

Parent Spec: [Spec](spec.md)

### Assumptions

The plan works under the approved SPEC-0264; the scope and exclusions are those of the Spec, and the change is already implemented on branch `feat/folder-agents-guide-hook`.

## Dependencies

### Prerequisites

The approved Spec.

### Dependency Order

W1, W3 and W5 have no dependencies; W2 starts after W1; W4 starts after W1 and W2.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2, 3, 4, 5 | Folder guide library, dispatcher wiring, tests and manifest entry | None | TSK-0001 | `test_folder_guides`; hook, manifest and entrypoint suites; `check-script-manifest.py` |
| W2 | 6 | Describe the delivery in both provider adapters | W1 | TSK-0001 | `provider_surface_renderer.py --check` |
| W3 | 7 | Audit the folder `AGENTS.md` files | None | TSK-0001 | `check-agent-governance-contract.py --mode repository` |
| W4 | 8 | Controller observes delivery in live Claude and Codex sessions (assigned by the owner), and confirms Codex sends SessionStart `source` `compact`, on which re-delivery after compaction depends | W1, W2 | TSK-0001 | Live observation in the Task |
| W5 | 1, 9, 10 | Render the folder `CLAUDE.md` import shims, admit them in the stage loaders and checks, and describe them in the documentation protocol | None | TSK-0001 | renderer tests in `test_validator_entrypoints`; `provider_surface_renderer.py --check`; metadata, link, contract and manifest checks |

### Change and Rollback

Rollback removes the hook branch in `agent-event-hook.sh` and the provider adapter text.
Rolling back W5 removes the shim records from the renderer, then `--write`
quarantines the shims for manual cleanup.

## Verification Plan

### Verification Matrix

Run the checks named in the table and the document checks of
`docs/03.specs/AGENTS.md`. Criterion 8 needs owner observation.

### Stage Placement

The Plan places no stage-specific checks beyond the Verification Matrix; the Task records each run.

## Risks

### Risks and Mitigations

Native delivery may differ from the dispatcher tests; W4 catches this.

### Escalation

Criterion 8 needs owner observation in live Claude and Codex sessions; work stops there until the owner supplies it.

## Promotion Map

### Durable Meaning

The folder guide delivery lives in the folder guide library, the dispatcher, both provider adapters and the documentation protocol.

### Owner and Receipt

Owner @buenhyden. The receipt is TSK-0001, named in the Work Breakdown Task column.

- [Task](tasks/tsk-0001-deliver-folder-guides.md)
