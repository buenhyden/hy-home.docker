---
title: "Workflows"
version: "2.0.0"
type: "governance/workflow"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: Workflows
  layer: agent
updated: "2026-11-20"
---

# Workflows

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the contract payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose

This document owns repeatable provider-neutral workflow order. Provider
adapters may map native controls but may not redefine these states.

#### Inputs

The approved Spec Package and current Task, canonical roles, required governance, and source-bound repository state.

#### Sequence

##### Change Lifecycle

Every repository change follows one lifecycle:

1. **Discover** — `workflow-supervisor` identifies the objective, current
   owners, protected boundaries, and repository state without mutation.
2. **Design/plan** — an approved contributor records the bounded approach,
   acceptance contract, recovery, and smallest meaningful checks in the active
   Spec Package and Task.
3. **Approval** — human approval for a new or unapproved scope, then the
   written Spec, Plan, and execution are distinct. A current explicit request
   remains effective for its unchanged scope and does not require repeated
   routine human approval. Required approval and read-only `rules-engineer`
   policy review are resolved before a protected mutation begins. The
   authorization source is owned by
   [approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md#authorization-source-and-records);
   Task records describe evidence and never authenticate it.
4. **Implement** — the assigned contributor changes only approved scope.
5. **Validate** — `qa-engineer` runs focused checks and any applicable
   repository Gate; a configured hook is supporting evidence, not approval.
6. **Review by risk** — the change gets the review its class requires under
   the [review risk standard](../../docs/00.workspace/04.quality/quality-standards.md#11-review-risk);
   [Review risk](#review-risk) below is how an agent runs it.
7. **Evidence** — the Task records commands, results, recovery, skipped checks
   with rationale, review disposition, and remaining uncertainty.
8. **Handoff** — `workflow-supervisor` reports the next owner or completion
   without broadening scope.

After required approval, a high-risk semantic review may close through the
smallest relevant deterministic checks plus an independent read-only agent
reviewer who did not implement the change. The reviewer evaluates the same diff and revision,
maps each applicable acceptance criterion to its canonical source and evidence,
and rejects unsupported claims. Record findings, `BLOCKED`, `NOT_RUN`, and
remaining uncertainty in the owning Task. Escalate semantic review to a human
when criteria or authority remain ambiguous, reviewers disagree, high-risk
uncertainty remains, a new or out-of-scope operation is needed, or a canonical
or protected-branch rule requires human review. Existing approval remains
applicable only while its recorded scope is unchanged; review and delegation
cannot broaden it.

##### Review Risk

The [review risk standard](../../docs/00.workspace/04.quality/quality-standards.md#11-review-risk)
owns the three classes and the review each requires. An agent applies it
this way: `workflow-supervisor` takes the higher class when unsure, assigns a
high-risk independent reviewer or a medium-risk primary reviewer who did not
write the change, and hands the reviewer the exact diff, the governing
criteria and the recorded check results with the
[diff review checklist](../prompts/diff-review.md). A low-risk author check
is recorded in the Task and is not called independent review.

A reviewer counts as read-only only where its runtime enforces it. When a
spawned reviewer would run with its parent's write access, or enforcement
on that route is unobserved, the review runs from a read-only parent. A
review whose read-only state was not enforced is recorded as such in the
owning Task and does not meet a read-only review requirement until it is
rerun on an enforced route or a human accepts it. The
[capability matrix](provider-capability-matrix.md) records the observed
routes.

##### Review Scope and Evidence Updates

One final independent review covers one frozen logical diff and its applicable
check evidence. Assign its owner and required expertise before execution. A
specialist review is added for an actual security, infrastructure or policy
boundary; it covers that boundary rather than replaying the whole diff. Any specialist review explicitly required by the protected-surface table or
another governing policy remains mandatory. A proposal review can
inform a protected change decision but does not replace final applied-input
review or supply authorization.

A correction invalidates only the affected source/evidence slice. Reuse a prior
review only when its exact bytes, contract, input and trust remain applicable;
changed dependencies, authority or criteria require affected revalidation.
Result-only Task updates receive document-minimum validation and evidence-delta
readback. They do not restart implementation tests, full QA or an unchanged
source review. A result update that changes contract meaning, acceptance or
approval is reviewed for that change. Preserve actual failures and review
history; do not manufacture a new approval from an existing verdict.

Each review's Task evidence row records when the reviewer was dispatched and
when it returned, and how many review rounds the change took. A number that
was not observed, such as queue wait or context loading inside the
reviewer, is reported as unmeasured, never estimated.

Static validation and independent review precede an operational action,
which waits for its exact target. An implementation that fails validation or independent
review may receive one narrower retry, for at most two implementation attempts.
A retry may correct the approved change but may not infer approval, add scope,
change owners, or weaken a Gate. Stop mutation and reconcile the Task when the
repository, worktree, HEAD, relevant digest, current approval, exclusive writer,
or partial-result state disagrees with the recorded handoff. Stop and escalate
after the bound, on unknown ownership, on an unresolved policy conflict, or
when required evidence is unavailable.

Evidence is value-free and sanitized. Never record auth files, credentials,
private keys, raw logs, secret values, shell history, or tokens. Historical
citations and version history preserve provenance only; they cannot authorize a
current operation.

##### SDLC Workflow

The [SDLC sequence](../../docs/00.workspace/03.process/sdlc.md#sequence) owns the stage order. `sdlc.md` owns stage boundaries, the Stage 99 registry owns document shapes
and lifecycle values, and `scripts/` owns executable validation.

##### Supporting Workflows

- Infrastructure: `compose-stack-agent` -> `infra-validate` -> independent review.
- Code review: self-verification -> findings -> owner resolution -> re-verification.
- Quality: tests first for behavior changes -> QA verification -> Task evidence.
- Security: audit plus threat modeling; escalate exposed secrets or critical risk.
- Incident: response record -> corrective Task routed to its canonical stage.
- Governance: source change -> validation -> regeneration -> independent review.

The [execution boundary](../../docs/00.workspace/04.quality/quality-standards.md#4-execution-boundary) owns the
only approved all-files pre-commit route and its clean linked-worktree,
Task, prefix, and Git-visible-state conditions. Workflows does not create a
second local invocation path.

##### Skill Lifecycle

Reusable procedures follow discovery, applicability, canonical agent governance source,
registered projection, focused validation, and evidence. Provider projections
do not own this lifecycle.

#### Stop Conditions

Apply the authorization and retry limits in Change Lifecycle. Missing authority, conflicting ownership, repeated failed verification, or a changed source binding stops the dependent operation.

#### Outputs

Task-owned commands, results, review disposition, sanitized evidence, and the next accountable owner.

#### Related Documents

- [SDLC](../../docs/00.workspace/03.process/sdlc.md)
- [Agentic policy](agentic.md)
- [Stage authoring matrix](../../docs/00.workspace/01.project/stage-authoring-matrix.md)
- [Provider capability matrix](provider-capability-matrix.md)

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
