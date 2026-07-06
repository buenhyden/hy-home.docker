---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md -->

# Reference: Security Framework Maturity Coverage

## Overview

This reference maps the current `hy-home.docker` security governance and
supply-chain evidence against NIST SSDF, SLSA, and OpenSSF Scorecard criteria.
It is a point-in-time audit view, not a certification claim.

## Purpose

The purpose is to close automation candidate `AEA-AUTO-006` by making the
SSDF/SLSA maturity gap explicit and reusable for later security planning.

## Repository Role

This document supports Stage 00 security governance, Stage 04 QA evidence,
Stage 90 research/audit references, and future security follow-up work. It does
not replace `.github/workflows/**`, `.github/SECURITY.md`, repository
protection settings, validation scripts, incident response procedures, or
runtime infrastructure hardening.

## Scope

### In Scope

- NIST SSDF practice-group coverage.
- SLSA v1.2 source/build/provenance coverage.
- OpenSSF Scorecard readiness signals that overlap with repository controls.
- Repo-local evidence for security policy, workflow security, dependency
  update automation, secret boundaries, hardening, and validation gates.
- Gaps that require future specs, policy changes, CI changes, or security
  automation.

### Out of Scope

- Formal SSDF, SLSA, or Scorecard adoption.
- Running OpenSSF Scorecard, OSV, SBOM, signing, or attestation tooling.
- Changing GitHub workflows, branch protection, rulesets, Dependabot, CI
  permissions, runtime Compose files, secrets, or infrastructure state.
- Reading, printing, summarizing, or committing secret values, private keys,
  tokens, raw secret logs, shell history, or `.env` values.

## Definitions / Facts

- **NIST SSDF**: NIST SP 800-218 Version 1.1 is a secure software development
  framework that organizes high-level secure development practices into
  Prepare the Organization, Protect the Software, Produce Well-Secured
  Software, and Respond to Vulnerabilities groups.
- **NIST SSDF update caveat**: NIST SP 800-218 Rev. 1 initial public draft
  for SSDF Version 1.2 was published on 2025-12-17, with public comments due
  on 2026-01-30. This report uses the final Version 1.1 publication as the
  baseline and treats the draft as a monitoring signal.
- **SLSA v1.2**: SLSA is an approved specification for incrementally improving
  software supply-chain security. Version 1.2 defines build and source tracks,
  levels, and recommended attestation formats including provenance.
- **OpenSSF Scorecard**: Scorecard is an automated open-source security health
  signal that checks supply-chain risk areas such as source, build,
  dependencies, testing, maintenance, security policy, dangerous workflows, and
  token permissions.
- **Coverage status**: `Implemented` means a repo-local control and validation
  or governance surface exists. `Partially Implemented` means evidence exists
  but framework depth, automation, or remote enforcement is incomplete. `Gap`
  means no current repo-local adoption evidence was found.

## Assessment Method

The audit used official framework sources as criteria and repo-local tracked
files as implementation evidence. The graph report was read first, but it is
stale relative to the current branch HEAD, so the claims below were
corroborated directly against Stage 00 governance, `.github/**`,
`.pre-commit-config.yaml`, validation scripts, security research, and existing
audit reports.

No remote GitHub settings were changed or re-verified for this report. Remote
branch protection state remains limited to the last recorded read-only evidence
in `.github/rulesets/main-protection.md`.

## SSDF Coverage Matrix

| SSDF Area | Status | Repo-local Evidence | Gap / Follow-up |
| --- | --- | --- | --- |
| Prepare the Organization (PO) | Implemented | [security scope](../../../00.agent-governance/scopes/security.md), [quality standards](../../../00.agent-governance/rules/quality-standards.md), [approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md), [GitHub governance](../../../00.agent-governance/rules/github-governance.md), [CODEOWNERS](../../../../.github/CODEOWNERS) | Governance exists locally, but formal external SSDF adoption and control-owner attestation are not claimed. |
| Protect the Software (PS) | Partially Implemented | [Security Policy](../../../../.github/SECURITY.md), `.gitleaks.toml`, `.pre-commit-config.yaml`, [template security baseline](../../../../scripts/validation/check-template-security-baseline.sh), [hardening script](../../../../scripts/hardening/check-all-hardening.sh), [security scope](../../../00.agent-governance/scopes/security.md) | Secret scanning and secret-boundary rules exist; SBOM generation, artifact signing, provenance distribution, and release-asset protection are not implemented as framework controls. |
| Produce Well-Secured Software (PW) | Partially Implemented | [CI quality workflow](../../../../.github/workflows/ci-quality.yml), [repo contracts](../../../../scripts/validation/check-repo-contracts.sh), [local QA runner](../../../../scripts/validation/run-local-qa-gates.sh), `.pre-commit-config.yaml`, [Dependabot](../../../../.github/dependabot.yml) | CI, lint, hardening, workflow-security, and dependency-update surfaces exist; systematic SAST/SCA vulnerability gating, threat-model evidence per change, and security regression suites are not complete across all surfaces. |
| Respond to Vulnerabilities (RV) | Partially Implemented | [Security Policy](../../../../.github/SECURITY.md), [incident operations](../../../05.operations/incidents/README.md), [security scope](../../../00.agent-governance/scopes/security.md) | Disclosure intake and incident structure exist; no current evidence of vulnerability triage automation, advisory workflow drill evidence, SLA dashboards, or post-remediation vulnerability metrics. |

