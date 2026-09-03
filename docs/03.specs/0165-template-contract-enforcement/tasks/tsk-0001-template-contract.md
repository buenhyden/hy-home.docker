---
title: Correct and Enforce the Template Contract
version: 1.0.0
type: sdlc/task
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0165-TSK-0001
parent_ids: [SPEC-0165, SPEC-0165-PLAN-0001]
created: 2026-09-03
updated: 2026-09-03
---

# Correct and Enforce the Template Contract

## Objective

Leave no template rule unreachable and no correct template reported.

## Inputs

- `scripts/lib/document_governance/metadata/heading.py` and `reference.py`
- `docs/99.templates/registry.json` and its schema
- the 34 Markdown templates and the catalog

## Work Log

Opening the excluded route produced 36 findings. Grouped by cause:

| Count | Finding | Cause |
| ---: | :--- | :--- |
| 22 | `layer must use the Stage 99 placeholder` | the rule demanded a placeholder from every template for any key that has one |
| 12 | `parent_ids must be a placeholder list` | the exemption tested each profile's `forbidden` list, which no profile populates |
| 1 | `name must use the Stage 99 placeholder` | the hook-policy template uses `<hook-slug>`, itself a registered placeholder |
| 1 | `README source metadata must match ...` | a special case froze the readme template at a two-key envelope it has outgrown |

Placeholder usage measured across all 34 templates before deciding:

| Key | Uses the placeholder | Concrete | Absent |
| :--- | ---: | ---: | ---: |
| `title` | 33 | 0 | 1 |
| `owner` | 33 | 0 | 1 |
| `layer` | 1 | 22 | 11 |

Only `title` and `owner` are fixed by no profile, so only those two are
required to render as placeholders. The single absence in each is the
provider-owned Claude agent template, whose profile forbids the key.

Section coverage was checked separately: 0 of 34 templates are missing a
required section from their target profile.

The catalog was in sync -- 38 roles, 38 rows, every row pointing at the
registered source -- and nothing verified it. Deleting a row passed both the
metadata and link validators.

Corrections made during the work rather than carried:

| Severity | Site | Defect |
| :--- | :--- | :--- |
| medium | this Task's own change | The first catalog rule reported the fixture repository, which holds 38 template sources but no catalog. The fixture now copies the catalog, derived from `template_catalog` rather than hardcoded. |
| medium | this Task's own test | The negative fixture wrote only the stripped catalog, so the rule governed nothing and the test passed for the wrong reason. It now places the omitted template on disk. |
| low | this Task's own method | A probe ran the checker twice per case and timed out. Reduced to one run per case. |

## Verification Evidence

- `run-ci-gate.py --profile full` -> `EXIT=0`, 18 OK suites, after both commits.
- With the exclusion removed, 34 templates report 0 findings, down from 36.
- Each corrected rule still reports: a concrete `title` and a concrete `owner`
  report `invalid-template-placeholder`; `<bogus>` as a layer reports as an
  unregistered placeholder, a check that did not exist before; `parent_ids`
  added to a profile that does not declare it reports `type-inappropriate-key`;
  a template seeding `completed` reports `invalid-template-status`.
- A concrete `layer` no longer reports.
- Dropping one catalog row reports `template-catalog-unlisted` naming the role.

## Review Evidence

Each step was verified against the full gate before the next began. Every
corrected rule was tested in both directions, so a correction that silenced a
rule outright would have failed its own test.

## Commit Ledger

| Commit | Scope |
| :--- | :--- |
| `4984bfe4` | three misfiring rules corrected; exclusion removed |
| `7f96d430` | catalog registered and enforced |

## Rulings

- The `layer` placeholder was not deleted from the vocabulary. It stays as the
  document-side forbidden token while ceasing to be demanded of templates,
  because the one list was serving two opposite purposes.
- The reverse catalog direction is not added. A row pointing at a deleted
  template already fails `missing-link-target`, the same split the package
  index rule uses.

## Deferred Items

- The `readme` profile's `layer` varies by stage, and nothing requires its
  template to keep `<layer>` now that `layer` is not a required placeholder.
  Enforcing that would need the Registry to record which keys a profile fixes.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
