---
title: "Reference: Security Governance and Secure Delivery"
version: "1.0.0"
type: "reference/research"
status: "published"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "references"
artifact_id: "RES-0002-m0017"
parent_ids:
- "RES-0002"
created: "2026-08-23"
reviewed_at: "2026-08-28"
review_cycle: "on-source-change"
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

| Concern                             | Current tracked evidence                                                                                                                                                                                                                   | State and limit                                                                                              | Owner / follow-up                                             |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| Disclosure                          | `.github/SECURITY.md` gives private routes and response targets.                                                                                                                                                                           | Implemented as policy; contact availability and target attainment unverified.                                | Security owner; exercise through approved incident procedure. |
| Approval / sandbox                  | `approval-boundaries.md` protects Compose, secrets, workflows, runtime, policy, and provider surfaces with validation/rollback records.                                                                                                    | Implemented governance; provider prompts do not broaden repository authority.                                | Stage 00/human approver.                                      |
| Workflow privilege                  | Seven workflows declare top-level permissions; `zizmor` has scoped SARIF rights; re-verified 2026-08-19, every tracked `uses:` action reference is a full-length commit SHA pin: 17 literal `uses:` lines across 7 files, resolving to 32 references once the `ci-quality.yml` `*checkout` anchor is expanded 15 times, over 8 distinct action identities. 17 is the count of literal lines, not of resolved references; the earlier wording here conflated the two and is corrected. | Implemented tracked definition; current hosted grants, runs, rulesets, and branch enforcement unverified.    | GitHub governance plus security review.                       |
| Secret scanning/boundary            | Gitleaks hook/config, template security baseline, root secret IDs and file-based grants.                                                                                                                                                   | Implemented static control; rotation, host permissions, and alternate plaintext channels unverified.         | Security/infra owners; metadata-only evidence.                |
| Container hardening                 | Eleven-tier hardening PASS, shared security templates, QuickWin/template checks, and registered exceptions.                                                                                                                                | Partially Implemented overall; selected repository assertions do not certify runtime/host posture.           | Security auditor and infra implementer.                       |
| Dependency update/audit             | Dependabot plus typed Storybook `npm audit --audit-level=high`.                                                                                                                                                                            | Partially Implemented by ecosystem; broad multi-ecosystem SCA remains a gap.                                 | QA/security Spec and gate owner.                              |
| Image provenance                    | 18 curated components/21 images; 20 pinned and one approved floating row.                                                                                                                                                                  | Partially Implemented; declaration provenance is not digest resolution, SBOM, signature, or SLSA provenance. | Infra registry owner.                                         |
| SBOM/scan/sign/Scorecard capability | Digest-pinned syft, grype, cosign, and Scorecard tool images plus sample-service verification/rehearsal scripts.                                                                                                                           | Partially Implemented, local and sample-scoped; no release/CI/public score evidence.                         | Supply-chain Spec owner; separate approval for integration.   |
| Incident response                   | Disclosure targets, security scope, incident/runbook ownership, and Stage 05 routes exist.                                                                                                                                                 | Partially Implemented; no exercise, live incident, or objective-attainment evidence.                         | Human incident commander / operations.                        |
| Provider/model change               | Typed model registry, exact-target approval, coupled adapter/generator/validator rules, and Task evidence are required.                                                                                                                    | Implemented governance; entitlement and live behavior unverified.                                            | Stage 00 model/provider owner and user approval.              |

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

### Security-readiness predecessor and typed-registry defect (resolved since Task 8)

At Task 8 baseline `910ce5f`, the canonical readiness `--check` exited 1
because the generator searched raw workflow text for leaf commands after CI
migrated to typed gate IDs, downgrading four controls (`SEC-AUTO-002`,
`SEC-AUTO-003`, `SEC-AUTO-005`, `SEC-AUTO-008`) below the semantic
classification that direct resolution of `.github/workflow-contract.yml`
supported. That semantic classification was 11 Implemented, 1 Partial, and
1 Gap, with the one real gap being broad dependency SCA.

