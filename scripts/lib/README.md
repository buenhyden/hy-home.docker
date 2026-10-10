---
title: "Shared Script Libraries"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
created: "2026-10-10"
---

# Shared Script Libraries

## Overview

`scripts/lib/`는 entrypoint가 재사용하는 domain library를 소유합니다.
진행 상태와 실행 권한은 owning Task에 기록하며 이 README는 탐색만 제공합니다.

## Scope

- `ops/`는 운영 계약과 안전한 helper를 소유합니다.
- 기타 library의 현재 분류와 실행 소비자는 [script manifest](../manifest.yaml)가 소유합니다.

## Related Documents

- [Scripts](../README.md)
- [Operations libraries](ops/README.md)
- [Library tests](../../tests/lib/README.md)
