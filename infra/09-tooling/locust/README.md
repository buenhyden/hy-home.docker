---
title: "Locust Load Testing Infrastructure"
version: "1.0.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2025-11-24"
---

<!-- [ID:09-tooling:locust] -->
# Locust Load Testing Infrastructure

> `hy-home.docker`를 위한 분산 성능 벤치마킹 및 사용자 시뮬레이션입니다.

## Overview

이 서비스 유닛은 플랫폼의 서비스를 로드 테스팅하기 위한 분산 부하 테스트 엔진(Locust)을 제공합니다. 마스터 노드가 여러 워커 노드를 오케스트레이션해 대규모 동시 트래픽을 시뮬레이션하며 결과는 Locust 통계와 로그를 통해 수집합니다.

## Audience

- QA Engineers (Load testing)
- SREs (Capacity planning)
- Performance Engineers

## Scope

### In Scope

- **Locust Master/Worker**: 분산 부하 생성 및 관리 UI.
- **Custom Docker Build**: pinned Locust base image를 사용하는 빌드.
- **Scenario Orchestration**: `locustfile.py`를 통한 테스트 로직 관리.

### Out of Scope

- **Metric Visualization**: Grafana 대시보드 구성은 관여하지 않음.
- **Long-term Metric Storage**: 장기 지표 저장소의 선택과 운영은 이 leaf의 책임이 아님.

## Structure

```text
locust/
├── locustfile.py       # 기본 테스트 스크립트 (시나리오 정의)
├── Dockerfile          # Pinned Locust base image
├── docker-compose.yml  # Master/Worker 오케스트레이션 정의
└── README.md           # This file
```

## Available Scripts

저장소 루트에서 다음 명령을 실행하며 런타임 승인이 있을 때만 서비스를 시작하거나 확장합니다.

| Command                                                    | Description                      |
| ---------------------------------------------------------- | -------------------------------- |
| `docker compose --profile testing up -d locust-master locust-worker` | 승인된 Locust Master/Worker 시작 |
| `docker compose --profile testing up -d --scale locust-worker=N locust-master locust-worker` | 승인된 테스트의 워커 수 확장 |
| `docker compose --profile testing logs --tail=200 locust-master` | 실행 중인 마스터 로그 확인 |

## Configuration

### Environment Variables

| Variable          | Required | Description                                  |
| ----------------- | -------- | -------------------------------------------- |
| `LOCUST_HOST_PORT` | No      | 외부 UI 접속 포트 (기본: 18089)              |
| `DEFAULT_TOOLING_DIR` | Yes  | Locust 데이터 마운트 경로                    |

## Validation

- Locust에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/hardening/check-all-hardening.sh 09-tooling`을 실행합니다.
- 서비스 문서와 운영 링크를 동기화하려면 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.
- 루트 파일이 이 leaf를 무조건 include하고 `testing` 프로필만 두 서비스를 해석하므로, 런타임 렌더링에는 루트 네트워크 컨텍스트가 포함되어야 합니다.

## Troubleshooting

- Locust 네트워크, 포트, 마운트된 테스트 참조가 계속 선언되어 있는지 hardening 점검으로 먼저 확인합니다.
- 테스트 러너나 대상 URL을 변경하기 전에 Locust 로그와 연결된 런북을 확인합니다.

## Related Documents

- **Guide**: Locust Load Testing Guide (`docs/05.operations/guides/0062-locust.md`)
- **Policy**: Locust operations policy (`docs/05.operations/policies/0062-locust.md`)
- **Runbook**: Locust recovery runbook (`docs/05.operations/runbooks/0062-locust.md`)
- [Documentation index](../../../docs/README.md)

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `09-tooling`의 Locust Load Testing Infrastructure 서비스 leaf; 서비스: `locust-master`, `locust-worker`; [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/locust/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Config files | `docker-compose.yml` |
| Config values | 프로필: `testing`; UI 포트 키: `LOCUST_HOST_PORT`, `LOCUST_PORT` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/locust/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Networks | project default |
| Volumes | `locust-data:/mnt/locust:rw`, `locust-data` |
| Ports | `${LOCUST_HOST_PORT:-18089}:${LOCUST_PORT:-8089}` |
| Labels | `hy-home.tier` |
| Secret refs | 선언되지 않음 |
| Healthcheck | `locust-master`, `locust-worker`에 Compose 헬스체크가 선언되어 있음 |
| Operations | Guide (`docs/05.operations/guides/0062-locust.md`), Policy (`docs/05.operations/policies/0062-locust.md`), Runbook (`docs/05.operations/runbooks/0062-locust.md`) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | hardening 점검으로 시작한 뒤 승인된 런타임 컨텍스트에서 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 검증을 제공합니다.

Build source authority: [Dockerfile](Dockerfile).
