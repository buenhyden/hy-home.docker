---
title: "AI Infrastructure Tier (08-ai)"
version: "1.0.7"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2025-11-12"
---

# AI Infrastructure Tier (08-ai)

> 로컬 LLM 추론 엔진, RAG 인터페이스, 벡터 기반 인텔리전스입니다.

## Overview

`08-ai` 티어는 플랫폼의 인공지능 역량을 제공하며 프라이버시를 보존하는 로컬 추론과 RAG(Retrieval-Augmented Generation)에 초점을 맞춥니다. NVIDIA GPU 가속을 활용해 Ollama로 대형 언어 모델(LLM)을 서비스하고 Open WebUI로 정교한 사용자 인터페이스를 제공합니다.

## Audience

이 README의 주요 독자:

- AI Engineers (모델 배포 및 RAG 튜닝)
- Backend Developers (LLM API 통합)
- SREs (GPU 리소스 오케스트레이션)

## Scope

### In Scope

- Ollama (LLM 추론 엔진)
- Open WebUI (사용자 인터페이스 및 RAG 오케스트레이션)
- NVIDIA CUDA 통합
- 로컬 모델 관리
- Open Notebook과 함께 배치된 SurrealDB의 지식 작업
- MLflow 실험·모델 메타데이터와 아티팩트 관리

### Out of Scope

- 모델 학습 또는 미세 조정 (외부 전용 클러스터에서 처리)
- 벡터 DB 호스팅 (`04-data/qdrant`에서 관리)
- 클라우드 기반 LLM API (OpenAI, Claude 등 - 프록시될 수는 있으나 호스팅되지 않음)

## Structure

```text
08-ai/
├── open-notebook/      # 선택적 지식 앱과 SurrealDB
├── mlflow/             # 선택적 실험 추적과 DB provisioner
├── ollama/             # Inference engine (Go-based)
├── open-webui/         # Web interface and RAG logic
├── comfyui/            # Image workflow UI
├── crawl4ai/           # Opt-in isolated crawler (profile crawl4ai)
└── README.md           # This file
```

## Usage

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../.agents/governance/agentic.md)와 [documentation protocol](../../.agents/governance/documentation-protocol.md)을 따른다.

1. Ollama Usage Guide(`docs/05.operations/guides/0056-ollama.md`)를 읽습니다.
2. Open WebUI Usage Guide(`docs/05.operations/guides/0057-open-webui.md`)와 RAG Workflow Guide(`docs/05.operations/guides/0059-rag-workflow.md`)를 따릅니다.
3. GPU, 모델, 접근, 로깅 통제는 운영 정책 색인(`docs/05.operations/policies/README.md`)에서 확인합니다.
4. NVIDIA 드라이버, OOM, Open WebUI 트러블슈팅은 AI Runbooks(`docs/05.operations/runbooks/README.md`)를 참고합니다.

5. RAG에서 참조하기 전에는 항상 `ollama pull <model>`로 모델을 명시적으로 내려받습니다.
6. 동시 추론 중 OOM을 방지하기 위해 `ollama-exporter`로 VRAM 사용량을 모니터링합니다.
7. RAG 작업에는 `qwen3-embedding:0.6b`(또는 현재 표준 모델)가 벡터화용으로 준비되어 있는지 확인합니다.

## Tech Stack

Ollama, Open WebUI, ComfyUI는 소유자가 확인한 상시 HOME 역량입니다. 런타임 이미지 고정 값은 각 서비스([Ollama](ollama/README.md), [Open WebUI](open-webui/README.md), [ComfyUI](comfyui/README.md))의 Compose 파일에 선언되어 있습니다. [파생된 Compose 이미지 프로젝션](../tech-stack.versions.json)은 드리프트 확인용 뷰입니다.

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Inference | Ollama | Compose에 선언됨 |
| Interface | Open WebUI | Compose에 선언됨 |
| Acceleration | NVIDIA CUDA | NVIDIA Container Toolkit 필요 |
| Vector store | Open WebUI 내장 로컬 스토어 | `VECTOR_DB` 미설정 시 사용됨; Qdrant(`04-data`)는 08-ai의 추적 Compose에 연결되어 있지 않음 |

