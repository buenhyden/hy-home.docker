---
status: active
artifact_id: reference:agentic-research:loop-engineering
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-07
review_cycle: on-source-change
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md -->

# Reference: Loop Engineering for Agentic Workspaces

## Overview

Loop engineering defines how an agent observes, decides, acts, verifies, and
either exits, retries, or escalates. A useful loop is not “keep trying”: its
input, action boundary, evidence, exit condition, retry boundary, and human
escalation path are explicit.

This reference maps research foundations and provider mechanisms to the
tracked workspace at baseline `1a80b6989304fa7b6a179861a9cad795dd875ca3`.
It does not create new retries, hooks, automation, or approval authority.

## Purpose

Describe the ten loops that matter to repository work and separate autonomous
local iteration from authority to affect protected or external systems.

## Repository Role

Stage 00 rules, Stage 04 plans/tasks, QA scope, CI workflows, scripts, and
Stage 05 incident artifacts remain canonical. This Stage 90 document is a
comparison and routing aid.

## Scope

### In Scope

- ReAct-style reason/action and Reflexion-style feedback concepts
- Local execution, validation, CI, eval, memory, review, security, automation,
  incident, and human pause/resume loops
- Exact evidence and stop/escalation boundaries

### Out of Scope

- New evaluation datasets or scorers
- New CI jobs, hooks, runbooks, or deployment automation
- Automatic external action or unlimited retries

## Definitions / Facts

- **ReAct** interleaves reasoning traces with actions that obtain observations
  from an environment. It is a conceptual basis for tool-result feedback, not
  workspace authorization.
- **Reflexion** uses verbal feedback and episodic memory across trials without
  updating model weights. It is a conceptual basis for durable learning
  evidence, not permission to turn memory into policy.
- Provider agent runtimes expose plan/tool/observation loops with different
  permissions, hooks, and resume mechanics. Provider mechanics are adapters;
  the repository's stop and approval rules remain controlling.

## Provider Loop Criteria

Provider cells state current official mechanisms revalidated at
`2026-08-07T12:45:40+09:00`;
the workspace column states tracked policy/evidence, and the final column keeps
task-fit inference and unresolved implementation gaps explicit.

