---
status: active
artifact_id: audit:agentic-engineering-implementation:sdlc-quality-formatting
artifact_type: audit
parent_ids: [audit:agentic-engineering-implementation:overview]
supersedes: [audit:agentic-engineering-implementation-2026-07-07:sdlc-qa-security]
reviewed_at: 2026-07-12
review_cycle: per-remediation-task
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md -->

# Reference: SDLC Quality Formatting Implementation

## Overview

This reference retains the cross-category summary for spec-driven development,
CI/CD, QA, formatting, linting, syntax checks, Docker Compose validation,
infrastructure validation, and security quality gates. Detailed current SDLC
and metadata criteria now live in the two focused Task 4 audit reports.

## Purpose

The purpose is to show which quality and SDLC controls are implemented and
where coverage remains partial or advisory.

## Repository Role

This document supports future QA and SDLC planning. It does not replace
validation scripts, CI workflow source, Stage 03 specs, Stage 04 task evidence,
or Stage 05 operations docs.

## Scope

### In Scope

- Spec-driven development and stage-gated SDLC summary; detailed role,
  numbering, parent, transition, frontmatter, template, and README findings are
  delegated to the focused Task 4 reports.
- CI/CD and local QA gates.
- Formatting, linting, syntax, and contract validation.
- Docker Compose and infrastructure validation.
- Security, hardening, and workflow security quality gates.

### Out of Scope

- Adding tests or CI jobs.
- Changing formatting/linting rules.
- Changing Docker Compose, infrastructure, security, or deployment behavior.
- Claiming production readiness from documentation checks alone.

## Definitions / Facts

- **Spec-driven development** means active design contracts live under
  `docs/03.specs/` and hand off to Stage 04 plans/tasks.
- **QA gate** means a local or CI check with a documented command and pass
  criterion.
- **Formatting/linting coverage** means automated or documented checks for
  style, syntax, or static correctness on a surface.

## Assessment Method

The Task 4 SDLC portion was revalidated on 2026-07-11 at baseline
`e4c92fa1e0e4e59af20efa9f1fcb104e3a8698eb`. Task 6 then reproduced the
quality inventory against tracked workflows, pre-commit configuration,
scripts, project commands, `CHANGELOG.md`, and the release runbook. Seven tracked
workflows contain 22 jobs; `ci-quality.yml` contains 15 quality jobs; the
pre-commit configuration contains 24 hook IDs; the local runner executes 20
script-backed steps or 18 harness steps and lists one advisory recommender
separately. Definitions
do not prove remote runs or branch-protection enforcement.

Read-only remote evidence captured on 2026-07-12 establishes a narrower
configuration fact: classic `main` protection is enabled with 12 required
contexts, while the local contract names 15; `docs-implementation-alignment`,
`agent-output-eval-fixture-gate`, and `dependency-vulnerability-audit` are
absent remotely. Repository rulesets and environments are both `0`. This does
not prove recent check execution and no remote setting was changed.

## Criterion Matrix

