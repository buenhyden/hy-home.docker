# AI Tier Guides (08-ai)

> LLM Inference, RAG Orchestration, and Intelligence Layer.

## Overview

이 디렉터리는 `hy-home.docker`의 AI 계층(08-ai)에 대한 기술 가이드와 시스템 이해 문서를 포함한다. 주로 모델 라이프사이클 관리와 추론 엔진 최적화를 다룬다.

## Documents

- [01. LLM Inference Guide](./01.llm-inference.md) - Model lifecycle and GPU optimization.
- [02. RAG Workflow Guide](./02.rag-workflow.md) - Vector search and retrieval setup.
- [Ollama System Guide](./ollama.md) - Core inference engine details and model management.
- [Open WebUI Guide](./open-webui.md) - Chat interface and RAG workflow orchestrator.
- [Local LLM Setup](./local-llm-setup.md) - Local environment requirements.

## How to Work in This Area

1. 새 가이드는 `guide.template.md`를 사용하여 작성한다.
2. 시스템 전반의 아키텍처는 [ARD](../../docs/02.ard/README.md)를 참조한다.
3. 운영 및 장애 대응은 각각 [08.operations](../08.operations/08-ai/README.md) 및 [09.runbooks](../09.runbooks/08-ai/README.md)를 참조한다.

## Related References

- [infra/08-ai/](../../infra/08-ai/README.md) - Infrastructure tier overview.
- [Operations Policy](../../docs/08.operations/08-ai/README.md) - Resource management.
- [AI Runbook](../../docs/09.runbooks/08-ai/README.md) - Recovery procedures.
