---
title: Utilities and Automation Scripts
version: 1.0.0
type: common/repository-readme
status: active
owner: "@buenhyden"
created: '2026-02-21'
updated: '2026-09-01'
---

# Utilities & Automation Scripts (`scripts/`)

> Repository maintenance, utility scripts, and automation triggers.

## Overview

**KR**: 빌드, 테스트, 환경 구성 등에 필요한 보조 스크립트와 자동화 툴을 포함하는 디렉토리입니다.
**EN**: Directory containing helper scripts and automation tools for build, test, and environment setup.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Repository validation, implementation-alignment checks, contract checks, local QA gate orchestration, and agent event hook automation scripts.
- Repo-local LLM Wiki index generation and freshness checks.
- Tier hardening checks and their shared helper library.
- Local preflight validation mode and safe secret file generation utility.
- Script inventory and lifecycle ownership rules for canonical purpose-folder paths.

### Out of Scope

- Plaintext secret values, credentials, tokens, private keys, and generated certificate contents.
- Long-form operating procedures that belong in `docs/05.operations/`.
- Generated Graphify output under `graphify-out/`.
- Service-specific Docker Compose source files under `infra/`.

## Structure

```text
scripts/
├── validation/          # Compose, repo, docs, template, quickwin, and preflight checks
├── hardening/           # Unified hardening check with tier arguments
├── hooks/               # Provider-neutral hook dispatcher and post-tool validation
├── knowledge/           # LLM Wiki and Graphify advisory utilities
├── operations/          # Local operations, delivery rehearsal, and generated evidence owners
├── security/            # Local supply-chain verification and generated summary ownership
├── requirements.txt     # Python modules required by repository validation scripts
├── requirements-pre-commit.txt # Exact CI-only pre-commit tool pin
├── lib/<domain>/        # Importable domain modules; never a public entrypoint
├── lib/hardening-lib.sh # Shared implementation for tier hardening checks
└── README.md            # This file
```

## Purpose Folder Implementation

The canonical script surface is the purpose-folder path. Root-level
`scripts/*.sh` duplicates were removed after docs, CI, hooks, and pre-commit
references moved to purpose-folder paths. Do not recreate root duplicate
wrappers unless a future approved compatibility plan explicitly requires them.

`scripts/lib/<domain>/` owns importable domain behavior and defines no public
entrypoint. Purpose folders such as `scripts/validation/`, `scripts/security/`,
and `scripts/operations/` own entrypoints and delegate domain logic to the
library layer. `tests/lib/<domain>/` mirrors library responsibilities, while
`tests/validation/` retains CLI, entrypoint, and execution-context tests.

The hardening surface is intentionally consolidated into
`scripts/hardening/check-all-hardening.sh`. Tier-specific wrapper entrypoints
were removed by the 2026-05-17 cleanup; use tier arguments instead.

| Purpose    | Canonical paths                                                                                                                                                                                                                                                                                                                                                                                                    |
| :--------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Validation | `scripts/validation/run-ci-gate.py`, `scripts/validation/run-local-qa-gates.sh`, `scripts/lib/gate/ci_gate_contract.py`, `scripts/validation/ci_gate_runner.py`, `scripts/lib/gate/ci_gate_adapters.py`, and the focused validators registered in `scripts/manifest.yaml` |
| Hardening  | `scripts/hardening/check-all-hardening.sh`                                                                                                                                                                                                                                                                                                                                                                         |
| Hooks      | `scripts/hooks/agent-event-hook.sh`, `scripts/hooks/post-tool-validate.sh`                                                                                                                                                                                                                                                                                          |
| Knowledge  | `scripts/knowledge/generate-llm-wiki.py`, `scripts/knowledge/report-graphify-health.sh`                                                                                                                                                                                                                                                                                                      |
| Operations | `scripts/operations/gen-secrets.sh`, `scripts/operations/rehearse-sample-service-delivery.sh`, `scripts/operations/generate-compose-profile-service-coverage.sh`, `scripts/operations/generate-tech-stack-version-provenance.sh`, `scripts/operations/provider_surface_renderer.py`, `scripts/operations/use-qa-ci-tools.sh`, `scripts/operations/sync-provider-surfaces.sh`, `scripts/operations/sync-tech-stack-versions.sh`                                                                                  |
| Security   | `scripts/security/seed-grype-db-cache.sh`, `scripts/security/verify-sample-service-supply-chain.sh`, `scripts/security/generate-supply-chain-sample-service-summary.sh`                                                                                                                                                                                                                                                                                     |
| Libraries  | `scripts/lib/hardening-lib.sh`, `scripts/requirements.txt`, `scripts/requirements-pre-commit.txt`                                                                                                                                                                                                                                                                                                                   |

## How to Work in This Area

