---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/operational/supabase.md -->

# Supabase Usage Guide

## Usage

### Overview (KR)

이 문서는 `hy-home.docker` 환경에서 Supabase 플랫폼을 구성하고 운영하기 위한 가이드다. PostgreSQL 기반의 통합 백엔드 서비스(Auth, Realtime, Storage, Edge Functions)의 구조와 로컬 관리 방법을 설명한다.
>
> Comprehensive guide for self-hosting Supabase in `hy-home.docker`.

---

### Usage Type

`system-guide | how-to`

### Target Audience

- Developer
- Operator
- AI Agents

### Purpose

- Understand the Supabase stack components and their interactions.
- Provide instructions for local setup and dashboard access.
- Define service boundaries and integration points.

### Prerequisites

- Docker and Docker Compose installed.
- Access to the `04-data/operational/supabase` directory.
- Properly configured `.env` file.

Copyright (c) 2026. Licensed under the MIT License.

---

### Step-by-step Instructions

1. 관련 README와 기존 본문을 먼저 읽는다.
2. 실제 compose/config 경로와 문서 설명이 일치하는지 확인한다.
3. 변경이 필요하면 대응 템플릿과 상위 README 링크를 함께 갱신한다.
4. 관련 검증 스크립트 또는 문서 audit를 실행한다.

### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

## Common Checks

- Step-by-step Instructions 의 검증 단계를 따른다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../../runbooks/04-data/operational/supabase.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/operational/supabase.md)
- [Recovery runbook](../../../runbooks/04-data/operational/supabase.md)
