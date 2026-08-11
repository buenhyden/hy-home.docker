---
status: active
artifact_id: reference:agentic-research:quality-ci-formatting
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-07
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md -->

# Reference: Quality, CI, CD, QA, and Formatting

## Overview

This reference compares primary quality and delivery guidance with the tracked
local, CI, and remote evidence surfaces in `hy-home.docker`. It inventories the
actual job and gate definitions at baseline
`ab3a047511c2bf9b5a95ebac737f3ebdb5589384`; generated Graphify data is
navigation-only because its report was built from older commit `30df271a`.

## Purpose

Give agents a source-backed gate taxonomy that separates formatting, linting,
syntax, type, test, build, coverage, security, traceability, and drift evidence
instead of treating “QA passed” as one undifferentiated claim.

## Repository Role

This Stage 90 reference explains tracked QA evidence. It does not define new
jobs, hooks, required checks, branch protection, formatter adoption, or scanner
policy. The [QA scope](../../../00.agent-governance/scopes/qa.md), tracked
scripts/configuration, and GitHub governance remain the active owners.
Generated-code ownership, review thresholds, escalation, and safe vibe-coding
criteria belong to
[`agent-instructions-vibe-coding.md`](./agent-instructions-vibe-coding.md);
this file owns only the concrete QA evidence-surface inventory.

## Scope

### In Scope

- Actual tracked workflow, pre-commit, and local-runner inventories
- Local, CI, and remote-only evidence classes and blocking behavior
- Primary-source comparison for Actions, pre-commit, EditorConfig, Prettier,
  DORA metrics, and continuous delivery
- Current gaps, canonical owners, and confidence

### Out of Scope

- Workflow, script, hook, tool-configuration, runtime, or remote GitHub changes
- Claims that local execution reproduces GitHub permissions or protected checks
- Adoption of any external source as workspace policy

## Definitions / Facts

- **Formatting** changes representation without supplying lint, syntax, type,
  test, build, coverage, or security evidence by itself.
- **Linting** reports rule or style violations; **syntax** proves only that a
  parser accepts the input; **type checking** proves the configured static type
  contract.
- **Test**, **build**, and **coverage** are separate: passing tests do not prove
  a production build, and coverage does not prove test quality.
- **Security evidence** includes secret, workflow, container, hardening, and
  dependency checks; it is not interchangeable with formatting or tests.
- **Blocking** below means a command or tracked job exits non-zero. It does not
  prove that GitHub currently requires that job before merge.
- **CI** builds and verifies changes on repository events. **CD** promotes a
  release candidate through named environments and records deployment outcome;
  build or tag verification alone is not CD.
- **Remote-only / unknown** means the tracked repository cannot establish
  current authenticated enforcement. The latest bounded observation at
  `2026-07-26T18:22:32+09:00` contains public repository/run metadata only;
  authenticated rulesets, branch protection, environments, secrets, and
  variables remain unverified.
- **Required checks** are remote branch/ruleset configuration that names check
  contexts; a matching local command, workflow file, or successful historical
  run does not prove the requirement is currently enforced.
- **Rulesets** and classic branch protection can both impose remote rules. Their
  observed configuration and evaluation belong to remote evidence, not to the
  tracked CI definition inventory.

## Tracked Inventory

The seven files under [`.github/workflows/`](../../../../.github/workflows/) define
**23 job IDs**: 16 in `ci-quality.yml` and seven in the other six workflows.
The quality workflow's 16 IDs are:

`docs-traceability`, `docs-implementation-alignment`, `repo-contracts`,
`agent-output-eval-fixture-gate`, `supply-chain-fixture-policy`,
`dependency-vulnerability-audit`,
`git-flow-contract`, `compose-validation`,
`compose-all-profiles-validation`, `infrastructure-hardening`,
`template-security-baseline`, `quickwin-baseline`, `pre-commit`,
`frontend-quality`, `storybook-coverage`, and `zizmor`.

The [pre-commit configuration](../../../../.pre-commit-config.yaml) defines
**24 hook IDs** across pre-commit, pre-push, and commit-msg stages. This hook
count is not the local-runner count.

The local runner was restructured since the previous revalidation and the old
counts no longer describe it. [`run-local-qa-gates.sh`](../../../../scripts/validation/run-local-qa-gates.sh)
is now a **63-line dispatcher** containing no gate logic; each mode `exec`s
`run-ci-gate.py` with a profile name drawn from
[`.github/workflow-contract.yml`](../../../../.github/workflow-contract.yml).
The previously documented `run_script_backed_gates` function, its 13 direct
calls, and its four helper groups have been removed.

Registered gate counts, measured on `2026-08-07` via
`run-ci-gate.py --profile <p> --list`:

| Profile               | Invocation                    |       Registered gates |
| --------------------- | ----------------------------- | ---------------------: |
| `local-script-backed` | default, or `--script-backed` |                     34 |
| `local-all-profiles`  | `--all-profiles`              |                     35 |
| `local-harness`       | `--harness`                   |                     32 |
| `ci`                  | CI job steps only             | 38 (32 leaf + 6 setup) |

