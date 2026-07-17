---
status: active
artifact_id: reference:agentic-research:security-governance
artifact_type: reference
parent_ids: [spec:123-agentic-engineering-audit-remediation]
reviewed_at: 2026-07-16
review_cycle: on-source-change
---
<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md -->

# Reference: Security Governance for Agentic Workspaces

## Overview

This reference compares tracked security controls and known gaps with current
secure-development, supply-chain, GitHub Actions, and Docker guidance. It keeps
active controls, external reference frameworks, missing implementations, and
human/remote approval boundaries distinct.

## Purpose

Provide reviewable security-governance evidence without adopting a framework,
changing policy or automation, reading secret values, or asserting unverified
remote/runtime enforcement.

## Repository Role

This Stage 90 reference supports Stage 00 security/approval rules, Stage 04
evidence, CI/hardening reviews, and future approved Stage 03/05 work. It does
not replace policy, workflow configuration, incident procedure, or runtime
security truth.

## Scope

### In Scope

- Stage 00 approval/security/QA/operations controls and their ownership
- `.github/SECURITY.md`, CODEOWNERS, tracked workflows, pre-commit, dependency
  audit, hardening/validation scripts, and generated security readiness
- NIST SSDF, OWASP SAMM, SLSA, GitHub Actions secure use, GitHub artifact/SBOM,
  OpenSSF Scorecard, and Docker secret/trust guidance
- Advisory status, risk, recommendation, one canonical owner, and approval
  boundary for every required concern

### Out of Scope

- Formal adoption or maturity certification for NIST SSDF, OWASP SAMM, SLSA,
  or OpenSSF Scorecard
- Secret-value reads, writes, rotation, or output
- Workflow, branch protection, remote GitHub, Compose, runtime, provider,
  credential, model-policy, or incident-state mutation
- Vulnerability, SBOM, signature, attestation, provenance, or Scorecard claims
  not supported by tracked evidence

## Definitions / Facts

- **Active control**: a tracked policy, script, hook, workflow, or generated
  contract that governs or checks current repository work.
- **Reference framework**: external comparison material; it is not adopted by
  appearing in this document.
- **Missing implementation**: no tracked workflow/script control was found for
  the named capability. Research prose is not an implementation.
- **Human/remote approval**: authority required before protected local changes,
  remote mutations, secret operations, model/provider changes, or operational
  execution. Tracked definitions do not prove a human approved or performed an
  action.
- **Tracked provenance snapshot**: registry/image-to-Compose declaration
  evidence. It is not SLSA build provenance, an attestation, or a signature.

## Control Census

The control census was revalidated on `2026-07-16` from tracked files and the
fresh canonical security-automation readiness generator.

| Control surface | Current tracked evidence | Boundary |
| --- | --- | --- |
| Vulnerability reporting | `.github/SECURITY.md` defines private reporting, response targets, remediation, and disclosure. | A tracked policy does not prove an incident exists or that targets were met. |
| Workflow topology | 7 tracked workflows; `ci-quality.yml` has 15 quality job IDs including dependency audit, Compose/hardening/security baselines, pre-commit, and `zizmor`. | Workflow definitions do not prove runs, branch protection, or current remote required-check state. |
| Action pinning | 18/18 tracked external `uses:` references are full 40-character commit SHAs. | Source review and remote action integrity still matter; count is tracked YAML only. |
| Workflow permissions | All 7 workflows declare top-level permissions; defaults are `contents: read` or `{}`, with job-scoped write permission for SARIF where needed. | Live organization/repository Actions settings were not queried. |
| Secret scanning | Pre-commit config includes gitleaks with `.gitleaks.toml`; CI runs pre-commit with documented project-specific skip behavior. | Hook definition does not prove every local commit was scanned. |
| Dependency controls | Dependabot is tracked; CI runs `npm audit --audit-level=high` for `projects/storybook/nextjs`. | This is not a repository-wide multi-ecosystem vulnerability verdict. |
| Container hardening | 11-tier hardening plus template/security and QuickWin baselines are tracked and wired into CI. | Selected rules/exceptions are not host or container certification. |
| Security automation readiness | Canonical scan covered 7 workflows, 29 scripts, and pre-commit: 7 Implemented, 1 Partially Implemented, 5 Gap under its generated schema. | Its `Gap` maps to shared research status `Missing`; it does not run external scanners. |
| Supply-chain generation | No tracked SBOM generator, signing/SLSA attestation command, or OpenSSF Scorecard automation was found. | Absence is limited to tracked workflow/script surfaces scanned by the generator. |
| Declaration provenance | Generated snapshot maps 21 curated registry images to Compose evidence: 20 pinned and 1 approved floating exception. | It explicitly excludes registry lookup, vulnerability scanning, SBOM, signing, and SLSA provenance. |

