---
title: "NFR Quality Measure Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0020"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# NFR Quality Measure Task

## Overview

### Objective

Execute W36: give the requirement template's non-functional line a quality
characteristic and a measure. This Task owns criterion 31 only.

## Inputs and Authorization

The original request asks that ISO/IEC 25010, 25023, and 25030 be reflected
in governance and templates by connecting them to existing quality
requirements and measures, not by adding a separate compliance system. Only
REQ-0003 applied them, through its own Quality Measurement table. On
2026-10-29 the owner approved one template line. The input is `main` at
merged PR #617. The authorization covers that template line, this branch, its
pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0020 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0020 | ready | in-progress | #objective |
| SPEC-0212-TSK-0020 | in-progress | completed | #evidence |

### Template line

`docs/99.templates/templates/requirements/requirement-package.template.md` now
declares a non-functional requirement as
`**REQ-####-NFR-#### — {{QUALITY_CHARACTERISTIC}}**:` followed by the
requirement and `measure: {{MEASURE_UNIT_ENVIRONMENT_AND_ACCEPTANCE}}`. It
uses the existing label slot of the requirement declaration grammar in
`scripts/lib/document_governance/requirements.py`; a first attempt that split
the declaration over three lines was rejected by that parser as malformed and
was not kept. Existing requirement packages are not rewritten.

### Kept

The 30-day expiry in `quality-standards.md` bounds a security risk
acceptance, not a work schedule, so it does not conflict with the request's
ban on time-boxed work. `github-governance.md` already assigns requests and
priority to Issues and a filtered work view to Projects.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Template tests | 31 | W36 | `python3 -m unittest tests.lib.document_governance.test_requirements tests.lib.document_governance.metadata.test_profile tests.lib.document_governance.metadata.test_heading tests.lib.document_governance.metadata.test_reference` | This branch | PASS | 159 tests OK | required | - |
| Template lint | 31 | W36 | `markdownlint-cli2` on the changed template | This branch | PASS | 0 issues | required | - |
| Metadata contracts | 31 | W36 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 31 | accepted | Template tests, Template lint, Metadata contracts | New non-functional requirements name a quality characteristic and a measure; no separate compliance structure was added. | SPEC-0212 TSK-0020 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
