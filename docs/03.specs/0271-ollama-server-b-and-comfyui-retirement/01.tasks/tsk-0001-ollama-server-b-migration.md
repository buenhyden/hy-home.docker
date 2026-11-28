---
title: 'Ollama Server B Migration Task'
version: 0.1.0
type: sdlc/task
status: draft
owner: '@buenhyden'
document_scope:
  subject: 'hy-home.docker'
  layer: workspace
document_lifecycle: draft
updated: '2026-11-28'
layer: specs
artifact_id: 'SPEC-0271-TSK-0001'
parent_ids:
- 'SPEC-0271-PLAN-0001'
created: '2026-11-28'
---

# Ollama Server B Migration Task

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

Own W1 to W7 of the [Plan](../plan.md) for [SPEC-0271](../spec.md) and decide AC-0001 to AC-0005.

##### Inputs and Authority

On 2026-11-28 the user asked in this chat to remove the HOME Ollama, use the Ollama on 192.168.0.22 from OpenClaw and every HOME consumer, review what was set up on 192.168.0.22, keep Ollama and ComfyUI only as Stage 05 documents, and remove the ComfyUI configuration and Dockerfile. Asked here, the user chose LAN access limited by the Windows firewall, OpenClaw on both servers, deleting ComfyUI data after removal, the models `embeddinggemma-2:740m-q8_0`, `gemma4:e2b` and `tev1:0.8b-q8_0` with `lfm2.5:8b`, `d1:3b`, `tev1:0.8b` and `minicpm-v4.6:1b` removed, and approved the plan. Brief `ollama-server-b` binds each change. Direct user authorization is authority; this record is not.

#### Execution Log

##### Work Performed

- Discovery on server A: HOME `ollama` 0.40.18 with eight models (25.1 GB); consumers `n8n-worker` (internal `n8n_ollama_net`), Open Notebook, docs eval, LAB Open WebUI, Hermes `lfm` alias on `127.0.0.1:11434`; OpenClaw on server A has no Ollama provider. Server B already runs Ollama 0.40.19 reachable from server A.
- W1 drafted: ADR-0064, this package and the registry allocation.

##### Blockers and Decisions

- The Spec and Plan are drafts in this first change; the owner's approval is recorded when they move to `approved`.
- W3 waits for E01: `gemma4:e2b` and `tev1:0.8b-q8_0` must be pulled on server B.
- Hermes's `lfm` alias points at `lfm2.5:8b`, which leaves service; it moves to `gemma4:e2b` in W4 unless the owner decides otherwise.

#### Verification Evidence

##### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | AC-0001 | W2 | observation | Server B from server A, 2026-11-28 | curl | `GET http://192.168.0.22:11434/api/version` and `/api/tags` | 0 | FAIL | Ollama 0.40.19 answers; `embeddinggemma-2:740m-q8_0`, `gemma4:e4b`, `bonsai-2:9b`, `mimo-v2.6:9b` present; `gemma4:e2b` and `tev1:0.8b-q8_0` missing | true | - |
| E02 | AC-0002 | W3 | automated | Server A and server B Ollama, 2026-11-28 | Python 3 urllib | `POST /api/embed` model `embeddinggemma-2:740m` on both hosts for three inputs (English, English, Korean); cosine of the 768-dimension vectors | 0 | PASS | Same digest `f4981a15b998` on both; cosine 0.999916, 0.999909, 0.99994 | true | - |

##### Resolution Links

E01 is resolved by a later C-01 row after the model pulls.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC-0001 | accept | pending | E01 | - | - | @buenhyden | - |
| AC-0002 | accept | pending | E02 | - | - | @buenhyden | - |
| AC-0003 | accept | pending | - | - | - | @buenhyden | - |
| AC-0004 | accept | pending | - | - | - | @buenhyden | - |
| AC-0005 | accept | pending | - | - | - | @buenhyden | - |

##### Remaining Conditions

W1 to W7 as planned.

#### Handoff

##### Promotion Receipt

None yet.

##### Next Owner

@buenhyden pulls `gemma4:e2b` and `tev1:0.8b-q8_0` on server B and applies the firewall rule; the agent continues W1 to W3.

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
