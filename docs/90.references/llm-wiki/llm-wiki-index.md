---
status: active
generated_by: scripts/knowledge/generate-llm-wiki-index.sh
---

<!-- Target: docs/90.references/llm-wiki/llm-wiki-index.md -->

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
- Deterministic refresh through `bash scripts/knowledge/generate-llm-wiki-index.sh`.

### Out of Scope

- Public website or public wiki deployment.
- `llms-full.txt` or any full-content export.
- External model calls, network publishing, deployment workflow, or Docker runtime behavior.
- Secret contents, credentials, private keys, tokens, shell history, raw logs, `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` as evidence.

## Definitions / Facts

- **Generated tracked repo-local index**: a committed Markdown path index regenerated from safe repository paths.
- **Tracked source boundary**: `git ls-files` is the primary path source; known in-progress LLM Wiki contract files are included only when present locally.
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
| [docs/90.references/llm-wiki/repository-map.md](repository-map.md) | Markdown reference |

### Agent governance

| Path | Role |
| --- | --- |
| [docs/00.agent-governance/README.md](../../00.agent-governance/README.md) | folder index |
| [docs/00.agent-governance/agents/README.md](../../00.agent-governance/agents/README.md) | folder index |
| [docs/00.agent-governance/agents/agents/ci-cd-engineer.md](../../00.agent-governance/agents/agents/ci-cd-engineer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/code-reviewer.md](../../00.agent-governance/agents/agents/code-reviewer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/doc-writer.md](../../00.agent-governance/agents/agents/doc-writer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/drift-detector.md](../../00.agent-governance/agents/agents/drift-detector.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/hook-developer.md](../../00.agent-governance/agents/agents/hook-developer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/iac-reviewer.md](../../00.agent-governance/agents/agents/iac-reviewer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/incident-responder.md](../../00.agent-governance/agents/agents/incident-responder.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/infra-implementer.md](../../00.agent-governance/agents/agents/infra-implementer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/qa-engineer.md](../../00.agent-governance/agents/agents/qa-engineer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/rules-engineer.md](../../00.agent-governance/agents/agents/rules-engineer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/security-auditor.md](../../00.agent-governance/agents/agents/security-auditor.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/skill-creator.md](../../00.agent-governance/agents/agents/skill-creator.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/style-enforcer.md](../../00.agent-governance/agents/agents/style-enforcer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/wiki-curator.md](../../00.agent-governance/agents/agents/wiki-curator.md) | Markdown reference |
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
| [docs/00.agent-governance/agents/functions/requirements-to-design-agent.md](../../00.agent-governance/agents/functions/requirements-to-design-agent.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/security-audit.md](../../00.agent-governance/agents/functions/security-audit.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/style-validation.md](../../00.agent-governance/agents/functions/style-validation.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/task-breakdown-agent.md](../../00.agent-governance/agents/functions/task-breakdown-agent.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/test-automator.md](../../00.agent-governance/agents/functions/test-automator.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/workspace-audit-revalidation.md](../../00.agent-governance/agents/functions/workspace-audit-revalidation.md) | Markdown reference |
| [docs/00.agent-governance/harness-implementation-map.md](../../00.agent-governance/harness-implementation-map.md) | Markdown reference |
| [docs/00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md](../../00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md) | Markdown reference |
| [docs/00.agent-governance/memory/README.md](../../00.agent-governance/memory/README.md) | folder index |
| [docs/00.agent-governance/memory/agentic-harness-contract-hardening.md](../../00.agent-governance/memory/agentic-harness-contract-hardening.md) | Markdown reference |
| [docs/00.agent-governance/memory/docker-doc-contract-backlog.md](../../00.agent-governance/memory/docker-doc-contract-backlog.md) | Markdown reference |
| [docs/00.agent-governance/memory/execution-stage-legacy-debt.md](../../00.agent-governance/memory/execution-stage-legacy-debt.md) | Markdown reference |
| [docs/00.agent-governance/memory/github-ci-contract-audit.md](../../00.agent-governance/memory/github-ci-contract-audit.md) | Markdown reference |
| [docs/00.agent-governance/memory/governance-memory-usage-contract.md](../../00.agent-governance/memory/governance-memory-usage-contract.md) | Markdown reference |
| [docs/00.agent-governance/memory/harness-agent-first-gap-audit.md](../../00.agent-governance/memory/harness-agent-first-gap-audit.md) | Markdown reference |
| [docs/00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md) | Markdown reference |
| [docs/00.agent-governance/memory/stage-docs-lifecycle-audit.md](../../00.agent-governance/memory/stage-docs-lifecycle-audit.md) | Markdown reference |
| [docs/00.agent-governance/memory/template.md](../../00.agent-governance/memory/template.md) | Markdown reference |
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
| [docs/00.agent-governance/scopes/backend.md](../../00.agent-governance/scopes/backend.md) | Markdown reference |
| [docs/00.agent-governance/scopes/common.md](../../00.agent-governance/scopes/common.md) | Markdown reference |
| [docs/00.agent-governance/scopes/docs.md](../../00.agent-governance/scopes/docs.md) | Markdown reference |
| [docs/00.agent-governance/scopes/entry.md](../../00.agent-governance/scopes/entry.md) | Markdown reference |
| [docs/00.agent-governance/scopes/frontend.md](../../00.agent-governance/scopes/frontend.md) | Markdown reference |
| [docs/00.agent-governance/scopes/infra.md](../../00.agent-governance/scopes/infra.md) | Markdown reference |
| [docs/00.agent-governance/scopes/meta.md](../../00.agent-governance/scopes/meta.md) | Markdown reference |
| [docs/00.agent-governance/scopes/mobile.md](../../00.agent-governance/scopes/mobile.md) | Markdown reference |
| [docs/00.agent-governance/scopes/ops.md](../../00.agent-governance/scopes/ops.md) | Markdown reference |
| [docs/00.agent-governance/scopes/product.md](../../00.agent-governance/scopes/product.md) | Markdown reference |
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
| [.claude/agents/hook-developer.md](../../../.claude/agents/hook-developer.md) | Markdown reference |
| [.claude/agents/iac-reviewer.md](../../../.claude/agents/iac-reviewer.md) | Markdown reference |
| [.claude/agents/incident-responder.md](../../../.claude/agents/incident-responder.md) | Markdown reference |
| [.claude/agents/infra-implementer.md](../../../.claude/agents/infra-implementer.md) | Markdown reference |
| [.claude/agents/qa-engineer.md](../../../.claude/agents/qa-engineer.md) | Markdown reference |
| [.claude/agents/rules-engineer.md](../../../.claude/agents/rules-engineer.md) | Markdown reference |
| [.claude/agents/security-auditor.md](../../../.claude/agents/security-auditor.md) | Markdown reference |
| [.claude/agents/skill-creator.md](../../../.claude/agents/skill-creator.md) | Markdown reference |
| [.claude/agents/style-enforcer.md](../../../.claude/agents/style-enforcer.md) | Markdown reference |
| [.claude/agents/wiki-curator.md](../../../.claude/agents/wiki-curator.md) | Markdown reference |
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
| [.claude/skills/adr-writing/skill.md](../../../.claude/skills/adr-writing/skill.md) | Markdown reference |
| [.claude/skills/ci-cd-patterns/skill.md](../../../.claude/skills/ci-cd-patterns/skill.md) | Markdown reference |
| [.claude/skills/code-review-dimensions/skill.md](../../../.claude/skills/code-review-dimensions/skill.md) | Markdown reference |
| [.claude/skills/code-reviewer/skill.md](../../../.claude/skills/code-reviewer/skill.md) | Markdown reference |
| [.claude/skills/compose-stack-agent/skill.md](../../../.claude/skills/compose-stack-agent/skill.md) | Markdown reference |
| [.claude/skills/container-threat-modeling/skill.md](../../../.claude/skills/container-threat-modeling/skill.md) | Markdown reference |
| [.claude/skills/deployment-pipeline-design/skill.md](../../../.claude/skills/deployment-pipeline-design/skill.md) | Markdown reference |
| [.claude/skills/docker-compose-patterns/skill.md](../../../.claude/skills/docker-compose-patterns/skill.md) | Markdown reference |
| [.claude/skills/e2e-testing/skill.md](../../../.claude/skills/e2e-testing/skill.md) | Markdown reference |
| [.claude/skills/execution-plan-agent/skill.md](../../../.claude/skills/execution-plan-agent/skill.md) | Markdown reference |
| [.claude/skills/incident-response/skill.md](../../../.claude/skills/incident-response/skill.md) | Markdown reference |
| [.claude/skills/infra-cross-validate/skill.md](../../../.claude/skills/infra-cross-validate/skill.md) | Markdown reference |
| [.claude/skills/infra-validate/skill.md](../../../.claude/skills/infra-validate/skill.md) | Markdown reference |
| [.claude/skills/knowledge-map-agent/skill.md](../../../.claude/skills/knowledge-map-agent/skill.md) | Markdown reference |
| [.claude/skills/ops-runbook-agent/skill.md](../../../.claude/skills/ops-runbook-agent/skill.md) | Markdown reference |
| [.claude/skills/policy-gate-agent/skill.md](../../../.claude/skills/policy-gate-agent/skill.md) | Markdown reference |
| [.claude/skills/requirements-to-design-agent/skill.md](../../../.claude/skills/requirements-to-design-agent/skill.md) | Markdown reference |
| [.claude/skills/security-audit/skill.md](../../../.claude/skills/security-audit/skill.md) | Markdown reference |
| [.claude/skills/style-validation/skill.md](../../../.claude/skills/style-validation/skill.md) | Markdown reference |
| [.claude/skills/task-breakdown-agent/skill.md](../../../.claude/skills/task-breakdown-agent/skill.md) | Markdown reference |
| [.claude/skills/test-automator/skill.md](../../../.claude/skills/test-automator/skill.md) | Markdown reference |
| [.claude/skills/workspace-audit-revalidation/skill.md](../../../.claude/skills/workspace-audit-revalidation/skill.md) | Markdown reference |
| [.codex/README.md](../../../.codex/README.md) | folder index |
| [.codex/agents/ci-cd-engineer.toml](../../../.codex/agents/ci-cd-engineer.toml) | source path |
| [.codex/agents/code-reviewer.toml](../../../.codex/agents/code-reviewer.toml) | source path |
| [.codex/agents/doc-writer.toml](../../../.codex/agents/doc-writer.toml) | source path |
| [.codex/agents/drift-detector.toml](../../../.codex/agents/drift-detector.toml) | source path |
| [.codex/agents/hook-developer.toml](../../../.codex/agents/hook-developer.toml) | source path |
| [.codex/agents/iac-reviewer.toml](../../../.codex/agents/iac-reviewer.toml) | source path |
| [.codex/agents/incident-responder.toml](../../../.codex/agents/incident-responder.toml) | source path |
| [.codex/agents/infra-implementer.toml](../../../.codex/agents/infra-implementer.toml) | source path |
| [.codex/agents/qa-engineer.toml](../../../.codex/agents/qa-engineer.toml) | source path |
| [.codex/agents/rules-engineer.toml](../../../.codex/agents/rules-engineer.toml) | source path |
| [.codex/agents/security-auditor.toml](../../../.codex/agents/security-auditor.toml) | source path |
| [.codex/agents/skill-creator.toml](../../../.codex/agents/skill-creator.toml) | source path |
| [.codex/agents/style-enforcer.toml](../../../.codex/agents/style-enforcer.toml) | source path |
| [.codex/agents/wiki-curator.toml](../../../.codex/agents/wiki-curator.toml) | source path |
| [.codex/agents/workflow-supervisor.toml](../../../.codex/agents/workflow-supervisor.toml) | source path |
| [.codex/hooks.json](../../../.codex/hooks.json) | JSON registry |
| [.codex/skills/adr-writing/skill.md](../../../.codex/skills/adr-writing/skill.md) | Markdown reference |
| [.codex/skills/ci-cd-patterns/skill.md](../../../.codex/skills/ci-cd-patterns/skill.md) | Markdown reference |
| [.codex/skills/code-review-dimensions/skill.md](../../../.codex/skills/code-review-dimensions/skill.md) | Markdown reference |
| [.codex/skills/code-reviewer/skill.md](../../../.codex/skills/code-reviewer/skill.md) | Markdown reference |
| [.codex/skills/compose-stack-agent/skill.md](../../../.codex/skills/compose-stack-agent/skill.md) | Markdown reference |
| [.codex/skills/container-threat-modeling/skill.md](../../../.codex/skills/container-threat-modeling/skill.md) | Markdown reference |
| [.codex/skills/deployment-pipeline-design/skill.md](../../../.codex/skills/deployment-pipeline-design/skill.md) | Markdown reference |
| [.codex/skills/docker-compose-patterns/skill.md](../../../.codex/skills/docker-compose-patterns/skill.md) | Markdown reference |
| [.codex/skills/e2e-testing/skill.md](../../../.codex/skills/e2e-testing/skill.md) | Markdown reference |
| [.codex/skills/execution-plan-agent/skill.md](../../../.codex/skills/execution-plan-agent/skill.md) | Markdown reference |
| [.codex/skills/incident-response/skill.md](../../../.codex/skills/incident-response/skill.md) | Markdown reference |
| [.codex/skills/infra-cross-validate/skill.md](../../../.codex/skills/infra-cross-validate/skill.md) | Markdown reference |
| [.codex/skills/infra-validate/skill.md](../../../.codex/skills/infra-validate/skill.md) | Markdown reference |
| [.codex/skills/knowledge-map-agent/skill.md](../../../.codex/skills/knowledge-map-agent/skill.md) | Markdown reference |
| [.codex/skills/ops-runbook-agent/skill.md](../../../.codex/skills/ops-runbook-agent/skill.md) | Markdown reference |
| [.codex/skills/policy-gate-agent/skill.md](../../../.codex/skills/policy-gate-agent/skill.md) | Markdown reference |
| [.codex/skills/requirements-to-design-agent/skill.md](../../../.codex/skills/requirements-to-design-agent/skill.md) | Markdown reference |
| [.codex/skills/security-audit/skill.md](../../../.codex/skills/security-audit/skill.md) | Markdown reference |
| [.codex/skills/style-validation/skill.md](../../../.codex/skills/style-validation/skill.md) | Markdown reference |
| [.codex/skills/task-breakdown-agent/skill.md](../../../.codex/skills/task-breakdown-agent/skill.md) | Markdown reference |
| [.codex/skills/test-automator/skill.md](../../../.codex/skills/test-automator/skill.md) | Markdown reference |
| [.codex/skills/workspace-audit-revalidation/skill.md](../../../.codex/skills/workspace-audit-revalidation/skill.md) | Markdown reference |

