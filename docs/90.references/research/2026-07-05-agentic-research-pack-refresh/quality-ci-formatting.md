---
status: active
---
<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md -->

# Reference: Quality, CI/CD, QA, and Formatting

## Overview

This reference compares primary quality and delivery guidance with the tracked
local, CI, and remote evidence surfaces in `hy-home.docker`. It inventories the
actual job and gate definitions at baseline
`505277817eee0de4270bc03ae7fb789ef9d02ad3`; generated Graphify data is
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
- **Remote-only / unknown** means the tracked repository cannot establish
  current remote enforcement. The historical proposal records a read-only
  2026-07-04 observation, but this task did not re-query remote state.

## Tracked Inventory

The six files under [`.github/workflows/`](../../../../.github/workflows/) define
**21 job IDs**: 15 in `ci-quality.yml` and six in the other five workflows.
The quality workflow's 15 IDs are:

`docs-traceability`, `docs-implementation-alignment`, `repo-contracts`,
`agent-output-eval-fixture-gate`, `dependency-vulnerability-audit`,
`git-flow-contract`, `compose-validation`,
`compose-all-profiles-validation`, `infrastructure-hardening`,
`template-security-baseline`, `quickwin-baseline`, `pre-commit`,
`frontend-quality`, `storybook-coverage`, and `zizmor`.

The [pre-commit configuration](../../../../.pre-commit-config.yaml) defines
**23 hook IDs** across pre-commit, pre-push, and commit-msg stages. This hook
count is not the local-runner count.

The [`run_script_backed_gates` function](../../../../scripts/validation/run-local-qa-gates.sh)
contains **12 executed `run_step` calls**. The default, `--script-backed`, and
`--all-profiles` modes all execute those 12 gates; `--harness` executes the 8
calls in `run_harness_gates`; and `--list` executes no gate. The list output
names `recommend-qa-gates.sh`, but labels that script advisory and does not
execute it. Therefore the headline local runner inventory remains **12 executed
default/script-backed gates + 1 non-executed advisory recommendation**, not 13
executed gates. The runner separates local checks from CI/local-tooling and
remote-only responsibilities; it is not a full CI replica.

## Quality Gate Matrix

