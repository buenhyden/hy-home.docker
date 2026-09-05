---
title: "LLM Wiki Generated Index"
version: "1.0.0"
type: "reference/data-pack"
status: "published"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "references"
artifact_id: "DATA-0082"
parent_ids: []
created: "2026-08-19"
observed_at: "2026-08-23"
generated_by: "scripts/knowledge/generate-llm-wiki.py"
---

# LLM Wiki Generated Index

## Purpose

이 문서는 `hy-home.docker`의 LLM Wiki가 사용하는 generated tracked repo-local index다. LLM 에이전트가 먼저 확인할 수 있는 안전한 경로 목록을 제공하되, 각 파일의 내용이나 runtime truth를 복제하지 않는다.

Provide a deterministic path index for repo-local AI agents without creating a public site, a full-content bundle, or a replacement for canonical source files.

## Schema

Each inventory row contains a repository-relative path and a lightweight role derived from the tracked file name or suffix.

## Provenance

This generated tracked repo-local index complements `llms.txt` and the DATA-0083 repository map. Runtime truth remains in `infra/`, `scripts/`, registry JSON files, Docker Compose files, and `docs/00.agent-governance/`.

Graphify output is advisory navigation context only. This index is generated from repository path metadata and does not treat `graphify-out/` as source material.

### In Scope

- Repo-relative path links for safe tracked source entrypoints.
- Governance, runtime, documentation, infrastructure, script, and secret-handling policy surfaces.
- Deterministic refresh through `python3 scripts/knowledge/generate-llm-wiki.py --write`.

### Out of Scope

- Public website or public wiki deployment.
- `llms-full.txt` or any full-content export.
- External model calls, network publishing, deployment workflow, or Docker runtime behavior.
- Secret contents, credentials, private keys, tokens, shell history, raw logs, `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` as evidence.

## Inventory

### Root entrypoints

