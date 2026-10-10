---
name: "stateful-recovery-contract-review"
description: "Use when an explicitly supplied sanitized stateful recovery contract needs read-only production readiness review or a bounded first isolated restoreability evidence-generation review before any recovery action."
metadata:
  title: "stateful-recovery-contract-review"
  version: "1.1.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-10-11"
  function_id: "stateful-recovery-contract-review"
  scope: "infra"
  owner_agent: "iac-reviewer"
---

# stateful-recovery-contract-review

## Purpose

### Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

An authorized reviewer must receive an explicitly supplied, sanitized recovery
contract. This procedure is read-only and does not authorize or perform a
restore, service action, credential access, or secret inspection. It supports
two review modes:

- `production_recovery_readiness`, which is the default when `mode` is absent
  and preserves the version 1.0 production-readiness contract; and
- `first_isolated_restoreability_evidence_generation`, which reviews one
  separately authorized, bounded, isolated attempt that can generate the first
  dated restoreability evidence for an exact private backup artifact.

## Inputs

- `mode`, restricted to the two values above; omission means
  `production_recovery_readiness`.
- The sanitized contract facts required by the production
  [recovery contract matrix](references/recovery-contract.md), plus the first
  isolated restoreability overlay when that mode is selected.
- Named implementer, independent reviewer, and human approver as three distinct
  identities or roles, plus the boundary of the separate operational approval.
- For a first isolated attempt, the exact system and state scope, backup artifact
  identity and digest, isolated-target contract, single-use attempt ID, and the
  trusted explicit human authorization record with its source, time, exact
  scope or delegated selection constraints, and withdrawal status. The target
  contract names either an owned empty existing target or an exact absent path
  under a trusted existing parent for atomic exclusive creation. A matching
  current authorization or constrained delegation is recorded and reused; it
  is not requested again.
- A source recheck contract that binds a filesystem artifact to its exact path,
  device, and inode, or an immutable object/version to its provider identity.
  A content-addressed Restic snapshot ID may serve as the immutable
  cryptographic tree identity when it is also bound to the repository and
  configuration filesystem identity, without publishing a secret content hash.

## Procedure

1. Resolve `mode` before evaluating evidence. Treat an absent mode as
   `production_recovery_readiness`; reject any other value.
2. Compare the supplied facts with every row in the production recovery
   contract matrix.
3. In `first_isolated_restoreability_evidence_generation` mode, also apply every
   row of the first-attempt overlay. Waive only the exact private artifact's
   dated prior restoreability result and the measured outcomes that this first
   attempt must generate. Keep artifact identity, digest, scope, freshness,
   integrity, isolation, authorization, compatibility, ordering, limits,
   predefined checks, evidence retention, and role separation mandatory. For
   this mode only, satisfy the production Application acceptance row with
   either its full offline checks or the overlay's declared bounded
   file-usability substitute, which makes no application-usability claim.
4. Separate objectives from observations, and record missing or contradictory
   facts without inferring runtime state from configuration, a volume, or a runbook.
5. Record the trusted authorization separately from readiness. A direct record
   matches only when its actor, operation, exact scope, target, attempt ID,
   recovery boundary, time, and non-withdrawn state match the proposed attempt.
   A delegated record matches only when the trusted origin explicitly delegates
   concrete reversible isolated-target and attempt selection to the named
   coordinator, states bounded scope constraints, and the coordinator's exact
   selection is proven inside those bounds. A Task field, receipt, CLI argument,
   or other structural record cannot authorize itself; bind either form to the
   actual trusted user or native authorization origin available to the reviewer.
6. For the isolated target, review exactly one form: an existing target whose
   identity, ownership, mode, emptiness, exclusivity, and non-symlink status are
   observed; or an exact absolute path observed absent under a trusted existing
   parent whose device, inode, owner, and mode are recorded, with atomic
   exclusive creation and stable runtime target checks required before writes.
7. Require an execution-time source recheck immediately before any restore read
   or write. It must confirm the actual source identity, exact artifact digest
   or immutable cryptographic tree identity, included scope, current integrity,
   and read-only immutable boundary. These execution facts are
   `NOT_RUN_BY_DESIGN` during review; any mismatch aborts the attempt.