## External Framework Position

External sources were revalidated on `2026-07-11` and remain reference-only.

| Reference | Supported scope | Workspace caveat |
| --- | --- | --- |
| NIST SP 800-218 SSDF v1.1 | High-level secure-development practices integrable into an SDLC. | No practice/task-to-control adoption or conformity assessment exists here. |
| OWASP SAMM v2 | Five business functions and fifteen security practices for measurable, risk-driven improvement. | No SAMM assessment, target maturity, score, or roadmap was performed. |
| SLSA v1.2 | Approved specification with source/build tracks, incremental levels, attestations, and provenance formats. | No workspace SLSA level is claimed; tracked image declaration provenance is different. |
| GitHub Actions secure use | Least privilege, secret hygiene, untrusted-input caution, full-SHA action pinning, and Scorecard as an advisory signal. | Guidance does not prove organization settings, workflow runs, or remote enforcement. |
| GitHub artifact attestations | Actions can establish build provenance and signed SBOM attestations with explicit permissions and verification. | Availability varies by repository visibility/plan; no tracked attest workflow exists here. |
| GitHub SBOM API | A repository dependency graph can be exported as SPDX-compatible SBOM data. | Remote feature availability/coverage was not queried; export capability is not a tracked release SBOM. |
| OpenSSF Scorecard | Automated heuristics report security-health signals such as token permissions, signed releases, and dangerous workflows. | A score is advisory and detection can be incomplete; no workspace scan or score was produced. |
| Docker Compose secrets/trust | Explicit secrets are mounted only to granted services; Compose files are trusted, host-affecting executable input. | Secret delivery does not prove rotation/host protection, and config inspection does not make untrusted Compose safe. |

## Security Category Ledger

This ledger provides the required comparison fields at category level. The
detailed concern table below adds control and approval-boundary detail.