### Active stage docs

| Path | Role |
| --- | --- |
| [docs/01.requirements/001-gateway.md](../../01.requirements/001-gateway.md) | Markdown reference |
| [docs/01.requirements/002-auth.md](../../01.requirements/002-auth.md) | Markdown reference |
| [docs/01.requirements/003-security.md](../../01.requirements/003-security.md) | Markdown reference |
| [docs/01.requirements/004-data.md](../../01.requirements/004-data.md) | Markdown reference |
| [docs/01.requirements/005-data-analytics.md](../../01.requirements/005-data-analytics.md) | Markdown reference |
| [docs/01.requirements/006-messaging.md](../../01.requirements/006-messaging.md) | Markdown reference |
| [docs/01.requirements/007-observability.md](../../01.requirements/007-observability.md) | Markdown reference |
| [docs/01.requirements/008-workflow.md](../../01.requirements/008-workflow.md) | Markdown reference |
| [docs/01.requirements/009-ai.md](../../01.requirements/009-ai.md) | Markdown reference |
| [docs/01.requirements/010-tooling.md](../../01.requirements/010-tooling.md) | Markdown reference |
| [docs/01.requirements/011-communication.md](../../01.requirements/011-communication.md) | Markdown reference |
| [docs/01.requirements/012-laboratory.md](../../01.requirements/012-laboratory.md) | Markdown reference |
| [docs/01.requirements/013-ai-open-webui.md](../../01.requirements/013-ai-open-webui.md) | Markdown reference |
| [docs/01.requirements/014-auth-optimization-hardening.md](../../01.requirements/014-auth-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/015-security-optimization-hardening.md](../../01.requirements/015-security-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/016-data-optimization-hardening.md](../../01.requirements/016-data-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/017-messaging-optimization-hardening.md](../../01.requirements/017-messaging-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/018-observability-optimization-hardening.md](../../01.requirements/018-observability-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/019-workflow-optimization-hardening.md](../../01.requirements/019-workflow-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/020-ai-optimization-hardening.md](../../01.requirements/020-ai-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/021-tooling-optimization-hardening.md](../../01.requirements/021-tooling-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/022-laboratory-optimization-hardening.md](../../01.requirements/022-laboratory-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/023-standardize-infra-net.md](../../01.requirements/023-standardize-infra-net.md) | Markdown reference |
| [docs/01.requirements/024-agent-governance-standardization.md](../../01.requirements/024-agent-governance-standardization.md) | Markdown reference |
| [docs/01.requirements/README.md](../../01.requirements/README.md) | folder index |
| [docs/02.architecture/README.md](../../02.architecture/README.md) | folder index |
| [docs/02.architecture/decisions/0001-traefik-nginx-hybrid.md](../../02.architecture/decisions/0001-traefik-nginx-hybrid.md) | Markdown reference |
| [docs/02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md](../../02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md) | Markdown reference |
| [docs/02.architecture/decisions/0003-vault-as-secrets-manager.md](../../02.architecture/decisions/0003-vault-as-secrets-manager.md) | Markdown reference |
| [docs/02.architecture/decisions/0004-postgresql-ha-patroni.md](../../02.architecture/decisions/0004-postgresql-ha-patroni.md) | Markdown reference |
| [docs/02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md](../../02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md) | Markdown reference |
| [docs/02.architecture/decisions/0006-lgtm-stack-selection.md](../../02.architecture/decisions/0006-lgtm-stack-selection.md) | Markdown reference |
| [docs/02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md](../../02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md) | Markdown reference |
| [docs/02.architecture/decisions/0008-ollama-openwebui-local-ai.md](../../02.architecture/decisions/0008-ollama-openwebui-local-ai.md) | Markdown reference |
| [docs/02.architecture/decisions/0009-tooling-services.md](../../02.architecture/decisions/0009-tooling-services.md) | Markdown reference |
| [docs/02.architecture/decisions/0010-communication-services.md](../../02.architecture/decisions/0010-communication-services.md) | Markdown reference |
| [docs/02.architecture/decisions/0011-laboratory-services.md](../../02.architecture/decisions/0011-laboratory-services.md) | Markdown reference |
| [docs/02.architecture/decisions/0015-analytics-engine-selection.md](../../02.architecture/decisions/0015-analytics-engine-selection.md) | Markdown reference |
| [docs/02.architecture/decisions/0016-open-webui-implementation.md](../../02.architecture/decisions/0016-open-webui-implementation.md) | Markdown reference |
| [docs/02.architecture/decisions/0017-auth-hardening-runtime-and-fail-closed.md](../../02.architecture/decisions/0017-auth-hardening-runtime-and-fail-closed.md) | Markdown reference |
| [docs/02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0019-04-data-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0019-04-data-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md) | Markdown reference |
| [docs/02.architecture/decisions/0026-standardize-infra-net.md](../../02.architecture/decisions/0026-standardize-infra-net.md) | Markdown reference |
| [docs/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md](../../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md) | Markdown reference |
| [docs/02.architecture/decisions/README.md](../../02.architecture/decisions/README.md) | folder index |
| [docs/02.architecture/requirements/0001-gateway-architecture.md](../../02.architecture/requirements/0001-gateway-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0002-auth-architecture.md](../../02.architecture/requirements/0002-auth-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0003-security-architecture.md](../../02.architecture/requirements/0003-security-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0004-data-architecture.md](../../02.architecture/requirements/0004-data-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0005-messaging-architecture.md](../../02.architecture/requirements/0005-messaging-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0006-observability-architecture.md](../../02.architecture/requirements/0006-observability-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0007-workflow-architecture.md](../../02.architecture/requirements/0007-workflow-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0008-ai-architecture.md](../../02.architecture/requirements/0008-ai-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0009-tooling-architecture.md](../../02.architecture/requirements/0009-tooling-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0010-communication-architecture.md](../../02.architecture/requirements/0010-communication-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0011-laboratory-architecture.md](../../02.architecture/requirements/0011-laboratory-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0012-data-analytics-architecture.md](../../02.architecture/requirements/0012-data-analytics-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0013-open-webui-architecture.md](../../02.architecture/requirements/0013-open-webui-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0014-auth-optimization-hardening-architecture.md](../../02.architecture/requirements/0014-auth-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0018-security-optimization-hardening-architecture.md](../../02.architecture/requirements/0018-security-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0019-data-optimization-hardening-architecture.md](../../02.architecture/requirements/0019-data-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md](../../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0021-observability-optimization-hardening-architecture.md](../../02.architecture/requirements/0021-observability-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md](../../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0023-ai-optimization-hardening-architecture.md](../../02.architecture/requirements/0023-ai-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0024-tooling-optimization-hardening-architecture.md](../../02.architecture/requirements/0024-tooling-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md](../../02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md) | Markdown reference |
| [docs/02.architecture/requirements/0026-standardize-infra-net.md](../../02.architecture/requirements/0026-standardize-infra-net.md) | Markdown reference |
| [docs/02.architecture/requirements/0027-agent-governance-canonical-adapter.md](../../02.architecture/requirements/0027-agent-governance-canonical-adapter.md) | Markdown reference |
| [docs/02.architecture/requirements/README.md](../../02.architecture/requirements/README.md) | folder index |
| [docs/03.specs/001-gateway/README.md](../../03.specs/001-gateway/README.md) | folder index |
| [docs/03.specs/001-gateway/spec.md](../../03.specs/001-gateway/spec.md) | Markdown reference |
| [docs/03.specs/002-auth/README.md](../../03.specs/002-auth/README.md) | folder index |
| [docs/03.specs/002-auth/spec.md](../../03.specs/002-auth/spec.md) | Markdown reference |
| [docs/03.specs/003-security/README.md](../../03.specs/003-security/README.md) | folder index |
| [docs/03.specs/003-security/spec.md](../../03.specs/003-security/spec.md) | Markdown reference |
| [docs/03.specs/004-data/README.md](../../03.specs/004-data/README.md) | folder index |
| [docs/03.specs/004-data/spec.md](../../03.specs/004-data/spec.md) | Markdown reference |
| [docs/03.specs/005-data-analytics/README.md](../../03.specs/005-data-analytics/README.md) | folder index |
| [docs/03.specs/005-data-analytics/spec.md](../../03.specs/005-data-analytics/spec.md) | Markdown reference |
| [docs/03.specs/006-messaging/README.md](../../03.specs/006-messaging/README.md) | folder index |
| [docs/03.specs/006-messaging/spec.md](../../03.specs/006-messaging/spec.md) | Markdown reference |
| [docs/03.specs/007-observability/README.md](../../03.specs/007-observability/README.md) | folder index |
| [docs/03.specs/007-observability/spec.md](../../03.specs/007-observability/spec.md) | Markdown reference |
| [docs/03.specs/008-workflow/README.md](../../03.specs/008-workflow/README.md) | folder index |
| [docs/03.specs/008-workflow/agent-design.md](../../03.specs/008-workflow/agent-design.md) | Markdown reference |
| [docs/03.specs/008-workflow/spec.md](../../03.specs/008-workflow/spec.md) | Markdown reference |
| [docs/03.specs/009-ai/README.md](../../03.specs/009-ai/README.md) | folder index |
| [docs/03.specs/009-ai/open-webui.md](../../03.specs/009-ai/open-webui.md) | Markdown reference |
| [docs/03.specs/009-ai/spec.md](../../03.specs/009-ai/spec.md) | Markdown reference |
| [docs/03.specs/010-tooling/README.md](../../03.specs/010-tooling/README.md) | folder index |
| [docs/03.specs/010-tooling/spec.md](../../03.specs/010-tooling/spec.md) | Markdown reference |
| [docs/03.specs/011-communication/README.md](../../03.specs/011-communication/README.md) | folder index |
| [docs/03.specs/011-communication/spec.md](../../03.specs/011-communication/spec.md) | Markdown reference |
| [docs/03.specs/012-laboratory/README.md](../../03.specs/012-laboratory/README.md) | folder index |
| [docs/03.specs/012-laboratory/spec.md](../../03.specs/012-laboratory/spec.md) | Markdown reference |
| [docs/03.specs/090-workspace-audit-2026-05/README.md](../../03.specs/090-workspace-audit-2026-05/README.md) | folder index |
| [docs/03.specs/090-workspace-audit-2026-05/spec.md](../../03.specs/090-workspace-audit-2026-05/spec.md) | Markdown reference |
| [docs/03.specs/091-workspace-doc-consistency-2026-05/spec.md](../../03.specs/091-workspace-doc-consistency-2026-05/spec.md) | Markdown reference |
| [docs/03.specs/092-workspace-consistency-2026-05b/spec.md](../../03.specs/092-workspace-consistency-2026-05b/spec.md) | Markdown reference |
| [docs/03.specs/093-docs-taxonomy-agent-first-migration/README.md](../../03.specs/093-docs-taxonomy-agent-first-migration/README.md) | folder index |
| [docs/03.specs/093-docs-taxonomy-agent-first-migration/spec.md](../../03.specs/093-docs-taxonomy-agent-first-migration/spec.md) | Markdown reference |
| [docs/03.specs/094-harness-agent-first-engineering/README.md](../../03.specs/094-harness-agent-first-engineering/README.md) | folder index |
| [docs/03.specs/094-harness-agent-first-engineering/spec.md](../../03.specs/094-harness-agent-first-engineering/spec.md) | Markdown reference |
| [docs/03.specs/095-infra-secrets-docs-refresh/README.md](../../03.specs/095-infra-secrets-docs-refresh/README.md) | folder index |
| [docs/03.specs/095-infra-secrets-docs-refresh/spec.md](../../03.specs/095-infra-secrets-docs-refresh/spec.md) | Markdown reference |
| [docs/03.specs/096-llm-wiki-agent-first-completion/README.md](../../03.specs/096-llm-wiki-agent-first-completion/README.md) | folder index |
| [docs/03.specs/096-llm-wiki-agent-first-completion/spec.md](../../03.specs/096-llm-wiki-agent-first-completion/spec.md) | Markdown reference |
| [docs/03.specs/097-home-docker-revalidation-deferred-follow-up/README.md](../../03.specs/097-home-docker-revalidation-deferred-follow-up/README.md) | folder index |
| [docs/03.specs/097-home-docker-revalidation-deferred-follow-up/spec.md](../../03.specs/097-home-docker-revalidation-deferred-follow-up/spec.md) | Markdown reference |
| [docs/03.specs/098-standardize-infra-net/README.md](../../03.specs/098-standardize-infra-net/README.md) | folder index |
| [docs/03.specs/098-standardize-infra-net/spec.md](../../03.specs/098-standardize-infra-net/spec.md) | Markdown reference |
| [docs/03.specs/099-template-system-numbered-sdlc-paths/README.md](../../03.specs/099-template-system-numbered-sdlc-paths/README.md) | folder index |
| [docs/03.specs/099-template-system-numbered-sdlc-paths/spec.md](../../03.specs/099-template-system-numbered-sdlc-paths/spec.md) | Markdown reference |
| [docs/03.specs/100-template-system-contract-standardization/spec.md](../../03.specs/100-template-system-contract-standardization/spec.md) | Markdown reference |
| [docs/03.specs/101-template-system-reorganization/README.md](../../03.specs/101-template-system-reorganization/README.md) | folder index |
| [docs/03.specs/101-template-system-reorganization/spec.md](../../03.specs/101-template-system-reorganization/spec.md) | Markdown reference |
| [docs/03.specs/102-workspace-document-contract-audit-pack/README.md](../../03.specs/102-workspace-document-contract-audit-pack/README.md) | folder index |
| [docs/03.specs/102-workspace-document-contract-audit-pack/spec.md](../../03.specs/102-workspace-document-contract-audit-pack/spec.md) | Markdown reference |
| [docs/03.specs/103-document-restructure-audit-contract-archive/README.md](../../03.specs/103-document-restructure-audit-contract-archive/README.md) | folder index |
| [docs/03.specs/103-document-restructure-audit-contract-archive/spec.md](../../03.specs/103-document-restructure-audit-contract-archive/spec.md) | Markdown reference |
| [docs/03.specs/104-agentic-research-pack-refresh/README.md](../../03.specs/104-agentic-research-pack-refresh/README.md) | folder index |
| [docs/03.specs/104-agentic-research-pack-refresh/spec.md](../../03.specs/104-agentic-research-pack-refresh/spec.md) | Markdown reference |
| [docs/03.specs/105-agentic-engineering-implementation-audit-pack/README.md](../../03.specs/105-agentic-engineering-implementation-audit-pack/README.md) | folder index |
| [docs/03.specs/105-agentic-engineering-implementation-audit-pack/spec.md](../../03.specs/105-agentic-engineering-implementation-audit-pack/spec.md) | Markdown reference |
| [docs/03.specs/106-workspace-support-surface-contract/README.md](../../03.specs/106-workspace-support-surface-contract/README.md) | folder index |
| [docs/03.specs/106-workspace-support-surface-contract/spec.md](../../03.specs/106-workspace-support-surface-contract/spec.md) | Markdown reference |
| [docs/03.specs/107-provider-semantic-parity-validator/README.md](../../03.specs/107-provider-semantic-parity-validator/README.md) | folder index |
| [docs/03.specs/107-provider-semantic-parity-validator/spec.md](../../03.specs/107-provider-semantic-parity-validator/spec.md) | Markdown reference |
| [docs/03.specs/108-compose-profile-service-coverage-snapshot/README.md](../../03.specs/108-compose-profile-service-coverage-snapshot/README.md) | folder index |
| [docs/03.specs/108-compose-profile-service-coverage-snapshot/spec.md](../../03.specs/108-compose-profile-service-coverage-snapshot/spec.md) | Markdown reference |
| [docs/03.specs/109-gap-routing-recommendation/README.md](../../03.specs/109-gap-routing-recommendation/README.md) | folder index |
| [docs/03.specs/109-gap-routing-recommendation/spec.md](../../03.specs/109-gap-routing-recommendation/spec.md) | Markdown reference |
| [docs/03.specs/110-agent-output-eval-fixtures/spec.md](../../03.specs/110-agent-output-eval-fixtures/spec.md) | Markdown reference |
| [docs/03.specs/111-qa-gate-recommendation-ci-summary/spec.md](../../03.specs/111-qa-gate-recommendation-ci-summary/spec.md) | Markdown reference |
| [docs/03.specs/112-audit-pack-coverage-report/spec.md](../../03.specs/112-audit-pack-coverage-report/spec.md) | Markdown reference |
| [docs/03.specs/113-llm-wiki-stage-category-coverage/spec.md](../../03.specs/113-llm-wiki-stage-category-coverage/spec.md) | Markdown reference |
| [docs/03.specs/114-tech-stack-version-provenance/spec.md](../../03.specs/114-tech-stack-version-provenance/spec.md) | Markdown reference |
| [docs/03.specs/115-provider-hook-parity-matrix/spec.md](../../03.specs/115-provider-hook-parity-matrix/spec.md) | Markdown reference |
| [docs/03.specs/116-agent-output-eval-runner/spec.md](../../03.specs/116-agent-output-eval-runner/spec.md) | Markdown reference |
| [docs/03.specs/117-security-automation-readiness-snapshot/spec.md](../../03.specs/117-security-automation-readiness-snapshot/spec.md) | Markdown reference |
| [docs/03.specs/118-audit-implementation-matrix-snapshot/spec.md](../../03.specs/118-audit-implementation-matrix-snapshot/spec.md) | Markdown reference |
| [docs/03.specs/119-sdlc-document-contract-corpus-normalization/README.md](../../03.specs/119-sdlc-document-contract-corpus-normalization/README.md) | folder index |
| [docs/03.specs/119-sdlc-document-contract-corpus-normalization/spec.md](../../03.specs/119-sdlc-document-contract-corpus-normalization/spec.md) | Markdown reference |
| [docs/03.specs/120-agent-output-eval-ci-gate/README.md](../../03.specs/120-agent-output-eval-ci-gate/README.md) | folder index |
| [docs/03.specs/120-agent-output-eval-ci-gate/spec.md](../../03.specs/120-agent-output-eval-ci-gate/spec.md) | Markdown reference |
| [docs/03.specs/121-dependency-vulnerability-audit-gate/README.md](../../03.specs/121-dependency-vulnerability-audit-gate/README.md) | folder index |
| [docs/03.specs/121-dependency-vulnerability-audit-gate/spec.md](../../03.specs/121-dependency-vulnerability-audit-gate/spec.md) | Markdown reference |
| [docs/03.specs/122-agentic-research-pack-consolidation/README.md](../../03.specs/122-agentic-research-pack-consolidation/README.md) | folder index |
| [docs/03.specs/122-agentic-research-pack-consolidation/spec.md](../../03.specs/122-agentic-research-pack-consolidation/spec.md) | Markdown reference |
| [docs/03.specs/123-agentic-engineering-audit-remediation/README.md](../../03.specs/123-agentic-engineering-audit-remediation/README.md) | folder index |
| [docs/03.specs/123-agentic-engineering-audit-remediation/spec.md](../../03.specs/123-agentic-engineering-audit-remediation/spec.md) | Markdown reference |
| [docs/03.specs/124-compose-runtime-readiness-remediation/README.md](../../03.specs/124-compose-runtime-readiness-remediation/README.md) | folder index |
| [docs/03.specs/124-compose-runtime-readiness-remediation/spec.md](../../03.specs/124-compose-runtime-readiness-remediation/spec.md) | Markdown reference |
| [docs/03.specs/125-infrastructure-operations-readiness-remediation/README.md](../../03.specs/125-infrastructure-operations-readiness-remediation/README.md) | folder index |
| [docs/03.specs/125-infrastructure-operations-readiness-remediation/spec.md](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md) | Markdown reference |
| [docs/03.specs/126-security-supply-chain-remediation/README.md](../../03.specs/126-security-supply-chain-remediation/README.md) | folder index |
| [docs/03.specs/126-security-supply-chain-remediation/spec.md](../../03.specs/126-security-supply-chain-remediation/spec.md) | Markdown reference |
| [docs/03.specs/127-deployment-release-engineering-remediation/README.md](../../03.specs/127-deployment-release-engineering-remediation/README.md) | folder index |
| [docs/03.specs/127-deployment-release-engineering-remediation/spec.md](../../03.specs/127-deployment-release-engineering-remediation/spec.md) | Markdown reference |
| [docs/03.specs/128-agentic-audit-harness-consolidation/spec.md](../../03.specs/128-agentic-audit-harness-consolidation/spec.md) | Markdown reference |
| [docs/03.specs/129-document-contract-canonicalization/spec.md](../../03.specs/129-document-contract-canonicalization/spec.md) | Markdown reference |
| [docs/03.specs/130-template-contract-system-canonicalization/spec.md](../../03.specs/130-template-contract-system-canonicalization/spec.md) | Markdown reference |
| [docs/03.specs/README.md](../../03.specs/README.md) | folder index |
| [docs/04.execution/README.md](../../04.execution/README.md) | folder index |
| [docs/04.execution/plans/2026-03-26-01-gateway-standardization.md](../../04.execution/plans/2026-03-26-01-gateway-standardization.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-26-02-auth-standardization.md](../../04.execution/plans/2026-03-26-02-auth-standardization.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-26-03-security-standardization.md](../../04.execution/plans/2026-03-26-03-security-standardization.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-26-04-data-standardization.md](../../04.execution/plans/2026-03-26-04-data-standardization.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-26-05-messaging-standardization.md](../../04.execution/plans/2026-03-26-05-messaging-standardization.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-26-06-observability-standardization.md](../../04.execution/plans/2026-03-26-06-observability-standardization.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-26-07-workflow-standardization.md](../../04.execution/plans/2026-03-26-07-workflow-standardization.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-26-08-ai-standardization.md](../../04.execution/plans/2026-03-26-08-ai-standardization.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-26-09-tooling-standardization.md](../../04.execution/plans/2026-03-26-09-tooling-standardization.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-26-10-communication-standardization.md](../../04.execution/plans/2026-03-26-10-communication-standardization.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-26-11-laboratory-standardization.md](../../04.execution/plans/2026-03-26-11-laboratory-standardization.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-27-08-ai-open-webui-plan.md](../../04.execution/plans/2026-03-27-08-ai-open-webui-plan.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-27-infra-service-optimization-priority-plan.md](../../04.execution/plans/2026-03-27-infra-service-optimization-priority-plan.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-28-01-gateway-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-01-gateway-optimization-hardening-plan.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-28-04-data-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-04-data-optimization-hardening-plan.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-28-06-observability-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-06-observability-optimization-hardening-plan.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-28-07-workflow-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-07-workflow-optimization-hardening-plan.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-28-08-ai-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-08-ai-optimization-hardening-plan.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-28-09-tooling-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-09-tooling-optimization-hardening-plan.md) | Markdown reference |
| [docs/04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md) | Markdown reference |
| [docs/04.execution/plans/2026-04-01-standardize-infra-net.md](../../04.execution/plans/2026-04-01-standardize-infra-net.md) | Markdown reference |
| [docs/04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md](../../04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-09-harness-agent-first-engineering.md](../../04.execution/plans/2026-05-09-harness-agent-first-engineering.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-09-infra-secrets-docs-refresh.md](../../04.execution/plans/2026-05-09-infra-secrets-docs-refresh.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md](../../04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-10-docs-taxonomy-agent-first-migration.md](../../04.execution/plans/2026-05-10-docs-taxonomy-agent-first-migration.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md](../../04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-17-requirements-standardization.md](../../04.execution/plans/2026-05-17-requirements-standardization.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-17-scripts-ci-qa-cleanup.md](../../04.execution/plans/2026-05-17-scripts-ci-qa-cleanup.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-18-docs-05-operations-purpose-remediation.md](../../04.execution/plans/2026-05-18-docs-05-operations-purpose-remediation.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-18-docs-bounded-consistency-audit.md](../../04.execution/plans/2026-05-18-docs-bounded-consistency-audit.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-18-execution-stage-remediation.md](../../04.execution/plans/2026-05-18-execution-stage-remediation.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-18-targeted-docs-precision-remediation.md](../../04.execution/plans/2026-05-18-targeted-docs-precision-remediation.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-22-agent-hook-completion-style-automation.md](../../04.execution/plans/2026-05-22-agent-hook-completion-style-automation.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-22-data-analytics-execution-traceability.md](../../04.execution/plans/2026-05-22-data-analytics-execution-traceability.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-22-lifecycle-readme-debt-closure.md](../../04.execution/plans/2026-05-22-lifecycle-readme-debt-closure.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-22-spec-execution-implementation-audit.md](../../04.execution/plans/2026-05-22-spec-execution-implementation-audit.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-22-workspace-docs-agent-governance-remediation.md](../../04.execution/plans/2026-05-22-workspace-docs-agent-governance-remediation.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-22-workspace-governance-bounded-reaudit.md](../../04.execution/plans/2026-05-22-workspace-governance-bounded-reaudit.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-24-workspace-audit-grill-review.md](../../04.execution/plans/2026-05-24-workspace-audit-grill-review.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-24-workspace-audit-improvement.md](../../04.execution/plans/2026-05-24-workspace-audit-improvement.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-24-workspace-audit-input-task-gap-closure.md](../../04.execution/plans/2026-05-24-workspace-audit-input-task-gap-closure.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-25-home-docker-revalidation-deferred-follow-up.md](../../04.execution/plans/2026-05-25-home-docker-revalidation-deferred-follow-up.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-25-home-docker-workspace-audit-improvement.md](../../04.execution/plans/2026-05-25-home-docker-workspace-audit-improvement.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-25-large-scale-authored-ssot-review.md](../../04.execution/plans/2026-05-25-large-scale-authored-ssot-review.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-26-workspace-audit-gap-closure.md](../../04.execution/plans/2026-05-26-workspace-audit-gap-closure.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-26-workspace-audit.md](../../04.execution/plans/2026-05-26-workspace-audit.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-28-workspace-doc-consistency.md](../../04.execution/plans/2026-05-28-workspace-doc-consistency.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-29-workspace-consistency-2026-05b.md](../../04.execution/plans/2026-05-29-workspace-consistency-2026-05b.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-31-claude-harness-governance-verification.md](../../04.execution/plans/2026-05-31-claude-harness-governance-verification.md) | Markdown reference |
| [docs/04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md](../../04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md) | Markdown reference |
| [docs/04.execution/plans/2026-06-02-agent-governance-phase-1-revalidation.md](../../04.execution/plans/2026-06-02-agent-governance-phase-1-revalidation.md) | Markdown reference |
| [docs/04.execution/plans/2026-06-02-agent-governance-phase-2-strategy-integration.md](../../04.execution/plans/2026-06-02-agent-governance-phase-2-strategy-integration.md) | Markdown reference |
| [docs/04.execution/plans/2026-06-02-agent-governance-phase-3-approved-surface-activation.md](../../04.execution/plans/2026-06-02-agent-governance-phase-3-approved-surface-activation.md) | Markdown reference |
| [docs/04.execution/plans/2026-06-02-agent-governance-phase-4-closure-reconciliation.md](../../04.execution/plans/2026-06-02-agent-governance-phase-4-closure-reconciliation.md) | Markdown reference |
| [docs/04.execution/plans/2026-06-02-docs-implementation-reconciliation.md](../../04.execution/plans/2026-06-02-docs-implementation-reconciliation.md) | Markdown reference |
| [docs/04.execution/plans/2026-06-02-governance-optimization.md](../../04.execution/plans/2026-06-02-governance-optimization.md) | Markdown reference |
| [docs/04.execution/plans/2026-06-03-governance-surgical-reverification.md](../../04.execution/plans/2026-06-03-governance-surgical-reverification.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-02-template-system-reorganization.md](../../04.execution/plans/2026-07-02-template-system-reorganization.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-03-document-contract-remediation-batches.md](../../04.execution/plans/2026-07-03-document-contract-remediation-batches.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-03-template-system-contract-standardization.md](../../04.execution/plans/2026-07-03-template-system-contract-standardization.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md](../../04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-04-document-restructure-audit-contract-archive.md](../../04.execution/plans/2026-07-04-document-restructure-audit-contract-archive.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-05-agent-output-eval-fixtures.md](../../04.execution/plans/2026-07-05-agent-output-eval-fixtures.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-05-agentic-engineering-implementation-audit-pack.md](../../04.execution/plans/2026-07-05-agentic-engineering-implementation-audit-pack.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-05-agentic-research-pack-refresh.md](../../04.execution/plans/2026-07-05-agentic-research-pack-refresh.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-05-audit-pack-coverage-report.md](../../04.execution/plans/2026-07-05-audit-pack-coverage-report.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-05-compose-profile-service-coverage-snapshot.md](../../04.execution/plans/2026-07-05-compose-profile-service-coverage-snapshot.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-05-gap-routing-recommendation.md](../../04.execution/plans/2026-07-05-gap-routing-recommendation.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-05-provider-semantic-parity-validator.md](../../04.execution/plans/2026-07-05-provider-semantic-parity-validator.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-05-provider-workspace-artifact-path-parity.md](../../04.execution/plans/2026-07-05-provider-workspace-artifact-path-parity.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-05-qa-gate-recommendation-ci-summary.md](../../04.execution/plans/2026-07-05-qa-gate-recommendation-ci-summary.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-05-template-system-numbered-sdlc-paths.md](../../04.execution/plans/2026-07-05-template-system-numbered-sdlc-paths.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-05-workspace-support-surface-contract.md](../../04.execution/plans/2026-07-05-workspace-support-surface-contract.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-06-agent-output-eval-ci-gate.md](../../04.execution/plans/2026-07-06-agent-output-eval-ci-gate.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-06-agent-output-eval-runner.md](../../04.execution/plans/2026-07-06-agent-output-eval-runner.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-06-audit-implementation-matrix-snapshot.md](../../04.execution/plans/2026-07-06-audit-implementation-matrix-snapshot.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-06-dependency-vulnerability-audit-gate.md](../../04.execution/plans/2026-07-06-dependency-vulnerability-audit-gate.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-06-llm-wiki-stage-category-coverage.md](../../04.execution/plans/2026-07-06-llm-wiki-stage-category-coverage.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-06-provider-hook-parity-matrix.md](../../04.execution/plans/2026-07-06-provider-hook-parity-matrix.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-06-sdlc-document-contract-corpus-normalization.md](../../04.execution/plans/2026-07-06-sdlc-document-contract-corpus-normalization.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-06-security-automation-readiness-snapshot.md](../../04.execution/plans/2026-07-06-security-automation-readiness-snapshot.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-06-tech-stack-version-provenance.md](../../04.execution/plans/2026-07-06-tech-stack-version-provenance.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-10-agentic-research-pack-consolidation.md](../../04.execution/plans/2026-07-10-agentic-research-pack-consolidation.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-11-agentic-engineering-audit-remediation.md](../../04.execution/plans/2026-07-11-agentic-engineering-audit-remediation.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-11-compose-runtime-readiness-remediation.md](../../04.execution/plans/2026-07-11-compose-runtime-readiness-remediation.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-11-deployment-release-engineering-remediation.md](../../04.execution/plans/2026-07-11-deployment-release-engineering-remediation.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-11-infrastructure-operations-readiness-remediation.md](../../04.execution/plans/2026-07-11-infrastructure-operations-readiness-remediation.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-11-security-supply-chain-remediation.md](../../04.execution/plans/2026-07-11-security-supply-chain-remediation.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-12-agentic-audit-harness-consolidation.md](../../04.execution/plans/2026-07-12-agentic-audit-harness-consolidation.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-13-document-contract-canonicalization.md](../../04.execution/plans/2026-07-13-document-contract-canonicalization.md) | Markdown reference |
| [docs/04.execution/plans/2026-07-13-template-contract-system-canonicalization.md](../../04.execution/plans/2026-07-13-template-contract-system-canonicalization.md) | Markdown reference |
| [docs/04.execution/plans/README.md](../../04.execution/plans/README.md) | folder index |
| [docs/04.execution/tasks/2026-03-26-01-gateway-tasks.md](../../04.execution/tasks/2026-03-26-01-gateway-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-26-02-auth-tasks.md](../../04.execution/tasks/2026-03-26-02-auth-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-26-03-security-tasks.md](../../04.execution/tasks/2026-03-26-03-security-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-26-04-data-tasks.md](../../04.execution/tasks/2026-03-26-04-data-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-26-05-messaging-tasks.md](../../04.execution/tasks/2026-03-26-05-messaging-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-26-06-observability-tasks.md](../../04.execution/tasks/2026-03-26-06-observability-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-26-07-workflow-tasks.md](../../04.execution/tasks/2026-03-26-07-workflow-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-26-08-ai-tasks.md](../../04.execution/tasks/2026-03-26-08-ai-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-26-09-tooling-tasks.md](../../04.execution/tasks/2026-03-26-09-tooling-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-26-10-communication-tasks.md](../../04.execution/tasks/2026-03-26-10-communication-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-26-11-laboratory-tasks.md](../../04.execution/tasks/2026-03-26-11-laboratory-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-27-08-ai-open-webui-tasks.md](../../04.execution/tasks/2026-03-27-08-ai-open-webui-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-28-02-auth-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-02-auth-optimization-hardening-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-28-04-data-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-04-data-optimization-hardening-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-06-observability-optimization-hardening-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-28-08-ai-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-08-ai-optimization-hardening-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md) | Markdown reference |
| [docs/04.execution/tasks/2026-04-01-standardize-infra-net.md](../../04.execution/tasks/2026-04-01-standardize-infra-net.md) | Markdown reference |
| [docs/04.execution/tasks/2026-04-10-infra-team-agent-cross-validation.md](../../04.execution/tasks/2026-04-10-infra-team-agent-cross-validation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-09-harness-agent-first-engineering.md](../../04.execution/tasks/2026-05-09-harness-agent-first-engineering.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md](../../04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-09-scripts-lifecycle-contract-cleanup.md](../../04.execution/tasks/2026-05-09-scripts-lifecycle-contract-cleanup.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-10-docs-taxonomy-agent-first-migration.md](../../04.execution/tasks/2026-05-10-docs-taxonomy-agent-first-migration.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md](../../04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-17-requirements-standardization.md](../../04.execution/tasks/2026-05-17-requirements-standardization.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-17-scripts-ci-qa-cleanup.md](../../04.execution/tasks/2026-05-17-scripts-ci-qa-cleanup.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-18-docs-05-operations-purpose-remediation.md](../../04.execution/tasks/2026-05-18-docs-05-operations-purpose-remediation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-18-docs-bounded-consistency-audit.md](../../04.execution/tasks/2026-05-18-docs-bounded-consistency-audit.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-18-execution-stage-remediation.md](../../04.execution/tasks/2026-05-18-execution-stage-remediation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-18-targeted-docs-precision-remediation.md](../../04.execution/tasks/2026-05-18-targeted-docs-precision-remediation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-22-agent-hook-completion-style-automation.md](../../04.execution/tasks/2026-05-22-agent-hook-completion-style-automation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-22-data-analytics-execution-traceability.md](../../04.execution/tasks/2026-05-22-data-analytics-execution-traceability.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-22-lifecycle-readme-debt-closure.md](../../04.execution/tasks/2026-05-22-lifecycle-readme-debt-closure.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-22-spec-execution-implementation-audit.md](../../04.execution/tasks/2026-05-22-spec-execution-implementation-audit.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-22-workspace-docs-agent-governance-remediation.md](../../04.execution/tasks/2026-05-22-workspace-docs-agent-governance-remediation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-22-workspace-governance-bounded-reaudit.md](../../04.execution/tasks/2026-05-22-workspace-governance-bounded-reaudit.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-24-workspace-audit-grill-review.md](../../04.execution/tasks/2026-05-24-workspace-audit-grill-review.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-24-workspace-audit-improvement.md](../../04.execution/tasks/2026-05-24-workspace-audit-improvement.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-24-workspace-audit-input-task-gap-closure.md](../../04.execution/tasks/2026-05-24-workspace-audit-input-task-gap-closure.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-25-home-docker-revalidation-deferred-follow-up.md](../../04.execution/tasks/2026-05-25-home-docker-revalidation-deferred-follow-up.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-25-home-docker-workspace-audit-improvement.md](../../04.execution/tasks/2026-05-25-home-docker-workspace-audit-improvement.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-25-large-scale-authored-ssot-review.md](../../04.execution/tasks/2026-05-25-large-scale-authored-ssot-review.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-26-workspace-audit-gap-closure.md](../../04.execution/tasks/2026-05-26-workspace-audit-gap-closure.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-26-workspace-audit.md](../../04.execution/tasks/2026-05-26-workspace-audit.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-28-workspace-doc-consistency.md](../../04.execution/tasks/2026-05-28-workspace-doc-consistency.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-29-workspace-consistency-2026-05b.md](../../04.execution/tasks/2026-05-29-workspace-consistency-2026-05b.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-31-claude-harness-governance-verification.md](../../04.execution/tasks/2026-05-31-claude-harness-governance-verification.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md](../../04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-02-agent-governance-phase-1-revalidation.md](../../04.execution/tasks/2026-06-02-agent-governance-phase-1-revalidation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-02-agent-governance-phase-2-strategy-integration.md](../../04.execution/tasks/2026-06-02-agent-governance-phase-2-strategy-integration.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-02-agent-governance-phase-3-approved-surface-activation.md](../../04.execution/tasks/2026-06-02-agent-governance-phase-3-approved-surface-activation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-02-agent-governance-phase-4-closure-reconciliation.md](../../04.execution/tasks/2026-06-02-agent-governance-phase-4-closure-reconciliation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-02-docs-implementation-reconciliation.md](../../04.execution/tasks/2026-06-02-docs-implementation-reconciliation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-02-governance-optimization.md](../../04.execution/tasks/2026-06-02-governance-optimization.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-03-governance-surgical-reverification.md](../../04.execution/tasks/2026-06-03-governance-surgical-reverification.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-04-docs-implementation-audit.md](../../04.execution/tasks/2026-06-04-docs-implementation-audit.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-harness-engineering.md](../../04.execution/tasks/2026-06-05-harness-engineering.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-boundary-audit.md](../../04.execution/tasks/2026-06-05-language-policy-boundary-audit.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-hard-enforcement.md](../../04.execution/tasks/2026-06-05-language-policy-hard-enforcement.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-normalization-batch-1.md](../../04.execution/tasks/2026-06-05-language-policy-normalization-batch-1.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-normalization-batch-2.md](../../04.execution/tasks/2026-06-05-language-policy-normalization-batch-2.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-normalization-batch-3.md](../../04.execution/tasks/2026-06-05-language-policy-normalization-batch-3.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-1.md](../../04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-1.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-2.md](../../04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-2.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-3.md](../../04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-3.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-4.md](../../04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-4.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-5.md](../../04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-5.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-6.md](../../04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-6.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-7.md](../../04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-7.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-8.md](../../04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-8.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-reference-normalization.md](../../04.execution/tasks/2026-06-05-language-policy-reference-normalization.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-1.md](../../04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-1.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-2.md](../../04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-2.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-3.md](../../04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-3.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-4.md](../../04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-4.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-5.md](../../04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-5.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-6.md](../../04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-6.md) | Markdown reference |
| [docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-7.md](../../04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-7.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-02-template-system-reorganization.md](../../04.execution/tasks/2026-07-02-template-system-reorganization.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md](../../04.execution/tasks/2026-07-03-document-contract-remediation-batches.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md](../../04.execution/tasks/2026-07-03-template-system-contract-standardization.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md](../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md](../../04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-04-examples-scaffold-contract-remediation.md](../../04.execution/tasks/2026-07-04-examples-scaffold-contract-remediation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-04-frontmatter-routing-evidence-refresh.md](../../04.execution/tasks/2026-07-04-frontmatter-routing-evidence-refresh.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-04-github-branch-protection-reverification.md](../../04.execution/tasks/2026-07-04-github-branch-protection-reverification.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-04-infra-tech-stack-version-refresh.md](../../04.execution/tasks/2026-07-04-infra-tech-stack-version-refresh.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-05-agent-output-eval-fixtures.md](../../04.execution/tasks/2026-07-05-agent-output-eval-fixtures.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-05-agentic-engineering-implementation-audit-pack.md](../../04.execution/tasks/2026-07-05-agentic-engineering-implementation-audit-pack.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md](../../04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-05-audit-pack-coverage-report.md](../../04.execution/tasks/2026-07-05-audit-pack-coverage-report.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-05-compose-profile-service-coverage-snapshot.md](../../04.execution/tasks/2026-07-05-compose-profile-service-coverage-snapshot.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-05-gap-routing-recommendation.md](../../04.execution/tasks/2026-07-05-gap-routing-recommendation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-05-provider-semantic-parity-validator.md](../../04.execution/tasks/2026-07-05-provider-semantic-parity-validator.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-05-provider-workspace-artifact-path-parity.md](../../04.execution/tasks/2026-07-05-provider-workspace-artifact-path-parity.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-05-qa-gate-recommendation-ci-summary.md](../../04.execution/tasks/2026-07-05-qa-gate-recommendation-ci-summary.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-05-template-system-numbered-sdlc-paths.md](../../04.execution/tasks/2026-07-05-template-system-numbered-sdlc-paths.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-05-workspace-support-surface-contract.md](../../04.execution/tasks/2026-07-05-workspace-support-surface-contract.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-06-agent-output-eval-ci-gate.md](../../04.execution/tasks/2026-07-06-agent-output-eval-ci-gate.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-06-agent-output-eval-runner.md](../../04.execution/tasks/2026-07-06-agent-output-eval-runner.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-06-audit-implementation-matrix-snapshot.md](../../04.execution/tasks/2026-07-06-audit-implementation-matrix-snapshot.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-06-dependency-vulnerability-audit-gate.md](../../04.execution/tasks/2026-07-06-dependency-vulnerability-audit-gate.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-06-llm-wiki-stage-category-coverage.md](../../04.execution/tasks/2026-07-06-llm-wiki-stage-category-coverage.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-06-provider-hook-parity-matrix.md](../../04.execution/tasks/2026-07-06-provider-hook-parity-matrix.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-06-sdlc-document-contract-corpus-normalization.md](../../04.execution/tasks/2026-07-06-sdlc-document-contract-corpus-normalization.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-06-security-automation-readiness-snapshot.md](../../04.execution/tasks/2026-07-06-security-automation-readiness-snapshot.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-06-tech-stack-version-provenance.md](../../04.execution/tasks/2026-07-06-tech-stack-version-provenance.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md](../../04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md](../../04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-12-agentic-audit-harness-consolidation.md](../../04.execution/tasks/2026-07-12-agentic-audit-harness-consolidation.md) | Markdown reference |
| [docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md](../../04.execution/tasks/2026-07-13-document-contract-canonicalization.md) | Markdown reference |
| [docs/04.execution/tasks/README.md](../../04.execution/tasks/README.md) | folder index |

