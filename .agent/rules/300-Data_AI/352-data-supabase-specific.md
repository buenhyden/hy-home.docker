---
trigger: always_on
glob: "**/*.{ts,tsx,js,jsx,sql}"
description: "Supabase: Postgres, Row-Level Security (RLS), and Real-time."
---
# Supabase Standards

## 1. PostgreSQL Conventions

- **Naming**: `snake_case` for tables and columns.
- **Indexes**: Index all columns used in joins and WHERE clauses.
- **Foreign Keys**: Always define FK constraints.

## 2. Row-Level Security (RLS)

- **Enable**: RLS must be enabled on all public tables.
- **Policies**: Create explicit read/write policies per role/user.
- **Default Deny**: `REVOKE ALL ON public.* FROM anon, authenticated;`.

## 3. Auth

- **Built-In**: Use Supabase Auth for user management.
- **Session**: Access user via `auth.uid()` in SQL policies.

## 4. Real-time

- **Subscriptions**: Use `supabase.channel()` for broadcast/presence.
- **Performance**: Limit channels to active features only.

## 5. Testing

- **Framework**: `pgTAP` for database unit tests.
