---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md -->

# Reference: SDLC Quality Formatting Implementation

## Overview

This reference audits implementation status for spec-driven development, SDLC,
CI/CD, QA, formatting, linting, syntax checks, Docker Compose validation,
infrastructure validation, and security quality gates.

## Purpose

The purpose is to show which quality and SDLC controls are implemented and
where coverage remains partial or advisory.

## Repository Role

This document supports future QA and SDLC planning. It does not replace
validation scripts, CI workflow source, Stage 03 specs, Stage 04 task evidence,
or Stage 05 operations docs.

## Scope

### In Scope

- Spec-driven development and stage-gated SDLC.
- CI/CD and local QA gates.
- Formatting, linting, syntax, and contract validation.
- Docker Compose and infrastructure validation.
- Security, hardening, and workflow security quality gates.

### Out of Scope

- Adding tests or CI jobs.
- Changing formatting/linting rules.
- Changing Docker Compose, infrastructure, security, or deployment behavior.
- Claiming production readiness from documentation checks alone.

## Definitions / Facts

- **Spec-driven development** means active design contracts live under
  `docs/03.specs/` and hand off to Stage 04 plans/tasks.
- **QA gate** means a local or CI check with a documented command and pass
  criterion.
- **Formatting/linting coverage** means automated or documented checks for
  style, syntax, or static correctness on a surface.

## Assessment Method

The audit read Stage 03/04 READMEs, the audit pack spec and plan, scripts,
CI workflow, documentation protocol, repo contracts, infra README, Compose
validation/hardening surfaces, and quality-related research.

## Implementation Status Matrix

| Area | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Spec-driven development | Implemented | [Stage 03 README](../../../03.specs/README.md), [audit pack spec](../../../03.specs/105-agentic-engineering-implementation-audit-pack/spec.md) | Active specs define contracts, verification, and handoff paths. |
| Execution planning | Implemented | [Stage 04 plans README](../../../04.execution/plans/README.md), [audit pack plan](../../../04.execution/plans/2026-07-05-agentic-engineering-implementation-audit-pack.md) | Plans define WBS, verification, risk, and completion criteria. |
| Task evidence | Implemented | [Stage 04 tasks README](../../../04.execution/tasks/README.md), [audit pack task](../../../04.execution/tasks/2026-07-05-agentic-engineering-implementation-audit-pack.md) | Task files record evidence, status, deviation, and validation results. |
| Documentation contracts | Implemented | [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md), `scripts/validation/check-repo-contracts.sh` | Required headings, frontmatter, language boundaries, links, and reference contracts are validator-backed. |
| CI/CD quality gates | Implemented | `.github/workflows/ci-quality.yml` | CI runs docs, repo, Compose, hardening, template/security, pre-commit, frontend, coverage, and workflow-security checks. |
| Local QA orchestration | Implemented | `scripts/validation/run-local-qa-gates.sh`, [scripts README](../../../../scripts/README.md) | Local gate runner lists local, CI/local-tooling, and remote-only responsibilities. |
| Formatting | Partially Implemented | `scripts/hooks/post-tool-validate.sh`, pre-commit workflow, provider notes | Text-file trim/newline and selected shell/frontend formatting/linting exist; global formatting across all languages is not complete. |
| Linting | Partially Implemented | `.github/workflows/ci-quality.yml`, pre-commit, frontend lint, shell syntax checks | Frontend and hook/script surfaces have checks; all repo languages do not have a single universal lint gate. |
| Syntax checks | Implemented | `python -m json.tool` examples in HAFE policy, `bash -n`, repo contracts, CI | JSON/YAML/workflow/script/document syntax checks are represented through scripts and CI. |
| Docker Compose validation | Implemented | `scripts/validation/validate-docker-compose.sh`, `.github/workflows/ci-quality.yml`, [infra README](../../../../infra/README.md) | Default and all-profile validation are in CI; local validation script exists. |
| Infrastructure hardening | Implemented | `scripts/hardening/check-all-hardening.sh`, `.github/workflows/ci-quality.yml` | Hardening baseline is a CI gate and local script. |
| Security quality | Partially Implemented | `.github/workflows/ci-quality.yml`, [approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md), `.github/SECURITY.md` | Workflow security and secret boundaries exist; full SSDF/SLSA automation is partial. |

## Findings

- SDLC implementation is strong: specs, plans, tasks, operations, references,
  templates, and validators form a coherent lifecycle.
- CI/CD implementation is strong for quality gates but is primarily validation
  and audit oriented, not deployment/CD release automation.
- QA coverage is strong for documentation, Compose, infrastructure hardening,
  frontend quality, workflow security, and repository contracts.
- Formatting/linting coverage is partial because not every language or artifact
  family has a uniform automated style gate.
- Security coverage is meaningful but should be described as repository
  security governance and workflow hardening, not full SSDF/SLSA maturity.

## Gap / Follow-up

| Gap | Status | Follow-up Direction |
| --- | --- | --- |
| Universal formatting/linting coverage | Partially Implemented | Add a scoped formatting/linting inventory before introducing new gates. |
| Agent-output eval as QA | Partially Implemented | Create eval fixtures and criteria for recurring agent tasks. |
| CI/CD release/deploy automation | Not Implemented / Out of Scope | Keep deployment automation separate from validation CI unless explicitly approved. |
| Security maturity framework automation | Partially Implemented | Add SSDF/SLSA mapping as a separate security reference or audit. |

## Automation Impact

Quality automation should prioritize inventory-driven expansion: identify
artifact families, existing checks, gaps, local command availability, and CI
runtime cost before adding new gates.

## Source Rules

- Use repository scripts and CI workflow for current implementation claims.
- Use external quality/security standards as criteria, not as adopted policy.
- Do not record raw logs or secret values as QA evidence.

## Sources

- [Spec-driven SDLC research](../../research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md) - SDLC criteria.
- [Quality CI formatting research](../../research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md) - QA/CI/formatting criteria.
- [Docker Compose infrastructure research](../../research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md) - Compose/infrastructure validation criteria.
- [Security governance research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md) - security criteria.
- [Stage 03 README](../../../03.specs/README.md) - spec stage contract.
- [Stage 04 plans README](../../../04.execution/plans/README.md) - plan stage contract.
- [Stage 04 tasks README](../../../04.execution/tasks/README.md) - task evidence contract.
- [scripts README](../../../../scripts/README.md) - local validation and QA scripts.
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - remote CI/CD gates.
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) - external CI syntax criteria.
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) - external workflow security criteria.
- [pre-commit](https://pre-commit.com/) - external pre-commit criteria.
- [EditorConfig](https://editorconfig.org/) - external formatting convention criteria.
- [Prettier CLI](https://prettier.io/docs/cli) - external formatting/check criteria.
- [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) - secure development framework criteria.
- [SLSA](https://slsa.dev/) - supply-chain integrity framework criteria.

## Maintenance

- **Owner**: QA Engineer / Documentation Specialist.
- **Review Cadence**: Review after CI workflow, validation script, template,
  infra hardening, or SDLC stage contract changes.
- **Update Trigger**: Update when new quality gates are added, skipped, removed,
  or moved between local and CI-only responsibility.

## Related Documents

- [Audit pack README](./README.md)
- [Implementation overview](./implementation-overview.md)
- [Automation candidates](./automation-candidates.md)
- [Workspace rules/environment audit](./workspace-rules-environment-implementation.md)