### Operations docs

| Path | Role |
| --- | --- |
| [docs/05.operations/README.md](../../05.operations/README.md) | folder index |
| [docs/05.operations/guides/00-workspace/README.md](../../05.operations/guides/00-workspace/README.md) | folder index |
| [docs/05.operations/guides/00-workspace/developer-setup.md](../../05.operations/guides/00-workspace/developer-setup.md) | Markdown reference |
| [docs/05.operations/guides/00-workspace/env-key-comparison.md](../../05.operations/guides/00-workspace/env-key-comparison.md) | Markdown reference |
| [docs/05.operations/guides/00-workspace/harness-agent-first-engineering.md](../../05.operations/guides/00-workspace/harness-agent-first-engineering.md) | Markdown reference |
| [docs/05.operations/guides/00-workspace/llm-wiki-maintenance.md](../../05.operations/guides/00-workspace/llm-wiki-maintenance.md) | Markdown reference |
| [docs/05.operations/guides/00-workspace/new-service-onboarding.md](../../05.operations/guides/00-workspace/new-service-onboarding.md) | Markdown reference |
| [docs/05.operations/guides/00-workspace/sensitive-env-vars-comparison.md](../../05.operations/guides/00-workspace/sensitive-env-vars-comparison.md) | Markdown reference |
| [docs/05.operations/guides/01-gateway/README.md](../../05.operations/guides/01-gateway/README.md) | folder index |
| [docs/05.operations/guides/01-gateway/nginx.md](../../05.operations/guides/01-gateway/nginx.md) | Markdown reference |
| [docs/05.operations/guides/01-gateway/setup.md](../../05.operations/guides/01-gateway/setup.md) | Markdown reference |
| [docs/05.operations/guides/01-gateway/traefik.md](../../05.operations/guides/01-gateway/traefik.md) | Markdown reference |
| [docs/05.operations/guides/02-auth/README.md](../../05.operations/guides/02-auth/README.md) | folder index |
| [docs/05.operations/guides/02-auth/keycloak.md](../../05.operations/guides/02-auth/keycloak.md) | Markdown reference |
| [docs/05.operations/guides/02-auth/oauth2-proxy.md](../../05.operations/guides/02-auth/oauth2-proxy.md) | Markdown reference |
| [docs/05.operations/guides/03-security/README.md](../../05.operations/guides/03-security/README.md) | folder index |
| [docs/05.operations/guides/03-security/vault.md](../../05.operations/guides/03-security/vault.md) | Markdown reference |
| [docs/05.operations/guides/04-data/README.md](../../05.operations/guides/04-data/README.md) | folder index |
| [docs/05.operations/guides/04-data/analytics/README.md](../../05.operations/guides/04-data/analytics/README.md) | folder index |
| [docs/05.operations/guides/04-data/analytics/influxdb.md](../../05.operations/guides/04-data/analytics/influxdb.md) | Markdown reference |
| [docs/05.operations/guides/04-data/analytics/ksqldb.md](../../05.operations/guides/04-data/analytics/ksqldb.md) | Markdown reference |
| [docs/05.operations/guides/04-data/analytics/opensearch.md](../../05.operations/guides/04-data/analytics/opensearch.md) | Markdown reference |
| [docs/05.operations/guides/04-data/analytics/warehouses.md](../../05.operations/guides/04-data/analytics/warehouses.md) | Markdown reference |
| [docs/05.operations/guides/04-data/cache-and-kv/README.md](../../05.operations/guides/04-data/cache-and-kv/README.md) | folder index |
| [docs/05.operations/guides/04-data/cache-and-kv/valkey-cluster.md](../../05.operations/guides/04-data/cache-and-kv/valkey-cluster.md) | Markdown reference |
| [docs/05.operations/guides/04-data/lake-and-object/README.md](../../05.operations/guides/04-data/lake-and-object/README.md) | folder index |
| [docs/05.operations/guides/04-data/lake-and-object/minio.md](../../05.operations/guides/04-data/lake-and-object/minio.md) | Markdown reference |
| [docs/05.operations/guides/04-data/lake-and-object/seaweedfs.md](../../05.operations/guides/04-data/lake-and-object/seaweedfs.md) | Markdown reference |
| [docs/05.operations/guides/04-data/nosql/README.md](../../05.operations/guides/04-data/nosql/README.md) | folder index |
| [docs/05.operations/guides/04-data/nosql/cassandra.md](../../05.operations/guides/04-data/nosql/cassandra.md) | Markdown reference |
| [docs/05.operations/guides/04-data/nosql/couchdb.md](../../05.operations/guides/04-data/nosql/couchdb.md) | Markdown reference |
| [docs/05.operations/guides/04-data/nosql/mongodb.md](../../05.operations/guides/04-data/nosql/mongodb.md) | Markdown reference |
| [docs/05.operations/guides/04-data/operational/README.md](../../05.operations/guides/04-data/operational/README.md) | folder index |
| [docs/05.operations/guides/04-data/operational/mng-db.md](../../05.operations/guides/04-data/operational/mng-db.md) | Markdown reference |
| [docs/05.operations/guides/04-data/operational/supabase.md](../../05.operations/guides/04-data/operational/supabase.md) | Markdown reference |
| [docs/05.operations/guides/04-data/optimization/README.md](../../05.operations/guides/04-data/optimization/README.md) | folder index |
| [docs/05.operations/guides/04-data/optimization/optimization-hardening.md](../../05.operations/guides/04-data/optimization/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/guides/04-data/relational/README.md](../../05.operations/guides/04-data/relational/README.md) | folder index |
| [docs/05.operations/guides/04-data/relational/postgresql-cluster.md](../../05.operations/guides/04-data/relational/postgresql-cluster.md) | Markdown reference |
| [docs/05.operations/guides/04-data/specialized/README.md](../../05.operations/guides/04-data/specialized/README.md) | folder index |
| [docs/05.operations/guides/04-data/specialized/neo4j.md](../../05.operations/guides/04-data/specialized/neo4j.md) | Markdown reference |
| [docs/05.operations/guides/04-data/specialized/qdrant.md](../../05.operations/guides/04-data/specialized/qdrant.md) | Markdown reference |
| [docs/05.operations/guides/05-messaging/README.md](../../05.operations/guides/05-messaging/README.md) | folder index |
| [docs/05.operations/guides/05-messaging/kafka.md](../../05.operations/guides/05-messaging/kafka.md) | Markdown reference |
| [docs/05.operations/guides/05-messaging/optimization-hardening.md](../../05.operations/guides/05-messaging/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/guides/05-messaging/rabbitmq.md](../../05.operations/guides/05-messaging/rabbitmq.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/README.md](../../05.operations/guides/06-observability/README.md) | folder index |
| [docs/05.operations/guides/06-observability/alertmanager.md](../../05.operations/guides/06-observability/alertmanager.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/alloy.md](../../05.operations/guides/06-observability/alloy.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/grafana.md](../../05.operations/guides/06-observability/grafana.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/lgtm-stack.md](../../05.operations/guides/06-observability/lgtm-stack.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/loki.md](../../05.operations/guides/06-observability/loki.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/optimization-hardening.md](../../05.operations/guides/06-observability/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/prometheus.md](../../05.operations/guides/06-observability/prometheus.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/pushgateway.md](../../05.operations/guides/06-observability/pushgateway.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/pyroscope.md](../../05.operations/guides/06-observability/pyroscope.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/tempo.md](../../05.operations/guides/06-observability/tempo.md) | Markdown reference |
| [docs/05.operations/guides/07-workflow/README.md](../../05.operations/guides/07-workflow/README.md) | folder index |
| [docs/05.operations/guides/07-workflow/airflow-dag-basics.md](../../05.operations/guides/07-workflow/airflow-dag-basics.md) | Markdown reference |
| [docs/05.operations/guides/07-workflow/airflow.md](../../05.operations/guides/07-workflow/airflow.md) | Markdown reference |
| [docs/05.operations/guides/07-workflow/n8n.md](../../05.operations/guides/07-workflow/n8n.md) | Markdown reference |
| [docs/05.operations/guides/07-workflow/optimization-hardening.md](../../05.operations/guides/07-workflow/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/guides/08-ai/README.md](../../05.operations/guides/08-ai/README.md) | folder index |
| [docs/05.operations/guides/08-ai/ollama.md](../../05.operations/guides/08-ai/ollama.md) | Markdown reference |
| [docs/05.operations/guides/08-ai/open-webui.md](../../05.operations/guides/08-ai/open-webui.md) | Markdown reference |
| [docs/05.operations/guides/08-ai/optimization-hardening.md](../../05.operations/guides/08-ai/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/guides/08-ai/rag-workflow.md](../../05.operations/guides/08-ai/rag-workflow.md) | Markdown reference |
| [docs/05.operations/guides/09-tooling/README.md](../../05.operations/guides/09-tooling/README.md) | folder index |
| [docs/05.operations/guides/09-tooling/k6.md](../../05.operations/guides/09-tooling/k6.md) | Markdown reference |
| [docs/05.operations/guides/09-tooling/locust.md](../../05.operations/guides/09-tooling/locust.md) | Markdown reference |
| [docs/05.operations/guides/09-tooling/optimization-hardening.md](../../05.operations/guides/09-tooling/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/guides/09-tooling/performance-testing.md](../../05.operations/guides/09-tooling/performance-testing.md) | Markdown reference |
| [docs/05.operations/guides/09-tooling/registry.md](../../05.operations/guides/09-tooling/registry.md) | Markdown reference |
| [docs/05.operations/guides/09-tooling/sonarqube.md](../../05.operations/guides/09-tooling/sonarqube.md) | Markdown reference |
| [docs/05.operations/guides/09-tooling/syncthing.md](../../05.operations/guides/09-tooling/syncthing.md) | Markdown reference |
| [docs/05.operations/guides/09-tooling/terraform.md](../../05.operations/guides/09-tooling/terraform.md) | Markdown reference |
| [docs/05.operations/guides/09-tooling/terrakube.md](../../05.operations/guides/09-tooling/terrakube.md) | Markdown reference |
| [docs/05.operations/guides/10-communication/README.md](../../05.operations/guides/10-communication/README.md) | folder index |
| [docs/05.operations/guides/10-communication/mail.md](../../05.operations/guides/10-communication/mail.md) | Markdown reference |
| [docs/05.operations/guides/11-laboratory/README.md](../../05.operations/guides/11-laboratory/README.md) | folder index |
| [docs/05.operations/guides/11-laboratory/dashboard.md](../../05.operations/guides/11-laboratory/dashboard.md) | Markdown reference |
| [docs/05.operations/guides/11-laboratory/dozzle.md](../../05.operations/guides/11-laboratory/dozzle.md) | Markdown reference |
| [docs/05.operations/guides/11-laboratory/open-notebook.md](../../05.operations/guides/11-laboratory/open-notebook.md) | Markdown reference |
| [docs/05.operations/guides/11-laboratory/optimization-hardening.md](../../05.operations/guides/11-laboratory/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/guides/11-laboratory/portainer.md](../../05.operations/guides/11-laboratory/portainer.md) | Markdown reference |
| [docs/05.operations/guides/11-laboratory/redisinsight.md](../../05.operations/guides/11-laboratory/redisinsight.md) | Markdown reference |
| [docs/05.operations/guides/12-infra-net/README.md](../../05.operations/guides/12-infra-net/README.md) | folder index |
| [docs/05.operations/guides/12-infra-net/standardize-infra-net.md](../../05.operations/guides/12-infra-net/standardize-infra-net.md) | Markdown reference |
| [docs/05.operations/guides/README.md](../../05.operations/guides/README.md) | folder index |
| [docs/05.operations/incidents/README.md](../../05.operations/incidents/README.md) | folder index |
| [docs/05.operations/policies/00-workspace/README.md](../../05.operations/policies/00-workspace/README.md) | folder index |
| [docs/05.operations/policies/00-workspace/common-optimizations-template-exceptions.md](../../05.operations/policies/00-workspace/common-optimizations-template-exceptions.md) | Markdown reference |
| [docs/05.operations/policies/00-workspace/harness-agent-first-engineering.md](../../05.operations/policies/00-workspace/harness-agent-first-engineering.md) | Markdown reference |
| [docs/05.operations/policies/00-workspace/infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md) | Markdown reference |
| [docs/05.operations/policies/00-workspace/llm-wiki-maintenance.md](../../05.operations/policies/00-workspace/llm-wiki-maintenance.md) | Markdown reference |
| [docs/05.operations/policies/01-gateway/README.md](../../05.operations/policies/01-gateway/README.md) | folder index |
| [docs/05.operations/policies/01-gateway/nginx.md](../../05.operations/policies/01-gateway/nginx.md) | Markdown reference |
| [docs/05.operations/policies/01-gateway/traefik.md](../../05.operations/policies/01-gateway/traefik.md) | Markdown reference |
| [docs/05.operations/policies/02-auth/README.md](../../05.operations/policies/02-auth/README.md) | folder index |
| [docs/05.operations/policies/02-auth/keycloak.md](../../05.operations/policies/02-auth/keycloak.md) | Markdown reference |
| [docs/05.operations/policies/02-auth/oauth2-proxy.md](../../05.operations/policies/02-auth/oauth2-proxy.md) | Markdown reference |
| [docs/05.operations/policies/03-security/README.md](../../05.operations/policies/03-security/README.md) | folder index |
| [docs/05.operations/policies/03-security/vault.md](../../05.operations/policies/03-security/vault.md) | Markdown reference |
| [docs/05.operations/policies/04-data/README.md](../../05.operations/policies/04-data/README.md) | folder index |
| [docs/05.operations/policies/04-data/analytics/README.md](../../05.operations/policies/04-data/analytics/README.md) | folder index |
| [docs/05.operations/policies/04-data/analytics/influxdb.md](../../05.operations/policies/04-data/analytics/influxdb.md) | Markdown reference |
| [docs/05.operations/policies/04-data/analytics/ksqldb.md](../../05.operations/policies/04-data/analytics/ksqldb.md) | Markdown reference |
| [docs/05.operations/policies/04-data/analytics/opensearch.md](../../05.operations/policies/04-data/analytics/opensearch.md) | Markdown reference |
| [docs/05.operations/policies/04-data/analytics/warehouses.md](../../05.operations/policies/04-data/analytics/warehouses.md) | Markdown reference |
| [docs/05.operations/policies/04-data/backup/README.md](../../05.operations/policies/04-data/backup/README.md) | folder index |
| [docs/05.operations/policies/04-data/backup/backup-policy.md](../../05.operations/policies/04-data/backup/backup-policy.md) | Markdown reference |
| [docs/05.operations/policies/04-data/cache-and-kv/README.md](../../05.operations/policies/04-data/cache-and-kv/README.md) | folder index |
| [docs/05.operations/policies/04-data/cache-and-kv/valkey-cluster.md](../../05.operations/policies/04-data/cache-and-kv/valkey-cluster.md) | Markdown reference |
| [docs/05.operations/policies/04-data/lake-and-object/README.md](../../05.operations/policies/04-data/lake-and-object/README.md) | folder index |
| [docs/05.operations/policies/04-data/lake-and-object/minio.md](../../05.operations/policies/04-data/lake-and-object/minio.md) | Markdown reference |
| [docs/05.operations/policies/04-data/lake-and-object/seaweedfs.md](../../05.operations/policies/04-data/lake-and-object/seaweedfs.md) | Markdown reference |
| [docs/05.operations/policies/04-data/nosql/README.md](../../05.operations/policies/04-data/nosql/README.md) | folder index |
| [docs/05.operations/policies/04-data/nosql/cassandra.md](../../05.operations/policies/04-data/nosql/cassandra.md) | Markdown reference |
| [docs/05.operations/policies/04-data/nosql/couchdb.md](../../05.operations/policies/04-data/nosql/couchdb.md) | Markdown reference |
| [docs/05.operations/policies/04-data/nosql/mongodb.md](../../05.operations/policies/04-data/nosql/mongodb.md) | Markdown reference |
| [docs/05.operations/policies/04-data/operational/README.md](../../05.operations/policies/04-data/operational/README.md) | folder index |
| [docs/05.operations/policies/04-data/operational/mng-db.md](../../05.operations/policies/04-data/operational/mng-db.md) | Markdown reference |
| [docs/05.operations/policies/04-data/operational/supabase.md](../../05.operations/policies/04-data/operational/supabase.md) | Markdown reference |
| [docs/05.operations/policies/04-data/optimization/README.md](../../05.operations/policies/04-data/optimization/README.md) | folder index |
| [docs/05.operations/policies/04-data/optimization/optimization-hardening.md](../../05.operations/policies/04-data/optimization/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/policies/04-data/relational/README.md](../../05.operations/policies/04-data/relational/README.md) | folder index |
| [docs/05.operations/policies/04-data/relational/postgresql-cluster.md](../../05.operations/policies/04-data/relational/postgresql-cluster.md) | Markdown reference |
| [docs/05.operations/policies/04-data/specialized/README.md](../../05.operations/policies/04-data/specialized/README.md) | folder index |
| [docs/05.operations/policies/04-data/specialized/neo4j.md](../../05.operations/policies/04-data/specialized/neo4j.md) | Markdown reference |
| [docs/05.operations/policies/04-data/specialized/qdrant.md](../../05.operations/policies/04-data/specialized/qdrant.md) | Markdown reference |
| [docs/05.operations/policies/05-messaging/README.md](../../05.operations/policies/05-messaging/README.md) | folder index |
| [docs/05.operations/policies/05-messaging/kafka.md](../../05.operations/policies/05-messaging/kafka.md) | Markdown reference |
| [docs/05.operations/policies/05-messaging/optimization-hardening.md](../../05.operations/policies/05-messaging/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/policies/05-messaging/rabbitmq.md](../../05.operations/policies/05-messaging/rabbitmq.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/README.md](../../05.operations/policies/06-observability/README.md) | folder index |
| [docs/05.operations/policies/06-observability/alertmanager.md](../../05.operations/policies/06-observability/alertmanager.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/alloy.md](../../05.operations/policies/06-observability/alloy.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/grafana.md](../../05.operations/policies/06-observability/grafana.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/loki.md](../../05.operations/policies/06-observability/loki.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/optimization-hardening.md](../../05.operations/policies/06-observability/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/prometheus.md](../../05.operations/policies/06-observability/prometheus.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/pushgateway.md](../../05.operations/policies/06-observability/pushgateway.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/pyroscope.md](../../05.operations/policies/06-observability/pyroscope.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/retention.md](../../05.operations/policies/06-observability/retention.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/tempo.md](../../05.operations/policies/06-observability/tempo.md) | Markdown reference |
| [docs/05.operations/policies/07-workflow/README.md](../../05.operations/policies/07-workflow/README.md) | folder index |
| [docs/05.operations/policies/07-workflow/airflow.md](../../05.operations/policies/07-workflow/airflow.md) | Markdown reference |
| [docs/05.operations/policies/07-workflow/dag-deployment.md](../../05.operations/policies/07-workflow/dag-deployment.md) | Markdown reference |
| [docs/05.operations/policies/07-workflow/n8n.md](../../05.operations/policies/07-workflow/n8n.md) | Markdown reference |
| [docs/05.operations/policies/07-workflow/optimization-hardening.md](../../05.operations/policies/07-workflow/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/policies/08-ai/README.md](../../05.operations/policies/08-ai/README.md) | folder index |
| [docs/05.operations/policies/08-ai/ollama.md](../../05.operations/policies/08-ai/ollama.md) | Markdown reference |
| [docs/05.operations/policies/08-ai/open-webui.md](../../05.operations/policies/08-ai/open-webui.md) | Markdown reference |
| [docs/05.operations/policies/08-ai/optimization-hardening.md](../../05.operations/policies/08-ai/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/policies/09-tooling/README.md](../../05.operations/policies/09-tooling/README.md) | folder index |
| [docs/05.operations/policies/09-tooling/iac-deployment-policy.md](../../05.operations/policies/09-tooling/iac-deployment-policy.md) | Markdown reference |
| [docs/05.operations/policies/09-tooling/k6.md](../../05.operations/policies/09-tooling/k6.md) | Markdown reference |
| [docs/05.operations/policies/09-tooling/locust.md](../../05.operations/policies/09-tooling/locust.md) | Markdown reference |
| [docs/05.operations/policies/09-tooling/optimization-hardening.md](../../05.operations/policies/09-tooling/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/policies/09-tooling/performance-testing.md](../../05.operations/policies/09-tooling/performance-testing.md) | Markdown reference |
| [docs/05.operations/policies/09-tooling/registry.md](../../05.operations/policies/09-tooling/registry.md) | Markdown reference |
| [docs/05.operations/policies/09-tooling/sonarqube.md](../../05.operations/policies/09-tooling/sonarqube.md) | Markdown reference |
| [docs/05.operations/policies/09-tooling/syncthing.md](../../05.operations/policies/09-tooling/syncthing.md) | Markdown reference |
| [docs/05.operations/policies/09-tooling/terraform.md](../../05.operations/policies/09-tooling/terraform.md) | Markdown reference |
| [docs/05.operations/policies/09-tooling/terrakube.md](../../05.operations/policies/09-tooling/terrakube.md) | Markdown reference |
| [docs/05.operations/policies/10-communication/README.md](../../05.operations/policies/10-communication/README.md) | folder index |
| [docs/05.operations/policies/10-communication/mail.md](../../05.operations/policies/10-communication/mail.md) | Markdown reference |
| [docs/05.operations/policies/11-laboratory/README.md](../../05.operations/policies/11-laboratory/README.md) | folder index |
| [docs/05.operations/policies/11-laboratory/dashboard.md](../../05.operations/policies/11-laboratory/dashboard.md) | Markdown reference |
| [docs/05.operations/policies/11-laboratory/dozzle.md](../../05.operations/policies/11-laboratory/dozzle.md) | Markdown reference |
| [docs/05.operations/policies/11-laboratory/open-notebook.md](../../05.operations/policies/11-laboratory/open-notebook.md) | Markdown reference |
| [docs/05.operations/policies/11-laboratory/optimization-hardening.md](../../05.operations/policies/11-laboratory/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/policies/11-laboratory/portainer.md](../../05.operations/policies/11-laboratory/portainer.md) | Markdown reference |
| [docs/05.operations/policies/11-laboratory/redisinsight.md](../../05.operations/policies/11-laboratory/redisinsight.md) | Markdown reference |
| [docs/05.operations/policies/12-infra-net/README.md](../../05.operations/policies/12-infra-net/README.md) | folder index |
| [docs/05.operations/policies/12-infra-net/standardize-infra-net.md](../../05.operations/policies/12-infra-net/standardize-infra-net.md) | Markdown reference |
| [docs/05.operations/policies/README.md](../../05.operations/policies/README.md) | folder index |
| [docs/05.operations/releases/README.md](../../05.operations/releases/README.md) | folder index |
| [docs/05.operations/runbooks/00-workspace/README.md](../../05.operations/runbooks/00-workspace/README.md) | folder index |
| [docs/05.operations/runbooks/00-workspace/harness-agent-first-engineering-validation.md](../../05.operations/runbooks/00-workspace/harness-agent-first-engineering-validation.md) | Markdown reference |
| [docs/05.operations/runbooks/00-workspace/llm-wiki-maintenance.md](../../05.operations/runbooks/00-workspace/llm-wiki-maintenance.md) | Markdown reference |
| [docs/05.operations/runbooks/00-workspace/release-management.md](../../05.operations/runbooks/00-workspace/release-management.md) | Markdown reference |
| [docs/05.operations/runbooks/01-gateway/README.md](../../05.operations/runbooks/01-gateway/README.md) | folder index |
| [docs/05.operations/runbooks/01-gateway/nginx.md](../../05.operations/runbooks/01-gateway/nginx.md) | Markdown reference |
| [docs/05.operations/runbooks/01-gateway/traefik.md](../../05.operations/runbooks/01-gateway/traefik.md) | Markdown reference |
| [docs/05.operations/runbooks/02-auth/README.md](../../05.operations/runbooks/02-auth/README.md) | folder index |
| [docs/05.operations/runbooks/02-auth/keycloak.md](../../05.operations/runbooks/02-auth/keycloak.md) | Markdown reference |
| [docs/05.operations/runbooks/02-auth/oauth2-proxy.md](../../05.operations/runbooks/02-auth/oauth2-proxy.md) | Markdown reference |
| [docs/05.operations/runbooks/03-security/README.md](../../05.operations/runbooks/03-security/README.md) | folder index |
| [docs/05.operations/runbooks/03-security/vault.md](../../05.operations/runbooks/03-security/vault.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/README.md](../../05.operations/runbooks/04-data/README.md) | folder index |
| [docs/05.operations/runbooks/04-data/analytics/README.md](../../05.operations/runbooks/04-data/analytics/README.md) | folder index |
| [docs/05.operations/runbooks/04-data/analytics/influxdb.md](../../05.operations/runbooks/04-data/analytics/influxdb.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/analytics/ksqldb.md](../../05.operations/runbooks/04-data/analytics/ksqldb.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/analytics/opensearch.md](../../05.operations/runbooks/04-data/analytics/opensearch.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/analytics/warehouses.md](../../05.operations/runbooks/04-data/analytics/warehouses.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/cache-and-kv/README.md](../../05.operations/runbooks/04-data/cache-and-kv/README.md) | folder index |
| [docs/05.operations/runbooks/04-data/cache-and-kv/valkey-cluster.md](../../05.operations/runbooks/04-data/cache-and-kv/valkey-cluster.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/lake-and-object/README.md](../../05.operations/runbooks/04-data/lake-and-object/README.md) | folder index |
| [docs/05.operations/runbooks/04-data/lake-and-object/minio.md](../../05.operations/runbooks/04-data/lake-and-object/minio.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/lake-and-object/seaweedfs.md](../../05.operations/runbooks/04-data/lake-and-object/seaweedfs.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/nosql/README.md](../../05.operations/runbooks/04-data/nosql/README.md) | folder index |
| [docs/05.operations/runbooks/04-data/nosql/cassandra.md](../../05.operations/runbooks/04-data/nosql/cassandra.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/nosql/couchdb.md](../../05.operations/runbooks/04-data/nosql/couchdb.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/nosql/mongodb.md](../../05.operations/runbooks/04-data/nosql/mongodb.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/operational/README.md](../../05.operations/runbooks/04-data/operational/README.md) | folder index |
| [docs/05.operations/runbooks/04-data/operational/mng-db.md](../../05.operations/runbooks/04-data/operational/mng-db.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/operational/supabase.md](../../05.operations/runbooks/04-data/operational/supabase.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/optimization/README.md](../../05.operations/runbooks/04-data/optimization/README.md) | folder index |
| [docs/05.operations/runbooks/04-data/optimization/optimization-hardening.md](../../05.operations/runbooks/04-data/optimization/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/relational/README.md](../../05.operations/runbooks/04-data/relational/README.md) | folder index |
| [docs/05.operations/runbooks/04-data/relational/postgresql-cluster.md](../../05.operations/runbooks/04-data/relational/postgresql-cluster.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/specialized/README.md](../../05.operations/runbooks/04-data/specialized/README.md) | folder index |
| [docs/05.operations/runbooks/04-data/specialized/neo4j.md](../../05.operations/runbooks/04-data/specialized/neo4j.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/specialized/qdrant.md](../../05.operations/runbooks/04-data/specialized/qdrant.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/storage/README.md](../../05.operations/runbooks/04-data/storage/README.md) | folder index |
| [docs/05.operations/runbooks/04-data/storage/storage-exhaustion.md](../../05.operations/runbooks/04-data/storage/storage-exhaustion.md) | Markdown reference |
| [docs/05.operations/runbooks/05-messaging/README.md](../../05.operations/runbooks/05-messaging/README.md) | folder index |
| [docs/05.operations/runbooks/05-messaging/kafka.md](../../05.operations/runbooks/05-messaging/kafka.md) | Markdown reference |
| [docs/05.operations/runbooks/05-messaging/optimization-hardening.md](../../05.operations/runbooks/05-messaging/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/runbooks/05-messaging/rabbitmq.md](../../05.operations/runbooks/05-messaging/rabbitmq.md) | Markdown reference |
| [docs/05.operations/runbooks/06-observability/README.md](../../05.operations/runbooks/06-observability/README.md) | folder index |
| [docs/05.operations/runbooks/06-observability/alertmanager.md](../../05.operations/runbooks/06-observability/alertmanager.md) | Markdown reference |
| [docs/05.operations/runbooks/06-observability/alloy.md](../../05.operations/runbooks/06-observability/alloy.md) | Markdown reference |
| [docs/05.operations/runbooks/06-observability/grafana.md](../../05.operations/runbooks/06-observability/grafana.md) | Markdown reference |
| [docs/05.operations/runbooks/06-observability/loki.md](../../05.operations/runbooks/06-observability/loki.md) | Markdown reference |
| [docs/05.operations/runbooks/06-observability/optimization-hardening.md](../../05.operations/runbooks/06-observability/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/runbooks/06-observability/prometheus.md](../../05.operations/runbooks/06-observability/prometheus.md) | Markdown reference |
| [docs/05.operations/runbooks/06-observability/pushgateway.md](../../05.operations/runbooks/06-observability/pushgateway.md) | Markdown reference |
| [docs/05.operations/runbooks/06-observability/pyroscope.md](../../05.operations/runbooks/06-observability/pyroscope.md) | Markdown reference |
| [docs/05.operations/runbooks/06-observability/tempo.md](../../05.operations/runbooks/06-observability/tempo.md) | Markdown reference |
| [docs/05.operations/runbooks/07-workflow/README.md](../../05.operations/runbooks/07-workflow/README.md) | folder index |
| [docs/05.operations/runbooks/07-workflow/airflow.md](../../05.operations/runbooks/07-workflow/airflow.md) | Markdown reference |
| [docs/05.operations/runbooks/07-workflow/n8n.md](../../05.operations/runbooks/07-workflow/n8n.md) | Markdown reference |
| [docs/05.operations/runbooks/07-workflow/optimization-hardening.md](../../05.operations/runbooks/07-workflow/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/runbooks/08-ai/README.md](../../05.operations/runbooks/08-ai/README.md) | folder index |
| [docs/05.operations/runbooks/08-ai/gpu-recovery.md](../../05.operations/runbooks/08-ai/gpu-recovery.md) | Markdown reference |
| [docs/05.operations/runbooks/08-ai/ollama.md](../../05.operations/runbooks/08-ai/ollama.md) | Markdown reference |
| [docs/05.operations/runbooks/08-ai/open-webui.md](../../05.operations/runbooks/08-ai/open-webui.md) | Markdown reference |
| [docs/05.operations/runbooks/08-ai/optimization-hardening.md](../../05.operations/runbooks/08-ai/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/runbooks/09-tooling/README.md](../../05.operations/runbooks/09-tooling/README.md) | folder index |
| [docs/05.operations/runbooks/09-tooling/k6.md](../../05.operations/runbooks/09-tooling/k6.md) | Markdown reference |
| [docs/05.operations/runbooks/09-tooling/locust.md](../../05.operations/runbooks/09-tooling/locust.md) | Markdown reference |
| [docs/05.operations/runbooks/09-tooling/optimization-hardening.md](../../05.operations/runbooks/09-tooling/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/runbooks/09-tooling/performance-testing.md](../../05.operations/runbooks/09-tooling/performance-testing.md) | Markdown reference |
| [docs/05.operations/runbooks/09-tooling/registry.md](../../05.operations/runbooks/09-tooling/registry.md) | Markdown reference |
| [docs/05.operations/runbooks/09-tooling/sonarqube.md](../../05.operations/runbooks/09-tooling/sonarqube.md) | Markdown reference |
| [docs/05.operations/runbooks/09-tooling/syncthing.md](../../05.operations/runbooks/09-tooling/syncthing.md) | Markdown reference |
| [docs/05.operations/runbooks/09-tooling/terraform.md](../../05.operations/runbooks/09-tooling/terraform.md) | Markdown reference |
| [docs/05.operations/runbooks/09-tooling/terrakube.md](../../05.operations/runbooks/09-tooling/terrakube.md) | Markdown reference |
| [docs/05.operations/runbooks/10-communication/README.md](../../05.operations/runbooks/10-communication/README.md) | folder index |
| [docs/05.operations/runbooks/10-communication/mail.md](../../05.operations/runbooks/10-communication/mail.md) | Markdown reference |
| [docs/05.operations/runbooks/11-laboratory/README.md](../../05.operations/runbooks/11-laboratory/README.md) | folder index |
| [docs/05.operations/runbooks/11-laboratory/dashboard.md](../../05.operations/runbooks/11-laboratory/dashboard.md) | Markdown reference |
| [docs/05.operations/runbooks/11-laboratory/dozzle.md](../../05.operations/runbooks/11-laboratory/dozzle.md) | Markdown reference |
| [docs/05.operations/runbooks/11-laboratory/open-notebook.md](../../05.operations/runbooks/11-laboratory/open-notebook.md) | Markdown reference |
| [docs/05.operations/runbooks/11-laboratory/optimization-hardening.md](../../05.operations/runbooks/11-laboratory/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/runbooks/11-laboratory/portainer.md](../../05.operations/runbooks/11-laboratory/portainer.md) | Markdown reference |
| [docs/05.operations/runbooks/11-laboratory/redisinsight.md](../../05.operations/runbooks/11-laboratory/redisinsight.md) | Markdown reference |
| [docs/05.operations/runbooks/12-infra-net/README.md](../../05.operations/runbooks/12-infra-net/README.md) | folder index |
| [docs/05.operations/runbooks/12-infra-net/standardize-infra-net.md](../../05.operations/runbooks/12-infra-net/standardize-infra-net.md) | Markdown reference |
| [docs/05.operations/runbooks/README.md](../../05.operations/runbooks/README.md) | folder index |