1. Read this README before adding, renaming, or removing a script.
2. Place new scripts under the existing purpose folder that owns the behavior.
3. Do not add root-level `scripts/*.sh` duplicates for purpose-folder scripts.
4. Reference canonical purpose-folder paths from docs, CI, hooks, and pre-commit entries.
5. Use `python3 scripts/validation/run-ci-gate.py --profile full` to verify the six public suites.
6. Keep secret-related examples procedural only; do not print or document generated secret values.
7. Keep Python module dependencies for repository validation scripts in `scripts/requirements.txt`.

## Active Surface Retention Rules

Keep a root `scripts/` implementation when any active surface uses it:

- GitHub Actions, pre-commit, Claude/Codex hooks, root README files, active
  specs, active operations docs, or `infra/**/README.md` reference the script.
- Another implementation script sources it as a library.
- The script is the single canonical entrypoint for a manual operation, such as
  local preflight checks or local secret file generation.

Remove or reject a script when it is only a duplicate wrapper, a one-off operation
captured by active documentation, or a deleted entrypoint reintroduced without an
approved compatibility plan. Historical references under completed requirements,
architecture decisions, execution evidence, governance memory, or generated
reference artifacts are audit evidence and do not by themselves justify keeping a
script.

## Navigation / Inventory

| Component                              | Path                                                                                        | Purpose                                                                                                                                                                                                         |
| :------------------------------------- | :------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Docker Validation                      | [validate-docker-compose.sh](./validation/validate-docker-compose.sh)                       | Validate root compose config                                                                                                                                                                                    |
| Compose Core Readiness Harness         | [run-compose-core-readiness.sh](./validation/run-compose-core-readiness.sh)                 | Preflight and execute the approved isolated five-service startup, recovery, timeout, typed-evidence, and owned-cleanup contract                                                                                  |
| Compose Core Readiness Library         | [compose-core-readiness.lib.sh](./validation/compose-core-readiness.lib.sh)                 | Shared fail-closed identity, path, render, readiness, recovery, evidence, redaction, and cleanup functions; source only through the harness or focused tests                                                     |
| PostgreSQL Logical Recovery Rehearsal  | [rehearse-postgres-logical-upgrade.sh](./lib/ops/rehearse-postgres-logical-upgrade.sh)   | `scripts/lib/ops/rehearse-postgres-logical-upgrade.sh` checks or runs the pinned synthetic PostgreSQL 17.6-to-18.4 logical backup, isolated restore, semantic integrity, negative-path, atomic verdict, and owned-cleanup contract |
| Harness Validation                     | [validate-harness.sh](./lib/ops/validate-harness.sh)                                     | Run the harness-surface validation wrapper without duplicating local QA gate logic                                                                                                                               |
| Agent Governance Contract Check        | [check-agent-governance-contract.py](./validation/check-agent-governance-contract.py)       | Validate duplicate-key-safe typed Stage 00 artifact, catalog, provider/model, path-authority, and adoption contracts; repository sections activate only after their owning convergence task                     |
| Agentic Audit Semantic Freshness       | [check-agentic-audit-semantic-freshness.py](./validation/check-agentic-audit-semantic-freshness.py) | Enforce the bounded canonical-audit closure assertions and lifecycle routes from tracked repository evidence                                                                                                     |
| Document Metadata Inventory / Changed Gate | [check-document-metadata.py](./validation/check-document-metadata.py)                    | Parse typed metadata profiles, generate/check the advisory inventory, and enforce safely selected changed/new Markdown without rewriting documents                                                              |
| Document Corpus Lifecycle Gate         | [check-document-corpus-lifecycle.py](./validation/check-document-corpus-lifecycle.py)    | Enforce migration contracts, promoted manifests, impacted records, safe Git provenance, duplicate reports, review signals, directory budgets, and deterministic lifecycle evidence without mutating corpus documents |
| Target Surface Contract Gate           | [check-target-surface-contract.py](./validation/check-target-surface-contract.py)          | Run the thin CLI over the immutable `target_surface_contract.py` finding API for manifest coverage, removed active targets/claims, phantom gitlinks, the sample Service, and reviewed duplicate disposition without rendering bodies or values |
| Target Surface Delta Contract Gate     | [check-target-surface-delta-contract.py](./validation/check-target-surface-delta-contract.py) | Validate the live six-suite ownership, changed-path impact, profile routing, tracked entrypoints, retired paths, and copied-command absence without branch/SHA snapshots |
| Typed Gate Contract Library            | [ci_gate_contract.py](./lib/gate/ci_gate_contract.py)                                    | Parse and validate the dependency-free strict-JSON schema-v2 gate DAG, suite ownership, required roots, and local profile roots |
| Typed Gate Runner                      | [run-ci-gate.py](./validation/run-ci-gate.py)                                              | Explain or execute the closed `changed` and `full` public profiles through tracked descriptor-bound entrypoints with minimal environments and bounded timeouts |
| Typed Gate Adapters                    | [ci_gate_adapters.py](./lib/gate/ci_gate_adapters.py)                                    | Implement the closed argument grammar used by typed gate leaves without shell interpolation or ambient secret forwarding |
| GitHub Workflow Contract Gate          | [check-github-workflow-contract.py](./validation/check-github-workflow-contract.py)          | Validate exact tracked workflow triggers, permissions, concurrency, job identities, the canonical typed gate registry, and locally evidenced full-SHA Action dependencies |
| CI-only Pre-commit Entry Point         | [run-ci-precommit.sh](./validation/run-ci-precommit.sh)                                      | Run the pinned all-files hook command only inside GitHub Actions with the dedicated frontend-lint skip; this script is not an Agent authorization path |
| Storybook Contract Check               | [check-storybook-contract.sh](./validation/check-storybook-contract.sh)                     | Enforce Storybook CI scripts, workflow wiring, and 90% coverage threshold metadata                                                                                                                              |
| QuickWin Baseline Check                | [check-quickwin-baseline.sh](./validation/check-quickwin-baseline.sh)                       | Enforce PLN-QW-001~005 baseline controls                                                                                                                                                                        |
| Template & Security Baseline Check     | [check-template-security-baseline.sh](./validation/check-template-security-baseline.sh)     | Enforce template adoption and required security controls                                                                                                                                                        |
| Audit Implementation Matrix Snapshot   | [generate-audit-implementation-matrix.sh](./validation/generate-audit-implementation-matrix.sh) | Generate and check the Stage 90 audit implementation matrix snapshot for audit report coverage, overview categories, automation candidate closure, generated evidence surfaces, and residual gap signals |
| Audit Criterion Completeness Contract  | [audit_criterion_contract.py](./validation/audit_criterion_contract.py)                           | Enforce the shared exact 11-report / 161-row manifest, 10-field schema, non-empty fields, IDs/prefixes, vocabularies, cardinalities, and uniqueness used by both audit scripts                         |
| Security Automation Readiness Snapshot | [generate-security-automation-readiness.sh](./validation/generate-security-automation-readiness.sh) | Generate and check the Stage 90 security automation readiness snapshot for vulnerability gate, SBOM, provenance/attestation, Scorecard, workflow security, secret scanning, Dependabot, and hardening coverage |
| Audit Pack Coverage Report             | [report-audit-pack-coverage.sh](./validation/report-audit-pack-coverage.sh)                 | Report and check implementation-status coverage for the agentic engineering audit pack without mutating audit reports                                                                                            |
| Agent Output Eval Fixture Runner       | [run-agent-output-eval-fixtures.sh](./validation/run-agent-output-eval-fixtures.sh)         | List, check, and locally score advisory agent-output eval fixtures without model calls, CI gates, or runtime mutation                                                                                           |
| Controlled Agent Pre-commit Wrapper    | [run-agent-precommit-all-files.sh](./validation/run-agent-precommit-all-files.sh)           | Run the configured all-files hook suite only at an approved final QA gate in a clean linked worktree, with tracked task evidence, explicit allowed path prefixes, and a value-free first-failure diagnostic       |
| Documentation Implementation Alignment | [check-doc-implementation-alignment.sh](./validation/check-doc-implementation-alignment.sh) | Validate active Stage 01-05 docs against tracked implementation surfaces, removed template names, archive index-only links, operations service coverage, scripts, and workflow paths                            |
| Documentation Traceability Check       | [check-doc-traceability.sh](./validation/check-doc-traceability.sh)                         | Enforce sync links across 03.specs plans ↔ 05.operations                                                                                                                                                    |
| Local QA Gate Runner                   | [run-local-qa-gates.sh](./validation/run-local-qa-gates.sh)                                 | Delegate changed, full, or explain requests to the public runner without owning validator composition                                                                                                                     |
| Supply-chain Fixture Policy             | [check-supply-chain-policy.py](./validation/check-supply-chain-policy.py)                    | Deterministically validate local pins, subject, exception, SBOM, provenance, signature, and advisory Scorecard fixtures without network access                                                                    |
| Grype DB Cache Seed Harness              | [seed-grype-db-cache.sh](./security/seed-grype-db-cache.sh)                                  | Task7-owned approved-network seed-only entrypoint; publishes a validated private cache generation while the supply-chain advisory remains offline                                                                 |
| Supply-chain Local Rehearsal            | [verify-sample-service-supply-chain.sh](./security/verify-sample-service-supply-chain.sh)    | Preflight, fixture-only, and optional local advisory baseline/candidate verification with an ephemeral `/tmp` signing key                                                                                        |
| Supply-chain Summary Generator          | [generate-supply-chain-sample-service-summary.sh](./security/generate-supply-chain-sample-service-summary.sh) | Generate or check the concise tracked local supply-chain reference summary                                                                                                                        |
| LLM Wiki Generator                     | [generate-llm-wiki.py](./knowledge/generate-llm-wiki.py)                                    | Generate and check both the repo-local path index and Stage 90 source-bucket/category coverage snapshot                                                                                                                               |
| Graphify Health Report                 | [report-graphify-health.sh](./knowledge/report-graphify-health.sh)                          | Report advisory health of generated Graphify corpus without blocking validation                                                                                                                                 |
| Agent Event Hook                       | [agent-event-hook.sh](./hooks/agent-event-hook.sh)                                          | Dispatch Claude/Codex hook events, including template-first target-stage docs guidance, current-task routing, post-edit style validation/formatting, logical commit completion reminders, and Stop gating        |
| Post Tool Validation                   | [post-tool-validate.sh](./hooks/post-tool-validate.sh)                                      | Run path-aware validation, including changed-doc template enforcement, after Claude/Codex file edits                                                                                                            |
| Unified Hardening Check                | [check-all-hardening.sh](./hardening/check-all-hardening.sh)                                | Run all tier hardening checks, or one selected tier                                                                                                                                                             |
| QA/CI Tooling Environment              | [use-qa-ci-tools.sh](./operations/use-qa-ci-tools.sh)                                       | Expose user-global QA/CI tools to restricted agent shells                                                                                                                                                       |
| Docker Preflight Mode                  | [validate-docker-compose.sh](./validation/validate-docker-compose.sh) `--preflight`         | Real local prerequisite validation without dummy file creation                                                                                                                                                  |
| Secret Generation                      | [gen-secrets.sh](./operations/gen-secrets.sh)                                               | Generate local Docker secret files; use `--check` or `--dry-run` before default generation                                                                                                                      |
| Sample Service Delivery Rehearsal      | [rehearse-sample-service-delivery.sh](./operations/rehearse-sample-service-delivery.sh)     | Validate fixture contracts or run the canonical-gated local baseline/canary promotion, rollback, atomic evidence, and owned-cleanup state machine                                                              |
| Provider Surface Renderer              | [provider_surface_renderer.py](./operations/provider_surface_renderer.py)                   | Deterministically render shared and Claude `SKILL.md` projections from typed Stage 00 function sources with confined, bounded writes; `--check` is read-only and `--write` applies                                                     |
| Provider Surface Sync                  | [sync-provider-surfaces.sh](./operations/sync-provider-surfaces.sh)                         | Thin compatibility wrapper for the Stage 00 provider renderer; default verifies, `--write` applies                                                                                                                |
| Tech-Stack Version Sync                | [sync-tech-stack-versions.sh](./operations/sync-tech-stack-versions.sh)                     | Re-point curated `infra/tech-stack.versions.json` images to declared compose tags; default writes, `--check` verifies, `--dry-run` previews                                                                     |
| Compose Profile Coverage Snapshot      | [generate-compose-profile-service-coverage.sh](./operations/generate-compose-profile-service-coverage.sh) | Generate and check the Stage 90 Docker Compose profile/service coverage reference from tracked Compose files                                                                                                    |
| Tech-Stack Version Provenance Snapshot | [generate-tech-stack-version-provenance.sh](./operations/generate-tech-stack-version-provenance.sh) | Generate and check the Stage 90 tech-stack registry drift severity and source provenance reference from curated registry and Compose image declarations                                                         |

