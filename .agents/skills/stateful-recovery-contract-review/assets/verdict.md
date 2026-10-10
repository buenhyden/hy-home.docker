# Stateful Recovery Contract Review

- Verdict: `BLOCKED`
- Review mode: `production_recovery_readiness`
- Review scope: `<system and state boundary>`
- Contract source: `<sanitized source>`
- Reviewed at: `<timestamp>`
- Separate operational approval boundary: `<named boundary or missing>`
- First isolated attempt ID: `<single-use ID or not applicable>`

## Evidence

| Contract area | Supplied evidence | Source | Observed at | Finding |
| --- | --- | --- | --- | --- |
| `<matrix row>` | `<bounded sanitized evidence>` | `<sanitized source>` | `<timestamp or not observed>` | `<ready or reason blocked>` |

## Missing or Contradictory Inputs

- `<exact field, contradiction, or none>`

## Responsibility

- Implementer: `<name>`
- Independent reviewer: `<name>`
- Human approver for separate recovery action: `<name>`
- Separation check: `<three distinct identities or exact conflict>`
- Delegated selection coordinator: `<name or not applicable>`
- Coordinator relationship to implementer: `<same, distinct, or not applicable>`
- Selection derivation: `<how exact target and attempt ID follow trusted constraints>`
- Selection/review separation: `<reviewer received but did not author selection, or exact conflict>`
- Separate operational approval boundary: `<named boundary or missing>`

## Trusted Authorization Record

- Status: `<MATCHED_DIRECT, MATCHED_DELEGATED, MISSING, MISMATCHED, WITHDRAWN, or not applicable>`
- Trusted user or native origin: `<sanitized origin or not supplied>`
- Authorizing actor: `<name or not supplied>`
- Authorization form: `<direct exact attempt, bounded selection delegation, or not supplied>`
- Exact operation and scope or delegated constraints: `<bounded operation and constraints or not supplied>`
- Authorized artifact and state scope: `<exact bounded identifiers or not supplied>`
- Direct target and attempt ID: `<bounded identifiers or not applicable>`
- Delegated coordinator and selection time: `<identity and timestamp or not applicable>`
- Coordinator-selected target and attempt ID: `<bounded identifiers or not applicable>`
- Selection-within-bounds evidence: `<bounded proof or not applicable>`
- Recovery boundary: `<bounded recovery or not supplied>`
- Authorized at: `<timestamp or not supplied>`
- Withdrawal status checked at: `<timestamp or not supplied>`

Record this section separately from readiness. A `MATCHED_DIRECT` record binds
the trusted origin to the exact attempt. A `MATCHED_DELEGATED` record binds the
trusted origin's explicit constraints to the named coordinator's exact
reversible isolated selection and proves it stayed within bounds. Either current
match avoids asking again; neither makes the review verdict an authorization.
A Task field, receipt, CLI argument, or other structural record cannot authorize
itself, and broad scope does not authorize an unrequested production or
live-system write.

## First-Attempt Target Contract

- Target form: `<owned empty existing target or atomic new target>`
- Exact absolute target path: `<path>`
- Existing target identity: `<device, inode, owner, mode, empty, exclusive, stable, or not applicable>`
- Absent-path observation: `<ABSENT with timestamp or not applicable>`
- Trusted existing parent: `<absolute path, device, inode, owner, mode, or not applicable>`
- Atomic exclusive creation plan: `<bounded procedure or not applicable>`
- Execution target verification: `<NOT_RUN_BY_DESIGN during review or actual result>`
- Symlink, shared, and live-destination rejection: `<bounded evidence>`
- Source/live write and egress boundary: `<read-only source, no live writes, egress blocked>`

## First-Attempt Source Contract

- Source form: `<filesystem artifact, immutable object/version, or content-addressed Restic snapshot>`
- Review-time source identity: `<path/device/inode, provider object/version, or snapshot plus repository/config filesystem identity>`
- Artifact digest or immutable cryptographic tree identity: `<sanitized identity>`
- Included state scope: `<exact bounded scope>`
- Current integrity result: `<bounded result>`
- Read-only immutable boundary: `<bounded evidence>`
- Execution source recheck: `<NOT_RUN_BY_DESIGN during review or actual result>`
- Abort rule: `<identity, digest/tree, scope, integrity, or read-only mismatch aborts before restore read/write>`

