---
title: "Reference: Security Automation Readiness"
version: "1.0.0"
type: "reference/data-pack"
status: "published"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "references"
artifact_id: "DATA-0078"
parent_ids: []
created: "2026-07-06"
observed_at: "2026-08-23"
generated_by: "scripts/validation/generate-security-automation-readiness.sh"
---

# Reference: Security Automation Readiness

## Purpose

This generated reference summarizes repository-local security automation
readiness for scoped vulnerability gating, broad dependency SCA, container/image
scanning, SBOM generation, provenance/attestation, workflow security, secret
scanning, dependency updates, and hardening.

### Audit Intent

The purpose is to make the remaining security automation gaps explicit from
tracked repository evidence. It does not run scanners, generate SBOMs, sign
artifacts, attest builds, query registries, or change CI behavior.

## Consumers

This reference supports Stage 90 security maturity audits and future Stage
03/04 security automation planning. It does not replace Stage 00 security
governance, `.github/workflows/**`, `.github/SECURITY.md`, runtime
hardening scripts, branch protection, release workflows, or vulnerability
management procedures.

## Limitations

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

## Schema

- **Implemented**: tracked local evidence exists for the automation surface.
- **Partially Implemented**: tracked evidence exists, but live enforcement,
  framework depth, or automation coverage is incomplete.
- **Gap**: no tracked workflow/script automation command or required evidence
  was found for that capability.
- **Readiness snapshot**: a generated reference for planning, not a security
  certification, score, vulnerability statement, SBOM, signature, or
  attestation.

## Inventory

| Status | Count |
| --- | ---: |
| Implemented | 11 |
| Partially Implemented | 1 |
| Gap | 1 |

### Readiness Matrix

