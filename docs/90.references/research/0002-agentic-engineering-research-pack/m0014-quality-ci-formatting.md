---
title: "Reference: Quality, CI, and Formatting"
version: "1.0.0"
type: "reference/research"
status: "published"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "references"
artifact_id: "RES-0002-m0014"
parent_ids:
- "RES-0002"
created: "2026-08-23"
reviewed_at: "2026-08-28"
review_cycle: "on-source-change"
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

Re-verified directly at `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c` on
2026-08-14: the 24-Python/2-shell test-file count, the 24-hook/17-pre-commit/
6-pre-push/1-commit-msg pre-commit inventory, and the html5lib validation-
runtime gap (below) are unchanged. This leaf additionally re-runs the
repository-contract gate directly rather than citing a prior result, and
applies an explicit five-state disposition (`configured`, `selected`,
`executed`, `passed`, `enforced`) to every capability row so "the CI passed"
can no longer stand in for "this specific gate ran and its result is
remotely required."

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

| Capability                        | Tracked owner and invocation                                                                                                                              | Local path                                                                              | Declared CI path                                                | Current state and limit                                                                                                                                  |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Basic formatting                  | `end-of-file-fixer`, `mixed-line-ending`, `trailing-whitespace`; `.editorconfig`                                                                          | Applicable pre-commit hooks when installed/run                                          | `pre-commit` job                                                | **Implemented, filtered.** Hooks may modify files; config presence alone is not execution evidence.                                                      |
| Prettier formatting               | `.prettierrc.json`, `.prettierignore`                                                                                                                     | No tracked invocation                                                                   | No tracked invocation                                           | **Configuration only / not enforced.** No `prettier --check` or `--write` route exists in shared automation or the project package scripts.              |
| Markdown lint                     | `markdownlint-cli2`                                                                                                                                       | Pre-commit hook                                                                         | `pre-commit` job                                                | **Implemented, filtered.** Structural Markdown lint is not spelling, grammar, terminology, link truth, or source review.                                 |
| YAML lint                         | `yamllint`                                                                                                                                                | Pre-commit hook                                                                         | `pre-commit` job                                                | **Implemented, filtered.** Style rules do not prove GitHub/Compose semantics.                                                                            |
| Shell lint                        | `shellcheck`                                                                                                                                              | Pre-commit; selected post-tool validation                                               | `pre-commit` job                                                | **Implemented, filtered.** `recommend-qa-gates.sh` is excluded by configuration.                                                                         |
| Workflow lint/syntax              | `actionlint` plus typed workflow checker                                                                                                                  | Pre-commit and focused local checker                                                    | `pre-commit` and `repo-contracts` expansions                    | **Implemented statically.** A pass cannot prove a hosted workflow ran.                                                                                   |
| JSON/TOML syntax                  | `check-json`, `check-toml`; selective JSON parsing                                                                                                        | Pre-commit / post-tool routes                                                           | `pre-commit` job                                                | **Implemented, filtered.** Parsing does not prove consumer semantics.                                                                                    |
| Shell syntax                      | `leaf.local-shell-syntax` invokes `bash -n` over tracked scripts and Claude hooks                                                                         | Local typed profiles                                                                    | No CI-profile membership                                        | **Local-only typed leaf.** Separate from ShellCheck.                                                                                                     |
| Frontend lint                     | `npm run lint` uses ESLint                                                                                                                                | Direct project command or `eslint-nextjs` hook                                          | `frontend-quality`; deliberately skipped in CI `pre-commit`     | **Implemented for one project.** Dedicated CI avoids duplicate ESLint execution.                                                                         |
| Frontend type                     | `npm run typecheck` uses `tsc --noEmit`; strict TS config                                                                                                 | Direct project command                                                                  | `frontend-quality`                                              | **Implemented for Storybook Next.js only.** `allowJs` and `skipLibCheck` are configured limits.                                                          |
| Python lint/format                | No Ruff, Black, Flake8, or Pylint owner in pre-commit, typed gates, or workflows                                                                          | None                                                                                    | None                                                            | **Missing shared enforcement.** Historical one-off command evidence is not an active gate.                                                               |
| Python type                       | No Mypy or Pyright owner in pre-commit, typed gates, or workflows                                                                                         | None                                                                                    | None                                                            | **Missing shared enforcement.** Type annotations in source do not establish checked coverage.                                                            |
| Python unit/regression            | 24 tracked `tests/validation/test_*.py` files using `unittest` (re-verified 2026-08-11; 22 at the Task 7 baseline)                                        | Selected modules in local typed roots; direct module/discovery commands remain possible | Selected modules in repo-contract, eval, and supply-chain roots | **Partial.** The typed roots do not claim one full 24-file discovery run.                                                                                |
| Shell wrapper regression          | Two tracked `test_*.sh` files                                                                                                                             | Focused commands                                                                        | `test_run_ci_precommit.sh` is a typed CI leaf                   | **Partial.** The controlled wrapper test and its actual authorized execution are different evidence.                                                     |
| Storybook browser/component tests | Three tracked `*.stories.ts`; Vitest Storybook plugin with Playwright/Chromium                                                                            | `npm run test`                                                                          | Coverage route runs the same Storybook project                  | **Implemented for three stories.** This is browser/component evidence, not a standalone application E2E journey.                                         |
| Standalone E2E                    | No tracked `*.spec.*`/`*.test.*` Playwright journey suite or dedicated E2E root was found                                                                 | None                                                                                    | None                                                            | **Missing as a separate capability.** Browser-backed Storybook tests must not be relabeled as full E2E.                                                  |
| Coverage                          | Vitest V8 coverage with 90% statements, branches, functions, and lines                                                                                    | `npm run coverage`                                                                      | `storybook-coverage` after Node and Playwright setup            | **Implemented for Storybook only.** No Python, shell, Compose, or whole-repository coverage gate.                                                        |
| Builds                            | Next.js build and Storybook static build                                                                                                                  | Project scripts                                                                         | `frontend-quality`                                              | **Implemented build feedback.** Build output is not uploaded, attested, promoted, deployed, or rollback evidence.                                        |
| Docs/contracts                    | Metadata, traceability, implementation alignment, corpus, target-surface, repo-contract gates                                                             | Focused commands and typed profiles                                                     | Dedicated roots and repo-contract expansion                     | **Implemented with named scopes.** Aggregate repo-contract failure counts need subject-level attribution.                                                |
| Configuration/security            | Compose validation, hardening, template/QuickWin, Gitleaks, Hadolint, npm audit, supply-chain fixture/policy checks, Zizmor SARIF                         | Mixed: pre-commit, typed profiles, focused scripts                                      | Dedicated jobs; Zizmor/SARIF is GitHub-only                     | **Partial by class.** Each result covers only its declared target and environment.                                                                       |
| Grammar/prose style               | No tracked owner: `rg -i "vale\|proselint\|write-good\|languagetool"` across tracked config, workflow, and pre-commit files returns no tool configuration | None                                                                                    | None                                                            | **Missing entirely.** Markdown lint is structural; there is no spelling, grammar, terminology-consistency, or prose-style gate for any tracked document. |

