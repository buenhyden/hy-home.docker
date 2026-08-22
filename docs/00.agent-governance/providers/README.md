---
profile_id: governance-provider-index
layer: agentic
status: active
---

# Provider Adapters

## Overview

Provider adapters translate Stage 00 policy, roles, and skills into runtime
syntax. They do not own shared behavior.

## Scope

Only Claude and Codex are supported. `registry.yaml` is the machine authority
for provider capabilities, work-profile model selections, projection paths, and
hook differences.

## Structure

- `claude.md` — Claude-specific loading and runtime mechanics.
- `codex.md` — Codex-specific loading and runtime mechanics.
- `registry.yaml` — typed provider and projection facts.

## How to Work in This Area

Change provider-neutral behavior in Stage 00 policy, role, or skill sources.
Change provider facts in `registry.yaml`, update the matching adapter, then run
the provider renderer in write and check modes.

## Related Documents

- [Governance hub](../README.md)
- [Bootstrap policy](../policies/bootstrap.md)
- [Stage 99 registry](../../99.templates/registry.json)
