---
title: "Loki Log Aggregation System"
version: "1.0.4"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2026-01-12"
---

# Loki Log Aggregation System

## Overview

`infra/06-observability/loki`에는 `06-observability` 티어의 Loki 구현이 들어 있습니다. Loki는 compose 서비스 `loki`, 컨테이너 `infra-loki`, 이미지 [declared runtime image](../../tech-stack.versions.json)로 실행되며 작업 데이터를 `loki-data`에 저장하고 로그 청크와 인덱스에는 SeaweedFS S3 버킷 `loki-bucket`을 사용합니다. 커스텀 이미지는 Loki의 업스트림 바이너리를 유지하면서 Docker Secret `seaweedfs_s3_loki_secret_key`에서 `S3_SECRET_KEY`를 내보내는 작은 엔트리포인트를 거쳐 `-config.expand-env=true` 옵션으로 Loki를 시작합니다.

## Audience

- 애플리케이션과 인프라 로그를 디버깅하는 Developers
- 보존, 저장, 쿼리 성능을 관리하는 SREs
- Loki 준비 상태와 SeaweedFS 연결을 유지 관리하는 Operators
- 시크릿 값을 노출하지 않고 근거를 수집하는 AI Agents

## Scope

### In Scope

- Grafana Alloy에서 `http://loki:3100/loki/api/v1/push`로의 로그 수집
- SeaweedFS 기반 Loki 저장소와 버킷 `loki-bucket`
- `config/loki-config.yaml`의 보존 및 compactor 설정
- Grafana 데이터소스 `Loki`를 통한 LogQL 쿼리
- Compose 서비스, 커스텀 이미지, 엔트리포인트, 시크릿, 라우트, 준비 상태 경계

### Out of Scope

- 애플리케이션 측 로깅 SDK 변경
- 활성 보존 정책을 넘어서는 장기 감사 아카이빙
- Loki 서비스 경계 밖의 SeaweedFS 버킷 라이프사이클 정책
- 운영 근거 없이 이루어지는 런타임 보존, 리소스, 시크릿, 라우트 변경

## Structure

```text
loki/
├── config/
│   └── loki-config.yaml   # Loki config with SeaweedFS, retention, compactor, and ruler settings
├── docker-entrypoint.sh   # Exports S3_SECRET_KEY from Docker Secret
├── Dockerfile             # Builds declared runtime image from upstream Loki plus entrypoint
└── README.md              # This file
```

## Service Boundary

