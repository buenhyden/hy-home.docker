---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md -->

# Automation Coverage Map

## Overview

This report maps the current CI/CD, QA, validation, formatting, security, and
automation coverage for the workspace document contract audit pack. It records
measured workflow and script coverage without changing workflow configuration,
validators, CI permissions, runtime infrastructure, provider adapters, or target
corpus documents.

## Evidence Snapshot Boundary

- **Evidence as of**: 2026-07-03
- **Current implementation route**: [canonical agentic implementation audit](../2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Citation rule**: Preserve the counts, findings, commands, and dispositions below as dated evidence. Do not cite them as the current workspace state without current tracked-source revalidation.

## Purpose

This reference preserves Task 4 automation evidence for the final
document-contract gap register. It helps later remediation work decide which
gaps need direct fixes, future batches, historical evidence, explicit
out-of-scope handling, or no action.

## Repository Role

This report supports Stage 04 execution evidence and future automation
planning. It is not active CI policy, not a branch protection source of truth,
not a validator specification, and not a replacement for `.github/workflows/`,
`scripts/`, `.pre-commit-config.yaml`, or `docs/00.agent-governance/`.

## Scope

### In Scope

- Tracked GitHub workflow files.
- Workflow trigger scopes, permissions, action pinning, and credential
  handling.
- Repo-local validation and QA scripts.
- Formatting hooks.
- Security and supply-chain signals.
- Current Task 4 validation results.

### Out of Scope

- Editing workflows or validators.
- Changing branch protection.
- Reading or printing secret values.
- Changing provider adapters.
- Normalizing target documents.
- Resolving existing infra image/version drift.
- Making remote GitHub changes.

## Method

| Evidence ID | Command or Read | Result Summary | Use |
| --- | --- | --- | --- |
| AUTO-001 | `git ls-files '.github/workflows/*.yml' '.github/workflows/*.yaml'` | 6 tracked workflow files. | Measured workflow baseline. |
| AUTO-002 | `rg -n '^(name:\|on:\|permissions:\|jobs:)\|uses:\|pull-requests:\|contents:\|id-token:\|persist-credentials\|actions/checkout\|secrets\.' .github/workflows` | Confirmed workflow names, trigger blocks, permissions, pinned actions, checkout credential handling, and built-in `GITHUB_TOKEN` use. | Workflow coverage and credential handling. |
| AUTO-003 | `git ls-files 'scripts/**/*.sh' 'scripts/*.sh' \| rg '(validation\|operations\|knowledge\|quality\|test\|lint\|format\|security\|audit)'` | 15 matching validation, operations, knowledge, QA, and security script paths. | Script inventory baseline. |
| AUTO-004 | `rg -n 'check-\|validate\|lint\|format\|test\|audit\|security\|provider\|llm-wiki\|hardening\|traceability\|alignment' scripts README.md AGENTS.md docs/00.agent-governance docs/04.execution/plans/README.md` | Large governance and script-reference scan; report records aggregated findings only. | Local QA, formatting, and policy coverage. |
| AUTO-005 | Targeted reads of workflows, `scripts/README.md`, `.pre-commit-config.yaml`, `.github/rulesets/main-protection.md`, `.github/dependabot.yml`, `.gitleaks.toml`, and listed validation, operations, hardening, hook, and knowledge scripts. | Confirmed command modes, CI wiring, local-only wrappers, manual secret-safe modes, and advisory scripts. | Coverage classifications. |
| AUTO-006 | Task 4 validation entrypoints before report creation. | All required checks passed except full repo contract, which failed only on known out-of-scope infra drift. | Current behavior evidence. |

## Definitions / Facts

- **Workflow baseline**: 6 tracked GitHub workflow files:
  `ci-quality.yml`, `generate-changelog.yml`, `greetings.yml`,
  `pr-labeler.yml`, `stale.yml`, and `tech-stack-version-sync.yml`.
- **Coverage status vocabulary**:
  - `enforced`: an automatic workflow, CI job, pre-commit hook, or validator
    blocks/fails or applies its automation in the declared trigger scope.
  - `report-only`: a command produces advisory evidence without blocking.
  - `local-only`: a command is available in repo-local tooling but is not a
    direct GitHub workflow job.
  - `manual`: an operator or agent must intentionally run the command.
  - `unguarded`: a rule exists but no current automated guard was found.
- **Approved dispositions**: `direct-fix`, `batch-fix`,
  `historical-evidence`, `out-of-scope-gap`, and `no-action`.
- **Action pinning fact**: Task 4 found all external workflow `uses:` entries
  pinned to full commit SHAs. Local actions were not used.
- **Credential handling fact**: checkout-based workflows set
  `persist-credentials: false`; workflows that use tokens use only the built-in
  `${{ secrets.GITHUB_TOKEN }}` and do not print secret values.
- **Permission fact**: workflows define top-level `permissions` explicitly.
  No workflow uses `pull_request_target`, `id-token`, or `contents: write`.
- **Current validation fact**: full `check-repo-contracts.sh` exits nonzero
  with `failures=2` only because of known infra drift: Keycloak hardening image
  mismatch and `infra/tech-stack.versions.json` expected-image drift.

## CI/CD Workflow Coverage

| Path or Command | Owner Surface | Current Status | Evidence | Proposed Next Action |
| --- | --- | --- | --- | --- |
| `.github/workflows/ci-quality.yml` | GitHub Actions QA gate | enforced | Triggers on `push` to `main`, `pull_request` to `main`, and `workflow_dispatch`; top-level `contents: read`; 13 QA jobs; checkout uses a full SHA and `persist-credentials: false`; `zizmor` uses `security-events: write`, `actions: read`, `contents: read`, and built-in `GITHUB_TOKEN` for SARIF upload. | Keep as canonical CI quality workflow; update `.github/rulesets/main-protection.md`, `github-governance.md`, and `check-repo-contracts.sh` together when job IDs change. |
| `.github/workflows/generate-changelog.yml` | Release tag check | enforced | Triggers on `push` tags matching `v*.*.*`; top-level `contents: read`; checkout is SHA-pinned and uses `persist-credentials: false`; verifies `CHANGELOG.md` contains the release tag. | Keep tag-time release guard; no Task 4 workflow edit. |
| `.github/workflows/tech-stack-version-sync.yml` | Infra version drift gate | enforced | Triggers on PR changes to root/infra Compose files or `infra/tech-stack.versions.json`; top-level and job-level `contents: read`; checkout is SHA-pinned with `persist-credentials: false`; runs `bash scripts/operations/sync-tech-stack-versions.sh --check`. | Keep read-only PR gate; resolve current registry drift only in a separate infra drift task. |
| `.github/workflows/greetings.yml` | GitHub community automation | enforced | Triggers on opened issues and PRs; top-level `permissions: {}`; job permissions are `issues: write` and `contents: read`; `actions/first-interaction` is SHA-pinned and uses built-in `GITHUB_TOKEN`; no checkout. | Keep classified as triage automation, not a QA gate. |
| `.github/workflows/pr-labeler.yml` | GitHub PR triage automation | enforced | Triggers on opened, synchronized, and reopened PRs to `main`; top-level `permissions: {}`; job permissions are `contents: read` and `pull-requests: write`; `actions/labeler` is SHA-pinned and uses built-in `GITHUB_TOKEN`; no checkout. | Keep label automation separate from required QA checks. |
| `.github/workflows/stale.yml` | GitHub stale-thread automation | enforced | Runs on daily schedule; top-level `permissions: {}`; job permissions are `issues: write`, `pull-requests: write`, and `contents: read`; `actions/stale` is SHA-pinned; no checkout or secret values. | Keep as scheduled triage automation; periodically review stale windows and messages. |
| `.github/rulesets/main-protection.md` | Local branch protection evidence | manual | Local proposal lists CI Quality Gates job names as required status checks. Current Remote State was last verified on 2026-05-28 and says `docs-implementation-alignment` still required remote re-verification before claiming remote enforcement. | Re-verify remote branch protection only in a future approved GitHub governance pass. |

## QA And Validation Coverage

| Path or Command | Owner Surface | Current Status | Evidence | Proposed Next Action |
| --- | --- | --- | --- | --- |
| `bash scripts/validation/check-doc-traceability.sh` | Stage 04 to Stage 05 traceability | enforced | CI job `docs-traceability`; pre-push hook; Task 4 run passed with `catalog_pairs_total=46`, `failures=0`. | Keep as required docs traceability gate. |
| `bash scripts/validation/check-doc-implementation-alignment.sh` | Active docs to implementation alignment | enforced | CI job `docs-implementation-alignment`; Task 4 run passed with `stage_docs_total=546`, `repo_local_markdown_links_checked=4107`, `failures=0`. | Keep workflow job; re-verify remote branch protection separately before asserting it is a required remote check. |
| `bash scripts/validation/check-repo-contracts.sh` | Repository contract gate | enforced | CI job `repo-contracts`, pre-push hook, and repo-local task verification. Task 4 full run reached all sections and failed only on known out-of-scope infra drift with `failures=2`. | Keep hard gate; do not resolve infra drift in Task 4. |
| `bash -n scripts/validation/check-repo-contracts.sh` | Shell syntax sanity check | local-only | Task 4 syntax check passed. `run-local-qa-gates.sh` also runs `bash -n` for `scripts/**/*.sh` and `.claude/hooks/*.sh`. | Keep as lightweight local verification before running full gates. |
| `bash scripts/validation/validate-docker-compose.sh` | Compose structural validation | enforced | CI jobs `compose-validation` and `compose-all-profiles-validation`; pre-push hook; default mode may create temporary `.env` and dummy secret files then remove files it created; `--preflight` is a real local prerequisite check. | Keep CI default and all-profile coverage; use `--preflight` for operator readiness checks. |
| `bash scripts/hardening/check-all-hardening.sh` | Infrastructure hardening baseline | enforced | CI job `infrastructure-hardening`; repo contracts call it as a hard gate; current failure is Keycloak image tag drift already classified out of scope. | Keep gate; fix current image expectations in a separate infra drift batch. |
| `bash scripts/validation/check-template-security-baseline.sh` | Compose template and security baseline | enforced | CI job `template-security-baseline`; pre-push hook; checks common optimization template adoption, `no-new-privileges`, and `cap_drop: ALL` with approved exceptions. | Keep gate; update exception registry only with explicit evidence. |
| `bash scripts/validation/check-quickwin-baseline.sh` | QuickWin compose baseline | enforced | CI job `quickwin-baseline`; pre-push hook; checks restart, healthcheck, no-new-privileges, CPU, memory, and secrets baselines. | Keep gate; preserve exception-driven handling. |
| `bash scripts/validation/check-storybook-contract.sh` | Storybook quality contract | enforced | Called by `check-repo-contracts.sh`; validates package scripts, CI workflow literals, and 90 percent Vitest coverage thresholds. | Keep as contract coverage for Storybook CI wiring. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | LLM Wiki freshness | enforced | Repo contracts invoke the check; Task 4 run passed before creating this report; generator excludes secret content, dependency trees, generated/minified artifacts, and `graphify-out/`. | Regenerate after adding this report, then rerun freshness check. |
| `bash scripts/operations/sync-provider-surfaces.sh --check` | Provider adapter drift | local-only | Verify mode is default unless `--write` is used; Task 4 run reported `sync-provider-surfaces: no drift`. Repo contracts also validate runtime catalog parity. | Keep as explicit local verification; do not write provider surfaces in this audit task. |
| `bash scripts/operations/sync-tech-stack-versions.sh --check` | Tech-stack registry drift | enforced | Read-only workflow `tech-stack-version-sync.yml` runs this check on matching PRs; `run-local-qa-gates.sh` lists it as a local script-backed gate; current full repo contract reports known registry drift. | Keep read-only guard; resolve drift out of scope. |
| `bash scripts/validation/run-local-qa-gates.sh --list` | Local QA/CI orchestration | local-only | Lists local script-backed gates, CI/local-tooling gates, and remote-only responsibilities; Task 4 read confirmed it does not run remote-only SARIF, branch protection, CODEOWNERS, or merge readiness. | Use for local planning; avoid duplicating GitHub-only jobs locally. |
| `bash scripts/validation/validate-harness.sh` | Harness-change scoped wrapper | local-only | Delegates to `run-local-qa-gates.sh --harness`; repo contracts enforce the wrapper exists and is referenced. | Keep wrapper thin; use for harness/governance changes. |
| `bash scripts/operations/gen-secrets.sh --check` and `--dry-run` | Secret generation safety checks | manual | `--check` verifies tools and layout without reading or writing secret values; `--dry-run` reports planned actions by ID/path only; no-argument mode may read/write local secret registry and secret files. | Keep safe modes manual and metadata-only; do not run no-argument mode during audits. |
| `bash scripts/knowledge/report-graphify-health.sh` | Graphify advisory health | report-only | Reads only `graphify-out/manifest.json`, `graphify-out/graph.json`, and `graphify-out/GRAPH_REPORT.md`; exits 0 even on advisory reasons. | Treat Graphify as advisory unless a future task adds a hard freshness gate. |
| `source scripts/operations/use-qa-ci-tools.sh` or `./scripts/operations/use-qa-ci-tools.sh` | Local QA/CI tool path helper | manual | Adds user-global tool paths when sourced; executable mode reports missing tools for git, bash, Python, Docker, jq, Node, pre-commit, zizmor, yamllint, markdownlint, shellcheck, shfmt, actionlint, hadolint, gitleaks, check-jsonschema, and commitizen. | Use when restricted shells cannot see installed QA tools. |

## Formatting Coverage

| Path or Command | Owner Surface | Current Status | Evidence | Proposed Next Action |
| --- | --- | --- | --- | --- |
| `.pre-commit-config.yaml` | Pre-commit formatting and lint hooks | enforced | Configured hook types are `pre-commit`, `pre-push`, and `commit-msg`; CI `pre-commit` job runs `pre-commit/action` with `SKIP=eslint-nextjs`; `frontend-quality` runs the skipped ESLint workload separately. | Keep CI duplication control; update hook pins through Dependabot review. |
| `pre-commit/pre-commit-hooks` entries | Basic file formatting and hygiene | enforced | Enforces large-file limit, case conflict, merge conflict, symlink, TOML, EOF, JSON, line ending, and trailing whitespace hooks. | Keep as first formatting layer. |
| `yamllint`, `markdownlint-cli2`, `shellcheck`, `actionlint`, `hadolint` hooks | YAML, Markdown, shell, GitHub Actions, and Dockerfile linting | enforced | `.pre-commit-config.yaml` pins each hook repository and limits file scopes. | Keep format/lint hooks pinned and update by PR. |
| `gitleaks` hook with `.gitleaks.toml` | Secret scanning | enforced | Pre-commit hook uses upstream defaults via `.gitleaks.toml`; no repo-specific broad allowlist. | Keep minimal allowlisting; never document secret values. |
| `commitizen` hook | Commit message format | enforced | Commit-msg hook pins `commitizen` and enforces Conventional Commit format with message length limit. | Keep for local commit hygiene. |
| `git diff --check` | Diff whitespace hygiene | local-only | Task 4 run passed; `run-local-qa-gates.sh` runs it as the first local gate; `post-tool-validate.sh` runs it for changed files. | Continue running before commits. |
| `bash -n` over shell scripts | Shell syntax formatting-adjacent check | local-only | Task 4 ran `bash -n scripts/validation/check-repo-contracts.sh`; local QA runner expands to `scripts/**/*.sh` and `.claude/hooks/*.sh`. | Use for changed shell scripts before heavier checks. |
| `scripts/hooks/post-tool-validate.sh --check` | Provider-neutral post-edit validation | local-only | Check-only mode disables whitespace writes and `shfmt -w`; normal mode can trim whitespace and run path-aware validation after file edits. | Use check-only mode for audit-only verification; keep hook behavior path-scoped. |

## Security And Supply-Chain Signals

| Path or Command | Owner Surface | Current Status | Evidence | Proposed Next Action |
| --- | --- | --- | --- | --- |
| Workflow permission contract in `check-repo-contracts.sh` | GitHub Actions security | enforced | Rejects missing top-level permissions, `pull_request_target`, `contents: write`, direct pushes to main, unpinned external actions, missing/extra CI jobs, and ruleset mismatch. | Keep as workflow security hard gate. |
| `.github/workflows/ci-quality.yml` `zizmor` job | GitHub Actions security scan | enforced | Runs `uvx zizmor . --format sarif . > results.sarif` and uploads SARIF through `github/codeql-action/upload-sarif` pinned by SHA. | Keep GitHub-only SARIF upload; do not duplicate locally unless needed for debugging. |
| `.github/dependabot.yml` | Dependency update automation | enforced | Weekly grouped updates cover GitHub Actions, Dockerfiles, Docker Compose images, and Storybook Next.js npm dependencies. | Keep grouped dependency PRs; review action SHA updates carefully. |
| `.pre-commit-config.yaml` `check-dependabot` | Dependabot config schema | enforced | `check-jsonschema` validates `.github/dependabot.yml` as a pre-commit hook. | Keep schema validation. |
| `.pre-commit-config.yaml` `gitleaks` | Secret leakage guard | enforced | Runs gitleaks with upstream default rules through `.gitleaks.toml`. | Keep as pre-commit secret scan; avoid adding broad allowlists. |
| `scripts/validation/check-template-security-baseline.sh` | Compose security baseline | enforced | Checks `no-new-privileges` and `cap_drop: ALL` across resolved services with exception registry. | Keep in CI and pre-push. |
| `scripts/validation/check-quickwin-baseline.sh` | QuickWin security/operability baseline | enforced | Checks service restart, healthcheck, no-new-privileges, CPU, memory, and secrets controls. | Keep in CI and pre-push. |
| `scripts/validation/check-repo-contracts.sh` floating image tag policy | Container supply-chain policy | enforced | Requires pinned image tags or explicit exceptions in `infra/image-tag-policy.exceptions.json`. | Keep gate; update exceptions only with owner evidence. |
| `scripts/operations/sync-tech-stack-versions.sh --check` | Curated image registry sync | enforced | CI drift workflow and repo contracts fail when curated expected images differ from Compose declarations. | Keep read-only guard; current drift remains out of scope. |
| `npm audit` / `pip audit` | Dependency vulnerability audit | unguarded | Task 4 scans found historical `npm audit` evidence in progress notes but no active workflow or script-backed gate for `npm audit` or `pip audit`. | Decide in a future security/QA batch whether to add explicit audit gates or document why Dependabot plus existing scans are sufficient. |

## Unguarded Rules

| Path or Command | Owner Surface | Current Status | Evidence | Proposed Next Action |
| --- | --- | --- | --- | --- |
| Remote branch protection re-verification | GitHub governance | unguarded | `.github/rulesets/main-protection.md` current remote state was last verified on 2026-05-28; Task 4 did not perform remote `gh api` checks by design. | Re-verify only in a future approved remote GitHub governance task. |
| `docs-implementation-alignment` remote required-check assertion | GitHub governance | unguarded | Local ruleset proposal lists the check, but the current remote-state note says agents must re-verify before asserting remote enforcement of the new context. | Track as remote-evidence follow-up, not a local workflow edit. |
| `npm audit` / `pip audit` before committing | Security / QA guidance | unguarded | Governance says audits should run before committing, but active CI/local gate inventory does not include npm or pip audit commands. | Add a future decision item for explicit dependency-audit gating. |
| `graphify update .` after code-file changes | Agent bootstrap governance | unguarded | Root `AGENTS.md` requires Graphify refresh when available; no CI freshness gate exists, and `report-graphify-health.sh` is advisory/report-only. | Consider a future Graphify availability/freshness gate only after the CLI is stable in the workspace. |
| Provider surface sync as a separate CI job | Provider adapter governance | unguarded | `sync-provider-surfaces.sh` is local-only in Task 4 and local QA, while repo contracts independently check runtime catalog parity. | No separate CI job needed unless provider drift recurs. |

## Gaps For Register

| Gap ID | Gap Candidate | Evidence | Disposition | Register Handling |
| --- | --- | --- | --- | --- |
| AUTO-GAP-001 | Full repo contract currently fails on known infra hardening drift. | `bash scripts/validation/check-repo-contracts.sh` reports `failures=2`; hardening hard gate fails on Keycloak image tag mismatch. | out-of-scope-gap | Carry forward as existing infra drift; do not patch in document-contract audit tasks. |
| AUTO-GAP-002 | Curated tech-stack image registry is out of sync with Compose declarations. | Full repo contract reports expected-image drift for Traefik, Keycloak, Vault, PostgreSQL, Kafka, Grafana, Alloy, n8n, Ollama, Open WebUI, and RedisInsight. | out-of-scope-gap | Carry forward to an infra version drift remediation task. |
| AUTO-GAP-003 | Remote branch protection evidence is historical and was not reverified in Task 4. | `.github/rulesets/main-protection.md` was last verified on 2026-05-28 and calls out `docs-implementation-alignment` re-verification. | out-of-scope-gap | Add to a future remote GitHub governance audit if owner approval is granted. |
| AUTO-GAP-004 | Explicit dependency vulnerability audit commands are not active CI/local gates. | No active `npm audit` or `pip audit` gate found in workflows or script-backed QA inventory. | batch-fix | Decide in a future security/QA batch whether to add audit jobs or document current Dependabot-based coverage. |
| AUTO-GAP-005 | Graphify refresh is instruction-based and report-only, not enforced. | `AGENTS.md` requires `graphify update .` when available; `report-graphify-health.sh` is advisory and exits 0. | batch-fix | Decide later whether Graphify should remain advisory or become a hard freshness check. |
| AUTO-GAP-006 | Provider sync direct command is local-only but covered indirectly by repo contracts. | `sync-provider-surfaces.sh --check` passed; `check-repo-contracts.sh` validates runtime catalog and provider parity. | no-action | Keep current coverage unless provider drift recurs. |
| AUTO-GAP-007 | Secret generation remains manual by design. | `gen-secrets.sh --check` and `--dry-run` avoid reading/writing values; no-argument mode may read/write secret registry and files. | no-action | Preserve manual redaction boundary; never run value-reading mode for audits. |

## Source Rules

- Prefer tracked workflow files, script files, and repo-local validators over
  historical notes when classifying current automation coverage.
- Summarize command output and validation results; do not paste raw logs or
  secret-bearing content.
- Re-run current checks before using this report for CI/CD, QA, security, or
  branch-protection decisions.
- Treat remote GitHub state as current only when freshly verified through an
  approved read-only audit.

## Sources

- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - Main QA, formatting, frontend, coverage, and workflow-security jobs.
- [Release changelog workflow](../../../../.github/workflows/generate-changelog.yml) - Tag-time changelog gate.
- [Greeting workflow](../../../../.github/workflows/greetings.yml) - First interaction automation.
- [Pull request labeler workflow](../../../../.github/workflows/pr-labeler.yml) - PR triage automation.
- [Stale workflow](../../../../.github/workflows/stale.yml) - Scheduled stale issue and PR automation.
- [Tech-stack version sync workflow](../../../../.github/workflows/tech-stack-version-sync.yml) - Read-only image registry drift gate.
- [Main protection proposal](../../../../.github/rulesets/main-protection.md) - Local branch protection evidence and required-check proposal.
- [Dependabot configuration](../../../../.github/dependabot.yml) - Dependency update automation.
- [Pre-commit configuration](../../../../.pre-commit-config.yaml) - Formatting, linting, secret scanning, and local project hooks.
- [Gitleaks configuration](../../../../.gitleaks.toml) - Secret-scanning defaults.
- [Scripts README](../../../../scripts/README.md) - Canonical script inventory and lifecycle rules.
- [Repository contract validator](../../../../scripts/validation/check-repo-contracts.sh) - Repository, workflow, script, LLM Wiki, provider, and infra contract gate.
- [Local QA gate runner](../../../../scripts/validation/run-local-qa-gates.sh) - Local/CI/remote responsibility split.
- [LLM Wiki index generator](../../../../scripts/knowledge/generate-llm-wiki-index.sh) - Generated index write/check behavior.
- [Provider surface sync](../../../../scripts/operations/sync-provider-surfaces.sh) - Provider adapter verify/write behavior.
- [Tech-stack version sync](../../../../scripts/operations/sync-tech-stack-versions.sh) - Curated registry sync and check behavior.
- [Secret generation utility](../../../../scripts/operations/gen-secrets.sh) - Manual secret-safe modes and value-reading boundary.

## Maintenance

- **Owner**: Documentation Specialist / `doc-writer`, with QA Engineer and
  Security Auditor review when automation contracts change.
- **Review Cadence**: Review when workflows, required checks, repo validators,
  pre-commit hooks, provider sync, LLM Wiki generation, or script inventory
  changes.
- **Update Trigger**: Update when Task 5 gap register supersedes these gaps,
  when a CI job is added/removed, when workflow permissions change, or when a
  local-only/manual gate becomes enforced.

## Related Documents

- [Document contract audit references](./README.md)
- [Contract governance map](./contract-governance-map.md)
- [Template application gaps](./template-application-gaps.md)
- [Frontmatter inventory](./frontmatter-inventory.md)
- [Section profile inventory](./section-profile-inventory.md)
- [README profile inventory](./readme-profile-inventory.md)
- [Workspace document contract audit pack task](../../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md)