| Category | Current tracked implementation | External criterion | Status | Gap | Recommendation | Canonical owner | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Secure SDLC governance | Stage 00 security, approval, QA, incident, and documentation contracts route protected work; CI and local checks supply selected verification. | NIST SSDF v1.1 groups practices into Prepare, Protect, Produce, and Respond and is designed to integrate with an existing SDLC. | Partially Implemented | No task/control-level SSDF adoption or conformity map exists. | Use SSDF as a comparison vocabulary until an approved security specification selects practices and evidence. | `docs/00.agent-governance/scopes/security.md` | High |
| Secure build | CI runs project lint/type/build/coverage, a scoped npm vulnerability audit, pre-commit, workflow security, and infrastructure checks. | OWASP SAMM Secure Build calls for repeatable builds, integrated security checks, dependency records, and failure on non-compliance. | Partially Implemented | Coverage is project/control specific; no repository artifact SBOM, broader container/SCA scan, or build provenance exists. | Define artifact/ecosystem scope and exception ownership before adding broader build gates. | `docs/00.agent-governance/scopes/qa.md` | High |
| Secure deployment / CD | Manual approval boundaries and a release-readiness runbook exist; no tracked workflow deploys to an environment or performs promotion/rollback. | OWASP SAMM Secure Deployment calls for documented/repeatable deployment, security milestones, separation of duties, records, integrity checks, and stop/reverse handling. | Missing | CI and changelog verification can be mistaken for CD despite no environment, deployment record, or executable rollback. | Route deployment targets, approvals, promotion, integrity verification, records, and rollback to a later Stage 03/04 contract. | `docs/03.specs/README.md` | High |
| Workflow security | All external actions are SHA pinned; workflows declare top-level permissions; `zizmor` produces SARIF in CI. | GitHub recommends least privilege, untrusted-input controls, full-SHA pinning, OIDC for cloud access, and source review. | Implemented | Remote organization settings, actual token grants, and deployment identities were not queried. | Preserve explicit permissions/pinning and require target-specific OIDC trust design before any deployment. | `docs/00.agent-governance/rules/github-governance.md` | High |
| Dependency and vulnerability response | Dependabot and one high-severity npm audit gate exist; disclosure and incident routing are tracked. | NIST SSDF includes producing secure releases and responding to residual vulnerabilities; OWASP SAMM covers dependency security. | Partially Implemented | No repository-wide multi-ecosystem/container vulnerability verdict or exception lifecycle exists. | Define ecosystems, severity, freshness, exceptions, remediation SLA, and release blocking before expansion. | `docs/00.agent-governance/scopes/qa.md` | High |
| SBOM | No tracked SBOM generator exists in seven workflows, 29 scanned scripts, or pre-commit. | OWASP SAMM Secure Build identifies bills of materials as dependency records; GitHub supports SPDX-compatible dependency-graph export and SBOM attestations. | Missing | Lockfiles and image inventories are not release-artifact SBOMs. | Specify artifact scope, format, generation, retention, publication, verification, and exception policy first. | `docs/03.specs/README.md` | High |
| Provenance, signing, and verification | The generated image declaration snapshot is current, but no signing/SLSA/GitHub attestation producer or verifier is tracked. | SLSA v1.2 Build L1 requires provenance; higher levels strengthen authenticity/tamper resistance, and provenance is useful only when verified against expectations. | Missing | No artifact identity, builder trust, signed provenance, verification policy, or deployment enforcement exists. | Design producer and consumer verification together; do not claim a SLSA level from declaration metadata. | `docs/03.specs/README.md` | High |
| OpenSSF Scorecard | No Scorecard CLI/action is tracked; `zizmor` is a different, workflow-focused scanner. | Scorecard provides heuristic checks such as CI tests, code review, pinned dependencies, token permissions, signed releases, and vulnerabilities. | Missing | No check interpretation, false-positive handling, token scope, publication, or trend owner exists. | Adopt only through an approved advisory/blocking policy with explicit limitations. | `docs/03.specs/README.md` | High |
| Runtime/container controls | Compose secrets, hardening, QuickWin, template baseline, policies, and runbooks cover selected static controls. | Docker treats Compose as trusted host-affecting input and OWASP SAMM separates build/deploy checks from operational evidence. | Partially Implemented | Static checks do not prove host, daemon, network, secret rotation, live health, recovery, migration, backup, or rollback. | Route runtime evidence to scoped Compose/infrastructure follow-ups and keep this task non-mutating. | `docs/00.agent-governance/scopes/security.md` | High |

## Primary Source Revalidation Ledger