Re-verified at `5580931` on 2026-08-11 against two independent evidence
sources. First, direct re-execution: `bash
scripts/validation/generate-security-automation-readiness.sh --check` now
exits 0 (`PASS: ... snapshot is fresh`), and `--dry-run` reports the same 13
controls as the stored snapshot: 11 Implemented, 1 Partially Implemented
(`SEC-AUTO-007` branch protection, live-remote-evidence limited), and 1 Gap
(`SEC-AUTO-012` broad dependency SCA), scanning 7 workflows, 37 scripts,
`.pre-commit-config.yaml`, and 54 reachable typed gates. Second, the tracked
Task ledger: the Task 10a workstream (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
(`WS-TASK10A-FIX1` through `WS-TASK10A-FIX5`, commits `eed66ec7` through
`08bbba79`, all landed 2026-08-08 after the Task 8 baseline) rebuilt the
generator's gate parser/expander, action registry, and workflow-projection
logic under RED/GREEN evidence, and records the final round's independent
reviews as specification "Needs fixes C0/I0/M1, load-bearing
Approved-equivalent" and Python/security "Approved-with-Minor C0/I0/M1" with
the prior Important finding resolved. Both sources agree the generator now
resolves typed gate indirection directly and the stored snapshot and live
generator output match; the typed-registry defect described above no longer
reproduces. This reference does not certify the readiness snapshot as a
vulnerability assessment or security certification, and it does not observe
whether Task 10 as a whole has been separately closed.

### Re-verification at current HEAD (2026-08-14)

**Counts re-measured 2026-08-29.** The reading rule below is unchanged and still
correct: a literal `uses:` line scan undercounts, because a YAML anchor resolves
to more references than the text shows. Its numbers have moved with the
workflows and are recorded here rather than edited into the 2026-08-14 reading
above, which stays as the observation it was. At this date the seven workflow
files hold **15** literal `uses:` occurrences and **one** `*checkout` reference,
resolving to **16**, not the 17-and-15-resolving-to-32 of the earlier reading;
the `&checkout` anchor is declared at `ci-quality.yml:30`. What did not move:
**8** distinct action identities, and **15 of 15** references pinned to a full
40-character SHA with none unpinned, so the Poisoned Pipeline Execution finding
below holds on its security property while its arithmetic is dated.

This leaf's 2026-08-11 re-verification cited commit `5580931`. At today's HEAD
`ece3eda9c3e1a603c6495dd55caba7df1c29ef6c` (no `.github/workflow-contract.yml`,
`.github/workflows/**`, or readiness-generator change occurred between the two
commits per `git log --oneline 5580931..HEAD -- .github scripts/validation/generate-security-automation-readiness.sh`
returning zero commits touching those paths for this generator), the readiness
generator was re-executed directly rather than re-read from the prior
snapshot: `bash scripts/validation/generate-security-automation-readiness.sh
--check` again exits 0 (`PASS: ... snapshot is fresh`), and `--dry-run`
reports the identical 11 Implemented / 1 Partially Implemented
(`SEC-AUTO-007`, branch protection) / 1 Gap (`SEC-AUTO-012`, broad dependency
SCA) split over 7 workflows, 37 scripts, `.pre-commit-config.yaml`, and 54
reachable typed gates. Separately, a direct re-scan of every `uses:` line
across `.github/workflows/*.yml` (Python regex over 7 files, not `rg`, to
avoid a local shell-alias artifact) finds exactly 17 `uses:` invocations
referencing 8 distinct actions, each pinned to a full 40-character commit SHA:
`actions/checkout` (4), `actions/setup-python` (4), `actions/setup-node` (3),
`actions/first-interaction` (2), `astral-sh/setup-uv` (1),
`github/codeql-action/upload-sarif` (1), `actions/labeler` (1), and
`actions/stale` (1).

Corrected 2026-08-18: 17 is the count of LITERAL `uses:` lines, not of resolved
references. `ci-quality.yml` declares an `&checkout` YAML anchor at line 25 and
invokes it 15 further times, so an anchor-resolving parser reports 32 of 32
resolved references across the same 8 action identities. A raw line scan
undercounts by exactly those 15, which is how a superseded 18/18 figure once
arose. The pin conclusion is unchanged; the coverage denominator is not, and the
retiring pack was the only tracked record of that distinction.

Cross-referencing `.github/workflow-contract.yml`'s
`actions` registry confirms the same 8 action identities and the same SHA for
each (for example `actions/checkout` at `3d3c42e5aac5ba805825da76410c181273ba90b1`);
the registry's own `consumers` arrays list 12 file-level pairs because several
actions are invoked more than once within a single workflow file (e.g.
`actions/setup-python` has 2 registered consumer files but 4 literal `uses:`
occurrences). This is a second, independently derived confirmation of the
17/8 action-pin claim, not a restatement of it, and it still does not observe
whether GitHub's hosted runs, branch protection, or ruleset enforcement
matches the tracked declaration — that remains `UNVERIFIED` under
`SEC-AUTO-007`.

`.github/CODEOWNERS` and `.github/rulesets/main-protection.md` were also read
directly today. CODEOWNERS assigns a single owner (`@buenhyden`) across `*`
and explicit high-value paths (`infra/**`, `scripts/**`, `secrets/**`,
`docs/00.agent-governance/**`, and the provider-adapter directories);
`main-protection.md` states its own observation boundary explicitly —
"Authenticated current ruleset, branch-protection, required-check, review,
environment, and repository-setting readback is unavailable... this proposal
does not infer applied remote state from tracked files or public workflow
metadata" — and lists the sixteen CI Quality Gates job names it proposes as
required checks. Both files are consistent with `SEC-AUTO-007`'s classification:
local, tracked branch-protection _intent_ exists; live GitHub enforcement of
that intent is not observable from this workspace and is not asserted here.

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

### Image signing and build-provenance mechanisms versus current state

The brief axis for this leaf names "container image signing and provenance"
explicitly; the predecessor leaf named the tool capability
(digest-pinned cosign) but not the verification mechanism. Two official
mechanisms apply, re-derived today from Sigstore and SLSA primary
documentation rather than repeated from a prior leaf:

- **cosign signature verification** (`docs.sigstore.dev/cosign/verifying/verify/`,
  retrieved 2026-08-14) checks three things: the cryptographic signature over
  the artifact digest; for keyless signing, that the signing certificate's
  identity and issuer match an expected value, anchored to Sigstore's Fulcio
  CA and transparency log as the trust root (for key-based signing, the trust
  root is whatever public key or KMS reference the operator supplies); and
  that the signed payload's embedded digest matches the container actually
  being verified. A passing `cosign verify` proves the artifact matches the
  signed digest and who signed it — it does **not** prove the artifact is
  vulnerability-free, that the signer is trustworthy beyond identity, or
  anything about code quality.
- **SLSA v1.2 build provenance** (`slsa.dev/spec/v1.2/build-provenance`,
  retrieved 2026-08-14) is a distinct, complementary mechanism: an in-toto
  attestation predicate (`https://slsa.dev/provenance/v1`) with a
  `buildDefinition` (`buildType`, `externalParameters`, `internalParameters`,
  `resolvedDependencies` — the declared build inputs) and `runDetails`
  (`builder.id`, the sole determiner of SLSA Build level; `builder.version`;
  `metadata` timestamps; `byproducts`). A consumer verifies provenance by
  checking `builder.id` against an accepted signer-builder pair, checking
  `externalParameters` against expected values, and verifying
  `resolvedDependencies` digests — this proves the artifact was built by a
  named, trusted platform from named, digest-pinned inputs; it does not by
  itself prove the artifact is signed, unless the builder also produces a
  signature over the provenance.

Both mechanisms are distinct from, and strictly stronger than, this
repository's current tracked evidence. The re-derived facts above (image
declaration parity: 20 `declared-pinned` plus 4 registered floating
exceptions; zero literal `:latest` tags; one untagged-but-registered image)
establish only that a Compose file names a specific tag or digest reference —
not that a signature was verified against a trust root, and not that a
build-provenance attestation was checked against a `builder.id`. The
`verify-sample-service-supply-chain.sh` script (`infra/supply-chain.cosign-offline-signing-config.json`,
`infra/supply-chain.cosign-offline-trusted-root.json`) demonstrates the
mechanism is understood and locally exercisable — its `--fixture-only` mode
pins exact `alpine:3.21` and `nginxinc/nginx-unprivileged` build/runtime
materials by repo digest and target-descriptor digest — but this remains a
sample-service rehearsal, not evidence that any of the 47 tracked infra
Compose variants' 137 image declarations carry a verified signature or a
checked SLSA provenance attestation. That gap is unchanged from the
predecessor's classification (`SBOM/scan/sign/Scorecard capability`:
Partially Implemented, local and sample-scoped).

