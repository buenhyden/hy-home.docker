---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md -->

# Reference: Agentic Engineering Automation Candidates

## Overview

This reference records automation, pipeline, and workflow opportunities
identified while auditing the agentic engineering implementation status.

## Purpose

The purpose is to separate future automation candidates from the current audit
scope. These candidates are not active implementation tasks until a later spec
or plan approves them.

## Repository Role

This document supports backlog shaping and future Stage 03/04 planning. It does
not change scripts, CI, provider hooks, workflows, or runtime behavior.

## Scope

### In Scope

- Pipeline and workflow automation candidates.
- Local/CI validation automation candidates.
- Provider adapter and hook parity automation candidates.
- Agent evaluation and loop automation candidates.
- Docker Compose and infrastructure inventory automation candidates.

### Out of Scope

- Implementing any listed automation.
- Changing `.github/workflows/**`, `scripts/**`, `.claude/**`, `.codex/**`,
  `.agents/**`, `infra/**`, or Docker Compose files.
- Remote job dispatch, paid work, credential changes, or deployment actions.

## Definitions / Facts

- **Automation candidate** means a scoped improvement idea that needs a future
  active-stage spec/plan before implementation.
- **Pipeline** means local or remote ordered validation, generation, or review
  flow.
- **Workflow** means a repeatable human/agent process, with or without
  executable automation.

## Assessment Method

The audit compared the automation research reference, scripts inventory, CI
quality workflow, provider hook surfaces, generated LLM Wiki loop, HAFE docs,
and audit gaps in the overview, harness, loop, quality, Compose, and security
reports. Tracked automation is classified as executable local, CI-defined,
remote-only, advisory, or missing; the presence of a script or workflow is not
treated as execution evidence.

## Criterion Matrix

| Criterion ID | External criterion | Workspace evidence | Status | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| AUT-01 | Orchestrate locally safe, deterministic validation without duplicating every CI responsibility. | The local runner executes 12 script-backed steps, supports an 8-step harness subset, and lists CI/remote-only work separately. | Implemented | 3 | Retain | Local QA runner owner | Existing orchestration; preserve one runner rather than adding wrappers. | Inspect `run_step` calls and `--list` output. | High. |
| AUT-02 | Recommend change-scoped QA gates without presenting recommendations as executed results. | The changed-path recommender prints deduplicated advice locally and to GitHub Step Summary; it executes no gate. | Implemented | 3 | Retain | QA recommendation script and CI summary step | Existing advisory automation. | Run with explicit paths and confirm output contains no gate execution. | High. |
| AUT-03 | Regenerate provider projections and fail on tracked drift without asserting runtime acceptance. | Provider sync generates/checks Codex and `.agents` projections and reports no drift; semantic/native compatibility remains separate. | Implemented | 3 | Retain | Stage 00 catalog and provider sync | Existing deterministic sync/check. | `bash scripts/operations/sync-provider-surfaces.sh --check`. | High. |
| AUT-04 | Generate tracked reference inventories with canonical write/check modes. | Wiki, Compose coverage, version provenance, hook parity, security readiness, and audit matrix generators have freshness checks. | Implemented | 3 | Retain | Individual generator owners and repo contracts | Existing generated-data automation; generated outputs are not hand-edited. | Run each applicable generator `--check` and repo contracts. | High. |
| AUT-05 | Keep agent-output fixtures reproducible while separating fixture freshness from semantic quality. | Three fixtures and a CI freshness gate exist; arbitrary-output scoring remains advisory and no model call occurs. | Partial | 3 | Improve | Eval runner owner and future eval spec | Retain freshness; semantic thresholds require separate approval. | `bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures`. | High. |
| AUT-06 | Route findings to one canonical stage before automating remediation. | Documentation protocol, gap tables, and a local advisory routing script exist. | Implemented | 2 | Retain | Stage 00 documentation protocol | Existing advisory routing; never auto-create or mutate owner artifacts. | Run routing script on representative text/path and review destination. | High. |
| AUT-07 | Generate a complete criterion-level audit matrix from every canonical criterion report. | Task 6 updates both audit scripts to require eleven criterion reports and validate/emit the complete 161-row set. | Implemented | 3 | Retain | Audit generator and coverage report owners | Existing canonical write/check modes after Task 6 consolidation. | Run generator write/check and coverage `--check`; confirm 11 reports / 161 unique rows. | High. |
| AUT-08 | Produce security readiness signals without running scanners or claiming security outcomes. | The readiness generator maps tracked controls and gaps; its output explicitly excludes scan/SBOM/signing/attestation execution. | Implemented | 3 | Retain | Security readiness generator owner | Existing advisory snapshot and freshness gate. | `bash scripts/validation/generate-security-automation-readiness.sh --check`. | High. |
| AUT-09 | Run agent all-files pre-commit only through an isolated, Stage-04-evidenced, changed-path-aware wrapper. | Direct execution remains prohibited and the controlled wrapper is absent until Task 9. | Missing | 0 | Add | Task 9 QA wrapper implementation | Wrapper/tests will be new automation; Task 6 performs no direct pre-commit. | Require wrapper contract tests and independent review before changing status. | High. |
| AUT-10 | Automate CD promotion/deployment only with environments, approvals, evidence, and rollback. | No tracked workflow deploys/promotes a target or performs rollback. | Missing | 0 | Add | Task 11 deployment/release engineering spec/plan | Future CD automation is independent from CI quality gates. | Require approved environment/promotion/deployment/rollback design and execution evidence. | High. |
| AUT-11 | Distinguish tracked automation definitions from remote enforcement and current run state. | Workflow/config definitions exist; Task 6 did not query current runs, required checks, branch protection, or CODEOWNERS enforcement. | Needs Revalidation | 1 | Improve | GitHub governance owner | Separately approved read-only remote verification, not a local inference. | Timestamped remote query with repository identity and named check contexts. | High for uncertainty boundary. |