| Criterion ID | External criterion | Workspace evidence | Status | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| QAF-01 | Name the applicable evidence class and command instead of claiming undifferentiated “QA.” | Research and scripts distinguish formatting, lint, syntax, type, test, build, coverage, dependency, security, traceability, eval, and freshness evidence. | Implemented | 2 | Retain | QA scope and task evidence owner | Existing named-gate inventory; applicability remains change-scoped. | Compare the quality research matrix with scripts, workflow jobs, and task evidence. | High. |
| QAF-02 | Provide deterministic local orchestration for locally safe gates and disclose excluded responsibilities. | `run-local-qa-gates.sh` executes 20 script-backed steps in default/script-backed/all-profile modes, 18 in harness mode, and lists one non-executed recommender plus CI/remote-only duties. The controlled all-files wrapper remains a separate approved final gate. | Implemented | 3 | Retain | `scripts/validation/run-local-qa-gates.sh` | Existing local orchestration; do not count the recommender or controlled wrapper as default runner steps. | `bash scripts/validation/run-local-qa-gates.sh --list`; inspect direct/helper `run_step` calls. | High. |
| QAF-03 | Enforce formatting only on declared file families and distinguish configuration from execution. | Whitespace/newline hooks and post-tool normalization exist; EditorConfig/Prettier configs exist, but shared automation does not invoke Prettier. | Partial | 2 | Improve | Common scope and relevant project owners | Candidate formatting coverage inventory before any new gate. | Inspect `.editorconfig`, Prettier config, pre-commit hooks, and post-tool script. | High. |
| QAF-04 | Run scoped static linting with explicit exclusions and duplicate-job ownership. | Markdown, YAML, shell, workflow, Dockerfile, and Storybook lint surfaces exist; `recommend-qa-gates.sh` is excluded from ShellCheck and CI pre-commit skips ESLint in favor of `frontend-quality`. | Partial | 3 | Improve | QA scope and language/project owners | Existing scoped hooks/jobs; inventory uncovered languages before expansion. | Inspect hook `files`/`exclude`, CI `SKIP`, and dedicated lint commands. | High. |
| QAF-05 | Parse supported shell, JSON, TOML, YAML, workflow, and Compose inputs without equating syntax with semantics. | `bash -n`, check-json, check-toml, yamllint, actionlint, Compose render, and repository contract checks exist at different layers. | Implemented | 3 | Retain | QA scope and validator owners | Existing parsers; semantic checks remain separately owned. | Run shell syntax and the applicable parser/validator for changed files. | High. |
| QAF-06 | Type-check typed application code without claiming repository-wide coverage. | Storybook Next.js has a dedicated TypeScript command in `frontend-quality`; no universal repository typecheck exists. | Partial | 3 | Retain | Storybook Next.js owner | Existing dedicated CI job; add only for newly typed projects. | `npm run typecheck --prefix projects/storybook/nextjs` or its CI result. | High. |
| QAF-07 | Execute project tests with change-appropriate scope and record N/A explicitly. | Storybook Vitest tests are available and coverage runs them; many documentation/Compose changes use structural validators instead of application tests. | Partial | 2 | Improve | Project owner and QA scope | Existing project tests; require explicit N/A for non-applicable changes. | `npm run test --prefix projects/storybook/nextjs` when applicable. | High. |
| QAF-08 | Build application/static artifacts without presenting build success as deployment. | `frontend-quality` builds Next.js and static Storybook outputs after dependency install. | Implemented | 3 | Retain | Storybook Next.js owner | Existing dedicated CI job. | `npm run build` and `npm run build-storybook` with the project prefix or CI result. | High for build definition; no deployment inference. |
| QAF-09 | Collect and enforce declared coverage thresholds for applicable test projects. | `storybook-coverage` runs the project coverage command, and the Storybook contract checks 90% threshold metadata. | Implemented | 3 | Retain | Storybook Next.js owner and QA scope | Existing CI coverage gate and metadata contract. | `npm run coverage --prefix projects/storybook/nextjs` and `check-storybook-contract.sh`. | High. |
| QAF-10 | Gate dependency vulnerabilities with explicit ecosystem, project, severity, and exception scope. | CI runs `npm audit --audit-level=high` only for `projects/storybook/nextjs`. | Partial | 3 | Improve | Security/QA owner and affected project | Existing scoped gate; broader SCA/container work is defined but still approval-gated in draft Spec 126. | Inspect `dependency-vulnerability-audit` and run only in an approved applicable environment. | High for the one npm project; no broader coverage. |
| QAF-11 | Preserve hook stage/file filters and report intentional skips. | Twenty-four hook IDs have explicit file/stage filters; CI pre-commit intentionally skips `eslint-nextjs` because a dedicated job owns it. | Implemented | 3 | Retain | `.pre-commit-config.yaml` and CI workflow owner | Existing hook/CI orchestration; skipped hook is not silently counted. | Count hook IDs and inspect `files`, `exclude`, `stages`, and CI `SKIP`. | High. |
| QAF-12 | Allow agents to run the full all-files pre-commit suite only through an isolated, evidence-bound wrapper. | Direct agent all-files execution remains prohibited; `run-agent-precommit-all-files.sh` provides the approved clean-linked-worktree, Stage-04-evidenced, changed-path-aware gate, and T-AER-009 independently approved its 29-case fake-hook suite. | Implemented | 3 | Retain | Controlled pre-commit wrapper and Stage 04 task owner | Retain wrapper contract tests and human-reviewed task evidence; observe only Git-visible, non-ignored repository paths. | Run the 29-case fake-hook suite; inspect T-AER-009 PASS/APPROVED evidence and wrapper contract. | High within the exact observation boundary; ignored/outside writes and process/filesystem sandboxing are not claimed. |
| QAF-13 | Define independent CI jobs with explicit permissions and reproducible commands. | Seven workflows define 22 jobs; `ci-quality.yml` defines 15 jobs with read permissions and SHA-pinned actions. | Implemented | 3 | Retain | GitHub workflow and repository-contract owners | Existing CI definitions and local contract validation. | Inspect workflow syntax and run applicable local validators. | High for tracked definitions. |
| QAF-14 | Separate tracked CI definitions from actual run results and required-check enforcement. | Local files define 15 quality jobs. The 2026-07-12 read-only observation found classic `main` protection with 12 required contexts and three local-only contexts; it did not collect recent workflow-run results or mutate enforcement. | Needs Revalidation | 1 | Improve | GitHub governance owner | Retain dated configuration evidence; separately verify recent named runs and synchronize protection only in an approved remote task. | Timestamped remote configuration plus separately collected named run evidence and repository identity. | High for the configuration/run/mutation boundary. |
| QAF-15 | Treat deployment, environment promotion, approvals, and rollback as CD rather than relabeling CI. | No tracked job declares an environment, deploys a target, promotes across environments, or performs automated rollback. | Missing | 0 | Add | Draft Spec 127 deployment/release chain | Keep the separately approval-gated CD design independent from quality CI. | Workflow scan plus later approved promotion/deployment/rollback acceptance evidence. | High. |
| QAF-16 | Record a release iteration with tag, changelog, artifact, approval, and outcome evidence. | A Release profile, checker route, template, and Stage 05 index exist beside a tag-triggered changelog-string check and manual release runbook; `CHANGELOG.md` has only `Unreleased`, and no Release event/deployment record is present. | Partial | 1 | Improve | Draft Spec 127 chain and Stage 05 Release owner | Retain contract readiness and require approved record/asset evidence from a real event; the current check remains readiness only. | Inspect the Release route/template, changelog workflow/runbook, and require an actual event record before claiming execution. | High. |

