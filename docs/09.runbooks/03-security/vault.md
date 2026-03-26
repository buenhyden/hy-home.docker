# Vault Runbook

: Vault Secret Management Layer

> Step-by-step procedures for troubleshooting and maintaining the Vault security layer in `hy-home.docker`.

---

## Overview (KR)

이 런북은 Vault 서비스의 주요 장애 상황(Seal status, Raft Cluster Failure)에 대한 대응 절차와 정기 점검(Snapshot Backup) 방법을 정의한다.

## Purpose

Vault의 가용성 상실(Sealed) 또는 Raft 합의 실패 상황에서 보안 관리자가 즉시 시스템을 복구할 수 있도록 돕는다.

## Canonical References

- **Spec**: [spec.md](../../04.specs/03-security/spec.md)
- **ARD**: [spec.md](../../04.specs/03-security/spec.md)

## When to Use

- Vault 서비스가 `Sealed: true` 상태일 때
- Raft 클러스터 노드 간 합의(Consensus)가 깨졌을 때
- 정기적인 데이터 백업 및 버전 업그레이드가 필요할 때

## Procedure or Checklist

### Checklist

- [ ] Unseal 키 관리자 전원 소집 (Threshold 3)
- [ ] Raft 데이터 볼륨 및 로그 가용성 확인
- [ ] Traefik 라우팅 및 헬스체크 상태 확인

### Procedure

#### 1. Unexpected Seal Recovery
1. Vault 상태를 확인한다: `docker exec vault vault status`
2. 보관된 Unseal 키를 3회 입력한다:
   ```bash
   docker exec -it vault vault operator unseal <KEY_1>
   docker exec -it vault vault operator unseal <KEY_2>
   docker exec -it vault vault operator unseal <KEY_3>
   ```

#### 2. Raft Cluster Partition Recovery
1. 피어 리스트를 확인한다: `docker exec vault vault operator raft list-peers`
2. 응답이 없는 구형 노드를 제거한다:
   ```bash
   vault operator raft remove-peer <NODE_ID>
   ```

## Verification Steps

- [ ] `docker exec vault vault status`에서 `Sealed: false` 확인
- [ ] 애플리케이션의 Vault Agent 로그에서 `successfully rendered` 메시지 확인

## Observability and Evidence Sources

- **Signals**: Prometheus `vault_core_unsealed` 메트릭, Docker Healthcheck `unhealthy` 상태
- **Evidence to Capture**: `docker logs vault`, `vault operator raft list-peers` 출력 결과

## Safe Rollback or Recovery Procedure

- 장애 복구 실패 시 직전 생성된 Raft 스냅샷을 사용하여 데이터 복구:
  ```bash
  vault operator raft snapshot restore /vault/data/backup.snapshot
  ```

## Related Operational Documents

- **Operation**: [vault.md](../../08.operations/03-security/vault.md)
- **Guide**: [vault.md](../../07.guides/03-security/vault.md)
