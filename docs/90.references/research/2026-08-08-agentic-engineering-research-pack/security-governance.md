---
status: draft
artifact_id: reference:agentic-engineering-research:security-governance
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-08
review_cycle: on-source-change
---

# Reference: Security Governance and Secure Delivery

## Overview

Security in this workspace is a chain of governance, approval boundaries,
tracked controls, validation, incident ownership, and runtime/operator
evidence. NIST SSDF 1.1, NIST CSF 2.0, OWASP SAMM 2.0, SLSA 1.2, Docker's
Compose model, and OpenSSF Scorecard provide comparison frameworks; this
reference does not formally adopt or certify against them.

At Task 8 baseline `910ce5f36641635118c64b1aa6cfe48f86ecde14`,
the repository has disclosure, least-privilege workflow definitions, secret
scanning, dependency updates, typed hardening and vulnerability gates,
curated image provenance, and a bounded sample-service supply-chain rehearsal.
It does not establish current vulnerabilities, formal framework maturity,
live branch protection, production signing/provenance, runtime container
posture, secret rotation, or incident-target performance.

## Purpose

Satisfy REQ-27 by mapping secure-SDLC, approval, secrets, workflow, container,
supply-chain, incident, and provider/model controls to exact tracked evidence,
verification limits, gaps, remediation ownership, and all fourteen scopes.

## Repository Role

This Stage 90 reference is advisory analysis. It neither changes security
policy nor authorizes a scan, secret read, credential operation, workflow
permission, runtime action, publication, or remote mutation. Current policy
lives in Stage 00; implementation and test owners live in tracked scripts,
workflows, and Specs; live response and recovery evidence belongs in Stage 05.

## Scope

### In scope

- Security trust boundaries, least privilege, approvals, secret handling,
  container/Compose controls, workflow security, dependency hygiene, supply
  chain, incident response, and provider/model change governance.
- Required Docker, NIST, OWASP, SLSA, and OpenSSF primary sources.
- Current readiness-generator check/dry-run evidence and the typed-registry
  false-gap defect.
- Findings versus registered exceptions, policy conflict versus actual secret
  exposure, implementation depth, and all fourteen scope implications.

### Out of scope

- Secret values, `.env` values, private keys, tokens, certificate bodies, raw
  logs, shell history, ignored volumes, and private provider state.
- Running vulnerability scanners, Scorecard, signing, SBOM, attestation,
  Compose/Docker, live incident, or remote GitHub checks.
- Repairing or regenerating the security-readiness artifact, changing policy,
  or promoting sample-service rehearsal controls into release claims.

## Definitions / Facts

### Evidence states and threat boundary

- **Implemented:** a current tracked owner and reachable enforcement path are
  verified for the stated scope. It is not proof of runtime success.
- **Partially Implemented:** a control exists but coverage, integration,
  runtime/remote proof, or release scope is incomplete.
- **Gap:** no adequate current owner/evidence was found for the stated scope.
- **Registered exception:** a tracked owner, reason, and cadence narrows a
  control. An undocumented omission is not an exception.
- **Exposure:** a value or reachable weakness was actually observed. A policy
  conflict or static risky declaration is not itself proof of exposure.

The read-only threat model covers: Compose files as host-affecting trusted
input; external workflow/action and dependency inputs; workflow token and
permission boundaries; container privileges, mounts, networks, ports, images,
and secret grants; artifact build/sign/verify paths; provider/model changes;
and incident/disclosure sinks. No external system or secret value was probed.

### Security control map

