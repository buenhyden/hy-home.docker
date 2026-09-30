---
title: "Repository-Root Style Classification"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
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

- RED: full H ran 47 tests in 16.622s and exposed 21 expected failures.
- GREEN: final independent full H passed 47/47 in 17.658s through the
  registered sanitized unittest adapter; focused four methods also passed.
- `bash -n .agents/skills/style-validation/scripts/classify-changed-files.sh`
  and `git diff --check`: exit 0. Executable mode remains 100755.
- Cases cover all buckets, root/subdirectory/skill cwd in a space-containing
  repository, staged/base selection, spaces/newlines, marker after frontmatter,
  uppercase extension preservation, binary NUL and split-line negatives,
  closed CLI, Git partial-output failure, head/grep failure, missing inputs and
  unsafe symlink/path rejection before a marker read.
- ShellCheck and shfmt are unavailable; no installation or lint PASS claimed.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| R09/R12/R34/R39 supporting checks | W5 | Focused/full H and Bash syntax PASS; installed lint unavailable | Existing style helper, skill and helper regression class |

## Review Evidence

Independent code-reviewer specification and quality verdicts: CLEAR / APPROVED.
Review found and verified corrections for global case-insensitive matching
changing extension buckets, and shell substitution losing binary NUL bytes.
The final helper uses a consuming non-quiet grep with pipeline status checking,
retains case-sensitive extension classification and reports neither partial
Git discovery nor failed marker reads as successful bucket output.
The known path-check/read race limitation is explicitly documented; W5 does not
claim descriptor-based race protection. No new dependency or framework.

## Commit Ledger

Task predecessors: draft `626179d1b`, ready `9f365996a`, in-progress `f92ef7d9d`.
The reviewed implementation and this completion receipt form one logical commit;
Git records its hash. Required broad/native acceptance remains owned by W10.

## Rulings

Explicitly waiting for the Git discovery child is permitted; the failure is
lost exit status, not process substitution itself. Use root-relative bounded
marker reads and inspect their status before matching. No new helper module,
parser, manifest, CI leaf or global configuration is needed.

## Deferred Items

W10 owns final broad/coverage/native acceptance. The evaluation subsystem stays
at its current path during W5; the user-authorized migration is assigned to W9.
