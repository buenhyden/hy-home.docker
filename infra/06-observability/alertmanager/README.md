---
title: "Alertmanager Notification Routing"
version: "1.0.4"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-01-12"
---

# Alertmanager Notification Routing

## Overview

Alertmanager는 Prometheus가 보낸 알림을 처리하여 중복을 제거하고, 그룹화하고, 억제하고, 무음 처리한 뒤 설정된 수신자(receiver) 통합으로 라우팅합니다. 이 스택에서는 `alertmanager`로 실행되며 [선언된 런타임 이미지](../../tech-stack.versions.json)를 사용합니다. 런타임 상태는 `alertmanager-data`에 저장하고 시작 시 Docker Secret 값을 임시 파일인 `/tmp/config.yml`로 렌더링합니다.

## Audience

이 README의 주요 독자:

- SREs (알림 라우팅 및 통합)
- On-call Engineers (무음 처리 및 트러블슈팅)
- DevOps Engineers (설정 관리)
- AI Agents (자동화된 무음 처리 관리)

## Scope

### In Scope

- Alertmanager 소스 설정(`config/config.yml`)과 시작 시 `/tmp/config.yml`로의 렌더링.
- 알림 라우팅 규칙과 수신자 통합.
- 무음(silencing) 및 억제(inhibition) 규칙.
- 로컬 배포, 보호된 라우트, 준비 상태, 연결 설정.

### Out of Scope

- 알림 규칙 정의 (Prometheus/Loki에서 관리).
- 전역 텔레메트리 수집 (Grafana Alloy에서 관리).
- 메트릭의 영속 저장소 (Prometheus TSDB에서 관리).

## Structure

```text
alertmanager/
├── config/    # Git-managed routing config with secret placeholders
└── README.md  # This file
```

## Usage

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../../.agents/governance/agentic.md)와 [documentation protocol](../../../.agents/governance/documentation-protocol.md)을 따른다.

1. **Understand Routing**: `config/config.yml`을 검토하여 알림이 어떻게 그룹화, 억제, 무음 처리, 전달되는지 파악합니다.
2. **Configuration Updates**: `config/config.yml`을 수정합니다. Compose는 이를 `/etc/alertmanager/config.yml.template`로 마운트하고 시작 시 시크릿을 `/tmp/config.yml`로 렌더링합니다.
3. **Secret Integration**: 배포 전에 SMTP 및 Slack webhook용 Docker Secret이 마운트되어 있는지 확인합니다. 렌더링된 시크릿 값은 기록하지 않습니다.
4. **Silence Management**: 점검 기간에는 Alertmanager UI/API로 임시 알림 무음을 설정하고 항상 만료 시간을 지정합니다.
5. **Runtime Checks**: 라우트, 수신자, 억제, 시크릿, 미들웨어 정책을 변경하기 전에 연결된 가이드와 런북을 사용합니다.

6. **Silences**: 알림 피로를 막도록 계획된 인프라 점검 기간에는 사전에 무음을 생성합니다.
7. **Grouping**: 정책과 설정을 함께 변경하지 않는 한 알림 그룹화는 `alertname`, `job`, `domain`, `severity` 기준을 유지합니다.
8. **Secret Rotation**: `slack_webhook`, `smtp_username`, `smtp_password`의 값 교체와 Compose 참조 변경을 구분합니다. 기존 mount가 가리키는 값의 재렌더링과 승인된 재생성은 RUN-0039를 따르며, restart만으로 새 Compose·secret 참조가 적용된다고 가정하지 않습니다.
9. **Evidence Hygiene**: 시크릿 ID와 명령 결과만 기록하고 렌더링된 webhook, SMTP 사용자명, SMTP 비밀번호 값은 절대 붙여넣지 않습니다.

## Tech Stack

| Category     | Technology   | Version | Notes                          |
| :----------- | :----------- | :------ | :----------------------------- |
| Alerting     | Alertmanager | declared version | Docker Secret로 렌더링되는 설정을 사용하는 단일 compose 서비스 |
| Integrations | Slack / SMTP | -       | Webhook 및 SMTP 릴레이         |

