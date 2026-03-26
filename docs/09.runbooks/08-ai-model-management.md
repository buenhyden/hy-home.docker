<!-- Target: docs/09.runbooks/08-ai-model-management.md -->

# 08-ai Model Management Runbook

## Overview (KR)

이 런북은 `08-ai` 계층의 모델 파일 관리, 백업, 복구 및 성능 문제 해결을 위한 절차를 기술한다.

## Tasks

### 1. Model Pull & Backup
신규 모델을 내려받거나 기존 모델을 백업하는 절차이다.

- **Download**:
  ```bash
  docker exec -it ollama ollama pull <model_name>
  ```
- **Backup**:
  모델 파일은 호스트의 `${DEFAULT_AI_MODEL_DIR}/ollama`에 저장된다. 해당 디렉토리를 압축하여 외부 스토리지로 복사한다.
  ```bash
  tar -cvf ai-models-backup-$(date +%F).tar ${DEFAULT_AI_MODEL_DIR}/ollama
  ```

### 2. Recovery from Crash
Ollama 또는 Open WebUI가 응답하지 않을 때의 복구 절차이다.

1. **상태 확인**:
   ```bash
   docker ps | grep ai
   ```
2. **로그 확인**:
   ```bash
   docker logs ollama --tail 50
   ```
3. **재시작**:
   ```bash
   docker compose restart ollama open-webui
   ```

### 3. GPU Out-of-Memory (OOM) Handling
VRAM 부족으로 추론이 실패할 경우의 대응 방안이다.

1. **VRAM 점유 확인**: `nvidia-smi`를 사용하여 어떤 모델이 VRAM을 점유 중인지 확인한다.
2. **프로세스 킬**: 필요 시 Ollama 컨테이너 내의 `ollama serve` 프로세스를 재시작하여 메모리를 초기화한다.
3. **모델 교체**: 더 작은 파라미터 또는 더 높은 양자화(Quantization) 수준의 모델 사용을 고려한다.

## Frequency
- **Daily**: 서비스 헬스 체크 자동화 모니터링.
- **Monthly**: 미사용 모델 정리 및 디스크 용량 점검.

## Related Documents

- **Operations**: [../../08.operations/08-ai-operational-policy.md](../../08.operations/08-ai-operational-policy.md)
- **Spec**: [../../04.specs/08-ai/spec.md](../../04.specs/08-ai/spec.md)