## Implementation Status Matrix

| Automation Area | Current Status | Evidence | Candidate |
| --- | --- | --- | --- |
| Local validation orchestration | Implemented | [scripts README](../../../../scripts/README.md), `scripts/validation/run-local-qa-gates.sh`, `scripts/validation/recommend-qa-gates.sh`, `.github/workflows/ci-quality.yml` | Changed-path gate recommendations are available locally and published to GitHub Step Summary in CI. |
| Repository contracts | Implemented | `scripts/validation/check-repo-contracts.sh`, `scripts/validation/report-audit-pack-coverage.sh` | Audit-pack implementation-status coverage output is now available locally and checked by repo contracts. |
| Provider surface sync | Implemented | `scripts/operations/sync-provider-surfaces.sh`, `scripts/validation/check-repo-contracts.sh`, [Provider semantic parity validator spec](../../../03.specs/107-provider-semantic-parity-validator/spec.md) | Semantic role-scope parity is now enforced for Stage 00 catalog scope, Claude adapters, Codex TOML adapters, Gemini pointer adapters, and the subagent protocol. Future work can add deeper free-text clause comparison if needed. |
| Provider hooks | Implemented | `.claude/hooks/`, `.codex/hooks.json`, [Gemini provider notes](../../../00.agent-governance/providers/gemini.md), [provider hook parity matrix](../../data/governance/provider-hook-parity-matrix.md) | Claude/Codex hook parity and Gemini behavioral reminders are generated and freshness-checked locally. |
| LLM Wiki freshness | Implemented | `scripts/knowledge/generate-llm-wiki-index.sh`, `scripts/knowledge/generate-llm-wiki-coverage.sh`, `docs/90.references/llm-wiki/llm-wiki-index.md`, [LLM Wiki coverage snapshot](../../data/knowledge/llm-wiki-stage-category-coverage.md) | Safe tracked-source index freshness and source-bucket/category coverage are generated and checked locally. |
| Compose validation | Implemented | `scripts/validation/validate-docker-compose.sh`, `.github/workflows/ci-quality.yml`, [Compose profile coverage reference](../../data/docker/compose-profile-service-coverage.md), `scripts/operations/generate-compose-profile-service-coverage.sh` | Profile-to-service coverage snapshot is now generated and freshness-checked locally; future work can publish grouped summaries into CI or audit reports if useful. |
| Tech-stack version sync | Implemented | `scripts/operations/sync-tech-stack-versions.sh`, `infra/tech-stack.versions.json`, [tech-stack version provenance](../../data/docker/tech-stack-version-provenance.md) | Drift severity and source provenance are generated and freshness-checked locally. |
| Agent-output eval | Fixture CI Gate Implemented / Scoring Advisory | [loop research](../../research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md), Stage 04 evidence patterns, [agent-output eval fixtures](../../data/governance/agent-output-eval-fixtures.md), `scripts/validation/run-agent-output-eval-fixtures.sh`, `.github/workflows/ci-quality.yml` | Small docs/provider/infra fixtures, a local advisory runner, and a CI fixture catalog freshness gate exist; semantic scoring for arbitrary agent outputs remains advisory and future-gated. |
| Gap routing | Implemented | Stage 04 task evidence, audit gap tables, [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md), [gap routing reference](../../data/governance/gap-to-stage-routing.md), `scripts/validation/recommend-gap-routing.sh` | Gap-to-stage suggestions are now available locally for text and path inputs; future work can decide whether to publish routing summaries into audit reports. |
| Audit implementation matrix | Implemented | [audit implementation matrix](../../data/governance/audit-implementation-matrix.md), `scripts/validation/generate-audit-implementation-matrix.sh`, `scripts/validation/check-repo-contracts.sh` | Audit report coverage, overview categories, automation candidate closure, generated evidence surfaces, and residual gap signals are generated and freshness-checked locally. |
| Security maturity | Mapped / Readiness Snapshot Implemented / Partially Implemented | `.github/workflows/ci-quality.yml`, [security research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md), [security framework maturity coverage](./security-framework-maturity.md), [security automation readiness](../../data/security/security-automation-readiness.md) | SSDF/SLSA/OpenSSF Scorecard coverage and repo-local readiness are now mapped; a scoped Storybook Next.js `npm audit` gate exists; SBOM generation, provenance/attestation, Scorecard, and broader ecosystem/container vulnerability scanning remain future work. |

