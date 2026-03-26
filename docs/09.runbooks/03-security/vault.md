# Vault Runbook

> Step-by-step procedures for troubleshooting and maintaining the Vault security layer.

---

## Overview (KR)

이 문서는 Vault 서비스의 주요 장애 상황(Seal status, Raft Cluster Failure)에 대한 대응 절차와 정기 점검(Snapshot Backup) 방법을 다룬다.

## Runbook Type

`incident-response | maintenance`

## Target Audience

- SRE / Platform Engineers
- Security Administrators
- On-call Responders

## Incident Response

### 1. Unexpected Seal (Service Unavailable)
- **Problem**: Vault가 갑자기 `Sealed: true` 상태가 되어 모든 서비스의 인증이 중단됨.
- **Diagnosis**: 
  ```bash
  docker logs vault
  docker exec vault vault status
  ```
- **Solution**:
  1. 기 보관된 Unseal 키 관리자들을 소집한다.
  2. [Vault Guide](../../07.guides/03-security/vault.md)의 Unseal 섹션에 따라 3개 이상의 키를 입력하여 봉인을 해제한다.

### 2. Raft Cluster Partition / Peer Loss
- **Problem**: Raft 피어 간 합의(Consensus) 실패로 서비스 지연 또는 오류 발생.
- **Diagnosis**:
  ```bash
  docker exec vault vault operator raft list-peers
  ```
- **Solution**:
  - 응답이 없는 노드를 클러스터에서 제거:
    ```bash
    vault operator raft remove-peer <NODE_ID>
    ```
  - 노드 재참가: 컨테이너 재시작 후 `vault operator raft join` 수행.

## Maintenance Tasks

### 1. Raft Snapshot Backup
데이터 정성적 보존을 위해 정기적으로 스냅샷을 생성해야 함:
```bash
# Snapshot 생성
docker exec vault vault operator raft snapshot save /vault/data/backup.snapshot

# 로컬로 복사
docker cp vault:/vault/data/backup.snapshot ./backups/
```

### 2. Version Upgrade
1. Raft 스냅샷을 생성한다.
2. `docker-compose.yml`의 이미지 태그를 변경한다.
3. 컨테이너를 하나씩 재시작하며 Unseal을 수행한다.

## Related Documents

- **Guide**: `[../../07.guides/03-security/vault.md]`
- **Operation**: `[../../08.operations/03-security/vault.md]`
- **Spec**: `[../../04.specs/03-security/spec.md]`
