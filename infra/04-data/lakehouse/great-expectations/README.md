---
title: "Great Expectations (lakehouse data quality)"
version: "1.0.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2026-09-23"
---

<!-- [ID:04-data:lakehouse-great-expectations] -->
# Great Expectations (lakehouse data quality)

> On-demand OPTIONAL data quality job that checks Iceberg tables through Trino against tracked suites.

## Overview

Great Expectations(GX Core)는 `lakehouse` profile로 선택되는 **OPTIONAL** one-shot
작업입니다. `suites/`의 suite 파일마다 대상 table과 expectation을 적고, 작업은
Trino(`trino:8080`, catalog `lakehouse`)로 table을 읽어 검사합니다. 기본 명령은
suite 목록만 출력합니다. exit `0`은 모든 suite 통과, `1`은 expectation 실패,
`2`는 검사 자체를 못 한 경우(suite 없음·형식 오류·Trino 오류)입니다. table이나 디스크에 쓰지
않고, 사용 통계를 보내지 않습니다.

## Audience

이 README의 주요 독자:

- Data engineers
- Operators
- AI Agents

## Scope

### In Scope

- GX Core with an ephemeral context, a Trino SQL data source and whole-table batches.
- Suites as tracked JSON under `suites/`.

### Out of Scope

- Data Docs, a stored GX project, checkpoints with actions and notifications.
- Spark or Flink data sources; Trino reads every Iceberg table they write.

## Structure

```text
great-expectations/
├── README.md             # This file
├── Dockerfile            # python base plus requirements.txt
├── requirements.txt      # GX Core and the Trino SQLAlchemy dialect (Renovate)
├── hyhome-gx.py          # list | validate [SUITE...]
├── docker-compose.yml    # One-shot job
└── suites/
    └── lakehouse-rehearsal.json   # Suite the rehearsal runs against test.gx_rehearsal
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Engine** | GX Core (version in `requirements.txt`) | Ephemeral context, no project files |
| **Data source** | Trino SQLAlchemy dialect | `trino://great-expectations@trino:8080/lakehouse` |
| **Runtime** | Python (base image in `Dockerfile`) | UID 1000, 1 CPU, 512 MiB, read-only root |

## Configuration

### Suite File

```json
{"name": "orders", "table": "dev.orders",
 "expectations": [{"type": "expect_column_values_to_not_be_null", "kwargs": {"column": "id"}}]}
```

`name`, when present, must match the file name; `table` is exactly
`<schema>.<table>` in the `lakehouse` catalog; each expectation is a GX
expectation type and its arguments. Some expectation arguments are raw SQL, so
suites are reviewed as code.

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `GX_TRINO_URL` | Yes (set in Compose) | SQLAlchemy URL of Trino and the catalog. |
| `GX_ANALYTICS_ENABLED` | Yes (set in Compose) | `false`: no usage events. |

No secret: Trino has no authentication.

## Available Scripts

Running the job requires runtime approval; it starts Trino when needed.

| Command | Description |
| :--- | :--- |
| `docker compose --profile lakehouse run --rm great-expectations` | List suites. |
| `docker compose --profile lakehouse run --rm great-expectations validate orders` | Check one suite; exit `1` on failure. |
| `docker compose --profile lakehouse run --rm great-expectations validate` | Check every suite. |

## Validation

- `HYHOME_COMPOSE_PROFILES=lakehouse bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests.test_3_great_expectations_passes_and_fails_through_trino`

## Troubleshooting

- `no suite '<name>'`: the file `suites/<name>.json` is missing.
- `TABLE_NOT_FOUND` from Trino: the suite's `table` does not exist in the `lakehouse` catalog.
- Exit `1` with `"success": false`: an expectation failed; the preceding lines name it.
- Exit `2`: the run checked nothing (no suites, malformed suite, Trino or GX error); stderr says which.

## Related Documents

- **Guide**: Lakehouse Usage Guide (`docs/05.operations/guides/0094-lakehouse.md`)
- **Policy**: Lakehouse Operations Policy (`docs/05.operations/policies/0094-lakehouse.md`)
- **Runbook**: Lakehouse Recovery Runbook (`docs/05.operations/runbooks/0094-lakehouse.md`)
- [Documentation index](../../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Great Expectations leaf in `04-data/lakehouse`; services: `great-expectations`; unconditional root include, profile-selected, in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/lakehouse/great-expectations/docker-compose.yml` |
| Config files | `Dockerfile`, `requirements.txt`, `hyhome-gx.py`, `docker-compose.yml`, `suites/*.json` |
| Config values | profiles: `lakehouse` |
| Compose linkage | unconditional root include, profile-selected, in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/lakehouse/great-expectations/docker-compose.yml` |
| Networks | `object_net` |
| Volumes | `./suites:/opt/hyhome/suites:ro` |
| Ports | none |
| Labels | `hy-home.tier` |
| Secret refs | none |
| Healthcheck | none (one-shot job) |
| Operations | Guide (`docs/05.operations/guides/0094-lakehouse.md`), Policy (`docs/05.operations/policies/0094-lakehouse.md`), Runbook (`docs/05.operations/runbooks/0094-lakehouse.md`) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Run `validate <suite>`, then follow the runbook. |

## How to Work in This Area

1. Add a suite as one JSON file under `suites/`; keep `test.gx_rehearsal` for the rehearsal.
2. Renovate updates `requirements.txt` and the `FROM` image; a GX bump also changes the `image:` tag in `docker-compose.yml` and the version projection (`scripts/operations/sync-tech-stack-versions.sh`). Rebuild and rerun the rehearsal after either.
3. Suites only read tables; a check that needs a write belongs to Spark or Trino.

Runtime image authority is [docker-compose.yml](docker-compose.yml);
the [derived Compose image projection](../../../tech-stack.versions.json) is drift evidence.