## Hardening Tier Arguments

Use `bash scripts/hardening/check-all-hardening.sh <tier>` for a selected
tier. Without arguments, all supported tiers are checked.

| Tier          | Accepted arguments                         |
| :------------ | :----------------------------------------- |
| Gateway       | `01-gateway`, `gateway`                    |
| Auth          | `02-auth`, `auth`                          |
| Security      | `03-security`, `security`                  |
| Data          | `04-data`, `data`                          |
| Messaging     | `05-messaging`, `messaging`                |
| Observability | `06-observability`, `observability`, `obs` |
| Workflow      | `07-workflow`, `workflow`                  |
| AI            | `08-ai`, `ai`                              |
| Tooling       | `09-tooling`, `tooling`                    |
| Laboratory    | `11-laboratory`, `laboratory`, `lab`       |

## Script Lifecycle

## Validation ownership

`scripts/manifest.yaml` is the executable ownership registry. Atomic validator
rows declare exactly one public suite: `agent-governance`,
`document-contract`, `document-graph`, `document-lifecycle`, `operations`, or
`repository-integrity`. The 35 retained Task 11 validator identities and suite
owners remain immutable. `execution_contexts` separately declares whether a
canonical standalone invocation is admitted locally, for a pull request, for a
push, or for manual workflow dispatch. An empty list preserves ownership for
library-only, argument-dependent, recursive-wrapper, or approved-runtime
consumers without auto-launching them; registered internal adapter subcommands
remain part of the context-filtered graph. Final-plan admission checks every
inherited and canonical invocation: local plans omit CI-only hardening, and
manual/runtime/recursive validator rebinding fails before execution. Internal
calls require their exact path, argv, and execution context; neither an adapter
path nor an unclassified path is an exemption. Explain validates this same
complete plan before rendering its canonical validator rows. The registry
rejects ownership and execution-policy drift. Focused document-governance tests
mirror their modules
under `tests/lib/document_governance/`; CLI and aggregate contracts remain under
`tests/validation/`.