## SLSA Coverage Matrix

| SLSA Area | Status | Repo-local Evidence | Gap / Follow-up |
| --- | --- | --- | --- |
| Source control and change review | Partially Implemented | [GitHub governance](../../../00.agent-governance/rules/github-governance.md), [main protection record](../../../../.github/rulesets/main-protection.md), [CODEOWNERS](../../../../.github/CODEOWNERS), [CI quality workflow](../../../../.github/workflows/ci-quality.yml) | Local governance requires protected-branch discipline and CODEOWNERS review; remote enforcement must be re-verified before it is asserted as current. |
| Workflow token and action integrity | Implemented | [CI quality workflow](../../../../.github/workflows/ci-quality.yml), [repo contracts](../../../../scripts/validation/check-repo-contracts.sh), [GitHub governance](../../../00.agent-governance/rules/github-governance.md) | Workflows use explicit permissions and SHA-pinned actions; continue checking any new workflow action references through repo contracts and workflow review. |
| Build track and artifact production | Gap | [CI quality workflow](../../../../.github/workflows/ci-quality.yml), [quality audit](./sdlc-quality-formatting-implementation.md) | CI validates docs, Compose, hardening, frontend build, coverage, and workflow security, but does not publish SLSA build provenance or declare SLSA build-level compliance. |
| Provenance, attestations, and verification | Gap | [security research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md) | No tracked provenance, attestation, signing, verification summary, or consumer verification workflow was found. |
| Dependency and image update hygiene | Partially Implemented | [Dependabot](../../../../.github/dependabot.yml), [tech-stack registry](../../../../infra/tech-stack.versions.json), [tech-stack sync script](../../../../scripts/operations/sync-tech-stack-versions.sh), [image tag policy](../../../../infra/image-tag-policy.exceptions.json) | Dependency update and version-drift controls exist; SBOM, OSV/SCA vulnerability gating, and signed dependency provenance are not implemented. |

## OpenSSF Scorecard Readiness Matrix

| Scorecard Signal | Status | Repo-local Evidence | Gap / Follow-up |
| --- | --- | --- | --- |
| Security Policy | Implemented | [Security Policy](../../../../.github/SECURITY.md) | Keep reporting contacts and response targets current. |
| Token Permissions | Implemented | [CI quality workflow](../../../../.github/workflows/ci-quality.yml), [GitHub governance](../../../00.agent-governance/rules/github-governance.md) | New workflows must preserve explicit least-privilege permissions. |
| Dangerous Workflow Patterns | Implemented | [repo contracts](../../../../scripts/validation/check-repo-contracts.sh), [zizmor CI job](../../../../.github/workflows/ci-quality.yml) | Continue treating `pull_request_target`, permission expansion, and untrusted interpolation as protected-surface findings. |
| Dependency Update Tool | Implemented | [Dependabot](../../../../.github/dependabot.yml) | Dependabot coverage exists for GitHub Actions, Docker, Docker Compose, and Storybook npm dependencies. |
| CI Tests | Partially Implemented | [CI quality workflow](../../../../.github/workflows/ci-quality.yml), [local QA runner](../../../../scripts/validation/run-local-qa-gates.sh) | CI is broad for docs, infra, frontend, and workflow security, but not a universal runtime or vulnerability test suite. |
| Code Review | Partially Implemented | [GitHub governance](../../../00.agent-governance/rules/github-governance.md), [main protection record](../../../../.github/rulesets/main-protection.md), [CODEOWNERS](../../../../.github/CODEOWNERS) | Local and last-recorded remote evidence exist; current remote enforcement must be rechecked before making live enforcement claims. |
| Vulnerabilities | Gap | `.pre-commit-config.yaml`, [Security Policy](../../../../.github/SECURITY.md) | Secret scanning exists through gitleaks, but no current Scorecard/OSV/SCA vulnerability gate or vulnerability dashboard is implemented. |

## Findings