### Five-state gate disposition

Naming a capability "implemented" collapses five genuinely different claims
into one word. This leaf adopts the same evidence-state vocabulary the
verification-and-validation leaf defines (`configured`, `selected`,
`executed`, `passed`, `enforced`, plus `UNVERIFIED`) and applies it per gate
class. `configured` means a tracked definition exists; `selected` means a
typed profile or CI job root actually includes that gate; `executed` means
the named command ran in a recorded environment (local execution this Task,
or a hosted run); `passed` means that execution met its declared oracle;
`enforced` means an authenticated remote authority (a required status check,
branch protection, or ruleset) blocks a merge when the gate is red.

| Gate class                                      |       configured        |        selected (typed root)        |                       executed (this Task)                       |                                          passed (this Task)                                           |                enforced (remote)                 |
| ----------------------------------------------- | :---------------------: | :---------------------------------: | :--------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------: | :----------------------------------------------: |
| Basic file-hygiene hooks                        |           Yes           |        Yes (`ci.pre-commit`)        |                      No — not run this Task                      |                                                  N/A                                                  |                   `UNVERIFIED`                   |
| Prettier                                        | Yes (config files only) |  No — no typed root references it   |                                No                                |                                                  N/A                                                  | `UNVERIFIED`; cannot be enforced without a route |
| Markdown lint                                   |           Yes           |        Yes (`ci.pre-commit`)        |                      No — not run this Task                      |                                                  N/A                                                  |                   `UNVERIFIED`                   |
| YAML lint                                       |           Yes           |        Yes (`ci.pre-commit`)        |                      No — not run this Task                      |                                                  N/A                                                  |                   `UNVERIFIED`                   |
| Shell lint (ShellCheck)                         |           Yes           |        Yes (`ci.pre-commit`)        |                      No — not run this Task                      |                                                  N/A                                                  |                   `UNVERIFIED`                   |
| Workflow lint/typed checker                     |           Yes           | Yes (`ci.repo-contracts` expansion) | **Yes** — `check-github-workflow-contract.py` run directly today |                                           **Yes** — `PASS`                                            |                   `UNVERIFIED`                   |
| Frontend lint (ESLint)                          |           Yes           |     Yes (`ci.frontend-quality`)     |                      No — not run this Task                      |                                                  N/A                                                  |                   `UNVERIFIED`                   |
| Frontend type (`tsc --noEmit`)                  |           Yes           |     Yes (`ci.frontend-quality`)     |                      No — not run this Task                      |                                                  N/A                                                  |                   `UNVERIFIED`                   |
| Python lint/type (Ruff/Mypy)                    |         **No**          |                 No                  |                               N/A                                |                                                  N/A                                                  |         N/A — no gate exists to enforce          |
| Python unit/regression                          |           Yes           |       Yes (selected modules)        |                  No full 24-file run this Task                   |                                                  N/A                                                  |                   `UNVERIFIED`                   |
| Storybook browser/component                     |           Yes           |    Yes (`ci.storybook-coverage`)    |                      No — not run this Task                      |                                                  N/A                                                  |                   `UNVERIFIED`                   |
| Coverage (Storybook, 90%)                       |           Yes           |    Yes (`ci.storybook-coverage`)    |                      No — not run this Task                      |                                                  N/A                                                  |                   `UNVERIFIED`                   |
| Repository contract (`check-repo-contracts.sh`) |           Yes           |      Yes (`ci.repo-contracts`)      |            **Yes** — run directly today at `ece3eda9`            | **No in the default interpreter** — `failures=1` (html5lib gap, below); PASS only in an isolated venv |                   `UNVERIFIED`                   |
| Grammar/prose style                             |         **No**          |                 No                  |                               N/A                                |                                                  N/A                                                  |         N/A — no gate exists to enforce          |

