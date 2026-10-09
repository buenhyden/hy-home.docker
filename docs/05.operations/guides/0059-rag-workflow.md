---
title: "RAG Workflow Usage Guide"
version: "1.0.4"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0059"
created: "2026-03-25"
---

# RAG Workflow Usage Guide

## Overview

이 가이드는 Open WebUI가 Ollama 임베딩 모델로 문서를 벡터화하고 검색 컨텍스트를 생성하는 RAG 사용 흐름을 설명한다. 현재 구현은 `infra/08-ai/open-webui/docker-compose.yml`의 `OLLAMA_BASE_URL`, `RAG_EMBEDDING_ENGINE`, `RAG_EMBEDDING_MODEL` 환경변수로 정의된다. `VECTOR_DB`를 설정하지 않으므로 벡터는 Open WebUI 기본 로컬 저장소(`open-webui` 데이터 볼륨)에 저장되며 Qdrant는 쓰지 않는다(SPEC-0182에서 쓰이지 않던 `VECTOR_DB_URL`을 제거했다).

## Audience and Goal

**대상**

- Operator
- AI Engineer
- Internal User
- AI Agent

**목적**

- Open WebUI에서 문서 업로드, 임베딩, 로컬 벡터 저장, 검색 컨텍스트 주입 흐름을 이해한다.
- RAG 연결성 점검은 현재 compose env와 선택한 profile 경계에 맞춰 수행한다.
- 장애 대응과 rollback은 Open WebUI runbook으로 넘긴다.

## Usage

### 사전 조건

- root `docker-compose.yml`은 AI compose 파일을 무조건 include하므로, `ai` profile을 선택해야 기동된다.
- Compose가 선언한 `RAG_EMBEDDING_MODEL` 모델이 Ollama에 준비되어야 한다.

### 사용 절차

1. Open WebUI compose env가 현재 계약과 일치하는지 확인한다.
   - `OLLAMA_BASE_URL=http://ollama:${OLLAMA_PORT:-11434}`
   - `RAG_EMBEDDING_ENGINE=ollama`
   - `RAG_EMBEDDING_MODEL`은 Compose 선언 값
2. Open WebUI에서 PDF, Markdown, 텍스트 문서를 업로드한다.
3. Open WebUI가 Ollama 임베딩 엔진으로 문서를 벡터화해 로컬 벡터 저장소에 저장하는지 확인한다.
4. 업로드 문서를 지정해 질문하고, 답변에 검색 컨텍스트가 반영되는지 확인한다.
5. 인덱싱 실패나 연결 실패가 반복되면 Open WebUI runbook으로 handoff한다.

### Local index ownership

선언 WebUI는 같은 volume의 SQLite·upload와 `DATA_DIR/vector_db` Chroma를 사용한다. Embedding-model 변경에는 재인덱싱이 필요할 수 있으므로 [WebUI Runbook](../runbooks/0057-open-webui.md) 전에 원문·접근권한·모델 출처를 보존한다. 답변 성공만으로 검색 권한을 증명하지 않는다. 허용된 시험 문서의 retrieval/citation과 거부 문서 경계를 비공개 내용 노출 없이 확인한다. 외부 Qdrant 도입은 별도 설계 변경이다.

### Common Checks

- `bash scripts/hardening/check-all-hardening.sh 08-ai`
- `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh`

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [Open WebUI recovery runbook](../runbooks/0057-open-webui.md)을 따른다.

### Traceability

- Governing authority: [AI Infrastructure Architecture Description](../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: `0059` 번호를 공유하는 Policy·Runbook은 없다.

## Troubleshooting

- 선언된 임베딩 모델이 Ollama에 없는데 RAG 인덱싱을 시작하는 경우.
- Open WebUI service-local compose 파일만 단독 검증해 선언된 network undefined 오류를 현재 구현 실패로 오해하는 경우.
- host localhost로 Open WebUI 내부 endpoint를 직접 조회하는 경우. 현재 Open WebUI는 Traefik route와 container-internal healthcheck를 기준으로 한다.

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Open WebUI usage guide](0057-open-webui.md)
- [Open WebUI operations policy](../policies/0057-open-webui.md)
- [Open WebUI recovery runbook](../runbooks/0057-open-webui.md)