| Criterion                            | Claude                                                                                                                                                     | Codex                                                                                                                                                                                                                                                               | Gemini                                                                                                                                                                                  | Workspace common contract                                                                                                                                                                                                                                                                | Gap / caveat                                                                                                                                                                                                                                                        |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| LOOP-01 — Observe and act            | A subagent runs an isolated context/tool loop and returns a result to its caller.                                                                          | Built-in/custom agents run bounded tool loops and propagate results, sandbox, and approvals through the parent session.                                                                                                                                             | Native subagents have independent context loops and may delegate automatically or by name.                                                                                              | Every action is bounded by the user request, loaded Stage 00 scope, latest observation, and approval boundary.                                                                                                                                                                           | Hidden reasoning is not auditable; only actions, observations, decisions, and evidence may support completion.                                                                                                                                                      |
| LOOP-02 — Pre/post action feedback   | Lifecycle hooks can block or enrich pre-tool behavior and inspect successful or failed post-tool behavior. 31 event names are documented and 15 can block. | Command hooks document 11 events and intercept Bash, `apply_patch`, MCP, and other local function tools, with hosted tools such as `WebSearch` still excluded. Four events can stop work: `PreToolUse`, `PermissionRequest`, `PostToolUse`, and `UserPromptSubmit`. | Native hooks document 11 synchronous command events covering before/after tool and agent, session, model, compression, and tool-selection. Only `BeforeTool` and `AfterAgent` can deny. | Seven semantic events render to seven Claude, six Codex, and seven Gemini mappings. All 21 bindings carry `runtime_depth: configured-not-executed`.                                                                                                                                      | Event-name parity is false and configured mappings do not prove live interception. The Codex six-mapping binding predates upstream `SessionEnd` support and remains a repository-side gap: `.codex/hooks.json` wires six events while Codex documents `SessionEnd`. |
| LOOP-03 — Validation and eval        | Hooks and agents can invoke tests; provider capability does not adopt a scorer.                                                                            | Agents/skills/hooks can invoke local checks and eval tooling.                                                                                                                                                                                                       | Headless/tools/hooks/subagents can invoke checks.                                                                                                                                       | Changed-file validation, CI/local routing, 11 exact fixtures, 16 synthetic regressions, deterministic scorers, calibrated thresholds, task evidence, and independent review define exit evidence.                                                                                        | The repository-semantic loop is implemented; no live provider-quality baseline is claimed.                                                                                                                                                                          |
| LOOP-04 — Retry and stop             | Stop/SubagentStop hooks can return a blocking decision; retry semantics remain event-specific.                                                             | A parent can continue or re-dispatch after evidence. The `stop_hook_active` flag in the Stop payload is the documented signal that a retry has already fired.                                                                                                       | Agent/tool hooks and checkpointing can support continuation; checkpointing is optional.                                                                                                 | Four typed harness loops bind positive attempt ceilings, exact stop conditions, failure actions, independent review, and one controlled all-files attempt. The Stop gate renders three distinct repository modes: `blocking` for Claude, `retry` for Codex, and `deny-retry` for Gemini. | Repository retry/stop semantics are enforced; provider continuation and checkpoint behavior remain separate runtime facts.                                                                                                                                          |
| LOOP-05 — Approval pause/resume      | Permissions and hooks can pause sensitive actions for a decision.                                                                                          | Approval policy is separate from sandbox; approval state propagates to subagents.                                                                                                                                                                                   | Confirmation modes and optional sandboxing govern tool execution.                                                                                                                       | Protected/external mutations pause before action, bind approval to exact scope, then refresh state before resume.                                                                                                                                                                        | Unattended modes can suppress provider prompts but never broaden repository authority; durable cross-provider resume evidence is not uniform.                                                                                                                       |
| LOOP-06 — Evidence and observability | Hook inputs, transcripts, and provider logs expose selected lifecycle data.                                                                                | Command output, optional OpenTelemetry, thread state, and hook records expose selected data.                                                                                                                                                                        | Hook payloads and opt-in telemetry expose selected data.                                                                                                                                | Diffs, exact checks, task/PR evidence, SARIF, and canonical lifecycle records support review.                                                                                                                                                                                            | No unified trace backend is tracked; telemetry can be disabled and must respect privacy/redaction boundaries.                                                                                                                                                       |

## Loop Contract Matrix

