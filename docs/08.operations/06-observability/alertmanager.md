# Alertmanager Operational Policy (06-observability)

> Notification Governance, Alert Severity, and Reliability Standards.

---

## Overview (KR)

이 문서는 Alertmanager(06-observability)의 운영 정책을 정의한다. 알림의 중요도(Severity)에 따른 대응 기준, 통지 방식, 그리고 알림 피로도를 관리하기 위한 통제 기준을 포함한다.

## Policy Scope

이 정책은 시스템의 모든 경보(Alert)가 사용자에게 도달하기까지의 라우팅, 필터링, 그리고 통지 과정을 제어한다.

## Applies To

- **Systems**: Alertmanager Cluster, Slack Webhook, SMTP Relay
- **Agents**: SRE-Agent, Monitoring-Agent
- **Environments**: Production (Standard), Staging

## Controls

### 1. Alert Severity Levels

| Level | Severity | Channel | Response Time | Description |
| :--- | :--- | :--- | :--- | :--- |
| **P0** | Critical | Slack + Email | Immediate | System down, data loss, or security breach. |
| **P1** | Warning | Slack | Business Hours | Performance degradation, approaching thresholds. |
| **P2** | Info | Dashboard | Weekly | Minor anomalies, maintenance logs, trend analysis. |

### 2. Notification Standards

- **Required**: 모든 P0 알림은 반드시 2개 이상의 별도 채널(Slack, Email 등)로 동시 발송되어야 한다.
- **Allowed**: P1 알림은 업무 시간(09:00 - 18:00) 내에만 발송되도록 `time_intervals`를 설정할 수 있다.
- **Disallowed**: 알림 피로도 방지를 위해 `repeat_interval`을 30분 미만으로 설정하는 것은 금지한다.

### 3. Silence Policy

- **Standard**: 계획된 작업(Maintenance) 시작 최소 15분 전에 Silence를 활성화해야 한다.
- **Expiry**: 모든 Silence는 반드시 종료 기간(Expiry)을 명시해야 하며, 무기한 Silence는 금지한다.

## Exceptions

- 보안 사고(Security Incident) 발생 시 즉각적이고 무제한적인 알림 발송이 허용되며, 이 경우 평시의 `repeat_interval` 제한을 무시할 수 있다.

## Verification

- **Compliance Check**: 주간 단위로 미처리 알림(Unresolved Alerts)과 Silence 현황을 감사한다.
- **Health Check**: Alertmanager 통합 테스트(Mock Alert 발송)를 월 1회 수행하여 통지 경로의 정합성을 검증한다.

## Review Cadence

- Quarterly (분기별) 알림 통계 분석 및 임계치 최적화 검토.

## AI Agent Policy Section

- **Automated Silencing**: AI 에이전트는 승인된 변경 작업(Change Management) 티켓이 있는 경우에만 자동으로 Silence를 생성할 수 있다.
- **Alert Triage**: 에이전트가 알림을 자동 분석할 때 `severity`와 `impact`를 최우선으로 고려해야 한다.

## Related Documents

- **ARD**: [Observability Architecture](../../02.ard/0006-observability-architecture.md)
- **Runbook**: [Alertmanager Recovery Runbook](../../09.runbooks/06-observability/alertmanager.md)
- **Guide**: [Alertmanager System Guide](../../07.guides/06-observability/alertmanager.md)
