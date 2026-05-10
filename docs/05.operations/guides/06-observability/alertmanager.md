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

- **ARD**: [Observability Architecture](../../../02.architecture/requirements/0006-observability-architecture.md)
- **Procedure**: [Alertmanager Recovery Procedure](./alertmanager.md)
- **Usage**: [Alertmanager System Usage](./alertmanager.md)

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/05.operations/06-observability/alertmanager.md` during the 2026-05-10 operations taxonomy consolidation.

### Alertmanager Notification Routing Usage (06-observability)

> Centralized alert routing, deduplication, and notification gateway.

---

#### Overview (KR)

이 문서는 Alertmanager(06-observability)의 알림 라우팅 체계와 설정 방법을 설명한다. 다양한 소스(Prometheus, Loki 등)에서 유입된 경보(Alert)를 그룹화하고 중복을 제거하여 적절한 대상(Slack, Email 등)으로 전달하는 과정을 다룬다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- Developer (SRE, Backend)
- Operator
- Agent-tuner

#### Purpose

이 가이드는 Alertmanager의 라우팅 규칙을 이해하고, 알림 수신자(Receiver)를 설정하며, 알림 피로도를 줄이기 위한 그룹화 설정을 돕는다.

#### Prerequisites

- [Alertmanager Infrastructure README](../../../../infra/06-observability/alertmanager/README.md)
- Prometheus 또는 Loki 등 알림 소스 구동 중
- Slack Webhook URL 또는 SMTP 서버 정보

#### Step-by-step Instructions

##### 1. Understanding Routing Tree

Alertmanager는 트리 구조의 라우팅 규칙을 사용한다. `route` 섹션에서 최상위 규칙을 정의하며, 하위 `routes`를 통해 조건별로 알림을 분기할 수 있다.

```yaml
route:
  group_by: ['alertname', 'job']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 1h
  receiver: 'team-notifications'
```

##### 2. Configuring Receivers

알림을 실제로 전달받을 대상(Slack, Email 등)을 `receivers` 섹션에 정의한다.

- **Slack Integration**: `slack_configs`를 사용하여 채널과 메시지 형식을 지정한다.
- **Email Integration**: `email_configs`를 사용하여 메일 서버와 수신자를 지정한다.

##### 3. Applying Silences

계획된 유지보수 기간 동안 발생하는 불필요한 알림을 차단하기 위해 Silence를 설정할 수 있다.

- **Alertmanager UI**: `http://localhost:9093/#/silences`에 접속하여 `New Silence`를 클릭한다.
- **API/CLI**: `amtool` 등을 사용하여 프로그래밍 방식으로 Silence를 관리할 수 있다.

#### Common Pitfalls

- **Notification Storms**: `group_wait`와 `group_interval`이 너무 짧으면 수많은 알림이 쏟아질 수 있다.
- **Resolution Delays**: `repeat_interval`이 너무 길면 해결된 문제가 다시 발생했을 때 알림이 늦게 올 수 있다.
- **Invalid Templates**: Slack 메시지 템플릿 문법 오류 시 알림 발송 자체가 실패할 수 있으므로 주의해야 한다.

#### Related Documents

- **Operation**: [Alertmanager Operational Policy](./alertmanager.md)
- **Procedure**: [Alertmanager Recovery Procedure](./alertmanager.md)

## Procedure

> Migrated from `docs/05.operations/06-observability/alertmanager.md` during the 2026-05-10 operations taxonomy consolidation.

### Alertmanager Recovery Procedure (06-observability)

: Alertmanager Notification Service

---

#### Overview (KR)

이 런북은 Alertmanager(06-observability) 알림 서비스의 장애 발생 시 복구 절차를 정의한다. 통지 실패, 설정 오류, 그리고 수신자 연결 문제를 신속하게 해결하는 방법을 제공한다.

#### Purpose

알림 서비스의 가용성을 복구하여 장애 상황이 운영자에게 지체 없이 전달되도록 보장한다.

#### Canonical References

- [Alertmanager Infrastructure README](../../../../infra/06-observability/alertmanager/README.md)
- [Alertmanager Operational Policy](./alertmanager.md)
- [Alertmanager System Usage](./alertmanager.md)

#### When to Use

- Prometheus/Loki에서 알림이 발생했으나 실제 통지(Slack/Email)가 오지 않을 때.
- Alertmanager UI에 접속이 불가능하거나 서비스가 응답하지 않을 때.
- 잘못된 Silence 설정으로 인해 중요 알림이 차단되었을 때.

#### Procedure or Checklist

##### Checklist

- [ ] Alertmanager 컨테이너 상태 확인 (`docker ps`)
- [ ] Slack Webhook URL 유효성 확인
- [ ] Alertmanager 로그 내 `level=error` 메시지 확인
- [ ] 활성화된 Silence 목록 확인

##### Procedure

###### 1. Service Restoration

Alertmanager 서비스가 중단된 경우 컨테이너를 재시작한다.

```bash
cd infra/06-observability/alertmanager
docker compose restart
```

###### 2. Configuration Validation

설정 오류(YAML 문법 등)가 의심되는 경우 로그를 확인하고 수정한 후 다시 로드한다.

```bash
docker logs alertmanager | grep "err"
```

###### 3. Notification Test

Mock 알림을 수동으로 발송하여 통지 경로를 테스트한다. (Prometheus API 사용 또는 `amtool` 사용)

#### Verification Steps

- [ ] Alertmanager UI (`http://localhost:9093`) 접속 확인.
- [ ] Slack `#notification` 채널에 테스트 메시지 수신 확인.

#### Observability and Evidence Sources

- **Signals**: `alertmanager_notifications_failed_total` 지표 상승 여부.
- **Evidence to Capture**: `alertmanager.log` 파일의 에러 스택 트레이스.

#### Safe Rollback or Recovery Procedure

- [ ] 설정을 변경한 후 서비스가 기동되지 않으면 이전 정상 버전의 `config.yml`로 복구한다.

#### Related Operational Documents

- **Incident examples**: `[../../05.operations/incidents/YYYY/YYYY-MM-DD-alertmanager-outage.md]`

---

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
