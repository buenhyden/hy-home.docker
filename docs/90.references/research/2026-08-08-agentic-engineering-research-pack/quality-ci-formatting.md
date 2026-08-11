---
status: draft
artifact_id: reference:agentic-engineering-research:quality-ci-formatting
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-11
review_cycle: on-source-change
---

# Reference: Quality, CI, and Formatting

## Overview

The workspace has substantial but deliberately uneven QA coverage. Tracked
automation separates formatting, linting, syntax, type checking, selected
Python unit/regression tests, Storybook browser tests, frontend coverage,
builds, documentation contracts, infrastructure validation, and security
checks. The presence of one class does not imply another.

At Task 7 baseline `c57d33f37843802f7692261c50801f0dd966d7cb`,
Prettier options and ignores are tracked but no shared hook, package script,
typed gate, or workflow invokes Prettier. Type checking and thresholded code
coverage apply to the Storybook Next.js project only. Python had 22 tracked
`unittest` files at the Task 7 baseline; re-verified at `5580931` on
2026-08-11 the count is 24 tracked `unittest` files. No tracked Ruff/Black/
Flake8/Pylint lint gate, no Mypy/Pyright type gate, and no Python coverage
gate exist at either point. These are partial states, not whole-repository
quality claims.

## Purpose

Satisfy REQ-24 through REQ-26 by making each QA capability, applicability
boundary, execution location, failure behavior, and evidence limitation
independently inspectable. The goal is to prevent shorthand such as “lint,
tests, and CI pass” from masking a formatting, type, coverage, E2E, security,
or remote-enforcement gap.

## Repository Role

This Stage 90 reference is advisory analysis. It does not add or weaken a gate,
install dependencies, execute the controlled all-files wrapper, change a
coverage threshold, make desired checks remotely required, or authorize
deployment. Canonical QA owners remain the tracked configurations, scripts,
tests, workflow contract, workflow YAML, Stage 00 governance, and separately
observed remote state.

## Scope

### In scope

- Formatting, lint, syntax, type, unit, integration/component, E2E, coverage,
  build, documentation, configuration, and security capabilities.
- Pre-commit stages and filters, typed local/CI roots, failure propagation,
  retries, and skipped-check behavior.
- Local configuration, local execution, declared CI, and remote-enforcement
  evidence as separate states.
- Gaps, risks, adoption rules, owners, and implications for all fourteen
  workspace scopes.

### Out of scope

- Running the 34-leaf local profile or controlled all-files pre-commit route.
- Running frontend browser/coverage jobs or the complete Python test corpus.
- Installing lint/type/coverage tools or changing QA configuration.
- Authenticated workflow, check, ruleset, environment, artifact, deployment,
  or secret inspection.
- Claiming product, runtime, accessibility, security, or deployment quality
  from static configuration alone.

## Definitions / Facts

### Capability model

| Capability                 | Question answered                                                                         | It does not answer                                               |
| -------------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Formatting                 | Does text conform to mechanical layout/whitespace rules, or can a formatter rewrite it?   | Semantics, correctness, prose quality, or lint findings.         |
| Linting                    | Does a domain-specific static rule report suspicious or disallowed constructs?            | Parsing every language, runtime behavior, or coverage.           |
| Syntax                     | Can a parser/load step accept the file or workflow grammar?                               | Type safety, cross-file behavior, or operational validity.       |
| Type checking              | Do declared type relationships hold for the configured project?                           | Runtime behavior, other languages, tests, or coverage.           |
| Unit/regression test       | Does a bounded behavior remain true under test-controlled inputs?                         | Full integration, hosted execution, or production behavior.      |
| Integration/component test | Do configured components interact in a bounded environment?                               | A complete user journey or production system.                    |
| E2E test                   | Does an end-to-end user/system journey pass through the deployed or representative stack? | Unit coverage or remote enforcement.                             |
| Coverage                   | Which measured code dimensions were exercised under one configured test run?              | Test quality, missing requirements, or another language/project. |
| Security check             | Does one scanner or deterministic control find its targeted class?                        | Absence of all vulnerabilities or safe deployment.               |

### Current capability matrix

