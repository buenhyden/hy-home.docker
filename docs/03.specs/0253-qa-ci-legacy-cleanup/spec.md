---
title: "QA and CI Legacy Cleanup Specification"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0253"
parent_ids:
- "REQ-0024"
- "AD-0027"
created: "2026-11-04"
---

# QA and CI Legacy Cleanup Specification

## Overview

### Intent

QA and CI still carry boundaries and labels that name records the repository
no longer has. This change removes them and checks QA, CI and scripts for
one-off items that only served a finished operation.

### Owning Requirements

The user directed that legacy and deprecated items in QA and CI/CD be deleted,
and that one-off scripts, tests and QA be deleted. After Stage 98 lost its
records, the pre-commit `frozen_archive_payloads` boundary matches no file,
the CI gate evidence owner names a deleted Task, and the DATA-0096 README
names run-specific files in a runnable command.

SPEC-0253 has parent_ids REQ-0024 and AD-0027. It makes concrete REQ-0024 (one canonical agent governance home) and the AD-0027 provider adapter placement for the QA and CI surfaces that still named removed records. The body cites no REQ-0024-FR or NFR identifier.

## Scope

### In Scope

- The pre-commit frozen archive boundary, the PostToolUse hook code that reads
  it, and their tests.
- The CI gate evidence `owner` label in the workflow contract, its readers and
  their tests.
- The DATA-0096 command block and stale wording in `scripts/README.md`,
  `.agents/governance/agentic.md` and `docs/99.templates/README.md`.
- An inventory of scripts, tests, workflows and QA exceptions for one-off and
  legacy items, deleting only items with no current caller.

### Non-goals

- Lifecycle-generation migration and identity-history code, owned by the
  legacy document status work and the SPEC-0209/0231 proof move.
- Registry archive profiles and lifecycle vocabulary.

## Behavior Contract

### Normal Behavior

The PostToolUse hook reports changed text files by default and normalizes
them only with `--write`, without reading a frozen boundary. CI gate evidence names
`.agents/governance/quality-standards.md#7-local-qaci-orchestration` as its
owner. The `commands` link mode reports no finding.

No runtime, remote or secret state changes.

### Failure and Edge Cases

A script, test or exception entry is deleted only when it has no current
caller, its purpose ended with a finished operation, and it is not a reusable
operator tool; anything else stays and is listed in the Task.

The workflow contract is a protected surface; the user's cleanup instruction
authorizes the owner label change, and the Task records it.

**Observable failures.** A deleted item still has a caller, or a check that read the removed boundary
now fails.

**Stop boundaries.** This Task pushes and merges nothing; the coordinator pushes and opens the pull
request, and the user merges.

## Acceptance Criteria

### Criteria

1. No QA or CI configuration, hook or contract names a frozen archive boundary
   or a deleted Task.
2. Every script, test and QA exception was checked for one-off or legacy use,
   and the Task records each candidate with its decision.
3. Gate, CI routing, manifest and hook tests, the document gates, the agent
   governance contract and renderer parity pass locally, with actual results in
   the Task.

### Evidence Requirements

- Criterion 1 is observed by searching QA and CI configuration, hooks and the workflow contract for the removed boundary and deleted Task names.
- Criterion 2 is observed in the Task, which records each candidate script, test and QA exception with its decision.
- Criterion 3 is verified by running the gate, CI routing, manifest and hook tests, the document gates, the agent governance contract and renderer parity locally; the actual results go in the Task.
- The frontmatter owner judges each criterion and records the decision in the Task's Criterion Acceptance table.

## References

### Normative and Evidence

- [Plan](plan.md)
- [Task](tasks/tsk-0001-qa-ci-legacy-cleanup.md)

### Historical and Navigation

No historical or navigation link applies; the package links only its Plan and Task.
