---
status: active
artifact_id: audit:agentic-engineering-implementation:automation-candidates
artifact_type: audit
parent_ids: [audit:agentic-engineering-implementation:overview]
supersedes: [audit:agentic-engineering-implementation-2026-07-07:automation-candidates]
reviewed_at: 2026-07-12
review_cycle: per-remediation-task
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

### Remote Evidence Boundary as of 2026-07-12

| Evidence class | Evidence | Limitation |
| --- | --- | --- |
| Tracked definitions | The local CI/protection contract names 15 contexts. | A tracked name proves neither execution nor remote enforcement. |
| Observed remote configuration | Classic `main` protection is enabled with 12 required contexts; repository rulesets are `0`; environments are `0`. | `docs-implementation-alignment`, `agent-output-eval-fixture-gate`, and `dependency-vulnerability-audit` are absent remotely. |
| Recent execution | No recent named check-run or deployment-run evidence was collected. | Remote configuration must not be reported as a successful run. |
| Enforcement mutation | No branch protection, ruleset, environment, workflow, or repository setting was changed. | Later synchronization requires separate approval, exact run evidence, rollback, and read-back. |

## Criterion Matrix

| Criterion ID | External criterion | Workspace evidence | Status | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| AUT-01 | Orchestrate locally safe, deterministic validation without duplicating every CI responsibility. | The local runner executes 20 script-backed steps, supports an 18-step harness subset, and lists CI/remote-only work separately. The controlled all-files wrapper is an explicit final-gate exception, not a duplicate default runner. | Implemented | 3 | Retain | Local QA runner owner | Existing orchestration; preserve one runner and the bounded wrapper exception. | Inspect direct and nested `run_step` calls and `--list` output. | High. |
| AUT-02 | Recommend change-scoped QA gates without presenting recommendations as executed results. | The changed-path recommender prints deduplicated advice locally and to GitHub Step Summary; it executes no gate. | Implemented | 3 | Retain | QA recommendation script and CI summary step | Existing advisory automation. | Run with explicit paths and confirm output contains no gate execution. | High. |
| AUT-03 | Regenerate provider projections and fail on tracked drift without asserting runtime acceptance. | The Stage 00-only renderer generates/checks 14 Claude, Codex, Gemini, and shared role adapters, 22 Claude/shared function skills, provider settings/hooks, and indexes; sync reports three providers and zero drift. Live acceptance remains separate. | Implemented | 3 | Retain | Stage 00 catalog and provider renderer | Existing deterministic write/check modes. | `bash scripts/operations/sync-provider-surfaces.sh --check`. | High. |
| AUT-04 | Generate tracked reference inventories with canonical write/check modes. | Wiki, Compose coverage, version provenance, hook parity, security readiness, and audit matrix generators have freshness checks. | Implemented | 3 | Retain | Individual generator owners and repo contracts | Existing generated-data automation; generated outputs are not hand-edited. | Run each applicable generator `--check` and repo contracts. | High. |
| AUT-05 | Keep agent-output fixtures reproducible while separating repository semantics from live model quality. | Eight exact fixtures, ten synthetic regressions, bounded value-free input handling, calibrated deterministic scorers, explicit thresholds, local routing, and exact CI markers are implemented. No network model call or live provider-quality claim occurs. | Implemented | 4 | Retain | `eval-engineer` and QA owner | Retain fixture/regression calibration and design live comparative evaluation only under separate approval. | `bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions` requires exact `8/8` and `10/10` markers. | High. |
| AUT-06 | Route findings to one canonical stage before automating remediation. | Documentation protocol, gap tables, and a local advisory routing script exist. | Implemented | 2 | Retain | Stage 00 documentation protocol | Existing advisory routing; never auto-create or mutate owner artifacts. | Run routing script on representative text/path and review destination. | High. |
| AUT-07 | Generate a complete criterion-level audit matrix from every canonical criterion report. | Both audit scripts import one shared manifest/parser that enforces the exact eleven reports, 161 exact IDs, ten non-empty fields, schema/vocabularies, per-report/prefix/total counts, and uniqueness; seven temp-copy fixtures cover valid and negative cases. | Implemented | 3 | Retain | Audit criterion contract, generator, and coverage owners | Shared deterministic parser plus canonical write/check modes; structural defects fail before generator write/freshness comparison. | Run the fixture tests, generator write/check, and coverage `--check`; confirm 11 reports / 161 unique rows and negative nonzero exits. | High. |
| AUT-08 | Produce security readiness signals without running scanners or claiming security outcomes. | The readiness generator maps tracked controls and gaps; its output explicitly excludes scan/SBOM/signing/attestation execution. | Implemented | 3 | Retain | Security readiness generator owner | Existing advisory snapshot and freshness gate. | `bash scripts/validation/generate-security-automation-readiness.sh --check`. | High. |
| AUT-09 | Run agent all-files pre-commit only through an isolated, Stage-04-evidenced, changed-path-aware wrapper. | Direct execution remains prohibited; `run-agent-precommit-all-files.sh` enforces the clean linked-worktree, task-path, allow-prefix, snapshot, exit, and evidence boundaries approved in T-AER-009, whose 29-case fake-hook suite passed independent review. | Implemented | 3 | Retain | Controlled pre-commit wrapper and Stage 04 task owner | Retain fake-hook contract coverage and require human-reviewed task evidence for each real invocation. | Run the 29-case fake-hook suite and inspect T-AER-009 PASS/APPROVED evidence. | High for Git-visible, non-ignored repository paths; ignored/outside writes and sandboxing are not observed. |
| AUT-10 | Automate CD promotion/deployment only with environments, approvals, evidence, and rollback. | No tracked workflow deploys/promotes a target or performs rollback. | Missing | 0 | Add | Draft Spec 127 deployment/release chain | The separately approval-gated CD design remains independent from CI quality gates. | Require approved environment/promotion/deployment/rollback execution evidence. | High. |
| AUT-11 | Distinguish tracked automation definitions from remote enforcement and current run state. | Workflow/config definitions exist. The 2026-07-12 read-only observation found classic `main` protection with 12 required contexts versus 15 local names, zero rulesets, and zero environments; it did not collect recent run results or mutate enforcement. | Needs Revalidation | 1 | Improve | GitHub governance owner | Retain the dated remote configuration record; collect recent named run evidence and approve a rollback-bound remote task before synchronization. | Timestamped configuration query plus separately collected run evidence, repository identity, exact context comparison, and post-mutation read-back when authorized. | High for the definition/configuration/run/mutation boundary. |

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
| Security maturity | Mapped / Readiness Snapshot Implemented / Partially Implemented | `.github/workflows/ci-quality.yml`, [security research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md), [security framework maturity coverage](./security-framework-maturity.md), [security automation readiness](../../data/security/security-automation-readiness.md) | SSDF/SLSA/OpenSSF Scorecard coverage and repo-local readiness are mapped; the scoped Storybook Next.js `npm audit` gate satisfies `SEC-AUTO-008`, while broad dependency SCA and container/image scanning remain separate gaps. |
| Remote required-check configuration | Partial / Dated Observation | [main protection record](../../../../.github/rulesets/main-protection.md), [Spec 129](../../../03.specs/129-document-contract-canonicalization/spec.md) | Classic protection and 12 contexts were observed read-only on 2026-07-12, but three local contexts are absent remotely; recent runs and mutation remain separate evidence classes. |

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
- Remote protection is neither wholly unknown nor synchronized: dated
  configuration evidence exists, but three local contexts remain absent and no
  recent-run or enforcement-mutation evidence was produced.

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
| AEA-AUTO-012 | Security automation readiness snapshot and scoped dependency vulnerability gate | Readiness snapshot implemented by [Security automation readiness snapshot spec](../../../03.specs/117-security-automation-readiness-snapshot/spec.md), [task evidence](../../../04.execution/tasks/2026-07-06-security-automation-readiness-snapshot.md), [generated security readiness data](../../data/security/security-automation-readiness.md), `scripts/validation/generate-security-automation-readiness.sh`, and repo-contract freshness coverage; scoped npm vulnerability gate implemented by [Dependency vulnerability audit gate spec](../../../03.specs/121-dependency-vulnerability-audit-gate/spec.md), [task evidence](../../../04.execution/tasks/2026-07-06-dependency-vulnerability-audit-gate.md), and `.github/workflows/ci-quality.yml`. The scoped gate satisfies only `SEC-AUTO-008`; `SEC-AUTO-012` and `SEC-AUTO-013` remain `Gap` and route to [draft Spec 126](../../../03.specs/126-security-supply-chain-remediation/spec.md), together with SBOM, signing/provenance attestation, and Scorecard automation. |
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
- Keep tracked definitions, observed remote configuration, recent run results,
  and remote mutation/read-back as separate evidence classes.

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