| Concern | Current tracked evidence | State and limit | Owner / follow-up |
| --- | --- | --- | --- |
| Disclosure | `.github/SECURITY.md` gives private routes and response targets. | Implemented as policy; contact availability and target attainment unverified. | Security owner; exercise through approved incident procedure. |
| Approval / sandbox | `approval-boundaries.md` protects Compose, secrets, workflows, runtime, policy, and provider surfaces with validation/rollback records. | Implemented governance; provider prompts do not broaden repository authority. | Stage 00/human approver. |
| Workflow privilege | Seven workflows declare top-level permissions; `zizmor` has scoped SARIF rights; 32 resolved external action references are full SHA pins. | Implemented tracked definition; current hosted grants, runs, rulesets, and branch enforcement unverified. | GitHub governance plus security review. |
| Secret scanning/boundary | Gitleaks hook/config, template security baseline, root secret IDs and file-based grants. | Implemented static control; rotation, host permissions, and alternate plaintext channels unverified. | Security/infra owners; metadata-only evidence. |
| Container hardening | Eleven-tier hardening PASS, shared security templates, QuickWin/template checks, and registered exceptions. | Partially Implemented overall; selected repository assertions do not certify runtime/host posture. | Security auditor and infra implementer. |
| Dependency update/audit | Dependabot plus typed Storybook `npm audit --audit-level=high`. | Partially Implemented by ecosystem; broad multi-ecosystem SCA remains a gap. | QA/security Spec and gate owner. |
| Image provenance | 18 curated components/21 images; 20 pinned and one approved floating row. | Partially Implemented; declaration provenance is not digest resolution, SBOM, signature, or SLSA provenance. | Infra registry owner. |
| SBOM/scan/sign/Scorecard capability | Digest-pinned syft, grype, cosign, and Scorecard tool images plus sample-service verification/rehearsal scripts. | Partially Implemented, local and sample-scoped; no release/CI/public score evidence. | Supply-chain Spec owner; separate approval for integration. |
| Incident response | Disclosure targets, security scope, incident/runbook ownership, and Stage 05 routes exist. | Partially Implemented; no exercise, live incident, or objective-attainment evidence. | Human incident commander / operations. |
| Provider/model change | Typed model registry, exact-target approval, coupled adapter/generator/validator rules, and Task evidence are required. | Implemented governance; entitlement and live behavior unverified. | Stage 00 model/provider owner and user approval. |

### Secret-policy conflict is not secret exposure

`approval-boundaries.md` says secret value files are read-forbidden. The
security scope separately describes a protocol under which an explicitly
approved, concrete value read/write/rotation could occur while values remain
non-output. Those owners conflict on whether any approved value read can be
authorized.

Task 8 applied the stricter unconditional rule: it read only identifiers,
paths, mappings, counts, and control metadata. No secret value, private key,
token, certificate body, `.env` value, or token-bearing log was read or
emitted. Therefore the finding is a governance-semantics conflict, not evidence
of actual secret exposure. Reconciliation requires a separately approved
Stage 00/security change that names both owners and preserves redaction,
validation, and recovery obligations.

### Hardening exceptions versus violations

The tracked template exception registry contains no
`no-new-privileges` exception and three `cap_drop: ALL` exceptions for the
Patroni/Spilo database services `pg-0`, `pg-1`, and `pg-2`. It also names
one-shot restart/health exceptions and five secret-use exceptions. These have
reasons and policy ownership and are valid registered exceptions at
configuration depth.

By contrast, the 37 non-gateway services publishing host ports without an
explicit host-IP bind have no matching exposure exception registry. They are
unresolved static policy conflicts, but not proof that a port is live,
internet-reachable, unauthenticated, or exploitable. A future threat review
must either document a narrow protocol/localhost/gateway exception or remediate
the selected topology.

### Security-readiness predecessor and typed-registry defect

The canonical readiness `--check` exited 1 because the stored generated file
is stale. Its non-writing `--dry-run` scanned 7 workflows, 37 shell scripts,
and `.pre-commit-config.yaml`, producing 13 controls: 7 Implemented, 3
Partially Implemented, and 3 Gap. The stored snapshot says 11/1/1 and 36
scripts. Neither artifact was edited or regenerated.

The dry-run downgrades four controls because the generator searches raw
workflow text for leaf commands after CI migrated to typed gate IDs:

| Control | Dry-run result | Current tracked resolution |
| --- | --- | --- |
| `SEC-AUTO-002` workflow security | Partial | Workflow permissions, Zizmor/SARIF job, typed workflow contract, and repository checks remain reachable. |
| `SEC-AUTO-003` secret baseline | Partial | Gitleaks remains configured and `ci.template-security-baseline` resolves to the tracked leaf script. |
| `SEC-AUTO-005` hardening | Gap | `ci.infrastructure-hardening` resolves through setup to `leaf.infrastructure-hardening`, whose entrypoint is `check-all-hardening.sh`. |
| `SEC-AUTO-008` scoped audit | Gap | `ci.dependency-vulnerability-audit` resolves to the leaf adapter arguments `npm audit --audit-level=high --prefix projects/storybook/nextjs`. |