### CI/CD pipeline risk mapping (OWASP Top 10 CI/CD Security Risks)

OWASP's Top 10 CI/CD Security Risks project (`owasp.org/www-project-top-10-ci-cd-security-risks/`,
retrieved 2026-08-14; v1.0, initial release September 2022, stable release
October 2022) is a new external source for this leaf, not cited by the
predecessor. Mapping its ten categories against this workspace's tracked CI
surface (`.github/workflows/*.yml`, `.github/workflow-contract.yml`) gives a
risk-shaped view the control-map table above does not:

| CICD-SEC risk | Category                                           | Tracked workspace disposition                                                                                                                                                                                                                                        |
| ------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1             | Insufficient Flow Control Mechanisms               | Seven workflows declare top-level `permissions`; branch-protection _intent_ is tracked in `.github/rulesets/main-protection.md` but live enforcement is `UNVERIFIED` (`SEC-AUTO-007`).                                                                               |
| 2             | Inadequate Identity and Access Management          | Single CODEOWNERS principal (`@buenhyden`) across all listed protected paths; no tracked evidence of scoped per-path bot/service identities.                                                                                                                         |
| 3             | Dependency Chain Abuse                             | Dependabot (`SEC-AUTO-004`, Implemented) plus scoped npm audit; broad multi-ecosystem SCA is the one tracked Gap (`SEC-AUTO-012`).                                                                                                                                   |
| 4             | Poisoned Pipeline Execution (PPE)                  | All tracked `uses:` action references are pinned to full 40-character commit SHAs (re-verified today) — 17 literal lines resolving to 32 references once the `ci-quality.yml` `*checkout` anchor is expanded, which forecloses the tag-mutation variant of PPE for registered actions; no tracked evidence rules out script-injection PPE via untrusted workflow inputs. |
| 5             | Insufficient PBAC (Pipeline-Based Access Controls) | Workflow permissions are declared per-workflow; no tracked environment-protection-rule evidence was found for this leaf's re-survey.                                                                                                                                 |
| 6             | Insufficient Credential Hygiene                    | Gitleaks (`.gitleaks.toml`, extends the upstream default ruleset) plus the file-based Docker Secrets contract; secret rotation cadence is not tracked (unchanged finding).                                                                                           |
| 7             | Insecure System Configuration                      | Eleven-tier hardening script PASS is the closest tracked control; it is selected-assertion evidence, not full runner/registry configuration audit.                                                                                                                   |
| 8             | Ungoverned Usage of 3rd Party Services             | The 8-action registry in `.github/workflow-contract.yml` is the tracked allow-list; no tracked policy blocks arbitrary unregistered third-party actions at the GitHub-platform level (`UNVERIFIED`, requires live Actions-permission readback).                      |
| 9             | Improper Artifact Integrity Validation             | This is exactly the gap the prior subsection names: declared image pins are tracked; signature/provenance verification is sample-scoped only, not applied to the 47 tracked infra variants.                                                                          |
| 10            | Insufficient Logging and Visibility                | `zizmor` SARIF upload is tracked (`ci-quality.yml`); no tracked evidence of centralized CI audit-log retention or alerting was found.                                                                                                                                |

