---
title: "Great Expectations (lakehouse data quality)"
version: "1.0.2"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2026-09-23"
---

<!-- [ID:04-data:lakehouse-great-expectations] -->
# Great Expectations (lakehouse data quality)

> 추적된 suite를 기준으로 Trino를 통해 Iceberg table을 검사하는 on-demand OPTIONAL 데이터 품질 job입니다.

## Overview

Great Expectations(GX Core)는 `lakehouse` profile로 선택되는 **OPTIONAL** one-shot
작업입니다. `suites/`의 suite 파일마다 대상 table과 expectation을 적고 작업은
Trino(`trino:8080`, catalog `lakehouse`)로 table을 읽어 검사합니다. 기본 명령은
suite 목록만 출력합니다. exit `0`은 모든 suite 통과, `1`은 expectation 실패,
`2`는 검사 자체를 못 한 경우(suite 없음·형식 오류·Trino 오류)입니다. table이나 디스크에 쓰지
않고 사용 통계를 보내지 않습니다.

## Audience

이 README의 주요 독자:

- Data engineers
- Operators
- AI Agents

## Scope

### In Scope

- Ephemeral context, Trino SQL data source, whole-table batch를 사용하는 GX Core.
- `suites/` 아래 추적된 JSON으로 정의된 suite.

### Out of Scope

- Data Docs, 저장된 GX project, action/notification이 있는 checkpoint.
- Spark나 Flink data source; Trino가 이들이 쓰는 모든 Iceberg table을 읽습니다.

## Structure

```text
great-expectations/
├── README.md             # 이 파일
├── Dockerfile            # python base와 requirements.txt
├── requirements.txt      # GX Core와 Trino SQLAlchemy dialect(Renovate)
├── hyhome-gx.py          # list | validate [SUITE...]
├── docker-compose.yml    # one-shot job
└── suites/
    └── lakehouse-rehearsal.json   # rehearsal이 test.gx_rehearsal에 대해 실행하는 suite
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Engine** | GX Core(버전은 `requirements.txt`) | ephemeral context, project 파일 없음 |
| **Data source** | Trino SQLAlchemy dialect | `trino://great-expectations@trino:8080/lakehouse` |
| **Runtime** | Python(`Dockerfile`의 base image) | UID 1000, 1 CPU, 512 MiB, read-only root |

## Configuration

### Suite File

```json
{"name": "orders", "table": "dev.orders",
 "expectations": [{"type": "expect_column_values_to_not_be_null", "kwargs": {"column": "id"}}]}
```

`name`이 있으면 파일 이름과 일치해야 합니다. `table`은 `lakehouse` catalog
안에서 정확히 `<schema>.<table>` 형식입니다. 각 expectation은 GX expectation type과
그 인자입니다. 일부 expectation 인자는 raw SQL이므로 suite는 코드처럼
리뷰합니다.

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `GX_TRINO_URL` | Yes(Compose에서 설정) | Trino와 catalog의 SQLAlchemy URL. |
| `GX_ANALYTICS_ENABLED` | Yes(Compose에서 설정) | `false`: 사용 이벤트 없음. |

Secret 없음: Trino에 인증이 없습니다.

## Available Scripts

job 실행에는 runtime 승인이 필요합니다. job은 필요할 때 Trino를 시작합니다.

| Command | Description |
| :--- | :--- |
| `docker compose --profile lakehouse run --rm great-expectations` | suite 목록. |
| `docker compose --profile lakehouse run --rm great-expectations validate orders` | 하나의 suite 검사; 실패 시 exit `1`. |
| `docker compose --profile lakehouse run --rm great-expectations validate` | 모든 suite 검사. |

## Validation

- `HYHOME_COMPOSE_PROFILES=lakehouse bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests.test_3_great_expectations_passes_and_fails_through_trino`

## Troubleshooting

- `no suite '<name>'`: `suites/<name>.json` 파일이 없습니다.
- Trino의 `TABLE_NOT_FOUND`: suite의 `table`이 `lakehouse` catalog에 존재하지 않습니다.
- `"success": false`와 함께 exit `1`: expectation이 실패했으며 앞선 줄에 이름이 있습니다.
- Exit `2`: 실행이 아무것도 검사하지 못했습니다(suite 없음, suite 형식 오류, Trino 또는 GX 오류). 원인은 stderr에 나옵니다.

## Related Documents

- **Guide**: Lakehouse Usage Guide (`docs/05.operations/guides/0094-lakehouse.md`)
- **Policy**: Lakehouse Operations Policy (`docs/05.operations/policies/0094-lakehouse.md`)
- **Runbook**: Lakehouse Recovery Runbook (`docs/05.operations/runbooks/0094-lakehouse.md`)
- [문서 인덱스](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `12-analytics`의 Great Expectations leaf; services: `great-expectations`; [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/12-analytics/great-expectations/docker-compose.yml` |
| Config files | `Dockerfile`, `requirements.txt`, `hyhome-gx.py`, `docker-compose.yml`, `suites/*.json` |
| Config values | profiles: `lakehouse` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/12-analytics/great-expectations/docker-compose.yml` |
| Networks | `object_net` |
| Volumes | `./suites:/opt/hyhome/suites:ro` |
| Ports | 없음 |
| Labels | `hy-home.tier` |
| Secret refs | 없음 |
| Healthcheck | 없음(one-shot job) |
| Operations | Guide (`docs/05.operations/guides/0094-lakehouse.md`), Policy (`docs/05.operations/policies/0094-lakehouse.md`), Runbook (`docs/05.operations/runbooks/0094-lakehouse.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `validate <suite>`를 실행한 뒤 runbook을 따름 |

## How to Work in This Area

1. `suites/` 아래에 JSON 파일 하나로 suite를 추가하십시오. rehearsal용 `test.gx_rehearsal`은 유지합니다.
2. Renovate가 `requirements.txt`와 `FROM` 이미지를 갱신합니다. GX 버전이 오르면 `docker-compose.yml`의 `image:` tag와 버전 투영(`scripts/operations/sync-tech-stack-versions.sh`)도 바뀝니다. 어느 쪽이든 변경 후 재빌드하고 rehearsal을 다시 실행하십시오.
3. Suite는 table을 읽기만 합니다. 쓰기가 필요한 검사는 Spark나 Trino의 몫입니다.

런타임 이미지 권한은 [docker-compose.yml](docker-compose.yml)이 소유하며
[derived Compose 이미지 투영](../../tech-stack.versions.json)은 drift 증거입니다.
