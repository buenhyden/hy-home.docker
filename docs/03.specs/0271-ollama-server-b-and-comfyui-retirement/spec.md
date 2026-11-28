---
title: 'Ollama on Server B and ComfyUI Retirement'
version: 0.1.0
type: sdlc/spec
status: draft
owner: '@buenhyden'
document_scope:
  subject: 'hy-home.docker'
  layer: workspace
updated: '2026-11-28'
layer: specs
artifact_id: 'SPEC-0271'
parent_ids:
- 'REQ-0009'
- 'AD-0008'
- 'ADR-0064'
created: '2026-11-28'
---

# Ollama on Server B and ComfyUI Retirement

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the spec payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Overview

##### Goal

Move LAN model inference from the HOME `ollama` container on server A (GTX 1060 6 GB) to the native Ollama on server B (192.168.0.22, RTX 4060 8 GB), point every consumer at it, and retire the HOME `ollama`, `ollama-exporter` and `comfyui` services, as [ADR-0064](../../02.architecture/02.decisions/0064-ollama-on-server-b.md) decides. It makes REQ-0009-FR-0001 and FR-0002 concrete on the new host within [AD-0008](../../02.architecture/01.descriptions/0008-ai-architecture.md).

##### Consumers

HOME services `n8n-worker` and Open Notebook, the docs retrieval eval, the LAB Open WebUI endpoint, host programs on server A (Hermes, OpenClaw), programs on server B (OpenClaw, blog-data), the operator who runs server B, and the Stage 05 Ollama and ComfyUI documents.

#### Scope

##### In Scope

- Server B Ollama settings, firewall rule and models, documented in Stage 05 and applied by the owner.
- Every HOME and server A consumer's endpoint and model names.
- Server B callers' endpoint and the retirement of the `ollama-api` route, its credentials and the server B loopback proxy.
- Removal of the HOME `ollama`, `ollama-exporter` and `comfyui` sources, networks, routes, metrics, backup entries and tests.
- Stage 05 documents that keep the Ollama and ComfyUI setup.

##### Out of Scope

- Managing server B's operating system, driver or Ollama version from this repository.
- New models beyond the three selected, model licences, or a second inference engine.
- Re-embedding Qdrant collections; C-04 shows it is not needed.
- Deleting host data; the owner deletes ComfyUI data after removal with the exact path.
- Any live change without the owner's approval at that step.

#### Behavior Contract

##### Inputs and Outputs

- Input: server B runs Ollama 0.40.19 or later, reachable from server A on port 11434.
- Output: HOME callers use `http://192.168.0.22:11434`; server B callers use `http://127.0.0.1:11434`.
- Models: `embeddinggemma-2:740m-q8_0` (embedding, the digest HOME used), `gemma4:e2b` (chat), `tev1:0.8b-q8_0` (decision). `lfm2.5:8b`, `d1:3b`, `tev1:0.8b` and `minicpm-v4.6:1b` leave service.
- Invariant: no HOME container keeps an internal-only network as its only path to server B.

##### Failure Behavior

- Server B unreachable or a model missing: stop before moving consumers; HOME keeps its container until C-01 passes.
- A consumer cannot reach the LAN: stop that consumer's change and keep its previous endpoint.
- Embedding drift (cosine under 0.999 on the sample): stop the removal and plan a re-index.
- Firewall not limited to server A: stop before the HOME Ollama is removed.
- Server B outage after the move: callers fail until server B is restored; HOME keeps no fallback engine.

#### Acceptance Criteria

##### Criteria

- **AC-0001**: Server B serves the three selected models on its GPU and answers server A, and its firewall admits only server A (C-01, C-02).
- **AC-0002**: Every HOME service and server A host program that used Ollama calls server B and gets a model answer, with the embedding still compatible with stored vectors (C-03, C-04).
- **AC-0003**: Server B's OpenClaw and blog-data call the local Ollama, and the `ollama-api` route, its credentials and the loopback proxy are retired (C-03, C-05).
- **AC-0004**: No HOME `ollama`, `ollama-exporter` or `comfyui` source, network, route, metric, backup entry or test remains, and Compose is valid (C-05).
- **AC-0005**: Stage 05 documents keep the server B Ollama setup and the retired ComfyUI setup (C-06).

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| C-01 | Server B serves the selected models on the GPU and answers server A | `/api/version`, `/api/tags`, `/api/ps` from server A | Does not prove the firewall blocks other hosts | Before any consumer moves | Observation |
| C-02 | The firewall admits only server A | Owner readback of the Windows rule and a refused call from another host | Owner-reported | Before the HOME Ollama is removed | Observation |
| C-03 | Each consumer calls server B and gets a model answer | Consumer config and one request per consumer, matched in time | One request per consumer | After each consumer change | Observation |
| C-04 | The embedding stays compatible with stored vectors | Embeddings for the same inputs from both hosts | Sample inputs only | Before the HOME Ollama is removed | Automated |
| C-05 | No `ollama`, `ollama-exporter` or `comfyui` service, route, network or secret remains and Compose is valid | Compose render, contract tests, secret catalog checks | Static source | After each removal | Automated |
| C-06 | Stage 05 keeps the Ollama and ComfyUI setup | Operations catalog and metadata checks | Document structure | After the documents change | Automated |

Live checks are observations recorded in the Task; static checks run at commit and in hosted CI.

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
