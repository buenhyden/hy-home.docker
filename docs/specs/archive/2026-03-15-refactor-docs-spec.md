---
layer: agentic
---

# Documentation Refactor Technical Specification

n**Overview (KR):** 기존 기술 문서의 분류 체계 재정립 및 구문 최적화 작업을 위한 명세입니다.

> **Parent PRD**: `[../prd/2026-03-15-refactor-docs-prd.md]`
> **Architecture Reference**: `[../ard/2026-03-15-doc-taxonomy-ard.md]`

**Overview (KR):** 이 명세서는 문서 재구성 작업의 기술적 구현 세부 사항을 정의합니다. 메타데이터 형식, 에이전트 지침 격리, 그리고 지연 로딩 시스템의 작동 방식을 설명합니다.

## 1. Metadata Schema

Every Markdown file must start with a YAML frontmatter block:

```yaml
---
layer: <layer_name>
---
```

Valid layers: `common | architecture | backend | frontend | infra | mobile | product | qa | security | entry | meta | ops | agentic`.

## 2. Agent Workflow Logic

Agents are instructed via `docs/agentic/instructions.md` to follow this sequence:

1. Start: Read `docs/agentic/gateway.md`.
2. Discover: Locate the index `README.md` for the relevant category.
3. Load: Read only the specific files found in step 2.

## 3. Directory Realignment

| Category | Folder Path | Purpose |
| --- | --- | --- |
| Decision | `docs/adr/` | Architectural decisions (ADRs) |
| Requirement | `docs/ard/` | Architectural requirements (ARDs) |
| Product | `docs/prd/` | Feature requirements (PRDs) |
| Tech Spec | `docs/specs/` | Implementation details |
| Plan | `docs/plans/` | Execution steps |
| Procedure | `docs/runbooks/` | Operational manuals |
| History | `docs/operations/` | Incidents and postmortems |

## 4. Skills Utilized

- `agent-md-refactor`: For systematic splitting of monolithic files.
- `claude-md-improver`: For qualitative content checking.
- `doc-coauthoring`: For generating complex PRDs/ARDs interactively.

## 5. Acceptance Tests

- `rg "layer:" docs/` must return a match for 100% of files.
- All links in `gateway.md` must resolve to valid README files.
- `docs/agentic/core-governance.md` must link to the new taxonomy paths.
