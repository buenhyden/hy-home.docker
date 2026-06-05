---
status: active
---
<!-- Target: docs/05.operations/guides/09-tooling/performance-testing.md -->

# Performance Testing Usage Guide

## Usage

### Overview

이 문서는 `09-tooling` 성능 테스트 워크플로우의 공통 사용 기준을 설명한다. 현재 구현은 `locust` leaf의 master/worker 구성과 `k6` leaf의 단일 `k6-master` Locust wrapper를 제공하며, 둘 다 InfluxDB 지표 전송과 host port UI 경계를 사용한다.

### Usage Type

`system-guide | performance-guide | operational-reference`

### Target Audience

- Developer
- Operator
- Performance Engineer

### Purpose

성능 테스트를 실행하기 전에 어떤 leaf를 선택해야 하는지, root optional compose 경계와 승인/검증 절차를 어떻게 적용해야 하는지 안내한다.

### Prerequisites

- `locust` leaf는 `locust-master`, `locust-worker` 분산 실행에 사용한다.
- `k6` leaf는 현재 단일 `k6-master` Locust wrapper이며 별도 worker service가 없다.
- InfluxDB service, Docker Secret `influxdb_api_token`, root `infra_net` context가 필요하다.
- 대규모 테스트는 승인된 테스트 윈도우와 대상 서비스 owner 승인이 필요하다.

### Step-by-step Instructions

1. 테스트 목적에 맞는 leaf를 선택한다.
   - 분산 worker가 필요하면 [Locust guide](./locust.md)를 사용한다.
   - `k6` leaf의 현재 wrapper 계약을 확인하려면 [k6 guide](./k6.md)를 사용한다.
2. 테스트 시나리오는 해당 leaf의 `locustfile.py`에 맞춰 작성한다.

   ```python
   from locust import HttpUser, task, between

   class WebsiteUser(HttpUser):
       wait_time = between(1, 5)

       @task
       def index_page(self):
           self.client.get("/")
   ```

3. 실행 전 공통 검증을 수행한다.
   - `bash scripts/hardening/check-all-hardening.sh 09-tooling`
   - `bash scripts/validation/check-repo-contracts.sh`
4. 실행이 승인된 환경에서 root compose와 선택 leaf compose를 함께 렌더링한다.
5. UI는 host port `http://localhost:${LOCUST_HOST_PORT:-18089}` 경계에서 접근한다.
6. Users, spawn rate, target host를 기록하고, 테스트 결과와 target SLI 변화를 evidence로 남긴다.

### Common Pitfalls

- 순간적인 대량 요청은 공유 gateway/auth/data tier에 영향을 줄 수 있으므로 ramp-up을 보수적으로 설정한다.
- host port UI를 공개 route처럼 문서화하지 않는다. 현재 Locust/k6 leaf에는 Traefik route가 없다.
- service-local compose 단독 config 실패를 구현 결함으로 해석하지 않는다. root context가 필요한 선택 leaf다.

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 09-tooling`
- `bash scripts/validation/check-repo-contracts.sh`
- 실행 승인 시 root+leaf overlay가 선택 leaf service와 InfluxDB dependency를 함께 렌더링하는지 확인한다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/09-tooling/performance-testing.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/09-tooling/performance-testing.md)
- [Recovery runbook](../../runbooks/09-tooling/performance-testing.md)