| Lifecycle                   | Scripts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CI / quality gate           | `python3 scripts/validation/run-ci-gate.py --profile changed`, `python3 scripts/validation/run-ci-gate.py --profile full` |
| Advisory evidence           | `scripts/validation/check-document-metadata.py --mode report`, `scripts/validation/generate-audit-implementation-matrix.sh`, `scripts/validation/generate-security-automation-readiness.sh`, `scripts/validation/report-audit-pack-coverage.sh`, `scripts/validation/run-agent-output-eval-fixtures.sh`, `scripts/knowledge/report-graphify-health.sh` |
| Runtime hook                | `scripts/hooks/agent-event-hook.sh`, `scripts/hooks/post-tool-validate.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Tier hardening              | `scripts/hardening/check-all-hardening.sh <tier>`                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Manual operations           | `scripts/validation/validate-docker-compose.sh --preflight`, `scripts/security/seed-grype-db-cache.sh --preflight`, `scripts/security/seed-grype-db-cache.sh --seed`, `scripts/security/verify-sample-service-supply-chain.sh --preflight`, `scripts/security/verify-sample-service-supply-chain.sh --fixture-only`, `scripts/security/verify-sample-service-supply-chain.sh --advisory`, `scripts/operations/gen-secrets.sh`, `scripts/operations/rehearse-sample-service-delivery.sh preflight`, `scripts/operations/rehearse-sample-service-delivery.sh rehearse`, `scripts/operations/rehearse-sample-service-delivery.sh cleanup`                                                                 |
| Agent QA/CI environment     | `source scripts/operations/use-qa-ci-tools.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Generated index maintenance | `scripts/knowledge/generate-llm-wiki.py --write`, `scripts/operations/generate-compose-profile-service-coverage.sh`, `scripts/operations/generate-tech-stack-version-provenance.sh`, `scripts/validation/generate-audit-implementation-matrix.sh`, `scripts/validation/generate-security-automation-readiness.sh`, `scripts/security/generate-supply-chain-sample-service-summary.sh` |
| Internal library            | `scripts/lib/hardening-lib.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

`scripts/operations/gen-secrets.sh` is a manual operation entrypoint. Its
no-argument mode may read or write local secret registry and secret files; use
`--check` for readiness checks and `--dry-run` for ID/path-only action previews
before running the default mode.

`scripts/security/seed-grype-db-cache.sh` is governed by the
[supply-chain policy checker](validation/check-supply-chain-policy.py).
Only its explicit `--seed` mode may use the approved pinned-Grype database
network boundary; `--preflight` is network-free. The consumer
`verify-sample-service-supply-chain.sh --advisory` never updates or downloads a
database and revalidates the published immutable seed before copying it into a
private, offline scan cache.

`scripts/hooks/post-tool-validate.sh` is a hook payload consumer. With no JSON
payload or no changed paths, it exits successfully without running validators.
Use `--check` or `POST_TOOL_VALIDATE_CHECK_ONLY=1` to run non-mutating
validation; check-only mode disables whitespace writes and `shfmt -w` while
preserving diff, syntax, and repo checks.

`scripts/validation/run-ci-gate.py` is the dependency-free typed-gate CLI. It
loads `.github/workflow-contract.yml` plus `scripts/manifest.yaml`, selects the
closed `changed` or `full` public profile, and keeps `--explain` execution-free.
Explain and execution use the same context-filtered, exact-once canonical plan.
PR and non-initial push bases are validated and forwarded as
`TEMPLATE_GATE_BASE`; local, initial push, and workflow dispatch use the explicit
active-corpus metadata mode without inventing a comparison base.

`scripts/validation/run-local-qa-gates.sh` is a thin local-profile wrapper.
`--changed`, `--full`, and `--explain` each delegate exactly once to the public
runner; the wrapper does not retain a child-command list or mutate `.env`.

`scripts/validation/audit_criterion_contract.py` is the shared parser and exact
manifest for both audit scripts. It rejects missing/unexpected reports, malformed
headers/separators/rows, any criterion row that does not have ten non-empty
trimmed fields, invalid state/depth/disposition values, missing/unexpected IDs,
wrong report/prefix/total counts, and duplicate IDs. The generated frontmatter
semantic inventory is a named non-criterion pack artifact and does not change
the exact eleven-report / 161-row criterion cardinality.

`scripts/validation/check-agentic-audit-semantic-freshness.py` is the bounded
canonical-audit semantic gate used by repository contracts, the audit matrix
generator, and the existing CI quality job. It proves that the eleven declared
closure assertions agree with their canonical rows, tracked evidence, completed
task evidence, stale-phrase exclusions, and audit-pack lifecycle routes. It is
offline and history-independent; it does not prove live runtime readiness,
remote CI or branch-protection enforcement, provider entitlement, deployment
state, broad security scanning, or semantic model quality.

`scripts/validation/check-document-metadata.py` uses the Stage 99 typed profile
contract and PyYAML safe loading with duplicate-key rejection. `--mode report`
always renders the sorted target-document inventory and treats semantic gaps as
advisory; parser/configuration failures remain errors. Use `--output <path>` to
generate the canonical snapshot and add `--check` for freshness. The
`--mode check-contracts` repository gate reuses that loaded registry to require
exact README ownership, complete and type-consistent copyable Markdown template
mapping, sole machine
ownership of full registry arrays, and `_workspace` exclusion from docs
inventory inference. `check-changed` is the pre-push blocking mode for a safely
selected diff;
`check-active` is the base-free active-corpus check. Base resolution prefers explicit, CI, and
safe local refs, then reports a working-tree-only fallback without selecting
the full corpus. A narrow base-existing legacy exception cannot apply to new
documents or partial typed migrations. Reverse transitions require a separate
scoped evidence manifest and the default hook supplies none. The legacy
exception validates a base record against the base manifest and admits only
stable current deficit identities already present at the merge base. Template
placeholder checks recursively detect registered angle-bracket tokens inside
composed scalars and lists without treating date-like ID text as a global
placeholder. Run the focused suite with
`python3 -m unittest discover -s tests/lib/document_governance/metadata -p 'test_*.py' -v`.
Changed-path review includes tracked, staged, unstaged-new, renamed, and
explicit existing Markdown paths while treating deletions as non-parseable
selected paths. The report exposes deterministic semantic states for every
Task 4 inventory field and normalizes YAML/configuration defects without raw
tracebacks or unsafe metadata values.

`scripts/validation/check-document-corpus-lifecycle.py` is the focused lifecycle
companion. It exposes exactly four modes, each reachable from a registered
gate: `--mode check-public`, `--mode check-contract`, `--mode check-promoted`,
and `--mode check-recovery`, which re-proves that every tombstone's
`commit:path` resolves to a regular Git blob. Any other `--mode` value is an
argparse error. Parser, contract, Git, path, redaction, and internal safety
failures still fail closed.
Run its focused inventory with
`python3 -m unittest discover -s tests/validation/lifecycle -p 'test_*.py' -v`.
The executable test inventory is the four responsibility modules under
`tests/validation/lifecycle/`; no legacy aggregate or redirect remains.

`scripts/validation/check-target-surface-contract.py` is the thin focused gate
for Spec 133 target convergence. The immutable library finding records expose
stable codes, safe repository paths, and value-free messages. Metadata,
archive, Compose, and workflow semantics remain delegated to their existing
owners. Run its focused suite with
`python3 -m unittest tests.lib.target_surface.test_target_surface_contracts -v`.

`scripts/validation/check-target-surface-delta-contract.py` is the live routing
gate. It validates six exact suites, exact-once manifest and executable route
ownership, changed-path impact, current tracked entrypoints, profile-surface
agreement, and retirement absence. Historical predecessor snapshots remain
Git/Migration evidence and are not regenerated as current gate state.
Run its focused suite with
`python3 -m unittest tests.lib.target_surface.test_target_surface_delta_contracts -v`.

`scripts/validation/run-agent-precommit-all-files.sh` is the only approved
agent entrypoint for `pre-commit run --all-files`. Use it only at the approved
final QA gate, from an initially clean linked worktree, with one tracked
`docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md` path and one or more narrow repository-relative
`--allow-prefix` values. Direct all-files execution is prohibited. The wrapper
captures hook output in ephemeral files, reports only the command, prefixes,
hook exit, a value-free first-failure result, and before/after/newly changed
Git-visible paths. A successful run reports `first_failure=not_applicable`. A
nonzero hook exit reports at most one tuple containing an exact, uniquely
registered `.pre-commit-config.yaml` hook ID and either `exit_0` through
`exit_255` or `files_modified`; absent, malformed, unregistered, duplicate,
ambiguous, oversized, binary, or spoofable metadata reports
`first_failure=unavailable`. Hook names, messages, durations, raw command
output, output-derived paths, configuration or environment values, and secrets
are never printed.
The wrapper never writes task evidence. Exit `20` means a hook changed a newly
observed path outside every prefix; otherwise the wrapper returns the hook's
exit status.
Review and record hook-managed edits separately. Never use reset, checkout, or
clean to conceal an unexpected result.

The observation boundary is limited to Git-visible, non-ignored repository
paths reported by `git status`. Ignored paths and writes outside the repository
are not observed, and the wrapper is not a process or filesystem sandbox. Task
evidence must use this same narrow claim. Task and existing allow-prefix path
components must not be symlinks; a nonexistent allow-prefix tail remains valid
for new output. Any before/after Git snapshot failure exits `6` rather than
treating an empty path set as success.

`scripts/validation/report-audit-pack-coverage.sh` reads the agentic engineering
implementation audit pack through the shared contract and prints exact
criterion coverage by report and prefix, normalized/raw status, and overview
category. Its `--check` mode is used by repo contracts to catch structural or
cardinality defects without modifying audit files.

`scripts/validation/generate-audit-implementation-matrix.sh` reads the agentic
engineering implementation audit pack through the shared contract and reads
generated evidence surfaces to create a Stage 90 governance data snapshot. It
fails before write or freshness comparison when the criterion contract or its
overview/candidate structure is invalid. It does not rewrite audit conclusions,
change CI gates, run model calls, run scanners, generate SBOMs, sign artifacts,
attest builds, query remote GitHub, or read secrets. Its `--check` mode is used
by repo contracts to keep the generated matrix fresh.

`scripts/validation/generate-security-automation-readiness.sh` reads tracked
workflow, script, governance, Dependabot, hardening, and registry-reference
surfaces to generate a Stage 90 security automation readiness snapshot. It does
not run vulnerability scanners, generate SBOMs, sign artifacts, attest builds,
query registries, query remote GitHub, or read secrets. Its `--check` mode is
used by repo contracts to keep the generated snapshot fresh.

Repo-local Hookify validation is selected through
`python3 scripts/validation/run-ci-gate.py --profile changed`; provider hooks do
not copy atomic validator commands.

---

## Utilities & Automation

### Standard Rules

- **Idempotency**: All scripts MUST be safe to run multiple times without causing corrupted state.
- **No Secrets**: Scripts must fetch credentials from environment variables; never hardcode them.
- **Deterministic**: Any automation added must comply with repository governance in `../docs/00.agent-governance/policies/`.

### Usage Examples

```bash
# Run real local preflight checks without creating dummy files
./scripts/validation/validate-docker-compose.sh --preflight