| Path | Role |
| --- | --- |
| [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | YAML config |
| [AGENTS.md](../../../../AGENTS.md) | Markdown reference |
| [CLAUDE.md](../../../../CLAUDE.md) | Markdown reference |
| [README.md](../../../../README.md) | folder index |
| [RTK.md](../../../../RTK.md) | Markdown reference |
| [docker-compose.yml](../../../../docker-compose.yml) | YAML config |
| [llms.txt](../../../../llms.txt) | text entrypoint |

### LLM Wiki reference

| Path | Role |
| --- | --- |
| [docs/90.references/data/0083-repository-map/README.md](../0083-repository-map/README.md) | folder index |

### Agent governance

| Path | Role |
| --- | --- |
| [docs/00.agent-governance/README.md](../../../00.agent-governance/README.md) | folder index |
| [docs/00.agent-governance/policies/agentic.md](../../../00.agent-governance/policies/agentic.md) | Markdown reference |
| [docs/00.agent-governance/policies/approval-boundaries.md](../../../00.agent-governance/policies/approval-boundaries.md) | Markdown reference |
| [docs/00.agent-governance/policies/bootstrap.md](../../../00.agent-governance/policies/bootstrap.md) | Markdown reference |
| [docs/00.agent-governance/policies/documentation-protocol.md](../../../00.agent-governance/policies/documentation-protocol.md) | Markdown reference |
| [docs/00.agent-governance/policies/environment-constraints.md](../../../00.agent-governance/policies/environment-constraints.md) | Markdown reference |
| [docs/00.agent-governance/policies/git-workflow.md](../../../00.agent-governance/policies/git-workflow.md) | Markdown reference |
| [docs/00.agent-governance/policies/github-governance.md](../../../00.agent-governance/policies/github-governance.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.block-absolute-file-link.md](../../../00.agent-governance/policies/hooks/hookify.block-absolute-file-link.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.block-direct-main-push.md](../../../00.agent-governance/policies/hooks/hookify.block-direct-main-push.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.block-gha-secrets-in-run.md](../../../00.agent-governance/policies/hooks/hookify.block-gha-secrets-in-run.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.block-git-no-verify.md](../../../00.agent-governance/policies/hooks/hookify.block-git-no-verify.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.block-plaintext-secret-compose.md](../../../00.agent-governance/policies/hooks/hookify.block-plaintext-secret-compose.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.block-unpinned-gha-action.md](../../../00.agent-governance/policies/hooks/hookify.block-unpinned-gha-action.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.enforce-docs-templates.md](../../../00.agent-governance/policies/hooks/hookify.enforce-docs-templates.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.require-logical-commits-before-stop.md](../../../00.agent-governance/policies/hooks/hookify.require-logical-commits-before-stop.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.warn-branch-naming.md](../../../00.agent-governance/policies/hooks/hookify.warn-branch-naming.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.warn-conventional-commit.md](../../../00.agent-governance/policies/hooks/hookify.warn-conventional-commit.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.warn-docker-infra-stop.md](../../../00.agent-governance/policies/hooks/hookify.warn-docker-infra-stop.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.warn-force-push.md](../../../00.agent-governance/policies/hooks/hookify.warn-force-push.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.warn-governance-memory-edit.md](../../../00.agent-governance/policies/hooks/hookify.warn-governance-memory-edit.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.warn-hook-parity-edit.md](../../../00.agent-governance/policies/hooks/hookify.warn-hook-parity-edit.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.warn-korean-in-governance.md](../../../00.agent-governance/policies/hooks/hookify.warn-korean-in-governance.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.warn-parallel-doc-file.md](../../../00.agent-governance/policies/hooks/hookify.warn-parallel-doc-file.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.warn-pre-commit-manual.md](../../../00.agent-governance/policies/hooks/hookify.warn-pre-commit-manual.md) | Markdown reference |
| [docs/00.agent-governance/policies/hooks/hookify.warn-stage-doc-edit.md](../../../00.agent-governance/policies/hooks/hookify.warn-stage-doc-edit.md) | Markdown reference |
| [docs/00.agent-governance/policies/output-style.md](../../../00.agent-governance/policies/output-style.md) | Markdown reference |
| [docs/00.agent-governance/policies/persona.md](../../../00.agent-governance/policies/persona.md) | Markdown reference |
| [docs/00.agent-governance/policies/postflight-checklist.md](../../../00.agent-governance/policies/postflight-checklist.md) | Markdown reference |
| [docs/00.agent-governance/policies/provider-capability-matrix.md](../../../00.agent-governance/policies/provider-capability-matrix.md) | Markdown reference |
| [docs/00.agent-governance/policies/quality-standards.md](../../../00.agent-governance/policies/quality-standards.md) | Markdown reference |
| [docs/00.agent-governance/policies/stage-authoring-matrix.md](../../../00.agent-governance/policies/stage-authoring-matrix.md) | Markdown reference |
| [docs/00.agent-governance/policies/standards.md](../../../00.agent-governance/policies/standards.md) | Markdown reference |
| [docs/00.agent-governance/policies/task-checklists.md](../../../00.agent-governance/policies/task-checklists.md) | Markdown reference |
| [docs/00.agent-governance/policies/workflows.md](../../../00.agent-governance/policies/workflows.md) | Markdown reference |
| [docs/00.agent-governance/providers/README.md](../../../00.agent-governance/providers/README.md) | folder index |
| [docs/00.agent-governance/providers/claude.md](../../../00.agent-governance/providers/claude.md) | Markdown reference |
| [docs/00.agent-governance/providers/codex.md](../../../00.agent-governance/providers/codex.md) | Markdown reference |
| [docs/00.agent-governance/providers/registry.yaml](../../../00.agent-governance/providers/registry.yaml) | YAML config |
| [docs/00.agent-governance/roles/ci-cd-engineer.md](../../../00.agent-governance/roles/ci-cd-engineer.md) | Markdown reference |
| [docs/00.agent-governance/roles/code-reviewer.md](../../../00.agent-governance/roles/code-reviewer.md) | Markdown reference |
| [docs/00.agent-governance/roles/doc-writer.md](../../../00.agent-governance/roles/doc-writer.md) | Markdown reference |
| [docs/00.agent-governance/roles/drift-detector.md](../../../00.agent-governance/roles/drift-detector.md) | Markdown reference |
| [docs/00.agent-governance/roles/eval-engineer.md](../../../00.agent-governance/roles/eval-engineer.md) | Markdown reference |
| [docs/00.agent-governance/roles/hook-developer.md](../../../00.agent-governance/roles/hook-developer.md) | Markdown reference |
| [docs/00.agent-governance/roles/iac-reviewer.md](../../../00.agent-governance/roles/iac-reviewer.md) | Markdown reference |
| [docs/00.agent-governance/roles/incident-responder.md](../../../00.agent-governance/roles/incident-responder.md) | Markdown reference |
| [docs/00.agent-governance/roles/infra-implementer.md](../../../00.agent-governance/roles/infra-implementer.md) | Markdown reference |
| [docs/00.agent-governance/roles/qa-engineer.md](../../../00.agent-governance/roles/qa-engineer.md) | Markdown reference |
| [docs/00.agent-governance/roles/rules-engineer.md](../../../00.agent-governance/roles/rules-engineer.md) | Markdown reference |
| [docs/00.agent-governance/roles/security-auditor.md](../../../00.agent-governance/roles/security-auditor.md) | Markdown reference |
| [docs/00.agent-governance/roles/skill-creator.md](../../../00.agent-governance/roles/skill-creator.md) | Markdown reference |
| [docs/00.agent-governance/roles/workflow-supervisor.md](../../../00.agent-governance/roles/workflow-supervisor.md) | Markdown reference |
| [docs/00.agent-governance/sdlc.md](../../../00.agent-governance/sdlc.md) | Markdown reference |
| [docs/00.agent-governance/skills/adr-writing.md](../../../00.agent-governance/skills/adr-writing.md) | Markdown reference |
| [docs/00.agent-governance/skills/change-review-execution.md](../../../00.agent-governance/skills/change-review-execution.md) | Markdown reference |
| [docs/00.agent-governance/skills/ci-cd-patterns.md](../../../00.agent-governance/skills/ci-cd-patterns.md) | Markdown reference |
| [docs/00.agent-governance/skills/code-review-dimensions.md](../../../00.agent-governance/skills/code-review-dimensions.md) | Markdown reference |
| [docs/00.agent-governance/skills/compose-stack-agent.md](../../../00.agent-governance/skills/compose-stack-agent.md) | Markdown reference |
| [docs/00.agent-governance/skills/container-threat-modeling.md](../../../00.agent-governance/skills/container-threat-modeling.md) | Markdown reference |
| [docs/00.agent-governance/skills/deployment-pipeline-design.md](../../../00.agent-governance/skills/deployment-pipeline-design.md) | Markdown reference |
| [docs/00.agent-governance/skills/docker-compose-patterns.md](../../../00.agent-governance/skills/docker-compose-patterns.md) | Markdown reference |
| [docs/00.agent-governance/skills/e2e-testing.md](../../../00.agent-governance/skills/e2e-testing.md) | Markdown reference |
| [docs/00.agent-governance/skills/execution-plan-agent.md](../../../00.agent-governance/skills/execution-plan-agent.md) | Markdown reference |
| [docs/00.agent-governance/skills/incident-response.md](../../../00.agent-governance/skills/incident-response.md) | Markdown reference |
| [docs/00.agent-governance/skills/infra-cross-validate.md](../../../00.agent-governance/skills/infra-cross-validate.md) | Markdown reference |
| [docs/00.agent-governance/skills/infra-validate.md](../../../00.agent-governance/skills/infra-validate.md) | Markdown reference |
| [docs/00.agent-governance/skills/knowledge-map-agent.md](../../../00.agent-governance/skills/knowledge-map-agent.md) | Markdown reference |
| [docs/00.agent-governance/skills/ops-runbook-agent.md](../../../00.agent-governance/skills/ops-runbook-agent.md) | Markdown reference |
| [docs/00.agent-governance/skills/policy-gate-agent.md](../../../00.agent-governance/skills/policy-gate-agent.md) | Markdown reference |
| [docs/00.agent-governance/skills/provider-model-evaluation.md](../../../00.agent-governance/skills/provider-model-evaluation.md) | Markdown reference |
| [docs/00.agent-governance/skills/requirements-to-design-agent.md](../../../00.agent-governance/skills/requirements-to-design-agent.md) | Markdown reference |
| [docs/00.agent-governance/skills/security-audit.md](../../../00.agent-governance/skills/security-audit.md) | Markdown reference |
| [docs/00.agent-governance/skills/style-validation.md](../../../00.agent-governance/skills/style-validation.md) | Markdown reference |
| [docs/00.agent-governance/skills/task-breakdown-agent.md](../../../00.agent-governance/skills/task-breakdown-agent.md) | Markdown reference |
| [docs/00.agent-governance/skills/test-authoring.md](../../../00.agent-governance/skills/test-authoring.md) | Markdown reference |
| [docs/00.agent-governance/skills/workspace-audit-revalidation.md](../../../00.agent-governance/skills/workspace-audit-revalidation.md) | Markdown reference |

### Runtime surfaces

| Path | Role |
| --- | --- |
| [.claude/CLAUDE.md](../../../../.claude/CLAUDE.md) | Markdown reference |
| [.claude/README.md](../../../../.claude/README.md) | folder index |
| [.claude/agents/ci-cd-engineer.md](../../../../.claude/agents/ci-cd-engineer.md) | Markdown reference |
| [.claude/agents/code-reviewer.md](../../../../.claude/agents/code-reviewer.md) | Markdown reference |
| [.claude/agents/doc-writer.md](../../../../.claude/agents/doc-writer.md) | Markdown reference |
| [.claude/agents/drift-detector.md](../../../../.claude/agents/drift-detector.md) | Markdown reference |
| [.claude/agents/eval-engineer.md](../../../../.claude/agents/eval-engineer.md) | Markdown reference |
| [.claude/agents/hook-developer.md](../../../../.claude/agents/hook-developer.md) | Markdown reference |
| [.claude/agents/iac-reviewer.md](../../../../.claude/agents/iac-reviewer.md) | Markdown reference |
| [.claude/agents/incident-responder.md](../../../../.claude/agents/incident-responder.md) | Markdown reference |
| [.claude/agents/infra-implementer.md](../../../../.claude/agents/infra-implementer.md) | Markdown reference |
| [.claude/agents/qa-engineer.md](../../../../.claude/agents/qa-engineer.md) | Markdown reference |
| [.claude/agents/rules-engineer.md](../../../../.claude/agents/rules-engineer.md) | Markdown reference |
| [.claude/agents/security-auditor.md](../../../../.claude/agents/security-auditor.md) | Markdown reference |
| [.claude/agents/skill-creator.md](../../../../.claude/agents/skill-creator.md) | Markdown reference |
| [.claude/agents/workflow-supervisor.md](../../../../.claude/agents/workflow-supervisor.md) | Markdown reference |
| [.claude/hooks/docker-compose-pre.sh](../../../../.claude/hooks/docker-compose-pre.sh) | script |
| [.claude/hooks/post-tool-validate.sh](../../../../.claude/hooks/post-tool-validate.sh) | script |
| [.claude/hooks/pre-compact.sh](../../../../.claude/hooks/pre-compact.sh) | script |
| [.claude/hooks/session-end.sh](../../../../.claude/hooks/session-end.sh) | script |
| [.claude/hooks/session-start.sh](../../../../.claude/hooks/session-start.sh) | script |
| [.claude/hooks/stop.sh](../../../../.claude/hooks/stop.sh) | script |
| [.claude/hooks/user-prompt-submit.sh](../../../../.claude/hooks/user-prompt-submit.sh) | script |
| [.claude/output-styles/hy-home.md](../../../../.claude/output-styles/hy-home.md) | Markdown reference |
| [.claude/settings.json](../../../../.claude/settings.json) | JSON registry |
| [.claude/skills/adr-writing/SKILL.md](../../../../.claude/skills/adr-writing/SKILL.md) | Markdown reference |
| [.claude/skills/change-review-execution/SKILL.md](../../../../.claude/skills/change-review-execution/SKILL.md) | Markdown reference |
| [.claude/skills/ci-cd-patterns/SKILL.md](../../../../.claude/skills/ci-cd-patterns/SKILL.md) | Markdown reference |
| [.claude/skills/code-review-dimensions/SKILL.md](../../../../.claude/skills/code-review-dimensions/SKILL.md) | Markdown reference |
| [.claude/skills/compose-stack-agent/SKILL.md](../../../../.claude/skills/compose-stack-agent/SKILL.md) | Markdown reference |
| [.claude/skills/container-threat-modeling/SKILL.md](../../../../.claude/skills/container-threat-modeling/SKILL.md) | Markdown reference |
| [.claude/skills/deployment-pipeline-design/SKILL.md](../../../../.claude/skills/deployment-pipeline-design/SKILL.md) | Markdown reference |
| [.claude/skills/docker-compose-patterns/SKILL.md](../../../../.claude/skills/docker-compose-patterns/SKILL.md) | Markdown reference |
| [.claude/skills/e2e-testing/SKILL.md](../../../../.claude/skills/e2e-testing/SKILL.md) | Markdown reference |
| [.claude/skills/execution-plan-agent/SKILL.md](../../../../.claude/skills/execution-plan-agent/SKILL.md) | Markdown reference |
| [.claude/skills/incident-response/SKILL.md](../../../../.claude/skills/incident-response/SKILL.md) | Markdown reference |
| [.claude/skills/infra-cross-validate/SKILL.md](../../../../.claude/skills/infra-cross-validate/SKILL.md) | Markdown reference |
| [.claude/skills/infra-validate/SKILL.md](../../../../.claude/skills/infra-validate/SKILL.md) | Markdown reference |
| [.claude/skills/knowledge-map-agent/SKILL.md](../../../../.claude/skills/knowledge-map-agent/SKILL.md) | Markdown reference |
| [.claude/skills/ops-runbook-agent/SKILL.md](../../../../.claude/skills/ops-runbook-agent/SKILL.md) | Markdown reference |
| [.claude/skills/policy-gate-agent/SKILL.md](../../../../.claude/skills/policy-gate-agent/SKILL.md) | Markdown reference |
| [.claude/skills/provider-model-evaluation/SKILL.md](../../../../.claude/skills/provider-model-evaluation/SKILL.md) | Markdown reference |
| [.claude/skills/requirements-to-design-agent/SKILL.md](../../../../.claude/skills/requirements-to-design-agent/SKILL.md) | Markdown reference |
| [.claude/skills/security-audit/SKILL.md](../../../../.claude/skills/security-audit/SKILL.md) | Markdown reference |
| [.claude/skills/style-validation/SKILL.md](../../../../.claude/skills/style-validation/SKILL.md) | Markdown reference |
| [.claude/skills/task-breakdown-agent/SKILL.md](../../../../.claude/skills/task-breakdown-agent/SKILL.md) | Markdown reference |
| [.claude/skills/test-authoring/SKILL.md](../../../../.claude/skills/test-authoring/SKILL.md) | Markdown reference |
| [.claude/skills/workspace-audit-revalidation/SKILL.md](../../../../.claude/skills/workspace-audit-revalidation/SKILL.md) | Markdown reference |
| [.codex/README.md](../../../../.codex/README.md) | folder index |
| [.codex/agents/ci-cd-engineer.toml](../../../../.codex/agents/ci-cd-engineer.toml) | source path |
| [.codex/agents/code-reviewer.toml](../../../../.codex/agents/code-reviewer.toml) | source path |
| [.codex/agents/doc-writer.toml](../../../../.codex/agents/doc-writer.toml) | source path |
| [.codex/agents/drift-detector.toml](../../../../.codex/agents/drift-detector.toml) | source path |
| [.codex/agents/eval-engineer.toml](../../../../.codex/agents/eval-engineer.toml) | source path |
| [.codex/agents/hook-developer.toml](../../../../.codex/agents/hook-developer.toml) | source path |
| [.codex/agents/iac-reviewer.toml](../../../../.codex/agents/iac-reviewer.toml) | source path |
| [.codex/agents/incident-responder.toml](../../../../.codex/agents/incident-responder.toml) | source path |
| [.codex/agents/infra-implementer.toml](../../../../.codex/agents/infra-implementer.toml) | source path |
| [.codex/agents/qa-engineer.toml](../../../../.codex/agents/qa-engineer.toml) | source path |
| [.codex/agents/rules-engineer.toml](../../../../.codex/agents/rules-engineer.toml) | source path |
| [.codex/agents/security-auditor.toml](../../../../.codex/agents/security-auditor.toml) | source path |
| [.codex/agents/skill-creator.toml](../../../../.codex/agents/skill-creator.toml) | source path |
| [.codex/agents/workflow-supervisor.toml](../../../../.codex/agents/workflow-supervisor.toml) | source path |
| [.codex/hooks.json](../../../../.codex/hooks.json) | JSON registry |

### Active stage docs

| Path | Role |
| --- | --- |
| [docs/01.requirements/0001-gateway.md](../../../01.requirements/0001-gateway.md) | Markdown reference |
| [docs/01.requirements/0002-auth.md](../../../01.requirements/0002-auth.md) | Markdown reference |
| [docs/01.requirements/0003-security.md](../../../01.requirements/0003-security.md) | Markdown reference |
| [docs/01.requirements/0004-data.md](../../../01.requirements/0004-data.md) | Markdown reference |
| [docs/01.requirements/0005-data-analytics.md](../../../01.requirements/0005-data-analytics.md) | Markdown reference |
| [docs/01.requirements/0006-messaging.md](../../../01.requirements/0006-messaging.md) | Markdown reference |
| [docs/01.requirements/0007-observability.md](../../../01.requirements/0007-observability.md) | Markdown reference |
| [docs/01.requirements/0008-workflow.md](../../../01.requirements/0008-workflow.md) | Markdown reference |
| [docs/01.requirements/0009-ai.md](../../../01.requirements/0009-ai.md) | Markdown reference |
| [docs/01.requirements/0010-tooling.md](../../../01.requirements/0010-tooling.md) | Markdown reference |
| [docs/01.requirements/0011-communication.md](../../../01.requirements/0011-communication.md) | Markdown reference |
| [docs/01.requirements/0012-laboratory.md](../../../01.requirements/0012-laboratory.md) | Markdown reference |
| [docs/01.requirements/0013-ai-open-webui.md](../../../01.requirements/0013-ai-open-webui.md) | Markdown reference |
| [docs/01.requirements/0023-standardize-infra-net.md](../../../01.requirements/0023-standardize-infra-net.md) | Markdown reference |
| [docs/01.requirements/0024-agent-governance-standardization.md](../../../01.requirements/0024-agent-governance-standardization.md) | Markdown reference |
| [docs/01.requirements/0025-operational-readiness-closure.md](../../../01.requirements/0025-operational-readiness-closure.md) | Markdown reference |
| [docs/01.requirements/0026-document-retention-and-retirement.md](../../../01.requirements/0026-document-retention-and-retirement.md) | Markdown reference |
| [docs/01.requirements/README.md](../../../01.requirements/README.md) | folder index |
| [docs/02.architecture/README.md](../../../02.architecture/README.md) | folder index |
| [docs/02.architecture/decisions/0001-traefik-nginx-hybrid.md](../../../02.architecture/decisions/0001-traefik-nginx-hybrid.md) | Markdown reference |
| [docs/02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md](../../../02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md) | Markdown reference |
| [docs/02.architecture/decisions/0003-vault-as-secrets-manager.md](../../../02.architecture/decisions/0003-vault-as-secrets-manager.md) | Markdown reference |
| [docs/02.architecture/decisions/0004-postgresql-ha-patroni.md](../../../02.architecture/decisions/0004-postgresql-ha-patroni.md) | Markdown reference |
| [docs/02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md](../../../02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md) | Markdown reference |
| [docs/02.architecture/decisions/0006-lgtm-stack-selection.md](../../../02.architecture/decisions/0006-lgtm-stack-selection.md) | Markdown reference |
| [docs/02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md](../../../02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md) | Markdown reference |
| [docs/02.architecture/decisions/0008-ollama-openwebui-local-ai.md](../../../02.architecture/decisions/0008-ollama-openwebui-local-ai.md) | Markdown reference |
| [docs/02.architecture/decisions/0009-tooling-services.md](../../../02.architecture/decisions/0009-tooling-services.md) | Markdown reference |
| [docs/02.architecture/decisions/0010-communication-services.md](../../../02.architecture/decisions/0010-communication-services.md) | Markdown reference |
| [docs/02.architecture/decisions/0011-laboratory-services.md](../../../02.architecture/decisions/0011-laboratory-services.md) | Markdown reference |
| [docs/02.architecture/decisions/0015-analytics-engine-selection.md](../../../02.architecture/decisions/0015-analytics-engine-selection.md) | Markdown reference |
| [docs/02.architecture/decisions/0016-open-webui-implementation.md](../../../02.architecture/decisions/0016-open-webui-implementation.md) | Markdown reference |
| [docs/02.architecture/decisions/0017-auth-hardening-runtime-and-fail-closed.md](../../../02.architecture/decisions/0017-auth-hardening-runtime-and-fail-closed.md) | Markdown reference |
| [docs/02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0019-data-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0019-data-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0026-standardize-infra-net.md](../../../02.architecture/decisions/0026-standardize-infra-net.md) | Markdown reference |
| [docs/02.architecture/decisions/0028-local-isolated-readiness-evidence.md](../../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md) | Markdown reference |
| [docs/02.architecture/decisions/0029-workspace-governance-authority.md](../../../02.architecture/decisions/0029-workspace-governance-authority.md) | Markdown reference |
| [docs/02.architecture/decisions/0031-preserved-archive-record.md](../../../02.architecture/decisions/0031-preserved-archive-record.md) | Markdown reference |
| [docs/02.architecture/decisions/README.md](../../../02.architecture/decisions/README.md) | folder index |
| [docs/02.architecture/descriptions/0001-gateway-architecture.md](../../../02.architecture/descriptions/0001-gateway-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0002-auth-architecture.md](../../../02.architecture/descriptions/0002-auth-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0003-security-architecture.md](../../../02.architecture/descriptions/0003-security-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0004-data-architecture.md](../../../02.architecture/descriptions/0004-data-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0005-messaging-architecture.md](../../../02.architecture/descriptions/0005-messaging-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0006-observability-architecture.md](../../../02.architecture/descriptions/0006-observability-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0007-workflow-architecture.md](../../../02.architecture/descriptions/0007-workflow-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0008-ai-architecture.md](../../../02.architecture/descriptions/0008-ai-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0009-tooling-architecture.md](../../../02.architecture/descriptions/0009-tooling-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0010-communication-architecture.md](../../../02.architecture/descriptions/0010-communication-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0011-laboratory-architecture.md](../../../02.architecture/descriptions/0011-laboratory-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0012-data-analytics-architecture.md](../../../02.architecture/descriptions/0012-data-analytics-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0013-open-webui-architecture.md](../../../02.architecture/descriptions/0013-open-webui-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0014-auth-optimization-hardening-architecture.md](../../../02.architecture/descriptions/0014-auth-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0018-security-optimization-hardening-architecture.md](../../../02.architecture/descriptions/0018-security-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0019-data-optimization-hardening-architecture.md](../../../02.architecture/descriptions/0019-data-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0020-messaging-optimization-hardening-architecture.md](../../../02.architecture/descriptions/0020-messaging-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0021-observability-optimization-hardening-architecture.md](../../../02.architecture/descriptions/0021-observability-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0022-workflow-optimization-hardening-architecture.md](../../../02.architecture/descriptions/0022-workflow-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0023-ai-optimization-hardening-architecture.md](../../../02.architecture/descriptions/0023-ai-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0024-tooling-optimization-hardening-architecture.md](../../../02.architecture/descriptions/0024-tooling-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0025-laboratory-optimization-hardening-architecture.md](../../../02.architecture/descriptions/0025-laboratory-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/0026-standardize-infra-net.md](../../../02.architecture/descriptions/0026-standardize-infra-net.md) | Markdown reference |
| [docs/02.architecture/descriptions/0027-agent-governance-canonical-adapter.md](../../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md) | Markdown reference |
| [docs/02.architecture/descriptions/0028-operational-readiness-closure.md](../../../02.architecture/descriptions/0028-operational-readiness-closure.md) | Markdown reference |
| [docs/02.architecture/descriptions/0030-document-lifecycle-governance.md](../../../02.architecture/descriptions/0030-document-lifecycle-governance.md) | Markdown reference |
| [docs/02.architecture/descriptions/README.md](../../../02.architecture/descriptions/README.md) | folder index |
| [docs/03.specs/0173-governance-qa-surface-convergence/plan.md](../../../03.specs/0173-governance-qa-surface-convergence/plan.md) | Markdown reference |
| [docs/03.specs/0173-governance-qa-surface-convergence/spec.md](../../../03.specs/0173-governance-qa-surface-convergence/spec.md) | Markdown reference |
| [docs/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0001-lifecycle-and-red-contracts.md](../../../03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0001-lifecycle-and-red-contracts.md) | Markdown reference |
| [docs/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0002-gate-composition-convergence.md](../../../03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0002-gate-composition-convergence.md) | Markdown reference |
| [docs/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0003-script-and-operation-ownership.md](../../../03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0003-script-and-operation-ownership.md) | Markdown reference |
| [docs/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0004-test-and-fixture-convergence.md](../../../03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0004-test-and-fixture-convergence.md) | Markdown reference |
| [docs/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0005-document-and-provider-residue.md](../../../03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0005-document-and-provider-residue.md) | Markdown reference |
| [docs/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0006-generated-evidence-and-final-verification.md](../../../03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0006-generated-evidence-and-final-verification.md) | Markdown reference |
| [docs/03.specs/README.md](../../../03.specs/README.md) | folder index |

### Operations docs

| Path | Role |
| --- | --- |
| [docs/05.operations/README.md](../../../05.operations/README.md) | folder index |
| [docs/05.operations/catalog/00-workspace/0001-common-optimizations-template-exceptions/policy.md](../../../05.operations/catalog/00-workspace/0001-common-optimizations-template-exceptions/policy.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/0002-developer-environment/guide.md](../../../05.operations/catalog/00-workspace/0002-developer-environment/guide.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/0003-env-key-comparison/guide.md](../../../05.operations/catalog/00-workspace/0003-env-key-comparison/guide.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/guide.md](../../../05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/guide.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/policy.md](../../../05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/policy.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/runbook.md](../../../05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/0006-infrastructure-optimization-governance/policy.md](../../../05.operations/catalog/00-workspace/0006-infrastructure-optimization-governance/policy.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md](../../../05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/policy.md](../../../05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/policy.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/runbook.md](../../../05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/0008-new-service-onboarding/guide.md](../../../05.operations/catalog/00-workspace/0008-new-service-onboarding/guide.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/0009-release-management/runbook.md](../../../05.operations/catalog/00-workspace/0009-release-management/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/0010-sensitive-env-vars-comparison/guide.md](../../../05.operations/catalog/00-workspace/0010-sensitive-env-vars-comparison/guide.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md) | Markdown reference |
| [docs/05.operations/catalog/00-workspace/README.md](../../../05.operations/catalog/00-workspace/README.md) | folder index |
| [docs/05.operations/catalog/01-gateway/0011-nginx/guide.md](../../../05.operations/catalog/01-gateway/0011-nginx/guide.md) | Markdown reference |
| [docs/05.operations/catalog/01-gateway/0011-nginx/policy.md](../../../05.operations/catalog/01-gateway/0011-nginx/policy.md) | Markdown reference |
| [docs/05.operations/catalog/01-gateway/0011-nginx/runbook.md](../../../05.operations/catalog/01-gateway/0011-nginx/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/01-gateway/0012-edge-routing-stack/guide.md](../../../05.operations/catalog/01-gateway/0012-edge-routing-stack/guide.md) | Markdown reference |
| [docs/05.operations/catalog/01-gateway/0013-traefik/guide.md](../../../05.operations/catalog/01-gateway/0013-traefik/guide.md) | Markdown reference |
| [docs/05.operations/catalog/01-gateway/0013-traefik/policy.md](../../../05.operations/catalog/01-gateway/0013-traefik/policy.md) | Markdown reference |
| [docs/05.operations/catalog/01-gateway/0013-traefik/runbook.md](../../../05.operations/catalog/01-gateway/0013-traefik/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/01-gateway/README.md](../../../05.operations/catalog/01-gateway/README.md) | folder index |
| [docs/05.operations/catalog/02-auth/0014-keycloak/guide.md](../../../05.operations/catalog/02-auth/0014-keycloak/guide.md) | Markdown reference |
| [docs/05.operations/catalog/02-auth/0014-keycloak/policy.md](../../../05.operations/catalog/02-auth/0014-keycloak/policy.md) | Markdown reference |
| [docs/05.operations/catalog/02-auth/0014-keycloak/runbook.md](../../../05.operations/catalog/02-auth/0014-keycloak/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/02-auth/0015-oauth2-proxy/guide.md](../../../05.operations/catalog/02-auth/0015-oauth2-proxy/guide.md) | Markdown reference |
| [docs/05.operations/catalog/02-auth/0015-oauth2-proxy/policy.md](../../../05.operations/catalog/02-auth/0015-oauth2-proxy/policy.md) | Markdown reference |
| [docs/05.operations/catalog/02-auth/0015-oauth2-proxy/runbook.md](../../../05.operations/catalog/02-auth/0015-oauth2-proxy/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/02-auth/README.md](../../../05.operations/catalog/02-auth/README.md) | folder index |
| [docs/05.operations/catalog/03-security/0016-vault/guide.md](../../../05.operations/catalog/03-security/0016-vault/guide.md) | Markdown reference |
| [docs/05.operations/catalog/03-security/0016-vault/policy.md](../../../05.operations/catalog/03-security/0016-vault/policy.md) | Markdown reference |
| [docs/05.operations/catalog/03-security/0016-vault/runbook.md](../../../05.operations/catalog/03-security/0016-vault/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/03-security/README.md](../../../05.operations/catalog/03-security/README.md) | folder index |
| [docs/05.operations/catalog/04-data/0017-influxdb/guide.md](../../../05.operations/catalog/04-data/0017-influxdb/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0017-influxdb/policy.md](../../../05.operations/catalog/04-data/0017-influxdb/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0017-influxdb/runbook.md](../../../05.operations/catalog/04-data/0017-influxdb/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0018-ksqldb/guide.md](../../../05.operations/catalog/04-data/0018-ksqldb/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0018-ksqldb/policy.md](../../../05.operations/catalog/04-data/0018-ksqldb/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0018-ksqldb/runbook.md](../../../05.operations/catalog/04-data/0018-ksqldb/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0019-opensearch/guide.md](../../../05.operations/catalog/04-data/0019-opensearch/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0019-opensearch/policy.md](../../../05.operations/catalog/04-data/0019-opensearch/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0019-opensearch/runbook.md](../../../05.operations/catalog/04-data/0019-opensearch/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0020-starrocks/guide.md](../../../05.operations/catalog/04-data/0020-starrocks/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0020-starrocks/policy.md](../../../05.operations/catalog/04-data/0020-starrocks/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0020-starrocks/runbook.md](../../../05.operations/catalog/04-data/0020-starrocks/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0021-backup-and-restore/policy.md](../../../05.operations/catalog/04-data/0021-backup-and-restore/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0022-valkey-cluster/guide.md](../../../05.operations/catalog/04-data/0022-valkey-cluster/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0022-valkey-cluster/policy.md](../../../05.operations/catalog/04-data/0022-valkey-cluster/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0022-valkey-cluster/runbook.md](../../../05.operations/catalog/04-data/0022-valkey-cluster/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0023-minio/guide.md](../../../05.operations/catalog/04-data/0023-minio/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0023-minio/policy.md](../../../05.operations/catalog/04-data/0023-minio/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0023-minio/runbook.md](../../../05.operations/catalog/04-data/0023-minio/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0024-seaweedfs/guide.md](../../../05.operations/catalog/04-data/0024-seaweedfs/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0024-seaweedfs/policy.md](../../../05.operations/catalog/04-data/0024-seaweedfs/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0024-seaweedfs/runbook.md](../../../05.operations/catalog/04-data/0024-seaweedfs/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0025-cassandra/guide.md](../../../05.operations/catalog/04-data/0025-cassandra/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0025-cassandra/policy.md](../../../05.operations/catalog/04-data/0025-cassandra/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0025-cassandra/runbook.md](../../../05.operations/catalog/04-data/0025-cassandra/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0026-couchdb/guide.md](../../../05.operations/catalog/04-data/0026-couchdb/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0026-couchdb/policy.md](../../../05.operations/catalog/04-data/0026-couchdb/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0026-couchdb/runbook.md](../../../05.operations/catalog/04-data/0026-couchdb/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0027-mongodb/guide.md](../../../05.operations/catalog/04-data/0027-mongodb/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0027-mongodb/policy.md](../../../05.operations/catalog/04-data/0027-mongodb/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0027-mongodb/runbook.md](../../../05.operations/catalog/04-data/0027-mongodb/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0028-management-database/guide.md](../../../05.operations/catalog/04-data/0028-management-database/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0028-management-database/policy.md](../../../05.operations/catalog/04-data/0028-management-database/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0028-management-database/runbook.md](../../../05.operations/catalog/04-data/0028-management-database/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0029-supabase/guide.md](../../../05.operations/catalog/04-data/0029-supabase/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0029-supabase/policy.md](../../../05.operations/catalog/04-data/0029-supabase/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0029-supabase/runbook.md](../../../05.operations/catalog/04-data/0029-supabase/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0030-optimization-hardening/guide.md](../../../05.operations/catalog/04-data/0030-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0030-optimization-hardening/policy.md](../../../05.operations/catalog/04-data/0030-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0030-optimization-hardening/runbook.md](../../../05.operations/catalog/04-data/0030-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0031-postgresql-cluster/guide.md](../../../05.operations/catalog/04-data/0031-postgresql-cluster/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0031-postgresql-cluster/policy.md](../../../05.operations/catalog/04-data/0031-postgresql-cluster/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md](../../../05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md](../../../05.operations/catalog/04-data/0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0033-neo4j/guide.md](../../../05.operations/catalog/04-data/0033-neo4j/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0033-neo4j/policy.md](../../../05.operations/catalog/04-data/0033-neo4j/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0033-neo4j/runbook.md](../../../05.operations/catalog/04-data/0033-neo4j/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0034-qdrant/guide.md](../../../05.operations/catalog/04-data/0034-qdrant/guide.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0034-qdrant/policy.md](../../../05.operations/catalog/04-data/0034-qdrant/policy.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0034-qdrant/runbook.md](../../../05.operations/catalog/04-data/0034-qdrant/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/0035-storage-exhaustion/runbook.md](../../../05.operations/catalog/04-data/0035-storage-exhaustion/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/04-data/README.md](../../../05.operations/catalog/04-data/README.md) | folder index |
| [docs/05.operations/catalog/05-messaging/0036-kafka/guide.md](../../../05.operations/catalog/05-messaging/0036-kafka/guide.md) | Markdown reference |
| [docs/05.operations/catalog/05-messaging/0036-kafka/policy.md](../../../05.operations/catalog/05-messaging/0036-kafka/policy.md) | Markdown reference |
| [docs/05.operations/catalog/05-messaging/0036-kafka/runbook.md](../../../05.operations/catalog/05-messaging/0036-kafka/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/05-messaging/0037-optimization-hardening/guide.md](../../../05.operations/catalog/05-messaging/0037-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/catalog/05-messaging/0037-optimization-hardening/policy.md](../../../05.operations/catalog/05-messaging/0037-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/catalog/05-messaging/0037-optimization-hardening/runbook.md](../../../05.operations/catalog/05-messaging/0037-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/05-messaging/0038-rabbitmq/guide.md](../../../05.operations/catalog/05-messaging/0038-rabbitmq/guide.md) | Markdown reference |
| [docs/05.operations/catalog/05-messaging/0038-rabbitmq/policy.md](../../../05.operations/catalog/05-messaging/0038-rabbitmq/policy.md) | Markdown reference |
| [docs/05.operations/catalog/05-messaging/0038-rabbitmq/runbook.md](../../../05.operations/catalog/05-messaging/0038-rabbitmq/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/05-messaging/README.md](../../../05.operations/catalog/05-messaging/README.md) | folder index |
| [docs/05.operations/catalog/06-observability/0039-alertmanager/guide.md](../../../05.operations/catalog/06-observability/0039-alertmanager/guide.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0039-alertmanager/policy.md](../../../05.operations/catalog/06-observability/0039-alertmanager/policy.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0039-alertmanager/runbook.md](../../../05.operations/catalog/06-observability/0039-alertmanager/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0040-alloy/guide.md](../../../05.operations/catalog/06-observability/0040-alloy/guide.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0040-alloy/policy.md](../../../05.operations/catalog/06-observability/0040-alloy/policy.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0040-alloy/runbook.md](../../../05.operations/catalog/06-observability/0040-alloy/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0041-grafana/guide.md](../../../05.operations/catalog/06-observability/0041-grafana/guide.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0041-grafana/policy.md](../../../05.operations/catalog/06-observability/0041-grafana/policy.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0041-grafana/runbook.md](../../../05.operations/catalog/06-observability/0041-grafana/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0042-lgtm-stack/guide.md](../../../05.operations/catalog/06-observability/0042-lgtm-stack/guide.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0043-loki/guide.md](../../../05.operations/catalog/06-observability/0043-loki/guide.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0043-loki/policy.md](../../../05.operations/catalog/06-observability/0043-loki/policy.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0043-loki/runbook.md](../../../05.operations/catalog/06-observability/0043-loki/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0044-optimization-hardening/guide.md](../../../05.operations/catalog/06-observability/0044-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0044-optimization-hardening/policy.md](../../../05.operations/catalog/06-observability/0044-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0044-optimization-hardening/runbook.md](../../../05.operations/catalog/06-observability/0044-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0045-prometheus/guide.md](../../../05.operations/catalog/06-observability/0045-prometheus/guide.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0045-prometheus/policy.md](../../../05.operations/catalog/06-observability/0045-prometheus/policy.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0045-prometheus/runbook.md](../../../05.operations/catalog/06-observability/0045-prometheus/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0046-pushgateway/guide.md](../../../05.operations/catalog/06-observability/0046-pushgateway/guide.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0046-pushgateway/policy.md](../../../05.operations/catalog/06-observability/0046-pushgateway/policy.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0046-pushgateway/runbook.md](../../../05.operations/catalog/06-observability/0046-pushgateway/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0047-pyroscope/guide.md](../../../05.operations/catalog/06-observability/0047-pyroscope/guide.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0047-pyroscope/policy.md](../../../05.operations/catalog/06-observability/0047-pyroscope/policy.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0047-pyroscope/runbook.md](../../../05.operations/catalog/06-observability/0047-pyroscope/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0048-telemetry-retention/policy.md](../../../05.operations/catalog/06-observability/0048-telemetry-retention/policy.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0049-tempo/guide.md](../../../05.operations/catalog/06-observability/0049-tempo/guide.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0049-tempo/policy.md](../../../05.operations/catalog/06-observability/0049-tempo/policy.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/0049-tempo/runbook.md](../../../05.operations/catalog/06-observability/0049-tempo/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/06-observability/README.md](../../../05.operations/catalog/06-observability/README.md) | folder index |
| [docs/05.operations/catalog/07-workflow/0050-airflow/guide.md](../../../05.operations/catalog/07-workflow/0050-airflow/guide.md) | Markdown reference |
| [docs/05.operations/catalog/07-workflow/0050-airflow/policy.md](../../../05.operations/catalog/07-workflow/0050-airflow/policy.md) | Markdown reference |
| [docs/05.operations/catalog/07-workflow/0050-airflow/runbook.md](../../../05.operations/catalog/07-workflow/0050-airflow/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/07-workflow/0051-airflow-dag-lifecycle/guide.md](../../../05.operations/catalog/07-workflow/0051-airflow-dag-lifecycle/guide.md) | Markdown reference |
| [docs/05.operations/catalog/07-workflow/0051-airflow-dag-lifecycle/policy.md](../../../05.operations/catalog/07-workflow/0051-airflow-dag-lifecycle/policy.md) | Markdown reference |
| [docs/05.operations/catalog/07-workflow/0053-n8n/guide.md](../../../05.operations/catalog/07-workflow/0053-n8n/guide.md) | Markdown reference |
| [docs/05.operations/catalog/07-workflow/0053-n8n/policy.md](../../../05.operations/catalog/07-workflow/0053-n8n/policy.md) | Markdown reference |
| [docs/05.operations/catalog/07-workflow/0053-n8n/runbook.md](../../../05.operations/catalog/07-workflow/0053-n8n/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/07-workflow/0054-optimization-hardening/guide.md](../../../05.operations/catalog/07-workflow/0054-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/catalog/07-workflow/0054-optimization-hardening/policy.md](../../../05.operations/catalog/07-workflow/0054-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/catalog/07-workflow/0054-optimization-hardening/runbook.md](../../../05.operations/catalog/07-workflow/0054-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/07-workflow/README.md](../../../05.operations/catalog/07-workflow/README.md) | folder index |
| [docs/05.operations/catalog/08-ai/0055-gpu-recovery/runbook.md](../../../05.operations/catalog/08-ai/0055-gpu-recovery/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/08-ai/0056-ollama/guide.md](../../../05.operations/catalog/08-ai/0056-ollama/guide.md) | Markdown reference |
| [docs/05.operations/catalog/08-ai/0056-ollama/policy.md](../../../05.operations/catalog/08-ai/0056-ollama/policy.md) | Markdown reference |
| [docs/05.operations/catalog/08-ai/0056-ollama/runbook.md](../../../05.operations/catalog/08-ai/0056-ollama/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/08-ai/0057-open-webui/guide.md](../../../05.operations/catalog/08-ai/0057-open-webui/guide.md) | Markdown reference |
| [docs/05.operations/catalog/08-ai/0057-open-webui/policy.md](../../../05.operations/catalog/08-ai/0057-open-webui/policy.md) | Markdown reference |
| [docs/05.operations/catalog/08-ai/0057-open-webui/runbook.md](../../../05.operations/catalog/08-ai/0057-open-webui/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/08-ai/0058-optimization-hardening/guide.md](../../../05.operations/catalog/08-ai/0058-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/catalog/08-ai/0058-optimization-hardening/policy.md](../../../05.operations/catalog/08-ai/0058-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/catalog/08-ai/0058-optimization-hardening/runbook.md](../../../05.operations/catalog/08-ai/0058-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/08-ai/0059-rag-workflow/guide.md](../../../05.operations/catalog/08-ai/0059-rag-workflow/guide.md) | Markdown reference |
| [docs/05.operations/catalog/08-ai/README.md](../../../05.operations/catalog/08-ai/README.md) | folder index |
| [docs/05.operations/catalog/09-tooling/0060-iac-deployment/policy.md](../../../05.operations/catalog/09-tooling/0060-iac-deployment/policy.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0061-k6/guide.md](../../../05.operations/catalog/09-tooling/0061-k6/guide.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0061-k6/policy.md](../../../05.operations/catalog/09-tooling/0061-k6/policy.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0061-k6/runbook.md](../../../05.operations/catalog/09-tooling/0061-k6/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0062-locust/guide.md](../../../05.operations/catalog/09-tooling/0062-locust/guide.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0062-locust/policy.md](../../../05.operations/catalog/09-tooling/0062-locust/policy.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0062-locust/runbook.md](../../../05.operations/catalog/09-tooling/0062-locust/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0063-optimization-hardening/guide.md](../../../05.operations/catalog/09-tooling/0063-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0063-optimization-hardening/policy.md](../../../05.operations/catalog/09-tooling/0063-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0063-optimization-hardening/runbook.md](../../../05.operations/catalog/09-tooling/0063-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0064-performance-testing/guide.md](../../../05.operations/catalog/09-tooling/0064-performance-testing/guide.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0064-performance-testing/policy.md](../../../05.operations/catalog/09-tooling/0064-performance-testing/policy.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0064-performance-testing/runbook.md](../../../05.operations/catalog/09-tooling/0064-performance-testing/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0065-registry/guide.md](../../../05.operations/catalog/09-tooling/0065-registry/guide.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0065-registry/policy.md](../../../05.operations/catalog/09-tooling/0065-registry/policy.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0065-registry/runbook.md](../../../05.operations/catalog/09-tooling/0065-registry/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0066-sonarqube/guide.md](../../../05.operations/catalog/09-tooling/0066-sonarqube/guide.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0066-sonarqube/policy.md](../../../05.operations/catalog/09-tooling/0066-sonarqube/policy.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0066-sonarqube/runbook.md](../../../05.operations/catalog/09-tooling/0066-sonarqube/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0067-syncthing/guide.md](../../../05.operations/catalog/09-tooling/0067-syncthing/guide.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0067-syncthing/policy.md](../../../05.operations/catalog/09-tooling/0067-syncthing/policy.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0067-syncthing/runbook.md](../../../05.operations/catalog/09-tooling/0067-syncthing/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0068-terraform/guide.md](../../../05.operations/catalog/09-tooling/0068-terraform/guide.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0068-terraform/policy.md](../../../05.operations/catalog/09-tooling/0068-terraform/policy.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0068-terraform/runbook.md](../../../05.operations/catalog/09-tooling/0068-terraform/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0069-terrakube/guide.md](../../../05.operations/catalog/09-tooling/0069-terrakube/guide.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0069-terrakube/policy.md](../../../05.operations/catalog/09-tooling/0069-terrakube/policy.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/0069-terrakube/runbook.md](../../../05.operations/catalog/09-tooling/0069-terrakube/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/09-tooling/README.md](../../../05.operations/catalog/09-tooling/README.md) | folder index |
| [docs/05.operations/catalog/10-communication/0070-mail/guide.md](../../../05.operations/catalog/10-communication/0070-mail/guide.md) | Markdown reference |
| [docs/05.operations/catalog/10-communication/0070-mail/policy.md](../../../05.operations/catalog/10-communication/0070-mail/policy.md) | Markdown reference |
| [docs/05.operations/catalog/10-communication/0070-mail/runbook.md](../../../05.operations/catalog/10-communication/0070-mail/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/10-communication/README.md](../../../05.operations/catalog/10-communication/README.md) | folder index |
| [docs/05.operations/catalog/11-laboratory/0071-homer-dashboard/guide.md](../../../05.operations/catalog/11-laboratory/0071-homer-dashboard/guide.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0071-homer-dashboard/policy.md](../../../05.operations/catalog/11-laboratory/0071-homer-dashboard/policy.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0071-homer-dashboard/runbook.md](../../../05.operations/catalog/11-laboratory/0071-homer-dashboard/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0072-dozzle/guide.md](../../../05.operations/catalog/11-laboratory/0072-dozzle/guide.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0072-dozzle/policy.md](../../../05.operations/catalog/11-laboratory/0072-dozzle/policy.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0072-dozzle/runbook.md](../../../05.operations/catalog/11-laboratory/0072-dozzle/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0073-open-notebook/guide.md](../../../05.operations/catalog/11-laboratory/0073-open-notebook/guide.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0073-open-notebook/policy.md](../../../05.operations/catalog/11-laboratory/0073-open-notebook/policy.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0073-open-notebook/runbook.md](../../../05.operations/catalog/11-laboratory/0073-open-notebook/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0074-optimization-hardening/guide.md](../../../05.operations/catalog/11-laboratory/0074-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0074-optimization-hardening/policy.md](../../../05.operations/catalog/11-laboratory/0074-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0074-optimization-hardening/runbook.md](../../../05.operations/catalog/11-laboratory/0074-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0075-portainer/guide.md](../../../05.operations/catalog/11-laboratory/0075-portainer/guide.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0075-portainer/policy.md](../../../05.operations/catalog/11-laboratory/0075-portainer/policy.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0075-portainer/runbook.md](../../../05.operations/catalog/11-laboratory/0075-portainer/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0076-redisinsight/guide.md](../../../05.operations/catalog/11-laboratory/0076-redisinsight/guide.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0076-redisinsight/policy.md](../../../05.operations/catalog/11-laboratory/0076-redisinsight/policy.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/0076-redisinsight/runbook.md](../../../05.operations/catalog/11-laboratory/0076-redisinsight/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/11-laboratory/README.md](../../../05.operations/catalog/11-laboratory/README.md) | folder index |
| [docs/05.operations/catalog/12-infra-net/0077-ip-address-management/guide.md](../../../05.operations/catalog/12-infra-net/0077-ip-address-management/guide.md) | Markdown reference |
| [docs/05.operations/catalog/12-infra-net/0077-ip-address-management/policy.md](../../../05.operations/catalog/12-infra-net/0077-ip-address-management/policy.md) | Markdown reference |
| [docs/05.operations/catalog/12-infra-net/0077-ip-address-management/runbook.md](../../../05.operations/catalog/12-infra-net/0077-ip-address-management/runbook.md) | Markdown reference |
| [docs/05.operations/catalog/12-infra-net/README.md](../../../05.operations/catalog/12-infra-net/README.md) | folder index |
| [docs/05.operations/catalog/README.md](../../../05.operations/catalog/README.md) | folder index |
| [docs/05.operations/incidents/README.md](../../../05.operations/incidents/README.md) | folder index |

### Reference and template docs

| Path | Role |
| --- | --- |
| [docs/90.references/README.md](../../README.md) | folder index |
| [docs/90.references/audits/0019-readme/README.md](../../audits/0019-readme/README.md) | folder index |
| [docs/90.references/audits/0020-agent-instructions-catalog-vibe-models/README.md](../../audits/0020-agent-instructions-catalog-vibe-models/README.md) | folder index |
| [docs/90.references/audits/0021-automation-candidates/README.md](../../audits/0021-automation-candidates/README.md) | folder index |
| [docs/90.references/audits/0022-compose-infrastructure-operations-readiness/README.md](../../audits/0022-compose-infrastructure-operations-readiness/README.md) | folder index |
| [docs/90.references/audits/0023-frontmatter-semantic-inventory/README.md](../../audits/0023-frontmatter-semantic-inventory/README.md) | folder index |
| [docs/90.references/audits/0024-frontmatter-template-readme-implementation/README.md](../../audits/0024-frontmatter-template-readme-implementation/README.md) | folder index |
| [docs/90.references/audits/0025-harness-engineering-implementation/README.md](../../audits/0025-harness-engineering-implementation/README.md) | folder index |
| [docs/90.references/audits/0026-implementation-overview/README.md](../../audits/0026-implementation-overview/README.md) | folder index |
| [docs/90.references/audits/0027-loop-engineering-implementation/README.md](../../audits/0027-loop-engineering-implementation/README.md) | folder index |
| [docs/90.references/audits/0028-provider-harness-loop-implementation/README.md](../../audits/0028-provider-harness-loop-implementation/README.md) | folder index |
| [docs/90.references/audits/0029-sdlc-document-contracts-implementation/README.md](../../audits/0029-sdlc-document-contracts-implementation/README.md) | folder index |
| [docs/90.references/audits/0030-sdlc-quality-formatting-implementation/README.md](../../audits/0030-sdlc-quality-formatting-implementation/README.md) | folder index |
| [docs/90.references/audits/0031-security-framework-maturity/README.md](../../audits/0031-security-framework-maturity/README.md) | folder index |
| [docs/90.references/audits/0032-workspace-rules-environment-implementation/README.md](../../audits/0032-workspace-rules-environment-implementation/README.md) | folder index |
| [docs/90.references/audits/0097-compose-domain-defect-register/README.md](../../audits/0097-compose-domain-defect-register/README.md) | folder index |
| [docs/90.references/audits/README.md](../../audits/README.md) | folder index |
| [docs/90.references/data/0059-compose-profile-service-coverage/README.md](../0059-compose-profile-service-coverage/README.md) | folder index |
| [docs/90.references/data/0060-image-version-interpretation/README.md](../0060-image-version-interpretation/README.md) | folder index |
| [docs/90.references/data/0061-tech-stack-version-provenance/README.md](../0061-tech-stack-version-provenance/README.md) | folder index |
| [docs/90.references/data/0064-agent-output-eval-fixtures/README.md](../0064-agent-output-eval-fixtures/README.md) | folder index |
| [docs/90.references/data/0065-audit-implementation-matrix/README.md](../0065-audit-implementation-matrix/README.md) | folder index |
| [docs/90.references/data/0066-foundation-summary/README.md](../0066-foundation-summary/README.md) | folder index |
| [docs/90.references/data/0067-foundation/README.md](../0067-foundation/README.md) | folder index |
| [docs/90.references/data/0067-foundation/data.yaml](../0067-foundation/data.yaml) | YAML config |
| [docs/90.references/data/0071-github-actions-control-plane-observation/README.md](../0071-github-actions-control-plane-observation/README.md) | folder index |
| [docs/90.references/data/0071-github-actions-control-plane-observation/data.yaml](../0071-github-actions-control-plane-observation/data.yaml) | YAML config |
| [docs/90.references/data/0072-provider-hook-parity-matrix/README.md](../0072-provider-hook-parity-matrix/README.md) | folder index |
| [docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md](../0076-llm-wiki-stage-category-coverage/README.md) | folder index |
| [docs/90.references/data/0078-security-automation-readiness/README.md](../0078-security-automation-readiness/README.md) | folder index |
| [docs/90.references/data/0079-supply-chain-sample-service/README.md](../0079-supply-chain-sample-service/README.md) | folder index |
| [docs/90.references/data/README.md](../README.md) | folder index |
| [docs/90.references/research/0002-agentic-engineering-research-pack/README.md](../../research/0002-agentic-engineering-research-pack/README.md) | folder index |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0001-agent-instructions-vibe-coding.md](../../research/0002-agentic-engineering-research-pack/m0001-agent-instructions-vibe-coding.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0002-agent-model-selection.md](../../research/0002-agentic-engineering-research-pack/m0002-agent-model-selection.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0003-ai-agent-catalogs.md](../../research/0002-agentic-engineering-research-pack/m0003-ai-agent-catalogs.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0004-automation-pipeline-workflow.md](../../research/0002-agentic-engineering-research-pack/m0004-automation-pipeline-workflow.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0005-docker-compose-infrastructure.md](../../research/0002-agentic-engineering-research-pack/m0005-docker-compose-infrastructure.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0006-document-metadata-lifecycle.md](../../research/0002-agentic-engineering-research-pack/m0006-document-metadata-lifecycle.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0007-documentation-architecture.md](../../research/0002-agentic-engineering-research-pack/m0007-documentation-architecture.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0008-harness-engineering.md](../../research/0002-agentic-engineering-research-pack/m0008-harness-engineering.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0009-llm-wiki-system.md](../../research/0002-agentic-engineering-research-pack/m0009-llm-wiki-system.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0010-loop-engineering.md](../../research/0002-agentic-engineering-research-pack/m0010-loop-engineering.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0011-memory-hierarchy.md](../../research/0002-agentic-engineering-research-pack/m0011-memory-hierarchy.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0012-provider-implementation-comparison.md](../../research/0002-agentic-engineering-research-pack/m0012-provider-implementation-comparison.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0013-provider-model-landscape.md](../../research/0002-agentic-engineering-research-pack/m0013-provider-model-landscape.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0014-quality-ci-formatting.md](../../research/0002-agentic-engineering-research-pack/m0014-quality-ci-formatting.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0015-scope-application-matrix.md](../../research/0002-agentic-engineering-research-pack/m0015-scope-application-matrix.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0016-sdlc-document-roles.md](../../research/0002-agentic-engineering-research-pack/m0016-sdlc-document-roles.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0017-security-governance.md](../../research/0002-agentic-engineering-research-pack/m0017-security-governance.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0018-spec-driven-sdlc.md](../../research/0002-agentic-engineering-research-pack/m0018-spec-driven-sdlc.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0019-verification-validation.md](../../research/0002-agentic-engineering-research-pack/m0019-verification-validation.md) | Markdown reference |
| [docs/90.references/research/0002-agentic-engineering-research-pack/m0020-workspace-baseline.md](../../research/0002-agentic-engineering-research-pack/m0020-workspace-baseline.md) | Markdown reference |
| [docs/90.references/research/0081-roadmap/README.md](../../research/0081-roadmap/README.md) | folder index |
| [docs/90.references/research/0084-github-actions-platform/README.md](../../research/0084-github-actions-platform/README.md) | folder index |
| [docs/90.references/research/0084-github-actions-platform/m0001-platform-mechanics.md](../../research/0084-github-actions-platform/m0001-platform-mechanics.md) | Markdown reference |
| [docs/90.references/research/0085-workspace-engineering-main-baseline-assessment/README.md](../../research/0085-workspace-engineering-main-baseline-assessment/README.md) | folder index |
| [docs/90.references/research/0085-workspace-engineering-main-baseline-assessment/m0001-request-scope.md](../../research/0085-workspace-engineering-main-baseline-assessment/m0001-request-scope.md) | Markdown reference |
| [docs/90.references/research/README.md](../../research/README.md) | folder index |
| [docs/99.templates/README.md](../../../99.templates/README.md) | folder index |
| [docs/99.templates/contracts/document-frontmatter.schema.json](../../../99.templates/contracts/document-frontmatter.schema.json) | JSON registry |
| [docs/99.templates/contracts/document-profile.schema.json](../../../99.templates/contracts/document-profile.schema.json) | JSON registry |
| [docs/99.templates/registry.json](../../../99.templates/registry.json) | JSON registry |
| [docs/99.templates/templates/README.md](../../../99.templates/templates/README.md) | folder index |
| [docs/99.templates/templates/architecture/decision.template.md](../../../99.templates/templates/architecture/decision.template.md) | Markdown reference |
| [docs/99.templates/templates/architecture/description.template.md](../../../99.templates/templates/architecture/description.template.md) | Markdown reference |
| [docs/99.templates/templates/archive/migration.template.md](../../../99.templates/templates/archive/migration.template.md) | Markdown reference |
| [docs/99.templates/templates/archive/tombstone.template.md](../../../99.templates/templates/archive/tombstone.template.md) | Markdown reference |
| [docs/99.templates/templates/common/readme-category.template.md](../../../99.templates/templates/common/readme-category.template.md) | Markdown reference |
| [docs/99.templates/templates/common/readme-documentation.template.md](../../../99.templates/templates/common/readme-documentation.template.md) | Markdown reference |
| [docs/99.templates/templates/common/readme-domain.template.md](../../../99.templates/templates/common/readme-domain.template.md) | Markdown reference |
| [docs/99.templates/templates/common/readme-package.template.md](../../../99.templates/templates/common/readme-package.template.md) | Markdown reference |
| [docs/99.templates/templates/common/readme-repository.template.md](../../../99.templates/templates/common/readme-repository.template.md) | Markdown reference |
| [docs/99.templates/templates/common/readme-runtime-governance.template.md](../../../99.templates/templates/common/readme-runtime-governance.template.md) | Markdown reference |
| [docs/99.templates/templates/common/readme-stage.template.md](../../../99.templates/templates/common/readme-stage.template.md) | Markdown reference |
| [docs/99.templates/templates/governance/contract.template.md](../../../99.templates/templates/governance/contract.template.md) | Markdown reference |
| [docs/99.templates/templates/governance/control.template.md](../../../99.templates/templates/governance/control.template.md) | Markdown reference |
| [docs/99.templates/templates/governance/provider.template.md](../../../99.templates/templates/governance/provider.template.md) | Markdown reference |
| [docs/99.templates/templates/governance/role.template.md](../../../99.templates/templates/governance/role.template.md) | Markdown reference |
| [docs/99.templates/templates/governance/rule.template.md](../../../99.templates/templates/governance/rule.template.md) | Markdown reference |
| [docs/99.templates/templates/governance/skill.template.md](../../../99.templates/templates/governance/skill.template.md) | Markdown reference |
| [docs/99.templates/templates/operations/guide.template.md](../../../99.templates/templates/operations/guide.template.md) | Markdown reference |
| [docs/99.templates/templates/operations/incident.template.md](../../../99.templates/templates/operations/incident.template.md) | Markdown reference |
| [docs/99.templates/templates/operations/policy.template.md](../../../99.templates/templates/operations/policy.template.md) | Markdown reference |
| [docs/99.templates/templates/operations/postmortem.template.md](../../../99.templates/templates/operations/postmortem.template.md) | Markdown reference |
| [docs/99.templates/templates/operations/runbook.template.md](../../../99.templates/templates/operations/runbook.template.md) | Markdown reference |
| [docs/99.templates/templates/references/audit-pack.template.md](../../../99.templates/templates/references/audit-pack.template.md) | Markdown reference |
| [docs/99.templates/templates/references/audit.template.md](../../../99.templates/templates/references/audit.template.md) | Markdown reference |
| [docs/99.templates/templates/references/data-pack.template.md](../../../99.templates/templates/references/data-pack.template.md) | Markdown reference |
| [docs/99.templates/templates/references/data.template.md](../../../99.templates/templates/references/data.template.md) | Markdown reference |
| [docs/99.templates/templates/references/research-pack.template.md](../../../99.templates/templates/references/research-pack.template.md) | Markdown reference |
| [docs/99.templates/templates/references/research.template.md](../../../99.templates/templates/references/research.template.md) | Markdown reference |
| [docs/99.templates/templates/requirements/requirement-package.template.md](../../../99.templates/templates/requirements/requirement-package.template.md) | Markdown reference |
| [docs/99.templates/templates/runtime/claude-agent.template.md](../../../99.templates/templates/runtime/claude-agent.template.md) | Markdown reference |
| [docs/99.templates/templates/runtime/codex-agent.template.toml](../../../99.templates/templates/runtime/codex-agent.template.toml) | source path |
| [docs/99.templates/templates/specs/contracts/data-model.template.md](../../../99.templates/templates/specs/contracts/data-model.template.md) | Markdown reference |
| [docs/99.templates/templates/specs/contracts/openapi.template.yaml](../../../99.templates/templates/specs/contracts/openapi.template.yaml) | YAML config |
| [docs/99.templates/templates/specs/contracts/schema.template.graphql](../../../99.templates/templates/specs/contracts/schema.template.graphql) | source path |
| [docs/99.templates/templates/specs/contracts/service.template.proto](../../../99.templates/templates/specs/contracts/service.template.proto) | source path |
| [docs/99.templates/templates/specs/plan.template.md](../../../99.templates/templates/specs/plan.template.md) | Markdown reference |
| [docs/99.templates/templates/specs/spec.template.md](../../../99.templates/templates/specs/spec.template.md) | Markdown reference |
| [docs/99.templates/templates/specs/task.template.md](../../../99.templates/templates/specs/task.template.md) | Markdown reference |
| [docs/README.md](../../../README.md) | folder index |

