---
title: "AI와 검색 런북"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# AI와 검색 런북

## Overview

AI와 검색의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

## Scope

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Qdrant Health and Recovery Triage Runbook](0034-qdrant.md) | `RUN-0034` | 범위: root에 포함된 Qdrant 서비스의 상태, SSO 뒤의 REST route 전제, 영속 경로, 증거 수집을 파괴적 데이터 작업 없이 점검한다. 이 런북은 health triage와 별도 승인 후 수행할 Qdrant snapshot의 격리 복 |
| [AI GPU Recovery Runbook](0055-gpu-recovery.md) | `RUN-0055` | > Scope: `infra/08-ai`의 `ollama` NVIDIA GPU 가속 복구. 이 런북은 Ollama 컨테이너가 NVIDIA GPU를 인식하지 못하거나 CPU fallback으로 동작할 때 실행한다. 호스트 드라이버, NVIDIA Cont |
| [Ollama Runbook](0056-ollama.md) | `RUN-0056` | 이 런북은 Ollama 추론 계층 장애에 대한 즉시 실행 절차를 제공한다. GPU 미인식, VRAM OOM, API 장애를 신속히 진단·복구하고 상위 서비스(Open WebUI) 영향도를 최소화한다. > 범위: Ollama 추론 서비스 - Ollama |
| [Open WebUI Runbook](0057-open-webui.md) | `RUN-0057` | 이 런북은 Open WebUI 장애 및 성능 저하 상황에서 즉시 실행 가능한 복구 절차를 제공한다. SQLite 데이터 복구, RAG 인덱스 재동기화, Ollama 연결과 local Chroma 일관성 복구를 표준화한다. > 범위: Open WebUI |
| [08-AI Optimization Hardening Runbook](0058-ai-optimization-hardening.md) | `RUN-0058` | 이 런북은 `08-ai` 하드닝 항목에서 발생하는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. gateway/SSO 체인 누락, Ollama concurrency 설정 누락, Open WebUI stateful 드리프트, exporter heal |
| [Open Notebook Recovery Runbook](0073-open-notebook.md) | `RUN-0073` | 이 런북은 OPTIONAL Open Notebook(`open_notebook`, `surrealdb`, profile `notebook`)의 장애 진단, 백업·격리 복원, 업그레이드 절차를 다룬다. 데이터베이스와 앱 데이터, 암호화 키가 하나의 복구 |
| [ComfyUI Runbook](0081-comfyui.md) | `RUN-0081` | 이 런북은 ComfyUI(`comfyui`, profile `ai`/`ai-image`)의 승인 게이트된 진단과 복구, custom-node·이미지 변경 실패 대응, 격리 복원 계획을 다룬다. |
| [Crawl4AI Recovery Runbook](0091-crawl4ai.md) | `RUN-0091` | 이 런북은 OPTIONAL `crawl4ai`(`crawl4ai`, `crawl4ai-egress`, profile `crawl4ai`)의 시작 실패, 토큰 노출, 메모리 압박 대응과 consumer 연결·해제, 제거 절차를 다룬다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 런북 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
