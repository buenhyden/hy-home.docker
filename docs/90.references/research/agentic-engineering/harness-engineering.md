---
status: active
---
<!-- Target: docs/90.references/research/agentic-engineering/harness-engineering.md -->

# Reference: Harness Engineering for Agentic Workspaces

## Overview

This reference interprets harness engineering as a combination of test harnesses, evaluation harnesses, runtime harnesses, and governance harnesses. It then maps those concepts onto the systems, environment, and rules needed in `hy-home.docker`.

## Purpose

Explain harness engineering as a control system that helps agents read, plan, act, verify, and leave evidence safely, not merely as a test runner.

## Repository Role

This reference provides background for the HAFE specification and policy, QA scope, scripts, and provider notes. It does not define new validators, hooks, policies, or runtime adapters.

## Scope

### In Scope

- Test harness and fixture concepts
- LLM/evaluation harnesses and benchmark loops
- Provider runtime harness components
- Approval, sandbox, secret boundaries, and evidence capture
- `hy-home.docker` application analysis

### Out of Scope

- New test framework adoption
- New evaluation benchmark execution
- Provider hook or configuration changes
- Active policy or runbook changes

## Definitions / Facts

- **Test harness**: ISTQB defines a test harness as a collection of drivers and test doubles needed to execute a test suite. This grounds the harness as a controlled execution environment.
- **Fixture**: pytest describes fixtures as defined, reliable, and consistent test context. A fixture is narrower than a harness but central to repeatable testing.
- **Evaluation harness**: OpenAI HumanEval, EleutherAI LM Evaluation Harness, and Inspect AI show how model or AI system behavior can be evaluated through repeatable task, scorer, and dataset structures.
- **Runtime harness**: In agentic coding providers, the runtime harness combines context files, hooks, tools, sandboxes, approvals, subagents, MCP, permissions, and configuration layers.
- **Governance harness**: In a repository-specific harness, Stage 00 rules, scopes, templates, validators, progress logs, and commit discipline make agent actions auditable.

## Harness Components

| Component | External Pattern | `hy-home.docker` Mapping |
| --- | --- | --- |
| Context input | `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, config files | root shims, provider notes, `.agents/README.md`, `.codex/README.md` |
| Execution boundary | test doubles, fixtures, sandbox, permissions | Codex sandbox/approval, Claude permissions/hooks, Gemini trust/sandbox references, filesystem sandbox |
| Tool surface | shell, file tools, MCP servers, web fetch | `scripts/**`, MCP baseline, provider hooks, validation commands |
| Validation harness | test suite, eval runner, scorer | `scripts/validation/**`, `scripts/hardening/**`, CI jobs, `git diff --check` |
| Evidence capture | test report, eval score, trace, log | `docs/04.execution/tasks/**`, `memory/progress.md`, PR validation evidence |
| Routing policy | test selection, agent selection, model policy | `subagent-protocol.md`, `agents/`, `scopes/`, model mapping |
| Safety control | no secrets, approvals, protected paths | approval boundaries, secrets rules, sandbox mode, external action boundaries |

## Analysis

Harness engineering centers on repeatable execution environments and observable outcomes. A traditional test harness controls the system under test with stubs, drivers, fixtures, and test data. An AI/agent harness extends that pattern with context input, tool permission, sandboxing, model routing, human approval, evaluation scoring, and trace capture.

`hy-home.docker` already has a repository-level harness. Stage 00 governance defines agent context and behavior, provider surfaces expose execution adapters, and scripts/CI provide validation harnesses. The HAFE policy controls root shims, runtime mirror parity, hook safety, template-first docs, and Graphify advisory boundaries, which matches a policy -> execution -> verification -> evidence harness model.

The main external-reference gap is explicit evaluation harnessing for agent outputs. The repository has strong contracts and CI gates, but it does not currently define a dataset/scorer-based eval harness for agent output quality. That remains a follow-up gap rather than an active change in this task.

## Application Notes for This Workspace

- Harness changes should be reviewed across context input, runtime adapters, validation scripts, evidence paths, and README links.
- Before an agent performs external action, the relevant sandbox, approval, and human gate should be clear.
- Provider-specific features should remain adapters and must not replace Stage 00 policy.
- Validation harnesses should separate locally reproducible checks from remote-only CI gates.
- Secret values cannot be harness evidence; only paths, IDs, metadata, or redacted evidence should be recorded.

## Potential Follow-up / Gap

- A future eval-driven agent-output harness would need separate `docs/03.specs` and `docs/04.execution` work.
- Provider release drift may justify a periodic official-docs snapshot or capability review.
- Gemini first-class subagent parity should be described as a capability gap unless a newer official source proves otherwise.

## Source Rules

- Harness terminology should prefer ISTQB, pytest, official eval framework docs, and provider official docs.
- Provider product features were checked against official sources on 2026-07-02 and must be rechecked before operational adoption.
- Repo-local application must be corroborated against Stage 00, HAFE docs, scripts, and CI workflow.

## Sources

- [ISTQB test harness glossary](https://glossary.istqb.org/en_US/term/test-harness) - test harness baseline definition
- [pytest fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) - reliable and modular test context concept
- [OpenAI HumanEval](https://github.com/openai/human-eval) - code evaluation harness example and sandbox caveat
- [EleutherAI LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) - model evaluation harness example
- [Inspect AI](https://inspect.aisi.org.uk/) - frontier AI evaluation framework with agentic task support
- [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) - provider lifecycle hook surface
- [Codex sandboxing](https://developers.openai.com/codex/concepts/sandboxing) - Codex sandbox boundary
- [Codex agent approvals and security](https://developers.openai.com/codex/agent-approvals-security) - approval and network controls
- [Gemini CLI configuration](https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html) - Gemini configuration surface
- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) - repo-local harness surface routing
- [HAFE policy](../../../05.operations/policies/00-workspace/harness-agent-first-engineering.md) - repo-local controls

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review quarterly or when provider harness surfaces change
- **Update Trigger**: Update when test/eval/provider harness sources or repo-local HAFE controls change

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [loop engineering](./loop-engineering.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
- [provider implementation comparison](./provider-implementation-comparison.md)
