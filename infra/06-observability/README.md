---
title: "Observability Tier (06-observability)"
version: "1.0.9"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
created: "2025-11-12"
---

# Observability Tier (06-observability)

## Overview

`06-observability` 티어는 현재의 LGTM 스택(Loki, Grafana, Tempo, Prometheus)에 Grafana Alloy, Alertmanager, Pushgateway, cAdvisor, Pyroscope를 결합해 구현합니다. 외부 장기 메트릭 저장소는 추적 중인 compose 파일에 선언되어 있지 않습니다.

## Audience

이 README의 주요 독자:

- SREs & Platform Engineers (스택 유지보수)
- Developers (디버깅 및 성능 튜닝)
- AI Agents (자동화된 헬스 모니터링)

## Scope

### In Scope

- LGTM 스택 (Loki, Grafana, Tempo, Prometheus)
- Grafana Alloy (통합 수집기)
- Pyroscope (연속 프로파일링)
- Alertmanager (알림 라우팅)
- cAdvisor (컨테이너 메트릭)
- Pushgateway (배치 작업 메트릭 푸시)
- Gatus (엔드포인트 가용성 모니터링)

### Out of Scope

- 애플리케이션 수준의 비즈니스 분석
- 외부 클라우드 모니터링(Datadog/New Relic)
- 장기 감사 로그 (`04-data` / `03-security`에서 처리)

## Structure

