---
status: active
generated_by: scripts/validation/check-document-metadata.py
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md -->

# Reference: Frontmatter Semantic Inventory

## Overview

This generated advisory reference inventories every tracked target-stage and
governance/template Markdown document except this self-referential output. It records inferred profiles
and metadata findings without printing body content, secret values, or raw logs.

## Purpose

Provide the deterministic pre-migration baseline for Spec 123 Tasks 7 and 8.
Semantic findings are advisory here and do not authorize metadata migration or
changed/new blocking enforcement.

## Repository Role

Stage 00 and Stage 99 own active metadata policy. This Stage 90 snapshot is
generated evidence only; regenerate it with `check-document-metadata.py`.

## Scope

### In Scope

- Tracked Markdown paths, inferred profiles, safe frontmatter parse state, and finding codes
- Identity, parent, lifecycle, freshness, README, generated, governance, template, and archive profiles

### Out of Scope

- Automatic document rewrites or lifecycle changes
- Filesystem modification times as freshness evidence
- Raw document bodies, logs, credentials, or secret values

## Definitions / Facts

- **Tracked records**: 876
- **Records with findings**: 581
- **Frontmatter parser failures**: 0
- **Enforcement state**: advisory-only; repository contracts check syntax, tests, and snapshot freshness only

## Profile Summary

| Profile | Records |
| --- | ---: |
| `adr` | 24 |
| `archive` | 20 |
| `ard` | 24 |
| `audit` | 33 |
| `generated` | 6 |
| `governance` | 109 |
| `guide` | 66 |
| `plan` | 88 |
| `policy` | 64 |
| `prd` | 24 |
| `readme` | 143 |
| `reference` | 30 |
| `runbook` | 61 |
| `spec` | 48 |
| `task` | 114 |
| `template-source` | 22 |

## Finding Summary

| Finding | Count |
| --- | ---: |
| `missing-required-key` | 1998 |
| `replacement-free-supersession` | 12 |
| `stale-active` | 125 |

## Inventory

