---
status: active
generated_by: scripts/knowledge/generate-llm-wiki.py
---

# Reference: LLM Wiki Generated Index

## Overview

이 문서는 `hy-home.docker`의 LLM Wiki가 사용하는 generated tracked repo-local index다. LLM 에이전트가 먼저 확인할 수 있는 안전한 경로 목록을 제공하되, 각 파일의 내용이나 runtime truth를 복제하지 않는다.

## Purpose

Provide a deterministic path index for repo-local AI agents without creating a public site, a full-content bundle, or a replacement for canonical source files.

## Repository Role

This generated tracked repo-local index complements `llms.txt` and `repository-map.md`. Runtime truth remains in `infra/`, `scripts/`, registry JSON files, Docker Compose files, and `docs/00.agent-governance/`.

Graphify output is advisory navigation context only. This index is generated from repository path metadata and does not treat `graphify-out/` as source material.

## Scope

### In Scope

- Repo-relative path links for safe tracked source entrypoints.
- Governance, runtime, documentation, infrastructure, script, and secret-handling policy surfaces.
- Deterministic refresh through `python3 scripts/knowledge/generate-llm-wiki.py --write`.

### Out of Scope

- Public website or public wiki deployment.
- `llms-full.txt` or any full-content export.
- External model calls, network publishing, deployment workflow, or Docker runtime behavior.
- Secret contents, credentials, private keys, tokens, shell history, raw logs, `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` as evidence.

## Definitions / Facts

- **Generated tracked repo-local index**: a committed Markdown path index regenerated from safe repository paths.
- **Tracked source boundary**: `git ls-files` plus present, non-ignored Task-local generator paths is the path source.
- **Runtime truth**: files that define actual behavior, such as Compose files, registry JSON files, scripts, and agent governance docs.
- **Advisory graph context**: generated Graphify output that can assist navigation but does not replace tracked source files.

## Source Rules

- Prefer canonical tracked source paths over generated artifacts.
- Keep links repo-relative; never use absolute filesystem links or filesystem URI links.
- Exclude secret contents and treat `secrets/README.md` as policy context only.
- Exclude `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/`.
- Regenerate this file after changes to root entrypoints, governance, operations docs, script inventory, infrastructure indexes, or LLM Wiki files.

## Generated Index

### Root entrypoints

| Path | Role |
| --- | --- |
| [.pre-commit-config.yaml](../../../.pre-commit-config.yaml) | YAML config |
| [AGENTS.md](../../../AGENTS.md) | Markdown reference |
| [CLAUDE.md](../../../CLAUDE.md) | Markdown reference |
| [GEMINI.md](../../../GEMINI.md) | Markdown reference |
| [README.md](../../../README.md) | folder index |
| [RTK.md](../../../RTK.md) | Markdown reference |
| [docker-compose.yml](../../../docker-compose.yml) | YAML config |
| [llms.txt](../../../llms.txt) | text entrypoint |

### LLM Wiki reference

| Path | Role |
| --- | --- |
| [docs/90.references/llm-wiki/README.md](README.md) | folder index |
| [docs/90.references/llm-wiki/ref-0083-repository-map.md](ref-0083-repository-map.md) | Markdown reference |

### Agent governance

| Path | Role |
| --- | --- |
| [docs/00.agent-governance/README.md](../../00.agent-governance/README.md) | folder index |
| [docs/00.agent-governance/agents/README.md](../../00.agent-governance/agents/README.md) | folder index |
| [docs/00.agent-governance/agents/agents/ci-cd-engineer.md](../../00.agent-governance/agents/agents/ci-cd-engineer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/code-reviewer.md](../../00.agent-governance/agents/agents/code-reviewer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/doc-writer.md](../../00.agent-governance/agents/agents/doc-writer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/drift-detector.md](../../00.agent-governance/agents/agents/drift-detector.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/eval-engineer.md](../../00.agent-governance/agents/agents/eval-engineer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/hook-developer.md](../../00.agent-governance/agents/agents/hook-developer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/iac-reviewer.md](../../00.agent-governance/agents/agents/iac-reviewer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/incident-responder.md](../../00.agent-governance/agents/agents/incident-responder.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/infra-implementer.md](../../00.agent-governance/agents/agents/infra-implementer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/qa-engineer.md](../../00.agent-governance/agents/agents/qa-engineer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/rules-engineer.md](../../00.agent-governance/agents/agents/rules-engineer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/security-auditor.md](../../00.agent-governance/agents/agents/security-auditor.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/skill-creator.md](../../00.agent-governance/agents/agents/skill-creator.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/workflow-supervisor.md](../../00.agent-governance/agents/agents/workflow-supervisor.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/adr-writing.md](../../00.agent-governance/agents/functions/adr-writing.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/ci-cd-patterns.md](../../00.agent-governance/agents/functions/ci-cd-patterns.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/code-review-dimensions.md](../../00.agent-governance/agents/functions/code-review-dimensions.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/code-reviewer.md](../../00.agent-governance/agents/functions/code-reviewer.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/compose-stack-agent.md](../../00.agent-governance/agents/functions/compose-stack-agent.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/container-threat-modeling.md](../../00.agent-governance/agents/functions/container-threat-modeling.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/deployment-pipeline-design.md](../../00.agent-governance/agents/functions/deployment-pipeline-design.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/docker-compose-patterns.md](../../00.agent-governance/agents/functions/docker-compose-patterns.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/e2e-testing.md](../../00.agent-governance/agents/functions/e2e-testing.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/execution-plan-agent.md](../../00.agent-governance/agents/functions/execution-plan-agent.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/incident-response.md](../../00.agent-governance/agents/functions/incident-response.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/infra-cross-validate.md](../../00.agent-governance/agents/functions/infra-cross-validate.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/infra-validate.md](../../00.agent-governance/agents/functions/infra-validate.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/knowledge-map-agent.md](../../00.agent-governance/agents/functions/knowledge-map-agent.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/ops-runbook-agent.md](../../00.agent-governance/agents/functions/ops-runbook-agent.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/policy-gate-agent.md](../../00.agent-governance/agents/functions/policy-gate-agent.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/project-memory-stewardship.md](../../00.agent-governance/agents/functions/project-memory-stewardship.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/provider-model-evaluation.md](../../00.agent-governance/agents/functions/provider-model-evaluation.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/requirements-to-design-agent.md](../../00.agent-governance/agents/functions/requirements-to-design-agent.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/security-audit.md](../../00.agent-governance/agents/functions/security-audit.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/style-validation.md](../../00.agent-governance/agents/functions/style-validation.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/task-breakdown-agent.md](../../00.agent-governance/agents/functions/task-breakdown-agent.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/test-automator.md](../../00.agent-governance/agents/functions/test-automator.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/workspace-audit-revalidation.md](../../00.agent-governance/agents/functions/workspace-audit-revalidation.md) | Markdown reference |
| [docs/00.agent-governance/contracts/agent-catalog.yaml](../../00.agent-governance/contracts/agent-catalog.yaml) | YAML config |
| [docs/00.agent-governance/contracts/agent-governance-artifacts.yaml](../../00.agent-governance/contracts/agent-governance-artifacts.yaml) | YAML config |
| [docs/00.agent-governance/contracts/provider-models.yaml](../../00.agent-governance/contracts/provider-models.yaml) | YAML config |
| [docs/00.agent-governance/harness-implementation-map.md](../../00.agent-governance/harness-implementation-map.md) | Markdown reference |
| [docs/00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md](../../00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md) | Markdown reference |
| [docs/00.agent-governance/memory/README.md](../../00.agent-governance/memory/README.md) | folder index |
| [docs/00.agent-governance/memory/agentic-harness-contract-hardening.md](../../00.agent-governance/memory/agentic-harness-contract-hardening.md) | Markdown reference |
| [docs/00.agent-governance/memory/current.md](../../00.agent-governance/memory/current.md) | Markdown reference |
| [docs/00.agent-governance/memory/docker-doc-contract-backlog.md](../../00.agent-governance/memory/docker-doc-contract-backlog.md) | Markdown reference |
| [docs/00.agent-governance/memory/execution-stage-legacy-debt.md](../../00.agent-governance/memory/execution-stage-legacy-debt.md) | Markdown reference |
| [docs/00.agent-governance/memory/governance-memory-usage-contract.md](../../00.agent-governance/memory/governance-memory-usage-contract.md) | Markdown reference |
| [docs/00.agent-governance/memory/harness-agent-first-gap-audit.md](../../00.agent-governance/memory/harness-agent-first-gap-audit.md) | Markdown reference |
| [docs/00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md) | Markdown reference |
| [docs/00.agent-governance/memory/stage-docs-lifecycle-audit.md](../../00.agent-governance/memory/stage-docs-lifecycle-audit.md) | Markdown reference |
| [docs/00.agent-governance/providers/agents-md.md](../../00.agent-governance/providers/agents-md.md) | Markdown reference |
| [docs/00.agent-governance/providers/claude.md](../../00.agent-governance/providers/claude.md) | Markdown reference |
| [docs/00.agent-governance/providers/codex.md](../../00.agent-governance/providers/codex.md) | Markdown reference |
| [docs/00.agent-governance/providers/gemini.md](../../00.agent-governance/providers/gemini.md) | Markdown reference |
| [docs/00.agent-governance/rules/agentic.md](../../00.agent-governance/rules/agentic.md) | Markdown reference |
| [docs/00.agent-governance/rules/approval-boundaries.md](../../00.agent-governance/rules/approval-boundaries.md) | Markdown reference |
| [docs/00.agent-governance/rules/bootstrap.md](../../00.agent-governance/rules/bootstrap.md) | Markdown reference |
| [docs/00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md) | Markdown reference |
| [docs/00.agent-governance/rules/environment-constraints.md](../../00.agent-governance/rules/environment-constraints.md) | Markdown reference |
| [docs/00.agent-governance/rules/git-workflow.md](../../00.agent-governance/rules/git-workflow.md) | Markdown reference |
| [docs/00.agent-governance/rules/github-governance.md](../../00.agent-governance/rules/github-governance.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.block-absolute-file-link.md](../../00.agent-governance/rules/hooks/hookify.block-absolute-file-link.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.block-direct-main-push.md](../../00.agent-governance/rules/hooks/hookify.block-direct-main-push.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.block-gha-secrets-in-run.md](../../00.agent-governance/rules/hooks/hookify.block-gha-secrets-in-run.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.block-git-no-verify.md](../../00.agent-governance/rules/hooks/hookify.block-git-no-verify.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.block-plaintext-secret-compose.md](../../00.agent-governance/rules/hooks/hookify.block-plaintext-secret-compose.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.block-unpinned-gha-action.md](../../00.agent-governance/rules/hooks/hookify.block-unpinned-gha-action.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.enforce-docs-templates.md](../../00.agent-governance/rules/hooks/hookify.enforce-docs-templates.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.require-logical-commits-before-stop.md](../../00.agent-governance/rules/hooks/hookify.require-logical-commits-before-stop.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.warn-branch-naming.md](../../00.agent-governance/rules/hooks/hookify.warn-branch-naming.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.warn-conventional-commit.md](../../00.agent-governance/rules/hooks/hookify.warn-conventional-commit.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.warn-docker-infra-stop.md](../../00.agent-governance/rules/hooks/hookify.warn-docker-infra-stop.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.warn-force-push.md](../../00.agent-governance/rules/hooks/hookify.warn-force-push.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.warn-governance-memory-edit.md](../../00.agent-governance/rules/hooks/hookify.warn-governance-memory-edit.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.warn-hook-parity-edit.md](../../00.agent-governance/rules/hooks/hookify.warn-hook-parity-edit.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.warn-korean-in-governance.md](../../00.agent-governance/rules/hooks/hookify.warn-korean-in-governance.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.warn-parallel-doc-file.md](../../00.agent-governance/rules/hooks/hookify.warn-parallel-doc-file.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.warn-post-edit-style-automation.md](../../00.agent-governance/rules/hooks/hookify.warn-post-edit-style-automation.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.warn-pre-commit-manual.md](../../00.agent-governance/rules/hooks/hookify.warn-pre-commit-manual.md) | Markdown reference |
| [docs/00.agent-governance/rules/hooks/hookify.warn-stage-doc-edit.md](../../00.agent-governance/rules/hooks/hookify.warn-stage-doc-edit.md) | Markdown reference |
| [docs/00.agent-governance/rules/jit-markers.md](../../00.agent-governance/rules/jit-markers.md) | Markdown reference |
| [docs/00.agent-governance/rules/output-style.md](../../00.agent-governance/rules/output-style.md) | Markdown reference |
| [docs/00.agent-governance/rules/persona.md](../../00.agent-governance/rules/persona.md) | Markdown reference |
| [docs/00.agent-governance/rules/postflight-checklist.md](../../00.agent-governance/rules/postflight-checklist.md) | Markdown reference |
| [docs/00.agent-governance/rules/provider-capability-matrix.md](../../00.agent-governance/rules/provider-capability-matrix.md) | Markdown reference |
| [docs/00.agent-governance/rules/quality-standards.md](../../00.agent-governance/rules/quality-standards.md) | Markdown reference |
| [docs/00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md) | Markdown reference |
| [docs/00.agent-governance/rules/standards.md](../../00.agent-governance/rules/standards.md) | Markdown reference |
| [docs/00.agent-governance/rules/task-checklists.md](../../00.agent-governance/rules/task-checklists.md) | Markdown reference |
| [docs/00.agent-governance/rules/workflows.md](../../00.agent-governance/rules/workflows.md) | Markdown reference |
| [docs/00.agent-governance/scopes/agentic.md](../../00.agent-governance/scopes/agentic.md) | Markdown reference |
| [docs/00.agent-governance/scopes/architecture.md](../../00.agent-governance/scopes/architecture.md) | Markdown reference |
| [docs/00.agent-governance/scopes/common.md](../../00.agent-governance/scopes/common.md) | Markdown reference |
| [docs/00.agent-governance/scopes/docs.md](../../00.agent-governance/scopes/docs.md) | Markdown reference |
| [docs/00.agent-governance/scopes/infra.md](../../00.agent-governance/scopes/infra.md) | Markdown reference |
| [docs/00.agent-governance/scopes/ops.md](../../00.agent-governance/scopes/ops.md) | Markdown reference |
| [docs/00.agent-governance/scopes/qa.md](../../00.agent-governance/scopes/qa.md) | Markdown reference |
| [docs/00.agent-governance/scopes/security.md](../../00.agent-governance/scopes/security.md) | Markdown reference |
| [docs/00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md) | Markdown reference |

### Runtime surfaces

| Path | Role |
| --- | --- |
| [.claude/CLAUDE.md](../../../.claude/CLAUDE.md) | Markdown reference |
| [.claude/agents/ci-cd-engineer.md](../../../.claude/agents/ci-cd-engineer.md) | Markdown reference |
| [.claude/agents/code-reviewer.md](../../../.claude/agents/code-reviewer.md) | Markdown reference |
| [.claude/agents/doc-writer.md](../../../.claude/agents/doc-writer.md) | Markdown reference |
| [.claude/agents/drift-detector.md](../../../.claude/agents/drift-detector.md) | Markdown reference |
| [.claude/agents/eval-engineer.md](../../../.claude/agents/eval-engineer.md) | Markdown reference |
| [.claude/agents/hook-developer.md](../../../.claude/agents/hook-developer.md) | Markdown reference |
| [.claude/agents/iac-reviewer.md](../../../.claude/agents/iac-reviewer.md) | Markdown reference |
| [.claude/agents/incident-responder.md](../../../.claude/agents/incident-responder.md) | Markdown reference |
| [.claude/agents/infra-implementer.md](../../../.claude/agents/infra-implementer.md) | Markdown reference |
| [.claude/agents/qa-engineer.md](../../../.claude/agents/qa-engineer.md) | Markdown reference |
| [.claude/agents/rules-engineer.md](../../../.claude/agents/rules-engineer.md) | Markdown reference |
| [.claude/agents/security-auditor.md](../../../.claude/agents/security-auditor.md) | Markdown reference |
| [.claude/agents/skill-creator.md](../../../.claude/agents/skill-creator.md) | Markdown reference |
| [.claude/agents/workflow-supervisor.md](../../../.claude/agents/workflow-supervisor.md) | Markdown reference |
| [.claude/hooks/docker-compose-pre.sh](../../../.claude/hooks/docker-compose-pre.sh) | script |
| [.claude/hooks/post-tool-validate.sh](../../../.claude/hooks/post-tool-validate.sh) | script |
| [.claude/hooks/pre-compact.sh](../../../.claude/hooks/pre-compact.sh) | script |
| [.claude/hooks/session-end.sh](../../../.claude/hooks/session-end.sh) | script |
| [.claude/hooks/session-start.sh](../../../.claude/hooks/session-start.sh) | script |
| [.claude/hooks/stop.sh](../../../.claude/hooks/stop.sh) | script |
| [.claude/hooks/user-prompt-submit.sh](../../../.claude/hooks/user-prompt-submit.sh) | script |
| [.claude/output-styles/hy-home.md](../../../.claude/output-styles/hy-home.md) | Markdown reference |
| [.claude/settings.json](../../../.claude/settings.json) | JSON registry |
| [.claude/skills/adr-writing/SKILL.md](../../../.claude/skills/adr-writing/SKILL.md) | Markdown reference |
| [.claude/skills/ci-cd-patterns/SKILL.md](../../../.claude/skills/ci-cd-patterns/SKILL.md) | Markdown reference |
| [.claude/skills/code-review-dimensions/SKILL.md](../../../.claude/skills/code-review-dimensions/SKILL.md) | Markdown reference |
| [.claude/skills/code-reviewer/SKILL.md](../../../.claude/skills/code-reviewer/SKILL.md) | Markdown reference |
| [.claude/skills/compose-stack-agent/SKILL.md](../../../.claude/skills/compose-stack-agent/SKILL.md) | Markdown reference |
| [.claude/skills/container-threat-modeling/SKILL.md](../../../.claude/skills/container-threat-modeling/SKILL.md) | Markdown reference |
| [.claude/skills/deployment-pipeline-design/SKILL.md](../../../.claude/skills/deployment-pipeline-design/SKILL.md) | Markdown reference |
| [.claude/skills/docker-compose-patterns/SKILL.md](../../../.claude/skills/docker-compose-patterns/SKILL.md) | Markdown reference |
| [.claude/skills/e2e-testing/SKILL.md](../../../.claude/skills/e2e-testing/SKILL.md) | Markdown reference |
| [.claude/skills/execution-plan-agent/SKILL.md](../../../.claude/skills/execution-plan-agent/SKILL.md) | Markdown reference |
| [.claude/skills/incident-response/SKILL.md](../../../.claude/skills/incident-response/SKILL.md) | Markdown reference |
| [.claude/skills/infra-cross-validate/SKILL.md](../../../.claude/skills/infra-cross-validate/SKILL.md) | Markdown reference |
| [.claude/skills/infra-validate/SKILL.md](../../../.claude/skills/infra-validate/SKILL.md) | Markdown reference |
| [.claude/skills/knowledge-map-agent/SKILL.md](../../../.claude/skills/knowledge-map-agent/SKILL.md) | Markdown reference |
| [.claude/skills/ops-runbook-agent/SKILL.md](../../../.claude/skills/ops-runbook-agent/SKILL.md) | Markdown reference |
| [.claude/skills/policy-gate-agent/SKILL.md](../../../.claude/skills/policy-gate-agent/SKILL.md) | Markdown reference |
| [.claude/skills/project-memory-stewardship/SKILL.md](../../../.claude/skills/project-memory-stewardship/SKILL.md) | Markdown reference |
| [.claude/skills/provider-model-evaluation/SKILL.md](../../../.claude/skills/provider-model-evaluation/SKILL.md) | Markdown reference |
| [.claude/skills/requirements-to-design-agent/SKILL.md](../../../.claude/skills/requirements-to-design-agent/SKILL.md) | Markdown reference |
| [.claude/skills/security-audit/SKILL.md](../../../.claude/skills/security-audit/SKILL.md) | Markdown reference |
| [.claude/skills/style-validation/SKILL.md](../../../.claude/skills/style-validation/SKILL.md) | Markdown reference |
| [.claude/skills/task-breakdown-agent/SKILL.md](../../../.claude/skills/task-breakdown-agent/SKILL.md) | Markdown reference |
| [.claude/skills/test-automator/SKILL.md](../../../.claude/skills/test-automator/SKILL.md) | Markdown reference |
| [.claude/skills/workspace-audit-revalidation/SKILL.md](../../../.claude/skills/workspace-audit-revalidation/SKILL.md) | Markdown reference |
| [.codex/README.md](../../../.codex/README.md) | folder index |
| [.codex/agents/ci-cd-engineer.toml](../../../.codex/agents/ci-cd-engineer.toml) | source path |
| [.codex/agents/code-reviewer.toml](../../../.codex/agents/code-reviewer.toml) | source path |
| [.codex/agents/doc-writer.toml](../../../.codex/agents/doc-writer.toml) | source path |
| [.codex/agents/drift-detector.toml](../../../.codex/agents/drift-detector.toml) | source path |
| [.codex/agents/eval-engineer.toml](../../../.codex/agents/eval-engineer.toml) | source path |
| [.codex/agents/hook-developer.toml](../../../.codex/agents/hook-developer.toml) | source path |
| [.codex/agents/iac-reviewer.toml](../../../.codex/agents/iac-reviewer.toml) | source path |
| [.codex/agents/incident-responder.toml](../../../.codex/agents/incident-responder.toml) | source path |
| [.codex/agents/infra-implementer.toml](../../../.codex/agents/infra-implementer.toml) | source path |
| [.codex/agents/qa-engineer.toml](../../../.codex/agents/qa-engineer.toml) | source path |
| [.codex/agents/rules-engineer.toml](../../../.codex/agents/rules-engineer.toml) | source path |
| [.codex/agents/security-auditor.toml](../../../.codex/agents/security-auditor.toml) | source path |
| [.codex/agents/skill-creator.toml](../../../.codex/agents/skill-creator.toml) | source path |
| [.codex/agents/workflow-supervisor.toml](../../../.codex/agents/workflow-supervisor.toml) | source path |
| [.codex/hooks.json](../../../.codex/hooks.json) | JSON registry |

