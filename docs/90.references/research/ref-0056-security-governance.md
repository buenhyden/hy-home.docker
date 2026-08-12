---
status: active
artifact_id: ref-0056
artifact_type: reference
parent_ids: []
observed_at: '2026-07-05'
reviewed_at: 2026-08-07
---

<!-- Target: docs/90.references/research/ref-0056-security-governance.md -->

# Reference: Security Governance for Agentic Workspaces

## Overview

This reference compares tracked security controls and known gaps with current
secure-development, supply-chain, GitHub Actions, and Docker guidance. It keeps
active controls, external reference frameworks, missing implementations, and
human/remote approval boundaries distinct.

The `2026-08-07` revalidation found the largest change in this document's
history. A tracked supply-chain toolchain now exists — syft, grype, cosign, and
OpenSSF Scorecard, all digest-pinned — which moves SBOM generation, signing and
attestation, Scorecard automation, and container vulnerability scanning out of
the _Missing_ class. The correction is not a promotion to production readiness.
Those capabilities exist as a **local, fixture-gated rehearsal contract scoped
to one example service**, and the sections below hold that boundary
deliberately, because the distance between "a cosign command exists in a
tracked script" and "released artifacts are signed and verified" is exactly
where supply-chain claims usually go wrong.

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

The control census was revalidated on `2026-08-07` from tracked files and the
canonical security-automation readiness generator. Four rows changed materially
since `2026-07-27` and are marked below.

| Control surface               | Current tracked evidence                                                                                                                                                                                                                                                | Boundary                                                                                                                                                                                                              |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Vulnerability reporting       | `.github/SECURITY.md` defines private reporting, response targets, remediation, and disclosure.                                                                                                                                                                         | A tracked policy does not prove an incident exists or that targets were met.                                                                                                                                          |
| Workflow topology             | 7 tracked workflows define 23 jobs; `ci-quality.yml` has 16 quality job IDs including supply-chain fixture policy, dependency audit, Compose/hardening/security baselines, pre-commit, and `zizmor`.                                                                    | Workflow definitions do not prove runs, branch protection, or current remote required-check state.                                                                                                                    |
| Action pinning                | **Corrected.** 32/32 resolved external `uses:` references are full 40-character SHAs across 8 distinct actions. Source text holds 17 literal `uses:` lines; the `*checkout` anchor is referenced 15 times in `ci-quality.yml`. The prior 18/18 did not resolve anchors. | Source review and remote action integrity still matter; count is tracked YAML only.                                                                                                                                   |
| Workflow permissions          | All 7 workflows declare top-level permissions; defaults are `contents: read` or `{}`, with job-scoped write permission for SARIF where needed.                                                                                                                          | Live organization/repository Actions settings were not queried.                                                                                                                                                       |
| Secret scanning               | Pre-commit config includes gitleaks with `.gitleaks.toml`; CI runs pre-commit with documented project-specific skip behavior.                                                                                                                                           | Hook definition does not prove every local commit was scanned.                                                                                                                                                        |
| Dependency controls           | Dependabot is tracked; CI runs `npm audit --audit-level=high` for `projects/storybook/nextjs`.                                                                                                                                                                          | This is not a repository-wide multi-ecosystem vulnerability verdict.                                                                                                                                                  |
| Container hardening           | 11-tier hardening plus template/security and QuickWin baselines are tracked and wired into CI.                                                                                                                                                                          | Selected rules/exceptions are not host or container certification.                                                                                                                                                    |
| Security automation readiness | **Corrected.** Canonical scan covered 7 workflows, 36 scripts, and pre-commit: **11 Implemented, 1 Partially Implemented, 1 Gap** across 13 controls. Previously 7/1/5 over 29 scripts.                                                                                 | The generator detects command _presence_ by regex in tracked surfaces. `Implemented` means a command exists, never that it ran, gates CI, or covers releases. Its one `Gap` maps to shared research status `Missing`. |
| Supply-chain generation       | **Corrected.** `scripts/security/verify-sample-service-supply-chain.sh` requires syft, grype, cosign, and scorecard, and `infra/supply-chain.tool-images.json` digest-pins all four. Sibling scripts seed a Grype DB cache and generate a redacted summary.             | Scoped to `examples/sample-web-service`. Local-only, Docker-dependent, and explicitly a rehearsal; no release artifact is produced, signed, or published.                                                             |
| Declaration provenance        | Generated snapshot maps 21 curated registry images to Compose evidence: 20 pinned and 1 approved floating exception.                                                                                                                                                    | It explicitly excludes registry lookup, vulnerability scanning, SBOM, signing, and SLSA provenance.                                                                                                                   |