## Findings

- The repository already automates many structural checks: contracts, docs
  traceability, Compose validation, hardening, pre-commit, frontend quality,
  generated index freshness, audit-pack coverage reporting, and workflow
  security scanning.
- A local advisory changed-path QA recommendation report exists and is now
  published into GitHub Step Summary from the CI quality workflow.
- Provider semantic role-scope parity, provider hook parity, LLM Wiki
  source-bucket/category coverage, Compose profile coverage inventory,
  tech-stack version provenance, agent-output eval fixtures/local runner, and
  security framework maturity mapping, security automation readiness, audit
  implementation matrix snapshots, the eval fixture freshness CI gate, and a
  scoped Storybook Next.js dependency vulnerability audit gate are now covered.
  The remaining highest-value gaps are required semantic eval scoring, SBOM
  generation, provenance/attestation automation, Scorecard, and broader
  ecosystem/container vulnerability scanning.
- Gemini-specific automation should remain reminder/checklist based until
  native hook/subagent support is confirmed by official sources.

## Gap / Follow-up

| Candidate ID | Candidate | Suggested Future Stage |
| --- | --- | --- |
| AEA-AUTO-001 | PR/CI summary integration for the changed-path QA-gate recommendation report | Implemented by [QA gate recommendation CI summary spec](../../../03.specs/111-qa-gate-recommendation-ci-summary/spec.md), [task evidence](../../../04.execution/tasks/2026-07-05-qa-gate-recommendation-ci-summary.md), `.github/workflows/ci-quality.yml`, and `scripts/validation/check-repo-contracts.sh`. |
| AEA-AUTO-002 | Provider semantic role-scope parity validator | Implemented by [Provider semantic parity validator spec](../../../03.specs/107-provider-semantic-parity-validator/spec.md) and [task evidence](../../../04.execution/tasks/2026-07-05-provider-semantic-parity-validator.md); deeper free-text clause comparison remains optional future work. |
| AEA-AUTO-003 | Agent-output eval fixture pack | Implemented by [Agent output eval fixtures spec](../../../03.specs/110-agent-output-eval-fixtures/spec.md), [task evidence](../../../04.execution/tasks/2026-07-05-agent-output-eval-fixtures.md), and [fixture reference](../../data/governance/agent-output-eval-fixtures.md). |
| AEA-AUTO-004 | Gap-to-stage routing generator for the Stage 00 manual routing contract | Implemented by [Gap routing recommendation spec](../../../03.specs/109-gap-routing-recommendation/spec.md), [task evidence](../../../04.execution/tasks/2026-07-05-gap-routing-recommendation.md), [gap routing reference](../../data/governance/gap-to-stage-routing.md), and `scripts/validation/recommend-gap-routing.sh`. |
| AEA-AUTO-005 | Compose profile/service coverage snapshot | Implemented by [Compose profile service coverage snapshot spec](../../../03.specs/108-compose-profile-service-coverage-snapshot/spec.md), [task evidence](../../../04.execution/tasks/2026-07-05-compose-profile-service-coverage-snapshot.md), [generated Docker data reference](../../data/docker/compose-profile-service-coverage.md), and `scripts/operations/generate-compose-profile-service-coverage.sh`. |
| AEA-AUTO-006 | SSDF/SLSA maturity coverage matrix | Implemented by [Security framework maturity coverage](./security-framework-maturity.md); follow-up security tooling remains future Stage 03/04 work. |
| AEA-AUTO-007 | Audit-pack implementation-status coverage output | Implemented by [Audit pack coverage report spec](../../../03.specs/112-audit-pack-coverage-report/spec.md), [task evidence](../../../04.execution/tasks/2026-07-05-audit-pack-coverage-report.md), `scripts/validation/report-audit-pack-coverage.sh`, and repo-contract `--check` coverage. |
| AEA-AUTO-008 | LLM Wiki stage/category coverage report | Implemented by [LLM Wiki stage category coverage spec](../../../03.specs/113-llm-wiki-stage-category-coverage/spec.md), [task evidence](../../../04.execution/tasks/2026-07-06-llm-wiki-stage-category-coverage.md), [generated coverage snapshot](../../data/knowledge/llm-wiki-stage-category-coverage.md), `scripts/knowledge/generate-llm-wiki-coverage.sh`, and repo-contract freshness coverage. |
| AEA-AUTO-009 | Tech-stack version drift severity and source provenance summary | Implemented by [Tech-stack version provenance spec](../../../03.specs/114-tech-stack-version-provenance/spec.md), [task evidence](../../../04.execution/tasks/2026-07-06-tech-stack-version-provenance.md), [generated provenance snapshot](../../data/docker/tech-stack-version-provenance.md), `scripts/operations/generate-tech-stack-version-provenance.sh`, and repo-contract freshness coverage. |
| AEA-AUTO-010 | Provider hook parity matrix and Gemini behavioral reminder checklist | Implemented by [Provider hook parity matrix spec](../../../03.specs/115-provider-hook-parity-matrix/spec.md), [task evidence](../../../04.execution/tasks/2026-07-06-provider-hook-parity-matrix.md), [generated hook matrix](../../data/governance/provider-hook-parity-matrix.md), `scripts/validation/report-provider-hook-parity.sh`, and repo-contract freshness coverage. |
| AEA-AUTO-011 | Local advisory agent-output eval runner and fixture freshness CI gate | Implemented by [Agent output eval runner spec](../../../03.specs/116-agent-output-eval-runner/spec.md), [Agent output eval CI gate spec](../../../03.specs/120-agent-output-eval-ci-gate/spec.md), [runner task evidence](../../../04.execution/tasks/2026-07-06-agent-output-eval-runner.md), [CI gate task evidence](../../../04.execution/tasks/2026-07-06-agent-output-eval-ci-gate.md), [fixture reference](../../data/governance/agent-output-eval-fixtures.md), `scripts/validation/run-agent-output-eval-fixtures.sh`, repo-contract fixture catalog checks, and `.github/workflows/ci-quality.yml`; required semantic scoring remains optional future work. |
| AEA-AUTO-012 | Security automation readiness snapshot and scoped dependency vulnerability gate | Readiness snapshot implemented by [Security automation readiness snapshot spec](../../../03.specs/117-security-automation-readiness-snapshot/spec.md), [task evidence](../../../04.execution/tasks/2026-07-06-security-automation-readiness-snapshot.md), [generated security readiness data](../../data/security/security-automation-readiness.md), `scripts/validation/generate-security-automation-readiness.sh`, and repo-contract freshness coverage; scoped npm vulnerability gate implemented by [Dependency vulnerability audit gate spec](../../../03.specs/121-dependency-vulnerability-audit-gate/spec.md), [task evidence](../../../04.execution/tasks/2026-07-06-dependency-vulnerability-audit-gate.md), and `.github/workflows/ci-quality.yml`; SBOM generation, signing/provenance attestation, Scorecard automation, and broader ecosystem/container vulnerability scanning remain future work. |
| AEA-AUTO-013 | Audit implementation matrix snapshot | Implemented by [Audit implementation matrix snapshot spec](../../../03.specs/118-audit-implementation-matrix-snapshot/spec.md), [task evidence](../../../04.execution/tasks/2026-07-06-audit-implementation-matrix-snapshot.md), [generated audit implementation matrix](../../data/governance/audit-implementation-matrix.md), `scripts/validation/generate-audit-implementation-matrix.sh`, and repo-contract freshness coverage; required semantic eval scoring and security tooling remain future work. |