### Active stage docs

| Path | Role |
| --- | --- |
| [docs/01.requirements/README.md](../../01.requirements/README.md) | folder index |
| [docs/01.requirements/prd-001-gateway.md](../../01.requirements/prd-001-gateway.md) | Markdown reference |
| [docs/01.requirements/prd-002-auth.md](../../01.requirements/prd-002-auth.md) | Markdown reference |
| [docs/01.requirements/prd-003-security.md](../../01.requirements/prd-003-security.md) | Markdown reference |
| [docs/01.requirements/prd-004-data.md](../../01.requirements/prd-004-data.md) | Markdown reference |
| [docs/01.requirements/prd-005-data-analytics.md](../../01.requirements/prd-005-data-analytics.md) | Markdown reference |
| [docs/01.requirements/prd-006-messaging.md](../../01.requirements/prd-006-messaging.md) | Markdown reference |
| [docs/01.requirements/prd-007-observability.md](../../01.requirements/prd-007-observability.md) | Markdown reference |
| [docs/01.requirements/prd-008-workflow.md](../../01.requirements/prd-008-workflow.md) | Markdown reference |
| [docs/01.requirements/prd-009-ai.md](../../01.requirements/prd-009-ai.md) | Markdown reference |
| [docs/01.requirements/prd-010-tooling.md](../../01.requirements/prd-010-tooling.md) | Markdown reference |
| [docs/01.requirements/prd-011-communication.md](../../01.requirements/prd-011-communication.md) | Markdown reference |
| [docs/01.requirements/prd-012-laboratory.md](../../01.requirements/prd-012-laboratory.md) | Markdown reference |
| [docs/01.requirements/prd-013-ai-open-webui.md](../../01.requirements/prd-013-ai-open-webui.md) | Markdown reference |
| [docs/01.requirements/prd-014-auth-optimization-hardening.md](../../01.requirements/prd-014-auth-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/prd-015-security-optimization-hardening.md](../../01.requirements/prd-015-security-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/prd-016-data-optimization-hardening.md](../../01.requirements/prd-016-data-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/prd-017-messaging-optimization-hardening.md](../../01.requirements/prd-017-messaging-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/prd-018-observability-optimization-hardening.md](../../01.requirements/prd-018-observability-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/prd-019-workflow-optimization-hardening.md](../../01.requirements/prd-019-workflow-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/prd-020-ai-optimization-hardening.md](../../01.requirements/prd-020-ai-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/prd-021-tooling-optimization-hardening.md](../../01.requirements/prd-021-tooling-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/prd-022-laboratory-optimization-hardening.md](../../01.requirements/prd-022-laboratory-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/prd-023-standardize-infra-net.md](../../01.requirements/prd-023-standardize-infra-net.md) | Markdown reference |
| [docs/01.requirements/prd-024-agent-governance-standardization.md](../../01.requirements/prd-024-agent-governance-standardization.md) | Markdown reference |
| [docs/01.requirements/prd-025-operational-readiness-closure.md](../../01.requirements/prd-025-operational-readiness-closure.md) | Markdown reference |
| [docs/02.architecture/README.md](../../02.architecture/README.md) | folder index |
| [docs/02.architecture/decisions/README.md](../../02.architecture/decisions/README.md) | folder index |
| [docs/02.architecture/decisions/adr-0001-traefik-nginx-hybrid.md](../../02.architecture/decisions/adr-0001-traefik-nginx-hybrid.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0002-keycloak-oauth2-proxy-choice.md](../../02.architecture/decisions/adr-0002-keycloak-oauth2-proxy-choice.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0003-vault-as-secrets-manager.md](../../02.architecture/decisions/adr-0003-vault-as-secrets-manager.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0004-postgresql-ha-patroni.md](../../02.architecture/decisions/adr-0004-postgresql-ha-patroni.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0005-kafka-vs-rabbitmq-selection.md](../../02.architecture/decisions/adr-0005-kafka-vs-rabbitmq-selection.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0006-lgtm-stack-selection.md](../../02.architecture/decisions/adr-0006-lgtm-stack-selection.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0007-airflow-n8n-hybrid-workflow.md](../../02.architecture/decisions/adr-0007-airflow-n8n-hybrid-workflow.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0008-ollama-openwebui-local-ai.md](../../02.architecture/decisions/adr-0008-ollama-openwebui-local-ai.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0009-tooling-services.md](../../02.architecture/decisions/adr-0009-tooling-services.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0010-communication-services.md](../../02.architecture/decisions/adr-0010-communication-services.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0011-laboratory-services.md](../../02.architecture/decisions/adr-0011-laboratory-services.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0015-analytics-engine-selection.md](../../02.architecture/decisions/adr-0015-analytics-engine-selection.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0016-open-webui-implementation.md](../../02.architecture/decisions/adr-0016-open-webui-implementation.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0017-auth-hardening-runtime-and-fail-closed.md](../../02.architecture/decisions/adr-0017-auth-hardening-runtime-and-fail-closed.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0018-vault-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/adr-0018-vault-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0019-04-data-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/adr-0019-04-data-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0020-messaging-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/adr-0020-messaging-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0021-observability-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/adr-0021-observability-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0022-workflow-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/adr-0022-workflow-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0023-ai-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/adr-0023-ai-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0024-tooling-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/adr-0024-tooling-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0025-laboratory-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/adr-0025-laboratory-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0026-standardize-infra-net.md](../../02.architecture/decisions/adr-0026-standardize-infra-net.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0027-stage-00-canonical-adapter-model.md](../../02.architecture/decisions/adr-0027-stage-00-canonical-adapter-model.md) | Markdown reference |
| [docs/02.architecture/decisions/adr-0028-local-isolated-readiness-evidence.md](../../02.architecture/decisions/adr-0028-local-isolated-readiness-evidence.md) | Markdown reference |
| [docs/02.architecture/descriptions/README.md](../../02.architecture/descriptions/README.md) | folder index |
| [docs/02.architecture/descriptions/ad-0001-gateway-architecture.md](../../02.architecture/descriptions/ad-0001-gateway-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0002-auth-architecture.md](../../02.architecture/descriptions/ad-0002-auth-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0003-security-architecture.md](../../02.architecture/descriptions/ad-0003-security-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0004-data-architecture.md](../../02.architecture/descriptions/ad-0004-data-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0005-messaging-architecture.md](../../02.architecture/descriptions/ad-0005-messaging-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0006-observability-architecture.md](../../02.architecture/descriptions/ad-0006-observability-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0007-workflow-architecture.md](../../02.architecture/descriptions/ad-0007-workflow-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0008-ai-architecture.md](../../02.architecture/descriptions/ad-0008-ai-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0009-tooling-architecture.md](../../02.architecture/descriptions/ad-0009-tooling-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0010-communication-architecture.md](../../02.architecture/descriptions/ad-0010-communication-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0011-laboratory-architecture.md](../../02.architecture/descriptions/ad-0011-laboratory-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0012-data-analytics-architecture.md](../../02.architecture/descriptions/ad-0012-data-analytics-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0013-open-webui-architecture.md](../../02.architecture/descriptions/ad-0013-open-webui-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0014-auth-optimization-hardening-architecture.md](../../02.architecture/descriptions/ad-0014-auth-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0018-security-optimization-hardening-architecture.md](../../02.architecture/descriptions/ad-0018-security-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0019-data-optimization-hardening-architecture.md](../../02.architecture/descriptions/ad-0019-data-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0020-messaging-optimization-hardening-architecture.md](../../02.architecture/descriptions/ad-0020-messaging-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0021-observability-optimization-hardening-architecture.md](../../02.architecture/descriptions/ad-0021-observability-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0022-workflow-optimization-hardening-architecture.md](../../02.architecture/descriptions/ad-0022-workflow-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0023-ai-optimization-hardening-architecture.md](../../02.architecture/descriptions/ad-0023-ai-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0024-tooling-optimization-hardening-architecture.md](../../02.architecture/descriptions/ad-0024-tooling-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0025-laboratory-optimization-hardening-architecture.md](../../02.architecture/descriptions/ad-0025-laboratory-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0026-standardize-infra-net.md](../../02.architecture/descriptions/ad-0026-standardize-infra-net.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0027-agent-governance-canonical-adapter.md](../../02.architecture/descriptions/ad-0027-agent-governance-canonical-adapter.md) | Markdown reference |
| [docs/02.architecture/descriptions/ad-0028-operational-readiness-closure.md](../../02.architecture/descriptions/ad-0028-operational-readiness-closure.md) | Markdown reference |
| [docs/03.specs/README.md](../../03.specs/README.md) | folder index |
| [docs/03.specs/spec-0001-gateway/spec.md](../../03.specs/spec-0001-gateway/spec.md) | Markdown reference |
| [docs/03.specs/spec-0002-auth/spec.md](../../03.specs/spec-0002-auth/spec.md) | Markdown reference |
| [docs/03.specs/spec-0003-security/spec.md](../../03.specs/spec-0003-security/spec.md) | Markdown reference |
| [docs/03.specs/spec-0004-data/spec.md](../../03.specs/spec-0004-data/spec.md) | Markdown reference |
| [docs/03.specs/spec-0005-data-analytics/spec.md](../../03.specs/spec-0005-data-analytics/spec.md) | Markdown reference |
| [docs/03.specs/spec-0006-messaging/spec.md](../../03.specs/spec-0006-messaging/spec.md) | Markdown reference |
| [docs/03.specs/spec-0007-observability/spec.md](../../03.specs/spec-0007-observability/spec.md) | Markdown reference |
| [docs/03.specs/spec-0008-workflow/spec.md](../../03.specs/spec-0008-workflow/spec.md) | Markdown reference |
| [docs/03.specs/spec-0009-ai/spec.md](../../03.specs/spec-0009-ai/spec.md) | Markdown reference |
| [docs/03.specs/spec-0010-tooling/spec.md](../../03.specs/spec-0010-tooling/spec.md) | Markdown reference |
| [docs/03.specs/spec-0011-communication/spec.md](../../03.specs/spec-0011-communication/spec.md) | Markdown reference |
| [docs/03.specs/spec-0012-laboratory/spec.md](../../03.specs/spec-0012-laboratory/spec.md) | Markdown reference |
| [docs/03.specs/spec-0090-workspace-audit-2026-05/spec.md](../../03.specs/spec-0090-workspace-audit-2026-05/spec.md) | Markdown reference |
| [docs/03.specs/spec-0091-workspace-doc-consistency-2026-05/spec.md](../../03.specs/spec-0091-workspace-doc-consistency-2026-05/spec.md) | Markdown reference |
| [docs/03.specs/spec-0092-workspace-consistency-2026-05b/spec.md](../../03.specs/spec-0092-workspace-consistency-2026-05b/spec.md) | Markdown reference |
| [docs/03.specs/spec-0093-docs-taxonomy-agent-first-migration/spec.md](../../03.specs/spec-0093-docs-taxonomy-agent-first-migration/spec.md) | Markdown reference |
| [docs/03.specs/spec-0094-harness-agent-first-engineering/spec.md](../../03.specs/spec-0094-harness-agent-first-engineering/spec.md) | Markdown reference |
| [docs/03.specs/spec-0095-infra-secrets-docs-refresh/spec.md](../../03.specs/spec-0095-infra-secrets-docs-refresh/spec.md) | Markdown reference |
| [docs/03.specs/spec-0096-llm-wiki-agent-first-completion/spec.md](../../03.specs/spec-0096-llm-wiki-agent-first-completion/spec.md) | Markdown reference |
| [docs/03.specs/spec-0097-home-docker-revalidation-deferred-follow-up/spec.md](../../03.specs/spec-0097-home-docker-revalidation-deferred-follow-up/spec.md) | Markdown reference |
| [docs/03.specs/spec-0098-standardize-infra-net/spec.md](../../03.specs/spec-0098-standardize-infra-net/spec.md) | Markdown reference |
| [docs/03.specs/spec-0102-workspace-document-contract-audit-pack/spec.md](../../03.specs/spec-0102-workspace-document-contract-audit-pack/spec.md) | Markdown reference |
| [docs/03.specs/spec-0103-document-restructure-audit-contract-archive/spec.md](../../03.specs/spec-0103-document-restructure-audit-contract-archive/spec.md) | Markdown reference |
| [docs/03.specs/spec-0105-agentic-engineering-implementation-audit-pack/spec.md](../../03.specs/spec-0105-agentic-engineering-implementation-audit-pack/spec.md) | Markdown reference |
| [docs/03.specs/spec-0123-agentic-engineering-audit-remediation/spec.md](../../03.specs/spec-0123-agentic-engineering-audit-remediation/spec.md) | Markdown reference |
| [docs/03.specs/spec-0123-agentic-engineering-audit-remediation/task.md](../../03.specs/spec-0123-agentic-engineering-audit-remediation/task.md) | Markdown reference |
| [docs/03.specs/spec-0131-document-corpus-lifecycle-migration-foundation/spec.md](../../03.specs/spec-0131-document-corpus-lifecycle-migration-foundation/spec.md) | Markdown reference |
| [docs/03.specs/spec-0132-agent-governance-harness-convergence/spec.md](../../03.specs/spec-0132-agent-governance-harness-convergence/spec.md) | Markdown reference |
| [docs/03.specs/spec-0133-target-surface-contract-convergence/spec.md](../../03.specs/spec-0133-target-surface-contract-convergence/spec.md) | Markdown reference |
| [docs/03.specs/spec-0134-agent-governance-canonical-convergence/plan.md](../../03.specs/spec-0134-agent-governance-canonical-convergence/plan.md) | Markdown reference |
| [docs/03.specs/spec-0134-agent-governance-canonical-convergence/spec.md](../../03.specs/spec-0134-agent-governance-canonical-convergence/spec.md) | Markdown reference |
| [docs/03.specs/spec-0134-agent-governance-canonical-convergence/task.md](../../03.specs/spec-0134-agent-governance-canonical-convergence/task.md) | Markdown reference |
| [docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md](../../03.specs/spec-0135-target-surface-delta-convergence/plan.md) | Markdown reference |
| [docs/03.specs/spec-0135-target-surface-delta-convergence/spec.md](../../03.specs/spec-0135-target-surface-delta-convergence/spec.md) | Markdown reference |
| [docs/03.specs/spec-0135-target-surface-delta-convergence/task.md](../../03.specs/spec-0135-target-surface-delta-convergence/task.md) | Markdown reference |
| [docs/03.specs/spec-0136-sdlc-taxonomy-convergence/plan.md](../../03.specs/spec-0136-sdlc-taxonomy-convergence/plan.md) | Markdown reference |
| [docs/03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md](../../03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md) | Markdown reference |
| [docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md](../../03.specs/spec-0136-sdlc-taxonomy-convergence/task.md) | Markdown reference |

### Operations docs

