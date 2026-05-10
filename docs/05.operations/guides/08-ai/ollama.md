<!-- Target: docs/05.operations/guides/08-ai/ollama.md -->

# Ollama Operations Policy

> GPU/VRAM 거버넌스와 모델 도입·승격·운영 통제 정책.

---

## Overview (KR)

이 문서는 Ollama 운영 정책을 정의한다. 제한된 GPU 자원에서 안정적으로 추론 서비스를 제공하기 위해 모델 도입 기준, 리소스 사용 한계, 장애 대응 기준을 규정한다.

## Policy Scope

Ollama 추론 엔진 운영 전반:

- 모델 도입/승격/퇴출 기준
- GPU/VRAM 자원 통제
- 추론 계층 변경 승인 및 검증

## Applies To

- **Systems**: `ollama`, `ollama-exporter`, `open-webui`
- **Agents**: 모델 배포/교체 자동화 에이전트, 추론 호출 에이전트
- **Environments**: `prod`, `staging`, `lab`

## Controls

- **Required**:
  - 모델 변경 전 staging에서 성능 및 안정성 검증을 수행해야 한다.
  - 운영 모델은 검증된 태그/소스만 사용해야 한다.
  - VRAM/메모리 사용량을 exporter 및 대시보드로 상시 관측해야 한다.
- **Allowed**:
  - 승인된 경량/양자화 모델 배포.
  - `keep_alive` 정책 기반 모델 언로드 최적화.
- **Disallowed**:
  - 승인 없는 대형 모델 상시 로드.
  - 출처 불명/무검증 모델 운영 반영.
  - 운영 시간대 무단 리소스 상향.

## Exceptions

- 장애 복구 목적의 단기 예외(예: 임시 모델 fallback)는 온콜 승인 하에 허용.
- 예외 종료 후 기본 정책으로 즉시 복귀하고 기록을 남겨야 한다.

## Verification

- 배포 전:
  - `nvidia-smi` 정상
  - `/api/tags` 응답 정상
  - 대상 모델 추론 smoke test 성공
- 운영 중:
  - VRAM 과점유, 응답 지연, 모델 로드 실패율 모니터링
- 증적:
  - 배포 로그, 모델 버전 기록, 롤백 결과

## Review Cadence

- **Quarterly**: 모델 포트폴리오/자원 정책 검토
- **Per Model Change**: 모델 도입/교체 건별 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**:
  - 모델/기본 프롬프트 변경은 변경 요청 + 검증 기록 + 운영 반영 순으로 진행
- **Eval / Guardrail Threshold**:
  - 배포 게이트: health, 기본 추론 성공, 리소스 임계 초과 없음
- **Log / Trace Retention**:
  - 추론 계층 운영 로그/지표 증적 최소 90일 보관
- **Safety Incident Thresholds**:
  - GPU 자원 고갈로 서비스 불능, 무단 모델 교체, 비인가 추론 엔드포인트 노출은 `Sev1`

## Related Documents

- **PRD**: `[../../01.requirements/2026-03-26-08-ai.md]`
- **ARD**: `[../../02.architecture/requirements/0008-ai-architecture.md]`
- **ADR**: `[../../02.architecture/decisions/0008-ollama-openwebui-local-ai.md]`
- **Spec**: `[../../03.specs/08-ai/spec.md]`
- **Usage**: `[../../05.operations/08-ai/ollama.md]`
- **Procedure**: `[../../05.operations/08-ai/ollama.md]`

## Usage

> Migrated from `docs/05.operations/08-ai/ollama.md` during the 2026-05-10 operations taxonomy consolidation.

### Ollama Inference Engine Usage

> 로컬 LLM 추론 엔진(Ollama) 운영 및 연동 가이드.

---

#### Overview (KR)

이 문서는 `hy-home.docker` AI 계층의 핵심 추론 엔진인 Ollama 사용 방법을 설명한다. 모델 라이프사이클(풀/조회/호출), GPU 가속 확인, Open WebUI 연동, exporter 관측 흐름을 표준 절차로 제공한다.

