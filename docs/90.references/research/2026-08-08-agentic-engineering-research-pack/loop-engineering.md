---
status: draft
artifact_id: reference:agentic-engineering-research:loop-engineering
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-08
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

| Element | Required question | Failure when absent |
| --- | --- | --- |
| Trigger/input | What current observation starts this attempt? | Work begins from stale or ambiguous state. |
| Owner | Who may act and at what permission level? | Responsibility and authority become implicit. |
| Action | What bounded operation is allowed? | The loop expands scope or changes unrelated state. |
| Feedback | What result can alter the next decision? | Retries repeat without diagnosis. |
| Exit gate | What observable condition means success? | Completion becomes subjective. |
| Attempt ceiling | How many attempts may occur? | A hook or agent can loop indefinitely. |
| Failure route | Narrow, stop, return, or escalate to whom? | Failure is suppressed or silently bypassed. |
| Independent review | Who checks the result without owning the implementation? | Self-review is mistaken for final approval. |
| Evidence | Which sanitized fields survive the run? | Secrets/raw logs leak or no durable proof remains. |

### Canonical lifecycle and typed loops

The ordered lifecycle has eight states:
`discover -> design/plan -> approval -> implement -> validate -> independent-review -> evidence -> handoff`.
`harness_loops` references those states; it is not a second lifecycle.

| Event ID | States | Owner / reviewer | Permission | Attempts | Stop condition | Failure route | Depth |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| `context-bootstrap` | `discover` | `workflow-supervisor` / `rules-engineer` | `read-only` | 1 | `bootstrap-contract-pass` | `escalate` | `repository-enforced` |
| `bounded-implementation-loop` | `implement`, `validate` | `qa-engineer` / `code-reviewer` | `workspace-write` | 2 | `focused-checks-pass` | `narrow_then_escalate` | `repository-enforced` |
| `independent-review-loop` | `implement`, `independent-review` | `code-reviewer` / `eval-engineer` | `read-only` | 2 | `critical_and_important_zero` | `escalate` | `repository-enforced` |
| `approved-all-files-gate` | `validate`, `evidence` | `qa-engineer` / `code-reviewer` | `workspace-write` | 1 | `controlled-wrapper-pass` | `record_and_stop` | `repository-enforced` |

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

| Pattern | Feedback signal | Exit/evidence owner | Typed relation and current state |
| --- | --- | --- | --- |
| Reason/action | Latest tool observation or clarification | Task implementer; inspected source/diff | Provider loop; constrained by typed bootstrap/implementation controls, hidden reasoning excluded. |
| Validation/format/lint | Focused check result | QA; exact command/result/skip | Closest to `bounded-implementation-loop`; locally executable. |
| CI gate | Remote job/check state | CI/CD owner; remote run evidence | No separate typed retry object; tracked workflow definition is not remote proof. |
| Evaluation/regression | Fixture score and threshold | Eval owner; 11 fixtures/16 regressions | Invoked by QA/harness gates; synthetic-only, no live model benchmark. |
| Memory/context | Verified milestone, decision, or stale finding | Lifecycle owner; canonical artifact | Bootstrap/evidence relationship; Memory remains advisory. |
| Plan/task/review | Exact diff plus reviewer verdict | Controller/reviewer; Stage 04 evidence | Closest to independent-review loop; SDD adds its own reviewed plan bounds. |
| Security/approval | Explicit decision on protected action | User/security/owner; redacted approval evidence | Approval state controls action; native permission mode never broadens authority. |
| Automation/pipeline | Stage result and propagated failure | Pipeline owner; immutable input/result | No separate typed retry object; idempotence and external authority remain explicit. |
| Incident/postmortem | Service symptom, recovery state, prevention action | Incident commander/owner; Stage 05 evidence | Applicable only to real incidents; no live service evidence in this Task. |
| Human pause/resume | Approve/reject/narrow decision plus refreshed state | Named human; decision and postcondition | Provider checkpoint semantics vary; stale state requires a new decision. |

### Semantic-event feedback depth

The semantic contract has seven events and three provider cells per event. At
this baseline, 20 of 21 cells are `configured-not-executed`; the Codex
`session-end` cell is `unsupported`. The predecessor claim that all 21 were
configured is therefore corrected.