# Enforce all six public suites
python3 scripts/validation/run-ci-gate.py --profile full

# Enforce focused target-surface convergence contracts
python3 scripts/validation/check-target-surface-contract.py

# Enforce advisory successor-delta and generated-summary contracts
python3 scripts/validation/check-target-surface-delta-contract.py --mode advisory

# Enforce active docs to tracked implementation alignment
bash scripts/validation/check-doc-implementation-alignment.sh

# Enforce Quick Win baseline
./scripts/validation/check-quickwin-baseline.sh

# Enforce Quick Win baseline for an explicit compose profile set
# Fails when any selected profile has baseline violations.
HYHOME_COMPOSE_PROFILES="core dev" ./scripts/validation/check-quickwin-baseline.sh

# Enforce template + security baseline
./scripts/validation/check-template-security-baseline.sh

# Enforce documentation traceability sync
./scripts/validation/check-doc-traceability.sh

# Run changed-path public suites
./scripts/validation/run-local-qa-gates.sh --changed

# Explain changed-path suite-to-validator ownership without execution
./scripts/validation/run-local-qa-gates.sh --explain

# Run the harness-change-scoped fast gate
./scripts/lib/ops/validate-harness.sh

# Report implementation-status coverage for the agentic engineering audit pack
./scripts/validation/report-audit-pack-coverage.sh

