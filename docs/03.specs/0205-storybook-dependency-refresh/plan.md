---
title: "Storybook Dependency Refresh Plan"
version: "0.1.2"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0205-PLAN-0001"
parent_ids:
- "SPEC-0205"
created: "2026-10-03"
---

# Storybook Dependency Refresh Plan

## Objective

Apply the user-requested latest compatible Storybook package update in one
isolated branch after this Spec Package and exact Task are approved.

## Dependencies

- Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; recheck main before source edit.
- Official [Storybook 10.6 release](https://storybook.js.org/releases/10.6),
  [10.6.1 release](https://github.com/storybookjs/storybook/releases/tag/v10.6.1),
  [Next.js Vite framework](https://storybook.js.org/docs/get-started/frameworks/nextjs-vite/),
  npm registry dist-tags/peer ranges checked on 2026-10-03.
- Existing Dependabot TS 7 exclusion and the unpatched
  [braces advisory](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm).
- No HOME, remote push/PR/merge or deployment approval is inferred.

## Execution Sequence

1. **W1: freeze targets.** Compare current main, package manifest/lock, npm
   latest stable dist-tags, peer dependencies and the existing CI owner.
   Covers acceptance 1.
2. **W2: update graph.** Change only Task-owned npm files; refresh lockfile
   with a task-local cache and install without unreviewed lifecycle scripts.
   Confirm exact resolved train and peers. Covers acceptance 2.
3. **W3: verify and review.** Run scoped install, lint, typecheck, Next build,
   Storybook build, Vitest browser coverage, Storybook contract checker, npm
   audit and diff review. Record failures and advisory path without bypass.
   Covers acceptance 3-4.

## Risk and Rollback

| Risk | Control |
| --- | --- |
| Peer mismatch or Next/Vite behavior change | Fail on npm resolution and build; revert only Task-owned manifest/lock. |
| Browser test cannot run locally | Mark that check NOT_RUN/BLOCKED, retain static results; do not claim full acceptance. |
| `braces` high advisory remains | Preserve failed security gate and user's held-merge decision; no exception or override. |
| Concurrent SPEC-0204 ID allocation | Keep this package at SPEC-0205 and reconcile registry serially before any integration. |

## Verification

Use repository-owned npm commands and `scripts/validation/check-storybook-contract.sh`.
Run document metadata/link/lifecycle and registry checks for the Spec diff.
Select path-aware gates; do not repeat the full public gate solely because a
package version changed. Commit only after required checks and approval; remote
operations remain separate.

## Rulings

Do not add Storybook services or move its project. Do not upgrade to Storybook
11 alpha or TypeScript 7. Keep Dependabot as npm update owner. The unpatched
advisory blocks the previously requested remote merge.