### Infrastructure source

| Path | Role |
| --- | --- |
| [infra/01-gateway/README.md](../../../../infra/01-gateway/README.md) | folder index |
| [infra/01-gateway/nginx/README.md](../../../../infra/01-gateway/nginx/README.md) | folder index |
| [infra/01-gateway/nginx/config/nginx.conf](../../../../infra/01-gateway/nginx/config/nginx.conf) | source path |
| [infra/01-gateway/nginx/docker-compose.yml](../../../../infra/01-gateway/nginx/docker-compose.yml) | YAML config |
| [infra/01-gateway/traefik/README.md](../../../../infra/01-gateway/traefik/README.md) | folder index |
| [infra/01-gateway/traefik/config/README.md](../../../../infra/01-gateway/traefik/config/README.md) | folder index |
| [infra/01-gateway/traefik/config/traefik.yml](../../../../infra/01-gateway/traefik/config/traefik.yml) | YAML config |
| [infra/01-gateway/traefik/docker-compose.yml](../../../../infra/01-gateway/traefik/docker-compose.yml) | YAML config |
| [infra/01-gateway/traefik/dynamic/README.md](../../../../infra/01-gateway/traefik/dynamic/README.md) | folder index |
| [infra/01-gateway/traefik/dynamic/adminer-k3d.yaml](../../../../infra/01-gateway/traefik/dynamic/adminer-k3d.yaml) | YAML config |
| [infra/01-gateway/traefik/dynamic/argocd-k3d.yaml](../../../../infra/01-gateway/traefik/dynamic/argocd-k3d.yaml) | YAML config |
| [infra/01-gateway/traefik/dynamic/headlamp-k3d.yaml](../../../../infra/01-gateway/traefik/dynamic/headlamp-k3d.yaml) | YAML config |
| [infra/01-gateway/traefik/dynamic/kiali-k3d.yaml](../../../../infra/01-gateway/traefik/dynamic/kiali-k3d.yaml) | YAML config |
| [infra/01-gateway/traefik/dynamic/middleware.yml](../../../../infra/01-gateway/traefik/dynamic/middleware.yml) | YAML config |
| [infra/01-gateway/traefik/dynamic/rollouts-k3d.yaml](../../../../infra/01-gateway/traefik/dynamic/rollouts-k3d.yaml) | YAML config |
| [infra/01-gateway/traefik/dynamic/tls.yaml](../../../../infra/01-gateway/traefik/dynamic/tls.yaml) | YAML config |
| [infra/02-auth/README.md](../../../../infra/02-auth/README.md) | folder index |
| [infra/02-auth/keycloak/Dockerfile](../../../../infra/02-auth/keycloak/Dockerfile) | source path |
| [infra/02-auth/keycloak/README.md](../../../../infra/02-auth/keycloak/README.md) | folder index |
| [infra/02-auth/keycloak/docker-compose.yml](../../../../infra/02-auth/keycloak/docker-compose.yml) | YAML config |
| [infra/02-auth/oauth2-proxy/Dockerfile](../../../../infra/02-auth/oauth2-proxy/Dockerfile) | source path |
| [infra/02-auth/oauth2-proxy/README.md](../../../../infra/02-auth/oauth2-proxy/README.md) | folder index |
| [infra/02-auth/oauth2-proxy/docker-compose.yml](../../../../infra/02-auth/oauth2-proxy/docker-compose.yml) | YAML config |
| [infra/02-auth/oauth2-proxy/docker-entrypoint.dev.sh](../../../../infra/02-auth/oauth2-proxy/docker-entrypoint.dev.sh) | script |
| [infra/02-auth/oauth2-proxy/docker-entrypoint.sh](../../../../infra/02-auth/oauth2-proxy/docker-entrypoint.sh) | script |
| [infra/03-security/README.md](../../../../infra/03-security/README.md) | folder index |
| [infra/03-security/vault/README.md](../../../../infra/03-security/vault/README.md) | folder index |
| [infra/03-security/vault/docker-compose.yml](../../../../infra/03-security/vault/docker-compose.yml) | YAML config |
| [infra/04-data/README.md](../../../../infra/04-data/README.md) | folder index |
| [infra/04-data/analytics/README.md](../../../../infra/04-data/analytics/README.md) | folder index |
| [infra/04-data/analytics/influxdb/README.md](../../../../infra/04-data/analytics/influxdb/README.md) | folder index |
| [infra/04-data/analytics/influxdb/docker-compose.yml](../../../../infra/04-data/analytics/influxdb/docker-compose.yml) | YAML config |
| [infra/04-data/analytics/ksql/README.md](../../../../infra/04-data/analytics/ksql/README.md) | folder index |
| [infra/04-data/analytics/ksql/docker-compose.yml](../../../../infra/04-data/analytics/ksql/docker-compose.yml) | YAML config |
| [infra/04-data/analytics/opensearch/Dockerfile](../../../../infra/04-data/analytics/opensearch/Dockerfile) | source path |
| [infra/04-data/analytics/opensearch/README.md](../../../../infra/04-data/analytics/opensearch/README.md) | folder index |
| [infra/04-data/analytics/opensearch/docker-compose.yml](../../../../infra/04-data/analytics/opensearch/docker-compose.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch-dashboards/config/opensearch_dashboards.yml](../../../../infra/04-data/analytics/opensearch/opensearch-dashboards/config/opensearch_dashboards.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/action_groups.yml](../../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/action_groups.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/config.yml](../../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/config.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/internal_users.template.yml](../../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/internal_users.template.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/roles.yml](../../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/roles.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/roles_mapping.yml](../../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/roles_mapping.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/tenants.yml](../../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/tenants.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch.yml](../../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt](../../../../infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt) | text entrypoint |
| [infra/04-data/analytics/opensearch/opensearch/opensearch-entrypoint.sh](../../../../infra/04-data/analytics/opensearch/opensearch/opensearch-entrypoint.sh) | script |
| [infra/04-data/analytics/warehouses/README.md](../../../../infra/04-data/analytics/warehouses/README.md) | folder index |
| [infra/04-data/analytics/warehouses/docker-compose.yml](../../../../infra/04-data/analytics/warehouses/docker-compose.yml) | YAML config |
| [infra/04-data/cache-and-kv/README.md](../../../../infra/04-data/cache-and-kv/README.md) | folder index |
| [infra/04-data/cache-and-kv/valkey-cluster/README.md](../../../../infra/04-data/cache-and-kv/valkey-cluster/README.md) | folder index |
| [infra/04-data/cache-and-kv/valkey-cluster/config/valkey.conf](../../../../infra/04-data/cache-and-kv/valkey-cluster/config/valkey.conf) | source path |
| [infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml](../../../../infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml) | YAML config |
| [infra/04-data/cache-and-kv/valkey-cluster/scripts/valkey-cluster-init.sh](../../../../infra/04-data/cache-and-kv/valkey-cluster/scripts/valkey-cluster-init.sh) | script |
| [infra/04-data/cache-and-kv/valkey-cluster/scripts/valkey-start.sh](../../../../infra/04-data/cache-and-kv/valkey-cluster/scripts/valkey-start.sh) | script |
| [infra/04-data/lake-and-object/README.md](../../../../infra/04-data/lake-and-object/README.md) | folder index |
| [infra/04-data/lake-and-object/minio/README.md](../../../../infra/04-data/lake-and-object/minio/README.md) | folder index |
| [infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml](../../../../infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml) | YAML config |
| [infra/04-data/lake-and-object/minio/docker-compose.yml](../../../../infra/04-data/lake-and-object/minio/docker-compose.yml) | YAML config |
| [infra/04-data/lake-and-object/seaweedfs/README.md](../../../../infra/04-data/lake-and-object/seaweedfs/README.md) | folder index |
| [infra/04-data/lake-and-object/seaweedfs/docker-compose.yml](../../../../infra/04-data/lake-and-object/seaweedfs/docker-compose.yml) | YAML config |
| [infra/04-data/nosql/README.md](../../../../infra/04-data/nosql/README.md) | folder index |
| [infra/04-data/nosql/cassandra/README.md](../../../../infra/04-data/nosql/cassandra/README.md) | folder index |
| [infra/04-data/nosql/cassandra/docker-compose.yml](../../../../infra/04-data/nosql/cassandra/docker-compose.yml) | YAML config |
| [infra/04-data/nosql/couchdb/README.md](../../../../infra/04-data/nosql/couchdb/README.md) | folder index |
| [infra/04-data/nosql/couchdb/docker-compose.yml](../../../../infra/04-data/nosql/couchdb/docker-compose.yml) | YAML config |
| [infra/04-data/nosql/mongodb/README.md](../../../../infra/04-data/nosql/mongodb/README.md) | folder index |
| [infra/04-data/nosql/mongodb/docker-compose.yml](../../../../infra/04-data/nosql/mongodb/docker-compose.yml) | YAML config |
| [infra/04-data/operational/README.md](../../../../infra/04-data/operational/README.md) | folder index |
| [infra/04-data/operational/mng-db/README.md](../../../../infra/04-data/operational/mng-db/README.md) | folder index |
| [infra/04-data/operational/mng-db/docker-compose.yml](../../../../infra/04-data/operational/mng-db/docker-compose.yml) | YAML config |
| [infra/04-data/operational/supabase/README.md](../../../../infra/04-data/operational/supabase/README.md) | folder index |
| [infra/04-data/operational/supabase/docker-compose.yml](../../../../infra/04-data/operational/supabase/docker-compose.yml) | YAML config |
| [infra/04-data/relational/README.md](../../../../infra/04-data/relational/README.md) | folder index |
| [infra/04-data/relational/postgresql-cluster/README.md](../../../../infra/04-data/relational/postgresql-cluster/README.md) | folder index |
| [infra/04-data/relational/postgresql-cluster/docker-compose.yml](../../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml) | YAML config |
| [infra/04-data/relational/postgresql-cluster/scripts/spilo-entrypoint-with-secrets.sh](../../../../infra/04-data/relational/postgresql-cluster/scripts/spilo-entrypoint-with-secrets.sh) | script |
| [infra/04-data/specialized/README.md](../../../../infra/04-data/specialized/README.md) | folder index |
| [infra/04-data/specialized/neo4j/README.md](../../../../infra/04-data/specialized/neo4j/README.md) | folder index |
| [infra/04-data/specialized/neo4j/docker-compose.yml](../../../../infra/04-data/specialized/neo4j/docker-compose.yml) | YAML config |
| [infra/04-data/specialized/neo4j/scripts/neo4j-entrypoint-with-secrets.sh](../../../../infra/04-data/specialized/neo4j/scripts/neo4j-entrypoint-with-secrets.sh) | script |
| [infra/04-data/specialized/qdrant/README.md](../../../../infra/04-data/specialized/qdrant/README.md) | folder index |
| [infra/04-data/specialized/qdrant/docker-compose.yml](../../../../infra/04-data/specialized/qdrant/docker-compose.yml) | YAML config |
| [infra/05-messaging/README.md](../../../../infra/05-messaging/README.md) | folder index |
| [infra/05-messaging/kafka/README.md](../../../../infra/05-messaging/kafka/README.md) | folder index |
| [infra/05-messaging/kafka/docker-compose.yml](../../../../infra/05-messaging/kafka/docker-compose.yml) | YAML config |
| [infra/05-messaging/kafka/jmx-exporter/kafka-config.yaml](../../../../infra/05-messaging/kafka/jmx-exporter/kafka-config.yaml) | YAML config |
| [infra/05-messaging/kafka/kafbat-ui/dynamic_config.template.yaml](../../../../infra/05-messaging/kafka/kafbat-ui/dynamic_config.template.yaml) | YAML config |
| [infra/05-messaging/rabbitmq/README.md](../../../../infra/05-messaging/rabbitmq/README.md) | folder index |
| [infra/05-messaging/rabbitmq/docker-compose.yml](../../../../infra/05-messaging/rabbitmq/docker-compose.yml) | YAML config |
| [infra/06-observability/README.md](../../../../infra/06-observability/README.md) | folder index |
| [infra/06-observability/alertmanager/README.md](../../../../infra/06-observability/alertmanager/README.md) | folder index |
| [infra/06-observability/alertmanager/config/config.yml](../../../../infra/06-observability/alertmanager/config/config.yml) | YAML config |
| [infra/06-observability/alloy/README.md](../../../../infra/06-observability/alloy/README.md) | folder index |
| [infra/06-observability/docker-compose.yml](../../../../infra/06-observability/docker-compose.yml) | YAML config |
| [infra/06-observability/grafana/README.md](../../../../infra/06-observability/grafana/README.md) | folder index |
| [infra/06-observability/grafana/dashboards/Applications/airflow-dag-overview.json](../../../../infra/06-observability/grafana/dashboards/Applications/airflow-dag-overview.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/airflow-dag.json](../../../../infra/06-observability/grafana/dashboards/Applications/airflow-dag.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/airflow-monitoring.json](../../../../infra/06-observability/grafana/dashboards/Applications/airflow-monitoring.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/airflow-operators.json](../../../../infra/06-observability/grafana/dashboards/Applications/airflow-operators.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/airflow3-monitoring.json](../../../../infra/06-observability/grafana/dashboards/Applications/airflow3-monitoring.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/argocd-app-overview.json](../../../../infra/06-observability/grafana/dashboards/Applications/argocd-app-overview.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/argocd-notifications.json](../../../../infra/06-observability/grafana/dashboards/Applications/argocd-notifications.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/argocd-operational.json](../../../../infra/06-observability/grafana/dashboards/Applications/argocd-operational.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/argocd.json](../../../../infra/06-observability/grafana/dashboards/Applications/argocd.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/n8n-system-health.json](../../../../infra/06-observability/grafana/dashboards/Applications/n8n-system-health.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/n8n-workflow-analytics.json](../../../../infra/06-observability/grafana/dashboards/Applications/n8n-workflow-analytics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/ollama.json](../../../../infra/06-observability/grafana/dashboards/Applications/ollama.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/vllm-monitoring.json](../../../../infra/06-observability/grafana/dashboards/Applications/vllm-monitoring.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Gateway/traefik.json](../../../../infra/06-observability/grafana/dashboards/Gateway/traefik.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/cadvisor.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/cadvisor.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/docker-metrics.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/docker-metrics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/docker-monitoring.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/docker-monitoring.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/docker-registry.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/docker-registry.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/etcd.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/etcd.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/haproxy.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/haproxy.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/k6.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/k6.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/kafka-exporter.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/kafka-exporter.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/kafka-overview.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/kafka-overview.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/minio-bucket.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/minio-bucket.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/minio.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/minio.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/neo4j-operations.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/neo4j-operations.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/neo4j.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/neo4j.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/opensearch.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/opensearch.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/postgres-exporter.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/postgres-exporter.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/postgres.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/postgres.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/qdrant.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/qdrant.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/redis-overview.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/redis-overview.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/valkey-overview.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/valkey-overview.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/vault-hcp.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/vault-hcp.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/vaults.json](../../../../infra/06-observability/grafana/dashboards/Infrastructure/vaults.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/argo-rollouts.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/argo-rollouts.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/cluster-policy-report.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/cluster-policy-report.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/external-secrets.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/external-secrets.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/istio-control-plane.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/istio-control-plane.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k3s-monitoring.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/k3s-monitoring.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-apiserver.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-apiserver.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-app-metrics.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-app-metrics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-autoscaler.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-autoscaler.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-cluster-monitoring-1.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-cluster-monitoring-1.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-cluster.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-cluster.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-dashboard-1.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-dashboard-1.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-deployment-metrics.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-deployment-metrics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-nginx-ingress.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-nginx-ingress.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-nodes.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-nodes.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-pod-metrics.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-pod-metrics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-storage.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-storage.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-views-pods.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-views-pods.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/kube-state-metrics.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/kube-state-metrics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/kubernetes-compute-resources.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/kubernetes-compute-resources.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/policy-report.json](../../../../infra/06-observability/grafana/dashboards/Kubernetes/policy-report.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/alertmanager.json](../../../../infra/06-observability/grafana/dashboards/Observability/alertmanager.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/loki-dashboard.json](../../../../infra/06-observability/grafana/dashboards/Observability/loki-dashboard.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/loki-global.json](../../../../infra/06-observability/grafana/dashboards/Observability/loki-global.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/loki-metrics.json](../../../../infra/06-observability/grafana/dashboards/Observability/loki-metrics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/otel-collector.json](../../../../infra/06-observability/grafana/dashboards/Observability/otel-collector.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/otel-tempo.json](../../../../infra/06-observability/grafana/dashboards/Observability/otel-tempo.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/prometheus.json](../../../../infra/06-observability/grafana/dashboards/Observability/prometheus.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Security/keycloak.json](../../../../infra/06-observability/grafana/dashboards/Security/keycloak.json) | JSON registry |
| [infra/06-observability/grafana/provisioning/dashboards/dashboards.yml](../../../../infra/06-observability/grafana/provisioning/dashboards/dashboards.yml) | YAML config |
| [infra/06-observability/grafana/provisioning/datasources/datasource.yml](../../../../infra/06-observability/grafana/provisioning/datasources/datasource.yml) | YAML config |
| [infra/06-observability/loki/Dockerfile](../../../../infra/06-observability/loki/Dockerfile) | source path |
| [infra/06-observability/loki/README.md](../../../../infra/06-observability/loki/README.md) | folder index |
| [infra/06-observability/loki/config/loki-config.yaml](../../../../infra/06-observability/loki/config/loki-config.yaml) | YAML config |
| [infra/06-observability/loki/docker-entrypoint.sh](../../../../infra/06-observability/loki/docker-entrypoint.sh) | script |
| [infra/06-observability/prometheus/README.md](../../../../infra/06-observability/prometheus/README.md) | folder index |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.k8s.yml](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.k8s.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.keycloak.yml](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.keycloak.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.auth.yml](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.auth.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.datastores.yml](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.datastores.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.gateway.yml](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.gateway.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.infra.yml](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.infra.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.messaging.yml](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.messaging.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.observability.yml](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.observability.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.prometheus.yml](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.prometheus.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.search.yml](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.search.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.vault.yml](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.vault.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/recording_rules.yml](../../../../infra/06-observability/prometheus/config/alert_rules/recording_rules.yml) | YAML config |
| [infra/06-observability/prometheus/config/prometheus.dev.yml](../../../../infra/06-observability/prometheus/config/prometheus.dev.yml) | YAML config |
| [infra/06-observability/prometheus/config/prometheus.yml](../../../../infra/06-observability/prometheus/config/prometheus.yml) | YAML config |
| [infra/06-observability/pushgateway/README.md](../../../../infra/06-observability/pushgateway/README.md) | folder index |
| [infra/06-observability/pyroscope/README.md](../../../../infra/06-observability/pyroscope/README.md) | folder index |
| [infra/06-observability/pyroscope/config/pyroscope.yaml](../../../../infra/06-observability/pyroscope/config/pyroscope.yaml) | YAML config |
| [infra/06-observability/tempo/Dockerfile](../../../../infra/06-observability/tempo/Dockerfile) | source path |
| [infra/06-observability/tempo/README.md](../../../../infra/06-observability/tempo/README.md) | folder index |
| [infra/06-observability/tempo/config/tempo.yaml](../../../../infra/06-observability/tempo/config/tempo.yaml) | YAML config |
| [infra/06-observability/tempo/docker-entrypoint.sh](../../../../infra/06-observability/tempo/docker-entrypoint.sh) | script |
| [infra/07-workflow/README.md](../../../../infra/07-workflow/README.md) | folder index |
| [infra/07-workflow/airflow/README.md](../../../../infra/07-workflow/airflow/README.md) | folder index |
| [infra/07-workflow/airflow/config/statsd_mapping.yml](../../../../infra/07-workflow/airflow/config/statsd_mapping.yml) | YAML config |
| [infra/07-workflow/airflow/docker-compose.yml](../../../../infra/07-workflow/airflow/docker-compose.yml) | YAML config |
| [infra/07-workflow/n8n/Dockerfile](../../../../infra/07-workflow/n8n/Dockerfile) | source path |
| [infra/07-workflow/n8n/README.md](../../../../infra/07-workflow/n8n/README.md) | folder index |
| [infra/07-workflow/n8n/docker-compose.yml](../../../../infra/07-workflow/n8n/docker-compose.yml) | YAML config |
| [infra/07-workflow/n8n/docker-entrypoint.dev.sh](../../../../infra/07-workflow/n8n/docker-entrypoint.dev.sh) | script |
| [infra/07-workflow/n8n/docker-entrypoint.sh](../../../../infra/07-workflow/n8n/docker-entrypoint.sh) | script |
| [infra/08-ai/README.md](../../../../infra/08-ai/README.md) | folder index |
| [infra/08-ai/ollama/README.md](../../../../infra/08-ai/ollama/README.md) | folder index |
| [infra/08-ai/ollama/docker-compose.yml](../../../../infra/08-ai/ollama/docker-compose.yml) | YAML config |
| [infra/08-ai/open-webui/README.md](../../../../infra/08-ai/open-webui/README.md) | folder index |
| [infra/08-ai/open-webui/docker-compose.yml](../../../../infra/08-ai/open-webui/docker-compose.yml) | YAML config |
| [infra/09-tooling/README.md](../../../../infra/09-tooling/README.md) | folder index |
| [infra/09-tooling/k6/README.md](../../../../infra/09-tooling/k6/README.md) | folder index |
| [infra/09-tooling/k6/docker-compose.yml](../../../../infra/09-tooling/k6/docker-compose.yml) | YAML config |
| [infra/09-tooling/locust/Dockerfile](../../../../infra/09-tooling/locust/Dockerfile) | source path |
| [infra/09-tooling/locust/README.md](../../../../infra/09-tooling/locust/README.md) | folder index |
| [infra/09-tooling/locust/docker-compose.yml](../../../../infra/09-tooling/locust/docker-compose.yml) | YAML config |
| [infra/09-tooling/registry/README.md](../../../../infra/09-tooling/registry/README.md) | folder index |
| [infra/09-tooling/registry/docker-compose.yml](../../../../infra/09-tooling/registry/docker-compose.yml) | YAML config |
| [infra/09-tooling/sonarqube/README.md](../../../../infra/09-tooling/sonarqube/README.md) | folder index |
| [infra/09-tooling/sonarqube/docker-compose.yml](../../../../infra/09-tooling/sonarqube/docker-compose.yml) | YAML config |
| [infra/09-tooling/syncthing/README.md](../../../../infra/09-tooling/syncthing/README.md) | folder index |
| [infra/09-tooling/syncthing/docker-compose.yml](../../../../infra/09-tooling/syncthing/docker-compose.yml) | YAML config |
| [infra/09-tooling/terraform/README.md](../../../../infra/09-tooling/terraform/README.md) | folder index |
| [infra/09-tooling/terraform/docker-compose.yml](../../../../infra/09-tooling/terraform/docker-compose.yml) | YAML config |
| [infra/09-tooling/terrakube/README.md](../../../../infra/09-tooling/terrakube/README.md) | folder index |
| [infra/09-tooling/terrakube/docker-compose.yml](../../../../infra/09-tooling/terrakube/docker-compose.yml) | YAML config |
| [infra/10-communication/README.md](../../../../infra/10-communication/README.md) | folder index |
| [infra/10-communication/mail/README.md](../../../../infra/10-communication/mail/README.md) | folder index |
| [infra/10-communication/mail/docker-compose.yml](../../../../infra/10-communication/mail/docker-compose.yml) | YAML config |
| [infra/11-laboratory/README.md](../../../../infra/11-laboratory/README.md) | folder index |
| [infra/11-laboratory/dashboard/README.md](../../../../infra/11-laboratory/dashboard/README.md) | folder index |
| [infra/11-laboratory/dashboard/config/config.yml](../../../../infra/11-laboratory/dashboard/config/config.yml) | YAML config |
| [infra/11-laboratory/dashboard/docker-compose.yml](../../../../infra/11-laboratory/dashboard/docker-compose.yml) | YAML config |
| [infra/11-laboratory/dozzle/README.md](../../../../infra/11-laboratory/dozzle/README.md) | folder index |
| [infra/11-laboratory/dozzle/docker-compose.yml](../../../../infra/11-laboratory/dozzle/docker-compose.yml) | YAML config |
| [infra/11-laboratory/open-notebook/README.md](../../../../infra/11-laboratory/open-notebook/README.md) | folder index |
| [infra/11-laboratory/open-notebook/docker-compose.yml](../../../../infra/11-laboratory/open-notebook/docker-compose.yml) | YAML config |
| [infra/11-laboratory/open-notebook/surrealdb/Dockerfile](../../../../infra/11-laboratory/open-notebook/surrealdb/Dockerfile) | source path |
| [infra/11-laboratory/open-notebook/surrealdb/docker-entrypoint.sh](../../../../infra/11-laboratory/open-notebook/surrealdb/docker-entrypoint.sh) | script |
| [infra/11-laboratory/portainer/README.md](../../../../infra/11-laboratory/portainer/README.md) | folder index |
| [infra/11-laboratory/portainer/docker-compose.yml](../../../../infra/11-laboratory/portainer/docker-compose.yml) | YAML config |
| [infra/11-laboratory/redisinsight/README.md](../../../../infra/11-laboratory/redisinsight/README.md) | folder index |
| [infra/11-laboratory/redisinsight/docker-compose.yml](../../../../infra/11-laboratory/redisinsight/docker-compose.yml) | YAML config |
| [infra/README.md](../../../../infra/README.md) | folder index |
| [infra/common-optimizations.exceptions.json](../../../../infra/common-optimizations.exceptions.json) | JSON registry |
| [infra/common-optimizations.yml](../../../../infra/common-optimizations.yml) | YAML config |
| [infra/image-tag-policy.exceptions.json](../../../../infra/image-tag-policy.exceptions.json) | JSON registry |
| [infra/supply-chain.cosign-offline-signing-config.json](../../../../infra/supply-chain.cosign-offline-signing-config.json) | JSON registry |
| [infra/supply-chain.cosign-offline-trusted-root.json](../../../../infra/supply-chain.cosign-offline-trusted-root.json) | JSON registry |
| [infra/supply-chain.network-approvals.md](../../../../infra/supply-chain.network-approvals.md) | Markdown reference |
| [infra/supply-chain.sample-service-policy.json](../../../../infra/supply-chain.sample-service-policy.json) | JSON registry |
| [infra/supply-chain.tool-images.json](../../../../infra/supply-chain.tool-images.json) | JSON registry |
| [infra/supply-chain.vulnerability-exceptions.json](../../../../infra/supply-chain.vulnerability-exceptions.json) | JSON registry |
| [infra/tech-stack.versions.json](../../../../infra/tech-stack.versions.json) | JSON registry |

