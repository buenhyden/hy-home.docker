---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/workspace-baseline.md -->

# Reference: Workspace Architecture and Governance Baseline

This document defines the system mapping, Spec-Driven Development (SDD) patterns, CI/CD pipeline structures, quality gates, and security rules that form the architectural baseline of the `hy-home.docker` workspace.

---

## Overview

The `hy-home.docker` workspace organizes system design, validation controls, and container runtimes into a structured hierarchy. It bridges standard systems engineering models (e.g. ISO/IEC/IEEE SDLC standards) with agent-centric execution environments (Harness and Loop Engineering), ensuring that autonomous coding agents operate under strict safety boundaries.

## Purpose

This baseline maps the repository's SDLC layout and validation mechanisms to guide developers and autonomous agents in maintaining codebase integrity. It establishes a reference for architecture audits.

## Repository Role

This document acts as an advisory architectural reference. It does not replace active configurations, stage-gated specifications, or live governance rules in Stage 00.

## Scope

### In Scope
- Mapping of the workspace SDLC directories to ISO/IEC/IEEE lifecycle standards.
- Spec-Driven Development (SDD) guidelines and validation hooks.
- CI/CD workflow pipeline architecture (GitHub Actions) and DORA alignment.
- Formatting, linting, and static analysis configurations.
- Security frameworks (NIST SSDF, OWASP SAMM) applied to local execution and agent isolation.
- Procedural conventions for scripts, templates, and bootstrap configurations.

### Out of Scope
- Active policies under `docs/00.agent-governance/`.
- Executable shell wrappers or runtime compose profiles.
- Plaintext secrets or credentials.

## Definitions / Facts

### 1. ISO/IEC/IEEE Standard-Based SDLC Mapping
The workspace maps its documentation stages to software and systems engineering standards such as **ISO/IEC/IEEE 12207** (Lifecycle Processes) and **ISO/IEC/IEEE 29148** (Requirements Engineering):

| SDLC Stage | Purpose & Responsibility (ISO Definition) | Workspace Path | Artifacts & Rules |
| :--- | :--- | :--- | :--- |
| **Requirements Definition** | Define stakeholder needs and identify bounds | [docs/01.requirements/](../../../01.requirements/) | Product Requirements Document (PRD) & Acceptance Criteria |
| **Architecture Design** | Design system boundaries and document ADRs | [docs/02.architecture/](../../../02.architecture/) | Architecture Requirements (ARD) & Architecture Decisions (ADR) |
| **Detailed Design / Specs** | Define interface contracts and validation rules | [docs/03.specs/](../../../03.specs/) | Technical Specifications (Specs) & schema contracts |
| **Execution Planning** | Break down work and establish risk rollbacks | [docs/04.execution/plans/](../../../04.execution/plans/) | Implementation Plans (`implementation_plan.md`) |
| **Implementation / Work** | Apply surgical code changes and record tasks | [docs/04.execution/tasks/](../../../04.execution/tasks/) | Task checklist and validation evidence (`task.md` / `walkthrough.md`) |
| **Operations / Maintenance** | Establish guides, policies, and runbooks | [docs/05.operations/](../../../05.operations/) | Operation Guides, Policies, Runbooks, & Incidents |

### 2. Spec-Driven Development (SDD) Model
Adhering to Fowler's Spec-Driven Development, specifications serve as the ultimate single source of truth (Spec-as-Source):
1. **Spec-Anchored Control**: Changes to source code must trace directly to an approved technical specification ([docs/03.specs/](../../../03.specs/)).
2. **Behavior-Driven Verification**: Acceptance criteria inside specs are programmatically checked against actual infrastructure using validation tools (e.g. `check-doc-implementation-alignment.sh`).

### 3. CI/CD Pipeline & QA Architecture
Workspace verification is governed via a two-tier feedback loop (remote CI and local scripts):
- **DORA Metrics Alignment**:
  - *Deployment Frequency*: Kept high by ensuring all main-branch changes are verified locally and in CI prior to merge.
  - *Lead Time for Changes*: Minimized through pre-commit and post-tool validate hooks that catch formatting/linting errors instantly.
  - *Change Failure Rate*: Kept low by enforcing strict Compose and hardening checks.
  - *Time to Restore Service*: Accelerated by structured recovery runbooks and postmortems.
- **GitHub Actions Pipeline**: Enforced via [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml) with parallelized quality jobs:
  - `docs-traceability`: Verifies doc-to-doc link consistency (`check-doc-traceability.sh`).
  - `repo-contracts`: Audits templates, catalog synchronization, and folder structures (`check-repo-contracts.sh`).
  - `compose-validation`: Parses compose syntax across dev and prod profiles (`validate-docker-compose.sh`).
  - `infrastructure-hardening`: Validates non-root runtime environments and network isolation (`check-all-hardening.sh`).
  - `zizmor-security`: Scans GitHub Actions files for workflow security vulnerabilities.
  - `frontend-quality`: Ensures Next.js build compliance and Storybook coverage thresholds.
- **Local QA Gate Runner**: Program execution can be run locally via [run-local-qa-gates.sh](../../../../scripts/validation/run-local-qa-gates.sh) to replicate CI conditions. Skipped check justifications must be signed and logged in `memory/progress.md`.