# Generate and check the audit implementation matrix snapshot
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/validation/generate-audit-implementation-matrix.sh --check

# List and check local advisory agent-output eval fixtures
bash scripts/validation/run-agent-output-eval-fixtures.sh --list
bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions

# Approved final QA only; prefixes must match the task's reviewed scope
bash scripts/validation/run-agent-precommit-all-files.sh \
  --task docs/03.specs/9999-example-change/tasks/tsk-0001-example.md \
  --allow-prefix docs/ \
  --allow-prefix scripts/

# Generate both repo-local LLM Wiki artifacts
python3 scripts/knowledge/generate-llm-wiki.py --write

# Verify both LLM Wiki artifacts are fresh
python3 scripts/knowledge/generate-llm-wiki.py --check

# Report advisory Graphify corpus health
./scripts/knowledge/report-graphify-health.sh

# Verify or regenerate Stage 00-derived provider skill projections
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/operations/sync-provider-surfaces.sh --write

# Dispatch a provider-neutral PreToolUse hook event
printf '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rg hook"}}' | bash scripts/hooks/agent-event-hook.sh PreToolUse

# Run provider-neutral post-edit validation from a file-edit hook payload
printf '{"tool_input":{"file_path":"docs/00.agent-governance/policies/task-checklists.md"}}' | bash scripts/hooks/post-tool-validate.sh

