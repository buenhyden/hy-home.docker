# 04-data Specifications

> 데이터 저장 및 관리 서비스 기술 사양

## Overview

`docs/03.specs/04-data`는 관계형 DB, NoSQL, 캐시, 오브젝트 스토리지 등 데이터 계층 서비스의 기술 사양을 포함합니다.

## Audience

이 README의 주요 독자:

- Developers
- System Architects
- QA Engineers
- AI Agents

## Scope

### In Scope

- 데이터 서비스 인터페이스, 스키마, 복제 및 고가용성 사양
- 시크릿 주입 패턴 및 볼륨 마운트

### Out of Scope

- 운영 절차 (`docs/05.operations/guides/04-data/` 담당)
- 분석 파이프라인 사양 (`04-data-analytics/` 담당)

## Structure

```text
04-data/
├── spec.md      # Data services technical specification
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
- [infra/04-data/README.md](../../../infra/04-data/README.md)
- [docs/05.operations/guides/04-data/](../../05.operations/guides/04-data/)