```text
06-observability/
├── alertmanager/    # Alert routing logic
├── alloy/          # Unified telemetry collection
├── gatus/          # Endpoint availability monitoring
├── grafana/        # Dashboards & Visualization
├── loki/           # Log aggregation
├── prometheus/     # Metrics storage
├── pushgateway/    # Batch job metric push endpoint
├── pyroscope/      # Continuous profiling
├── tempo/          # Distributed tracing
├── docker-compose.yml      # Observability compose, selected by obs and dev
└── README.md
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Observability Tier (06-observability) 폴더 색인. 서비스: `prometheus`, `loki`, `tempo`, `alloy`, `grafana`, `cadvisor`, `pyroscope`, `alertmanager`, `pushgateway`, `gatus`; 루트 include는 [root docker-compose.yml](../../docker-compose.yml) -> `infra/06-observability/docker-compose.yml` 경로로 활성화됨 |
| Config files | `docker-compose.yml` |
| Config values | 비밀이 아닌 S3 액세스 키 ID(`loki`, `tempo`), Grafana 서버/OAuth 설정, 서비스 포트를 사용함. 프로필: `obs`, `dev` |
| Compose linkage | 루트 include는 [root docker-compose.yml](../../docker-compose.yml) -> `infra/06-observability/docker-compose.yml` 경로로 활성화됨. `PROMETHEUS_CONFIG_FILE`, `CADVISOR_CPUS`, `CADVISOR_MEM_LIMIT`가 과거에는 별도 파일이었던 토폴로지를 선택함. |
| Networks | `edge_net`, `mng_data_net`, `object_net`, `obs_net` |
| Volumes | Prometheus/Loki/Tempo/Alloy/Grafana/Pyroscope 설정 마운트와 `${DEFAULT_OBSERVABILITY_DIR}` 하위 바인드 기반 명명 데이터 볼륨 |
| Ports | `${LOKI_HOST_PORT:-3100}:${LOKI_PORT:-3100}`, `${TEMPO_HOST_PORT:-3200}:${TEMPO_PORT:-3200}`, `${ALLOY_OTLP_GRPC_HOST_PORT:-4317}:${ALLOY_OTLP_GRPC_PORT:-4317}`, `${ALLOY_OTLP_HTTP_HOST_PORT:-4318}:${ALLOY_OTLP_HTTP_PORT:-4318}`, `${CADVISOR_PORT:-8080}`, `${PUSHGATEWAY_PORT:-9091}`, `${PYROSCOPE_HOST_PORT:-4040}:${PYROSCOPE_PORT:-4040}` |
| Labels | `hy-home.tier`와 Prometheus, Loki, Tempo, Alloy, Grafana, cAdvisor, Pyroscope, Alertmanager, Pushgateway용 Traefik 라우터/서비스 레이블 |
| Secret refs | 이름: `opensearch_exporter_password`, `openbao_token`, `qdrant_read_only_api_key`, `seaweedfs_s3_loki_secret_key`, `seaweedfs_s3_tempo_secret_key`, `grafana_admin_password`, `grafana_client_secret`, `smtp_username`, `smtp_password`, `slack_webhook`; 마운트: `/run/secrets/opensearch_exporter_password`, `/run/secrets/openbao_token`, `/run/secrets/qdrant_read_only_api_key`, `/run/secrets/seaweedfs_s3_loki_secret_key`, `/run/secrets/seaweedfs_s3_tempo_secret_key`, `/run/secrets/grafana_admin_password`, `/run/secrets/grafana_client_secret`, `/run/secrets/smtp_username`, `/run/secrets/smtp_password`, `/run/secrets/slack_webhook` |
| Healthcheck | `prometheus`, `loki`, `tempo`, `alloy`, `grafana`, `cadvisor`, `pyroscope`, `alertmanager`, `pushgateway`에 Compose 헬스체크가 선언되어 있음 |
| Operations | Guide 색인(`docs/05.operations/README.md`), Policy 색인(`docs/05.operations/README.md`), Runbook 색인(`docs/05.operations/README.md`) |
| Validation | [validate-docker-compose.sh](../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | 저장소 루트에서 `docker compose --profile obs config --quiet`를 실행한 뒤 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |

## How to Work in This Area

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../.agents/governance/agentic.md)와 [documentation protocol](../../.agents/governance/documentation-protocol.md)을 따른다.

1. LGTM 스택 가이드(`docs/05.operations/guides/0042-lgtm-stack.md`)를 따릅니다.
2. 데이터 파이핑은 Alloy 수집기 가이드(`docs/05.operations/guides/0040-alloy.md`)를 참고합니다.
3. 보존 정책은 Operations Policy(`docs/05.operations/policies/README.md`)에서 확인합니다.
4. 복구 절차는 Observability Runbook(`docs/05.operations/runbooks/README.md`)을 참고합니다.
5. 텔레메트리 데이터(OTLP)의 기본 진입점으로는 항상 `Alloy`를 사용합니다.
6. 대시보드는 반드시 `grafana/`의 프로비저닝 설정을 통해 코드로 관리해야 합니다. 세부 경로는 [grafana/README.md](grafana/README.md)를 참고합니다.
7. 레코딩 규칙과 알림 규칙은 반드시 `prometheus/`의 설정에서 정의해야 합니다. 세부 경로는 [prometheus/README.md](prometheus/README.md)를 참고합니다.
8. SeaweedFS S3 버킷 상태는 Loki/Tempo 가용성에 직결되므로 모니터링합니다.

## Tech Stack

런타임 이미지 고정 값은 [Compose](docker-compose.yml)에 선언되어 있습니다. [파생된 Compose 이미지 프로젝션](../tech-stack.versions.json)은 드리프트 확인용 뷰입니다.

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| 메트릭    | Prometheus                     | Compose에 선언됨                   |
| 로그       | Loki                           | Compose에 선언됨, SeaweedFS 버킷 `loki-bucket` |
| 트레이싱    | Tempo                          | Compose에 선언됨, SeaweedFS 버킷 `tempo-bucket` |
| 프로파일링  | Pyroscope                      | Compose에 선언됨                    |
| 수집기  | Grafana Alloy                  | Compose에 선언됨                   |
| UI         | Grafana                        | Compose에 선언됨                   |
| 알림   | Alertmanager                   | Compose에 선언됨                   |
| 배치 메트릭 | Pushgateway                 | Compose에 선언됨                   |
| 컨테이너 메트릭 | cAdvisor                | Compose에 선언됨                   |
| 가용성 모니터링 | Gatus                   | Compose에 선언됨                   |

## Configuration

- **Persistence**: Loki와 Tempo는 SeaweedFS(`04-data`)를 S3 호환 오브젝트 스토어로 사용하고 Prometheus와 Pyroscope는 로컬 바인드 기반 볼륨을 사용합니다.
- **Auth**: Grafana는 OAuth2 SSO용으로 Keycloak(`02-auth`)과 통합되어 있습니다.
- **OpenBao metrics**: Prometheus 소스 설정은 전용 `openbao_token` Docker Secret과 OpenBao `prometheus` 정책만 선언합니다. 시크릿 계약은 스테이징 상태로 아직 프로비저닝되지 않았습니다. 과거에 관측된 "Vault 다운/OpenBao 미로드" 상태는 현재 소스 준비 상태와 별개입니다. 추적된 소스 변경만으로는 실행 중인 Prometheus가 해당 잡을 로드했는지, 대상이 정상인지 증명되지 않습니다.
- **Networking**: 모든 텔레메트리 트래픽은 `obs_net`을 통해 흐릅니다.

## Testing

```bash
# Check service health
docker exec infra-prometheus wget -qO- http://localhost:9090/-/healthy

