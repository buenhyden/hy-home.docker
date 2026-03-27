# AI Tier Guides (08-ai)

> `08-ai` 계층의 사용/설정/이해를 위한 가이드 문서 모음.

## Overview

이 디렉터리는 AI 계층의 사용자·엔지니어 가이드를 관리한다. 서비스 운영 정책(08)이나 장애 복구 절차(09)가 아니라, 기능 이해와 재현 가능한 사용 방법을 제공하는 것이 목적이다.

## Audience

이 README의 주요 독자:

- AI Engineer
- Operator
- Developer
- Internal User
- AI Agent

## Scope

### In Scope

- Open WebUI 사용 및 RAG 활용 가이드
- Ollama 추론 엔진 사용 가이드
- AI 계층 공통 학습/운영 준비용 가이드 문서

### Out of Scope

- 정책/통제 기준 정의 (08.operations)
- 장애 대응/복구 절차 (09.runbooks)
- 사고 기록/회고 문서

## Structure

```text
08-ai/
├── 01.llm-inference.md
├── 02.rag-workflow.md
├── local-llm-setup.md
├── ollama.md
├── open-webui.md
└── README.md
```

## Documents

- [Open WebUI Interface & RAG Guide](./open-webui.md)
- [Ollama Inference Engine Guide](./ollama.md)
- [01. LLM Inference Guide](./01.llm-inference.md)
- [02. RAG Workflow Guide](./02.rag-workflow.md)
- [Local LLM Setup](./local-llm-setup.md)

## How to Work in This Area

1. 새 가이드는 `docs/99.templates/guide.template.md` 구조를 따른다.
2. Open WebUI와 Ollama의 역할을 분리해서 문서를 작성한다.
3. 가이드 변경 시 대응 Operation/Runbook 링크를 함께 점검한다.
4. 상대 경로만 사용하고 깨진 링크를 남기지 않는다.

## Related References

- [AI PRD (공통)](../../01.prd/2026-03-26-08-ai.md)
- [Open WebUI PRD](../../01.prd/2026-03-27-08-ai-open-webui.md)
- [AI ARD (공통)](../../02.ard/0008-ai-architecture.md)
- [Open WebUI ARD](../../02.ard/0013-open-webui-architecture.md)
- [AI Operations](../../08.operations/08-ai/README.md)
- [AI Runbooks](../../09.runbooks/08-ai/README.md)
- [AI Infra](../../../infra/08-ai/README.md)
