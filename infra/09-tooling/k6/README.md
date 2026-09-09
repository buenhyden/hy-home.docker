---
title: "\U0001F9EA k6 Performance Testing Infrastructure"
version: "1.3.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
created: "2026-03-26"
---

<!-- [ID:09-tooling:k6] -->
# 🧪 k6 Performance Testing Infrastructure

> Distributed performance benchmarking and user simulation for `hy-home.docker`.

## Overview

이 서비스 유닛은 플랫폼의 서비스를 로드 테스팅하기 위한 분산 부하 테스트 엔진을 제공합니다.

> [!NOTE]
> **Implementation Detail**: 현재 이 디렉토리(`infra/09-tooling/k6`)는 **Locust** 엔진을 통해 마스터-워커 분산 부하 구조를 구현하고 있습니다.

## Audience

- QA Engineers (Load testing)
- SREs (Capacity planning)
- Performance Engineers

## Scope

### In Scope

- **Benchmark Orchestration**: `k6` 서비스가 실행하는 k6 시나리오 관리.
- **Result Evidence**: k6 요약 출력과 Prometheus remote write로 보낸 지표를 evidence로 기록.
- **Scenario Mount**: `k6-data:/scripts:ro` volume 계약 유지.

### Out of Scope

- **Metric Storage Layer**: 장기 지표 저장소의 선택과 운영은 이 leaf의 책임이 아님.
  이 leaf는 Prometheus remote write endpoint로 내보내기만 한다.
- **Visualization**: Grafana 대시보드 자체의 소유는 `06-observability`에 있다.

## Structure

```text
k6/
├── Dockerfile          # 고정된 grafana/k6 이미지
├── docker-compose.yml  # 부하 시험 작업 정의
└── README.md           # This file

시나리오 스크립트는 저장소가 아니라 `DEFAULT_TOOLING_DIR`의 host bind mount에
둔다. `locust` leaf와 같은 규약이다.
```

## Available Scripts

| Command                                                    | Description                      |
| ---------------------------------------------------------- | -------------------------------- |
| `bash scripts/hardening/check-all-hardening.sh 09-tooling` | Static hardening contract check |
| `python3 scripts/validation/run-ci-gate.py --profile changed` | Documentation and stale-literal guard |
| `docker compose ... logs -f k6` | Approved runtime context에서 실행 로그 확인 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `K6_SCRIPT` | No | 실행할 시나리오 경로 (기본: `/scripts/smoke.js`) |
| `K6_TESTID` | No | Grafana 대시보드가 필터로 쓰는 `testid` 태그 (기본: `local`) |
| `K6_TREND_STATS` | No | remote write로 내보낼 trend 통계 (기본: `min,max,p(95),p(99)`) |
| `K6_PROMETHEUS_HOST` | No | remote write 대상 호스트 (기본: `prometheus`) |
| `K6_PROMETHEUS_PORT` | No | remote write 대상 포트 (기본: `9090`) |
| `DEFAULT_TOOLING_DIR` | Yes | 스크립트 볼륨의 호스트 경로 |

## Validation

- Run `bash scripts/hardening/check-all-hardening.sh 09-tooling` after README or Compose reference changes that affect k6.
- Run `python3 scripts/validation/run-ci-gate.py --profile changed` to keep service documentation and operation links synchronized.
- Runtime rendering must provide root `infra_net` context because the root file includes this leaf unconditionally and the `testing` profile decides whether its service resolves.

## Troubleshooting

- Start with the hardening check to confirm k6 network, volume, and metric sink references stay declared.
- Check k6 run output and the linked runbook before changing test scripts or metric destinations.

## Related Documents

- **Guide**: k6 Performance Testing Guide (`docs/05.operations/catalog/09-tooling/0061-k6/guide.md`)
- **Policy**: k6 operations policy (`docs/05.operations/catalog/09-tooling/0061-k6/policy.md`)
- **Runbook**: k6 recovery runbook (`docs/05.operations/catalog/09-tooling/0061-k6/runbook.md`)
- [Documentation index](../../../docs/README.md)

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | 🧪 k6 Performance Testing Infrastructure service leaf in `09-tooling`; services: `k6`; the root [docker-compose.yml](../../../docker-compose.yml) includes this leaf's `docker-compose.yml` unconditionally |
| Config files | `Dockerfile`, `docker-compose.yml` |
| Config values | profiles: `testing`; scenario and export keys: `K6_SCRIPT`, `K6_TESTID`, `K6_TREND_STATS`, `K6_PROMETHEUS_HOST`, `K6_PROMETHEUS_PORT` |
| Compose linkage | root include active; the `testing` profile selects `k6` |
| Networks | `infra_net` |
| Volumes | `k6-data:/scripts:ro`, `k6-data` |
| Ports | None declared; k6 is CLI-driven and publishes no host port |
| Labels | `hy-home.tier` |
| Secret refs | None declared |
| Healthcheck | None declared; `k6` runs one scenario and exits, so `restart` is `no` |
| Operations | Guide (`docs/05.operations/catalog/09-tooling/0061-k6/guide.md`), Policy (`docs/05.operations/catalog/09-tooling/0061-k6/policy.md`), Runbook (`docs/05.operations/catalog/09-tooling/0061-k6/runbook.md`) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Start with the hardening check, then inspect service logs and linked operations/runbook evidence in an approved runtime context. |

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