# Run provider-neutral post-edit validation without formatting writes
printf '{"tool_input":{"file_path":"docs/00.agent-governance/policies/task-checklists.md"}}' | bash scripts/hooks/post-tool-validate.sh --check

# Enforce all tier hardening baselines
./scripts/hardening/check-all-hardening.sh

# Enforce one selected tier
./scripts/hardening/check-all-hardening.sh 01-gateway

# Inspect secret-generation readiness without reading or writing secret values
./scripts/operations/gen-secrets.sh --check

# Preview secret-generation actions by ID/path only
./scripts/operations/gen-secrets.sh --dry-run

# Verify the tech-stack version registry is synced to declared compose tags
bash scripts/operations/sync-tech-stack-versions.sh --check

# Preview planned tech-stack registry tag updates without writing
bash scripts/operations/sync-tech-stack-versions.sh --dry-run

# Re-point the tech-stack registry to declared compose tags
bash scripts/operations/sync-tech-stack-versions.sh

# Generate the Docker Compose profile/service coverage reference
bash scripts/operations/generate-compose-profile-service-coverage.sh

# Verify the Docker Compose profile/service coverage reference is fresh
bash scripts/operations/generate-compose-profile-service-coverage.sh --check

# Generate and verify the tech-stack version provenance reference
bash scripts/operations/generate-tech-stack-version-provenance.sh
bash scripts/operations/generate-tech-stack-version-provenance.sh --check

