---
title: "Governance and QA Convergence Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0174-PLAN-0001"
parent_ids:
- "SPEC-0174"
created: "2026-09-05"
---

# Governance and QA Convergence Plan

## Objective

Execute the bounded [specification](spec.md) with test-first logical units and
explicit local/hosted evidence. Use the executing-plans workflow for this plan.

## Dependencies

- Baseline `main` and an isolated task-owned worktree.
- Stage 00 bootstrap, approval, workflow, quality, Git, and completion policies.
- Stage 99's existing Spec/Plan/Task templates; no parallel planning directory.
- PRs #140 and #141 overlapped at initial inspection and were later merged into
  `main` at `4c6d211129615eab372d720ebd209b6c27618c86`. This candidate
  preserves that upstream commit. Their branches were not modified, and their
  test conclusions are not this candidate's evidence. SPEC-0174 keeps its
  separate 0174 identity; it does not reuse the other work's 0173 namespace.

## Execution Sequence

1. Record clean baseline, open PR overlap, provider regression results, and hosted
   failure evidence in the Task. Separate snapshot-export plumbing from delivery.
2. Add failing tests to `tests/validation/test_provider_native_surfaces.py` and
   `tests/lib/agent_governance/test_agent_governance_contract.py` for removal,
   canonical Codex skill loading, and retired-path rejection. Verify failure.
3. Change `providers/registry.yaml`, the typed contract, renderer, hook guidance,
   Stage 99 runtime README route, ownership/labels, and active policy consumers.
   Remove only known tracked generated shared files; regenerate native outputs.
   Adapt safety fixtures to real remaining surfaces, removing duplicate shared
   assertions without deleting symlink, ownership, quarantine, or fail-closed tests.
4. Run provider/native/hook/contract tests, renderer `--check`, and diff hygiene.
   Commit the provider retirement and its inseparable contract/docs/tests together.
5. Reproduce QA/workflow inconsistencies. Reuse the bounded Compose-selection fix
   from PR #140/#141 after exact-diff review. Test aggregate override rejection,
   gate de-duplication, local scanner routing, and required job shape before fixes.
   Keep profile interfaces and least-privilege uploads intact; commit QA behavior
   and its regression evidence as a separate unit.
6. Consolidate shared QA instructions, conditional PR evidence, fixture scope,
   term ownership, and current-vs-historical document guidance. Move incompatible
   active historical prescriptions through the existing lifecycle contract rather
   than rewriting frozen bodies. Reuse current templates; remove obsolete routes.
7. Regenerate catalogs; run focused tests, public profile explanations, metadata,
   traceability, lifecycle, and applicable local/hosted QA. Record unavailable
   dependencies or reviews explicitly, not as passing checks.
8. Review the exact final diff, create logical commits, remove temporary snapshot
   workflow, and open a PR. Leave it draft if acceptance or review remains unmet.

## Risk and Rollback

Recover through logical `git revert` commits; never reset another worker or force
push. Preserve generated-file ownership checks. Native skill-picker behavior may
change when the shared directory is removed, so explicit canonical loading and
its limitation must be documented and tested before retirement.

## Verification

```sh
python3 -m unittest tests.validation.test_provider_native_surfaces tests.validation.test_provider_surface_renderer tests.lib.agent_governance.test_agent_governance_contract
bash scripts/operations/sync-provider-surfaces.sh --check
python3 scripts/validation/check-github-workflow-contract.py
python3 scripts/validation/run-ci-gate.py --profile changed --explain
python3 scripts/validation/check-document-links.py --mode traceability
python3 scripts/validation/check-document-corpus-lifecycle.py
python3 scripts/validation/run-ci-gate.py --profile changed
python3 scripts/validation/run-ci-gate.py --profile full
git diff --check
```

The Task owns actual command outcomes. The commands above are a verification
plan, not an assertion that every command has run or passed.

## Rulings

Retain the existing small public profile interface, canonical Stage 00/99 split,
and independent review boundary. Optimize repeated work, not check strength.
Treat the user's request as scope authorization, not as a fabricated independent
review or permission to merge, deploy, or modify repository protection.
