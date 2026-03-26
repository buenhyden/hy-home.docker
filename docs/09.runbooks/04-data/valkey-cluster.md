# Valkey Cluster Recovery Runbook

: `valkey-cluster`

---

## Overview (KR)

이 런북은 Valkey Cluster에서 발생할 수 있는 노드 장애, 슬롯 불일치 및 네트워크 파티션 상황에 대한 긴급 복구 절차를 정의합니다.

## Purpose

장애 상황에서 클러스터를 정상 상태(`cluster_state:ok`)로 신속히 복구하고 데이터 무결성을 보장합니다.

## Canonical References

- **PRD**: [2026-03-26-04-data.md](../../01.prd/2026-03-26-04-data.md)
- **ARD**: [0004-data-architecture.md](../../02.ard/0004-data-architecture.md)
- **Spec**: [spec.md](../../04.specs/04-data/spec.md)
- **Operation**: [valkey-cluster.md](../../08.operations/04-data/valkey-cluster.md)
- **Guide**: [valkey-cluster.md](../../07.guides/04-data/valkey-cluster.md)

## When to Use

- `cluster_state:fail` 상태가 감지될 때
- `cluster_slots_assigned`가 16384 미만일 때
- 프라이머리 노드 다운 후 자동 페일오버가 실패했을 때

## Procedure or Checklist

### Checklist

- [ ] 모든 Valkey 노드 컨테이너가 Running 상태인지 확인
- [ ] 노드 간 네트워크 통신이 가능한지 확인
- [ ] 마스터 패스워드(`service_valkey_password`)가 유효한지 확인

### Procedure

#### 1. 클러스터 상태 진단

```bash
docker exec valkey-node-0 valkey-cli -a $PASS --cluster check localhost:6379
```

#### 2. 슬롯 자동 복구 (Inconsistent Slots)

슬롯 할당 불일치 시 다음 명령을 통해 자동으로 슬롯을 재할당하거나 수정합니다.

```bash
docker exec valkey-node-0 valkey-cli -a $PASS --cluster fix localhost:6379
```

#### 3. 실패한 노드 수동 리셋 (Node Recovery)

복구된 노드가 클러스터에 합류하지 못할 경우:

```bash
# 해당 노드에서
docker exec [failed-node] valkey-cli -a $PASS cluster reset soft
# 마스터 노드에서 다시 추가
docker exec valkey-node-0 valkey-cli -a $PASS --cluster add-node [new-ip]:[port] [master-ip]:[port]
```

## Verification Steps

- [ ] `valkey-cli cluster info | grep cluster_state` 결과가 `ok`인지 확인
- [ ] `valkey-cli cluster nodes` 결과 모든 노드가 `connected` 상태인지 확인

## Observability and Evidence Sources

- **Signals**: Prometheus Alert `ValkeyClusterDown`
- **Evidence to Capture**: `valkey-cli cluster nodes` 출력 결과, 노드 에러 로그

## Safe Rollback or Recovery Procedure

- 클러스터 데이터 손상이 심각할 경우, 모든 노드를 중지하고 데이터 볼륨의 백업본(RDB/AOF)을 복원한 후 클러스터를 재구성합니다.
