---
title: "Repository-Root Style Classification"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-TSK-0005"
parent_ids:
- "SPEC-0190"
- "SPEC-0190-PLAN-0001"
created: "2026-09-29"
---

# Repository-Root Style Classification

## Objective

Implement Plan W5: classify staged or base-relative files consistently from any
caller directory, preserving generated ownership and reporting discovery/read
failures instead of silently treating failed input as authored content.

## Inputs

- [Approved Spec](../spec.md), [approved Plan](../plan.md), W4 `db15e0361`.
- User approval includes local implementation, focused tests, independent review
  and logical commits. No installation, remote, runtime or global mutation.
- Primary writer: qa-engineer; independent reviewer: code-reviewer.
- Exact files: `.agents/skills/style-validation/scripts/classify-changed-files.sh`,
  `.agents/skills/style-validation/SKILL.md`, and
  `tests/validation/test_agent_governance_ci_routing.py`. Root owns this Task.
  W4 released exclusive ownership of the shared tests before W5 implementation.

## Work Log

Read-only preparation found masked process-substitution Git failures,
caller-relative marker reads, pipeline read/SIGPIPE ambiguity and permissive
argument combinations. Existing Bash NUL-list handling plus explicit child
status checking can preserve filenames without a new dependency or temp file.
W4 implementation and independent review are complete; actual required-tool
acceptance remains BLOCKED in W4/W10 evidence and is not overridden here.

## Verification Evidence

NOT_RUN: focused RED/GREEN H, Bash syntax and available shell lint.
Preserve output buckets, no-argument staged mode, `--base <ref>` ref...HEAD mode,
and standalone `--help`/`-h`. Test root/subdirectory/skill/space-containing cwd,
generated marker after frontmatter, malformed CLI, Git failure and marker read
failure. Missing installed lint remains explicit rather than a success claim.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| R09/R12/R34/R39 supporting checks | W5 | NOT_RUN | Existing style helper, skill and helper regression class |

## Review Evidence

Independent exact-diff review pending. Tests must preserve category behavior and
actual error propagation without weakening the previous W4 checks.

## Commit Ledger

Root validates and commits draft, ready and in-progress predecessors before GO.
No W5 implementation commit yet.

## Rulings

Explicitly waiting for the Git discovery child is permitted; the failure is
lost exit status, not process substitution itself. Use root-relative bounded
marker reads and inspect their status before matching. No new helper module,
parser, manifest, CI leaf or global configuration is needed.

## Deferred Items

W10 owns final broad/coverage/native acceptance. The evaluation subsystem stays
at its current path during W5; the user-authorized migration is assigned to W9.