The latest public remote observation at `2026-07-26T18:22:32+09:00` records
default commit `a897978f`, failed run `29777690571`, and 15 observed jobs; its
root cause is unverified. It also lists three GitHub-managed workflows from
public metadata. Authenticated branch protection, rulesets, environments,
secrets, and variables remain unverified, and no remote setting was mutated.

## Security System, Rules, and Implementation Method

### The system

Security control in this workspace is layered, and each layer has a different
authority and a different failure mode.

| Layer           | Surface                                                                       | Enforces                                                   | Fails by                                                  |
| --------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------- |
| Policy          | `docs/00.agent-governance/scopes/security.md`, `rules/approval-boundaries.md` | What is protected and who may approve                      | Drift between owners; one such conflict is recorded below |
| Pre-commit      | `.gitleaks.toml` + `gitleaks`, `hadolint-docker`, `actionlint`                | Secret patterns and config lint before commit              | Local bypass; scanner blind spots                         |
| CI              | 16 typed gates in `ci-quality.yml`                                            | Workflow security, hardening, baselines, dependency audit  | Not proven required before merge                          |
| Infra hardening | `check-all-hardening.sh`, 11 tiers                                            | Declared container privilege, mounts, secrets, IPs         | Static assertions only; literal image tags drift          |
| Supply chain    | `scripts/security/*`, `infra/supply-chain.*.json`                             | SBOM, vuln scan, signing, Scorecard for one sample service | Local-only, Docker-dependent, one service                 |
| Remote          | branch protection, rulesets, environments                                     | Merge and deployment gating                                | **Unverified** — no authenticated readback                |

### The rules

- **Deny by default in workflows.** All 7 workflows declare top-level
  `permissions`; `ci-quality.yml` defaults to `contents: read` and only the
  `zizmor` job raises scope for SARIF upload. This matches GitHub's documented
  least-privilege recommendation.
- **Immutable action references.** All 32 resolved `uses:` references pin a
  full 40-character SHA, and `.github/workflow-contract.yml` records each
  action's runtime, manifest URL, retrieval date, consumers, and security
  disposition. GitHub's secure-use page states full-SHA pinning is "currently
  the only way to use an action as an immutable release."
- **Secrets are file-mounted, never inlined.** The root Compose file declares
  70 secret IDs; 107 of 168 service entries request them. No value was read in
  producing this document.
- **Approval precedes protected mutation.** Compose, secrets, workflows,
  scripts, runtime, and policy are protected surfaces requiring explicit human
  approval.

### The implementation method for supply chain

This is the newly implemented area and its method deserves precise description,
because the naive reading of "SBOM: Implemented" is wrong.