| Source owner | Primary source | Published / version | Retrieved | Supported claim | Workspace applicability |
| --- | --- | --- | --- | --- | --- |
| NIST | [SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | February 2022 | 2026-07-11 | Secure-development practices integrate into existing SDLCs and address preparation, protection, production, and vulnerability response. | Comparison only; no formal workspace adoption. |
| NIST | [SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | April 2025 | 2026-07-11 | Incident response belongs across cybersecurity risk management and includes preparation, detection, response, and recovery considerations. | Supports incident/recovery handoff, not proof of exercises. |
| OWASP SAMM | [Secure Build](https://owaspsamm.org/model/implementation/secure-build/) and [Secure Deployment](https://owaspsamm.org/model/implementation/secure-deployment/) | SAMM v2 mutable pages | 2026-07-11 | Repeatable secure builds, dependency controls, documented/automated deployment, security milestones, separation of duties, and secret handling. | Criteria only; no maturity score is claimed. |
| SLSA | [SLSA specification v1.2](https://slsa.dev/spec/v1.2/) and [verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts) | v1.2 Approved | 2026-07-11 | Build/source tracks, provenance levels, attestations, and consumer verification against expectations. | Confirms current missing implementation; no level claim. |
| OpenSSF | [Scorecard](https://github.com/ossf/scorecard) | Mutable official repository | 2026-07-11 | Automated heuristic security checks and their detection limits. | Candidate signal only; no scan or score produced. |
| GitHub | [Secure use](https://docs.github.com/en/actions/reference/security/secure-use) and [deployments/environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) | Mutable product documentation | 2026-07-11 | Least privilege, immutable action refs, OIDC, environment approvals/restrictions/secrets, and deployment protection. | Retrieval-time comparison; remote settings remain unverified. |

## Unresolved Secret-Read Policy Tension

This task records and does not resolve a current policy conflict:

- Owner `docs/00.agent-governance/rules/approval-boundaries.md` states
  unconditionally that secret value files are read-forbidden and lists reading
  a secret value as a Hard Stop.
- Owner `docs/00.agent-governance/scopes/security.md` states that user-approved,
  concrete secret-value reads, writes, or rotations may occur when task evidence
  records the target, redaction boundary, validation, and recovery path, while
  values remain non-output data.

The stricter unconditional ban governed this research pass: no secret value,
private key, token, certificate body, `.env` value, or token-bearing log was
read or emitted. A separate explicitly approved Stage 00/security policy task
must decide the authoritative semantics and synchronize both owning files plus
any affected validators/provider guidance. That follow-up is out of scope here.

## Security Comparison

| Security concern | Workspace control / evidence | External basis | Status | Gap / conflict | Recommendation | Canonical owner | Approval boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Threat boundaries | Security scope requires lightweight threat modeling; approval boundaries protect Compose, secrets, workflows, scripts, runtime, and policy; Docker treats Compose as trusted executable input. | NIST SSDF prepare/protect framing; Docker Compose trust model. | Partially Implemented | No task-wide threat-model artifact or exhaustive transitive Compose privilege review is generated automatically. | Require a scoped threat-boundary record for new/changed services and review resolved Compose before approved execution. | `docs/00.agent-governance/scopes/security.md` | Analysis is local/read-only; any protected-surface or runtime action requires human approval. |
| Least privilege | Security scope requires least privilege; workflows default to read/empty permissions and scope SARIF writes to `zizmor`; hardening checks selected container controls. | NIST SSDF protection practices; GitHub secure-use least-privilege guidance. | Partially Implemented | Static workflow/Compose checks do not prove host users, runtime RBAC/ABAC, repository settings, or every container privilege. | Preserve deny-by-default workflow permissions and expand runtime checks only through approved security specs/tasks. | `docs/00.agent-governance/scopes/security.md` | Permission expansion, workflow edits, and runtime privilege changes require explicit approval. |
| Sandbox and approval | Stage 00 separates protected surfaces, validations, rollback, and operational approval; provider sandbox/approval mechanisms are adapter/runtime-specific. | NIST SSDF protective environments; Docker trusted-input boundary. | Partially Implemented | Tracked files cannot prove the operator's global provider sandbox settings or that every execution path prompts. | Keep repository authority independent of provider prompts and record actual sandbox/approval evidence per high-risk task. | `docs/00.agent-governance/rules/approval-boundaries.md` | Human approval is mandatory for named protected changes; provider approval never broadens it. |
| Secret redaction and policy semantics | Gitleaks, template/security checks, task redaction rules, and metadata-only evidence are active; the two Stage 00 owners conflict on whether approved value reads can ever occur. | GitHub warns automatic redaction is not guaranteed and recommends least privilege, masking, audit, and rotation. | Partially Implemented | `approval-boundaries.md` unconditional ban conflicts with the approved concrete-read protocol in `scopes/security.md`. | Keep the stricter no-read rule now; route a separately approved policy reconciliation that names both owners and retains non-output/redaction guarantees. | `docs/00.agent-governance/rules/approval-boundaries.md` | No value read is authorized by this reference; policy resolution requires explicit user approval. |
| Compose secrets | Root declares 70 IDs; 112/169 service entries and 42/60 root-included entries request secrets; no value was read. | Docker Compose grants declared secrets to named services as mounted files. | Partially Implemented | Declaration does not prove permissions, rotation, Vault-backed flow, live availability, or absence of alternate plaintext channels. | Retain file-based injection and metadata-only validation; verify rotation/recovery only in approved service tasks. | `docs/00.agent-governance/scopes/security.md` | Secret files/values and mapping changes are protected; operational secret work requires concrete approval. |
| Action pinning | 18/18 tracked external workflow `uses:` references use full commit SHAs; repository contracts enforce full-SHA refs. | GitHub calls a full commit SHA the immutable action reference and recommends source verification. | Implemented | Pinning reduces mutable-tag risk but does not audit action source, dependency chain, or compromise. | Keep SHA enforcement and reviewer ownership; review new action source and permission needs before adoption. | `docs/00.agent-governance/rules/github-governance.md` | Any workflow/action change is protected and requires security review/approval. |
| Workflow permissions | All 7 workflows have top-level `permissions`; `ci-quality.yml` defaults to `contents: read`, and only required jobs receive scoped additional rights. | GitHub recommends minimum `GITHUB_TOKEN` permissions and job-level increases only as required. | Implemented | Remote default settings, environment protection, branch enforcement, and actual token grants were not queried. | Maintain explicit top-level defaults, job-scoped writes, and current repo-contract/zizmor checks. | `docs/00.agent-governance/rules/github-governance.md` | Permission expansion or remote setting mutation requires explicit user approval and before/after evidence. |
| Dependency scanning | Dependabot is configured and CI runs high-severity `npm audit` for Storybook Next.js. | OWASP SAMM Secure Build tracks third-party dependency security; NIST SSDF includes vulnerability response. | Partially Implemented | The gate is project/ecosystem scoped; no repository-wide container/image and multi-ecosystem vulnerability result is established. | Define intended ecosystems, severity/exception handling, freshness, and owner before broadening scanning. | `docs/00.agent-governance/scopes/qa.md` | Scanner/workflow changes require approval; current vulnerability state outside the gate remains unknown. |
| Container hardening | Tiered hardening, template/security baseline, QuickWin checks, exception registries, and CI jobs cover selected non-root/capability/mount/health/resource controls. | Docker trust model highlights privilege, capabilities, mounts, network modes, devices, images, and file references. | Partially Implemented | Repository assertions and exceptions are not exhaustive runtime, daemon, kernel, image, or host hardening proof. | Preserve exception ownership and add any new enforced field through approved threat model/spec/task work. | `docs/00.agent-governance/scopes/security.md` | Compose/script/runtime changes and service restarts require separate approvals. |
| SBOM | Canonical readiness scan found no tracked SBOM generation command across 7 workflows, 29 scripts, and pre-commit. | GitHub supports SPDX-compatible dependency-graph export and signed SBOM attestations. | Missing | Dependency lockfiles and image lists are not an artifact SBOM, storage policy, or release evidence. | Approve a Stage 03 supply-chain contract defining artifact scope, format, generation, storage, verification, retention, and exceptions. | `docs/03.specs/README.md` | Adding workflow permissions/tools or publishing SBOMs requires explicit human/remote approval. |
| Signing and attestation | No tracked cosign, SLSA generator, or `actions/attest` command exists in scanned workflow/script surfaces. | SLSA defines attestation/provenance concepts; GitHub Actions can generate and verify build/SBOM attestations. | Missing | No artifact identity, signing authority, keyless/OIDC trust, verification policy, or release integration is defined. | Design signing/attestation together with artifact/release ownership and rollback before implementation. | `docs/03.specs/README.md` | Identity-token/write permissions, trust roots, registry writes, and release changes require explicit approval. |
| Provenance | Generated tech-stack snapshot maps 21 curated images to Compose declarations: 20 pinned and 1 floating exception. | SLSA v1.2 describes build/source provenance and incremental security guarantees. | Partially Implemented | Declaration provenance is not builder identity, materials, immutable build parameters, signed attestation, or SLSA level evidence. | Keep the snapshot accurately labeled; define build provenance only for actual artifact-producing workflows. | `docs/03.specs/README.md` | No SLSA claim or release mutation without approved design, build evidence, and verification. |
| OpenSSF Scorecard | Canonical readiness scan found no Scorecard CLI/action command; `zizmor` covers GitHub workflow risks but is a different tool. | GitHub secure-use cites Scorecard as an advisory workflow/security signal; Scorecard reports heuristic checks. | Missing | No score, check selection, false-positive process, publishing decision, token scope, or trend owner exists. | If maintainers want the signal, first approve advisory-only scope, check interpretation, permissions, and non-blocking/blocking policy. | `docs/03.specs/README.md` | Running/publishing a remote score or adding workflow automation requires user approval. |
| Incident and response handoff | `.github/SECURITY.md` defines private disclosure/response targets; security scope requires incident/postmortem links; ops scope owns live incidents and SEV1/SEV2 postmortems. | NIST SSDF vulnerability-response practices; OWASP SAMM Operations includes Incident Management. | Partially Implemented | Tracked procedures do not prove contact availability, target attainment, exercises, live incident state, or provider-specific incident approval. | Periodically review contact/targets and execute exercises only through approved incident/runbook procedures with redacted evidence. | `docs/05.operations/incidents/README.md` | A human incident commander/provider owner approves live response, disclosure, credential, and remote actions. |
| Model and provider change approval | Stage 00 model/provider protocol requires a concrete model, role, provider, evidence source, coupled adapter/generator/validator updates, Stage 04 evidence, and sync result. | NIST SSDF change-control and integrity framing; external provider catalogs remain mutable evidence. | Implemented | Policy does not prove provider availability, entitlement, remote model behavior, or that a requested change was approved. | Preserve exact-target approval and report unsupported/unverified provider state rather than changing adapters speculatively. | `docs/00.agent-governance/subagent-protocol.md` | User approval is mandatory; this task changed no model policy, provider adapter, or remote state. |

Status totals: **15 concerns — 3 Implemented, 9 Partially Implemented,
3 Missing, 0 Not Applicable**.

## Potential Follow-up / Gap

- Separately approve and resolve the secret-read policy tension; do not resolve
  it through a Stage 90 reference.
- Supply-chain work should start with one Stage 03 contract covering artifact
  scope, SBOM, signing/attestation, provenance verification, Scorecard role,
  permissions, exceptions, retention, and rollback before workflow mutation.
- Reverify remote branch protection, Actions settings, incident contacts, and
  provider/model availability when an approved task needs current remote state.

## Source Rules

- Repo-local claims use tracked files at base `cf8790ca`; Graphify at
  `30df271a` is stale/advisory and not security evidence.
- External sources were retrieved on `2026-07-11`; mutable pages without a
  displayed update date prove retrieval-time guidance only.
- NIST SSDF, OWASP SAMM, SLSA, GitHub, OpenSSF, and Docker material is not
  formally adopted through this reference.
- No secret value, private key, token, certificate body, `.env` value, raw log,
  or shell history is source material.

## Sources

- [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) - high-level secure-development framework, published February 2022
- [OWASP SAMM model](https://owaspsamm.org/model/) - five business functions and fifteen security practices
- [OWASP SAMM Secure Build](https://owaspsamm.org/model/implementation/secure-build/) - repeatable builds, security checks, dependency records, and vulnerability handling
- [OWASP SAMM Secure Deployment](https://owaspsamm.org/model/implementation/secure-deployment/) - deployment documentation/automation, security milestones, separation of duties, and secret handling
- [SLSA v1.2](https://slsa.dev/spec/v1.2/) - approved source/build tracks, levels, attestations, and provenance
- [SLSA artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts) - provenance authenticity and expectation verification
- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) - incident response and recovery integration across cybersecurity risk management
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) - workflow permissions, secrets, untrusted input, pinning, and Scorecard guidance
- [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations) - build/SBOM attestation generation and verification
- [GitHub SBOM API](https://docs.github.com/en/rest/dependency-graph/sboms) - SPDX-compatible dependency-graph export capability
- [OpenSSF Scorecard](https://github.com/ossf/scorecard) - automated heuristic security-health checks and limitations
- [Docker Compose secrets](https://docs.docker.com/compose/how-tos/use-secrets/) - service-granted secret file delivery
- [Docker Compose trust model](https://docs.docker.com/compose/trust-model/) - trusted-input and host-affecting execution boundary
- [Security disclosure](../../../../.github/SECURITY.md) - vulnerability reporting and disclosure expectations
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) - protected surfaces and unconditional secret-read ban
- [Security scope](../../../00.agent-governance/scopes/security.md) - security controls and conflicting approved-secret-work protocol
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md) - workflow and remote-action control owner
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - dependency, Compose, hardening, baseline, pre-commit, and zizmor jobs
- [Pre-commit config](../../../../.pre-commit-config.yaml) - gitleaks and local hook definitions
- [Security readiness snapshot](../../data/security/security-automation-readiness.md) - generated tracked-control/gap census
- [Tech-stack provenance snapshot](../../data/docker/tech-stack-version-provenance.md) - declaration provenance and explicit exclusions
- [Hardening entry point](../../../../scripts/hardening/check-all-hardening.sh) - 11-tier hardening checks

## Maintenance

- **Owner**: Documentation maintainers with Security and QA review
- **Review Cadence**: Review after security/approval policy, workflows,
  hardening, generated readiness, incident ownership, or external framework
  changes
- **Update Trigger**: Recompute tracked controls, keep unknown remote/runtime
  state unknown, and revalidate sources before operational use

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [Docker Compose and infrastructure](./docker-compose-infrastructure.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
- [loop engineering](./loop-engineering.md)
