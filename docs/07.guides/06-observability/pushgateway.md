# Pushgateway Guide

> Metrics buffer for ephemeral and batch jobs.

---

## Overview (KR)

이 문서는 Pushgateway에 대한 가이드다. Pushgateway는 프로메테우스의 Pull 모델이 직접 적용되기 어려운 단기 실행 작업(Ephemeral jobs)이나 배치 스크립트의 메트릭을 일시적으로 보관하고 프로메테우스가 이를 스크랩할 수 있게 하는 버퍼 역할을 한다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- Operator
- Agent-tuner

## Purpose

Pushgateway의 역할과 동작 방식을 이해하고, 배치 작업에서 메트릭을 올바르게 전송하고 관리하는 방법을 익힌다.

## Prerequisites

- [Prometheus](prometheus.md) 가동 중
- 네트워크 연결 (`infra_net`)
- 메트릭 전송 권한 (Traefik을 통한 외부 노출 시)

## Step-by-step Instructions

### 1. 메트릭 전송 (Pushing Metrics)

배치 작업 종료 시 또는 주기적으로 HTTP POST/PUT을 사용하여 메트릭을 Push한다.

```bash
# 단일 메트릭 전송
echo "batch_job_duration_seconds 120" | curl --data-binary @- http://pushgateway.local/metrics/job/my_batch_job

# 레이블과 함께 전송
cat <<EOF | curl --data-binary @- http://pushgateway.local/metrics/job/my_batch_job/instance/worker-01
# HELP batch_process_items Total items processed by batch.
# TYPE batch_process_items counter
batch_process_items 1500
EOF
```

### 2. 프로메테우스 스크랩 설정

프로메테우스는 Pushgateway의 `/metrics` 엔드포인트를 주기적으로 스크랩한다. 이때 `honor_labels: true` 설정이 권장된다.

### 3. 메트릭 삭제 (Deleting Metrics)

Pushgateway는 수신된 메트릭을 명시적으로 삭제하기 전까지 계속 보관한다. 작업이 완전히 종료되거나 더 이상 유효하지 않은 인스턴스의 메트릭은 삭제 API를 호출해야 한다.

```bash
curl -X DELETE http://pushgateway.local/metrics/job/my_batch_job
```

## Common Pitfalls

- **메트릭 잔류 (Stale Metrics)**: Pushgateway는 수신된 마지막 값을 계속 보관한다. 만약 실패한 배치가 메트릭을 업데이트하지 못하면 프로메테우스는 마지막 성공 값을 계속 수집하여 오해를 유발할 수 있다.
- **인스턴스 레이블 충돌**: 여러 인스턴스가 동일한 `job` 레이블로 Push하면 데이터가 덮어씌워진다. `instance` 레이블을 활용하여 구분해야 한다.
- **오남용 (Anti-pattern)**: 일반적인 서비스의 메트릭 수집을 위해 Pushgateway를 사용하지 마라. 이는 프로메테우스의 가용성 감지 기능을 무력화한다.

## Related Documents

- **Infrastructure**: `[infra/06-observability/pushgateway/README.md](../../../infra/06-observability/pushgateway/README.md)`
- **Operation**: `[../08.operations/06-observability/pushgateway.md](../../08.operations/06-observability/pushgateway.md)`
- **Runbook**: `[../09.runbooks/06-observability/pushgateway.md](../../09.runbooks/06-observability/pushgateway.md)`
