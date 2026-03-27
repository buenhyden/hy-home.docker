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
  - Daily backups of the core PostgreSQL database.
  - Encryption at rest for sensitive volumes.
  - JWT expiry must be strictly enforced (default 1 hour).
- **Allowed**:
  - Local Studio access for schema design in development.
  - Horizontal scaling of the `rest` and `auth` containers.
- **Disallowed**:
  - Direct root access to the database via public network.
  - Disabling SSL for the Kong API gateway.

## Exceptions

- Emergency schema fixes during incidents require Lead Architect approval and a following ADR.

## Verification

- Monthly audit of JWT logs and failed login attempts.
- Weekly verification of backup consistency.

## Review Cadence

- Quarterly.

## Related Documents

- **ARD**: `[../../02.ard/04-data/operational-data-architecture.md]`
- **Runbook**: `[../../09.runbooks/04-data/operational/supabase.md]`
- **Guide**: `[../../07.guides/04-data/operational/supabase.md]`
