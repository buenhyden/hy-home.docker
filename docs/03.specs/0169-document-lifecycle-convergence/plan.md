---
title: Document Lifecycle Convergence Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0169-PLAN-0001
parent_ids: [SPEC-0169]
created: 2026-09-03
updated: 2026-09-03
---

# Document Lifecycle Convergence Plan

## Objective

Make the declared section contract real, put every stage document on the
vocabulary its stage owns, and give retirement a route in the two stages that
lack one.

## Dependencies

- SPEC-0168 keyed the README section gate on registered profile rather than
  filename; this package applies the same principle to the remaining profiles.
- The tombstone contract (ADR-0030) already defines the record shape; only its
  namespace needs extending.
- `docs/05.operations/catalog` subject numbering and the `operations-domain-readme`
  profile are unchanged by this work.

## Execution Sequence

1. **Phase 1 — declarations.** Reconcile `guide`, `policy`, `runbook` sections
   in the registry and the three templates. Extend REQ-0026, AD-0030, ADR-0030,
   and `documentation-protocol.md` with the Stage 01/02 retirement route,
   tombstone namespaces, and a concrete member-disposal test. Collapse the four
   Stage 03 title conventions to one. → the registry and templates agree with
   each other and with the corpus core; blast radius per profile is measured and
   recorded.
2. **Phase 2 — Stage 01/02.** Prove per-domain destination coverage. Relocate
   solution-dependent clauses from `REQ-0014`–`REQ-0022` and the nine hardening
   architecture descriptions. Retire them under new tombstone namespaces. Strip
   stacked legacy headings from 66 documents. → Stage 01 names no implementation
   artifact; unregistered headings in Stages 01 and 02 reach zero.
3. **Phase 3 — Stage 03.** Retire the twelve permanently-active domain packages.
   Remove `plan.md` and tasks from the eleven completed packages that retain
   them. → no `active` package without execution members.
4. **Phase 4 — Stage 05.** Normalize 192 catalog documents to the reconciled
   vocabulary and add `Traceability`. → unregistered and missing headings reach
   zero for the three operations profiles.
5. **Phase 5 — enforcement.** Remove the typed-target bypass in
   `validate_body_contract`; add mutation coverage. → both mutation directions
   fail closed for all seven affected profiles.

Each phase is one logical commit, or a small ordered set where a generated
artifact must be regenerated separately.

## Risk and Rollback

- Retiring content its destination does not own. Phase 2 begins with the
  coverage proof; a domain that fails it is reported and left in place.
- Enforcement failing closed on an unmeasured profile. Phase 1 records the blast
  radius per profile and Phase 5 re-measures before the switch.
- A generated artifact drifting mid-phase. Regenerate from its own generator and
  commit as a separate unit, per the quality standard.
- Rollback is `git revert` of a phase commit. Tombstones carry the recovery
  commit, so retired content stays reachable.

## Verification

- `python3 scripts/validation/run-ci-gate.py --profile full` at each phase
  boundary.
- A corpus measurement script reporting missing and unregistered headings per
  profile, run before and after each phase.
- Mutation tests for both directions on each affected profile.
- `bash scripts/validation/run-agent-precommit-all-files.sh` at the final QA gate.

## Related Documents

- [Specification](spec.md)
- [Execution task](tasks/tsk-0001-document-lifecycle-convergence.md)
