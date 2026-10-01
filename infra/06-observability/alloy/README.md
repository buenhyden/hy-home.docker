---
title: "Grafana Alloy Unified Collector"
version: "1.0.4"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2026-01-12"
---

# Grafana Alloy Unified Collector

## Overview

Alloy는 `hy-home.docker` 플랫폼의 통합 수집 에이전트입니다. 프로그래밍 가능한 설정(Alloy HCL)으로 메트릭, 로그, 트레이스를 수집·처리·내보내며 레거시 에이전트를 대체합니다. 인프라 내 모든 애플리케이션의 기본 OTLP 게이트웨이 역할을 합니다.

## Audience

이 README의 주요 독자:

- Developers (데이터 수집 및 계측)
- Operators (파이프라인 모니터링 및 튜닝)
- SREs (계층 간 텔레메트리 거버넌스)
- AI Agents (자동화된 트러블슈팅 및 온보딩)

## Scope

### In Scope

- **Ingestion**: OTLP(gRPC/HTTP), Docker 소켓 디스커버리.
- **Processing**: 대상 재레이블링, 메타데이터 보강, 배치 처리.
- **Exporting**:
  - Metrics -> Prometheus가 Alloy `/metrics`를 직접 scrape함; self remote-write는 제거됨
  - Logs -> Loki
  - Traces -> Tempo
  - Profiling -> 선언된 Go pprof/SeaweedFS scrape 소스에서 Pyroscope writer로 전달
- **Status**: Alloy UI를 통한 실시간 파이프라인 디버깅.

### Out of Scope

- **Storage**: 메트릭/로그/트레이스 영속화 (Prometheus/Loki/Tempo에서 관리).
- **Visualization**: 대시보드 (Grafana에서 관리).
- **Instrumentation**: 애플리케이션 측 SDK 구현.

## Structure

```text
alloy/
├── config/    # Telemetry pipeline definitions (HCL)
└── README.md  # This file
```

## How to Work in This Area

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../../.agents/governance/agentic.md)와 [documentation protocol](../../../.agents/governance/documentation-protocol.md)을 따른다.

1. Alloy 가이드(`docs/05.operations/guides/0040-alloy.md`)를 따릅니다.
2. 새로운 파이프라인 컴포넌트나 재레이블링 규칙을 추가하려면 `config.alloy`를 수정합니다.
3. 파이프라인을 디버깅하고 컴포넌트 상태를 확인하려면 `https://alloy.${DEFAULT_URL}`의 Alloy UI에 접속합니다.
4. 변경 사항은 Alloy Operation Policy(`docs/05.operations/policies/0040-alloy.md`)에서 확인합니다.
5. 컨테이너 메타데이터를 자동으로 보강하려면 Alloy의 `discovery.docker`를 사용합니다.

6. **OTLP First**: 향후 호환성을 보장하도록 새로운 애플리케이션 계측에는 `OTLP` 수집을 우선 사용합니다.
7. **Performance**: 고부하 기간의 데이터 손실이나 지연을 방지하려면 Alloy UI로 `batch` 처리 메트릭을 모니터링합니다.
8. **Relabeling Rules**: 새 서비스를 추가할 때는 `config.alloy`의 재레이블링 규칙이 `scope`(infra vs app)를 올바르게 지정하는지 확인합니다.

## Tech Stack

런타임 이미지 고정 값은 [Compose](../docker-compose.yml)에 선언되어 있습니다. [버전 레지스트리](../../tech-stack.versions.json)는 정제된 프로젝션입니다.

| Category  | Technology    | Runtime source | Notes                    |
| :-------- | :------------ | :------ | :----------------------- |
| Collector | Grafana Alloy | Compose에 선언됨 | 통합 에이전트            |
| Protocol  | OTLP          | v1.x    | 표준 인터페이스       |
| Runtime   | Docker        | Latest  | 컨테이너화된 배포 |

## Available Scripts

| Command                        | Description                 |
| :----------------------------- | :-------------------------- |
| `docker compose --profile obs restart alloy` | 저장소 루트에서 설정 변경 사항 적용 |
| `docker compose --profile obs logs -f alloy` | 저장소 루트에서 수집기 로그 확인 |

## Configuration

### Environment Variables

| Variable               | Required | Description                        |
| :--------------------- | :------: | :--------------------------------- |
| `ALLOY_PORT`           |    No    | UI 리스닝 포트 (기본값: 12345) |
| `ALLOY_OTLP_GRPC_PORT` |    No    | OTLP gRPC 포트 (기본값: 4317)     |
| `ALLOY_OTLP_HTTP_PORT` |    No    | OTLP HTTP 포트 (기본값: 4318)     |

## Validation

- Compose 또는 설정 참조를 변경한 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.
- `config.alloy` 변경 후 `docker logs --tail=200 infra-alloy`로 OTLP 파이프라인 상태를 확인합니다.
- Loki/Tempo 전달, Prometheus의 Alloy scrape, 선언된 pprof 소스의 Pyroscope 전달을 각각 확인합니다. 추적 설정 `config/config.alloy`에 scrape 소스가 있어도 실제 수집 성공은 별도 관찰로 검증합니다.

## Troubleshooting

- 네트워크, 볼륨, 시크릿, 레이블 참조가 올바르게 렌더링되는지 `docker compose --profile obs config --quiet`로 먼저 확인합니다.
- 설정이나 시크릿 참조를 변경하기 전에 컨테이너 로그와 연결된 런북을 확인합니다.
- OTLP 수집 오류: 포트 바인딩(`ALLOY_OTLP_GRPC_PORT`, `ALLOY_OTLP_HTTP_PORT`)을 확인하고 애플리케이션이 올바른 Alloy 엔드포인트를 대상으로 하는지 확인합니다.
- 수집기 설정 오류: `config.alloy`의 HCL 문법을 검증하고 `https://alloy.${DEFAULT_URL}`의 Alloy UI에서 컴포넌트 상태를 확인합니다.
- exporter 오류: 다운스트림 서비스(Prometheus, Loki, Tempo, Pyroscope)에 접근 가능한지, 엔드포인트가 `config.alloy`의 내보내기 대상과 일치하는지 확인합니다.
- Docker 소켓/컨테이너 마운트 또는 재레이블링 카디널리티 변경: 현재 정책 경계를 변경하기 전에 중지하고 연결된 런북의 에스컬레이션 경로를 사용합니다.

### Convergence contract

- Classification: **HOME**. Exact profiles: `obs`, `logs`, `tracing`, `profiling`.
- Source authority: `infra/06-observability/docker-compose.yml`과 이 패키지의 추적 설정/빌드 입력. 이미지 선언이 권위이며 `infra/tech-stack.versions.json`은 파생 값입니다.
- Root preflight: `docker compose --profile obs config --quiet`. Root targeted start: `docker compose --profile obs up -d alloy`.
- 안정적인 진입점은 [docs/README.md](../../../docs/README.md)입니다. 정확한 Stage 05 경로: `docs/05.operations/guides/0040-alloy.md`; ID: `GDE-0040`, `POL-0040`, `RUN-0040`.
- 해당 런북의 계획된 격리 복구 절차를 따릅니다. 날짜가 명시된 근거가 없는 한 아직 실행되지 않은 것으로 간주하며 이 README에서 운영 중인 상태를 변경하지 않습니다.

## Related Documents

- **System Guide**: `docs/05.operations/guides/0040-alloy.md`
- **Policy**: `docs/05.operations/policies/0040-alloy.md`
- **Runbooks**: `docs/05.operations/runbooks/0040-alloy.md`
- [Documentation index](../../../docs/README.md)