| Capability                        | Tracked owner and invocation                                                                                                      | Local path                                                                              | Declared CI path                                                | Current state and limit                                                                                                                     |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Basic formatting                  | `end-of-file-fixer`, `mixed-line-ending`, `trailing-whitespace`; `.editorconfig`                                                  | Applicable pre-commit hooks when installed/run                                          | `pre-commit` job                                                | **Implemented, filtered.** Hooks may modify files; config presence alone is not execution evidence.                                         |
| Prettier formatting               | `.prettierrc.json`, `.prettierignore`                                                                                             | No tracked invocation                                                                   | No tracked invocation                                           | **Configuration only / not enforced.** No `prettier --check` or `--write` route exists in shared automation or the project package scripts. |
| Markdown lint                     | `markdownlint-cli2`                                                                                                               | Pre-commit hook                                                                         | `pre-commit` job                                                | **Implemented, filtered.** Structural Markdown lint is not spelling, grammar, terminology, link truth, or source review.                    |
| YAML lint                         | `yamllint`                                                                                                                        | Pre-commit hook                                                                         | `pre-commit` job                                                | **Implemented, filtered.** Style rules do not prove GitHub/Compose semantics.                                                               |
| Shell lint                        | `shellcheck`                                                                                                                      | Pre-commit; selected post-tool validation                                               | `pre-commit` job                                                | **Implemented, filtered.** `recommend-qa-gates.sh` is excluded by configuration.                                                            |
| Workflow lint/syntax              | `actionlint` plus typed workflow checker                                                                                          | Pre-commit and focused local checker                                                    | `pre-commit` and `repo-contracts` expansions                    | **Implemented statically.** A pass cannot prove a hosted workflow ran.                                                                      |
| JSON/TOML syntax                  | `check-json`, `check-toml`; selective JSON parsing                                                                                | Pre-commit / post-tool routes                                                           | `pre-commit` job                                                | **Implemented, filtered.** Parsing does not prove consumer semantics.                                                                       |
| Shell syntax                      | `leaf.local-shell-syntax` invokes `bash -n` over tracked scripts and Claude hooks                                                 | Local typed profiles                                                                    | No CI-profile membership                                        | **Local-only typed leaf.** Separate from ShellCheck.                                                                                        |
| Frontend lint                     | `npm run lint` uses ESLint                                                                                                        | Direct project command or `eslint-nextjs` hook                                          | `frontend-quality`; deliberately skipped in CI `pre-commit`     | **Implemented for one project.** Dedicated CI avoids duplicate ESLint execution.                                                            |
| Frontend type                     | `npm run typecheck` uses `tsc --noEmit`; strict TS config                                                                         | Direct project command                                                                  | `frontend-quality`                                              | **Implemented for Storybook Next.js only.** `allowJs` and `skipLibCheck` are configured limits.                                             |
| Python lint/format                | No Ruff, Black, Flake8, or Pylint owner in pre-commit, typed gates, or workflows                                                  | None                                                                                    | None                                                            | **Missing shared enforcement.** Historical one-off command evidence is not an active gate.                                                  |
| Python type                       | No Mypy or Pyright owner in pre-commit, typed gates, or workflows                                                                 | None                                                                                    | None                                                            | **Missing shared enforcement.** Type annotations in source do not establish checked coverage.                                               |
| Python unit/regression            | 24 tracked `tests/validation/test_*.py` files using `unittest` (re-verified 2026-08-11; 22 at the Task 7 baseline)                | Selected modules in local typed roots; direct module/discovery commands remain possible | Selected modules in repo-contract, eval, and supply-chain roots | **Partial.** The typed roots do not claim one full 24-file discovery run.                                                                   |
| Shell wrapper regression          | Two tracked `test_*.sh` files                                                                                                     | Focused commands                                                                        | `test_run_ci_precommit.sh` is a typed CI leaf                   | **Partial.** The controlled wrapper test and its actual authorized execution are different evidence.                                        |
| Storybook browser/component tests | Three tracked `*.stories.ts`; Vitest Storybook plugin with Playwright/Chromium                                                    | `npm run test`                                                                          | Coverage route runs the same Storybook project                  | **Implemented for three stories.** This is browser/component evidence, not a standalone application E2E journey.                            |
| Standalone E2E                    | No tracked `*.spec.*`/`*.test.*` Playwright journey suite or dedicated E2E root was found                                         | None                                                                                    | None                                                            | **Missing as a separate capability.** Browser-backed Storybook tests must not be relabeled as full E2E.                                     |
| Coverage                          | Vitest V8 coverage with 90% statements, branches, functions, and lines                                                            | `npm run coverage`                                                                      | `storybook-coverage` after Node and Playwright setup            | **Implemented for Storybook only.** No Python, shell, Compose, or whole-repository coverage gate.                                           |
| Builds                            | Next.js build and Storybook static build                                                                                          | Project scripts                                                                         | `frontend-quality`                                              | **Implemented build feedback.** Build output is not uploaded, attested, promoted, deployed, or rollback evidence.                           |
| Docs/contracts                    | Metadata, traceability, implementation alignment, corpus, target-surface, repo-contract gates                                     | Focused commands and typed profiles                                                     | Dedicated roots and repo-contract expansion                     | **Implemented with named scopes.** Aggregate repo-contract failure counts need subject-level attribution.                                   |
| Configuration/security            | Compose validation, hardening, template/QuickWin, Gitleaks, Hadolint, npm audit, supply-chain fixture/policy checks, Zizmor SARIF | Mixed: pre-commit, typed profiles, focused scripts                                      | Dedicated jobs; Zizmor/SARIF is GitHub-only                     | **Partial by class.** Each result covers only its declared target and environment.                                                          |