# Verify Alloy configuration
docker exec infra-alloy alloy run --test /etc/alloy/config.alloy
```

## Change Impact

- Loki/Tempo의 보존 기간을 변경하면 SeaweedFS 저장 사용량에 영향을 줍니다.
- Alloy OTLP 엔드포인트를 변경하면 모든 하위 서비스의 텔레메트리가 중단됩니다.
- Grafana 플러그인을 업데이트하면 대시보드를 수동으로 마이그레이션해야 할 수 있습니다.

## Validation

- 옵저버빌리티 스택에 영향을 주는 README 또는 Compose 참조 변경 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 옵저버빌리티 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.

## Troubleshooting

- 저장소 루트에서 `docker compose --profile obs config --quiet`로 LGTM 서비스, 네트워크, 볼륨, 시크릿 참조가 렌더링되는지 먼저 확인합니다.
- 서비스별 로그를 먼저 확인한 뒤 데이터 경로 장애는 연결된 옵저버빌리티 런북을 따릅니다.

### Convergence service and command map

모든 명령은 저장소 루트에서 실행합니다. `docker compose --profile <profile> config --quiet`는 정적 사전 점검이고, `docker compose --profile <profile> up -d <service>`는 지정한 대상을 시작합니다. profile 선택을 바꿔도 이미 실행 중인 컨테이너는 자동으로 중지되지 않습니다. 새 대상에 Pushgateway가 없거나 `tracing`·`profiling`이 빠지면 해당 Pushgateway, Tempo, Pyroscope를 명시적으로 중지해야 합니다.

| Service | Class | Exact profiles |
| --- | --- | --- |
| `prometheus` | HOME | `obs`, `obs-core`, `dev`, `alerting`, `batch-metrics` |
| `grafana` | HOME | `obs`, `obs-core`, `dev`, `logs`, `tracing`, `profiling`, `alerting`, `batch-metrics` |
| `loki` | HOME | `obs`, `logs` |
| `alloy` | HOME | `obs`, `logs`, `tracing`, `profiling` |
| `node-exporter`, `cadvisor` | HOME | `obs`, `obs-host`, `dev` |
| `gatus` | HOME | `obs`, `availability`, `dev` |
| `alertmanager` | HOME | `obs`, `alerting` |
| `tempo` | HOME | `obs`, `tracing` |
| `pyroscope` | HOME | `obs`, `profiling` |
| `dcgm-exporter` | HOME | `obs-gpu` |
| `pushgateway` | OPTIONAL | `obs`, `batch-metrics` |

안정적인 문서 진입점은 [docs/README.md](../../docs/README.md)입니다. 정확한 Stage 05 대상은 `docs/05.operations/README.md` 하위의 `GDE/POL/RUN-0039`, `0040`, `0041`, `0043`, `0044`, `0045`, `0046`, `0047`, `0049`, `0087`입니다.

## Related Documents

- [04-data](../04-data/README.md) - 텔레메트리 저장용 SeaweedFS S3.
- [02-auth](../02-auth/README.md) - SSO용 Keycloak.
- [01-gateway](../01-gateway/README.md) - UI로 라우팅하는 Traefik.
- [Documentation index](../../docs/README.md)
