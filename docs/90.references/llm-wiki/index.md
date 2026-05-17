---
status: active
generated_by: scripts/knowledge/generate-llm-wiki-index.sh
---

# Reference: LLM Wiki Generated Index

## Overview (KR)

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
| [docs/00.agent-governance/agents/agents/code-reviewer.md](../../00.agent-governance/agents/agents/code-reviewer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/doc-writer.md](../../00.agent-governance/agents/agents/doc-writer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/drift-detector.md](../../00.agent-governance/agents/agents/drift-detector.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/iac-reviewer.md](../../00.agent-governance/agents/agents/iac-reviewer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/incident-responder.md](../../00.agent-governance/agents/agents/incident-responder.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/infra-implementer.md](../../00.agent-governance/agents/agents/infra-implementer.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/security-auditor.md](../../00.agent-governance/agents/agents/security-auditor.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/wiki-curator.md](../../00.agent-governance/agents/agents/wiki-curator.md) | Markdown reference |
| [docs/00.agent-governance/agents/agents/workflow-supervisor.md](../../00.agent-governance/agents/agents/workflow-supervisor.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/adr-writing.md](../../00.agent-governance/agents/functions/adr-writing.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/ci-cd-patterns.md](../../00.agent-governance/agents/functions/ci-cd-patterns.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/code-review-dimensions.md](../../00.agent-governance/agents/functions/code-review-dimensions.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/code-reviewer.md](../../00.agent-governance/agents/functions/code-reviewer.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/container-threat-modeling.md](../../00.agent-governance/agents/functions/container-threat-modeling.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/docker-compose-patterns.md](../../00.agent-governance/agents/functions/docker-compose-patterns.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/incident-response.md](../../00.agent-governance/agents/functions/incident-response.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/infra-cross-validate.md](../../00.agent-governance/agents/functions/infra-cross-validate.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/infra-validate.md](../../00.agent-governance/agents/functions/infra-validate.md) | Markdown reference |
| [docs/00.agent-governance/agents/functions/security-audit.md](../../00.agent-governance/agents/functions/security-audit.md) | Markdown reference |
| [docs/00.agent-governance/memory/README.md](../../00.agent-governance/memory/README.md) | folder index |
| [docs/00.agent-governance/memory/agentic-harness-contract-hardening.md](../../00.agent-governance/memory/agentic-harness-contract-hardening.md) | Markdown reference |
| [docs/00.agent-governance/memory/docker-doc-contract-backlog.md](../../00.agent-governance/memory/docker-doc-contract-backlog.md) | Markdown reference |
| [docs/00.agent-governance/memory/github-ci-contract-audit.md](../../00.agent-governance/memory/github-ci-contract-audit.md) | Markdown reference |
| [docs/00.agent-governance/memory/governance-memory-usage-contract.md](../../00.agent-governance/memory/governance-memory-usage-contract.md) | Markdown reference |
| [docs/00.agent-governance/memory/harness-agent-first-gap-audit.md](../../00.agent-governance/memory/harness-agent-first-gap-audit.md) | Markdown reference |
| [docs/00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md) | Markdown reference |
| [docs/00.agent-governance/memory/template.md](../../00.agent-governance/memory/template.md) | Markdown reference |
| [docs/00.agent-governance/providers/agents-md.md](../../00.agent-governance/providers/agents-md.md) | Markdown reference |
| [docs/00.agent-governance/providers/claude.md](../../00.agent-governance/providers/claude.md) | Markdown reference |
| [docs/00.agent-governance/providers/codex.md](../../00.agent-governance/providers/codex.md) | Markdown reference |
| [docs/00.agent-governance/providers/gemini.md](../../00.agent-governance/providers/gemini.md) | Markdown reference |
| [docs/00.agent-governance/rules/agentic.md](../../00.agent-governance/rules/agentic.md) | Markdown reference |
| [docs/00.agent-governance/rules/bootstrap.md](../../00.agent-governance/rules/bootstrap.md) | Markdown reference |
| [docs/00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md) | Markdown reference |
| [docs/00.agent-governance/rules/git-workflow.md](../../00.agent-governance/rules/git-workflow.md) | Markdown reference |
| [docs/00.agent-governance/rules/github-governance.md](../../00.agent-governance/rules/github-governance.md) | Markdown reference |
| [docs/00.agent-governance/rules/persona.md](../../00.agent-governance/rules/persona.md) | Markdown reference |
| [docs/00.agent-governance/rules/postflight-checklist.md](../../00.agent-governance/rules/postflight-checklist.md) | Markdown reference |
| [docs/00.agent-governance/rules/quality-standards.md](../../00.agent-governance/rules/quality-standards.md) | Markdown reference |
| [docs/00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md) | Markdown reference |
| [docs/00.agent-governance/rules/standards.md](../../00.agent-governance/rules/standards.md) | Markdown reference |
| [docs/00.agent-governance/rules/task-checklists.md](../../00.agent-governance/rules/task-checklists.md) | Markdown reference |
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
| [.claude/agents/code-reviewer.md](../../../.claude/agents/code-reviewer.md) | Markdown reference |
| [.claude/agents/doc-writer.md](../../../.claude/agents/doc-writer.md) | Markdown reference |
| [.claude/agents/drift-detector.md](../../../.claude/agents/drift-detector.md) | Markdown reference |
| [.claude/agents/iac-reviewer.md](../../../.claude/agents/iac-reviewer.md) | Markdown reference |
| [.claude/agents/incident-responder.md](../../../.claude/agents/incident-responder.md) | Markdown reference |
| [.claude/agents/infra-implementer.md](../../../.claude/agents/infra-implementer.md) | Markdown reference |
| [.claude/agents/security-auditor.md](../../../.claude/agents/security-auditor.md) | Markdown reference |
| [.claude/agents/wiki-curator.md](../../../.claude/agents/wiki-curator.md) | Markdown reference |
| [.claude/agents/workflow-supervisor.md](../../../.claude/agents/workflow-supervisor.md) | Markdown reference |
| [.claude/hooks/docker-compose-pre.sh](../../../.claude/hooks/docker-compose-pre.sh) | script |
| [.claude/hooks/post-tool-validate.sh](../../../.claude/hooks/post-tool-validate.sh) | script |
| [.claude/hooks/session-start.sh](../../../.claude/hooks/session-start.sh) | script |
| [.claude/settings.json](../../../.claude/settings.json) | JSON registry |
| [.claude/skills/adr-writing/skill.md](../../../.claude/skills/adr-writing/skill.md) | Markdown reference |
| [.claude/skills/ci-cd-patterns/skill.md](../../../.claude/skills/ci-cd-patterns/skill.md) | Markdown reference |
| [.claude/skills/code-review-dimensions/skill.md](../../../.claude/skills/code-review-dimensions/skill.md) | Markdown reference |
| [.claude/skills/code-reviewer/skill.md](../../../.claude/skills/code-reviewer/skill.md) | Markdown reference |
| [.claude/skills/container-threat-modeling/skill.md](../../../.claude/skills/container-threat-modeling/skill.md) | Markdown reference |
| [.claude/skills/docker-compose-patterns/skill.md](../../../.claude/skills/docker-compose-patterns/skill.md) | Markdown reference |
| [.claude/skills/incident-response/skill.md](../../../.claude/skills/incident-response/skill.md) | Markdown reference |
| [.claude/skills/infra-cross-validate/skill.md](../../../.claude/skills/infra-cross-validate/skill.md) | Markdown reference |
| [.claude/skills/infra-validate/skill.md](../../../.claude/skills/infra-validate/skill.md) | Markdown reference |
| [.claude/skills/security-audit/skill.md](../../../.claude/skills/security-audit/skill.md) | Markdown reference |
| [.codex/README.md](../../../.codex/README.md) | folder index |
| [.codex/hooks.json](../../../.codex/hooks.json) | JSON registry |