### Pre-commit is filtered orchestration, not universal coverage

`.pre-commit-config.yaml` registers 24 hook IDs: 17 use the default
`pre-commit` stage, 6 are `pre-push`, and 1 is `commit-msg`. File/type filters
and stage selection mean a configured hook may legitimately skip a change.
The CI pre-commit wrapper requires `SKIP=eslint-nextjs`; ESLint runs inside
`frontend-quality` instead.

Repository governance prohibits direct Agent execution of `pre-commit run`.
The controlled all-files wrapper additionally requires an initially clean
linked worktree, tracked Task evidence, minimal allowed prefixes, and review of
Git-visible non-ignored paths. Task 7 did not authorize or run it. Therefore
this reference reports configuration and declared CI, not an all-files result.

### Test and coverage depth

The Python corpus contains 22 `unittest` modules and two shell regression
wrappers. The typed DAG selects named modules for gate-contract, runner,
adapter, workflow, governance-routing, agent-output, corpus, target-surface,
and supply-chain behaviors. Selection is explicit and reproducible, but it is
not synonymous with full discovery of every tracked test file.

The frontend fixture contains three Storybook story files. Vitest's Storybook
plugin runs them headlessly in Chromium through the Playwright provider. The
coverage command enforces 90% thresholds independently for statements,
branches, functions, and lines. No repository-wide coverage aggregation or
Python coverage threshold is tracked.

### Failure propagation, retries, and skipped checks

- The typed runner verifies the plan, executes unique leaves in order, and
  returns immediately on the first non-zero child. Local dispatch uses
  `set -euo pipefail`.
- No workflow or gate encodes automatic retry, backoff, attempt limits, or
  `continue-on-error`. Correct-and-rerun is a human/authorized remote action.
- `docs-implementation-alignment` still attempts its recommendation leaf with
  `if: always()`; the diagnostic step does not convert the gate failure to a
  pass.
- Job timeouts and cancellation bound resource use. They are not test retries.
- A skipped check needs an applicability reason. Docs-only work can mark
  runtime/domain tests N/A, but must still run cheap document/diff checks.
- Local passes do not replace GitHub-only SARIF or applied required checks;
  workflow YAML does not prove either ran remotely.

### Evidence and enforcement states

