# Security Runbook (03-security)

> Vault Maintenance & Incident Recovery (03-security)

## Overview

이 런북은 `hy-home.docker`의 보안 인프라(03-security)에서 발생할 수 있는 주요 장애 상황과 정기 유지보수 절차를 정의한다.

## Purpose

Vault의 가용성을 유지하고, 봉인 상태 해제 및 데이터 복구를 신속하게 수행하기 위함이다.

---

## Recovery Procedures

### 1. Vault 봉인 해제 (Unseal)

Vault 컨테이너가 재시작되었거나 수동으로 봉인된 경우 수행한다.

1. **상태 확인**:
   ```bash
   docker exec vault vault status
   ```
2. **키 입력 (3회)**:
   ```bash
   docker exec -it vault vault operator unseal <KEY_1>
   docker exec -it vault vault operator unseal <KEY_2>
   docker exec -it vault vault operator unseal <KEY_3>
   ```
3. **상태 재확인**: `Sealed: false`인지 확인한다.

### 2. Raft 데이터 백업 및 복구

1. **스냅샷 생성**:
   ```bash
   docker exec vault vault operator raft snapshot save /vault/data/backup_$(date +%F).snapshot
   ```
2. **복구 (Restore)**:
   ```bash
   docker exec vault vault operator raft snapshot restore /vault/data/your_snapshot.snapshot
   ```
   > [!WARNING]
   > 복구 작업은 현재의 모든 데이터를 스냅샷 시점으로 덮어쓰므로 극도로 주의해야 함.

### 3. Unseal Key 조각 분실 대응

키 조각 중 일부(2개 이하)를 분실한 경우, 나머지 3개를 사용하여 즉시 **키 재생성(Rekey)**을 수행해야 한다.

1. **Rekey 프로세스 시작**:
   ```bash
   docker exec -it vault vault operator rekey -init -key-shares=5 -key-threshold=3
   ```
2. **기존 키 입력**: 나머지 관리자들이 각자의 키를 입력한다.
3. **새 키 생성**: 완료 후 새로 생성된 5개의 조각을 다시 분산 보관한다.

---

## Maintenance Tasks

- **Audit Log 전송 확인**: 로그 파일이 회전되거나 소실되지 않는지 점검.
- **Raft Peer 상태 점검**: `vault operator raft list-peers` 명령어로 클러스터 건강 상태 확인.

## Verification Steps

- [ ] `wget http://localhost:8200/v1/sys/health` 응답 200 확인.
- [ ] Vault Dashboard 로그인 및 데이터 접근 테스트.

## Related Operational Documents

- **Operations Policy**: `[../../08.operations/03-security/README.md]`
- **Setup Guide**: `[../../07.guides/03-security/01.setup.md]`
