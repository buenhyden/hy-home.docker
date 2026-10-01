---
title: "Performance Testing Usage Guide"
version: "1.0.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0064"
parent_ids:
- "POL-0064"
created: "2026-05-10"
---

# Performance Testing Usage Guide

## Usage

### Overview

이 문서는 `11-quality` 성능 테스트 워크플로우의 공통 사용 기준을 설명한다. 현재 구현은 두 가지다. `locust` leaf는 master/worker 구성과 host port UI를 제공하고, `k6` leaf는 UI 없이 시나리오를 한 번 실행한 뒤 지표를 Prometheus remote write로 내보낸다.

### Usage Type

`system-guide | performance-guide | operational-reference`

### Target Audience

- Developer
- Operator
- Performance Engineer

### Purpose

성능 테스트를 실행하기 전에 어떤 leaf를 선택해야 하는지, root compose와 profile 선택 경계, 승인/검증 절차를 어떻게 적용해야 하는지 안내한다.

### Prerequisites

- `locust` leaf는 `locust-master`, `locust-worker` 분산 실행에 사용한다.
- `k6` leaf는 단일 `k6` 작업이며 worker service가 없다. 결과는 UI가 아니라 Grafana `k6 Prometheus` 대시보드에서 본다.
- 루트 Compose 문맥이 필요하다. Locust는 기본 네트워크, k6는 `obs_net`을 사용한다.
- 대규모 테스트는 승인된 테스트 윈도우와 대상 서비스 owner 승인이 필요하다.

### Step-by-step Instructions

1. 테스트 목적에 맞는 leaf를 선택한다.
   - 분산 worker가 필요하면 [Locust guide](0062-locust.md)를 사용한다.
   - `k6` leaf의 현재 wrapper 계약을 확인하려면 [k6 guide](0061-k6.md)를 사용한다.
2. Locust 시나리오는 호스트에 마운트한 `locustfile.py`, k6 시나리오는 해당
   스크립트 bind의 JavaScript로 작성한다. 다음 예제는 Locust에만 적용한다.

   ```python
   from locust import HttpUser, task, between

   class WebsiteUser(HttpUser):
       wait_time = between(1, 5)

       @task
       def index_page(self):
           self.client.get("/")
   ```

3. 실행 전 공통 검증을 수행한다.
   - `bash scripts/hardening/check-all-hardening.sh 11-quality`
   - `python3 scripts/validation/run-ci-gate.py --profile changed`
4. 루트 Compose는 leaf를 이미 include한다. 같은 leaf를 `-f`로 다시 겹치지 않고
   루트에서 `testing` 프로필의 서비스 선택을 확인한다. 실제 실행은 런북의 승인을 따른다.
5. UI는 host port `http://localhost:${LOCUST_HOST_PORT:-18089}` 경계에서 접근한다.
6. Users, spawn rate, target host를 기록하고, 테스트 결과와 target SLI 변화를 evidence로 남긴다.

### Common Pitfalls

- 순간적인 대량 요청은 공유 gateway/auth/data tier에 영향을 줄 수 있으므로 ramp-up을 보수적으로 설정한다.
- host port UI를 공개 route처럼 문서화하지 않는다. 현재 Locust/k6 leaf에는 Traefik route가 없다.
- service-local compose 단독 config 실패를 구현 결함으로 해석하지 않는다. root context가 필요한 선택 leaf다.

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 11-quality`
- `python3 scripts/validation/run-ci-gate.py --profile changed`
- 루트 Compose에서 정확한 서비스와 선언된 네트워크가 선택되는지 확인한다. 렌더링은 대상의 준비·회복 증거가 아니다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0064-performance-testing.md)을 따른다.

## Traceability

- 상위 문서: [Performance Testing Operations Policy](../policies/0064-performance-testing.md) (`POL-0064`)
- 설계 근거: [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- 동일 주제 문서: [Policy](../policies/0064-performance-testing.md) (`POL-0064`), [Runbook](../runbooks/0064-performance-testing.md) (`RUN-0064`)

## Related Documents

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0064-performance-testing.md)
- [Recovery runbook](../runbooks/0064-performance-testing.md)