| Path | Role |
| --- | --- |
| [docs/05.operations/00-workspace/README.md](../../05.operations/00-workspace/README.md) | folder index |
| [docs/05.operations/00-workspace/ops-0001-common-optimizations-template-exceptions/policy.md](../../05.operations/00-workspace/ops-0001-common-optimizations-template-exceptions/policy.md) | Markdown reference |
| [docs/05.operations/00-workspace/ops-0002-developer-setup/guide.md](../../05.operations/00-workspace/ops-0002-developer-setup/guide.md) | Markdown reference |
| [docs/05.operations/00-workspace/ops-0003-env-key-comparison/guide.md](../../05.operations/00-workspace/ops-0003-env-key-comparison/guide.md) | Markdown reference |
| [docs/05.operations/00-workspace/ops-0004-harness-agent-first-engineering/guide.md](../../05.operations/00-workspace/ops-0004-harness-agent-first-engineering/guide.md) | Markdown reference |
| [docs/05.operations/00-workspace/ops-0004-harness-agent-first-engineering/policy.md](../../05.operations/00-workspace/ops-0004-harness-agent-first-engineering/policy.md) | Markdown reference |
| [docs/05.operations/00-workspace/ops-0005-harness-agent-first-engineering-validation/runbook.md](../../05.operations/00-workspace/ops-0005-harness-agent-first-engineering-validation/runbook.md) | Markdown reference |
| [docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md](../../05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md) | Markdown reference |
| [docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/guide.md](../../05.operations/00-workspace/ops-0007-llm-wiki-maintenance/guide.md) | Markdown reference |
| [docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/policy.md](../../05.operations/00-workspace/ops-0007-llm-wiki-maintenance/policy.md) | Markdown reference |
| [docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/runbook.md](../../05.operations/00-workspace/ops-0007-llm-wiki-maintenance/runbook.md) | Markdown reference |
| [docs/05.operations/00-workspace/ops-0008-new-service-onboarding/guide.md](../../05.operations/00-workspace/ops-0008-new-service-onboarding/guide.md) | Markdown reference |
| [docs/05.operations/00-workspace/ops-0009-release-management/runbook.md](../../05.operations/00-workspace/ops-0009-release-management/runbook.md) | Markdown reference |
| [docs/05.operations/00-workspace/ops-0010-sensitive-env-vars-comparison/guide.md](../../05.operations/00-workspace/ops-0010-sensitive-env-vars-comparison/guide.md) | Markdown reference |
| [docs/05.operations/01-gateway/README.md](../../05.operations/01-gateway/README.md) | folder index |
| [docs/05.operations/01-gateway/ops-0011-nginx/guide.md](../../05.operations/01-gateway/ops-0011-nginx/guide.md) | Markdown reference |
| [docs/05.operations/01-gateway/ops-0011-nginx/policy.md](../../05.operations/01-gateway/ops-0011-nginx/policy.md) | Markdown reference |
| [docs/05.operations/01-gateway/ops-0011-nginx/runbook.md](../../05.operations/01-gateway/ops-0011-nginx/runbook.md) | Markdown reference |
| [docs/05.operations/01-gateway/ops-0012-setup/guide.md](../../05.operations/01-gateway/ops-0012-setup/guide.md) | Markdown reference |
| [docs/05.operations/01-gateway/ops-0013-traefik/guide.md](../../05.operations/01-gateway/ops-0013-traefik/guide.md) | Markdown reference |
| [docs/05.operations/01-gateway/ops-0013-traefik/policy.md](../../05.operations/01-gateway/ops-0013-traefik/policy.md) | Markdown reference |
| [docs/05.operations/01-gateway/ops-0013-traefik/runbook.md](../../05.operations/01-gateway/ops-0013-traefik/runbook.md) | Markdown reference |
| [docs/05.operations/02-auth/README.md](../../05.operations/02-auth/README.md) | folder index |
| [docs/05.operations/02-auth/ops-0014-keycloak/guide.md](../../05.operations/02-auth/ops-0014-keycloak/guide.md) | Markdown reference |
| [docs/05.operations/02-auth/ops-0014-keycloak/policy.md](../../05.operations/02-auth/ops-0014-keycloak/policy.md) | Markdown reference |
| [docs/05.operations/02-auth/ops-0014-keycloak/runbook.md](../../05.operations/02-auth/ops-0014-keycloak/runbook.md) | Markdown reference |
| [docs/05.operations/02-auth/ops-0015-oauth2-proxy/guide.md](../../05.operations/02-auth/ops-0015-oauth2-proxy/guide.md) | Markdown reference |
| [docs/05.operations/02-auth/ops-0015-oauth2-proxy/policy.md](../../05.operations/02-auth/ops-0015-oauth2-proxy/policy.md) | Markdown reference |
| [docs/05.operations/02-auth/ops-0015-oauth2-proxy/runbook.md](../../05.operations/02-auth/ops-0015-oauth2-proxy/runbook.md) | Markdown reference |
| [docs/05.operations/03-security/README.md](../../05.operations/03-security/README.md) | folder index |
| [docs/05.operations/03-security/ops-0016-vault/guide.md](../../05.operations/03-security/ops-0016-vault/guide.md) | Markdown reference |
| [docs/05.operations/03-security/ops-0016-vault/policy.md](../../05.operations/03-security/ops-0016-vault/policy.md) | Markdown reference |
| [docs/05.operations/03-security/ops-0016-vault/runbook.md](../../05.operations/03-security/ops-0016-vault/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/README.md](../../05.operations/04-data/README.md) | folder index |
| [docs/05.operations/04-data/ops-0017-analytics-influxdb/guide.md](../../05.operations/04-data/ops-0017-analytics-influxdb/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0017-analytics-influxdb/policy.md](../../05.operations/04-data/ops-0017-analytics-influxdb/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0017-analytics-influxdb/runbook.md](../../05.operations/04-data/ops-0017-analytics-influxdb/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0018-analytics-ksqldb/guide.md](../../05.operations/04-data/ops-0018-analytics-ksqldb/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0018-analytics-ksqldb/policy.md](../../05.operations/04-data/ops-0018-analytics-ksqldb/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0018-analytics-ksqldb/runbook.md](../../05.operations/04-data/ops-0018-analytics-ksqldb/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0019-analytics-opensearch/guide.md](../../05.operations/04-data/ops-0019-analytics-opensearch/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0019-analytics-opensearch/policy.md](../../05.operations/04-data/ops-0019-analytics-opensearch/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0019-analytics-opensearch/runbook.md](../../05.operations/04-data/ops-0019-analytics-opensearch/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0020-analytics-warehouses/guide.md](../../05.operations/04-data/ops-0020-analytics-warehouses/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0020-analytics-warehouses/policy.md](../../05.operations/04-data/ops-0020-analytics-warehouses/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0020-analytics-warehouses/runbook.md](../../05.operations/04-data/ops-0020-analytics-warehouses/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0021-backup-backup-policy/policy.md](../../05.operations/04-data/ops-0021-backup-backup-policy/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/guide.md](../../05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/policy.md](../../05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/runbook.md](../../05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0023-lake-and-object-minio/guide.md](../../05.operations/04-data/ops-0023-lake-and-object-minio/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0023-lake-and-object-minio/policy.md](../../05.operations/04-data/ops-0023-lake-and-object-minio/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0023-lake-and-object-minio/runbook.md](../../05.operations/04-data/ops-0023-lake-and-object-minio/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/guide.md](../../05.operations/04-data/ops-0024-lake-and-object-seaweedfs/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/policy.md](../../05.operations/04-data/ops-0024-lake-and-object-seaweedfs/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/runbook.md](../../05.operations/04-data/ops-0024-lake-and-object-seaweedfs/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0025-nosql-cassandra/guide.md](../../05.operations/04-data/ops-0025-nosql-cassandra/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0025-nosql-cassandra/policy.md](../../05.operations/04-data/ops-0025-nosql-cassandra/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0025-nosql-cassandra/runbook.md](../../05.operations/04-data/ops-0025-nosql-cassandra/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0026-nosql-couchdb/guide.md](../../05.operations/04-data/ops-0026-nosql-couchdb/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0026-nosql-couchdb/policy.md](../../05.operations/04-data/ops-0026-nosql-couchdb/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0026-nosql-couchdb/runbook.md](../../05.operations/04-data/ops-0026-nosql-couchdb/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0027-nosql-mongodb/guide.md](../../05.operations/04-data/ops-0027-nosql-mongodb/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0027-nosql-mongodb/policy.md](../../05.operations/04-data/ops-0027-nosql-mongodb/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0027-nosql-mongodb/runbook.md](../../05.operations/04-data/ops-0027-nosql-mongodb/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0028-operational-mng-db/guide.md](../../05.operations/04-data/ops-0028-operational-mng-db/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0028-operational-mng-db/policy.md](../../05.operations/04-data/ops-0028-operational-mng-db/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0028-operational-mng-db/runbook.md](../../05.operations/04-data/ops-0028-operational-mng-db/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0029-operational-supabase/guide.md](../../05.operations/04-data/ops-0029-operational-supabase/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0029-operational-supabase/policy.md](../../05.operations/04-data/ops-0029-operational-supabase/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0029-operational-supabase/runbook.md](../../05.operations/04-data/ops-0029-operational-supabase/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/guide.md](../../05.operations/04-data/ops-0030-optimization-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/policy.md](../../05.operations/04-data/ops-0030-optimization-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/runbook.md](../../05.operations/04-data/ops-0030-optimization-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/guide.md](../../05.operations/04-data/ops-0031-relational-postgresql-cluster/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/policy.md](../../05.operations/04-data/ops-0031-relational-postgresql-cluster/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/runbook.md](../../05.operations/04-data/ops-0031-relational-postgresql-cluster/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0032-relational-postgresql-logical-upgrade-restore-rehearsal/runbook.md](../../05.operations/04-data/ops-0032-relational-postgresql-logical-upgrade-restore-rehearsal/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0033-specialized-neo4j/guide.md](../../05.operations/04-data/ops-0033-specialized-neo4j/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0033-specialized-neo4j/policy.md](../../05.operations/04-data/ops-0033-specialized-neo4j/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0033-specialized-neo4j/runbook.md](../../05.operations/04-data/ops-0033-specialized-neo4j/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0034-specialized-qdrant/guide.md](../../05.operations/04-data/ops-0034-specialized-qdrant/guide.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0034-specialized-qdrant/policy.md](../../05.operations/04-data/ops-0034-specialized-qdrant/policy.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0034-specialized-qdrant/runbook.md](../../05.operations/04-data/ops-0034-specialized-qdrant/runbook.md) | Markdown reference |
| [docs/05.operations/04-data/ops-0035-storage-storage-exhaustion/runbook.md](../../05.operations/04-data/ops-0035-storage-storage-exhaustion/runbook.md) | Markdown reference |
| [docs/05.operations/05-messaging/README.md](../../05.operations/05-messaging/README.md) | folder index |
| [docs/05.operations/05-messaging/ops-0036-kafka/guide.md](../../05.operations/05-messaging/ops-0036-kafka/guide.md) | Markdown reference |
| [docs/05.operations/05-messaging/ops-0036-kafka/policy.md](../../05.operations/05-messaging/ops-0036-kafka/policy.md) | Markdown reference |
| [docs/05.operations/05-messaging/ops-0036-kafka/runbook.md](../../05.operations/05-messaging/ops-0036-kafka/runbook.md) | Markdown reference |
| [docs/05.operations/05-messaging/ops-0037-optimization-hardening/guide.md](../../05.operations/05-messaging/ops-0037-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/05-messaging/ops-0037-optimization-hardening/policy.md](../../05.operations/05-messaging/ops-0037-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/05-messaging/ops-0037-optimization-hardening/runbook.md](../../05.operations/05-messaging/ops-0037-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/05-messaging/ops-0038-rabbitmq/guide.md](../../05.operations/05-messaging/ops-0038-rabbitmq/guide.md) | Markdown reference |
| [docs/05.operations/05-messaging/ops-0038-rabbitmq/policy.md](../../05.operations/05-messaging/ops-0038-rabbitmq/policy.md) | Markdown reference |
| [docs/05.operations/05-messaging/ops-0038-rabbitmq/runbook.md](../../05.operations/05-messaging/ops-0038-rabbitmq/runbook.md) | Markdown reference |
| [docs/05.operations/06-observability/README.md](../../05.operations/06-observability/README.md) | folder index |
| [docs/05.operations/06-observability/ops-0039-alertmanager/guide.md](../../05.operations/06-observability/ops-0039-alertmanager/guide.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0039-alertmanager/policy.md](../../05.operations/06-observability/ops-0039-alertmanager/policy.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0039-alertmanager/runbook.md](../../05.operations/06-observability/ops-0039-alertmanager/runbook.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0040-alloy/guide.md](../../05.operations/06-observability/ops-0040-alloy/guide.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0040-alloy/policy.md](../../05.operations/06-observability/ops-0040-alloy/policy.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0040-alloy/runbook.md](../../05.operations/06-observability/ops-0040-alloy/runbook.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0041-grafana/guide.md](../../05.operations/06-observability/ops-0041-grafana/guide.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0041-grafana/policy.md](../../05.operations/06-observability/ops-0041-grafana/policy.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0041-grafana/runbook.md](../../05.operations/06-observability/ops-0041-grafana/runbook.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0042-lgtm-stack/guide.md](../../05.operations/06-observability/ops-0042-lgtm-stack/guide.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0043-loki/guide.md](../../05.operations/06-observability/ops-0043-loki/guide.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0043-loki/policy.md](../../05.operations/06-observability/ops-0043-loki/policy.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0043-loki/runbook.md](../../05.operations/06-observability/ops-0043-loki/runbook.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0044-optimization-hardening/guide.md](../../05.operations/06-observability/ops-0044-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0044-optimization-hardening/policy.md](../../05.operations/06-observability/ops-0044-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0044-optimization-hardening/runbook.md](../../05.operations/06-observability/ops-0044-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0045-prometheus/guide.md](../../05.operations/06-observability/ops-0045-prometheus/guide.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0045-prometheus/policy.md](../../05.operations/06-observability/ops-0045-prometheus/policy.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0045-prometheus/runbook.md](../../05.operations/06-observability/ops-0045-prometheus/runbook.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0046-pushgateway/guide.md](../../05.operations/06-observability/ops-0046-pushgateway/guide.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0046-pushgateway/policy.md](../../05.operations/06-observability/ops-0046-pushgateway/policy.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0046-pushgateway/runbook.md](../../05.operations/06-observability/ops-0046-pushgateway/runbook.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0047-pyroscope/guide.md](../../05.operations/06-observability/ops-0047-pyroscope/guide.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0047-pyroscope/policy.md](../../05.operations/06-observability/ops-0047-pyroscope/policy.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0047-pyroscope/runbook.md](../../05.operations/06-observability/ops-0047-pyroscope/runbook.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0048-retention/policy.md](../../05.operations/06-observability/ops-0048-retention/policy.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0049-tempo/guide.md](../../05.operations/06-observability/ops-0049-tempo/guide.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0049-tempo/policy.md](../../05.operations/06-observability/ops-0049-tempo/policy.md) | Markdown reference |
| [docs/05.operations/06-observability/ops-0049-tempo/runbook.md](../../05.operations/06-observability/ops-0049-tempo/runbook.md) | Markdown reference |
| [docs/05.operations/07-workflow/README.md](../../05.operations/07-workflow/README.md) | folder index |
| [docs/05.operations/07-workflow/ops-0050-airflow/guide.md](../../05.operations/07-workflow/ops-0050-airflow/guide.md) | Markdown reference |
| [docs/05.operations/07-workflow/ops-0050-airflow/policy.md](../../05.operations/07-workflow/ops-0050-airflow/policy.md) | Markdown reference |
| [docs/05.operations/07-workflow/ops-0050-airflow/runbook.md](../../05.operations/07-workflow/ops-0050-airflow/runbook.md) | Markdown reference |
| [docs/05.operations/07-workflow/ops-0051-airflow-dag-basics/guide.md](../../05.operations/07-workflow/ops-0051-airflow-dag-basics/guide.md) | Markdown reference |
| [docs/05.operations/07-workflow/ops-0052-dag-deployment/policy.md](../../05.operations/07-workflow/ops-0052-dag-deployment/policy.md) | Markdown reference |
| [docs/05.operations/07-workflow/ops-0053-n8n/guide.md](../../05.operations/07-workflow/ops-0053-n8n/guide.md) | Markdown reference |
| [docs/05.operations/07-workflow/ops-0053-n8n/policy.md](../../05.operations/07-workflow/ops-0053-n8n/policy.md) | Markdown reference |
| [docs/05.operations/07-workflow/ops-0053-n8n/runbook.md](../../05.operations/07-workflow/ops-0053-n8n/runbook.md) | Markdown reference |
| [docs/05.operations/07-workflow/ops-0054-optimization-hardening/guide.md](../../05.operations/07-workflow/ops-0054-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/07-workflow/ops-0054-optimization-hardening/policy.md](../../05.operations/07-workflow/ops-0054-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/07-workflow/ops-0054-optimization-hardening/runbook.md](../../05.operations/07-workflow/ops-0054-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/08-ai/README.md](../../05.operations/08-ai/README.md) | folder index |
| [docs/05.operations/08-ai/ops-0055-gpu-recovery/runbook.md](../../05.operations/08-ai/ops-0055-gpu-recovery/runbook.md) | Markdown reference |
| [docs/05.operations/08-ai/ops-0056-ollama/guide.md](../../05.operations/08-ai/ops-0056-ollama/guide.md) | Markdown reference |
| [docs/05.operations/08-ai/ops-0056-ollama/policy.md](../../05.operations/08-ai/ops-0056-ollama/policy.md) | Markdown reference |
| [docs/05.operations/08-ai/ops-0056-ollama/runbook.md](../../05.operations/08-ai/ops-0056-ollama/runbook.md) | Markdown reference |
| [docs/05.operations/08-ai/ops-0057-open-webui/guide.md](../../05.operations/08-ai/ops-0057-open-webui/guide.md) | Markdown reference |
| [docs/05.operations/08-ai/ops-0057-open-webui/policy.md](../../05.operations/08-ai/ops-0057-open-webui/policy.md) | Markdown reference |
| [docs/05.operations/08-ai/ops-0057-open-webui/runbook.md](../../05.operations/08-ai/ops-0057-open-webui/runbook.md) | Markdown reference |
| [docs/05.operations/08-ai/ops-0058-optimization-hardening/guide.md](../../05.operations/08-ai/ops-0058-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/08-ai/ops-0058-optimization-hardening/policy.md](../../05.operations/08-ai/ops-0058-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/08-ai/ops-0058-optimization-hardening/runbook.md](../../05.operations/08-ai/ops-0058-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/08-ai/ops-0059-rag-workflow/guide.md](../../05.operations/08-ai/ops-0059-rag-workflow/guide.md) | Markdown reference |
| [docs/05.operations/09-tooling/README.md](../../05.operations/09-tooling/README.md) | folder index |
| [docs/05.operations/09-tooling/ops-0060-iac-deployment-policy/policy.md](../../05.operations/09-tooling/ops-0060-iac-deployment-policy/policy.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0061-k6/guide.md](../../05.operations/09-tooling/ops-0061-k6/guide.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0061-k6/policy.md](../../05.operations/09-tooling/ops-0061-k6/policy.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0061-k6/runbook.md](../../05.operations/09-tooling/ops-0061-k6/runbook.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0062-locust/guide.md](../../05.operations/09-tooling/ops-0062-locust/guide.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0062-locust/policy.md](../../05.operations/09-tooling/ops-0062-locust/policy.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0062-locust/runbook.md](../../05.operations/09-tooling/ops-0062-locust/runbook.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0063-optimization-hardening/guide.md](../../05.operations/09-tooling/ops-0063-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0063-optimization-hardening/policy.md](../../05.operations/09-tooling/ops-0063-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0063-optimization-hardening/runbook.md](../../05.operations/09-tooling/ops-0063-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0064-performance-testing/guide.md](../../05.operations/09-tooling/ops-0064-performance-testing/guide.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0064-performance-testing/policy.md](../../05.operations/09-tooling/ops-0064-performance-testing/policy.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0064-performance-testing/runbook.md](../../05.operations/09-tooling/ops-0064-performance-testing/runbook.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0065-registry/guide.md](../../05.operations/09-tooling/ops-0065-registry/guide.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0065-registry/policy.md](../../05.operations/09-tooling/ops-0065-registry/policy.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0065-registry/runbook.md](../../05.operations/09-tooling/ops-0065-registry/runbook.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0066-sonarqube/guide.md](../../05.operations/09-tooling/ops-0066-sonarqube/guide.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0066-sonarqube/policy.md](../../05.operations/09-tooling/ops-0066-sonarqube/policy.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0066-sonarqube/runbook.md](../../05.operations/09-tooling/ops-0066-sonarqube/runbook.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0067-syncthing/guide.md](../../05.operations/09-tooling/ops-0067-syncthing/guide.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0067-syncthing/policy.md](../../05.operations/09-tooling/ops-0067-syncthing/policy.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0067-syncthing/runbook.md](../../05.operations/09-tooling/ops-0067-syncthing/runbook.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0068-terraform/guide.md](../../05.operations/09-tooling/ops-0068-terraform/guide.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0068-terraform/policy.md](../../05.operations/09-tooling/ops-0068-terraform/policy.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0068-terraform/runbook.md](../../05.operations/09-tooling/ops-0068-terraform/runbook.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0069-terrakube/guide.md](../../05.operations/09-tooling/ops-0069-terrakube/guide.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0069-terrakube/policy.md](../../05.operations/09-tooling/ops-0069-terrakube/policy.md) | Markdown reference |
| [docs/05.operations/09-tooling/ops-0069-terrakube/runbook.md](../../05.operations/09-tooling/ops-0069-terrakube/runbook.md) | Markdown reference |
| [docs/05.operations/10-communication/README.md](../../05.operations/10-communication/README.md) | folder index |
| [docs/05.operations/10-communication/ops-0070-mail/guide.md](../../05.operations/10-communication/ops-0070-mail/guide.md) | Markdown reference |
| [docs/05.operations/10-communication/ops-0070-mail/policy.md](../../05.operations/10-communication/ops-0070-mail/policy.md) | Markdown reference |
| [docs/05.operations/10-communication/ops-0070-mail/runbook.md](../../05.operations/10-communication/ops-0070-mail/runbook.md) | Markdown reference |
| [docs/05.operations/11-laboratory/README.md](../../05.operations/11-laboratory/README.md) | folder index |
| [docs/05.operations/11-laboratory/ops-0071-dashboard/guide.md](../../05.operations/11-laboratory/ops-0071-dashboard/guide.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0071-dashboard/policy.md](../../05.operations/11-laboratory/ops-0071-dashboard/policy.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0071-dashboard/runbook.md](../../05.operations/11-laboratory/ops-0071-dashboard/runbook.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0072-dozzle/guide.md](../../05.operations/11-laboratory/ops-0072-dozzle/guide.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0072-dozzle/policy.md](../../05.operations/11-laboratory/ops-0072-dozzle/policy.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0072-dozzle/runbook.md](../../05.operations/11-laboratory/ops-0072-dozzle/runbook.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0073-open-notebook/guide.md](../../05.operations/11-laboratory/ops-0073-open-notebook/guide.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0073-open-notebook/policy.md](../../05.operations/11-laboratory/ops-0073-open-notebook/policy.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0073-open-notebook/runbook.md](../../05.operations/11-laboratory/ops-0073-open-notebook/runbook.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0074-optimization-hardening/guide.md](../../05.operations/11-laboratory/ops-0074-optimization-hardening/guide.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0074-optimization-hardening/policy.md](../../05.operations/11-laboratory/ops-0074-optimization-hardening/policy.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0074-optimization-hardening/runbook.md](../../05.operations/11-laboratory/ops-0074-optimization-hardening/runbook.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0075-portainer/guide.md](../../05.operations/11-laboratory/ops-0075-portainer/guide.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0075-portainer/policy.md](../../05.operations/11-laboratory/ops-0075-portainer/policy.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0075-portainer/runbook.md](../../05.operations/11-laboratory/ops-0075-portainer/runbook.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0076-redisinsight/guide.md](../../05.operations/11-laboratory/ops-0076-redisinsight/guide.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0076-redisinsight/policy.md](../../05.operations/11-laboratory/ops-0076-redisinsight/policy.md) | Markdown reference |
| [docs/05.operations/11-laboratory/ops-0076-redisinsight/runbook.md](../../05.operations/11-laboratory/ops-0076-redisinsight/runbook.md) | Markdown reference |
| [docs/05.operations/12-infra-net/README.md](../../05.operations/12-infra-net/README.md) | folder index |
| [docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/guide.md](../../05.operations/12-infra-net/ops-0077-standardize-infra-net/guide.md) | Markdown reference |
| [docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/policy.md](../../05.operations/12-infra-net/ops-0077-standardize-infra-net/policy.md) | Markdown reference |
| [docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/runbook.md](../../05.operations/12-infra-net/ops-0077-standardize-infra-net/runbook.md) | Markdown reference |
| [docs/05.operations/README.md](../../05.operations/README.md) | folder index |
| [docs/05.operations/incidents/README.md](../../05.operations/incidents/README.md) | folder index |
| [docs/05.operations/releases/README.md](../../05.operations/releases/README.md) | folder index |

