---
title: "Reference: Security Framework Maturity Coverage"
type: reference/audit-pack
layer: references
status: active
owner: "@buenhyden"
artifact_id: AUD-0031
parent_ids:
- AUD-0026
created: '2026-07-05'
updated: '2026-08-23'
observed_at: '2026-07-05'
reviewed_at: 2026-07-27
---

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

The current agent harness adds bounded value-free credential rejection,
exact synthetic evaluator inputs, protected-path QA routing, strict generated
provider schemas, and an evidence-bound controlled all-files wrapper. These
strengthen repository-local validation and redaction controls but do not run a
live provider, scanner, deployment, or remote enforcement mutation, so no
supply-chain or remote-security criterion is promoted from those definitions
alone.

No remote GitHub setting was changed for this report. Seven tracked workflows
now define 23 jobs, including 16 in `ci-quality.yml`. The latest public remote
observation at `2026-07-26T18:22:32+09:00` records default commit `a897978f`,
failed run `29777690571`, and 15 observed jobs; its root cause is unverified.
Authenticated classic protection, rulesets, environments, secrets, variables,
and complete CODEOWNERS enforcement were not available in that observation.
The older 2026-07-12 12-context result remains historical evidence rather than
current remote control state.

### Remote Evidence Classes as of 2026-07-26

| Evidence class | Evidence | Security boundary |
| --- | --- | --- |
| Tracked definitions | Seven local workflows define 23 jobs, including 16 quality jobs, and tracked governance includes CODEOWNERS policy. | Local source is not remote enforcement or execution evidence. |
| Public remote observation | Default commit `a897978f` and failed run `29777690571` expose 15 observed jobs plus three GitHub-managed workflows. | The failed run's root cause is unverified and does not prove current local-definition coverage. |
| Authenticated remote controls | Classic protection, rulesets, environments, secrets, variables, and complete CODEOWNERS enforcement remain unverified in the latest observation. | Historical 2026-07-12 configuration must not be promoted to current state. |
| Enforcement mutation | No protection, ruleset, environment, workflow, CODEOWNERS, or repository setting was changed. | A later change needs separate approval, exact contexts, rollback evidence, and read-back. |

## Bounded Revalidation (through 2026-07-27)

The framework criterion statuses below preserve the existing baseline, while the
2026-07-19 scanner observations remain dated historical evidence. The current
security supply-chain task
has deterministic local fixture, policy, orchestration, and immutable
build-context surfaces with hardened input validation. Its present runtime boundary is still blocked before
Docker execution because no approved current scanner database seed is
available; consequently, no current policy pass, accepted verdicts, or
generation-bound pair manifest exists. The earlier vulnerable-image advisory result is historical
and superseded, not an active exception or current acceptance result.

The deployment and release task
therefore has implementation and static verification only. It has not produced
positive promotion or rollback runtime evidence. This bounded local progress
does not establish broad dependency or image coverage, SBOM retention, SLSA
provenance, signing or attestation verification, OpenSSF Scorecard maturity,
remote enforcement, or production readiness. Exact commands, classifications,
digests, reviews, and commits remain owned by the linked Stage 04 task records.

## Criterion Matrix