### Reference and template docs

| Path | Role |
| --- | --- |
| [docs/90.references/README.md](../README.md) | folder index |
| [docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/README.md](../audits/2026-07-03-workspace-document-contract-audit-pack/README.md) | folder index |
| [docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md](../audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md) | Markdown reference |
| [docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/ci-qa-parser-graphify-decision.md](../audits/2026-07-03-workspace-document-contract-audit-pack/ci-qa-parser-graphify-decision.md) | Markdown reference |
| [docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/contract-governance-map.md](../audits/2026-07-03-workspace-document-contract-audit-pack/contract-governance-map.md) | Markdown reference |
| [docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-inventory.md](../audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-inventory.md) | Markdown reference |
| [docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-routing-profile.md](../audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-routing-profile.md) | Markdown reference |
| [docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md](../audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md) | Markdown reference |
| [docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/historical-evidence-preservation.md](../audits/2026-07-03-workspace-document-contract-audit-pack/historical-evidence-preservation.md) | Markdown reference |
| [docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/readme-profile-inventory.md](../audits/2026-07-03-workspace-document-contract-audit-pack/readme-profile-inventory.md) | Markdown reference |
| [docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/section-profile-inventory.md](../audits/2026-07-03-workspace-document-contract-audit-pack/section-profile-inventory.md) | Markdown reference |
| [docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/template-application-gaps.md](../audits/2026-07-03-workspace-document-contract-audit-pack/template-application-gaps.md) | Markdown reference |
| [docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/README.md](../audits/2026-07-04-document-restructure-audit-contract-archive/README.md) | folder index |
| [docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/ci-qa-formatting-contract.md](../audits/2026-07-04-document-restructure-audit-contract-archive/ci-qa-formatting-contract.md) | Markdown reference |
| [docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/frontmatter-profile-inventory.md](../audits/2026-07-04-document-restructure-audit-contract-archive/frontmatter-profile-inventory.md) | Markdown reference |
| [docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/operations-bucket-restructure.md](../audits/2026-07-04-document-restructure-audit-contract-archive/operations-bucket-restructure.md) | Markdown reference |
| [docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/restructure-gap-register.md](../audits/2026-07-04-document-restructure-audit-contract-archive/restructure-gap-register.md) | Markdown reference |
| [docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/sdlc-spec-archive-candidates.md](../audits/2026-07-04-document-restructure-audit-contract-archive/sdlc-spec-archive-candidates.md) | Markdown reference |
| [docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/template-contract-drift.md](../audits/2026-07-04-document-restructure-audit-contract-archive/template-contract-drift.md) | Markdown reference |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md) | folder index |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/agent-instructions-catalog-vibe-models.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/agent-instructions-catalog-vibe-models.md) | Markdown reference |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md) | Markdown reference |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/compose-infrastructure-operations-readiness.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/compose-infrastructure-operations-readiness.md) | Markdown reference |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md) | Markdown reference |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-template-readme-implementation.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-template-readme-implementation.md) | Markdown reference |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/harness-engineering-implementation.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/harness-engineering-implementation.md) | Markdown reference |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md) | Markdown reference |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/loop-engineering-implementation.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/loop-engineering-implementation.md) | Markdown reference |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/provider-harness-loop-implementation.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/provider-harness-loop-implementation.md) | Markdown reference |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-document-contracts-implementation.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-document-contracts-implementation.md) | Markdown reference |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md) | Markdown reference |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md) | Markdown reference |
| [docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/workspace-rules-environment-implementation.md](../audits/2026-07-05-agentic-engineering-implementation-audit-pack/workspace-rules-environment-implementation.md) | Markdown reference |
| [docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/README.md](../audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/README.md) | folder index |
| [docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/agent-catalog-audit.md](../audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/agent-catalog-audit.md) | Markdown reference |
| [docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/automation-candidates.md](../audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/automation-candidates.md) | Markdown reference |
| [docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/harness-loop-audit.md](../audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/harness-loop-audit.md) | Markdown reference |
| [docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/implementation-overview.md](../audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/implementation-overview.md) | Markdown reference |
| [docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/sdlc-qa-security-audit.md](../audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/sdlc-qa-security-audit.md) | Markdown reference |
| [docs/90.references/audits/README.md](../audits/README.md) | folder index |
| [docs/90.references/data/README.md](../data/README.md) | folder index |
| [docs/90.references/data/docker/README.md](../data/docker/README.md) | folder index |
| [docs/90.references/data/docker/compose-profile-service-coverage.md](../data/docker/compose-profile-service-coverage.md) | Markdown reference |
| [docs/90.references/data/docker/image-version-interpretation.md](../data/docker/image-version-interpretation.md) | Markdown reference |
| [docs/90.references/data/docker/tech-stack-version-provenance.md](../data/docker/tech-stack-version-provenance.md) | Markdown reference |
| [docs/90.references/data/glossary/README.md](../data/glossary/README.md) | folder index |
| [docs/90.references/data/glossary/stable-reference-terms.md](../data/glossary/stable-reference-terms.md) | Markdown reference |
| [docs/90.references/data/governance/README.md](../data/governance/README.md) | folder index |
| [docs/90.references/data/governance/agent-output-eval-fixtures.md](../data/governance/agent-output-eval-fixtures.md) | Markdown reference |
| [docs/90.references/data/governance/audit-implementation-matrix.md](../data/governance/audit-implementation-matrix.md) | Markdown reference |
| [docs/90.references/data/governance/gap-to-stage-routing.md](../data/governance/gap-to-stage-routing.md) | Markdown reference |
| [docs/90.references/data/governance/provider-hook-parity-matrix.md](../data/governance/provider-hook-parity-matrix.md) | Markdown reference |
| [docs/90.references/data/hads/README.md](../data/hads/README.md) | folder index |
| [docs/90.references/data/hads/profile.md](../data/hads/profile.md) | Markdown reference |
| [docs/90.references/data/knowledge/README.md](../data/knowledge/README.md) | folder index |
| [docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md](../data/knowledge/llm-wiki-stage-category-coverage.md) | Markdown reference |
| [docs/90.references/data/kubernetes/README.md](../data/kubernetes/README.md) | folder index |
| [docs/90.references/data/kubernetes/docker-compose-to-k3s-migration.md](../data/kubernetes/docker-compose-to-k3s-migration.md) | Markdown reference |
| [docs/90.references/data/security/README.md](../data/security/README.md) | folder index |
| [docs/90.references/data/security/security-automation-readiness.md](../data/security/security-automation-readiness.md) | Markdown reference |
| [docs/90.references/learning/README.md](../learning/README.md) | folder index |
| [docs/90.references/learning/roadmap-v1.md](../learning/roadmap-v1.md) | Markdown reference |
| [docs/90.references/learning/roadmap.md](../learning/roadmap.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md](../research/2026-07-05-agentic-research-pack-refresh/README.md) | folder index |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-instructions-vibe-coding.md](../research/2026-07-05-agentic-research-pack-refresh/agent-instructions-vibe-coding.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md](../research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md](../research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md](../research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md](../research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/document-metadata-lifecycle.md](../research/2026-07-05-agentic-research-pack-refresh/document-metadata-lifecycle.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md](../research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md](../research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md](../research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md](../research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md](../research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md](../research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md](../research/2026-07-05-agentic-research-pack-refresh/security-governance.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md](../research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md) | Markdown reference |
| [docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md](../research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md) | Markdown reference |
| [docs/90.references/research/2026-07-07-agentic-research-pack-update/README.md](../research/2026-07-07-agentic-research-pack-update/README.md) | folder index |
| [docs/90.references/research/2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md](../research/2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md) | Markdown reference |
| [docs/90.references/research/2026-07-07-agentic-research-pack-update/harness-engineering.md](../research/2026-07-07-agentic-research-pack-update/harness-engineering.md) | Markdown reference |
| [docs/90.references/research/2026-07-07-agentic-research-pack-update/loop-engineering.md](../research/2026-07-07-agentic-research-pack-update/loop-engineering.md) | Markdown reference |
| [docs/90.references/research/2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md](../research/2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md) | Markdown reference |
| [docs/90.references/research/2026-07-07-agentic-research-pack-update/workspace-baseline.md](../research/2026-07-07-agentic-research-pack-update/workspace-baseline.md) | Markdown reference |
| [docs/90.references/research/README.md](../research/README.md) | folder index |
| [docs/99.templates/README.md](../../99.templates/README.md) | folder index |
| [docs/99.templates/support/README.md](../../99.templates/support/README.md) | folder index |
| [docs/99.templates/support/common-document-contract.md](../../99.templates/support/common-document-contract.md) | Markdown reference |
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
| [docs/99.templates/templates/common/readme.template.md](../../99.templates/templates/common/readme.template.md) | Markdown reference |
| [docs/99.templates/templates/common/reference.template.md](../../99.templates/templates/common/reference.template.md) | Markdown reference |
| [docs/99.templates/templates/governance/README.md](../../99.templates/templates/governance/README.md) | folder index |
| [docs/99.templates/templates/governance/harness-task-contract.template.md](../../99.templates/templates/governance/harness-task-contract.template.md) | Markdown reference |
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
| [docs/99.templates/templates/sdlc/ard.template.md](../../99.templates/templates/sdlc/ard.template.md) | Markdown reference |
| [docs/99.templates/templates/sdlc/plan.template.md](../../99.templates/templates/sdlc/plan.template.md) | Markdown reference |
| [docs/99.templates/templates/sdlc/prd.template.md](../../99.templates/templates/sdlc/prd.template.md) | Markdown reference |
| [docs/99.templates/templates/sdlc/spec.template.md](../../99.templates/templates/sdlc/spec.template.md) | Markdown reference |
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
| [infra/04-data/analytics/influxdb/docker-compose.v2.yml](../../../infra/04-data/analytics/influxdb/docker-compose.v2.yml) | YAML config |
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
| [infra/04-data/lake-and-object/seaweedfs/config/security.toml](../../../infra/04-data/lake-and-object/seaweedfs/config/security.toml) | source path |
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
| [infra/tech-stack.versions.json](../../../infra/tech-stack.versions.json) | JSON registry |