## Service Matrix

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `ollama` | HTTP | `ai`, `dev` | `${OLLAMA_HOST_PORT}:${OLLAMA_PORT}`와 `ollama.${DEFAULT_URL}` |
| `open-webui` | HTTP | `ai` | Traefik을 통한 `chat.${DEFAULT_URL}`; 선언된 호스트 포트 없음 |
| `ollama-exporter` | HTTP metrics | `ai`, `dev` | `ai_net` 내부에서 `${OLLAMA_EXPORTER_PORT}`로 노출됨 |
| `comfyui` | HTTP | `ai`, `ai-image` | `comfyui.${DEFAULT_URL}`와 선언된 루프백 포트 |

## Configuration

- **GPU Access**: 서비스는 NVIDIA GPU에 접근하도록 `reservations.devices`로 설정되어 있습니다.
- **SSO**: `chat.${DEFAULT_URL}`과 `ollama.${DEFAULT_URL}`으로 접근하며 Keycloak 인증 미들웨어로 보호됩니다.
- **Persistence**: 수 GB 다운로드가 반복되지 않도록 모델은 `${DEFAULT_AI_MODEL_DIR}/ollama`에 저장됩니다.

## Testing

```bash
# Verify GPU availability inside Ollama
docker compose exec ollama nvidia-smi

# List loaded models
docker compose exec ollama ollama list
```

### Convergence service and command map

저장소 루트에서 실행합니다. 정적 사전 점검은 `docker compose --profile ai config --quiet`, 승인된 HOME 대상 시작은 `docker compose --profile ai up -d`입니다.

| Services | Class | Exact profiles |
| --- | --- | --- |
| `ollama`, `ollama-exporter` | HOME | `ai`, `ai-llm`, `ollama` |
| `open-webui` | HOME | `ai`, `ai-llm` |
| `comfyui` | HOME | `ai`, `ai-image` |

안정적인 문서 진입점은 [docs/README.md](../../docs/README.md)입니다. 정확한 Stage 05 대상은 `docs/05.operations/guides/0056-ollama.md`의 `GDE/POL/RUN-0056`, `.../0057-open-webui/`의 `GDE/POL/RUN-0057`, `.../0081-comfyui/`의 `GDE/POL/RUN-0081`입니다.

### 선택적 지식·실험 관리

[Open Notebook](open-notebook/README.md)은 `notebook`, 함께 있는 SurrealDB는
`notebook`·`surrealdb`로 선택합니다. `admin`이나 `dev`로 켜지지 않습니다.
앱 비밀번호·admin CIDR을 쓰며 공유 SSO는 사용하지 않습니다. `/app/data`,
SurrealDB `/mydata`와 암호화 키가 하나의 복구 세트이며 키 유실 시 저장한
provider 자격 증명을 읽지 못할 수 있습니다. provider egress는 별도 승인 경계입니다.

[MLflow](mlflow/README.md)와 DB provisioner는 `mlops`·`data-science`를 유지합니다.
추적 DB는 mng-pg, 아티팩트는 전용 SeaweedFS bucket identity를 사용합니다.
브라우저 SSO는 `edge_net`·`ai_net`·`mng_data_net`·`object_net`의 직접 SDK 접근을
보호하지 않습니다. 이 이동은 인증·학습·서빙 기능을 새로 구현하지 않습니다.
운영 subject0073,0080,0088이 해당 통제와 복구를 소유합니다.

## Related Documents

- [infra/README.md](../README.md)
- Operations guides - 08-ai (`docs/05.operations/guides/README.md`)
- Operations policies - 08-ai (`docs/05.operations/policies/README.md`)
- Operations runbooks - 08-ai (`docs/05.operations/runbooks/README.md`)
- [Documentation index](../../docs/README.md)
