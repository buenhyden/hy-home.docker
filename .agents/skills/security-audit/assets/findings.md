<!-- Output shape for a read-only security analysis. Not a stage document:
     Stage 99 owns those. It exists so a finding carries its mechanism and its
     evidence rather than a severity word on its own. -->

# Security analysis

**Change**: `<commit range or diff scope>`
**Axes covered**: trust boundaries / exposed inputs / privileges / dependencies

Every axis gets a row even when it found nothing, because an axis with no row is
one nobody looked at.

| Axis | Looked at | Result |
| --- | --- | --- |
| Trust boundaries | `<what was examined>` | findings / none / `not-assessable` |

## Findings

| Severity | Axis | Mechanism | Evidence | Owner |
| --- | --- | --- | --- | --- |
| Critical / Important / Minor | `<axis>` | `<how it could be reached and used>` | `<file:line, config key, or lock entry>` | `<who fixes it>` |

Severity follows reachability, not category. An unreachable class of issue is
`Minor` and says why it is unreachable; a reachable one is not downgraded
because it is common.

## Not assessable

- `<what could not be determined read-only, and what evidence would settle it>`

`not-assessable` is a result. It is never recorded as a pass.
