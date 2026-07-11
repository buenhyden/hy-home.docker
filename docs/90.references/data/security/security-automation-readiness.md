---
status: active
generated_by: scripts/validation/generate-security-automation-readiness.sh
---

<!-- Target: docs/90.references/data/security/security-automation-readiness.md -->

# Reference: Security Automation Readiness

## Overview

This generated reference summarizes repository-local security automation
readiness for vulnerability gating, SBOM generation, provenance/attestation,
workflow security, secret scanning, dependency updates, and hardening.

## Purpose

The purpose is to make the remaining security automation gaps explicit from
tracked repository evidence. It does not run scanners, generate SBOMs, sign
artifacts, attest builds, query registries, or change CI behavior.

## Repository Role

This reference supports Stage 90 security maturity audits and future Stage
03/04 security automation planning. It does not replace Stage 00 security
governance, `.github/workflows/**`, `.github/SECURITY.md`, runtime
hardening scripts, branch protection, release workflows, or vulnerability
management procedures.

## Scope

### In Scope

- Tracked workflow, script, governance, Dependabot, hardening, and registry
  evidence.
- Readiness classification for security automation capabilities.
- Explicit distinction between implemented controls and future gates.

### Out of Scope

- Running OSV, SCA, SAST, container scanners, Scorecard, SBOM tools, signing,
  attestation, registry lookups, or remote GitHub checks.
- Changing workflow permissions, CI required checks, release artifacts,
  branch protection, runtime Compose files, secrets, credentials, tokens,
  private keys, shell history, raw logs, or `.env` values.

## Definitions / Facts

- **Implemented**: tracked local evidence exists for the automation surface.
- **Partially Implemented**: tracked evidence exists, but live enforcement,
  framework depth, or automation coverage is incomplete.
- **Gap**: no tracked workflow/script automation command or required evidence
  was found for that capability.
- **Readiness snapshot**: a generated reference for planning, not a security
  certification, score, vulnerability statement, SBOM, signature, or
  attestation.

## Summary

| Status | Count |
| --- | ---: |
| Implemented | 7 |
| Partially Implemented | 1 |
| Gap | 3 |

## Readiness Matrix

| Control ID | Control | Status | Evidence | Gap / Next Step |
| --- | --- | --- | --- | --- |
| SEC-AUTO-001 | Security disclosure and vulnerability reporting boundary | Implemented | [.github/SECURITY.md](../../../../.github/SECURITY.md) | Keep reporting and response expectations current. |
| SEC-AUTO-002 | Workflow permissions and dangerous-workflow scanning | Implemented | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[scripts/validation/check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) | Continue checking SHA-pinned actions, least-privilege permissions, and zizmor SARIF upload. |
| SEC-AUTO-003 | Secret scanning and secret-boundary enforcement | Implemented | [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml)<br>[.gitleaks.toml](../../../../.gitleaks.toml)<br>[scripts/validation/check-template-security-baseline.sh](../../../../scripts/validation/check-template-security-baseline.sh) | Pre-commit secret scanning and template/security baseline exist; keep secret values out of generated reports. |
| SEC-AUTO-004 | Dependency update automation | Implemented | [.github/dependabot.yml](../../../../.github/dependabot.yml) | Dependabot coverage exists; vulnerability severity gating remains separate. |
| SEC-AUTO-005 | Infrastructure hardening baseline | Implemented | [scripts/hardening/check-all-hardening.sh](../../../../scripts/hardening/check-all-hardening.sh)<br>[.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml) | Hardening script is wired into CI quality checks. |
| SEC-AUTO-006 | Tracked image/version provenance snapshot | Implemented | [infra/tech-stack.versions.json](../../../../infra/tech-stack.versions.json)<br>[infra/image-tag-policy.exceptions.json](../../../../infra/image-tag-policy.exceptions.json)<br>[scripts/operations/generate-tech-stack-version-provenance.sh](../../../../scripts/operations/generate-tech-stack-version-provenance.sh)<br>[docs/90.references/data/docker/tech-stack-version-provenance.md](../../../../docs/90.references/data/docker/tech-stack-version-provenance.md) | Generated provenance describes tracked registry/Compose evidence, not SBOMs, signatures, or SLSA attestations. |
| SEC-AUTO-008 | OSV/SCA vulnerability gate | Implemented | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | A vulnerability gate command is present in tracked workflow/script surfaces. |
| SEC-AUTO-007 | Branch protection and review evidence | Partially Implemented | [.github/CODEOWNERS](../../../../.github/CODEOWNERS)<br>[.github/rulesets/main-protection.md](../../../../.github/rulesets/main-protection.md) | Local and last-recorded branch-protection evidence exist; live remote enforcement must be re-verified before current claims. |
| SEC-AUTO-009 | SBOM generation | Gap | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | No tracked SBOM generator command was found in workflow/script surfaces. Scanned tracked workflow/script surfaces: 6 workflows, 29 scripts, and `.pre-commit-config.yaml`. |
| SEC-AUTO-010 | Artifact signing or provenance attestation | Gap | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | No tracked signing, SLSA provenance, or attestation workflow command was found. Scanned tracked workflow/script surfaces: 6 workflows, 29 scripts, and `.pre-commit-config.yaml`. |
| SEC-AUTO-011 | OpenSSF Scorecard automation | Gap | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | No tracked OpenSSF Scorecard automation command was found. Scanned tracked workflow/script surfaces: 6 workflows, 29 scripts, and `.pre-commit-config.yaml`. |

