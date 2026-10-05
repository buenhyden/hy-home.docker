---
title: "Common Document Contract Adoption Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "completed"
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
authored documents. W4/W5 also own the remaining bounded consumer-recovery
slice. The Task is the only progress and evidence ledger.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Inventory profiles, templates, schemas, authored documents, consumers, and dispositions. | None | TSK-0001 | Whole-stage inventory recorded. |
| W2 | 2 | Align Registry, JSON schemas, and Markdown/non-Python templates with v4. | W1 | TSK-0001 | Focused metadata/schema checks. |
| W3 | 3 | Migrate current authored Markdown and active links; preserve frozen and completed Task bodies. | W2 | TSK-0001 | Focused link and metadata checks. |
| W4 | 4 | QA owner aligns consumers, tests, and generated projections for generations 3–5; restores bounded raw-byte and historical compatibility in the three approved consumers and five regression files. | W2 | TSK-0001 | Witnessed CRLF RED/GREEN and negative-boundary regressions. |
| W5 | 5 | Record independent review and final changed-gate evidence for closure of the consumer-recovery slice. | W2–W4 | TSK-0001 | Root-owned staged public changed gate and minimal final-receipt metadata/link checks. |

## Verification Plan

Run only focused metadata, schema, link, and formatting diagnostics during
authoring. The QA owner owns scripts, tests, and generated projections. Root
owns the final public changed gate after the final implementation is staged.
For the consumer-recovery slice, apply the five approved test hunks first and
witness the CRLF regression before applying the three consumer hunks. Run only
new or changed focused regressions and scoped registered Ruff checks; leave
aggregate metadata and library suites to the public gate. Freeze exactly the
eleven owned files before explaining and running that gate. Independent review
uses the exact diff and results. Final receipt changes require only the affected
package documents' minimal metadata/link checks.

The approved attempt permits one initial batch and one narrower correction to
P02-owned defects, with at most two public changed-gate executions on different
inputs. Identical leaf/input/configuration/tool/mode/trust checks are not repeated.
An out-of-scope required failure or a remaining failure after that correction
blocks closure and local commit; it does not expand the file or operation scope.

## Risks and Rollback

The primary risks are rewriting preserved historical evidence, weakening native
provider envelopes, or leaving mismatched headings and links. Revert the
logical documentation change if a focused contract check fails; do not change
runtime, archive, external, or credential state.

## Related Documents

- [Specification](spec.md)
- [Task 0001](tasks/tsk-0001-common-document-contract-adoption.md)
- [Stage 99 Registry](../../99.templates/registry.json)
