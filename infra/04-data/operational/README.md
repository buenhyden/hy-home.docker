---
title: "Operational Data Tier (04-data/operational)"
version: "1.0.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
created: "2026-03-27"
---

# Operational data

## Overview

This area documents the operational data packages used by repository services.

## Audience

It is intended for operators and maintainers of shared operational state.

## Scope

It covers the HOME management databases and the separate optional application
platform.

## Structure

### Packages and ownership

- [`mng-db`](mng-db/README.md) is HOME shared PostgreSQL and Valkey for current
  auth, workflow and tooling consumers.
- [`supabase`](supabase/README.md) is a separate OPTIONAL application platform.
It does not replace, extend or share directories with `mng-db`.

## How to Work in This Area

Operate each through its exact root profile. Never merge schemas, credentials,
queues or volumes because two packages expose similar database/cache protocols.
Promotion, consolidation or removal needs a named application, schema/data
migration, isolated recovery proof and rollback.

## Related Documents

Use the [documentation entry point](../../../docs/README.md) to locate Stage 05
subject `04-data/0028-management-database` and backup policy POL-0021.
