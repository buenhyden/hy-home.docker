<!-- Target: docs/07.guides/04-data/operational/supabase.md -->

# Supabase Platform Guide

> Comprehensive guide for self-hosting Supabase in `hy-home.docker`.

---

## Overview (KR)

이 문서는 `hy-home.docker` 환경에서 Supabase 플랫폼을 구성하고 운영하기 위한 가이드다. PostgreSQL 기반의 통합 백엔드 서비스(Auth, Realtime, Storage, Edge Functions)의 구조와 로컬 관리 방법을 설명한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Developer
- Operator
- AI Agents

## Purpose

- Understand the Supabase stack components and their interactions.
- Provide instructions for local setup and dashboard access.
- Define service boundaries and integration points.

## Prerequisites

- Docker and Docker Compose installed.
- Access to the `04-data/operational/supabase` directory.
- Properly configured `.env` file.

## Step-by-step Instructions

### 1. Initialization

1. Navigate to `infra/04-data/operational/supabase/`.
2. Copy `.env.example` to `.env` and fill in the required keys (especially `JWT_SECRET`).
3. Run `docker compose up -d`.

### 2. Accessing the Dashboard
- Open `http://localhost:3000` in your browser.
- The Studio UI allows managing the database schema, viewing logs, and configuring Auth.

### 3. Using the API
- The Kong Gateway is exposed at `http://localhost:8000`.
- All requests should include the `apikey` header (service role or anon key).

## Common Pitfalls

- **JWT Secret Mismatch**: Ensure `JWT_SECRET` is consistent across all services in `.env`.
- **Database Migrations**: Manual changes in Studio are not persisted in `volumes/db/` unless exported. Use `supabase-cli` for formal migrations.
- **Service Dependency**: Kong and Studio depend on the health of the PostgreSQL database.

## Related Documents

- **Infrastructure**: `[../../../infra/04-data/operational/supabase/README.md]`
- **Operation**: `[../../08.operations/04-data/operational/supabase.md]`
- **Runbook**: `[../../09.runbooks/04-data/operational/supabase.md]`
- **PostgreSQL Cluster**: `[./postgresql-cluster.md]`
