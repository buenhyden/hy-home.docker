---
status: active
---
<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md -->

# Reference: Automation, Pipeline, and Workflow Loops

## Overview

This reference analyzes automation, pipelines, and workflows for an agent-first
workspace. It compares GitHub Actions workflow concepts and provider hook
surfaces with repo-local scripts, hooks, CI gates, task evidence, and approval
boundaries.

## Purpose

Explain how local and remote automation support loop engineering without
granting authority for external actions or protected-surface changes.

## Repository Role

This reference supports the loop-engineering research, QA scope, scripts README,
provider notes, HAFE documents, and future active-stage automation work. It does
not create new workflows, hooks, scripts, provider settings, CI jobs, or remote
automation behavior.

## Scope

### In Scope

- GitHub Actions workflow, job, and step concepts
- Provider hook and automation surfaces as reference context
- Repo-local script, hook, CI, and task-evidence loops
- Local versus remote automation boundaries

### Out of Scope

- CI workflow edits
- Provider runtime configuration changes
- Remote action dispatch, merge, publish, or paid job execution
- New script or hook implementation

## Definitions / Facts

- **Workflow**: GitHub Actions workflows are YAML-defined automated processes
  triggered by repository events or manual dispatch.
- **Job and step**: GitHub Actions organizes work into jobs and steps, with jobs
  running on runners and steps executing commands or actions.
- **Provider hooks**: Claude Code and Codex document hook surfaces that can run
  at lifecycle or tool-use events. Their event models differ, so repo-local
  governance treats them as adapters rather than policy sources.
- **Provider context substrate**: Codex uses `AGENTS.md` guidance, Claude uses
  Claude Code context and hook surfaces, and Gemini CLI uses `GEMINI.md`,
  settings, commands, and MCP surfaces. Stage 00 remains the policy SSoT.
- **Automation evidence**: This repository records automation results through
  command output summaries, task evidence, generated indexes, progress memory,
  PR checks, SARIF, or skipped-check rationale.

## Analysis

Automation loops are useful because they turn repeated work into bounded,
inspectable feedback. Local scripts can validate docs, Compose, hardening,
provider surfaces, and generated indexes. Provider hooks can guide or validate
agent behavior around tool use. GitHub Actions can run required gates and
security analysis in a remote CI environment.

The same automation surfaces do not grant authority. A workflow trigger, hook,
or script can produce feedback, but posting, publishing, pushing, merging,
opening paid jobs, changing credentials, changing provider runtime config, or
modifying protected GitHub settings still requires explicit user approval and
task evidence.

| Loop Surface | Repo-local Evidence | Boundary |
| --- | --- | --- |
| Local validation | `scripts/validation/**`, `scripts/hardening/**` | Runs local checks and records pass/fail evidence; does not change runtime services. |
| Provider hooks | `scripts/hooks/**`, `.codex/hooks.json`, provider notes | Adapts Stage 00 behavior to provider mechanics; does not redefine policy. |
| CI pipeline | `.github/workflows/ci-quality.yml` | Runs remote checks and SARIF upload; local docs cannot prove remote branch protection by themselves. |
| Knowledge generation | `scripts/knowledge/generate-llm-wiki-index.sh` | Regenerates reference navigation when indexed docs change. |
| Operations scripts | `scripts/operations/**` | May require explicit approval when touching provider surfaces, secrets, versions, or generated files. |
| Task evidence | `docs/04.execution/tasks/**` | Records what ran, what passed, what was skipped, and why. |

For this research pack, automation and workflow analysis remains advisory. New
automation should enter the active lifecycle through the correct requirements,
architecture, spec, plan, task, and operations documents.

## Potential Follow-up / Gap

- A future active automation spec could define a workflow inventory report that
  links GitHub jobs, local validators, and provider hooks.
- A future provider-surface audit could compare Claude, Codex, and Gemini hook
  parity against Stage 00 behavior.
- A future runbook could separate locally reproducible QA gates from CI-only and
  remote-only responsibilities for operators.

## Source Rules

- Prefer official GitHub Actions docs, official provider docs, and repo-local
  canonical scripts/workflows.
- Treat provider hooks and GitHub workflows as execution adapters, not policy
  sources.
- Record remote actions as approval-gated; do not infer authority from
  automation capability.

## Sources

- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) - workflow, job, step, trigger, and YAML syntax reference
- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) - workflow security and secret-handling guidance
- [Claude Code hooks](https://code.claude.com/docs/en/hooks) - provider lifecycle and tool-use hook reference
- [Codex hooks](https://developers.openai.com/codex/hooks) - Codex hook events and execution model
- [Codex CLI](https://developers.openai.com/codex/cli) - Codex local and noninteractive coding agent context
- [Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md) - project instruction discovery
- [Gemini CLI docs](https://google-gemini.github.io/gemini-cli/docs/) - Gemini CLI context, command, and tool documentation entrypoint
- [Scripts README](../../../../scripts/README.md) - repo-local validation, hardening, hooks, knowledge, operations, and library inventory
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - repo-local CI pipeline
- [QA scope](../../../00.agent-governance/scopes/qa.md) - local versus remote QA evidence model
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md) - workflow security, protected-branch, and remote mutation boundaries
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) - protected-surface approval matrix
- [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) - repo-local provider-neutral capability framing

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when workflows, provider hooks, scripts, QA scope,
  or provider documentation changes
- **Update Trigger**: Update when automation authority, pipeline structure, or
  provider hook assumptions change

## Related Documents

- [research pack index](./README.md)
- [loop engineering](./loop-engineering.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
- [provider implementation comparison](./provider-implementation-comparison.md)
- [workspace baseline](./workspace-baseline.md)