Direct resolution of `.github/workflow-contract.yml` supports the prior
semantic classifications 11 Implemented, 1 Partial, and 1 Gap; the one real
gap is broad dependency SCA. The stored snapshot is still stale because its
evidence/count and old-pack routes are obsolete, while the current generator
is semantically invalid because it cannot resolve typed indirection. Task 10
must remain blocked until the user separately approves a tested generator
correction; only then may the canonical output be regenerated. This reference
does not call either readiness check a PASS.

### Secure SDLC and supply-chain interpretation

NIST SSDF 1.1 supplies high-level practices to prepare the organization,
protect software, produce well-secured software, and respond to
vulnerabilities. NIST CSF 2.0 supplies outcome-based cybersecurity risk
governance and explicitly does not prescribe implementation. OWASP SAMM 2.0
organizes five business functions and fifteen practices. SLSA 1.2 is an
Approved specification with Build and Source tracks and attestation formats.
OpenSSF Scorecard provides heuristic project-health checks; a score is neither
certification nor proof that this repository is vulnerability-free.

The workspace uses pieces of these ideas but makes no formal conformance or
SLSA-level claim. The sample-service scripts prove tracked capability only;
Task 8 did not execute them, build/release an artifact, publish an SBOM or
score, use a production trust root, or verify an artifact at deployment.

The OpenSSF repository is mutable. Its `main` ref was resolved at retrieval to
`40c1e35996730d4fdcbdb2e6a23917a2467e29b7`, and the immutable commit page was
verified. Conclusions use that exact revision, not mutable `main` as fixed
evidence.

### Severity-ranked findings

| Severity | Finding | Evidence / reachability | Remediation owner |
| --- | --- | --- | --- |
| Important | Readiness generator produces false downgrades and stale routes. | `--check` FAIL; dry-run 7/3/3 versus typed resolution 11/1/1. Blocks truthful regeneration and Task 10. | Separately approved generator/test owner; Task 10. |
| Important | 37 non-gateway port-bearing services lack explicit host-IP binding and registered exposure exceptions. | Static Compose declarations only; runtime reachability unverified. | Infra/entry/security owners by selected topology. |
| Important | Persistent-volume backup and restore proof is missing. | 102 declarations, zero backup labels, no runtime exercise. | Infra/ops per dataset. |
| Important | Secret-read policy owners conflict. | Two tracked Stage 00 owners; no value was read or exposed. | Separately approved governance/security task. |
| Important | Broad dependency SCA remains absent. | One scoped npm audit and one sample image path do not cover repository ecosystems. | Security/QA specification owner. |
| Minor | Supply-chain tools can be overreported as release automation. | Tool registry/scripts exist; no CI/release/published result was observed. | Supply-chain and documentation reviewers. |

No Critical finding is established by the authorized static evidence. That is
not a statement that no Critical runtime vulnerability exists.

## Scope Implications

| Scope | Security implication |
| --- | --- |
| `agentic` | Enforce permission, evidence, retry, redaction, and approval boundaries; synthetic/configured controls do not prove native execution. |
| `architecture` | Own threat boundaries, trust zones, identity/data flows, secure-delivery requirements, SLO/recovery design, and exception criteria. |
| `backend` | No backend product surface is established; future services need authz, validation, dependency, secret, data, logging, and abuse-case tests. |
| `common` | Keep shared secure defaults, dependency/format rules, and reusable redaction patterns centralized without weakening layer-specific controls. |
| `docs` | Preserve source dates, evidence states, incident secrecy, exception ownership, and the distinction between policy conflict and exposure. |
| `entry` | Review gateway auth/TLS and the 37 non-gateway published-port declarations; require explicit host binding or registered exception evidence. |
| `frontend` | Current Storybook audit is scoped QA evidence, not a complete frontend security program; future UI needs CSP/auth/session/input tests. |
| `infra` | Own Compose privileges, networks, ports, volumes, images, secrets, backup/restore, and runtime-approved remediation. |
| `meta` | Generated readiness must resolve typed registry semantics and stay byte-exact; stale counts and links cannot be treated as current truth. |
| `mobile` | No mobile surface exists; future clients need secure storage, transport, identity, privacy, dependency, and release-integrity contracts. |
| `ops` | Own incident command, private disclosure, audit/log access, rotation, recovery, exercises, and verified operational objectives. |
| `product` | Define abuse cases, protected assets, privacy impact, risk acceptance, and user-visible security/recovery requirements. |
| `qa` | Keep secret, workflow, dependency, container, supply-chain, runtime, and remote tests separate; record exact scope and skipped checks. |
| `security` | Rank reachability and impact, preserve stricter secret boundaries, review exceptions, and require remediation/residual-risk ownership. |

