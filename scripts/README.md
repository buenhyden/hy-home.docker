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
├── operations/          # Safe secret-generation utility
├── requirements.txt     # Python modules required by repository validation scripts
├── lib/
│   └── hardening-lib.sh # Shared implementation for tier hardening checks
└── README.md            # This file
```

## Purpose Folder Implementation

The canonical script surface is the purpose-folder path. Root-level
`scripts/*.sh` duplicates were removed after docs, CI, hooks, and pre-commit
references moved to purpose-folder paths. Do not recreate root duplicate
wrappers unless a future approved compatibility plan explicitly requires them.

The hardening surface is intentionally consolidated into
`scripts/hardening/check-all-hardening.sh`. Tier-specific wrapper entrypoints
were removed by the 2026-05-17 cleanup; use tier arguments instead.

| Purpose    | Canonical paths                                                                                                                                                                                                                                                                                                                                                                                                    |
| :--------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Validation | `scripts/validation/validate-docker-compose.sh`, `scripts/validation/validate-harness.sh`, `scripts/validation/check-repo-contracts.sh`, `scripts/validation/check-document-metadata.py`, `scripts/validation/check-agentic-audit-semantic-freshness.py`, `scripts/validation/check-doc-implementation-alignment.sh`, `scripts/validation/check-storybook-contract.sh`, `scripts/validation/check-doc-traceability.sh`, `scripts/validation/check-quickwin-baseline.sh`, `scripts/validation/check-template-security-baseline.sh`, `scripts/validation/generate-audit-implementation-matrix.sh`, `scripts/validation/generate-security-automation-readiness.sh`, `scripts/validation/recommend-gap-routing.sh`, `scripts/validation/recommend-qa-gates.sh`, `scripts/validation/report-audit-pack-coverage.sh`, `scripts/validation/report-provider-hook-parity.sh`, `scripts/validation/run-agent-output-eval-fixtures.sh`, `scripts/validation/run-agent-precommit-all-files.sh`, `scripts/validation/run-local-qa-gates.sh` |
| Hardening  | `scripts/hardening/check-all-hardening.sh`                                                                                                                                                                                                                                                                                                                                                                         |
| Hooks      | `scripts/hooks/agent-event-hook.sh`, `scripts/hooks/patch-graphify-post-commit.sh`, `scripts/hooks/post-tool-validate.sh`                                                                                                                                                                                                                                                                                          |
| Knowledge  | `scripts/knowledge/generate-llm-wiki-index.sh`, `scripts/knowledge/generate-llm-wiki-coverage.sh`, `scripts/knowledge/report-graphify-health.sh`                                                                                                                                                                                                                                                                                                      |
| Operations | `scripts/operations/gen-secrets.sh`, `scripts/operations/generate-compose-profile-service-coverage.sh`, `scripts/operations/generate-tech-stack-version-provenance.sh`, `scripts/operations/use-qa-ci-tools.sh`, `scripts/operations/sync-provider-surfaces.sh`, `scripts/operations/sync-tech-stack-versions.sh`                                                                                                                                                                |
| Libraries  | `scripts/lib/hardening-lib.sh`, `scripts/requirements.txt`                                                                                                                                                                                                                                                                                                                                                         |

## How to Work in This Area

1. Read this README before adding, renaming, or removing a script.
2. Place new scripts under the existing purpose folder that owns the behavior.
3. Do not add root-level `scripts/*.sh` duplicates for purpose-folder scripts.
4. Reference canonical purpose-folder paths from docs, CI, hooks, and pre-commit entries.
5. Use `scripts/validation/check-repo-contracts.sh` to verify script inventory, references, and library usage.
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
| Harness Validation                     | [validate-harness.sh](./validation/validate-harness.sh)                                     | Run the harness-surface validation wrapper without duplicating local QA gate logic                                                                                                                               |
| Repo Contract Check                    | [check-repo-contracts.sh](./validation/check-repo-contracts.sh)                             | Enforce the canonical document registry, typed template and README ownership, Release routes, `_workspace` independence, docs, GitHub, script, image, runtime governance, Hookify metadata, execution evidence status, and closed English-only doc surface contracts               |
| Agent Governance Contract Check        | [check-agent-governance-contract.py](./validation/check-agent-governance-contract.py)       | Validate duplicate-key-safe typed Stage 00 artifact, catalog, provider/model, path-authority, and adoption contracts; repository sections activate only after their owning convergence task                     |
| Agentic Audit Semantic Freshness       | [check-agentic-audit-semantic-freshness.py](./validation/check-agentic-audit-semantic-freshness.py) | Enforce the bounded canonical-audit closure assertions and lifecycle routes from tracked repository evidence                                                                                                     |
| Document Metadata Inventory / Changed Gate | [check-document-metadata.py](./validation/check-document-metadata.py)                    | Parse typed metadata profiles, generate/check the advisory inventory, and enforce safely selected changed/new Markdown without rewriting documents                                                              |
| Document Corpus Lifecycle Gate         | [check-document-corpus-lifecycle.py](./validation/check-document-corpus-lifecycle.py)    | Enforce migration contracts, promoted manifests, impacted records, safe Git provenance, duplicate reports, review signals, directory budgets, and deterministic lifecycle evidence without mutating corpus documents |
| Storybook Contract Check               | [check-storybook-contract.sh](./validation/check-storybook-contract.sh)                     | Enforce Storybook CI scripts, workflow wiring, and 90% coverage threshold metadata                                                                                                                              |
| QuickWin Baseline Check                | [check-quickwin-baseline.sh](./validation/check-quickwin-baseline.sh)                       | Enforce PLN-QW-001~005 baseline controls                                                                                                                                                                        |
| Template & Security Baseline Check     | [check-template-security-baseline.sh](./validation/check-template-security-baseline.sh)     | Enforce template adoption and required security controls                                                                                                                                                        |
| Audit Implementation Matrix Snapshot   | [generate-audit-implementation-matrix.sh](./validation/generate-audit-implementation-matrix.sh) | Generate and check the Stage 90 audit implementation matrix snapshot for audit report coverage, overview categories, automation candidate closure, generated evidence surfaces, and residual gap signals |
| Audit Criterion Completeness Contract  | [audit_criterion_contract.py](./validation/audit_criterion_contract.py)                           | Enforce the shared exact 11-report / 161-row manifest, 10-field schema, non-empty fields, IDs/prefixes, vocabularies, cardinalities, and uniqueness used by both audit scripts                         |
| Security Automation Readiness Snapshot | [generate-security-automation-readiness.sh](./validation/generate-security-automation-readiness.sh) | Generate and check the Stage 90 security automation readiness snapshot for vulnerability gate, SBOM, provenance/attestation, Scorecard, workflow security, secret scanning, Dependabot, and hardening coverage |
| Gap Routing Recommendation Report      | [recommend-gap-routing.sh](./validation/recommend-gap-routing.sh)                           | Print advisory canonical-stage routing suggestions for gap descriptions or related paths without mutating repository/runtime state                                                                               |
| QA Gate Recommendation Report          | [recommend-qa-gates.sh](./validation/recommend-qa-gates.sh)                                 | Print changed-path-based local QA gate recommendations without executing gates or mutating repository/runtime state                                                                                             |
| Audit Pack Coverage Report             | [report-audit-pack-coverage.sh](./validation/report-audit-pack-coverage.sh)                 | Report and check implementation-status coverage for the agentic engineering audit pack without mutating audit reports                                                                                            |
| Provider Hook Parity Report            | [report-provider-hook-parity.sh](./validation/report-provider-hook-parity.sh)               | Generate and check the Stage 90 provider hook parity matrix and Gemini behavioral reminder checklist from tracked provider/governance surfaces                                                                  |
| Agent Output Eval Fixture Runner       | [run-agent-output-eval-fixtures.sh](./validation/run-agent-output-eval-fixtures.sh)         | List, check, and locally score advisory agent-output eval fixtures without model calls, CI gates, or runtime mutation                                                                                           |
| Controlled Agent Pre-commit Wrapper    | [run-agent-precommit-all-files.sh](./validation/run-agent-precommit-all-files.sh)           | Run the configured all-files hook suite only at an approved final QA gate in a clean linked worktree, with tracked task evidence and explicit allowed path prefixes                                             |
| Documentation Implementation Alignment | [check-doc-implementation-alignment.sh](./validation/check-doc-implementation-alignment.sh) | Validate active Stage 01-05 docs against tracked implementation surfaces, removed template names, archive index-only links, operations service coverage, scripts, and workflow paths                            |
| Documentation Traceability Check       | [check-doc-traceability.sh](./validation/check-doc-traceability.sh)                         | Enforce sync links across 04.execution/plans ↔ 05.operations                                                                                                                                                    |
| Local QA Gate Runner                   | [run-local-qa-gates.sh](./validation/run-local-qa-gates.sh)                                 | Run locally reproducible script-backed QA/CI gates and list remote-only CI responsibilities                                                                                                                     |
| LLM Wiki Index Generator               | [generate-llm-wiki-index.sh](./knowledge/generate-llm-wiki-index.sh)                        | Generate and check the repo-local LLM Wiki path index                                                                                                                                                           |
| LLM Wiki Coverage Generator            | [generate-llm-wiki-coverage.sh](./knowledge/generate-llm-wiki-coverage.sh)                  | Generate and check the Stage 90 LLM Wiki source-bucket/category coverage snapshot                                                                                                                               |
| Graphify Health Report                 | [report-graphify-health.sh](./knowledge/report-graphify-health.sh)                          | Report advisory health of generated Graphify corpus without blocking validation                                                                                                                                 |
| Agent Event Hook                       | [agent-event-hook.sh](./hooks/agent-event-hook.sh)                                          | Dispatch Claude/Codex hook events, including template-first target-stage docs guidance, governance memory guidance, post-edit style validation/formatting, logical commit completion reminders, and Stop gating |
| Post Tool Validation                   | [post-tool-validate.sh](./hooks/post-tool-validate.sh)                                      | Run path-aware validation, including changed-doc template enforcement, after Claude/Codex file edits                                                                                                            |
| Graphify Post-commit Patcher           | [patch-graphify-post-commit.sh](./hooks/patch-graphify-post-commit.sh)                      | Re-apply the graphify-out filter to `.git/hooks/post-commit` after hook resets                                                                                                                                  |
| Unified Hardening Check                | [check-all-hardening.sh](./hardening/check-all-hardening.sh)                                | Run all tier hardening checks, or one selected tier                                                                                                                                                             |
| QA/CI Tooling Environment              | [use-qa-ci-tools.sh](./operations/use-qa-ci-tools.sh)                                       | Expose user-global QA/CI tools to restricted agent shells                                                                                                                                                       |
| Docker Preflight Mode                  | [validate-docker-compose.sh](./validation/validate-docker-compose.sh) `--preflight`         | Real local prerequisite validation without dummy file creation                                                                                                                                                  |
| Secret Generation                      | [gen-secrets.sh](./operations/gen-secrets.sh)                                               | Generate local Docker secret files; use `--check` or `--dry-run` before default generation                                                                                                                      |
| Provider Surface Sync                  | [sync-provider-surfaces.sh](./operations/sync-provider-surfaces.sh)                         | Regenerate the Codex mirror and Gemini reference index from the canonical Claude runtime; default verifies, `--write` applies                                                                                   |
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

| Lifecycle                   | Scripts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CI / quality gate           | `scripts/validation/validate-harness.sh`, `scripts/validation/run-local-qa-gates.sh`, `scripts/validation/check-repo-contracts.sh`, `scripts/validation/check-agent-governance-contract.py --mode contract`, `scripts/validation/check-agentic-audit-semantic-freshness.py`, `scripts/validation/check-document-corpus-lifecycle.py`, `scripts/validation/check-doc-implementation-alignment.sh`, `scripts/validation/validate-docker-compose.sh`, `scripts/validation/check-doc-traceability.sh`, `scripts/validation/check-storybook-contract.sh`, `scripts/validation/check-quickwin-baseline.sh`, `scripts/validation/check-template-security-baseline.sh`, `scripts/hardening/check-all-hardening.sh`, `scripts/knowledge/generate-llm-wiki-index.sh --check`, `scripts/knowledge/generate-llm-wiki-coverage.sh --check` |
| Advisory evidence           | `scripts/validation/check-document-metadata.py --mode report`, `scripts/validation/generate-audit-implementation-matrix.sh`, `scripts/validation/generate-security-automation-readiness.sh`, `scripts/validation/recommend-gap-routing.sh`, `scripts/validation/recommend-qa-gates.sh`, `scripts/validation/report-audit-pack-coverage.sh`, `scripts/validation/report-provider-hook-parity.sh`, `scripts/validation/run-agent-output-eval-fixtures.sh`, `scripts/knowledge/report-graphify-health.sh`                                                                                                                                                                                                                                                   |
| Runtime hook                | `scripts/hooks/agent-event-hook.sh`, `scripts/hooks/post-tool-validate.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Tier hardening              | `scripts/hardening/check-all-hardening.sh <tier>`                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Manual operations           | `scripts/validation/validate-docker-compose.sh --preflight`, `scripts/operations/gen-secrets.sh`                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Agent QA/CI environment     | `source scripts/operations/use-qa-ci-tools.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Generated index maintenance | `scripts/knowledge/generate-llm-wiki-index.sh`, `scripts/knowledge/generate-llm-wiki-coverage.sh`, `scripts/operations/generate-compose-profile-service-coverage.sh`, `scripts/operations/generate-tech-stack-version-provenance.sh`, `scripts/validation/generate-audit-implementation-matrix.sh`, `scripts/validation/generate-security-automation-readiness.sh`                                                                                                                                                                                                                                                                                 |
| Internal library            | `scripts/lib/hardening-lib.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

`scripts/operations/gen-secrets.sh` is a manual operation entrypoint. Its
no-argument mode may read or write local secret registry and secret files; use
`--check` for readiness checks and `--dry-run` for ID/path-only action previews
before running the default mode.

`scripts/hooks/post-tool-validate.sh` is a hook payload consumer. With no JSON
payload or no changed paths, it exits successfully without running validators.
Use `--check` or `POST_TOOL_VALIDATE_CHECK_ONLY=1` to run non-mutating
validation; check-only mode disables whitespace writes and `shfmt -w` while
preserving diff, syntax, and repo checks.

`scripts/validation/run-local-qa-gates.sh` is the local script-backed QA/CI
orchestrator. Default mode runs only checks that are safe to execute locally.
Use `--list` to see local, CI/local-tooling, and remote-only responsibilities.
Use `--all-profiles` to run the same local gates with the governed all-profile
Compose set unless `HYHOME_COMPOSE_PROFILES` is already set.

`scripts/validation/recommend-qa-gates.sh` is an advisory changed-path report.
It prints recommended local gates and remote/manual responsibilities without
executing checks or mutating repository, runtime, remote, or secret state. The
CI quality workflow publishes the same advisory report to `GITHUB_STEP_SUMMARY`
without changing the required job set.

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
mapping, consistent Release selection and Stage 00/05 routes, sole machine
ownership of full registry arrays, and `_workspace` exclusion from docs
inventory inference. `check-changed` is the pre-push blocking mode for a safely
selected diff;
`check-active` remains non-gating. Base resolution prefers explicit, CI, and
safe local refs, then reports a working-tree-only fallback without selecting
the full corpus. A narrow base-existing legacy exception cannot apply to new
documents or partial typed migrations. Reverse transitions require a separate
scoped evidence manifest and the default hook supplies none. The legacy
exception validates a base record against the base manifest and admits only
stable current deficit identities already present at the merge base. Template
placeholder checks recursively detect registered angle-bracket tokens inside
composed scalars and lists without treating date-like ID text as a global
placeholder. Run the focused suite with
`python3 -m unittest discover -s tests/validation -p 'test_document_metadata.py' -v`.
Changed-path review includes tracked, staged, unstaged-new, renamed, and
explicit existing Markdown paths while treating deletions as non-parseable
selected paths. The report exposes deterministic semantic states for every
Task 4 inventory field and normalizes YAML/configuration defects without raw
tracebacks or unsafe metadata values.

`scripts/validation/check-document-corpus-lifecycle.py` is the focused lifecycle
companion. Repository contracts always run `--mode check-contract` and
`--mode check-promoted`, then run `--mode check-impacted` only with a verified
explicit comparison commit or a resolvable local `HEAD~1`. The scheduled/manual
workflow keeps full-corpus debt advisory through `--mode report-full`; parser,
contract, Git, path, redaction, and internal safety failures still fail closed.
Run its focused inventory with
`python3 -m unittest discover -s tests/validation -p 'test_document_corpus_lifecycle.py' -v`.
The executable test inventory is
`tests/validation/test_document_corpus_lifecycle.py`.

`scripts/validation/run-agent-precommit-all-files.sh` is the only approved
agent entrypoint for `pre-commit run --all-files`. Use it only at the approved
final QA gate, from an initially clean linked worktree, with one tracked
`docs/04.execution/tasks/` path and one or more narrow repository-relative
`--allow-prefix` values. Direct all-files execution is prohibited. The wrapper
captures hook output in ephemeral files, reports only the command, prefixes,
hook exit, and before/after/newly changed Git-visible paths.
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

Repo-local Hookify metadata validation currently supports only `bash`, `file`,
and `stop` events, as enforced by
`scripts/validation/check-repo-contracts.sh`. External Hookify event names are
not automatically accepted by this repository.

---

## Utilities & Automation

### Standard Rules

- **Idempotency**: All scripts MUST be safe to run multiple times without causing corrupted state.
- **No Secrets**: Scripts must fetch credentials from environment variables; never hardcode them.
- **Deterministic**: Any automation added must comply with repository governance in `../docs/00.agent-governance/rules/`.

### Usage Examples

```bash
# Run real local preflight checks without creating dummy files
./scripts/validation/validate-docker-compose.sh --preflight

# Enforce repository contracts
./scripts/validation/check-repo-contracts.sh

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

# Run locally reproducible QA/CI gates
./scripts/validation/run-local-qa-gates.sh

# Show local vs remote-only QA/CI responsibilities
./scripts/validation/run-local-qa-gates.sh --list

# Run the harness-change-scoped fast gate
./scripts/validation/validate-harness.sh

# Run the same harness subset through the local QA gate runner
./scripts/validation/run-local-qa-gates.sh --harness

# Recommend QA gates for staged and unstaged changes without running them
./scripts/validation/recommend-qa-gates.sh

# Recommend QA gates for an explicit path list
./scripts/validation/recommend-qa-gates.sh --files docs/00.agent-governance/rules/documentation-protocol.md scripts/README.md

# Report implementation-status coverage for the agentic engineering audit pack
./scripts/validation/report-audit-pack-coverage.sh

# Generate and check the audit implementation matrix snapshot
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/validation/generate-audit-implementation-matrix.sh --check

# Generate and verify provider hook parity matrix
bash scripts/validation/report-provider-hook-parity.sh
bash scripts/validation/report-provider-hook-parity.sh --check

# List and check local advisory agent-output eval fixtures
bash scripts/validation/run-agent-output-eval-fixtures.sh --list
bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures

# Approved final QA only; prefixes must match the task's reviewed scope
bash scripts/validation/run-agent-precommit-all-files.sh \
  --task docs/04.execution/tasks/YYYY-MM-DD-feature.md \
  --allow-prefix docs/ \
  --allow-prefix scripts/

# Recommend canonical-stage routing for a gap description
./scripts/validation/recommend-gap-routing.sh --text "runbook recovery procedure is missing rollback evidence"

# Recommend canonical-stage routing for related paths
./scripts/validation/recommend-gap-routing.sh --files docs/03.specs/108-compose-profile-service-coverage-snapshot/spec.md

# Generate the repo-local LLM Wiki path index
bash scripts/knowledge/generate-llm-wiki-index.sh

# Verify the repo-local LLM Wiki path index is fresh
bash scripts/knowledge/generate-llm-wiki-index.sh --check

# Generate and verify the LLM Wiki stage/category coverage snapshot
bash scripts/knowledge/generate-llm-wiki-coverage.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check

# Report advisory Graphify corpus health
./scripts/knowledge/report-graphify-health.sh

# Dispatch a provider-neutral PreToolUse hook event
printf '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rg hook"}}' | bash scripts/hooks/agent-event-hook.sh PreToolUse

# Run provider-neutral post-edit validation from a file-edit hook payload
printf '{"tool_input":{"file_path":"docs/00.agent-governance/memory/progress.md"}}' | bash scripts/hooks/post-tool-validate.sh

# Run provider-neutral post-edit validation without formatting writes
printf '{"tool_input":{"file_path":"docs/00.agent-governance/memory/progress.md"}}' | bash scripts/hooks/post-tool-validate.sh --check

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

## Related Documents

- [🤖 Agent Governance](../AGENTS.md)
- [⚙️ Operations Baseline](../docs/05.operations/README.md)
- [📘 Runbooks](../docs/05.operations/README.md)
- [LLM Wiki Maintenance](../docs/05.operations/guides/00-workspace/llm-wiki-maintenance.md)
- [LLM Wiki Generated Index](../docs/90.references/llm-wiki/llm-wiki-index.md)
- [Scripts CI/CD & QA Cleanup Plan](../docs/04.execution/plans/2026-05-17-scripts-ci-qa-cleanup.md)
- [Scripts Lifecycle Contract Cleanup Plan](../docs/04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md)

Note: QuickWin baseline exceptions are sourced from `infra/common-optimizations.exceptions.json`.
