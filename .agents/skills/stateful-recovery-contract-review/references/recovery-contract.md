# Recovery Contract Matrix

Review only sanitized facts supplied for the named system and scope. Record the
source and observation time for evidence without copying secret values, raw
credentials, or unrelated runtime data.

## Production Recovery Readiness

| Area | Required contract facts | Ready condition |
| --- | --- | --- |
| State and volumes | Stateful components, data classes, volume or storage identifiers, ownership, and exclusions | Every required state source has one disposition and owner. |
| Backup or rebuild | Sanitized backup artifact identity, source, capture or freshness time, integrity result, and dated prior restoreability verification; or the versioned inputs and deterministic procedure that prove rebuildability | Each state source has a backup whose identity, integrity, freshness, and dated prior restoreability evidence support the reviewed scope, or a provable rebuild path; volume existence alone is insufficient. |
| Consistency | Quiescing, snapshot, transaction, replication, or other consistency boundary and its dependent components | The method covers the dependency set and states its consistency limit. |
| Retention and capacity | Retention window, restore-point selection, source size, target capacity, and expected growth | The selected restore point is retained and the target has bounded capacity evidence. |
| Encryption and key custody | Encryption boundary plus named key custodian and approved key-availability process, without key material | Required keys have an accountable custody and availability path. |
| Dependency and restore order | Ordered components, prerequisites, identity or network dependencies, and decision points | The order is complete and has explicit stop conditions. |
| Version compatibility | Source version, target version, format or schema compatibility, and required migrations | Compatibility is supported by current evidence and migrations are bounded. |
| Isolated target | Named non-production or otherwise isolated target, access boundary, network boundary, and cleanup owner | Validation cannot affect the source or an unapproved runtime. |
| RPO and RTO | Objectives, separately recorded observations, observation time, and measurement method | Objectives and observations are labeled separately; an objective is never reported as an observed result. |
| Application acceptance | Data integrity, application behavior, dependency, and rollback checks with expected results | Checks determine whether the restored application is usable, not only whether storage mounted. |
| Failure and stop | Abort signals, partial-result handling, preservation needs, cleanup, and escalation owner | Unsafe, ambiguous, or partial recovery has a bounded stop and escalation path. |
| Responsibility | Named implementer, independent reviewer, and human approver for the separate operational action, each assigned to a distinct identity or role | Implementation, independent review, and human approval are pairwise distinct; no implementer or reviewer approves their own protected action or review. |

Any missing row, contradiction, stale evidence that cannot support the stated
scope, or request for secret/live inspection makes the verdict `BLOCKED`.

Dated historical recovery observations are supplied evidence only. They do not
mean this review executed recovery. The verdict always records the current
operational action as `NOT_RUN` and records historical operational evidence
separately with its source and observation time.

## First Isolated Restoreability Evidence Generation

Apply this overlay only when `mode` is
`first_isolated_restoreability_evidence_generation`. It does not replace the
production matrix. It waives only the exact private backup artifact's dated
prior restoreability result and the observations or check outcomes that the
first attempt itself must generate. Mark those items `NOT_RUN_BY_DESIGN` during
review. Every other production row and every overlay row remains required.
For this mode only, the production Application acceptance row is satisfied by
either its full offline application checks or the bounded file-usability
acceptance substitute below. The substitute is not a waiver: it checks only the
declared files and explicitly makes no application behavior or usability claim.