## Sources

| Source | Accessed | Class | Verification state |
| --- | --- | --- | --- |
| [NIST SP 800-218, SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | 2026-08-08T18:18:06+09:00 | External fixed publication | Verified official page; February 2022 final, comparison only. |
| [NIST Cybersecurity Framework 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) | 2026-08-08T18:18:06+09:00 | External fixed publication | Verified official CSWP 29 page; outcome/risk framework, not workspace adoption. |
| [OWASP SAMM model](https://owaspsamm.org/model/) | 2026-08-08T18:18:06+09:00 | External mutable | Verified official model 2.0 page; five functions/fifteen practices. |
| [SLSA specification 1.2](https://slsa.dev/spec/v1.2/) | 2026-08-08T18:18:06+09:00 | External fixed version | Verified Approved v1.2 page; no local SLSA level inferred. |
| [OpenSSF Scorecard repository](https://github.com/ossf/scorecard) | 2026-08-08T18:18:06+09:00 | External mutable | Official repository verified; mutable `main` not used as immutable proof. |
| [OpenSSF Scorecard commit `40c1e359`](https://github.com/ossf/scorecard/commit/40c1e35996730d4fdcbdb2e6a23917a2467e29b7) | 2026-08-08T18:18:06+09:00 | External fixed at pinned revision | `git ls-remote` and immutable commit page verified. |
| [Docker Compose file reference](https://docs.docker.com/reference/compose-file/) | 2026-08-08T18:18:06+09:00 | External mutable | Verified official application-model page; local adoption remains tracked evidence. |
| [Security scope](../../../00.agent-governance/scopes/security.md) | 2026-08-08 | Workspace tracked policy | Identity, secrets, container/network hardening, and approved-secret-work protocol. |
| [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) | 2026-08-08 | Workspace tracked policy | Protected surfaces and unconditional secret-value-read prohibition. |
| [Typed workflow contract](../../../../.github/workflow-contract.yml) | 2026-08-08 | Workspace tracked at `910ce5f` | Gate indirection, leaf entrypoints, action pins, and profiles resolved directly. |
| [CI quality workflow](../../../../.github/workflows/ci-quality.yml) | 2026-08-08 | Workspace tracked | Permissions and typed gate calls; no hosted result inferred. |
| [Security readiness generator](../../../../scripts/validation/generate-security-automation-readiness.sh) | 2026-08-08 | Workspace tracked/executed read-only | `--check` FAIL; `--dry-run` 7/3/3 over 7 workflows/37 scripts; no write. |
| [Stored readiness snapshot](../../data/security/security-automation-readiness.md) | 2026-08-08 | Workspace generated/tracked stale | 11/1/1 and 36-script text retained; not current canonical evidence. |
| [Hardening entry point](../../../../scripts/hardening/check-all-hardening.sh) and [template exceptions](../../../../infra/common-optimizations.exceptions.json) | 2026-08-08 | Workspace tracked/executed | Eleven tiers PASS; selected static controls and registered exceptions only. |
| [Supply-chain tool registry](../../../../infra/supply-chain.tool-images.json) | 2026-08-08 | Workspace tracked | Digest-pinned tool identities; execution/release integration unverified. |
| [Security disclosure policy](../../../../.github/SECURITY.md) | 2026-08-08 | Workspace tracked | Private reporting paths and response targets; operational attainment unverified. |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md) | 2026-08-08 | Workspace tracked stale/advisory | Built from `f8a72211`; corroborated and not used as security proof. |

## Maintenance

Reopen every mutable external source and re-resolve the exact Scorecard commit
after security policy, typed workflow gates, hardening, dependencies,
supply-chain scripts, incident ownership, or readiness generation changes.
Keep configured, reachable, locally executed, hosted/remote, runtime, and
release evidence separate. Owner: Documentation maintainers with independent
Security, QA, Infra, and Operations review.

## Related Documents

- [Docker Compose and infrastructure](./docker-compose-infrastructure.md)
- [Automation pipeline and workflow](./automation-pipeline-workflow.md)
- [Quality, CI, and formatting](./quality-ci-formatting.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Security data index](../../data/security/README.md)
