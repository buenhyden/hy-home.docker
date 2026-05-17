<!-- [ID:08-tooling:syncthing] -->
# Syncthing Operations Policy

> Governance for P2P data synchronization and integrity.

## Overview

This policy defines the operational standards for the Syncthing service. It ensures that decentralized data synchronization is reliable, secure, and performs optimally across all paired devices.

## Scope

- **Governance**: Data sync patterns, conflict resolution rules.
- **Maintenance**: Database health, version upgrades.
- **Security**: Device pairing approval, encrypted transfer enforcement.

## Operational Standards

### 1. Data Integrity and Conflicts

- **Conflict Handling**: If a sync conflict occurs, Syncthing generates a `.sync-conflict-` file. Operators/Users must manually resolve these to ensure data consistency.
- **Ignore Patterns**: Use `.stignore` files to prevent synchronization of temporary or large log files that do not require P2P distribution.
- **Folder Type**: Use "Send Only" for master nodes (e.g., a central backup server) and "Receive Only" for immutable mirrors where appropriate.

### 2. Routine Maintenance

| Frequency | Task | Owner |
| :--- | :--- | :--- |
| **Weekly** | Check for "Out of Sync" alerts in GUI. | Operators |
| **Monthly** | Database consistency check (`-verify-db`). | Operators |
| **Quarterly** | Device pairing audit (remove stale devices). | Security |

### 3. Resource Optimization

- **CPU Usage**: Enable "Low Priority" for the scanning process on low-resource nodes.
- **Memory**: Monitor the `syncthing` process; large folder structures may require higher JVM/RAM allocation via `stateful-med` optimizations.

## Monitoring Strategy

- **Health Check**: REST API `/rest/noauth/health` returns `OK`.
- **Key Metrics**:
  - `folder_state` (Idle, Syncing, Error).
  - `device_count` (Online vs Total).
  - `throughput` (Inbound/Outbound).

## Related Documents

- **Infrastructure**: [Syncthing Service](../../../../infra/09-tooling/syncthing/README.md)
- **Usage**: [Syncthing System Usage](./syncthing.md)
- **Procedure**: [Syncthing Procedure](./syncthing.md)

---

## Overview (KR)

이 문서는 `docs/05.operations/09-tooling/syncthing.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Related Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## Usage

> Migrated from `docs/05.operations/09-tooling/syncthing.md` during the 2026-05-10 operations taxonomy consolidation.

<!-- [ID:07-tooling:syncthing] -->
### Syncthing System Usage

> Usage for real-time, secure peer-to-peer file synchronization.

#### Overview

Syncthing is the platform's decentralized solution for file synchronization. It allows for secure data replication across infrastructure nodes and personal devices without relying on third-party cloud providers.

#### Architecture Context

- **Endpoint**: `https://syncthing.${DEFAULT_URL}`
- **Protocol**: BEP (Block Exchange Protocol)
- **Local Discovery**: UDP Broadcast on port 21027
- **Data Transfer**: TCP/UDP on port 22000

#### How-to Procedures

##### 1. Accessing the GUI

1. Navigate to `https://syncthing.${DEFAULT_URL}`.
2. Log in using the platform credentials (`SYNCTHING_USERNAME`).
3. Note your **Device ID** via **Actions** -> **Show ID**.

##### 2. Pairing a New Device

To sync files with another device:

1. Obtain the **Device ID** of the remote device.
2. In the Syncthing GUI, click **Add Remote Device**.
3. Paste the Device ID and give it a recognizable **Device Name**.
4. Click **Save**.
5. On the remote device, a notification will appear; click **Add Device** to confirm the pairing.

##### 3. Sharing the Sync Folder

1. Click **Add Folder** or edit an existing one (e.g., `Default Folder`).
2. Ensure the **Folder Path** is correctly set (usually `/var/syncthing/` or specifically `/Sync` for resource data).
3. In the **Sharing** tab, check the box for the remote device(s) you want to sync with.
4. Click **Save**.
5. The remote device will receive a request to join the folder; accept it to begin synchronization.

#### Troubleshooting & Pitfalls

##### "Out of Sync" State

**Symptom**: Folder status shows "Out of Sync" even after recent changes.

**Solution**:

