---
title: "Handoff Prompt"
version: "0.2.0"
type: "governance/prompt"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-07"
created: "2026-09-06"
---

# Handoff Prompt

## Purpose

Produce a handoff that lets the next session resume from tracked files and Git
state alone. The receiving session may be a different provider, a different
model, or the same agent after a context reset. The handoff exists so that
resuming never requires the previous conversation.

## Required Inputs

- The current Spec Package Task path and its `Work Log`, `Verification
  Evidence`, and `Commit Ledger` sections.
- Branch name and `git rev-parse HEAD`, both read from Git. A branch name
  written in a Task is historical: a short branch is retired at integration,
  so the file cannot stay current. Report the Git value, and report a
  disagreement with the Task rather than reconciling it.
- `git status --porcelain` output, so uncommitted work is stated rather than
  implied.
- The approval scope recorded in the Task's `Inputs`.
- The governing Spec's `Acceptance Contract` and the Plan's work-unit labels.

Stop and request the missing input if the Task, the branch, or the approval
scope cannot be identified.

## Output Contract

A single block with exactly these labeled parts, in this order:

1. **Task** — the Task path and artifact id; the governing Spec and Plan.
2. **Position** — branch, HEAD, working-tree state, and which Plan work unit is
   next.
3. **Purpose** — the objective in one sentence, taken from the Spec.
4. **Approved scope** — what the current authorization does and does not cover,
   copied from the Task, not inferred.
5. **File ownership** — which paths this work owns, and which paths belong to a
   concurrent package or another worker and must not be touched.
6. **Verification state** — each check with its exit code and one of PASS,
   FAIL, BLOCKED, NOT_RUN, or N/A. A blocked or unexecuted check names its
   missing input.
7. **Not executed** — checks, observations, and actions deliberately not
   performed, each with its reason.
8. **Next action** — the single next step, expressed as a command or an edit to
   a named file.

Every claim is traceable to a tracked file or a Git fact. Where a claim is not,
the handoff says so.

## Prohibited

- Conversation transcripts, chat excerpts, or reasoning narration.
- Secret values, credentials, private keys, tokens, auth files, raw logs, or
  shell history.
- User-global provider settings or any path outside the repository.
- A second progress or handoff document. The Task is the only such authority;
  this prompt renders a view of it and writes no new ledger.
- Promoting a configured, static, or local result into runtime, entitlement,
  Hosted CI, or remote acceptance.
- Restating a policy body. Link the owning policy instead.

## Failure Handling

If the Task's recorded state disagrees with observed Git state, report the
disagreement and stop; do not reconcile it inside the handoff. If the Task is
absent or terminal while work remains, route to `workflow-supervisor` rather
than opening a new ledger. If a required input is unavailable, emit the handoff
with that part marked unavailable and name what is needed.

## Applies To

- Roles: any role may consume a handoff; `workflow-supervisor` owns producing
  one at a boundary. Consuming a handoff grants no permission beyond the
  reader's own role and approved Task scope.
- Skills: [execution-plan-agent](../skills/execution-plan-agent/SKILL.md) owns
  sequencing procedure; this prompt owns only the handoff envelope.
- Evaluation: the handoff is adequate when a reader with no prior context can
  name the next action, the owned paths, and the unverified state without
  opening the previous conversation.

## Related Documents

- [Prompt index](README.md)
- [Workflows](../governance/workflows.md)
- [Task checklists](../governance/task-checklists.md)
- [Approval boundaries](../governance/approval-boundaries.md)
