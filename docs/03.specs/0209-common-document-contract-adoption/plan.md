---
title: "Common Document Contract Adoption Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "blocked"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0209-PLAN-0001"
parent_ids:
- "SPEC-0209"
created: "2026-10-05"
---

# Common Document Contract Adoption Plan

## Overview

Adopt the approved common-document contract across Stage 99 and current
authored documents. The Task is the only progress and evidence ledger.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Inventory profiles, templates, schemas, authored documents, consumers, and dispositions. | None | TSK-0001 | Whole-stage inventory recorded. |
| W2 | 2 | Align Registry, JSON schemas, and Markdown/non-Python templates with v4. | W1 | TSK-0001 | Focused metadata/schema checks. |
| W3 | 3 | Migrate current authored Markdown and active links; preserve frozen and completed Task bodies. | W2 | TSK-0001 | Focused link and metadata checks. |
| W4 | 4 | QA owner aligns consumers, tests, and generated projections for generations 3–5. | W2 | TSK-0001 | QA-owned checks recorded. |
| W5 | 5 | Record review and final changed-gate evidence for closure. | W2–W4 | TSK-0001 | Root-owned final gate. |

## Verification Plan

Run only focused metadata, schema, link, and formatting diagnostics during
authoring. The QA owner owns scripts, tests, and generated projections. Root
owns the final public changed gate after the final implementation is staged.

## Risks and Rollback

The primary risks are rewriting preserved historical evidence, weakening native
provider envelopes, or leaving mismatched headings and links. Revert the
logical documentation change if a focused contract check fails; do not change
runtime, archive, external, or credential state.

## Related Documents

- [Specification](spec.md)
- [Task 0001](tasks/tsk-0001-common-document-contract-adoption.md)
- [Stage 99 Registry](../../99.templates/registry.json)
