---
status: active
---

<!-- Target: docs/05.operations/policies/04-data/operational/supabase.md -->

# Supabase Operations Policy

> Operational policy and governance for the Supabase platform in `hy-home.docker`.

---

## Overview (KR)

이 문서는 Supabase 플랫폼의 운영 정책을 정의한다. 데이터 백업, 보안 통제, 리소스 확장 및 규정 준수 확인 방법을 규정한다.

## Policy Scope

- Persistence layer (PostgreSQL) management.
- Authentication and JWT security.
- Asset storage and websocket realtime policies.
- Edge function deployment and runtime limits.

## Applies To

- **Systems**: Supabase Stack (db, auth, rest, storage, kong, realtime, functions).
- **Agents**: AI Agents managing or interacting with Supabase APIs.
- **Environments**: Production and Staging.

## Controls

- **Required**:
Copyright (c) 2026. Licensed under the MIT License.

---

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/operational/supabase.md)
- [Recovery runbook](../../../runbooks/04-data/operational/supabase.md)
- [Operations template](../../../../99.templates/operation.template.md)
