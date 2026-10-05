---
title: "AI GPU Recovery Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0055"
created: "2026-03-25"
---

# AI GPU Recovery Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### Overview

> Scope: `infra/08-ai`의 `ollama` NVIDIA GPU 가속 복구.

이 런북은 Ollama 컨테이너가 NVIDIA GPU를 인식하지 못하거나 CPU fallback으로 동작할 때 실행한다. 호스트 드라이버, NVIDIA Container Toolkit, compose device reservation을 순서대로 확인하고 복구한다.

### Purpose

- Ollama GPU 가속 경로를 빠르게 복구한다.
- Docker daemon 또는 GPU-dependent container 재시작 전에 증적과 승인 기준을 남긴다.
- 복구 후 Ollama와 Open WebUI 연동 상태를 확인한다.

### When to Use

- Ollama 로그에 GPU driver load failure 또는 CPU-only fallback이 나타난다.
- `docker compose exec ollama nvidia-smi`가 실패한다.
- 모델 로딩이 GPU 미할당 또는 VRAM 접근 오류로 실패한다.
- Open WebUI에서 모델 응답이 급격히 느려지고 GPU 사용률이 0에 머문다.

## Procedure

### Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### Checklist

- [ ] 최근 GPU driver, Docker, NVIDIA Container Toolkit 변경 이력을 확인한다.
- [ ] Docker daemon 재시작이 다른 서비스에 미치는 영향을 확인하고 운영 승인을 받는다.
- [ ] `ollama`와 `open-webui` 컨테이너 상태와 로그를 캡처한다.

### Steps

1. 호스트 GPU 상태를 확인한다.

   ```bash
   nvidia-smi
   ```

2. 호스트 driver와 호환되는 승인된 CUDA 진단 image를 `GPU_DIAGNOSTIC_IMAGE`로 지정한 뒤 NVIDIA Container Toolkit 경로를 검증한다. Image tag 또는 digest는 운영자가 사용하는 driver 호환성 기준에서 선택한다.

   ```bash
   : "${GPU_DIAGNOSTIC_IMAGE:?Set an approved CUDA diagnostic image compatible with the host driver}"
   docker run --rm --runtime=nvidia --gpus all "$GPU_DIAGNOSTIC_IMAGE" nvidia-smi
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

- `docker compose exec ollama nvidia-smi`가 성공한다.
- `curl -f http://localhost:${OLLAMA_HOST_PORT:-11434}/api/tags`가 성공한다.
- `docker compose exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags`가 실행 중인 Open WebUI에서 성공한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail 200 ollama`, `docker logs --tail 200 open-webui`
- **Metrics**: `nvidia-smi`의 GPU 사용률·VRAM과 제공되는 Ollama exporter 지표
- **Host Evidence**: Docker daemon 재시작 시각, NVIDIA driver·toolkit 버전, `docker inspect`의 device 요청

### Safe Rollback or Recovery Procedure

1. Docker daemon 재시작이 더 넓은 서비스에 영향을 주면 추가 변경을 멈추고 정제된 로그로 에스컬레이션한다.
2. 최근 모델 변경이 VRAM 고갈을 일으켰다면 [Ollama Runbook](0056-ollama.md)의 승인 경계에서 unload 또는 제거한다.
3. 승인된 daemon 재시작 뒤에도 GPU를 사용할 수 없으면 명시적 owner 승인 아래에서만 degraded 상태를 유지하고 사용자를 Incident 소유자에게 안내한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: GPU runtime은 prompt를 소유하지 않으므로 적용하지 않는다.
- **Model Fallback**: 운영자 승인 후에만 승인된 낮은 VRAM 모델로 전환한다.
- **Tool Disable / Revoke**: 복구 중 자동 고동시성 추론을 중단한다.
- **Eval Re-run**: 복구 후 목록/API와 별도 승인된 추론 검증을 수행한다.

## Verification

### Evidence

- 명령·시각, daemon 재시작 승인과 GPU 전후 상태를 기록한다.
- 실패 검사·증상과 최종 복구 또는 에스컬레이션 상태를 Task/Incident에 남긴다.

## Rollback and Escalation

### Rollback or Recovery

`## Procedure`에 기록된 복구만 사용한다. 승인된 daemon 재시작 뒤에도 host GPU runtime이 실패하면 추가 변경을 멈추고 에스컬레이션한다.

### Escalation

Host `nvidia-smi`, NVIDIA Container Toolkit 검사 실패, daemon 재시작 승인 부재 또는 `08-ai` 밖 영향이면 중단하고 @buenhyden에게 넘긴다. 정제된 로그, 시도한 단계와 현재 복구 상태를 전달한다.

### Traceability

- Governing authority: [AI Infrastructure Architecture Description](../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: `0055` 번호를 공유하는 Guide·Policy는 없다.

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Ollama usage guide](../guides/0056-ollama.md)
- [Ollama operations policy](../policies/0056-ollama.md)
- [Ollama runbook](0056-ollama.md)