This mapping does not change any severity-ranked finding below; it re-frames
the same tracked evidence against an external, named risk taxonomy so a
reviewer can see which of the ten categories have zero tracked mitigation
(none do) versus partial (most: 1, 2, 5, 7, 8, 10) versus substantially closed
for the registered scope (4, 6) versus an explicit named gap (3, 9).

### Severity-ranked findings

| Severity                           | Finding                                                                                                | Evidence / reachability                                                                                                                                                                  | Remediation owner                                                                                                                                                                                                                                                                       |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Resolved (was Important at Task 8) | Readiness generator produced false downgrades and stale routes.                                        | Task 8: `--check` FAIL; dry-run 7/3/3 versus typed resolution 11/1/1. Re-verified 2026-08-11: `--check` PASS (fresh); dry-run and stored snapshot both report 11/1/1 across 13 controls. | Fixed by the tracked Task 10a workstream (`WS-TASK10A-FIX1`-`FIX5`, commits `eed66ec7`-`08bbba79`), independently reviewed Approved-equivalent/Approved-with-Minor with no remaining Critical/Important finding; Task 10's overall status is otherwise outside this leaf's observation. |
| Important                          | 37 non-gateway port-bearing services lack explicit host-IP binding and registered exposure exceptions. | Static Compose declarations only; runtime reachability unverified.                                                                                                                       | Infra/entry/security owners by selected topology.                                                                                                                                                                                                                                       |
| Important                          | Persistent-volume backup and restore proof is missing.                                                 | 102 declarations, zero backup labels, no runtime exercise.                                                                                                                               | Infra/ops per dataset.                                                                                                                                                                                                                                                                  |
| Important                          | Secret-read policy owners conflict.                                                                    | Two tracked Stage 00 owners; no value was read or exposed.                                                                                                                               | Separately approved governance/security task.                                                                                                                                                                                                                                           |
| Important                          | Broad dependency SCA remains absent.                                                                   | One scoped npm audit and one sample image path do not cover repository ecosystems.                                                                                                       | Security/QA specification owner.                                                                                                                                                                                                                                                        |
| Minor                              | Supply-chain tools can be overreported as release automation.                                          | Tool registry/scripts exist; no CI/release/published result was observed.                                                                                                                | Supply-chain and documentation reviewers.                                                                                                                                                                                                                                               |

