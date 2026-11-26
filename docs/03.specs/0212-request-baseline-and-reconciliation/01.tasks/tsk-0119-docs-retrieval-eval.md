---
title: "Repository Docs Retrieval Evaluation Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-26"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0119"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-26"
---

# Repository Docs Retrieval Evaluation Task

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

Own criterion176/W192 in the [Spec](../spec.md) and [Plan](../plan.md): run
the reproducibility experiment criterion 70 deferred, as a retrieval
evaluation on this repository's own documents.

##### Inputs and Authority

On 2026-11-26 the owner, reviewing D06-T06 under the lifecycle v8 prompt
`06_ai_ollama_local_cloud_sandbox.md`, chose this evaluation over keeping
criterion 70 not-required, then chose BM25 plus hybrid fusion as the
baseline, Qdrant as the vector store and document structure as the query
source. SearXNG was dropped as a baseline because it searches the public
web, not these documents. TSK-0043 is completed, so criterion 70 keeps its
recorded not-required decision and this Task owns the new criterion176.
Work ran on branch `feat/docs-retrieval-eval` in
`.claude/worktrees/c70-eval` from `main` `c01fe08eb`; brief `c70-eval`
bound the paths before the first edit.

#### Execution Log

##### Work Performed

###### Change

- `scripts/lib/ops/docs_retrieval_eval.py`: `build` reads every
  `docs/**/*.md` at one commit through git, takes the frontmatter title as
  the query and the document as its answer, drops documents whose title is
  not unique (template placeholders), removes the title line and every line
  shared by at least 20% of documents, and stamps each document with the
  commit that first added it (`--no-renames`, so a move counts as an add).
  `run` embeds up to six 1200-character chunks per document with
  `embeddinggemma-2:740m` on local Ollama, indexes them in a throwaway
  Qdrant collection, ranks BM25, dense (best chunk per document) and
  reciprocal rank fusion, picks the fusion constant on the earlier 80% of
  documents, reports the later 20%, logs to the MLflow experiment
  `docs-retrieval-eval` and deletes the collection. The Qdrant key is read
  from a mounted file and never printed.
- The MLflow runbook (OPS-0088) gains the run procedure; it uses the running
  `mlflow` image, so no image is downloaded.
- Spec criterion176 and Plan W192 record the experiment.

###### Results

Corpus: 591 documents at `c01fe08eb` (created 2026-01-12 to 2026-11-25), 472
for tuning and 119 for testing, cutoff 2026-11-19 19:59 KST; the fusion
constant k=10 won on tuning. Test results:

| Method | recall@1 | recall@5 | recall@10 | MRR@10 |
| --- | --- | --- | --- | --- |
| BM25 | 0.294 | 0.739 | 0.815 | 0.472 |
| Dense (Qdrant, embeddinggemma) | 0.437 | 0.731 | 0.849 | 0.566 |
| Hybrid (RRF k=10) | 0.429 | 0.866 | 0.916 | 0.616 |

Tuning shows the same order (MRR@10 0.419, 0.567, 0.581). Dense retrieval
finds the exact document first more often; hybrid fusion keeps that and
places the answer in the top five or ten most often, so hybrid is the
candidate mode for Wiki preparation search. The run took 248 s and left no
`docs_eval_` collection behind.

###### Limits

Queries are document titles, a structural proxy, not human relevance
judgments; the answer set is one document per query. A moved document's
date is its move date. The time split orders queries; every query searches
the full corpus at the same commit, so the split guards the tuned constant,
not the index contents. The result does not adopt a product or change any
consumer.

##### Blockers and Decisions

Criterion 70 stays not-required in TSK-0043; this Task records the new
experiment under criterion176.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 176 | W192 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.ops.test_docs_retrieval_eval tests.lib.test_surface_ownership | Change on c01fe08eb | PASS | 8 behavior tests (parsing, boilerplate, ambiguous titles, time split, Korean BM25, fusion, metrics, chunks) and surface ownership OK | required | - |
| E02 | 176 | W192 | method=automated; tool=Python3 venv; command=check-script-manifest.py | Change on c01fe08eb | PASS | Manifest valid; the module is governed by the MLflow runbook | required | - |
| E03 | 176 | W192 | method=automated; tool=docker, mlflow image, Ollama, Qdrant, MLflow; command=docs_retrieval_eval build then run on ai_net | HOME, 2026-11-26, corpus c01fe08eb | PASS | 591 documents, MLflow run 0b373755ce9f4bf5803757c7342a69f6 in experiment docs-retrieval-eval; test MRR@10 BM25 0.472, dense 0.566, hybrid 0.616; no docs_eval_ collection left | required | - |

##### Resolution Links

None.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 176 | pending | E01,E02,E03 | The evaluation ran and is recorded; the owner decides acceptance | @buenhyden |

##### Remaining Conditions

Owner acceptance of criterion176.

#### Handoff

##### Promotion Receipt

The MLflow runbook carries the run procedure.

##### Next Owner

The owner decides acceptance and whether Wiki preparation search adopts
hybrid retrieval.

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
