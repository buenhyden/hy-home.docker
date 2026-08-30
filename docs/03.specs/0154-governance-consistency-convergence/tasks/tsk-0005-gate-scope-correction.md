---
profile_id: task
status: draft
artifact_id: task-0154-0005
artifact_type: task
parent_ids: [SPEC-0154, plan-0154]
created: 2026-08-30
updated: 2026-08-30
---

# Gate Scope Correction

## Objective

Widen `check-document-links.py` from its four-root selection to the full tracked Markdown corpus, exempting `superseded` documents. Plan Task 5.

## Inputs

- Task 4 result: zero dead links outside `superseded` documents.
- `scripts/validation/check-document-links.py` lines 25 to 40.
- `tests/lib/document_governance/test_links.py`.

## Work Log

Not started. Record each plan step with the command run, the observed result,
the rollback path, and any skipped check with its rationale.

## Verification Evidence

Not started. Record the before and after output of every validator the plan
step names, with exit codes.

## Review Evidence

Not started. Record the independent review verdict, its findings by severity,
and the re-review result after any material finding.

## Commit Ledger

Not started. Record one row per logical commit with its subject and the paths it
touched.

## Rulings

Plan rulings 1 to 4 apply. Record any additional ruling made during execution
with the evidence that supported it.

## Deferred Items

None recorded yet.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