| Control ID | Control | Status | Evidence | Gap / Next Step |
| --- | --- | --- | --- | --- |
| SEC-AUTO-001 | Security disclosure and vulnerability reporting boundary | Implemented | [.github/SECURITY.md](../../../../.github/SECURITY.md) | Keep reporting and response expectations current. |
| SEC-AUTO-002 | Workflow permissions and dangerous-workflow scanning | Implemented | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[scripts/validation/run-ci-gate.py](../../../../scripts/validation/run-ci-gate.py) | Continue checking SHA-pinned actions, least-privilege permissions, and zizmor SARIF upload. |
| SEC-AUTO-003 | Secret scanning and secret-boundary enforcement | Implemented | [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml)<br>[.gitleaks.toml](../../../../.gitleaks.toml)<br>[scripts/validation/check-template-security-baseline.sh](../../../../scripts/validation/check-template-security-baseline.sh) | Pre-commit secret scanning and template/security baseline exist; keep secret values out of generated reports. |
| SEC-AUTO-004 | Dependency update automation | Implemented | [.github/dependabot.yml](../../../../.github/dependabot.yml) | Dependabot coverage exists; vulnerability severity gating remains separate. |
| SEC-AUTO-005 | Infrastructure hardening baseline | Implemented | [scripts/hardening/check-all-hardening.sh](../../../../scripts/hardening/check-all-hardening.sh)<br>[.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml) | Hardening script is wired into CI quality checks. |
| SEC-AUTO-006 | Tracked image/version provenance snapshot | Implemented | [infra/tech-stack.versions.json](../../../../infra/tech-stack.versions.json)<br>[infra/image-tag-policy.exceptions.json](../../../../infra/image-tag-policy.exceptions.json)<br>[scripts/operations/generate-tech-stack-version-provenance.sh](../../../../scripts/operations/generate-tech-stack-version-provenance.sh)<br>[docs/90.references/data/0061-tech-stack-version-provenance/README.md](../../../../docs/90.references/data/0061-tech-stack-version-provenance/README.md) | Generated provenance describes tracked registry/Compose evidence, not SBOMs, signatures, or SLSA attestations. |
| SEC-AUTO-008 | Scoped ecosystem vulnerability gate | Implemented | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml) | The tracked Storybook Next.js npm audit gate has an explicit project and severity scope. |
| SEC-AUTO-009 | SBOM generation | Implemented | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[.github/workflow-contract.yml](../../../../.github/workflow-contract.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | An SBOM generation command is present in tracked workflow/script surfaces. |
| SEC-AUTO-010 | Artifact signing or provenance attestation | Implemented | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[.github/workflow-contract.yml](../../../../.github/workflow-contract.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | Signing or attestation command is present in tracked workflow/script surfaces. |
| SEC-AUTO-011 | OpenSSF Scorecard automation | Implemented | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[.github/workflow-contract.yml](../../../../.github/workflow-contract.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | Scorecard automation is present in tracked workflow/script surfaces. |
| SEC-AUTO-013 | Container/image vulnerability scanning | Implemented | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[.github/workflow-contract.yml](../../../../.github/workflow-contract.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | A container/image vulnerability scanning command is present in tracked workflow/script surfaces. |
| SEC-AUTO-007 | Branch protection and review evidence | Partially Implemented | [.github/CODEOWNERS](../../../../.github/CODEOWNERS)<br>[.github/rulesets/main-protection.md](../../../../.github/rulesets/main-protection.md) | Local and last-recorded branch-protection evidence exist; live remote enforcement must be re-verified before current claims. |
| SEC-AUTO-012 | Broad dependency SCA coverage | Gap | [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml)<br>[.github/workflow-contract.yml](../../../../.github/workflow-contract.yml)<br>[scripts/README.md](../../../../scripts/README.md)<br>[.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | No tracked broad dependency SCA command was found; the scoped npm audit does not satisfy this control. Scanned tracked workflow/script surfaces: 6 workflows, 24 scripts, `.pre-commit-config.yaml`, and 65 reachable typed gates. |

## Provenance

- Security disclosure, workflow security, secret scanning, Dependabot,
  hardening, and tracked image-version provenance all have repo-local
  evidence.
- Branch protection and review evidence is partial because the repository
  stores CODEOWNERS and last-recorded ruleset evidence, but this generator
  does not query live remote GitHub settings.
- The scoped Storybook Next.js npm audit gate does not close broad dependency
  SCA. Local sample-service image scanning is a separate fixture-policy and
  advisory-rehearsal contract, not a live runtime or release claim.
- broad dependency SCA remains a gap in tracked workflow/script surfaces.

### Gap / Follow-up

| Gap ID | Gap | Suggested Future Stage |
| --- | --- | --- |
| `SEC-AUTO-012` | Define broad dependency SCA ecosystems, thresholds, exceptions, remediation ownership, and rollout mode. | Stage 98 migration lookup: `docs/98.archive/migrations/0003-workspace-governance-simplification.md` |

### Source Rules

- Use tracked repository files for readiness claims.
- Admit typed commands and Actions only after complete canonical workflow
  validation plus narrow fail-closed job/step shape and failure checks;
  registered Action evidence must use a single unconditional parsed `uses`.
- Treat this generated snapshot as planning evidence, not active policy or
  runtime truth.
- Do not include secret values, private keys, tokens, shell history, raw
  secret logs, or `.env` values.

### Sources

- [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml) - CI quality and workflow-security evidence.
- [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) - local pre-commit and secret-scanning hook evidence.
- [.github/dependabot.yml](../../../../.github/dependabot.yml) - dependency update automation evidence.
- [.github/SECURITY.md](../../../../.github/SECURITY.md) - vulnerability reporting boundary.
- [Security framework maturity audit](../../audits/0031-security-framework-maturity/README.md) - framework coverage and gap baseline.
- [Security governance research](../../research/0002-agentic-engineering-research-pack/m0017-security-governance.md) - secure SDLC and supply-chain reference context.
- [.github/workflow-contract.yml](../../../../.github/workflow-contract.yml) - typed workflow gates, adapters, actions, and job-root reachability.
- [Public validation runner](../../../../scripts/validation/run-ci-gate.py) - contract-owned changed and full suite routing.

## Refresh

- **Owner**: Security Reviewer / QA Engineer.
- **Review Cadence**: Regenerate after security workflow, Dependabot,
  hardening, vulnerability-gate, broad SCA, container/image scanning, SBOM,
  signing, attestation, or Scorecard
  changes.
- **Update Trigger**: Update when tracked workflow/script security automation
  changes or when Stage 90 security maturity audits are refreshed.

## Traceability

- [security data index](./README.md)
- [reference data index](../README.md)
- [security framework maturity audit](../../audits/0031-security-framework-maturity/README.md)
- [automation candidates](../../audits/0021-automation-candidates/README.md)
- [security governance research](../../research/0002-agentic-engineering-research-pack/m0017-security-governance.md)