| Gate | Purpose | Local command / tool | CI job | Evidence class | Blocking behavior | External basis | Gap / recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Whitespace and diff hygiene | Detect trailing whitespace and conflict-marker drift | `git diff --check`; `trailing-whitespace`, `mixed-line-ending`, `end-of-file-fixer` in [pre-commit](../../../../.pre-commit-config.yaml) | `pre-commit` | formatting | Blocks the local runner or hook when applicable; CI job failure is separate | [EditorConfig](https://editorconfig.org/) supports editor-consistent style | Keep the tracked local runner authoritative. Owner: [`scripts/validation/run-local-qa-gates.sh`](../../../../scripts/validation/run-local-qa-gates.sh). |
| Editor defaults | Align charset, LF endings, indentation, final newline, and whitespace defaults | [`.editorconfig`](../../../../.editorconfig) | None directly | formatting configuration | Editor-dependent; not a repository gate by itself | [EditorConfig site](https://editorconfig.org/) and [specification](https://spec.editorconfig.org/) | Do not claim editor compliance from file presence. Owner: [`.editorconfig`](../../../../.editorconfig). |
| Prettier configuration | Define shared print/style options for supported files | [`.prettierrc.json`](../../../../.prettierrc.json) and [`.prettierignore`](../../../../.prettierignore) | None | formatting configuration | Non-blocking in tracked shared automation | [Prettier overview](https://prettier.io/docs) and [CLI](https://prettier.io/docs/cli) document formatter and check-mode behavior | The shared [post-tool hook](../../../../scripts/hooks/post-tool-validate.sh) does not invoke Prettier, and no tracked shared job enforces it. Owner: [common scope](../../../00.agent-governance/scopes/common.md). |
| Markdown lint | Check Markdown rules | `markdownlint-cli2` in [pre-commit](../../../../.pre-commit-config.yaml) | `pre-commit` | lint | Blocks applicable hook/CI execution | [pre-commit](https://pre-commit.com/) supports configured hook execution | Keep claims tied to the hook ID, not all Markdown semantics. Owner: [pre-commit config](../../../../.pre-commit-config.yaml). |
| YAML lint | Check YAML style rules | `yamllint` with [`.yamllint`](../../../../.yamllint) | `pre-commit` | lint | Blocks applicable hook/CI execution | pre-commit supports file-filtered hooks | Relaxed rules do not prove workflow semantics. Owner: [pre-commit config](../../../../.pre-commit-config.yaml). |
| JSON syntax | Parse JSON files accepted by the configured hook | `check-json`; selective `python3 -m json.tool` in [post-tool validation](../../../../scripts/hooks/post-tool-validate.sh) | `pre-commit` | syntax | Blocks applicable hook/CI execution | pre-commit supports per-hook file selection | Post-tool parsing covers only three named JSON surfaces. Owner: [pre-commit config](../../../../.pre-commit-config.yaml). |
| TOML syntax | Parse TOML inputs | `check-toml` in [pre-commit](../../../../.pre-commit-config.yaml) | `pre-commit` | syntax | Blocks applicable hook/CI execution | pre-commit supports configured parser hooks | Syntax does not prove tool-specific semantics. Owner: [pre-commit config](../../../../.pre-commit-config.yaml). |
| Shell syntax | Parse tracked shell scripts and Claude hooks | `bash -n` in [local runner](../../../../scripts/validation/run-local-qa-gates.sh) | None directly | syntax | Blocks the script-backed or harness run | No fixed external source mandates this repository command | Keep separate from ShellCheck. Owner: [`run-local-qa-gates.sh`](../../../../scripts/validation/run-local-qa-gates.sh). |
| ShellCheck | Detect shell correctness and portability issues | `shellcheck` in [pre-commit](../../../../.pre-commit-config.yaml); conditional post-tool check | `pre-commit` | lint | Blocks applicable hook/CI execution | pre-commit supports multi-language hooks | `recommend-qa-gates.sh` is explicitly excluded. Owner: [pre-commit config](../../../../.pre-commit-config.yaml). |
| actionlint | Validate GitHub Actions syntax/expressions | `actionlint` in [pre-commit](../../../../.pre-commit-config.yaml) | `pre-commit` | syntax/lint | Blocks workflow-file hook/CI execution | [Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) defines keys, triggers, jobs, and steps | Local validation cannot prove a remote run. Owner: [pre-commit config](../../../../.pre-commit-config.yaml). |
| Hadolint | Lint Dockerfiles | `hadolint-docker` in [pre-commit](../../../../.pre-commit-config.yaml) | `pre-commit` | lint/security | Blocks applicable hook/CI execution | pre-commit supports file-filtered hooks | Applies only to matching Dockerfiles. Owner: [pre-commit config](../../../../.pre-commit-config.yaml). |
| Secret scanning | Detect committed secret patterns | `gitleaks` with [`.gitleaks.toml`](../../../../.gitleaks.toml) via pre-commit | `pre-commit` | security | Blocks applicable hook/CI execution | [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use) supports least privilege and secret/log caution | Scanner pass is not proof that no secret exists. Owner: [security scope](../../../00.agent-governance/scopes/security.md). |
| ESLint | Lint Storybook Next.js source | `npm run lint --prefix projects/storybook/nextjs`; `eslint-nextjs` hook | `frontend-quality`; skipped in CI `pre-commit` via `SKIP` | lint | Blocks local command or dedicated CI job | pre-commit supports selective skip; duplication policy is repo-local | Keep the dedicated CI job as the CI evidence. Owner: [`projects/storybook/nextjs/package.json`](../../../../projects/storybook/nextjs/package.json). |
| TypeScript | Type-check without emitting | `npm run typecheck --prefix projects/storybook/nextjs` | `frontend-quality` | type | Blocks local command or CI job | No fixed external source defines this project contract | Applies only to the Storybook Next.js project. Owner: [`package.json`](../../../../projects/storybook/nextjs/package.json). |
| Storybook tests | Execute the configured Vitest Storybook project | `npm run test --prefix projects/storybook/nextjs` | `storybook-coverage` runs the same project through the coverage script | test | Local command or CI coverage job exits non-zero | Fowler describes automated tests as delivery-pipeline feedback | A coverage run is the tracked CI route; no separate `test` job exists. Owner: [`package.json`](../../../../projects/storybook/nextjs/package.json). |
| Frontend builds | Build the Next.js app and static Storybook | `npm run build` and `npm run build-storybook` with project prefix | `frontend-quality` | build | Blocks local commands or CI job | [Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html) uses builds/tests as pipeline feedback | Build success is not deployment evidence. Owner: [`ci-quality.yml`](../../../../.github/workflows/ci-quality.yml). |
| Storybook coverage | Collect configured browser-test coverage | `npm run coverage --prefix projects/storybook/nextjs` | `storybook-coverage` | coverage/test | Blocks local command or CI job | DORA metrics do not define code-coverage thresholds | Docs-only Task 4 coverage is N/A. Owner: [QA scope](../../../00.agent-governance/scopes/qa.md). |
| Compose validation | Render root and governed profile configurations | [`validate-docker-compose.sh`](../../../../scripts/validation/validate-docker-compose.sh) | `compose-validation`, `compose-all-profiles-validation` | syntax/configuration | Blocks local runner or either CI job | No fixed source substitutes for Docker-specific validation | Keep core/all-profile evidence distinct. Owner: [`validate-docker-compose.sh`](../../../../scripts/validation/validate-docker-compose.sh). |
| Hardening and baselines | Check tier hardening, template/security, and QuickWin controls | [`check-all-hardening.sh`](../../../../scripts/hardening/check-all-hardening.sh), [`check-template-security-baseline.sh`](../../../../scripts/validation/check-template-security-baseline.sh), [`check-quickwin-baseline.sh`](../../../../scripts/validation/check-quickwin-baseline.sh) | `infrastructure-hardening`, `template-security-baseline`, `quickwin-baseline` | security | Blocks local runner or corresponding CI job | GitHub secure-use guidance is workflow-specific, not an infra-control mapping | Preserve three separately named results. Owner: [security scope](../../../00.agent-governance/scopes/security.md). |
| Docs traceability | Check execution/operations links | [`check-doc-traceability.sh`](../../../../scripts/validation/check-doc-traceability.sh) | `docs-traceability` | traceability | Blocks local runner or CI job | No external source defines the repository taxonomy | Owner: [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md). |
| Docs implementation alignment | Compare active docs with tracked implementation surfaces | [`check-doc-implementation-alignment.sh`](../../../../scripts/validation/check-doc-implementation-alignment.sh) | `docs-implementation-alignment` | traceability | Blocks local runner or CI job | External sources do not prove repo-local current truth | Owner: [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md). |
| Repository contracts | Validate taxonomy, templates, workflow/job coupling, generated references, and implementation drift | [`check-repo-contracts.sh`](../../../../scripts/validation/check-repo-contracts.sh) | `repo-contracts` | contract/security | Blocks local runner or CI job | GitHub syntax supports job structure, not repository-specific contracts | Owner: [`check-repo-contracts.sh`](../../../../scripts/validation/check-repo-contracts.sh). |
| Agent-output eval fixtures | Validate the tracked fixture catalog | [`run-agent-output-eval-fixtures.sh --check-fixtures`](../../../../scripts/validation/run-agent-output-eval-fixtures.sh) | `agent-output-eval-fixture-gate` | test/eval | CI-blocking; local command is available but not one of the 12 runner steps | No fixed external source defines fixture semantics | This checks fixture integrity, not live model quality. Owner: [eval fixture runner](../../../../scripts/validation/run-agent-output-eval-fixtures.sh). |
| Dependency vulnerability audit | Fail on high-severity Storybook Next.js dependency findings | `npm audit --audit-level=high --prefix projects/storybook/nextjs` | `dependency-vulnerability-audit` | security | Dedicated CI job blocks on threshold | GitHub secure-use is complementary, not npm policy | Scope is one project/package lock. Owner: [`ci-quality.yml`](../../../../.github/workflows/ci-quality.yml). |
| Provider drift | Compare generated Codex/Gemini projections with canonical sources | [`sync-provider-surfaces.sh`](../../../../scripts/operations/sync-provider-surfaces.sh) verify mode | `repo-contracts` supplies broader catalog parity, not the exact command | drift | Blocks the local runner on detected drift | No fixed external source defines provider projection policy | Verification does not prove provider runtime acceptance. Owner: [provider adapter model](../../../00.agent-governance/providers/agents-md.md). |
| Generated-data freshness | Check Wiki index and generated contract snapshots | [`generate-llm-wiki-index.sh --check`](../../../../scripts/knowledge/generate-llm-wiki-index.sh); generators checked inside repo contracts | `repo-contracts` | freshness | Blocks local runner/repo-contracts when stale | External sources do not define generated artifact ownership | Never hand-edit generated data; run its canonical generator. Owner: [QA scope](../../../00.agent-governance/scopes/qa.md). |
| Workflow security scan | Analyze Actions and upload SARIF | No equivalent local runner step | `zizmor` | security | GitHub job blocks when run; SARIF upload needs remote permissions | GitHub secure use supports SHA pinning, least privilege, and injection caution | Correct job ID is `zizmor`, not the obsolete variant. Owner: [GitHub governance](../../../00.agent-governance/rules/github-governance.md). |
| Remote branch protection | Require remote checks/reviews before merge | No local command can prove enforcement | Remote GitHub settings | remote enforcement | Unknown for 2026-07-11; no current remote query was performed | Actions syntax says required skipped checks can remain pending, but does not prove configuration | Treat as remote-only/unknown until directly reverified. Owner: [GitHub governance](../../../00.agent-governance/rules/github-governance.md). |

## Workspace Comparison and Ownership

| Category | Current state | Primary comparison | Status | Gap | Recommendation | Canonical owner | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QA and evidence classes | Tracked gates distinguish format, lint, syntax, type, test, build, coverage, security, traceability, eval, and freshness evidence. | pre-commit supports hook orchestration; GitHub Actions supports jobs/steps. | Implemented | Applicability still varies by changed surface. | Record named commands/jobs and N/A rationale rather than “all QA.” | `docs/00.agent-governance/scopes/qa.md` | Matrix above; tracked runner/workflow/config | High |
| CI/CD feedback | Six workflows define 21 jobs; `ci-quality.yml` defines 15 quality jobs. | GitHub syntax defines automation; Fowler describes releasable pipeline feedback; DORA defines five delivery metrics. | Partially Implemented | Tracked CI does not prove deployment readiness, DORA measurement, or remote required checks. | Keep CI evidence and operational-delivery claims separate. | `docs/00.agent-governance/rules/github-governance.md` | `.github/workflows/*.yml` | High |
| Formatting | EditorConfig and Prettier configuration exist; pre-commit/post-tool supply other formatting checks. | EditorConfig specifies hierarchical style settings; Prettier documents parsing/reprinting and a CI check mode. | Partially Implemented | No tracked shared automation invokes Prettier. | Do not imply Prettier enforcement unless the active owner approves and implements it. | `docs/00.agent-governance/scopes/common.md` | `.editorconfig`, `.prettierrc.json`, `.prettierignore`, post-tool hook | High |

## Analysis

The tracked layers intentionally differ. The default/script-backed/all-profile
runner modes provide a 12-step subset, the harness mode provides 8 steps, and
list mode provides advisory inventory without execution. Pre-commit adds 23
file/stage-filtered hook IDs; CI adds heavy frontend, coverage, dependency, and
SARIF behavior. None of those layers proves current branch-protection
enforcement. DORA's current five
metrics—change lead time, deployment frequency, failed deployment recovery
time, change fail rate, and deployment rework rate—require production delivery
data this repository task did not collect.

## Application Notes for This Workspace

- Cite the exact script, hook ID, or workflow job for every QA claim.
- Record `zizmor` as GitHub-only SARIF evidence.
- Record the local runner by mode: 12 gates for default, `--script-backed`, and
  `--all-profiles`; 8 for `--harness`; and 0 for `--list`, whose one recommender
  entry remains advisory and non-executed.
- Do not claim that post-tool validation runs Prettier.
- Keep remote required-check and branch-protection state unknown unless a
  current direct query is recorded.

## Potential Follow-up / Gap

- Any proposal to enforce Prettier belongs first to the Common scope and an
  approved Stage 03/04 change, not this reference.
- Current branch protection and required-check contexts need a separately
  approved/read-only remote verification before an enforcement claim.
- Operating DORA metrics requires application/service deployment and incident
  data sources; CI job presence alone is insufficient.

## Source Rules

- External sources were retrieved on **2026-07-11** and support comparison only.
- Mutable official pages prove retrieval-time guidance, not historical behavior
  or workspace enforcement.
- Repo-local claims cite tracked sources at baseline `505277817e`; Graphify is
  advisory because its report is older.
- No external source in this reference is adopted workspace policy.

## Sources

- [Task 4 source ledger](../../../04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md) - retrieval date, supported claim, evidence-surface class, and caveat for every fixed source
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) - workflow/job/step and trigger syntax
- [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use) - least privilege, untrusted input, secret, and immutable-action guidance
- [pre-commit](https://pre-commit.com/) - hook configuration, local execution, CI use, and skips
- [EditorConfig](https://editorconfig.org/) - cross-editor consistency
- [EditorConfig specification](https://spec.editorconfig.org/) - hierarchical file processing and supported pairs
- [Prettier overview](https://prettier.io/docs) - formatter behavior and supported inputs
- [Prettier CLI](https://prettier.io/docs/cli) - check-mode and exit-code behavior
- [DORA metrics](https://dora.dev/guides/dora-metrics/) - current five-metric throughput/instability model
- [Martin Fowler: Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html) - releasability and automated pipeline feedback
- [CI workflow](../../../../.github/workflows/ci-quality.yml) - 15 tracked quality job IDs
- [Local QA runner](../../../../scripts/validation/run-local-qa-gates.sh) - 12 executed local gates and responsibility split
- [pre-commit config](../../../../.pre-commit-config.yaml) - 23 tracked hook IDs
- [Scripts README](../../../../scripts/README.md) - script lifecycle and authority

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when workflows, gate scripts/configuration, remote evidence, or fixed primary sources change
- **Update Trigger**: Recount from tracked definitions; never copy prior totals without revalidation

## Related Documents

- [research pack index](./README.md)
- [automation, pipeline, and workflow loops](./automation-pipeline-workflow.md)
- [workspace baseline](./workspace-baseline.md)
- [QA scope](../../../00.agent-governance/scopes/qa.md)
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md)