Two rows in this table were not merely re-cited but freshly executed today:
the workflow-contract checker (`PASS`, unchanged) and `check-repo-contracts.sh`
in this session's default, non-isolated Python interpreter, which returned
`failures=1` — see "Test and coverage depth" and "Gaps, risks" below for the
exact failing check. Every other `executed`/`passed` cell is `No`/`N/A`
because this leaf did not run those commands; citing a prior Task's static
configuration read as if it were today's execution would misstate the
evidence class.

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

`scripts/requirements-pre-commit.txt` pins the orchestrator itself to
`pre-commit==4.6.1`; the `pre-commit` CI job installs that exact version
before invoking `run-ci-precommit.sh`. `scripts/requirements.txt` separately
pins the repository-contract validation dependencies (`PyYAML>=6.0,<7.0`,
`markdown-it-py>=3.0,<4.0`, `html5lib>=1.1,<2.0`) used by
`check-repo-contracts.sh` and related checkers. These are two different
pinned dependency sets serving two different gate families; a local
interpreter can satisfy one without satisfying the other, which is exactly
the html5lib gap documented below — orchestrator-version parity does not
imply validation-dependency parity.

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

### Reading the repository contract check's failure count

The repository contract check prints `failures=<n>`, and that number counts
failing SUBJECTS rather than failing findings or failing lines. A single
reported failure can therefore stand for many findings, and the count moving
from one number to another does not indicate a proportional change in the
amount of work. Re-derive both figures before comparing two runs: the subject
count is what the script prints, and the finding count has to be read from the
output body. Verified 2026-08-19 against the script, which increments its
counter once per failing subject and echoes that counter at the end.

### Evidence and enforcement states

| State                 | Task 7 result                                                                                                                                                                                        |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tracked configuration | Verified at `c57d33f`: configs, package scripts, test files, thresholds, typed roots, and workflow definitions read directly.                                                                        |
| Local execution       | Focused workflow contract PASS and profile list-only result; later Task 7 document validators are recorded in the Task ledger. No 34-leaf profile, frontend test, or all-files pre-commit execution. |
| Declared CI           | Sixteen quality jobs and their ordered root expansions verified statically.                                                                                                                          |
| Remote CI/rulesets    | Current run results, required-check conclusions, branch protection, and rulesets are **UNVERIFIED**.                                                                                                 |
| CD/runtime            | Environments, secrets, deployment, promotion, rollback, and production quality are **UNVERIFIED**; no tracked CD job exists.                                                                         |

