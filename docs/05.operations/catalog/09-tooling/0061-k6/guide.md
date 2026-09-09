---
title: "k6 Usage Guide"
version: "1.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "operations"
artifact_id: "GDE-0061"
parent_ids:
- "POL-0061"
created: "2026-05-10"
---

# k6 Usage Guide

<!-- [ID:09-tooling:k6] -->

## Usage

### Overview

이 문서는 `infra/09-tooling/k6` leaf의 현재 사용 경계를 설명한다. 현재 compose는 JavaScript k6 engine이 아니라 Locust 기반 wrapper 서비스 `k6-master`를 빌드하며, `k6-data:/mnt/locust:rw` 볼륨을 사용해 테스트 시나리오를 제공한다.

### Usage Type

`system-guide | performance-guide | operational-reference`

### Target Audience

- QA Engineer
- SRE
- Performance Engineer

### Purpose

현재 k6 leaf를 사용할 때 실제 서비스명, 시나리오 위치, UI 접근 경계, 검증 경계를 혼동하지 않도록 안내한다.

### Prerequisites

- root [docker-compose.yml](../../../../../docker-compose.yml)는 `infra/09-tooling/k6/docker-compose.yml`를 무조건 include하므로, 기동 여부는 선택한 profile이 결정한다. `k6-master`는 `tooling`과 `testing`에 속한다.
- Root `infra_net` context가 제공되는지 확인.
- 현재 구현은 Locust 시나리오를 사용하므로 Python/Locust 문법을 기준으로 테스트 파일을 작성한다.

### Step-by-step Instructions

1. 현재 leaf의 구현 경계를 확인한다.
   - 서비스명: `k6-master`
   - profiles: `tooling`, `testing`
   - mount: `k6-data:/mnt/locust:rw`
   - UI port mapping: `${K6_HOST_PORT:-18189}:${K6_PORT:-8089}`
2. 테스트 시나리오를 `infra/09-tooling/k6/locustfile.py` 기준으로 준비한다.

   ```python
   from locust import HttpUser, task

   class PlatformUser(HttpUser):
       @task
       def visit_homepage(self):
           self.client.get("/")
   ```

3. 런타임 실행 전 정적 기준선을 확인한다.
   - `bash scripts/hardening/check-all-hardening.sh 09-tooling`
   - `python3 scripts/validation/run-ci-gate.py --profile changed`
4. 실행이 승인된 환경에서 root compose와 leaf compose를 함께 렌더링해 `infra_net`이 해석되는지 확인한다.
5. 서비스 기동 후 UI는 host port `http://localhost:${K6_HOST_PORT:-18189}` 경계에서 확인한다.
6. 테스트 중 Locust 요청 통계, target SLI 저하, `k6-master` healthcheck 상태를 evidence로 기록한다.

### Common Pitfalls

- **미해결 결함: 빌드 컨텍스트에 Dockerfile이 없다.** `k6-master`는 `build: .`을
  선언하지만 `infra/09-tooling/k6/`에는 `Dockerfile`도 `locustfile.py`도 없고
  `README.md`와 `docker-compose.yml`만 있다. 따라서 `tooling` 또는 `testing`
  profile로 기동하면 빌드 단계에서 실패한다. 정적 렌더링과 `run-ci-gate.py`는
  이 결함을 잡지 못한다.
- **현재 compose는 locust leaf의 복사본이다.** command, mount 경로 `/mnt/locust`,
  healthcheck port 8089가 `locust-master`와 같고 worker service만 빠져 있다.
  반면 세 개의 추적 표면은 실제 k6를 전제한다.
  `infra/06-observability/grafana/dashboards/Infrastructure/k6.json`은 패널 17개의
  `k6 Prometheus` 대시보드이고, `.github/dependabot.yml`은 이 디렉터리를 docker
  ecosystem으로 등록하며, `K6_HOST_PORT`/18189는 `testing`에서 두 서비스가 18089를
  두고 충돌하던 것을 나누려고 만들어졌다. 즉 의도는 실제 k6였고 구현만 locust
  복사본에 머문 상태다. 해소 방향은 이 subject 소유자의 판단이며, 실제 k6 engine
  전환은 런타임 검증이 필요한 인프라 변경이라 별도 승인 대상이다. 디렉터리를
  제거하는 방향을 고르면 위 세 표면과 이 subject 문서가 함께 정리 대상이 된다.
- 현재 leaf에는 별도 worker service가 없다. worker scaling 절차가 필요하면 `locust.md`의 `locust-worker` 기준을 사용한다.
- service-local compose 파일만 단독으로 `docker compose config`하면 root `infra_net` context가 없어 실패할 수 있다.
- `k6` 이름만 보고 JavaScript k6 script를 투입하면 현재 container command와 맞지 않는다.

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 09-tooling`
- `python3 scripts/validation/run-ci-gate.py --profile changed`
- 실행 승인 시 root+leaf compose overlay의 rendered service list에 `k6-master`가 포함되는지 확인한다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](runbook.md)을 따른다.

## Traceability

- Declared parent: [k6 Operations Policy](policy.md) (`POL-0061`)
- Governing authority: [Tooling Tier Architecture Description](../../../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- Subject peers: [Policy](policy.md) (`POL-0061`), [Runbook](runbook.md) (`RUN-0061`)

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
