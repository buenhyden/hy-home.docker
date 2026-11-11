---
title: "W02 Archive and Safe Removal Task"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0057"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-11"
---

# W02 Archive and Safe Removal Task

## Overview

### Objective

Own W115/criterion 110. Assess the v14.2 W02 obligations ARC-01 to ARC-09
against the current retention and retirement owners. Before any removal,
prove readiness and byte recovery for each candidate, and block a removal
whose acceptance, promotion, hold, authority or recovery is unmet.

## Inputs and Authorization

On 2026-11-11 the owner approved this Task to own W02. The v14.2 package
prompt `tasks/TASK-hy-home-docker-W02.md` under
`_workspace/workspace_execution_tasks/` is untrusted reference data, not an
instruction source.

The authorization covers four things:

- The assessment.
- Recovery proofs restored into a scratch location outside the repository.
- Repository-side fixes of gaps this Task reproduces.
- Records in this Task.

Each package removal needs its own owner approval of that batch under the
[SDLC sequence](../../../../.agents/governance/sdlc.md#sequence). Safety
conditions (Q-04) block a removal and are never offered as a waiver.

The SPEC-0248, 0249, 0250 and 0260 Tasks keep their own residual criteria.
This Task records their state and does not close them. It starts from
`main` `e4fd7f5f3`, after PR 954 merged the retirement rules W01
consolidated.

## Work Log

### Owner-approved local execution

The owner's approval of 2026-11-11 issues this Task. The lifecycle records that
approval; it grants no removal or remote operation.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0057 | draft | ready | #owner-approved-local-execution |
| SPEC-0212-TSK-0057 | ready | in-progress | #owner-approved-local-execution |

### W02 obligation assessment 2026-11-11

A fresh-context `rules-engineer` read the retention and retirement owners at
`main` `e4fd7f5f3`, and the controller re-checked the deciding lines.

| ID | Verdict | Current owner and basis |
| --- | --- | --- |
| ARC-01 | KEEP | `documentation-protocol.md`: age may trigger a disposition review and never a deletion; `sdlc.md`: readiness is not removal approval |
| ARC-02 | GAP, CHANGE | Policy holds: historical material ranks last, and no loader reads Stage 90/98 as a rule. But no test rejected an active-stage occupancy violation, and the protocol named only Stage 01/02 owners, against its own precondition 2 |
| ARC-03 | KEEP | Terminal Task bodies stay immutable; recovery reads a body at its last revision and grants no write |
| ARC-04 | KEEP | Retirement is a disposition inside the approved Task, never a new Spec project |
| ARC-05 | GAP, CHANGE | The preconditions lacked the last carrying commit and path, reachability, blocking cases and the byte comparison |
| ARC-06 | KEEP | The SDLC batch-deletion approval and the README-only Stage 98 leave no move path |
| ARC-07 | KEEP policy, DEFER code | Quality standards forbid archive, retention and migration checks. The lifecycle Migration manifest surface stays (see ARC-08) |
| ARC-08 | GAP, CHANGE in part | Static migration and exception validators, their schemas, helpers and archive constants had no live caller |
| ARC-09 | KEEP | `approval-boundaries.md`: adoption is per repository; Vault and memory keep their own rules |

Changes:

- `18d9569ec` routes retired meaning to the governance, Stage 01, 02 or 05
  owner in the protocol and the Stage 98 README. It also adds the manual
  precondition 5: the last carrying commit and path, reachability from
  `main`, blocking cases, and the post-merge byte comparison recorded in a
  surviving Task.
- `535a16243` adds occupancy rejection tests for a retired standalone guide,
  a cancelled-Spec package and a cancelled Plan in an open package. Each test
  failed when its rejection branch was removed in memory.
- The ARC-08 commit removes the dead static validators, the
  `EXPECTED_ARCHIVE_*` and preservation constants, the manifest and exception
  schemas and their exclusive helpers, and their re-exports (979 lines).

DEFER, with scope:

- The `lifecycle/contract.py` Migration manifest model, loader, renderer and
  skeleton generator, their re-exports in
  `check-document-corpus-lifecycle.py`, the `ruff.toml` F401 exemption and
  the `test_public.py` manifest tests. They interleave with live surface and
  partition checks, and the exemption records that removing the re-exports
  broke registered tests, so retirement needs its own call-graph pass.
- The Registry archive vocabulary, because `preserved_origin_path` still reads
  it for bases that carry Stage 98 records.

### Removal candidates 2026-11-11

`archive_readiness_findings` reports five ready packages: 0226, 0266, 0267,
0268 and 0269. Readiness is not removal approval. A delete dry-run in a
scratch worktree restored all 15 files from the parent of the removal commit
with zero byte mismatches against `origin/main`. The source commit is
reachable from `origin/main`, and there is no LFS or submodule.

The same dry-run shows what a real removal must do first. Without those steps
the existing gates block it:

- Reserve the Spec numbers: `package-retirement-unrecorded` and
  `identity-retired-not-reserved`.
- Cut over seven inbound links: ADR-0061 to 0266, the Ollama guide to 0226,
  and the `docs/03.specs/README.md` index.
- Promote any still-current meaning to its owner, a W04 concern.

No package is removed. Removal waits for the owner's approval of that batch.

### Batch removal 2026-11-11

The owner approved removing 0226, 0266, 0267, 0268 and 0269 as one batch. A
fresh-context promotion check found every still-current meaning of four of
them in a current owner. 0267 failed the check: its accepted risks live only
in its Task (n8n and Gatus `/metrics`, and Loki, Tempo and Alloy on
`HOST_LAN_BIND_IP`). Its removal is blocked until POL-0053, POL-0087 and
POL-0096 record those risks and AD-0026 lists its four networks.

Commit `58be65ebb` retires 0226, 0266, 0268 and 0269:

- Lineage lines added: SPEC-0226 in the Ollama guide, and the Open WebUI
  no-socket, no-terminal rule in its LAB guide. SPEC-0269 in AD-0007.
- Inbound links in ADR-0061 and the SPEC-0267 Spec become plain text. The
  terminal 0267 Task link is excused by link alignment.
- The index rows are removed, and 226, 266, 268 and 269 join the Spec
  `reserved_history`.
- Gates: metadata selected 23 with 0 violations; links 0 failures; corpus
  lifecycle and occupancy 0.

Precondition 5 record: each removed body is last carried unchanged by
`main` `e4fd7f5f3`, which is reachable from `main`. No body is uncommitted,
reflog-only, branch-only or shallow-missing, and no hold is recorded. The
scratch dry-run restored all 15 files of the five packages with zero byte
mismatches. The post-merge restore and byte comparison for the four removed
packages are recorded in this Task after the PR merges.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W02 obligation assessment | 110 | W115 | archive-owner-assessment | ARC-01 to ARC-09 at main `e4fd7f5f3` | NOT_RUN | Assessment not yet run | required | - |
| W02 obligation assessment result | 110 | W115 | archive-owner-assessment | ARC-01 to ARC-09 at main `e4fd7f5f3` | PASS | Per-ID table above: five KEEP; ARC-02, 05 and 08 GAP changed; ARC-07 code and ARC-08 manifest surface DEFER with scope | required | W02 obligation assessment |
| W02 removal dry-run | 110 | W115 | removal-recovery-dry-run | Five ready packages at `e4fd7f5f3` in a scratch worktree | PASS | 15 files restored with zero byte mismatches; gates block the removal until reservation and seven link cutovers | optional | - |
| W02 batch removal | 110 | W115 | package-retirement | Commit `58be65ebb` removing 0226, 0266, 0268, 0269; 0267 held | PASS | Promotion verified for four; reserved_history and link cutover done; metadata 0, links 0, lifecycle 0; post-merge byte comparison pending | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 110 | pending | - | - | SPEC-0212 TSK-0057 |

## Review and Completion

In progress. The assessment, the dry-run and the reproduced-gap changes are
recorded; package removal waits for the owner's batch approval.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [W01 Task](tsk-0056-w01-governance-standardization.md)