## Automation Impact

These implemented candidates reduce manual audit maintenance and make loop
engineering more measurable. Remaining residual gaps should be implemented only
after separate approval because they touch provider surfaces, model eval gates,
required semantic scoring, or security classification.

## Source Rules

- Automation candidates must be framed as future work, not instructions to run
  or mutate state.
- Each candidate must cite the current manual or partial implementation surface
  that it would improve.

## Sources

- [Automation research](../../research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md) - research criteria.
- [scripts README](../../../../scripts/README.md) - current automation inventory.
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - current remote pipeline.
- [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) - provider automation boundary.
- [Loop implementation audit](./loop-engineering-implementation.md) - loop gaps.
- [Harness implementation audit](./harness-engineering-implementation.md) - harness gaps.
- [Docker Compose infrastructure research](../../research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md) - Compose/infrastructure criteria.
- [Security governance research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md) - security criteria.

## Maintenance

- **Owner**: Agentic Workflow Specialist / QA Engineer.
- **Review Cadence**: Review after new scripts, CI jobs, provider adapters, or
  validation gates are introduced.
- **Update Trigger**: Update when an automation candidate is implemented,
  rejected, superseded, or moved into an active plan.

## Related Documents

- [Audit pack README](./README.md)
- [Implementation overview](./implementation-overview.md)
- [Workspace rules/environment audit](./workspace-rules-environment-implementation.md)
- [SDLC quality implementation audit](./sdlc-quality-formatting-implementation.md)
