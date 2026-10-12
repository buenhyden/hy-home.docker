---
title: "AI와 검색 정책"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# AI와 검색 정책

## Overview

AI와 검색의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

## Scope

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Qdrant Operations Policy](0034-qdrant.md) | `POL-0034` | 이 정책은 root-active `HOME` Qdrant 운영 기준을 정의한다. 기준은 Qdrant Compose 구현의 단일 service, exact `ai`/`ai-llm`/`qdrant` profiles, `ai_net`, API key sec |
| [Ollama Operations Policy](0056-ollama.md) | `POL-0056` | 이 문서는 Ollama 운영 정책을 정의한다. 제한된 GPU 자원에서 안정적으로 추론 서비스를 제공하기 위해 모델 도입 기준, 리소스 사용 한계, 장애 대응 기준을 규정한다. |
| [Open WebUI Operations Policy](0057-open-webui.md) | `POL-0057` | 이 문서는 Open WebUI 운영 정책을 정의한다. 인증/접근 통제, 문서 업로드 및 RAG 처리 기준, 구성 변경 승인 절차를 명확히 하여 서비스 안정성과 보안을 유지한다. |
| [08-AI Optimization Hardening Operations Policy](0058-ai-optimization-hardening.md) | `POL-0058` | 이 문서는 `08-ai` 계층의 최적화/하드닝 운영 정책을 정의한다. gateway 경계 보안, Ollama GPU 보호, Open WebUI stateful 운영, 모델 승격/접근 통제/로그 보존 정책을 통제한다. |
| [Open Notebook Operations Policy](0073-open-notebook.md) | `POL-0073` | Open Notebook은 OPTIONAL 지식/모델 워크스페이스다. 콘텐츠, 데이터베이스, provider 자격 증명, 암호화 키가 하나의 복구 경계를 이룬다. |
| [ComfyUI Policy](0081-comfyui.md) | `POL-0081` | ComfyUI는 항상 켜져 있는 HOME 이미지 워크플로 인터페이스다. |
| [Crawl4AI Operations Policy](0091-crawl4ai.md) | `POL-0091` | Crawl4AI는 SSRF가 가능한 서비스다. 검토된 consumer가 필요로 할 때까지 격리하고 인증을 적용한 채 사용하지 않는 상태로 유지한다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 정책 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