### html5lib gap, re-verified by direct execution

Prior Task evidence (recorded in project Memory) reports the repository
contract passing in an isolated validation virtual environment and failing
with exactly one dependency gap in the default interpreter. This leaf did
not merely re-cite that record: it ran `bash
scripts/validation/check-repo-contracts.sh` directly, today, in this
session's default (non-isolated) Python 3, at `ece3eda9`. The exact output
was:

```text
==> Governance memory contract
FAIL: AGC-DEPENDENCY-MISSING path=html5lib location=validation-runtime
...
Repo contract check
failures=1
```

A direct `python3 -c "import html5lib"` in the same interpreter confirmed
`ModuleNotFoundError: No module named 'html5lib'`; `markdown_it` (the other
`scripts/requirements.txt` dependency) imported successfully, so the gap is
specific to `html5lib`, not a general missing-requirements-file condition.
Every other repo-contract subsection in the same run — reference stage
contract, LLM Wiki contract, HADS reference profile, gap-routing
recommender, audit pack coverage, agentic audit semantic freshness,
controlled pre-commit wrapper contract, script reference integrity, service
documentation coverage, script usage contract, floating image tag policy,
tech-stack version drift, documentation runtime version drift, and the three
current-truth drift checks — produced no failure output. This is
`Workspace tracked/local execution` evidence, re-derived independently
rather than copied forward, and it confirms the gap is exactly as narrow as
prior evidence claimed: one declared-but-unsatisfied dependency, in this
interpreter, blocking one governance-memory subsection of one aggregate gate.
It remains unowned: no Task in this pack's traceable history installs
`html5lib` into the default interpreter or removes the dependency, and this
leaf does not adopt either fix.

### Gaps, risks, and follow-up route

- **Formatting gap:** Prettier configuration can be mistaken for enforcement.
  Any adoption proposal must name files, check/write mode, hook/CI location,
  version ownership, migration diff, and conflict with current linters.
- **Grammar/prose-style gap:** no tracked tool (Vale, proselint, write-good,
  LanguageTool, or equivalent) checks spelling, grammar, terminology
  consistency, or prose style for any tracked document. Markdown lint
  (`markdownlint-cli2`) only enforces structural rules — heading levels, list
  formatting, line-length-adjacent style — and explicitly does not read
  prose for correctness. A future adoption proposal must name the tool,
  its false-positive rate against this repository's mixed English/Korean
  corpus, hook/CI placement, and whether it blocks or only annotates.
- **html5lib gap (re-verified 2026-08-14):** declared in
  `scripts/requirements.txt` but absent from the default interpreter used in
  this session; confirmed failing exactly one governance-memory subsection
  of the repository-contract gate. This is an environment-provisioning gap,
  not a validator-logic defect — the checker correctly detects and reports
  its own missing dependency rather than silently skipping the check.
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

### QA taxonomy and adoption mechanics

Formatting answers whether a tool can normalize layout; linting applies
domain-specific static rules; syntax checks parser acceptance; type checking
checks declared type relationships. Unit/regression tests exercise controlled
oracles, integration/component tests exercise bounded interactions, and system
or end-to-end evidence needs a representative journey. Coverage measures what
one configured run exercised, not requirement completeness or test quality.
Security checks cover their named class; independent review assesses the
adequacy of evidence and is not replaceable by a command exit code.

For a change, first identify the artifact and applicable owner, then select the
smallest matching check, record the immutable revision and raw outcome, and
escalate gaps to the owning specification or Task. The repository has no shared
Python formatter/linter/type-checker declaration and no standalone end-to-end
journey suite in these measured controls; do not relabel a missing capability
as a passing alternative. Prettier configuration without a tracked invocation
is configuration, not formatting enforcement.