## First-Attempt Overlay

Complete this section only for
`first_isolated_restoreability_evidence_generation`.

| Overlay area | Supplied evidence | Source | Observed at | Finding |
| --- | --- | --- | --- | --- |
| `<overlay row>` | `<bounded sanitized evidence>` | `<sanitized source>` | `<timestamp or not observed>` | `<ready, NOT_RUN_BY_DESIGN, or reason blocked>` |

## Evidence Status

- Static contract review: `BLOCKED`
- Provider-native skill invocation: `NOT_OBSERVED`
- Supplied historical operational evidence: `NOT_OBSERVED`
- Operational action in this review: `NOT_RUN`
- First isolated rehearsal in this review: `NOT_RUN`

Use `READY_FOR_SEPARATE_RECOVERY_APPROVAL` for Static contract review only when
every matrix row is supplied and consistent. Set supplied historical operational
evidence to `OBSERVED` only when its sanitized source and observation time are
recorded above. Provider-native invocation requires separate native evidence.
Operational action in this review remains `NOT_RUN`. None of these fields
approves, executes, or proves a current restore. Keep `BLOCKED` when any required
fact is missing or contradictory.

For `first_isolated_restoreability_evidence_generation`, use
`READY_FOR_SEPARATELY_AUTHORIZED_FIRST_ISOLATED_REHEARSAL` only when every
production matrix row is satisfied, with only the explicitly waived dated prior
exact private restoreability result and first-attempt outcomes marked
`NOT_RUN_BY_DESIGN`; the production Application acceptance row is satisfied by full
offline application checks or the declared first-mode-only file-usability
substitute; every overlay row satisfies its ready condition, with only the
enumerated pre-execution checks marked `NOT_RUN_BY_DESIGN`; and the trusted
authorization record is `MATCHED_DIRECT` or `MATCHED_DELEGATED`. This verdict is
single-use for the exact attempt ID. It is not production readiness, a recovery
`PASS`, an RPO or RTO observation, custody or authenticity proof, deployment
approval, or authorization outside that exact attempt. File-usability acceptance
makes no application behavior or usability claim.

## Post-Attempt Receipt (Separate Operation)

This review leaves receipt status `NOT_RUN`. A later separately executed first
attempt preserves this section for every result, including failure, abort, and
partial completion.

- Receipt status: `NOT_RUN`
- Review mode: `<mode>`
- System and state scope: `<exact scope>`
- Actual source identity: `<path/device/inode, provider object/version, or snapshot plus repository/config filesystem identity>`
- Backup artifact digest or immutable cryptographic tree identity: `<identity without private content>`
- Included state scope: `<exact bounded scope>`
- Execution integrity and read-only-boundary verification: `<actual outcomes>`
- Isolated target: `<exact absolute path plus actual device, inode, owner, and mode>`
- Single-use attempt ID: `<ID>`
- Started and finished at: `<timestamps>`
- Measured files, bytes, and duration: `<measurements>`
- Limit, timeout, and abort observations: `<bounded outcomes>`
- Predefined check outcomes: `<integrity and offline application or file-usability results>`
- Final outcome: `<succeeded, failed, aborted, partial, or NOT_RUN>`
- Retained or quarantined evidence: `<redacted references>`
- Cleanup owner and date: `<owner and date>`
- Implementer and independent reviewer: `<distinct identities>`
- Direct-authorization or delegation reference: `<sanitized reference>`
- Coordinator selection record: `<sanitized reference or not applicable>`
- Receipt source and observed at: `<source and timestamp>`

Do not overwrite, relabel, or reuse a failed, aborted, or partial receipt. A
retry requires a new attempt ID and a new review that consumes the preserved
receipt and redacted partial evidence.
