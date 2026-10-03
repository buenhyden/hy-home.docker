---
title: "Refresh Storybook Packages Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0205-TSK-0001"
parent_ids:
- "SPEC-0205"
- "SPEC-0205-PLAN-0001"
created: "2026-10-03"
---

# Refresh Storybook Packages Task

## Objective

Update the existing Storybook workspace to current compatible stable direct
packages with a reproducible lockfile and scoped verification.

## Inputs

User's 2026-10-03 request for latest Storybook-related packages; baseline
`d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; SPEC-0201 05 handoff;
current package manifest/lock and official release/registry facts.
This is the exact source approval draft. Its existence does not grant source
write, HOME, remote or credential authority.

## Work Log

| Current -> target | Exact writer files | Regression / rollback |
| --- | --- | --- |
| Storybook 10.6.0 locked -> 10.6.1 train; direct declarations vary from 10.4.6 to 10.6.0 | `projects/storybook/nextjs/package.json`, `package-lock.json` | `npm ci`, Storybook build, browser coverage; revert only those two files. |
| Chromatic 5.3.1 -> 5.4.0; Next 16.3.6 -> 16.3.8; Vitest 5.0.1 -> 5.0.3; Vite 8.3.0 -> 8.3.2; ESLint 10.11.0 -> 10.12.0; Node types 26.6.2 -> 26.6.4; Tailwind declaration 4.3.2 -> 4.3.3 | Same two npm files | Peer, lint, typecheck and Next build; revert only those two files. |
| TypeScript 7 and braces no-patch advisory | READ_ONLY: `.github/dependabot.yml`, audit graph and official advisory | Keep TS 6.0.3 and security finding visible; no audit bypass. |

No source changes are needed in Storybook configuration, CI, Dependabot,
README or generated infrastructure projection unless a focused test identifies
a concrete break and this Task's exact writer scope is amended. `node_modules`
and generated build output are task-local ignored artifacts, not deliverables.

## Verification Evidence

| Check | Result | Limit |
| --- | --- | --- |
| Official npm registry dist-tags and peer ranges, Storybook release and Next guide | READ_ONLY | Checked 2026-10-03; recheck before source write. |
| Manifest/lock update and frontend build/test | NOT_RUN | Await Spec/Plan/Task approval. |
| `npm audit --audit-level=high` | BASELINE FAIL | `braces@3.0.3` has no patched release; confirm after update. |
| HOME, remote merge and publication | NOT_RUN | Separate action scope. |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PARTIAL: read-only target inventory | This Task and Dependabot/Stage 05 policy |
| 2 | W2 | NOT_RUN | npm manifest and lock |
| 3 | W3 | NOT_RUN | This Task; existing Storybook contract checker |
| 4 | W3 | NOT_RUN | This Task and existing README if meaning changes |

## Review Evidence

Independent source and security review follows the exact implementation diff.

## Commit Ledger

No SPEC-0205 commit. Baseline only: `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`.

## Rulings

No forced npm audit fix, blanket package override, coverage reduction,
Storybook 11 alpha, TypeScript 7 or duplicate npm updater.

## Deferred Items

Source approval; patched braces release or validated replacement; HOME and
remote actions remain separate.
