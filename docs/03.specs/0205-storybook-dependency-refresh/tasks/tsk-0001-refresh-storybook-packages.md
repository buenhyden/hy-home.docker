---
title: "Refresh Storybook Packages Task"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
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
The user's explicit request authorizes the two named npm source files; the
Spec review and Task readiness are recorded here before source modification.
HOME, remote and credential actions remain separately gated.

## Work Log

| Current -> target | Exact writer files | Regression / rollback |
| --- | --- | --- |
| Storybook 10.6.0 locked -> 10.6.1 train; direct declarations vary from 10.4.6 to 10.6.0 | `projects/storybook/nextjs/package.json`, `package-lock.json` | `npm ci`, Storybook build, browser coverage; revert only those two files. |
| Chromatic 5.3.1 -> 5.4.0; Next 16.3.6 -> 16.3.8; Vitest 5.0.1 -> 5.0.3; Vite 8.3.0 -> 8.3.2; ESLint 10.11.0 -> 10.12.0; Node types 26.6.2 -> 26.6.4; Tailwind declaration 4.3.2 -> 4.3.3 | Same two npm files | Peer, lint, typecheck and Next build; revert only those two files. |
| TypeScript 7 and braces no-patch advisory | READ_ONLY: `.github/dependabot.yml`, audit graph and official advisory | Keep TS 6.0.3 and security finding visible; no audit bypass. |
| Baseline optional vite-tsconfig-paths -> tsconfck TypeScript ^5 peer versus root TypeScript 6.0.3 | READ_ONLY baseline lock; generated lock pruned of one extraneous nested TypeScript 5 entry | Lock-only npm ls exits 1 both before and after; clean npm ci and builds pass. No override or downgrade. |

No source changes are needed in Storybook configuration, CI, Dependabot,
README or generated infrastructure projection unless a focused test identifies
a concrete break and this Task's exact writer scope is amended. `node_modules`
and generated build output are task-local ignored artifacts, not deliverables.

## Verification Evidence

| Check | Result | Limit |
| --- | --- | --- |
| Official npm registry dist-tags and peer ranges, Storybook release and Next guide | PASS | Checked 2026-10-03 against stable tags and peer ranges; Storybook 11 remains alpha. |
| Clean npm ci --ignore-scripts --no-audit --no-fund with task-local cache | PASS, exit 0 | 530 packages; lifecycle scripts skipped. |
| npm run lint, npm run typecheck, Storybook contract checker | PASS, exits 0/0/0 | Existing repository checks. |
| NEXT_TELEMETRY_DISABLED=1 npm run build; STORYBOOK_DISABLE_TELEMETRY=1 npm run build-storybook | PASS, exits 0/0 | Next 16.3.8 and Storybook 10.6.1/Vite 8.3.2 static builds. |
| Playwright task-local browser plus STORYBOOK_DISABLE_TELEMETRY=1 npm run coverage | PASS, exit 0 | 3 files, 9 browser tests; 100% statements, branches, functions and lines. Initial missing-browser run failed before browser installation. |
| npm ls --package-lock-only --all --json | BASELINE FAIL, exit 1 | Existing optional tsconfck TypeScript ^5 peer versus root TypeScript 6.0.3; clean install/build pass. |
| npm audit --audit-level=high --json | FAIL, exit 1 | Five high reports from one dev-only eslint-config-next -> @next/eslint-plugin-next -> fast-glob -> micromatch -> braces@3.0.3 chain; no patch. |
| npm audit --omit=dev --audit-level=high --json | PASS, exit 0 | Zero production-dependency vulnerabilities reported. |
| HOME, remote merge and publication | NOT_RUN | Separate action scope. |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: verified stable targets and preserved TypeScript 6 | This Task and Dependabot/Stage 05 policy |
| 2 | W2 | PASS: manifest, lock and clean install; baseline optional peer exception recorded | npm manifest and lock |
| 3 | W3 | PASS with known audit failure: lint, typecheck, builds, browser coverage and contract checker pass | This Task; existing Storybook contract checker |
| 4 | W3 | PASS: independent source and security reviews approved local commit; deployment and merge remain separate | This Task |

## Review Evidence

Independent docs-only review found no blocking issue after SPEC-0204 and
SPEC-0205 were serialized in the branch. Independent security review found no
new high/critical advisory or new registry source and accepted a local commit;
it retained the user's remote-merge hold for braces. Independent source
review approved the corrected specification and source diff.

### Source completion and disposition receipt

The 2026-10-03 completion review confirms all four source acceptance
criteria from the recorded immutable package update `fbbea9123751c13588022cdb76213fd8b5a14b6e`.
The source is integrated locally into `codex/spec-0201-0205-closure`; it has
not landed on protected main. A fresh npm audit still reports five high
findings and exit 1, and the official GHSA-vfj7-8cjw-p6xm advisory still
lists no patched braces version. This receipt does not waive that gate.
The completed package waits in Stage 03 until protected delivery succeeds;
it is not eligible for completed archive capture yet. Current update and
audit obligations remain with the npm manifest/lock, Dependabot and the
existing Storybook quality gate. HOME and publication remain NOT_RUN.

## Commit Ledger

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; SPEC-0204 draft
`0f67cb297`; SPEC-0205 draft/review/activation `eb8edc6e3`, `49f15e948`,
`c517bf402`, `cc7b4addd`. The commit containing this Task revision records the package update.

## Rulings

No forced npm audit fix, blanket package override, coverage reduction,
Storybook 11 alpha, TypeScript 7 or duplicate npm updater.

## Deferred Items

Patched braces release or validated replacement; HOME and remote actions
remain separate.
