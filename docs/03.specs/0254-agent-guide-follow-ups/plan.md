---
title: "Agent Guide Follow-ups Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0254-PLAN-0001"
parent_ids:
- "SPEC-0254"
created: "2026-11-04"
---

# Agent Guide Follow-ups Plan

## Overview

Replace the outside-docs stage links, add the CI routing rule and its test,
rename the guide type, and activate the guides.

## Scope

The files named in the Spec; no runtime or remote state changes.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Plain-text identities in the nine `infra` README lines | None | TSK-0001 | links entrypoint |
| W2 | 2 | Workflow-contract rule for the seven guides that did not select agent-governance; routing test | None | TSK-0001 | CI routing tests |
| W3 | 3 | `common/agent-guide` in the Registry, template, guides, matrix and protocol; guides to `active` | None | TSK-0001 | metadata check-changed and check-active |
| W4 | 4 | Record local results | W1–W3 | TSK-0001 | the checks above |

## Verification Plan

Run `check-document-links.py` in `alignment`, `navigation`, `language`,
`traceability`, `entrypoint` and `commands` modes, `check-document-metadata.py`
in `check-changed` and `check-active` modes,
`check-document-corpus-lifecycle.py`, `check-agent-governance-contract.py`,
`provider_surface_renderer.py --check`, `check-script-manifest.py`, and the
document-governance and CI routing unit suites.

## Risks and Recovery

### Risks and Rollback

A narrower rule would shrink selection for a path that previously selected
every suite; the rule lists only the seven guides that did not select
agent-governance. Revert the branch to restore the previous state; no outside
state changes.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-agent-guide-follow-ups.md)
