<!-- Output shape for the policy-gate verdict. This is not a stage document:
     Stage 99 owns those. It exists so a verdict cannot quietly omit the
     distinction between a gate that passed and one that never ran. -->

# Policy gate verdict

**Change**: `<commit range or diff scope>`
**Authority profile**: `<exactly one>`
**Owner**: `<canonical owner>`

## Gate results

Every registered gate in scope gets a row. A gate with no row is a gate nobody
looked at, which is the failure this table exists to make visible.

| Gate | Result | Evidence |
| --- | --- | --- |
| `<gate id>` | PASS / FAIL / NOT_RUN / SKIPPED / BLOCKED / REMOTE_ONLY / NOT_APPLICABLE | `<command and its output line>` |

`PASS` means the gate ran here and returned zero. It is never inferred from a
gate that was skipped, from a remote-only job, or from a tool that is missing.

## Findings

| Severity | Gate | Finding | Correction owner |
| --- | --- | --- | --- |
| Critical / Important / Minor | `<gate id>` | `<what failed and why it matters>` | `<canonical owner that must fix it>` |

## Unresolved approvals

- `<protected surface>`: `<what approval is missing, and from whom>`

## Verdict

`pass` when every in-scope gate returned PASS and no approval is outstanding.
Otherwise `blocked`, naming the first row above that made it so.
