---
title: "Tempo Distributed Tracing"
version: "1.0.5"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-01-12"
---

# Tempo Distributed Tracing

관련 구성요소의 현재 선언은 [버전 레지스트리](../../tech-stack.versions.json)가 가리키는 Compose 원본에서 확인합니다. 로컬 빌드의 기준 이미지는 [Dockerfile](Dockerfile)에서 확인합니다.

## Overview

Tempo는 S3 호환 백엔드(SeaweedFS)에 트레이스 데이터를 저장합니다. "TraceQL"로 강력한 쿼리를 지원하며 Span ID를 시작점으로 메트릭, 로그, 트레이스 간 상관관계를 분석할 수 있습니다. 또한 span 메트릭과 서비스 그래프를 자동으로 생성합니다.

## Audience

이 README의 주요 독자:

- Backend Developers (지연 시간 분석)
- SRE / DevOps Engineers (시스템 병목 식별)
- AI Agents

## Scope

### In Scope

- Tempo 서비스 설정 및 배포.
- OTLP 트레이스 데이터 수집 및 저장.
- Span 메트릭 및 서비스 그래프 생성.

### Out of Scope

- 애플리케이션 수준 계측 (OpenTelemetry SDK에서 처리).
- 장기 트레이스 아카이빙 (Retention Policy(`docs/05.operations/policies/0049-tempo.md`)에서 관리).

## Structure

```text
tempo/
├── README.md           # This file
├── config/
│   └── tempo.yaml      # Main configuration file
└── Dockerfile          # Custom Tempo image build
```

## Tech Stack

런타임 이미지 고정 값은 [Compose](../docker-compose.yml)에 선언되어 있습니다. [버전 레지스트리](../../tech-stack.versions.json)는 정제된 프로젝션입니다.

