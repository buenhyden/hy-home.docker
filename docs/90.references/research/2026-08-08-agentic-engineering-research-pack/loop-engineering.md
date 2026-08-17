---
status: draft
artifact_id: reference:agentic-engineering-research:loop-engineering
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-17
review_cycle: on-source-change
---

# Reference: Loop Engineering

## Overview

Loop engineering turns agent activity into bounded feedback systems. Each loop
needs an observable input, an authorized action, a result or failure signal, a
stop condition, a retry ceiling, an escalation route, and sanitized evidence.
Without those elements, repeated prompting is merely repetition rather than a
controlled loop.

This reference satisfies REQ-02 at baseline
`9a6e09ca06d99ae8234199443974c978640f3ae6`. It separates the four canonical
typed harness loops from broader analytical patterns and from provider-native
event loops.

## Purpose

Define loop elements and feedback patterns, measure the local typed workflow,
hook, evaluation, and review implementation, and state where feedback is
configured, repository-enforced, runtime-unverified, or outside current scope.

## Repository Role

This Stage 90 leaf explains current loop structure and gaps. The exact retry,
stop, permission, reviewer, and evidence values remain owned by
`contracts/provider-models.yaml`; this document creates no prompt-local retry
policy and authorizes no execution.

## Scope

### In scope

- Agent observation/action, validation, review, approval, evaluation, memory,
  automation, CI, incident, and human decision feedback.
- The eight workflow states, four typed loops, seven semantic events, hook
  dispatcher, fixtures, regressions, and relevant tests.
- Claude and Codex loop mechanisms and all fourteen scope implications.

### Out of scope

- Hidden chain-of-thought or unobservable internal reasoning.
- Live provider quality comparisons, telemetry, remote CI enforcement, service
  health, private state, credentials, raw logs, or secret values.
- Adding retry counters, hooks, workflows, fixtures, or provider mappings.

## Definitions / Facts

### Loop anatomy

| Element            | Required question                                        | Failure when absent                                |
| ------------------ | -------------------------------------------------------- | -------------------------------------------------- |
| Trigger/input      | What current observation starts this attempt?            | Work begins from stale or ambiguous state.         |
| Owner              | Who may act and at what permission level?                | Responsibility and authority become implicit.      |
| Action             | What bounded operation is allowed?                       | The loop expands scope or changes unrelated state. |
| Feedback           | What result can alter the next decision?                 | Retries repeat without diagnosis.                  |
| Exit gate          | What observable condition means success?                 | Completion becomes subjective.                     |
| Attempt ceiling    | How many attempts may occur?                             | A hook or agent can loop indefinitely.             |
| Failure route      | Narrow, stop, return, or escalate to whom?               | Failure is suppressed or silently bypassed.        |
| Independent review | Who checks the result without owning the implementation? | Self-review is mistaken for final approval.        |
| Evidence           | Which sanitized fields survive the run?                  | Secrets/raw logs leak or no durable proof remains. |

### Canonical lifecycle and typed loops

The ordered lifecycle has eight states:
`discover -> design/plan -> approval -> implement -> validate -> independent-review -> evidence -> handoff`.
`harness_loops` references those states; it is not a second lifecycle.

| Event ID                      | States                            | Owner / reviewer                         | Permission        | Attempts | Stop condition                | Failure route          | Depth                 |
| ----------------------------- | --------------------------------- | ---------------------------------------- | ----------------- | -------: | ----------------------------- | ---------------------- | --------------------- |
| `context-bootstrap`           | `discover`                        | `workflow-supervisor` / `rules-engineer` | `read-only`       |        1 | `bootstrap-contract-pass`     | `escalate`             | `repository-enforced` |
| `bounded-implementation-loop` | `implement`, `validate`           | `qa-engineer` / `code-reviewer`          | `workspace-write` |        2 | `focused-checks-pass`         | `narrow_then_escalate` | `repository-enforced` |
| `independent-review-loop`     | `implement`, `independent-review` | `code-reviewer` / `eval-engineer`        | `read-only`       |        2 | `critical_and_important_zero` | `escalate`             | `repository-enforced` |
| `approved-all-files-gate`     | `validate`, `evidence`            | `qa-engineer` / `code-reviewer`          | `workspace-write` |        1 | `controlled-wrapper-pass`     | `record_and_stop`      | `repository-enforced` |

