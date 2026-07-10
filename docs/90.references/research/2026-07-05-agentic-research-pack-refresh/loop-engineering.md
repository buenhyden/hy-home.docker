---
status: active
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

## Loop Contract Matrix

| Loop | Exact input | Action | Evidence | Exit condition | Retry limit | Escalation | Status | Gap / risk | Canonical owner | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Inner reason/action loop | Current user request, loaded Stage 00 context, scoped files, and latest tool observation | Select one bounded read or authorized mutation, execute it, then interpret the result before another action | Tool output, inspected source, patch/diff, and stated assumption | Requested local outcome is achieved and proportionate verification passes, or an approval/clarification boundary is reached | No blind automatic retry; diagnose every failure and stop when the same unresolved blocker repeats | Ask for the missing decision/authority, or report the external/environmental blocker | Implemented | Provider hidden reasoning is not auditable; only actions and evidence are reviewable | `docs/00.agent-governance/rules/agentic.md` | High |
| Validation, formatting, and lint loop | Changed-file set plus the QA/change-type gate map | Run applicable repository-configured checks, fix in-scope defects, rerun only affected checks, then run the completion gate | Exact commands, exit codes, relevant output, final `git diff --check`, and skipped-check rationale | All applicable checks pass and no unexplained skip remains | Retry while each attempt makes an evidence-backed in-scope correction; repeated unchanged failure stops the loop | Route tool/environment failures to the user or owning scope; do not suppress a gate | Implemented | Hook validation is selective: `post-tool-validate.sh` does not run `prettier --check` and cannot prove every CI-only gate | `docs/00.agent-governance/scopes/qa.md` | High |
| CI gate loop | Pushed commit or pull-request event and tracked workflow YAML | Run independent quality jobs and expose logs/status; an authorized maintainer responds to failures | Workflow run, job logs, annotations/SARIF, and required-check state | Required jobs pass and the governing remote merge rule is satisfied | CI retries are operator-controlled; rerun only after diagnosing flake, environment, or code change | Escalate persistent infrastructure/permission failure or required-check ambiguity to repository maintainers | Partially Implemented | Local checkout proves workflow definitions, not remote branch protection or required-check configuration | `docs/00.agent-governance/rules/github-governance.md` | High |
| Evaluation and regression loop | Versioned task/fixture set, baseline, scorer, privacy boundary, and changed system/prompt | Run fixed cases, score outputs, cluster failures, compare to baseline, and record interpretation | Dataset/fixture identity, runner version, scores, failure samples, and regression decision | Acceptance threshold passes with no unexplained high-risk regression | Retry only after a declared system or eval correction; do not tune repeatedly against hidden test answers | Human review calibrates ambiguous scorers and approves any threshold/baseline change | Partially Implemented | Deterministic agent-output fixtures exist, but no general semantic dataset/scorer/baseline contract is adopted | `docs/00.agent-governance/scopes/qa.md` | High |
| Memory and context loop | Material verified finding, completed milestone, unresolved blocker, or approved decision | Record concise durable evidence in the owning lifecycle/memory artifact; reload only relevant context on later work | Stage artifact update, progress entry when in scope, source link, and date/commit context | Future work can recover the decision and provenance without treating memory as active policy | One correction per discovered stale/incorrect entry; conflicting evidence pauses further propagation | Route policy conflicts to the canonical Stage 00 or lifecycle owner | Implemented | Memory can become stale, overlong, or mistaken for authority; exact-scope tasks may intentionally exclude `progress.md` | `docs/00.agent-governance/memory/README.md` | High |
| Plan, task, and review loop | Approved Stage 04 plan entry, bounded task card, and base commit | Implement only assigned files, record checks and deviations, move to Ready for Review, then obtain an independent verdict | Plan/task links, changed-file inventory, commit range, check output, implementer report, and reviewer report | Independent review records pass/accepted verdict; only the controller closes the task | Implementation revisions are bounded by reviewer findings; each new revision receives a fresh independent review | Scope conflict, missing authority, or incompatible evidence returns to the controller/user | Implemented | Self-review cannot satisfy the independent verdict; generic `implementation_plan.md`/`walkthrough.md` are not canonical artifacts | `docs/04.execution/tasks/README.md` | High |
| Security and approval loop | Proposed protected, secret-bearing, destructive, paid, credential, or external mutation | Stop before action, state impact and exact command/change, obtain explicit approval, execute narrowly, then verify | Approval record, redacted command/result, security checks, and changed-resource identity | Approved scoped action completes and postcondition is verified, or approval is denied | Zero execution retries without continuing authority; changed scope requires new approval | User/maintainer/security owner decides; unresolved risk remains blocked rather than bypassed | Implemented | Native provider approval modes can be disabled or run unattended and never broaden repository authority | `docs/00.agent-governance/rules/approval-boundaries.md` | High |
| Automation and pipeline loop | Authorized trigger, immutable input/ref, declared permissions, and tracked workflow/script | Execute bounded stages, propagate failure, retain logs, and avoid external mutation outside the trigger's authority | Script/workflow version, trigger/ref, logs, artifacts/SARIF, and final state | Every required stage passes or the pipeline stops with an attributable failure | Retry only idempotent stages after cause classification; external writes require explicit original or renewed authority | Pipeline owner handles non-idempotence, credential, remote-service, or repeated infrastructure failure | Partially Implemented | Local scripts/hooks/CI are present, but remote schedules, secrets, and enforcement cannot be proved from tracked files | `scripts/README.md` | High |
| Incident and postmortem loop | Live service-impacting symptom, time, scope, and available telemetry | Triage, contain, communicate, recover, record timeline, then write a reviewed learning artifact and track actions | Incident record, timeline, command/metric evidence, recovery proof, postmortem, and follow-up owners | Service is recovered/contained and follow-up actions have owners/status; postmortem review completes | Operational retries follow the owning runbook; repeated ineffective mitigation changes strategy and escalates | Incident command and service owner; security incidents follow disclosure/security routes | Partially Implemented | Stage 05 templates/routing exist, but a document cannot prove every service has tested rollback or live telemetry | `docs/05.operations/incidents/README.md` | High |
| Human-in-the-loop pause/resume | Sensitive proposed action plus serialized task state, rationale, and required decision | Pause before the action, present approve/reject/narrow choices, record the decision, then resume from verified current state | Decision identity/time, approved scope, refreshed diff/state, and resumed action result | Human rejects, narrows, or approves; after approval the exact postcondition is verified | One resume per recorded decision; stale state or changed action requires a new pause/decision | The named human owner decides; no response leaves the action unexecuted | Partially Implemented | Repository rules define the boundary, but durable cross-provider checkpoint/resume behavior is not uniform | `docs/00.agent-governance/rules/approval-boundaries.md` | High |

