---
title: '2026-03 Documentation Taxonomy and Agentic Framework ARD'
status: 'Accepted'
date: '2026-03-15'
scope: 'master'
layer: architecture
---

# 2026-03 Documentation Taxonomy and Agentic Framework ARD

**Overview (KR):** 본 문서는 2026년 3월 기준의 문서 분류 체계와 AI 에이전트 프레임워크 표준을 정의합니다. 모든 문서는 메타데이터를 포함해야 하며, 에이전트 진입점은 경량화된 트리거 형태로 구성됩니다.

## 1. Vision & Goals

Ensure a high-discovery, low-context-bloat documentation ecosystem where AI agents and human operators can navigate the multi-tier infrastructure efficiently.

- **Flat Taxonomy**: Type-first directory structure under `docs/`.
- **Metadata Compliance**: 100% usage of `layer:` key in frontmatter.
- **Lazy Loading**: Intent-based rule triggers in root `.md` files.

## 2. Requirements

- **[REQ-ARD-DOC-01]** All ADRs must reside in `docs/adr/`.
- **[REQ-ARD-DOC-02]** All ARDs must reside in `docs/ard/`.
- **[REQ-ARD-DOC-03]** All Implementation Plans must reside in `docs/plans/`.
- **[REQ-ARD-DOC-04]** All files must contain `layer: <layer>` metadata.
- **[REQ-ARD-AGT-01]** `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` must be lightweight triggers.
- **[REQ-ARD-AGT-02]** Full Skill Autonomy must be explicitly granted but governed by behavioral instructions.

## 3. Success Criteria

- Successful `docker compose config` validation.
- All documentation links are relative and functional.
- Zero "restricted skills" messages in agent entrypoints.

## Related

- [../adr/README.md]
- [../prd/README.md]