| Area | Required first-attempt facts | Ready condition |
| --- | --- | --- |
| Attempt identity | Exact system and state scope, a unique single-use attempt ID, and the retained attempt ledger consulted at review time | The ledger shows the ID unused; the review and any later receipt bind to one immutable attempt, and a failed, aborted, or partial ID cannot be relabeled or reused. |
| Backup input | Exact artifact identity, cryptographic digest or immutable cryptographic tree identity, included state scope, capture and freshness times, current integrity result, and a read-only immutable source boundary; filesystem sources also provide exact path, device, and inode, while immutable object/version sources provide their provider identity. A content-addressed Restic snapshot ID is acceptable when bound to repository and configuration filesystem identity without publishing a secret content hash | The artifact is bounded and verified without relying on volume existence; only its dated prior restoreability result and the execution-time source recheck may be `NOT_RUN_BY_DESIGN`. Immediately before any restore read or write, actual source identity, digest or tree identity, included scope, integrity, and the read-only immutable boundary must match; mismatch aborts. |
| Trusted authorization | Either a current direct trusted-human authorization for the exact attempt, or a current trusted-human authorization that explicitly delegates concrete reversible isolated-target and attempt selection to a named coordinator within stated system, state, artifact, target-parent, operation, and recovery constraints; plus authorization time, withdrawal status, and, for delegation, the coordinator's exact selected target and attempt ID, selection time, and proof that they are within bounds | The actual trusted user or native origin names the human approver and is not withdrawn; direct authorization matches the exact attempt, or the coordinator's selection is proven inside the explicit delegation. A Task field, receipt, CLI argument, or other structural record cannot authorize itself; broad scope never permits an unrequested production or live-system write, and a matching record is not requested again. |
| Isolation | Either an owned empty existing target identified by exact absolute path, device, inode, owner, and mode, or an exact absolute path observed absent under a trusted existing parent identified by absolute path, device, inode, owner, and mode, with atomic exclusive creation planned; plus no source or live-system writes, blocked egress, and claim-time and execution-time exclusivity checks | An existing target is empty, owned, stable, exclusive, non-symlink, unshared, and non-live at review; its execution recheck is `NOT_RUN_BY_DESIGN` during review and mandatory before writes. For an absent target, path absence and parent identity are verified at review, the parent identity is rechecked immediately before atomic exclusive creation, and target device, inode, owner, mode, emptiness, and stability checks are `NOT_RUN_BY_DESIGN` during review and mandatory before restored bytes are written. Neither form can reach external systems. |
| Compatibility and order | Source and target versions, format compatibility, exact restore order, prerequisites, and stop points | Compatibility is supported before execution and every ordered step has a bounded stop. |
| Resource and time bounds | Maximum files, maximum bytes, deadline or timer, capacity evidence, abort signals, and partial-result behavior | Every bound is measurable before and during execution; crossing one aborts without widening scope. |
| Offline validation | Predefined integrity checks and offline application checks with expected results; or, as the first-mode-only substitute for the production Application acceptance row, exact file paths, file-level checks, and expected results for a bounded file-usability scope that explicitly disclaims application behavior and usability | The selected acceptance form can classify the bounded result without egress or live dependencies; file-usability acceptance makes no application claim, and all pre-run outcomes are `NOT_RUN_BY_DESIGN`, never `PASS`. |
| Evidence disposition | Receipt owner, retention period, quarantine rule, cleanup owner and date, redaction rule, and preservation path for failures and partial artifacts | Success and failure evidence are retained as declared; cleanup cannot erase required failed or partial evidence. |
| Responsibility | Named implementer, independent reviewer, and human approver for the exact attempt; delegated selection also names the coordinator and records how the exact target and attempt ID were derived from the trusted constraints | Implementer, reviewer, and human approver are pairwise distinct. The selection coordinator is distinct from the reviewer and human approver but may also be the implementer; the reviewer receives and reviews the selection and derivation without authoring them. |

`READY_FOR_SEPARATELY_AUTHORIZED_FIRST_ISOLATED_REHEARSAL` means only that the
exact reviewed attempt has a complete first-attempt contract and matching direct
trusted authorization or bounded trusted delegation. The operational action
remains `NOT_RUN`. The verdict is not production readiness, a recovery `PASS`,
an RPO or RTO result, backup authenticity or key-custody proof, deployment
approval, or authorization for another scope or attempt.

### Required Post-Attempt Receipt

The later operator preserves one redacted, immutable receipt for every outcome,
including failure, abort, and partial completion. It records:

- review mode, system and state scope, actual source identity, exact backup
  artifact digest or immutable cryptographic tree identity, included scope,
  execution-time integrity and read-only-boundary verification, isolated target
  absolute path and execution-time device, inode, owner, and mode, and single-use
  attempt ID;
- start and finish times, measured duration, file count, byte count, resource
  limit observations, and abort or timeout state;
- each predefined integrity, application, or file-usability check and its actual
  outcome, without secret values or raw private content;
- final outcome (`succeeded`, `failed`, `aborted`, or `partial`), retained or
  quarantined artifact references, cleanup owner and date, and a redacted
  failure reason when applicable; and
- implementer, independent reviewer, direct-authorization or delegation record
  reference, coordinator selection record when used, and the receipt's source
  and observation time.

A dated actual first-attempt receipt can supply prior restoreability evidence to
a later `production_recovery_readiness` review. It never changes a failed or
partial attempt into success, proves facts outside its exact scope, or authorizes
an unreviewed retry.