| State                 | Task 7 result                                                                                                                                                                                        |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tracked configuration | Verified at `c57d33f`: configs, package scripts, test files, thresholds, typed roots, and workflow definitions read directly.                                                                        |
| Local execution       | Focused workflow contract PASS and profile list-only result; later Task 7 document validators are recorded in the Task ledger. No 34-leaf profile, frontend test, or all-files pre-commit execution. |
| Declared CI           | Sixteen quality jobs and their ordered root expansions verified statically.                                                                                                                          |
| Remote CI/rulesets    | Current run results, required-check conclusions, branch protection, and rulesets are **UNVERIFIED**.                                                                                                 |
| CD/runtime            | Environments, secrets, deployment, promotion, rollback, and production quality are **UNVERIFIED**; no tracked CD job exists.                                                                         |

### Gaps, risks, and follow-up route

- **Formatting gap:** Prettier configuration can be mistaken for enforcement.
  Any adoption proposal must name files, check/write mode, hook/CI location,
  version ownership, migration diff, and conflict with current linters.
- **Python gap:** lint, type, and coverage are absent as shared gates. A future
  Stage 03/04 design must scope ordinary modules versus embedded/heredoc code,
  baseline debt, blocking threshold, dependency pinning, and local/CI parity.
- **E2E gap:** Storybook browser tests are valuable component evidence but do
  not exercise a deployed user journey. A future product surface needs named
  journeys, test data, environment, failure artifacts, flake/retry policy, and
  an owner before an E2E gate is claimed.
- **Coverage risk:** the 90% frontend thresholds must never be reported as 90%
  repository coverage. Coverage is one measured project/run, not correctness.
- **Remote risk:** static check names are desired state until authenticated
  readback and current run evidence are separately authorized.
- **Follow-up route:** open the earliest applicable Requirement/Spec/Plan/Task
  and change canonical configs/scripts/tests together; Stage 90 cannot adopt a
  tool or weaken a gate.

## Scope Implications

| Scope          | Quality implication                                                                                                                                       |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Use named fixture, governance, provider-drift, and workflow-contract gates; synthetic evals do not prove live model quality.                              |
| `architecture` | Define quality attributes and evidence per component; cross-cutting coverage or E2E policy requires an approved architecture/specification owner.         |
| `backend`      | No backend application QA surface is established; future services need language lint/type/unit/integration/coverage and contract tests scoped by Spec.    |
| `common`       | Own shared formatting/lint conventions and applicability; Prettier remains configuration-only until an approved enforcement route exists.                 |
| `docs`         | Run metadata, traceability, implementation-alignment, repo-contract, heading/scope, and diff gates; Markdown lint is not factual/source review.           |
| `entry`        | Gateway configuration needs syntax, security, contract, integration, and recovery evidence tied to the real entry surface.                                |
| `frontend`     | ESLint, strict TypeScript, builds, three Storybook browser stories, and 90% four-axis coverage are implemented for the fixture; standalone E2E is absent. |
| `infra`        | Compose/hardening checks validate tracked definitions; runtime health, upgrade, failure injection, deployment, and rollback remain separate evidence.     |
| `meta`         | Metadata/profile/registry validators are first-class QA; schema conformance cannot prove content truth or applied enforcement.                            |
| `mobile`       | No mobile source or test surface is established, so mobile lint/type/test/coverage/E2E are not applicable until an approved project exists.               |
| `ops`          | Own operational acceptance, observability, rollback rehearsal, and failure evidence; CI/build status alone is insufficient.                               |
| `product`      | Define user-visible acceptance and critical journeys before E2E or coverage targets; numeric coverage is not product value.                               |
| `qa`           | Maintain the capability matrix, applicability/skip rationale, failure attribution, flake policy, local/CI split, and exact evidence records.              |
| `security`     | Keep Gitleaks, Hadolint, npm audit, hardening, supply-chain checks, and Zizmor distinct; no single pass proves secure delivery.                           |

## Sources