| Loop                                  | Exact input                                                                                                                         | Action                                                                                                                       | Evidence                                                                                                       | Exit condition                                                                                                              | Retry limit                                                                                                             | Escalation                                                                                                        | Status                | Gap / risk                                                                                                                        | Canonical owner                                         | Confidence |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ---------- |
| Inner reason/action loop              | Current user request, loaded Stage 00 context, scoped files, and latest tool observation                                            | Select one bounded read or authorized mutation, execute it, then interpret the result before another action                  | Tool output, inspected source, patch/diff, and stated assumption                                               | Requested local outcome is achieved and proportionate verification passes, or an approval/clarification boundary is reached | No blind automatic retry; diagnose every failure and stop when the same unresolved blocker repeats                      | Ask for the missing decision/authority, or report the external/environmental blocker                              | Implemented           | Provider hidden reasoning is not auditable; only actions and evidence are reviewable                                              | `docs/00.agent-governance/rules/agentic.md`             | High       |
| Validation, formatting, and lint loop | Changed-file set plus the QA/change-type gate map                                                                                   | Run applicable repository-configured checks, fix in-scope defects, rerun only affected checks, then run the completion gate  | Exact commands, exit codes, relevant output, final `git diff --check`, and skipped-check rationale             | All applicable checks pass and no unexplained skip remains                                                                  | Retry while each attempt makes an evidence-backed in-scope correction; repeated unchanged failure stops the loop        | Route tool/environment failures to the user or owning scope; do not suppress a gate                               | Implemented           | Hook validation is selective: `post-tool-validate.sh` does not run `prettier --check` and cannot prove every CI-only gate         | `docs/00.agent-governance/scopes/qa.md`                 | High       |
| CI gate loop                          | Pushed commit or pull-request event and tracked workflow YAML                                                                       | Run independent quality jobs and expose logs/status; an authorized maintainer responds to failures                           | Workflow run, job logs, annotations/SARIF, and required-check state                                            | Required jobs pass and the governing remote merge rule is satisfied                                                         | CI retries are operator-controlled; rerun only after diagnosing flake, environment, or code change                      | Escalate persistent infrastructure/permission failure or required-check ambiguity to repository maintainers       | Partially Implemented | Local checkout proves workflow definitions, not remote branch protection or required-check configuration                          | `docs/00.agent-governance/rules/github-governance.md`   | High       |
| Evaluation and regression loop        | Eleven versioned synthetic fixtures, 16 positive/negative regressions, exact thresholds, bounded scorer, and changed harness/prompt | Run fixed cases, score bounded outputs, compare exact thresholds, and record value-free results                              | Fixture/regression identity, exact pass markers, threshold result, review verdict, and sanitized failure class | All 11 fixtures and 16 regressions pass with no unexplained harness regression                                              | Retry only after a declared harness/eval correction; do not tune repeatedly against hidden answers                      | Independent review approves scorer/threshold changes; live datasets require separate privacy/entitlement approval | Implemented           | Synthetic repository semantics do not establish live cross-provider model quality, latency, or cost                               | `docs/00.agent-governance/scopes/qa.md`                 | High       |
| Memory and context loop               | Material verified finding, completed milestone, unresolved blocker, or approved decision                                            | Record concise durable evidence in the owning lifecycle/memory artifact; reload only relevant context on later work          | Stage artifact update, progress entry when in scope, source link, and date/commit context                      | Future work can recover the decision and provenance without treating memory as active policy                                | One correction per discovered stale/incorrect entry; conflicting evidence pauses further propagation                    | Route policy conflicts to the canonical Stage 00 or lifecycle owner                                               | Implemented           | Memory can become stale, overlong, or mistaken for authority; exact-scope tasks may intentionally exclude `progress.md`           | `docs/00.agent-governance/memory/README.md`             | High       |
| Plan, task, and review loop           | Approved Stage 04 plan entry, bounded task card, and base commit                                                                    | Implement only assigned files, record checks and deviations, move to Ready for Review, then obtain an independent verdict    | Plan/task links, changed-file inventory, commit range, check output, implementer report, and reviewer report   | Independent review records pass/accepted verdict; only the controller closes the task                                       | Implementation revisions are bounded by reviewer findings; each new revision receives a fresh independent review        | Scope conflict, missing authority, or incompatible evidence returns to the controller/user                        | Implemented           | Self-review cannot satisfy the independent verdict; generic `implementation_plan.md`/`walkthrough.md` are not canonical artifacts | `docs/04.execution/tasks/README.md`                     | High       |
| Security and approval loop            | Proposed protected, secret-bearing, destructive, paid, credential, or external mutation                                             | Stop before action, state impact and exact command/change, obtain explicit approval, execute narrowly, then verify           | Approval record, redacted command/result, security checks, and changed-resource identity                       | Approved scoped action completes and postcondition is verified, or approval is denied                                       | Zero execution retries without continuing authority; changed scope requires new approval                                | User/maintainer/security owner decides; unresolved risk remains blocked rather than bypassed                      | Implemented           | Native provider approval modes can be disabled or run unattended and never broaden repository authority                           | `docs/00.agent-governance/rules/approval-boundaries.md` | High       |
| Automation and pipeline loop          | Authorized trigger, immutable input/ref, declared permissions, and tracked workflow/script                                          | Execute bounded stages, propagate failure, retain logs, and avoid external mutation outside the trigger's authority          | Script/workflow version, trigger/ref, logs, artifacts/SARIF, and final state                                   | Every required stage passes or the pipeline stops with an attributable failure                                              | Retry only idempotent stages after cause classification; external writes require explicit original or renewed authority | Pipeline owner handles non-idempotence, credential, remote-service, or repeated infrastructure failure            | Partially Implemented | Local scripts/hooks/CI are present, but remote schedules, secrets, and enforcement cannot be proved from tracked files            | `scripts/README.md`                                     | High       |
| Incident and postmortem loop          | Live service-impacting symptom, time, scope, and available telemetry                                                                | Triage, contain, communicate, recover, record timeline, then write a reviewed learning artifact and track actions            | Incident record, timeline, command/metric evidence, recovery proof, postmortem, and follow-up owners           | Service is recovered/contained and follow-up actions have owners/status; postmortem review completes                        | Operational retries follow the owning runbook; repeated ineffective mitigation changes strategy and escalates           | Incident command and service owner; security incidents follow disclosure/security routes                          | Partially Implemented | Stage 05 templates/routing exist, but a document cannot prove every service has tested rollback or live telemetry                 | `docs/05.operations/incidents/README.md`                | High       |
| Human-in-the-loop pause/resume        | Sensitive proposed action plus serialized task state, rationale, and required decision                                              | Pause before the action, present approve/reject/narrow choices, record the decision, then resume from verified current state | Decision identity/time, approved scope, refreshed diff/state, and resumed action result                        | Human rejects, narrows, or approves; after approval the exact postcondition is verified                                     | One resume per recorded decision; stale state or changed action requires a new pause/decision                           | The named human owner decides; no response leaves the action unexecuted                                           | Partially Implemented | Repository rules define the boundary, but durable cross-provider checkpoint/resume behavior is not uniform                        | `docs/00.agent-governance/rules/approval-boundaries.md` | High       |

