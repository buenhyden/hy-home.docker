---
profile_id: policy
status: active
artifact_id: policy-0007
artifact_type: policy
parent_ids:
  - SPEC-0096
created: 2026-07-04
updated: 2026-08-11
---

# LLM Wiki Maintenance Operations Policy

## Overview

이 문서는 `hy-home.docker`의 repo-local LLM Wiki를 갱신하고 검증하는 운영 가이드다. LLM Wiki는 source contents를 합치는 문서가 아니라, LLM 에이전트가 안전하게 canonical path를 찾도록 돕는 index layer다.

## Policy Scope

이 가이드는 루트 `llms.txt`, `docs/90.references/data/0082-llm-wiki-index/`, `scripts/knowledge/generate-llm-wiki.py`, `doc-writer` 역할과 `knowledge-map-agent` 함수의 운영 절차를 다룬다.

- **Systems**: `hy-home.docker` documentation and agent-governance surfaces
- **Agents**: `doc-writer`, `workflow-supervisor`
- **Environments**: local repository worktree and CI validation

## Controls

- **Required**: Generated LLM Wiki output must be refreshed after root entrypoints, governance docs, operations docs, script inventory, infrastructure indexes, or LLM Wiki source files change.
- **Allowed**: Graphify output may be used as advisory navigation context when corroborated against tracked source files.
- **Disallowed**: Do not include secret values, runtime volume contents, generated dependency artifacts, or Graphify output as authoritative source material.

## Exceptions

- Exceptions require explicit user approval and must record why the existing generated index or repository map cannot cover the navigation need.
- Do not add runtime hooks for LLM Wiki refresh unless a later task establishes a concrete failure mode that post-tool validation cannot catch.

## Verification

- `python3 scripts/knowledge/generate-llm-wiki.py --check`
- `bash scripts/validation/check-repo-contracts.sh`
- `python3 scripts/validation/check-document-links.py --mode traceability`

## Review Cadence

- Review when linked service configuration, architecture, or runbook behavior changes.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