#### Usage Type

`system-guide`

#### Target Audience

- AI Engineer
- Developer
- Operator
- Agent-tuner

#### Purpose

- Ollama 모델 운용 절차를 표준화한다.
- API/CLI/관측(Exporter) 경로를 일관된 방식으로 점검한다.
- Open WebUI/RAG 연동 전에 필요한 추론 계층 준비 상태를 확보한다.

#### Prerequisites

- NVIDIA GPU 및 NVIDIA Container Toolkit이 정상 설치되어야 한다.
- `ollama` 컨테이너가 기동 가능해야 한다.
- 모델 영속 저장 경로 `${DEFAULT_AI_MODEL_DIR}/ollama`가 준비되어야 한다.
- 기본 포트/엔드포인트:
  - API: `${OLLAMA_PORT:-11434}`
  - Exporter: `${OLLAMA_EXPORTER_PORT:-11435}`

#### Step-by-step Instructions

##### 1. Service & GPU Health Check

```bash
### 호스트 GPU 상태
nvidia-smi

### Ollama health endpoint
curl -f http://localhost:${OLLAMA_PORT:-11434}/api/tags

### 컨테이너 내부 GPU 인식 확인
docker exec ollama nvidia-smi
```

##### 2. Model Lifecycle (CLI)

```bash
### 모델 다운로드
docker exec ollama ollama pull llama3

### 모델 목록 확인
docker exec ollama ollama list
```

##### 3. Inference API Check

```bash
curl http://localhost:${OLLAMA_PORT:-11434}/api/generate -d '{
  "model": "llama3",
  "prompt": "Hello from hy-home"
}'
```

##### 4. Open WebUI Integration Check

1. Open WebUI 환경변수 `OLLAMA_BASE_URL`가 `http://ollama:${OLLAMA_PORT:-11434}`를 가리키는지 확인.
2. Open WebUI UI에서 모델 목록이 정상 조회되는지 확인.
3. 모델 미노출 시 `ollama` health/log를 먼저 확인.

##### 5. Exporter Observability Check

```bash
### exporter metrics endpoint
curl -f http://localhost:${OLLAMA_EXPORTER_PORT:-11435}/metrics
```

- 주요 관측 대상: 모델 로드 수, 메모리 사용량, scrape 상태.

#### Common Pitfalls

- **GPU 미인식**: 컨테이너는 실행되지만 CPU 추론으로 강등됨.
- **VRAM OOM**: 대형 모델 동시 로드 시 응답 실패/지연.
- **모델 태그 불일치**: Open WebUI 설정 모델명과 Ollama 실제 태그 불일치.
- **Exporter 미수집**: 관측 포트 설정 불일치로 지표 공백 발생.

#### Related Documents

- **PRD (AI 공통)**: `[../../01.requirements/2026-03-26-08-ai.md]`
- **ARD (AI 공통)**: `[../../02.architecture/requirements/0008-ai-architecture.md]`
- **ADR (AI 공통)**: `[../../02.architecture/decisions/0008-ollama-openwebui-local-ai.md]`
- **Spec (AI 공통)**: `[../../03.specs/08-ai/spec.md]`
- **Plan (AI 공통)**: `[../../04.execution/plans/2026-03-26-08-ai-standardization.md]`
- **Task (AI 공통)**: `[../../04.execution/tasks/2026-03-26-08-ai-tasks.md]`
- **Operation**: `[../../05.operations/08-ai/ollama.md]`
- **Procedure**: `[../../05.operations/08-ai/ollama.md]`
- **Infrastructure**: `[../../../infra/08-ai/ollama/README.md]`

## Procedure

> Migrated from `docs/05.operations/08-ai/ollama.md` during the 2026-05-10 operations taxonomy consolidation.

### Ollama Maintenance & Recovery Procedure

: Ollama Inference Service

---

#### Overview (KR)

이 런북은 Ollama 추론 계층 장애에 대한 즉시 실행 절차를 제공한다. GPU 미인식, VRAM OOM, API 장애를 신속히 진단·복구하고 상위 서비스(Open WebUI) 영향도를 최소화한다.