### Active stage docs

| Path | Role |
| --- | --- |
| [docs/01.requirements/2026-03-26-01-gateway.md](../../01.requirements/2026-03-26-01-gateway.md) | Markdown reference |
| [docs/01.requirements/2026-03-26-02-auth.md](../../01.requirements/2026-03-26-02-auth.md) | Markdown reference |
| [docs/01.requirements/2026-03-26-03-security.md](../../01.requirements/2026-03-26-03-security.md) | Markdown reference |
| [docs/01.requirements/2026-03-26-04-data-analytics.md](../../01.requirements/2026-03-26-04-data-analytics.md) | Markdown reference |
| [docs/01.requirements/2026-03-26-04-data.md](../../01.requirements/2026-03-26-04-data.md) | Markdown reference |
| [docs/01.requirements/2026-03-26-05-messaging.md](../../01.requirements/2026-03-26-05-messaging.md) | Markdown reference |
| [docs/01.requirements/2026-03-26-06-observability.md](../../01.requirements/2026-03-26-06-observability.md) | Markdown reference |
| [docs/01.requirements/2026-03-26-07-workflow.md](../../01.requirements/2026-03-26-07-workflow.md) | Markdown reference |
| [docs/01.requirements/2026-03-26-08-ai.md](../../01.requirements/2026-03-26-08-ai.md) | Markdown reference |
| [docs/01.requirements/2026-03-26-09-tooling.md](../../01.requirements/2026-03-26-09-tooling.md) | Markdown reference |
| [docs/01.requirements/2026-03-26-10-communication.md](../../01.requirements/2026-03-26-10-communication.md) | Markdown reference |
| [docs/01.requirements/2026-03-26-11-laboratory.md](../../01.requirements/2026-03-26-11-laboratory.md) | Markdown reference |
| [docs/01.requirements/2026-03-27-08-ai-open-webui.md](../../01.requirements/2026-03-27-08-ai-open-webui.md) | Markdown reference |
| [docs/01.requirements/2026-03-28-02-auth-optimization-hardening.md](../../01.requirements/2026-03-28-02-auth-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/2026-03-28-03-security-optimization-hardening.md](../../01.requirements/2026-03-28-03-security-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/2026-03-28-04-data-optimization-hardening.md](../../01.requirements/2026-03-28-04-data-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/2026-03-28-05-messaging-optimization-hardening.md](../../01.requirements/2026-03-28-05-messaging-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/2026-03-28-06-observability-optimization-hardening.md](../../01.requirements/2026-03-28-06-observability-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/2026-03-28-07-workflow-optimization-hardening.md](../../01.requirements/2026-03-28-07-workflow-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/2026-03-28-08-ai-optimization-hardening.md](../../01.requirements/2026-03-28-08-ai-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/2026-03-28-09-tooling-optimization-hardening.md](../../01.requirements/2026-03-28-09-tooling-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/2026-03-28-11-laboratory-optimization-hardening.md](../../01.requirements/2026-03-28-11-laboratory-optimization-hardening.md) | Markdown reference |
| [docs/01.requirements/2026-04-01-standardize-infra-net.md](../../01.requirements/2026-04-01-standardize-infra-net.md) | Markdown reference |
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
| [docs/02.architecture/decisions/2026-04-01-standardize-infra-net.md](../../02.architecture/decisions/2026-04-01-standardize-infra-net.md) | Markdown reference |
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
| [docs/02.architecture/requirements/2026-04-01-standardize-infra-net.md](../../02.architecture/requirements/2026-04-01-standardize-infra-net.md) | Markdown reference |
| [docs/02.architecture/requirements/README.md](../../02.architecture/requirements/README.md) | folder index |
| [docs/03.specs/01-gateway/README.md](../../03.specs/01-gateway/README.md) | folder index |
| [docs/03.specs/01-gateway/spec.md](../../03.specs/01-gateway/spec.md) | Markdown reference |
| [docs/03.specs/02-auth/README.md](../../03.specs/02-auth/README.md) | folder index |
| [docs/03.specs/02-auth/spec.md](../../03.specs/02-auth/spec.md) | Markdown reference |
| [docs/03.specs/03-security/README.md](../../03.specs/03-security/README.md) | folder index |
| [docs/03.specs/03-security/spec.md](../../03.specs/03-security/spec.md) | Markdown reference |
| [docs/03.specs/04-data-analytics/README.md](../../03.specs/04-data-analytics/README.md) | folder index |
| [docs/03.specs/04-data-analytics/spec.md](../../03.specs/04-data-analytics/spec.md) | Markdown reference |
| [docs/03.specs/04-data/README.md](../../03.specs/04-data/README.md) | folder index |
| [docs/03.specs/04-data/spec.md](../../03.specs/04-data/spec.md) | Markdown reference |
| [docs/03.specs/05-messaging/README.md](../../03.specs/05-messaging/README.md) | folder index |
| [docs/03.specs/05-messaging/spec.md](../../03.specs/05-messaging/spec.md) | Markdown reference |
| [docs/03.specs/06-observability/README.md](../../03.specs/06-observability/README.md) | folder index |
| [docs/03.specs/06-observability/spec.md](../../03.specs/06-observability/spec.md) | Markdown reference |
| [docs/03.specs/07-workflow/README.md](../../03.specs/07-workflow/README.md) | folder index |
| [docs/03.specs/07-workflow/agent-design.md](../../03.specs/07-workflow/agent-design.md) | Markdown reference |
| [docs/03.specs/07-workflow/spec.md](../../03.specs/07-workflow/spec.md) | Markdown reference |
| [docs/03.specs/08-ai/README.md](../../03.specs/08-ai/README.md) | folder index |
| [docs/03.specs/08-ai/open-webui.md](../../03.specs/08-ai/open-webui.md) | Markdown reference |
| [docs/03.specs/08-ai/spec.md](../../03.specs/08-ai/spec.md) | Markdown reference |
| [docs/03.specs/09-tooling/README.md](../../03.specs/09-tooling/README.md) | folder index |
| [docs/03.specs/09-tooling/spec.md](../../03.specs/09-tooling/spec.md) | Markdown reference |
| [docs/03.specs/10-communication/README.md](../../03.specs/10-communication/README.md) | folder index |
| [docs/03.specs/10-communication/spec.md](../../03.specs/10-communication/spec.md) | Markdown reference |
| [docs/03.specs/11-laboratory/README.md](../../03.specs/11-laboratory/README.md) | folder index |
| [docs/03.specs/11-laboratory/spec.md](../../03.specs/11-laboratory/spec.md) | Markdown reference |
| [docs/03.specs/README.md](../../03.specs/README.md) | folder index |
| [docs/03.specs/docs-taxonomy-agent-first-migration/README.md](../../03.specs/docs-taxonomy-agent-first-migration/README.md) | folder index |
| [docs/03.specs/docs-taxonomy-agent-first-migration/spec.md](../../03.specs/docs-taxonomy-agent-first-migration/spec.md) | Markdown reference |
| [docs/03.specs/harness-agent-first-engineering/README.md](../../03.specs/harness-agent-first-engineering/README.md) | folder index |
| [docs/03.specs/harness-agent-first-engineering/spec.md](../../03.specs/harness-agent-first-engineering/spec.md) | Markdown reference |
| [docs/03.specs/infra-secrets-docs-refresh/README.md](../../03.specs/infra-secrets-docs-refresh/README.md) | folder index |
| [docs/03.specs/infra-secrets-docs-refresh/spec.md](../../03.specs/infra-secrets-docs-refresh/spec.md) | Markdown reference |
| [docs/03.specs/llm-wiki-agent-first-completion/README.md](../../03.specs/llm-wiki-agent-first-completion/README.md) | folder index |
| [docs/03.specs/llm-wiki-agent-first-completion/spec.md](../../03.specs/llm-wiki-agent-first-completion/spec.md) | Markdown reference |
| [docs/03.specs/standardize-infra-net/README.md](../../03.specs/standardize-infra-net/README.md) | folder index |
| [docs/03.specs/standardize-infra-net/spec.md](../../03.specs/standardize-infra-net/spec.md) | Markdown reference |
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
| [docs/04.execution/plans/2026-03-29-k8s-migration-strategy.md](../../04.execution/plans/2026-03-29-k8s-migration-strategy.md) | Markdown reference |
| [docs/04.execution/plans/2026-04-01-standardize-infra-net.md](../../04.execution/plans/2026-04-01-standardize-infra-net.md) | Markdown reference |
| [docs/04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md](../../04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-09-harness-agent-first-engineering.md](../../04.execution/plans/2026-05-09-harness-agent-first-engineering.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-09-infra-secrets-docs-refresh.md](../../04.execution/plans/2026-05-09-infra-secrets-docs-refresh.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md](../../04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-10-docs-taxonomy-agent-first-migration.md](../../04.execution/plans/2026-05-10-docs-taxonomy-agent-first-migration.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md](../../04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md) | Markdown reference |
| [docs/04.execution/plans/2026-05-17-scripts-ci-qa-cleanup.md](../../04.execution/plans/2026-05-17-scripts-ci-qa-cleanup.md) | Markdown reference |
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
| [docs/04.execution/tasks/2026-05-09-harness-agent-first-engineering.md](../../04.execution/tasks/2026-05-09-harness-agent-first-engineering.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md](../../04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-10-docs-taxonomy-agent-first-migration.md](../../04.execution/tasks/2026-05-10-docs-taxonomy-agent-first-migration.md) | Markdown reference |
| [docs/04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md](../../04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md) | Markdown reference |
| [docs/04.execution/tasks/README.md](../../04.execution/tasks/README.md) | folder index |