### Reference and template docs

| Path | Role |
| --- | --- |
| [docs/90.references/README.md](../README.md) | folder index |
| [docs/90.references/audits/README.md](../audits/README.md) | folder index |
| [docs/90.references/audits/ref-0001-readme.md](../audits/ref-0001-readme.md) | Markdown reference |
| [docs/90.references/audits/ref-0002-automation-coverage-map.md](../audits/ref-0002-automation-coverage-map.md) | Markdown reference |
| [docs/90.references/audits/ref-0003-ci-qa-parser-graphify-decision.md](../audits/ref-0003-ci-qa-parser-graphify-decision.md) | Markdown reference |
| [docs/90.references/audits/ref-0004-contract-governance-map.md](../audits/ref-0004-contract-governance-map.md) | Markdown reference |
| [docs/90.references/audits/ref-0005-frontmatter-inventory.md](../audits/ref-0005-frontmatter-inventory.md) | Markdown reference |
| [docs/90.references/audits/ref-0006-frontmatter-routing-profile.md](../audits/ref-0006-frontmatter-routing-profile.md) | Markdown reference |
| [docs/90.references/audits/ref-0007-gap-register.md](../audits/ref-0007-gap-register.md) | Markdown reference |
| [docs/90.references/audits/ref-0008-historical-evidence-preservation.md](../audits/ref-0008-historical-evidence-preservation.md) | Markdown reference |
| [docs/90.references/audits/ref-0009-readme-profile-inventory.md](../audits/ref-0009-readme-profile-inventory.md) | Markdown reference |
| [docs/90.references/audits/ref-0010-section-profile-inventory.md](../audits/ref-0010-section-profile-inventory.md) | Markdown reference |
| [docs/90.references/audits/ref-0011-template-application-gaps.md](../audits/ref-0011-template-application-gaps.md) | Markdown reference |
| [docs/90.references/audits/ref-0012-readme.md](../audits/ref-0012-readme.md) | Markdown reference |
| [docs/90.references/audits/ref-0013-ci-qa-formatting-contract.md](../audits/ref-0013-ci-qa-formatting-contract.md) | Markdown reference |
| [docs/90.references/audits/ref-0014-frontmatter-profile-inventory.md](../audits/ref-0014-frontmatter-profile-inventory.md) | Markdown reference |
| [docs/90.references/audits/ref-0015-operations-bucket-restructure.md](../audits/ref-0015-operations-bucket-restructure.md) | Markdown reference |
| [docs/90.references/audits/ref-0016-restructure-gap-register.md](../audits/ref-0016-restructure-gap-register.md) | Markdown reference |
| [docs/90.references/audits/ref-0017-sdlc-spec-archive-candidates.md](../audits/ref-0017-sdlc-spec-archive-candidates.md) | Markdown reference |
| [docs/90.references/audits/ref-0018-template-contract-drift.md](../audits/ref-0018-template-contract-drift.md) | Markdown reference |
| [docs/90.references/audits/ref-0019-readme.md](../audits/ref-0019-readme.md) | Markdown reference |
| [docs/90.references/audits/ref-0020-agent-instructions-catalog-vibe-models.md](../audits/ref-0020-agent-instructions-catalog-vibe-models.md) | Markdown reference |
| [docs/90.references/audits/ref-0021-automation-candidates.md](../audits/ref-0021-automation-candidates.md) | Markdown reference |
| [docs/90.references/audits/ref-0022-compose-infrastructure-operations-readiness.md](../audits/ref-0022-compose-infrastructure-operations-readiness.md) | Markdown reference |
| [docs/90.references/audits/ref-0023-frontmatter-semantic-inventory.md](../audits/ref-0023-frontmatter-semantic-inventory.md) | Markdown reference |
| [docs/90.references/audits/ref-0024-frontmatter-template-readme-implementation.md](../audits/ref-0024-frontmatter-template-readme-implementation.md) | Markdown reference |
| [docs/90.references/audits/ref-0025-harness-engineering-implementation.md](../audits/ref-0025-harness-engineering-implementation.md) | Markdown reference |
| [docs/90.references/audits/ref-0026-implementation-overview.md](../audits/ref-0026-implementation-overview.md) | Markdown reference |
| [docs/90.references/audits/ref-0027-loop-engineering-implementation.md](../audits/ref-0027-loop-engineering-implementation.md) | Markdown reference |
| [docs/90.references/audits/ref-0028-provider-harness-loop-implementation.md](../audits/ref-0028-provider-harness-loop-implementation.md) | Markdown reference |
| [docs/90.references/audits/ref-0029-sdlc-document-contracts-implementation.md](../audits/ref-0029-sdlc-document-contracts-implementation.md) | Markdown reference |
| [docs/90.references/audits/ref-0030-sdlc-quality-formatting-implementation.md](../audits/ref-0030-sdlc-quality-formatting-implementation.md) | Markdown reference |
| [docs/90.references/audits/ref-0031-security-framework-maturity.md](../audits/ref-0031-security-framework-maturity.md) | Markdown reference |
| [docs/90.references/audits/ref-0032-workspace-rules-environment-implementation.md](../audits/ref-0032-workspace-rules-environment-implementation.md) | Markdown reference |
| [docs/90.references/audits/ref-0033-readme.md](../audits/ref-0033-readme.md) | Markdown reference |
| [docs/90.references/audits/ref-0034-agent-catalog-audit.md](../audits/ref-0034-agent-catalog-audit.md) | Markdown reference |
| [docs/90.references/audits/ref-0035-automation-candidates.md](../audits/ref-0035-automation-candidates.md) | Markdown reference |
| [docs/90.references/audits/ref-0036-harness-loop-audit.md](../audits/ref-0036-harness-loop-audit.md) | Markdown reference |
| [docs/90.references/audits/ref-0037-implementation-overview.md](../audits/ref-0037-implementation-overview.md) | Markdown reference |
| [docs/90.references/audits/ref-0038-sdlc-qa-security-audit.md](../audits/ref-0038-sdlc-qa-security-audit.md) | Markdown reference |
| [docs/90.references/data/README.md](../data/README.md) | folder index |
| [docs/90.references/data/docker/README.md](../data/docker/README.md) | folder index |
| [docs/90.references/data/docker/ref-0059-compose-profile-service-coverage.md](../data/docker/ref-0059-compose-profile-service-coverage.md) | Markdown reference |
| [docs/90.references/data/docker/ref-0060-image-version-interpretation.md](../data/docker/ref-0060-image-version-interpretation.md) | Markdown reference |
| [docs/90.references/data/docker/ref-0061-tech-stack-version-provenance.md](../data/docker/ref-0061-tech-stack-version-provenance.md) | Markdown reference |
| [docs/90.references/data/glossary/README.md](../data/glossary/README.md) | folder index |
| [docs/90.references/data/glossary/ref-0062-stable-reference-terms.md](../data/glossary/ref-0062-stable-reference-terms.md) | Markdown reference |
| [docs/90.references/data/governance/README.md](../data/governance/README.md) | folder index |
| [docs/90.references/data/governance/document-corpus-lifecycle/README.md](../data/governance/document-corpus-lifecycle/README.md) | folder index |
| [docs/90.references/data/governance/document-corpus-lifecycle/ref-0066-foundation-summary.md](../data/governance/document-corpus-lifecycle/ref-0066-foundation-summary.md) | Markdown reference |
| [docs/90.references/data/governance/document-corpus-lifecycle/ref-0067-foundation.yaml](../data/governance/document-corpus-lifecycle/ref-0067-foundation.yaml) | YAML config |
| [docs/90.references/data/governance/document-corpus-lifecycle/ref-0068-target-surface-convergence-summary.md](../data/governance/document-corpus-lifecycle/ref-0068-target-surface-convergence-summary.md) | Markdown reference |
| [docs/90.references/data/governance/document-corpus-lifecycle/ref-0069-target-surface-convergence.yaml](../data/governance/document-corpus-lifecycle/ref-0069-target-surface-convergence.yaml) | YAML config |
| [docs/90.references/data/governance/ref-0063-agent-governance-retirement-ledger.yaml](../data/governance/ref-0063-agent-governance-retirement-ledger.yaml) | YAML config |
| [docs/90.references/data/governance/ref-0064-agent-output-eval-fixtures.md](../data/governance/ref-0064-agent-output-eval-fixtures.md) | Markdown reference |
| [docs/90.references/data/governance/ref-0065-audit-implementation-matrix.md](../data/governance/ref-0065-audit-implementation-matrix.md) | Markdown reference |
| [docs/90.references/data/governance/ref-0070-gap-to-stage-routing.md](../data/governance/ref-0070-gap-to-stage-routing.md) | Markdown reference |
| [docs/90.references/data/governance/ref-0071-github-actions-control-plane-observation.yaml](../data/governance/ref-0071-github-actions-control-plane-observation.yaml) | YAML config |
| [docs/90.references/data/governance/ref-0072-provider-hook-parity-matrix.md](../data/governance/ref-0072-provider-hook-parity-matrix.md) | Markdown reference |
| [docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml](../data/governance/ref-0073-target-surface-delta-manifest.yaml) | YAML config |
| [docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md](../data/governance/ref-0074-target-surface-delta-summary.md) | Markdown reference |
| [docs/90.references/data/hads/README.md](../data/hads/README.md) | folder index |
| [docs/90.references/data/hads/ref-0075-profile.md](../data/hads/ref-0075-profile.md) | Markdown reference |
| [docs/90.references/data/knowledge/README.md](../data/knowledge/README.md) | folder index |
| [docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md](../data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md) | Markdown reference |
| [docs/90.references/data/kubernetes/README.md](../data/kubernetes/README.md) | folder index |
| [docs/90.references/data/kubernetes/ref-0077-docker-compose-to-k3s-migration.md](../data/kubernetes/ref-0077-docker-compose-to-k3s-migration.md) | Markdown reference |
| [docs/90.references/data/security/README.md](../data/security/README.md) | folder index |
| [docs/90.references/data/security/ref-0078-security-automation-readiness.md](../data/security/ref-0078-security-automation-readiness.md) | Markdown reference |
| [docs/90.references/data/security/ref-0079-supply-chain-sample-service.md](../data/security/ref-0079-supply-chain-sample-service.md) | Markdown reference |
| [docs/90.references/learning/README.md](../learning/README.md) | folder index |
| [docs/90.references/learning/ref-0080-roadmap-v1.md](../learning/ref-0080-roadmap-v1.md) | Markdown reference |
| [docs/90.references/learning/ref-0081-roadmap.md](../learning/ref-0081-roadmap.md) | Markdown reference |
| [docs/90.references/research/README.md](../research/README.md) | folder index |
| [docs/90.references/research/ref-0039-readme.md](../research/ref-0039-readme.md) | Markdown reference |
| [docs/90.references/research/ref-0040-agent-instructions-vibe-coding.md](../research/ref-0040-agent-instructions-vibe-coding.md) | Markdown reference |
| [docs/90.references/research/ref-0041-agent-model-selection.md](../research/ref-0041-agent-model-selection.md) | Markdown reference |
| [docs/90.references/research/ref-0042-ai-agent-catalogs.md](../research/ref-0042-ai-agent-catalogs.md) | Markdown reference |
| [docs/90.references/research/ref-0043-automation-pipeline-workflow.md](../research/ref-0043-automation-pipeline-workflow.md) | Markdown reference |
| [docs/90.references/research/ref-0044-docker-compose-infrastructure.md](../research/ref-0044-docker-compose-infrastructure.md) | Markdown reference |
| [docs/90.references/research/ref-0045-document-metadata-lifecycle.md](../research/ref-0045-document-metadata-lifecycle.md) | Markdown reference |
| [docs/90.references/research/ref-0046-documentation-architecture.md](../research/ref-0046-documentation-architecture.md) | Markdown reference |
| [docs/90.references/research/ref-0047-harness-engineering.md](../research/ref-0047-harness-engineering.md) | Markdown reference |
| [docs/90.references/research/ref-0048-llm-wiki-system.md](../research/ref-0048-llm-wiki-system.md) | Markdown reference |
| [docs/90.references/research/ref-0049-loop-engineering.md](../research/ref-0049-loop-engineering.md) | Markdown reference |
| [docs/90.references/research/ref-0050-memory-hierarchy.md](../research/ref-0050-memory-hierarchy.md) | Markdown reference |
| [docs/90.references/research/ref-0051-provider-implementation-comparison.md](../research/ref-0051-provider-implementation-comparison.md) | Markdown reference |
| [docs/90.references/research/ref-0052-provider-model-landscape.md](../research/ref-0052-provider-model-landscape.md) | Markdown reference |
| [docs/90.references/research/ref-0053-quality-ci-formatting.md](../research/ref-0053-quality-ci-formatting.md) | Markdown reference |
| [docs/90.references/research/ref-0054-scope-application-matrix.md](../research/ref-0054-scope-application-matrix.md) | Markdown reference |
| [docs/90.references/research/ref-0055-sdlc-document-roles.md](../research/ref-0055-sdlc-document-roles.md) | Markdown reference |
| [docs/90.references/research/ref-0056-security-governance.md](../research/ref-0056-security-governance.md) | Markdown reference |
| [docs/90.references/research/ref-0057-spec-driven-sdlc.md](../research/ref-0057-spec-driven-sdlc.md) | Markdown reference |
| [docs/90.references/research/ref-0058-workspace-baseline.md](../research/ref-0058-workspace-baseline.md) | Markdown reference |
| [docs/90.references/research/ref-0084-github-actions-platform.md](../research/ref-0084-github-actions-platform.md) | Markdown reference |
| [docs/90.references/research/ref-0085-verification-validation.md](../research/ref-0085-verification-validation.md) | Markdown reference |
| [docs/99.templates/README.md](../../99.templates/README.md) | folder index |
| [docs/99.templates/support/README.md](../../99.templates/support/README.md) | folder index |
| [docs/99.templates/support/archive-retention-contract.md](../../99.templates/support/archive-retention-contract.md) | Markdown reference |
| [docs/99.templates/support/common-document-contract.md](../../99.templates/support/common-document-contract.md) | Markdown reference |
| [docs/99.templates/support/corpus-migration-contract.md](../../99.templates/support/corpus-migration-contract.md) | Markdown reference |
| [docs/99.templates/support/document-corpus-migration-contract.yaml](../../99.templates/support/document-corpus-migration-contract.yaml) | YAML config |
| [docs/99.templates/support/document-metadata-profiles.yaml](../../99.templates/support/document-metadata-profiles.yaml) | YAML config |
| [docs/99.templates/support/external-source-rationale.md](../../99.templates/support/external-source-rationale.md) | Markdown reference |
| [docs/99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md) | Markdown reference |
| [docs/99.templates/support/lifecycle-status.md](../../99.templates/support/lifecycle-status.md) | Markdown reference |
| [docs/99.templates/support/readme-profile-contract.md](../../99.templates/support/readme-profile-contract.md) | Markdown reference |
| [docs/99.templates/support/sdlc-document-contract.md](../../99.templates/support/sdlc-document-contract.md) | Markdown reference |
| [docs/99.templates/support/template-contract.md](../../99.templates/support/template-contract.md) | Markdown reference |
| [docs/99.templates/support/template-governance.md](../../99.templates/support/template-governance.md) | Markdown reference |
| [docs/99.templates/support/template-selection.md](../../99.templates/support/template-selection.md) | Markdown reference |
| [docs/99.templates/templates/README.md](../../99.templates/templates/README.md) | folder index |
| [docs/99.templates/templates/common/README.md](../../99.templates/templates/common/README.md) | folder index |
| [docs/99.templates/templates/common/archive.template.md](../../99.templates/templates/common/archive.template.md) | Markdown reference |
| [docs/99.templates/templates/common/audit.template.md](../../99.templates/templates/common/audit.template.md) | Markdown reference |
| [docs/99.templates/templates/common/readme.template.md](../../99.templates/templates/common/readme.template.md) | Markdown reference |
| [docs/99.templates/templates/common/reference.template.md](../../99.templates/templates/common/reference.template.md) | Markdown reference |
| [docs/99.templates/templates/governance/README.md](../../99.templates/templates/governance/README.md) | folder index |
| [docs/99.templates/templates/governance/memory.template.md](../../99.templates/templates/governance/memory.template.md) | Markdown reference |
| [docs/99.templates/templates/governance/progress.template.md](../../99.templates/templates/governance/progress.template.md) | Markdown reference |
| [docs/99.templates/templates/operations/README.md](../../99.templates/templates/operations/README.md) | folder index |
| [docs/99.templates/templates/operations/guide.template.md](../../99.templates/templates/operations/guide.template.md) | Markdown reference |
| [docs/99.templates/templates/operations/incident.template.md](../../99.templates/templates/operations/incident.template.md) | Markdown reference |
| [docs/99.templates/templates/operations/policy.template.md](../../99.templates/templates/operations/policy.template.md) | Markdown reference |
| [docs/99.templates/templates/operations/postmortem.template.md](../../99.templates/templates/operations/postmortem.template.md) | Markdown reference |
| [docs/99.templates/templates/operations/release.template.md](../../99.templates/templates/operations/release.template.md) | Markdown reference |
| [docs/99.templates/templates/operations/runbook.template.md](../../99.templates/templates/operations/runbook.template.md) | Markdown reference |
| [docs/99.templates/templates/sdlc/README.md](../../99.templates/templates/sdlc/README.md) | folder index |
| [docs/99.templates/templates/sdlc/adr.template.md](../../99.templates/templates/sdlc/adr.template.md) | Markdown reference |
| [docs/99.templates/templates/sdlc/architecture-description.template.md](../../99.templates/templates/sdlc/architecture-description.template.md) | Markdown reference |
| [docs/99.templates/templates/sdlc/interface-requirement.template.md](../../99.templates/templates/sdlc/interface-requirement.template.md) | Markdown reference |
| [docs/99.templates/templates/sdlc/plan.template.md](../../99.templates/templates/sdlc/plan.template.md) | Markdown reference |
| [docs/99.templates/templates/sdlc/prd.template.md](../../99.templates/templates/sdlc/prd.template.md) | Markdown reference |
| [docs/99.templates/templates/sdlc/spec.template.md](../../99.templates/templates/sdlc/spec.template.md) | Markdown reference |
| [docs/99.templates/templates/sdlc/srs.template.md](../../99.templates/templates/sdlc/srs.template.md) | Markdown reference |
| [docs/99.templates/templates/sdlc/task.template.md](../../99.templates/templates/sdlc/task.template.md) | Markdown reference |
| [docs/99.templates/templates/spec-contracts/README.md](../../99.templates/templates/spec-contracts/README.md) | folder index |
| [docs/99.templates/templates/spec-contracts/agent-design.template.md](../../99.templates/templates/spec-contracts/agent-design.template.md) | Markdown reference |
| [docs/99.templates/templates/spec-contracts/api-spec.template.md](../../99.templates/templates/spec-contracts/api-spec.template.md) | Markdown reference |
| [docs/99.templates/templates/spec-contracts/data-model.template.md](../../99.templates/templates/spec-contracts/data-model.template.md) | Markdown reference |
| [docs/99.templates/templates/spec-contracts/openapi.template.yaml](../../99.templates/templates/spec-contracts/openapi.template.yaml) | YAML config |
| [docs/99.templates/templates/spec-contracts/schema.template.graphql](../../99.templates/templates/spec-contracts/schema.template.graphql) | source path |
| [docs/99.templates/templates/spec-contracts/service.template.md](../../99.templates/templates/spec-contracts/service.template.md) | Markdown reference |
| [docs/99.templates/templates/spec-contracts/service.template.proto](../../99.templates/templates/spec-contracts/service.template.proto) | source path |
| [docs/99.templates/templates/spec-contracts/tests.template.md](../../99.templates/templates/spec-contracts/tests.template.md) | Markdown reference |
| [docs/README.md](../../README.md) | folder index |

