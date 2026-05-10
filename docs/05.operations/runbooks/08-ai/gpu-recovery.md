---
status: migrated
---
<!-- Target: docs/05.operations/runbooks/08-ai/gpu-recovery.md -->

# Gpu Recovery Operations

> Migrated from `docs/05.operations/08-ai/gpu-recovery.md` during the 2026-05-10 operations taxonomy consolidation.

## Procedure

### GPU Recovery Procedure

Procedures for restoring NVIDIA GPU acceleration if containers fail to detect the hardware.

#### 1. Symptom

- Ollama logs show "CPU only" or "Failed to load NVIDIA driver".
- `nvidia-smi` fails inside the container.

#### 2. Verification Steps (Host)

Check if the NVIDIA Container Toolkit is healthy:

```bash
nvidia-smi
docker run --rm --runtime=nvidia --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
```

#### 3. Recovery Procedure

1. **Restart Docker Service**:

   ```bash
   sudo systemctl restart docker
   ```

2. **Recreate Container**:

   ```bash
   docker-compose down ollama
   docker-compose up -d ollama
   ```

3. **Verify Reservation**: Check `docker inspect ollama` and look for `DeviceRequests`.

#### 4. Escalation

If hardware failure is suspected, check host kernel logs:

```bash
dmesg | grep -i nvidia
```

---

#### Overview (KR)

이 런북은 `docs/05.operations/08-ai/gpu-recovery.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

#### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

#### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

#### When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

#### Procedure or Checklist

##### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

##### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

#### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/incidents/README.md](../../incidents/README.md)