No Critical finding is established by the authorized static evidence. That is
not a statement that no Critical runtime vulnerability exists.

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

## Scope Implications

| Scope          | Security implication                                                                                                                         |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Enforce permission, evidence, retry, redaction, and approval boundaries; synthetic/configured controls do not prove native execution.        |
| `architecture` | Own threat boundaries, trust zones, identity/data flows, secure-delivery requirements, SLO/recovery design, and exception criteria.          |
| `backend`      | No backend product surface is established; future services need authz, validation, dependency, secret, data, logging, and abuse-case tests.  |
| `common`       | Keep shared secure defaults, dependency/format rules, and reusable redaction patterns centralized without weakening layer-specific controls. |
| `docs`         | Preserve source dates, evidence states, incident secrecy, exception ownership, and the distinction between policy conflict and exposure.     |
| `entry`        | Review gateway auth/TLS and the 37 non-gateway published-port declarations; require explicit host binding or registered exception evidence.  |
| `frontend`     | Current Storybook audit is scoped QA evidence, not a complete frontend security program; future UI needs CSP/auth/session/input tests.       |
| `infra`        | Own Compose privileges, networks, ports, volumes, images, secrets, backup/restore, and runtime-approved remediation.                         |
| `meta`         | Generated readiness must resolve typed registry semantics and stay byte-exact; stale counts and links cannot be treated as current truth.    |
| `mobile`       | No mobile surface exists; future clients need secure storage, transport, identity, privacy, dependency, and release-integrity contracts.     |
| `ops`          | Own incident command, private disclosure, audit/log access, rotation, recovery, exercises, and verified operational objectives.              |
| `product`      | Define abuse cases, protected assets, privacy impact, risk acceptance, and user-visible security/recovery requirements.                      |
| `qa`           | Keep secret, workflow, dependency, container, supply-chain, runtime, and remote tests separate; record exact scope and skipped checks.       |
| `security`     | Rank reachability and impact, preserve stricter secret boundaries, review exceptions, and require remediation/residual-risk ownership.       |

## Sources