## Typed Harness Loops

Ten loops are described above as repository practice. Only four of them are
typed in `docs/00.agent-governance/contracts/provider-models.yaml` under
`harness_loops`, and those four are the only loops whose attempt ceiling and
stop condition a validator can read. Re-derived 2026-08-07.

| Criterion | `event_id`                    | Owner                 | Reviewer         | Permission        | Max attempts | Stop condition                | On failure             |
| --------- | ----------------------------- | --------------------- | ---------------- | ----------------- | ------------ | ----------------------------- | ---------------------- |
| THL-01    | `context-bootstrap`           | `workflow-supervisor` | `rules-engineer` | `read-only`       | 1            | `bootstrap-contract-pass`     | `escalate`             |
| THL-02    | `bounded-implementation-loop` | `qa-engineer`         | `code-reviewer`  | `workspace-write` | 2            | `focused-checks-pass`         | `narrow_then_escalate` |
| THL-03    | `independent-review-loop`     | `code-reviewer`       | `eval-engineer`  | `read-only`       | 2            | `critical_and_important_zero` | `escalate`             |
| THL-04    | `approved-all-files-gate`     | `qa-engineer`         | `code-reviewer`  | `workspace-write` | 1            | `controlled-wrapper-pass`     | `record_and_stop`      |

Three properties of this set matter more than the individual rows.

- All four carry `runtime_depth: repository-enforced`, which is the only value
  in the contract that asserts the repository itself enforces the behavior.
  Every one of the 21 semantic-event bindings carries
  `configured-not-executed` instead. The contract therefore already separates
  loops it enforces from events it merely wires.
- Every loop names a reviewer distinct from its owner, which is how "an
  implementer may inspect its own diff, but cannot issue the final independent
  verdict" is expressed as data rather than prose.
- Every loop declares the same `prohibited_evidence` set: `auth_files`,
  `credentials`, `raw_logs`, `secret_values`, `shell_history`, and `tokens`.
  The evidence contract is uniform, so a loop cannot widen what it may record
  by being the one that discovered something sensitive.

The remaining six loops in the contract matrix — CI gate, evaluation and
regression, memory and context, plan/task/review, security and approval,
automation and pipeline, and incident and postmortem — have owners and evidence
paths but no typed attempt ceiling. That is the largest single gap between how
this document describes loop engineering and how much of it a machine can
check.

## Claude and Codex Implementation Status

The Stop gate is the only loop boundary this repository actually enforces
through a provider hook, so its Claude and Codex behavior is worth stating
exactly rather than by analogy.

| Criterion | Concern                         | Claude                                                                                          | Codex                                                                                                                                         |
| --------- | ------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| LCS-01    | Wired Stop event                | Yes, `Stop` in `.claude/settings.json` with a 30 s timeout                                      | Yes, `Stop` in `.codex/hooks.json` with the uniform 600 s timeout                                                                             |
| LCS-02    | Repository mode                 | `blocking`                                                                                      | `retry`                                                                                                                                       |
| LCS-03    | Emitted payload                 | `decision: block` plus `reason` and `systemMessage`                                             | `decision: block` on the first pass; `continue: false` with `stopReason` beginning `Stop retry limit reached` once `stop_hook_active` is true |
| LCS-04    | Retry ceiling mechanism         | None in the dispatcher; Claude's own Stop semantics govern                                      | One, driven by the provider-supplied `stop_hook_active` flag                                                                                  |
| LCS-05    | Blocked condition               | Changed target-stage documentation that fails `bash scripts/validation/check-repo-contracts.sh` | Same                                                                                                                                          |
| LCS-06    | Uncommitted-work gate           | Stop blocks while task-owned uncommitted paths remain                                           | Same                                                                                                                                          |
| LCS-07    | Event coverage of the ten loops | 7 of 7 semantic events wired                                                                    | 6 of 7; `session-end` unwired                                                                                                                 |

