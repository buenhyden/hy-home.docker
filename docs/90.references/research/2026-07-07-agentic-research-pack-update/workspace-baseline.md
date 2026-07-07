---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/workspace-baseline.md -->

# Reference: Agentic Engineering Workspace Baseline

## Overview

This reference summarizes the current `hy-home.docker` workspace purpose, roles, system structure, rules, SDLC, QA, formatting, linting, and security constraints from repo-local evidence.

## Purpose

Define a stable workspace baseline before conducting gap analysis and comparative audits against external harness engineering and multi-agent systems.

## Repository Role

This document is a reference snapshot for workspace environment and rules. It does not replace or override Stage 00 policy, active execution plans, task evidence, or runtime Docker Compose/script code.

## Scope

### In Scope

- Workspace purpose, structure, and governance hub taxonomy
- SDLC stage gates and spec-driven development rules
- QA gates, formatting rules, linting, and syntax checks
- Automation pipeline and CI/CD workflow mechanisms
- Security controls, credential boundaries, and vibe coding control procedures

### Out of Scope

- Modifying active system rules or runtime configurations
- Exposing sensitive keys, passwords, or credentials
- Enforcing new operational procedures directly from this reference

## Definitions / Facts

- **Workspace Purpose & Rules**: `hy-home.docker` is an agent-first engineering workspace that connects local Docker Compose infrastructure with stage-gated documentation. It treats AI agents as first-class engineering workers with explicit routing and verification requirements.
- **Governance Hub**: `docs/00.agent-governance/` is the single source of truth (SSoT) for agent protocols, rules, scopes, and model tier policies.
- **Spec-driven SDLC**: The development cycle strictly follows Stage 00 (Governance) -> Stage 01 (Requirements) -> Stage 02 (Architecture) -> Stage 03 (Specs) -> Stage 04 (Execution) -> Stage 05 (Operations), supported by Stage 90 (References) and Stage 99 (Templates). Features must be defined in specifications (Stage 03) and plans (Stage 04) before implementation.
- **QA, Formatting, & Linting**: Code and document hygiene is enforced through local hooks (`post-tool-validate.sh`), pre-commit hooks (`.pre-commit-config.yaml`), and linting tools (ESLint, Shellcheck, YAML lint) to check formatting, styles, and parsing syntax.
- **CI/CD Pipeline**: GitHub Actions (`ci-quality.yml`) runs parallel jobs to verify document traceability, repo contracts, Compose configurations, security baseline checks, and script integrity.
- **Security Boundaries**: Credentials and API keys must be isolated using `.env.example` and the `secrets/` directory. They must never be checked into git.
- **Vibe Coding Controls**: Arbitrary coding is suppressed by forcing agents to define implementation plans (`implementation_plan.md`) and tasks (`task.md`), perform surgical edits only, and submit automated check logs as validation evidence.

## Sources

- [Root README](../../../../README.md) - Workspace overview and quality gate summary
- [Agent governance README](../../../00.agent-governance/README.md) - Governance framework SSoT
- [Bootstrap rules](../../../00.agent-governance/rules/bootstrap.md) - Stage taxonomy and bootstrap sequences
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - Template and language contracts
- [QA scope](../../../00.agent-governance/scopes/qa.md) - QA/CI validation gate model
- [Security scope](../../../00.agent-governance/scopes/security.md) - Secret boundaries and access controls
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md) - Branch protection and required checks
- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) - Local harness routing map

## Maintenance

- **Owner**: Workspace Platform Maintainers
- **Review Cadence**: Review when stage-gate contracts, CI workflows, or formatting rules change
- **Update Trigger**: Update when local governance rules are amended or when external SDLC reference models are revised

## Related Documents

- [README.md](./README.md)
- [harness-engineering.md](./harness-engineering.md)
- [loop-engineering.md](./loop-engineering.md)
- [../README.md](../README.md)
