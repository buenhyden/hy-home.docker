---
title: Retire the Legacy Profile Layer
version: 1.0.0
type: sdlc/task
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0161-TSK-0001
parent_ids: [SPEC-0161, SPEC-0161-PLAN-0001]
created: 2026-09-03
updated: 2026-09-03
---

# Retire the Legacy Profile Layer

## Objective

Leave `registry.json` as the only profile authority, with no behavior change for
any document the corpus contains.

## Inputs

- `scripts/lib/document_governance/metadata/profile.py`
- `scripts/lib/document_governance/registry.py`
- `docs/99.templates/registry.json` and its schema
- the frozen blob `49406580:docs/99.templates/support/document-metadata-profiles.yaml`

## Work Log

Measured reach over one full gate run before touching anything:

| Legacy surface | Reads | Disposition |
| :--- | ---: | :--- |
| `document_families` | 1689 | derived from `registry.profiles` |
| `build_registry_transition_profiles` | 76 | replaced by `build_registry_profiles` |
| `_load_legacy_profiles` | 7 | deleted |
| `matching_readme_profiles` | 5 | one consumer repointed, rest deleted |
| `matching_archive_profiles` | 0 | deleted |

Then retired them in ascending order of reach, one commit per section.

Corrections made during the work rather than carried:

| Severity | Site | Defect |
| :--- | :--- | :--- |
| blocker | this Task's own method | A first probe used an environment variable, which the gate strips (`ci_gate_contract.py:1230`). It reported the whole layer unreachable. Caught before acting on it, because a test that provably calls the loader recorded nothing. Every later probe writes to a fixed path and is self-tested. |
| blocker | `metadata/profile.py` | A constant removal used the next blank-line run as its end boundary and swallowed `CREDENTIAL_KEY_NAME` and eleven other constants; redone with exact AST spans |
| high | `metadata/profile.py` | `load_registry` returns nested `mappingproxy`, which `copy.deepcopy` cannot pickle, so `common` needed `_thaw` rather than a deep copy |

## Verification Evidence

- `run-ci-gate.py --profile full` -> `EXIT=0`, 17 OK suites, 0 failures, after
  each of the five commits.
- Step 1 equivalence: the Registry declares no `archive` profile, and Stage 98
  documents classify as `migration`, `readme`, or `tombstone`.
- Step 3 equivalence: the Registry-derived typed-target set is the previous set
  minus exactly `archive`, `interface-requirement`, `prd`, `reference`, `srs` —
  the five legacy-only profiles measured at 0 documents over 755 tracked files.
- `check-document-corpus-lifecycle.py` -> `violations=0`, recovery `violations=0`.

## Review Evidence

Each step was verified against the full gate before the next began, so every
commit in the ledger is independently green and independently revertible.

## Commit Ledger

| Commit | Scope |
| :--- | :--- |
| `3e1d0bb3` | `archive_profiles` and its unreachable routing |
| `99de0477` | `readme_profiles`; the live consumer reads the Registry |
| `b7ff9ecc` | `document_families`; typed targets derive from the Registry |
| `5c03496d` | `common` moved into `registry.json`; envelope built from the Registry |
| `b75e501f` | the loader itself, and the constants that only validated it |

## Rulings

- `common` moved verbatim. Its members include stale entries — `typed_keys` and
  `frontmatter_order` still list the retired `artifact_type`, and
  `globally_forbidden` still lists `type` and `owner`, which are now required —
  but correcting them inside a move would hide a behavior change in a
  relocation. That cleanup is its own step.
- Three tests asserted the retired behavior rather than a contract worth
  keeping: one read `adapted["_legacy_profiles"]`, one expected a legacy `prd`
  route to classify, and one expected an unclassifiable README. All three now
  state the post-retirement contract, and the change is named in each commit.
- `docs/99.templates/support/document-metadata-profiles.yaml` stays in the
  retired-path list. It is a historical record of a path that once existed.

## Deferred Items

- The `common` contract's stale members are unreviewed: `artifact_type` in
  `typed_keys` and `frontmatter_order`, and `type` and `owner` in
  `globally_forbidden`. They are now editable in `registry.json` rather than
  frozen in a Git blob, which is what this package set out to achieve.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