All four loops require the same evidence keys: `command`, `result`, `rollback`,
and `skipped_checks`. They prohibit auth files, credentials, raw logs, secret
values, shell history, and tokens. Each reviewer differs from the owner.
Validator tests enforce those structural properties. `repository-enforced`
means the repository validates the contract and gates its own workflow; it is
not proof that a provider event fired during this Task.

### Analytical feedback patterns

The predecessor leaf presented ten prose rows. That count describes an
analytical taxonomy, not ten typed or independently enforced loop objects. The
old text then called seven named patterns “the remaining six,” an arithmetic
and modeling error. The current interpretation keeps the useful ten-pattern
taxonomy but does not subtract the four typed controls from it: the two views
overlap and have no one-to-one mapping.

| Pattern                | Feedback signal                                     | Exit/evidence owner                             | Typed relation and current state                                                                  |
| ---------------------- | --------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Reason/action          | Latest tool observation or clarification            | Task implementer; inspected source/diff         | Provider loop; constrained by typed bootstrap/implementation controls, hidden reasoning excluded. |
| Validation/format/lint | Focused check result                                | QA; exact command/result/skip                   | Closest to `bounded-implementation-loop`; locally executable.                                     |
| CI gate                | Remote job/check state                              | CI/CD owner; remote run evidence                | No separate typed retry object; tracked workflow definition is not remote proof.                  |
| Evaluation/regression  | Fixture score and threshold                         | Eval owner; 11 fixtures/16 regressions          | Invoked by QA/harness gates; synthetic-only, no live model benchmark.                             |
| Memory/context         | Verified milestone, decision, or stale finding      | Lifecycle owner; canonical artifact             | Bootstrap/evidence relationship; Memory remains advisory.                                         |
| Plan/task/review       | Exact diff plus reviewer verdict                    | Controller/reviewer; Stage 04 evidence          | Closest to independent-review loop; SDD adds its own reviewed plan bounds.                        |
| Security/approval      | Explicit decision on protected action               | User/security/owner; redacted approval evidence | Approval state controls action; native permission mode never broadens authority.                  |
| Automation/pipeline    | Stage result and propagated failure                 | Pipeline owner; immutable input/result          | No separate typed retry object; idempotence and external authority remain explicit.               |
| Incident/postmortem    | Service symptom, recovery state, prevention action  | Incident commander/owner; Stage 05 evidence     | Applicable only to real incidents; no live service evidence in this Task.                         |
| Human pause/resume     | Approve/reject/narrow decision plus refreshed state | Named human; decision and postcondition         | Provider checkpoint semantics vary; stale state requires a new decision.                          |

### External loop-primitive taxonomy versus the four typed loops

A 2026 source-code study of 13 open-source coding-agent scaffolds at pinned
commits (arXiv 2604.03515, retrieved 2026-08-14) identifies five composable
control-loop primitives — ReAct, generate-test-repair, plan-execute,
multi-attempt retry, and tree search — and finds 11 of 13 scaffolds combine
more than one primitive rather than relying on a single loop. Mapped against
this workspace's four typed loops:

| Typed loop                    | Nearest external primitive                                 | Fit                                                                                                                                                                                                   |
| ----------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `context-bootstrap`           | None of the five (a pre-loop discovery gate)               | Not a control-loop primitive in that taxonomy; it precedes one.                                                                                                                                       |
| `bounded-implementation-loop` | Multi-attempt retry, with elements of generate-test-repair | Partial: the 2-attempt ceiling matches "multi-attempt retry," but the loop does not itself run a test-repair cycle — `focused-checks-pass` is an external validator call, not an in-loop repair step. |
| `independent-review-loop`     | Generate-test-repair (review-as-verification variant)      | Partial: `critical_and_important_zero` is a review-verdict gate, not a code-execution test.                                                                                                           |
| `approved-all-files-gate`     | None of the five (a terminal one-shot gate)                | Not iterative; `max_attempts: 1` makes it a checkpoint, not a loop.                                                                                                                                   |