| Source                                                                                                                                    | Accessed                    | Class                            | Verification state                                                                                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Prettier CLI](https://prettier.io/docs/cli)                                                                                              | 2026-08-08T17:45:01+09:00   | External mutable                 | Verified official page; `--write`, `--check`, ignore, and exit semantics used only to distinguish configuration from execution.                                                              |
| [pre-commit documentation](https://pre-commit.com/)                                                                                       | 2026-08-08T17:45:01+09:00   | External mutable                 | Verified official project page; hook stages, file filters, all-files behavior, and non-zero failure semantics used.                                                                          |
| [TypeScript `noEmit`](https://www.typescriptlang.org/tsconfig/noEmit.html)                                                                | 2026-08-08T17:45:01+09:00   | External mutable                 | Verified official page; upstream capability only; tracked project config remains local evidence.                                                                                             |
| [Vitest coverage](https://vitest.dev/guide/coverage.html)                                                                                 | 2026-08-08T17:45:01+09:00   | External mutable                 | Verified official page; coverage capability only; tracked thresholds define this project.                                                                                                    |
| [Storybook Vitest addon](https://storybook.js.org/docs/writing-tests/integrations/vitest-addon)                                           | 2026-08-08T17:45:01+09:00   | External mutable                 | Verified official page; Storybook/Vitest browser capability only; local configuration defines adoption depth.                                                                                |
| [ESLint getting started](https://eslint.org/docs/latest/use/getting-started)                                                              | 2026-08-08T17:45:01+09:00   | External mutable                 | Verified official page; lint capability only; project package/config define local enforcement.                                                                                               |
| [GitHub workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)                         | 2026-08-08T17:45:01+09:00   | External mutable                 | Verified official page with redirect to current route; job/step/failure/timeout semantics only.                                                                                              |
| [GitHub secure use](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) | 2026-08-08T17:45:01+09:00   | External mutable                 | Verified official page with redirect; least privilege and SHA-pinning guidance only.                                                                                                         |
| [Pre-commit configuration](../../../../.pre-commit-config.yaml)                                                                           | 2026-08-08                  | Workspace tracked                | Complete 24-hook inventory and stage/file filters read at `c57d33f`.                                                                                                                         |
| [Typed workflow registry](../../../../.github/workflow-contract.yml)                                                                      | 2026-08-08                  | Workspace tracked                | Complete root/leaf/profile expansion and QA entrypoints re-derived.                                                                                                                          |
| [CI quality workflow](../../../../.github/workflows/ci-quality.yml)                                                                       | 2026-08-08                  | Workspace tracked                | Sixteen job definitions, skipped ESLint duplication, timeouts, permissions, and two-leaf alignment behavior verified.                                                                        |
| [Storybook package scripts](../../../../projects/storybook/nextjs/package.json)                                                           | 2026-08-08                  | Workspace tracked                | Lint, typecheck, test, coverage, Next.js build, and Storybook build scripts verified.                                                                                                        |
| [Vitest configuration](../../../../projects/storybook/nextjs/vitest.config.ts)                                                            | 2026-08-08                  | Workspace tracked                | Playwright/Chromium Storybook project and four 90% thresholds verified.                                                                                                                      |
| [CI gate contract tests](../../../../tests/validation/test_ci_gate_contract.py)                                                           | 2026-08-11 (was 2026-08-08) | Workspace tracked                | Re-verified at `5580931`: the tracked validation directory contains 24 Python and 2 shell test files (22 Python at the Task 7 baseline `c57d33f`); file presence is not a full-suite result. |
| [GitHub governance](../../../00.agent-governance/rules/github-governance.md)                                                              | 2026-08-08                  | Workspace tracked policy         | Local/CI/remote split, controlled wrapper boundary, and change-type evidence matrix.                                                                                                         |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                                                               | 2026-08-08                  | Workspace tracked stale/advisory | Built from `f8a72211`; corroborated and not used as current proof.                                                                                                                           |

## Maintenance

Re-measure the hook inventory, test files, project scripts, coverage thresholds,
typed expansions, and workflow jobs whenever their owners change. Reopen all
mutable primary documentation before changing a capability conclusion. Keep
configuration, local execution, CI definition, hosted result, remote
enforcement, runtime acceptance, and deployment evidence in separate fields.

## Related Documents

- [Verification and validation](./verification-validation.md)
- [Automation pipeline and workflow topology](./automation-pipeline-workflow.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Spec-driven SDLC](./spec-driven-sdlc.md)
- [Document metadata lifecycle](./document-metadata-lifecycle.md)
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
