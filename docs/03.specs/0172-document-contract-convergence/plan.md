---
title: "Document Contract Convergence Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "specs"
artifact_id: "SPEC-0172-PLAN-0001"
parent_ids:
- "SPEC-0172"
created: "2026-09-04"
---

# Document Contract Convergence Plan

## Objective

Converge document authority, Registry, schemas, templates, validators, tests,
README guidance, and active authored documents; integrate through a feature
branch and PR; retain bounded external observations without runtime or
archive-body mutation.

## Dependencies

- REQ-0024, AD-0027, and ADR-0029 own the governance authority split.
- REQ-0026, AD-0030, and ADR-0031 own retention and frozen preservation.
- Stage 99 allocates SPEC-0172 above high-water without ID reuse.
- CODEOWNERS supplies ownership; Stage 00, Stage 99, and scripts are protected
  surfaces requiring focused validation and review evidence.

## Execution Sequence

1. Record safety state, baseline gates, current owners, and the corpus gap matrix.
2. Update durable Requirement and Architecture owners where current obligations
   or component boundaries are incomplete or contradictory.
3. Replace duplicate Registry classifier fields with stable `id`-to-`type` mapping;
   close schema responsibilities while preserving allocation and extensions.
4. Normalize registered templates and align the single human catalog.
5. Update Registry consumers and focused positive/negative tests.
6. Migrate active prose and authored metadata; do not rewrite preserved bodies.
7. Run focused, changed, traceability, lifecycle, full, diff, and status checks;
   record observed evidence and limitations in the Task.
8. Run independent policy and exact-diff reviews; correct blocking findings and
   repeat the affected gates and reviews.
9. Commit the initial lifecycle entry, push the feature branch, open a PR, and
   observe Hosted CI without bypassing checks. If an existing public gate fails,
   reproduce it and apply only the minimum dependency, lockfile, build-time
   compiler-path, registered CI-tool provisioning, or pinned format-hook
   normalization or exact lint-conformance correction before rerunning the same
   gate. Preserve the entry state
   through the first merge; record forward transitions in post-merge follow-up
   changes.
10. Record provider, runtime, and branch-protection observations separately from
    acceptance. Stop before any mutation whose target, desired state, recovery,
    tag version, release scope, or merge authority is not exact.

## Risk and Rollback

- Keep patches reviewable; recover with a targeted inverse patch or normal
  `git revert` after commit, never reset or clean.
- Inventory active provenance before closing the grammar.
- Do not run a formatter until frozen-path ignore coverage is proven.
- Compare full-gate results with the clean pre-change baseline.
- Do not replace configured required-check contexts until the PR exposes the
  actual Hosted CI context names and a recovery path is recorded.
- A reachable Docker daemon is not a deployment target. No runtime mutation is
  attempted without a named stack, change set, observation plan, and rollback.

## Verification

- Focused document-governance unit and mutation tests.
- `python3 scripts/validation/run-ci-gate.py --profile changed`.
- `python3 scripts/validation/check-document-links.py --mode traceability`.
- `python3 scripts/validation/check-document-corpus-lifecycle.py`.
- `python3 scripts/validation/run-ci-gate.py --profile full`.
- `git diff --check`, unstaged diff, staged diff, and status.
- Independent rules-engineer and code-reviewer verdicts.
- Feature-branch Hosted CI and current branch-protection context comparison.
- Storybook clean install, `npm ls --all`, tracked high-severity audit, lint,
  typecheck, and production build; Hosted default build and browser coverage.
- Required-job `setup-uv` parity, immutable action provenance, and Hosted
  `zizmor` completion without PR-job permission expansion.
- Ruff 0.15.12 and markdownlint-cli2 0.22.1 checks plus focused behavior tests
  for the exact 12-Python and one-Markdown format-hook set reported by Hosted
  CI.
- Hadolint v2.14.0 on the exact sample-service Dockerfile reported by Hosted CI;
  verify the healthcheck command and arguments remain equivalent.

## Rulings

- Reuse ADR-0029; do not create a parallel authority ADR.
- Preserve ADR-0031's frozen archive body decision.
- Select Release Record behavior from actual evidence consumers.
- Do not claim hosted, provider, cluster, or deployment acceptance from tracked
  configuration or read-only reachability alone.

## Related Documents

- [Specification](spec.md)
- [Execution task](tasks/tsk-0001-document-contract-convergence.md)