### Scripts and validators

| Path | Role |
| --- | --- |
| [scripts/README.md](../../../scripts/README.md) | folder index |
| [scripts/hardening/check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh) | script |
| [scripts/hooks/agent-event-hook.sh](../../../scripts/hooks/agent-event-hook.sh) | script |
| [scripts/hooks/patch-graphify-post-commit.sh](../../../scripts/hooks/patch-graphify-post-commit.sh) | script |
| [scripts/hooks/post-tool-validate.sh](../../../scripts/hooks/post-tool-validate.sh) | script |
| [scripts/knowledge/generate-llm-wiki-coverage.sh](../../../scripts/knowledge/generate-llm-wiki-coverage.sh) | script |
| [scripts/knowledge/generate-llm-wiki-index.sh](../../../scripts/knowledge/generate-llm-wiki-index.sh) | script |
| [scripts/knowledge/report-graphify-health.sh](../../../scripts/knowledge/report-graphify-health.sh) | script |
| [scripts/lib/hardening-lib.sh](../../../scripts/lib/hardening-lib.sh) | script |
| [scripts/operations/gen-secrets.sh](../../../scripts/operations/gen-secrets.sh) | script |
| [scripts/operations/generate-compose-profile-service-coverage.sh](../../../scripts/operations/generate-compose-profile-service-coverage.sh) | script |
| [scripts/operations/generate-tech-stack-version-provenance.sh](../../../scripts/operations/generate-tech-stack-version-provenance.sh) | script |
| [scripts/operations/sync-provider-surfaces.sh](../../../scripts/operations/sync-provider-surfaces.sh) | script |
| [scripts/operations/sync-tech-stack-versions.sh](../../../scripts/operations/sync-tech-stack-versions.sh) | script |
| [scripts/operations/use-qa-ci-tools.sh](../../../scripts/operations/use-qa-ci-tools.sh) | script |
| [scripts/requirements.txt](../../../scripts/requirements.txt) | text entrypoint |
| [scripts/validation/agentic-audit-semantic-contract.json](../../../scripts/validation/agentic-audit-semantic-contract.json) | JSON registry |
| [scripts/validation/check-doc-implementation-alignment.sh](../../../scripts/validation/check-doc-implementation-alignment.sh) | script |
| [scripts/validation/check-doc-traceability.sh](../../../scripts/validation/check-doc-traceability.sh) | script |
| [scripts/validation/check-quickwin-baseline.sh](../../../scripts/validation/check-quickwin-baseline.sh) | script |
| [scripts/validation/check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) | script |
| [scripts/validation/check-storybook-contract.sh](../../../scripts/validation/check-storybook-contract.sh) | script |
| [scripts/validation/check-template-security-baseline.sh](../../../scripts/validation/check-template-security-baseline.sh) | script |
| [scripts/validation/generate-audit-implementation-matrix.sh](../../../scripts/validation/generate-audit-implementation-matrix.sh) | script |
| [scripts/validation/generate-security-automation-readiness.sh](../../../scripts/validation/generate-security-automation-readiness.sh) | script |
| [scripts/validation/recommend-gap-routing.sh](../../../scripts/validation/recommend-gap-routing.sh) | script |
| [scripts/validation/recommend-qa-gates.sh](../../../scripts/validation/recommend-qa-gates.sh) | script |
| [scripts/validation/report-audit-pack-coverage.sh](../../../scripts/validation/report-audit-pack-coverage.sh) | script |
| [scripts/validation/report-provider-hook-parity.sh](../../../scripts/validation/report-provider-hook-parity.sh) | script |
| [scripts/validation/run-agent-output-eval-fixtures.sh](../../../scripts/validation/run-agent-output-eval-fixtures.sh) | script |
| [scripts/validation/run-agent-precommit-all-files.sh](../../../scripts/validation/run-agent-precommit-all-files.sh) | script |
| [scripts/validation/run-local-qa-gates.sh](../../../scripts/validation/run-local-qa-gates.sh) | script |
| [scripts/validation/validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh) | script |
| [scripts/validation/validate-harness.sh](../../../scripts/validation/validate-harness.sh) | script |