### Scripts and validators

| Path | Role |
| --- | --- |
| [evals/README.md](../../../../evals/README.md) | folder index |
| [evals/run-agent-output-eval-fixtures.sh](../../../../evals/run-agent-output-eval-fixtures.sh) | script |
| [scripts/README.md](../../../../scripts/README.md) | folder index |
| [scripts/hardening/check-all-hardening.sh](../../../../scripts/hardening/check-all-hardening.sh) | script |
| [scripts/hooks/agent-event-hook.sh](../../../../scripts/hooks/agent-event-hook.sh) | script |
| [scripts/hooks/post-tool-validate.sh](../../../../scripts/hooks/post-tool-validate.sh) | script |
| [scripts/knowledge/generate-llm-wiki.py](../../../../scripts/knowledge/generate-llm-wiki.py) | script |
| [scripts/knowledge/report-graphify-health.sh](../../../../scripts/knowledge/report-graphify-health.sh) | script |
| [scripts/lib/hardening-lib.sh](../../../../scripts/lib/hardening-lib.sh) | script |
| [scripts/lib/ops/compose-core-readiness.sh](../../../../scripts/lib/ops/compose-core-readiness.sh) | script |
| [scripts/manifest.yaml](../../../../scripts/manifest.yaml) | YAML config |
| [scripts/operations/check-compose-core-readiness.sh](../../../../scripts/operations/check-compose-core-readiness.sh) | script |
| [scripts/operations/gen-secrets.sh](../../../../scripts/operations/gen-secrets.sh) | script |
| [scripts/operations/generate-compose-profile-service-coverage.sh](../../../../scripts/operations/generate-compose-profile-service-coverage.sh) | script |
| [scripts/operations/generate-tech-stack-version-provenance.sh](../../../../scripts/operations/generate-tech-stack-version-provenance.sh) | script |
| [scripts/operations/rehearse-postgres-logical-upgrade.sh](../../../../scripts/operations/rehearse-postgres-logical-upgrade.sh) | script |
| [scripts/operations/rehearse-sample-service-delivery.sh](../../../../scripts/operations/rehearse-sample-service-delivery.sh) | script |
| [scripts/operations/sync-tech-stack-versions.sh](../../../../scripts/operations/sync-tech-stack-versions.sh) | script |
| [scripts/operations/use-qa-ci-tools.sh](../../../../scripts/operations/use-qa-ci-tools.sh) | script |
| [scripts/requirements-pre-commit.txt](../../../../scripts/requirements-pre-commit.txt) | text entrypoint |
| [scripts/requirements.txt](../../../../scripts/requirements.txt) | text entrypoint |
| [scripts/security/generate-supply-chain-sample-service-summary.sh](../../../../scripts/security/generate-supply-chain-sample-service-summary.sh) | script |
| [scripts/security/seed-grype-db-cache.sh](../../../../scripts/security/seed-grype-db-cache.sh) | script |
| [scripts/security/verify-sample-service-supply-chain.sh](../../../../scripts/security/verify-sample-service-supply-chain.sh) | script |
| [scripts/validation/agentic-audit-semantic-contract.json](../../../../scripts/validation/agentic-audit-semantic-contract.json) | JSON registry |
| [scripts/validation/check-quickwin-baseline.sh](../../../../scripts/validation/check-quickwin-baseline.sh) | script |
| [scripts/validation/check-storybook-contract.sh](../../../../scripts/validation/check-storybook-contract.sh) | script |
| [scripts/validation/check-template-security-baseline.sh](../../../../scripts/validation/check-template-security-baseline.sh) | script |
| [scripts/validation/generate-audit-implementation-matrix.sh](../../../../scripts/validation/generate-audit-implementation-matrix.sh) | script |
| [scripts/validation/generate-security-automation-readiness.sh](../../../../scripts/validation/generate-security-automation-readiness.sh) | script |
| [scripts/validation/report-provider-hook-parity.sh](../../../../scripts/validation/report-provider-hook-parity.sh) | script |
| [scripts/validation/run-agent-precommit-all-files.sh](../../../../scripts/validation/run-agent-precommit-all-files.sh) | script |
| [scripts/validation/run-ci-precommit.sh](../../../../scripts/validation/run-ci-precommit.sh) | script |
| [scripts/validation/validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh) | script |

