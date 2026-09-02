---
title: README Entrypoint Form Registration Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0160-PLAN-0001
parent_ids: [SPEC-0160]
created: 2026-09-02
updated: 2026-09-02
---

# README Entrypoint Form Registration Plan

## Objective

Register one Stage 99 form per README entrypoint kind, in five reviewable
increments that each leave the gate green.

## Dependencies

- SPEC-0159 completed the type, layer, identity, and template-layout convergence.
- The Registry schema and its validators own every rule this plan changes.

## Execution Sequence

1. Stage 90 category index: add the `{category}` token, the
   `reference-category-readme` profile, and its form; retire
   `spec-package-readme` because Stage 03 packages carry no README.
2. Documentation space: add `documentation-readme` over `docs/README.md` and
   remove the contract-free `repo-support` profile it supersedes.
3. Repository entrypoints: give the Registry a bounded non-docs root allowlist,
   register `repository-readme`, and narrow the target-surface invariant.
4. Package entrypoints: add the `{subpath}` token and register `package-readme`
   over the infrastructure, project, and example trees.
5. Runtime-governance entrypoint: register `runtime-governance-readme` and have
   the provider surface renderer emit its frontmatter.

## Risk and Rollback

Each step is one commit with a green gate, so any step reverts alone. The
highest-risk step is 3: it moves an architectural boundary that a test asserted.
That test was narrowed rather than deleted, so the boundary still fails closed
everywhere outside the registered entrypoint forms.

## Verification

`python3 scripts/validation/run-ci-gate.py --profile full` after every step.

## Related Documents

- [Specification](./spec.md)
- [Task](./tasks/tsk-0001-readme-entrypoint-forms.md)
