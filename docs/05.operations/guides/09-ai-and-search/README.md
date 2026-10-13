---
title: "AI와 검색 가이드"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "operations"
---

# AI와 검색 가이드

## Overview

AI와 검색의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

## Scope

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Qdrant Usage Guide](0034-qdrant.md) | `GDE-0034` | 이 문서는 root compose에 active include된 [Qdrant Compose 구현](../../../../infra/04-data/qdrant/docker-compose.yml)을 설명한다. |
| [Ollama Usage Guide](0056-ollama.md) | `GDE-0056` | 이 문서는 `hy-home.docker` AI 계층의 핵심 추론 엔진인 Ollama 사용 방법을 설명한다. 현재 구현은 `infra/08-ai/ollama/docker-compose.yml`에 있고 root `docker-compose.yml`이 이를 |
| [Open WebUI Usage Guide](0057-open-webui.md) | `GDE-0057` | 이 문서는 `hy-home.docker` 환경에서 Open WebUI를 통해 Ollama 모델과 대화하고, 문서 기반 RAG를 사용하는 방법을 설명한다. 현재 구현은 `infra/08-ai/open-webui/docker-compose.yml`에 있고 |
| [08-AI Optimization Hardening Usage Guide](0058-ai-optimization-hardening.md) | `GDE-0058` | 이 문서는 `08-ai` 계층의 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. gateway 경계 보안, GPU concurrency 제어, stateful 템플릿 일관성, health 기반 검증 절차를 제공한다. |
| [RAG Workflow Usage Guide](0059-rag-workflow.md) | `GDE-0059` | 이 가이드는 Open WebUI가 Ollama 임베딩 모델로 문서를 벡터화하고 검색 컨텍스트를 생성하는 RAG 사용 흐름을 설명한다. |
| [Open Notebook Usage Guide](0073-open-notebook.md) | `GDE-0073` | Open Notebook은 OPTIONAL 노트북 지식 워크스페이스이다. `open_notebook` 서비스는 오직 `notebook`에만 속한다. 소유자 커밋 `d5912ab03`가 이를 포괄 `admin` selector에서 제거했으며 HOME에서 |
| [ComfyUI Guide](0081-comfyui.md) | `GDE-0081` | ComfyUI는 `ai`와 `ai-image`가 선택하는 상시 실행 HOME 이미지 워크플로 UI이다. |
| [Crawl4AI Usage Guide](0091-crawl4ai.md) | `GDE-0091` | Crawl4AI는 `crawl4ai`로만 선택되는 OPTIONAL 크롤러다. 예정된 소비자는 Open Notebook의 remote-crawler 설정이지만 아직 주석 처리되어 있어 지금은 이를 사용하는 서비스가 없다. 선택하지 않으면 실행 자원을 소 |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 가이드 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