## Implementation Status Matrix

| Area | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Spec-driven development | Partially Implemented | [SDLC and document-contract audit](./sdlc-document-contracts-implementation.md), [Stage 03 README](../../../03.specs/README.md) | Stage roles, numbering, templates, tasks, broad traceability, and typed direct-parent/transition checks are implemented for the migrated active chain and changed/new documents. Historical lifecycle reconstruction and release execution records remain incomplete. |
| Execution planning | Implemented | [Stage 04 plans README](../../../04.execution/plans/README.md), [audit pack plan](../../../04.execution/plans/2026-07-05-agentic-engineering-implementation-audit-pack.md) | Plans define WBS, verification, risk, and completion criteria. |
| Task evidence | Implemented | [Stage 04 tasks README](../../../04.execution/tasks/README.md), [audit pack task](../../../04.execution/tasks/2026-07-05-agentic-engineering-implementation-audit-pack.md) | Task files record evidence, status, deviation, and validation results. |
| Documentation contracts | Partially Implemented | [frontmatter/template/README audit](./frontmatter-template-readme-implementation.md), [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md), `scripts/validation/check-repo-contracts.sh` | Required headings, lifecycle syntax, links, typed identity/parents, deterministic serialization, freshness, transitions, template instantiation, and README profile/consumer classification are validator-backed. The historical inventory and 37 status-bearing README migration remain advisory. |
| CI quality gates | Implemented | `.github/workflows/ci-quality.yml` | CI defines docs, repo, Compose, hardening, template/security, pre-commit, frontend, coverage, dependency, and workflow-security checks. Only 12 of the 15 locally contracted contexts were remotely required on 2026-07-12, and tracked definitions do not prove recent runs. |
| Local QA orchestration | Implemented | `scripts/validation/run-local-qa-gates.sh`, [scripts README](../../../../scripts/README.md) | Local gate runner lists local, CI/local-tooling, and remote-only responsibilities. |
| Formatting | Partially Implemented | `scripts/hooks/post-tool-validate.sh`, pre-commit workflow, provider notes | Text-file trim/newline and selected shell/frontend formatting/linting exist; global formatting across all languages is not complete. |
| Linting | Partially Implemented | `.github/workflows/ci-quality.yml`, pre-commit, frontend lint, shell syntax checks | Frontend and hook/script surfaces have checks; all repo languages do not have a single universal lint gate. |
| Syntax checks | Implemented | `python -m json.tool` examples in HAFE policy, `bash -n`, repo contracts, CI | JSON/YAML/workflow/script/document syntax checks are represented through scripts and CI. |
| Docker Compose validation | Implemented | `scripts/validation/validate-docker-compose.sh`, `.github/workflows/ci-quality.yml`, [infra README](../../../../infra/README.md) | Default and all-profile validation are in CI; local validation script exists. |
| Infrastructure hardening | Implemented | `scripts/hardening/check-all-hardening.sh`, `.github/workflows/ci-quality.yml` | Hardening baseline is a CI gate and local script. |
| Security quality | Partially Implemented | `.github/workflows/ci-quality.yml`, [approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md), `.github/SECURITY.md` | Workflow security and secret boundaries exist; full SSDF/SLSA automation is partial. |
| CD / promotion / deployment | Not Implemented | `.github/workflows/*.yml`, [release runbook](../../../05.operations/runbooks/00-workspace/release-management.md) | No tracked environment, promotion, deployment, release asset, or automated rollback job exists; the 2026-07-12 remote environment count was also `0`. |

