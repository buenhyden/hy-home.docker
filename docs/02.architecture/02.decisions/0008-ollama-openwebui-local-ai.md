---
title: "Ollama and Open WebUI for Local AI Infrastructure"
version: "2.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "architecture"
artifact_id: "ADR-0008"
parent_ids:
- "AD-0008"
created: "2026-03-26"
---

# ADR-0008: Ollama and Open WebUI for Local AI Infrastructure

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-decision payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context

##### Problem and Drivers

This document records the decision to select Ollama and Open WebUI as the core technology stack for building the AI infrastructure. Local resource use, data privacy, and RAG extensibility were the top considerations.

To provide intelligent services within the project, an LLM inference engine and a user interface that can use it are needed. In addition, RAG (Retrieval-Augmented Generation) is essential for generating answers based on internal documents. Commercial APIs (OpenAI, etc.) were excluded due to cost and security concerns, and various open-source alternatives capable of local operation were reviewed.

###### Sources
<!-- core-payload-level:4 -->

The confirming evidence for this decision is limited to the Architecture Description, Spec, and Operations documents linked below, and the current repository configuration. It makes no claim about runtime state without separate execution evidence.

- **PRD**: [009-ai.md](../../01.requirements/0009-ai.md)
- **Architecture Description**: [0008-ai-architecture.md](../01.descriptions/0008-ai-architecture.md)

##### Decision Scope

Explicit non-goals:

- Building a large-scale serving optimization environment such as vLLM or Text Generation Inference (TGI) (extreme resource consumption and many management points).
- Direct replacement development of cloud-only model APIs.

#### Options

##### Considered Options

###### vLLM
<!-- core-payload-level:4 -->

- Good: throughput performance is excellent, enabling highly efficient serving.
- Bad: configuration is complex, VRAM usage stays consistently high, and model management is more cumbersome than Ollama.

###### LocalAI
<!-- core-payload-level:4 -->

- Good: broadly supports various models (audio, image, etc.).
- Bad: less optimized for performance than Ollama, and deployment configuration is relatively heavy.

##### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| vLLM | Excellent throughput performance, enabling highly efficient serving. | Configuration is complex, VRAM usage stays consistently high, and model management is more cumbersome than Ollama. | Not chosen because configuration is complex, VRAM usage stays high, and model management is more cumbersome than Ollama. |
| LocalAI | Broadly supports various models (audio, image, etc.). | Less optimized for performance than Ollama, and deployment configuration is relatively heavy. | Not chosen because it is less optimized than Ollama and its deployment configuration is relatively heavy. |
| `Ollama` inference engine with `Open WebUI` for UI/RAG and NVIDIA Docker runtime GPU pass-through | Fast Go-based execution, easy model deployment and GPU acceleration, built-in Qdrant RAG and OpenAI API compatibility; works without external network, with no API token cost and no data leakage path. | Dependency on the host OS's GPU driver and kernel version, and local models have performance and context-length limits compared to commercial models. | Local resource use, data privacy and RAG extensibility were the top considerations; commercial APIs were excluded due to cost and security concerns. |

vLLM was not chosen because configuration is complex, VRAM usage stays high, and model management is more cumbersome than Ollama. LocalAI was not chosen because it is less optimized for performance than Ollama and its deployment configuration is relatively heavy.

#### Decision

##### Chosen Option

- **Inference engine**: adopt `Ollama`. (Go-based fast execution, easy model deployment, strong GPU acceleration support)
- **UI/RAG**: adopt `Open WebUI`. (UI convenience, built-in Qdrant-integrated RAG support, OpenAI API spec compatibility)
- **Accelerator**: keep a dedicated technical GPU pass-through via the NVIDIA Docker runtime.

##### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval record is linked. Effective from 2026-03-26.

#### Consequences

##### Impacts

- **Positive**:
  - AI services remain usable even when external network access is cut off.
  - Unlimited experimentation without separate API token costs.
  - Data leakage paths are completely blocked.
- **Trade-offs**:
  - Creates a dependency on the host OS's GPU driver and kernel version.
  - Local open-source models have performance and context-length limits compared to commercial models.

###### Agent-related Example Decisions
<!-- core-payload-level:4 -->

- **Model selection**: adopt `llama3.1-8b` for lightweight work and the `qwen2.5-coder` family for complex reasoning.
- **Tool gating**: agents perform inference indirectly through Open WebUI's API endpoint.

##### Follow-up

On 2026-11-17 the owner, @buenhyden, directed an in-place amendment of this
record: its sections moved line for line to the core decision form, and the
options table under Trade-offs was derived from the options it records. The
decision text is unchanged.

No follow-up work is recorded in this decision.

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
