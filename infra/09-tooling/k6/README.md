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
- **Benchmark Orchestration**: 마스터 노드를 통한 분산 부하 생성 시나리오 관리.
- **Metric Exporting**: InfluxDB 연동을 통한 성능 지표 실시간 전송.
- **Worker Scaling**: `k6-worker`(Locust 기반) 노드의 동적 확장.

### Out of Scope
- **Metric Storage Layer**: InfluxDB 자체의 운영 및 백업은 Data 계층 담당.
- **Visualization**: Grafana 대시보드 연동 작업.

## Structure

```text
k6/
├── locustfile.py       # 테스트 시나리오 정의 (Python 기반)
├── Dockerfile          # Locust 커스텀 빌드 (influxdb-client 포함)
├── docker-compose.yml  # 분산 테스팅 오케스트레이션
└── README.md           # This file
```

## Available Scripts

| Command                                                    | Description                      |
| ---------------------------------------------------------- | -------------------------------- |
| `docker-compose --profile tooling up -d`                   | 테스팅 인프라 전체 시작          |
| `docker compose up --scale k6-worker=N -d`                | 워커 노드 수 확장 (N개 지정)     |
| `docker compose logs -f k6-master`                        | 마스터 노드 로그 및 상태 모니터링 |

## Configuration

### Environment Variables

| Variable          | Required | Description                                  |
| ----------------- | -------- | -------------------------------------------- |
| `LOCUST_HOST_PORT` | No      | 외부 UI 접속 포트 (기본: 18089)              |
| `INFLUXDB_ORG`    | Yes      | InfluxDB v2 조직 명칭                        |
| `INFLUXDB_BUCKET` | Yes      | 지표를 저장할 버켓 명칭                      |

## Related References

- **Guide**: [k6 Performance Testing Guide](../../../docs/07.guides/09-tooling/k6.md)
- **Operation**: [k6 Operations Policy](../../../docs/08.operations/09-tooling/k6.md)
- **Runbook**: [k6 Recovery Runbook](../../../docs/09.runbooks/09-tooling/k6.md)

---

Copyright (c) 2026. Licensed under the MIT License.