## Findings

- SDLC structure is strong: specs, plans, tasks, operations, references,
  templates, and validators form a coherent lifecycle. Semantic identity,
  parent, transition, and freshness checks are implemented for the migrated
  active chain and changed/new documents; historical corpus reconstruction
  remains advisory. README profile classification is implemented but corpus
  adoption is partial; actual Release event evidence remains missing.
- CI implementation is strong for quality gates. CD, environment promotion,
  deployment records, release assets, and automated rollback are missing and
  must not be inferred from green builds or tag-string validation.
- QA coverage is strong for documentation, Compose, infrastructure hardening,
  frontend quality, workflow security, and repository contracts.
- Formatting/linting coverage is partial because not every language or artifact
  family has a uniform automated style gate.
- Security coverage is meaningful but should be described as repository
  security governance and workflow hardening, not full SSDF/SLSA maturity.

## Gap / Follow-up

| Gap | Status | Follow-up Direction |
| --- | --- | --- |
| Universal formatting/linting coverage | Partially Implemented | Add a scoped formatting/linting inventory before introducing new gates. |
| Typed document identity, parents, lifecycle, and README profiles | Partially Implemented | Retain the implemented registry/checker/contract foundation and use the [frontmatter/template/README audit](./frontmatter-template-readme-implementation.md) to bound later corpus migration. |
| Actual Release record | Not Implemented | Keep the implemented Release profile/template/index, changelog communication, and release runbook distinct; create a record only from an actual event. |
| Agent-output eval as QA | Fixture Pack Implemented / Runner Partial | Use [agent-output eval fixtures](../../data/governance/agent-output-eval-fixtures.md) for recurring docs, provider, and infra tasks; executable QA gating remains future work. |
| CI/CD release/deploy automation | Not Implemented / Out of Scope | Route deployment/release engineering through the separately approval-gated draft Spec 127 chain; keep it separate from validation CI. |
| Security maturity framework mapping | Implemented / Tooling Partial | SSDF/SLSA/OpenSSF Scorecard mapping exists in [security framework maturity coverage](./security-framework-maturity.md); SBOM, provenance, attestation, and vulnerability gates remain future work. |

## Automation Impact

Quality automation should prioritize inventory-driven expansion: identify
artifact families, existing checks, gaps, local command availability, and CI
runtime cost before adding new gates.

## Source Rules

- Use repository scripts and CI workflow for current implementation claims.
- Use external quality/security standards as criteria, not as adopted policy.
- Exact GitHub workflow-syntax and secure-use URLs plus pre-commit were
  re-opened on 2026-07-19; no stale claim was confirmed. The tracked 15-job
  quality workflow is local source truth, while the 2026-07-12 remote
  12-context observation remains dated and unverified.
- Do not record raw logs or secret values as QA evidence.

## Sources

- [Spec-driven SDLC research](../../research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md) - SDLC criteria.
- [Quality CI formatting research](../../research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md) - QA/CI/formatting criteria.
- [Docker Compose infrastructure research](../../research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md) - Compose/infrastructure validation criteria.
- [Security governance research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md) - security criteria.
- [Stage 03 README](../../../03.specs/README.md) - spec stage contract.
- [Stage 04 plans README](../../../04.execution/plans/README.md) - plan stage contract.
- [Stage 04 tasks README](../../../04.execution/tasks/README.md) - task evidence contract.
- [scripts README](../../../../scripts/README.md) - local validation and QA scripts.
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - remote CI/CD gates.
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) - external CI syntax criteria.
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) - external workflow security criteria.
- [pre-commit](https://pre-commit.com/) - external pre-commit criteria.
- [EditorConfig](https://editorconfig.org/) - external formatting convention criteria.
- [Prettier CLI](https://prettier.io/docs/cli) - external formatting/check criteria.
- [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) - secure development framework criteria.
- [SLSA](https://slsa.dev/) - supply-chain integrity framework criteria.

## Maintenance

- **Owner**: QA Engineer / Documentation Specialist.
- **Review Cadence**: Review after CI workflow, validation script, template,
  infra hardening, or SDLC stage contract changes.
- **Update Trigger**: Update when new quality gates are added, skipped, removed,
  or moved between local and CI-only responsibility.

## Related Documents

- [Audit pack README](./README.md)
- [Implementation overview](./implementation-overview.md)
- [SDLC and document-contract implementation audit](./sdlc-document-contracts-implementation.md)
- [Frontmatter, template, and README implementation audit](./frontmatter-template-readme-implementation.md)
- [Automation candidates](./automation-candidates.md)
- [Security framework maturity coverage](./security-framework-maturity.md)
- [Workspace rules/environment audit](./workspace-rules-environment-implementation.md)
