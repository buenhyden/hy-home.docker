---
title: Entrypoint README Registration Task
version: 1.0.0
type: sdlc/task
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0168-TSK-0001
parent_ids: [SPEC-0168, SPEC-0168-PLAN-0001]
created: 2026-09-03
updated: 2026-09-03
---

# Entrypoint README Registration Task

## Objective

Put all twelve entrypoint folders on their registered README form and give the
agent evaluation harness a governed root.

## Inputs

- The twelve folders named in the request.
- `docs/99.templates/registry.json` profiles and `template_roles`.
- `scripts/lib/document_governance/registry.py` non-docs authority allowlist.
- `scripts/lib/document_governance/metadata/reference.py` README section gate.

## Work Log

### Survey

| Folder | Before | After |
| :--- | :--- | :--- |
| `infra` `projects` `scripts` `secrets` `tests` | `repository-readme` | unchanged |
| `.agents` | `runtime-governance-readme` | unchanged |
| `_workspace` | unregistered, no frontmatter | `repository-readme` |
| `examples` | file absent | `repository-readme` |
| `.claude` `.codex` | file absent | `runtime-governance-readme`, generated |
| `.github` | `INDEX.md`, `github-navigation-index` | `repository-surface.md`, `repository-readme` |
| `evals` | directory absent | created; `repository-readme` |

### The section gate keyed on the wrong thing

`reference.py` skipped any tracked Markdown not named `README.md`, so
`github-navigation-index` declared five required sections that nothing checked,
and a renamed README form would inherit that silence. Two candidate keys were
measured before changing it:

| Candidate key | Non-`README.md` files newly covered | Currently failing |
| :--- | ---: | ---: |
| declares `required_sections` | 468 | 195 |
| profile type is a README form | 1 | 0 |

The second was chosen. Mutation test: renaming `## Audience` to `## Readers` in
`.github/repository-surface.md` produced `readme-heading-missing`; restoring it
returned zero findings.

### Why `.github` is not `README.md`

GitHub resolves a repository's displayed README from the root, `.github/`, and
`docs/`. A `.github/README.md` would take the landing page from the root README.
The folder keeps one surface map under a name that cannot collide.

### `_workspace` documented a contract nothing implemented

The README claimed `.gitignore` ignored `_workspace/**` with two re-included
contract files. `git check-ignore` matched no rule, and no validator enforced the
tracked-file list, while `scripts/security/` and `scripts/lib/ops/` write real
artifacts under `repo-support/`. The rule was added and the claim made verifiable
in the document itself. Probe results before and after differed on exactly the
two scratch paths; both tracked READMEs stayed visible.

### Six READMEs pointed at the wrong template

Every one named `readme-stage.template.md`, which the registry maps only to
`docs/{stage}/README.md`. Corrected to the repository, documentation, or package
template per profile. A wrong pointer propagates into every README written from
it.

### The authoring matrix disagreed with the registry

Three rows: `sdlc` listed `package-readme` which is a `common` kind, `reference`
omitted `category-readme`, and `common` listed the removed `navigation-index`
while omitting the three live `*-readme` kinds. Both directions now compare
empty.

### Moving the harness surfaced three latent gaps

| Gap | Consequence if unfixed | Caught by |
| :--- | :--- | :--- |
| Manifest declaration and coverage were two `scripts/` literals | An `evals/` script could ship unregistered | Own mutation test |
| Changed-path routing had no `evals/` prefix | The eval validator would not select its own suite on a PR that changed it | `target_surface_delta_contract` |
| The LLM wiki indexed six roots, not `evals/` | The harness would vanish from the generated index | `test_exact_script_identity_excludes_transition_wrappers` |

`_workspace/` had the same routing gap for its newly enforced sections and was
routed to the document contract suites in the same change.

## Verification Evidence

| Check | Result |
| :--- | :--- |
| `run-ci-gate.py --profile full` | `EXIT=0`, 18 suites |
| `check-document-metadata.py --mode check-contracts` | `violations=0` |
| `check-script-manifest.py` | `PASS: script manifest is valid` |
| `check-target-surface-delta-contract.py --mode blocking` | `PASS` |
| `provider_surface_renderer.py --check` | `PASS providers=2 drift=0` |
| `evals/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions` | `10/10`, `14/14`, both `pass` |
| Twelve folders classified and section-complete | 12/12 |

Mutation evidence:

- Renamed required heading in `.github/repository-surface.md` → caught.
- Tracked unregistered `evals/probe-unregistered.sh` → `manifest-record-missing`.

Routing verified by calling `select_public_suites` directly: `evals/*` selects
all six suites, matching `scripts/*`; `_workspace/README.md` selects the three
document contract suites plus the fallback.

## Review Evidence

Generated artifacts were regenerated from their own generators, never
hand-edited: LLM wiki index and coverage, audit implementation matrix, security
automation readiness, and both runtime README projections.

## Commit Ledger

| Commit | Scope |
| :--- | :--- |
| `7feaab5f` | Eleven folders, registry, section gate, stale links, workspace ignore |
| `8a4ae87c` | `evals/` root, manifest roots, shell glob, routing, wiki index |

## Rulings

- The registry decides which README form applies; the filename does not. The
  gate now reflects that.
- Declaration and coverage of an automation root are one value. Two literals
  were the defect, not the width.
- Stage 90 dated observations keep their historical paths. `0074` still names
  `.github/INDEX.md` as observed on 2026-08-23, and that remains accurate for
  that date.

## Deferred Items

- `docs/99.templates/registry.json` `common.generated_outputs` names
  `check-target-surface-delta-contract.py` as the owner of `0074`, but that
  script has no write path and the document declares no `generated_by`. The
  declaration is inert.
- Stage 90 audits `0021`, `0025`, `0027` and data `0065` state exact eval
  markers of `11/11` and `16/16`; the harness reports `10/10` and `14/14`. The
  audit text is dated observation, so the numbers were left as recorded rather
  than rewritten.
- `_workspace/repo-support/README.md` remains unregistered. Only the twelve
  named folders were in scope.
- `examples/sample-web-service/site/index.html` still has no formatter, carried
  from SPEC-0166.

## Related Documents

- [Specification](../spec.md)
- [Implementation plan](../plan.md)
- [Quality standards](../../../00.agent-governance/policies/quality-standards.md)