### Infrastructure source

| Path | Role |
| --- | --- |
| [infra/01-gateway/README.md](../../../infra/01-gateway/README.md) | folder index |
| [infra/01-gateway/nginx/README.md](../../../infra/01-gateway/nginx/README.md) | folder index |
| [infra/01-gateway/nginx/config/nginx.conf](../../../infra/01-gateway/nginx/config/nginx.conf) | source path |
| [infra/01-gateway/nginx/docker-compose.yml](../../../infra/01-gateway/nginx/docker-compose.yml) | YAML config |
| [infra/01-gateway/traefik/README.md](../../../infra/01-gateway/traefik/README.md) | folder index |
| [infra/01-gateway/traefik/config/README.md](../../../infra/01-gateway/traefik/config/README.md) | folder index |
| [infra/01-gateway/traefik/config/traefik.yml](../../../infra/01-gateway/traefik/config/traefik.yml) | YAML config |
| [infra/01-gateway/traefik/docker-compose.yml](../../../infra/01-gateway/traefik/docker-compose.yml) | YAML config |
| [infra/01-gateway/traefik/dynamic/README.md](../../../infra/01-gateway/traefik/dynamic/README.md) | folder index |
| [infra/01-gateway/traefik/dynamic/adminer-k3d.yaml](../../../infra/01-gateway/traefik/dynamic/adminer-k3d.yaml) | YAML config |
| [infra/01-gateway/traefik/dynamic/argocd-k3d.yaml](../../../infra/01-gateway/traefik/dynamic/argocd-k3d.yaml) | YAML config |
| [infra/01-gateway/traefik/dynamic/headlamp-k3d.yaml](../../../infra/01-gateway/traefik/dynamic/headlamp-k3d.yaml) | YAML config |
| [infra/01-gateway/traefik/dynamic/kiali-k3d.yaml](../../../infra/01-gateway/traefik/dynamic/kiali-k3d.yaml) | YAML config |
| [infra/01-gateway/traefik/dynamic/middleware.yml](../../../infra/01-gateway/traefik/dynamic/middleware.yml) | YAML config |
| [infra/01-gateway/traefik/dynamic/rollouts-k3d.yaml](../../../infra/01-gateway/traefik/dynamic/rollouts-k3d.yaml) | YAML config |
| [infra/01-gateway/traefik/dynamic/tls.yaml](../../../infra/01-gateway/traefik/dynamic/tls.yaml) | YAML config |
| [infra/02-auth/README.md](../../../infra/02-auth/README.md) | folder index |
| [infra/02-auth/keycloak/Dockerfile](../../../infra/02-auth/keycloak/Dockerfile) | source path |
| [infra/02-auth/keycloak/README.md](../../../infra/02-auth/keycloak/README.md) | folder index |
| [infra/02-auth/keycloak/docker-compose.yml](../../../infra/02-auth/keycloak/docker-compose.yml) | YAML config |
| [infra/02-auth/oauth2-proxy/Dockerfile](../../../infra/02-auth/oauth2-proxy/Dockerfile) | source path |
| [infra/02-auth/oauth2-proxy/README.md](../../../infra/02-auth/oauth2-proxy/README.md) | folder index |
| [infra/02-auth/oauth2-proxy/docker-compose.dev.yml](../../../infra/02-auth/oauth2-proxy/docker-compose.dev.yml) | YAML config |
| [infra/02-auth/oauth2-proxy/docker-compose.yml](../../../infra/02-auth/oauth2-proxy/docker-compose.yml) | YAML config |
| [infra/02-auth/oauth2-proxy/docker-entrypoint.dev.sh](../../../infra/02-auth/oauth2-proxy/docker-entrypoint.dev.sh) | script |
| [infra/02-auth/oauth2-proxy/docker-entrypoint.sh](../../../infra/02-auth/oauth2-proxy/docker-entrypoint.sh) | script |
| [infra/03-security/README.md](../../../infra/03-security/README.md) | folder index |
| [infra/03-security/vault/README.md](../../../infra/03-security/vault/README.md) | folder index |
| [infra/03-security/vault/docker-compose.yml](../../../infra/03-security/vault/docker-compose.yml) | YAML config |
| [infra/04-data/README.md](../../../infra/04-data/README.md) | folder index |
| [infra/04-data/analytics/README.md](../../../infra/04-data/analytics/README.md) | folder index |
| [infra/04-data/analytics/influxdb/README.md](../../../infra/04-data/analytics/influxdb/README.md) | folder index |
| [infra/04-data/analytics/influxdb/docker-compose.yml](../../../infra/04-data/analytics/influxdb/docker-compose.yml) | YAML config |
| [infra/04-data/analytics/ksql/README.md](../../../infra/04-data/analytics/ksql/README.md) | folder index |
| [infra/04-data/analytics/ksql/docker-compose.yml](../../../infra/04-data/analytics/ksql/docker-compose.yml) | YAML config |
| [infra/04-data/analytics/opensearch/Dockerfile](../../../infra/04-data/analytics/opensearch/Dockerfile) | source path |
| [infra/04-data/analytics/opensearch/README.md](../../../infra/04-data/analytics/opensearch/README.md) | folder index |
| [infra/04-data/analytics/opensearch/docker-compose.cluster.yml](../../../infra/04-data/analytics/opensearch/docker-compose.cluster.yml) | YAML config |
| [infra/04-data/analytics/opensearch/docker-compose.yml](../../../infra/04-data/analytics/opensearch/docker-compose.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch-dashboards/config/opensearch_dashboards.yml](../../../infra/04-data/analytics/opensearch/opensearch-dashboards/config/opensearch_dashboards.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/action_groups.yml](../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/action_groups.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/config.yml](../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/config.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/internal_users.template.yml](../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/internal_users.template.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/roles.yml](../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/roles.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/roles_mapping.yml](../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/roles_mapping.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/tenants.yml](../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch-security/tenants.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/opensearch.yml](../../../infra/04-data/analytics/opensearch/opensearch/config/opensearch.yml) | YAML config |
| [infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt](../../../infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt) | text entrypoint |
| [infra/04-data/analytics/opensearch/opensearch/opensearch-entrypoint.sh](../../../infra/04-data/analytics/opensearch/opensearch/opensearch-entrypoint.sh) | script |
| [infra/04-data/analytics/warehouses/README.md](../../../infra/04-data/analytics/warehouses/README.md) | folder index |
| [infra/04-data/analytics/warehouses/docker-compose.yml](../../../infra/04-data/analytics/warehouses/docker-compose.yml) | YAML config |
| [infra/04-data/cache-and-kv/README.md](../../../infra/04-data/cache-and-kv/README.md) | folder index |
| [infra/04-data/cache-and-kv/valkey-cluster/README.md](../../../infra/04-data/cache-and-kv/valkey-cluster/README.md) | folder index |
| [infra/04-data/cache-and-kv/valkey-cluster/config/valkey.conf](../../../infra/04-data/cache-and-kv/valkey-cluster/config/valkey.conf) | source path |
| [infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml](../../../infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml) | YAML config |
| [infra/04-data/cache-and-kv/valkey-cluster/scripts/valkey-cluster-init.sh](../../../infra/04-data/cache-and-kv/valkey-cluster/scripts/valkey-cluster-init.sh) | script |
| [infra/04-data/cache-and-kv/valkey-cluster/scripts/valkey-start.sh](../../../infra/04-data/cache-and-kv/valkey-cluster/scripts/valkey-start.sh) | script |
| [infra/04-data/lake-and-object/README.md](../../../infra/04-data/lake-and-object/README.md) | folder index |
| [infra/04-data/lake-and-object/minio/README.md](../../../infra/04-data/lake-and-object/minio/README.md) | folder index |
| [infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml](../../../infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml) | YAML config |
| [infra/04-data/lake-and-object/minio/docker-compose.yml](../../../infra/04-data/lake-and-object/minio/docker-compose.yml) | YAML config |
| [infra/04-data/lake-and-object/seaweedfs/README.md](../../../infra/04-data/lake-and-object/seaweedfs/README.md) | folder index |
| [infra/04-data/lake-and-object/seaweedfs/docker-compose.yml](../../../infra/04-data/lake-and-object/seaweedfs/docker-compose.yml) | YAML config |
| [infra/04-data/nosql/README.md](../../../infra/04-data/nosql/README.md) | folder index |
| [infra/04-data/nosql/cassandra/README.md](../../../infra/04-data/nosql/cassandra/README.md) | folder index |
| [infra/04-data/nosql/cassandra/docker-compose.yml](../../../infra/04-data/nosql/cassandra/docker-compose.yml) | YAML config |
| [infra/04-data/nosql/couchdb/README.md](../../../infra/04-data/nosql/couchdb/README.md) | folder index |
| [infra/04-data/nosql/couchdb/docker-compose.yml](../../../infra/04-data/nosql/couchdb/docker-compose.yml) | YAML config |
| [infra/04-data/nosql/mongodb/README.md](../../../infra/04-data/nosql/mongodb/README.md) | folder index |
| [infra/04-data/nosql/mongodb/docker-compose.yml](../../../infra/04-data/nosql/mongodb/docker-compose.yml) | YAML config |
| [infra/04-data/operational/README.md](../../../infra/04-data/operational/README.md) | folder index |
| [infra/04-data/operational/mng-db/README.md](../../../infra/04-data/operational/mng-db/README.md) | folder index |
| [infra/04-data/operational/mng-db/docker-compose.yml](../../../infra/04-data/operational/mng-db/docker-compose.yml) | YAML config |
| [infra/04-data/operational/supabase/README.md](../../../infra/04-data/operational/supabase/README.md) | folder index |
| [infra/04-data/operational/supabase/docker-compose.yml](../../../infra/04-data/operational/supabase/docker-compose.yml) | YAML config |
| [infra/04-data/relational/README.md](../../../infra/04-data/relational/README.md) | folder index |
| [infra/04-data/relational/postgresql-cluster/README.md](../../../infra/04-data/relational/postgresql-cluster/README.md) | folder index |
| [infra/04-data/relational/postgresql-cluster/docker-compose.yml](../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml) | YAML config |
| [infra/04-data/relational/postgresql-cluster/scripts/spilo-entrypoint-with-secrets.sh](../../../infra/04-data/relational/postgresql-cluster/scripts/spilo-entrypoint-with-secrets.sh) | script |
| [infra/04-data/specialized/README.md](../../../infra/04-data/specialized/README.md) | folder index |
| [infra/04-data/specialized/neo4j/README.md](../../../infra/04-data/specialized/neo4j/README.md) | folder index |
| [infra/04-data/specialized/neo4j/docker-compose.yml](../../../infra/04-data/specialized/neo4j/docker-compose.yml) | YAML config |
| [infra/04-data/specialized/neo4j/scripts/neo4j-entrypoint-with-secrets.sh](../../../infra/04-data/specialized/neo4j/scripts/neo4j-entrypoint-with-secrets.sh) | script |
| [infra/04-data/specialized/qdrant/README.md](../../../infra/04-data/specialized/qdrant/README.md) | folder index |
| [infra/04-data/specialized/qdrant/docker-compose.yml](../../../infra/04-data/specialized/qdrant/docker-compose.yml) | YAML config |
| [infra/05-messaging/README.md](../../../infra/05-messaging/README.md) | folder index |
| [infra/05-messaging/kafka/README.md](../../../infra/05-messaging/kafka/README.md) | folder index |
| [infra/05-messaging/kafka/docker-compose.dev.yml](../../../infra/05-messaging/kafka/docker-compose.dev.yml) | YAML config |
| [infra/05-messaging/kafka/docker-compose.yml](../../../infra/05-messaging/kafka/docker-compose.yml) | YAML config |
| [infra/05-messaging/kafka/jmx-exporter/kafka-config.yaml](../../../infra/05-messaging/kafka/jmx-exporter/kafka-config.yaml) | YAML config |
| [infra/05-messaging/kafka/kafbat-ui/dynamic_config.template.yaml](../../../infra/05-messaging/kafka/kafbat-ui/dynamic_config.template.yaml) | YAML config |
| [infra/05-messaging/rabbitmq/README.md](../../../infra/05-messaging/rabbitmq/README.md) | folder index |
| [infra/05-messaging/rabbitmq/docker-compose.yml](../../../infra/05-messaging/rabbitmq/docker-compose.yml) | YAML config |
| [infra/06-observability/README.md](../../../infra/06-observability/README.md) | folder index |
| [infra/06-observability/alertmanager/README.md](../../../infra/06-observability/alertmanager/README.md) | folder index |
| [infra/06-observability/alertmanager/config/config.yml](../../../infra/06-observability/alertmanager/config/config.yml) | YAML config |
| [infra/06-observability/alloy/README.md](../../../infra/06-observability/alloy/README.md) | folder index |
| [infra/06-observability/docker-compose.dev.yml](../../../infra/06-observability/docker-compose.dev.yml) | YAML config |
| [infra/06-observability/docker-compose.yml](../../../infra/06-observability/docker-compose.yml) | YAML config |
| [infra/06-observability/grafana/README.md](../../../infra/06-observability/grafana/README.md) | folder index |
| [infra/06-observability/grafana/dashboards/Applications/airflow-dag-overview.json](../../../infra/06-observability/grafana/dashboards/Applications/airflow-dag-overview.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/airflow-dag.json](../../../infra/06-observability/grafana/dashboards/Applications/airflow-dag.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/airflow-monitoring.json](../../../infra/06-observability/grafana/dashboards/Applications/airflow-monitoring.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/airflow-operators.json](../../../infra/06-observability/grafana/dashboards/Applications/airflow-operators.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/airflow3-monitoring.json](../../../infra/06-observability/grafana/dashboards/Applications/airflow3-monitoring.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/argocd-app-overview.json](../../../infra/06-observability/grafana/dashboards/Applications/argocd-app-overview.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/argocd-notifications.json](../../../infra/06-observability/grafana/dashboards/Applications/argocd-notifications.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/argocd-operational.json](../../../infra/06-observability/grafana/dashboards/Applications/argocd-operational.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/argocd.json](../../../infra/06-observability/grafana/dashboards/Applications/argocd.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/n8n-system-health.json](../../../infra/06-observability/grafana/dashboards/Applications/n8n-system-health.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/n8n-workflow-analytics.json](../../../infra/06-observability/grafana/dashboards/Applications/n8n-workflow-analytics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/ollama.json](../../../infra/06-observability/grafana/dashboards/Applications/ollama.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Applications/vllm-monitoring.json](../../../infra/06-observability/grafana/dashboards/Applications/vllm-monitoring.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Gateway/traefik.json](../../../infra/06-observability/grafana/dashboards/Gateway/traefik.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/cadvisor.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/cadvisor.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/docker-metrics.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/docker-metrics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/docker-monitoring.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/docker-monitoring.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/docker-registry.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/docker-registry.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/etcd.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/etcd.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/haproxy.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/haproxy.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/k6.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/k6.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/kafka-exporter.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/kafka-exporter.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/kafka-overview.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/kafka-overview.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/minio-bucket.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/minio-bucket.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/minio.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/minio.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/neo4j-operations.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/neo4j-operations.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/neo4j.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/neo4j.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/opensearch.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/opensearch.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/postgres-exporter.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/postgres-exporter.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/postgres.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/postgres.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/qdrant.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/qdrant.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/redis-overview.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/redis-overview.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/valkey-overview.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/valkey-overview.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/vault-hcp.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/vault-hcp.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Infrastructure/vaults.json](../../../infra/06-observability/grafana/dashboards/Infrastructure/vaults.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/argo-rollouts.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/argo-rollouts.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/cluster-policy-report.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/cluster-policy-report.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/external-secrets.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/external-secrets.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/istio-control-plane.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/istio-control-plane.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k3s-monitoring.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/k3s-monitoring.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-apiserver.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-apiserver.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-app-metrics.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-app-metrics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-autoscaler.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-autoscaler.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-cluster-monitoring-1.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-cluster-monitoring-1.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-cluster.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-cluster.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-dashboard-1.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-dashboard-1.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-deployment-metrics.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-deployment-metrics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-nginx-ingress.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-nginx-ingress.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-nodes.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-nodes.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-pod-metrics.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-pod-metrics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-storage.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-storage.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/k8s-views-pods.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/k8s-views-pods.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/kube-state-metrics.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/kube-state-metrics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/kubernetes-compute-resources.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/kubernetes-compute-resources.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Kubernetes/policy-report.json](../../../infra/06-observability/grafana/dashboards/Kubernetes/policy-report.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/alertmanager.json](../../../infra/06-observability/grafana/dashboards/Observability/alertmanager.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/loki-dashboard.json](../../../infra/06-observability/grafana/dashboards/Observability/loki-dashboard.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/loki-global.json](../../../infra/06-observability/grafana/dashboards/Observability/loki-global.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/loki-metrics.json](../../../infra/06-observability/grafana/dashboards/Observability/loki-metrics.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/otel-collector.json](../../../infra/06-observability/grafana/dashboards/Observability/otel-collector.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/otel-tempo.json](../../../infra/06-observability/grafana/dashboards/Observability/otel-tempo.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Observability/prometheus.json](../../../infra/06-observability/grafana/dashboards/Observability/prometheus.json) | JSON registry |
| [infra/06-observability/grafana/dashboards/Security/keycloak.json](../../../infra/06-observability/grafana/dashboards/Security/keycloak.json) | JSON registry |
| [infra/06-observability/grafana/provisioning/dashboards/dashboards.yml](../../../infra/06-observability/grafana/provisioning/dashboards/dashboards.yml) | YAML config |
| [infra/06-observability/grafana/provisioning/datasources/datasource.yml](../../../infra/06-observability/grafana/provisioning/datasources/datasource.yml) | YAML config |
| [infra/06-observability/loki/Dockerfile](../../../infra/06-observability/loki/Dockerfile) | source path |
| [infra/06-observability/loki/README.md](../../../infra/06-observability/loki/README.md) | folder index |
| [infra/06-observability/loki/config/loki-config.yaml](../../../infra/06-observability/loki/config/loki-config.yaml) | YAML config |
| [infra/06-observability/loki/docker-entrypoint.sh](../../../infra/06-observability/loki/docker-entrypoint.sh) | script |
| [infra/06-observability/prometheus/README.md](../../../infra/06-observability/prometheus/README.md) | folder index |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.k8s.yml](../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.k8s.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.keycloak.yml](../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.keycloak.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.auth.yml](../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.auth.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.datastores.yml](../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.datastores.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.gateway.yml](../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.gateway.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.infra.yml](../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.infra.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.messaging.yml](../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.messaging.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.observability.yml](../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.observability.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.prometheus.yml](../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.prometheus.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.local.search.yml](../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.search.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/alert_rules.vault.yml](../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.vault.yml) | YAML config |
| [infra/06-observability/prometheus/config/alert_rules/recording_rules.yml](../../../infra/06-observability/prometheus/config/alert_rules/recording_rules.yml) | YAML config |
| [infra/06-observability/prometheus/config/prometheus.dev.yml](../../../infra/06-observability/prometheus/config/prometheus.dev.yml) | YAML config |
| [infra/06-observability/prometheus/config/prometheus.yml](../../../infra/06-observability/prometheus/config/prometheus.yml) | YAML config |
| [infra/06-observability/pushgateway/README.md](../../../infra/06-observability/pushgateway/README.md) | folder index |
| [infra/06-observability/pyroscope/README.md](../../../infra/06-observability/pyroscope/README.md) | folder index |
| [infra/06-observability/pyroscope/config/pyroscope.yaml](../../../infra/06-observability/pyroscope/config/pyroscope.yaml) | YAML config |
| [infra/06-observability/tempo/Dockerfile](../../../infra/06-observability/tempo/Dockerfile) | source path |
| [infra/06-observability/tempo/README.md](../../../infra/06-observability/tempo/README.md) | folder index |
| [infra/06-observability/tempo/config/tempo.yaml](../../../infra/06-observability/tempo/config/tempo.yaml) | YAML config |
| [infra/06-observability/tempo/docker-entrypoint.sh](../../../infra/06-observability/tempo/docker-entrypoint.sh) | script |
| [infra/07-workflow/README.md](../../../infra/07-workflow/README.md) | folder index |
| [infra/07-workflow/airflow/README.md](../../../infra/07-workflow/airflow/README.md) | folder index |
| [infra/07-workflow/airflow/config/statsd_mapping.yml](../../../infra/07-workflow/airflow/config/statsd_mapping.yml) | YAML config |
| [infra/07-workflow/airflow/docker-compose.dev.yml](../../../infra/07-workflow/airflow/docker-compose.dev.yml) | YAML config |
| [infra/07-workflow/airflow/docker-compose.yml](../../../infra/07-workflow/airflow/docker-compose.yml) | YAML config |
| [infra/07-workflow/n8n/Dockerfile](../../../infra/07-workflow/n8n/Dockerfile) | source path |
| [infra/07-workflow/n8n/README.md](../../../infra/07-workflow/n8n/README.md) | folder index |
| [infra/07-workflow/n8n/docker-compose.dev.yml](../../../infra/07-workflow/n8n/docker-compose.dev.yml) | YAML config |
| [infra/07-workflow/n8n/docker-compose.yml](../../../infra/07-workflow/n8n/docker-compose.yml) | YAML config |
| [infra/07-workflow/n8n/docker-entrypoint.dev.sh](../../../infra/07-workflow/n8n/docker-entrypoint.dev.sh) | script |
| [infra/07-workflow/n8n/docker-entrypoint.sh](../../../infra/07-workflow/n8n/docker-entrypoint.sh) | script |
| [infra/08-ai/README.md](../../../infra/08-ai/README.md) | folder index |
| [infra/08-ai/ollama/README.md](../../../infra/08-ai/ollama/README.md) | folder index |
| [infra/08-ai/ollama/docker-compose.yml](../../../infra/08-ai/ollama/docker-compose.yml) | YAML config |
| [infra/08-ai/open-webui/README.md](../../../infra/08-ai/open-webui/README.md) | folder index |
| [infra/08-ai/open-webui/docker-compose.yml](../../../infra/08-ai/open-webui/docker-compose.yml) | YAML config |
| [infra/09-tooling/README.md](../../../infra/09-tooling/README.md) | folder index |
| [infra/09-tooling/k6/README.md](../../../infra/09-tooling/k6/README.md) | folder index |
| [infra/09-tooling/k6/docker-compose.yml](../../../infra/09-tooling/k6/docker-compose.yml) | YAML config |
| [infra/09-tooling/locust/Dockerfile](../../../infra/09-tooling/locust/Dockerfile) | source path |
| [infra/09-tooling/locust/README.md](../../../infra/09-tooling/locust/README.md) | folder index |
| [infra/09-tooling/locust/docker-compose.yml](../../../infra/09-tooling/locust/docker-compose.yml) | YAML config |
| [infra/09-tooling/registry/README.md](../../../infra/09-tooling/registry/README.md) | folder index |
| [infra/09-tooling/registry/docker-compose.yml](../../../infra/09-tooling/registry/docker-compose.yml) | YAML config |
| [infra/09-tooling/sonarqube/README.md](../../../infra/09-tooling/sonarqube/README.md) | folder index |
| [infra/09-tooling/sonarqube/docker-compose.yml](../../../infra/09-tooling/sonarqube/docker-compose.yml) | YAML config |
| [infra/09-tooling/syncthing/README.md](../../../infra/09-tooling/syncthing/README.md) | folder index |
| [infra/09-tooling/syncthing/docker-compose.yml](../../../infra/09-tooling/syncthing/docker-compose.yml) | YAML config |
| [infra/09-tooling/terraform/README.md](../../../infra/09-tooling/terraform/README.md) | folder index |
| [infra/09-tooling/terraform/docker-compose.yml](../../../infra/09-tooling/terraform/docker-compose.yml) | YAML config |
| [infra/09-tooling/terrakube/README.md](../../../infra/09-tooling/terrakube/README.md) | folder index |
| [infra/09-tooling/terrakube/docker-compose.yml](../../../infra/09-tooling/terrakube/docker-compose.yml) | YAML config |
| [infra/10-communication/README.md](../../../infra/10-communication/README.md) | folder index |
| [infra/10-communication/mail/README.md](../../../infra/10-communication/mail/README.md) | folder index |
| [infra/10-communication/mail/docker-compose.yml](../../../infra/10-communication/mail/docker-compose.yml) | YAML config |
| [infra/11-laboratory/README.md](../../../infra/11-laboratory/README.md) | folder index |
| [infra/11-laboratory/dashboard/README.md](../../../infra/11-laboratory/dashboard/README.md) | folder index |
| [infra/11-laboratory/dashboard/config/config.yml](../../../infra/11-laboratory/dashboard/config/config.yml) | YAML config |
| [infra/11-laboratory/dashboard/docker-compose.yml](../../../infra/11-laboratory/dashboard/docker-compose.yml) | YAML config |
| [infra/11-laboratory/dozzle/README.md](../../../infra/11-laboratory/dozzle/README.md) | folder index |
| [infra/11-laboratory/dozzle/docker-compose.yml](../../../infra/11-laboratory/dozzle/docker-compose.yml) | YAML config |
| [infra/11-laboratory/open-notebook/README.md](../../../infra/11-laboratory/open-notebook/README.md) | folder index |
| [infra/11-laboratory/open-notebook/docker-compose.yml](../../../infra/11-laboratory/open-notebook/docker-compose.yml) | YAML config |
| [infra/11-laboratory/open-notebook/surrealdb/Dockerfile](../../../infra/11-laboratory/open-notebook/surrealdb/Dockerfile) | source path |
| [infra/11-laboratory/open-notebook/surrealdb/docker-entrypoint.sh](../../../infra/11-laboratory/open-notebook/surrealdb/docker-entrypoint.sh) | script |
| [infra/11-laboratory/portainer/README.md](../../../infra/11-laboratory/portainer/README.md) | folder index |
| [infra/11-laboratory/portainer/docker-compose.yml](../../../infra/11-laboratory/portainer/docker-compose.yml) | YAML config |
| [infra/11-laboratory/redisinsight/README.md](../../../infra/11-laboratory/redisinsight/README.md) | folder index |
| [infra/11-laboratory/redisinsight/docker-compose.yml](../../../infra/11-laboratory/redisinsight/docker-compose.yml) | YAML config |
| [infra/README.md](../../../infra/README.md) | folder index |
| [infra/common-optimizations.exceptions.json](../../../infra/common-optimizations.exceptions.json) | JSON registry |
| [infra/common-optimizations.yml](../../../infra/common-optimizations.yml) | YAML config |
| [infra/image-tag-policy.exceptions.json](../../../infra/image-tag-policy.exceptions.json) | JSON registry |
| [infra/supply-chain.cosign-offline-signing-config.json](../../../infra/supply-chain.cosign-offline-signing-config.json) | JSON registry |
| [infra/supply-chain.cosign-offline-trusted-root.json](../../../infra/supply-chain.cosign-offline-trusted-root.json) | JSON registry |
| [infra/supply-chain.sample-service-policy.json](../../../infra/supply-chain.sample-service-policy.json) | JSON registry |
| [infra/supply-chain.tool-images.json](../../../infra/supply-chain.tool-images.json) | JSON registry |
| [infra/supply-chain.vulnerability-exceptions.json](../../../infra/supply-chain.vulnerability-exceptions.json) | JSON registry |
| [infra/tech-stack.versions.json](../../../infra/tech-stack.versions.json) | JSON registry |

