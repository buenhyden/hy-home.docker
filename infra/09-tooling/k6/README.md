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
| `docker compose --profile tooling up -d`                   | 테스팅 인프라 전체 시작          |
| `docker compose up --scale k6-worker=N -d`                | 워커 노드 수 확장 (N개 지정)     |
| `docker compose logs -f k6-master`                        | 마스터 노드 로그 및 상태 모니터링 |

## Configuration

### Environment Variables

| Variable          | Required | Description                                  |
| ----------------- | -------- | -------------------------------------------- |
| `LOCUST_HOST_PORT` | No      | 외부 UI 접속 포트 (기본: 18089)              |
| `INFLUXDB_ORG`    | Yes      | InfluxDB v2 조직 명칭                        |
| `INFLUXDB_BUCKET` | Yes      | 지표를 저장할 버켓 명칭                      |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect k6.
- Run `bash scripts/validation/check-repo-contracts.sh` to keep service documentation and operation links synchronized.

## Troubleshooting

- Start with `docker compose config` to confirm k6 network, volume, and metric sink references render.
- Check k6 run output and the linked runbook before changing test scripts or metric destinations.

## Related Documents

- **Guide**: [k6 Performance Testing Guide](../../../docs/05.operations/guides/09-tooling/k6.md)
- **Policy**: [k6 Operations Policy](../../../docs/05.operations/policies/09-tooling/k6.md)
- **Runbook**: [k6 Recovery Runbook](../../../docs/05.operations/runbooks/09-tooling/k6.md)

---

Copyright (c) 2026. Licensed under the MIT License.

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | 🧪 k6 Performance Testing Infrastructure service leaf in `09-tooling`; services: `k6-master`; local compose only: `docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `LOCUST_INFLUXDB_HOST`, `LOCUST_INFLUXDB_PORT`, `LOCUST_INFLUXDB_ORG`, `LOCUST_INFLUXDB_BUCKET`; profiles: `tooling`, `testing` |
| Compose linkage | local compose only: `docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `k6-data:/mnt/locust:rw`, `k6-data` |
| Ports | `${LOCUST_HOST_PORT:-18089}:${LOCUST_PORT:-8089}` |
| Labels | `hy-home.tier` |
| Secret refs | names: `influxdb_api_token`; mounts: `/run/secrets/influxdb_api_token` |
| Healthcheck | Compose healthcheck declared for `k6-master` |
| Operations | [Guide](../../../docs/05.operations/guides/09-tooling/k6.md), [Policy](../../../docs/05.operations/policies/09-tooling/k6.md), [Runbook](../../../docs/05.operations/runbooks/09-tooling/k6.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
