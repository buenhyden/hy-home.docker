# 06-observability Specifications

> 모니터링, 로깅, 추적 서비스 기술 사양

## Overview

`docs/03.specs/06-observability`는 Prometheus, Grafana, Loki, Tempo, Alloy 등 관측성 스택의 기술 사양을 포함합니다.

## Scope

### In Scope

- 메트릭, 로그, 트레이스 수집 및 저장 사양
- 대시보드 경계, 알림 규칙, 데이터 보존 정책 사양

### Out of Scope

- 운영 절차 (`docs/05.operations/guides/06-observability/` 담당)

## Structure

```text
06-observability/
├── spec.md      # Observability stack technical specification
└── README.md    # This file
```

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [infra/06-observability/README.md](../../../infra/06-observability/README.md)
- [docs/05.operations/guides/06-observability/](../../05.operations/guides/06-observability/)