### Scripts and validators

| Path | Role |
| --- | --- |
| [scripts/README.md](../../../scripts/README.md) | folder index |
| [scripts/hardening/check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh) | script |
| [scripts/hooks/agent-event-hook.sh](../../../scripts/hooks/agent-event-hook.sh) | script |
| [scripts/hooks/patch-graphify-post-commit.sh](../../../scripts/hooks/patch-graphify-post-commit.sh) | script |
| [scripts/hooks/post-tool-validate.sh](../../../scripts/hooks/post-tool-validate.sh) | script |
| [scripts/knowledge/generate-llm-wiki.py](../../../scripts/knowledge/generate-llm-wiki.py) | script |
| [scripts/knowledge/report-graphify-health.sh](../../../scripts/knowledge/report-graphify-health.sh) | script |
| [scripts/lib/hardening-lib.sh](../../../scripts/lib/hardening-lib.sh) | script |
| [scripts/manifest.yaml](../../../scripts/manifest.yaml) | YAML config |
| [scripts/operations/gen-secrets.sh](../../../scripts/operations/gen-secrets.sh) | script |
| [scripts/operations/generate-compose-profile-service-coverage.sh](../../../scripts/operations/generate-compose-profile-service-coverage.sh) | script |
| [scripts/operations/generate-tech-stack-version-provenance.sh](../../../scripts/operations/generate-tech-stack-version-provenance.sh) | script |
| [scripts/operations/rehearse-sample-service-delivery.sh](../../../scripts/operations/rehearse-sample-service-delivery.sh) | script |
| [scripts/operations/sync-provider-surfaces.sh](../../../scripts/operations/sync-provider-surfaces.sh) | script |
| [scripts/operations/sync-tech-stack-versions.sh](../../../scripts/operations/sync-tech-stack-versions.sh) | script |
| [scripts/operations/use-qa-ci-tools.sh](../../../scripts/operations/use-qa-ci-tools.sh) | script |
| [scripts/requirements-pre-commit.txt](../../../scripts/requirements-pre-commit.txt) | text entrypoint |
| [scripts/requirements.txt](../../../scripts/requirements.txt) | text entrypoint |
| [scripts/security/generate-supply-chain-sample-service-summary.sh](../../../scripts/security/generate-supply-chain-sample-service-summary.sh) | script |
| [scripts/security/seed-grype-db-cache.sh](../../../scripts/security/seed-grype-db-cache.sh) | script |
| [scripts/security/verify-sample-service-supply-chain.sh](../../../scripts/security/verify-sample-service-supply-chain.sh) | script |
| [scripts/validation/agentic-audit-semantic-contract.json](../../../scripts/validation/agentic-audit-semantic-contract.json) | JSON registry |
| [scripts/validation/check-doc-implementation-alignment.sh](../../../scripts/validation/check-doc-implementation-alignment.sh) | script |
| [scripts/validation/check-doc-traceability.sh](../../../scripts/validation/check-doc-traceability.sh) | script |
| [scripts/validation/check-quickwin-baseline.sh](../../../scripts/validation/check-quickwin-baseline.sh) | script |
| [scripts/validation/check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) | script |
| [scripts/validation/check-storybook-contract.sh](../../../scripts/validation/check-storybook-contract.sh) | script |
| [scripts/validation/check-template-security-baseline.sh](../../../scripts/validation/check-template-security-baseline.sh) | script |
| [scripts/validation/compose-core-readiness.lib.sh](../../../scripts/validation/compose-core-readiness.lib.sh) | script |
| [scripts/validation/generate-audit-implementation-matrix.sh](../../../scripts/validation/generate-audit-implementation-matrix.sh) | script |
| [scripts/validation/generate-security-automation-readiness.sh](../../../scripts/validation/generate-security-automation-readiness.sh) | script |
| [scripts/validation/recommend-gap-routing.sh](../../../scripts/validation/recommend-gap-routing.sh) | script |
| [scripts/validation/recommend-qa-gates.sh](../../../scripts/validation/recommend-qa-gates.sh) | script |
| [scripts/validation/rehearse-postgres-logical-upgrade.sh](../../../scripts/validation/rehearse-postgres-logical-upgrade.sh) | script |
| [scripts/validation/report-audit-pack-coverage.sh](../../../scripts/validation/report-audit-pack-coverage.sh) | script |
| [scripts/validation/report-provider-hook-parity.sh](../../../scripts/validation/report-provider-hook-parity.sh) | script |
| [scripts/validation/run-agent-output-eval-fixtures.sh](../../../scripts/validation/run-agent-output-eval-fixtures.sh) | script |
| [scripts/validation/run-agent-precommit-all-files.sh](../../../scripts/validation/run-agent-precommit-all-files.sh) | script |
| [scripts/validation/run-ci-precommit.sh](../../../scripts/validation/run-ci-precommit.sh) | script |
| [scripts/validation/run-compose-core-readiness.sh](../../../scripts/validation/run-compose-core-readiness.sh) | script |
| [scripts/validation/run-local-qa-gates.sh](../../../scripts/validation/run-local-qa-gates.sh) | script |
| [scripts/validation/validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh) | script |
| [scripts/validation/validate-harness.sh](../../../scripts/validation/validate-harness.sh) | script |

### GitHub workflow surface