These supersede the previously recorded 24 script-backed, 22 harness, and
"25 bullets" figures. `--list` still executes nothing. `recommend-qa-gates.sh`
is no longer only advisory stdout: it is now reachable in CI through the
`leaf.docs-qa-gate-recommendations` gate, while remaining non-blocking advice
rather than a pass/fail gate. The separate controlled all-files wrapper is not
a runner step in any profile. The runner separates local checks from
CI/local-tooling and remote-only responsibilities; it is not a full CI replica.

### Current validator results

Measured on `2026-08-07`, read-only:

- `bash scripts/validation/validate-docker-compose.sh` — passes,
  `services_total=5` on the `core` profile.
- `bash scripts/validation/check-repo-contracts.sh` — `failures=4`. The counter
  reports failing _subjects_, not failing lines; the four subjects emit 12 FAIL
  lines between them:

| Failing subject                 | FAIL lines | Substance                                                                                                                     |
| ------------------------------- | ---------: | ----------------------------------------------------------------------------------------------------------------------------- |
| Metadata comparison guide drift |          1 | `.env` and `.env.example` key sets differ; `INFLUXDB_BUCKET`, `INFLUXDB_ORG`, and `INFLUXDB_USERNAME` exist only in `.env`    |
| Storybook coverage contract     |          6 | `ci-quality.yml` no longer contains six expected literal `npm` commands, because those steps moved behind typed gate adapters |
| Governance memory contract      |          1 | `AGC-DEPENDENCY-MISSING path=html5lib`; declared in `scripts/requirements.txt`, not installed                                 |
| Script reference integrity      |          4 | Two Stage 04 documents reference `scripts/governance/validate-cross-links.sh`, which is absent                                |

The Storybook subject is the informative one: it is a **contract-lag failure,
not a quality regression**. The commands still run; the repo-contract check
still expects to find them as literals inside the workflow file, where the
typed-gate migration no longer puts them. Reporting this as a Storybook quality
failure would be wrong. Reading `failures=4` as "four problems" would also be
wrong — it is four subjects covering twelve findings and at least two distinct
root causes.

## QA Sub-Areas

"QA passed" is not one claim. The tracked surfaces divide into four named
sub-areas with materially different coverage, and the gaps only become visible
once they are separated.

### Formatting

Whitespace and newline hygiene is enforced: `trailing-whitespace`,
`end-of-file-fixer`, and `mixed-line-ending` run as pre-commit hooks, and
`post-tool-validate.sh` normalizes the same properties on changed files.
`.editorconfig` supplies editor defaults, which are editor-dependent and not a
repository gate.

Prettier remains configured but **unenforced**. `.prettierrc.json` and
`.prettierignore` are tracked, but no pre-commit hook, no CI gate, and no hook
script invokes Prettier. The only occurrence of the string in shared automation
is `\.prettierignore` inside a pre-commit `files:` path regex — a path
pattern, not an invocation. This was re-verified on `2026-08-07` and the
earlier finding stands unchanged.

### Linting

| Language / surface | Linter                      | Wired in                                                                |
| ------------------ | --------------------------- | ----------------------------------------------------------------------- |
| Shell              | `shellcheck`                | pre-commit; conditionally in `post-tool-validate.sh`                    |
| YAML               | `yamllint` with `.yamllint` | pre-commit                                                              |
| Markdown           | `markdownlint-cli2`         | pre-commit                                                              |
| Dockerfiles        | `hadolint-docker`           | pre-commit                                                              |
| GitHub Actions     | `actionlint`                | pre-commit                                                              |
| Actions security   | `zizmor==1.28.0`            | CI `zizmor` job, pinned in `ci_gate_adapters.py:1010`                   |
| JS/TS              | ESLint                      | dedicated `frontend-quality` CI job; `eslint-nextjs` hook skipped in CI |
| **Python**         | **none**                    | **not wired anywhere**                                                  |

The Python row is the substantive gap. `.pre-commit-config.yaml` declares 24
hook IDs across eight upstream repositories plus local hooks, and none of them
is `ruff`, `black`, `mypy`, `pylint`, `flake8`, or `pyright`. No CI job lints
Python either.

This matters more than a missing linter usually would, because of where the
repository's Python actually lives.
`scripts/validation/check-repo-contracts.sh` is 4,045 lines. Of those,
**3,555 lines sit inside 34 `python3 - <<'PY'` heredocs**, leaving roughly
422 lines of actual shell outside them. ShellCheck runs on the file and sees
only that shell wrapper; the heredoc bodies are opaque string literals to it.
So the single largest validator in the repository is approximately 88 percent
unlinted Python by line count, and the tool that appears to cover it does not.

The same pattern recurs across `scripts/validation/`, which holds sizeable
standalone Python — `agent_governance_contract.py`, `check-document-metadata.py`,
`check-document-corpus-lifecycle.py`, `check-supply-chain-policy.py`,
`github_workflow_contract.py`, and the `ci_gate_*.py` trio among them. All of it
is currently unlinted and untyped by any tracked gate.

### Testing

