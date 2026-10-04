---
title: "Workflows"
version: "1.3.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-04"
---

# Workflows

This document owns repeatable provider-neutral workflow order. Provider
adapters may map native controls but may not redefine these states.

## Change Lifecycle

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
   [approval boundaries](approval-boundaries.md#authorization-source-and-records);
   Task records describe evidence and never authenticate it.
4. **Implement** — the assigned contributor changes only approved scope.
5. **Validate** — `qa-engineer` runs focused checks and any applicable
   repository Gate; a configured hook is supporting evidence, not approval.
6. **Independent review** — a read-only reviewer who did not implement the
   change evaluates the exact diff and verification evidence.
7. **Evidence** — the Task records commands, results, recovery, skipped checks
   with rationale, review disposition, and remaining uncertainty.
8. **Handoff** — `workflow-supervisor` reports the next owner or completion
   without broadening scope.

After required approval, routine semantic review may close through the smallest
relevant deterministic checks plus an independent read-only agent reviewer who
did not implement the change. The reviewer evaluates the same diff and revision,
maps each applicable acceptance criterion to its canonical source and evidence,
and rejects unsupported claims. Record findings, `BLOCKED`, `NOT_RUN`, and
remaining uncertainty in the owning Task. Escalate semantic review to a human
when criteria or authority remain ambiguous, reviewers disagree, high-risk
uncertainty remains, a new or out-of-scope operation is needed, or a canonical
or protected-branch rule requires human review. Existing approval remains
applicable only while its recorded scope is unchanged; review and delegation
cannot broaden it.

Static validation and independent review precede a separately approved
operational action. An implementation that fails validation or independent
review may receive one narrower retry, for at most two implementation attempts.
A retry may correct the approved change but may not infer approval, add scope,
change owners, or weaken a Gate. Stop mutation and reconcile the Task when the
repository, worktree, HEAD, relevant digest, current approval, exclusive writer,
or partial-result state disagrees with the recorded handoff. Stop and escalate
after the bound, on unknown ownership, on an unresolved policy conflict, or
when required evidence is unavailable.

Evidence is value-free and sanitized. Never record auth files, credentials,
private keys, raw logs, secret values, shell history, or tokens. Historical
citations and archive records preserve provenance only; they cannot authorize a
current operation.

## SDLC Workflow

1. Capture long-lived, solution-independent needs in Stage 01.
2. Capture current structure and durable decisions in Stage 02.
3. Define a bounded change contract, approach, plan, and Task in Stage 03.
4. Implement only approved Task scope and verify its acceptance contract.
5. Maintain operator knowledge and runtime procedures in Stage 05.
6. Preserve external evidence in Stage 90 and minimal recovery in Stage 98.

`sdlc.md` owns stage boundaries, the Stage 99 registry owns document shapes
and lifecycle values, and `scripts/` owns executable validation.

## Supporting Workflows

- Infrastructure: `compose-stack-agent` -> `infra-validate` -> independent review.
- Code review: self-verification -> findings -> owner resolution -> re-verification.
- Quality: tests first for behavior changes -> QA verification -> Task evidence.
- Security: audit plus threat modeling; escalate exposed secrets or critical risk.
- Incident: response record -> corrective Task routed to its canonical stage.
- Governance: source change -> validation -> regeneration -> independent review.

Agents run all-files pre-commit only through
`scripts/validation/run-agent-precommit-all-files.sh` and only after the
task-owned state is a Git-visible, non-ignored repository change.

## Skill Lifecycle

Reusable procedures follow discovery, applicability, canonical agent governance source,
registered projection, focused validation, and evidence. Provider projections
do not own this lifecycle.

## Related Documents

- [SDLC](sdlc.md)
- [Agentic policy](agentic.md)
- [Stage authoring matrix](stage-authoring-matrix.md)
- [Provider capability matrix](provider-capability-matrix.md)
