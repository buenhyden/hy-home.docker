# Alertmanager Recovery Runbook (06-observability)

: Alertmanager Notification Service

---

## Overview (KR)

이 런북은 Alertmanager(06-observability) 알림 서비스의 장애 발생 시 복구 절차를 정의한다. 통지 실패, 설정 오류, 그리고 수신자 연결 문제를 신속하게 해결하는 방법을 제공한다.

## Purpose

알림 서비스의 가용성을 복구하여 장애 상황이 운영자에게 지체 없이 전달되도록 보장한다.

## Canonical References

- [Alertmanager Infrastructure README](../../../infra/06-observability/alertmanager/README.md)
- [Alertmanager Operational Policy](../../08.operations/06-observability/alertmanager.md)
- [Alertmanager System Guide](../../07.guides/06-observability/alertmanager.md)

## When to Use

- Prometheus/Loki에서 알림이 발생했으나 실제 통지(Slack/Email)가 오지 않을 때.
- Alertmanager UI에 접속이 불가능하거나 서비스가 응답하지 않을 때.
- 잘못된 Silence 설정으로 인해 중요 알림이 차단되었을 때.

## Procedure or Checklist

### Checklist

- [ ] Alertmanager 컨테이너 상태 확인 (`docker ps`)
- [ ] Slack Webhook URL 유효성 확인
- [ ] Alertmanager 로그 내 `level=error` 메시지 확인
- [ ] 활성화된 Silence 목록 확인

### Procedure

#### 1. Service Restoration

Alertmanager 서비스가 중단된 경우 컨테이너를 재시작한다.

```bash
cd infra/06-observability/alertmanager
docker compose restart
```

#### 2. Configuration Validation

설정 오류(YAML 문법 등)가 의심되는 경우 로그를 확인하고 수정한 후 다시 로드한다.

```bash
docker logs alertmanager | grep "err"
```

#### 3. Notification Test

Mock 알림을 수동으로 발송하여 통지 경로를 테스트한다. (Prometheus API 사용 또는 `amtool` 사용)

## Verification Steps

- [ ] Alertmanager UI (`http://localhost:9093`) 접속 확인.
- [ ] Slack `#notification` 채널에 테스트 메시지 수신 확인.

## Observability and Evidence Sources

- **Signals**: `alertmanager_notifications_failed_total` 지표 상승 여부.
- **Evidence to Capture**: `alertmanager.log` 파일의 에러 스택 트레이스.

## Safe Rollback or Recovery Procedure

- [ ] 설정을 변경한 후 서비스가 기동되지 않으면 이전 정상 버전의 `config.yml`로 복구한다.

## Related Operational Documents

- **Incident examples**: `[../../10.incidents/YYYY/YYYY-MM-DD-alertmanager-outage.md]`
