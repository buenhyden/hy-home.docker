---
title: Entrypoint README Registration Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0168-PLAN-0001
parent_ids: [SPEC-0168]
created: 2026-09-03
updated: 2026-09-03
---

# Entrypoint README Registration Plan

## Objective

Register every entrypoint README, make registration the thing that enforces the
form, and give the agent evaluation harness its own governed root.

## Dependencies

- SPEC-0167 routed `leaf.pre-commit` into the changed-profile fallback suite.
- The provider surface renderer already stamps the runtime-governance
  frontmatter for any projection path named `README.md`.
- `target_surface_delta_contract` already cross-checks declared `public_suites`
  against changed-path routing.

## Execution Sequence

1. Survey the twelve folders against the registry → six unregistered, one
   folder absent.
2. Rename `.github/INDEX.md` to `repository-surface.md` and reshape it → one
   surface map, repository README form.
3. Register the new paths in `registry.json` and `_NON_DOCS_FILES` → all
   classify.
4. Key the README section gate on profile type → measure the delta before
   changing it.
5. Author `_workspace` and `examples` READMEs; declare the two runtime
   projections and generate them.
6. Correct stale template links, the retired stage route, and the authoring
   matrix rows.
7. Move the eval harness to `evals/`, widening the manifest roots, the shell
   glob, the changed-path routing, and the wiki index together.
8. Regenerate every derived artifact from its own generator.

## Risk and Rollback

- Widening the README gate by the wrong key would have failed 195 documents.
  Measured first; the profile-typed key adds exactly one file.
- Moving a gated validator out of `scripts/` risks losing manifest coverage,
  shell linting, gate routing, and wiki indexing. Each was closed and verified
  individually; two were caught by existing contracts rather than by review.
- Rollback is `git revert` of the two commits; no runtime state changes.

## Verification

- `python3 scripts/validation/run-ci-gate.py --profile full`
- `bash evals/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions`
- `bash scripts/validation/run-agent-precommit-all-files.sh` at the approved
  final QA gate.

## Related Documents

- [Specification](spec.md)
- [Execution task](tasks/tsk-0001-entrypoint-readme-registration.md)
