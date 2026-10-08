---
title: "Pyroscope Continuous Profiling"
version: "1.0.5"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-03-19"
---

# Pyroscope Continuous Profiling

## Overview

Pyroscope는 애플리케이션을 연속적으로 프로파일링하여 성능 병목, CPU 핫 패스, 메모리 누수를 식별합니다. 프로파일링 데이터(CPU, 메모리 등)를 수집합니다. 개발자는 플레임그래프로 시간 경과에 따른 변화를 시각화할 수 있습니다.

## Audience

이 README의 주요 독자:

- Backend Developers (성능 최적화)
- SRE / DevOps Engineers (리소스 관리)
- AI Agents

## Scope

### In Scope

- Pyroscope 서비스 설정 및 배포.
- 연속 프로파일링 데이터 수집 및 저장.
- 시각화를 위한 Grafana 연동.

### Out of Scope

- 애플리케이션 수준 프로파일링 에이전트 ([Grafana Alloy](../alloy/README.md)에서 처리).
- 프로파일링 데이터의 장기 보관 (Retention Policy(`docs/05.operations/policies/0047-pyroscope.md`)에서 관리).

## Structure

```text
pyroscope/
├── README.md  # This file
└── config/    # Main configuration file
```

## Tech Stack

런타임 이미지 고정 값은 [Compose](../docker-compose.yml)에 선언되어 있습니다. [버전 레지스트리](../../tech-stack.versions.json)는 정제된 프로젝션입니다.

| Category | Technology | Runtime source | Role |
| :--- | :--- | :--- | :--- |
| Profiling | [Grafana Pyroscope](https://github.com/grafana/pyroscope) | Compose에 선언됨 | 연속 프로파일링 엔진 |
| Collector | [Grafana Alloy](../alloy/README.md) | Compose에 선언됨 | 프로파일 스크레이핑 및 재매핑 |
| Visualization | [Grafana](../grafana/README.md) | Compose에 선언됨 | 통합 대시보드 |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose --profile obs up -d pyroscope` | 저장소 루트에서 Pyroscope 서비스 시작 |
| `docker compose --profile obs restart pyroscope` | 저장소 루트에서 설정 변경 사항 적용 |

## Configuration

- **Ingestion**: HTTP를 통한 Protobuf로 프로파일링 데이터를 수신합니다 (포트 4040).
- **Storage**: 로컬 파일시스템 백엔드(`/var/lib/pyroscope`).
- **Retention**: `pyroscope.yaml`에 고정 보존 기간이 선언되어 있지 않습니다. 용량 및 보존 변경은 정책 검토가 필요합니다.

## Operational Status

> [!IMPORTANT]
> Pyroscope는 현재 `/var/lib/pyroscope`에 마운트된 로컬 파일시스템 백엔드를 사용합니다. `pyroscope.yaml`에는 고정 보존 기간이 선언되어 있지 않습니다. 용량 및 보존 변경에는 승인된 설정 업데이트가 필요합니다.

## Validation

- Compose 또는 설정 참조를 변경한 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.
- 설정 변경 후 `docker logs --tail=200 pyroscope`로 프로파일링 수집을 확인합니다.
- Alloy가 프로파일링 데이터를 전송한 후 Grafana Pyroscope 데이터소스에 프로파일이 나타나는지 확인합니다.
- `docker compose exec -T pyroscope /usr/bin/profilecli ready --url=http://127.0.0.1:4040`로 Pyroscope 준비 상태를 확인합니다.

## Troubleshooting

- 네트워크, 볼륨, 시크릿, 레이블 참조가 올바르게 렌더링되는지 `docker compose --profile obs config --quiet`로 먼저 확인합니다.
- 설정이나 시크릿 참조를 변경하기 전에 컨테이너 로그와 연결된 런북을 확인합니다.
- 수집 오류: Alloy의 Pyroscope exporter 엔드포인트가 Pyroscope 컨테이너의 push API와 일치하는지 확인합니다.
- 프로파일 누락: Alloy의 프로파일링 설정에 있는 서비스명 레이블이 예상되는 Pyroscope 앱 이름과 일치하는지 확인합니다.
- 저장소 문제: Pyroscope 데이터 볼륨이 마운트되어 있고 디스크 여유 공간이 충분한지 확인합니다.
- 보존, 저장소 백엔드, 수집 한도, 프로파일 데이터 삭제: 데이터 손실 위험이 있는 작업을 하기 전에 중지하고 연결된 런북의 에스컬레이션 경로를 사용합니다.

### Convergence contract

- Classification: **HOME**. Exact profiles: `obs`, `profiling`.
- Source authority: `infra/06-observability/docker-compose.yml`과 이 패키지의 추적 설정/빌드 입력. 이미지 선언이 권위이며 `infra/tech-stack.versions.json`은 파생 값입니다.
- Root preflight: `docker compose --profile obs config --quiet`. Root targeted start: `docker compose --profile obs up -d pyroscope`.
- 안정적인 진입점은 [docs/README.md](../../../docs/README.md)입니다. 정확한 Stage 05 경로: `docs/05.operations/guides/0047-pyroscope.md`; ID: `GDE-0047`, `POL-0047`, `RUN-0047`.
- 해당 런북의 계획된 격리 복구 절차를 따릅니다. 날짜가 명시된 근거가 없는 한 아직 실행되지 않은 것으로 간주합니다. 이 README에서는 운영 중인 상태를 변경하지 않습니다.

## Related Documents

- Usage guide (`docs/05.operations/guides/0047-pyroscope.md`)
- Operations policy (`docs/05.operations/policies/0047-pyroscope.md`)
- Recovery runbook (`docs/05.operations/runbooks/0047-pyroscope.md`)
- [Documentation index](../../../docs/README.md)

## Usage

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../../.agents/governance/agentic.md)와 [documentation protocol](../../../.agents/governance/documentation-protocol.md)을 따른다.

1. **Flamegraph Analysis**: Grafana의 `traceqlEditor` 기능 토글로 프로파일을 트레이스와 연관 짓습니다.
2. **Resource Monitoring**: 프로파일링 수집은 CPU 사용량이 클 수 있으므로, 피크 부하 동안 `pyroscope` 컨테이너 통계를 모니터링합니다.
3. **Traceability**: 재매핑 로직과 커스텀 레이블은 전용 시스템 가이드를 참고합니다.
