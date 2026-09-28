---
title: "Grafana Visualization and Dashboards"
version: "1.0.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-01-12"
---

# Grafana Visualization and Dashboards

## Overview

`infra/06-observability/grafana`에는 `06-observability` 티어의 Grafana 구현이 들어 있습니다. Grafana는 compose 서비스 `grafana`, 컨테이너 `infra-grafana`, 이미지 [declared runtime image](../../tech-stack.versions.json)로 실행되며 런타임 상태를 `grafana-data`에 저장하고 프로비저닝 및 대시보드 트리를 읽기 전용으로 마운트하며 접근 제어에는 Keycloak Generic OAuth 역할 매핑을 사용합니다.

## Audience

- 메트릭, 로그, 트레이스, 알림, 프로파일을 탐색하는 Developers
- 데이터소스와 대시보드 프로비저닝을 유지 관리하는 SREs
- SSO, 대시보드, 데이터소스 장애를 처리하는 Operators
- 시크릿이나 토큰을 노출하지 않고 마스킹된 근거를 수집하는 AI Agents

## Scope

### In Scope

- Grafana compose 서비스와 보호된 라우트 `https://grafana.${DEFAULT_URL}`
- `provisioning/datasources/datasource.yml`의 데이터소스 프로비저닝
- `provisioning/dashboards/dashboards.yml`의 대시보드 프로비저닝
- `dashboards/`의 대시보드 JSON 파일
- Keycloak Generic OAuth 역할 매핑과 Docker Secret 파일 참조

### Out of Scope

- JSON으로 내보내지 않은 UI 전용 대시보드 변경
- Grafana compose 경계 밖의 Keycloak realm/client 변경
- Prometheus, Loki, Tempo, Pyroscope가 관리하는 백엔드 텔레메트리 저장소
- 운영 근거 없이 이루어지는 런타임 역할 매핑, 시크릿, 라우트, 이미지, 프로비저닝 정책 변경

## Structure

```text
grafana/
├── dashboards/       # Provisioned dashboard JSON tree
├── provisioning/
│   ├── dashboards/   # Dashboard provider YAML
│   └── datasources/  # Datasource provisioning YAML
└── README.md         # This file
```

## Service Boundary

