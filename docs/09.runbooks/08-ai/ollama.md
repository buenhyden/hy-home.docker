<!-- Target: docs/09.runbooks/08-ai/ollama.md -->

# Ollama Maintenance & Recovery Runbook

: Ollama Inference Service

---

## Overview (KR)

이 런북은 Ollama 추론 계층 장애에 대한 즉시 실행 절차를 제공한다. GPU 미인식, VRAM OOM, API 장애를 신속히 진단·복구하고 상위 서비스(Open WebUI) 영향도를 최소화한다.

## Purpose

- Ollama 추론 가용성을 빠르게 복구한다.
- GPU 경로 이상과 리소스 고갈 문제를 표준 절차로 처리한다.
- 복구 후 Open WebUI 연동 상태를 검증한다.

## Canonical References

- `[../../02.ard/0008-ai-architecture.md]`
- `[../../03.adr/0008-ollama-openwebui-local-ai.md]`
- `[../../04.specs/08-ai/spec.md]`
- `[../../05.plans/2026-03-26-08-ai-standardization.md]`

## When to Use

- Ollama API(`/api/tags`, `/api/generate`) 호출 실패.
- 컨테이너 내부 GPU 미인식 또는 CPU fallback 발생.
- 모델 로드 시 VRAM OOM으로 추론 실패.
- Open WebUI에서 모델 목록 미표시.

## Procedure or Checklist

### Checklist

- [ ] 호스트 `nvidia-smi` 정상 여부 확인
- [ ] `ollama` 컨테이너 healthcheck 확인
- [ ] 최근 모델 변경/배포 이력 확인
- [ ] Open WebUI 영향 범위 확인

### Procedure

#### 1. Initial Health & API Check

```bash
docker ps --filter name=ollama
docker logs --tail 200 ollama
curl -f http://localhost:${OLLAMA_PORT:-11434}/api/tags
```

#### 2. GPU Recognition Recovery

```bash
# 호스트 GPU 상태
nvidia-smi

# 컨테이너 내부 GPU 상태
docker exec ollama nvidia-smi

# 필요 시 컨테이너 재기동
docker restart ollama
```

#### 3. VRAM OOM Mitigation

```bash
# keep_alive=0으로 상주 모델 언로드(예시)
curl -X POST http://localhost:${OLLAMA_PORT:-11434}/api/generate -d '{
  "model": "llama3",
  "prompt": "release memory",
  "keep_alive": 0
}'
```

- 고부하 모델 사용 중이면 임시로 경량 모델로 fallback한다.

#### 4. Model Integrity Check

```bash
docker exec ollama ollama list
```

- 운영 기준 모델 태그가 존재하는지 확인한다.

#### 5. Open WebUI Dependency Recheck

```bash
# Open WebUI 컨테이너에서 Ollama 접근 확인
docker exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags
```

## Verification Steps

- [ ] `curl -f http://localhost:${OLLAMA_PORT:-11434}/api/tags` 성공
- [ ] `docker exec ollama nvidia-smi` 성공
- [ ] 기본 추론 요청(`/api/generate`) 성공
- [ ] Open WebUI에서 모델 조회/채팅 성공

## Observability and Evidence Sources

- **Signals**:
  - GPU 사용률 급락(미인식), VRAM 과점유, API 에러율 증가
- **Evidence to Capture**:
  - `ollama`/`open-webui` 로그
  - 수행 명령과 결과
  - 복구 전후 지표 스냅샷

## Safe Rollback or Recovery Procedure

- [ ] 직전 안정 모델 세트로 복원
- [ ] 임시 변경(대형 모델 상주, 디버그 설정) 제거
- [ ] 운영 정책 기준으로 자원 제한/모델 목록 재정렬

## Agent Operations (If Applicable)

- **Prompt Rollback**: 모델별 기본 프롬프트를 직전 안정값으로 복원
- **Model Fallback**: 장애 시 경량 모델로 자동/수동 전환
- **Tool Disable / Revoke**: 문제 모델 호출 경로 일시 차단
- **Eval Re-run**: 추론 smoke test + Open WebUI 연동 테스트 재실행
- **Trace Capture**: 장애 시간대 API/리소스 로그 보존

## Related Operational Documents

- **Operations Policy**: `[../../08.operations/08-ai/ollama.md]`
- **Guide**: `[../../07.guides/08-ai/ollama.md]`
- **Incident examples**: `[../../10.incidents/README.md]`
- **Postmortem examples**: `[../../11.postmortems/README.md]`
