# Stateful Recovery Contract Review

- Verdict: `BLOCKED`
- Review scope: `<system and state boundary>`
- Contract source: `<sanitized source>`
- Reviewed at: `<timestamp>`
- Separate operational approval boundary: `<named boundary or missing>`

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
- Separate operational approval boundary: `<named boundary or missing>`

## Evidence Status

- Static contract review: `BLOCKED`
- Provider-native skill invocation: `NOT_OBSERVED`
- Supplied historical operational evidence: `NOT_OBSERVED`
- Operational action in this review: `NOT_RUN`

Use `READY_FOR_SEPARATE_RECOVERY_APPROVAL` for Static contract review only when
every matrix row is supplied and consistent. Set supplied historical operational
evidence to `OBSERVED` only when its sanitized source and observation time are
recorded above. Provider-native invocation requires separate native evidence.
Operational action in this review remains `NOT_RUN`. None of these fields
approves, executes, or proves a current restore. Keep `BLOCKED` when any required
fact is missing or contradictory.
