---
status: draft
artifact_id: plan:2026-07-11-security-supply-chain-remediation
artifact_type: plan
parent_ids:
  - spec:126-security-supply-chain-remediation
---

# Security Supply-Chain Remediation Implementation Plan

## Overview

This draft sequences the later implementation of Spec 126 for broader scanning,
SBOM, provenance/attestation, signing/verification, and reviewed Scorecard
signals. It selects no tool and authorizes no scan, workflow, build, secret,
registry, artifact, runtime, or remote action.

## Context and Inputs

The repository has important baseline controls and one scoped npm audit, but no
broad dependency/image gate or artifact-bound SBOM, provenance, signing,
verification, or Scorecard execution. The work must establish artifact/trust
architecture before automating any producer or consumer.

## Prerequisites and Approval State

| Gate | Current state | Required resolution |
| --- | --- | --- |
| Parent spec | Active | Spec 126 is traced to PRD 025, ARD 0028, and ADR 0028; this Plan remains draft. |
| Architecture | Approved local design | PRD 025, ARD 0028, and ADR 0028 bind the sample-service artifact and local trust flow; this Plan must pin exact tool images and policies. |
| Human | Unresolved | Security/artifact owners approve scope, thresholds, blocking, exceptions, retention, and risk. |
| Runtime | Unresolved | Exact targets/tools/commands/resources/failure/cleanup in a future task. |
| Secret | Unresolved/not authorized | Exact signing/OIDC/registry IDs/claims/paths, revocation, and redaction; no values. |
| Remote | Unresolved/not authorized | Exact GitHub/registry/store/repository, permissions, actions, evidence, and rollback. |

Spec 123 approval does not satisfy any gate.

## Goals and Non-goals

- **Goals**: Build a digest-bound, policy/versioned, independently verified
  supply-chain evidence path with explicit advisory/blocking and exception rules.
- **In Scope**: Current official tool-pin verification, deterministic fixtures, advisory
  rollout, failure cases, exception review, identity/secret/remote approvals,
  verifier integration, and independent review.

## Non-Goals & Out-of-Scope

- **Non-goals**: Claim a SLSA level, treat Scorecard as maturity, expose raw
  findings, or duplicate deployment promotion.
- **Out of Scope now**: Tool/workflow/runtime/secret/registry/remote mutation and
  artifact publication before separate approvals.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| `PLN-SSC-001` | Pin sample-service build identity, tool container digests, SBOM/provenance formats, local signing policy, exceptions, and advisory Scorecard mode | Spec 126, this Plan, and future Task | `SSC-001`–`SSC-005` | Artifact, identity class, policy, retention, exception, producer, and consumers are explicit. |
| `PLN-SSC-002` | Create protected-surface task and deterministic local fixtures | Future task/test paths; no task exists now | `SSC-001`–`SSC-005` | Exact surfaces/permissions/redaction/rollback and success/failure fixtures exist. |
| `PLN-SSC-003` | Implement advisory scanning/SBOM/provenance with digest association | Approved build/CI/test surfaces | `SSC-001`–`SSC-003` | Reproducible outputs and subject/material/builder bindings pass. |
| `PLN-SSC-004` | Implement signing/verification and Scorecard advisory review | Approved identity/CI/remote surfaces | `SSC-004`, `SSC-005` | Correct/tampered/wrong-identity cases and reviewed Scorecard disposition pass. |
| `PLN-SSC-005` | Review false positives/exceptions, then separately approve any blocking consumer | Future task/policy/operations surfaces | `SSC-001`–`SSC-005` | Independent review and explicit promotion-gate approval; rollback/revocation ready. |

## Sequencing, Migration, and Rollout

1. Verify the active architecture chain and bind artifact, consumers, trust, policies, and evidence.
2. Pin current official tool containers and approve the future Task boundary.
3. Validate deterministic local fixtures including failure/tampering.
4. Introduce advisory CI/remote evidence only after permissions approval.
5. Review findings, false positives, exceptions, retention, and identities.
6. Add blocking/promotion consumption only through separate approval.

## Rollback and Recovery Strategy

- Keep the current scoped npm gate until approved replacement parity is proven.
- Remove/revert new workflow/tool calls by reviewed commit; retain prior evidence
  and disclose coverage reduction.
- Revoke/rotate signing/OIDC/registry identity through approved procedures.
- Disable the newly approved blocking consumer while preserving advisory
  evidence when false positives, verifier, identity, or registry failures occur.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| `VAL-PLN-SSC-001` | Documentation | Typed metadata/traceability/contracts | Explicit-base metadata checker plus doc gates | Zero new violations; no tool/runtime claim. |
| `VAL-PLN-SSC-002` | Fixture | Deterministic artifact/scan/SBOM/provenance/signing fixtures | Future approved task | Reproducible subject/material identity and failure cases pass. |
| `VAL-PLN-SSC-003` | Advisory | Scoped tools and redacted results | Future approved task only | Policies, permissions, exceptions, retention, and review pass. |
| `VAL-PLN-SSC-004` | Verification | Correct, tampered, and wrong-identity artifacts | Future approved task only | Verifier accepts/rejects exactly per approved policy. |
| `VAL-PLN-SSC-005` | Review | Security/artifact/QA and consumer review | Review future task/evidence | No unresolved critical/important finding before blocking rollout. |

## Risks and Rollback

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Wrong artifact/digest association | Critical | Immutable subject identity and verifier failure cases. |
| Signing/OIDC/registry compromise | Critical | Least privilege, exact identity, no secret values, revocation/rotation. |
| False-positive blocking | High | Advisory-first rollout, reviewed exceptions, rollback switch. |
| Raw vulnerability leakage | High | Redacted summaries and protected evidence location. |
| Tool output inflated into maturity claim | High | Evidence-specific acceptance and explicit limitations. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Deterministic local fixtures for success, tampering,
  wrong identity, threshold, exception, and SBOM/provenance association.
- **Sandbox / Canary Rollout**: Advisory on non-release/test artifacts before
  real build/release consumers.
- **Human Approval Gate**: Security/artifact approval before remote, identity,
  publication, or blocking changes.
- **Rollback Trigger**: Identity/digest mismatch, false-positive threshold,
  expired exception, verifier/registry failure, or leakage.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [ ] Required PRD/ARD/ADRs exist and are approved.
- [ ] This Plan is reviewed and activated while Spec 126 remains active.
- [ ] A separate protected-surface Stage 04 task authorizes exact execution.
- [ ] Human, runtime, secret, remote, and architecture gates are resolved.
- [ ] Deterministic success/failure fixtures and advisory rollout pass.
- [ ] Any blocking/promotion integration has separate approval and rollback.

## Related Documents

- **Spec**: [Security supply-chain remediation](../../03.specs/126-security-supply-chain-remediation/spec.md)
- **Umbrella lineage**: [Spec 123](../../03.specs/123-agentic-engineering-audit-remediation/spec.md)
- **Deployment consumer**: [Deployment/release plan](./2026-07-11-deployment-release-engineering-remediation.md)
- **Runtime consumers**: [Compose runtime plan](./2026-07-11-compose-runtime-readiness-remediation.md), [Infrastructure operations plan](./2026-07-11-infrastructure-operations-readiness-remediation.md)
- **Operations**: [Operations index](../../05.operations/README.md)
