---
title: "Ollama and Open WebUI for Local AI Infrastructure"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0008"
parent_ids:
- "AD-0008"
created: "2026-03-26"
---
# ADR-0008: Ollama and Open WebUI for Local AI Infrastructure

## Context

This document records the decision to select Ollama and Open WebUI as the core technology stack for building the AI infrastructure. Local resource use, data privacy, and RAG extensibility were the top considerations.

To provide intelligent services within the project, an LLM inference engine and a user interface that can use it are needed. In addition, RAG (Retrieval-Augmented Generation) is essential for generating answers based on internal documents. Commercial APIs (OpenAI, etc.) were excluded due to cost and security concerns, and various open-source alternatives capable of local operation were reviewed.

## Decision

- **Inference engine**: adopt `Ollama`. (Go-based fast execution, easy model deployment, strong GPU acceleration support)
- **UI/RAG**: adopt `Open WebUI`. (UI convenience, built-in Qdrant-integrated RAG support, OpenAI API spec compatibility)
- **Accelerator**: keep a dedicated technical GPU pass-through via the NVIDIA Docker runtime.

## Consequences

- **Positive**:
  - AI services remain usable even when external network access is cut off.
  - Unlimited experimentation without separate API token costs.
  - Data leakage paths are completely blocked.
- **Trade-offs**:
  - Creates a dependency on the host OS's GPU driver and kernel version.
  - Local open-source models have performance and context-length limits compared to commercial models.

### Explicit Non-goals

- Building a large-scale serving optimization environment such as vLLM or Text Generation Inference (TGI) (extreme resource consumption and many management points).
- Direct replacement development of cloud-only model APIs.

### Agent-related Example Decisions

- **Model selection**: adopt `llama3.1-8b` for lightweight work and the `qwen2.5-coder` family for complex reasoning.
- **Tool gating**: agents perform inference indirectly through Open WebUI's API endpoint.

## Options Considered

### vLLM

- Good: throughput performance is excellent, enabling highly efficient serving.
- Bad: configuration is complex, VRAM usage stays consistently high, and model management is more cumbersome than Ollama.

### LocalAI

- Good: broadly supports various models (audio, image, etc.).
- Bad: less optimized for performance than Ollama, and deployment configuration is relatively heavy.

## Traceability

The confirming evidence for this decision is limited to the Architecture Description, Spec, and Operations documents linked in `Related Documents`, and the current repository configuration. It makes no claim about runtime state without separate execution evidence.

## Decision Drivers

The decision context above records the applicable drivers and evidence.

## Related Documents

- **PRD**: [009-ai.md](../../01.requirements/0009-ai.md)
- **Architecture Description**: [0008-ai-architecture.md](../descriptions/0008-ai-architecture.md)
- **Spec**: [009-ai/spec.md](../descriptions/0008-ai-architecture.md)