## Current-State Assessment

| Category | Current state | Primary comparison | Status | Gap | Recommendation | Canonical owner | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Loop engineering | Local action, validation, task/review, security, memory, CI, automation, and incident loops have tracked owners and evidence paths. | ReAct and Reflexion explain observation/feedback; official provider and CI/HITL docs supply current mechanisms. | Partially Implemented | General semantic evals, remote enforcement proof, uniform checkpoint/resume, and tested service recovery are incomplete. | Require the matrix fields for new loops and route implementation through the listed owner instead of encoding it in this reference. | `docs/00.agent-governance/rules/agentic.md` | Matrix above; Stage 00, Stage 04/05, scripts, and workflow YAML | High |

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
establishes the provider capability, not workspace adoption: no tracked
`.gemini` agent or hook configuration wires those mechanisms, and `.agents`
remains a separate Antigravity/reference surface. ReAct and Reflexion are
research foundations only; neither paper defines repository retry limits,
approvals, or evidence policy.

Provider pages were retrieved on 2026-07-10. Mutable documentation proves the
current described surface, not historical availability at an earlier cutoff.

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
- [Codex hooks](https://developers.openai.com/codex/hooks)
- [Codex subagents](https://developers.openai.com/codex/subagents)
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
- [Agentic rule](../../../00.agent-governance/rules/agentic.md)
- [Task checklists](../../../00.agent-governance/rules/task-checklists.md)
- [QA scope](../../../00.agent-governance/scopes/qa.md)
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md)

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
