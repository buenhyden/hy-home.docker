---
title: "npm Risk Acceptance Extension Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0222-TSK-0001"
parent_ids:
- "SPEC-0222-PLAN-0001"
created: "2026-10-09"
---

# npm Risk Acceptance Extension Task

## Objective

Extend the GHSA-vfj7-8cjw-p6xm acceptance by the owner's approval and let a
future approval extend it without a code or governance change.

## Inputs and Authorization

On 2026-10-09 the owner asked to upgrade to a patched version after SPEC-0221.
The official advisory (`GET /advisories/GHSA-vfj7-8cjw-p6xm`) lists
`braces <= 3.0.3` with no patched version; npm lists `braces` 3.0.3 (2024-05),
`eslint-config-next` and `@next/eslint-plugin-next` 16.4.0, and `fast-glob`
3.3.3, which still depends on `micromatch`. Offered an extension, removal of
the Next lint chain, or expiry, the owner chose a 30-day extension and asked to
replace the dated text in the quality standard with a rule that lets an
approval extend the window.

## Work Log

### W1 Contract Window

`_parse_npm_audit_acceptance` keeps the advisory, owner, project, chain and
URL pinned and accepts `approved_at` and `expires_at` as UTC timestamps with
`approved_at < expires_at <= approved_at + 30 days`. The record carries
`approved_at` `2026-10-09T07:00:00Z` and `expires_at` `2026-11-08T07:00:00Z`.
The window is counted from the approval, so it ends on 2026-11-08 rather than
30 days after the old expiry. Contract and adapter tests: 68 pass.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Contract window | 1 | W1 | Contract and adapter tests | `ebffea9bb` | PASS | W1 Contract Window | accepted |

## Review and Completion

Not complete: W2 and W3 remain.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