#### Purpose

- Ollama 추론 가용성을 빠르게 복구한다.
- GPU 경로 이상과 리소스 고갈 문제를 표준 절차로 처리한다.
- 복구 후 Open WebUI 연동 상태를 검증한다.

#### Canonical References

- `[../../02.architecture/requirements/0008-ai-architecture.md]`
- `[../../02.architecture/decisions/0008-ollama-openwebui-local-ai.md]`
- `[../../03.specs/08-ai/spec.md]`
- `[../../04.execution/plans/2026-03-26-08-ai-standardization.md]`

#### When to Use

- Ollama API(`/api/tags`, `/api/generate`) 호출 실패.
- 컨테이너 내부 GPU 미인식 또는 CPU fallback 발생.
- 모델 로드 시 VRAM OOM으로 추론 실패.
- Open WebUI에서 모델 목록 미표시.

#### Procedure or Checklist

##### Checklist

- [ ] 호스트 `nvidia-smi` 정상 여부 확인
- [ ] `ollama` 컨테이너 healthcheck 확인
- [ ] 최근 모델 변경/배포 이력 확인
- [ ] Open WebUI 영향 범위 확인

##### Procedure

###### 1. Initial Health & API Check

```bash
docker ps --filter name=ollama
docker logs --tail 200 ollama
curl -f http://localhost:${OLLAMA_PORT:-11434}/api/tags
```

###### 2. GPU Recognition Recovery

```bash
### 호스트 GPU 상태
nvidia-smi

### 컨테이너 내부 GPU 상태
docker exec ollama nvidia-smi

### 필요 시 컨테이너 재기동
docker restart ollama
```

###### 3. VRAM OOM Mitigation

```bash
### keep_alive=0으로 상주 모델 언로드(예시)
curl -X POST http://localhost:${OLLAMA_PORT:-11434}/api/generate -d '{
  "model": "llama3",
  "prompt": "release memory",
  "keep_alive": 0
}'
```

- 고부하 모델 사용 중이면 임시로 경량 모델로 fallback한다.

###### 4. Model Integrity Check

```bash
docker exec ollama ollama list
```

- 운영 기준 모델 태그가 존재하는지 확인한다.

###### 5. Open WebUI Dependency Recheck

```bash
### Open WebUI 컨테이너에서 Ollama 접근 확인
docker exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags
```

#### Verification Steps

- [ ] `curl -f http://localhost:${OLLAMA_PORT:-11434}/api/tags` 성공
- [ ] `docker exec ollama nvidia-smi` 성공
- [ ] 기본 추론 요청(`/api/generate`) 성공
- [ ] Open WebUI에서 모델 조회/채팅 성공

#### Observability and Evidence Sources

- **Signals**:
  - GPU 사용률 급락(미인식), VRAM 과점유, API 에러율 증가
- **Evidence to Capture**:
  - `ollama`/`open-webui` 로그
  - 수행 명령과 결과
  - 복구 전후 지표 스냅샷

#### Safe Rollback or Recovery Procedure

- [ ] 직전 안정 모델 세트로 복원
- [ ] 임시 변경(대형 모델 상주, 디버그 설정) 제거
- [ ] 운영 정책 기준으로 자원 제한/모델 목록 재정렬

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 모델별 기본 프롬프트를 직전 안정값으로 복원
- **Model Fallback**: 장애 시 경량 모델로 자동/수동 전환
- **Tool Disable / Revoke**: 문제 모델 호출 경로 일시 차단
- **Eval Re-run**: 추론 smoke test + Open WebUI 연동 테스트 재실행
- **Trace Capture**: 장애 시간대 API/리소스 로그 보존

#### Related Operational Documents

- **Operations Policy**: `[../../05.operations/08-ai/ollama.md]`
- **Usage**: `[../../05.operations/08-ai/ollama.md]`
- **Incident examples**: `[../../05.operations/incidents/README.md]`
- **Postmortem examples**: `[../../05.operations/incidents/README.md]`
