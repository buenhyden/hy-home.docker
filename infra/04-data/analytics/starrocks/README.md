---
title: "StarRocks (OLAP Warehouse)"
version: "1.1.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
created: "2026-03-26"
---

# StarRocks (OLAP Warehouse)

> High-performance analytical database for real-time analytics.

## Overview

`starrocks` 스택은 서브-세컨드 OLAP 쿼리 및 대규모 데이터 웨어하우징을 위해 같은 host의 FE/BE pair를 제공한다. `infra_net`과 통합되지만 host-level HA를 제공하지 않는다.

## Audience

이 README의 주요 독자:

- **Data Engineers**: 데이터 수집 및 모델링 설계
- **Analytics Developers**: 대량 데이터 쿼리 최적화
- **AI Agents**: 인프라 탐색 및 웨어하우스 상태 분석

## Scope

### In Scope

- StarRocks Frontend (FE) 및 Backend (BE) 노드 구성
- 데이터 및 메타데이터를 위한 로컬 볼륨 영속성
- Compose healthcheck를 통한 FE/BE 생존 확인
- 단일 FE/BE pair와 BE auto-registration command 확인

### Out of Scope

- 외부 카탈로그 통합 (예: Iceberg, Hudi) (-> 시스템 가이드 참조)
- 루틴 데이터 수집 (ETL) 절차 수행
- 리소스 파티셔닝 및 멀티테넌시 세부 관리

## Structure

```text
starrocks/
├── docker-compose.yml  # Standard StarRocks stack
└── README.md           # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | StarRocks (OLAP Warehouse) service leaf in `04-data`; services: `starrocks-fe`, `starrocks-be`; the root [docker-compose.yml](../../../../docker-compose.yml) includes this leaf's `docker-compose.yml` unconditionally |
| Config files | `docker-compose.yml` |
| Config values | exact profile: `starrocks` |
| Compose linkage | root include active; the `starrocks` profile selects `starrocks-fe` and `starrocks-be` |
| Networks | `infra_net` |
| Volumes | `starrocks-fe-data:/opt/starrocks/fe/meta:rw`, `starrocks-be-data:/opt/starrocks/be/storage:rw`, `starrocks-fe-data`, `starrocks-be-data` |
| Ports | `9030:9030`, `8030:8030`, `8040:8040` |
| Labels | `hy-home.tier` |
| Secret refs | Not declared |
| Healthcheck | Compose healthcheck declared for `starrocks-fe`, `starrocks-be` |
| Operations | Guide (`docs/05.operations/catalog/04-data/0020-starrocks/guide.md`), Policy (`docs/05.operations/catalog/04-data/0020-starrocks/policy.md`), Runbook (`docs/05.operations/catalog/04-data/0020-starrocks/runbook.md`) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Start with linked repository validators and service logs; service-local compose parsing requires root network context or a local validation overlay. |

## How to Work in This Area

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../../../.agents/governance/agentic.md)와 [documentation protocol](../../../../.agents/governance/documentation-protocol.md)을 따른다.

1. 아키텍처 컨텍스트는 시스템 가이드 (`docs/05.operations/catalog/04-data/0020-starrocks/guide.md`)를 참조한다.
2. 자원 거버넌스는 운영 정책 (`docs/05.operations/catalog/04-data/0020-starrocks/policy.md`)을 확인한다.
3. 유지보수 및 복구 절차는 복구 런북 (`docs/05.operations/catalog/04-data/0020-starrocks/runbook.md`)을 사용한다.

4. StarRocks 노드(FE/BE)를 수정하기 전에 메타데이터 저장 경로와 영속성 설정을 확인한다.
5. BE 노드 확장 시 FE 노드에서의 등록 절차를 런북에서 먼저 찾아본다.
6. 데이터 쿼리 효율성을 높이기 위해 스키마 변경을 제안하기 전 시스템 가이드의 최적화 파트를 읽는다.

## Validation

Classification is `OPTIONAL`. Host ports are Compose-declared and no Docker Secret is wired, so default/root authentication is a pre-production gap. Recovery uses repository-backed StarRocks `BACKUP`/`RESTORE` with required repository/export privileges in a fresh isolated pair. Owning artifacts are `GDE-0020`, `POL-0020`, and `RUN-0020`.

- Run `python3 scripts/validation/check-document-links.py --mode all` after README or Compose reference changes that affect StarRocks.
- Run `python3 scripts/validation/run-ci-gate.py --profile changed` to keep service documentation and operation links synchronized.

## Troubleshooting

- Start with repository validators and Docker logs for runtime evidence. Service-local compose config requires root network context or a local validation overlay.
- Check warehouse container logs and the linked runbook before changing retention or persistence settings.

## Related Documents

- [Compose implementation](docker-compose.yml)

- **System Guide**: `docs/05.operations/catalog/04-data/0020-starrocks/guide.md` (`GDE-0020`)
- **Policy**: `docs/05.operations/catalog/04-data/0020-starrocks/policy.md`
- **Runbook**: `docs/05.operations/catalog/04-data/0020-starrocks/runbook.md`
- **Health**: FE/BE healthchecks in `docker-compose.yml`
- [Documentation index](../../../../docs/README.md)

---
Copyright (c) 2026. Analytics Tier Infrastructure.
