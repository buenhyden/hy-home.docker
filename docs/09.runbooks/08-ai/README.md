# AI Runbook (08-ai)

> NVIDIA Driver Issues, VRAM OOM & Inference Recovery

## Overview

이 런북은 `08-ai` 계층에서 발생할 수 있는 GPU 가속 실패 및 추론 엔진 장애에 대한 대응 방법을 설명한다.

## Emergency Procedures

### 1. NVIDIA 드라이버 인식 실패 (GPU Lost)

컨테이너 내부에서 GPU를 인식하지 못하고 CPU 추론으로 전환되는 경우.

1. **Host 점검**: 호스트에서 `nvidia-smi`를 실행하여 드라이버 상태 확인.
2. **Toolkit 재시작**: NVIDIA Container Toolkit 상태를 확인하고 필요 시 다시 설치/재시작.
3. **컨테이너 재생성**: `docker compose up -d --force-recreate` 명령으로 GPU 예약 재시도.

### 2. VRAM Out-of-Memory (OOM)

대규모 모델을 로드하거나 동시 요청이 많아 GPU 메모리가 부족할 때.

1. **모델 언로드**: `curl -X POST http://ollama:11434/api/generate -d '{"model": "name", "keep_alive": 0}'`를 통해 강제 언로드.
2. **Ollama 재시작**: 좀비 메모리 프로세스가 남은 경우 Ollama 컨테이너를 재시작.
3. **모니터링**: `ollama-exporter`를 통해 VRAM 점유 추이를 분석하고 정책 재검토.

### 3. Open WebUI와 Ollama 간 통신 장애

채팅창에서 'Service Unavailable' 에러가 발생하는 경우.

1. **네트워크 확인**: `infra_net` 상에서 `ollama` 호스트로의 `ping` 및 `curl` 테스트.
2. **Healthcheck 점검**: Ollama의 헬스체크가 통과하고 있는지 확인.

---

## Verification Steps

- [ ] `docker exec -it ollama nvidia-smi`를 통한 CUDA 가속 확인.
- [ ] `ollama pull` 및 `ollama run`을 통한 기본 추론 동작 확인.

## Related Operational Documents

- [Operations Policy](../../docs/08.operations/08-ai/README.md)
- [Inference Guide](../../docs/07.guides/08-ai/01.llm-inference.md)
