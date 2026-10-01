---
title: "InfluxDB (TSDB)"
version: "1.0.6"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2025-11-21"
---

# InfluxDB (TSDB)

> 메트릭과 분석을 위한 고성능 시계열 데이터베이스입니다.

## Overview

`influxdb` 서비스는 `hy-home.docker`의 시계열 데이터 영속성 계층을 제공한다. 현재 구현은 InfluxDB 3 Core 단일 compose이며 SQL 조회와 HTTP line-protocol 쓰기의 source interface를 정의한다.

## Audience

이 README의 주요 독자:

- **Developers**: 지표 통합 및 데이터 연동
- **Operators**: 자원 관리 및 성능 튜닝
- **AI Agents**: 인프라 탐색 및 메트릭 분석

## Scope

### In Scope

- 관측성을 위한 시계열 데이터 영속성
- InfluxDB 3 Core database와 line-protocol write endpoint source 계약 확인
- 별도 runtime 승인이 필요한 token provisioning 경계 확인
- bind-backed named volume 기반 data/plugin persistence 확인

### Out of Scope

- 장기 로그 저장 (-> Loki 담당)
- 객체 저장 (-> SeaweedFS 담당)
- 실시간 스트림 처리 (-> `lakehouse/flink` 담당)

## Structure

```text
influxdb/
├── docker-compose.yml       # InfluxDB 3 Core 배포
└── README.md                # 이 파일
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `04-data`의 InfluxDB (TSDB) 서비스 leaf; primary service: `influxdb`; [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/04-data/influxdb/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | exact profile: `influxdb`; database 이름은 명시적 write-request 입력이며 root 환경 키가 아님 |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 |
| Networks | `edge_net` |
| Volumes | `influxdb-data:/var/lib/influxdb3/data:rw`, `influxdb-plugins:/var/lib/influxdb3/plugins:rw` |
| Ports | 선언된 호스트 포트 없음; Traefik 서비스 포트 `${INFLUXDB_PORT:-8181}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.influxdb.rule`, `traefik.http.routers.influxdb.entrypoints`, `traefik.http.routers.influxdb.tls`, `traefik.http.routers.influxdb.middlewares`, `traefik.http.services.influxdb.loadbalancer.server.port` |
| Secret refs | 루트 Compose가 `influxdb_api_token`과 `influxdb_password`를 저장소 메타데이터로 선언하지만 루트 선언과 메타데이터는 leaf 서버 배선이 아님; 이 leaf는 두 secret 모두 마운트하지 않으며 서버 token을 provisioning하지 않음 |
| Write API | `POST http://influxdb:8181/api/v3/write_lp?db=<operator-selected-database>`는 승인된 operator/named token이 필요함; token 생성/provisioning과 인증된 write acceptance는 별도 runtime 승인이 필요하며 아직 미확인 상태임 |
| Healthcheck | `http://127.0.0.1:8181/`을 probe하며 `200`, `204`, `401`을 정상으로 인정함 |
| Operations | Guide (`docs/05.operations/guides/0017-influxdb.md`), Policy (`docs/05.operations/policies/0017-influxdb.md`), Runbook (`docs/05.operations/runbooks/0017-influxdb.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | 연결된 저장소 validator와 서비스 로그부터 시작함; service-local compose parsing에는 root 네트워크/secret 컨텍스트 또는 local validation overlay가 필요함 |

## How to Work in This Area

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../../.agents/governance/agentic.md)와 [documentation protocol](../../../.agents/governance/documentation-protocol.md)을 따른다.

1. 아키텍처 세부 사항은 InfluxDB 시스템 가이드 (`docs/05.operations/guides/0017-influxdb.md`)를 참조한다.
2. 데이터 보존 및 보안 규약은 운영 정책 (`docs/05.operations/policies/0017-influxdb.md`)을 따른다.
3. 수집 장애 발생 시 복구 런북 (`docs/05.operations/runbooks/0017-influxdb.md`)을 참조한다.
4. 루트 secret 선언은 메타데이터일 뿐입니다. 소스만으로는 인가를 증명할 수 없으며 token 생성/provisioning과 인증된 write acceptance에는 별도 runtime 승인이 필요합니다.

5. 이 README를 읽고 InfluxDB 3 Core의 database/endpoint source contract와 token-provisioning 승인 경계를 파악한다.
6. Token provisioning은 별도 runtime 승인과 인증 쓰기 acceptance evidence 없이는 완료로 간주하지 않는다.
7. 데이터 보존 정책을 수정하기 전에 반드시 운영 정책 문서를 대조한다.

## Validation

Classification은 `OPTIONAL`입니다. 복구는 InfluxDB 3 Core의 순서 있는 local-object-store 세트(snapshot, database, WAL, catalog, checkpoint)와 새로운 호환 target을 사용하며 내장 백업 명령이나 live 데이터 복사는 주장하지 않습니다. 소유 artifact는 `docs/05.operations/guides/0017-influxdb.md` 아래의 `GDE-0017`, `POL-0017`, `RUN-0017`입니다.

- InfluxDB에 영향을 주는 README나 Compose 참조 변경 후에는 `python3 scripts/validation/check-document-links.py --mode all`을 실행합니다.
- 서비스 문서와 운영 링크를 동기화하려면 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.

## Troubleshooting

- runtime 증거를 위해 저장소 validator와 `docker compose --profile influxdb logs --tail=120 influxdb`부터 시작합니다.
- 추정된 secret 경로로 write를 진단하지 않습니다. retention, database, 버전 설정을 변경하기 전에 승인된 token provisioning과 인증된 write acceptance를 에스컬레이션합니다.

## Related Documents

- **System Guide**: `docs/05.operations/guides/0017-influxdb.md`
- **Policy**: `docs/05.operations/policies/0017-influxdb.md`
- **Runbook**: `docs/05.operations/runbooks/0017-influxdb.md`
- **공식 token 관리**: [InfluxDB 3 Core token management](https://docs.influxdata.com/influxdb3/core/admin/tokens/)
- **Monitoring**: `https://grafana.${DEFAULT_URL}`
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [derived Compose 이미지 투영](../../tech-stack.versions.json)은 drift 검증에 쓰입니다.
