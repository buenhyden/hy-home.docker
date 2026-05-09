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

## Related References

- **Infrastructure**: [Syncthing Service](../../../infra/09-tooling/syncthing/README.md)
- **Guide**: [Syncthing System Guide](../../07.guides/09-tooling/syncthing.md)
- **Runbook**: [Syncthing Runbook](../../09.runbooks/09-tooling/syncthing.md)

---

## Overview (KR)

이 문서는 `docs/08.operations/09-tooling/syncthing.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

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

- [../README.md](../README.md)
- [../../07.guides/README.md](../../07.guides/README.md)
- [../../09.runbooks/README.md](../../09.runbooks/README.md)
