# 04-data Specifications

> 데이터 저장 및 관리 서비스 기술 사양

## Overview

`docs/03.specs/04-data`는 관계형 DB, NoSQL, 캐시, 오브젝트 스토리지 등 데이터 계층 서비스의 기술 사양을 포함합니다.

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

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [infra/04-data/README.md](../../../infra/04-data/README.md)
- [docs/05.operations/guides/04-data/](../../05.operations/guides/04-data/)
