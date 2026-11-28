---
title: "Qdrant and Ollama Embedding Contract Task"
version: "0.2.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0127"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-28"
---

# Qdrant and Ollama Embedding Contract Task

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Objective and Parent

Own criterion184/W200 in the [Spec](../spec.md) and [Plan](../plan.md): make
the HOME client that embeds with Ollama and writes to Qdrant follow the
[Qdrant Ollama embedding guide](https://qdrant.tech/documentation/embeddings/ollama/)
and document that contract and its consumer.

##### Inputs and Authority

On 2026-11-28 the user asked, in this chat, to organize the Qdrant and Ollama
integration with that guide. Work ran in the primary checkout on branch
`feat/qdrant-ollama-embedding-contract` from `main` `d42dac611`; brief
`qdrant-ollama` bound this Task, the Spec and Plan rows, the eval script and
test, and the four operations documents. No secret value was read or printed,
and no Qdrant collection or Ollama model was changed. Direct user
authorization is authority; this record is not.

#### Execution Log

##### Work Performed

###### Findings

| Item | Guide | HOME before | Change |
| --- | --- | --- | --- |
| Pattern | The client embeds with Ollama and writes to Qdrant; Qdrant never calls Ollama | Same | Documented in the Qdrant guide |
| Endpoint | `/api/embed` with an input list; `/api/embeddings` is deprecated | `docs_retrieval_eval.py` already uses `/api/embed` | None |
| Distance and size | Cosine; collection size equals the model dimension | Cosine, size from the first vector (768 for `embeddinggemma-2:740m`) | Documented |
| Task prompts | Ollama adds none; `embeddinggemma-2` needs `task: search result \| query: {query}` and `title: none \| text: {document}` | Missing | `prompted()` adds them per model family (also qwen3-embedding and nomic-embed-text) |
| Long input | Truncated silently unless `truncate: false` | Default | The eval sends `truncate: false` |
| Consumers | - | Only the docs retrieval eval; no n8n workflow has a Qdrant or Ollama-embedding node, and n8n and n8n-worker are not on `ai_net` | The Qdrant README consumer cell and the AI README row, which claimed n8n handles HOME RAG, are corrected |

Earlier MLflow `docs-retrieval-eval` dense and hybrid runs used unprompted
input; the MLflow runbook now says they are not directly comparable.

###### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0127 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0127 | ready | in-progress | #work-performed |
| SPEC-0212-TSK-0127 | in-progress | completed | #criterion-decisions |

##### Blockers and Decisions

None. Changing the default embedding model, adding a RAG consumer or a
persistent collection is out of this scope.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 184 | W200 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.ops.test_docs_retrieval_eval | New prompt test before the change | FAIL | `prompted` missing | required | - |
| E02 | 184 | W200 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.ops.test_docs_retrieval_eval | After the change | PASS | 9 tests OK; ruff check and format pass | required | E01 |
| E03 | 184 | W200 | method=observation; tool=wget on ai_net; command=POST /api/embed with prompted query and document inputs and truncate false | Ollama 0.40.18, `embeddinggemma-2:740m` | PASS | Both returned embeddings | required | - |
| E04 | 184 | W200 | method=observation; tool=psql; command=n8n workflow node types matching qdrant, embeddingsOllama or vectorStore | n8n DB, 2026-11-28 | PASS | No match | required | - |

##### Resolution Links

E02 resolves E01.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 184 | accepted | E01,E02,E03,E04 | Owner @buenhyden accepted on 2026-11-28 in this chat after PR #1296 merged | @buenhyden |

##### Remaining Conditions

None.

#### Handoff

##### Promotion Receipt

The contract is promoted to the Qdrant guide (GDE-0034) and the MLflow
runbook.

##### Next Owner

None; criterion184 is accepted and this Task is completed. The next
`docs-retrieval-eval` run records the prompted baseline. No other prompt is
started automatically.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