| Control | Declared mechanics | Exact local investigation target | Verification limit |
| --- | --- | --- | --- |
| Formatting | File-normalization hooks and `.editorconfig` guide layout; Prettier has configuration but no tracked shared invocation. | `.pre-commit-config.yaml`, `.editorconfig`, `.prettierrc.json` | Formatting does not assess prose, correctness, or execution. |
| Linting | Markdown, YAML, shell, action, secret, and project ESLint checks target selected file classes. | `.pre-commit-config.yaml`, `projects/storybook/nextjs/package.json` | Lint does not prove parser completeness, behavior, or acceptance. |
| Syntax | JSON/TOML hooks and workflow/static validators parse bounded formats. | `.pre-commit-config.yaml`, `scripts/validation/github_workflow_contract.py` | Parse success does not prove consumer or hosted semantics. |
| Type checking | `tsc --noEmit` is declared for the Storybook Next.js project. | `projects/storybook/nextjs/package.json`, `tsconfig.json` | It does not cover Python, shell, Compose, or runtime behavior. |
| Unit / regression | Validation tests and typed gates contain controlled oracles for selected contracts. | `tests/validation/`, `scripts/validation/ci_gate_runner.py` | File inventory does not prove full discovery or an executed suite. |
| Integration / component | Storybook Vitest scripts cover configured browser/component work. | `projects/storybook/nextjs/package.json`, `vitest.config.ts` | Component evidence is not a product end-to-end journey. |
| System / end-to-end | No standalone journey suite is declared in the measured configuration. | `tests/`, `projects/storybook/nextjs/` | Do not substitute Storybook tests for system validation. |
| Security | Gitleaks, Hadolint, dependency, Compose, hardening, and Zizmor routes cover named classes. | `.pre-commit-config.yaml`, `ci-quality.yml` | A scanner/configuration is not a clean security certification. |
| Independent review | Task review records require evidence-range review after author checks. | `tasks/tsk-0004-canonical-research-refresh.md` | Review does not replace an unexecuted oracle or acceptance authority. |

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