No typed loop corresponds to **plan-execute** or **tree search**. This is a
named gap, not a defect: `workflow_states` supplies a `design/plan` state and
`approval` gate around the four loops, so planning exists at the lifecycle
level, but no typed loop re-plans and re-attempts with backtracking the way a
tree-search or plan-execute primitive would. The observation that would close
this gap is a Stage 00 decision on whether backtracking/replanning behavior
should become a fifth typed loop or stay an untyped, agent-discretion pattern
under `independent-review-loop`'s `escalate` route.

A companion 2026 study of 20,574 real-world coding-agent sessions across
1,639 repositories (arXiv 2605.29442, retrieved 2026-08-14) found 90.50% of
misalignment episodes cost effort/trust rather than causing system damage,
yet 91.49% still required explicit user correction, across seven recurring
failure categories including how agents bound their own actions and report
progress. This corroborates, from an external and much larger sample, the
same three failure shapes this pack's typed-loop model exists to prevent:
unbounded action (addressed here by `max_attempts` and `permission_profile`),
unverified self-reporting (addressed by requiring `command`/`result` evidence
fields), and silent scope drift (addressed by `narrow_then_escalate` on
`bounded-implementation-loop`). None of this workspace's typed-loop evidence
was drawn from that external session corpus; the correspondence is
structural, not a shared dataset.

### Unbounded loop risk in this workspace

Three concrete places where this workspace's tracked construction could run
without an enforced ceiling, verified by reading the executing code rather
than the contract prose:

1. **`max_attempts` is a contract field, not a counted runtime value.**
   `contracts/provider-models.yaml` `harness_loops` declares
   `max_attempts: 2` for `bounded-implementation-loop` and
   `independent-review-loop`, but no script in `scripts/hooks/` or
   `scripts/validation/` reads or increments an attempt counter against that
   field. The ceiling is a documented behavioral expectation for the agent
   and its reviewer to self-observe, not a tool-enforced stop. An agent (or a
   provider auto-retry) that ignores the contract has no local mechanism that
   would block a third attempt.
2. **`PreToolUse` can repeat the same advisory guidance indefinitely.**
   Because the repository dispatcher treats `PreToolUse` as advisory only
   (see [harness-engineering.md](./harness-engineering.md)), a session that
   keeps triggering the same changed-path pattern (for example repeatedly
   editing a target-stage doc without fixing the template violation) receives
   the same reminder text on every call with no escalation, count, or
   eventual block — the loop's "failure route" for that specific trigger is
   undefined below the `Stop` gate.
3. **The Stop gate's retry bound is a provider-payload interpretation, not a
   repository counter.** `template_stop_gate` and `logical_commit_stop_gate`
   in `scripts/hooks/agent-event-hook.sh` decide `continue: false` only when
   the _provider_ reports `stop_hook_active: true` in its payload (Codex
   branch) or via the Claude-native blocking response; the repository itself
   keeps no count of how many times Stop has already fired in this session.
   If a provider's payload shape changed to omit `stop_hook_active`, or if
   Gemini's `AfterAgent` `deny-retry` mode (recorded in
   `contracts/provider-models.yaml`, not previously described in this pack)
   never signals a terminal retry, the bash-level loop has no independent
   ceiling of its own.

None of these is a defect in what is documented — the contract is explicit
that these are behavioral/self-observed bounds — but they are the concrete
answer to "where can a loop here run unbounded," which this pack's earlier
revision did not enumerate.

### Semantic-event feedback depth

The semantic contract has seven events and three provider cells per event. At
this baseline, 20 of 21 cells are `configured-not-executed`; the Codex
`session-end` cell is `unsupported`. The predecessor claim that all 21 were
configured is therefore corrected.