| Criterion ID | External criterion | Workspace evidence | Status | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| SEC-01 | Publish a vulnerability reporting boundary and response expectations. | `.github/SECURITY.md` defines reporting channels and boundaries. | Implemented | 2 | Retain | Security governance owner | Document freshness review; no intake automation claimed. | Inspect policy links, contacts, and supported-version language. | High. |
| SEC-02 | Require explicit approval and redacted evidence for protected security/runtime surfaces. | Stage 00 approval boundaries, scopes, task checklists, and Stage 04 evidence requirements exist. | Implemented | 2 | Retain | Stage 00 security/approval governance | Existing contract checks; approvals remain human/state dependent. | Trace one protected-surface task contract and repo contracts. | High. |
| SEC-03 | Minimize workflow permissions and pin third-party actions. | `ci-quality.yml` uses explicit read permissions and SHA-pinned actions; repo contracts check workflow patterns. The workflow pins `zizmor==1.28.0`, which is patched for the advisory affecting 1.27.0. | Implemented | 3 | Retain | GitHub workflow and repository-contract owners | Existing workflow contract and pinned zizmor definition. | Inspect permissions/action refs and run applicable workflow validators. | High for tracked definitions. |
| SEC-04 | Scan committed content for secret patterns while preserving redaction boundaries. | Gitleaks is configured in pre-commit; governance prohibits recording secret values and routes secrets to mounts/Docker Secrets. | Implemented | 3 | Retain | Security scope and pre-commit owner | Existing file-filtered secret scan; a pass is not proof of zero secrets. | Applicable gitleaks hook result without exposing findings. | High. |
| SEC-05 | Automate dependency updates for declared ecosystems and keep update coverage separate from vulnerability gating. | Dependabot covers Actions, Docker, Compose, and Storybook npm dependencies. | Implemented | 3 | Retain | Dependabot/GitHub governance owner | Existing update PR automation. | Inspect `.github/dependabot.yml` ecosystems/directories/schedule. | High. |
| SEC-06 | Fail builds on an approved vulnerability threshold for an explicitly scoped project. | CI runs high-severity `npm audit` for Storybook Next.js only. | Partial | 3 | Improve | Security/QA and Storybook owner | Existing scoped npm gate; exception/coverage semantics remain narrow. | Inspect/run `dependency-vulnerability-audit` in an approved applicable environment. | High for the scoped npm project. |
| SEC-07 | Scan broader dependencies and container images with owned severity, exception, and remediation rules. | No broad OSV/SCA or container-image scanning gate exists; the one npm audit must not be generalized. | Missing | 0 | Add | Task 11 security supply-chain spec/plan | Future scanner selection and policy with redacted evidence. | Require ecosystem/image scope, severity threshold, exceptions, ownership, and test evidence. | High. |
| SEC-08 | Generate and retain an SBOM for artifact-producing build/release flows. | The security readiness scan finds no tracked SBOM generation command or artifact policy. | Missing | 0 | Add | Task 11 security supply-chain spec/plan | Future SPDX/CycloneDX generation/storage design. | Require deterministic generation, artifact association, retention, and consumer evidence. | High. |
| SEC-09 | Produce build provenance/attestations for artifact-producing workflows. | Tracked version provenance describes declarations only; no SLSA build provenance or attestation workflow exists. | Missing | 0 | Add | Task 11 security supply-chain spec/plan | Future provenance/attestation design after an artifact boundary exists. | Require builder identity, source/materials, subject digest, and verifier acceptance. | High. |
| SEC-10 | Sign artifacts and verify signatures/attestations before promotion or consumption. | No tracked signing keyless flow, signature, attestation verification, or promotion check exists. | Missing | 0 | Add | Task 11 security supply-chain and deployment/release specs/plans | Future signing and verification automation with key/identity boundaries. | Require test artifact, signer identity, verification result, failure case, and rollback. | High. |
| SEC-11 | Run OpenSSF Scorecard only as an explicit security-health signal with reviewed findings. | Framework mapping exists, but no Scorecard action/CLI execution or score evidence exists. | Missing | 0 | Add | Task 11 security supply-chain spec/plan | Candidate advisory Scorecard report; no maturity claim from mapping alone. | Require pinned tool/action, scoped permissions, result review, and false-positive handling. | High. |
| SEC-12 | Attach threat-model evidence to changes that cross trust or protected-surface boundaries. | Security scopes and threat-model guidance exist, but no universal change-scoped machine gate or complete evidence inventory exists. | Partial | 1 | Improve | Stage 00 security governance plus affected Stage 03/04 owner | Candidate profile/checklist integration only after false-positive review. | Review protected-surface task evidence for threats, mitigations, and residual risk. | Medium. |
| SEC-13 | Maintain incident/vulnerability response procedures and exercise them periodically. | Security policy and Stage 05 incident structure exist; no current vulnerability drill, SLA dashboard, or remediation-metric evidence was collected. | Partial | 1 | Improve | Security and Operations/SRE owners | Future tabletop/drill evidence; do not manufacture incidents. | Require dated scenario, roles, timeline, decisions, actions, and improvement owners. | High for documents; no exercise evidence. |
| SEC-14 | Revalidate remote branch protection, required checks, and CODEOWNERS enforcement before asserting live protection. | The 2026-07-26 public observation records default commit `a897978f`, failed run `29777690571`, and 15 observed jobs with unverified root cause. Current authenticated protection, rulesets, environments, secrets, variables, and complete CODEOWNERS enforcement remain unknown; no mutation occurred. | Needs Revalidation | 1 | Improve | GitHub governance owner | Retain dated public evidence; verify authenticated controls, CODEOWNERS, and recent named runs before any separately approved rollback-bound synchronization task. | Timestamped public observation, authorized protection/context/CODEOWNERS query, exact local/remote diff, and post-mutation read-back when approved. | High for the tracked-definition/public-run/authenticated-control/mutation boundary. |