| Source                                                                                                                                    | Accessed                                            | Class                             | Verification state                                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Prettier CLI](https://prettier.io/docs/cli)                                                                                              | 2026-08-08T17:45:01+09:00                           | External mutable                  | Verified official page; `--write`, `--check`, ignore, and exit semantics used only to distinguish configuration from execution.                                                                                    |
| [pre-commit documentation](https://pre-commit.com/)                                                                                       | 2026-08-08T17:45:01+09:00                           | External mutable                  | Verified official project page; hook stages, file filters, all-files behavior, and non-zero failure semantics used.                                                                                                |
| [TypeScript `noEmit`](https://www.typescriptlang.org/tsconfig/noEmit.html)                                                                | 2026-08-08T17:45:01+09:00                           | External mutable                  | Verified official page; upstream capability only; tracked project config remains local evidence.                                                                                                                   |
| [Vitest coverage](https://vitest.dev/guide/coverage.html)                                                                                 | 2026-08-08T17:45:01+09:00                           | External mutable                  | Verified official page; coverage capability only; tracked thresholds define this project.                                                                                                                          |
| [Storybook Vitest addon](https://storybook.js.org/docs/writing-tests/integrations/vitest-addon)                                           | 2026-08-08T17:45:01+09:00                           | External mutable                  | Verified official page; Storybook/Vitest browser capability only; local configuration defines adoption depth.                                                                                                      |
| [ESLint getting started](https://eslint.org/docs/latest/use/getting-started)                                                              | 2026-08-08T17:45:01+09:00                           | External mutable                  | Verified official page; lint capability only; project package/config define local enforcement.                                                                                                                     |
| [GitHub workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)                         | 2026-08-08T17:45:01+09:00                           | External mutable                  | Verified official page with redirect to current route; job/step/failure/timeout semantics only.                                                                                                                    |
| [GitHub secure use](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) | 2026-08-08T17:45:01+09:00                           | External mutable                  | Verified official page with redirect; least privilege and SHA-pinning guidance only.                                                                                                                               |
| [Pre-commit configuration](../../../../.pre-commit-config.yaml)                                                                           | 2026-08-08; re-verified 2026-08-14                  | Workspace tracked                 | Complete 24-hook inventory (17 default/6 pre-push/1 commit-msg) re-read and re-counted at `ece3eda9`; matches `c57d33f`.                                                                                           |
| [Typed workflow registry](../../../../.github/workflow-contract.yml)                                                                      | 2026-08-08                                          | Workspace tracked                 | Complete root/leaf/profile expansion and QA entrypoints re-derived.                                                                                                                                                |
| [CI quality workflow](../../../../.github/workflows/ci-quality.yml)                                                                       | 2026-08-08                                          | Workspace tracked                 | Sixteen job definitions, skipped ESLint duplication, timeouts, permissions, and two-leaf alignment behavior verified.                                                                                              |
| [Storybook package scripts](../../../../projects/storybook/nextjs/package.json)                                                           | 2026-08-08                                          | Workspace tracked                 | Lint, typecheck, test, coverage, Next.js build, and Storybook build scripts verified.                                                                                                                              |
| [Vitest configuration](../../../../projects/storybook/nextjs/vitest.config.ts)                                                            | 2026-08-08                                          | Workspace tracked                 | Playwright/Chromium Storybook project and four 90% thresholds verified.                                                                                                                                            |
| [CI gate contract tests](../../../../tests/lib/gate/test_ci_gate_contract.py)                                                           | 2026-08-11 (was 2026-08-08); re-verified 2026-08-14 | Workspace tracked                 | Re-verified at `ece3eda9` via direct file count: 24 Python and 2 shell test files (22 Python at the Task 7 baseline `c57d33f`); file presence is not a full-suite result.                                          |
| [Repository-contract validation dependencies](../../../../scripts/requirements.txt)                                                       | 2026-08-14                                          | Workspace tracked                 | `PyYAML>=6.0,<7.0`, `markdown-it-py>=3.0,<4.0`, `html5lib>=1.1,<2.0` read directly; the `html5lib` pin is the source of the re-verified gap below.                                                                 |
| [Pre-commit orchestrator pin](../../../../scripts/requirements-pre-commit.txt)                                                            | 2026-08-14                                          | Workspace tracked                 | `pre-commit==4.6.1`, a separate pinned dependency set from `scripts/requirements.txt`; distinguishes orchestrator-version parity from validation-dependency parity.                                                |
| Repository contract checker (retired path: `../../../../scripts/validation/check-repo-contracts.sh`)                                                     | 2026-08-14                                          | Workspace tracked/local execution | Run directly today in this session's default interpreter at `ece3eda9`: `failures=1`, exactly the `AGC-DEPENDENCY-MISSING path=html5lib` governance-memory finding; confirmed by direct `import html5lib` failure. |
| [GitHub governance](../../../00.agent-governance/policies/github-governance.md)                                                              | 2026-08-08                                          | Workspace tracked policy          | Local/CI/remote split, controlled wrapper boundary, and change-type evidence matrix.                                                                                                                               |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                                                               | 2026-08-08                                          | Workspace tracked stale/advisory  | Built from `f8a72211`; corroborated and not used as current proof.                                                                                                                                                 |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Give generated changes an explicit artifact-specific QA route. | Inspect selected gate and Task evidence. | A generic green claim is insufficient. |
| architecture | applies | Review quality attributes and contract changes with their owner. | Inspect traceability and design evidence. | Static checks do not validate architecture fitness. |
| common | applies | Keep shared hooks and conventions narrowly scoped. | Inspect hook filters and stage declarations. | Filtered hooks may not cover a file. |
| docs | applies | Run metadata/link checks appropriate to documentation changes. | Record command and result. | Markdown lint is not factual review. |
| infra | applies | Use declared Compose/security checks for a concrete infra change. | Inspect named gate/oracle. | Static checks do not observe a live target. |
| ops | applies | Require operational acceptance and recovery evidence for release work. | Inspect runbook/event evidence. | CI does not establish release readiness. |
| qa | applies | Preserve the taxonomy from formatter through independent review. | Map each result to its actual oracle. | Coverage is not validation. |
| security | applies | Use the relevant scanner/control and security review. | Record target, version, result, and disposition. | A named scanner is not an absence-of-vulnerabilities claim. |

## Maintenance

Re-measure the hook inventory, test files, project scripts, coverage thresholds,
typed expansions, and workflow jobs whenever their owners change. Reopen all
mutable primary documentation before changing a capability conclusion. Keep
configuration, local execution, CI definition, hosted result, remote
enforcement, runtime acceptance, and deployment evidence in separate fields.

## Related Documents

- [Verification and validation](./m0019-verification-validation.md)
- [Automation pipeline and workflow topology](./m0004-automation-pipeline-workflow.md)
- [Workspace baseline](./m0020-workspace-baseline.md)
- [Scope application matrix](./m0015-scope-application-matrix.md)
- [Spec-driven SDLC](./m0018-spec-driven-sdlc.md)
- [Document metadata lifecycle](./m0006-document-metadata-lifecycle.md)
- [GitHub governance](../../../00.agent-governance/policies/github-governance.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
