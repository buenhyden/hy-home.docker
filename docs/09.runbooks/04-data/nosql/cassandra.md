<!-- Target: docs/09.runbooks/04-data/nosql/cassandra.md -->

# Apache Cassandra Recovery Runbook

: `cassandra-node1`

> Cassandra 서비스 장애 상황 발생 시 즉각적인 복구 및 데이터 복원을 위한 실행 절차.

---

## Overview (KR)

이 런북은 Cassandra 노드 다운, 데이터 오염 또는 패스워드 분실 등의 긴급 상황에서 운영자가 즉시 수행해야 할 단계를 정의한다.

## Purpose

서비스 중단 시간을 최소화하고 데이터 손실 없이 Cassandra 엔진을 정상 상태로 복구한다.

## Canonical References

- **ARD**: [04-data Architecture](../../../docs/02.ard/0004-data-architecture.md)
- **Operation**: [Cassandra Operations Policy](../../../docs/08.operations/04-data/nosql/cassandra.md)
- **Guide**: [Cassandra System Guide](../../../docs/07.guides/04-data/nosql/cassandra.md)

## When to Use

- `cassandra-node1` 컨테이너가 비정상 종료되었거나 재시작이 반복될 때.
- `nodetool status` 결과 노드가 `DN` (Down) 상태로 표시될 때.
- 디스크 공간 부족으로 쓰기 작업이 거부될 때.

## Procedure or Checklist

### Checklist

- [ ] `docker logs cassandra-node1` 명령으로 에러 메시지 확인.
- [ ] 호스트 시스템의 남은 디스크 용량 확인 (`df -h`).
- [ ] Docker Secret `cassandra_password` 파일 존재 여부 확인.

### Procedure

#### 1. 노드 재시작 및 상태 강제 동기화

일시적인 네트워크 지연이나 메모리 부족 시 컨테이너를 재배포한다.

```bash
docker compose -f infra/04-data/nosql/cassandra/docker-compose.yml restart cassandra-node1
```

#### 2. 데이터 손상 시 스냅샷 복구

호스트 볼륨의 데이터를 백업 시점으로 복원한다.

1. 서비스 중지: `docker compose stop cassandra-node1`
2. 데이터 디렉터리(`node1/data`)를 백업본으로 교체.
3. 서비스 시작 및 리페어 수행: `docker exec -it cassandra-node1 nodetool repair`

#### 3. 디스크 공간 부족 대응

불필요한 스냅샷을 제거하여 공간을 확보한다.

```bash
docker exec -it cassandra-node1 nodetool clearsnapshot
```

## Verification Steps

- [ ] `nodetool status` 결과에서 `UN` (Up Normal) 상태 확인.
- [ ] `cqlsh` 접속 후 간단한 `DESCRIBE KEYSPACES` 쿼리 가능 여부 체크.

## Observability and Evidence Sources

- **Signals**: Prometheus Alert `CassandraNodeDown` / `CassandraHighHeapUsage`.
- **Evidence to Capture**: `docker logs --tail 200 cassandra-node1` 출력물, `nodetool info` 결과.

## Safe Rollback or Recovery Procedure

- 복구 실패 시, `infra/` 경로의 `docker-compose.yml` 설정을 초기 상태로 되돌리고 `DEFAULT_DATA_DIR`의 완전한 이전 백업본을 사용하여 복원한다.

## Related Operational Documents

- **Runbook Index**: [Data Tier Runbooks](../README.md)
- **Monitoring**: Grafana Cassandra Dashboard
