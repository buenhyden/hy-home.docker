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

`scripts/lib/` contains domain libraries reused by repository entrypoints.
Their execution authority and evidence remain in the owning Task.

## Scope

- [`ops/`](ops/README.md) contains bounded operations helpers.
- The script manifest owns the current classification and execution consumers.

## Related Documents

- [Scripts](../README.md)
- [Library tests](../../tests/lib/README.md)
