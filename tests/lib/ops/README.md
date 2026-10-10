---
title: "Operations Library Tests"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
created: "2026-10-10"
---

# Operations Library Tests

## Overview

`tests/lib/ops/`는 운영 helper의 순수 동작과 합성 입력을 검증합니다. 실제
비밀값, HOME 서비스와 업무 데이터는 시험 입력이 아닙니다.

## Scope

- `test_compose_core_readiness.py`는 Compose readiness helper를 검증합니다.
- `test_wiki_preparation.py`는 P09 준비 계약 helper의 허용·거절 경계를 검증합니다.

## Related Documents

- [Library tests](../README.md)
- [Operations libraries](../../../scripts/lib/ops/README.md)
