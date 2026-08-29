---
status: active
artifact_id: reference:agentic-engineering-research:security-governance
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Security Governance

## Overview

This leaf presents retained secure-SDLC and supply-chain material as an
advisory layered governance model. It does not certify the workspace, report a
vulnerability posture, establish remote enforcement, or replace a security
owner's risk decision.

## Purpose

Connect lifecycle, pipeline, provenance, verification, and disclosure concerns
to precise workspace investigation targets while preserving the difference
between a declared control, an executed check, a hosted result, and accepted
residual risk.

## Scope

The review uses only retained observations and read-only tracked declarations
at literal base `af8de6583ac3bc14bcc8fbe5c3a8a37b3b7fdf1a`. It excludes secret
values, live repositories, branch settings, scanner execution, image builds,
signature verification, hosted CI, incidents, and any claim of compliance or
release approval.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `SG-001` | Retained SSDF 1.1, CSF 2.0, and SAMM 2.0 observations provide complementary secure-development, risk-governance, and maturity-practice framing. | retained official observation | HISTORICAL VERIFIED | retained Task 0001 security ledger | Apply a framework only after mapping a named practice to an accountable local owner, evidence, and residual-risk decision; framework availability is not adoption. |
| `SG-002` | Retained SLSA v1.2 and pinned OpenSSF Scorecard observations describe supply-chain provenance and assessment concepts, not a local SLSA level or Scorecard result. | retained official observation | HISTORICAL VERIFIED | `.github/workflow-contract.yml`, `.github/workflows/`, and future build evidence | Before claiming a supply-chain property, identify the artifact, builder, materials, provenance, and verifier evidence. |
| `SG-003` | Retained OWASP CI/CD, SLSA build-provenance, and Sigstore Cosign observations support layered review of pipeline risks, provenance fields, and signature verification mechanisms. | retained official observation | HISTORICAL VERIFIED | `.github/workflow-contract.yml`, `.github/workflows/`, and a future artifact verification record | A future adoption must bind each claimed risk control to an exact pipeline or artifact and an observed result. |
| `SG-004` | Tracked security policy, workflow contract, and secret-scanning configuration are local declarations whose effective enforcement and operational attainment remain unobserved. | tracked configuration | VERIFIED | `.github/SECURITY.md`, `.github/workflow-contract.yml`, `.gitleaks.toml` at `af8de6583ac3bc14bcc8fbe5c3a8a37b3b7fdf1a` | Keep disclosure, workflow, and scanning evidence separate from hosted enforcement, incident handling, and certification claims. |

### Layered adoption model

SSDF supplies prepare/protect/produce/respond practice framing; CSF supplies
outcome-based risk governance without prescribing an implementation; SAMM
organizes five business functions and fifteen practices. These purposes are
complementary rather than competing compliance labels. Use a layered sequence:
define assets and risk ownership; map those expectations to development and
review controls; constrain pipeline identity and permissions; capture build
provenance where an artifact exists; verify signatures or attestations against
an explicit trust decision; and retain a named exception or residual-risk
decision. Each layer needs its own target, evidence, and owner. A scanner
definition, a YAML permission, or a policy file cannot substitute for an
observed control outcome.

Retained SLSA provenance describes `buildDefinition` (including build type,
parameters, and resolved dependencies) and `runDetails` (including
`builder.id`, version, metadata, and byproducts). Retained Cosign guidance
distinguishes three checks: signature over the artifact digest, signer
identity/certificate and trust root as applicable, and the payload digest's
match to the artifact. Neither mechanism proves that an artifact is
vulnerability-free, that every signer is appropriate, or that application code
is correct. OWASP CI/CD risks provide a review taxonomy: map a named flow,
identity, dependency, execution, access, credential, configuration,
third-party, integrity, or visibility risk to a specific local control and
its evidence rather than infer that the category is closed.

| Subitem | Exact local investigation target | Adoption condition | Verification limit |
| --- | --- | --- | --- |
| Secure-SDLC governance | `docs/03.specs/`, Task 0004, and named owner records | Map SSDF/CSF/SAMM practice to an accountable control and residual-risk owner. | A framework/source mapping is not conformance or an accepted risk. |
| Pipeline identity and access | `.github/workflow-contract.yml` and `.github/workflows/*.yml` | Identify the workflow, trigger, principal, permission, and protected target. | YAML does not prove hosted enforcement or effective credentials. |
| Dependency and third-party risk | `.github/workflow-contract.yml`, workflow `uses:` entries, and dependency manifests | Bind an OWASP CI/CD category to a declared control and a result. | A registered or pinned reference is not an executed or sufficient control. |
| Provenance | a named build workflow and its future artifact/provenance record | Require expected builder, inputs, artifact, and verifier criteria before a provenance claim. | No local provenance predicate or artifact verification was observed. |
| Signature verification | a named artifact digest, verification policy, and future Cosign result | Set the expected identity, issuer/trust root, and digest before verification. | No signature, certificate, trust root, or verification result was inspected. |
| Disclosure and scanning | `.github/SECURITY.md` and `.gitleaks.toml` | Assign report, triage, remediation, and scan-result ownership. | Policy/configuration does not prove response exercise or secret absence. |

