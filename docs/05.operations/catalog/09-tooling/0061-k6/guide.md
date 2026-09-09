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

이 문서는 `infra/09-tooling/k6` leaf의 현재 사용 경계를 설명한다. compose는 고정된 `grafana/k6` 이미지를 빌드해 `k6` 서비스로 시나리오를 한 번 실행하고 종료하며, `k6-data:/scripts:ro` 볼륨에서 시나리오를 읽고 결과 지표를 Prometheus remote write로 내보낸다.

### Usage Type

`system-guide | performance-guide | operational-reference`

### Target Audience

- QA Engineer
- SRE
- Performance Engineer

### Purpose

현재 k6 leaf를 사용할 때 실제 서비스명, 시나리오 위치, UI 접근 경계, 검증 경계를 혼동하지 않도록 안내한다.

### Prerequisites

- root [docker-compose.yml](../../../../../docker-compose.yml)는 `infra/09-tooling/k6/docker-compose.yml`를 무조건 include하므로, 기동 여부는 선택한 profile이 결정한다. `k6`는 `testing`에만 속한다. 도메인 전체를 뜻하는 `tooling`을 골라도 부하 시험은 실행되지 않는다.
- Root `infra_net` context가 제공되는지 확인.
- 시나리오는 JavaScript k6 문법으로 작성하고 `DEFAULT_TOOLING_DIR`의 host bind mount에 둔다.
- 지표를 Grafana에서 보려면 `obs` profile의 Prometheus가 이미 떠 있어야 한다. `k6`는 `depends_on`을 선언하지 않는다. Prometheus가 `testing`을 선언하지 않아 선언하면 렌더링이 깨지기 때문이다.

### Step-by-step Instructions

1. 현재 leaf의 구현 경계를 확인한다.
   - 서비스명: `k6`
   - profiles: `testing`
   - mount: `k6-data:/scripts:ro`
   - host port: 없음. k6는 CLI로 구동하며 UI를 제공하지 않는다.
2. 테스트 시나리오를 `${DEFAULT_TOOLING_DIR}/k6/smoke.js` 기준으로 준비한다.

   ```javascript
   import http from 'k6/http';
   import { check } from 'k6';

   export const options = { vus: 5, duration: '30s' };

   export default function () {
     const response = http.get(`https://${__ENV.TARGET_HOST}/`);
     check(response, { 'status is 200': (r) => r.status === 200 });
   }
   ```

3. 런타임 실행 전 정적 기준선을 확인한다.
   - `bash scripts/hardening/check-all-hardening.sh 09-tooling`
   - `python3 scripts/validation/run-ci-gate.py --profile changed`
4. 실행이 승인된 환경에서 root compose와 leaf compose를 함께 렌더링해 `infra_net`이 해석되는지 확인한다.
5. 결과는 UI가 아니라 Grafana `k6 Prometheus` 대시보드에서 확인한다. 대시보드는
   `testid` 라벨로 실행을 구분하므로 `K6_TESTID`를 실행마다 다르게 준다.
6. k6 요약 출력, target SLI 저하, 컨테이너 종료 코드를 evidence로 기록한다.
   `k6`는 healthcheck를 선언하지 않는다. 한 번 실행하고 끝나는 작업이라
   healthy 상태가 존재하지 않기 때문이다.

### Common Pitfalls

- **`K6_TREND_STATS`를 줄이면 대시보드 절반이 빈다.** Grafana `k6 Prometheus`
  대시보드는 `k6_http_req_duration_min`, `_max`, `_p95`, `_p99`를 조회하는데
  k6의 기본 trend 통계는 `p(99)` 하나뿐이다. compose는 네 값을 모두 요청하도록
  기본값을 준다.
- **`restart` 정책을 템플릿 기본값으로 되돌리면 안 된다.** `template-infra-med`는
  `restart: unless-stopped`를 준다. 한 번 실행하고 끝나는 작업에 그 값을 쓰면
  부하 시험이 무한히 재실행된다. compose는 `restart: 'no'`로 덮어쓴다.
- 이 leaf에는 worker service가 없다. k6는 단일 프로세스가 VU를 실행한다. 분산 부하가 필요하면 `locust` leaf의 `locust-worker` 구성을 사용한다.
- service-local compose 파일만 단독으로 `docker compose config`하면 root `infra_net` context가 없어 실패할 수 있다.
- 시나리오 경로를 바꾸려면 `K6_SCRIPT`를 쓴다. compose command를 직접 고치면 이 문서와 어긋난다.

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 09-tooling`
- `python3 scripts/validation/run-ci-gate.py --profile changed`
- 실행 승인 시 root+leaf compose overlay의 rendered service list에 `k6`가 포함되는지 확인한다.

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
