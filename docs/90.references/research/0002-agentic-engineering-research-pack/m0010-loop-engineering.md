---
title: "Reference: Loop Engineering"
version: "1.2.0"
type: "reference/research"
status: "published"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0002-m0010"
parent_ids:
- "RES-0002"
created: "2026-08-23"
observed_at: "2026-09-05"
reviewed_at: "2026-09-05"
review_cycle: "on-source-change"
---

# Reference: Loop Engineering

## Current External Research

This member owns bounded iteration/continuation. Original sources were opened on 2026-09-27. No loop, schedule, provider call or internal controller was executed. The earlier taxonomies and retry values remain historical evidence. Internal adoption: **Not assessed in this run**. Unless an original explicitly states a maturity label, formal stable/preview/experimental status is **not stated**; current documentation is not a stability guarantee.

### Working definition and control contract

**C-m0010-01 — design advice.** Anthropic distinguishes predefined workflows from dynamically directed agents and recommends feedback, stopping conditions and human checkpoints. It is a design pattern, not an autonomous-loop standard. Primary metadata: [m0001](m0001-agent-instructions-vibe-coding.md#claims-and-sources), S-anthropic-com-building-effective-agents ([original](https://www.anthropic.com/engineering/building-effective-agents)).

**C-m0010-02 — interpretation / recommendation.** This pack’s working loop is goal → state/plan → one scoped act → observation → verification/review → stop, retry or handoff. A scheduled wakeup is a trigger; a passing check is evidence; neither supplies a total task budget. Before a trial, set finite attempt, elapsed-time, token/cost, tool-call and concurrent-writer limits. Declare completion, failure, cancellation, unchanged-evidence stall and permission-needed outcomes. These are evaluation inputs, not claims of existing enforcement.

| Shape | Use condition | Progress evidence | Stop / alternative |
| --- | --- | --- | --- |
| Repair | Concrete reproducible failure | Failure changes or relevant check passes | Same failure repeats; limit reached; manual diagnosis |
| Research | Named claim needs more primary evidence | New supporting/contradicting original | Source unavailable or budget exhausted; report limitation |
| Review | Concrete defect | Defect resolved with relevant evidence | No actionable new issue; independent check breaks correlated agreement |
| Continuation | Approved objective spans contexts | Canonical task, constraints and next step survive | Completion/cancel/budget; checkpoint handoff |
| Monitor | Explicit future trigger/notification intent | Meaningful defined state transition | Expiry/failure/cancel; local/cloud data reach differs |

**C-m0010-03 — native facts.** Claude subagent maxTurns (v2.1.246+) stops one invocation with a partial result but permits resume. Claude Stop hooks expose stop_hook_active to avoid repeated blocking. Codex matching command hooks can launch concurrently and have native continuation-result precedence. These controls are narrower than one overall budget. Sources and details are canonical in [m0012](m0012-provider-implementation-comparison.md#claims-and-sources): [Claude agents](https://code.claude.com/docs/en/sub-agents), [Claude hooks](https://code.claude.com/docs/en/hooks), [Codex hooks](https://learn.chatgpt.com/docs/hooks).

**C-m0010-04 — native facts.** [Claude schedules](https://code.claude.com/docs/en/scheduled-tasks) distinguish cloud fresh-clone tasks (machine can be off, min1h), desktop local/on tasks (min1m) and session loops requiring an open session; recurring session tasks expire after seven days. [Codex automation](https://learn.chatgpt.com/docs/automations) distinguishes available local app/host from web uploaded/connector context without local-folder continuity. Scheduler availability is not completion assurance; source metadata is owned by m0012.

**C-m0010-05 — recommendation.** Progress should reduce unresolved work with evidence. A changed file, new child or repeated continue message alone may not. Retry only a classified transient/recoverable failure; use bounded backoff and retry ceilings rather than immediate duplicate calls or model switches after denial. Deduplicate triggers/results and make authorized mutations idempotent where possible. Disjoint writes or isolated worktrees reduce conflicts; their merge/review cost remains. Checkpoint to the existing Task/handoff owner, preserving baseline, approved scope, decisions, check results, unresolved work and next action. Compacted/generated context points back to durable evidence; it is not acceptance. [m0008](m0008-harness-engineering.md#current-external-research) owns continuity design; [m0011](m0011-memory-hierarchy.md#current-external-research) owns memory lifecycle.

## Claims and Sources

| Claim ID | Claim | Source ID / detail section | Publication/revision date | Checked at | Product / version / channel | Fact / interpretation / recommendation | Limits / conflict / recheck | Internal adoption |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C-m0010-01 | Workflow versus autonomous agent | [S-anthropic-com-building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents); When to use agents / Agents | 2024-12-19 | 2026-09-27 | Native client/environment or working design; see source owner | Design advice | Published 2024-12-19; later products differ | Not assessed in this run |
| C-m0010-02 | Bounded loop working definition | [S-anthropic-com-building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents); When to use agents / Agents | 2024-12-19 | 2026-09-27 | Native client/environment or working design; see source owner | Interpretation / recommendation | Real total enforcement needs proof | Not assessed in this run |
| C-m0010-03 | Invocation versus overall limits | [S-code-claude-com-sub-agents](https://code.claude.com/docs/en/sub-agents); frontmatter/plugin restrictions/maxTurns/memory; [S-code-claude-com-hooks](https://code.claude.com/docs/en/hooks); handler types/Stop continuation state; [S-learn-chatgpt-com-hooks](https://learn.chatgpt.com/docs/hooks); trust/types/concurrency/Stop/PostToolUse | Not displayed; maxTurns v2.1.246 boundary / Not displayed | 2026-09-27 | Native client/environment or working design; see source owner | Facts | Invocation/resume semantics version-specific | Not assessed in this run |
| C-m0010-04 | Scheduler environment differences | [S-code-claude-com-scheduled-tasks](https://code.claude.com/docs/en/scheduled-tasks); cloud/Desktop/session/expiry; [S-learn-chatgpt-com-automations](https://learn.chatgpt.com/docs/automations); local desktop/web execution | Not displayed | 2026-09-27 | Native client/environment or working design; see source owner | Facts | Distinct availability/data/expiry | Not assessed in this run |
| C-m0010-05 | Evidence-based continuation | [S-anthropic-com-building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents); When to use agents / Agents; [S-anthropic-com-effective-harnesses-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents); initializer/coding-agent and artifacts | 2024-12-19 / 2025-11-26 | 2026-09-27 | Native client/environment or working design; see source owner | Recommendation | Separately approved bounded task | Not assessed in this run |

Native originals were opened 2026-09-27; publication dates are not displayed. Version limits are explicit in m0012. No unverified academic success statistic, current event count or historical retry value becomes a product guarantee.

## Future Internal Checks

Candidate surfaces do not assert implementation. These checks require a separate authorized task.

| Topic / claim ID | Analytical scope | Applicability condition | Future surface candidates | Concrete question | Required evidence | Future method | Pass/fail criterion | Additional authorization / risk | Likely role | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C-m0010-02–03 / bounds | Task/session/provider and execution control | If autonomous loop is proposed | Loop/hook/controller and Task owner candidates | Do retries, resumes and hooks share a finite budget? | Limits, attempt ledger, cancel/time/cost/stall/denial traces | Authorized disposable loop with external kill limit | All fixtures terminate; resume/hook cannot evade overall bound | Runtime/provider spend separately approved; no remote loop here | loop-operator / eval-engineer | Not assessed in this run |
| C-m0010-04–05 / scheduling | Execution environment and operational notification | If scheduling is separately requested | Local/cloud scheduler and notification owner | Do duplicate triggers avoid duplicate mutations/noise? | Trigger/expiry/host-off/duplicate traces and approved notification intent | Authorized synthetic events or isolated schedule | Expected availability/expiry; one intended mutation; meaningful notice only | Creating schedules/sending messages requires explicit scope | ci-cd-engineer / loop-operator | Not assessed in this run |

## Historical Workspace Observations

The complete earlier body is preserved at its original cutoff, including then-current external assertions and workspace observations. It is not current implementation authority; its dates are unchanged.

> Historical evidence (not current authority; source: Git history):
>
> Current routing (2026-09-06): [canonical agent governance](../../../../.agents/README.md) and
> [ADR-0032](../../../02.architecture/decisions/0032-canonical-agent-governance-home.md) own the active source location.
> Earlier Stage 00 paths, inventories, provider projections, and check results
> below remain dated observations, not current instructions or new runtime
> acceptance evidence. Source links now navigate to current owners; the
> original `observed_at`, `reviewed_at`, status, and measured facts are preserved.
>
> ## Overview
>
> Loop engineering turns agent activity into bounded feedback systems. Each loop
> needs an observable input, an authorized action, a result or failure signal, a
> stop condition, a retry ceiling, an escalation route, and sanitized evidence.
> Without those elements, repeated prompting is merely repetition rather than a
> controlled loop.
>
> This reference satisfies REQ-02 at baseline
> `9a6e09ca06d99ae8234199443974c978640f3ae6`. It separates the four canonical
> typed harness loops from broader analytical patterns and from provider-native
> event loops.
>
> ## Purpose
>
> Define loop elements and feedback patterns, measure the local typed workflow,
> hook, evaluation, and review implementation, and state where feedback is
> configured, repository-enforced, runtime-unverified, or outside current scope.
>
> ## Repository Role
>
> This Stage 90 leaf explains current loop structure and gaps. The exact retry,
> stop, permission, reviewer, and evidence values remain owned by
> `contracts/provider-models.yaml`; this document creates no prompt-local retry
> policy and authorizes no execution.
>
> ## Scope
>
> ### In scope
>
> - Agent observation/action, validation, review, approval, evaluation, memory,
>   automation, CI, incident, and human decision feedback.
> - The eight workflow states, four typed loops, seven semantic events, hook
>   dispatcher, fixtures, regressions, and relevant tests.
> - Claude and Codex loop mechanisms and all fourteen scope implications.
>
> ### Out of scope
>
> - Hidden chain-of-thought or unobservable internal reasoning.
> - Live provider quality comparisons, telemetry, remote CI enforcement, service
>   health, private state, credentials, raw logs, or secret values.
> - Adding retry counters, hooks, workflows, fixtures, or provider mappings.
>
> ## Definitions / Facts
>
> ### Loop anatomy
>
> | Element            | Required question                                        | Failure when absent                                |
> | ------------------ | -------------------------------------------------------- | -------------------------------------------------- |
> | Trigger/input      | What current observation starts this attempt?            | Work begins from stale or ambiguous state.         |
> | Owner              | Who may act and at what permission level?                | Responsibility and authority become implicit.      |
> | Action             | What bounded operation is allowed?                       | The loop expands scope or changes unrelated state. |
> | Feedback           | What result can alter the next decision?                 | Retries repeat without diagnosis.                  |
> | Exit gate          | What observable condition means success?                 | Completion becomes subjective.                     |
> | Attempt ceiling    | How many attempts may occur?                             | A hook or agent can loop indefinitely.             |
> | Failure route      | Narrow, stop, return, or escalate to whom?               | Failure is suppressed or silently bypassed.        |
> | Independent review | Who checks the result without owning the implementation? | Self-review is mistaken for final approval.        |
> | Evidence           | Which sanitized fields survive the run?                  | Secrets/raw logs leak or no durable proof remains. |
>
> ### Canonical lifecycle and typed loops
>
> The ordered lifecycle has eight states:
> `discover -> design/plan -> approval -> implement -> validate -> independent-review -> evidence -> handoff`.
> `harness_loops` references those states; it is not a second lifecycle.
>
> | Event ID                      | States                            | Owner / reviewer                         | Permission        | Attempts | Stop condition                | Failure route          | Depth                 |
> | ----------------------------- | --------------------------------- | ---------------------------------------- | ----------------- | -------: | ----------------------------- | ---------------------- | --------------------- |
> | `context-bootstrap`           | `discover`                        | `workflow-supervisor` / `rules-engineer` | `read-only`       |        1 | `bootstrap-contract-pass`     | `escalate`             | `repository-enforced` |
> | `bounded-implementation-loop` | `implement`, `validate`           | `qa-engineer` / `code-reviewer`          | `workspace-write` |        2 | `focused-checks-pass`         | `narrow_then_escalate` | `repository-enforced` |
> | `independent-review-loop`     | `implement`, `independent-review` | `code-reviewer` / `eval-engineer`        | `read-only`       |        2 | `critical_and_important_zero` | `escalate`             | `repository-enforced` |
> | `approved-all-files-gate`     | `validate`, `evidence`            | `qa-engineer` / `code-reviewer`          | `workspace-write` |        1 | `controlled-wrapper-pass`     | `record_and_stop`      | `repository-enforced` |
>
> All four loops require the same evidence keys: `command`, `result`, `rollback`,
> and `skipped_checks`. They prohibit auth files, credentials, raw logs, secret
> values, shell history, and tokens. Each reviewer differs from the owner.
> Validator tests enforce those structural properties. `repository-enforced`
> means the repository validates the contract and gates its own workflow; it is
> not proof that a provider event fired during this Task.
>
> ### Analytical feedback patterns
>
> The predecessor leaf presented ten prose rows. That count describes an
> analytical taxonomy, not ten typed or independently enforced loop objects. The
> old text then called seven named patterns “the remaining six,” an arithmetic
> and modeling error. The current interpretation keeps the useful ten-pattern
> taxonomy but does not subtract the four typed controls from it: the two views
> overlap and have no one-to-one mapping.
>
> | Pattern                | Feedback signal                                     | Exit/evidence owner                             | Typed relation and current state                                                                  |
> | ---------------------- | --------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------- |
> | Reason/action          | Latest tool observation or clarification            | Task implementer; inspected source/diff         | Provider loop; constrained by typed bootstrap/implementation controls, hidden reasoning excluded. |
> | Validation/format/lint | Focused check result                                | QA; exact command/result/skip                   | Closest to `bounded-implementation-loop`; locally executable.                                     |
> | CI gate                | Remote job/check state                              | CI/CD owner; remote run evidence                | No separate typed retry object; tracked workflow definition is not remote proof.                  |
> | Evaluation/regression  | Fixture score and threshold                         | Eval owner; 11 fixtures/16 regressions          | Invoked by QA/harness gates; synthetic-only, no live model benchmark.                             |
> | Memory/context         | Verified milestone, decision, or stale finding      | Lifecycle owner; canonical artifact             | Bootstrap/evidence relationship; Memory remains advisory.                                         |
> | Plan/task/review       | Exact diff plus reviewer verdict                    | Controller/reviewer; Stage 04 evidence          | Closest to independent-review loop; SDD adds its own reviewed plan bounds.                        |
> | Security/approval      | Explicit decision on protected action               | User/security/owner; redacted approval evidence | Approval state controls action; native permission mode never broadens authority.                  |
> | Automation/pipeline    | Stage result and propagated failure                 | Pipeline owner; immutable input/result          | No separate typed retry object; idempotence and external authority remain explicit.               |
> | Incident/postmortem    | Service symptom, recovery state, prevention action  | Incident commander/owner; Stage 05 evidence     | Applicable only to real incidents; no live service evidence in this Task.                         |
> | Human pause/resume     | Approve/reject/narrow decision plus refreshed state | Named human; decision and postcondition         | Provider checkpoint semantics vary; stale state requires a new decision.                          |
>
> ### External loop-primitive taxonomy versus the four typed loops
>
> A 2026 source-code study of 13 open-source coding-agent scaffolds at pinned
> commits (arXiv 2604.03515, retrieved 2026-08-14) identifies five composable
> control-loop primitives — ReAct, generate-test-repair, plan-execute,
> multi-attempt retry, and tree search — and finds 11 of 13 scaffolds combine
> more than one primitive rather than relying on a single loop. Mapped against
> this workspace's four typed loops:
>
> | Typed loop                    | Nearest external primitive                                 | Fit                                                                                                                                                                                                   |
> | ----------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | `context-bootstrap`           | None of the five (a pre-loop discovery gate)               | Not a control-loop primitive in that taxonomy; it precedes one.                                                                                                                                       |
> | `bounded-implementation-loop` | Multi-attempt retry, with elements of generate-test-repair | Partial: the 2-attempt ceiling matches "multi-attempt retry," but the loop does not itself run a test-repair cycle — `focused-checks-pass` is an external validator call, not an in-loop repair step. |
> | `independent-review-loop`     | Generate-test-repair (review-as-verification variant)      | Partial: `critical_and_important_zero` is a review-verdict gate, not a code-execution test.                                                                                                           |
> | `approved-all-files-gate`     | None of the five (a terminal one-shot gate)                | Not iterative; `max_attempts: 1` makes it a checkpoint, not a loop.                                                                                                                                   |
>
> No typed loop corresponds to **plan-execute** or **tree search**. This is a
> named gap, not a defect: `workflow_states` supplies a `design/plan` state and
> `approval` gate around the four loops, so planning exists at the lifecycle
> level, but no typed loop re-plans and re-attempts with backtracking the way a
> tree-search or plan-execute primitive would. The observation that would close
> this gap is a canonical agent governance decision on whether backtracking/replanning behavior
> should become a fifth typed loop or stay an untyped, agent-discretion pattern
> under `independent-review-loop`'s `escalate` route.
>
> A companion 2026 study of 20,574 real-world coding-agent sessions across
> 1,639 repositories (arXiv 2605.29442, retrieved 2026-08-14) found 90.50% of
> misalignment episodes cost effort/trust rather than causing system damage,
> yet 91.49% still required explicit user correction, across seven recurring
> failure categories including how agents bound their own actions and report
> progress. This corroborates, from an external and much larger sample, the
> same three failure shapes this pack's typed-loop model exists to prevent:
> unbounded action (addressed here by `max_attempts` and `permission_profile`),
> unverified self-reporting (addressed by requiring `command`/`result` evidence
> fields), and silent scope drift (addressed by `narrow_then_escalate` on
> `bounded-implementation-loop`). None of this workspace's typed-loop evidence
> was drawn from that external session corpus; the correspondence is
> structural, not a shared dataset.
>
> ### Unbounded loop risk in this workspace
>
> Three concrete places where this workspace's tracked construction could run
> without an enforced ceiling, verified by reading the executing code rather
> than the contract prose:
>
> 1. **`max_attempts` is a contract field, not a counted runtime value.**
>    `contracts/provider-models.yaml` `harness_loops` declares
>    `max_attempts: 2` for `bounded-implementation-loop` and
>    `independent-review-loop`, but no script in `scripts/hooks/` or
>    `scripts/validation/` reads or increments an attempt counter against that
>    field. The ceiling is a documented behavioral expectation for the agent
>    and its reviewer to self-observe, not a tool-enforced stop. An agent (or a
>    provider auto-retry) that ignores the contract has no local mechanism that
>    would block a third attempt.
> 2. **`PreToolUse` can repeat the same advisory guidance indefinitely.**
>    Because the repository dispatcher treats `PreToolUse` as advisory only
>    (see [harness-engineering.md](./m0008-harness-engineering.md)), a session that
>    keeps triggering the same changed-path pattern (for example repeatedly
>    editing a target-stage doc without fixing the template violation) receives
>    the same reminder text on every call with no escalation, count, or
>    eventual block — the loop's "failure route" for that specific trigger is
>    undefined below the `Stop` gate.
> 3. **The Stop gate's retry bound is a provider-payload interpretation, not a
>    repository counter.** `template_stop_gate` and `logical_commit_stop_gate`
>    in `scripts/hooks/agent-event-hook.sh` decide `continue: false` only when
>    the _provider_ reports `stop_hook_active: true` in its payload (Codex
>    branch) or via the Claude-native blocking response; the repository itself
>    keeps no count of how many times Stop has already fired in this session.
>    If a provider's payload shape changed to omit `stop_hook_active`, or if
>    Gemini's `AfterAgent` `deny-retry` mode (recorded in
>    `contracts/provider-models.yaml`, not previously described in this pack)
>    never signals a terminal retry, the bash-level loop has no independent
>    ceiling of its own.
>
> None of these is a defect in what is documented — the contract is explicit
> that these are behavioral/self-observed bounds — but they are the concrete
> answer to "where can a loop here run unbounded," which this pack's earlier
> revision did not enumerate.
>
> ### Semantic-event feedback depth
>
> The semantic contract has seven events and three provider cells per event. At
> this baseline, 20 of 21 cells are `configured-not-executed`; the Codex
> `session-end` cell is `unsupported`. The predecessor claim that all 21 were
> configured is therefore corrected.
>
> | Semantic event       | Claude local       | Codex local        | Repository mode / finding                                                                                                |
> | -------------------- | ------------------ | ------------------ | ------------------------------------------------------------------------------------------------------------------------ |
> | `session-start`      | `SessionStart`     | `SessionStart`     | Advisory context; configured, not execution proof.                                                                       |
> | `pre-tool`           | `PreToolUse`       | `PreToolUse`       | Provider can block; repository dispatcher is advisory.                                                                   |
> | `post-tool`          | `PostToolUse`      | `PostToolUse`      | Runs shared changed-file validation routing when fired.                                                                  |
> | `pre-compaction`     | `PreCompact`       | `PreCompact`       | Advisory; no `PostCompact` local binding.                                                                                |
> | `user-prompt-intake` | `UserPromptSubmit` | `UserPromptSubmit` | Provider can block; local repository mode is advisory.                                                                   |
> | `stop`               | `Stop`             | `Stop`             | Claude `blocking`; Codex `retry`; shared target-doc and uncommitted-work gates.                                          |
> | `session-end`        | `SessionEnd`       | No local binding   | Contract says Codex unsupported, but current official Codex docs support a main-thread advisory `SessionEnd`; local gap. |
>
> Claude wires all seven tracked semantic events. Codex wires six. Current
> official documentation enumerates 31 Claude event names and 11 Codex event
> names, but event vocabulary size does not measure local coverage or
> enforcement. Only Stop is configured as a blocking/retry repository gate here;
> the other provider primitives remain advisory in local policy even where the
> vendor permits a blocking decision.
>
> ### Stop and retry behavior
>
> The shared dispatcher distinguishes provider payloads. Claude receives a
> blocking decision plus a reason. Codex receives `decision: block` on the first
> failed Stop gate; if the provider payload marks `stop_hook_active`, the second
> failure returns `continue: false` and a `stopReason`. This is a bounded local
> translation of provider semantics, not a general repository counter. A vendor
> payload change could therefore invalidate the behavior and must be tested
> against current official schemas.
>
> The gate currently checks changed target-stage document contracts and
> task-owned uncommitted work. `post-tool-validate.sh` routes focused style,
> syntax, Compose, governance, and traceability checks by changed path. Hook
> configuration and dispatcher tests demonstrate local construction, but this
> Task did not execute a native Claude or Codex session to prove firing.
>
> A third Stop-equivalent mode exists in the tracked contract but was not
> previously recorded here: `contracts/provider-models.yaml`'s `stop`
> semantic-event row lists Gemini's native binding as `AfterAgent` with
> `repository_hook_mode: deny-retry` and `provider_can_block: true`.
> `providers/gemini.md` §6 explains the mechanism directly: `AfterAgent` "may
> deny a response and force a retry; it maps to the shared Stop gate as
> `deny-retry`, not as an irreversible session stop." This is a third distinct
> retry shape alongside Claude's single blocking response and Codex's
> two-strike `stop_hook_active` escalation — three providers, three different
> native retry primitives, one shared Python decision function
> (`template_stop_gate`/`logical_commit_stop_gate`) translating into each.
> Official Claude documentation retrieved 2026-08-14 adds a schema detail not
> previously recorded: Claude's `Stop` hook accepts _either_ an exit-code-2
> block _or_ a JSON `continue: false` + `stopReason` response — two independent
> mechanisms for the same blocking outcome, both consumed by this repository's
> shared dispatcher output.
>
> The two Hookify rules scoped to `event: stop`
> (`require-logical-commits-before-stop`, `warn-docker-infra-stop` — see
> [harness-engineering.md](./m0008-harness-engineering.md) for the full catalog) name
> the same completion behavior already hard-coded in
> `logical_commit_stop_gate`. They add no additional retry ceiling or stop
> condition of their own; they exist as human-readable policy text with no
> verified runtime execution path in this worktree.
>
> ### Environment and rules for workspace application
>
> Each rule below restates a fact established earlier in this leaf; none
> introduces a new claim or copies a policy body from a canonical owner. The
> companion harness-side list is
> [harness-engineering.md](./m0008-harness-engineering.md).
>
> 1. Name all nine loop-anatomy elements before the first attempt. An
>    unstated trigger, owner, exit gate, attempt ceiling, or failure route is
>    the failure mode itself, not a detail to settle mid-loop.
> 2. Select one of the four typed loops declared in `harness_loops` and stay
>    inside its declared states, permission profile, and stop condition. Do not
>    invent a fifth typed loop: no typed loop covers plan-execute or tree
>    search, and closing that gap requires a canonical agent governance decision, not
>    agent discretion.
> 3. Count attempts yourself. `max_attempts` is a contract field that no script
>    in `scripts/hooks/` or `scripts/validation/` reads or increments, so the
>    ceiling binds only the owner and reviewer who self-observe it. Treat a
>    third attempt as a boundary breach even though nothing local blocks it.
> 4. Do not mistake repeated advisory output for a control. `PreToolUse`
>    guidance re-emits on every matching call with no count, escalation, or
>    block, so the same reminder arriving again is evidence of an unbounded
>    trigger rather than of enforcement.
> 5. Treat the Stop gate as a provider-payload translation, not a repository
>    counter. Claude's blocking response, Codex's two-strike
>    `stop_hook_active` escalation, and Gemini's `AfterAgent` `deny-retry` are
>    three distinct native primitives behind one shared decision function; a
>    vendor schema change can invalidate the bound, so re-test against current
>    official schemas before relying on it.
> 6. Route failure explicitly to the declared destination — narrow, stop,
>    record, or escalate — and require a reviewer distinct from the loop owner.
>    `critical_and_important_zero` is a review-verdict gate, so self-review
>    cannot close it.
> 7. Record exactly `command`, `result`, `rollback`, and `skipped_checks`, and
>    keep auth files, credentials, raw logs, secret values, shell history, and
>    tokens outside the evidence. `repository-enforced` means the repository
>    validated its own contract, never that a provider event fired.
> 8. Keep the ten analytical feedback patterns as analysis. They overlap the
>    four typed controls with no one-to-one mapping, and converting any of them
>    into retry policy requires a reviewed canonical agent governance/03/04 change.
>
> ### Carried source-evidence claims
>
> Source-evidence claims carried forward from the superseded 2026-07-05
> research pack on 2026-08-19. Each states what the upstream evidence supports
> and, where it matters more, what it does not.
>
> - **Only a minority of documented provider events can block.** Of the events each provider documents, only a minority can block: as recorded in the retiring pack, exactly four of the eleven documented Codex events can stop work and Gemini exposes two, and Claude documents 31 event names of which 15 can block. **Claude half restored 2026-08-19** after a seat found it dropped: the paragraph's own argument is that stating only that a minority can block preserves the shape and discards the claim, and the discarded figure was the largest of the three. Those totals are dated vendor observations rather than current facts, and they are the content of the correction — stating only that a minority can block preserves the shape and discards the claim. Regardless of what a provider permits, only the stop gate is blocking in this repository.
>
> ### Bounded feedback pattern
>
> | Phase | Required content | Exit or escalation |
> | --- | --- | --- |
> | Input | Approved objective, current repository state, applicable authority, and changed-path boundary. | Stop when authority or ownership is unknown. |
> | Action | A permission-compatible, scoped mutation or read-only inspection. | Do not broaden paths or tools implicitly. |
> | Feedback | Focused validator output, a reviewer finding, or an explicit skip record. | Fix only the stated scoped failure. |
> | Exit | Named gate and evidence fields are satisfied. | Hand off to the next owner. |
> | Escalation | Ceiling reached, protected boundary encountered, or source is insufficient. | Request direction; do not loop indefinitely. |
>
> The workflow data places discovery before design/plan, approval before
> implementation, validation before independent review, and evidence before
> handoff. These states describe intended routing. They do not prove that a
> provider invoked a hook or that a remote CI gate accepted a change.
>
> Historical provider observations add useful, non-local context: Claude's
> subagent page described role/schema/model/effort facts, while Codex's described
> orchestration, schema, model, and sandbox facts. Both are inputs to choosing a
> bounded action; neither proves that this workspace dispatched a subagent or
> received hook feedback. The local registry remains the owner of actual loop
> ceilings and review gates. Its generic independent-review threshold is
> critical-and-important-zero; the approved D0–D7 unit contract is stricter and
> requires external C0/I0/M0 before publication.
>
> The retained taxonomy gives a useful interpretation of the actual four local
> loops: context-bootstrap precedes a control loop; bounded-implementation is
> nearest to multi-attempt retry but has only initial work plus one correction;
> independent review is a verdict gate, not test execution; and the one-attempt
> approved-all-files gate is a checkpoint rather than a multi-turn loop. The
> contract's exit and escalation fields, not the taxonomy, remain operative.
>
> ## Scope Implications
>
> The status and owner basis comes from the
> [scope application matrix](./m0015-scope-application-matrix.md); every row below is
> the loop-specific implication.
>
> | Scope          | Loop implication                                                                         | Disposition / exit route                                                |
> | -------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
> | `agentic`      | Owns lifecycle, typed retry/stop controls, provider translation, and handoff.            | Implemented as contracts; provider execution unverified.                |
> | `architecture` | Design/review loops return unresolved trade-offs to ARD/ADR/Spec.                        | Partial; human/system architect route, no typed agent.                  |
> | `backend`      | Build/test/deploy feedback applies after a backend is specified.                         | Not Applicable now; stop until product/Spec surface exists.             |
> | `common`       | Diff hygiene and independent correctness review close cross-layer loops.                 | Partial; use `code-reviewer`; no direct all-files pre-commit.           |
> | `docs`         | Template, metadata, link, source, and review feedback closes document work.              | Implemented locally; route switch and pack review pending.              |
> | `entry`        | Gateway validation and incident feedback require infra ownership and runtime evidence.   | Partial; escalate through infra/ops; edge state unverified.             |
> | `frontend`     | UI build, accessibility, browser, and regression loops bind only to an actual surface.   | Partial; current Storybook fixture is QA-owned.                         |
> | `infra`        | Compose preflight, drift, rollout, rollback, and postcheck form controlled loops.        | Definitions exist; live loops were not run.                             |
> | `meta`         | Metadata and generator freshness provide deterministic documentation feedback.           | Partial; route through docs; typed meta agent missing.                  |
> | `mobile`       | Device/build/signing/store feedback requires a mobile surface.                           | Not Applicable; no tracked source or runtime.                           |
> | `ops`          | Monitoring, incident, recovery, postmortem, and follow-up loops need live evidence.      | Partial; no service or incident proof collected.                        |
> | `product`      | Human decisions close priority, risk, cost, and acceptance feedback.                     | Partial; human approval precedes implementation.                        |
> | `qa`           | Owns focused validation, fixture/regression scoring, aggregate gates, and evidence.      | Extensive local implementation; remote and live-model state unverified. |
> | `security`     | Protected actions pause for approval; findings return to the owning implementation loop. | Partial; redacted evidence only; secret/runtime state excluded.         |
>
> ## Sources
>
> External pages were retrieved 2026-08-08 (initial) and 2026-08-14
> (re-verification plus new sources); all returned HTTP 200 without redirect
> and expose no stable revision, so they are mutable primary observations, not
> permanent runtime guarantees. The two arXiv papers are external mutable
> primary sources with a fixed preprint identifier but no confirmed pinned
> version in this retrieval; treat exact figures as subject to revision on a
> future arXiv version.
>
> <!-- Historical evidence table (not current authority; source: Git history). -->
> | Source                                                                                         | Class                           | Verification                                                                                                          |
> | ---------------------------------------------------------------------------------------------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
> | [Claude hooks](https://code.claude.com/docs/en/hooks)                                          | External mutable, primary       | Re-verified 2026-08-14: Stop schema accepts exit-2 or `continue:false`+`stopReason`; full event/decision breakdown.   |
> | [Claude subagents](https://code.claude.com/docs/en/sub-agents)                                 | External mutable, primary       | Verified 2026-08-08: isolated contexts, turns, tools, permissions, model/effort, hooks.                               |
> | [Codex hooks](https://learn.chatgpt.com/docs/hooks)                                            | External mutable, primary       | Re-verified 2026-08-14: 11-event table, `stop_hook_active`, main-thread `SessionEnd`.                                 |
> | [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)                | External mutable, primary       | Verified 2026-08-08: orchestration, thread control, sandbox/permission inheritance.                                   |
> | [Inside the Scaffold (arXiv 2604.03515)](https://arxiv.org/abs/2604.03515)                     | External mutable, primary paper | New 2026-08-14: 13 scaffolds, 5 loop primitives, 11/13 combine multiple primitives.                                   |
> | [How Coding Agents Fail Their Users (arXiv 2605.29442)](https://arxiv.org/abs/2605.29442)      | External mutable, primary paper | New 2026-08-14: 20,574 sessions/1,639 repos, seven failure categories, 90.50%/91.49% figures.                         |
> | Provider/model contract (retired path: `../../../00.agent-governance/contracts/provider-models.yaml`)         | Workspace tracked               | Re-read 2026-08-14: eight-state, four-loop, seven-event, 21-cell derivation, including Gemini `deny-retry` Stop mode. |
> | Agent catalog (retired path: `../../../00.agent-governance/contracts/agent-catalog.yaml`)                     | Workspace tracked               | Re-read 2026-08-14: `evaluation.fixture_count`/`regression_count` typed fields (11/16), scorer, runner, tests.        |
> | Subagent protocol (retired path: `../../../00.agent-governance/subagent-protocol.md`)                         | Workspace tracked               | Verified human routing view and exact four typed loop rules.                                                          |
> | [Provider capability matrix](../../../../.agents/governance/provider-capability-matrix.md) | Workspace tracked               | Re-read 2026-08-14: three-provider Stop-mode row (`blocking`/`retry`/`deny-retry`).                                   |
> | `providers/gemini.md` (retired path: `../../../00.agent-governance/providers/gemini.md`)                      | Workspace tracked               | Read 2026-08-14: `AfterAgent` deny-retry mechanism description.                                                       |
> | [Shared dispatcher](../../../../scripts/hooks/agent-event-hook.sh)                             | Workspace tracked, executable   | Read directly 2026-08-14: no attempt-counter code path against `max_attempts`.                                        |
> | [Hookify catalog](../../../../.agents/governance/hooks)                                   | Workspace tracked               | Counted 2026-08-14: 2 of 19 rules scoped to `event: stop`; no runtime binding found.                                  |
> | Graphify report (`graphify-out/GRAPH_REPORT.md`, untracked local output since 2026-09-08)                                    | Workspace tracked, stale        | Read first; built from `f8a72211`; every lead corroborated.                                                           |
>
> ## Scope Application
>
> | Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
> | --- | --- | --- | --- | --- |
> | agentic | applies | Use the registered loop for state. | Inspect `harness_loops`, `workflow_states`, and named owner/reviewer fields. | No live loop run. |
> | architecture | applies | Escalate design ambiguity to its owner. | Confirm owner before action. | No design accepted here. |
> | common | applies | Bound shared-worktree retries. | Inspect exact owned paths. | A ceiling is not enforcement proof. |
> | docs | applies | Use feedback to correct only documented gaps. | Review links and metadata. | No broad cleanup. |
> | infra | applies | Stop before runtime actions lacking approval. | Require target and rollback. | No service loop. |
> | ops | applies | Hand off operational failure to ops owner. | Record sanitized evidence. | No operational result. |
> | qa | applies | Use focused gates before review. | Inspect the registered gate and record its actual exit status. | Broad gates remain separate. |
> | security | applies | Escalate sensitive or protected failures. | Verify redaction boundary. | No security test. |
>
> ## 2026-09-05 Revalidation
>
> Baseline: `main@4c6d211129615eab372d720ebd209b6c27618c86`.
> Stage 00 defines a bounded loop from discovery and planning through approval,
> execution, verification, review, correction, completion, or handoff. The
> repository now has a concrete example in SPEC-0172: repeated Hosted failures
> were fixed without removing gates, followed by exact remote read-back.
>
> | Capability | Repository implementation | Evidence depth | Gap | Verification route |
> | --- | --- | --- | --- | --- |
> | Retry and stop | Bounded retry, blocker, and handoff policies | Defined, Repository-enforced | Provider adherence is not deterministic | Task evidence and stop-hook tests |
> | Review loop | Exact-diff independent review is required for material changes | Defined | Reviewer quality varies | recorded verdict and corrected rerun |
> | Evidence handoff | Current Task owns verified state, blockers, and next action | Repository-enforced | Cross-session semantic loss remains possible | Task and compaction contract checks |
>
> Recommendation: terminate loops on verified completion, an explicit approval
> boundary, or a durable blocker; do not equate additional turns with progress.
>
> ## Maintenance
>
> Re-measure the eight states, four typed loops, seven semantic events, binding
> depths, provider hook schemas, dispatcher decisions, fixture/regression counts,
> and review protocol whenever their canonical owners change. Do not convert the
> ten analytical patterns into retry policy without a reviewed canonical agent governance/03/04
> change.

## Related Documents

- [Research pack](README.md)
- [Harness engineering](./m0008-harness-engineering.md)
- [Provider implementation comparison](./m0012-provider-implementation-comparison.md)
- [Workspace baseline](./m0020-workspace-baseline.md)
- [Scope application matrix](./m0015-scope-application-matrix.md)
- [SPEC-0158 preservation contract](../../../98.archive/completed/03.specs/0158-document-governance-lifecycle-convergence/spec.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
