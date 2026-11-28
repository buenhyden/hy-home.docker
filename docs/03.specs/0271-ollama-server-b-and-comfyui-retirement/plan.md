---
title: 'Ollama on Server B and ComfyUI Retirement Plan'
version: 0.1.0
type: sdlc/plan
status: draft
owner: '@buenhyden'
document_scope:
  subject: 'hy-home.docker'
  layer: workspace
updated: '2026-11-28'
layer: specs
artifact_id: 'SPEC-0271-PLAN-0001'
parent_ids:
- 'SPEC-0271'
created: '2026-11-28'
---

# Ollama on Server B and ComfyUI Retirement Plan

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the plan payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Overview

##### Outcome

Delivers [SPEC-0271](spec.md): every Ollama caller on server B's native Ollama and the HOME `ollama`, `ollama-exporter` and `comfyui` services retired.

##### Constraints

- Fact: server B runs Ollama 0.40.19 on `0.0.0.0:11434`, reachable from server A; `embeddinggemma-2:740m` there has digest `f4981a15b998`, the same as HOME, and sample embeddings agree at cosine 0.9999 or more.
- Fact: `gemma4:e2b` and `tev1:0.8b-q8_0` are not yet on server B.
- Assumption: the owner applies the Windows settings and firewall rule on server B.
- Authority: the owner approved this plan on 2026-11-28; each live change (container removal, Traefik or n8n recreate, user config edits) waits for the owner's approval at that step.

#### Dependencies

##### Prerequisites

ADR-0064; the n8n Local Ollama credential stored in n8n; blog-data's consumer contract in the Qdrant and Ollama READMEs; the server B loopback proxy pattern in RUN-0110 step 7.

##### Shared Resources

`docker-compose.yml` and Traefik are touched by W3, W5, W6 and W7 in that order. The HOME `ollama` container stays until W5 ends so any consumer can roll back.

#### Work Breakdown

##### Work Units

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| W1 | ADR-0064, REQ-0009 and AD-0008 record Ollama on server B and ComfyUI's retirement | None | TSK-0001 | `docs/02.architecture/`, `docs/01.requirements/0009-ai.md`, this package, `docs/99.templates/registry.json` | AC-0005 | C-06 |
| W2 | Stage 05 server B Ollama runbook and guide: settings, firewall, models, checks; the owner applies them on server B | W1 | TSK-0001 | `docs/05.operations/` Ollama documents | AC-0001, AC-0005 | C-01, C-02, C-06 |
| W3 | HOME consumers call server B: `n8n-worker` network and credential, Open Notebook, model policy and its checks, docs eval default, LAB Open WebUI endpoint, embedding tag | W2 | TSK-0001 | `infra/07-workflow/n8n/`, `infra/08-ai/open-notebook/`, `labs/`, `scripts/lib/ops/`, `docker-compose.yml`, tests | AC-0002 | C-03, C-04, C-05 |
| W4 | Server A host programs: Hermes model alias and OpenClaw provider point at server B | W2 | TSK-0001 | `~/.hermes/config.yaml`, `~/.openclaw/openclaw.json` (owner-approved, outside the repository) | AC-0002 | C-03 |
| W5 | Server B callers use the local Ollama; the `ollama-api` route, `INFRA-009`, `AI-012`, `AI-013` and the loopback proxy are retired; blog-data is notified | W3, W4 | TSK-0001 | Traefik, secret catalog, Stage 05 documents | AC-0003 | C-03, C-05 |
| W6 | Remove the HOME `ollama` and `ollama-exporter` sources, routes, networks, metrics, dashboard, alerts, backup entries, ledger entries and tests | W5 | TSK-0001 | `infra/08-ai/ollama/` and its consumers, tests | AC-0004 | C-05 |
| W7 | Remove ComfyUI sources, networks, ledger entries and tests; Stage 05 keeps its setup; the owner deletes its host data | W1 | TSK-0001 | `infra/08-ai/comfyui/` and its consumers, `docs/05.operations/`, tests | AC-0004, AC-0005 | C-05, C-06 |

##### Dependency Edges

W1, then W2. W3 and W4 move consumers once C-01 passes; W5 retires the cross-host route once they are verified; W6 removes HOME Ollama last. W7 is independent after W1. Rollback before W6: point a consumer back at `http://ollama:11434`. After W6, rollback is restoring `infra/08-ai/ollama/` from Git and its model store, which stays on disk until the owner deletes it.

#### Verification Plan

##### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| C-01 | Server B serves the selected models on the GPU and answers server A | `/api/version`, `/api/tags`, `/api/ps` from server A | Does not prove the firewall blocks other hosts | Before any consumer moves | Observation |
| C-02 | The firewall admits only server A | Owner readback of the Windows rule and a refused call from another host | Owner-reported | Before the HOME Ollama is removed | Observation |
| C-03 | Each consumer calls server B and gets a model answer | Consumer config and one request per consumer, matched in time | One request per consumer | After each consumer change | Observation |
| C-04 | The embedding stays compatible with stored vectors | Embeddings for the same inputs from both hosts | Sample inputs only | Before the HOME Ollama is removed | Automated |
| C-05 | No `ollama`, `ollama-exporter` or `comfyui` service, route, network or secret remains and Compose is valid | Compose render, contract tests, secret catalog checks | Static source | After each removal | Automated |
| C-06 | Stage 05 keeps the Ollama and ComfyUI setup | Operations catalog and metadata checks | Document structure | After the documents change | Automated |

##### Evidence Plan

Static checks (C-05, C-06) run at commit and in hosted CI; live observations (C-01 to C-04) are recorded in the Task by the agent or the owner as stated. A failed live check stops the next work unit.

#### Promotion Map

##### Durable Owners

- Where Ollama runs and how it is reached: ADR-0064, AD-0008, the Stage 05 Ollama guide and runbook.
- ComfyUI's retired setup: a Stage 05 ComfyUI document.

##### Consumer Updates

Consumers are listed in W3 to W5; TSK-0001's Promotion Receipt records each document and commit.

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
