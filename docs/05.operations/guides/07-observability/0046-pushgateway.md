---
title: "Pushgateway Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
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

## Purpose

### Outcome

이 문서는 Pushgateway의 역할과 기본 사용법을 설명한다. Pushgateway는 Prometheus pull 모델이 직접 적용되기 어려운 단기 실행·배치 작업의 metric을 일시적으로 받아 두는 버퍼다. 장기 실행 서비스의 일반 metric 수집 경로로 쓰지 않는다.

대상 독자는 개발자, 운영자, agent 튜닝 담당자다. Pushgateway의 역할과 동작 방식을 이해하고, 배치 작업에서 메트릭을 올바르게 전송하고 관리하는 방법을 익히는 것이 목표다.

### Boundaries

- Declared parent: [Pushgateway Operations Policy](../../policies/07-observability/0046-pushgateway.md) (`POL-0046`)
- Governing authority: [Observability Architecture Description](../../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Policy](../../policies/07-observability/0046-pushgateway.md) (`POL-0046`), [Runbook](../../runbooks/07-observability/0046-pushgateway.md) (`RUN-0046`)

- [Observability Compose](../../../../infra/06-observability/docker-compose.yml)
- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

## Prerequisites

### Environment

이 가이드가 전제하는 환경과 개념은 아래와 같다.

#### Preconditions

- `pushgateway` service가 `obs` 또는 `batch-metrics` profile에서 실행 중이어야 한다.
- 작업이 `obs_net` 또는 Pushgateway에 도달할 수 있는 네트워크 경로에 있어야 한다.
- Prometheus에 의존하는 dashboard나 alert를 만들기 전에 Pushgateway scrape job이 추가되었는지 확인한다. 현재 선택 config(`PROMETHEUS_CONFIG_FILE`, 기본 `prometheus.dev.yml`)와 `prometheus.yml` 모두 해당 job이 없다.

### Permissions

Pushgateway에는 Docker Secret이 없다. Prometheus scrape job 추가는 별도 승인 작업이며, 종료된 group 정리는 RUN-0046이 소유한다.

## Procedure

### Actions

정상 사용과 확인 절차는 아래 항목을 따른다.

#### Normal use

정상 사용 절차는 아래 항목을 따른다.

##### 서비스 도달성 확인

기존 승인된 `obs_net` client에서 ready endpoint를 확인한다. Compose DNS는 host shell에서 해석된다고 가정하지 않는다; gateway redirect는 backend readiness 성공이 아니다.

```bash
curl -I http://pushgateway:9091/-/ready
```

##### 메트릭 전송

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

##### Prometheus scrape 연동 확인

Prometheus dashboard나 alert가 Pushgateway metric에 의존하기 전에 scrape job 존재를 확인한다. 현재는 없으므로 gap으로 기록하고 추가는 별도 승인 작업으로 둔다.

확인 명령은 [Common Checks](#common-checks)에 있다.

##### 메트릭 삭제

실행 중에는 metric TTL이 없어 마지막 값을 유지하지만 현재 persistence가 없어 process restart 시 사라진다. 종료된 group 정리는 [RUN-0046](../../runbooks/07-observability/0046-pushgateway.md)의 승인된 정확한 grouping-key 절차를 따른다. 삭제 명령은 [RUN-0046 절차](../../runbooks/07-observability/0046-pushgateway.md#procedure)가 소유한다.

#### Source-backed operating contract

- **목적·분류·구현 소유권**: `pushgateway`는 `OPTIONAL` batch metric 중계 서비스이며 `obs`/`batch-metrics`로 선택한다. [Compose](../../../../infra/06-observability/docker-compose.yml)가 구현을 소유한다.
- **흐름·의존성·보안**: 승인된 단기 job이 metric을 push한다. 현재 두 Prometheus config(`prometheus.yml`, `prometheus.dev.yml`)에는 Pushgateway scrape job이 없어 push된 metric은 Prometheus에 들어오지 않는다. Traefik이 UI/API route를 보호하지만 producer 인가와 metric-label 관리 규칙은 여전히 필요하다. Prometheus, gateway/auth와 `obs_net`이 의존성이다.
- **상태**: 현재 Compose에는 volume과 `--persistence.file`이 선언되어 있지 않다. metric은 process memory에 있으며 restart하면 사라진다. Docker Secret은 없다. 현재 Pushgateway 내용을 영속적이거나 정확히 복구할 수 있다고 설명하지 않는다.
- **자원·정상 사용**: source limit은 여유 용량을 뜻하지 않는다. 저장소 root에서 렌더링하고 batch 용도로만 시작한다. label을 붙인 test group을 push하여 Pushgateway `/metrics`에서 확인하고(Prometheus scrape job이 추가된 뒤에는 Prometheus target도 확인한다), producer가 완료되면 오래된 group을 삭제한다.
- **수명 주기·복구**: backup 대상은 gateway memory가 아니라 producer 정의와 metric 계약이다. restart/rebuild 후 producer는 현재 유효한 metric만 다시 push한다. 오래된 관찰 결과를 재전송하지 않는다. upgrade할 때 API/label 호환성을 확인한다.
- **공식 문서·license**: 공식 [Prometheus Pushgateway 저장소](https://github.com/prometheus/pushgateway)를 따른다. Pushgateway에는 Apache-2.0 license가 적용된다.

### Exceptions

Prometheus scrape job 부재와 persistence 부재의 한계는 Actions의 `Prometheus scrape 연동 확인`, `메트릭 삭제`, `Source-backed operating contract`에 기술되어 있다.

## Verification

### Expected Result

확인 항목과 기대 결과는 아래와 같다.

#### Common Checks

- `docker compose --profile obs ps pushgateway`
- `curl -I http://pushgateway:9091/-/ready`
- `rg -n 'job_name: "pushgateway"|pushgateway:9091|honor_labels' infra/06-observability/prometheus/config/` (현재 출력 없음: scrape job 미구현)

### Troubleshooting

- **Stale metrics**: Pushgateway는 마지막 값을 유지한다. 실패한 배치가 metric을 갱신하지 못하면 오래된 성공 값이 계속 보일 수 있다.
- **Label collision**: 여러 worker가 같은 `job`만 사용하면 metric group이 덮어써질 수 있다. worker 구분이 필요할 때만 안정적인 `instance` label을 추가한다.
- **High cardinality**: user ID, request ID, unbounded build ID를 label에 넣으면 cleanup이 어려워지고 메모리 사용량이 커진다.
- **Scrape assumption**: Pushgateway service가 떠 있어도 Prometheus scrape job이 없으면 Prometheus target이나 alert에서 해당 metric을 볼 수 없다.

#### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/07-observability/0046-pushgateway.md)을 따른다.

- [Operations index](../../README.md)
- [Operations policy](../../policies/07-observability/0046-pushgateway.md)
- [Recovery runbook](../../runbooks/07-observability/0046-pushgateway.md)
