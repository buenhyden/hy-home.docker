---
title: "Pushgateway Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0046"
parent_ids:
- "POL-0046"
implementation_services:
  infra/06-observability/docker-compose.yml:
  - pushgateway
created: "2026-05-10"
---

# Pushgateway Usage Guide

## Usage

### Overview

이 문서는 Pushgateway의 역할과 기본 사용법을 설명한다. Pushgateway는 Prometheus pull 모델이 직접 적용되기 어려운 short-lived or batch job metric을 일시적으로 받아 두는 버퍼이며, 장기 실행 서비스의 일반 metric 수집 경로로 쓰지 않는다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- Agent-tuner

### Purpose

Pushgateway의 역할과 동작 방식을 이해하고, 배치 작업에서 메트릭을 올바르게 전송하고 관리하는 방법을 익힌다.

### Prerequisites

- `pushgateway` service가 `obs` 또는 `batch-metrics` profile에서 실행 중이어야 한다.
- 작업이 `obs_net` 또는 Pushgateway에 도달할 수 있는 네트워크 경로에 있어야 한다.
- Prometheus에 의존하는 dashboard or alert를 만들기 전에는 `prometheus.yml`의 Pushgateway scrape job 존재를 확인해야 한다.

### Step-by-step Instructions

#### 1. 서비스 도달성 확인

기존 승인된 `obs_net` client에서 ready endpoint를 확인한다. Compose DNS는 host shell에서 해석된다고 가정하지 않는다; gateway redirect는 backend readiness 성공이 아니다.

```bash
curl -I http://pushgateway:9091/-/ready
```

#### 2. 메트릭 전송

배치 작업 종료 시 또는 주기적으로 HTTP POST/PUT을 사용하여 metric을 push한다. 모든 path에는 안정적인 `job` label을 포함한다.

```bash
echo "batch_job_duration_seconds 120" | curl --data-binary @- http://pushgateway:9091/metrics/job/my_batch_job
```

고유 worker를 구분해야 할 때만 bounded `instance` label을 사용한다.

```bash
cat <<EOF | curl --data-binary @- http://pushgateway:9091/metrics/job/my_batch_job/instance/worker-01
# HELP batch_process_items Total items processed by batch.
# TYPE batch_process_items counter
batch_process_items 1500
EOF
```

#### 3. Prometheus scrape 연동 확인

Prometheus dashboard or alert가 Pushgateway metric에 의존하기 전에는 `prometheus.yml`에 Pushgateway scrape job이 있는지 확인한다. 현재 문서 정리 범위는 runtime 설정 변경이 아니므로, scrape job이 없으면 gap으로 기록하고 별도 작업에서 추가한다.

```bash
rg -n 'job_name: "pushgateway"|pushgateway:9091|honor_labels' infra/06-observability/prometheus/config/prometheus.yml
```

#### 4. 메트릭 삭제

실행 중에는 metric TTL이 없어 마지막 값을 유지하지만 현재 persistence가 없어 process restart 시 사라진다. 종료된 group 정리는 [RUN-0046](../runbooks/0046-pushgateway.md)의 승인된 정확한 grouping-key 절차를 따른다. 아래는 job-only group 예시이며 instance 하위 group을 cascade 삭제하지 않는다.

```bash
curl -X DELETE http://pushgateway:9091/metrics/job/my_batch_job
```

### Common Pitfalls

- **Stale metrics**: Pushgateway는 마지막 값을 유지한다. 실패한 배치가 metric을 갱신하지 못하면 오래된 성공 값이 계속 보일 수 있다.
- **Label collision**: 여러 worker가 같은 `job`만 사용하면 metric group이 덮어써질 수 있다. worker 구분이 필요할 때만 안정적인 `instance` label을 추가한다.
- **High cardinality**: user ID, request ID, unbounded build ID를 label에 넣으면 cleanup이 어려워지고 메모리 사용량이 커진다.
- **Scrape assumption**: Pushgateway service가 떠 있어도 Prometheus scrape job이 없으면 Prometheus target이나 alert에서 해당 metric을 볼 수 없다.

### Source-backed operating contract

- **목적·분류·구현 소유권**: `pushgateway`는 `OPTIONAL` batch metric 중계 서비스이며 `obs`/`batch-metrics`로 선택한다. [Compose](../../../infra/06-observability/docker-compose.yml)가 구현을 소유한다.
- **흐름·의존성·보안**: 승인된 단기 job이 metric을 push하고 Prometheus가 이를 scrape한다. Traefik이 UI/API route를 보호하지만 producer 인가와 metric-label 관리 규칙은 여전히 필요하다. Prometheus, gateway/auth와 `obs_net`이 의존성이다.
- **상태**: 현재 Compose에는 volume과 `--persistence.file`이 선언되어 있지 않다. metric은 process memory에 있으며 restart하면 사라진다. Docker Secret은 없다. 현재 Pushgateway 내용을 영속적이거나 정확히 복구할 수 있다고 설명하지 않는다.
- **자원·정상 사용**: source limit은 여유 용량을 뜻하지 않는다. 저장소 root에서 렌더링하고 batch 용도로만 시작한다. label을 붙인 test group을 push하여 Prometheus scrape를 확인하고, producer가 완료되면 오래된 group을 삭제한다.
- **수명 주기·복구**: backup 대상은 gateway memory가 아니라 producer 정의와 metric 계약이다. restart/rebuild 후 producer는 현재 유효한 metric만 다시 push한다. 오래된 관찰 결과를 재전송하지 않는다. upgrade할 때 API/label 호환성을 확인한다.
- **공식 문서·license**: 공식 [Prometheus Pushgateway 저장소](https://github.com/prometheus/pushgateway)를 따른다. Pushgateway에는 Apache-2.0 license가 적용된다.


## Common Checks

- `docker compose --profile obs ps pushgateway`
- `curl -I http://pushgateway:9091/-/ready`
- `rg -n 'job_name: "pushgateway"|pushgateway:9091|honor_labels' infra/06-observability/prometheus/config/prometheus.yml`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0046-pushgateway.md)을 따른다.

## Traceability

- Declared parent: [Pushgateway Operations Policy](../policies/0046-pushgateway.md) (`POL-0046`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Policy](../policies/0046-pushgateway.md) (`POL-0046`), [Runbook](../runbooks/0046-pushgateway.md) (`RUN-0046`)

## Related Documents

- [Observability Compose](../../../infra/06-observability/docker-compose.yml)

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0046-pushgateway.md)
- [Recovery runbook](../runbooks/0046-pushgateway.md)