- Security governance is meaningful and repository-real: secret boundaries,
  protected-surface approvals, disclosure guidance, workflow permissions,
  action pinning, Dependabot, gitleaks, hardening, and template/security gates
  all have tracked evidence.
- The repository should not claim formal SSDF adoption, SLSA compliance, or
  OpenSSF Scorecard maturity. Current evidence is a control mapping, not a
  certification, score, or external attestation.
- The largest SLSA gaps are artifact provenance, build attestations, signing,
  and verification. These cannot be inferred from CI build success.
- The largest SSDF gaps are formal vulnerability-management automation,
  repeatable threat-model evidence, and release/artifact supply-chain
  assurance.
- The generated security automation readiness snapshot now makes the local
  workflow/script readiness state explicit; it does not close actual
  vulnerability-gate, SBOM, signing, attestation, or Scorecard gaps.
- Remote GitHub protection should be described as last-recorded evidence unless
  re-verified in a dedicated GitHub governance pass.

## Gap / Follow-up

| Gap ID | Gap | Suggested Future Stage |
| --- | --- | --- |
| SEC-MAT-001 | Add OSV/SCA vulnerability gate or advisory report for dependency and container-image risk. | Stage 03 security spec + Stage 04 plan |
| SEC-MAT-002 | Add SBOM generation and storage rules for build or release artifacts. | Stage 03 security spec + Stage 04 plan |
| SEC-MAT-003 | Add SLSA provenance/attestation design for any artifact-producing workflow. | Stage 03 security spec + Stage 04 plan |
| SEC-MAT-004 | Define change-scoped threat-model evidence requirements for protected surfaces. | Stage 00 governance update + Stage 04 task evidence |
| SEC-MAT-005 | Re-verify remote branch protection and CODEOWNERS enforcement before asserting live protection maturity. | Stage 04 GitHub governance audit |

## Automation Impact

This report closes the audit-matrix part of `AEA-AUTO-006`. The generated
security readiness snapshot provides repo-local planning evidence for the
remaining tooling gaps. Neither document implements security tooling. Future
automation should start with an approved security spec that chooses whether the
next investment is vulnerability gating, SBOM generation, SLSA provenance,
Scorecard reporting, or threat-model evidence.

## Source Rules

- Use official standards and project documentation for framework facts.
- Use tracked repository files for implementation claims.
- Treat local policy and last-recorded remote evidence separately.
- Do not record secret values, private keys, tokens, shell history, raw secret
  logs, or `.env` values.

## Sources

- [NIST SP 800-218 SSDF Version 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) - SSDF practice-group and secure SDLC criteria.
- [NIST SP 800-218 Rev. 1 Initial Public Draft](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd) - SSDF Version 1.2 draft update caveat.
- [SLSA specification v1.2](https://slsa.dev/spec/v1.2/) - source/build tracks, levels, and attestation criteria.
- [OpenSSF Scorecard](https://scorecard.dev/) - supply-chain security check categories and scoring model.
- [OpenSSF Scorecard checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md) - detailed check criteria for CI, code review, dangerous workflows, dependency update tools, token permissions, and vulnerabilities.
- [Security governance research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md) - prior secure SDLC and supply-chain reference analysis.
- [Quality CI formatting research](../../research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md) - QA/CI and secure quality gate criteria.
- [Security scope](../../../00.agent-governance/scopes/security.md) - repo-local security and redaction scope.
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md) - workflow security and repository protection policy.
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) - protected-surface approval matrix.
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - repo-local CI and workflow-security gates.
- [Dependabot config](../../../../.github/dependabot.yml) - dependency update automation coverage.
- [Security Policy](../../../../.github/SECURITY.md) - repo-local vulnerability reporting boundary.
- [Repository contracts](../../../../scripts/validation/check-repo-contracts.sh) - workflow action pinning and required quality-gate contract.
- [Security automation readiness](../../data/security/security-automation-readiness.md) - generated repo-local security automation readiness snapshot.

## Maintenance

- **Owner**: Security Reviewer / QA Engineer.
- **Review Cadence**: Review after security policy, CI workflow, Dependabot,
  branch protection, hardening, template/security, release, SBOM, signing, or
  provenance changes.
- **Update Trigger**: Update when the repository adopts new security controls,
  framework mappings, vulnerability gates, attestation workflows, or external
  framework versions.

## Related Documents

- [Audit pack README](./README.md)
- [Implementation overview](./implementation-overview.md)
- [SDLC quality formatting implementation](./sdlc-quality-formatting-implementation.md)
- [Automation candidates](./automation-candidates.md)
- [Security governance research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md)
- [Security automation readiness](../../data/security/security-automation-readiness.md)