1. Check the **Failed Items** link for specific file errors (e.g., permissions).
2. Use **Actions** -> **Rescan All** to force a file system check.
3. If persistent, refer to the [Procedure](./syncthing.md) for database reset procedures.

##### Connection Failures

**Symptom**: Devices show as "Disconnected".

**Solution**:

1. Ensure port `22000` (TCP/UDP) is open between devices.
2. Verify that **Global Discovery** and **Relaying** are enabled if devices are on different networks.

#### Related Documents

- **Infrastructure**: [Syncthing Service](../../../../infra/09-tooling/syncthing/README.md)
- **Operation**: [Syncthing Operations Policy](./syncthing.md)
- **Procedure**: [Syncthing Procedure](./syncthing.md)

---

#### Overview (KR)

이 문서는 `docs/05.operations/09-tooling/syncthing.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- AI Agent

#### Purpose

관련 인프라 서비스나 문서 영역을 이해하고 안전하게 변경 또는 운영할 수 있도록 돕는다.

#### Prerequisites

- Repository root README 확인
- 관련 `infra/` 서비스 README 확인
- 필요한 경우 대응 operation/runbook 문서 확인

#### Step-by-step Instructions

1. 관련 README와 기존 본문을 먼저 읽는다.
2. 실제 compose/config 경로와 문서 설명이 일치하는지 확인한다.
3. 변경이 필요하면 대응 템플릿과 상위 README 링크를 함께 갱신한다.
4. 관련 검증 스크립트 또는 문서 audit를 실행한다.

#### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

#### Related Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## Procedure

> Migrated from `docs/05.operations/09-tooling/syncthing.md` during the 2026-05-10 operations taxonomy consolidation.

<!-- [ID:09-tooling:syncthing] -->
### Procedure: Syncthing Service Recovery (P2)

> Procedures for recovering from Syncthing synchronization failures and connectivity issues.

#### Symptoms

- Folder status shows "Out of Sync" or "Error".
- Devices appear as "Disconnected" or "Never Seen".
- GUI inaccessible via `https://syncthing.${DEFAULT_URL}`.
- High CPU usage on small nodes during disk scanning.

#### Diagnostic Steps

##### 1. Check Service Status

```bash
cd ${DEFAULT_TOOLING_DIR}/syncthing
docker compose ps
docker compose logs --tail=100 -f syncthing
```

##### 2. Verify Port Connectivity

Syncthing requires port `22000` (TCP/UDP) for data transfer. Use `nc` or `telnet` to verify.

```bash
### From another node
nc -zv <syncthing-node-ip> 22000
```

#### Recovery Procedures

##### 1. Resolving "Out of Sync" Items

If specific files fail to sync:

1. Click on the **Failed Items** link in the GUI to see error details (often permission issues).
2. Fix permissions on the host filesystem if necessary.
3. Click **Actions** -> **Rescan All**.

##### 2. Repairing Corrupted Database

If the internal database is corrupted, try resetting the deltas before a full reset.

```bash
### Stop the service
docker compose stop syncthing

### Start with delta reset (Requires editing compose or temporary exec)
### Alternative: Manual removal of the index directory
sudo rm -rf ${DEFAULT_TOOLING_DIR}/syncthing/index-v0.14.0.db

### Restart service
docker compose start syncthing
```

> [!WARNING]
> Deleting the index directory will trigger a full re-scan of all synchronized folders. This may be CPU-intensive.

##### 3. Resetting GUI Password

If the admin password is lost:

1. Locate the `config.xml` in `${DEFAULT_TOOLING_DIR}/syncthing`.
2. Edit the file and remove the `<user>` and `<password>` values within the `<gui>` tag.
3. Restart Syncthing; it will start without a password, and you can set a new one in the GUI.

#### Escalation Policy

- **P1**: Critical sync failure for production resource data -> Notify SRE Team.
- **P2**: Intermittent connectivity or "Out of Sync" for non-critical data -> Follow manual re-scan procedures.

#### Related Documents

- **Infrastructure**: [Syncthing Service](../../../../infra/09-tooling/syncthing/README.md)
- **Usage**: [Syncthing System Usage](./syncthing.md)
- **Operation**: [Syncthing Operations Policy](./syncthing.md)

---

#### Overview (KR)

이 런북은 `docs/05.operations/09-tooling/syncthing.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

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