### GitHub workflow surface

| Path | Role |
| --- | --- |
| [.github/CODEOWNERS](../../../../.github/CODEOWNERS) | source path |
| [.github/ISSUE_TEMPLATE/bug_report.yml](../../../../.github/ISSUE_TEMPLATE/bug_report.yml) | YAML config |
| [.github/ISSUE_TEMPLATE/feature_request.yml](../../../../.github/ISSUE_TEMPLATE/feature_request.yml) | YAML config |
| [.github/PULL_REQUEST_TEMPLATE.md](../../../../.github/PULL_REQUEST_TEMPLATE.md) | Markdown reference |
| [.github/SECURITY.md](../../../../.github/SECURITY.md) | Markdown reference |
| [.github/dependabot.yml](../../../../.github/dependabot.yml) | YAML config |
| [.github/labeler.yml](../../../../.github/labeler.yml) | YAML config |
| [.github/repository-surface.md](../../../../.github/repository-surface.md) | Markdown reference |
| [.github/rulesets/main-protection.md](../../../../.github/rulesets/main-protection.md) | Markdown reference |
| [.github/workflow-contract.yml](../../../../.github/workflow-contract.yml) | YAML config |
| [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml) | YAML config |
| [.github/workflows/generate-changelog.yml](../../../../.github/workflows/generate-changelog.yml) | YAML config |
| [.github/workflows/greetings.yml](../../../../.github/workflows/greetings.yml) | YAML config |
| [.github/workflows/pr-labeler.yml](../../../../.github/workflows/pr-labeler.yml) | YAML config |
| [.github/workflows/stale.yml](../../../../.github/workflows/stale.yml) | YAML config |
| [.github/workflows/tech-stack-version-sync.yml](../../../../.github/workflows/tech-stack-version-sync.yml) | YAML config |

