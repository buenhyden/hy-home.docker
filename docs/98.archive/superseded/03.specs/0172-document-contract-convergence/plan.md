---
title: "Document Contract Convergence Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0172-PLAN-0001"
parent_ids:
- "SPEC-0172"
created: "2026-09-04"
---

# Document Contract Convergence Plan

## Objective

Close the remaining document-contract gaps in the current checkout, preserving
existing IDs, frozen payloads, native formats and earlier historical evidence.

## Dependencies

REQ-0024/REQ-0026, AD-0027/AD-0030 and ADR-0029/ADR-0031 remain the durable
owners. SPEC-0172-TSK-0001 owns current audit, migration and validation evidence.
The current request supersedes prior remote integration scope for this run.

## Execution Sequence

1. W1: record current root, branch, HEAD, clean index, tool versions, full corpus
   inventory, frozen byte digests and baseline metadata/direct tests.
2. W2: reproduce missing literal, template and residue validation before changing
   Registry, schemas, consumers and direct negative tests together.
3. W3: correct current Stage 00/README contradictions, retain explicit ID/type
   mapping and release evidence mode, and update template guidance through its
   registered owner without touching accepted ADR or frozen bodies.
4. W4: migrate only individually reviewed affected active documents, rerun
   formal document/identity/link/lifecycle and generator freshness checks, and
   compare final frozen digests, allocation spaces and Git index to baseline.
5. W5: obtain independent policy and code review, correct findings, and record
   exact results and remaining DEFER conditions without staging or committing.

## Risk and Rollback

- Restore only this request's edits with a reviewed inverse patch if needed.
  Never reset, clean, stash, change branches or overwrite another worker.
- Root `parent_ids: []` expresses an allowed structural root. Do not tighten a
  shared array grammar in a way that breaks it; reject empty optional fields at
  the selected profile boundary.
- Existing architecture successor edges are singular and reciprocal. Retain
  that contract after considering arrays; changing it requires coordinated
  graph and preserved-lineage migration, not a schema-only substitution.
- Full and changed may select Compose and real environment consumption. Do not
  execute a selected unsafe route, disable it, or substitute a partial PASS.
- No formatter may alter a frozen record. Prove ignore coverage and digests.

## Verification

- W1/W2: current Registry and metadata tests, followed by focused RED/GREEN cases.
- W3/W4: metadata contracts/active/changed, template ownership, traceability,
  identity high-water, lifecycle/recovery, archive and native format tests.
- W4: registered generator checks, frozen-body byte comparison, diff whitespace,
  unstaged/staged diff and final status. Index and HEAD must remain unchanged.
- W5: independent exact-diff policy and Python reviews; Task records acceptance
  criterion to work-unit to executed result and durable owner promotion links.
- Required public changed/full commands are PASS only if executed safely in
  their complete selected scope. Otherwise record selection and exact DEFER.

## Rulings

- Current-main local edits and no commit/push/branch switching follow the latest
  direct user request; previous integration instructions are historical only.
- Keep existing lifecycle state until a separately valid recorded transition;
  tests and narrative evidence must not fabricate approval or completion.
- Keep short Registry IDs as explicit one-to-one mappings to unique types.
- Preserve ADR-0031 and the existing external-release-evidence decision.

## Related Documents

- [Specification](spec.md)
- [Execution task](tasks/tsk-0001-document-contract-convergence.md)
