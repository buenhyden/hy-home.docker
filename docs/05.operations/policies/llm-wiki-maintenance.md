---
status: active
---

# LLM Wiki Maintenance Operations Policy

## Overview (KR)

이 문서는 `hy-home.docker`의 repo-local LLM Wiki를 갱신하고 검증하는 운영 가이드다. LLM Wiki는 source contents를 합치는 문서가 아니라, LLM 에이전트가 안전하게 canonical path를 찾도록 돕는 index layer다.

## Policy Scope

이 가이드는 루트 `llms.txt`, `docs/90.references/llm-wiki/`, `scripts/knowledge/generate-llm-wiki-index.sh`, `wiki-curator` 역할의 운영 절차를 다룬다.

## Applies To

- **Systems**: `hy-home.docker` documentation and agent-governance surfaces
- **Agents**: `wiki-curator`, `doc-writer`, `workflow-supervisor`
- **Environments**: local repository worktree and CI validation

## Review Cadence

- Review when linked service configuration, architecture, or runbook behavior changes.

## Related Documents

- [Operations index](../README.md)
- [Usage guide](../guides/llm-wiki-maintenance.md)
- [Recovery runbook](../runbooks/llm-wiki-maintenance.md)
- [Operations template](../../99.templates/operation.template.md)