| Semantic event       | Claude local       | Codex local        | Repository mode / finding                                                                                                |
| -------------------- | ------------------ | ------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| `session-start`      | `SessionStart`     | `SessionStart`     | Advisory context; configured, not execution proof.                                                                       |
| `pre-tool`           | `PreToolUse`       | `PreToolUse`       | Provider can block; repository dispatcher is advisory.                                                                   |
| `post-tool`          | `PostToolUse`      | `PostToolUse`      | Runs shared changed-file validation routing when fired.                                                                  |
| `pre-compaction`     | `PreCompact`       | `PreCompact`       | Advisory; no `PostCompact` local binding.                                                                                |
| `user-prompt-intake` | `UserPromptSubmit` | `UserPromptSubmit` | Provider can block; local repository mode is advisory.                                                                   |
| `stop`               | `Stop`             | `Stop`             | Claude `blocking`; Codex `retry`; shared target-doc and uncommitted-work gates.                                          |
| `session-end`        | `SessionEnd`       | No local binding   | Contract says Codex unsupported, but current official Codex docs support a main-thread advisory `SessionEnd`; local gap. |

Claude wires all seven tracked semantic events. Codex wires six. Current
official documentation enumerates 31 Claude event names and 11 Codex event
names, but event vocabulary size does not measure local coverage or
enforcement. Only Stop is configured as a blocking/retry repository gate here;
the other provider primitives remain advisory in local policy even where the
vendor permits a blocking decision.

### Stop and retry behavior

The shared dispatcher distinguishes provider payloads. Claude receives a
blocking decision plus a reason. Codex receives `decision: block` on the first
failed Stop gate; if the provider payload marks `stop_hook_active`, the second
failure returns `continue: false` and a `stopReason`. This is a bounded local
translation of provider semantics, not a general repository counter. A vendor
payload change could therefore invalidate the behavior and must be tested
against current official schemas.

The gate currently checks changed target-stage document contracts and
task-owned uncommitted work. `post-tool-validate.sh` routes focused style,
syntax, Compose, governance, and traceability checks by changed path. Hook
configuration and dispatcher tests demonstrate local construction, but this
Task did not execute a native Claude or Codex session to prove firing.

A third Stop-equivalent mode exists in the tracked contract but was not
previously recorded here: `contracts/provider-models.yaml`'s `stop`
semantic-event row lists Gemini's native binding as `AfterAgent` with
`repository_hook_mode: deny-retry` and `provider_can_block: true`.
`providers/gemini.md` §6 explains the mechanism directly: `AfterAgent` "may
deny a response and force a retry; it maps to the shared Stop gate as
`deny-retry`, not as an irreversible session stop." This is a third distinct
retry shape alongside Claude's single blocking response and Codex's
two-strike `stop_hook_active` escalation — three providers, three different
native retry primitives, one shared Python decision function
(`template_stop_gate`/`logical_commit_stop_gate`) translating into each.
Official Claude documentation retrieved 2026-08-14 adds a schema detail not
previously recorded: Claude's `Stop` hook accepts _either_ an exit-code-2
block _or_ a JSON `continue: false` + `stopReason` response — two independent
mechanisms for the same blocking outcome, both consumed by this repository's
shared dispatcher output.

The two Hookify rules scoped to `event: stop`
(`require-logical-commits-before-stop`, `warn-docker-infra-stop` — see
[harness-engineering.md](./harness-engineering.md) for the full catalog) name
the same completion behavior already hard-coded in
`logical_commit_stop_gate`. They add no additional retry ceiling or stop
condition of their own; they exist as human-readable policy text with no
verified runtime execution path in this worktree.

### Environment and rules for workspace application

Each rule below restates a fact established earlier in this leaf; none
introduces a new claim or copies a policy body from a canonical owner. The
companion harness-side list is
[harness-engineering.md](./harness-engineering.md).

