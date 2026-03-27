# Open WebUI Product Requirements Document

<!-- Target: docs/01.prd/2026-03-27-08-ai-open-webui.md -->

---

## Open WebUI Product Requirements

## Overview (KR)

이 문서는 Open WebUI의 제품 요구사항을 정의한다. Open WebUI는 로컬 LLM과의 상호작용 및 RAG(Retrieval-Augmented Generation) 오케스트레이션을 위한 종합적인 웹 인터페이스를 제공한다. 사용자 가치, 문제 정의, 성공 기준을 명확히 하여 후속 설계와 구현의 기준으로 사용한다.

## Vision

Provide a premium, ChatGPT-like interface for the `hy-home.docker` ecosystem that empowers users to interact with local LLMs and manage document-based knowledge sharing via RAG.

## Problem Statement

Interacting with local LLMs often requires CLI knowledge or fragmented tools. Users need a unified, visual, and secure interface that supports multi-user collaboration, document indexing, and seamless integration with existing AI/Data tiers (Ollama, Qdrant).

## Personas

- **Persona 1**: **End User** (Chat interface for daily tasks)
- **Persona 2**: **AI Engineer** (RAG orchestration & prompt engineering)
- **Persona 3**: **Operator** (Resource monitoring & SSO integration)

## Key Use Cases

- **STORY-01**: As an end user, I want to chat with local models (Ollama) through a beautiful web UI.
- **STORY-02**: As an AI engineer, I want to upload PDF/Text documents and query them using RAG.
- **STORY-03**: As an operator, I want to ensure only authenticated users can access the AI interface via SSO.

## Functional Requirements

- **REQ-PRD-FUN-01**: Support multi-model selection from the Ollama backend.
- **REQ-PRD-FUN-02**: Provide a RAG engine integrating with Qdrant for document indexing and retrieval.
- **REQ-PRD-FUN-03**: Support persistent chat history and document metadata storage.
- **REQ-PRD-FUN-04**: Integration with Traefik for SSL termination and SSO middleware.

## Success Criteria

- **REQ-PRD-MET-01**: Successful connection to Ollama and Qdrant services within the local network.
- **REQ-PRD-MET-02**: Document indexing latency under 5 seconds for standard PDF files (using CUDA acceleration).

## Scope and Non-goals

- **In Scope**:
  - Web interface (Svelte-based) configuration.
  - RAG orchestration logic (Embedding engine selection).
  - Traefik routing and SSO labels.
- **Out of Scope**:
  - Managing model weight downloads (Handled by Ollama).
  - Hardening the Qdrant database (Handled by Data Tier).
- **Non-goals**:
  - Building a custom LLM training platform.

## Risks, Dependencies, and Assumptions

- **Dependency**: Requires `ollama` service to be healthy for inference.
- **Dependency**: Requires `qdrant` service for vector storage.
- **Assumption**: Users have sufficient GPU memory for CUDA-accelerated embedding/inference.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: Updating documentation links, adjusting environment variables in `docker-compose.yml`.
- **Disallowed Actions**: Disabling SSO middlewares without approval.
- **Human-in-the-loop Requirement**: Required for upgrading major image versions.

## Related Documents

- **ARD**: `[../02.ard/0013-open-webui-architecture.md]`
- **Spec**: `[../04.specs/08-ai/open-webui.md]`
- **Plan**: `[../05.plans/2026-03-27-08-ai-open-webui-plan.md]`
- **ADR**: `[../03.adr/0016-open-webui-implementation.md]`