The asymmetry in LCS-03 is the substantive one. Claude's Stop loop terminates
because Claude Code stops re-invoking a blocked Stop hook; Codex's terminates
because the dispatcher reads a provider flag and converts the second pass into
a hard `continue: false`. Neither is a repository-level counter, so neither
loop's retry ceiling survives a provider changing its Stop semantics. A
repository-owned counter would be the change that makes LOOP-04 provider-
independent, and it does not exist today.

## Corrections to Stale Claims

- Corrected 2026-08-07. Earlier text implied that partial Codex hook
  interception explains the six-mapping binding. It does not. Codex documents
  11 hook events including `SessionEnd`; the missing seventh mapping is a
  repository-side omission in `.codex/hooks.json` and in the contract's Codex
  `session-end` binding, which still records `native_event: null` and
  `capability_status: unsupported`.
- Corrected 2026-08-07. The Codex blocking surface is narrower than "hooks can
  block" suggests. Exactly four of the 11 documented Codex events can stop
  work, and Gemini exposes only two. Only the Stop gate is blocking in this
  repository regardless of what a provider permits.
- Confirmed 2026-08-07. `scripts/hooks/post-tool-validate.sh` still contains no
  `prettier` invocation across its 232 lines. The validation loop's recorded
  gap is accurate.

## Current-State Assessment

| Category         | Current state                                                                                                                                                              | Primary comparison                                                                                              | Status                | Gap                                                                                                                                                     | Recommendation                                                                                                                      | Canonical owner                             | Evidence                                                               | Confidence |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ---------------------------------------------------------------------- | ---------- |
| Loop engineering | Local action, typed retry/stop, calibrated synthetic evaluation, task/review, security, memory, CI, automation, and incident loops have tracked owners and evidence paths. | ReAct and Reflexion explain observation/feedback; official provider and CI/HITL docs supply current mechanisms. | Partially Implemented | Live provider parity, remote enforcement proof, uniform checkpoint/resume, comparative model evaluation, and tested service recovery remain incomplete. | Require the matrix fields for new loops and route implementation through the listed owner instead of encoding it in this reference. | `docs/00.agent-governance/rules/agentic.md` | Matrix above; typed contracts, Stage 04/05, scripts, and workflow YAML | High       |

## Loop Design Rules

1. **Observation is not authority.** A tool result can justify another local
   step but cannot authorize a remote or protected mutation.
2. **Retries must change something.** A retry follows diagnosis, a scoped
   correction, or a classified transient failure; identical blind repetition
   is not a loop design.
3. **Evidence is part of the exit condition.** A result without a source,
   check, or recorded decision is not complete.
4. **Memory is advisory.** Verified decisions belong in their canonical stage;
   memory makes them discoverable but cannot replace them.
5. **Independent review is a separate loop actor.** An implementer may inspect
   its own diff, but cannot issue the final independent verdict.
6. **Pause/resume revalidates state.** Approval applies to the exact proposed
   action; a changed diff, command, or external state requires a fresh check.

## Provider and Research Boundary

Claude, Codex, and Gemini CLI all document native custom-agent and lifecycle
mechanisms, but their schemas and events differ. Gemini CLI public subagent
support was announced in v0.38.1 on 2026-04-16; project/user definitions use
`.gemini/agents/*.md` with isolated context and bounded tool/MCP/model/run
controls. Gemini CLI hooks were announced with v0.26.0 on 2026-01-28 and now
document tool, agent, session, model, and tool-selection events. This
establishes the provider capability. The workspace now generates native
`.gemini` agents, settings, and hook wrappers while keeping `.agents` as a
separate compatibility/shared-skill surface. Generation establishes tracked
adoption, not live runtime acceptance. ReAct and Reflexion are
research foundations only; neither paper defines repository retry limits,
approvals, or evidence policy.