1. Name all nine loop-anatomy elements before the first attempt. An
   unstated trigger, owner, exit gate, attempt ceiling, or failure route is
   the failure mode itself, not a detail to settle mid-loop.
2. Select one of the four typed loops declared in `harness_loops` and stay
   inside its declared states, permission profile, and stop condition. Do not
   invent a fifth typed loop: no typed loop covers plan-execute or tree
   search, and closing that gap requires a Stage 00 decision, not
   agent discretion.
3. Count attempts yourself. `max_attempts` is a contract field that no script
   in `scripts/hooks/` or `scripts/validation/` reads or increments, so the
   ceiling binds only the owner and reviewer who self-observe it. Treat a
   third attempt as a boundary breach even though nothing local blocks it.
4. Do not mistake repeated advisory output for a control. `PreToolUse`
   guidance re-emits on every matching call with no count, escalation, or
   block, so the same reminder arriving again is evidence of an unbounded
   trigger rather than of enforcement.
5. Treat the Stop gate as a provider-payload translation, not a repository
   counter. Claude's blocking response, Codex's two-strike
   `stop_hook_active` escalation, and Gemini's `AfterAgent` `deny-retry` are
   three distinct native primitives behind one shared decision function; a
   vendor schema change can invalidate the bound, so re-test against current
   official schemas before relying on it.
6. Route failure explicitly to the declared destination — narrow, stop,
   record, or escalate — and require a reviewer distinct from the loop owner.
   `critical_and_important_zero` is a review-verdict gate, so self-review
   cannot close it.
7. Record exactly `command`, `result`, `rollback`, and `skipped_checks`, and
   keep auth files, credentials, raw logs, secret values, shell history, and
   tokens outside the evidence. `repository-enforced` means the repository
   validated its own contract, never that a provider event fired.
8. Keep the ten analytical feedback patterns as analysis. They overlap the
   four typed controls with no one-to-one mapping, and converting any of them
   into retry policy requires a reviewed Stage 00/03/04 change.

## Scope Implications

The status and owner basis comes from the
[scope application matrix](./scope-application-matrix.md); every row below is
the loop-specific implication.

| Scope          | Loop implication                                                                         | Disposition / exit route                                                |
| -------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `agentic`      | Owns lifecycle, typed retry/stop controls, provider translation, and handoff.            | Implemented as contracts; provider execution unverified.                |
| `architecture` | Design/review loops return unresolved trade-offs to ARD/ADR/Spec.                        | Partial; human/system architect route, no typed agent.                  |
| `backend`      | Build/test/deploy feedback applies after a backend is specified.                         | Not Applicable now; stop until product/Spec surface exists.             |
| `common`       | Diff hygiene and independent correctness review close cross-layer loops.                 | Partial; use `code-reviewer`; no direct all-files pre-commit.           |
| `docs`         | Template, metadata, link, source, and review feedback closes document work.              | Implemented locally; route switch and pack review pending.              |
| `entry`        | Gateway validation and incident feedback require infra ownership and runtime evidence.   | Partial; escalate through infra/ops; edge state unverified.             |
| `frontend`     | UI build, accessibility, browser, and regression loops bind only to an actual surface.   | Partial; current Storybook fixture is QA-owned.                         |
| `infra`        | Compose preflight, drift, rollout, rollback, and postcheck form controlled loops.        | Definitions exist; live loops were not run.                             |
| `meta`         | Metadata and generator freshness provide deterministic documentation feedback.           | Partial; route through docs; typed meta agent missing.                  |
| `mobile`       | Device/build/signing/store feedback requires a mobile surface.                           | Not Applicable; no tracked source or runtime.                           |
| `ops`          | Monitoring, incident, recovery, postmortem, and follow-up loops need live evidence.      | Partial; no service or incident proof collected.                        |
| `product`      | Human decisions close priority, risk, cost, and acceptance feedback.                     | Partial; human approval precedes implementation.                        |
| `qa`           | Owns focused validation, fixture/regression scoring, aggregate gates, and evidence.      | Extensive local implementation; remote and live-model state unverified. |
| `security`     | Protected actions pause for approval; findings return to the owning implementation loop. | Partial; redacted evidence only; secret/runtime state excluded.         |