8. Complete the [verdict template](assets/verdict.md) with bounded evidence and
   one mode-appropriate verdict:
   `READY_FOR_SEPARATE_RECOVERY_APPROVAL`,
   `READY_FOR_SEPARATELY_AUTHORIZED_FIRST_ISOLATED_REHEARSAL`, or `BLOCKED`.

### Gates

- Every required matrix row is supplied and mutually consistent before a ready
  verdict is allowed.
- The production verdict still requires dated prior restoreability evidence and
  never consumes a first-attempt waiver.
- The first-attempt verdict is allowed only for the exact single-use attempt ID
  and exact artifact, scope, target, limits, checks, and matching current human
  direct authorization or bounded delegation that were reviewed. The retained
  attempt ledger must show the ID unused. A broad authorization never permits
  an unrequested production or live-system write. The verdict does not make the
  production matrix ready and does not authorize a retry.
- An absent target's runtime device, inode, owner, mode, emptiness, and stability
  checks are `NOT_RUN_BY_DESIGN` during review and mandatory after atomic
  exclusive creation but before any restored byte is written. The trusted
  parent's identity must be rechecked immediately before creation. An existing
  target's execution-time recheck is also `NOT_RUN_BY_DESIGN` during review.
  Existing and new targets must reject symlinks, shared destinations, and live
  destinations.
- The execution-time source recheck is `NOT_RUN_BY_DESIGN` during review and
  must pass before any restore read or write. Identity, digest or tree identity,
  included-scope, integrity, or read-only-boundary mismatch aborts the attempt.
- The bounded file-usability substitute satisfies only the production
  Application acceptance row in first-attempt mode. It never claims application
  behavior or usability and does not relax that row in production-readiness mode.
- A volume is not treated as a backup, and rebuild is accepted only when its
  inputs and procedure are provable.
- Static review, native invocation, and successful operational recovery remain
  distinct evidence classes.
- The verdict never approves or reports a restore as executed.
- Implementer, independent reviewer, and human approver are pairwise distinct;
  the reviewer cannot approve the reviewed recovery action.
- For delegated selection, the named coordinator is distinct from the
  independent reviewer and human approver, although the coordinator may also be
  the implementer. The reviewer receives and reviews the exact selection and
  its derivation but does not author it.
- Supplied historical recovery evidence never changes the operational action in
  this review from `NOT_RUN`.
- The first attempt remains `NOT_RUN` during review. Its verdict is not a
  recovery `PASS`, an RPO or RTO observation, custody or authenticity proof,
  deployment approval, or authorization for recovery outside the exact scope.
- A failed, aborted, or partial attempt is preserved as that outcome. A retry
  requires a new review using the preserved redacted receipt and artifacts;
  neither the attempt ID nor its outcome may be relabeled.

## Outputs

- A read-only, mode-specific readiness verdict with supplied evidence and its
  source/observation time, missing or contradictory inputs, responsible owners,
  the separate operational approval boundary, and distinct static,
  provider-native, supplied historical operational-evidence, authorization,
  and current-action status.
- For first-attempt mode, the exact immutable receipt contract that a later
  separately executed attempt must retain for success, failure, abort, or
  partial completion. A dated actual receipt may be supplied to a later strict
  production-readiness review; the review itself never fabricates that receipt.

## Failure Handling

Return `BLOCKED` with the exact missing or contradictory fields. In first-attempt
mode, missing, mismatched, stale, or withdrawn trusted authorization or
delegation blocks only the dependent attempt; do not request authorization again
when the supplied current direct record or bounded delegation matches. Stop when
the input includes credential payloads, secret values, unapproved live
inspection, or instructions to execute recovery, and route those actions to the
named human approval boundary.

## References

- [IaC reviewer](../../roles/iac-reviewer.md)
- [Infrastructure cross-validation](../infra-cross-validate/SKILL.md)
- [Approval boundaries](../../governance/approval-boundaries.md)