## SSDF Coverage Matrix

| SSDF Area | Status | Repo-local Evidence | Gap / Follow-up |
| --- | --- | --- | --- |
| Prepare the Organization (PO) | Implemented | security scope (retired path: `00.agent-governance/scopes/security.md`), [quality standards](../../../00.agent-governance/policies/quality-standards.md), [approval boundaries](../../../00.agent-governance/policies/approval-boundaries.md), [GitHub governance](../../../00.agent-governance/policies/github-governance.md), [CODEOWNERS](../../../../.github/CODEOWNERS) | Governance exists locally, but formal external SSDF adoption and control-owner attestation are not claimed. |
| Protect the Software (PS) | Partially Implemented | [Security Policy](../../../../.github/SECURITY.md), `.gitleaks.toml`, `.pre-commit-config.yaml`, [template security baseline](../../../../scripts/validation/check-template-security-baseline.sh), [hardening script](../../../../scripts/hardening/check-all-hardening.sh), security scope (retired path: `00.agent-governance/scopes/security.md`) | Secret scanning and secret-boundary rules exist; SBOM generation, artifact signing, provenance distribution, and release-asset protection are not implemented as framework controls. |
| Produce Well-Secured Software (PW) | Partially Implemented | [CI quality workflow](../../../../.github/workflows/ci-quality.yml), repo contracts (retired path: `scripts/validation/check-repo-contracts.sh`), [local QA runner](../../../../scripts/validation/run-local-qa-gates.sh), `.pre-commit-config.yaml`, [Dependabot](../../../../.github/dependabot.yml) | CI, lint, hardening, workflow-security, dependency-update, and scoped Storybook Next.js npm vulnerability audit surfaces exist; systematic SAST, container/image vulnerability scanning, threat-model evidence per change, and security regression suites are not complete across all surfaces. |
| Respond to Vulnerabilities (RV) | Partially Implemented | [Security Policy](../../../../.github/SECURITY.md), [incident operations](../../../05.operations/incidents/README.md), security scope (retired path: `00.agent-governance/scopes/security.md`) | Disclosure intake and incident structure exist; no current evidence of vulnerability triage automation, advisory workflow drill evidence, SLA dashboards, or post-remediation vulnerability metrics. |

## SLSA Coverage Matrix

| SLSA Area | Status | Repo-local Evidence | Gap / Follow-up |
| --- | --- | --- | --- |
| Source control and change review | Partially Implemented | [GitHub governance](../../../00.agent-governance/policies/github-governance.md), GitHub Actions control-plane observation (retired path: `data/governance/ref-0071-github-actions-control-plane-observation.yaml`), [CODEOWNERS](../../../../.github/CODEOWNERS), [CI quality workflow](../../../../.github/workflows/ci-quality.yml) | Dated public evidence records a failed 15-job run; current authenticated protection/ruleset state and complete CODEOWNERS enforcement remain unverified. |
| Workflow token and action integrity | Implemented | [CI quality workflow](../../../../.github/workflows/ci-quality.yml), repo contracts (retired path: `scripts/validation/check-repo-contracts.sh`), [GitHub governance](../../../00.agent-governance/policies/github-governance.md) | Workflows use explicit permissions and SHA-pinned actions; continue checking any new workflow action references through repo contracts and workflow review. |
| Build track and artifact production | Gap | [CI quality workflow](../../../../.github/workflows/ci-quality.yml), [quality audit](../0030-sdlc-quality-formatting-implementation/README.md) | CI validates docs, Compose, hardening, frontend build, coverage, and workflow security, but does not publish SLSA build provenance or declare SLSA build-level compliance. |
| Provenance, attestations, and verification | Gap | `security research` (retiring 2026-07-05 pack, cited without a path because pre-deletion gate 4 admits no clickable link; `security-governance` leaf) | No tracked provenance, attestation, signing, verification summary, or consumer verification workflow was found. |
| Dependency and image update hygiene | Partially Implemented | [Dependabot](../../../../.github/dependabot.yml), [tech-stack registry](../../../../infra/tech-stack.versions.json), [tech-stack sync script](../../../../scripts/operations/sync-tech-stack-versions.sh), [image tag policy](../../../../infra/image-tag-policy.exceptions.json), `.github/workflows/ci-quality.yml` | Dependency update, version-drift, and scoped Storybook Next.js npm vulnerability audit controls exist; SBOM, broad OSV/container vulnerability scanning, and signed dependency provenance are not implemented. |

## OpenSSF Scorecard Readiness Matrix

