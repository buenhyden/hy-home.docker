---
title: Close the Validation Blind Spots
version: 1.0.0
type: sdlc/task
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0162-TSK-0001
parent_ids: [SPEC-0162, SPEC-0162-PLAN-0001]
created: 2026-09-03
updated: 2026-09-03
---

# Close the Validation Blind Spots

## Objective

Make every rule the gate declares reachable in the route the repository runs,
and register the one rule the corpus stated only in prose.

## Inputs

- `scripts/lib/document_governance/metadata/reference.py`
- `scripts/lib/document_governance/registry.py`
- `docs/99.templates/registry.json` and its schema
- the tracked document corpus and Git history as measurement sources

## Work Log

Three rules were declared and could not fire. Each was confirmed by applying the
exact defect it claims to catch and observing that nothing was reported.

| Rule | Why it was silent | Evidence before the fix |
| :--- | :--- | :--- |
| `invalid-status` | gated on `status == "active"`, and a document with a status outside its lifecycle is by definition not active | a bogus status on a provider README reported `violations=0` |
| `template-placeholder-in-target` | `common.template_placeholders` held the legacy vocabulary; the intersection with the tokens templates declare was empty | ten hook policies shipped `title: "<title>"` past a green gate |
| `invalid-transition` | fires only when a record carries `previous_status`, and the `check-contracts` route collected records with no predecessor | `completed -> active` on a completed Spec gave `run-ci-gate.py --profile full` `EXIT=0` |

Measured outcomes:

| Step | Measurement |
| :--- | :--- |
| index resync | mismatched rows 1 and absent rows 3 to 0 |
| hook placeholders | residual placeholders 10 to 0 |
| README lifecycles | profiles allowing a status with no lifecycle 6 to 0 |
| authority duplication | identity restatements 25 to 1; key restatements 22 to 11 |
| `invalid-status` | records validated 427 to 587, new violations 0 |
| placeholder vocabulary | declared and used token intersection 0 to 20 of 20 |
| `invalid-transition` | unreachable to reachable from `--profile full` |
| index contract | governed documents 0 to 62 |

For `invalid-status`, three filter variants were measured before choosing:
dropping the filter outright produced 118 findings, all Stage 99 template
placeholders; skipping template sources produced 0. The second was applied.

Corrections made during the work rather than carried:

| Severity | Site | Defect |
| :--- | :--- | :--- |
| blocker | this Task's own method | The first transition probe attributed a deleted file's `-status:` lines to the previously seen path, inflating 11 real events to 14 and misclassifying a rename-with-edit. Found by a self-test, not by review. Every later probe carries a known-positive and a known-negative case. |
| high | this Task's own output | An interim report said six historical transitions were illegal. Six of the seven predate the `spec-package` lifecycle, which is absent at `4e2e71cc`. One, SPEC-0154 at `aff97225`, violated a rule already in force. The count and its meaning were corrected. |
| high | this Task's own change | `index-member-unpatterned` was written, then measured unreachable: the schema already requires `path_pattern`, so `validate_registry` returns at `schema-invalid` first. It was removed rather than shipped. |
| medium | this Task's own report | A template carrying `status: open` was first counted as a status-membership violation. `heading.py:122` validates a template against its target profile's initial status, and the incident lifecycle starts at `open`. The real count is 0. |

## Verification Evidence

- `run-ci-gate.py --profile full` -> `EXIT=0`, 18 OK suites, after every commit.
- `invalid-status`: `status: bogus-state` on the provider index README is now
  reported; before the change the same edit reported `violations=0`.
- `template-placeholder-in-target`: restoring `title: "<title>"` on
  `hookify.warn-branch-naming.md` is now reported.
- `invalid-transition`: `completed -> active` on SPEC-0093 is now reported by
  `--mode check-contracts --history-scope full`; `draft -> active` on the
  SPEC-0156 Task is not, so the rule does not over-fire.
- `index-member-unlisted`: one row removed from each of the four registered
  indexes is reported, four times out of four; the clean tree reports 0.
- Template rename: pointing a role source at the old path reports
  `template-source-missing`, so no consumer could be missed silently.
- `check-document-links.py --mode all` -> 588 documents, 4454 links, 0 failures.
- `check-document-corpus-lifecycle.py` -> `violations=0`, recovery
  `violations=0`.

## Review Evidence

Every step was verified against the full gate before the next began, so each
commit in the ledger is independently green and independently revertible. Each
repaired rule was tested in both directions: the illegal case must be reported
and the legal case must not.

## Commit Ledger

| Commit | Scope |
| :--- | :--- |
| `b7ae4b26` | Stage 03 package index resynchronized |
| `156980fc` | unreplaced `<title>` in ten hook policies |
| `df415cb4` | six README profiles bound to a lifecycle |
| `9063c93e` | stale members of the shared `common` contract |
| `85121e1f` | policy prose stops restating the machine contract |
| `fb77c037` | record validation no longer gates on the status being correct |
| `b7b7c37d` | placeholder check points at the vocabulary templates use |
| `a46635f4` | the transition rule receives a committed predecessor |
| `eb9918bf` | Stage 90 member templates named after their roles |
| `2505b86a` | index contract registered and the missing direction enforced |

## Rulings

- History is not validated. The `spec-package` lifecycle is absent at
  `4e2e71cc`, so six of the seven `completed -> active` moves predate the
  contract that would judge them. Judging past events by a later contract would
  make the gate permanently red for facts that cannot be repaired.
- The three `archived -> completed` moves on Stage 98 documents are repairs of a
  status the `historical` lifecycle never defined, already excused by
  `repairs_undefined_previous`.
- The stale index direction was not implemented, because measurement showed it
  is already covered: a row pointing at a deleted package fails
  `missing-link-target`.
- AUD-0023 stays outside the index rule because it is already listed in
  `common.inventory_excludes`. That is an existing decision, not a new
  exemption.
- Full-profile transition checking runs without `transition_overrides`, so an
  override recorded for `check-changed` does not apply there. No override exists
  in this repository, so the difference is currently unobservable.

## Deferred Items

- `reference.py` skips the README section-heading check for any README whose
  profile is not exactly `readme`, and the comment justifying the skip cites the
  legacy corpus retired by SPEC-0161. The comment is stale and the skip is
  unreviewed.
- `common.globally_forbidden` is inert. The executed check reads each profile's
  own `forbidden` list, which no profile populates. Its incorrect members were
  removed, but the list still enforces nothing.
- `docs/98.archive` holds 83 tombstones and 3 migration ledgers. This is
  consistent with the repository's own archive policy, which authorizes the
  recovery commit recorded in a tombstone. It is reported because an external
  brief treated any archive body as a duplicate authority; no change was made.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
