---
status: active
---
<!-- Target: docs/05.operations/runbooks/09-tooling/syncthing.md -->

# Syncthing Runbook

<!-- [ID:09-tooling:syncthing] -->

## Overview (KR)

이 런북은 `docs/05.operations/runbooks/09-tooling/syncthing.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

## Procedure: Syncthing Service Recovery (P2)

> Procedures for recovering from Syncthing synchronization failures and connectivity issues.

### Symptoms

- Folder status shows "Out of Sync" or "Error".
- Devices appear as "Disconnected" or "Never Seen".
- GUI inaccessible via `https://syncthing.${DEFAULT_URL}`.
- High CPU usage on small nodes during disk scanning.

### Diagnostic Steps

#### 1. Check Service Status

```bash
cd ${DEFAULT_TOOLING_DIR}/syncthing
docker compose ps
docker compose logs --tail=100 -f syncthing
```

#### 2. Verify Port Connectivity

Syncthing requires port `22000` (TCP/UDP) for data transfer. Use `nc` or `telnet` to verify.

```bash
## From another node
nc -zv <syncthing-node-ip> 22000
```

### Recovery Procedures

#### 1. Resolving "Out of Sync" Items

If specific files fail to sync:

1. Click on the **Failed Items** link in the GUI to see error details (often permission issues).
2. Fix permissions on the host filesystem if necessary.
3. Click **Actions** -> **Rescan All**.

#### 2. Repairing Corrupted Database

If the internal database is corrupted, try resetting the deltas before a full reset.

```bash
## Stop the service
docker compose stop syncthing

## Start with delta reset (Requires editing compose or temporary exec)
## Alternative: Manual removal of the index directory
sudo rm -rf ${DEFAULT_TOOLING_DIR}/syncthing/index-v0.14.0.db

## Restart service
docker compose start syncthing
```

> [!WARNING]
> Deleting the index directory will trigger a full re-scan of all synchronized folders. This may be CPU-intensive.

### 3. Resetting GUI Password

If the admin password is lost:

1. Locate the `config.xml` in `${DEFAULT_TOOLING_DIR}/syncthing`.
2. Edit the file and remove the `<user>` and `<password>` values within the `<gui>` tag.
3. Restart Syncthing; it will start without a password, and you can set a new one in the GUI.

### Escalation Policy

- **P1**: Critical sync failure for production resource data -> Notify SRE Team.
- **P2**: Intermittent connectivity or "Out of Sync" for non-critical data -> Follow manual re-scan procedures.

### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

## Procedure

### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

### Steps

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Capture command output, timestamps, and operator/agent actions for any execution of this runbook.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/09-tooling/syncthing.md)
- [Operations policy](../../policies/09-tooling/syncthing.md)

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

- Stop and escalate to the owning operator with captured evidence when the documented procedure does not match the observed failure.