| Path | Role |
| --- | --- |
| [.github/CODEOWNERS](../../../.github/CODEOWNERS) | source path |
| [.github/INDEX.md](../../../.github/INDEX.md) | Markdown reference |
| [.github/ISSUE_TEMPLATE/bug_report.yml](../../../.github/ISSUE_TEMPLATE/bug_report.yml) | YAML config |
| [.github/ISSUE_TEMPLATE/feature_request.yml](../../../.github/ISSUE_TEMPLATE/feature_request.yml) | YAML config |
| [.github/PULL_REQUEST_TEMPLATE.md](../../../.github/PULL_REQUEST_TEMPLATE.md) | Markdown reference |
| [.github/SECURITY.md](../../../.github/SECURITY.md) | Markdown reference |
| [.github/dependabot.yml](../../../.github/dependabot.yml) | YAML config |
| [.github/labeler.yml](../../../.github/labeler.yml) | YAML config |
| [.github/rulesets/main-protection.md](../../../.github/rulesets/main-protection.md) | Markdown reference |
| [.github/workflow-contract.yml](../../../.github/workflow-contract.yml) | YAML config |
| [.github/workflows/ci-quality.yml](../../../.github/workflows/ci-quality.yml) | YAML config |
| [.github/workflows/document-corpus-lifecycle.yml](../../../.github/workflows/document-corpus-lifecycle.yml) | YAML config |
| [.github/workflows/generate-changelog.yml](../../../.github/workflows/generate-changelog.yml) | YAML config |
| [.github/workflows/greetings.yml](../../../.github/workflows/greetings.yml) | YAML config |
| [.github/workflows/pr-labeler.yml](../../../.github/workflows/pr-labeler.yml) | YAML config |
| [.github/workflows/stale.yml](../../../.github/workflows/stale.yml) | YAML config |
| [.github/workflows/tech-stack-version-sync.yml](../../../.github/workflows/tech-stack-version-sync.yml) | YAML config |

### Secret-handling policy

| Path | Role |
| --- | --- |
| [secrets/README.md](../../../secrets/README.md) | folder index |

### Other tracked source

