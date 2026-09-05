---
title: "Generated Evidence and Final Verification Task"
version: "0.1.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0173-TSK-0006"
parent_ids:
- "SPEC-0173"
- "SPEC-0173-PLAN-0001"
created: "2026-09-05"
---

# Generated Evidence and Final Verification Task

## Objective

Regenerate only affected derived artifacts, prove the converged surface with
focused checks and one final canonical full gate, and obtain independent review
without expanding into remote delivery.

## Inputs

- [SPEC-0173](../spec.md), its [implementation plan](../plan.md), and the
  completed local changes from Tasks 0001 through 0005.
- Canonical generators, generated-freshness checks, public validation profiles,
  script manifest validation, document validators, and Git diff checks.
- The final invocation-identity inventory and deletion consumer searches.

## Work Log

Task 5's implementation milestone passed independent code, Python, and policy
review; its corrections are committed as `0b237043`, `0fbbb962`, and `3fbb62aa`.
The user authorized proceeding with final verification and cleaning the feature
branch/worktree after local integration. No remote mutation is authorized.

The Task 5 read-only preflight identified two stale outputs: DATA-0059's
generator emits an obsolete metadata envelope, and DATA-0078 has old inventory
counts. DATA-0065 must preserve the corrected source audits' historical
designation in derived tables. Correct these reproduced generator defects at
their existing source owners with RED/GREEN tests before regeneration; never
hand-edit generated output or weaken validators. No Task 6 write or aggregate
has run at this ready checkpoint.

## Verification Evidence

Final execution evidence is pending. Final acceptance requires all
focused checks in the Plan, `git diff --check`, and exactly one successful
`python3 scripts/validation/run-ci-gate.py --profile full` on the final local
tree.

## Review Evidence

No implementation review has occurred. The final reviewer must receive the
exact commit and verification evidence and must be independent of the
implementation work.

## Commit Ledger

No implementation commit exists. The planning-package changes are not
implementation or acceptance evidence.

## Rulings

- Generated output changes are accepted only when their canonical source set
  changed and write/check modes agree.
- A local full-gate pass proves repository enforcement only; it does not prove
  Hosted CI, runtime, deployment, entitlement, or remote protection state.
- The completion full gate runs after durable evidence and evidence-derived
  outputs are final; no content edit follows that verification.
- Final lifecycle completion happens only after review findings are resolved
  and durable evidence is written to the canonical owner.

## Deferred Items

- Commit publication, push, pull request, Hosted CI, branch protection,
  deployment, tag, release, and merge require separate authorization and are
  outside this Plan.
- Runtime and remote observations remain explicitly unverified.

## Related Documents

- [SPEC-0173 package](../spec.md)
- [SPEC-0173 implementation plan](../plan.md)
- [Document and provider residue Task](tsk-0005-document-and-provider-residue.md)
- [Stage 03 index](../../README.md)
