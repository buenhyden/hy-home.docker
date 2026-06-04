---
status: active
---
<!-- Target: docs/05.operations/runbooks/08-ai/gpu-recovery.md -->

# AI GPU Recovery Runbook

## AI GPU Recovery Procedure

> Scope: NVIDIA GPU acceleration for `ollama` in `infra/08-ai`.

### Overview (KR)

이 런북은 Ollama 컨테이너가 NVIDIA GPU를 인식하지 못하거나 CPU fallback으로 동작할 때 실행한다. 호스트 드라이버, NVIDIA Container Toolkit, compose device reservation을 순서대로 확인하고 복구한다.

### Purpose

- Ollama GPU 가속 경로를 빠르게 복구한다.
- Docker daemon 또는 GPU-dependent container 재시작 전에 증적과 승인 기준을 남긴다.
- 복구 후 Ollama와 Open WebUI 연동 상태를 확인한다.

### Canonical References

- **Spec**: [../../../03.specs/08-ai/spec.md](../../../03.specs/08-ai/spec.md)
- **Policy**: [../../policies/08-ai/ollama.md](../../policies/08-ai/ollama.md)
- **Guide**: [../../guides/08-ai/ollama.md](../../guides/08-ai/ollama.md)

## When to Use

- Ollama 로그에 GPU driver load failure 또는 CPU-only fallback이 나타난다.
- `docker compose exec ollama nvidia-smi`가 실패한다.
- 모델 로딩이 GPU 미할당 또는 VRAM 접근 오류로 실패한다.
- Open WebUI에서 모델 응답이 급격히 느려지고 GPU 사용률이 0에 머문다.

## Procedure

### Checklist

- [ ] 최근 GPU driver, Docker, NVIDIA Container Toolkit 변경 이력을 확인한다.
- [ ] Docker daemon 재시작이 다른 서비스에 미치는 영향을 확인하고 운영 승인을 받는다.
- [ ] `ollama`와 `open-webui` 컨테이너 상태와 로그를 캡처한다.

### Steps

1. 호스트 GPU 상태를 확인한다.

   ```bash
   nvidia-smi
   ```

2. NVIDIA Container Toolkit 경로를 검증한다.

   ```bash
   docker run --rm --runtime=nvidia --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
   ```

3. Ollama 컨테이너 내부 GPU 인식을 확인한다.

   ```bash
   docker compose exec ollama nvidia-smi
   ```

4. compose device reservation이 유지되는지 확인한다.

   ```bash
   docker inspect ollama --format '{{json .HostConfig.DeviceRequests}}'
   ```

5. toolkit은 정상이고 컨테이너만 드리프트된 경우 Ollama를 재시작한다.

   ```bash
   docker compose restart ollama
   ```

6. Docker runtime 자체가 GPU를 전달하지 못하면 승인 후 Docker daemon을 재시작한다.

   ```bash
   sudo systemctl restart docker
   ```

7. daemon 재시작 후 root compose project에서 Ollama를 다시 기동하고 GPU를 재검증한다.

   ```bash
   docker compose up -d ollama
   docker compose exec ollama nvidia-smi
   ```

### Verification Steps

- `docker compose exec ollama nvidia-smi` succeeds.
- `curl -f http://localhost:${OLLAMA_PORT:-11434}/api/tags` succeeds.
- `docker compose exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags` succeeds when Open WebUI is running.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail 200 ollama`, `docker logs --tail 200 open-webui`
- **Metrics**: GPU utilization/VRAM from `nvidia-smi`, Ollama exporter metrics when available
- **Host Evidence**: Docker daemon restart time, NVIDIA driver/toolkit version, `docker inspect` device requests

### Safe Rollback or Recovery Procedure

1. If Docker daemon restart causes broader service impact, stop further changes and escalate with captured logs.
2. If a recent model change triggered VRAM exhaustion, unload or remove the model according to [Ollama runbook](./ollama.md).
3. If GPU runtime remains unavailable after daemon restart, keep Ollama in degraded state only with explicit operator approval and route users to the incident owner.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: Switch to an approved lower-VRAM model only after operator approval.
- **Tool Disable / Revoke**: Disable automated high-concurrency inference jobs while GPU recovery is in progress.
- **Eval Re-run**: Run Ollama model list/API smoke checks after recovery.

## Evidence

- Capture command output, timestamps, operator approval for daemon restart, and before/after GPU state.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

Use only the recovery steps documented in `## Procedure`; if host GPU runtime still fails after approved daemon restart, stop changes and escalate.

## Escalation

Stop and escalate to the owning operator when host `nvidia-smi` fails, NVIDIA Container Toolkit test fails, Docker daemon restart is not approved, or service impact extends beyond `08-ai`. Include captured logs, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Ollama usage guide](../../guides/08-ai/ollama.md)
- [Ollama operations policy](../../policies/08-ai/ollama.md)
- [Ollama runbook](./ollama.md)
