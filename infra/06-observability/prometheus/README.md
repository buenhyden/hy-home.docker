---
title: "Prometheus"
version: "1.0.4"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-01-12"
---

# Prometheus

## Overview

`infra/06-observability/prometheus`는 `hy-home.docker` 플랫폼의 핵심 메트릭 엔진인 Prometheus의 구현 위치입니다. `config/prometheus.yml`에 정의된 대상을 스크레이프하고 시계열 데이터를 `prometheus-data` 볼륨에 저장하며 알림 규칙을 평가합니다. 레이블 카디널리티는 운영 정책을 통해 통제되어야 합니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

- **Role**: 메트릭 수집 및 알림 엔진.
- **Layer**: `06-observability` (텔레메트리 저장소).
- **Interface**: Traefik을 경유하는 `https://prometheus.${DEFAULT_URL}`.

## Structure

```text
infra/06-observability/prometheus/
├── config/  # 하위 구성 영역
└── README.md  # This file
```

## Tech Stack

런타임 이미지 고정 값은 [Compose](../docker-compose.yml)에 선언되어 있습니다. [버전 레지스트리](../../tech-stack.versions.json)는 정제된 프로젝션입니다.

| Component | Technology | Runtime source |
| :--- | :--- | :--- |
| Metrics DB | Prometheus | Compose에 선언됨 |
| Configuration | YAML 기반 | 정적 구성 및 파일 기반 서비스 디스커버리 |
| Tooling | promtool | 설정/규칙 검증 |

## System Components

- **Scrape Configs**: `config/prometheus.yml`에 정의됨(정확한 잡 수는 해당 파일을 기준으로 확인).
- **Alerting Rules**: `config/alert_rules/`에 도메인별로 모듈화됨.
- **Storage**: 영속 TSDB 볼륨. 명시적 보존 플래그는 Compose에 선언되어 있지 않습니다.

## Management Guide

### 1. Operations & Configuration

- **Scrape Targets**: `prometheus.yml`의 `scrape_configs`를 업데이트합니다.
- **Alerting Rules**: `config/alert_rules/`의 YAML 파일을 추가/수정합니다.
- **Validation**:

  ```bash
  docker exec prometheus promtool check config /etc/prometheus/prometheus.yml
  ```

### 2. Traceability

- **System Guide**: `docs/05.operations/guides/0045-prometheus.md`
- **Operations Policy**: `docs/05.operations/policies/0045-prometheus.md`
- **Runbook**: `docs/05.operations/runbooks/0045-prometheus.md`

## Usage

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../../.agents/governance/agentic.md)와 [documentation protocol](../../../.agents/governance/documentation-protocol.md)을 따른다.

1. **PromQL Optimization**: 비용이 큰 대시보드 쿼리에는 Recording Rules를 사용합니다.
2. **Rule Management**: 변경 사항을 적용하기 전에 항상 `promtool`로 검증합니다.
3. **Scrape Settings**: 전역 간격은 `30s`이며 Prometheus의 `15s`나 cAdvisor의 `1m`처럼 서비스별 재정의는 의도적으로 유지해야 합니다.
4. **Networking**: 스크레이프 대상은 `obs_net`에서 접근 가능해야 합니다.

## Validation

- Compose 또는 설정 참조를 변경한 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.
- `docker exec prometheus promtool check config /etc/prometheus/prometheus.yml`로 Prometheus 설정을 검증합니다.
- `docker exec prometheus /bin/sh -c 'promtool check rules /etc/prometheus/alert_rules/*.yml'`로 알림 규칙을 검증합니다. 컨테이너 셸이 컨테이너 전용 경로를 확장한 뒤 `promtool`이 존재하는 파일을 받습니다.
- `prometheus.yml` 변경 후 Prometheus UI의 Targets 페이지에서 스크레이프 대상이 UP 상태인지 확인합니다.
- 설정이나 규칙 변경 후 `docker logs --tail=200 prometheus`로 알림 규칙이 정상적으로 로드되었는지 확인합니다.

## Troubleshooting

- 네트워크, 볼륨, 시크릿, 레이블 참조가 올바르게 렌더링되는지 `docker compose --profile obs config --quiet`로 먼저 확인합니다.
- 설정이나 시크릿 참조를 변경하기 전에 컨테이너 로그와 연결된 런북을 확인합니다.
- 스크레이프 오류: `prometheus.yml`의 스크레이프 설정을 검증하고 대상 엔드포인트가 Prometheus 컨테이너에서 접근 가능한지 확인합니다.
- 알림 규칙 오류: 규칙 파일의 YAML 문법을 확인하고 `rule_files` 경로가 올바르게 마운트되어 있는지 확인합니다.
- 저장소 문제: Prometheus 데이터 볼륨이 마운트되어 있고 디스크 여유 공간이 충분한지 확인합니다.

### Convergence contract

- Classification: **HOME**. Exact profiles: `obs`, `obs-core`, `dev`, `alerting`, `batch-metrics`.
- Source authority: `infra/06-observability/docker-compose.yml`과 이 패키지의 추적 설정/빌드 입력. 이미지 선언이 권위이며 `infra/tech-stack.versions.json`은 파생 값입니다.
- Root preflight: `docker compose --profile obs config --quiet`. Root targeted start: `docker compose --profile obs up -d prometheus`.
- 안정적인 진입점은 [docs/README.md](../../../docs/README.md)입니다. 정확한 Stage 05 경로: `docs/05.operations/guides/0045-prometheus.md`; ID: `GDE-0045`, `POL-0045`, `RUN-0045`.
- 해당 런북의 계획된 격리 복구 절차를 따릅니다. 날짜가 명시된 근거가 없는 한 아직 실행되지 않은 것으로 간주하며 이 README에서 운영 중인 상태를 변경하지 않습니다.

## Related Documents

- [infra/README.md](../../README.md)
- `docs/05.operations/README.md`
- Prometheus usage guide (`docs/05.operations/guides/0045-prometheus.md`)
- Prometheus operations policy (`docs/05.operations/policies/0045-prometheus.md`)
- Prometheus recovery runbook (`docs/05.operations/runbooks/0045-prometheus.md`)
- [Documentation index](../../../docs/README.md)
