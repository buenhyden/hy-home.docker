---
title: "k6 Performance Testing Infrastructure"
version: "1.3.3"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2026-03-26"
---

<!-- [ID:11-quality:k6] -->
# k6 Performance Testing Infrastructure

> `hy-home.docker`를 위한 1회성 k6 성능 벤치마킹입니다.

## Overview

이 서비스 유닛은 플랫폼의 서비스를 로드 테스팅하기 위해 k6 시나리오를 한 번 실행하는 부하 테스트 작업을 제공합니다.

> [!NOTE]
> **Implementation Detail**: 이 디렉토리(`infra/11-quality/k6`)는 `testing` profile이 선택하는 단일 `k6` 서비스로 실제 k6 engine을 한 번 실행하고 종료합니다. 분산 master-worker 부하는 `infra/11-quality/locust`가 담당합니다.

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
```

시나리오 스크립트는 저장소가 아니라 `DEFAULT_TOOLING_DIR`의 host bind mount에
둔다. `locust` leaf와 같은 규약이다.

## Available Scripts

| Command                                                    | Description                      |
| ---------------------------------------------------------- | -------------------------------- |
| `bash scripts/hardening/check-all-hardening.sh 11-quality` | 정적 hardening 계약 검사 |
| `python3 scripts/validation/run-ci-gate.py --profile changed` | 문서 및 오래된 리터럴 가드 |
| `docker compose ... logs -f k6` | 승인된 runtime context에서 실행 로그 확인 |

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

- k6에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/hardening/check-all-hardening.sh 11-quality`을 실행합니다.
- 서비스 문서와 운영 링크를 동기화하려면 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.
- 루트 파일이 이 leaf를 무조건 include하고 `testing` 프로필이 해당 서비스의 해석 여부를 결정하므로, 런타임 렌더링에는 루트 네트워크 컨텍스트가 필요합니다.

## Troubleshooting

- k6 네트워크, 볼륨, 지표 싱크 참조가 계속 선언되어 있는지 hardening 점검으로 먼저 확인합니다.
- 테스트 스크립트나 지표 대상을 변경하기 전에 k6 실행 출력과 연결된 런북을 확인합니다.

## Related Documents

- **Guide**: k6 Performance Testing Guide (`docs/05.operations/guides/0061-k6.md`)
- **Policy**: k6 operations policy (`docs/05.operations/policies/0061-k6.md`)
- **Runbook**: k6 recovery runbook (`docs/05.operations/runbooks/0061-k6.md`)
- [Documentation index](../../../docs/README.md)

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `11-quality`의 k6 Performance Testing Infrastructure 서비스 leaf; 서비스: `k6`; 루트 [docker-compose.yml](../../../docker-compose.yml)이 이 leaf의 `docker-compose.yml`을 무조건 include함 |
| Config files | `Dockerfile`, `docker-compose.yml` |
| Config values | 프로필: `testing`; 시나리오/내보내기 키: `K6_SCRIPT`, `K6_TESTID`, `K6_TREND_STATS`, `K6_PROMETHEUS_HOST`, `K6_PROMETHEUS_PORT` |
| Compose linkage | 루트 include 활성; `testing` 프로필이 `k6`를 선택함 |
| Networks | `obs_net` |
| Volumes | `k6-data:/scripts:ro`, `k6-data` |
| Ports | 선언되지 않음; k6는 CLI로 구동되며 호스트 포트를 게시하지 않음 |
| Labels | `hy-home.tier` |
| Secret refs | 선언되지 않음 |
| Healthcheck | 선언되지 않음; `k6`는 시나리오 하나를 실행하고 종료하므로 `restart`는 `no` |
| Operations | Guide (`docs/05.operations/guides/0061-k6.md`), Policy (`docs/05.operations/policies/0061-k6.md`), Runbook (`docs/05.operations/runbooks/0061-k6.md`) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | hardening 점검으로 시작한 뒤 승인된 런타임 컨텍스트에서 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 검증을 제공합니다.

Build source authority: [Dockerfile](Dockerfile).