### GitHub workflow surface

| Path | Role |
| --- | --- |
| [.github/CODEOWNERS](../../../.github/CODEOWNERS) | source path |
| [.github/ISSUE_TEMPLATE/bug_report.yml](../../../.github/ISSUE_TEMPLATE/bug_report.yml) | YAML config |
| [.github/ISSUE_TEMPLATE/feature_request.yml](../../../.github/ISSUE_TEMPLATE/feature_request.yml) | YAML config |
| [.github/PULL_REQUEST_TEMPLATE.md](../../../.github/PULL_REQUEST_TEMPLATE.md) | Markdown reference |
| [.github/SECURITY.md](../../../.github/SECURITY.md) | Markdown reference |
| [.github/dependabot.yml](../../../.github/dependabot.yml) | YAML config |
| [.github/labeler.yml](../../../.github/labeler.yml) | YAML config |
| [.github/rulesets/main-protection.md](../../../.github/rulesets/main-protection.md) | Markdown reference |
| [.github/workflows/ci-quality.yml](../../../.github/workflows/ci-quality.yml) | YAML config |
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
| [docs/98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md](../../98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md) | Markdown reference |
| [docs/98.archive/04.execution/plans/2026-05-30-standardizing-agent-governance.md](../../98.archive/04.execution/plans/2026-05-30-standardizing-agent-governance.md) | Markdown reference |
| [docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md](../../98.archive/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md) | Markdown reference |
| [docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase2-alignment.md](../../98.archive/04.execution/plans/2026-06-01-agent-governance-phase2-alignment.md) | Markdown reference |
| [docs/98.archive/04.execution/tasks/2026-05-30-standardizing-agent-governance.md](../../98.archive/04.execution/tasks/2026-05-30-standardizing-agent-governance.md) | Markdown reference |
| [docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase1-diagnostic.md](../../98.archive/04.execution/tasks/2026-06-01-agent-governance-phase1-diagnostic.md) | Markdown reference |
| [docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-implementation.md](../../98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-implementation.md) | Markdown reference |
| [docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-stage01-02-continuation.md](../../98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-stage01-02-continuation.md) | Markdown reference |
| [docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-strategy-integration.md](../../98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-strategy-integration.md) | Markdown reference |
| [docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase4-closure.md](../../98.archive/04.execution/tasks/2026-06-01-agent-governance-phase4-closure.md) | Markdown reference |
| [docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-stage01-02-alignment.md](../../98.archive/04.execution/tasks/2026-06-01-agent-governance-stage01-02-alignment.md) | Markdown reference |
| [docs/98.archive/05.operations/guides/03-security/01.setup.md](../../98.archive/05.operations/guides/03-security/01.setup.md) | Markdown reference |
| [docs/98.archive/05.operations/guides/05-messaging/ksql-streaming.md](../../98.archive/05.operations/guides/05-messaging/ksql-streaming.md) | Markdown reference |
| [docs/98.archive/05.operations/guides/07-workflow/01.airflow-dag-dev.md](../../98.archive/05.operations/guides/07-workflow/01.airflow-dag-dev.md) | Markdown reference |
| [docs/98.archive/05.operations/guides/07-workflow/airbyte.md](../../98.archive/05.operations/guides/07-workflow/airbyte.md) | Markdown reference |
| [docs/98.archive/05.operations/guides/08-ai/01.llm-inference.md](../../98.archive/05.operations/guides/08-ai/01.llm-inference.md) | Markdown reference |
| [docs/98.archive/05.operations/guides/08-ai/local-llm-setup.md](../../98.archive/05.operations/guides/08-ai/local-llm-setup.md) | Markdown reference |
| [docs/98.archive/05.operations/guides/09-tooling/01.iac-automation.md](../../98.archive/05.operations/guides/09-tooling/01.iac-automation.md) | Markdown reference |
| [docs/98.archive/05.operations/policies/07-workflow/airbyte.md](../../98.archive/05.operations/policies/07-workflow/airbyte.md) | Markdown reference |
| [docs/98.archive/05.operations/runbooks/07-workflow/airbyte.md](../../98.archive/05.operations/runbooks/07-workflow/airbyte.md) | Markdown reference |
| [docs/98.archive/README.md](../../98.archive/README.md) | folder index |

## Sources

- [llms.txt](../../../llms.txt) - root LLM entrypoint and boundary statement
- [repository-map.md](./repository-map.md) - curated canonical source map
- [generate-llm-wiki-index.sh](../../../scripts/knowledge/generate-llm-wiki-index.sh) - deterministic generator
- [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) - freshness and safety validator

## Maintenance

- **Owner**: `wiki-curator`
- **Review Cadence**: Review when root entrypoints, governance, operations docs, script inventory, infrastructure indexes, or LLM Wiki files change
- **Update Trigger**: Run `bash scripts/knowledge/generate-llm-wiki-index.sh` after in-scope path changes and `bash scripts/knowledge/generate-llm-wiki-index.sh --check` during validation

## Related Documents

- [LLM Wiki references](./README.md)
- [LLM Wiki repository map](./repository-map.md)
- [LLM Wiki maintenance guide](../../05.operations/guides/00-workspace/llm-wiki-maintenance.md)
- [Agent governance hub](../../00.agent-governance/README.md)
