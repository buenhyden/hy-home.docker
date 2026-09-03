---
title: Align the Lifecycle Vocabulary with Each Role
version: 1.0.0
type: sdlc/task
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0164-TSK-0001
parent_ids: [SPEC-0164, SPEC-0164-PLAN-0001]
created: 2026-09-03
updated: 2026-09-03
---

# Align the Lifecycle Vocabulary with Each Role

## Objective

Leave every profile bound to a lifecycle it can actually reach, and every
lifecycle-bound document in a state.

## Inputs

- `docs/99.templates/registry.json`
- `scripts/lib/document_governance/metadata/reference.py`
- the tracked Markdown corpus and the 34 Markdown templates

## Work Log

Surveyed all seven lifecycles, 42 profiles, and the observed status of every
classified document before changing anything.

| Mismatch | Evidence |
| :--- | :--- |
| `runtime-projection-claude` and `-codex` declared `living` | both forbid `status`: it is neither required nor optional, so the whitelist rejects it |
| `template-source` declared `living` | `living` lacks `open`, which `incident.template.md` carries, and offers `active`, `superseded`, `retired`, which no template can be |
| `point-in-time` duplicated `living` | statuses and transitions byte-identical; applied to `audit` and `postmortem` while `data` and `research`, which require `observed_at`, were `living` |
| 51 documents carried no status | 15 of 16 governance policies, 18 of 18 hook policies, 13 of 13 operations domain READMEs, 2 of 13 `readme`, 2 of 70 package READMEs, 1 documentation README |

Templates were checked against their target's initial status: 33 of 34 matched,
and the one that did not was `claude-agent.template.md`, correct because its
profile forbids `status`.

Corrections made during the work rather than carried:

| Severity | Site | Defect |
| :--- | :--- | :--- |
| high | this Task's own change | `template-source` was first set to `lifecycle_id: null`. Its `allowed_statuses` then went empty and every template reported `invalid-status`. The existing profile-contract test caught it; the binding was corrected to a new `template` lifecycle instead of removed. |
| medium | this Task's own change | The first commit carried a validator change its message did not describe. Amended to cover both files before continuing. |
| low | this Task's own method | `lifecycle_id` cannot be absent; the schema requires the key. `null` is the shape a lifecycle-free profile uses, as `github-navigation-index` already showed. |

## Verification Evidence

- `run-ci-gate.py --profile full` -> `EXIT=0`, 18 OK suites, after each of the
  four commits.
- A template seeding `completed` reports `invalid-template-status`; one seeding
  a status outside the target lifecycle reports `template-status-invalid`.
  Before the change the full route reported neither.
- 0 lifecycle-bound documents carry no status, down from 51.
- Deleting the status from one document per profile reports
  `missing-required-key` -- five profiles tested, five reported.
- Seven lifecycles became six plus `template`; no two share a state machine.

## Review Evidence

Each step was verified against the full gate before the next began. The
`point-in-time` merge asserts machine equality inside the change, so the same
step run against a future divergence fails rather than flattens.

## Commit Ledger

| Commit | Scope |
| :--- | :--- |
| `6050c4d6` | three bindings corrected; `template` lifecycle; template status reachable |
| `f8f00663` | `point-in-time` removed as a duplicate |
| `534c7baf` | 51 documents given a state; two `infra/` envelopes completed |
| `2e710b1d` | `status` required wherever a lifecycle is declared |

## Rulings

- `execution` keeps `draft -> completed`. Six of seven Tasks used it and none
  was ever `active`, so removing the edge would retroactively invalidate the
  repository's own practice. The asymmetry with `spec-package`, which requires
  passing through `active`, is reported rather than resolved.
- `retired`, `blocked`, `cancelled`, and `rejected` are never used by any
  document. They are legitimate states that have not occurred, not dead
  vocabulary, and are kept.
- `historical` keeps `draft` although no migration or tombstone has ever been
  one. A ledger is authored before it is committed as complete.

## Deferred Items

- `invalid-template-placeholder` reports 35 templates that carry a concrete
  `layer`. This is the rule being wrong, not the templates: a Spec template's
  layer is always `specs`, and only one generic README template varies. The
  rule demands a placeholder registered for one template from all of them. The
  template-source skip withholds it, and the narrowed skip in `6050c4d6` still
  does.
- Record-level frontmatter validation covers `docs/` only -- 593 records, all
  under `docs/`. The 70 package READMEs, 6 repository READMEs, and the runtime
  governance README outside `docs/` receive section checks but no frontmatter
  checks, which is why two `infra/` READMEs carried a one-key envelope
  unreported.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
