---
title: "Folder Guide Delivery Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0264-PLAN-0001"
parent_ids:
- "SPEC-0264"
created: "2026-11-06"
---

# Folder Guide Delivery Plan

## Overview

The change is already implemented on branch `feat/folder-agents-guide-hook`.
This Plan records the work units and the evidence that closes them.

## Scope

The scope and exclusions are those of SPEC-0264.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2, 3, 4, 5 | Folder guide library, dispatcher wiring, tests and manifest entry | None | TSK-0001 | `test_folder_guides`; hook, manifest and entrypoint suites; `check-script-manifest.py` |
| W2 | 6 | Describe the delivery in both provider adapters | W1 | TSK-0001 | `provider_surface_renderer.py --check` |
| W3 | 7 | Audit the folder `AGENTS.md` files | None | TSK-0001 | `check-agent-governance-contract.py --mode repository` |
| W4 | 8 | Owner observes delivery in live Claude and Codex sessions | W1, W2 | TSK-0001 | Owner step in the Task |

## Verification Plan

Run the checks named in the table and the document checks of
`docs/03.specs/AGENTS.md`. Criterion 8 needs owner observation.

## Risks and Recovery

### Risks and Rollback

Native delivery may differ from the dispatcher tests; W4 catches this. Rollback
removes the hook branch in `agent-event-hook.sh` and the provider adapter text.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-deliver-folder-guides.md)