| Scorecard Signal | Status | Repo-local Evidence | Gap / Follow-up |
| --- | --- | --- | --- |
| Security Policy | Implemented | [Security Policy](../../../../.github/SECURITY.md) | Keep reporting contacts and response targets current. |
| Token Permissions | Implemented | [CI quality workflow](../../../../.github/workflows/ci-quality.yml), [GitHub governance](../../../00.agent-governance/policies/github-governance.md) | New workflows must preserve explicit least-privilege permissions. |
| Dangerous Workflow Patterns | Implemented | repo contracts (retired path: `scripts/validation/check-repo-contracts.sh`), [zizmor CI job](../../../../.github/workflows/ci-quality.yml) | `zizmor==1.28.0` is pinned after the 1.27.0 advisory; continue treating `pull_request_target`, permission expansion, and untrusted interpolation as protected-surface findings. |
| Dependency Update Tool | Implemented | [Dependabot](../../../../.github/dependabot.yml) | Dependabot coverage exists for GitHub Actions, Docker, Docker Compose, and Storybook npm dependencies. |
| CI Tests | Partially Implemented | [CI quality workflow](../../../../.github/workflows/ci-quality.yml), [local QA runner](../../../../scripts/validation/run-local-qa-gates.sh) | CI is broad for docs, infra, frontend, and workflow security, but not a universal runtime or vulnerability test suite. |
| Code Review | Partially Implemented | [GitHub governance](../../../00.agent-governance/policies/github-governance.md), GitHub Actions control-plane observation (retired path: `data/governance/ref-0071-github-actions-control-plane-observation.yaml`), [CODEOWNERS](../../../../.github/CODEOWNERS) | Public run metadata is dated evidence; current authenticated protection and complete CODEOWNERS enforcement remain separately unverified. |
| Vulnerabilities | Partially Implemented | `.pre-commit-config.yaml`, [Security Policy](../../../../.github/SECURITY.md), `.github/workflows/ci-quality.yml` | Secret scanning exists through gitleaks and Storybook Next.js has a high-severity npm audit gate; Scorecard vulnerability reporting, OSV/container scanning, and vulnerability dashboards are not implemented. |

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
- The largest SSDF gaps are broad vulnerability-management automation,
  repeatable threat-model evidence, and release/artifact supply-chain
  assurance; the scoped Storybook Next.js npm gate does not cover non-npm or
  container/image risk.
- The generated security automation readiness snapshot now makes the local
  workflow/script readiness state explicit. The scoped npm vulnerability gate
  satisfies only `SEC-AUTO-008`; broad dependency SCA (`SEC-AUTO-012`) and
  container/image vulnerability scanning (`SEC-AUTO-013`) remain `Gap`, along
  with SBOM, signing, attestation, and Scorecard automation.
- Remote GitHub state should be described by evidence class: the dated
  2026-07-26 public observation records a failed 15-job run with unverified
  root cause, while authenticated protection/ruleset/environment state and
  complete CODEOWNERS enforcement remain unknown. No remote mutation is
  claimed.

## Gap / Follow-up

| Gap ID | Gap | Suggested Future Stage |
| --- | --- | --- |
| SEC-MAT-001 | Broaden vulnerability automation beyond the scoped Storybook Next.js npm audit gate to cover OSV/SCA and container-image risk. | Draft Spec 126 |
| SEC-MAT-002 | Add SBOM generation and storage rules for build or release artifacts. | Draft Spec 126 |
| SEC-MAT-003 | Add SLSA provenance/attestation design for any artifact-producing workflow. | Draft Spec 126 |
| SEC-MAT-004 | Define change-scoped threat-model evidence requirements for protected surfaces. | Stage 00 governance update + Stage 04 task evidence |
| SEC-MAT-005 | Verify authenticated protection/ruleset/environment state, recent named runs, and complete CODEOWNERS enforcement; reconcile any confirmed drift only through a separately approved rollback-bound remote task. | Stage 04 GitHub governance audit |

## Automation Impact

This report closes the audit-matrix part of `AEA-AUTO-006`. The generated
security readiness snapshot provides repo-local planning evidence for the
remaining tooling gaps. The scoped npm vulnerability gate is now implemented,
but neither document implements SBOM, signing, attestation, Scorecard, or broad
scanner coverage. Future automation should start with an approved security spec
that chooses whether the next investment is broader vulnerability scanning,
SBOM generation, SLSA provenance, Scorecard reporting, or threat-model evidence.

## Source Rules

