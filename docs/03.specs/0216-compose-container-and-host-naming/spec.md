---
title: "Compose Container and Host Naming"
version: "0.2.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0216"
parent_ids:
- "REQ-0027"
- "AD-0031"
created: "2026-10-08"
---

# Compose Container and Host Naming

## Overview

Every service in an `infra/` Compose file declares `container_name` equal to
the service key unless it has a registered naming exception. `hostname` also
equals the service key, except for node-exporter's host-network configuration
introduced by SPEC-0225. Before this package, 111 of 121
root services had no `hostname`, eight had no `container_name`, and 21 used a
different container name (`infra-*`, `supabase-*` and one exporter).

## Scope

Included: the naming rule in POL-0001, an exception registry entry type, the
Compose edits across `infra/`, a regression test, renamed container references
in operations documents and READMEs, and recreation of the renamed or newly
named containers on HOME.

Excluded: standalone `labs/*.yml` files, service key renames, and changes to
service-to-service addresses, which already use service keys.

## Contracts

1. Each `infra/` Compose service sets `hostname` to its service key, except
   node-exporter while it uses `network_mode: host` for SPEC-0225 host metrics.
   That configuration keeps `container_name: node-exporter` and no `hostname`.
2. Each sets `container_name` to its service key, unless
   `infra/common-optimizations.exceptions.json` `naming_exceptions` lists the
   service with its `container_name` and a `reason`.
3. Supabase naming exceptions now belong to
   `labs/supabase/naming-exceptions.json` for `labs/supabase.yml`, outside this
   package's `infra/` scope. They are not duplicated in the root naming
   exception registry; the original implementation remains in the Task history.
4. Documents and commands name the container by its current name.

## Acceptance Criteria

1. The regression test fails for every service missing either key before the
   change and passes after it, and it rejects an exception without a reason.
2. No active document or README cites a retired container name.
3. The root Compose model renders, and the full Compose validation passes.
4. HOME runs the renamed containers under their new names, with their
   volumes, health and scrape targets intact, or the Task records why not.

## Failure Conditions

A missing service-key hostname fails outside contract 1's node-exporter
configuration. A differing or missing container name fails unless it has an
exact, reasoned naming exception. Retired container references or a
HOME recreation that loses volumes, health or scrape targets leave the
naming change unverified; service keys and inter-service addresses are not
renamed.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-compose-container-and-host-naming.md)
- [Template exceptions policy](../../05.operations/policies/01-common/0001-common-optimizations-template-exceptions.md)