Testing is present but narrow and unevenly located.

- **Frontend**: Vitest via `npm run test`, with the CI route being
  `storybook-coverage` running the coverage script. There is no separate CI
  `test` job.
- **Repository logic**: regression gates registered in the typed contract —
  `leaf.ci-gate-contract-regressions`, `leaf.ci-gate-runner-regressions`,
  `leaf.ci-gate-adapter-regressions`, `leaf.workflow-contract-regressions`,
  `leaf.repo-contracts-control-plane-regressions`,
  `leaf.local-document-corpus-lifecycle-tests`,
  `leaf.local-target-surface-regressions`,
  `leaf.local-target-delta-regressions`, and `leaf.ci-precommit-regressions`
  (which runs `tests/validation/test_run_ci_precommit.sh`).
- **Agent output**: 11 exact synthetic fixtures plus 16 deterministic
  regressions behind `leaf.agent-output-eval-fixture-gate`.
- **Coverage**: measured only for the Storybook Next.js project. No coverage
  figure exists for the shell or Python validator corpus, and no threshold is
  enforced outside the frontend.

The asymmetry is worth naming plainly: the validators that gate the entire
repository have regression tests for their control plane, but no line-coverage
measurement and no static analysis of their own implementation language.

### Syntax and grammar checking

"Syntax" and "lint" are distinct evidence classes here and the distinction is
load-bearing.

| Input                | Check                                                                | Class                           |
| -------------------- | -------------------------------------------------------------------- | ------------------------------- |
| Shell                | `bash -n` via `leaf.local-shell-syntax`                              | parse only                      |
| JSON                 | `check-json`; selective `python3 -m json.tool` in the post-tool hook | parse only                      |
| TOML                 | `check-toml`                                                         | parse only                      |
| YAML                 | `yamllint`                                                           | style rules, not schema         |
| Dependabot config    | `check-dependabot` (check-jsonschema)                                | schema                          |
| Workflow expressions | `actionlint`                                                         | syntax and expression semantics |
| Compose              | `validate-docker-compose.sh` rendering `docker compose config`       | resolved-model syntax           |
| Markdown prose       | `markdownlint-cli2`                                                  | structural rules                |

`check-jsonschema` is present but is bound to the single `check-dependabot`
hook; it is not a general JSON-schema gate across the repository's many typed
JSON contracts.

Natural-language grammar and spelling are **not checked by any tracked gate**.
`markdownlint-cli2` enforces Markdown structure — heading order, list style,
line length — and no more. No spell-checker, prose linter, or terminology
gate exists. Document _contract_ validation
(`check-document-metadata.py`, `check-document-corpus-lifecycle.py`) checks
frontmatter keys, heading contracts, and lifecycle state, not language quality.
Claims about documentation "quality" should therefore be scoped to structure
and metadata, never to prose correctness.

## Quality Gate Matrix

