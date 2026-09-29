---
title: "Recursive Skill Resource Boundaries"
version: "0.1.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-TSK-0003"
parent_ids:
- "SPEC-0190"
- "SPEC-0190-PLAN-0001"
created: "2026-09-29"
---

# Recursive Skill Resource Boundaries

## Objective

Implement Plan W3: preserve legitimate skill-owned resources while rejecting
unsafe nodes, unreachable content, unintended execution and unbounded traversal.
Own R12/R25/R26 evidence; supporting units still own their relevant receipts.

## Inputs

- [Approved Spec](../spec.md), [approved Plan](../plan.md), W2 commit `69c336e91`.
- User approval covers local implementation, focused tests, review and commits;
  no installation, remote mutation, live environment or secret access.
- Primary writer: qa-engineer; README contribution: doc-writer. Independent
  security-auditor reviews exact diff and negative/race evidence.
- Exact files: Plan W3 four paths plus this Task. Root owns lifecycle/evidence;
  the assigned writer owns implementation exclusively and preserves other work.

## Work Log

- Read-only security audit traced CLI and renderer through
  `load_agent_governance` into `validate_canonical_agent_home`.
- Existing top-level directory allowance skips all resource descendants.
- Shared renderer fixture copies SKILL bodies but omits their eight current
  resource leaves. Its existing safe copier must include owned resource files
  so strengthened reachability sees a valid fixture; no registry rows are added.
- Plan exact file map amended before implementation. W2 completed and reviewed;
  no overlapping writer remains on the shared README.

## Verification Evidence

NOT_RUN: G/P/repository contract and resource RED/GREEN. Required cases include
direct/transitive use, no-follow/race denial, special files, malformed paths,
orphan/executable rejection and 4096-entry/64-depth/16-MiB text bounds.
The existing 4-MiB text-file cap remains; binary assets are terminal.

## Review Evidence

Read-only security design audit identified the fixture dependency and required
identity checks before reading a replacement. Implementation review is pending.

## Commit Ledger

No W3 implementation commit yet. Git records the validated draft/ready/active
Task predecessor chain; Task transitions do not claim acceptance.

## Rulings

- Add the shared renderer fixture copier and P to W3 before implementation:
  every renderer test loads the same validator, so omitting resources would
  fabricate invalid fixtures. This is necessary existing-consumer maintenance
  within approved resource validation, not a new production surface.
- Reuse descriptor/no-follow safety and the existing Finding/ContractLoadError
  contract. Do not add a resource manifest, separate parser service or import
  or execute resource content. Safe outward governance links remain citations.

## Deferred Items

Native discovery/execution acceptance remains W10; static resource validation
cannot establish runtime invocation or recovery success.
