---
title: "Storybook Dependency Refresh Specification"
version: "0.1.1"
type: "sdlc/spec"
status: "review"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0205"
parent_ids:
- "REQ-0027"
- "AD-0031"
- "SPEC-0201"
created: "2026-10-03"
---

# Storybook Dependency Refresh Specification

## Overview

Refresh the existing shared Storybook Next.js workspace to current compatible
stable packages. The 2026-10-03 baseline is `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`.
The user requested source updates; this draft records the exact package and
verification contract before source modification. It does not move or deploy
Storybook, merge a branch, or waive the held high-severity npm advisory.

## Boundaries and Inputs

Own only `projects/storybook/nextjs/package.json` and `package-lock.json` for
the dependency change. The existing `.storybook/`, Vitest, ESLint, Next.js,
CI and Dependabot declarations are compatibility inputs; edit one only if a
focused failing check proves it necessary and an amended Task names the file.
Reuse REQ-0027 version ownership, AD-0031's Dependabot ownership and SPEC-0201's
05 handoff. The separate SPEC-0204 approval draft retains its reserved ID and
its infrastructure scope.

## Behavior Contract

1. Pin the seven Storybook train declarations (`storybook`, framework, four
   addons, ESLint plugin) to compatible stable `10.6.1`. Keep the lockfile
   resolved to the same train; no alpha/canary package enters the graph.
2. Update directly related compatible packages to npm's verified stable
   versions: Chromatic addon `5.4.0`, Next.js and ESLint config `16.3.8`,
   Vitest/browser/browser-playwright/coverage `5.0.3`, Vite `8.3.2`, ESLint
   `10.12.0`, Node types `26.6.4`, and Tailwind declaration `4.3.3`.
   React, React DOM, their types, PostCSS, Playwright and addon-designs are
   already at their latest verified stable versions and retain their contracts.
3. TypeScript stays at `6.0.3`: the existing Dependabot exclusion records a
   TypeScript 7 / typescript-eslint incompatibility. A new compatibility
   result and separate scoped Task are required before changing it.
4. `npm ci`, lint, typecheck, Next build, Storybook build and Storybook Vitest
   browser coverage use this repository's existing scripts and pass, or record
   a specific blocked/failing reason. Do not weaken the 90% coverage threshold.
5. The npm audit reports every high/critical result. `braces@3.0.3` currently
   has no patched release in the official advisory; neither lock refresh nor
   Storybook upgrade may be reported as its fix. Preserve the user's decision
   to hold remote merge while that advisory has no patch.

## Technical Approach

Read official Storybook and npm registry stable tags and peer ranges; update
the two npm files together using the installed npm version. Use current
Dependabot ownership rather than adding a second npm updater. Run existing
path-aware and frontend checks. Recheck the resolved graph, then record exact
commands and exits in TSK-0001. Make no generated tech-stack version edit:
that projection covers infrastructure image declarations, not Storybook npm.

## Interfaces and Data

Input: tracked manifest/lock, official stable dist-tags and peer dependencies,
existing Storybook configuration and synthetic local build/test fixtures.
Output: reviewed manifest/lock versions and Task verification evidence.
No secrets, HOME data, user browser sessions or deployed service state are inputs.

## Failure Modes and Guardrails

Reject mismatched Storybook train packages, peer-resolution overrides, an
unplanned major upgrade, install scripts with unreviewed effects, and a lockfile
that differs from the manifest. Stop on failed build, browser coverage, or new
security finding; diagnose the exact dependency path without `npm audit fix
--force`, a blanket override, or lowering the audit gate. Keep npm cache and
installed modules inside task-owned scratch/worktree scope.

## Acceptance Contract

1. The exact latest stable and compatible target versions and existing
   package/CI owner are evidenced, including TypeScript 7 and `braces` limits.
2. Manifest and lockfile resolve the selected versions with one Storybook
   train and no unrelated application/runtime configuration change.
3. Existing frontend and Storybook checks execute with recorded exit codes,
   and the high advisory remains visible rather than bypassed.
4. The diff is independently reviewed and the final report separates local
   source, static/browser verification, deployment and remote merge status.

## Traceability

- [REQ-0027](../../01.requirements/0027-home-development-host.md)
- [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md)
- [SPEC-0201](../0201-home-infrastructure-diagnosis-and-work-design/spec.md)

## Open Questions

No package selection value is missing. Real browser execution depends on a
bounded Playwright install and local tool availability. A patched `braces`
release or validated replacement is needed before the held remote merge.

## Operational Impact

This is a source dependency update. It does not run Storybook as a HOME
service or publish its static output. Local npm install/build may consume
network, disk and CPU only in the isolated task worktree.