| Source                                                                                                                                                                                                            | Accessed                    | Class                                | Verification state                                                                                                                                                                                                                                                                            |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [NIST SP 800-218, SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final)                                                                                                                                          | 2026-08-08T18:18:06+09:00   | External fixed publication           | Verified official page; February 2022 final, comparison only.                                                                                                                                                                                                                                 |
| [NIST Cybersecurity Framework 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20)                                                                                                         | 2026-08-08T18:18:06+09:00   | External fixed publication           | Verified official CSWP 29 page; outcome/risk framework, not workspace adoption.                                                                                                                                                                                                               |
| [OWASP SAMM model](https://owaspsamm.org/model/)                                                                                                                                                                  | 2026-08-08T18:18:06+09:00   | External mutable                     | Verified official model 2.0 page; five functions/fifteen practices.                                                                                                                                                                                                                           |
| [SLSA specification 1.2](https://slsa.dev/spec/v1.2/)                                                                                                                                                             | 2026-08-08T18:18:06+09:00   | External fixed version               | Verified Approved v1.2 page; no local SLSA level inferred.                                                                                                                                                                                                                                    |
| [OpenSSF Scorecard repository](https://github.com/ossf/scorecard)                                                                                                                                                 | 2026-08-08T18:18:06+09:00   | External mutable                     | Official repository verified; mutable `main` not used as immutable proof.                                                                                                                                                                                                                     |
| [OpenSSF Scorecard commit `40c1e359`](https://github.com/ossf/scorecard/commit/40c1e35996730d4fdcbdb2e6a23917a2467e29b7)                                                                                          | 2026-08-08T18:18:06+09:00   | External fixed at pinned revision    | `git ls-remote` and immutable commit page verified.                                                                                                                                                                                                                                           |
| [Docker Compose file reference](https://docs.docker.com/reference/compose-file/)                                                                                                                                  | 2026-08-08T18:18:06+09:00   | External mutable                     | Verified official application-model page; local adoption remains tracked evidence.                                                                                                                                                                                                            |
| Security scope (retired path: `../../../00.agent-governance/scopes/security.md`)                                                                                                                                                 | 2026-08-08                  | Workspace tracked policy             | Identity, secrets, container/network hardening, and approved-secret-work protocol.                                                                                                                                                                                                            |
| [Approval boundaries](../../../00.agent-governance/policies/approval-boundaries.md)                                                                                                                                  | 2026-08-08                  | Workspace tracked policy             | Protected surfaces and unconditional secret-value-read prohibition.                                                                                                                                                                                                                           |
| [Typed workflow contract](../../../../.github/workflow-contract.yml)                                                                                                                                              | 2026-08-08                  | Workspace tracked at `910ce5f`       | Gate indirection, leaf entrypoints, action pins, and profiles resolved directly.                                                                                                                                                                                                              |
| [CI quality workflow](../../../../.github/workflows/ci-quality.yml)                                                                                                                                               | 2026-08-08                  | Workspace tracked                    | Permissions and typed gate calls; no hosted result inferred.                                                                                                                                                                                                                                  |
| [Security readiness generator](../../../../scripts/validation/generate-security-automation-readiness.sh)                                                                                                          | 2026-08-11 (was 2026-08-08) | Workspace tracked/executed read-only | Re-verified at `5580931`: `--check` PASS (fresh, exit 0); `--dry-run` 11/1/1 over 7 workflows/37 scripts/54 reachable typed gates. The Task 8 `--check` FAIL / dry-run 7/3/3 result no longer reproduces after fix commits `eed66ec7`-`08bbba79`; no write performed by this re-verification. |
| [Stored readiness snapshot](../../data/0078-security-automation-readiness/README.md)                                                                                                                                 | 2026-08-11 (was 2026-08-08) | Workspace generated/tracked          | Re-verified: 11/1/1 and 37-script text, matching the live `--check`/`--dry-run` output; now current canonical evidence (was stale at Task 8).                                                                                                                                                 |
| [Hardening entry point](../../../../scripts/hardening/check-all-hardening.sh) and [template exceptions](../../../../infra/common-optimizations.exceptions.json)                                                   | 2026-08-08                  | Workspace tracked/executed           | Eleven tiers PASS; selected static controls and registered exceptions only.                                                                                                                                                                                                                   |
| [Supply-chain tool registry](../../../../infra/supply-chain.tool-images.json)                                                                                                                                     | 2026-08-08                  | Workspace tracked                    | Digest-pinned tool identities; execution/release integration unverified.                                                                                                                                                                                                                      |
| [Security disclosure policy](../../../../.github/SECURITY.md)                                                                                                                                                     | 2026-08-08                  | Workspace tracked                    | Private reporting paths and response targets; operational attainment unverified.                                                                                                                                                                                                              |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                                                                                                                                       | 2026-08-08                  | Workspace tracked stale/advisory     | Built from `f8a72211`; corroborated and not used as security proof.                                                                                                                                                                                                                           |
| [OWASP Top 10 CI/CD Security Risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/)                                                                                                                   | 2026-08-14                  | External fixed publication           | Verified official project page; v1.0, stable release October 2022. New source for this leaf; ten-category risk mapping added.                                                                                                                                                                 |
| [SLSA v1.2 build provenance](https://slsa.dev/spec/v1.2/build-provenance)                                                                                                                                         | 2026-08-14                  | External fixed version               | Verified Approved v1.2 page; predicate structure (`buildDefinition`, `runDetails`, `builder.id`) read directly, not inferred from the summary landing page.                                                                                                                                   |
| [Sigstore cosign verification](https://docs.sigstore.dev/cosign/verifying/verify/)                                                                                                                                | 2026-08-14                  | External mutable                     | Verified official page; signature/certificate/digest verification mechanism and Fulcio trust root confirmed; explicit non-claims (not vulnerability-free) noted.                                                                                                                              |
| [CODEOWNERS](../../../../.github/CODEOWNERS)                                                                                                                                                                      | 2026-08-14                  | Workspace tracked                    | Read in full; single principal (`@buenhyden`) across all listed protected paths.                                                                                                                                                                                                              |
| [Main branch protection proposal](../../../../.github/rulesets/main-protection.md)                                                                                                                                | 2026-08-14                  | Workspace tracked                    | Read in full; states its own live-enforcement observation boundary explicitly and lists 16 proposed required-check job names.                                                                                                                                                                 |
| [Gitleaks configuration](../../../../.gitleaks.toml)                                                                                                                                                              | 2026-08-14                  | Workspace tracked                    | Read in full; extends the upstream default ruleset, no repository-specific secret allowlist beyond that default.                                                                                                                                                                              |
| Direct Python re-scan of `.github/workflows/*.yml` `uses:` lines and `.github/workflow-contract.yml` `actions` registry                                                                                           | 2026-08-14                  | Workspace tracked                    | Independently re-derived (not `rg`, to avoid a local shell alias) 17 `uses:` occurrences across 8 distinct SHA-pinned actions; cross-checked against the registry's 12 file-level consumer pairs and found consistent.                                                                        |
| [Security readiness generator](../../../../scripts/validation/generate-security-automation-readiness.sh)                                                                                                          | 2026-08-14 (was 2026-08-11) | Workspace tracked/executed read-only | Re-executed at HEAD `ece3eda9`: `--check` PASS (fresh, exit 0); `--dry-run` still 11/1/1 over 7 workflows/37 scripts/54 reachable typed gates, unchanged from the 2026-08-11 re-verification; no `.github` or generator-script commit occurred in between.                                    |
| [Sample-service supply-chain rehearsal script](../../../../scripts/security/verify-sample-service-supply-chain.sh) and [cosign offline config](../../../../infra/supply-chain.cosign-offline-signing-config.json) | 2026-08-14                  | Workspace tracked                    | Read in full (not executed); digest-pinned `alpine:3.21` and `nginxinc/nginx-unprivileged` build/runtime materials confirmed; four execution modes (`--fixture-only`, `--preflight`, `--advisory`, `--scorecard-advisory`) read directly, none invoked.                                       |

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

## Maintenance

Reopen every mutable external source and re-resolve the exact Scorecard commit
after security policy, typed workflow gates, hardening, dependencies,
supply-chain scripts, incident ownership, or readiness generation changes.
Keep configured, reachable, locally executed, hosted/remote, runtime, and
release evidence separate. Owner: Documentation maintainers with independent
Security, QA, Infra, and Operations review.

## Related Documents

- [Verification and validation](./m0019-verification-validation.md)
- [Docker Compose and infrastructure](./m0005-docker-compose-infrastructure.md)
- [Automation pipeline and workflow](./m0004-automation-pipeline-workflow.md)
- [Quality, CI, and formatting](./m0014-quality-ci-formatting.md)
- [Workspace baseline](./m0020-workspace-baseline.md)
- [Scope application matrix](./m0015-scope-application-matrix.md)
- [Data index](../../data/README.md)
- [SPEC-0158 preservation contract](../../../98.archive/completed/03.specs/0158-document-governance-lifecycle-convergence/spec.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
