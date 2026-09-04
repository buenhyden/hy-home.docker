---
title: "Provider Adapters"
version: "1.0.0"
type: "governance/provider-index"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
---

# Provider Adapters

## Overview

Provider adapters translate Stage 00 policy, roles, and skills into runtime
syntax. They do not own shared behavior.

## Scope

Only Claude and Codex are supported. `registry.yaml` is the machine authority
for provider identities, work-profile model selections, permission
translations, projection paths, semantic events, and hook commands. It does
not own workflow, approval, retry, evidence, stop, or document-profile rules.

## Structure

- `claude.md` — Claude-specific loading and runtime mechanics.
- `codex.md` — Codex-specific loading and runtime mechanics.
- `registry.yaml` — typed provider and projection facts.

## How to Work in This Area

Change provider-neutral behavior in Stage 00 policy, role, or skill sources.
Change provider facts in `registry.yaml` and update the matching adapter. After
an approved canonical change, run the provider renderer once with `--write`
and immediately with `--check`. Ordinary validation and CI use `--check` only.
If `--write` reports quarantined stale projections, stop: the command has
removed them from active provider paths but has intentionally retained the
revalidated blobs under `.provider-surface-quarantine/`. Verify the reported
paths against the approved retirement and Git recovery boundary, remove only
those exact quarantine files in the explicit cleanup step, and rerun `--write`
then `--check`. Pending cleanup is a failing `--check` state and must not be
reported as convergence.

## Related Documents

- [Governance hub](../README.md)
- [Bootstrap policy](../policies/bootstrap.md)
- [Provider capability matrix](../policies/provider-capability-matrix.md)
