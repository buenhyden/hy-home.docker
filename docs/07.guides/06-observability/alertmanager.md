# Alertmanager Notification Routing Guide (06-observability)

> Centralized alert routing, deduplication, and notification gateway.

---

## Overview (KR)

이 문서는 Alertmanager(06-observability)의 알림 라우팅 체계와 설정 방법을 설명한다. 다양한 소스(Prometheus, Loki 등)에서 유입된 경보(Alert)를 그룹화하고 중복을 제거하여 적절한 대상(Slack, Email 등)으로 전달하는 과정을 다룬다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Developer (SRE, Backend)
- Operator
- Agent-tuner

## Purpose

이 가이드는 Alertmanager의 라우팅 규칙을 이해하고, 알림 수신자(Receiver)를 설정하며, 알림 피로도를 줄이기 위한 그룹화 설정을 돕는다.

## Prerequisites

- [Alertmanager Infrastructure README](../../../infra/06-observability/alertmanager/README.md)
- Prometheus 또는 Loki 등 알림 소스 구동 중
- Slack Webhook URL 또는 SMTP 서버 정보

## Step-by-step Instructions

### 1. Understanding Routing Tree

Alertmanager는 트리 구조의 라우팅 규칙을 사용한다. `route` 섹션에서 최상위 규칙을 정의하며, 하위 `routes`를 통해 조건별로 알림을 분기할 수 있다.

```yaml
route:
  group_by: ['alertname', 'job']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 1h
  receiver: 'team-notifications'
```

### 2. Configuring Receivers

알림을 실제로 전달받을 대상(Slack, Email 등)을 `receivers` 섹션에 정의한다.

- **Slack Integration**: `slack_configs`를 사용하여 채널과 메시지 형식을 지정한다.
- **Email Integration**: `email_configs`를 사용하여 메일 서버와 수신자를 지정한다.

### 3. Applying Silences

계획된 유지보수 기간 동안 발생하는 불필요한 알림을 차단하기 위해 Silence를 설정할 수 있다.

- **Alertmanager UI**: `http://localhost:9093/#/silences`에 접속하여 `New Silence`를 클릭한다.
- **API/CLI**: `amtool` 등을 사용하여 프로그래밍 방식으로 Silence를 관리할 수 있다.

## Common Pitfalls

- **Notification Storms**: `group_wait`와 `group_interval`이 너무 짧으면 수많은 알림이 쏟아질 수 있다.
- **Resolution Delays**: `repeat_interval`이 너무 길면 해결된 문제가 다시 발생했을 때 알림이 늦게 올 수 있다.
- **Invalid Templates**: Slack 메시지 템플릿 문법 오류 시 알림 발송 자체가 실패할 수 있으므로 주의해야 한다.

## Related Documents

- **Operation**: [Alertmanager Operational Policy](../../08.operations/06-observability/alertmanager.md)
- **Runbook**: [Alertmanager Recovery Runbook](../../09.runbooks/06-observability/alertmanager.md)