| Field | Evidence |
| --- | --- |
| Purpose | `06-observability` 티어의 메트릭, 로그, 트레이스, 알림, 프로파일 시각화 허브 |
| Compose service | `infra/06-observability/docker-compose.yml`의 `grafana` |
| Compose linkage | `infra/06-observability/docker-compose.yml`에 선언됨 |
| Container | `infra-grafana` |
| Image | [declared runtime image](../../tech-stack.versions.json) |
| Config files | `provisioning/datasources/datasource.yml`, `provisioning/dashboards/dashboards.yml`, 대시보드 JSON 파일 |
| Config values | 데이터소스 UID `Prometheus`, `Loki`, `Tempo`, `alertmanager`; Pyroscope 데이터소스 타입 `grafana-pyroscope-datasource`; 대시보드 프로바이더 `editable: false`; `/admins`, `/editors` 역할 매핑 |
| Volumes | `./grafana/provisioning:/etc/grafana/provisioning:ro`, `./grafana/dashboards:/etc/grafana/dashboards:ro`, `grafana-data:/var/lib/grafana:rw` |
| Secret refs | `grafana_admin_password`, `grafana_client_secret` |
| Networks | `edge_net`, `obs_net` |
| Ports | `traefik.http.services.grafana-svc.loadbalancer.server.port: ${GRAFANA_PORT:-3000}` |
| Labels | `traefik.http.routers.grafana.*`, `traefik.http.routers.grafana-static.*`, `traefik.http.services.grafana-svc.*` |
| Healthcheck | `http://localhost:${GRAFANA_PORT:-3000}/api/health` |
| Operations | Guide (`docs/05.operations/guides/0041-grafana.md`), Policy (`docs/05.operations/policies/0041-grafana.md`), Runbook (`docs/05.operations/runbooks/0041-grafana.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh), [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | 연결된 런북, compose 설정 렌더링, 서비스 로그, 헬스체크, 마스킹된 OAuth/데이터소스 근거로 시작합니다 |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose --profile obs up -d grafana` | 저장소 루트에서 Grafana 시작 |
| `docker compose --profile obs restart grafana` | 승인된 프로비저닝, 대시보드, 시크릿 참조 변경 후 Grafana 재시작 |
| `docker compose --profile obs logs -f grafana` | 저장소 루트에서 Grafana 로그 확인 |

## Configuration

### Datasources

- **Prometheus**: `uid: Prometheus`, URL `http://prometheus:9090`
- **Loki**: `uid: Loki`, URL `http://loki:3100`
- **Tempo**: `uid: Tempo`, URL `http://tempo:3200`, `tracesToLogsV2`가 `Loki`와 연결됨
- **Alertmanager**: `uid: alertmanager`, URL `http://alertmanager:9093`
- **Pyroscope**: 데이터소스 타입 `grafana-pyroscope-datasource`, URL `http://pyroscope:4040`

### Dashboards and Access

- 대시보드 프로바이더는 `/etc/grafana/dashboards/*`에서 JSON 파일을 마운트합니다.
- 프로바이더 `editable: false`는 대시보드를 코드 소유 상태로 유지합니다.
- 대시보드 보유 현황은 `find infra/06-observability/grafana/dashboards -type f -name '*.json' | wc -l`로 확인합니다.
- Keycloak 그룹 `/admins`와 `/editors`는 Grafana `Admin`, `Editor`로 매핑되며 그 외 인증된 사용자는 기본적으로 `Viewer`가 됩니다.
- `grafana_admin_password`와 `grafana_client_secret`은 Docker Secret 파일 참조를 통해 주입됩니다.

## How to Work in This Area

1. 사용법과 프로비저닝 맥락은 Grafana 가이드(`docs/05.operations/guides/0041-grafana.md`)를 따릅니다.
2. 준비 상태, SSO, 데이터소스, 대시보드 프로비저닝, 재시작, 롤백 절차는 Grafana 런북(`docs/05.operations/runbooks/0041-grafana.md`)을 따릅니다.
3. 관리자 비밀번호, OAuth 클라이언트 시크릿, 토큰, 렌더링된 시크릿 값은 문서, 로그, 태스크 근거, 커밋 메시지에 남기지 않습니다.
4. 계획/태스크 근거와 롤백 기록 없이는 역할 매핑, 데이터소스 UID, 대시보드 프로바이더 잠금, 시크릿 참조, 이미지 버전, 라우트 미들웨어를 변경하지 않습니다.

## Validation

- Compose 또는 설정 참조를 변경한 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 인프라 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.
- `docker compose --profile obs ps grafana`와 `docker exec infra-grafana wget -q --spider http://localhost:3000/api/health`로 준비 상태를 확인합니다.
- `rg -n 'uid: Prometheus|uid: Loki|uid: Tempo|uid: alertmanager|type: grafana-pyroscope-datasource' infra/06-observability/grafana/provisioning/datasources/datasource.yml`로 데이터소스 프로비저닝을 확인합니다.
- `rg -n 'folder:|editable: false|path: /etc/grafana/dashboards' infra/06-observability/grafana/provisioning/dashboards/dashboards.yml`로 대시보드 프로비저닝을 확인합니다.
- `find infra/06-observability/grafana/dashboards -type f -name '*.json' | wc -l`로 대시보드 보유 현황을 확인합니다.

## Troubleshooting

- 네트워크, 볼륨, 시크릿, 환경, 레이블 참조가 올바르게 렌더링되는지 `docker compose --profile obs config --quiet`로 먼저 확인합니다.
- 설정이나 시크릿 참조를 변경하기 전에 컨테이너 로그와 연결된 런북을 확인합니다.
- SSO 실패 시 마스킹된 OAuth/역할 매핑 로그를 확인하고 `/admins` 또는 `/editors` 그룹 소속을 별도로 확인합니다.
- 데이터소스 오류 시 프로비저닝 YAML에서 데이터소스 UID와 백엔드 엔드포인트를 확인합니다.
- 대시보드 로딩 오류 시 대시보드 프로바이더 경로와 대시보드 JSON 파일을 검증합니다.

### Convergence contract

- Classification: **HOME**. Exact profiles: `obs`, `obs-core`, `dev`, `logs`, `tracing`, `profiling`, `alerting`, `batch-metrics`.
- Source authority: `infra/06-observability/docker-compose.yml`과 이 패키지의 추적 설정/빌드 입력. 이미지 선언이 권위이며 `infra/tech-stack.versions.json`은 파생 값입니다.
- Root preflight: `docker compose --profile obs config --quiet`. Root targeted start: `docker compose --profile obs up -d grafana`.
- 안정적인 진입점은 [docs/README.md](../../../docs/README.md)입니다. 정확한 Stage 05 경로: `docs/05.operations/guides/0041-grafana.md`; ID: `GDE-0041`, `POL-0041`, `RUN-0041`.
- 해당 런북의 계획된 격리 복구 절차를 따릅니다. 날짜가 명시된 근거가 없는 한 아직 실행되지 않은 것으로 간주하며 이 README에서 운영 중인 상태를 변경하지 않습니다.

## Related Documents

- [infra/README.md](../../README.md)
- Operations index (`docs/05.operations/README.md`)
- Grafana guide (`docs/05.operations/guides/0041-grafana.md`)
- Grafana policy (`docs/05.operations/policies/0041-grafana.md`)
- Grafana runbook (`docs/05.operations/runbooks/0041-grafana.md`)
- [Documentation index](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 검증을 제공합니다.