| Path | Profile | Parse | Status | Artifact ID | Parent Count | Findings | Disposition |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| `docs/00.agent-governance/README.md` | `readme` | valid | — | — | 0 | none | README exception |
| `docs/00.agent-governance/agents/README.md` | `readme` | valid | — | — | 0 | none | README exception |
| `docs/00.agent-governance/agents/agents/ci-cd-engineer.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/code-reviewer.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/doc-writer.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/drift-detector.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/hook-developer.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/iac-reviewer.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/incident-responder.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/infra-implementer.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/qa-engineer.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/rules-engineer.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/security-auditor.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/skill-creator.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/style-enforcer.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/wiki-curator.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/agents/workflow-supervisor.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/adr-writing.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/ci-cd-patterns.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/code-review-dimensions.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/code-reviewer.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/compose-stack-agent.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/container-threat-modeling.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/deployment-pipeline-design.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/docker-compose-patterns.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/e2e-testing.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/execution-plan-agent.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/incident-response.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/infra-cross-validate.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/infra-validate.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/knowledge-map-agent.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/ops-runbook-agent.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/policy-gate-agent.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/requirements-to-design-agent.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/security-audit.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/style-validation.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/task-breakdown-agent.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/test-automator.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/agents/functions/workspace-audit-revalidation.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/harness-implementation-map.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/memory/README.md` | `readme` | valid | — | — | 0 | none | README exception |
| `docs/00.agent-governance/memory/agentic-harness-contract-hardening.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/memory/docker-doc-contract-backlog.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/memory/execution-stage-legacy-debt.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/memory/github-ci-contract-audit.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/memory/governance-memory-usage-contract.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/memory/harness-agent-first-gap-audit.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/memory/progress.md` | `governance` | valid | active | — | 0 | none | governance exception |
| `docs/00.agent-governance/memory/stage-docs-lifecycle-audit.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/memory/template.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/providers/agents-md.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/providers/claude.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/providers/codex.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/providers/gemini.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/agentic.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/approval-boundaries.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/bootstrap.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/documentation-protocol.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/environment-constraints.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/git-workflow.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/github-governance.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.block-absolute-file-link.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.block-direct-main-push.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.block-gha-secrets-in-run.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.block-git-no-verify.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.block-plaintext-secret-compose.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.block-unpinned-gha-action.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.enforce-docs-templates.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.require-logical-commits-before-stop.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.warn-branch-naming.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.warn-conventional-commit.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.warn-docker-infra-stop.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.warn-force-push.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.warn-governance-memory-edit.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.warn-hook-parity-edit.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.warn-korean-in-governance.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.warn-parallel-doc-file.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.warn-post-edit-style-automation.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.warn-pre-commit-manual.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/hooks/hookify.warn-stage-doc-edit.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/jit-markers.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/output-style.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/persona.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/postflight-checklist.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/provider-capability-matrix.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/quality-standards.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/stage-authoring-matrix.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/standards.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/task-checklists.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/rules/workflows.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/agentic.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/architecture.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/backend.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/common.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/docs.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/entry.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/frontend.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/infra.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/meta.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/mobile.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/ops.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/product.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/qa.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/scopes/security.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/00.agent-governance/subagent-protocol.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/01.requirements/001-gateway.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/002-auth.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/003-security.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/004-data.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/005-data-analytics.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/006-messaging.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/007-observability.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/008-workflow.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/009-ai.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/010-tooling.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/011-communication.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/012-laboratory.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/013-ai-open-webui.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/014-auth-optimization-hardening.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/015-security-optimization-hardening.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/016-data-optimization-hardening.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/017-messaging-optimization-hardening.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/018-observability-optimization-hardening.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/019-workflow-optimization-hardening.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/020-ai-optimization-hardening.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/021-tooling-optimization-hardening.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/022-laboratory-optimization-hardening.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/023-standardize-infra-net.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/024-agent-governance-standardization.md` | `prd` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/01.requirements/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/02.architecture/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/02.architecture/decisions/0001-traefik-nginx-hybrid.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0003-vault-as-secrets-manager.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0004-postgresql-ha-patroni.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0006-lgtm-stack-selection.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0008-ollama-openwebui-local-ai.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0009-tooling-services.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0010-communication-services.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0011-laboratory-services.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0015-analytics-engine-selection.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0016-open-webui-implementation.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0017-auth-hardening-runtime-and-fail-closed.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0019-04-data-hardening-and-ha-expansion-strategy.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0026-standardize-infra-net.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md` | `adr` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/decisions/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/02.architecture/requirements/0001-gateway-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0002-auth-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0003-security-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0004-data-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0005-messaging-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0006-observability-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0007-workflow-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0008-ai-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0009-tooling-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0010-communication-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0011-laboratory-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0012-data-analytics-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0013-open-webui-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0014-auth-optimization-hardening-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0018-security-optimization-hardening-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0019-data-optimization-hardening-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0021-observability-optimization-hardening-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0023-ai-optimization-hardening-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0024-tooling-optimization-hardening-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0026-standardize-infra-net.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/0027-agent-governance-canonical-adapter.md` | `ard` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/02.architecture/requirements/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/03.specs/001-gateway/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/001-gateway/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/002-auth/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/002-auth/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/003-security/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/003-security/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/004-data/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/004-data/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/005-data-analytics/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/005-data-analytics/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/006-messaging/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/006-messaging/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/007-observability/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/007-observability/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/008-workflow/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/008-workflow/agent-design.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/008-workflow/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/009-ai/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/009-ai/open-webui.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/009-ai/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/010-tooling/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/010-tooling/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/011-communication/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/011-communication/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/012-laboratory/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/012-laboratory/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/090-workspace-audit-2026-05/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/090-workspace-audit-2026-05/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/091-workspace-doc-consistency-2026-05/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/092-workspace-consistency-2026-05b/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/093-docs-taxonomy-agent-first-migration/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/093-docs-taxonomy-agent-first-migration/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/094-harness-agent-first-engineering/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/094-harness-agent-first-engineering/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/095-infra-secrets-docs-refresh/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/095-infra-secrets-docs-refresh/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/096-llm-wiki-agent-first-completion/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/096-llm-wiki-agent-first-completion/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/097-home-docker-revalidation-deferred-follow-up/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/097-home-docker-revalidation-deferred-follow-up/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/098-standardize-infra-net/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/03.specs/098-standardize-infra-net/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/099-template-system-numbered-sdlc-paths/README.md` | `readme` | valid | completed | — | 0 | none | README exception |
| `docs/03.specs/099-template-system-numbered-sdlc-paths/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/100-template-system-contract-standardization/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/101-template-system-reorganization/README.md` | `readme` | valid | superseded | — | 0 | none | README exception |
| `docs/03.specs/101-template-system-reorganization/spec.md` | `spec` | valid | superseded | — | 0 | missing-required-key, replacement-free-supersession | migration candidate |
| `docs/03.specs/102-workspace-document-contract-audit-pack/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/03.specs/102-workspace-document-contract-audit-pack/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/103-document-restructure-audit-contract-archive/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/03.specs/103-document-restructure-audit-contract-archive/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/104-agentic-research-pack-refresh/README.md` | `readme` | valid | completed | — | 0 | none | README exception |
| `docs/03.specs/104-agentic-research-pack-refresh/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/105-agentic-engineering-implementation-audit-pack/README.md` | `readme` | valid | completed | — | 0 | none | README exception |
| `docs/03.specs/105-agentic-engineering-implementation-audit-pack/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/106-workspace-support-surface-contract/README.md` | `readme` | valid | completed | — | 0 | none | README exception |
| `docs/03.specs/106-workspace-support-surface-contract/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/107-provider-semantic-parity-validator/README.md` | `readme` | valid | completed | — | 0 | none | README exception |
| `docs/03.specs/107-provider-semantic-parity-validator/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/108-compose-profile-service-coverage-snapshot/README.md` | `readme` | valid | completed | — | 0 | none | README exception |
| `docs/03.specs/108-compose-profile-service-coverage-snapshot/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/109-gap-routing-recommendation/README.md` | `readme` | valid | completed | — | 0 | none | README exception |
| `docs/03.specs/109-gap-routing-recommendation/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/110-agent-output-eval-fixtures/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/111-qa-gate-recommendation-ci-summary/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/112-audit-pack-coverage-report/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/113-llm-wiki-stage-category-coverage/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/114-tech-stack-version-provenance/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/115-provider-hook-parity-matrix/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/116-agent-output-eval-runner/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/117-security-automation-readiness-snapshot/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/118-audit-implementation-matrix-snapshot/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/119-sdlc-document-contract-corpus-normalization/README.md` | `readme` | valid | completed | — | 0 | none | README exception |
| `docs/03.specs/119-sdlc-document-contract-corpus-normalization/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/120-agent-output-eval-ci-gate/README.md` | `readme` | valid | completed | — | 0 | none | README exception |
| `docs/03.specs/120-agent-output-eval-ci-gate/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/121-dependency-vulnerability-audit-gate/README.md` | `readme` | valid | completed | — | 0 | none | README exception |
| `docs/03.specs/121-dependency-vulnerability-audit-gate/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/122-agentic-research-pack-consolidation/README.md` | `readme` | valid | completed | — | 0 | none | README exception |
| `docs/03.specs/122-agentic-research-pack-consolidation/spec.md` | `spec` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/123-agentic-engineering-audit-remediation/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/03.specs/123-agentic-engineering-audit-remediation/spec.md` | `spec` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/03.specs/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/04.execution/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/04.execution/plans/2026-03-26-01-gateway-standardization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-26-02-auth-standardization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-26-03-security-standardization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-26-04-data-standardization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-26-05-messaging-standardization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-26-06-observability-standardization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-26-07-workflow-standardization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-26-08-ai-standardization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-26-09-tooling-standardization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-26-10-communication-standardization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-26-11-laboratory-standardization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-27-08-ai-open-webui-plan.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-27-infra-service-optimization-priority-plan.md` | `plan` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-28-01-gateway-optimization-hardening-plan.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-28-04-data-optimization-hardening-plan.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-28-06-observability-optimization-hardening-plan.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-28-07-workflow-optimization-hardening-plan.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-28-08-ai-optimization-hardening-plan.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-28-09-tooling-optimization-hardening-plan.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-04-01-standardize-infra-net.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-09-harness-agent-first-engineering.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-09-infra-secrets-docs-refresh.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-10-docs-taxonomy-agent-first-migration.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-17-requirements-standardization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-17-scripts-ci-qa-cleanup.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-18-docs-05-operations-purpose-remediation.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-18-docs-bounded-consistency-audit.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-18-execution-stage-remediation.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-18-targeted-docs-precision-remediation.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-22-agent-hook-completion-style-automation.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-22-data-analytics-execution-traceability.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-22-lifecycle-readme-debt-closure.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-22-spec-execution-implementation-audit.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-22-workspace-docs-agent-governance-remediation.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-22-workspace-governance-bounded-reaudit.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-24-workspace-audit-grill-review.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-24-workspace-audit-improvement.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-24-workspace-audit-input-task-gap-closure.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-25-home-docker-revalidation-deferred-follow-up.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-25-home-docker-workspace-audit-improvement.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-25-large-scale-authored-ssot-review.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-26-workspace-audit-gap-closure.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-26-workspace-audit.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-28-workspace-doc-consistency.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-29-workspace-consistency-2026-05b.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-05-31-claude-harness-governance-verification.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-06-02-agent-governance-phase-1-revalidation.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-06-02-agent-governance-phase-2-strategy-integration.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-06-02-agent-governance-phase-3-approved-surface-activation.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-06-02-agent-governance-phase-4-closure-reconciliation.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-06-02-docs-implementation-reconciliation.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-06-02-governance-optimization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-06-03-governance-surgical-reverification.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-02-template-system-reorganization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-03-document-contract-remediation-batches.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-03-template-system-contract-standardization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-04-document-restructure-audit-contract-archive.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-05-agent-output-eval-fixtures.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-05-agentic-engineering-implementation-audit-pack.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-05-agentic-research-pack-refresh.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-05-audit-pack-coverage-report.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-05-compose-profile-service-coverage-snapshot.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-05-gap-routing-recommendation.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-05-provider-semantic-parity-validator.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-05-provider-workspace-artifact-path-parity.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-05-qa-gate-recommendation-ci-summary.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-05-template-system-numbered-sdlc-paths.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-05-workspace-support-surface-contract.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-06-agent-output-eval-ci-gate.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-06-agent-output-eval-runner.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-06-audit-implementation-matrix-snapshot.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-06-dependency-vulnerability-audit-gate.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-06-llm-wiki-stage-category-coverage.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-06-provider-hook-parity-matrix.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-06-sdlc-document-contract-corpus-normalization.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-06-security-automation-readiness-snapshot.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-06-tech-stack-version-provenance.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-10-agentic-research-pack-consolidation.md` | `plan` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/2026-07-11-agentic-engineering-audit-remediation.md` | `plan` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/plans/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/04.execution/tasks/2026-03-26-01-gateway-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-26-02-auth-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-26-03-security-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-26-04-data-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-26-05-messaging-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-26-06-observability-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-26-07-workflow-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-26-08-ai-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-26-09-tooling-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-26-10-communication-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-26-11-laboratory-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-27-08-ai-open-webui-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-28-02-auth-optimization-hardening-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-28-04-data-optimization-hardening-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-28-06-observability-optimization-hardening-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-28-08-ai-optimization-hardening-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-04-01-standardize-infra-net.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-04-10-infra-team-agent-cross-validation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-09-harness-agent-first-engineering.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-09-scripts-lifecycle-contract-cleanup.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-10-docs-taxonomy-agent-first-migration.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-17-requirements-standardization.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-17-scripts-ci-qa-cleanup.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-18-docs-05-operations-purpose-remediation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-18-docs-bounded-consistency-audit.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-18-execution-stage-remediation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-18-targeted-docs-precision-remediation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-22-agent-hook-completion-style-automation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-22-data-analytics-execution-traceability.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-22-lifecycle-readme-debt-closure.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-22-spec-execution-implementation-audit.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-22-workspace-docs-agent-governance-remediation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-22-workspace-governance-bounded-reaudit.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-24-workspace-audit-grill-review.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-24-workspace-audit-improvement.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-24-workspace-audit-input-task-gap-closure.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-25-home-docker-revalidation-deferred-follow-up.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-25-home-docker-workspace-audit-improvement.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-25-large-scale-authored-ssot-review.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-26-workspace-audit-gap-closure.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-26-workspace-audit.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-28-workspace-doc-consistency.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-29-workspace-consistency-2026-05b.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-05-31-claude-harness-governance-verification.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-02-agent-governance-phase-1-revalidation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-02-agent-governance-phase-2-strategy-integration.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-02-agent-governance-phase-3-approved-surface-activation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-02-agent-governance-phase-4-closure-reconciliation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-02-docs-implementation-reconciliation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-02-governance-optimization.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-03-governance-surgical-reverification.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-04-docs-implementation-audit.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-harness-engineering.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-boundary-audit.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-hard-enforcement.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-normalization-batch-1.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-normalization-batch-2.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-normalization-batch-3.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-1.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-2.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-3.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-4.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-5.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-6.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-7.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-8.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-reference-normalization.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-1.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-2.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-3.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-4.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-5.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-6.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-7.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-02-template-system-reorganization.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-04-examples-scaffold-contract-remediation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-04-frontmatter-routing-evidence-refresh.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-04-github-branch-protection-reverification.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-04-infra-tech-stack-version-refresh.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-05-agent-output-eval-fixtures.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-05-agentic-engineering-implementation-audit-pack.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-05-audit-pack-coverage-report.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-05-compose-profile-service-coverage-snapshot.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-05-gap-routing-recommendation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-05-provider-semantic-parity-validator.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-05-provider-workspace-artifact-path-parity.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-05-qa-gate-recommendation-ci-summary.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-05-template-system-numbered-sdlc-paths.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-05-workspace-support-surface-contract.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-06-agent-output-eval-ci-gate.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-06-agent-output-eval-runner.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-06-audit-implementation-matrix-snapshot.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-06-dependency-vulnerability-audit-gate.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-06-llm-wiki-stage-category-coverage.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-06-provider-hook-parity-matrix.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-06-sdlc-document-contract-corpus-normalization.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-06-security-automation-readiness-snapshot.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-06-tech-stack-version-provenance.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md` | `task` | valid | completed | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md` | `task` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/04.execution/tasks/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/05.operations/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/05.operations/guides/00-workspace/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/00-workspace/developer-setup.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/00-workspace/env-key-comparison.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/00-workspace/harness-agent-first-engineering.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/00-workspace/llm-wiki-maintenance.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/00-workspace/new-service-onboarding.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/00-workspace/sensitive-env-vars-comparison.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/01-gateway/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/01-gateway/nginx.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/01-gateway/setup.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/01-gateway/traefik.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/02-auth/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/02-auth/keycloak.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/02-auth/oauth2-proxy.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/03-security/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/03-security/vault.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/04-data/analytics/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/04-data/analytics/influxdb.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/analytics/ksqldb.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/analytics/opensearch.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/analytics/warehouses.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/cache-and-kv/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/04-data/cache-and-kv/valkey-cluster.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/lake-and-object/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/04-data/lake-and-object/minio.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/lake-and-object/seaweedfs.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/nosql/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/04-data/nosql/cassandra.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/nosql/couchdb.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/nosql/mongodb.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/operational/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/04-data/operational/mng-db.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/operational/supabase.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/optimization/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/04-data/optimization/optimization-hardening.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/relational/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/04-data/relational/postgresql-cluster.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/specialized/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/04-data/specialized/neo4j.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/04-data/specialized/qdrant.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/05-messaging/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/05-messaging/kafka.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/05-messaging/optimization-hardening.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/05-messaging/rabbitmq.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/06-observability/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/06-observability/alertmanager.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/06-observability/alloy.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/06-observability/grafana.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/06-observability/lgtm-stack.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/06-observability/loki.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/06-observability/optimization-hardening.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/06-observability/prometheus.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/06-observability/pushgateway.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/06-observability/pyroscope.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/06-observability/tempo.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/07-workflow/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/07-workflow/airflow-dag-basics.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/07-workflow/airflow.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/07-workflow/n8n.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/07-workflow/optimization-hardening.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/08-ai/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/08-ai/ollama.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/08-ai/open-webui.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/08-ai/optimization-hardening.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/08-ai/rag-workflow.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/09-tooling/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/09-tooling/k6.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/09-tooling/locust.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/09-tooling/optimization-hardening.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/09-tooling/performance-testing.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/09-tooling/registry.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/09-tooling/sonarqube.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/09-tooling/syncthing.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/09-tooling/terraform.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/09-tooling/terrakube.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/10-communication/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/10-communication/mail.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/11-laboratory/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/11-laboratory/dashboard.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/11-laboratory/dozzle.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/11-laboratory/open-notebook.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/11-laboratory/optimization-hardening.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/11-laboratory/portainer.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/11-laboratory/redisinsight.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/12-infra-net/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/guides/12-infra-net/standardize-infra-net.md` | `guide` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/05.operations/guides/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/incidents/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/00-workspace/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/00-workspace/common-optimizations-template-exceptions.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/00-workspace/harness-agent-first-engineering.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/00-workspace/infra-service-optimization-catalog.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/00-workspace/llm-wiki-maintenance.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/01-gateway/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/01-gateway/nginx.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/01-gateway/traefik.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/02-auth/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/02-auth/keycloak.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/02-auth/oauth2-proxy.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/03-security/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/03-security/vault.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/04-data/analytics/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/04-data/analytics/influxdb.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/analytics/ksqldb.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/analytics/opensearch.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/analytics/warehouses.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/backup/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/04-data/backup/backup-policy.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/cache-and-kv/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/04-data/cache-and-kv/valkey-cluster.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/lake-and-object/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/04-data/lake-and-object/minio.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/lake-and-object/seaweedfs.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/nosql/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/04-data/nosql/cassandra.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/nosql/couchdb.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/nosql/mongodb.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/operational/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/04-data/operational/mng-db.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/operational/supabase.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/optimization/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/04-data/optimization/optimization-hardening.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/relational/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/04-data/relational/postgresql-cluster.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/specialized/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/04-data/specialized/neo4j.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/04-data/specialized/qdrant.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/05-messaging/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/05-messaging/kafka.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/05-messaging/optimization-hardening.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/05-messaging/rabbitmq.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/06-observability/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/06-observability/alertmanager.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/06-observability/alloy.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/06-observability/grafana.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/06-observability/loki.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/06-observability/optimization-hardening.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/06-observability/prometheus.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/06-observability/pushgateway.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/06-observability/pyroscope.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/06-observability/retention.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/06-observability/tempo.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/07-workflow/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/07-workflow/airflow.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/07-workflow/dag-deployment.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/07-workflow/n8n.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/07-workflow/optimization-hardening.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/08-ai/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/08-ai/ollama.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/08-ai/open-webui.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/08-ai/optimization-hardening.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/09-tooling/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/09-tooling/iac-deployment-policy.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/09-tooling/k6.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/09-tooling/locust.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/09-tooling/optimization-hardening.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/09-tooling/performance-testing.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/09-tooling/registry.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/09-tooling/sonarqube.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/09-tooling/syncthing.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/09-tooling/terraform.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/09-tooling/terrakube.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/10-communication/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/10-communication/mail.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/11-laboratory/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/11-laboratory/dashboard.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/11-laboratory/dozzle.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/11-laboratory/open-notebook.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/11-laboratory/optimization-hardening.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/11-laboratory/portainer.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/11-laboratory/redisinsight.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/12-infra-net/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/policies/12-infra-net/standardize-infra-net.md` | `policy` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/policies/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/00-workspace/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/00-workspace/harness-agent-first-engineering-validation.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/00-workspace/llm-wiki-maintenance.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/00-workspace/release-management.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/01-gateway/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/01-gateway/nginx.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/01-gateway/traefik.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/02-auth/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/02-auth/keycloak.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/02-auth/oauth2-proxy.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/03-security/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/03-security/vault.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/04-data/analytics/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/04-data/analytics/influxdb.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/analytics/ksqldb.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/analytics/opensearch.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/analytics/warehouses.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/cache-and-kv/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/04-data/cache-and-kv/valkey-cluster.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/lake-and-object/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/04-data/lake-and-object/minio.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/lake-and-object/seaweedfs.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/nosql/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/04-data/nosql/cassandra.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/nosql/couchdb.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/nosql/mongodb.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/operational/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/04-data/operational/mng-db.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/operational/supabase.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/optimization/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/04-data/optimization/optimization-hardening.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/relational/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/04-data/relational/postgresql-cluster.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/specialized/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/04-data/specialized/neo4j.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/specialized/qdrant.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/04-data/storage/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/04-data/storage/storage-exhaustion.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/05-messaging/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/05-messaging/kafka.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/05-messaging/optimization-hardening.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/05-messaging/rabbitmq.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/06-observability/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/06-observability/alertmanager.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/06-observability/alloy.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/06-observability/grafana.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/06-observability/loki.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/06-observability/optimization-hardening.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/06-observability/prometheus.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/06-observability/pushgateway.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/06-observability/pyroscope.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/06-observability/tempo.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/07-workflow/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/07-workflow/airflow.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/07-workflow/n8n.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/07-workflow/optimization-hardening.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/08-ai/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/08-ai/gpu-recovery.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/08-ai/ollama.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/08-ai/open-webui.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/08-ai/optimization-hardening.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/09-tooling/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/09-tooling/k6.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/09-tooling/locust.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/09-tooling/optimization-hardening.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/09-tooling/performance-testing.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/09-tooling/registry.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/09-tooling/sonarqube.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/09-tooling/syncthing.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/09-tooling/terraform.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/09-tooling/terrakube.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/10-communication/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/10-communication/mail.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/11-laboratory/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/11-laboratory/dashboard.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/11-laboratory/dozzle.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/11-laboratory/open-notebook.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/11-laboratory/optimization-hardening.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/11-laboratory/portainer.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/11-laboratory/redisinsight.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/12-infra-net/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/05.operations/runbooks/12-infra-net/standardize-infra-net.md` | `runbook` | valid | active | — | 0 | missing-required-key, stale-active | migration candidate |
| `docs/05.operations/runbooks/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/90.references/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/ci-qa-parser-graphify-decision.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/contract-governance-map.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-inventory.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-routing-profile.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/historical-evidence-preservation.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/readme-profile-inventory.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/section-profile-inventory.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/template-application-gaps.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/ci-qa-formatting-contract.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/frontmatter-profile-inventory.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/operations-bucket-restructure.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/restructure-gap-register.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/sdlc-spec-archive-candidates.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/template-contract-drift.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/agent-instructions-catalog-vibe-models.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/compose-infrastructure-operations-readiness.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-template-readme-implementation.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/harness-engineering-implementation.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/loop-engineering-implementation.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/provider-harness-loop-implementation.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-document-contracts-implementation.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/workspace-rules-environment-implementation.md` | `audit` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/README.md` | `readme` | valid | superseded | — | 0 | none | README exception |
| `docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/agent-catalog-audit.md` | `audit` | valid | superseded | — | 0 | missing-required-key, replacement-free-supersession | migration candidate |
| `docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/automation-candidates.md` | `audit` | valid | superseded | — | 0 | missing-required-key, replacement-free-supersession | migration candidate |
| `docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/harness-loop-audit.md` | `audit` | valid | superseded | — | 0 | missing-required-key, replacement-free-supersession | migration candidate |
| `docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/implementation-overview.md` | `audit` | valid | superseded | — | 0 | missing-required-key, replacement-free-supersession | migration candidate |
| `docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/sdlc-qa-security-audit.md` | `audit` | valid | superseded | — | 0 | missing-required-key, replacement-free-supersession | migration candidate |
| `docs/90.references/audits/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/90.references/data/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/90.references/data/docker/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/90.references/data/docker/compose-profile-service-coverage.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/data/docker/image-version-interpretation.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/data/docker/tech-stack-version-provenance.md` | `generated` | valid | active | — | 0 | none | generated exception |
| `docs/90.references/data/glossary/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/90.references/data/glossary/stable-reference-terms.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/data/governance/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/90.references/data/governance/agent-output-eval-fixtures.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/data/governance/audit-implementation-matrix.md` | `generated` | valid | active | — | 0 | none | generated exception |
| `docs/90.references/data/governance/gap-to-stage-routing.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/data/governance/provider-hook-parity-matrix.md` | `generated` | valid | active | — | 0 | none | generated exception |
| `docs/90.references/data/hads/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/90.references/data/hads/profile.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/data/knowledge/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md` | `generated` | valid | active | — | 0 | none | generated exception |
| `docs/90.references/data/kubernetes/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/90.references/data/kubernetes/docker-compose-to-k3s-migration.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/data/security/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/90.references/data/security/security-automation-readiness.md` | `generated` | valid | active | — | 0 | none | generated exception |
| `docs/90.references/learning/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/90.references/learning/roadmap-v1.md` | `reference` | valid | superseded | — | 0 | missing-required-key, replacement-free-supersession | migration candidate |
| `docs/90.references/learning/roadmap.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/llm-wiki/README.md` | `readme` | missing | — | — | 0 | none | README exception |
| `docs/90.references/llm-wiki/llm-wiki-index.md` | `generated` | valid | active | — | 0 | none | generated exception |
| `docs/90.references/llm-wiki/repository-map.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-instructions-vibe-coding.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/document-metadata-lifecycle.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md` | `reference` | valid | active | — | 0 | missing-required-key | migration candidate |
| `docs/90.references/research/2026-07-07-agentic-research-pack-update/README.md` | `readme` | valid | superseded | — | 0 | none | README exception |
| `docs/90.references/research/2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md` | `reference` | valid | superseded | — | 0 | missing-required-key, replacement-free-supersession | migration candidate |
| `docs/90.references/research/2026-07-07-agentic-research-pack-update/harness-engineering.md` | `reference` | valid | superseded | — | 0 | missing-required-key, replacement-free-supersession | migration candidate |
| `docs/90.references/research/2026-07-07-agentic-research-pack-update/loop-engineering.md` | `reference` | valid | superseded | — | 0 | missing-required-key, replacement-free-supersession | migration candidate |
| `docs/90.references/research/2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md` | `reference` | valid | superseded | — | 0 | missing-required-key, replacement-free-supersession | migration candidate |
| `docs/90.references/research/2026-07-07-agentic-research-pack-update/workspace-baseline.md` | `reference` | valid | superseded | — | 0 | missing-required-key, replacement-free-supersession | migration candidate |
| `docs/90.references/research/README.md` | `readme` | valid | active | — | 0 | none | README exception |
| `docs/98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/04.execution/plans/2026-05-30-standardizing-agent-governance.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase2-alignment.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/04.execution/tasks/2026-05-30-standardizing-agent-governance.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase1-diagnostic.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-implementation.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-stage01-02-continuation.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-strategy-integration.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase4-closure.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-stage01-02-alignment.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/05.operations/guides/03-security/01.setup.md` | `archive` | valid | archived | — | 0 | missing-required-key | archive exception |
| `docs/98.archive/05.operations/guides/05-messaging/ksql-streaming.md` | `archive` | valid | archived | — | 0 | missing-required-key | archive exception |
| `docs/98.archive/05.operations/guides/07-workflow/01.airflow-dag-dev.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/05.operations/guides/07-workflow/airbyte.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/05.operations/guides/08-ai/01.llm-inference.md` | `archive` | valid | archived | — | 0 | missing-required-key | archive exception |
| `docs/98.archive/05.operations/guides/08-ai/local-llm-setup.md` | `archive` | valid | archived | — | 0 | missing-required-key | archive exception |
| `docs/98.archive/05.operations/guides/09-tooling/01.iac-automation.md` | `archive` | valid | archived | — | 0 | missing-required-key | archive exception |
| `docs/98.archive/05.operations/policies/07-workflow/airbyte.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/05.operations/runbooks/07-workflow/airbyte.md` | `archive` | valid | archived | — | 0 | none | archive exception |
| `docs/98.archive/README.md` | `readme` | valid | — | — | 0 | none | README exception |
| `docs/99.templates/README.md` | `readme` | valid | — | — | 0 | none | README exception |
| `docs/99.templates/support/README.md` | `readme` | valid | — | — | 0 | none | README exception |
| `docs/99.templates/support/external-source-rationale.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/99.templates/support/frontmatter-contract.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/99.templates/support/lifecycle-status.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/99.templates/support/template-contract.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/99.templates/support/template-governance.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/99.templates/support/template-selection.md` | `governance` | valid | — | — | 0 | none | governance exception |
| `docs/99.templates/templates/README.md` | `readme` | valid | — | — | 0 | none | README exception |
| `docs/99.templates/templates/common/README.md` | `readme` | valid | — | — | 0 | none | README exception |
| `docs/99.templates/templates/common/archive.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/common/readme.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/common/reference.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/governance/README.md` | `readme` | valid | — | — | 0 | none | README exception |
| `docs/99.templates/templates/governance/harness-task-contract.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/governance/memory.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/governance/progress.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/operations/README.md` | `readme` | valid | — | — | 0 | none | README exception |
| `docs/99.templates/templates/operations/guide.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/operations/incident.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/operations/policy.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/operations/postmortem.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/operations/runbook.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/sdlc/README.md` | `readme` | valid | — | — | 0 | none | README exception |
| `docs/99.templates/templates/sdlc/adr.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/sdlc/ard.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/sdlc/plan.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/sdlc/prd.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/sdlc/spec.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/sdlc/task.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/spec-contracts/README.md` | `readme` | valid | — | — | 0 | none | README exception |
| `docs/99.templates/templates/spec-contracts/agent-design.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/spec-contracts/api-spec.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/spec-contracts/data-model.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/spec-contracts/service.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |
| `docs/99.templates/templates/spec-contracts/tests.template.md` | `template-source` | valid | draft | — | 0 | none | template-source exception |

## Source Rules

- Paths come from sorted `git ls-files '*.md'` output filtered to canonical docs stages; non-Git fixtures use sorted recursive discovery.
- YAML is parsed with PyYAML `safe_load` behavior plus duplicate-key rejection.
- The report shows only bounded metadata fields, counts, and finding codes.
- Graphify is advisory and is not used as inventory proof.

## Sources

- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md) - metadata ownership and exception rules
- [Lifecycle status](../../../99.templates/support/lifecycle-status.md) - lifecycle vocabulary and transitions
- [Spec 123](../../../03.specs/123-agentic-engineering-audit-remediation/spec.md) - typed metadata and rollout contract
- [Semantic audit](./frontmatter-template-readme-implementation.md) - pre-remediation criteria and baseline

## Maintenance

- **Owner**: Metadata program owner / rules-engineer
- **Review Cadence**: Regenerate when tracked Markdown or metadata profiles change
- **Update Trigger**: Profile, parser, lifecycle, relation, exception, or corpus changes

## Related Documents

- [Audit pack README](./README.md)
- [Frontmatter/template/README audit](./frontmatter-template-readme-implementation.md)
- [SDLC and document-contract audit](./sdlc-document-contracts-implementation.md)
