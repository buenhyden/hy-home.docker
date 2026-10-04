---
title: "Refresh Storybook Packages Task"
version: "0.1.6"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-04"
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

### Approved Bounded Audit Acceptance — 2026-10-04

The owner explicitly approves replacing the previous patch-only merge hold
with one expiring risk acceptance for GHSA-vfj7-8cjw-p6xm / CVE-2026-93687.
This amendment supersedes only that hold; preceding audit FAIL receipts remain
historical evidence. Keep Next, React Hooks, TypeScript and accessibility lint.
The exact development dependency chain is eslint-config-next@16.3.8 ->
@next/eslint-plugin-next@16.3.8 -> fast-glob@3.3.1 -> micromatch@4.0.8 ->
braces@3.0.3 in projects/storybook/nextjs. Owner: @buenhyden. Expiry:
2026-10-11 00:00:00 KST (2026-10-10T15:00:00Z), without automatic extension.

Reuse the typed workflow contract and existing gate adapter. Preserve the full
and production npm audits, report raw audit FAIL separately from ACCEPTED_RISK,
and admit derived findings only when every advisory leaf is that exact GHSA
on the verified development lock graph. Unknown/malformed reports, command or
network failures, advisory lookup failure, changed paths/versions, other
high/critical findings, production findings, expiry, or an available patch
fail closed. A clean full audit needs no risk acceptance. No threshold change,
continue-on-error, skipped gate, dependency removal or branch protection bypass.

Acceptance requires RED/GREEN negative fixtures, scoped contract/adapter tests,
format/lint/document checks, independent rules and security review, and the
normal required hosted PR gate. Recovery reverts this bounded policy and
adapter to strict audit failure; HOME execution is not approved.

#### Exact Amendment Writer Scope

- `docs/03.specs/0205-storybook-dependency-refresh/spec.md`
- `docs/03.specs/0205-storybook-dependency-refresh/plan.md`
- `docs/03.specs/0205-storybook-dependency-refresh/tasks/tsk-0001-refresh-storybook-packages.md`
- `.agents/governance/quality-standards.md`
- `.github/workflow-contract.yml`
- `scripts/lib/gate/ci_gate_contract.py`
- `scripts/lib/gate/ci_gate_adapters.py`
- `tests/lib/gate/test_ci_gate_contract.py`
- `tests/lib/gate/test_ci_gate_adapters.py`

Order: amend approved contract -> independent policy review -> RED fixtures ->
minimal shared adapter/typed contract -> GREEN focused checks -> independent
review -> record evidence -> commit/push/required CI -> protected integration.
No completion or archive is claimed before its evidence and delivery boundary.

#### Current Implementation Evidence

Baseline: `7f939ae802afc1d23f96b8eca4100abfcc2bf629`. The exact nine-file
amendment passed independent pre-implementation rules review. The typed
acceptance regression first failed (exit 1, missing API/metadata), then passed
(exit 0, 3 tests). Full contract tests passed (exit 0, 22 tests). Adapter
negative fixtures first failed (exit 1), then passed (exit 0, 35 tests).
The scoped contract/adapter/workflow consumer modules passed (exit 0,
106 tests); workflow contract validator passed (5 workflows, 9 jobs, 8 actions).
An initially mistyped nonexistent runner module caused one import failure;
this was a command selection error, not a product or accepted gate failure.
Registered runner module checks passed (exit 0, 48 tests). Metadata checks
passed (selected=4, violations=0, exit 0); the first attempt rejected new H2
headings, then existing-template H3/H4 placement passed without a waiver.
Final adapter tests passed (exit 0, 39 tests). The final combined contract,
adapter, workflow and runner regression command passed (157 tests, exit 0).
Ruff 0.15.12 lint/format checks, Markdownlint CLI2 0.22.1 and diff checks passed
(exits 0). Independent final policy/source/security review: PASS, including
the observed downgrade delta. Live standalone adapter integration passed
(exit 0): full raw audit FAIL (exit 1), production audit PASS (exit 0), exact
GHSA ACCEPTED_RISK. This is isolated adapter verification, not a hosted PR
gate or deployment. The public network test used task-local cache and sterile
npm config paths; no real HOME state, secret or user-global configuration was
read or changed. Hosted required CI and protected delivery remain pending.

The owner separately approved transmission of public package names/versions
to npm audit and read-only public GitHub advisory requests after automatic
approval review rejected the initial network check. No secret or private app
payload is permitted. Live npm reports suggest an exact Next preset downgrade
to 14.2.35 rather than a braces patch; no downgrade is applied. Such a report
is admissible only for the exact accepted chain and the verified unpatched
advisory. Unknown suggestions remain failures.
