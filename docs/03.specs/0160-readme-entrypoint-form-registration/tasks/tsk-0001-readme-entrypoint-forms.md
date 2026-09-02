---
title: Register One Stage 99 Form per README Entrypoint Kind
version: 1.0.0
type: sdlc/task
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0160-TSK-0001
parent_ids: [SPEC-0160, SPEC-0160-PLAN-0001]
created: 2026-09-02
updated: 2026-09-02
---

# Register One Stage 99 Form per README Entrypoint Kind

## Objective

Give every README entrypoint kind one registered Stage 99 form, and extend the
Registry only as far as naming those entrypoints requires.

## Inputs

- `docs/99.templates/registry.json`
- `scripts/lib/document_governance/registry.py`
- `scripts/operations/provider_surface_renderer.py`
- the frozen legacy profile YAML, read only to measure the corpus

## Work Log

1. Measured the corpus first: 149 tracked READMEs, 68 under `docs/` and 81
   outside it, of which 78 carried no frontmatter, at path depths 0 through 4.
2. Registered the Stage 90 category index (`{audits,data,research}/README.md`)
   as `reference-category-readme` with a `{category}` path token, so one profile
   covers all three categories the way `{stage}` and `{domain}` already work.
3. Retired `spec-package-readme` and `common/readme-package.template.md`: Stage
   03 packages carry no README, so the profile reached zero documents.
4. Registered `documentation-readme` over `docs/README.md` and removed
   `repo-support`, a profile with no template, no sections, and no contract.
5. Gave the Registry a bounded non-docs vocabulary and registered
   `repository-readme` over the six repository entrypoints.
6. Added the `{subpath}` token and registered `package-readme` over the 70
   infrastructure, project, and example package READMEs.
7. Registered `runtime-governance-readme` over the projected `.agents/README.md`
   and moved its frontmatter into the renderer.

Corrections made during the work rather than carried:

| Severity | Site | Defect |
| :--- | :--- | :--- |
| blocker | `infra/04-data/analytics/README.md`, `infra/09-tooling/README.md` | Generated `title` values contained `:`, so the frontmatter failed to parse |
| high | `docs/99.templates/templates/references/*-pack.template.md` | A first draft carried live relative links; Stage 99 templates carry placeholders only |

## Verification Evidence

- `python3 scripts/validation/run-ci-gate.py --profile full` → `EXIT=0`,
  17 OK suites, 0 failures, after every one of the five steps.
- `check-document-metadata.py --mode check-contracts` → `violations=0`.
- `check-document-links.py --mode all` → `failures=0`.
- `provider_surface_renderer.py --check` → `drift=0`.
- Registry classification after the change: 145 of 149 tracked READMEs resolve
  to a registered profile, against 0 outside a handful of `docs/` routes before.

## Review Evidence

Each step was verified against the full gate before the next began, so every
commit in the ledger below is independently green and independently revertible.

## Commit Ledger

| Commit | Scope |
| :--- | :--- |
| `91ae4c6b` | Stage 90 category README form; retire the Stage 03 package README |
| `84f02be8` | Documentation-space README form; drop `repo-support` |
| `521d0efd` | Repository entrypoint README form; bounded non-docs roots |
| `edd7f790` | Package entrypoint README form; `{subpath}` token |
| `ea448d0d` | Runtime-governance entrypoint README form |

## Rulings

- Level ② (`{cat}/####-<slug>/README.md`) keeps `*-pack.template.md` and level
  ③ (`m####-*.md`) keeps `*-reference.template.md`. An earlier draft rebound
  `*-pack` to the category index; the member template pins
  `artifact_id: AUD-####-m####`, so it cannot serve a package whose identity is
  `AUD-####`, and the rebind was reverted.
- `_workspace/**` stays outside the Registry, matching
  `environment-constraints.md`, which states it is not an active stage.
- `tests/lib/README.md` and `tests/validation/README.md` stay unregistered: they
  are suite notes, not entrypoints, and inventing a six-section form for a
  two-paragraph stub would add ceremony without an owner.
- `.claude/CLAUDE.md` and the other provider instruction files stay
  frontmatter-free; only projected READMEs gained the envelope.

## Deferred Items

- The legacy transition envelope is still loaded. Its README half is now nearly
  spent — 145 of 149 READMEs resolve through the Registry — but four sections
  remain live and are consumed by six modules:

  | Legacy section | Consumers |
  | :--- | :--- |
  | `common` | `lifecycle/contract.py`, `lifecycle/promoted.py`, `metadata/identity.py` |
  | `readme_profiles` | `metadata/heading.py`, `metadata/lifecycle.py`, `metadata/profile.py` |
  | `archive_profiles` | `metadata/heading.py`, `metadata/lifecycle.py`, `metadata/profile.py` |
  | `document_families` | `metadata/profile.py` |

  Retirement means moving those four sections into `registry.json` and rewriting
  the six consumers, then deleting `_load_legacy_profiles`,
  `EXPECTED_TEMPLATE_ROLE_NAMES`, the `HistoricalDocument` constants, and the
  legacy merge in `build_registry_transition_profiles`. The source is a frozen
  Git blob, so this is a migration, not a deletion in place.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
