---
title: "Agentic Research Refresh Plan"
version: "1.0.2"
type: "sdlc/plan"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0185-PLAN-0001"
parent_ids:
- "SPEC-0185"
created: "2026-09-27"
---

# Agentic Research Refresh Plan

## Objective

Implement the [Spec](spec.md) through one [Task](tasks/tsk-0001-external-research-refresh.md).

## Dependencies

Registered templates and gates at the baseline; owner approval for research and
local commits plus the new package and minimal allocation. SPEC-0184 is already
issued on the other active branch, so reserve it and allocate SPEC-0185 here.

## Execution Sequence

1. W1: Inventory research identity, questions, sources, headings and historical
   evidence; establish isolated baseline and source/claim conventions (AC1).
2. W2: Research and update m0001/2/3/8/10/12/13 for instructions, models,
   catalogues, harnesses, loops and provider comparison (AC2–3).
3. W3: Research and update m0005/9/11/21 for Compose, knowledge and memory;
   preserve service-specific observations (AC1–3).
4. W4: Research and update m0006/7/16/18 for lifecycle, architecture, operations
   documentation and project tracking (AC2–3).
5. W5: Research and update m0004/14/17/19 for automation, QA, security and
   verification/validation (AC2–3).
6. W6: Integrate README, m0015, m0020 and research index; verify coverage,
   historical preservation and links; independently review, run gates and
   create logical local commits (AC1–5).

## Risk and Rollback

W2–W5 have disjoint member ownership. Controller alone changes README, indexes,
Task, Registry and Git index. Research and independent review cannot grant
permissions. Revert only this branch's logical commits if necessary; never
reset, stash or clean another worker's files. All historical dates remain intact.

## Verification

Read gate help; explain changed scope before execution. Record the same explicit
baseline and path selection across baseline/final comparison, including committed
paths. Run metadata, source/claim, coverage and link checks plus independent
review. Domain coverage and runtime tests do not apply. Do not run pre-commit
directly, the all-files wrapper, CI-only commands or the retired wiki generator.

## Rulings

- Use the existing research pack; neither another root nor new members are needed.
- The owner's detailed execution brief supplies the design and scope; the explicit
  follow-up permits this package and allocation only, not general Registry changes.
- Use subagent-driven development with disjoint authorship and independent review;
  keep progress here in the Task, overriding the skill's parallel scratch ledger.
- Local branch/worktree preservation is the requested finishing option.