### Secret-handling policy

| Path | Role |
| --- | --- |
| [secrets/README.md](../../../../secrets/README.md) | folder index |

### Other tracked source

| Path | Role |
| --- | --- |
| [docs/98.archive/README.md](../../../98.archive/README.md) | folder index |
| [docs/98.archive/completed/03.specs/0093-docs-taxonomy-agent-first-migration/spec.md](../../../98.archive/completed/03.specs/0093-docs-taxonomy-agent-first-migration/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0094-harness-agent-first-engineering/spec.md](../../../98.archive/completed/03.specs/0094-harness-agent-first-engineering/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0095-infra-secrets-docs-refresh/spec.md](../../../98.archive/completed/03.specs/0095-infra-secrets-docs-refresh/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0096-llm-wiki-agent-first-completion/spec.md](../../../98.archive/completed/03.specs/0096-llm-wiki-agent-first-completion/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0097-home-docker-revalidation-deferred-follow-up/spec.md](../../../98.archive/completed/03.specs/0097-home-docker-revalidation-deferred-follow-up/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0098-standardize-infra-net/spec.md](../../../98.archive/completed/03.specs/0098-standardize-infra-net/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0154-governance-consistency-convergence/spec.md](../../../98.archive/completed/03.specs/0154-governance-consistency-convergence/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0155-validation-surface-reduction/spec.md](../../../98.archive/completed/03.specs/0155-validation-surface-reduction/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0156-compose-enablement-model-convergence/plan.md](../../../98.archive/completed/03.specs/0156-compose-enablement-model-convergence/plan.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0156-compose-enablement-model-convergence/spec.md](../../../98.archive/completed/03.specs/0156-compose-enablement-model-convergence/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0156-compose-enablement-model-convergence/tasks/tsk-0001-compose-enablement.md](../../../98.archive/completed/03.specs/0156-compose-enablement-model-convergence/tasks/tsk-0001-compose-enablement.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0157-script-surface-ownership-convergence/spec.md](../../../98.archive/completed/03.specs/0157-script-surface-ownership-convergence/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0158-document-governance-lifecycle-convergence/spec.md](../../../98.archive/completed/03.specs/0158-document-governance-lifecycle-convergence/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0159-document-taxonomy-identity-convergence/spec.md](../../../98.archive/completed/03.specs/0159-document-taxonomy-identity-convergence/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0160-readme-entrypoint-form-registration/spec.md](../../../98.archive/completed/03.specs/0160-readme-entrypoint-form-registration/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0161-legacy-profile-layer-retirement/spec.md](../../../98.archive/completed/03.specs/0161-legacy-profile-layer-retirement/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0162-validation-blind-spot-closure/spec.md](../../../98.archive/completed/03.specs/0162-validation-blind-spot-closure/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0163-deferred-contract-enforcement/spec.md](../../../98.archive/completed/03.specs/0163-deferred-contract-enforcement/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0164-lifecycle-vocabulary-alignment/spec.md](../../../98.archive/completed/03.specs/0164-lifecycle-vocabulary-alignment/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0165-template-contract-enforcement/spec.md](../../../98.archive/completed/03.specs/0165-template-contract-enforcement/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0166-formatting-authority-convergence/spec.md](../../../98.archive/completed/03.specs/0166-formatting-authority-convergence/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0167-quality-gate-convergence/spec.md](../../../98.archive/completed/03.specs/0167-quality-gate-convergence/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0168-entrypoint-readme-registration/spec.md](../../../98.archive/completed/03.specs/0168-entrypoint-readme-registration/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0169-document-lifecycle-convergence/plan.md](../../../98.archive/completed/03.specs/0169-document-lifecycle-convergence/plan.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0169-document-lifecycle-convergence/spec.md](../../../98.archive/completed/03.specs/0169-document-lifecycle-convergence/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0169-document-lifecycle-convergence/tasks/tsk-0001-document-lifecycle-convergence.md](../../../98.archive/completed/03.specs/0169-document-lifecycle-convergence/tasks/tsk-0001-document-lifecycle-convergence.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0170-archive-preservation-model/plan.md](../../../98.archive/completed/03.specs/0170-archive-preservation-model/plan.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0170-archive-preservation-model/spec.md](../../../98.archive/completed/03.specs/0170-archive-preservation-model/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0170-archive-preservation-model/tasks/tsk-0001-archive-preservation-model.md](../../../98.archive/completed/03.specs/0170-archive-preservation-model/tasks/tsk-0001-archive-preservation-model.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0171-compose-sibling-pair-resolution/plan.md](../../../98.archive/completed/03.specs/0171-compose-sibling-pair-resolution/plan.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0171-compose-sibling-pair-resolution/spec.md](../../../98.archive/completed/03.specs/0171-compose-sibling-pair-resolution/spec.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0171-compose-sibling-pair-resolution/tasks/tsk-0001-sibling-pair-resolution.md](../../../98.archive/completed/03.specs/0171-compose-sibling-pair-resolution/tasks/tsk-0001-sibling-pair-resolution.md) | Markdown reference |
| [docs/98.archive/completed/03.specs/0172-document-contract-convergence/spec.md](../../../98.archive/completed/03.specs/0172-document-contract-convergence/spec.md) | Markdown reference |
| [docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md](../../../98.archive/migrations/0001-sdlc-taxonomy-convergence.md) | Markdown reference |
| [docs/98.archive/migrations/0002-operations-catalog-convergence.md](../../../98.archive/migrations/0002-operations-catalog-convergence.md) | Markdown reference |
| [docs/98.archive/migrations/0003-workspace-governance-simplification.md](../../../98.archive/migrations/0003-workspace-governance-simplification.md) | Markdown reference |
| [docs/98.archive/retired/01.requirements/0014-auth-optimization-hardening.md](../../../98.archive/retired/01.requirements/0014-auth-optimization-hardening.md) | Markdown reference |
| [docs/98.archive/retired/01.requirements/0015-security-optimization-hardening.md](../../../98.archive/retired/01.requirements/0015-security-optimization-hardening.md) | Markdown reference |
| [docs/98.archive/retired/01.requirements/0016-data-optimization-hardening.md](../../../98.archive/retired/01.requirements/0016-data-optimization-hardening.md) | Markdown reference |
| [docs/98.archive/retired/01.requirements/0017-messaging-optimization-hardening.md](../../../98.archive/retired/01.requirements/0017-messaging-optimization-hardening.md) | Markdown reference |
| [docs/98.archive/retired/01.requirements/0018-observability-optimization-hardening.md](../../../98.archive/retired/01.requirements/0018-observability-optimization-hardening.md) | Markdown reference |
| [docs/98.archive/retired/01.requirements/0019-workflow-optimization-hardening.md](../../../98.archive/retired/01.requirements/0019-workflow-optimization-hardening.md) | Markdown reference |
| [docs/98.archive/retired/01.requirements/0020-ai-optimization-hardening.md](../../../98.archive/retired/01.requirements/0020-ai-optimization-hardening.md) | Markdown reference |
| [docs/98.archive/retired/01.requirements/0021-tooling-optimization-hardening.md](../../../98.archive/retired/01.requirements/0021-tooling-optimization-hardening.md) | Markdown reference |
| [docs/98.archive/retired/01.requirements/0022-laboratory-optimization-hardening.md](../../../98.archive/retired/01.requirements/0022-laboratory-optimization-hardening.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0001-gateway/spec.md](../../../98.archive/retired/03.specs/0001-gateway/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0002-auth/spec.md](../../../98.archive/retired/03.specs/0002-auth/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0003-security/spec.md](../../../98.archive/retired/03.specs/0003-security/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0004-data/spec.md](../../../98.archive/retired/03.specs/0004-data/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0005-data-analytics/spec.md](../../../98.archive/retired/03.specs/0005-data-analytics/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0006-messaging/spec.md](../../../98.archive/retired/03.specs/0006-messaging/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0007-observability/spec.md](../../../98.archive/retired/03.specs/0007-observability/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0008-workflow/spec.md](../../../98.archive/retired/03.specs/0008-workflow/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0009-ai/spec.md](../../../98.archive/retired/03.specs/0009-ai/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0010-tooling/spec.md](../../../98.archive/retired/03.specs/0010-tooling/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0011-communication/spec.md](../../../98.archive/retired/03.specs/0011-communication/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0012-laboratory/spec.md](../../../98.archive/retired/03.specs/0012-laboratory/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0090-workspace-audit-2026-05/spec.md](../../../98.archive/retired/03.specs/0090-workspace-audit-2026-05/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0091-workspace-doc-consistency-2026-05/spec.md](../../../98.archive/retired/03.specs/0091-workspace-doc-consistency-2026-05/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0092-workspace-consistency-2026-05b/spec.md](../../../98.archive/retired/03.specs/0092-workspace-consistency-2026-05b/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0102-workspace-document-contract-audit-pack/spec.md](../../../98.archive/retired/03.specs/0102-workspace-document-contract-audit-pack/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0103-document-restructure-audit-contract-archive/spec.md](../../../98.archive/retired/03.specs/0103-document-restructure-audit-contract-archive/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0105-agentic-engineering-implementation-audit-pack/spec.md](../../../98.archive/retired/03.specs/0105-agentic-engineering-implementation-audit-pack/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0123-agentic-engineering-audit-remediation/spec.md](../../../98.archive/retired/03.specs/0123-agentic-engineering-audit-remediation/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0131-document-corpus-lifecycle-migration-foundation/spec.md](../../../98.archive/retired/03.specs/0131-document-corpus-lifecycle-migration-foundation/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0132-agent-governance-harness-convergence/spec.md](../../../98.archive/retired/03.specs/0132-agent-governance-harness-convergence/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0133-target-surface-contract-convergence/spec.md](../../../98.archive/retired/03.specs/0133-target-surface-contract-convergence/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0134-agent-governance-canonical-convergence/spec.md](../../../98.archive/retired/03.specs/0134-agent-governance-canonical-convergence/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0135-target-surface-delta-convergence/spec.md](../../../98.archive/retired/03.specs/0135-target-surface-delta-convergence/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0136-sdlc-taxonomy-convergence/spec.md](../../../98.archive/retired/03.specs/0136-sdlc-taxonomy-convergence/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0137-agentic-research-pack-rebuild/spec.md](../../../98.archive/retired/03.specs/0137-agentic-research-pack-rebuild/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0152-deleted-reference-leaf-disposition/spec.md](../../../98.archive/retired/03.specs/0152-deleted-reference-leaf-disposition/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/0153-workspace-governance-simplification/spec.md](../../../98.archive/retired/03.specs/0153-workspace-governance-simplification/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/099-template-system-numbered-sdlc-paths/spec.md](../../../98.archive/retired/03.specs/099-template-system-numbered-sdlc-paths/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/100-template-system-contract-standardization/spec.md](../../../98.archive/retired/03.specs/100-template-system-contract-standardization/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/101-template-system-reorganization/spec.md](../../../98.archive/retired/03.specs/101-template-system-reorganization/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/104-agentic-research-pack-refresh/spec.md](../../../98.archive/retired/03.specs/104-agentic-research-pack-refresh/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/106-workspace-support-surface-contract/spec.md](../../../98.archive/retired/03.specs/106-workspace-support-surface-contract/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/107-provider-semantic-parity-validator/spec.md](../../../98.archive/retired/03.specs/107-provider-semantic-parity-validator/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/108-compose-profile-service-coverage-snapshot/spec.md](../../../98.archive/retired/03.specs/108-compose-profile-service-coverage-snapshot/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/109-gap-routing-recommendation/spec.md](../../../98.archive/retired/03.specs/109-gap-routing-recommendation/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/110-agent-output-eval-fixtures/spec.md](../../../98.archive/retired/03.specs/110-agent-output-eval-fixtures/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/111-qa-gate-recommendation-ci-summary/spec.md](../../../98.archive/retired/03.specs/111-qa-gate-recommendation-ci-summary/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/112-audit-pack-coverage-report/spec.md](../../../98.archive/retired/03.specs/112-audit-pack-coverage-report/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/113-llm-wiki-stage-category-coverage/spec.md](../../../98.archive/retired/03.specs/113-llm-wiki-stage-category-coverage/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/114-tech-stack-version-provenance/spec.md](../../../98.archive/retired/03.specs/114-tech-stack-version-provenance/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/115-provider-hook-parity-matrix/spec.md](../../../98.archive/retired/03.specs/115-provider-hook-parity-matrix/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/116-agent-output-eval-runner/spec.md](../../../98.archive/retired/03.specs/116-agent-output-eval-runner/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/117-security-automation-readiness-snapshot/spec.md](../../../98.archive/retired/03.specs/117-security-automation-readiness-snapshot/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/118-audit-implementation-matrix-snapshot/spec.md](../../../98.archive/retired/03.specs/118-audit-implementation-matrix-snapshot/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/119-sdlc-document-contract-corpus-normalization/spec.md](../../../98.archive/retired/03.specs/119-sdlc-document-contract-corpus-normalization/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/120-agent-output-eval-ci-gate/spec.md](../../../98.archive/retired/03.specs/120-agent-output-eval-ci-gate/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/121-dependency-vulnerability-audit-gate/spec.md](../../../98.archive/retired/03.specs/121-dependency-vulnerability-audit-gate/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/122-agentic-research-pack-consolidation/spec.md](../../../98.archive/retired/03.specs/122-agentic-research-pack-consolidation/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/124-compose-runtime-readiness-remediation/spec.md](../../../98.archive/retired/03.specs/124-compose-runtime-readiness-remediation/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/125-infrastructure-operations-readiness-remediation/spec.md](../../../98.archive/retired/03.specs/125-infrastructure-operations-readiness-remediation/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/126-security-supply-chain-remediation/spec.md](../../../98.archive/retired/03.specs/126-security-supply-chain-remediation/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/127-deployment-release-engineering-remediation/spec.md](../../../98.archive/retired/03.specs/127-deployment-release-engineering-remediation/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/128-agentic-audit-harness-consolidation/spec.md](../../../98.archive/retired/03.specs/128-agentic-audit-harness-consolidation/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/129-document-contract-canonicalization/spec.md](../../../98.archive/retired/03.specs/129-document-contract-canonicalization/spec.md) | Markdown reference |
| [docs/98.archive/retired/03.specs/130-template-contract-system-canonicalization/spec.md](../../../98.archive/retired/03.specs/130-template-contract-system-canonicalization/spec.md) | Markdown reference |
| [docs/98.archive/retired/05.operations/guides/03-security/01.setup.md](../../../98.archive/retired/05.operations/guides/03-security/01.setup.md) | Markdown reference |
| [docs/98.archive/retired/05.operations/guides/05-messaging/ksql-streaming.md](../../../98.archive/retired/05.operations/guides/05-messaging/ksql-streaming.md) | Markdown reference |
| [docs/98.archive/retired/05.operations/guides/07-workflow/01.airflow-dag-dev.md](../../../98.archive/retired/05.operations/guides/07-workflow/01.airflow-dag-dev.md) | Markdown reference |
| [docs/98.archive/retired/05.operations/guides/07-workflow/airbyte.md](../../../98.archive/retired/05.operations/guides/07-workflow/airbyte.md) | Markdown reference |
| [docs/98.archive/retired/05.operations/guides/08-ai/01.llm-inference.md](../../../98.archive/retired/05.operations/guides/08-ai/01.llm-inference.md) | Markdown reference |
| [docs/98.archive/retired/05.operations/guides/08-ai/local-llm-setup.md](../../../98.archive/retired/05.operations/guides/08-ai/local-llm-setup.md) | Markdown reference |
| [docs/98.archive/retired/05.operations/guides/09-tooling/01.iac-automation.md](../../../98.archive/retired/05.operations/guides/09-tooling/01.iac-automation.md) | Markdown reference |
| [docs/98.archive/retired/05.operations/policies/07-workflow/airbyte.md](../../../98.archive/retired/05.operations/policies/07-workflow/airbyte.md) | Markdown reference |
| [docs/98.archive/retired/05.operations/runbooks/07-workflow/airbyte.md](../../../98.archive/retired/05.operations/runbooks/07-workflow/airbyte.md) | Markdown reference |
| [docs/98.archive/retired/90.references/audits/0001-readme/README.md](../../../98.archive/retired/90.references/audits/0001-readme/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0002-automation-coverage-map/README.md](../../../98.archive/retired/90.references/audits/0002-automation-coverage-map/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0003-ci-qa-parser-graphify-decision/README.md](../../../98.archive/retired/90.references/audits/0003-ci-qa-parser-graphify-decision/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0004-contract-governance-map/README.md](../../../98.archive/retired/90.references/audits/0004-contract-governance-map/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0005-frontmatter-inventory/README.md](../../../98.archive/retired/90.references/audits/0005-frontmatter-inventory/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0006-frontmatter-routing-profile/README.md](../../../98.archive/retired/90.references/audits/0006-frontmatter-routing-profile/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0007-gap-register/README.md](../../../98.archive/retired/90.references/audits/0007-gap-register/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0008-historical-evidence-preservation/README.md](../../../98.archive/retired/90.references/audits/0008-historical-evidence-preservation/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0009-readme-profile-inventory/README.md](../../../98.archive/retired/90.references/audits/0009-readme-profile-inventory/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0010-section-profile-inventory/README.md](../../../98.archive/retired/90.references/audits/0010-section-profile-inventory/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0011-template-application-gaps/README.md](../../../98.archive/retired/90.references/audits/0011-template-application-gaps/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0012-readme/README.md](../../../98.archive/retired/90.references/audits/0012-readme/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0013-ci-qa-formatting-contract/README.md](../../../98.archive/retired/90.references/audits/0013-ci-qa-formatting-contract/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0014-frontmatter-profile-inventory/README.md](../../../98.archive/retired/90.references/audits/0014-frontmatter-profile-inventory/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0015-operations-bucket-restructure/README.md](../../../98.archive/retired/90.references/audits/0015-operations-bucket-restructure/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0016-restructure-gap-register/README.md](../../../98.archive/retired/90.references/audits/0016-restructure-gap-register/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0017-sdlc-spec-archive-candidates/README.md](../../../98.archive/retired/90.references/audits/0017-sdlc-spec-archive-candidates/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0018-template-contract-drift/README.md](../../../98.archive/retired/90.references/audits/0018-template-contract-drift/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0034-agent-catalog-audit/README.md](../../../98.archive/retired/90.references/audits/0034-agent-catalog-audit/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0035-automation-candidates/README.md](../../../98.archive/retired/90.references/audits/0035-automation-candidates/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0036-harness-loop-audit/README.md](../../../98.archive/retired/90.references/audits/0036-harness-loop-audit/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0037-implementation-overview/README.md](../../../98.archive/retired/90.references/audits/0037-implementation-overview/README.md) | folder index |
| [docs/98.archive/retired/90.references/audits/0038-sdlc-qa-security-audit/README.md](../../../98.archive/retired/90.references/audits/0038-sdlc-qa-security-audit/README.md) | folder index |
| [docs/98.archive/retired/90.references/data/0062-stable-reference-terms/README.md](../../../98.archive/retired/90.references/data/0062-stable-reference-terms/README.md) | folder index |
| [docs/98.archive/retired/90.references/data/0063-agent-governance-retirement-ledger/README.md](../../../98.archive/retired/90.references/data/0063-agent-governance-retirement-ledger/README.md) | folder index |
| [docs/98.archive/retired/90.references/data/0068-target-surface-convergence-summary/README.md](../../../98.archive/retired/90.references/data/0068-target-surface-convergence-summary/README.md) | folder index |
| [docs/98.archive/retired/90.references/data/0069-target-surface-convergence/README.md](../../../98.archive/retired/90.references/data/0069-target-surface-convergence/README.md) | folder index |
| [docs/98.archive/retired/90.references/data/0070-gap-to-stage-routing/README.md](../../../98.archive/retired/90.references/data/0070-gap-to-stage-routing/README.md) | folder index |
| [docs/98.archive/retired/90.references/data/0073-target-surface-delta-manifest/README.md](../../../98.archive/retired/90.references/data/0073-target-surface-delta-manifest/README.md) | folder index |
| [docs/98.archive/retired/90.references/data/0074-target-surface-delta-summary/README.md](../../../98.archive/retired/90.references/data/0074-target-surface-delta-summary/README.md) | folder index |
| [docs/98.archive/retired/90.references/data/0075-profile/README.md](../../../98.archive/retired/90.references/data/0075-profile/README.md) | folder index |
| [docs/98.archive/retired/90.references/data/0077-docker-compose-to-k3s-migration/README.md](../../../98.archive/retired/90.references/data/0077-docker-compose-to-k3s-migration/README.md) | folder index |
| [docs/98.archive/retired/90.references/research/0001-agentic-research-pack-refresh/README.md](../../../98.archive/retired/90.references/research/0001-agentic-research-pack-refresh/README.md) | folder index |
| [docs/98.archive/retired/archive/Windows-Network-IP.md](../../../98.archive/retired/archive/Windows-Network-IP.md) | Markdown reference |
| [docs/98.archive/superseded/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md](../../../98.archive/superseded/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md) | Markdown reference |
| [docs/98.archive/superseded/02.architecture/decisions/0030-tombstone-retirement-record.md](../../../98.archive/superseded/02.architecture/decisions/0030-tombstone-retirement-record.md) | Markdown reference |
| [docs/98.archive/superseded/03.specs/0172-document-contract-convergence/plan.md](../../../98.archive/superseded/03.specs/0172-document-contract-convergence/plan.md) | Markdown reference |
| [docs/98.archive/superseded/03.specs/0172-document-contract-convergence/spec.md](../../../98.archive/superseded/03.specs/0172-document-contract-convergence/spec.md) | Markdown reference |
| [docs/98.archive/superseded/03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md](../../../98.archive/superseded/03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md) | Markdown reference |
| [docs/98.archive/superseded/03.specs/0174-governance-qa-convergence/plan.md](../../../98.archive/superseded/03.specs/0174-governance-qa-convergence/plan.md) | Markdown reference |
| [docs/98.archive/superseded/03.specs/0174-governance-qa-convergence/spec.md](../../../98.archive/superseded/03.specs/0174-governance-qa-convergence/spec.md) | Markdown reference |
| [docs/98.archive/superseded/03.specs/0174-governance-qa-convergence/tasks/tsk-0001-converge-governance-and-qa.md](../../../98.archive/superseded/03.specs/0174-governance-qa-convergence/tasks/tsk-0001-converge-governance-and-qa.md) | Markdown reference |
| [docs/98.archive/superseded/90.references/audits/0033-readme/README.md](../../../98.archive/superseded/90.references/audits/0033-readme/README.md) | folder index |
| [docs/98.archive/superseded/90.references/research/0080-roadmap-v1/README.md](../../../98.archive/superseded/90.references/research/0080-roadmap-v1/README.md) | folder index |

## Refresh

- **Owner**: `doc-writer` using the `knowledge-map-agent` function
- **Review Cadence**: Review when root entrypoints, governance, operations docs, script inventory, infrastructure indexes, or LLM Wiki files change
- **Update Trigger**: Run `python3 scripts/knowledge/generate-llm-wiki.py --write` after in-scope path changes and `python3 scripts/knowledge/generate-llm-wiki.py --check` during validation

## Consumers

`llms.txt`, repository readers, documentation validators, and AI agents consume this package as navigation evidence only.

## Traceability

- [llms.txt](../../../../llms.txt) - root LLM entrypoint and boundary statement
- [LLM Wiki repository map](../0083-repository-map/README.md)
- [generate-llm-wiki.py](../../../../scripts/knowledge/generate-llm-wiki.py)
- [LLM Wiki maintenance guide](../../../05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md)
- [Agent governance hub](../../../00.agent-governance/README.md)
