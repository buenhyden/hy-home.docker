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
| `docker compose --profile tooling up -d`                   | Locust 인프라 전체(Master/Worker) 시작 |
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

## Validation

- Run `bash scripts/hardening/check-all-hardening.sh 09-tooling` after README or Compose reference changes that affect Locust.
- Run `bash scripts/validation/check-repo-contracts.sh` to keep service documentation and operation links synchronized.
- Runtime rendering must include root `infra_net`, `influxdb`, and `influxdb_api_token` context because the root include is optional/commented.

## Troubleshooting

- Start with the hardening check to confirm Locust network, port, and mounted test references stay declared.
- Check Locust logs and the linked runbook before changing test runners or target URLs.

## Related Documents

- **Guide**: [Locust Load Testing Guide](../../../docs/05.operations/guides/09-tooling/locust.md)
- **Policy**: [Locust operations policy](../../../docs/05.operations/policies/09-tooling/locust.md)
- **Runbook**: [Locust recovery runbook](../../../docs/05.operations/runbooks/09-tooling/locust.md)

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | 🦗 Locust Load Testing Infrastructure service leaf in `09-tooling`; services: `locust-master`, `locust-worker`; root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/locust/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `LOCUST_INFLUXDB_HOST`, `LOCUST_INFLUXDB_PORT`, `LOCUST_INFLUXDB_ORG`, `LOCUST_INFLUXDB_BUCKET`; profiles: `tooling`, `testing` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/locust/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `locust-data:/mnt/locust:rw`, `locust-data` |
| Ports | `${LOCUST_HOST_PORT:-18089}:${LOCUST_PORT:-8089}` |
| Labels | `hy-home.tier` |
| Secret refs | names: `influxdb_api_token`; mounts: `/run/secrets/influxdb_api_token` |
| Healthcheck | Compose healthcheck declared for `locust-master`, `locust-worker` |
| Operations | [Guide](../../../docs/05.operations/guides/09-tooling/locust.md), [Policy](../../../docs/05.operations/policies/09-tooling/locust.md), [Runbook](../../../docs/05.operations/runbooks/09-tooling/locust.md) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with the hardening check, then inspect service logs and linked operations/runbook evidence in an approved runtime context. |

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
