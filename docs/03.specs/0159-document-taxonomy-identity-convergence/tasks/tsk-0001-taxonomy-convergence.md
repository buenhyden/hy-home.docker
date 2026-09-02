---
title: Converge Document Taxonomy, Envelope, and Template Layout
version: 1.0.0
type: sdlc/task
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0159-TSK-0001
parent_ids: [SPEC-0159, SPEC-0159-PLAN-0001]
created: 2026-09-02
updated: 2026-09-02
---

# Converge Document Taxonomy, Envelope, and Template Layout

## Objective

Execute the plan: one `family/kind` taxonomy, a stage-scoped `layer`, a required
`version`, a Registry-matching Stage 99 layout, and one template catalog.

## Inputs

- SPEC-0159 and its Plan.
- The Stage 99 Registry and the registered document-contract gate.
- The uncommitted in-flight change that had placed an unquoted `#.#.#`
  placeholder in nineteen templates.

## Work Log

1. Established the baseline: the gate failed with 5 failures because
   `version: #.#.#` parses as YAML null.
2. Retyped 366 documents and relayered 165 onto the Registry taxonomy.
3. Moved and renamed the Stage 99 template sources, added the six governance
   forms, the two runtime forms, the three README forms, and
   `specs/contracts/data-model.template.md`.
4. Rebuilt `template_roles` from one mapping so each profile binds one role.
5. Promoted `version` to required on every managed profile except the two
   provider-owned runtime projections, and set `1.0.0` on 548 documents.
6. Removed `layer` from 87 Stage 00 and Stage 99 documents and from the Stage 00
   governance profiles, so a declared layer now fails closed there.
7. Consolidated the three per-category Stage 99 catalogs into
   `templates/README.md`.
8. Reconciled the docs index Structure and Routing tables with the Registry path
   patterns.

Defects repaired at their cause rather than by relaxing a contract:

| Severity | Site | Defect |
| :--- | :--- | :--- |
| blocker | Stage 99 templates | `#` opens a YAML comment, so the version placeholder parsed as null |
| blocker | `scripts/lib/document_governance/metadata/heading.py` | Heading enforcement routed on `template_id`, so a profile that gained a template lost its section contract |
| high | `scripts/lib/document_governance/metadata/profile.py` | `_registry_path_glob` did not translate `{hook_slug}` |
| medium | `scripts/lib/document_governance/metadata/profile.py` | Stage 00 governance profiles were classified as typed SDLC targets |
| medium | `.github/INDEX.md` | Retired `profile_id` key in place of `type` |
| medium | `docs/README.md` | No frontmatter, and an incident route that contradicted the Registry |

## Verification Evidence

- Baseline: `run-ci-gate.py --profile full` → 5 failures, all from the null
  version placeholder.
- After each step the same command was rerun; the final run exits 0 with 18 OK
  suites, 0 FAILED, and 0 test failures.
- `check-document-metadata.py --mode check-contracts` → `violations=0`.
- `check-document-links.py --mode all` → `failures=0`.
- `provider_surface_renderer.py --check` → `drift=0`.
- Corpus assertions: 0 documents missing `version`, 0 non-semver values, 0
  Stage 00 or Stage 99 documents declaring `layer`, 0 retired keys, 0 titles
  repeating their `artifact_id`, 0 duplicate domain identity keys.

## Review Evidence

Self-review against the Plan's risk table. Each surfaced failure was traced to a
cause before any contract was changed; no required frontmatter key or section
was removed to make the gate pass. The three frozen Stage 98 migrations were
repinned only after each body was verified byte-identical to its predecessor
blob, with the delta confirmed as the single added `version` line.

## Commit Ledger

| Commit | Scope |
| :--- | :--- |
| `d20254f5` | Converge document type, layer, and Stage 99 template taxonomy |
| `68ed869b` | Require `version` and scope `layer` to Stages 01-98 |
| `f038de00` | Consolidate Stage 99 catalogs into one template README |

## Rulings

- Existing documents received `version: 1.0.0` rather than a status-derived
  value; inventing a `0.x` convention was outside the request.
- Stage 99's own documents use no `layer`; template sources keep the layer of
  the stage they author into.
- `templates/operations/README.md` was removed rather than rewritten: its
  subject and handoff rules restated Stage 05 authority.

## Deferred Items

- The legacy transition layer in `scripts/lib/document_governance/` is still
  loaded at run time by `lifecycle/contract.py` and is not retired here; it
  needs its own bounded package.
- The Graphify report is built from an earlier commit and remains advisory, as
  the bootstrap policy already provides for.
