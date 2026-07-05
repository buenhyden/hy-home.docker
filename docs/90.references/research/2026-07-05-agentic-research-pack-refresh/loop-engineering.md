---
status: active
---
<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md -->

# Reference: Loop Engineering for Agentic Workspaces

## Overview

This reference analyzes agent loops, feedback loops, evaluation loops, CI loops, and human approval loops, then maps them to the stage gates and validation flow in `hy-home.docker`.

## Purpose

Define loop engineering as designing the structures that let agents observe, decide, act, verify, and revise repeatedly while preserving boundaries and evidence.

## Repository Role

This reference provides background for `agentic.md`, QA scope, provider notes, hooks, and CI workflow. It does not define new workflows or hooks.

## Scope

### In Scope

- ReAct-style reason/action loops
- Reflexion-style feedback/memory loops
- Eval-driven development loops
- CI feedback loops
- Human-in-the-loop approval patterns
- Repo-local loop mapping

### Out of Scope

- New AI eval execution
- New hook events
- Automatic deployment or external action
- Active policy changes

## Definitions / Facts

- **Reason/action loop**: ReAct proposes interleaving reasoning traces and task-specific actions so the model can interact with external environments.
- **Reflective feedback loop**: Reflexion stores task feedback as verbal reflection and episodic memory to improve later trials without model weight updates.
- **Tool-use loop**: Agent runtimes repeatedly plan, call tools, observe results, and choose next actions. Google describes Gemini CLI as using a ReAct loop with built-in tools and MCP servers.
- **Eval loop**: Eval-driven development uses scoped tests, logging, automation, human calibration, and continuous evaluation to improve system behavior.
- **CI loop**: GitHub Actions workflows run jobs and steps on push, pull request, or other events to provide automated feedback.
- **Human approval loop**: OpenAI Agents SDK and LangChain HITL docs describe pausing execution for sensitive tool calls and resuming after human decisions.

## Loop Map

| Loop Type | Trigger | Action | Feedback | Repo-local Mapping |
| --- | --- | --- | --- | --- |
| Agent discovery loop | user task, bootstrap | read context, load rules, resolve scope | assumptions, ambiguity, plan | `bootstrap.md`, `agentic.md`, `task-checklists.md` |
| Tool execution loop | file edit, shell command, provider tool call | execute bounded action | command output, diff, hook result | sandbox, approval, `post-tool-validate.sh` |
| Verification loop | changed files, completion gate | run validators | pass/fail and skipped-check rationale | `check-repo-contracts.sh`, `check-doc-traceability.sh`, CI jobs |
| CI loop | push, PR, dispatch | GitHub Actions jobs | required checks and logs | `.github/workflows/ci-quality.yml` |
| Automation pipeline loop | script, hook, CI, or provider workflow trigger | run local or remote automation | pass/fail logs, SARIF, task evidence, progress memory | scripts, provider hooks, `.github/workflows/ci-quality.yml` |
| Security review loop | protected surface, workflow change, secret boundary, dependency or action risk | inspect against policy and scanners | findings, skipped-check rationale, escalation | security scope, GitHub governance, `.github/SECURITY.md`, zizmor |
| Human approval loop | risky ambiguity, external action, protected surface | stop and ask | explicit approval or narrowed scope | user approval boundaries, sandbox escalation |
| Memory loop | material progress or durable finding | update progress/memory | future retrieval context | `memory/progress.md`, memory notes |
| Eval loop | future eval-backed work | run eval tasks/scorers | score, error clusters, regression signals | potential follow-up, not current active surface |

## Analysis

Loop engineering allows repetition while specifying inputs, outputs, stop conditions, and evidence. ReAct and Gemini CLI's ReAct description show how actions connected to external tools or environments produce observations that shape the next step. Reflexion provides a conceptual basis for storing feedback as memory for later trials.

The loops in `hy-home.docker` are broader than a provider's internal agent loop. Stage 00 bootstrap creates a context-loading loop, hooks create tool-lifecycle loops, validation scripts and GitHub Actions create feedback loops, and `memory/progress.md` lets future agents retrieve prior work context.

Automation pipeline loops add another form of repetition: scripts, hooks, CI jobs, and provider workflows can run locally or remotely and feed back logs, SARIF, task evidence, and memory updates. They improve observability, but they do not authorize external actions by themselves. Posting, publishing, pushing, merging, opening paid jobs, changing credentials, or modifying protected surfaces still requires explicit approval and recorded evidence.

The important distinction is between loop autonomy and loop authority. An agent can iterate inside the local sandbox, but external posting, publishing, pushing, merging, credentials, and protected surfaces require explicit approval. Without this separation, loop engineering becomes uncontrolled execution.

## Application Notes for This Workspace

- Every loop should have a trigger, action, feedback, stop condition, and evidence path.
- Failed validation is an observation that should drive the next action, not noise to ignore.
- Human approval loops are critical for external actions, secrets, remote resources, provider config, and policy surfaces.
- Memory loops must stay advisory and must not become active policy.
- Eval loops require datasets, scorers, baselines, regression budgets, and privacy boundaries before adoption.

## Potential Follow-up / Gap

- The repository has strong validation and CI loops, but no explicit agent-output eval loop artifact.
- Provider event support differs, so shared behavioral contracts and provider-native event parity must stay separate.
- Graphify remains an advisory navigation loop and should not become architecture authority.

## Source Rules

- Loop concepts should prefer primary papers, official provider docs, and official eval/HITL docs.
- Framework-specific loop terms are reference context and must not be promoted to repo-local policy without a separate approved change.
- Fast-moving provider behavior must be revalidated before operational adoption.

## Sources

- [ReAct paper](https://arxiv.org/abs/2210.03629) - reasoning/action interleaving concept
- [Google Research ReAct summary](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/) - accessible ReAct overview
- [Reflexion paper](https://arxiv.org/abs/2303.11366) - feedback and episodic memory loop concept
- [Gemini CLI official page](https://developers.google.com/gemini-code-assist/docs/gemini-cli) - Gemini CLI ReAct loop and tool/MCP usage
- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) - eval-driven development loop guidance
- [OpenAI Agents SDK HITL](https://openai.github.io/openai-agents-python/human_in_the_loop/) - approval and resume flow
- [LangChain human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) - policy-based pause and decision pattern
- [GitHub Actions workflow syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions) - workflow/jobs/steps automation loop
- [Agentic rule](../../../00.agent-governance/rules/agentic.md) - repo-local execution loop
- [QA scope](../../../00.agent-governance/scopes/qa.md) - repo-local verification evidence loop
- [Security scope](../../../00.agent-governance/scopes/security.md) - repo-local security review and secret-boundary loop
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md) - workflow security, SARIF, and protected-surface evidence
- [Security disclosure](../../../../.github/SECURITY.md) - vulnerability reporting boundary
- [CI workflow](../../../../.github/workflows/ci-quality.yml) - repo-local CI feedback loop

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review quarterly or when provider loop/hook/eval features change
- **Update Trigger**: Update when repository loop contracts or external loop sources change

## Related Documents

- [research pack index](./README.md)
- [harness engineering](./harness-engineering.md)
- [workspace baseline](./workspace-baseline.md)
- [provider implementation comparison](./provider-implementation-comparison.md)
- [agentic rule](../../../00.agent-governance/rules/agentic.md)
