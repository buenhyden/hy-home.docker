---
title: "Pushgateway"
version: "1.0.5"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2026-01-12"
---

# Pushgateway

## Overview

Pushgateway는 표준 pull 모델을 사용할 수 없는 경우(예: 수명이 짧은 CI/CD 작업이나 배치 스크립트) 임시/배치 작업이 Prometheus에 메트릭을 노출할 수 있게 합니다. 일치하는 스크레이프 잡이 설정되어 있을 때 Prometheus가 스크레이프할 수 있는 임시 버퍼 역할을 합니다.

## Audience

이 README의 주요 독자:

- DevOps Engineers
- Backend Developers (Batch/CI)
- AI Agents

## Scope

### In Scope

- Pushgateway 서비스 설정 및 배포.
- 임시 작업을 위한 메트릭 수집 및 노출.
- Prometheus 스크레이프 계약과 검증.

### Out of Scope

- 범용 메트릭 프록시 또는 장기 저장소.
- 카디널리티가 높은 시계열 저장소(가능하면 직접 계측을 사용).

## Structure

```text
pushgateway/
└── README.md           # This file
```

## Tech Stack

런타임 이미지 고정 값은 [Compose](../docker-compose.yml)에 선언되어 있습니다. [버전 레지스트리](../../tech-stack.versions.json)는 정제된 프로젝션입니다.

| Category | Technology | Runtime source | Role |
| :--- | :--- | :--- | :--- |
| Buffer | [prom/pushgateway](https://hub.docker.com/r/prom/pushgateway) | Compose에 선언됨 | 메트릭 수집 버퍼 |
| Ingress | [Traefik](../../01-gateway/README.md) | Compose에 선언됨 | SSL 종료 및 라우팅 |
| Scraper | [Prometheus](../prometheus/README.md) | Compose에 선언됨 | 예상되는 scrape-to-pull 브리지. 푸시된 메트릭에 의존하기 전에 스크레이프 잡을 확인해야 합니다 |

## Usage Instructions

### Starting the Service

저장소 루트에서 승인된 대상만 시작하거나 재시작합니다. 재시작하면 현재 메트릭을 잃으므로 재전송 담당자와 유효한 관측 범위를 먼저 확인합니다.

```bash
docker compose --profile obs up -d pushgateway
docker compose --profile obs restart pushgateway
```

### Pushing Metrics

작업은 간단한 HTTP POST/PUT 요청으로 메트릭을 푸시할 수 있습니다.

```bash
echo "some_metric 42" | curl --data-binary @- http://pushgateway:9091/metrics/job/some_job
```

## Configuration

- **Ingestion**: 표준 Prometheus Pushgateway API (포트 9091).
- **Exposure**: 보호된 Traefik 라우트를 통해 `https://pushgateway.${DEFAULT_URL}`로 접근 가능합니다.
- **Network**: `obs_net`에 통합되어 있습니다.
- **Persistence**: 현재 Compose 서비스에는 Pushgateway 영속화 옵션이 선언되어 있지 않습니다.

## Operational Status

> [!CAUTION]
> Pushgateway는 범용 프록시가 **아닙니다**. 프로세스가 유지되는 동안 메트릭에는 자동 TTL이 없어 삭제하거나 덮어쓸 때까지 남습니다. 현재 영속화 설정이 없으므로 재시작 시 잃으며, 복구는 여전히 유효한 관측을 다시 push하는 방식입니다. 관리되지 않는 메트릭 증가는 메모리 고갈과 성능 저하로 이어질 수 있습니다.

## Validation

- Compose 또는 설정 참조를 변경한 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.
- `docker logs --tail=200 pushgateway`를 확인하고 푸시된 메트릭이 Pushgateway UI에 나타나는지 확인하여 메트릭 푸시를 검증합니다.
- Prometheus 대시보드나 알림에 의존하기 전에 `infra/06-observability/prometheus/config/prometheus.yml`에 Pushgateway 스크레이프 잡이 존재하고 Prometheus Targets 페이지에서 대상이 UP 상태인지 확인합니다.

## Troubleshooting

- 네트워크, 볼륨, 시크릿, 레이블 참조가 올바르게 렌더링되는지 `docker compose --profile obs config --quiet`로 먼저 확인합니다.
- 설정이나 시크릿 참조를 변경하기 전에 컨테이너 로그와 연결된 런북을 확인합니다.
- 푸시 오류: 푸시 URL 형식(`http://pushgateway:9091/metrics/job/<job>`)을 검증하고 푸시하는 서비스에서 네트워크 연결이 되는지 확인합니다.
- 오래된 메트릭: Pushgateway UI나 런북의 DELETE 명령으로 오래된 작업 그룹을 제거합니다.
- 영속화 요구 사항: `--persistence.file`은 런타임 설정 변경으로 취급하고 활성화하기 전에 정책, 런북, Compose 근거를 업데이트합니다.
- 스크레이프 오류: `prometheus.yml`에 Pushgateway 스크레이프 잡이 정의되어 있는지 확인합니다. 없다면 Pushgateway가 다운된 것으로 취급하지 말고 구현 공백으로 기록합니다.

### Convergence contract

- Classification: **OPTIONAL**. Exact profiles: `obs`, `batch-metrics`.
- Source authority: `infra/06-observability/docker-compose.yml`과 이 패키지의 추적 설정/빌드 입력. 이미지 선언이 권위이며 `infra/tech-stack.versions.json`은 파생 값입니다.
- Root preflight: `docker compose --profile obs config --quiet`. Root targeted start: `docker compose --profile obs up -d pushgateway`.
- 안정적인 진입점은 [docs/README.md](../../../docs/README.md)입니다. 정확한 Stage 05 경로: `docs/05.operations/guides/0046-pushgateway.md`; ID: `GDE-0046`, `POL-0046`, `RUN-0046`.
- 해당 런북의 계획된 격리 복구 절차를 따릅니다. 날짜가 명시된 근거가 없는 한 아직 실행되지 않은 것으로 간주하며 이 README에서 운영 중인 상태를 변경하지 않습니다.

## Related Documents

- Usage guide (`docs/05.operations/guides/0046-pushgateway.md`)
- Operations policy (`docs/05.operations/policies/0046-pushgateway.md`)
- Recovery runbook (`docs/05.operations/runbooks/0046-pushgateway.md`)
- [Documentation index](../../../docs/README.md)

## How to Work in This Area

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../../.agents/governance/agentic.md)와 [documentation protocol](../../../.agents/governance/documentation-protocol.md)을 따른다.

1. **PromQL Optimization**: Pushgateway에서 메트릭을 쿼리할 때는 서로 다른 배치 실행을 구분할 수 있도록 항상 `job` 레이블을 포함합니다.
2. **Maintenance**: 갱신되지 않은 오래된 메트릭이 있는지 주기적으로 확인합니다.
3. **Traceability**: 정리 로직과 근거 수집은 전용 가이드와 런북을 참고합니다.
