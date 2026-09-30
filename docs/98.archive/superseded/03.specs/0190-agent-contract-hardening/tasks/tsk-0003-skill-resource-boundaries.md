---
title: "Recursive Skill Resource Boundaries"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
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
- Exact files: Plan W3 six paths plus this Task. Root owns lifecycle/evidence;
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

- Initial RED: registered G exited 1, 48 tests with eight expected failures and
  four missing-symbol errors for the previously unvisited resource contract.
- Additional witnessed RED/GREEN covered unsafe inode replacement, descriptor
  failures, resource bounds, hidden/comment/metadata consumers, cross-skill and
  external URL references, and parser CPU/attribute-context bypasses.
- Final L: registered sanitized adapter, 95 tests, exit 0, 112.494s.
- Final G: registered sanitized adapter, 53 tests, exit 0, 88.638s.
- Final P: three registered provider modules, 54 tests, exit 0, 55.396s.
- Final C: repository contract, exit 0, failures=0, 2.913s.
- `git diff --check`: exit 0. Ruff and coverage executables unavailable;
  neither was installed and no coverage percentage is claimed.
- Plan verification table owns the exact commands and module lists above.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| R12 | W3 | Resource cases PASS; other units retain their checks | Existing resource validator and tests |
| R25 | W3 | PASS: regular/no-follow/race and bounded traversal checks | Existing resource validator |
| R26 | W3 | W3 PASS; new-skill/evaluation consumers remain W6/W9 | Existing resource graph and bundle documentation |

## Review Evidence

Independent security-auditor final verdict PASS / CLEAR, no open finding.
Review reproduced and corrected CPU scanning, allocation, and hidden-context
reachability defects rather than accepting the earlier passing test set alone.
Final review includes actual versus title-contained/data-href HTML attributes,
quoted tag boundaries, escaped links, comments, frontmatter, safe outward links,
binary terminals, and all eight existing resource leaves. Graph and navigation
reuse the same exact-attribute extraction backed by stdlib HTMLParser.

## Commit Ledger

This Task is committed with the reviewed W3 implementation; Git owns its hash.
The real predecessor chain records draft, ready and in-progress states; the
completion transition is checked against the committed in-progress Task.

## Rulings

- Add the shared renderer fixture copier and P to W3 before implementation:
  every renderer test loads the same validator, so omitting resources would
  fabricate invalid fixtures. This is necessary existing-consumer maintenance
  within approved resource validation, not a new production surface.
- Reuse descriptor/no-follow safety and the existing Finding/ContractLoadError
  contract. Do not add a resource manifest, separate parser service or import
  or execute resource content. Safe outward governance links remain citations.

- Independent review reproduced quadratic work in two reused Markdown opener
  patterns with repeated unclosed brackets. Plan W3 now includes the shared
  parser and existing link tests before those edits, plus L verification. Fix
  the two character classes and overlapping destination rescans at their common
  source. Both malformed-input families require witnessed regression checks.
  Retain the 16,384-opening-bracket precheck as a distinct parser output bound: a
  valid multi-megabyte input otherwise materializes hundreds of thousands of
  link records before graph deduplication. The output bound is not a CPU fix.

## Deferred Items

Native discovery/execution acceptance remains W10; static resource validation
cannot establish runtime invocation or recovery success.