## Available Scripts

| Command                  | Description                 |
| :----------------------- | :-------------------------- |
| `docker compose --profile obs up -d alertmanager` | 저장소 루트에서 Alertmanager 시작 |
| `docker compose --profile obs restart alertmanager` | 저장소 루트에서 설정 변경 사항 적용 |
| `docker compose --profile obs logs -f alertmanager` | 저장소 루트에서 Alertmanager 로그 확인 |

## Configuration

### Docker Secrets

| Secret | Required | Description |
| :----- | :------- | :---------- |
| `slack_webhook` | Yes | `__SLACK_WEBHOOK_URL__`로 렌더링되는 Slack incoming webhook 엔드포인트 |
| `smtp_username` | Yes | `__SMTP_USERNAME__`로 렌더링되는 SMTP 인증 사용자명 |
| `smtp_password` | Yes | `__SMTP_PASSWORD__`로 렌더링되는 SMTP 인증 비밀번호 |

## Validation

- Compose 또는 설정 참조를 변경한 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.
- `docker compose --profile obs ps alertmanager`와 `docker exec alertmanager wget -q --spider http://localhost:9093/-/ready`로 서비스 준비 상태를 확인합니다.
- `config.yml` 변경 후 `docker logs --tail=200 alertmanager`로 라우팅 트리 문법을 확인합니다.
- `rg -n 'alertmanagers:|targets: \["alertmanager:9093"\]' infra/06-observability/prometheus/config/prometheus.yml`로 Prometheus 전달 여부를 확인합니다.
- 테스트 알림을 발생시켜 예상한 Slack 채널에 도달하는지 보고 수신자 연결을 검증합니다.

## Troubleshooting

- 네트워크, 볼륨, 시크릿, 레이블 참조가 올바르게 렌더링되는지 `docker compose --profile obs config --quiet`로 먼저 확인합니다.
- 설정이나 시크릿 참조를 변경하기 전에 컨테이너 로그와 연결된 런북을 확인합니다.
- 라우팅 트리 오류: `config.yml` YAML 문법을 검증하고 참조된 모든 수신자가 정의되어 있는지 확인합니다.
- 알림 전달 실패: `slack_webhook`, `smtp_username`, `smtp_password` Docker Secret이 마운트되어 있는지 확인합니다.
- 억제 규칙 문제: `config.yml`의 `inhibit_rules`에서 소스와 대상의 매치 레이블이 올바른지 검토합니다.
- `/tmp/config.yml`이나 시크릿 값은 트러블슈팅 근거로 캡처하지 않습니다.

### Convergence contract

- Classification: **HOME**. Exact profiles: `obs`, `alerting`.
- Source authority: `infra/06-observability/docker-compose.yml`과 이 패키지의 추적 설정/빌드 입력. 이미지 선언이 권위이며 `infra/tech-stack.versions.json`은 파생 값입니다.
- Root preflight: `docker compose --profile obs config --quiet`. Root targeted start: `docker compose --profile obs up -d alertmanager`.
- 안정적인 진입점은 [docs/README.md](../../../docs/README.md)입니다. 정확한 Stage 05 경로: `docs/05.operations/guides/0039-alertmanager.md`; ID: `GDE-0039`, `POL-0039`, `RUN-0039`.
- 해당 런북의 계획된 격리 복구 절차를 따릅니다. 날짜가 명시된 근거가 없는 한 아직 실행되지 않은 것으로 간주하며 이 README에서 운영 중인 상태를 변경하지 않습니다.

## Related Documents

- **Guides**: `docs/05.operations/guides/0039-alertmanager.md`
- **Policy**: `docs/05.operations/policies/0039-alertmanager.md`
- **Runbook**: `docs/05.operations/runbooks/0039-alertmanager.md`
- [Documentation index](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 검증에 쓰입니다.
