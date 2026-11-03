---
title: "README and Agent Guide Split Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0251-PLAN-0001"
parent_ids:
- "SPEC-0251"
created: "2026-11-03"
---

# README and Agent Guide Split Plan

## Overview

Add the placement rule, register the folder guide profile, write the nine
guides, move agent-directed README sections into them, and let the stage
loaders accept the new file.

## Scope

The files named in the Spec; no runtime or remote state changes.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Documentation protocol rule, language rule, bootstrap step, provider loading notes, stage authoring matrix kind | None | TSK-0001 | agent governance contract; renderer parity |
| W2 | 2, 4 | Registry `folder-agent-guide` profile, template and owned paths; stage loaders, operations catalog, Stage 90 corpus and navigation accept `AGENTS.md` | W1 | TSK-0001 | metadata check-changed; operations catalog; document-governance suites |
| W3 | 2, 3 | Write the nine AGENTS.md files; move README agent sections | W2 | TSK-0001 | links alignment, navigation, language |
| W4 | 4 | Record local results | W1–W3 | TSK-0001 | the checks above |

## Verification Plan

Run `check-document-metadata.py` in `check-changed` and `check-active` modes,
`check-document-corpus-lifecycle.py`, `check-operations-catalog.py`,
`check-document-links.py` in `alignment`, `navigation`, `language`,
`entrypoint` and `commands` modes, `check-agent-governance-contract.py`,
`provider_surface_renderer.py --check`, `check-script-manifest.py`, and the
document-governance and CI routing unit suites.

## Risks and Recovery

### Risks and Rollback

A loader that still rejects `AGENTS.md` fails its stage check, which W2 runs.
Revert the branch to remove the guides and restore the READMEs; no outside
state changes.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-readme-and-agents-guide-split.md)