| Path | Role |
| --- | --- |
| [docs/98.archive/README.md](../../98.archive/README.md) | folder index |
| [docs/98.archive/changes/chg-0002-01-gateway-standardization/plan.md](../../98.archive/changes/chg-0002-01-gateway-standardization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0003-02-auth-standardization/plan.md](../../98.archive/changes/chg-0003-02-auth-standardization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0004-03-security-standardization/plan.md](../../98.archive/changes/chg-0004-03-security-standardization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0005-04-data-standardization/plan.md](../../98.archive/changes/chg-0005-04-data-standardization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0006-05-messaging-standardization/plan.md](../../98.archive/changes/chg-0006-05-messaging-standardization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0007-06-observability-standardization/plan.md](../../98.archive/changes/chg-0007-06-observability-standardization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0008-07-workflow-standardization/plan.md](../../98.archive/changes/chg-0008-07-workflow-standardization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0009-08-ai-standardization/plan.md](../../98.archive/changes/chg-0009-08-ai-standardization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0010-09-tooling-standardization/plan.md](../../98.archive/changes/chg-0010-09-tooling-standardization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0011-10-communication-standardization/plan.md](../../98.archive/changes/chg-0011-10-communication-standardization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0012-11-laboratory-standardization/plan.md](../../98.archive/changes/chg-0012-11-laboratory-standardization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0013-08-ai-open-webui/plan.md](../../98.archive/changes/chg-0013-08-ai-open-webui/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0013-08-ai-open-webui/task.md](../../98.archive/changes/chg-0013-08-ai-open-webui/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0015-01-gateway-optimization-hardening/plan.md](../../98.archive/changes/chg-0015-01-gateway-optimization-hardening/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0015-01-gateway-optimization-hardening/task.md](../../98.archive/changes/chg-0015-01-gateway-optimization-hardening/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0016-02-auth-optimization-hardening/plan.md](../../98.archive/changes/chg-0016-02-auth-optimization-hardening/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0016-02-auth-optimization-hardening/task.md](../../98.archive/changes/chg-0016-02-auth-optimization-hardening/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0017-03-security-optimization-hardening/plan.md](../../98.archive/changes/chg-0017-03-security-optimization-hardening/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0017-03-security-optimization-hardening/task.md](../../98.archive/changes/chg-0017-03-security-optimization-hardening/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0018-04-data-optimization-hardening/plan.md](../../98.archive/changes/chg-0018-04-data-optimization-hardening/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0018-04-data-optimization-hardening/task.md](../../98.archive/changes/chg-0018-04-data-optimization-hardening/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0019-05-messaging-optimization-hardening/plan.md](../../98.archive/changes/chg-0019-05-messaging-optimization-hardening/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0019-05-messaging-optimization-hardening/task.md](../../98.archive/changes/chg-0019-05-messaging-optimization-hardening/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0020-06-observability-optimization-hardening/plan.md](../../98.archive/changes/chg-0020-06-observability-optimization-hardening/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0020-06-observability-optimization-hardening/task.md](../../98.archive/changes/chg-0020-06-observability-optimization-hardening/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0021-07-workflow-optimization-hardening/plan.md](../../98.archive/changes/chg-0021-07-workflow-optimization-hardening/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0021-07-workflow-optimization-hardening/task.md](../../98.archive/changes/chg-0021-07-workflow-optimization-hardening/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0022-08-ai-optimization-hardening/plan.md](../../98.archive/changes/chg-0022-08-ai-optimization-hardening/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0022-08-ai-optimization-hardening/task.md](../../98.archive/changes/chg-0022-08-ai-optimization-hardening/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0023-09-tooling-optimization-hardening/plan.md](../../98.archive/changes/chg-0023-09-tooling-optimization-hardening/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0023-09-tooling-optimization-hardening/task.md](../../98.archive/changes/chg-0023-09-tooling-optimization-hardening/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0024-11-laboratory-optimization-hardening/plan.md](../../98.archive/changes/chg-0024-11-laboratory-optimization-hardening/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0024-11-laboratory-optimization-hardening/task.md](../../98.archive/changes/chg-0024-11-laboratory-optimization-hardening/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0025-standardize-infra-net/plan.md](../../98.archive/changes/chg-0025-standardize-infra-net/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0025-standardize-infra-net/task.md](../../98.archive/changes/chg-0025-standardize-infra-net/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0026-infra-team-agent-cross-validation/plan.md](../../98.archive/changes/chg-0026-infra-team-agent-cross-validation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0026-infra-team-agent-cross-validation/task.md](../../98.archive/changes/chg-0026-infra-team-agent-cross-validation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0027-harness-agent-first-engineering/plan.md](../../98.archive/changes/chg-0027-harness-agent-first-engineering/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0027-harness-agent-first-engineering/task.md](../../98.archive/changes/chg-0027-harness-agent-first-engineering/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0028-infra-secrets-docs-refresh/plan.md](../../98.archive/changes/chg-0028-infra-secrets-docs-refresh/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0028-infra-secrets-docs-refresh/task.md](../../98.archive/changes/chg-0028-infra-secrets-docs-refresh/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0029-scripts-lifecycle-contract-cleanup/plan.md](../../98.archive/changes/chg-0029-scripts-lifecycle-contract-cleanup/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0029-scripts-lifecycle-contract-cleanup/task.md](../../98.archive/changes/chg-0029-scripts-lifecycle-contract-cleanup/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0030-docs-taxonomy-agent-first-migration/plan.md](../../98.archive/changes/chg-0030-docs-taxonomy-agent-first-migration/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0030-docs-taxonomy-agent-first-migration/task.md](../../98.archive/changes/chg-0030-docs-taxonomy-agent-first-migration/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0031-llm-wiki-agent-first-completion/plan.md](../../98.archive/changes/chg-0031-llm-wiki-agent-first-completion/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0031-llm-wiki-agent-first-completion/task.md](../../98.archive/changes/chg-0031-llm-wiki-agent-first-completion/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0032-requirements-standardization/plan.md](../../98.archive/changes/chg-0032-requirements-standardization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0032-requirements-standardization/task.md](../../98.archive/changes/chg-0032-requirements-standardization/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0033-scripts-ci-qa-cleanup/plan.md](../../98.archive/changes/chg-0033-scripts-ci-qa-cleanup/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0033-scripts-ci-qa-cleanup/task.md](../../98.archive/changes/chg-0033-scripts-ci-qa-cleanup/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0034-docs-05-operations-purpose-remediation/plan.md](../../98.archive/changes/chg-0034-docs-05-operations-purpose-remediation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0034-docs-05-operations-purpose-remediation/task.md](../../98.archive/changes/chg-0034-docs-05-operations-purpose-remediation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0035-docs-bounded-consistency-audit/plan.md](../../98.archive/changes/chg-0035-docs-bounded-consistency-audit/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0035-docs-bounded-consistency-audit/task.md](../../98.archive/changes/chg-0035-docs-bounded-consistency-audit/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0036-execution-stage-remediation/plan.md](../../98.archive/changes/chg-0036-execution-stage-remediation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0036-execution-stage-remediation/task.md](../../98.archive/changes/chg-0036-execution-stage-remediation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0037-targeted-docs-precision-remediation/plan.md](../../98.archive/changes/chg-0037-targeted-docs-precision-remediation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0037-targeted-docs-precision-remediation/task.md](../../98.archive/changes/chg-0037-targeted-docs-precision-remediation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0038-agent-hook-completion-style-automation/plan.md](../../98.archive/changes/chg-0038-agent-hook-completion-style-automation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0038-agent-hook-completion-style-automation/task.md](../../98.archive/changes/chg-0038-agent-hook-completion-style-automation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0039-data-analytics-execution-traceability/plan.md](../../98.archive/changes/chg-0039-data-analytics-execution-traceability/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0039-data-analytics-execution-traceability/task.md](../../98.archive/changes/chg-0039-data-analytics-execution-traceability/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0040-lifecycle-readme-debt-closure/plan.md](../../98.archive/changes/chg-0040-lifecycle-readme-debt-closure/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0040-lifecycle-readme-debt-closure/task.md](../../98.archive/changes/chg-0040-lifecycle-readme-debt-closure/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0041-spec-execution-implementation-audit/plan.md](../../98.archive/changes/chg-0041-spec-execution-implementation-audit/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0041-spec-execution-implementation-audit/task.md](../../98.archive/changes/chg-0041-spec-execution-implementation-audit/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0042-workspace-docs-agent-governance-remediation/plan.md](../../98.archive/changes/chg-0042-workspace-docs-agent-governance-remediation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0042-workspace-docs-agent-governance-remediation/task.md](../../98.archive/changes/chg-0042-workspace-docs-agent-governance-remediation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0043-workspace-governance-bounded-reaudit/plan.md](../../98.archive/changes/chg-0043-workspace-governance-bounded-reaudit/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0043-workspace-governance-bounded-reaudit/task.md](../../98.archive/changes/chg-0043-workspace-governance-bounded-reaudit/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0044-workspace-audit-grill-review/plan.md](../../98.archive/changes/chg-0044-workspace-audit-grill-review/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0044-workspace-audit-grill-review/task.md](../../98.archive/changes/chg-0044-workspace-audit-grill-review/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0045-workspace-audit-improvement/plan.md](../../98.archive/changes/chg-0045-workspace-audit-improvement/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0045-workspace-audit-improvement/task.md](../../98.archive/changes/chg-0045-workspace-audit-improvement/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0046-workspace-audit-input-task-gap-closure/plan.md](../../98.archive/changes/chg-0046-workspace-audit-input-task-gap-closure/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0046-workspace-audit-input-task-gap-closure/task.md](../../98.archive/changes/chg-0046-workspace-audit-input-task-gap-closure/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0047-home-docker-revalidation-deferred-follow-up/plan.md](../../98.archive/changes/chg-0047-home-docker-revalidation-deferred-follow-up/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0047-home-docker-revalidation-deferred-follow-up/task.md](../../98.archive/changes/chg-0047-home-docker-revalidation-deferred-follow-up/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0048-home-docker-workspace-audit-improvement/plan.md](../../98.archive/changes/chg-0048-home-docker-workspace-audit-improvement/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0048-home-docker-workspace-audit-improvement/task.md](../../98.archive/changes/chg-0048-home-docker-workspace-audit-improvement/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0049-large-scale-authored-ssot-review/plan.md](../../98.archive/changes/chg-0049-large-scale-authored-ssot-review/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0049-large-scale-authored-ssot-review/task.md](../../98.archive/changes/chg-0049-large-scale-authored-ssot-review/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0050-workspace-audit-gap-closure/plan.md](../../98.archive/changes/chg-0050-workspace-audit-gap-closure/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0050-workspace-audit-gap-closure/task.md](../../98.archive/changes/chg-0050-workspace-audit-gap-closure/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0051-workspace-audit/plan.md](../../98.archive/changes/chg-0051-workspace-audit/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0051-workspace-audit/task.md](../../98.archive/changes/chg-0051-workspace-audit/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0052-workspace-doc-consistency/plan.md](../../98.archive/changes/chg-0052-workspace-doc-consistency/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0052-workspace-doc-consistency/task.md](../../98.archive/changes/chg-0052-workspace-doc-consistency/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0053-workspace-consistency-2026-05b/plan.md](../../98.archive/changes/chg-0053-workspace-consistency-2026-05b/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0053-workspace-consistency-2026-05b/task.md](../../98.archive/changes/chg-0053-workspace-consistency-2026-05b/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0054-claude-harness-governance-verification/plan.md](../../98.archive/changes/chg-0054-claude-harness-governance-verification/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0054-claude-harness-governance-verification/task.md](../../98.archive/changes/chg-0054-claude-harness-governance-verification/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0055-agent-governance-decision-items/plan.md](../../98.archive/changes/chg-0055-agent-governance-decision-items/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0056-agent-governance-phase-1-revalidation/plan.md](../../98.archive/changes/chg-0056-agent-governance-phase-1-revalidation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0056-agent-governance-phase-1-revalidation/task.md](../../98.archive/changes/chg-0056-agent-governance-phase-1-revalidation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0057-agent-governance-phase-2-strategy-integration/plan.md](../../98.archive/changes/chg-0057-agent-governance-phase-2-strategy-integration/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0057-agent-governance-phase-2-strategy-integration/task.md](../../98.archive/changes/chg-0057-agent-governance-phase-2-strategy-integration/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0058-agent-governance-phase-3-approved-surface-activation/plan.md](../../98.archive/changes/chg-0058-agent-governance-phase-3-approved-surface-activation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0058-agent-governance-phase-3-approved-surface-activation/task.md](../../98.archive/changes/chg-0058-agent-governance-phase-3-approved-surface-activation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0059-agent-governance-phase-4-closure-reconciliation/plan.md](../../98.archive/changes/chg-0059-agent-governance-phase-4-closure-reconciliation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0059-agent-governance-phase-4-closure-reconciliation/task.md](../../98.archive/changes/chg-0059-agent-governance-phase-4-closure-reconciliation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0060-docs-implementation-reconciliation/plan.md](../../98.archive/changes/chg-0060-docs-implementation-reconciliation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0060-docs-implementation-reconciliation/task.md](../../98.archive/changes/chg-0060-docs-implementation-reconciliation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0061-governance-optimization/plan.md](../../98.archive/changes/chg-0061-governance-optimization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0061-governance-optimization/task.md](../../98.archive/changes/chg-0061-governance-optimization/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0062-governance-surgical-reverification/plan.md](../../98.archive/changes/chg-0062-governance-surgical-reverification/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0062-governance-surgical-reverification/task.md](../../98.archive/changes/chg-0062-governance-surgical-reverification/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0063-template-system-reorganization/plan.md](../../98.archive/changes/chg-0063-template-system-reorganization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0063-template-system-reorganization/task.md](../../98.archive/changes/chg-0063-template-system-reorganization/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0064-document-contract-remediation-batches/plan.md](../../98.archive/changes/chg-0064-document-contract-remediation-batches/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0064-document-contract-remediation-batches/task.md](../../98.archive/changes/chg-0064-document-contract-remediation-batches/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0065-template-system-contract-standardization/plan.md](../../98.archive/changes/chg-0065-template-system-contract-standardization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0065-template-system-contract-standardization/task.md](../../98.archive/changes/chg-0065-template-system-contract-standardization/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0066-workspace-document-contract-audit-pack/plan.md](../../98.archive/changes/chg-0066-workspace-document-contract-audit-pack/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0066-workspace-document-contract-audit-pack/task.md](../../98.archive/changes/chg-0066-workspace-document-contract-audit-pack/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0067-document-restructure-audit-contract-archive/plan.md](../../98.archive/changes/chg-0067-document-restructure-audit-contract-archive/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0067-document-restructure-audit-contract-archive/task.md](../../98.archive/changes/chg-0067-document-restructure-audit-contract-archive/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0068-agent-output-eval-fixtures/plan.md](../../98.archive/changes/chg-0068-agent-output-eval-fixtures/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0068-agent-output-eval-fixtures/task.md](../../98.archive/changes/chg-0068-agent-output-eval-fixtures/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0069-agentic-engineering-implementation-audit-pack/plan.md](../../98.archive/changes/chg-0069-agentic-engineering-implementation-audit-pack/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0069-agentic-engineering-implementation-audit-pack/task.md](../../98.archive/changes/chg-0069-agentic-engineering-implementation-audit-pack/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0070-agentic-research-pack-refresh/plan.md](../../98.archive/changes/chg-0070-agentic-research-pack-refresh/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0070-agentic-research-pack-refresh/task.md](../../98.archive/changes/chg-0070-agentic-research-pack-refresh/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0071-audit-pack-coverage-report/plan.md](../../98.archive/changes/chg-0071-audit-pack-coverage-report/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0071-audit-pack-coverage-report/task.md](../../98.archive/changes/chg-0071-audit-pack-coverage-report/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0072-compose-profile-service-coverage-snapshot/plan.md](../../98.archive/changes/chg-0072-compose-profile-service-coverage-snapshot/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0072-compose-profile-service-coverage-snapshot/task.md](../../98.archive/changes/chg-0072-compose-profile-service-coverage-snapshot/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0073-gap-routing-recommendation/plan.md](../../98.archive/changes/chg-0073-gap-routing-recommendation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0073-gap-routing-recommendation/task.md](../../98.archive/changes/chg-0073-gap-routing-recommendation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0074-provider-semantic-parity-validator/plan.md](../../98.archive/changes/chg-0074-provider-semantic-parity-validator/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0074-provider-semantic-parity-validator/task.md](../../98.archive/changes/chg-0074-provider-semantic-parity-validator/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0075-provider-workspace-artifact-path-parity/plan.md](../../98.archive/changes/chg-0075-provider-workspace-artifact-path-parity/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0075-provider-workspace-artifact-path-parity/task.md](../../98.archive/changes/chg-0075-provider-workspace-artifact-path-parity/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0076-qa-gate-recommendation-ci-summary/plan.md](../../98.archive/changes/chg-0076-qa-gate-recommendation-ci-summary/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0076-qa-gate-recommendation-ci-summary/task.md](../../98.archive/changes/chg-0076-qa-gate-recommendation-ci-summary/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0077-template-system-numbered-sdlc-paths/plan.md](../../98.archive/changes/chg-0077-template-system-numbered-sdlc-paths/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0077-template-system-numbered-sdlc-paths/task.md](../../98.archive/changes/chg-0077-template-system-numbered-sdlc-paths/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0078-workspace-support-surface-contract/plan.md](../../98.archive/changes/chg-0078-workspace-support-surface-contract/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0078-workspace-support-surface-contract/task.md](../../98.archive/changes/chg-0078-workspace-support-surface-contract/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0079-agent-output-eval-ci-gate/plan.md](../../98.archive/changes/chg-0079-agent-output-eval-ci-gate/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0079-agent-output-eval-ci-gate/task.md](../../98.archive/changes/chg-0079-agent-output-eval-ci-gate/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0080-agent-output-eval-runner/plan.md](../../98.archive/changes/chg-0080-agent-output-eval-runner/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0080-agent-output-eval-runner/task.md](../../98.archive/changes/chg-0080-agent-output-eval-runner/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0081-audit-implementation-matrix-snapshot/plan.md](../../98.archive/changes/chg-0081-audit-implementation-matrix-snapshot/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0081-audit-implementation-matrix-snapshot/task.md](../../98.archive/changes/chg-0081-audit-implementation-matrix-snapshot/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0082-dependency-vulnerability-audit-gate/plan.md](../../98.archive/changes/chg-0082-dependency-vulnerability-audit-gate/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0082-dependency-vulnerability-audit-gate/task.md](../../98.archive/changes/chg-0082-dependency-vulnerability-audit-gate/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0083-llm-wiki-stage-category-coverage/plan.md](../../98.archive/changes/chg-0083-llm-wiki-stage-category-coverage/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0083-llm-wiki-stage-category-coverage/task.md](../../98.archive/changes/chg-0083-llm-wiki-stage-category-coverage/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0084-provider-hook-parity-matrix/plan.md](../../98.archive/changes/chg-0084-provider-hook-parity-matrix/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0084-provider-hook-parity-matrix/task.md](../../98.archive/changes/chg-0084-provider-hook-parity-matrix/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0085-sdlc-document-contract-corpus-normalization/plan.md](../../98.archive/changes/chg-0085-sdlc-document-contract-corpus-normalization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0085-sdlc-document-contract-corpus-normalization/task.md](../../98.archive/changes/chg-0085-sdlc-document-contract-corpus-normalization/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0086-security-automation-readiness-snapshot/plan.md](../../98.archive/changes/chg-0086-security-automation-readiness-snapshot/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0086-security-automation-readiness-snapshot/task.md](../../98.archive/changes/chg-0086-security-automation-readiness-snapshot/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0087-tech-stack-version-provenance/plan.md](../../98.archive/changes/chg-0087-tech-stack-version-provenance/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0087-tech-stack-version-provenance/task.md](../../98.archive/changes/chg-0087-tech-stack-version-provenance/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0088-agentic-research-pack-consolidation/plan.md](../../98.archive/changes/chg-0088-agentic-research-pack-consolidation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0088-agentic-research-pack-consolidation/task.md](../../98.archive/changes/chg-0088-agentic-research-pack-consolidation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0089-agentic-engineering-audit-remediation/plan.md](../../98.archive/changes/chg-0089-agentic-engineering-audit-remediation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0089-agentic-engineering-audit-remediation/task.md](../../98.archive/changes/chg-0089-agentic-engineering-audit-remediation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0090-compose-runtime-readiness-remediation/plan.md](../../98.archive/changes/chg-0090-compose-runtime-readiness-remediation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0090-compose-runtime-readiness-remediation/task.md](../../98.archive/changes/chg-0090-compose-runtime-readiness-remediation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0091-deployment-release-engineering-remediation/plan.md](../../98.archive/changes/chg-0091-deployment-release-engineering-remediation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0091-deployment-release-engineering-remediation/task.md](../../98.archive/changes/chg-0091-deployment-release-engineering-remediation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0092-infrastructure-operations-readiness-remediation/plan.md](../../98.archive/changes/chg-0092-infrastructure-operations-readiness-remediation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0092-infrastructure-operations-readiness-remediation/task.md](../../98.archive/changes/chg-0092-infrastructure-operations-readiness-remediation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0093-security-supply-chain-remediation/plan.md](../../98.archive/changes/chg-0093-security-supply-chain-remediation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0093-security-supply-chain-remediation/task.md](../../98.archive/changes/chg-0093-security-supply-chain-remediation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0094-agentic-audit-harness-consolidation/plan.md](../../98.archive/changes/chg-0094-agentic-audit-harness-consolidation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0094-agentic-audit-harness-consolidation/task.md](../../98.archive/changes/chg-0094-agentic-audit-harness-consolidation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0095-document-contract-canonicalization/plan.md](../../98.archive/changes/chg-0095-document-contract-canonicalization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0095-document-contract-canonicalization/task.md](../../98.archive/changes/chg-0095-document-contract-canonicalization/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0096-template-contract-system-canonicalization/plan.md](../../98.archive/changes/chg-0096-template-contract-system-canonicalization/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0096-template-contract-system-canonicalization/task.md](../../98.archive/changes/chg-0096-template-contract-system-canonicalization/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0097-document-corpus-lifecycle-migration-foundation/plan.md](../../98.archive/changes/chg-0097-document-corpus-lifecycle-migration-foundation/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0097-document-corpus-lifecycle-migration-foundation/task.md](../../98.archive/changes/chg-0097-document-corpus-lifecycle-migration-foundation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0098-agent-governance-harness-convergence/plan.md](../../98.archive/changes/chg-0098-agent-governance-harness-convergence/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0098-agent-governance-harness-convergence/task.md](../../98.archive/changes/chg-0098-agent-governance-harness-convergence/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0099-target-surface-contract-convergence/plan.md](../../98.archive/changes/chg-0099-target-surface-contract-convergence/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0099-target-surface-contract-convergence/task.md](../../98.archive/changes/chg-0099-target-surface-contract-convergence/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0100-operational-readiness-closure-program/plan.md](../../98.archive/changes/chg-0100-operational-readiness-closure-program/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0100-operational-readiness-closure-program/task.md](../../98.archive/changes/chg-0100-operational-readiness-closure-program/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0104-01-gateway/task.md](../../98.archive/changes/chg-0104-01-gateway/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0105-02-auth/task.md](../../98.archive/changes/chg-0105-02-auth/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0106-03-security/task.md](../../98.archive/changes/chg-0106-03-security/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0107-04-data/task.md](../../98.archive/changes/chg-0107-04-data/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0108-05-messaging/task.md](../../98.archive/changes/chg-0108-05-messaging/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0109-06-observability/task.md](../../98.archive/changes/chg-0109-06-observability/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0110-07-workflow/task.md](../../98.archive/changes/chg-0110-07-workflow/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0111-08-ai/task.md](../../98.archive/changes/chg-0111-08-ai/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0112-09-tooling/task.md](../../98.archive/changes/chg-0112-09-tooling/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0113-10-communication/task.md](../../98.archive/changes/chg-0113-10-communication/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0114-11-laboratory/task.md](../../98.archive/changes/chg-0114-11-laboratory/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0115-agent-governance-missing-items-implementation/task.md](../../98.archive/changes/chg-0115-agent-governance-missing-items-implementation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0116-docs-implementation-audit/task.md](../../98.archive/changes/chg-0116-docs-implementation-audit/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0117-harness-engineering/task.md](../../98.archive/changes/chg-0117-harness-engineering/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0118-language-policy-boundary-audit/task.md](../../98.archive/changes/chg-0118-language-policy-boundary-audit/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0119-language-policy-hard-enforcement/task.md](../../98.archive/changes/chg-0119-language-policy-hard-enforcement/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0120-language-policy-normalization-batch-1/task.md](../../98.archive/changes/chg-0120-language-policy-normalization-batch-1/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0121-language-policy-normalization-batch-2/task.md](../../98.archive/changes/chg-0121-language-policy-normalization-batch-2/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0122-language-policy-normalization-batch-3/task.md](../../98.archive/changes/chg-0122-language-policy-normalization-batch-3/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0123-language-policy-plan-normalization-batch-1/task.md](../../98.archive/changes/chg-0123-language-policy-plan-normalization-batch-1/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0124-language-policy-plan-normalization-batch-2/task.md](../../98.archive/changes/chg-0124-language-policy-plan-normalization-batch-2/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0125-language-policy-plan-normalization-batch-3/task.md](../../98.archive/changes/chg-0125-language-policy-plan-normalization-batch-3/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0126-language-policy-plan-normalization-batch-4/task.md](../../98.archive/changes/chg-0126-language-policy-plan-normalization-batch-4/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0127-language-policy-plan-normalization-batch-5/task.md](../../98.archive/changes/chg-0127-language-policy-plan-normalization-batch-5/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0128-language-policy-plan-normalization-batch-6/task.md](../../98.archive/changes/chg-0128-language-policy-plan-normalization-batch-6/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0129-language-policy-plan-normalization-batch-7/task.md](../../98.archive/changes/chg-0129-language-policy-plan-normalization-batch-7/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0130-language-policy-plan-normalization-batch-8/task.md](../../98.archive/changes/chg-0130-language-policy-plan-normalization-batch-8/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0131-language-policy-reference-normalization/task.md](../../98.archive/changes/chg-0131-language-policy-reference-normalization/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0132-language-policy-task-normalization-batch-1/task.md](../../98.archive/changes/chg-0132-language-policy-task-normalization-batch-1/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0133-language-policy-task-normalization-batch-2/task.md](../../98.archive/changes/chg-0133-language-policy-task-normalization-batch-2/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0134-language-policy-task-normalization-batch-3/task.md](../../98.archive/changes/chg-0134-language-policy-task-normalization-batch-3/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0135-language-policy-task-normalization-batch-4/task.md](../../98.archive/changes/chg-0135-language-policy-task-normalization-batch-4/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0136-language-policy-task-normalization-batch-5/task.md](../../98.archive/changes/chg-0136-language-policy-task-normalization-batch-5/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0137-language-policy-task-normalization-batch-6/task.md](../../98.archive/changes/chg-0137-language-policy-task-normalization-batch-6/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0138-language-policy-task-normalization-batch-7/task.md](../../98.archive/changes/chg-0138-language-policy-task-normalization-batch-7/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0139-examples-scaffold-contract-remediation/task.md](../../98.archive/changes/chg-0139-examples-scaffold-contract-remediation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0140-frontmatter-routing-evidence-refresh/task.md](../../98.archive/changes/chg-0140-frontmatter-routing-evidence-refresh/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0141-github-branch-protection-reverification/task.md](../../98.archive/changes/chg-0141-github-branch-protection-reverification/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0142-infra-tech-stack-version-refresh/task.md](../../98.archive/changes/chg-0142-infra-tech-stack-version-refresh/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0143-ai-governance-reorg/plan.md](../../98.archive/changes/chg-0143-ai-governance-reorg/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0144-standardizing-agent-governance/plan.md](../../98.archive/changes/chg-0144-standardizing-agent-governance/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0144-standardizing-agent-governance/task.md](../../98.archive/changes/chg-0144-standardizing-agent-governance/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0145-agent-governance-phase1-diagnostic/plan.md](../../98.archive/changes/chg-0145-agent-governance-phase1-diagnostic/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0145-agent-governance-phase1-diagnostic/task.md](../../98.archive/changes/chg-0145-agent-governance-phase1-diagnostic/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0146-agent-governance-phase2-alignment/plan.md](../../98.archive/changes/chg-0146-agent-governance-phase2-alignment/plan.md) | Markdown reference |
| [docs/98.archive/changes/chg-0147-agent-governance-phase3-implementation/task.md](../../98.archive/changes/chg-0147-agent-governance-phase3-implementation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0148-agent-governance-phase3-stage01-02-continuation/task.md](../../98.archive/changes/chg-0148-agent-governance-phase3-stage01-02-continuation/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0149-agent-governance-phase3-strategy-integration/task.md](../../98.archive/changes/chg-0149-agent-governance-phase3-strategy-integration/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0150-agent-governance-phase4-closure/task.md](../../98.archive/changes/chg-0150-agent-governance-phase4-closure/task.md) | Markdown reference |
| [docs/98.archive/changes/chg-0151-agent-governance-stage01-02-alignment/task.md](../../98.archive/changes/chg-0151-agent-governance-stage01-02-alignment/task.md) | Markdown reference |
| [docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md](../../98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0099-template-system-numbered-sdlc-paths.md](../../98.archive/tombstones/03.specs/spec-0099-template-system-numbered-sdlc-paths.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0100-template-system-contract-standardization.md](../../98.archive/tombstones/03.specs/spec-0100-template-system-contract-standardization.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0101-template-system-reorganization.md](../../98.archive/tombstones/03.specs/spec-0101-template-system-reorganization.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0104-agentic-research-pack-refresh.md](../../98.archive/tombstones/03.specs/spec-0104-agentic-research-pack-refresh.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0106-workspace-support-surface-contract.md](../../98.archive/tombstones/03.specs/spec-0106-workspace-support-surface-contract.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0107-provider-semantic-parity-validator.md](../../98.archive/tombstones/03.specs/spec-0107-provider-semantic-parity-validator.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0108-compose-profile-service-coverage-snapshot.md](../../98.archive/tombstones/03.specs/spec-0108-compose-profile-service-coverage-snapshot.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0109-gap-routing-recommendation.md](../../98.archive/tombstones/03.specs/spec-0109-gap-routing-recommendation.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0110-agent-output-eval-fixtures.md](../../98.archive/tombstones/03.specs/spec-0110-agent-output-eval-fixtures.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0111-qa-gate-recommendation-ci-summary.md](../../98.archive/tombstones/03.specs/spec-0111-qa-gate-recommendation-ci-summary.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0112-audit-pack-coverage-report.md](../../98.archive/tombstones/03.specs/spec-0112-audit-pack-coverage-report.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0113-llm-wiki-stage-category-coverage.md](../../98.archive/tombstones/03.specs/spec-0113-llm-wiki-stage-category-coverage.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0114-tech-stack-version-provenance.md](../../98.archive/tombstones/03.specs/spec-0114-tech-stack-version-provenance.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0115-provider-hook-parity-matrix.md](../../98.archive/tombstones/03.specs/spec-0115-provider-hook-parity-matrix.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0116-agent-output-eval-runner.md](../../98.archive/tombstones/03.specs/spec-0116-agent-output-eval-runner.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0117-security-automation-readiness-snapshot.md](../../98.archive/tombstones/03.specs/spec-0117-security-automation-readiness-snapshot.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0118-audit-implementation-matrix-snapshot.md](../../98.archive/tombstones/03.specs/spec-0118-audit-implementation-matrix-snapshot.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0119-sdlc-document-contract-corpus-normalization.md](../../98.archive/tombstones/03.specs/spec-0119-sdlc-document-contract-corpus-normalization.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0120-agent-output-eval-ci-gate.md](../../98.archive/tombstones/03.specs/spec-0120-agent-output-eval-ci-gate.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0121-dependency-vulnerability-audit-gate.md](../../98.archive/tombstones/03.specs/spec-0121-dependency-vulnerability-audit-gate.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0122-agentic-research-pack-consolidation.md](../../98.archive/tombstones/03.specs/spec-0122-agentic-research-pack-consolidation.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0124-compose-runtime-readiness-remediation.md](../../98.archive/tombstones/03.specs/spec-0124-compose-runtime-readiness-remediation.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0125-infrastructure-operations-readiness-remediation.md](../../98.archive/tombstones/03.specs/spec-0125-infrastructure-operations-readiness-remediation.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0126-security-supply-chain-remediation.md](../../98.archive/tombstones/03.specs/spec-0126-security-supply-chain-remediation.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0127-deployment-release-engineering-remediation.md](../../98.archive/tombstones/03.specs/spec-0127-deployment-release-engineering-remediation.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0128-agentic-audit-harness-consolidation.md](../../98.archive/tombstones/03.specs/spec-0128-agentic-audit-harness-consolidation.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0129-document-contract-canonicalization.md](../../98.archive/tombstones/03.specs/spec-0129-document-contract-canonicalization.md) | Markdown reference |
| [docs/98.archive/tombstones/03.specs/spec-0130-template-contract-system-canonicalization.md](../../98.archive/tombstones/03.specs/spec-0130-template-contract-system-canonicalization.md) | Markdown reference |
| [docs/98.archive/tombstones/05.operations/ref-0086-01-setup.md](../../98.archive/tombstones/05.operations/ref-0086-01-setup.md) | Markdown reference |
| [docs/98.archive/tombstones/05.operations/ref-0087-ksql-streaming.md](../../98.archive/tombstones/05.operations/ref-0087-ksql-streaming.md) | Markdown reference |
| [docs/98.archive/tombstones/05.operations/ref-0088-01-airflow-dag-dev.md](../../98.archive/tombstones/05.operations/ref-0088-01-airflow-dag-dev.md) | Markdown reference |
| [docs/98.archive/tombstones/05.operations/ref-0089-airbyte.md](../../98.archive/tombstones/05.operations/ref-0089-airbyte.md) | Markdown reference |
| [docs/98.archive/tombstones/05.operations/ref-0090-01-llm-inference.md](../../98.archive/tombstones/05.operations/ref-0090-01-llm-inference.md) | Markdown reference |
| [docs/98.archive/tombstones/05.operations/ref-0091-local-llm-setup.md](../../98.archive/tombstones/05.operations/ref-0091-local-llm-setup.md) | Markdown reference |
| [docs/98.archive/tombstones/05.operations/ref-0092-01-iac-automation.md](../../98.archive/tombstones/05.operations/ref-0092-01-iac-automation.md) | Markdown reference |
| [docs/98.archive/tombstones/05.operations/ref-0093-airbyte.md](../../98.archive/tombstones/05.operations/ref-0093-airbyte.md) | Markdown reference |
| [docs/98.archive/tombstones/05.operations/ref-0094-airbyte.md](../../98.archive/tombstones/05.operations/ref-0094-airbyte.md) | Markdown reference |
| [docs/98.archive/tombstones/05.operations/ref-0095-windows-network-ip.md](../../98.archive/tombstones/05.operations/ref-0095-windows-network-ip.md) | Markdown reference |

## Sources

- [llms.txt](../../../llms.txt) - root LLM entrypoint and boundary statement
- [ref-0083-repository-map.md](./ref-0083-repository-map.md) - curated canonical source map
- [generate-llm-wiki.py](../../../scripts/knowledge/generate-llm-wiki.py) - deterministic two-output generator
- [check-script-manifest.py](../../../scripts/validation/check-script-manifest.py) - aggregate generated-output freshness gate

## Maintenance

- **Owner**: `doc-writer` using the `knowledge-map-agent` function
- **Review Cadence**: Review when root entrypoints, governance, operations docs, script inventory, infrastructure indexes, or LLM Wiki files change
- **Update Trigger**: Run `python3 scripts/knowledge/generate-llm-wiki.py --write` after in-scope path changes and `python3 scripts/knowledge/generate-llm-wiki.py --check` during validation

## Related Documents

- [LLM Wiki references](./README.md)
- [LLM Wiki repository map](./ref-0083-repository-map.md)
- [LLM Wiki maintenance guide](../../05.operations/00-workspace/ops-0007-llm-wiki-maintenance/guide.md)
- [Agent governance hub](../../00.agent-governance/README.md)