## Findings

- Security disclosure, workflow security, secret scanning, Dependabot,
  hardening, and tracked image-version provenance all have repo-local
  evidence.
- Branch protection and review evidence is partial because the repository
  stores CODEOWNERS and last-recorded ruleset evidence, but this generator
  does not query live remote GitHub settings.
- SBOM generation, artifact signing/provenance attestation, and OpenSSF Scorecard automation are still gaps in tracked workflow/script surfaces.

## Gap / Follow-up

| Gap ID | Gap | Suggested Future Stage |
| --- | --- | --- |
| SEC-AUTO-009 | Add SBOM generation and storage rules for build or release artifacts. | Stage 03 security spec + Stage 04 plan |
| SEC-AUTO-010 | Add artifact signing, SLSA provenance, or attestation design for artifact-producing workflows. | Stage 03 security spec + Stage 04 plan |
| SEC-AUTO-011 | Add OpenSSF Scorecard advisory reporting if maintainers want an external security-health signal. | Stage 03 security spec + Stage 04 plan |

## Source Rules

- Use tracked repository files for readiness claims.
- Treat this generated snapshot as planning evidence, not active policy or
  runtime truth.
- Do not include secret values, private keys, tokens, shell history, raw
  secret logs, or `.env` values.

## Sources

- [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml) - CI quality and workflow-security evidence.
- [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) - local pre-commit and secret-scanning hook evidence.
- [.github/dependabot.yml](../../../../.github/dependabot.yml) - dependency update automation evidence.
- [.github/SECURITY.md](../../../../.github/SECURITY.md) - vulnerability reporting boundary.
- [Security framework maturity audit](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md) - framework coverage and gap baseline.
- [Security governance research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md) - secure SDLC and supply-chain reference context.
- [Repository contracts](../../../../scripts/validation/check-repo-contracts.sh) - repo-local governance and workflow contract checks.

## Maintenance

- **Owner**: Security Reviewer / QA Engineer.
- **Review Cadence**: Regenerate after security workflow, Dependabot,
  hardening, vulnerability-gate, SBOM, signing, attestation, or Scorecard
  changes.
- **Update Trigger**: Update when tracked workflow/script security automation
  changes or when Stage 90 security maturity audits are refreshed.

## Related Documents

- [security data index](./README.md)
- [reference data index](../README.md)
- [security framework maturity audit](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md)
- [automation candidates](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
- [security governance research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md)
