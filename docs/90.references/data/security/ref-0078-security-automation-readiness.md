---
status: active
generated_by: scripts/validation/generate-security-automation-readiness.sh
---

# Reference: Security Automation Readiness

## Overview

This generated reference summarizes repository-local security automation
readiness for scoped vulnerability gating, broad dependency SCA, container/image
scanning, SBOM generation, provenance/attestation, workflow security, secret
scanning, dependency updates, and hardening.

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
| Partially Implemented | 3 |
| Gap | 3 |

## Readiness Matrix

| Control ID | Control | Status | Evidence | Gap / Next Step |
| --- | --- | --- | --- | --- |
| SEC-AUTO-001 | Security disclosure and vulnerability reporting boundary | Implemented | [.github/SECURITY.md](../../../../.github/SECURITY.md) | Keep reporting and response expectations current. |
| SEC-AUTO-004 | Dependency update automation | Implemented | [.github/dependabot.yml](../../../../.github/dependabot.yml) | Dependabot coverage exists; vulnerability severity gating remains separate. |
| SEC-AUTO-006 | Tracked image/version provenance snapshot | Implemented | [infra/tech-stack.versions.json](../../../../infra/tech-stack.versions.json)<br>[infra/image-tag-policy.exceptions.json](../../../../infra/image-tag-policy.exceptions.json)<br>[scripts/operations/generate-tech-stack-version-provenance.sh](../../../../scripts/operations/generate-tech-stack-version-provenance.sh)<br>[docs/90.references/data/docker/ref-0061-tech-stack-version-provenance.md](../../../../docs/90.references/data/docker/ref-0061-tech-stack-version-provenance.md) | Generated provenance describes tracked registry/Compose evidence, not SBOMs, signatures, or SLSA attestations. |
| SEC-AUTO-009 | SBOM generation | Implemented | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | An SBOM generation command is present in tracked workflow/script surfaces. |
| SEC-AUTO-010 | Artifact signing or provenance attestation | Implemented | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | Signing or attestation command is present in tracked workflow/script surfaces. |
| SEC-AUTO-011 | OpenSSF Scorecard automation | Implemented | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | Scorecard automation is present in tracked workflow/script surfaces. |
| SEC-AUTO-013 | Container/image vulnerability scanning | Implemented | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | A container/image vulnerability scanning command is present in tracked workflow/script surfaces. |
| SEC-AUTO-002 | Workflow permissions and dangerous-workflow scanning | Partially Implemented | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[scripts/validation/check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) | Wire workflow-security checks into CI and repo contracts. |
| SEC-AUTO-003 | Secret scanning and secret-boundary enforcement | Partially Implemented | [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml)<br>[.gitleaks.toml](../../../../.gitleaks.toml)<br>[scripts/validation/check-template-security-baseline.sh](../../../../scripts/validation/check-template-security-baseline.sh) | Add or verify gitleaks and template/security baseline coverage. |
| SEC-AUTO-007 | Branch protection and review evidence | Partially Implemented | [.github/CODEOWNERS](../../../../.github/CODEOWNERS)<br>[.github/rulesets/main-protection.md](../../../../.github/rulesets/main-protection.md) | Local and last-recorded branch-protection evidence exist; live remote enforcement must be re-verified before current claims. |
| SEC-AUTO-005 | Infrastructure hardening baseline | Gap | [scripts/hardening/check-all-hardening.sh](../../../../scripts/hardening/check-all-hardening.sh)<br>[.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml) | Wire hardening checks into local and CI quality gates. |
| SEC-AUTO-008 | Scoped ecosystem vulnerability gate | Gap | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml) | Add an explicitly scoped dependency vulnerability gate with project, ecosystem, severity, and exception ownership. |
| SEC-AUTO-012 | Broad dependency SCA coverage | Gap | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | No tracked broad dependency SCA command was found; the scoped npm audit does not satisfy this control. Scanned tracked workflow/script surfaces: 7 workflows, 37 scripts, and `.pre-commit-config.yaml`. |

## Findings

- Security disclosure, workflow security, secret scanning, Dependabot,
  hardening, and tracked image-version provenance all have repo-local
  evidence.
- Branch protection and review evidence is partial because the repository
  stores CODEOWNERS and last-recorded ruleset evidence, but this generator
  does not query live remote GitHub settings.
- The scoped Storybook Next.js npm audit gate does not close broad dependency
  SCA. Local sample-service image scanning is a separate fixture-policy and
  advisory-rehearsal contract, not a live runtime or release claim.
- broad dependency SCA are still gaps in tracked workflow/script surfaces.

## Gap / Follow-up

| Gap ID | Gap | Suggested Future Stage |
| --- | --- | --- |
| `SEC-AUTO-008` | Add a scoped ecosystem vulnerability gate with explicit project, severity, and exception handling. | Stage 03 security spec + Stage 04 plan |
| `SEC-AUTO-012` | Define broad dependency SCA ecosystems, thresholds, exceptions, remediation ownership, and rollout mode. | Spec 126 archived provenance: `docs/98.archive/tombstones/03.specs/spec-0126-security-supply-chain-remediation.md` |

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
- [Security framework maturity audit](../../audits/ref-0031-security-framework-maturity.md) - framework coverage and gap baseline.
- [Security governance research](../../research/ref-0056-security-governance.md) - secure SDLC and supply-chain reference context.
- [Repository contracts](../../../../scripts/validation/check-repo-contracts.sh) - repo-local governance and workflow contract checks.

## Maintenance

- **Owner**: Security Reviewer / QA Engineer.
- **Review Cadence**: Regenerate after security workflow, Dependabot,
  hardening, vulnerability-gate, broad SCA, container/image scanning, SBOM,
  signing, attestation, or Scorecard
  changes.
- **Update Trigger**: Update when tracked workflow/script security automation
  changes or when Stage 90 security maturity audits are refreshed.

## Related Documents

- [security data index](./README.md)
- [reference data index](../README.md)
- [security framework maturity audit](../../audits/ref-0031-security-framework-maturity.md)
- [automation candidates](../../audits/ref-0021-automation-candidates.md)
- [security governance research](../../research/ref-0056-security-governance.md)
