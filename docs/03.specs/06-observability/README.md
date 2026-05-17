# 06-observability Specifications

> 모니터링, 로깅, 추적 서비스 기술 사양

## Overview

`docs/03.specs/06-observability`는 Prometheus, Grafana, Loki, Tempo, Alloy 등 관측성 스택의 기술 사양을 포함합니다.

## Audience

이 README의 주요 독자:

- Developers
- System Architects
- QA Engineers
- AI Agents

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

## How to Work in This Area

1. 구현 또는 검증 전 [spec.md](./spec.md)를 먼저 확인합니다.
2. 상위 요구사항과 아키텍처 맥락은 Related Documents의 PRD/ARD/ADR 링크에서 추적합니다.
3. 새 child contract가 필요하면 `docs/99.templates`의 대응 템플릿을 사용하고 이 폴더 README를 함께 갱신합니다.
4. 운영 절차, 정책, runbook 내용은 `docs/05.operations/`에 두고 여기에는 구현 계약만 유지합니다.

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [infra/06-observability/README.md](../../../infra/06-observability/README.md)
- [docs/05.operations/guides/06-observability/](../../05.operations/guides/06-observability/)
