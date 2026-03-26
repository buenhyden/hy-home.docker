# Observability Runbooks

> Incident Response & Recovery Procedures for the LGTM Stack.

## Overview (KR)

이 디렉터리는 `hy-home.docker`의 가시성 체계(06-observability) 장애 발생 시 복구 절차를 포함한다. 데이터 소실 방지와 고가용성 유지를 위한 핵심 대응 매뉴얼이다.

## Recovery Procedures

- [01. LGTM Stack Recovery](./01.lgtm-recovery.md) - Standard recovery steps for Loki, Grafana, Tempo.
- [02. Alloy- [Grafana Alloy](./alloy.md)
- [Loki Recovery Runbo- [Loki](./loki.md)
- [Prometheus](./prometheus.md)
- [Pushgateway](./pushgateway.md)
- [Pyroscope](./pyroscope.md)
- [Tempo](./tempo.md)
- [Prometheus Alertmanager](./alertmanager.md)

## Incident Response Flow

1. **Detection**: Prometheus Alertmanager 또는 Grafana On-call 알람 수신.
2. **Triaging**: 영향도 파악 (데이터 수집 중단 vs 시각화 중단).
3. **Mitigation**: Runbook 절차에 따른 서비스 재시작 또는 로그 분석.
4. **Resolution**: 정상 상태 확인 및 Post-mortem 작성.

## Emergency Contacts

- **Infrastructure Lead**: `@infra-oncall`
- **SRE Team**: `#ops-observability` (Slack)

## Related Documents

- **Guides**: `[../../07.guides/06-observability/README.md]`
- **Operations**: `[../../08.operations/06-observability/README.md]`