### 4. Formatting and Linting Controls
To prevent parsing issues and maintain style consistency, the following tools are integrated:
- **EditorConfig**: Standardizes line endings and indents ([.editorconfig](../../../../.editorconfig)).
- **Prettier**: Resolves spacing and syntax alignment ([.prettierrc.json](../../../../.prettierrc.json)).
- **Shellcheck**: Flags bash anti-patterns and uninitialized variables ([.shellcheckrc](../../../../.shellcheckrc)).
- **Yamllint**: Prevents duplicate keys and syntax errors ([.yamllint](../../../../.yamllint)).
- **Markdown Lint**: Enforces header nesting and layout rules ([.markdownlint-cli2.yaml](../../../../.markdownlint-cli2.yaml)).
- **Automated Hooks**:
  - *Pre-commit*: Blocks commits containing style violations.
  - *Post-Tool Validation*: Run after file modifications by agents to auto-format workspace surfaces (`post-tool-validate.sh`).

### 5. Security Governance & Credential Isolation
- **NIST SSDF & OWASP SAMM Mapping**:
  - *Prepare the Organization (PO)*: Vulnerability reporting guidelines ([.github/SECURITY.md](../../../../.github/SECURITY.md)) and secret redaction rules.
  - *Protect the Software (PS)*: Automated scanners (`gitleaks`, `zizmor`) intercept credentials and workflow configurations.
  - *Produce Well-Secured Software (PW)*: Mandatory checks ([check-template-security-baseline.sh](../../../../scripts/validation/check-template-security-baseline.sh)) audit container minimum privileges.
  - *OWASP Governance / Implementation*: Third-party actions are pinned to SHA hashes for secure builds.
- **Credential Separation**:
  - Non-sensitive variables are declared in [.env.example](../../../../.env.example). Real secrets are stored in untracked `.env` files.
  - Sensitive Docker configurations use files mounted via Docker secrets (`secrets:`) rather than bare environment keys.
  - *Redaction Boundaries*: Agents must never write private keys, plain secrets, or raw token logs into repository reports; only existence or exit status may be documented.
- **Mitigating "Vibe Coding"**:
  - *Mandatory Planning*: `implementation_plan.md` must be reviewed and approved by a human operator before core code changes occur.
  - *Surgical Changes*: Agents must only modify files specified by their current task scope.
  - *Evidence Logs*: Code additions must be validated with shell and test output logs appended to execution tasks.

### 6. Templates and Script Rules
- **Templates**: All newly authored documentation must adopt standard layouts in [docs/99.templates/](../../../99.templates/).
- **Script Purpose Folders**: Per [scripts/README.md](../../../../scripts/README.md), scripts must reside in designated subdirectories:
  - `scripts/validation/` - verification tools.
  - `scripts/hardening/` - OS and container security policies.
  - `scripts/hooks/` - agent inputs and validation triggers.
  - `scripts/knowledge/` - index generators.
  - `scripts/operations/` - backup and setup runbooks.
- **Integration Flow**:
  - 1. Read `docs/00.agent-governance/rules/bootstrap.md` to load the current worker persona.
  - 2. Map compose inclusions and environment parameters.
  - 3. Consult Graphify outputs for cross-component dependencies.

### 7. Follow-up Gaps and Future Actions
- **Automate Graphify Updates**: Link `graphify update .` to post-commit hooks or PR pipelines.
- **DORA Analytics Dashboard**: Establish Grafana boards tracking deployment metrics.
- **Deep Security Scans**: Integrate image vulnerability assessments (`Trivy`) directly into QA pipelines.

## Sources

- [Root README](../../../../README.md) - Workspace architecture and quality gates
- [Agent Governance README](../../../00.agent-governance/README.md) - Governance hub overview
- [Bootstrap Rules](../../../00.agent-governance/rules/bootstrap.md) - SDLC taxonomy and load priorities
- [Documentation Protocol](../../../00.agent-governance/rules/documentation-protocol.md) - Target language and template standards
- [QA Scope](../../../00.agent-governance/scopes/qa.md) - Local and remote QA gates
- [Security Scope](../../../00.agent-governance/scopes/security.md) - Zero-trust and secret redaction rules
- [GitHub Governance](../../../00.agent-governance/rules/github-governance.md) - Pipeline security and branch protection policies
- [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md) - Local harness surfaces mapping
- [NIST SP 800-218 SSDF Specification](https://csrc.nist.gov/pubs/sp/800/218/final) - Secure Software Development Framework
- [OWASP SAMM Version 2.0](https://owasp.org/www-project-samm/) - Software Assurance Maturity Model

## Maintenance

- **Owner**: Workspace Platform Governance Board
- **Review Cadence**: Quarterly, or upon changes to the CI/CD pipelines/formatting configs.
- **Update Trigger**: Triggered by changes to validation scripts, the addition of Compose layers, or updates to security standards.

## Related Documents

- [Research Index README](./README.md)
- [References Category README](../README.md)
- [References Root README](../../README.md)
- [harness-engineering.md](./harness-engineering.md)
- [loop-engineering.md](./loop-engineering.md)
- [provider-implementation-comparison.md](./provider-implementation-comparison.md)
- [ai-agent-catalogs.md](./ai-agent-catalogs.md)
