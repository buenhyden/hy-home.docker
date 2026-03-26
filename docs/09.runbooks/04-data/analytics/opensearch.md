<!-- Target: docs/09.runbooks/04-data/analytics/opensearch.md -->

# OpenSearch Recovery Runbook

: OpenSearch Cluster Maintenance

---

## Overview (KR)

이 런북은 OpenSearch 클러스터 장애 발생 시 대응 절차를 정의한다. 클러스터 상태(Yellow/Red) 복구, 디스크 부족 해결, 인증서 갱신 단계를 제공한다.

## Purpose

OpenSearch 서비스 중단 또는 성능 저하 발생 시 운영자가 신속하게 서비스를 정상화하도록 돕는다.

## Canonical References

- `[../../02.ard/04-data-tier.md]`
- `[../../../07.guides/04-data/analytics/opensearch.md]`
- `[../../../08.operations/04-data/analytics/opensearch.md]`

## When to Use

- 클러스터 헬스 체크 상태가 `red` 일 때.
- 샤드 할당 실패로 인해 인덱스 쓰기가 불가능할 때.
- 인증서 만료로 인해 노드 간 통신이 단절되었을 때.

## Procedure or Checklist

### Checklist

- [ ] `curl -k https://opensearch:9200/_cluster/health` 결과 확인.
- [ ] Docker logs (`docker compose logs opensearch`) 확인.
- [ ] 디스크 여유 공간 (`df -h`) 확인.

### Procedure

#### 1. Cluster Health Recovery (Unassigned Shards)
클러스터가 `red` 상태인 경우 할당되지 않은 샤드를 확인하고 재할당을 시도한다.
```bash
# 할당되지 않은 샤드 확인
curl -X GET "https://opensearch:9200/_cat/shards?v=true&h=index,shard,prirep,state,unassigned.reason" -u admin:<password> --insecure

# 샤드 재할당 시도 (필요시)
curl -X POST "https://opensearch:9200/_cluster/reroute?retry_failed=true" -u admin:<password> --insecure
```

#### 2. Local Storage Cleanup
디스크 사용량이 85% (Low Watermark) 이상인 경우 오래된 인덱스를 삭제하거나 삭제 정책을 적용한다.
```bash
# 인덱스별 용량 확인
curl -X GET "https://opensearch:9200/_cat/indices?v&s=store.size:desc" -u admin:<password> --insecure
```

## Verification Steps

- [ ] `/_cluster/health` 결과가 `green` 또는 `yellow`로 복구되었는가?
- [ ] Dashboards UI 로그인 및 데이터 조회가 정상적인가?

## Related Operational Documents

- **Incident examples**: `[N/A]`
- **Postmortem examples**: `[N/A]`