No retained source establishes that this workspace meets SSDF, CSF, SAMM, SLSA,
Scorecard, OWASP CI/CD, or Sigstore requirements. No OCI Image Specification
observation was retained for this draft; any OCI-specific proposition is
`UNVERIFIED` until separately sourced and reviewed.

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SG-SRC-001` | `SG-001` | SP 800-218 SSDF 1.1 / NIST | [SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | retained fixed publication | [dated security leaf, source row 355](../2026-08-08-agentic-engineering-research-pack/security-governance.md#sources) | 2026-08-08T18:18:06+09:00 | Comparison framing only; it proves neither local implementation nor conformance. |
| `SG-SRC-002` | `SG-001` | Cybersecurity Framework 2.0 / NIST | [CSF 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) | retained official observation | [dated security leaf, source row 356](../2026-08-08-agentic-engineering-research-pack/security-governance.md#sources) | 2026-08-08T18:18:06+09:00 | Risk framework observation only; no local outcome is inferred. |
| `SG-SRC-003` | `SG-001` | SAMM 2.0 model / OWASP | [SAMM model](https://owaspsamm.org/model/) | retained official observation | [dated security leaf, source row 357](../2026-08-08-agentic-engineering-research-pack/security-governance.md#sources) | 2026-08-08T18:18:06+09:00 | Maturity-practice framing is not a maturity assessment. |
| `SG-SRC-004` | `SG-002` | SLSA v1.2 specification / SLSA | [SLSA v1.2](https://slsa.dev/spec/v1.2/) | retained fixed publication | [dated security leaf, source row 358](../2026-08-08-agentic-engineering-research-pack/security-governance.md#sources) | 2026-08-08T18:18:06+09:00 | No local SLSA level, provenance, or builder result is asserted. |
| `SG-SRC-005` | `SG-002` | Scorecard pinned revision / OpenSSF | [commit `40c1e359`](https://github.com/ossf/scorecard/commit/40c1e35996730d4fdcbdb2e6a23917a2467e29b7) | retained pinned observation | [dated security leaf, source row 360](../2026-08-08-agentic-engineering-research-pack/security-governance.md#sources); `40c1e35996730d4fdcbdb2e6a23917a2467e29b7` | 2026-08-08T18:18:06+09:00 | The pin supports a retained tool-source observation, not a repository score. |
| `SG-SRC-006` | `SG-003` | Top 10 CI/CD Security Risks / OWASP | [OWASP CI/CD risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/) | retained fixed publication | [dated security leaf, source row 372](../2026-08-08-agentic-engineering-research-pack/security-governance.md#sources) | 2026-08-14 | Risk taxonomy only; no category is declared closed locally. |
| `SG-SRC-007` | `SG-003` | Build provenance v1.2 / SLSA | [build provenance](https://slsa.dev/spec/v1.2/build-provenance) | retained fixed publication | [dated security leaf, source row 373](../2026-08-08-agentic-engineering-research-pack/security-governance.md#sources) | 2026-08-14 | Describes retained predicate structure; no local provenance is observed. |
| `SG-SRC-008` | `SG-003` | Verification / Sigstore | [Cosign verification](https://docs.sigstore.dev/cosign/verifying/verify/) | retained official observation | [dated security leaf, source row 374](../2026-08-08-agentic-engineering-research-pack/security-governance.md#sources) | 2026-08-14 | Mechanism observation only; no signature, certificate, digest, or trust decision was inspected. |
| `SG-SRC-009` | `SG-004` | Security, workflow, and secret-scan declarations / workspace | [.github/SECURITY.md](../../../../.github/SECURITY.md), [.github/workflow-contract.yml](../../../../.github/workflow-contract.yml), [.gitleaks.toml](../../../../.gitleaks.toml) | tracked configuration | `af8de6583ac3bc14bcc8fbe5c3a8a37b3b7fdf1a` | 2026-08-28 | Configuration does not prove an executed scan, hosted enforcement, incident response, or secret absence. |

## Maintenance

Remeasure the named tracked declarations after a security-policy, workflow,
secret-scanning, build, artifact, or ownership change. Reopen mutable and
versioned external sources only under authorized source access. Preserve exact
artifact, trust, command, result, exception, and decision evidence before
upgrading any declared control to an execution or assurance claim.

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | An agent action has an explicit permission, evidence, and escalation boundary. | Inspect task and tool contract. | A prompt or task is not policy enforcement. |
| architecture | applies | Threat, trust, and recovery boundaries have a named decision owner. | Inspect architecture decision and risk record. | No threat model or acceptance is created. |
| common | applies | Shared controls define owner, exception path, and scope-specific evidence. | Inspect declared control and owner mapping. | Reuse does not prove consistent enforcement. |
| docs | applies | Security statements preserve source state, caveat, and evidence class. | Inspect claim/source traceability. | Documentation cannot certify security. |
| infra | applies | Infrastructure controls bind a service or artifact to an accountable operator. | Inspect exact Compose/build declaration and approval. | No runtime, image, or registry observation exists. |
| ops | applies | Disclosure, incident, rollback, and recovery have approved operational evidence. | Inspect policy/runbook and event record. | A policy declaration is not an exercised response. |
| qa | applies | A security check states its threat class, target, oracle, and result. | Record exact scanner/test evidence. | Configured scanning is not a clean result. |
| security | applies | A risk acceptance names asset, control, residual risk, owner, and review date. | Inspect signed or approved decision evidence. | No acceptance, compliance, or certification is claimed. |

## Related Documents

- [Docker Compose Infrastructure](./docker-compose-infrastructure.md)
- [Automation Pipeline Workflow](./automation-pipeline-workflow.md)
- [Quality CI and Formatting](./quality-ci-formatting.md)
- [Verification and Validation](./verification-validation.md)
- [Scope Application Matrix](./scope-application-matrix.md)
- [Task 0004](../../../03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md)