| Category | Technology | Runtime source | Role |
| :--- | :--- | :--- | :--- |
| Tracing | [Grafana Tempo](https://github.com/grafana/tempo) | Compose에 선언됨 | 분산 트레이싱 백엔드 |
| Storage | [SeaweedFS](../../04-data/lake-and-object/seaweedfs/README.md) | [Compose](../../04-data/lake-and-object/seaweedfs/docker-compose.yml) | S3 호환 오브젝트 스토어 |
| Ingestion | [Grafana Alloy](../alloy/README.md) | Compose에 선언됨 | OTLP 수신 및 전달 |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose --profile obs up -d tempo` | 저장소 루트에서 Tempo 서비스 시작 |
| `docker compose --profile obs logs -f tempo` | 저장소 루트에서 Tempo 로그 확인 |

## Configuration

- **Ingestion**: gRPC(4317)와 HTTP(4318)를 통한 OTLP를 지원합니다.
- **Persistence**: SeaweedFS의 버킷 `tempo-bucket`.
- **WAL**: write-ahead 로깅에 로컬 디스크를 사용합니다(`/var/tempo/wal`).

## Operational Status

> [!IMPORTANT]
> `config/tempo.yaml`에는 명시적인 보존(retention) 키가 선언되어 있지 않습니다. 정확한 블록 보존 기간은 [config/tempo.yaml](config/tempo.yaml)을 기준으로 확인하고 확정되지 않은 값을 문서에 단정적으로 기재하지 않습니다.

## Validation

- Compose 또는 설정 참조를 변경한 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.
- 설정 변경 후 `docker logs --tail=200 infra-tempo`로 트레이스 수집을 확인합니다.
- Grafana Tempo 데이터소스에 트레이스가 나타나는지 보고 Alloy에서 OTLP 엔드포인트에 접근할 수 있는지 확인합니다.
- `docker exec infra-tempo wget --no-verbose --tries=1 --spider http://localhost:3200/ready`로 Tempo 준비 상태를 확인합니다.

## Troubleshooting

- 네트워크, 볼륨, 시크릿, 레이블 참조가 올바르게 렌더링되는지 `docker compose --profile obs config --quiet`로 먼저 확인합니다.
- 설정이나 시크릿 참조를 변경하기 전에 컨테이너 로그와 연결된 런북을 확인합니다.
- OTLP 수집 오류: 포트 바인딩과 Alloy의 Tempo exporter가 올바른 엔드포인트를 가리키는지 확인합니다.
- 트레이스 쿼리 오류: Grafana의 Tempo 데이터소스 URL이 Tempo 컨테이너의 네트워크 주소와 일치하는지 확인합니다.
- 저장소 문제: Tempo 데이터 볼륨이 마운트되어 있고 백엔드 저장소 경로가 올바르게 설정되어 있는지 확인합니다.
- WAL, 버킷, 보존, 오브젝트 변경: 데이터 손실 위험이 있는 작업을 하기 전에 중지하고 연결된 런북의 에스컬레이션 경로를 사용합니다.

### Convergence contract

- Classification: **OPTIONAL**. Exact profiles: `obs`, `tracing`.
- Source authority: `infra/06-observability/docker-compose.yml`과 이 패키지의 추적 설정/빌드 입력. 이미지 선언이 권위이며 `infra/tech-stack.versions.json`은 파생 값입니다.
- Root preflight: `docker compose --profile obs config --quiet`. Root targeted start: `docker compose --profile obs up -d tempo`.
- 안정적인 진입점은 [docs/README.md](../../../docs/README.md)입니다. 정확한 Stage 05 경로: `docs/05.operations/guides/0049-tempo.md`; ID: `GDE-0049`, `POL-0049`, `RUN-0049`.
- 해당 런북의 계획된 격리 복구 절차를 따릅니다. 날짜가 명시된 근거가 없는 한 아직 실행되지 않은 것으로 간주합니다. 이 README에서는 운영 중인 상태를 변경하지 않습니다.

## Related Documents

- Usage guide (`docs/05.operations/guides/0049-tempo.md`)
- Operations policy (`docs/05.operations/policies/0049-tempo.md`)
- Recovery runbook (`docs/05.operations/runbooks/0049-tempo.md`)
- [Documentation index](../../../docs/README.md)

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `06-observability`의 Tempo Distributed Tracing 서비스 leaf; compose 서비스 `tempo`, 이미지 출처는 [Compose](../docker-compose.yml) |
| Config files | `config`, `config/tempo.yaml` |
| Config values | compose에 선언된 비밀이 아닌 설정 키 없음 |
| Compose linkage | `../docker-compose.yml`에 선언되고 루트 파일이 이를 무조건 include합니다. `tempo`는 `obs`, `dev` 프로필에서 해석됩니다 |
| Networks | `edge_net`, `object_net`, `obs_net` |
| Volumes | `./tempo/config/tempo.yaml:/etc/tempo.yaml:ro`, `tempo-data:/var/tempo:rw` |
| Ports | `${TEMPO_HOST_PORT:-3200}:${TEMPO_PORT:-3200}` |
| Labels | `traefik.http.routers.tempo.*`, `traefik.http.services.tempo.loadbalancer.server.port` |
| Secret refs | `seaweedfs_s3_tempo_secret_key` |
| Healthcheck | `http://localhost:${TEMPO_PORT:-3200}/ready` |
| Operations | Guide (`docs/05.operations/guides/0049-tempo.md`), Policy (`docs/05.operations/policies/0049-tempo.md`), Runbook (`docs/05.operations/runbooks/0049-tempo.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `docker compose --profile obs config --quiet`로 시작한 뒤 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |

## How to Work in This Area

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../../.agents/governance/agentic.md)와 [documentation protocol](../../../.agents/governance/documentation-protocol.md)을 따른다.

1. **TraceQL Analysis**: TraceQL로 지연 시간이 높은 span을 특정 서비스명과 상태 코드와 연관 짓습니다.
2. **Service Graphs**: Grafana에서 서비스 의존성 맵을 시각화하려면 `metrics_generator`가 활성 상태인지 확인합니다.
3. **Storage Health**: 트레이스 수집 공백이 발생하면 SeaweedFS 버킷 가용성을 모니터링합니다.
