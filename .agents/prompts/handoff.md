---
title: "Handoff Prompt"
version: "2.0.0"
type: "governance/prompt"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: Handoff Prompt
  layer: agent
updated: "2026-11-20"
created: "2026-09-06"
---

# Handoff Prompt

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the prompt payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose

Produce a handoff that lets the next session reconstruct its working state
from tracked files and Git. The receiving session may be a different provider,
a different model, or the same agent after a context reset. The controller
resolves current authorization through
[Approval Boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md#authorization-source-and-records).

#### Inputs

- The current Spec Package Task path and its `Work Performed`, `Results`, and
  `Next Owner` subsections.
- Branch name and `git rev-parse HEAD`, both read from Git. A branch name
  written in a Task is historical: a short branch is retired at integration,
  so the file cannot stay current. Report the Git value, and report a
  disagreement with the Task rather than reconciling it.
- `git status --porcelain` output, so uncommitted work is stated rather than
  implied.
- The approval scope recorded in the Task's `Inputs and Authority`.
- The governing Spec's `Acceptance Contract` and the Plan's work-unit labels.
- Repository and worktree identities, relevant owned-file digests, request
  identity and revision when supplied by the trusted origin, authorization
  source, scope and current applicability, exclusive writer, partial-result state,
  declared applicable request, token, time, concurrency, and retry ceilings;
  shared-budget identity and remaining allocation; unsupported fields recorded
  as unknown; and knowledge validity.

The receiver re-reads Git, the Task and the applicable trusted request. For a
repository, worktree, HEAD, digest, writer, partial-result, budget or
knowledge-validity mismatch, reconcile the dependent work. For a changed
request, resolve whether the latest authority still covers the target, scope
and conditions. Keep using the approval if it still applies. If a material
mismatch or unresolved applicability prevents continuation, stop dependent
mutation and additional spending, record the missing binding, and return to
`workflow-supervisor`. A digest records resume evidence. Ask for missing input
only when it is needed for the dependent work.

#### Instructions

##### Constraints

- Conversation transcripts, chat excerpts, or reasoning narration.
- Secret values, credentials, private keys, tokens, auth files, raw logs, or
  shell history.
- User-global provider settings or any path outside the repository.
- A second progress or handoff document. The Task is the only such authority;
  this prompt renders a view of it and writes no new ledger.
- Promoting a configured, static, or local result into runtime, entitlement,
  Hosted CI, or remote acceptance.
- Restating a policy body. Link the owning policy instead.

##### Applies To

- Roles: any role may consume a handoff; `workflow-supervisor` owns producing
  one at a boundary. Consuming a handoff grants no permission beyond the
  reader's own role and approved Task scope.
- Skills: [execution-plan-agent](../skills/execution-plan-agent/SKILL.md) owns
  sequencing procedure; this prompt owns only the handoff envelope.
- Evaluation: the handoff is adequate when a reader with no prior context can
  name the next action, the owned paths, and the unverified state without
  opening the previous conversation.

#### Outputs

A single block with exactly these labeled parts, in this order:

1. **Task** — the Task path and artifact id; the governing Spec and Plan.
2. **Position** — repository and worktree identities, branch, HEAD, relevant
   owned-file digests, working-tree state, and which Plan work unit is next.
3. **Purpose** — the objective in one sentence, taken from the Spec.
4. **Approved scope** — what the current authorization does and does not cover,
   including the request identity and revision supplied by the trusted origin
   or recorded as unknown, the authorization source and applicability, and its
   declared applicable request, token, time, concurrency, and retry ceilings;
   shared-budget identity and remaining allocation; and unsupported fields
   recorded as unknown, not inferred.
5. **File ownership** — which paths this work owns, the exclusive writer, the
   partial-result state, and which paths belong to a concurrent package or
   another worker and must not be touched.
6. **Verification state** — each check with its exit code and one of PASS,
   FAIL, BLOCKED, NOT_RUN, or N/A, plus knowledge validity. A blocked or
   unexecuted check names its missing input.
7. **Not executed** — checks, observations, and actions deliberately not
   performed, each with its reason.
8. **Next action** — the single next step, expressed as a command or an edit to
   a named file.

Every claim is traceable to a tracked file or a Git fact. Where a claim is not,
the handoff says so.

#### Failure Handling

If the Task's recorded state disagrees with observed Git state, report the
disagreement and stop; do not reconcile it inside the handoff. If the Task is
absent or terminal while work remains, route to `workflow-supervisor` rather
than opening a new ledger. If a required input is unavailable, emit the handoff
with that part marked unavailable and name what is needed.

#### Related Documents

- [Prompt index](README.md)
- [Workflows](../governance/workflows.md)
- [Task checklists](../../docs/00.workspace/04.quality/task-checklists.md)
- [Approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