### Operations docs

| Path | Role |
| --- | --- |
| [docs/05.operations/README.md](../../05.operations/README.md) | folder index |
| [docs/05.operations/guides/0012-standardize-infra-net.md](../../05.operations/guides/0012-standardize-infra-net.md) | Markdown reference |
| [docs/05.operations/guides/01-gateway/01.setup.md](../../05.operations/guides/01-gateway/01.setup.md) | Markdown reference |
| [docs/05.operations/guides/01-gateway/README.md](../../05.operations/guides/01-gateway/README.md) | folder index |
| [docs/05.operations/guides/01-gateway/nginx.md](../../05.operations/guides/01-gateway/nginx.md) | Markdown reference |
| [docs/05.operations/guides/01-gateway/traefik.md](../../05.operations/guides/01-gateway/traefik.md) | Markdown reference |
| [docs/05.operations/guides/02-auth/README.md](../../05.operations/guides/02-auth/README.md) | folder index |
| [docs/05.operations/guides/02-auth/keycloak.md](../../05.operations/guides/02-auth/keycloak.md) | Markdown reference |
| [docs/05.operations/guides/02-auth/oauth2-proxy.md](../../05.operations/guides/02-auth/oauth2-proxy.md) | Markdown reference |
| [docs/05.operations/guides/03-security/01.setup.md](../../05.operations/guides/03-security/01.setup.md) | Markdown reference |
| [docs/05.operations/guides/03-security/README.md](../../05.operations/guides/03-security/README.md) | folder index |
| [docs/05.operations/guides/03-security/vault.md](../../05.operations/guides/03-security/vault.md) | Markdown reference |
| [docs/05.operations/guides/04-data/01.relational-dbs.md](../../05.operations/guides/04-data/01.relational-dbs.md) | Markdown reference |
| [docs/05.operations/guides/04-data/02.cache-kv-dbs.md](../../05.operations/guides/04-data/02.cache-kv-dbs.md) | Markdown reference |
| [docs/05.operations/guides/04-data/04.storage-systems.md](../../05.operations/guides/04-data/04.storage-systems.md) | Markdown reference |
| [docs/05.operations/guides/04-data/05.analytical-specialized-dbs.md](../../05.operations/guides/04-data/05.analytical-specialized-dbs.md) | Markdown reference |
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
| [docs/05.operations/guides/04-data/optimization-hardening.md](../../05.operations/guides/04-data/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/guides/04-data/relational.md](../../05.operations/guides/04-data/relational.md) | Markdown reference |
| [docs/05.operations/guides/04-data/relational/README.md](../../05.operations/guides/04-data/relational/README.md) | folder index |
| [docs/05.operations/guides/04-data/relational/postgresql-cluster.md](../../05.operations/guides/04-data/relational/postgresql-cluster.md) | Markdown reference |
| [docs/05.operations/guides/04-data/specialized/README.md](../../05.operations/guides/04-data/specialized/README.md) | folder index |
| [docs/05.operations/guides/04-data/specialized/neo4j.md](../../05.operations/guides/04-data/specialized/neo4j.md) | Markdown reference |
| [docs/05.operations/guides/04-data/specialized/qdrant.md](../../05.operations/guides/04-data/specialized/qdrant.md) | Markdown reference |
| [docs/05.operations/guides/04-data/valkey-cluster.md](../../05.operations/guides/04-data/valkey-cluster.md) | Markdown reference |
| [docs/05.operations/guides/05-messaging/03.ksql-streaming.md](../../05.operations/guides/05-messaging/03.ksql-streaming.md) | Markdown reference |
| [docs/05.operations/guides/05-messaging/README.md](../../05.operations/guides/05-messaging/README.md) | folder index |
| [docs/05.operations/guides/05-messaging/kafka.md](../../05.operations/guides/05-messaging/kafka.md) | Markdown reference |
| [docs/05.operations/guides/05-messaging/optimization-hardening.md](../../05.operations/guides/05-messaging/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/guides/05-messaging/rabbitmq.md](../../05.operations/guides/05-messaging/rabbitmq.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/01.lgtm-stack.md](../../05.operations/guides/06-observability/01.lgtm-stack.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/README.md](../../05.operations/guides/06-observability/README.md) | folder index |
| [docs/05.operations/guides/06-observability/alertmanager.md](../../05.operations/guides/06-observability/alertmanager.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/alloy.md](../../05.operations/guides/06-observability/alloy.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/grafana.md](../../05.operations/guides/06-observability/grafana.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/loki.md](../../05.operations/guides/06-observability/loki.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/optimization-hardening.md](../../05.operations/guides/06-observability/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/prometheus.md](../../05.operations/guides/06-observability/prometheus.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/pushgateway.md](../../05.operations/guides/06-observability/pushgateway.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/pyroscope.md](../../05.operations/guides/06-observability/pyroscope.md) | Markdown reference |
| [docs/05.operations/guides/06-observability/tempo.md](../../05.operations/guides/06-observability/tempo.md) | Markdown reference |
| [docs/05.operations/guides/07-workflow/01.airflow-dag-dev.md](../../05.operations/guides/07-workflow/01.airflow-dag-dev.md) | Markdown reference |
| [docs/05.operations/guides/07-workflow/01.dag-deployment.md](../../05.operations/guides/07-workflow/01.dag-deployment.md) | Markdown reference |
| [docs/05.operations/guides/07-workflow/02.n8n-automation.md](../../05.operations/guides/07-workflow/02.n8n-automation.md) | Markdown reference |
| [docs/05.operations/guides/07-workflow/README.md](../../05.operations/guides/07-workflow/README.md) | folder index |
| [docs/05.operations/guides/07-workflow/airbyte.md](../../05.operations/guides/07-workflow/airbyte.md) | Markdown reference |
| [docs/05.operations/guides/07-workflow/airflow-dag-basics.md](../../05.operations/guides/07-workflow/airflow-dag-basics.md) | Markdown reference |
| [docs/05.operations/guides/07-workflow/airflow.md](../../05.operations/guides/07-workflow/airflow.md) | Markdown reference |
| [docs/05.operations/guides/07-workflow/n8n.md](../../05.operations/guides/07-workflow/n8n.md) | Markdown reference |
| [docs/05.operations/guides/07-workflow/optimization-hardening.md](../../05.operations/guides/07-workflow/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/guides/08-ai/01.llm-inference.md](../../05.operations/guides/08-ai/01.llm-inference.md) | Markdown reference |
| [docs/05.operations/guides/08-ai/02.rag-workflow.md](../../05.operations/guides/08-ai/02.rag-workflow.md) | Markdown reference |
| [docs/05.operations/guides/08-ai/README.md](../../05.operations/guides/08-ai/README.md) | folder index |
| [docs/05.operations/guides/08-ai/local-llm-setup.md](../../05.operations/guides/08-ai/local-llm-setup.md) | Markdown reference |
| [docs/05.operations/guides/08-ai/ollama.md](../../05.operations/guides/08-ai/ollama.md) | Markdown reference |
| [docs/05.operations/guides/08-ai/open-webui.md](../../05.operations/guides/08-ai/open-webui.md) | Markdown reference |
| [docs/05.operations/guides/08-ai/optimization-hardening.md](../../05.operations/guides/08-ai/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/guides/09-tooling/01.iac-automation.md](../../05.operations/guides/09-tooling/01.iac-automation.md) | Markdown reference |
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
| [docs/05.operations/guides/README.md](../../05.operations/guides/README.md) | folder index |
| [docs/05.operations/guides/developer-setup.md](../../05.operations/guides/developer-setup.md) | Markdown reference |
| [docs/05.operations/guides/harness-agent-first-engineering.md](../../05.operations/guides/harness-agent-first-engineering.md) | Markdown reference |
| [docs/05.operations/guides/llm-wiki-maintenance.md](../../05.operations/guides/llm-wiki-maintenance.md) | Markdown reference |
| [docs/05.operations/incidents/README.md](../../05.operations/incidents/README.md) | folder index |
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
| [docs/05.operations/policies/04-data/backup-policy.md](../../05.operations/policies/04-data/backup-policy.md) | Markdown reference |
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
| [docs/05.operations/policies/04-data/optimization-hardening.md](../../05.operations/policies/04-data/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/policies/04-data/relational.md](../../05.operations/policies/04-data/relational.md) | Markdown reference |
| [docs/05.operations/policies/04-data/relational/README.md](../../05.operations/policies/04-data/relational/README.md) | folder index |
| [docs/05.operations/policies/04-data/relational/postgresql-cluster.md](../../05.operations/policies/04-data/relational/postgresql-cluster.md) | Markdown reference |
| [docs/05.operations/policies/04-data/specialized/README.md](../../05.operations/policies/04-data/specialized/README.md) | folder index |
| [docs/05.operations/policies/04-data/specialized/neo4j.md](../../05.operations/policies/04-data/specialized/neo4j.md) | Markdown reference |
| [docs/05.operations/policies/04-data/specialized/qdrant.md](../../05.operations/policies/04-data/specialized/qdrant.md) | Markdown reference |
| [docs/05.operations/policies/04-data/valkey-cluster.md](../../05.operations/policies/04-data/valkey-cluster.md) | Markdown reference |
| [docs/05.operations/policies/05-messaging/README.md](../../05.operations/policies/05-messaging/README.md) | folder index |
| [docs/05.operations/policies/05-messaging/kafka.md](../../05.operations/policies/05-messaging/kafka.md) | Markdown reference |
| [docs/05.operations/policies/05-messaging/optimization-hardening.md](../../05.operations/policies/05-messaging/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/policies/05-messaging/rabbitmq.md](../../05.operations/policies/05-messaging/rabbitmq.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/01.retention.md](../../05.operations/policies/06-observability/01.retention.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/README.md](../../05.operations/policies/06-observability/README.md) | folder index |
| [docs/05.operations/policies/06-observability/alertmanager.md](../../05.operations/policies/06-observability/alertmanager.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/alloy.md](../../05.operations/policies/06-observability/alloy.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/grafana.md](../../05.operations/policies/06-observability/grafana.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/loki.md](../../05.operations/policies/06-observability/loki.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/optimization-hardening.md](../../05.operations/policies/06-observability/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/prometheus.md](../../05.operations/policies/06-observability/prometheus.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/pushgateway.md](../../05.operations/policies/06-observability/pushgateway.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/pyroscope.md](../../05.operations/policies/06-observability/pyroscope.md) | Markdown reference |
| [docs/05.operations/policies/06-observability/tempo.md](../../05.operations/policies/06-observability/tempo.md) | Markdown reference |
| [docs/05.operations/policies/07-workflow/README.md](../../05.operations/policies/07-workflow/README.md) | folder index |
| [docs/05.operations/policies/07-workflow/airbyte.md](../../05.operations/policies/07-workflow/airbyte.md) | Markdown reference |
| [docs/05.operations/policies/07-workflow/airflow.md](../../05.operations/policies/07-workflow/airflow.md) | Markdown reference |
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
| [docs/05.operations/policies/12-infra-service-optimization-catalog.md](../../05.operations/policies/12-infra-service-optimization-catalog.md) | Markdown reference |
| [docs/05.operations/policies/13-common-optimizations-template-exceptions.md](../../05.operations/policies/13-common-optimizations-template-exceptions.md) | Markdown reference |
| [docs/05.operations/policies/README.md](../../05.operations/policies/README.md) | folder index |
| [docs/05.operations/policies/harness-agent-first-engineering.md](../../05.operations/policies/harness-agent-first-engineering.md) | Markdown reference |
| [docs/05.operations/policies/llm-wiki-maintenance.md](../../05.operations/policies/llm-wiki-maintenance.md) | Markdown reference |
| [docs/05.operations/policies/standardize-infra-net.md](../../05.operations/policies/standardize-infra-net.md) | Markdown reference |
| [docs/05.operations/runbooks/0012-standardize-infra-net.md](../../05.operations/runbooks/0012-standardize-infra-net.md) | Markdown reference |
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
| [docs/05.operations/runbooks/04-data/optimization-hardening.md](../../05.operations/runbooks/04-data/optimization-hardening.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/relational.md](../../05.operations/runbooks/04-data/relational.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/relational/README.md](../../05.operations/runbooks/04-data/relational/README.md) | folder index |
| [docs/05.operations/runbooks/04-data/relational/postgresql-cluster.md](../../05.operations/runbooks/04-data/relational/postgresql-cluster.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/specialized/README.md](../../05.operations/runbooks/04-data/specialized/README.md) | folder index |
| [docs/05.operations/runbooks/04-data/specialized/neo4j.md](../../05.operations/runbooks/04-data/specialized/neo4j.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/specialized/qdrant.md](../../05.operations/runbooks/04-data/specialized/qdrant.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/storage-exhaustion.md](../../05.operations/runbooks/04-data/storage-exhaustion.md) | Markdown reference |
| [docs/05.operations/runbooks/04-data/valkey-cluster.md](../../05.operations/runbooks/04-data/valkey-cluster.md) | Markdown reference |
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
| [docs/05.operations/runbooks/06-observability/prometheus-recovery.md](../../05.operations/runbooks/06-observability/prometheus-recovery.md) | Markdown reference |
| [docs/05.operations/runbooks/06-observability/prometheus.md](../../05.operations/runbooks/06-observability/prometheus.md) | Markdown reference |
| [docs/05.operations/runbooks/06-observability/pushgateway.md](../../05.operations/runbooks/06-observability/pushgateway.md) | Markdown reference |
| [docs/05.operations/runbooks/06-observability/pyroscope.md](../../05.operations/runbooks/06-observability/pyroscope.md) | Markdown reference |
| [docs/05.operations/runbooks/06-observability/tempo.md](../../05.operations/runbooks/06-observability/tempo.md) | Markdown reference |
| [docs/05.operations/runbooks/07-workflow/README.md](../../05.operations/runbooks/07-workflow/README.md) | folder index |
| [docs/05.operations/runbooks/07-workflow/airbyte.md](../../05.operations/runbooks/07-workflow/airbyte.md) | Markdown reference |
| [docs/05.operations/runbooks/07-workflow/airflow-worker-recovery.md](../../05.operations/runbooks/07-workflow/airflow-worker-recovery.md) | Markdown reference |
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
| [docs/05.operations/runbooks/README.md](../../05.operations/runbooks/README.md) | folder index |
| [docs/05.operations/runbooks/harness-agent-first-engineering-validation.md](../../05.operations/runbooks/harness-agent-first-engineering-validation.md) | Markdown reference |
| [docs/05.operations/runbooks/llm-wiki-maintenance.md](../../05.operations/runbooks/llm-wiki-maintenance.md) | Markdown reference |

