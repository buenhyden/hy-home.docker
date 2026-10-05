---
title: "Ollama Usage Guide"
version: "2.0.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0056"
parent_ids:
- "POL-0056"
implementation_services:
  infra/08-ai/ollama/docker-compose.yml:
  - ollama
  - ollama-exporter
created: "2026-05-10"
---

# Ollama Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Overview

이 문서는 `hy-home.docker` AI 계층의 핵심 추론 엔진인 Ollama 사용 방법을 설명한다. 현재 구현은 `infra/08-ai/ollama/docker-compose.yml`에 있고 root `docker-compose.yml`이 이를 무조건 include하며, `ollama`와 `ollama-exporter`는 `ai`, `ai-llm` 또는 `ollama` profile을 선택할 때 기동된다. 모델 라이프사이클, GPU 가속 확인, Open WebUI 연동, exporter 관측 흐름은 그 profile이 선택된 런타임을 기준으로 수행한다.

### Usage Type

`system-guide`

### Target Audience

- AI Engineer
- Developer
- Operator
- Agent-tuner

### Purpose

- Ollama 모델 운용 절차를 표준화한다.
- API/CLI/관측(Exporter) 경로를 일관된 방식으로 점검한다.
- Open WebUI/RAG 연동 전에 필요한 추론 계층 준비 상태를 확보한다.

### Prerequisites

- NVIDIA GPU 및 NVIDIA Container Toolkit이 정상 설치되어야 한다.
- root `docker-compose.yml`은 `infra/08-ai/ollama/docker-compose.yml`을 무조건 include하므로, 실행 시 `ai`, `ai-llm` 또는 `ollama` profile을 선택해야 한다.
- `ollama` 컨테이너가 root compose project 안에서 기동 가능해야 한다.
- 모델 영속 저장 경로 `${DEFAULT_AI_MODEL_DIR}/ollama`가 준비되어야 한다.
- 기본 포트/엔드포인트:
  - Host API: `127.0.0.1:${OLLAMA_HOST_PORT:-11434}`; container API: `ollama:${OLLAMA_PORT:-11434}`
  - Exporter: `OLLAMA_EXPORTER_PORT`는 연결한 Compose와 공개 `.env.example`이 소유한다. 내부 지표 listener이며 모델 추론을 중계하지 않는다.

### Step-by-step Instructions

#### 1. Service & GPU Health Check

```bash
# 호스트 GPU 상태
nvidia-smi

# Ollama API health via host port
curl -f http://localhost:${OLLAMA_HOST_PORT:-11434}/api/tags

# 컨테이너 내부 GPU 인식 확인
docker compose exec ollama nvidia-smi
```

### 2. Model Lifecycle (CLI)

```bash
# 모델 목록 확인
docker compose exec ollama ollama list
```

모델 변경(`ollama pull` 등)은 [Ollama Operations Policy](../policies/0056-ollama.md)가 요구하는 승인된 local/dev rehearsal 없이 무조건 실행하지 않는다. 절차는 [Ollama runbook](../runbooks/0056-ollama.md)을 따른다.

### 3. Inference API Check

```bash
curl http://localhost:${OLLAMA_HOST_PORT:-11434}/api/generate -d '{
  "model": "llama3",
  "prompt": "Hello from hy-home"
}'
```

#### 3a. Decision API Smoke

