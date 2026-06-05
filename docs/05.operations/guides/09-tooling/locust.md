---
status: active
---
<!-- Target: docs/05.operations/guides/09-tooling/locust.md -->

# Locust Usage Guide

## Usage

### Overview

이 문서는 `infra/09-tooling/locust`의 현재 Locust master/worker 부하 테스트 구성을 설명한다. 현재 compose는 `locust-master`, `locust-worker`를 빌드하고, InfluxDB Docker Secret과 `locust-data:/mnt/locust:rw` 볼륨을 사용한다.

### Usage Type

`system-guide | performance-guide | troubleshooting-guide`

### Target Audience

- QA Engineer
- Performance Engineer
- SRE

### Purpose

분산 Locust 실행 시 실제 서비스명, root optional include 경계, UI 접근 포트, worker 복제본 기준을 현재 compose와 일치하게 안내한다.

### Prerequisites

- `infra/09-tooling/locust/docker-compose.yml`와 root [docker-compose.yml](../../../../docker-compose.yml)의 선택 include 상태 확인.
- InfluxDB service와 Docker Secret `influxdb_api_token`이 root context에서 제공되는지 확인.
- 테스트 시나리오 작성을 위한 Python/Locust 문법 이해.

### Step-by-step Instructions

1. 테스트 시나리오는 `infra/09-tooling/locust/locustfile.py` 기준으로 작성한다.

   ```python
   from locust import HttpUser, task, between

   class BenchmarkUser(HttpUser):
       wait_time = between(1, 2)

       @task
       def test_endpoint(self):
           self.client.get("/api/v1/health")
   ```

2. 실행 전 정적 기준선을 확인한다.
   - `bash scripts/hardening/check-all-hardening.sh 09-tooling`
   - `bash scripts/validation/check-repo-contracts.sh`
3. 실행이 승인된 환경에서 root compose와 leaf compose를 함께 렌더링해 `infra_net`, `influxdb`, `influxdb_api_token`이 모두 해석되는지 확인한다.
4. 승인된 테스트 윈도우에서 `locust-master`와 `locust-worker`를 기동한다. worker 확장이 필요하면 `locust-worker`만 scale 대상이다.
5. UI는 host port `http://localhost:${LOCUST_HOST_PORT:-18089}` 경계에서 확인한다.
6. Users, spawn rate, target host를 입력하고 테스트 중 target SLI와 InfluxDB 전송 상태를 기록한다.

### Common Pitfalls

- service-local compose 파일만 단독으로 렌더링하면 root `infra_net`/secret/dependency context가 없어 실패할 수 있다.
- 현재 compose에는 Traefik Locust route가 없다. UI 접근은 host port mapping 기준이다.
- `locust-worker`는 `locust-master` health 이후 연결되므로 master healthcheck 실패를 먼저 확인한다.

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 09-tooling`
- `bash scripts/validation/check-repo-contracts.sh`
- 실행 승인 시 rendered service list에 `locust-master`, `locust-worker`가 포함되는지 확인한다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/09-tooling/locust.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/09-tooling/locust.md)
- [Recovery runbook](../../runbooks/09-tooling/locust.md)