`scripts/security/verify-sample-service-supply-chain.sh` operates on
`examples/sample-web-service` with four modes:
`--fixture-only` (deterministic, Docker-independent), `--preflight` (checks
daemon, Buildx driver, exact local image IDs), `--advisory` (explicitly "never
pulls images or downloads a vulnerability database"), and
`--scorecard-advisory`. It defines eight typed exit classes — usage, policy,
build, SBOM, vulnerability, provenance, signature, and scorecard — so a failure
names its own category rather than collapsing into exit 1.

Its containment discipline is notable. It sets `umask 077`, creates artifact
directories with mode 700, binds the Grype DB seed read-only, runs the seeding
container with `--pull=never --network none`, and keeps raw artifacts in a
private tree so that only redacted summaries and an accepted-verdict pair reach
the task-owned output directory. Build and runtime materials are pinned by
repository digest, target descriptor digest, and image config ID
simultaneously — three independent identity bindings, not one tag.

What CI actually runs is narrower than what the script can do. The
`supply-chain-fixture-policy` job invokes
`run-ci-gate.py --profile ci --gate ci.supply-chain-fixture-policy`, and the
local profiles register `leaf.supply-chain-deterministic-policy`
(`check-supply-chain-policy.py`) and `leaf.supply-chain-summary-freshness`.
**None of these invokes syft, grype, cosign, or scorecard.** The live tooling
runs only from an operator-initiated local rehearsal. CI verifies the policy
and fixture contract around the rehearsal, not the rehearsal itself.

So the accurate status is: the _capability_ is implemented and carefully
bounded; the _coverage_ is one example service; and the _release integration_
is absent. The generated readiness snapshot agrees, recording that "Local
sample-service image scanning is a separate fixture-policy and
advisory-rehearsal contract, not a live runtime or release claim."

## External Framework Position

The original external framework set was retrieved on `2026-07-11`; selected
mutable GitHub and zizmor evidence was revalidated on `2026-07-27`. All remain
reference-only.

| Reference                    | Supported scope                                                                                                                                                                                                                                                 | Workspace caveat                                                                                                                                                            |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NIST SP 800-218 SSDF v1.1    | High-level secure-development practices integrable into an SDLC.                                                                                                                                                                                                | No practice/task-to-control adoption or conformity assessment exists here.                                                                                                  |
| OWASP SAMM v2                | Five business functions and fifteen security practices for measurable, risk-driven improvement.                                                                                                                                                                 | No SAMM assessment, target maturity, score, or roadmap was performed.                                                                                                       |
| SLSA v1.2                    | Approved specification with source/build tracks, incremental levels, attestations, and provenance formats.                                                                                                                                                      | No workspace SLSA level is claimed; tracked image declaration provenance is different.                                                                                      |
| GitHub Actions secure use    | Least privilege, secret hygiene, untrusted-input caution, full-SHA action pinning, and Scorecard as an advisory signal.                                                                                                                                         | Guidance does not prove organization settings, workflow runs, or remote enforcement.                                                                                        |
| GitHub artifact attestations | The current documentation consolidates generation into `actions/attest@v4` and requires `id-token: write`, `contents: read`, and `attestations: write`, plus `packages: write` for container images and `artifact-metadata: write` for linked-artifact storage. | The page states no SLSA level and no plan or visibility restriction, so the earlier availability caveat is withdrawn as unverified. No tracked attest workflow exists here. |
| GitHub SBOM API              | A repository dependency graph can be exported as SPDX-compatible SBOM data.                                                                                                                                                                                     | Remote feature availability/coverage was not queried; export capability is not a tracked release SBOM.                                                                      |
| OpenSSF Scorecard            | Automated heuristics report security-health signals such as token permissions, signed releases, and dangerous workflows.                                                                                                                                        | A score is advisory and detection can be incomplete; no workspace scan or score was produced.                                                                               |
| Docker Compose secrets/trust | Explicit secrets are mounted only to granted services; Compose files are trusted, host-affecting executable input.                                                                                                                                              | Secret delivery does not prove rotation/host protection, and config inspection does not make untrusted Compose safe.                                                        |

## Security Category Ledger

This ledger provides the required comparison fields at category level. The
detailed concern table below adds control and approval-boundary detail.

| Category                              | Current tracked implementation                                                                                                                                                                                                                    | External criterion                                                                                                                                                                                                         | Status                | Gap                                                                                                                                                 | Recommendation                                                                                                                  | Canonical owner                                               | Confidence |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | ---------- |
| Secure SDLC governance                | Stage 00 security, approval, QA, incident, and documentation contracts route protected work; CI and local checks supply selected verification.                                                                                                    | NIST SSDF v1.1 groups practices into Prepare, Protect, Produce, and Respond and is designed to integrate with an existing SDLC.                                                                                            | Partially Implemented | No task/control-level SSDF adoption or conformity map exists.                                                                                       | Use SSDF as a comparison vocabulary until an approved security specification selects practices and evidence.                    | `docs/00.agent-governance/scopes/security.md`                 | High       |
| Secure build                          | CI runs project lint/type/build/coverage, a scoped npm vulnerability audit, pre-commit, workflow security, and infrastructure checks.                                                                                                             | OWASP SAMM Secure Build calls for repeatable builds, integrated security checks, dependency records, and failure on non-compliance.                                                                                        | Partially Implemented | Coverage is project/control specific; no repository artifact SBOM, broader container/SCA scan, or build provenance exists.                          | Define artifact/ecosystem scope and exception ownership before adding broader build gates.                                      | `docs/00.agent-governance/scopes/qa.md`                       | High       |
| Secure deployment / CD                | Manual approval boundaries and a release-readiness runbook exist; no tracked workflow deploys to an environment or performs promotion/rollback.                                                                                                   | OWASP SAMM Secure Deployment calls for documented/repeatable deployment, security milestones, separation of duties, records, integrity checks, and stop/reverse handling.                                                  | Missing               | CI and changelog verification can be mistaken for CD despite no environment, deployment record, or executable rollback.                             | Route deployment targets, approvals, promotion, integrity verification, records, and rollback to a later Stage 03/04 contract.  | `docs/03.specs/README.md`                                     | High       |
| Workflow security                     | All external actions are SHA pinned; workflows declare top-level permissions; `zizmor==1.28.0` produces SARIF in CI and is patched for the advisory affecting 1.27.0.                                                                             | GitHub recommends least privilege, untrusted-input controls, full-SHA pinning, OIDC for cloud access, and source review.                                                                                                   | Implemented           | Public run metadata does not establish authenticated organization settings, actual token grants, or deployment identities.                          | Preserve explicit permissions/pinning and require target-specific OIDC trust design before any deployment.                      | `docs/00.agent-governance/rules/github-governance.md`         | High       |
| Dependency and vulnerability response | Dependabot and one high-severity npm audit gate exist; disclosure and incident routing are tracked.                                                                                                                                               | NIST SSDF includes producing secure releases and responding to residual vulnerabilities; OWASP SAMM covers dependency security.                                                                                            | Partially Implemented | No repository-wide multi-ecosystem/container vulnerability verdict or exception lifecycle exists.                                                   | Define ecosystems, severity, freshness, exceptions, remediation SLA, and release blocking before expansion.                     | `docs/00.agent-governance/scopes/qa.md`                       | High       |
| SBOM                                  | **Corrected from Missing.** `verify-sample-service-supply-chain.sh` produces and validates a CycloneDX SBOM (`sbom.cdx.json`) bound to source revision, image config digest, and OCI archive SHA-256 for the sample service.                      | OWASP SAMM Secure Build identifies bills of materials as dependency records; GitHub supports SPDX-compatible dependency-graph export and SBOM attestations.                                                                | Partially Implemented | Scope is one example service, local-only, and not produced for any released artifact or infra image. No retention or publication policy exists.     | Extend from the working sample-service method to a defined artifact scope with retention, publication, and verification.        | `docs/03.specs/126-security-supply-chain-remediation/spec.md` | High       |
| Provenance, signing, and verification | **Corrected from Missing.** A cosign producer and verifier now exist for the sample service, with `infra/supply-chain.cosign-offline-signing-config.json` and an offline trusted root; the generated image declaration snapshot remains separate. | SLSA v1.2 Build L1 requires provenance; higher levels strengthen authenticity/tamper resistance, and provenance is useful only when verified against expectations.                                                         | Partially Implemented | Offline rehearsal trust root, one service, no release integration, no deployment-time verification enforcement. No SLSA level is claimed or earned. | Promote the offline trust root to a real signing authority only with an approved key-management and verification-policy design. | `docs/03.specs/126-security-supply-chain-remediation/spec.md` | High       |
| OpenSSF Scorecard                     | **Corrected from Missing.** Scorecard is digest-pinned in `infra/supply-chain.tool-images.json` and reachable through the `--scorecard-advisory` mode with a dedicated exit class.                                                                | Scorecard publishes 23 heuristic checks including Branch-Protection, Token-Permissions, Pinned-Dependencies, and Signed-Releases, and states that its checks are heuristics with both false positives and false negatives. | Partially Implemented | Advisory rehearsal only. No score is produced, published, tracked over time, or interpreted by a named owner, and no threshold is defined.          | Decide advisory-versus-blocking policy, check selection, and false-positive handling before any score is treated as evidence.   | `docs/03.specs/126-security-supply-chain-remediation/spec.md` | High       |
| Runtime/container controls            | Compose secrets, hardening, QuickWin, template baseline, policies, and runbooks cover selected static controls.                                                                                                                                   | Docker treats Compose as trusted host-affecting input and OWASP SAMM separates build/deploy checks from operational evidence.                                                                                              | Partially Implemented | Static checks do not prove host, daemon, network, secret rotation, live health, recovery, migration, backup, or rollback.                           | Route runtime evidence to scoped Compose/infrastructure follow-ups and keep this task non-mutating.                             | `docs/00.agent-governance/scopes/security.md`                 | High       |

## Primary Source Revalidation Ledger

| Source owner | Primary source                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Published / version                                                                                            | Retrieved  | Supported claim                                                                                                                                                                                                                                                                                                                      | Workspace applicability                                                                                                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NIST         | [SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final)                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | February 2022                                                                                                  | 2026-07-11 | Secure-development practices integrate into existing SDLCs and address preparation, protection, production, and vulnerability response.                                                                                                                                                                                              | Comparison only; no formal workspace adoption.                                                                                                                                          |
| NIST         | [SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | April 2025                                                                                                     | 2026-07-11 | Incident response belongs across cybersecurity risk management and includes preparation, detection, response, and recovery considerations.                                                                                                                                                                                           | Supports incident/recovery handoff, not proof of exercises.                                                                                                                             |
| OWASP SAMM   | [Secure Build](https://owaspsamm.org/model/implementation/secure-build/) and [Secure Deployment](https://owaspsamm.org/model/implementation/secure-deployment/)                                                                                                                                                                                                                                                                                                                                                                                  | SAMM v2 mutable pages                                                                                          | 2026-07-11 | Repeatable secure builds, dependency controls, documented/automated deployment, security milestones, separation of duties, and secret handling.                                                                                                                                                                                      | Criteria only; no maturity score is claimed.                                                                                                                                            |
| SLSA         | [SLSA specification v1.2](https://slsa.dev/spec/v1.2/) and [verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts)                                                                                                                                                                                                                                                                                                                                                                                                                 | v1.2, status Approved, re-confirmed on page                                                                    | 2026-08-07 | Build and Source tracks, provenance levels, attestations, and consumer verification against expectations.                                                                                                                                                                                                                            | The workspace now has a local signing rehearsal but still claims no SLSA level; provenance without enforced verification earns none.                                                    |
| OpenSSF      | [Scorecard](https://github.com/ossf/scorecard)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Mutable official repository                                                                                    | 2026-08-07 | 23 documented checks including Branch-Protection, Token-Permissions, Pinned-Dependencies, and Signed-Releases; the project states its checks are heuristics with false positives and negatives and rejects aggregate-score interpretation.                                                                                           | Tool is now digest-pinned and reachable in advisory mode; still no scan, score, or owner.                                                                                               |
| GitHub       | [Secure use](https://docs.github.com/en/actions/reference/security/secure-use), [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations), [SBOM API](https://docs.github.com/en/rest/dependency-graph/sboms), and [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) | Mutable product documentation, no visible last-updated dates; SBOM API version `2026-03-10`                    | 2026-08-07 | Least privilege and job-level permission override; full-SHA pinning as the only immutable action reference; redaction relying on exact match; `actions/attest@v4` with its required permission set; three SBOM endpoints with one-week report retention; rulesets aggregating with classic protection under a most-restrictive rule. | Retrieval-time comparison; authenticated remote settings remain unverified.                                                                                                             |
| zizmor       | [Advisory index](https://github.com/zizmorcore/zizmor/security/advisories) and [GHSA-f42p-wjw5-97qh](https://github.com/zizmorcore/zizmor/security/advisories/GHSA-f42p-wjw5-97qh)                                                                                                                                                                                                                                                                                                                                                               | One published advisory total, dated 2026-07-21; 1.27.0 affected and 1.28.0 patched per the earlier direct read | 2026-08-07 | The advisory index still lists exactly one advisory. The tracked pin remains `zizmor==1.28.0`, now located at `scripts/validation/ci_gate_adapters.py:1010` rather than inline in workflow YAML.                                                                                                                                     | **Partially re-verified.** The index page does not render affected version ranges, so the 1.27.0-only boundary is carried forward and not independently re-confirmed at this retrieval. |

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

| Security concern                      | Workspace control / evidence                                                                                                                                                                                                                                           | External basis                                                                                                                                                                                                                                                                                                                | Status                | Gap / conflict                                                                                                                                   | Recommendation                                                                                                                                            | Canonical owner                                               | Approval boundary                                                                                              |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Threat boundaries                     | Security scope requires lightweight threat modeling; approval boundaries protect Compose, secrets, workflows, scripts, runtime, and policy; Docker treats Compose as trusted executable input.                                                                         | NIST SSDF prepare/protect framing; Docker Compose trust model.                                                                                                                                                                                                                                                                | Partially Implemented | No task-wide threat-model artifact or exhaustive transitive Compose privilege review is generated automatically.                                 | Require a scoped threat-boundary record for new/changed services and review resolved Compose before approved execution.                                   | `docs/00.agent-governance/scopes/security.md`                 | Analysis is local/read-only; any protected-surface or runtime action requires human approval.                  |
| Least privilege                       | Security scope requires least privilege; workflows default to read/empty permissions and scope SARIF writes to `zizmor`; hardening checks selected container controls.                                                                                                 | NIST SSDF protection practices; GitHub secure-use least-privilege guidance.                                                                                                                                                                                                                                                   | Partially Implemented | Static workflow/Compose checks do not prove host users, runtime RBAC/ABAC, repository settings, or every container privilege.                    | Preserve deny-by-default workflow permissions and expand runtime checks only through approved security specs/tasks.                                       | `docs/00.agent-governance/scopes/security.md`                 | Permission expansion, workflow edits, and runtime privilege changes require explicit approval.                 |
| Sandbox and approval                  | Stage 00 separates protected surfaces, validations, rollback, and operational approval; provider sandbox/approval mechanisms are adapter/runtime-specific.                                                                                                             | NIST SSDF protective environments; Docker trusted-input boundary.                                                                                                                                                                                                                                                             | Partially Implemented | Tracked files cannot prove the operator's global provider sandbox settings or that every execution path prompts.                                 | Keep repository authority independent of provider prompts and record actual sandbox/approval evidence per high-risk task.                                 | `docs/00.agent-governance/rules/approval-boundaries.md`       | Human approval is mandatory for named protected changes; provider approval never broadens it.                  |
| Secret redaction and policy semantics | Gitleaks, template/security checks, task redaction rules, and metadata-only evidence are active; the two Stage 00 owners conflict on whether approved value reads can ever occur.                                                                                      | GitHub warns automatic redaction is not guaranteed and recommends least privilege, masking, audit, and rotation.                                                                                                                                                                                                              | Partially Implemented | `approval-boundaries.md` unconditional ban conflicts with the approved concrete-read protocol in `scopes/security.md`.                           | Keep the stricter no-read rule now; route a separately approved policy reconciliation that names both owners and retains non-output/redaction guarantees. | `docs/00.agent-governance/rules/approval-boundaries.md`       | No value read is authorized by this reference; policy resolution requires explicit user approval.              |
| Compose secrets                       | Root declares 70 IDs; 107/168 service entries and 42/60 root-included entries request secrets; no value was read. Corrected from 111 on `2026-08-07`.                                                                                                                  | Docker Compose grants declared secrets to named services as mounted files.                                                                                                                                                                                                                                                    | Partially Implemented | Declaration does not prove permissions, rotation, Vault-backed flow, live availability, or absence of alternate plaintext channels.              | Retain file-based injection and metadata-only validation; verify rotation/recovery only in approved service tasks.                                        | `docs/00.agent-governance/scopes/security.md`                 | Secret files/values and mapping changes are protected; operational secret work requires concrete approval.     |
| Action pinning                        | 32/32 resolved external workflow `uses:` references use full commit SHAs across 8 distinct actions; repository contracts enforce full-SHA refs, and `.github/workflow-contract.yml` records each action's SHA, runtime, manifest URL, retrieval date, and disposition. | GitHub calls a full commit SHA the immutable action reference and recommends source verification.                                                                                                                                                                                                                             | Implemented           | Pinning reduces mutable-tag risk but does not audit action source, dependency chain, or compromise.                                              | Keep SHA enforcement and reviewer ownership; review new action source and permission needs before adoption.                                               | `docs/00.agent-governance/rules/github-governance.md`         | Any workflow/action change is protected and requires security review/approval.                                 |
| Workflow permissions                  | All 7 workflows have top-level `permissions`; `ci-quality.yml` defaults to `contents: read`, and only required jobs receive scoped additional rights.                                                                                                                  | GitHub recommends minimum `GITHUB_TOKEN` permissions and job-level increases only as required.                                                                                                                                                                                                                                | Implemented           | Public metadata does not establish authenticated default settings, environment protection, branch enforcement, or actual token grants.           | Maintain explicit top-level defaults, job-scoped writes, and current repo-contract/zizmor checks.                                                         | `docs/00.agent-governance/rules/github-governance.md`         | Permission expansion or remote setting mutation requires explicit user approval and before/after evidence.     |
| Dependency scanning                   | Dependabot is configured and CI runs high-severity `npm audit` for Storybook Next.js.                                                                                                                                                                                  | OWASP SAMM Secure Build tracks third-party dependency security; NIST SSDF includes vulnerability response.                                                                                                                                                                                                                    | Partially Implemented | The gate is project/ecosystem scoped; no repository-wide container/image and multi-ecosystem vulnerability result is established.                | Define intended ecosystems, severity/exception handling, freshness, and owner before broadening scanning.                                                 | `docs/00.agent-governance/scopes/qa.md`                       | Scanner/workflow changes require approval; current vulnerability state outside the gate remains unknown.       |
| Container hardening                   | Tiered hardening, template/security baseline, QuickWin checks, exception registries, and CI jobs cover selected non-root/capability/mount/health/resource controls.                                                                                                    | Docker trust model highlights privilege, capabilities, mounts, network modes, devices, images, and file references.                                                                                                                                                                                                           | Partially Implemented | Repository assertions and exceptions are not exhaustive runtime, daemon, kernel, image, or host hardening proof.                                 | Preserve exception ownership and add any new enforced field through approved threat model/spec/task work.                                                 | `docs/00.agent-governance/scopes/security.md`                 | Compose/script/runtime changes and service restarts require separate approvals.                                |
| SBOM                                  | Canonical readiness scan across 7 workflows, 36 scripts, and pre-commit now finds an SBOM generation command. syft is digest-pinned and the sample-service script emits and subject-binds `sbom.cdx.json`.                                                             | GitHub supports SPDX-compatible dependency-graph export via three REST endpoints at API version `2026-03-10`, with generated reports retained up to one week, plus signed SBOM attestations.                                                                                                                                  | Partially Implemented | One example service, local-only. Dependency lockfiles and infra image lists still have no SBOM, storage policy, or release evidence.             | Extend the proven sample-service method to a defined artifact scope with storage, verification, retention, and exceptions.                                | `docs/03.specs/126-security-supply-chain-remediation/spec.md` | Adding workflow permissions/tools or publishing SBOMs requires explicit human/remote approval.                 |
| Signing and attestation               | cosign is digest-pinned and exercised for the sample service with an offline signing config and trusted root; dedicated `EXIT_SIGNATURE` and `EXIT_PROVENANCE` classes separate the two failure modes. No `actions/attest` usage exists in any workflow.               | SLSA v1.2 is an Approved specification with Build and Source tracks; GitHub Actions generates and verifies build/SBOM attestations through `actions/attest@v4`, requiring `id-token: write`, `contents: read`, and `attestations: write`, plus `packages: write` for container images. The GitHub page asserts no SLSA level. | Partially Implemented | Offline trust root, one service, no CI integration, no release attestation, no deployment-time verification.                                     | Design the real trust root, key management, and consumer verification together before promoting the rehearsal.                                            | `docs/03.specs/126-security-supply-chain-remediation/spec.md` | Identity-token/write permissions, trust roots, registry writes, and release changes require explicit approval. |
| Provenance                            | Generated tech-stack snapshot maps 21 curated images to Compose declarations: 20 pinned and 1 floating exception.                                                                                                                                                      | SLSA v1.2 describes build/source provenance and incremental security guarantees.                                                                                                                                                                                                                                              | Partially Implemented | Declaration provenance is not builder identity, materials, immutable build parameters, signed attestation, or SLSA level evidence.               | Keep the snapshot accurately labeled; define build provenance only for actual artifact-producing workflows.                                               | `docs/03.specs/README.md`                                     | No SLSA claim or release mutation without approved design, build evidence, and verification.                   |
| OpenSSF Scorecard                     | Scorecard is digest-pinned in the tool registry and reachable through `--scorecard-advisory` with its own `EXIT_SCORECARD` class; `zizmor` remains a different, workflow-focused tool.                                                                                 | GitHub secure-use cites Scorecard as an advisory signal; Scorecard publishes 23 heuristic checks and states its checks produce both false positives and false negatives.                                                                                                                                                      | Partially Implemented | No score is produced, published, tracked, or interpreted; no check selection, false-positive process, token scope, or trend owner exists.        | Approve advisory-only scope, check interpretation, permissions, and non-blocking/blocking policy before treating any score as evidence.                   | `docs/03.specs/126-security-supply-chain-remediation/spec.md` | Running/publishing a remote score or adding workflow automation requires user approval.                        |
| Incident and response handoff         | `.github/SECURITY.md` defines private disclosure/response targets; security scope requires incident/postmortem links; ops scope owns live incidents and SEV1/SEV2 postmortems.                                                                                         | NIST SSDF vulnerability-response practices; OWASP SAMM Operations includes Incident Management.                                                                                                                                                                                                                               | Partially Implemented | Tracked procedures do not prove contact availability, target attainment, exercises, live incident state, or provider-specific incident approval. | Periodically review contact/targets and execute exercises only through approved incident/runbook procedures with redacted evidence.                       | `docs/05.operations/incidents/README.md`                      | A human incident commander/provider owner approves live response, disclosure, credential, and remote actions.  |
| Model and provider change approval    | Stage 00 model/provider protocol requires a concrete model, role, provider, evidence source, coupled adapter/generator/validator updates, Stage 04 evidence, and sync result.                                                                                          | NIST SSDF change-control and integrity framing; external provider catalogs remain mutable evidence.                                                                                                                                                                                                                           | Implemented           | Policy does not prove provider availability, entitlement, remote model behavior, or that a requested change was approved.                        | Preserve exact-target approval and report unsupported/unverified provider state rather than changing adapters speculatively.                              | `docs/00.agent-governance/subagent-protocol.md`               | User approval is mandatory; this task changed no model policy, provider adapter, or remote state.              |

Status totals after the `2026-08-07` corrections: **15 concerns — 3
Implemented, 12 Partially Implemented, 0 Missing, 0 Not Applicable**. The three
formerly Missing concerns (SBOM, signing and attestation, Scorecard) each moved
to Partially Implemented because a bounded local capability now exists. None
moved to Implemented, because none covers a released artifact.

## Potential Follow-up / Gap

- Separately approve and resolve the secret-read policy tension; do not resolve
  it through a Stage 90 reference.
- Supply-chain work is now underway rather than absent, so the follow-up
  changes shape. The remaining questions are scope and integration, not
  capability: which artifacts beyond `examples/sample-web-service` are in
  scope, whether the offline cosign trust root is promoted to a real signing
  authority and under what key management, whether any of syft/grype/cosign
  runs in CI rather than only in an operator-initiated local rehearsal, and
  what consumer-side verification would enforce provenance at deployment.
  Spec 126 is the tracked owner.
- Broad dependency SCA (`SEC-AUTO-012`) is the one remaining generated `Gap`.
  The scoped Storybook npm audit does not satisfy it, and the sample-service
  Grype path covers container images for one service rather than repository
  dependencies across ecosystems.
- Treat the generated readiness snapshot's `Implemented` verdicts as
  command-presence detection, not coverage. Four controls flipped to
  `Implemented` on the strength of regex matches against tracked scripts; this
  reference deliberately records them as Partially Implemented instead.
- Obtain authenticated branch protection, ruleset, environment, and Actions
  settings only when an approved task needs current remote control state;
  preserve the dated public failed-run observation separately.

## Source Rules

- Repo-local claims were re-derived on `2026-08-07` from tracked files and the
  canonical readiness generator; Graphify is advisory and not security evidence.
- Action-pinning counts resolve YAML anchors through a parser. Raw `grep` on
  `uses:` undercounts by 15 in `ci-quality.yml` because of the `*checkout`
  anchor, which is how the superseded 18/18 figure arose.
- External framework sources retain their original retrieval dates; selected
  mutable GitHub and zizmor sources were revalidated on `2026-07-27` and prove
  retrieval-time guidance only.
- The exact official GitHub secure-use, monitoring, and rulesets pages plus the
  zizmor advisory and patched release were re-opened on `2026-07-27`.
  Repository controls do not establish a SLSA level, formal NIST adoption,
  remote enforcement, or runtime/container posture.
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
- [zizmor 1.27.0 advisory](https://github.com/zizmorcore/zizmor/security/advisories/GHSA-f42p-wjw5-97qh) - affected-version boundary
- [zizmor 1.28.0 release](https://github.com/zizmorcore/zizmor/releases/tag/v1.28.0) - patched release evidence
- [OpenSSF Scorecard](https://github.com/ossf/scorecard) - automated heuristic security-health checks and limitations
- [Docker Compose secrets](https://docs.docker.com/compose/how-tos/use-secrets/) - service-granted secret file delivery
- [Docker Compose trust model](https://docs.docker.com/compose/trust-model/) - trusted-input and host-affecting execution boundary
- [Security disclosure](../../../.github/SECURITY.md) - vulnerability reporting and disclosure expectations
- [Approval boundaries](../../00.agent-governance/rules/approval-boundaries.md) - protected surfaces and unconditional secret-read ban
- [Security scope](../../00.agent-governance/scopes/security.md) - security controls and conflicting approved-secret-work protocol
- [GitHub governance](../../00.agent-governance/rules/github-governance.md) - workflow and remote-action control owner
- [CI quality workflow](../../../.github/workflows/ci-quality.yml) - dependency, Compose, hardening, baseline, pre-commit, and zizmor jobs
- [Pre-commit config](../../../.pre-commit-config.yaml) - gitleaks and local hook definitions
- [Security readiness snapshot](../data/security/ref-0078-security-automation-readiness.md) - generated tracked-control/gap census
- [GitHub Actions control-plane observation](../data/governance/ref-0071-github-actions-control-plane-observation.yaml) - dated public run/workflow metadata and authenticated-control boundary
- [Tech-stack provenance snapshot](../data/docker/ref-0061-tech-stack-version-provenance.md) - declaration provenance and explicit exclusions
- [Hardening entry point](../../../scripts/hardening/check-all-hardening.sh) - 11-tier hardening checks
- [Supply-chain verification rehearsal](../../../scripts/security/verify-sample-service-supply-chain.sh) - syft, grype, cosign, and scorecard rehearsal with eight typed exit classes
- [Supply-chain tool registry](../../../infra/supply-chain.tool-images.json) - digest-pinned tool identities
- [Cosign offline signing config](../../../infra/supply-chain.cosign-offline-signing-config.json) and [offline trusted root](../../../infra/supply-chain.cosign-offline-trusted-root.json) - offline rehearsal trust material
- [Sample service policy](../../../infra/supply-chain.sample-service-policy.json) - scoped policy for the one rehearsed service
- [Typed workflow contract](../../../.github/workflow-contract.yml) - per-action SHA, runtime, manifest URL, retrieval date, and security disposition
- [Main branch protection proposal](../../../.github/rulesets/main-protection.md) - tracked required-check proposal recording verification as unverified
- [Scorecard checks](https://github.com/ossf/scorecard) - 23 heuristic checks and stated detection limits

## Maintenance

- **Owner**: Documentation maintainers with Security and QA review
- **Review Cadence**: Review after security/approval policy, workflows,
  hardening, generated readiness, incident ownership, or external framework
  changes
- **Update Trigger**: Recompute tracked controls, keep unknown remote/runtime
  state unknown, and revalidate sources before operational use

## Related Documents

- [research pack index](ref-0039-readme.md)
- [workspace baseline](ref-0058-workspace-baseline.md)
- [Docker Compose and infrastructure](ref-0044-docker-compose-infrastructure.md)
- [quality, CI, and formatting](ref-0053-quality-ci-formatting.md)
- [github actions platform](ref-0084-github-actions-platform.md)
- [loop engineering](ref-0049-loop-engineering.md)
