---
status: active
---
<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md -->

# Reference: Security Governance for Agentic Workspaces

## Overview

This reference analyzes security governance for an agent-first infrastructure
workspace. It compares secure SDLC and supply-chain frameworks with repo-local
security reporting, approval boundaries, GitHub workflow security, hardening,
template/security validation, and secret redaction rules.

## Purpose

Provide source-backed context for security decisions without adopting new
security policy, changing runtime controls, or exposing sensitive data.

## Repository Role

This reference supports Stage 00 security scope, GitHub governance, QA evidence,
HAFE research, and future active-stage security work. It does not replace
security policy, incident procedures, workflow rules, secret management, or
runtime hardening scripts.

## Scope

### In Scope

- Secure SDLC reference frameworks
- GitHub Actions security guidance
- Compose secret handling as reference context
- Repo-local vulnerability reporting, approval, and redaction boundaries
- Security governance follow-up gaps

### Out of Scope

- Formal adoption of NIST SSDF, OWASP SAMM, or SLSA
- Secret value reads, writes, rotations, or disclosure
- Workflow, branch-protection, or remote GitHub setting changes
- Runtime hardening changes

## Definitions / Facts

- **NIST SSDF**: NIST SP 800-218 provides high-level secure software
  development practices that organizations can integrate into an SDLC.
- **OWASP SAMM**: OWASP SAMM is a software assurance maturity model for
  assessing and improving application security practices.
- **SLSA**: SLSA frames supply-chain integrity controls for software artifacts,
  including provenance and build integrity concepts.
- **GitHub Actions secure use**: GitHub guidance highlights workflow risks such
  as untrusted input, secrets exposure, token permissions, third-party actions,
  and cache boundaries.
- **Compose secrets**: Docker Compose secrets provide a way to mount sensitive
  data as files instead of placing values in images or plaintext environment
  variables.
- **Repo-local redaction boundary**: Stage 00 security scope allows metadata
  evidence such as paths, IDs, key names, and command success/failure, while
  prohibiting plaintext secrets, private keys, token-bearing logs, shell
  history, and full secret file bodies.

## Analysis

External frameworks are useful reference lenses, not adopted policy. NIST SSDF
helps organize secure development practices, OWASP SAMM helps reason about
maturity, and SLSA helps frame supply-chain integrity. This repository adopts
security behavior only through active governance, approved specs/tasks, scripts,
workflows, and validation evidence.

Repo-local security governance currently has these evidence classes:

| Evidence Class | Repo-local Surface | Governance Role |
| --- | --- | --- |
| Reporting boundary | `.github/SECURITY.md` | Defines private vulnerability reporting and response expectations. |
| Security scope | `docs/00.agent-governance/scopes/security.md` | Defines zero-trust goal, secret handling, container hardening, and redaction rules. |
| GitHub governance | `docs/00.agent-governance/rules/github-governance.md` | Defines protected-branch discipline, workflow security, required checks, and remote mutation protocol. |
| Approval boundary | `docs/00.agent-governance/rules/approval-boundaries.md` | Defines protected surfaces and evidence required before risky changes. |
| Template/security baseline | `scripts/validation/check-template-security-baseline.sh` | Checks template adoption and security baseline expectations. |
| Workflow security scan | `.github/workflows/ci-quality.yml` `zizmor` job | Provides GitHub Actions security analysis with SARIF upload in CI. |
| Infrastructure hardening | `scripts/hardening/check-all-hardening.sh` | Checks repo-local hardening baseline across infrastructure tiers. |

Security governance for agents depends on the difference between evidence and
authority. A scanner result, framework reference, or research finding is
evidence. It does not authorize secret access, remote mutation, workflow edits,
or runtime changes. Those require an approved active-stage task, concrete
target, redaction boundary, validation command, and rollback or recovery path.

## Potential Follow-up / Gap

- A future active security spec could map NIST SSDF, OWASP SAMM, or SLSA to
  repo-local controls, but this reference does not adopt that mapping.
- A future workflow-security audit could compare every action pin and
  permission block against GitHub's current security guidance.
- A future secret-management audit could verify metadata and rotation readiness
  without exposing secret values.

## Source Rules

- Prefer official standards, official security guidance, and repo-local
  canonical security files.
- Treat frameworks as reference sources until active governance adopts them.
- Never quote, summarize, or commit secret values, private keys, tokens, shell
  history, or raw secret logs.

## Sources

- [NIST SP 800-218 SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) - secure software development practice reference
- [OWASP SAMM](https://owasp.org/www-project-samm/) - software assurance maturity model reference
- [SLSA](https://slsa.dev/) - supply-chain integrity framework reference
- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) - workflow security guidance
- [Use secrets in Compose](https://docs.docker.com/compose/how-tos/use-secrets/) - Compose secret handling model
- [Security disclosure](../../../../.github/SECURITY.md) - repo-local vulnerability reporting boundary
- [Security scope](../../../00.agent-governance/scopes/security.md) - repo-local security and redaction scope
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md) - protected branch, workflow security, and remote mutation policy
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) - protected-surface approval matrix
- [Template/security baseline check](../../../../scripts/validation/check-template-security-baseline.sh) - repo-local template and security baseline gate
- [Hardening script](../../../../scripts/hardening/check-all-hardening.sh) - repo-local infrastructure hardening gate
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - repo-local security scan and required quality gates

## Maintenance

- **Owner**: Documentation maintainers and security reviewers
- **Review Cadence**: Review when security scope, GitHub governance, workflow
  security guidance, hardening scripts, or secure SDLC references change
- **Update Trigger**: Update when security reference assumptions or repo-local
  security gates change

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
- [harness engineering](./harness-engineering.md)
- [loop engineering](./loop-engineering.md)