### Reference and template docs

| Path | Role |
| --- | --- |
| [docs/90.references/README.md](../README.md) | folder index |
| [docs/90.references/docker/README.md](../docker/README.md) | folder index |
| [docs/90.references/learning/README.md](../learning/README.md) | folder index |
| [docs/90.references/learning/roadmap-v1.md](../learning/roadmap-v1.md) | Markdown reference |
| [docs/90.references/learning/roadmap.md](../learning/roadmap.md) | Markdown reference |
| [docs/99.templates/README.md](../../99.templates/README.md) | folder index |
| [docs/99.templates/adr.template.md](../../99.templates/adr.template.md) | Markdown reference |
| [docs/99.templates/agent-design.template.md](../../99.templates/agent-design.template.md) | Markdown reference |
| [docs/99.templates/api-spec.template.md](../../99.templates/api-spec.template.md) | Markdown reference |
| [docs/99.templates/ard.template.md](../../99.templates/ard.template.md) | Markdown reference |
| [docs/99.templates/data-model.template.md](../../99.templates/data-model.template.md) | Markdown reference |
| [docs/99.templates/incident.template.md](../../99.templates/incident.template.md) | Markdown reference |
| [docs/99.templates/memory.template.md](../../99.templates/memory.template.md) | Markdown reference |
| [docs/99.templates/openapi.template.yaml](../../99.templates/openapi.template.yaml) | YAML config |
| [docs/99.templates/operation.template.md](../../99.templates/operation.template.md) | Markdown reference |
| [docs/99.templates/plan.template.md](../../99.templates/plan.template.md) | Markdown reference |
| [docs/99.templates/postmortem.template.md](../../99.templates/postmortem.template.md) | Markdown reference |
| [docs/99.templates/prd.template.md](../../99.templates/prd.template.md) | Markdown reference |
| [docs/99.templates/progress.template.md](../../99.templates/progress.template.md) | Markdown reference |
| [docs/99.templates/readme.template.md](../../99.templates/readme.template.md) | Markdown reference |
| [docs/99.templates/reference.template.md](../../99.templates/reference.template.md) | Markdown reference |
| [docs/99.templates/schema.template.graphql](../../99.templates/schema.template.graphql) | source path |
| [docs/99.templates/service.template.proto](../../99.templates/service.template.proto) | source path |
| [docs/99.templates/spec.template.md](../../99.templates/spec.template.md) | Markdown reference |
| [docs/99.templates/task.template.md](../../99.templates/task.template.md) | Markdown reference |
| [docs/99.templates/tests.template.md](../../99.templates/tests.template.md) | Markdown reference |
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
| [scripts/hooks/post-tool-validate.sh](../../../scripts/hooks/post-tool-validate.sh) | script |
| [scripts/knowledge/generate-llm-wiki-index.sh](../../../scripts/knowledge/generate-llm-wiki-index.sh) | script |
| [scripts/knowledge/report-graphify-health.sh](../../../scripts/knowledge/report-graphify-health.sh) | script |
| [scripts/lib/hardening-lib.sh](../../../scripts/lib/hardening-lib.sh) | script |
| [scripts/operations/gen-secrets.sh](../../../scripts/operations/gen-secrets.sh) | script |
| [scripts/validation/check-doc-traceability.sh](../../../scripts/validation/check-doc-traceability.sh) | script |
| [scripts/validation/check-quickwin-baseline.sh](../../../scripts/validation/check-quickwin-baseline.sh) | script |
| [scripts/validation/check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) | script |
| [scripts/validation/check-template-security-baseline.sh](../../../scripts/validation/check-template-security-baseline.sh) | script |
| [scripts/validation/validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh) | script |

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

### Secret-handling policy

| Path | Role |
| --- | --- |
| [secrets/README.md](../../../secrets/README.md) | folder index |

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
- [LLM Wiki maintenance guide](../../05.operations/guides/llm-wiki-maintenance.md)
- [Agent governance hub](../../00.agent-governance/README.md)
