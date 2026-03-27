<!-- Target: docs/08.operations/04-data/operational/supabase.md -->

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