| Semantic event | Claude local | Codex local | Repository mode / finding |
| --- | --- | --- | --- |
| `session-start` | `SessionStart` | `SessionStart` | Advisory context; configured, not execution proof. |
| `pre-tool` | `PreToolUse` | `PreToolUse` | Provider can block; repository dispatcher is advisory. |
| `post-tool` | `PostToolUse` | `PostToolUse` | Runs shared changed-file validation routing when fired. |
| `pre-compaction` | `PreCompact` | `PreCompact` | Advisory; no `PostCompact` local binding. |
| `user-prompt-intake` | `UserPromptSubmit` | `UserPromptSubmit` | Provider can block; local repository mode is advisory. |
| `stop` | `Stop` | `Stop` | Claude `blocking`; Codex `retry`; shared target-doc and uncommitted-work gates. |
| `session-end` | `SessionEnd` | No local binding | Contract says Codex unsupported, but current official Codex docs support a main-thread advisory `SessionEnd`; local gap. |

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

## Scope Implications

The status and owner basis comes from the
[scope application matrix](./scope-application-matrix.md); every row below is
the loop-specific implication.

| Scope | Loop implication | Disposition / exit route |
| --- | --- | --- |
| `agentic` | Owns lifecycle, typed retry/stop controls, provider translation, and handoff. | Implemented as contracts; provider execution unverified. |
| `architecture` | Design/review loops return unresolved trade-offs to ARD/ADR/Spec. | Partial; human/system architect route, no typed agent. |
| `backend` | Build/test/deploy feedback applies after a backend is specified. | Not Applicable now; stop until product/Spec surface exists. |
| `common` | Diff hygiene and independent correctness review close cross-layer loops. | Partial; use `code-reviewer`; no direct all-files pre-commit. |
| `docs` | Template, metadata, link, source, and review feedback closes document work. | Implemented locally; route switch and pack review pending. |
| `entry` | Gateway validation and incident feedback require infra ownership and runtime evidence. | Partial; escalate through infra/ops; edge state unverified. |
| `frontend` | UI build, accessibility, browser, and regression loops bind only to an actual surface. | Partial; current Storybook fixture is QA-owned. |
| `infra` | Compose preflight, drift, rollout, rollback, and postcheck form controlled loops. | Definitions exist; live loops were not run. |
| `meta` | Metadata and generator freshness provide deterministic documentation feedback. | Partial; route through docs; typed meta agent missing. |
| `mobile` | Device/build/signing/store feedback requires a mobile surface. | Not Applicable; no tracked source or runtime. |
| `ops` | Monitoring, incident, recovery, postmortem, and follow-up loops need live evidence. | Partial; no service or incident proof collected. |
| `product` | Human decisions close priority, risk, cost, and acceptance feedback. | Partial; human approval precedes implementation. |
| `qa` | Owns focused validation, fixture/regression scoring, aggregate gates, and evidence. | Extensive local implementation; remote and live-model state unverified. |
| `security` | Protected actions pause for approval; findings return to the owning implementation loop. | Partial; redacted evidence only; secret/runtime state excluded. |

## Sources

External pages were directly retrieved at
`2026-08-08T15:48:51+09:00`, returned HTTP 200 without redirect, and expose no
stable revision. They are mutable primary observations, not permanent runtime
guarantees.

| Source | Class | Verification |
| --- | --- | --- |
| [Claude hooks](https://code.claude.com/docs/en/hooks) | External mutable, primary | Verified event lifecycle, decisions, Stop, subagent, compaction, and session events. |
| [Claude subagents](https://code.claude.com/docs/en/sub-agents) | External mutable, primary | Verified isolated delegated contexts, turns, tools, permissions, model/effort, and hooks. |
| [Codex hooks](https://learn.chatgpt.com/docs/hooks) | External mutable, primary | Verified 11-event table, Stop decisions, `stop_hook_active`, and main-thread advisory `SessionEnd`. |
| [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | External mutable, primary | Verified orchestration, thread control, parent sandbox/permission inheritance, and agent fields. |
| [Provider/model contract](../../../00.agent-governance/contracts/provider-models.yaml) | Tracked mutable | Complete eight-state, four-loop, seven-event, 21-cell derivation at Task 3 BASE. |
| [Agent catalog](../../../00.agent-governance/contracts/agent-catalog.yaml) | Tracked mutable | Verified evaluation owner, 11 fixtures, 16 regressions, scorer, runner, and tests. |
| [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) | Tracked mutable | Verified human routing view and exact four typed loop rules. |
| [Shared dispatcher](../../../../scripts/hooks/agent-event-hook.sh) | Tracked executable | Read directly; demonstrates constructed decisions, not native firing. |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md) | Tracked stale/advisory | Read first; built from `f8a72211`; every lead corroborated. |

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
