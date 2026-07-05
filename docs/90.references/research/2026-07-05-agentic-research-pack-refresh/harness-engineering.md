---
status: active
---
<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md -->

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
- **Infrastructure harness**: Docker Compose project files, profiles, networks, secrets, health checks, validation scripts, and hardening checks form the controlled runtime environment that agents inspect and validate.
- **Security harness**: Approval boundaries, secret redaction, workflow security scans, sandbox controls, and supply-chain checks constrain what automation may do and what evidence may be recorded.
- **Governance harness**: In a repository-specific harness, Stage 00 rules, scopes, templates, validators, progress logs, and commit discipline make agent actions auditable.

## Harness Components

| Component | External Pattern | `hy-home.docker` Mapping |
| --- | --- | --- |
| Context input | `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, config files | root shims, provider notes, `.agents/README.md`, `.codex/README.md` |
| Execution boundary | test doubles, fixtures, sandbox, permissions | Codex sandbox/approval, Claude permissions/hooks, Gemini trust/sandbox references, filesystem sandbox |
| Tool surface | shell, file tools, MCP servers, web fetch | `scripts/**`, MCP baseline, provider hooks, validation commands |
| Validation harness | test suite, eval runner, scorer | `scripts/validation/**`, `scripts/hardening/**`, CI jobs, `git diff --check` |
| Infrastructure harness | Compose project, profiles, networks, secrets, health checks | `docker-compose.yml`, `infra/**/docker-compose*.yml`, `validate-docker-compose.sh`, `check-all-hardening.sh` |
| Security harness | sandbox, approvals, secret boundaries, workflow security, supply-chain checks | approval boundaries, `.github/SECURITY.md`, GitHub governance, zizmor, template/security baseline |
| Evidence capture | test report, eval score, trace, log | `docs/04.execution/tasks/**`, `memory/progress.md`, PR validation evidence |
| Routing policy | test selection, agent selection, model policy | `subagent-protocol.md`, `agents/`, `scopes/`, model mapping |
| Safety control | no secrets, approvals, protected paths | approval boundaries, secrets rules, sandbox mode, external action boundaries |

## Analysis

Harness engineering centers on repeatable execution environments and observable outcomes. A traditional test harness controls the system under test with stubs, drivers, fixtures, and test data. An AI/agent harness extends that pattern with context input, tool permission, sandboxing, model routing, human approval, evaluation scoring, and trace capture.

`hy-home.docker` already has a repository-level harness. Stage 00 governance defines agent context and behavior, provider surfaces expose execution adapters, and scripts/CI provide validation harnesses. The HAFE policy controls root shims, runtime mirror parity, hook safety, template-first docs, and Graphify advisory boundaries, which matches a policy -> execution -> verification -> evidence harness model.

Infrastructure and security harnesses are adjacent to, but distinct from, test and eval harnesses. Test and eval harnesses measure behavior against tests, scorers, and datasets; infrastructure harnesses render and validate the Docker Compose runtime boundary; security harnesses enforce approval, redaction, workflow, and supply-chain constraints. Stage 90 can describe these harnesses, but the runtime and policy sources of truth remain in Compose, infra, Stage 00, scripts, and CI.

The main external-reference gap is explicit evaluation harnessing for agent outputs. The repository has strong contracts and CI gates, but it does not currently define a dataset/scorer-based eval harness for agent output quality. That remains a follow-up gap rather than an active change in this task.

## Application Notes for This Workspace

- Harness changes should be reviewed across context input, runtime adapters, validation scripts, evidence paths, and README links.
- Before an agent performs external action, the relevant sandbox, approval, and human gate should be clear.
- Provider-specific features should remain adapters and must not replace Stage 00 policy.
- Validation harnesses should separate locally reproducible checks from remote-only CI gates.
- Infrastructure harness claims should cite Compose, infra, validation, and hardening sources rather than restating runtime configuration.
- Security harness claims should cite approval boundaries, disclosure guidance, GitHub governance, zizmor/SARIF, and template/security baseline checks rather than inventing new controls.
- Secret values cannot be harness evidence; only paths, IDs, metadata, or redacted evidence should be recorded.

## Potential Follow-up / Gap

- A future eval-driven agent-output harness would need separate `docs/03.specs` and `docs/04.execution` work.
- Provider release drift may justify a periodic official-docs snapshot or capability review.
- Gemini first-class subagent parity should be described as a capability gap unless a newer official source proves otherwise.

## Source Rules

- Harness terminology should prefer ISTQB, pytest, official eval framework docs, and provider official docs.
- Provider, Docker Compose, and security-source facts were checked against official and repo-local sources on 2026-07-05 and must be rechecked before operational adoption.
- Repo-local application must be corroborated against Stage 00, HAFE docs, scripts, and CI workflow.

## Sources

- [ISTQB test harness glossary](https://glossary.istqb.org/en_US/term/test-harness) - test harness baseline definition
- [pytest fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) - reliable and modular test context concept
- [OpenAI HumanEval](https://github.com/openai/human-eval) - code evaluation harness example and sandbox caveat
- [EleutherAI LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) - model evaluation harness example
- [Inspect AI](https://inspect.aisi.org.uk/) - frontier AI evaluation framework with agentic task support
- [Claude Code hooks](https://code.claude.com/docs/en/hooks) - provider lifecycle hook surface
- [Codex sandboxing](https://developers.openai.com/codex/concepts/sandboxing) - Codex sandbox boundary
- [Codex agent approvals and security](https://developers.openai.com/codex/agent-approvals-security) - approval and network controls
- [Gemini CLI configuration](https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html) - Gemini configuration surface
- [Docker Compose overview](https://docs.docker.com/compose/) - Compose project and runtime orchestration context
- [Docker Compose file reference](https://docs.docker.com/reference/compose-file/) - Compose profiles, networks, secrets, and healthcheck reference context
- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) - repo-local harness surface routing
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) - protected surface and approval matrix
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md) - workflow security and required-check contracts
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
