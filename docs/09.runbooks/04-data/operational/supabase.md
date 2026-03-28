<!-- Target: docs/09.runbooks/04-data/operational/supabase.md -->

# Supabase Platform Runbook

: Supabase Stack

> Operational procedures for common Supabase maintenance and recovery tasks.

---

## Overview (KR)

이 런북은 Supabase 플랫폼 운영 중 발생하는 일반적인 작업(재해 복구, 비밀번호 초기화, 로그 분석 등)에 대한 실행 절차를 정의한다.

## Purpose

- Provide step-by-step recovery procedures for database failure.
- Define manual management tasks for Auth and Storage.
- Standardize log troubleshooting across the stack.

## Canonical References

- `[../../02.ard/04-data/operational-data-architecture.md]`
- `[../../../infra/04-data/operational/supabase/docker-compose.yml]`

## When to Use

- Database container fails to start due to corruption.
- JWT secret rotation is required.
- Storage volume reaches capacity.

## Procedure or Checklist

### Database Recovery

1. Stop the stack: `docker compose down`.
2. Locate the last healthy backup in `${DEFAULT_DATA_DIR}/backups/supabase/`.
3. Restore the SQL dump to the database volume.
4. Restart the stack: `docker compose up -d`.

### Password Reset (Initial)

1. Access Studio at `http://localhost:3000`.
2. Navigate to Authentication -> Users.
Copyright (c) 2026. Licensed under the MIT License.