| Gate                           | Purpose                                                                                             | Local command / tool                                                                                                                                                                                                                                                                     | CI job                                                                        | Evidence class           | Blocking behavior                                                               | External basis                                                                                                                                        | Gap / recommendation                                                                                                                                                                                                              |
| ------------------------------ | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Whitespace and diff hygiene    | Detect trailing whitespace and conflict-marker drift                                                | `git diff --check`; `trailing-whitespace`, `mixed-line-ending`, `end-of-file-fixer` in [pre-commit](../../../../.pre-commit-config.yaml)                                                                                                                                                 | `pre-commit`                                                                  | formatting               | Blocks the local runner or hook when applicable; CI job failure is separate     | [EditorConfig](https://editorconfig.org/) supports editor-consistent style                                                                            | Keep the tracked local runner authoritative. Owner: [`scripts/validation/run-local-qa-gates.sh`](../../../../scripts/validation/run-local-qa-gates.sh).                                                                           |
| Editor defaults                | Align charset, LF endings, indentation, final newline, and whitespace defaults                      | [`.editorconfig`](../../../../.editorconfig)                                                                                                                                                                                                                                             | None directly                                                                 | formatting configuration | Editor-dependent; not a repository gate by itself                               | [EditorConfig site](https://editorconfig.org/) and [specification](https://spec.editorconfig.org/)                                                    | Do not claim editor compliance from file presence. Owner: [`.editorconfig`](../../../../.editorconfig).                                                                                                                           |
| Prettier configuration         | Define shared print/style options for supported files                                               | [`.prettierrc.json`](../../../../.prettierrc.json) and [`.prettierignore`](../../../../.prettierignore)                                                                                                                                                                                  | None                                                                          | formatting configuration | Non-blocking in tracked shared automation                                       | [Prettier overview](https://prettier.io/docs) and [CLI](https://prettier.io/docs/cli) document formatter and check-mode behavior                      | The shared [post-tool hook](../../../../scripts/hooks/post-tool-validate.sh) does not invoke Prettier, and no tracked shared job enforces it. Owner: [common scope](../../../00.agent-governance/scopes/common.md).               |
| Markdown lint                  | Check Markdown rules                                                                                | `markdownlint-cli2` in [pre-commit](../../../../.pre-commit-config.yaml)                                                                                                                                                                                                                 | `pre-commit`                                                                  | lint                     | Blocks applicable hook/CI execution                                             | [pre-commit](https://pre-commit.com/) supports configured hook execution                                                                              | Keep claims tied to the hook ID, not all Markdown semantics. Owner: [pre-commit config](../../../../.pre-commit-config.yaml).                                                                                                     |
| YAML lint                      | Check YAML style rules                                                                              | `yamllint` with [`.yamllint`](../../../../.yamllint)                                                                                                                                                                                                                                     | `pre-commit`                                                                  | lint                     | Blocks applicable hook/CI execution                                             | pre-commit supports file-filtered hooks                                                                                                               | Relaxed rules do not prove workflow semantics. Owner: [pre-commit config](../../../../.pre-commit-config.yaml).                                                                                                                   |
| JSON syntax                    | Parse JSON files accepted by the configured hook                                                    | `check-json`; selective `python3 -m json.tool` in [post-tool validation](../../../../scripts/hooks/post-tool-validate.sh)                                                                                                                                                                | `pre-commit`                                                                  | syntax                   | Blocks applicable hook/CI execution                                             | pre-commit supports per-hook file selection                                                                                                           | Post-tool parsing covers only three named JSON surfaces. Owner: [pre-commit config](../../../../.pre-commit-config.yaml).                                                                                                         |
| TOML syntax                    | Parse TOML inputs                                                                                   | `check-toml` in [pre-commit](../../../../.pre-commit-config.yaml)                                                                                                                                                                                                                        | `pre-commit`                                                                  | syntax                   | Blocks applicable hook/CI execution                                             | pre-commit supports configured parser hooks                                                                                                           | Syntax does not prove tool-specific semantics. Owner: [pre-commit config](../../../../.pre-commit-config.yaml).                                                                                                                   |
| Shell syntax                   | Parse tracked shell scripts and Claude hooks                                                        | `bash -n` in [local runner](../../../../scripts/validation/run-local-qa-gates.sh)                                                                                                                                                                                                        | None directly                                                                 | syntax                   | Blocks the script-backed or harness run                                         | No fixed external source mandates this repository command                                                                                             | Keep separate from ShellCheck. Owner: [`run-local-qa-gates.sh`](../../../../scripts/validation/run-local-qa-gates.sh).                                                                                                            |
| ShellCheck                     | Detect shell correctness and portability issues                                                     | `shellcheck` in [pre-commit](../../../../.pre-commit-config.yaml); conditional post-tool check                                                                                                                                                                                           | `pre-commit`                                                                  | lint                     | Blocks applicable hook/CI execution                                             | pre-commit supports multi-language hooks                                                                                                              | `recommend-qa-gates.sh` is explicitly excluded. Owner: [pre-commit config](../../../../.pre-commit-config.yaml).                                                                                                                  |
| actionlint                     | Validate GitHub Actions syntax/expressions                                                          | `actionlint` in [pre-commit](../../../../.pre-commit-config.yaml)                                                                                                                                                                                                                        | `pre-commit`                                                                  | syntax/lint              | Blocks workflow-file hook/CI execution                                          | [Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) defines keys, triggers, jobs, and steps | Local validation cannot prove a remote run. Owner: [pre-commit config](../../../../.pre-commit-config.yaml).                                                                                                                      |
| Hadolint                       | Lint Dockerfiles                                                                                    | `hadolint-docker` in [pre-commit](../../../../.pre-commit-config.yaml)                                                                                                                                                                                                                   | `pre-commit`                                                                  | lint/security            | Blocks applicable hook/CI execution                                             | pre-commit supports file-filtered hooks                                                                                                               | Applies only to matching Dockerfiles. Owner: [pre-commit config](../../../../.pre-commit-config.yaml).                                                                                                                            |
| Secret scanning                | Detect committed secret patterns                                                                    | `gitleaks` with [`.gitleaks.toml`](../../../../.gitleaks.toml) via pre-commit                                                                                                                                                                                                            | `pre-commit`                                                                  | security                 | Blocks applicable hook/CI execution                                             | [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use) supports least privilege and secret/log caution                 | Scanner pass is not proof that no secret exists. Owner: [security scope](../../../00.agent-governance/scopes/security.md).                                                                                                        |
| ESLint                         | Lint Storybook Next.js source                                                                       | `npm run lint --prefix projects/storybook/nextjs`; `eslint-nextjs` hook                                                                                                                                                                                                                  | `frontend-quality`; skipped in CI `pre-commit` via `SKIP`                     | lint                     | Blocks local command or dedicated CI job                                        | pre-commit supports selective skip; duplication policy is repo-local                                                                                  | Keep the dedicated CI job as the CI evidence. Owner: [`projects/storybook/nextjs/package.json`](../../../../projects/storybook/nextjs/package.json).                                                                              |
| TypeScript                     | Type-check without emitting                                                                         | `npm run typecheck --prefix projects/storybook/nextjs`                                                                                                                                                                                                                                   | `frontend-quality`                                                            | type                     | Blocks local command or CI job                                                  | No fixed external source defines this project contract                                                                                                | Applies only to the Storybook Next.js project. Owner: [`package.json`](../../../../projects/storybook/nextjs/package.json).                                                                                                       |
| Storybook tests                | Execute the configured Vitest Storybook project                                                     | `npm run test --prefix projects/storybook/nextjs`                                                                                                                                                                                                                                        | `storybook-coverage` runs the same project through the coverage script        | test                     | Local command or CI coverage job exits non-zero                                 | Fowler describes automated tests as delivery-pipeline feedback                                                                                        | A coverage run is the tracked CI route; no separate `test` job exists. Owner: [`package.json`](../../../../projects/storybook/nextjs/package.json).                                                                               |
| Frontend builds                | Build the Next.js app and static Storybook                                                          | `npm run build` and `npm run build-storybook` with project prefix                                                                                                                                                                                                                        | `frontend-quality`                                                            | build                    | Blocks local commands or CI job                                                 | [Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html) uses builds/tests as pipeline feedback                                  | Build success is not deployment evidence. Owner: [`ci-quality.yml`](../../../../.github/workflows/ci-quality.yml).                                                                                                                |
| Storybook coverage             | Collect configured browser-test coverage                                                            | `npm run coverage --prefix projects/storybook/nextjs`                                                                                                                                                                                                                                    | `storybook-coverage`                                                          | coverage/test            | Blocks local command or CI job                                                  | DORA metrics do not define code-coverage thresholds                                                                                                   | Docs-only Task 4 coverage is N/A. Owner: [QA scope](../../../00.agent-governance/scopes/qa.md).                                                                                                                                   |
| Compose validation             | Render root and governed profile configurations                                                     | [`validate-docker-compose.sh`](../../../../scripts/validation/validate-docker-compose.sh)                                                                                                                                                                                                | `compose-validation`, `compose-all-profiles-validation`                       | syntax/configuration     | Blocks local runner or either CI job                                            | No fixed source substitutes for Docker-specific validation                                                                                            | Keep core/all-profile evidence distinct. Owner: [`validate-docker-compose.sh`](../../../../scripts/validation/validate-docker-compose.sh).                                                                                        |
| Hardening and baselines        | Check tier hardening, template/security, and QuickWin controls                                      | [`check-all-hardening.sh`](../../../../scripts/hardening/check-all-hardening.sh), [`check-template-security-baseline.sh`](../../../../scripts/validation/check-template-security-baseline.sh), [`check-quickwin-baseline.sh`](../../../../scripts/validation/check-quickwin-baseline.sh) | `infrastructure-hardening`, `template-security-baseline`, `quickwin-baseline` | security                 | Blocks local runner or corresponding CI job                                     | GitHub secure-use guidance is workflow-specific, not an infra-control mapping                                                                         | Preserve three separately named results. Owner: [security scope](../../../00.agent-governance/scopes/security.md).                                                                                                                |
| Docs traceability              | Check execution/operations links                                                                    | [`check-doc-traceability.sh`](../../../../scripts/validation/check-doc-traceability.sh)                                                                                                                                                                                                  | `docs-traceability`                                                           | traceability             | Blocks local runner or CI job                                                   | No external source defines the repository taxonomy                                                                                                    | Owner: [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md).                                                                                                                                    |
| Docs implementation alignment  | Compare active docs with tracked implementation surfaces                                            | [`check-doc-implementation-alignment.sh`](../../../../scripts/validation/check-doc-implementation-alignment.sh)                                                                                                                                                                          | `docs-implementation-alignment`                                               | traceability             | Blocks local runner or CI job                                                   | External sources do not prove repo-local current truth                                                                                                | Owner: [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md).                                                                                                                                    |
| Repository contracts           | Validate taxonomy, templates, workflow/job coupling, generated references, and implementation drift | [`check-repo-contracts.sh`](../../../../scripts/validation/check-repo-contracts.sh)                                                                                                                                                                                                      | `repo-contracts`                                                              | contract/security        | Blocks local runner or CI job                                                   | GitHub syntax supports job structure, not repository-specific contracts                                                                               | Owner: [`check-repo-contracts.sh`](../../../../scripts/validation/check-repo-contracts.sh).                                                                                                                                       |
| Agent-output eval fixtures     | Validate and score 11 exact synthetic fixtures plus 16 deterministic regressions                    | [`run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions`](../../../../scripts/validation/run-agent-output-eval-fixtures.sh)                                                                                                                                             | `agent-output-eval-fixture-gate`                                              | test/eval                | CI/local routing requires exact fixture and regression pass markers             | No fixed external source defines repository fixture semantics                                                                                         | This gates bounded repository semantics, not live model quality. Owner: [eval fixture runner](../../../../scripts/validation/run-agent-output-eval-fixtures.sh).                                                                  |
| Dependency vulnerability audit | Fail on high-severity Storybook Next.js dependency findings                                         | `npm audit --audit-level=high --prefix projects/storybook/nextjs`                                                                                                                                                                                                                        | `dependency-vulnerability-audit`                                              | security                 | Dedicated CI job blocks on threshold                                            | GitHub secure-use is complementary, not npm policy                                                                                                    | Scope is one project/package lock. Owner: [`ci-quality.yml`](../../../../.github/workflows/ci-quality.yml).                                                                                                                       |
| Provider drift                 | Compare generated Codex/Gemini projections with canonical sources                                   | [`sync-provider-surfaces.sh`](../../../../scripts/operations/sync-provider-surfaces.sh) verify mode                                                                                                                                                                                      | `repo-contracts` supplies broader catalog parity, not the exact command       | drift                    | Blocks the local runner on detected drift                                       | No fixed external source defines provider projection policy                                                                                           | Verification does not prove provider runtime acceptance. Owner: [provider adapter model](../../../00.agent-governance/providers/agents-md.md).                                                                                    |
| Generated-data freshness       | Check Wiki index and generated contract snapshots                                                   | [`generate-llm-wiki-index.sh --check`](../../../../scripts/knowledge/generate-llm-wiki-index.sh); generators checked inside repo contracts                                                                                                                                               | `repo-contracts`                                                              | freshness                | Blocks local runner/repo-contracts when stale                                   | External sources do not define generated artifact ownership                                                                                           | Never hand-edit generated data; run its canonical generator. Owner: [QA scope](../../../00.agent-governance/scopes/qa.md).                                                                                                        |
| Workflow security scan         | Analyze Actions and upload SARIF                                                                    | No equivalent local runner step                                                                                                                                                                                                                                                          | `zizmor`                                                                      | security                 | GitHub job blocks when run; SARIF upload needs remote permissions               | GitHub secure use supports SHA pinning, least privilege, and injection caution                                                                        | The tracked command pins patched `zizmor==1.28.0`; advisory GHSA-f42p-wjw5-97qh affects only 1.27.0. Owner: [GitHub governance](../../../00.agent-governance/rules/github-governance.md).                                         |
| Remote branch protection       | Require remote checks/reviews before merge                                                          | No local command can prove enforcement                                                                                                                                                                                                                                                   | Remote GitHub settings                                                        | remote enforcement       | The 2026-07-26 public observation cannot read authenticated control-plane state | Rulesets can enforce branch/tag interaction, but documentation and public run metadata do not prove configuration                                     | Treat rulesets, branch protection, environments, secrets, and variables as unverified until authenticated readback is separately authorized. Owner: [GitHub governance](../../../00.agent-governance/rules/github-governance.md). |

## Workspace Comparison and Ownership

| Category                | Current state                                                                                                                                                                                                                                                                                                                                                                     | Primary comparison                                                                                                              | Status                | Gap                                                                                                                                          | Recommendation                                                                                                      | Canonical owner                                                  | Evidence                                                               | Confidence                                   |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------- |
| QA and evidence classes | Tracked gates distinguish format, lint, syntax, type, test, build, coverage, security, traceability, eval, and freshness evidence.                                                                                                                                                                                                                                                | pre-commit supports hook orchestration; GitHub Actions supports jobs/steps.                                                     | Implemented           | Applicability still varies by changed surface.                                                                                               | Record named commands/jobs and N/A rationale rather than “all QA.”                                                  | `docs/00.agent-governance/scopes/qa.md`                          | Matrix above; tracked runner/workflow/config                           | High                                         |
| CI feedback             | Seven workflows define 23 jobs; `ci-quality.yml` defines 16 independent quality jobs and none declares a deployment environment. The latest public remote run observation contains 15 jobs and a failure with unverified root cause.                                                                                                                                              | GitHub workflow syntax and monitoring docs define jobs, logs, and run views; rulesets remain a separate control plane.          | Partially Implemented | Tracked definitions do not prove successful runs or current required-check enforcement; public metadata cannot explain the observed failure. | Report exact tracked jobs, observed run metadata, and authenticated enforcement as separate evidence classes.       | `docs/00.agent-governance/rules/github-governance.md`            | `.github/workflows/*.yml`; GitHub Actions control-plane observation    | High                                         |
| CD / promotion          | No tracked workflow deploys an application or infrastructure target, references a GitHub environment, promotes across environments, or performs rollback.                                                                                                                                                                                                                         | GitHub environments support reviewer/custom protection rules, branch restrictions, environment secrets, and deployment history. | Missing               | Green CI/build/tag checks can be mislabeled as deployment readiness.                                                                         | Define promotion, approval, deployment record, verification, and rollback in a later Stage 03/04 delivery contract. | `docs/03.specs/README.md`                                        | Workflow scan plus Stage 05 release runbook                            | High                                         |
| Release record          | `CHANGELOG.md`, a manual release-management runbook, and a tag-triggered changelog coverage check exist; the workflow does not create release notes or assets.                                                                                                                                                                                                                    | GitHub Releases bind a tagged iteration to release notes and optional downloadable assets.                                      | Partially Implemented | Tag-string coverage is not a complete release record or artifact integrity statement.                                                        | Preserve the manual readiness boundary and define release artifact/record ownership with future CD work.            | `docs/05.operations/00-workspace/ops-0009-release-management/runbook.md` | `CHANGELOG.md`; `.github/workflows/generate-changelog.yml`             | High                                         |
| Pre-commit semantics    | The config defines 24 hook IDs; hooks are stage/file filtered, and CI runs the suite with `eslint-nextjs` skipped in favor of its dedicated job. Direct agent all-files execution is prohibited; the implemented wrapper requires an initially clean linked worktree, tracked Task evidence, explicit allowed prefixes, a Git-visible snapshot comparison, and sanitized results. | pre-commit documents staged-file default execution, `--all-files`, explicit stages, file selection, and CI use.                 | Implemented           | Hook count is not equivalent to executed coverage for every change or stage; wrapper observation excludes ignored/outside paths.             | Use the controlled wrapper only at the approved QA stage and record markers/path sets rather than raw logs.         | `.pre-commit-config.yaml` and wrapper                            | Config, wrapper tests, CI workflow                                     | High within the bounded observation contract |
| Formatting              | EditorConfig and Prettier configuration exist; pre-commit/post-tool supply other formatting checks.                                                                                                                                                                                                                                                                               | EditorConfig specifies hierarchical style settings; Prettier documents parsing/reprinting and a CI check mode.                  | Partially Implemented | No tracked shared automation invokes Prettier.                                                                                               | Do not imply Prettier enforcement unless the active owner approves and implements it.                               | `docs/00.agent-governance/scopes/common.md`                      | `.editorconfig`, `.prettierrc.json`, `.prettierignore`, post-tool hook | High                                         |

## Analysis

The tracked layers intentionally differ. The default `local-script-backed`
profile registers 34 gates, `--all-profiles` 35, `--harness` 32, and list mode
provides inventory without execution. Pre-commit adds 24 file/stage-filtered
hook IDs — 17 at the default pre-commit stage, six at `pre-push`, and one at
`commit-msg`. CI registers 38 entries and adds frontend, coverage, dependency,
document-metadata, git-flow, and SARIF behavior that no local profile carries.
None of those layers proves current branch-protection enforcement. DORA's current five
metrics—change lead time, deployment frequency, failed deployment recovery
time, change fail rate, and deployment rework rate—require production delivery
data this repository task did not collect.

The document-contract rollout follows the same evidence separation. Typed
local validation can report the full historical inventory while blocking only
the safely selected changed/new surface. A tracked CI job may execute that
contract, but only an observed protected-branch rule or ruleset can establish
that GitHub requires its named context before merge. This staged model prevents
schema introduction from becoming an accidental corpus-wide or remote gate.

## Application Notes for This Workspace

- Cite the exact script, hook ID, or workflow job for every QA claim.
- Record `zizmor` as GitHub-only SARIF evidence.
- Record the local runner by mode from the typed registry, not from reading the
  dispatcher: 34 gates for `local-script-backed` (the default), 35 for
  `--all-profiles`, 32 for `--harness`, and 0 for `--list`. The previously
  recorded 20/18 and 24/22 figures are both stale.
- Never claim Python is linted. No `ruff`, `black`, `mypy`, `pylint`, `flake8`,
  or `pyright` is wired into pre-commit or CI, and ShellCheck inspects only the
  ~422-line shell wrapper of `check-repo-contracts.sh`, not the 3,555 heredoc
  lines it carries.
- Never claim prose is checked. `markdownlint-cli2` enforces Markdown structure
  only; no spelling, grammar, or terminology gate exists.
- Read `failures=N` from `check-repo-contracts.sh` as a count of failing
  subjects, not findings, and inspect the subject headers before summarizing.
- Do not claim that post-tool validation runs Prettier.
- Keep remote required-check and branch-protection state unknown unless a
  current direct query is recorded.
- Apply AIV-06 through AIV-10 when generated code is reviewed, then cite the
  exact command, hook, or CI job from this inventory as verification evidence.

## Potential Follow-up / Gap

- Any proposal to enforce Prettier belongs first to the Common scope and an
  approved Stage 03/04 change, not this reference.
- Python static analysis for `scripts/validation/` is the largest uncovered QA
  surface. Any proposal should decide three things before tooling: whether
  heredoc-embedded Python is in scope at all, whether the 34 heredocs in
  `check-repo-contracts.sh` should be extracted into importable modules so a
  linter can reach them, and what severity is blocking versus advisory during
  rollout.
- The `Storybook coverage contract` failure is contract lag from the typed-gate
  migration, not a frontend regression. Fixing it means updating the expected
  literals in `check-repo-contracts.sh` to match gate-adapter indirection, and
  that belongs to the contract owner rather than the frontend owner.
- The `html5lib` dependency gap is environmental: it is declared in
  `scripts/requirements.txt` but not installed, and PEP 668 blocks installation
  into this externally managed interpreter. A virtual environment or a
  distribution package is required; no repository change resolves it.
- Current branch protection and required-check contexts need a separately
  approved/read-only remote verification before an enforcement claim.
- Operating DORA metrics requires application/service deployment and incident
  data sources; CI job presence alone is insufficient.

## Source Rules

- External sources were retrieved on **2026-07-11** and support comparison only.
  GitHub ruleset, protected-branch/required-check, and deployment-environment
  guidance was re-opened on **2026-07-13**; the earlier dated inventory remains
  unchanged.
- The official GitHub secure-use, workflow-syntax, and rulesets pages, plus
  pre-commit, Prettier CLI, and DORA metrics, were re-opened on `2026-08-07`.
  Confirmed: secure use still names full-SHA pinning as the only immutable
  action reference and warns that redaction relies on exact-match; rulesets
  aggregate with classic branch protection and the most restrictive rule wins;
  pre-commit documents version 4.6.1; Prettier `--check` exits 0/1/2 for
  formatted/unformatted/tool-error and `--list-different` prints filenames;
  DORA publishes five metrics and shows a visible last-updated date of
  `2026-01-05`. The GitHub and Prettier pages expose no last-updated date.
- The zizmor advisory index was re-opened on `2026-08-07` and still lists
  exactly one advisory, GHSA-f42p-wjw5-97qh, published `2026-07-21`. The
  advisory index page does not render affected version ranges, so the
  1.27.0-only boundary is carried forward from the earlier direct advisory
  read and is **not re-verified** at this revalidation. The tracked pin is
  still `zizmor==1.28.0`, though it moved out of the workflow YAML into
  `scripts/validation/ci_gate_adapters.py:1010`.
- Tracked YAML and 16 local quality jobs still do not prove remote runs or
  enforcement. The latest public observation records 15 jobs and a failed run,
  while authenticated control-plane state and root cause remain unverified.
- Mutable official pages prove retrieval-time guidance, not historical behavior
  or workspace enforcement.
- Repo-local claims cite tracked sources at baseline `ab3a0475`; Graphify is
  advisory because its report is older.
- No external source in this reference is adopted workspace policy.

## Sources

- Task 4 source ledger - retrieval date, supported claim, evidence-surface class, and caveat for every fixed source
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) - workflow/job/step and trigger syntax
- [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use) - least privilege, untrusted input, secret, and immutable-action guidance
- [GitHub workflow monitoring](https://docs.github.com/en/actions/how-tos/monitor-workflows) - run graph, history, job status, and log evidence surfaces
- [GitHub deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) - deployment approvals, environment secrets, restrictions, and protection rules
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) - layered remote branch/tag rule enforcement
- [zizmor v1.28.0](https://github.com/zizmorcore/zizmor/releases/tag/v1.28.0) and [GHSA-f42p-wjw5-97qh](https://github.com/zizmorcore/zizmor/security/advisories/GHSA-f42p-wjw5-97qh) - patched version and the 1.27.0-only credential debug-log advisory
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) - required status check and merge-protection behavior
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) - tagged release records, notes, and assets
- [pre-commit](https://pre-commit.com/) - hook configuration, local execution, CI use, and skips
- [EditorConfig](https://editorconfig.org/) - cross-editor consistency
- [EditorConfig specification](https://spec.editorconfig.org/) - hierarchical file processing and supported pairs. The site returns a Cloudflare bot challenge to automated clients; version 0.17.2 and the property set were re-verified 2026-08-07 from the `editorconfig/specification` upstream source. The specification defines nine properties, adding `spelling_language` to the eight commonly cited, and states that `unset` removes any pair
- [Prettier overview](https://prettier.io/docs) - formatter behavior and supported inputs
- [Prettier CLI](https://prettier.io/docs/cli) - check-mode and exit-code behavior
- [DORA metrics](https://dora.dev/guides/dora-metrics/) - current five-metric throughput/instability model
- [Martin Fowler: Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html) - releasability and automated pipeline feedback
- [CI workflow](../../../../.github/workflows/ci-quality.yml) - 16 tracked quality job IDs
- [Local QA runner](../../../../scripts/validation/run-local-qa-gates.sh) - 63-line dispatcher selecting a typed profile; holds no gate logic
- [Typed workflow contract](../../../../.github/workflow-contract.yml) - registry defining 80 gate nodes and the local/CI profiles
- [Typed gate runner](../../../../scripts/validation/run-ci-gate.py) - closed-grammar profile and gate executor
- [Repo contracts validator](../../../../scripts/validation/check-repo-contracts.sh) - 4,045 lines, 3,555 of them inside 34 Python heredocs
- [pre-commit config](../../../../.pre-commit-config.yaml) - 24 tracked hook IDs
- [Scripts README](../../../../scripts/README.md) - script lifecycle and authority

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when workflows, gate scripts/configuration, remote evidence, or fixed primary sources change
- **Update Trigger**: Recount from tracked definitions; never copy prior totals without revalidation

## Related Documents

- [research pack index](./README.md)
- [automation, pipeline, and workflow loops](./automation-pipeline-workflow.md)
- [verification and validation](./verification-validation.md)
- [github actions platform](./github-actions-platform.md)
- [workspace baseline](./workspace-baseline.md)
- [agent instructions and safe vibe coding](./agent-instructions-vibe-coding.md)
- [QA scope](../../../00.agent-governance/scopes/qa.md)
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md)
