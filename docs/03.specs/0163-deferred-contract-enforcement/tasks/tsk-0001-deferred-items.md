---
title: Resolve the SPEC-0162 Deferred Items
version: 1.0.0
type: sdlc/task
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0163-TSK-0001
parent_ids: [SPEC-0163, SPEC-0163-PLAN-0001]
created: 2026-09-03
updated: 2026-09-03
---

# Resolve the SPEC-0162 Deferred Items

## Objective

Leave no SPEC-0162 deferred item unresolved, and no resolution asserted without
a negative test.

## Inputs

- `scripts/lib/document_governance/metadata/reference.py`
- `scripts/lib/document_governance/metadata/lifecycle.py`
- `scripts/lib/document_governance/archive.py` and `lifecycle/recovery.py`
- `scripts/validation/generate-audit-implementation-matrix.sh`
- the Stage 99 Registry and the tracked README corpus

## Work Log

### README section skip

Measured coverage before touching it by deleting a required heading from one
document per profile:

| Profile | Documents | Reported before |
| :--- | ---: | :--- |
| `readme` | 13 | yes |
| `package-readme` | 70 | no |
| `operations-domain-readme` | 13 | no |
| `repository-readme` | 6 | no |
| `reference-category-readme` | 3 | no |
| `documentation-readme` | 1 | no |
| `audit` / `data` / `research` | 37 | no |

The skip existed because the check read the `readme` profile's list rather than
the document's own, so applying it to everything would have enforced the wrong
contract. Reading the classified profile fixes the skip and its cause together.

131 documents came under the check with 2 failures, both real and both fixed
first so the enforcement commit lands green.

### globally_forbidden

The contract named three retired keys and decided nothing: it was read only to
pick a code inside a loop gated on each profile's `forbidden` list, which no
profile declares. `forbidden-key` appears once in the repository, in that dead
branch, and no test asserted it.

The keys were still rejected, by a separate whitelist, as undeclared. The
contract was therefore redundant rather than merely inert. Enforcement was
chosen over deletion because the whitelist reports a retired key and a typo
identically, and the declaration is what distinguishes them.

### Stage 98 disposition

| Measurement | Value |
| :--- | :--- |
| Tombstones | 83, 598-1373 bytes, 63 KB total |
| Tombstone contract | five pointer sections, no body |
| Migration ledgers | 3, `source_path -> target_path -> recovery_commit` rows |
| Largest ledger | 905 mapping rows |

No archive body duplicates a canonical owner. The question resolved as no
defect, but testing whether the invariant is enforced surfaced one: a body
pasted into a tombstone failed as `internal-error: lifecycle operation failed
safely` with exit 3, because a bare `except Exception` flattened a precise
ValueError that already named the file.

Corrections made during the work rather than carried:

| Severity | Site | Defect |
| :--- | :--- | :--- |
| medium | this Task's own method | A first probe deleted `## Overview` from an audit package README and read the silence as a coverage gap. The `audit` profile does not require `Overview`. Retested against `Criteria`, which it does require. |
| low | this Task's own method | The gate pins entrypoint identity to the tracked object, so a modified generator fails `ci-gate-entrypoint-identity` until staged. Measured, not worked around. |

## Verification Evidence

- `run-ci-gate.py --profile full` -> `EXIT=0`, 18 OK suites, after each of the
  four commits.
- Section check: nine profiles that declare sections each report
  `readme-heading-missing` when a required heading is deleted; before the
  change only `readme` did. 0 of 149 tracked READMEs are missing a required
  section.
- Forbidden keys: `links`, `document_type`, and `template_type` each report
  `forbidden-key: key is forbidden repository-wide`; `bogus_key` still reports
  `type-inappropriate-key: key is not declared`.
- Archive: a body pasted into a tombstone reports `archive-contract-invalid`
  naming the file, exit 1. The intact archive loads 3 migrations, 83
  tombstones, 229 decisions, 317 recovery rows.

## Review Evidence

Every step was verified against the full gate before the next began. Each
contract was tested in both directions: the violating case must be reported and
the conforming case must not.

## Commit Ledger

| Commit | Scope |
| :--- | :--- |
| `a6db986d` | the two READMEs that fail once the section check covers them |
| `7e6327a6` | README sections read from the classified profile |
| `35a66168` | `globally_forbidden` joins each profile's forbidden set |
| `39aacccb` | archive contract violations become findings that name the file |

## Rulings

- The `data` profile's section contract was applied to the audit implementation
  matrix generator rather than the reverse. 17 of 18 data packages already
  conformed, so the generator was the outlier, not the contract.
- Two of the generator's six new sections are renames of sections whose content
  already was the registered section, `Sources` to `Provenance` and
  `Maintenance` to `Refresh`. The four genuinely new sections state only facts
  the generator already holds.
- The 66 archive raise sites other than the tombstone parse keep plain
  ValueError. They fall back to reporting the archive root, which is still a
  finding rather than an internal error.

## Deferred Items

None. Every SPEC-0162 deferred item is resolved here.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
