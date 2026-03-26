<!-- [ID:09-tooling:locust] -->
# 🦗 Locust Load Testing Infrastructure

> Distributed performance benchmarking and user simulation for `hy-home.docker`.

## Overview

이 서비스 유닛은 플랫폼의 서비스를 로드 테스팅하기 위한 분산 부하 테스트 엔진(Locust)을 제공합니다. 마스터 노드가 여러 워커 노드를 오케스트레이션하여 대규모 동시 트래픽을 시뮬레이션하며, 결과 지표는 **InfluxDB**에 영구 저장됩니다.

## Audience

- QA Engineers (Load testing)
- SREs (Capacity planning)
- Performance Engineers

## Scope

### In Scope

- **Locust Master/Worker**: 분산 부하 생성 및 관리 UI.
- **Custom Docker Build**: `influxdb-client` 등 필수 플러그인이 포함된 빌드.
- **Scenario Orchestration**: `locustfile.py`를 통한 테스트 로직 관리.

### Out of Scope

- **Metric Visualization**: Grafana 대시보드 구성은 관여하지 않음.
- **Long-term Metric Storage**: InfluxDB 자체의 클러스터링 및 백업은 Data 계층 담당.

## Structure

```text
locust/
├── locustfile.py       # 기본 테스트 스크립트 (시나리오 정의)
├── Dockerfile          # Locust 커스텀 빌드 (influxdb-client 포함)
├── docker-compose.yml  # Master/Worker 오케스트레이션 정의
└── README.md           # This file
```

## Available Scripts

| Command                                                    | Description                      |
| ---------------------------------------------------------- | -------------------------------- |
| `docker-compose --profile tooling up -d`                   | Locust 인프라 전체(Master/Worker) 시작 |
| `docker compose up --scale locust-worker=N -d`             | 워커 노드 수 확장 (N개 지정)     |
| `docker compose logs -f locust-master`                     | 마스터 노드 로그 실시간 확인     |

## Configuration

### Environment Variables

| Variable          | Required | Description                                  |
| ----------------- | -------- | -------------------------------------------- |
| `LOCUST_HOST_PORT` | No      | 외부 UI 접속 포트 (기본: 18089)              |
| `INFLUXDB_ORG`    | Yes      | InfluxDB v2 조직 명칭                        |
| `INFLUXDB_BUCKET` | Yes      | 지표를 저장할 버켓 명칭                      |
| `DEFAULT_TOOLING_DIR` | Yes  | Locust 데이터 마운트 경로                    |

## Related References

- **Guide**: [Locust Load Testing Guide](../../../docs/07.guides/09-tooling/locust.md)
- **Operation**: [Locust Operations Policy](../../../docs/08.operations/09-tooling/locust.md)
- **Runbook**: [Locust Recovery Runbook](../../../docs/09.runbooks/09-tooling/locust.md)

---

Copyright (c) 2026. Licensed under the MIT License.
