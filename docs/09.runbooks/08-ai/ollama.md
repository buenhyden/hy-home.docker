# Ollama Maintenance & Recovery Runbook

: Ollama Inference Service

---

## Overview (KR)

이 런북은 Ollama 추론 엔진에서 발생할 수 있는 GPU 가속 실패, 메모리 부족(OOM), 그리고 API 통신 장애에 대한 즉각적인 대응 절차를 정의한다.

## Purpose

추론 서비스의 가용성을 유지하고, 장애 발생 시 최단 시간 내에 GPU 가속 기능을 복구한다.

## Canonical References

- `[../02.ard/08-ai/llm-inference.md]` (TBD)
- [Ollama Operations Policy](../../08.operations/08-ai/ollama.md)
- [Ollama System Guide](../../07.guides/08-ai/ollama.md)

## When to Use

- 컨테이너 내부에서 GPU를 인식하지 못할 때 (CPU 추론으로 전환됨)
- 모델 로드 중 `Out of Memory` 에러가 발생할 때
- `Open WebUI` 등 상위 서비스에서 Ollama로의 연결이 실패할 때

## Procedure or Checklist

### Checklist

- [ ] 호스트의 `nvidia-smi` 결과가 정상인가?
- [ ] `ollama` 컨테이너의 헬스체크 상태가 `healthy` 인가?
- [ ] VRAM 잔여 용량이 로드하려는 모델 크기보다 충분한가?

### Procedure

#### 1. GPU 가속 복구 (GPU Lost)

```bash
# 1. 호스트 드라이버 상태 확인
nvidia-smi

# 2. 컨테이너 GPU 인식 재시도 (재생성)
cd infra/08-ai/ollama
docker compose up -d --force-recreate

# 3. 내부 인식 확인
docker exec -it ollama nvidia-smi
```

#### 2. VRAM OOM 강제 해제

모델이 메모리에 상주하여 새로운 모델을 로드할 수 없는 경우:

```bash
# 특정 모델 언로드 (API 호출)
curl -X POST http://localhost:11434/api/generate -d '{"model": "llama3", "keep_alive": 0}'

# 또는 Ollama 서비스 재시작 (모든 모델 언로드)
docker restart ollama
```

#### 3. API 통신 장애 점검

```bash
# 컨테이너 네트워크 로그 확인
docker logs ollama

# 로컬 API 호출 테스트
curl -i http://localhost:11434/api/tags
```

## Verification Steps

- [x] `nvidia-smi` 명령어 결과에 `ollama` 프로세스가 표시되는지 확인.
- [x] `ollama list` 결과에 대상 모델이 존재하는지 확인.

## Safe Rollback or Recovery Procedure

- 장애 복구 실패 시, `01-gateway`에서 해당 경로를 유지보수 페이지로 전환한다.
- 하드웨어 장애(GPU Fault)가 의심될 경우 시스템 로그(`dmesg`)를 확인하고 호스트 재부팅을 검토한다.

## Related Operational Documents

- **Incident examples**: `[../10.incidents/README.md]`
- **Postmortem examples**: `[../11.postmortems/README.md]`
