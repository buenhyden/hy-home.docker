---
status: active
artifact_id: plan:2026-07-11-deployment-release-engineering-remediation
artifact_type: plan
parent_ids:
  - prd:025-operational-readiness-closure
  - ard:0028-operational-readiness-closure
  - adr:0028-local-isolated-readiness-evidence
  - spec:127-deployment-release-engineering-remediation
---

# Deployment and Release Engineering Remediation Implementation Plan

## Overview

This active plan turns Spec 127 into an executable local sequence for
`examples/sample-web-service` baseline/canary environments, verified-digest
promotion, health gates, release/deployment evidence records, and previous
digest rollback. It is prospective; actual local runtime evidence belongs in
the future sibling Task.

The implementation rehearses delivery mechanics only. It does not create a
GitHub Environment, GitHub Release, registry publication, remote deployment,
production release event, paid job, or credential change.

## Context and Inputs

Inputs:

- [PRD 025](../../01.requirements/025-operational-readiness-closure.md)
- [ARD 0028](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- [Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md)
- [examples/sample-web-service/docker-compose.yml](../../../examples/sample-web-service/docker-compose.yml)
- Spec 124 readiness result, Spec 125 recovery boundary, and Spec 126 verified
  artifact verdict when available.

Planning implication: CI/build success, changelog text, and local image
existence are inputs, not deployment evidence. The rehearsal must require an
immutable verified digest, promote only after gates pass, and prove rollback to
the previous verified digest.

## Goals and Non-goals

Goals:

- Prove `DRE-001` with explicit local baseline/canary/stable environments,
  separation of gates, and deployment history.
- Prove `DRE-002` with a local release-iteration evidence record that binds
  tag/version placeholder, source revision, artifact digest, approval, verifier
  verdict, outcome, and rollback disposition.
- Prove `DRE-003` with a local promotion wrapper that fails closed on missing
  approval, security verdict, readiness, health, or rollback.
- Prove `DRE-004` with previous verified digest rollback and post-rollback
  health; data recovery remains a Spec 125 handoff.

Non-goals:

- No real GitHub Release or production deployment.
- No GitHub Actions workflow/environment/ruleset mutation.
- No registry push, remote target, secret-value, OIDC, or deployment credential.
- No claim that local canary equals production release readiness.

## Work Breakdown

| Unit | Purpose | Planned owned files | Requirements | RED/GREEN evidence | Commit boundary |
| --- | --- | --- | --- | --- | --- |
| `T-DRE-001` | Define local deployment evidence schema, gate contract, and baseline/canary project identities. | `scripts/validation/local-release-readiness.*`, `scripts/validation/fixtures/local-release/**`, Task evidence file. | `DRE-001`–`DRE-004` | RED: mutable tag, missing verifier verdict, missing rollback identity, remote target. GREEN: dry-run resolves source revision, verified digest, projects, gates, ports, cleanup, rollback. | `feat(release): add local promotion and rollback` |
| `T-DRE-002` | Implement local baseline/canary startup and health gate using the verified sample-service digest. | Same harness/tests; sample-service Compose overlays only if task-approved. | `DRE-001`, `DRE-003` | RED: canary starts without Spec 126 verdict or health gate. GREEN: baseline remains separate, canary starts with verified digest, health passes before promotion. | Same DRE commit unless split by review. |
| `T-DRE-003` | Implement stable promotion, release/deployment record, failure injection, and rollback. | Harness tests and fixture evidence. | `DRE-002`, `DRE-004` | RED: promotion records success without record/health or rollback cannot restore previous digest. GREEN: promotion record is complete; injected failure rolls back and health passes. | Same DRE commit unless split by review. |
| `T-DRE-004` | Independent release/spec/security/ops review and SDLC closure. | Task evidence and lifecycle updates only after evidence. | `VAL-DRE-001`–`004` | Spec review C0/I0/M0 and quality/security review C0/I0/M0. | `docs(evidence): record local release closure` if separate evidence-only commit is needed. |

## Sequence

1. Create the active Task with exact local artifact digest source, Spec 126
   verifier verdict dependency, Spec 124 readiness dependency, Spec 125 data
   handoff, project identities, ports, health criteria, rollback, cleanup, and
   redaction.
2. Implement dry-run/preflight. It must fail when the artifact is mutable,
   verifier verdict is missing, target is remote, rollback identity is missing,
   or cleanup is unscoped.
3. Add fixtures for missing approval, wrong digest, failed security verdict,
   failed health, partial promotion, missing release record, and rollback
   failure.
4. Start local baseline and canary projects using task-scoped names and the
   verified digest. Use health probes from the approved Task.
5. Promote canary to local stable only after all gates pass. Record the local
   release/deployment evidence record.
6. Inject one bounded failure after canary or promotion and verify rollback to
   the previous digest plus post-rollback health.
7. Record concise Task evidence only: digest, source revision, gate verdicts,
   project identities, health summaries, promotion/rollback outcome, cleanup,
   and stable failure class.
8. Run independent specification review, then quality/security review. Fix and
   re-review findings before lifecycle closure.

## Verification Plan

| Gate | Command / method | Expected pass evidence |
| --- | --- | --- |
| Metadata and lifecycle | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref <safe-base>` | Changed Stage 04 docs remain valid. |
| Traceability | `bash scripts/validation/check-doc-traceability.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` | `DRE-001`–`DRE-004` map to implemented files and Task evidence. |
| Repository contract | `bash scripts/validation/check-repo-contracts.sh` | No new contract breakage. |
| Fixture/unit tests | Future focused test command owned by `T-DRE-001` | Gate, promotion, record, and rollback fixtures pass. |
| Local runtime rehearsal | Future Task-approved Docker/Compose command envelope | Canary, promotion, health, release/deployment record, rollback, and cleanup pass. |
| Review | Independent spec and quality/security review | C0/I0/M0 or all findings resolved and re-reviewed. |

## Risks and Rollback

| Risk | Impact | Mitigation / rollback |
| --- | --- | --- |
| Mutable or unverified artifact promoted | Critical | Require Spec 126 digest/verifier verdict; reject tags without digest. |
| Local rehearsal confused with production release | High | Evidence labels local-only; no GitHub Release or environment mutation. |
| Partial promotion without rollback | Critical | Previous digest is mandatory input; injected failure proves rollback. |
| Health gate too shallow | High | Health probes are explicit and independent from build success. |
| Data rollback overclaim | Critical | Config/application rollback only; data impact routes to Spec 125. |

Rollback is by running the task-owned rollback wrapper to the previous digest,
then reverting the logical commit if implementation files must be removed.
Cleanup may remove only task-owned local projects, networks, and containers.

## Approval Gates

- Human approval exists for this active Plan conversion.
- The future Task must approve exact local runtime commands, artifact digest,
  health gates, ports, project names, cleanup, and rollback before execution.
- GitHub Environments/Releases, workflow mutation, registry push, remote
  deployment, OIDC/secret identity, and production targets remain unapproved.

## Completion Criteria

- [ ] Active Task maps `DRE-001`–`DRE-004` to exact files, commands, rollback,
      redaction, and reviews.
- [ ] Dry-run/preflight and fixtures reject mutable artifact, missing verifier,
      failed health, missing record, and rollback failure.
- [ ] Local canary starts only with a verified digest and health gate.
- [ ] Promotion produces a local release/deployment evidence record.
- [ ] Injected failure rolls back to previous digest and post-rollback health
      passes.
- [ ] Independent specification and quality/security reviews pass.
- [ ] Spec 127 lifecycle reflects only local delivery mechanics; remote,
      production, registry, GitHub Release, and environment exclusions remain
      explicit.

## Related Documents

- **PRD**: [Operational readiness closure](../../01.requirements/025-operational-readiness-closure.md)
- **ARD**: [Operational readiness closure architecture](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- **ADR**: [ADR-0028 local-isolated readiness evidence](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- **Spec**: [Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md)
- **Runtime dependency**: [Spec 124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md)
- **Recovery dependency**: [Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
- **Security dependency**: [Spec 126](../../03.specs/126-security-supply-chain-remediation/spec.md)
- **Sample service Compose file**: [examples/sample-web-service/docker-compose.yml](../../../examples/sample-web-service/docker-compose.yml)