# Make globally installed QA/CI tools available in restricted agent shells
source scripts/operations/use-qa-ci-tools.sh

# Verify the agent-visible QA/CI toolchain
./scripts/operations/use-qa-ci-tools.sh

```

---

## Invocation Safety

Check-only validators use `mutation: none`. Generators and synchronizers use
`mutation: check-write`: their default invocation must check or render without
changing repository state, while an explicit `--write` is required for a
repository update. A retained check-write generator registers a safe argv
`check_command` and the exact tracked `outputs` that it owns. `mutation:
runtime` scripts are Operations entrypoints;
they are not run during document migration and require a current Runbook plus
the declared test evidence before explicit invocation.

Do not invoke a `mutation: runtime` row from inventory or migration evidence;
follow its current Runbook and explicit operator boundary. Do not invoke a
default-write generator without its documented non-mutating check option;
rows that lack safe defaults are classified for rewrite or merge. Consumers
and tests require semantic invocation/import evidence: a manifest mention,
generated index, archive record, or ownership glob is not consumption.

The canonical LLM Wiki generator is
`python3 scripts/knowledge/generate-llm-wiki.py`. It owns both tracked outputs,
defaults to `--check`, and mutates them only with explicit `--write`.

## Verification

Run the manifest and generated-output gates with:

```bash
python3 scripts/validation/check-script-manifest.py
python3 scripts/validation/check-script-manifest.py --check-generated
python3 scripts/knowledge/generate-llm-wiki.py --check
PYTHONPATH=. .venv/bin/python tests/validation/test_script_manifest.py
PYTHONPATH=. .venv/bin/python tests/validation/test_generate_llm_wiki.py
```

The gate derives coverage from tracked plus present non-ignored Task-local
paths, verifies exact field and vocabulary contracts, checks deterministic
ordering, and requires all declared consumer and test paths to contain
invocation/import evidence. `--check-generated` runs only retained check-write
generators; it never invokes runtime-changing rows.

## Related Documents

- [🤖 Agent Governance](../AGENTS.md)
- [⚙️ Operations Baseline](../docs/05.operations/README.md)
- [📘 Runbooks](../docs/05.operations/README.md)
- [LLM Wiki Maintenance](../docs/05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md)
- [LLM Wiki Generated Index](../docs/90.references/data/0082-llm-wiki-index/README.md)
- [Public Suite Ownership Manifest](manifest.yaml)
- [Workspace Governance Authority](../docs/02.architecture/decisions/0029-workspace-governance-authority.md)
- [Document Profile Registry](../docs/99.templates/registry.json)

Note: QuickWin baseline exceptions are sourced from `infra/common-optimizations.exceptions.json`.
