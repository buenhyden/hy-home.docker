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
and audit gaps in the overview, harness, and loop reports.

## Implementation Status Matrix

| Automation Area | Current Status | Evidence | Candidate |
| --- | --- | --- | --- |
| Local validation orchestration | Implemented | [scripts README](../../../../scripts/README.md), `scripts/validation/run-local-qa-gates.sh`, `scripts/validation/recommend-qa-gates.sh`, `.github/workflows/ci-quality.yml` | Changed-path gate recommendations are available locally and published to GitHub Step Summary in CI. |
| Repository contracts | Implemented | `scripts/validation/check-repo-contracts.sh`, `scripts/validation/report-audit-pack-coverage.sh` | Audit-pack implementation-status coverage output is now available locally and checked by repo contracts. |
| Provider surface sync | Implemented | `scripts/operations/sync-provider-surfaces.sh`, `scripts/validation/check-repo-contracts.sh`, [Provider semantic parity validator spec](../../../03.specs/107-provider-semantic-parity-validator/spec.md) | Semantic role-scope parity is now enforced for Stage 00 catalog scope, Claude adapters, Codex TOML adapters, Gemini pointer adapters, and the subagent protocol. Future work can add deeper free-text clause comparison if needed. |
| Provider hooks | Partially Implemented | `.claude/hooks/`, `.codex/hooks.json`, [Gemini provider notes](../../../00.agent-governance/providers/gemini.md) | Generate hook parity matrix and Gemini behavioral reminder checklist. |
| LLM Wiki freshness | Implemented | `scripts/knowledge/generate-llm-wiki-index.sh`, `docs/90.references/llm-wiki/llm-wiki-index.md` | Add report grouping by stage/category for audit consumers. |
| Compose validation | Implemented | `scripts/validation/validate-docker-compose.sh`, `.github/workflows/ci-quality.yml`, [Compose profile coverage reference](../../data/docker/compose-profile-service-coverage.md), `scripts/operations/generate-compose-profile-service-coverage.sh` | Profile-to-service coverage snapshot is now generated and freshness-checked locally; future work can publish grouped summaries into CI or audit reports if useful. |
| Tech-stack version sync | Implemented | `scripts/operations/sync-tech-stack-versions.sh`, `infra/tech-stack.versions.json` | Add drift severity and source provenance summary. |
| Agent-output eval | Fixture Pack Implemented / Runner Partial | [loop research](../../research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md), Stage 04 evidence patterns, [agent-output eval fixtures](../../data/governance/agent-output-eval-fixtures.md) | Small docs/provider/infra fixtures now exist; executable runner or CI gate remains future work. |
| Gap routing | Implemented | Stage 04 task evidence, audit gap tables, [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md), [gap routing reference](../../data/governance/gap-to-stage-routing.md), `scripts/validation/recommend-gap-routing.sh` | Gap-to-stage suggestions are now available locally for text and path inputs; future work can decide whether to publish routing summaries into audit reports. |
| Security maturity | Mapped / Partially Implemented | `.github/workflows/ci-quality.yml`, [security research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md), [security framework maturity coverage](./security-framework-maturity.md) | SSDF/SLSA/OpenSSF Scorecard coverage is now mapped; tooling adoption, SBOM, provenance, and vulnerability gates remain future work. |

## Findings

- The repository already automates many structural checks: contracts, docs
  traceability, Compose validation, hardening, pre-commit, frontend quality,
  generated index freshness, audit-pack coverage reporting, and workflow
  security scanning.
- A local advisory changed-path QA recommendation report exists and is now
  published into GitHub Step Summary from the CI quality workflow.
- Provider semantic role-scope parity, Compose profile coverage inventory,
  agent-output eval fixtures, and security framework maturity mapping are now
  covered. The remaining highest-value gaps are executable eval runner
  adoption, vulnerability gating, SBOM, and provenance/attestation automation.
- Gemini-specific automation should remain reminder/checklist based until
  native hook/subagent support is confirmed by official sources.

## Gap / Follow-up

| Candidate ID | Candidate | Suggested Future Stage |
| --- | --- | --- |
| AEA-AUTO-001 | PR/CI summary integration for the changed-path QA-gate recommendation report | Implemented by [QA gate recommendation CI summary spec](../../../03.specs/111-qa-gate-recommendation-ci-summary/spec.md), [task evidence](../../../04.execution/tasks/2026-07-05-qa-gate-recommendation-ci-summary.md), `.github/workflows/ci-quality.yml`, and `scripts/validation/check-repo-contracts.sh`. |
| AEA-AUTO-002 | Provider semantic role-scope parity validator | Implemented by [Provider semantic parity validator spec](../../../03.specs/107-provider-semantic-parity-validator/spec.md) and [task evidence](../../../04.execution/tasks/2026-07-05-provider-semantic-parity-validator.md); deeper free-text clause comparison remains optional future work. |
| AEA-AUTO-003 | Agent-output eval fixture pack | Implemented by [Agent output eval fixtures spec](../../../03.specs/110-agent-output-eval-fixtures/spec.md), [task evidence](../../../04.execution/tasks/2026-07-05-agent-output-eval-fixtures.md), and [fixture reference](../../data/governance/agent-output-eval-fixtures.md); executable runner or CI gate remains optional future work. |
| AEA-AUTO-004 | Gap-to-stage routing generator for the Stage 00 manual routing contract | Implemented by [Gap routing recommendation spec](../../../03.specs/109-gap-routing-recommendation/spec.md), [task evidence](../../../04.execution/tasks/2026-07-05-gap-routing-recommendation.md), [gap routing reference](../../data/governance/gap-to-stage-routing.md), and `scripts/validation/recommend-gap-routing.sh`. |
| AEA-AUTO-005 | Compose profile/service coverage snapshot | Implemented by [Compose profile service coverage snapshot spec](../../../03.specs/108-compose-profile-service-coverage-snapshot/spec.md), [task evidence](../../../04.execution/tasks/2026-07-05-compose-profile-service-coverage-snapshot.md), [generated Docker data reference](../../data/docker/compose-profile-service-coverage.md), and `scripts/operations/generate-compose-profile-service-coverage.sh`. |
| AEA-AUTO-006 | SSDF/SLSA maturity coverage matrix | Implemented by [Security framework maturity coverage](./security-framework-maturity.md); follow-up security tooling remains future Stage 03/04 work. |
| AEA-AUTO-007 | Audit-pack implementation-status coverage output | Implemented by [Audit pack coverage report spec](../../../03.specs/112-audit-pack-coverage-report/spec.md), [task evidence](../../../04.execution/tasks/2026-07-05-audit-pack-coverage-report.md), `scripts/validation/report-audit-pack-coverage.sh`, and repo-contract `--check` coverage. |

## Automation Impact

These candidates would reduce manual audit maintenance and make loop
engineering more measurable. They should be implemented only after separate
approval because they touch scripts, CI, provider surfaces, or security
classification.

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