- Use official standards and project documentation for framework facts.
- Use tracked repository files for implementation claims.
- Treat local policy and last-recorded remote evidence separately.
- Separate tracked definitions, dated remote configuration, recent run results,
  and remote mutation/read-back.
- The exact GitHub secure-use and rulesets URLs, SLSA v1.2, and NIST SP 800-61
  Rev. 3 were re-opened during bounded revalidation. The zizmor 1.27.0
  advisory and 1.28.0 patched release were also verified. This does not
  establish SLSA conformance, NIST adoption, remote enforcement, or runtime
  security posture.
- Do not record secret values, private keys, tokens, shell history, raw secret
  logs, or `.env` values.

## Sources

- [NIST SP 800-218 SSDF Version 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) - SSDF practice-group and secure SDLC criteria.
- [NIST SP 800-218 Rev. 1 Initial Public Draft](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd) - SSDF Version 1.2 draft update caveat.
- [SLSA specification v1.2](https://slsa.dev/spec/v1.2/) - source/build tracks, levels, and attestation criteria.
- [OpenSSF Scorecard](https://scorecard.dev/) - supply-chain security check categories and scoring model.
- [OpenSSF Scorecard checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md) - detailed check criteria for CI, code review, dangerous workflows, dependency update tools, token permissions, and vulnerabilities.
- [zizmor 1.27.0 advisory](https://github.com/zizmorcore/zizmor/security/advisories/GHSA-f42p-wjw5-97qh) - affected-version boundary.
- [zizmor 1.28.0 release](https://github.com/zizmorcore/zizmor/releases/tag/v1.28.0) - patched release evidence.
- `Security governance research` (retiring 2026-07-05 pack, cited without a path because pre-deletion gate 4 admits no clickable link; `security-governance` leaf) - prior secure SDLC and supply-chain reference analysis.
- `Quality CI formatting research` (retiring 2026-07-05 pack, cited without a path because pre-deletion gate 4 admits no clickable link; `quality-ci-formatting` leaf) - QA/CI and secure quality gate criteria.
- Security scope (retired path: `00.agent-governance/scopes/security.md`) - repo-local security and redaction scope.
- [GitHub governance](../../../00.agent-governance/policies/github-governance.md) - workflow security and repository protection policy.
- [Approval boundaries](../../../00.agent-governance/policies/approval-boundaries.md) - protected-surface approval matrix.
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - repo-local CI and workflow-security gates.
- [Dependabot config](../../../../.github/dependabot.yml) - dependency update automation coverage.
- [Security Policy](../../../../.github/SECURITY.md) - repo-local vulnerability reporting boundary.
- Repository contracts (retired path: `scripts/validation/check-repo-contracts.sh`) - workflow action pinning and required quality-gate contract.
- [Security automation readiness](../../data/0078-security-automation-readiness/README.md) - generated repo-local security automation readiness snapshot.
- GitHub Actions control-plane observation (retired path: `data/governance/ref-0071-github-actions-control-plane-observation.yaml`) - latest dated public workflow metadata and authenticated-control boundary.
- Spec 129 - 2026-07-12 read-only remote evidence boundary and later-wave mutation guardrail.

## Maintenance

- **Owner**: Security Reviewer / QA Engineer.
- **Review Cadence**: Review after security policy, CI workflow, Dependabot,
  branch protection, hardening, template/security, release, SBOM, signing, or
  provenance changes.
- **Update Trigger**: Update when the repository adopts new security controls,
  framework mappings, vulnerability gates, attestation workflows, or external
  framework versions.

## Related Documents

- [Audit pack README](../0019-readme/README.md)
- [Implementation overview](../0026-implementation-overview/README.md)
- [SDLC quality formatting implementation](../0030-sdlc-quality-formatting-implementation/README.md)
- [Automation candidates](../0021-automation-candidates/README.md)
- `Security governance research` (retiring 2026-07-05 pack, cited without a path because pre-deletion gate 4 admits no clickable link; `security-governance` leaf)
- [Security automation readiness](../../data/0078-security-automation-readiness/README.md)

## Objective

This package preserves its existing audit evidence under the Stage 99 `audit` contract.

## Criteria

This package preserves its existing audit evidence under the Stage 99 `audit` contract.

## Evidence

This package preserves its existing audit evidence under the Stage 99 `audit` contract.

## Conformance

This package preserves its existing audit evidence under the Stage 99 `audit` contract.

## Actions

This package preserves its existing audit evidence under the Stage 99 `audit` contract.

## Traceability

This package preserves its existing audit evidence under the Stage 99 `audit` contract.
