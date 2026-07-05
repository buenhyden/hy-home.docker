<!-- Target: docs/03.specs/097-home-docker-revalidation-deferred-follow-up/README.md -->

# home-docker-revalidation-deferred-follow-up Specifications

> Home Docker 재검증 및 deferred follow-up 계약

## Overview

`docs/03.specs/097-home-docker-revalidation-deferred-follow-up`는 2026-05-25 Home Docker workspace audit 이후 재검증과 deferred 항목 추적 계약을 보존합니다.

## Audience

이 README의 주요 독자:

- Documentation Writers
- Repository Maintainers
- AI Agents

## Status

이 사양은 completed audit baseline 이후 값·런타임·원격 변경 없이 재검증 evidence와 deferred boundary를 추적하는 계약입니다.

## Scope

### In Scope

- Home Docker workspace audit 재검증 계약
- metadata-only env/secret drift 기록 기준
- runtime, value-bearing, remote, deployment 작업의 deferred boundary
- Stage 04 plan/task evidence와의 추적성 링크

### Out of Scope

- 실제 `.env` 값 동기화
- secret value 또는 private credential 기록
- Docker runtime start/stop, deployment, port, permission 변경
- remote GitHub branch protection 또는 required-check 변경

## Structure

```text
home-docker-revalidation-deferred-follow-up/
├── spec.md      # Revalidation and deferred follow-up specification
└── README.md    # This file
```

## How to Work in This Area

1. 후속 작업 전 [spec.md](./spec.md)의 deferred boundary와 verification contract를 먼저 확인합니다.
2. 실행 순서와 작업 evidence는 `docs/04.execution/`의 plan/task 문서에 기록합니다.
3. `.env`와 secret registry는 값이 아니라 key, ID, metadata 수준으로만 비교합니다.
4. runtime, remote GitHub, deployment 변경은 별도 operator approval이 있는 작업으로 분리합니다.

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [Home Docker revalidation deferred follow-up plan](../../04.execution/plans/2026-05-25-home-docker-revalidation-deferred-follow-up.md)
- [Home Docker revalidation deferred follow-up task](../../04.execution/tasks/2026-05-25-home-docker-revalidation-deferred-follow-up.md)
- [Large-scale authored SSoT review task](../../04.execution/tasks/2026-05-25-large-scale-authored-ssot-review.md)