| Field | Evidence |
| --- | --- |
| Purpose | `06-observability` 티어의 로그 수집 및 LogQL 쿼리 백엔드 |
| Compose service | `infra/06-observability/docker-compose.yml`의 `loki` |
| Compose linkage | `infra/06-observability/docker-compose.yml`에 선언됨 |
| Container | `infra-loki` |
| Image | [declared runtime image](../../tech-stack.versions.json) |
| Runtime user | `10001:10001` |
| Config files | `config/loki-config.yaml`, `Dockerfile`, `docker-entrypoint.sh` |
| Config values | SeaweedFS S3 엔드포인트 `http://seaweedfs-s3:8333`, 버킷 `loki-bucket`, 보존 `168h`, compactor 주기 `10m` |
| Config mount | `./loki/config/loki-config.yaml:/etc/loki/loki-config.yaml:ro` |
| Volumes | `loki-data:/loki:rw` |
| Secret refs | `seaweedfs_s3_loki_secret_key` |
| Environment refs | `S3_ACCESS_KEY` |
| Networks | `edge_net`, `object_net`, `obs_net` |
| Ports | `${LOKI_HOST_PORT:-3100}:${LOKI_PORT:-3100}` |
| Route | `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 거치는 `https://loki.${DEFAULT_URL}` |
| Labels | `traefik.http.routers.loki.*`, `traefik.http.services.loki.loadbalancer.server.port` |
| Healthcheck | `http://127.0.0.1:${LOKI_PORT:-3100}/ready` |
| Operations | Guide (`docs/05.operations/guides/0043-loki.md`), Policy (`docs/05.operations/policies/0043-loki.md`), Runbook (`docs/05.operations/runbooks/0043-loki.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh), [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | 연결된 런북, compose 설정 렌더링, 서비스 로그, 마스킹된 저장소/수집 근거로 시작합니다 |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose --profile obs up -d loki` | 저장소 루트에서 Loki 시작 |
| `docker compose --profile obs restart loki` | 이미 연결된 설정 파일 내용의 승인된 재적용; Compose·시크릿 참조·이미지 또는 baked entrypoint 변경은 RUN-0043을 따르되 marker 보존 결함이 해소되기 전에는 재생성 중단 |
| `docker compose --profile obs logs -f loki` | 저장소 루트에서 Loki 로그 확인 |

## Configuration

### Storage and Retention

- **Bucket**: `loki-bucket`
- **S3 endpoint**: `http://seaweedfs-s3:8333`
- **Access key source**: 환경 변수 참조 `S3_ACCESS_KEY`
- **Secret key source**: Docker Secret `seaweedfs_s3_loki_secret_key`, `S3_SECRET_KEY`로 내보내짐
- **Retention**: `retention_enabled: true`, `retention_period: 168h`
- **Compactor**: `compaction_interval: 10m`, `retention_delete_delay: 2h`

### Ingestion and Querying

- Alloy는 `loki.write.local_loki`를 통해 `http://loki:3100/loki/api/v1/push`로 로그를 전송합니다.
- Grafana는 URL `http://loki:3100`으로 데이터소스 `Loki`를 프로비저닝합니다.
- `service_name`, `env`, `stream`처럼 카디널리티가 낮은 레이블로 Grafana Explore에서 쿼리합니다.

## How to Work in This Area

1. 사용법과 쿼리 맥락은 Loki 가이드(`docs/05.operations/guides/0043-loki.md`)를 따릅니다.
2. 준비 상태, 저장소, 수집, 재시작, 롤백 절차는 Loki 런북(`docs/05.operations/runbooks/0043-loki.md`)을 따릅니다.
3. `S3_SECRET_KEY`, 렌더링된 환경 변수 값, SeaweedFS 자격 증명은 문서, 로그, 태스크 근거, 커밋 메시지에 남기지 않습니다.
4. 계획/태스크 근거와 롤백 기록 없이는 보존, compactor, SeaweedFS 버킷, 리소스 상한, 시크릿 참조, 레이블 카디널리티 정책, 라우트 미들웨어를 변경하지 않습니다.

## Validation

- Compose 또는 설정 참조를 변경한 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 인프라 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.
- `docker compose --profile obs ps loki`와 `docker exec infra-loki wget -qO- http://127.0.0.1:3100/ready`로 준비 상태를 확인합니다.
- `rg -n 'bucketnames: loki-bucket|retention_enabled: true|retention_period: 168h|compaction_interval: 10m' infra/06-observability/loki/config/loki-config.yaml`로 저장소/보존 설정을 확인합니다.
- `rg -n 'loki.source.docker|loki.write|http://loki:3100/loki/api/v1/push' infra/06-observability/alloy/config/config.alloy`로 수집 연결을 확인합니다.

## Troubleshooting

- 네트워크, 볼륨, 시크릿, 레이블 참조가 올바르게 렌더링되는지 `docker compose --profile obs config --quiet`로 먼저 확인합니다.
- 설정이나 시크릿 참조를 변경하기 전에 컨테이너 로그와 연결된 런북을 확인합니다.
- 로그가 누락되면 Alloy `loki.write` 상태와 Grafana 데이터소스 `Loki`를 확인합니다.
- 저장소 오류 시 SeaweedFS, 버킷, 보존, compactor, 자격 증명 오류에 대한 마스킹된 Loki 로그 증상을 확인합니다.
- 쿼리 지연 시 레이블 카디널리티를 검토하고 카디널리티가 높은 필드를 레이블로 승격하지 않습니다.

### Convergence contract

- Classification: **HOME**. Exact profiles: `obs`, `logs`.
- Source authority: `infra/06-observability/docker-compose.yml`과 이 패키지의 추적 설정/빌드 입력. 이미지 선언이 권위이며 `infra/tech-stack.versions.json`은 파생 값입니다.
- Root preflight: `docker compose --profile obs config --quiet`. Root targeted start: `docker compose --profile obs up -d loki`.
- 안정적인 진입점은 [docs/README.md](../../../docs/README.md)입니다. 정확한 Stage 05 경로: `docs/05.operations/guides/0043-loki.md`; ID: `GDE-0043`, `POL-0043`, `RUN-0043`.
- 해당 런북의 계획된 격리 복구 절차를 따릅니다. 날짜가 명시된 근거가 없는 한 아직 실행되지 않은 것으로 간주하며 이 README에서 운영 중인 상태를 변경하지 않습니다.

## Related Documents

- [infra/README.md](../../README.md)
- Operations index (`docs/05.operations/README.md`)
- Loki guide (`docs/05.operations/guides/0043-loki.md`)
- Loki policy (`docs/05.operations/policies/0043-loki.md`)
- Loki runbook (`docs/05.operations/runbooks/0043-loki.md`)
- [Documentation index](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.

Build source authority: [Dockerfile](Dockerfile).