Provider pages were originally retrieved on 2026-07-10 and revalidated on
`2026-08-07T12:45:40+09:00`. Mutable documentation proves only the latest
described surface;
later announcements cannot be backdated into the fixed 2026-07-10 10:00 KST
model cutoff.

## Adoption Boundary

Nothing in this document authorizes a new loop. Adding one in this workspace
means resolving four concrete questions first, each of which touches a tracked
file rather than a research pattern.

1. **Does the loop need a typed attempt ceiling?** If yes it belongs in
   `harness_loops` with an owner, a distinct reviewer, a positive
   `max_attempts`, an exact `stop_condition`, and an `on_failure` action. If it
   cannot supply all five it is a practice, not a typed loop, and should stay
   in prose.
2. **Which semantic event carries it?** Only the seven registered events exist.
   A loop that needs `session-end` on Codex is blocked on the unwired binding
   described above; a loop that needs an event outside the seven requires a
   contract change, not a hook.
3. **What is the evidence, and is it permitted?** The uniform
   `prohibited_evidence` set excludes `auth_files`, `credentials`, `raw_logs`,
   `secret_values`, `shell_history`, and `tokens`. A loop whose only proof is
   raw output cannot record that proof here.
4. **Who breaks the tie?** Every typed loop names a reviewer that is not its
   owner. A proposed loop without an independent reviewer cannot satisfy the
   review rule no matter how its retries are bounded.

Retry ceilings, approval authority, and evidence rules remain owned by
`docs/00.agent-governance/rules/agentic.md` and
`docs/00.agent-governance/rules/approval-boundaries.md`. ReAct and Reflexion
supply vocabulary for observation and feedback; neither supplies authority.

## Source Rules

- Use original papers for research concepts and official provider/framework
  sources for current mechanisms.
- Keep repository retry, authority, and evidence rules tied to their tracked
  canonical owners.
- Revalidate mutable provider behavior before operational use.

## Sources

- [ReAct paper](https://arxiv.org/abs/2210.03629)
- [Reflexion paper](https://arxiv.org/abs/2303.11366)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Codex hooks](https://learn.chatgpt.com/docs/hooks)
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Gemini CLI documentation](https://google-gemini.github.io/gemini-cli/docs/)
- [Gemini CLI subagents](https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md)
- [Gemini CLI v0.38.1 subagent announcement](https://github.com/google-gemini/gemini-cli/discussions/25562)
- [Gemini CLI hooks](https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/writing-hooks.md)
- [Gemini CLI hook configuration](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/configuration.md)
- [Gemini CLI hook commands](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/commands.md)
- [Gemini CLI v0.26.0 hook announcement](https://github.com/google-gemini/gemini-cli/discussions/17790)
- [Gemini CLI checkpointing](https://google-gemini.github.io/gemini-cli/docs/cli/checkpointing.html)
- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [OpenAI Agents SDK human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/)
- [GitHub Actions workflow syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
- [Provider model contract](../../../00.agent-governance/contracts/provider-models.yaml) - the four typed `harness_loops` and the seven `semantic_events` with their `runtime_depth` values
- [Shared hook dispatcher](../../../../scripts/hooks/agent-event-hook.sh) - the seven-arm event `case` and the provider-specific Stop payloads
- [Agentic rule](../../../00.agent-governance/rules/agentic.md)
- [Task checklists](../../../00.agent-governance/rules/task-checklists.md)
- [QA scope](../../../00.agent-governance/scopes/qa.md)
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md)

All external provider pages in this list were re-fetched on 2026-08-07 and are
recorded above as observed at that retrieval. Every workspace claim, including
the loop table, the Stop payload behavior, and the event counts, was re-derived
from the tracked tree on the same date.

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Quarterly, or when loop/hook/eval mechanisms change
- **Update Trigger**: Stage 00 loop rules, Stage 04/05 contracts, CI, or
  provider lifecycle behavior changes

## Related Documents

- [research pack index](./README.md)
- [harness engineering](./harness-engineering.md)
- [workspace baseline](./workspace-baseline.md)
- [provider implementation comparison](./provider-implementation-comparison.md)
- [agentic rule](../../../00.agent-governance/rules/agentic.md)