[Ollama release notes](https://github.com/ollama/ollama/releases)의 `/v1/systemone`은 선택 또는 점수형 결정을 지원한다. 아래 요청은 실제 업무 데이터 없이 [tev1:0.8b](https://ollama.com/library/tev1)를 확인하며, `keep_alive: 0`으로 요청 뒤 모델을 내린다.

```bash
curl --fail-with-body --max-time 120 http://127.0.0.1:${OLLAMA_HOST_PORT:-11434}/v1/systemone \
  -H 'Content-Type: application/json' \
  -d '{"model":"tev1:0.8b","state":"Our checkout returns HTTP 500 errors.","questions":{"label":{"type":"choice","instructions":"Classify this ticket.","criteria":{"bug":"Software errors","billing":"Payments and refunds"}}},"keep_alive":0}'
```

선택값은 `criteria` 안에 있어야 하고, 확률은 유한한 `0`~`1` 값이며 합계가 약 `1`인지 확인한다. `confidence`와 선택 확률은 모델 판단값이지 정확도나 보정된 신뢰도가 아니다.

GTX 1060 6 GiB에서는 [tev1:0.8b](https://ollama.com/library/tev1)를 먼저 사용한다. [tev1:4b](https://ollama.com/library/tev1)(약 4.5 GB)와 [nimble:9b](https://ollama.com/library/nimble)(약 9.5 GB)는 파일 크기와 실행 메모리가 같지 않으므로 VRAM 여유를 별도로 확인한 승인된 rehearsal에서만 사용한다.

[tev1:0.8b](https://ollama.com/library/tev1)가 없으면 승인된 rehearsal에서만 `docker compose exec ollama ollama pull tev1:0.8b`로 가져온 뒤 위 요청을 실행한다.

#### 4. Open WebUI Integration Check

1. Open WebUI 환경변수 `OLLAMA_BASE_URL`가 `http://ollama:${OLLAMA_PORT:-11434}`를 가리키는지 확인.
2. Open WebUI UI에서 모델 목록이 정상 조회되는지 확인.
3. 모델 미노출 시 `ollama` health/log를 먼저 확인.

#### 5. Exporter Observability Check

```bash
# exporter exposes metrics inside `ai_net`; it is not published to host.
docker compose exec ollama-exporter sh -lc 'wget -q -O- "http://localhost:${OLLAMA_EXPORTER_PORT:-8000}/metrics"'
```

- 주요 관측 대상: 모델 로드 수, 메모리 사용량, scrape 상태.

### Common Pitfalls

- **GPU 미인식**: 컨테이너는 실행되지만 CPU 추론으로 강등됨.
- **VRAM OOM**: 대형 모델 동시 로드 시 응답 실패/지연.
- **모델 태그 불일치**: Open WebUI 설정 모델명과 Ollama 실제 태그 불일치.
- **Exporter 미수집**: host-published 포트로 오해해 localhost에서 직접 조회하는 경우. exporter는 compose healthcheck와 `ai_net` 내부 scrape 경로를 기준으로 확인한다.

### Source-backed operating contract

- **목적·분류**: `ollama`와 `ollama-exporter`는 소유자가 확인한 `HOME` local inference 및 metric 서비스다.
- **profile·구현 소유권**: `ai`/`ai-llm`은 Ollama를 선택하고 `ollama`는 해당 서비스만 선택하는 방법을 제공한다. [Compose](../../../infra/08-ai/ollama/docker-compose.yml)와 선택된 image 선언이 구현을 소유한다.
- **흐름·의존성**: Open WebUI와 승인된 client는 `ai_net`으로 Ollama를 호출하며 exporter는 Prometheus에 제공할 metric을 위해 Ollama API를 읽는다. NVIDIA runtime/driver, model storage, Traefik, gateway auth와 root CA가 전제 조건이다. loopback host port는 운영자 endpoint이며 public route는 계속 gateway의 보호를 받는다.
- **상태·환경 설정**: `ollama-data:/root/.ollama`는 model manifest/blob을 담는다. model 이름, source, digest, parameter, license와 호환성 evidence를 보존한다. cache에 있다는 사실만으로 출처가 입증되지는 않는다. port/model/concurrency 변수는 secret이 아니다. remote registry credential을 사용하는 경우 해당 secret 소유자의 규칙을 따르며 Compose 출력이나 log에 포함하지 않는다.
- **자원·보안**: Compose는 CPU 4개, 8 GiB limit, 4 GiB reservation과 GPU 접근을 선언한다. 이는 source limit이며 측정된 CPU/RAM/VRAM 여유 용량이 아니다. 인증되지 않은 non-loopback API를 노출하거나 검토하지 않은 model/tool content를 실행하지 않는다.
- **정상 사용·수명 주기**: `docker compose --profile ai config --quiet`로 렌더링하고 명시적으로 승인된 model을 list/pull한다. `/api/tags`와 대표 inference를 검증하며 exporter/GPU 신호를 관찰한다. image나 model migration 전에 digest와 model 출처를 기록하고, model volume 또는 재현 가능한 manifest를 보존한다. 호환성 경계를 한 번에 하나씩 변경한 뒤 inference와 Open WebUI 연동을 다시 확인한다.
- **공식 문서·license**: 공식 [Ollama 저장소](https://github.com/ollama/ollama)와 release note를 따른다. Ollama에는 MIT license가 적용된다. 각 model의 별도 조건도 기록하고 검토해야 한다.

### Model and exporter capacity boundary

`ollama`/`ollama-exporter`는 `ai`/`ai-llm`/`ollama`가 선택하는 HOME이다. 모델·추론은 Ollama가 소유하고 병렬·loaded-model·queue 설정은 context 크기와 공유 GPU 메모리와 함께 평가한다. 한도는 실측 여유가 아니며 과부하 요청은 실패할 수 있다. Exporter는 Ollama health 뒤 내부 model 목록·실행 모델·VRAM metric을 제공한다. Model volume, Docker Secret, 사용자 route나 독립 복구 상태는 없고 추론 proxy 또는 token throughput 증거도 아니다. Maintainer tag는 확인했으나 버전 일치 소스는 확보하지 못했으므로 Compose·maintainer 설명을 넘는 동작을 단정하지 않는다. Upgrade에는 metric 호환성과 제한된 추론 검증이 필요하다. 모델 삭제·download·driver 변경은 기존 승인·출처 및 [GPU 복구](../runbooks/0055-gpu-recovery.md) 경계를 따른다.

### Common Checks

- 직접 API는 호스트 loopback에서만 접근한다. Open WebUI와 exporter는 `ollama` 서비스 DNS로 통신하며, 원격 접근은 인증된 gateway 경로를 사용한다. 기존 LAN 직접 API 소비자는 설정 적용 전에 전환해야 한다.

- `bash scripts/hardening/check-all-hardening.sh 08-ai`
- `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh`
- Runtime approval 후 `ai` profile을 선택한 상태에서 `docker compose exec ollama ollama list`

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0056-ollama.md)을 따른다.

### Traceability

- Declared parent: [Ollama Operations Policy](../policies/0056-ollama.md) (`POL-0056`)
- Governing authority: [AI Infrastructure Architecture Description](../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: [Policy](../policies/0056-ollama.md) (`POL-0056`), [Runbook](../runbooks/0056-ollama.md) (`RUN-0056`)

## Related Documents

- [Ollama Compose](../../../infra/08-ai/ollama/docker-compose.yml)

- [Ollama server configuration](https://docs.ollama.com/faq#how-do-i-configure-ollama-server): `OLLAMA_HOST`로 컨테이너 listener 주소와 포트를 함께 지정한다.

- [Ollama release notes](https://github.com/ollama/ollama/releases), [tev1 model page](https://ollama.com/library/tev1), [nimble model page](https://ollama.com/library/nimble)

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0056-ollama.md)
- [Recovery runbook](../runbooks/0056-ollama.md)