## Sources

External pages were retrieved 2026-08-08 (initial) and 2026-08-14
(re-verification plus new sources); all returned HTTP 200 without redirect
and expose no stable revision, so they are mutable primary observations, not
permanent runtime guarantees. The two arXiv papers are external mutable
primary sources with a fixed preprint identifier but no confirmed pinned
version in this retrieval; treat exact figures as subject to revision on a
future arXiv version.

| Source                                                                                         | Class                           | Verification                                                                                                          |
| ---------------------------------------------------------------------------------------------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [Claude hooks](https://code.claude.com/docs/en/hooks)                                          | External mutable, primary       | Re-verified 2026-08-14: Stop schema accepts exit-2 or `continue:false`+`stopReason`; full event/decision breakdown.   |
| [Claude subagents](https://code.claude.com/docs/en/sub-agents)                                 | External mutable, primary       | Verified 2026-08-08: isolated contexts, turns, tools, permissions, model/effort, hooks.                               |
| [Codex hooks](https://learn.chatgpt.com/docs/hooks)                                            | External mutable, primary       | Re-verified 2026-08-14: 11-event table, `stop_hook_active`, main-thread `SessionEnd`.                                 |
| [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)                | External mutable, primary       | Verified 2026-08-08: orchestration, thread control, sandbox/permission inheritance.                                   |
| [Inside the Scaffold (arXiv 2604.03515)](https://arxiv.org/abs/2604.03515)                     | External mutable, primary paper | New 2026-08-14: 13 scaffolds, 5 loop primitives, 11/13 combine multiple primitives.                                   |
| [How Coding Agents Fail Their Users (arXiv 2605.29442)](https://arxiv.org/abs/2605.29442)      | External mutable, primary paper | New 2026-08-14: 20,574 sessions/1,639 repos, seven failure categories, 90.50%/91.49% figures.                         |
| [Provider/model contract](../../../00.agent-governance/contracts/provider-models.yaml)         | Workspace tracked               | Re-read 2026-08-14: eight-state, four-loop, seven-event, 21-cell derivation, including Gemini `deny-retry` Stop mode. |
| [Agent catalog](../../../00.agent-governance/contracts/agent-catalog.yaml)                     | Workspace tracked               | Re-read 2026-08-14: `evaluation.fixture_count`/`regression_count` typed fields (11/16), scorer, runner, tests.        |
| [Subagent protocol](../../../00.agent-governance/subagent-protocol.md)                         | Workspace tracked               | Verified human routing view and exact four typed loop rules.                                                          |
| [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) | Workspace tracked               | Re-read 2026-08-14: three-provider Stop-mode row (`blocking`/`retry`/`deny-retry`).                                   |
| [`providers/gemini.md`](../../../00.agent-governance/providers/gemini.md)                      | Workspace tracked               | Read 2026-08-14: `AfterAgent` deny-retry mechanism description.                                                       |
| [Shared dispatcher](../../../../scripts/hooks/agent-event-hook.sh)                             | Workspace tracked, executable   | Read directly 2026-08-14: no attempt-counter code path against `max_attempts`.                                        |
| [Hookify catalog](../../../00.agent-governance/rules/hooks/)                                   | Workspace tracked               | Counted 2026-08-14: 2 of 19 rules scoped to `event: stop`; no runtime binding found.                                  |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                    | Workspace tracked, stale        | Read first; built from `f8a72211`; every lead corroborated.                                                           |

## Maintenance

Re-measure the eight states, four typed loops, seven semantic events, binding
depths, provider hook schemas, dispatcher decisions, fixture/regression counts,
and review protocol whenever their canonical owners change. Do not convert the
ten analytical patterns into retry policy without a reviewed Stage 00/03/04
change.

## Related Documents

- [Harness engineering](./harness-engineering.md)
- [Provider implementation comparison](./provider-implementation-comparison.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
