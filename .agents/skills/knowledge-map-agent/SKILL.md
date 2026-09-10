---
name: "knowledge-map-agent"
description: "Use when tracked documentation navigation needs canonical ownership, safe source coverage, and corroboration of advisory graph output against tracked source."
metadata:
  title: "knowledge-map-agent"
  version: "2.0.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-10"
  function_id: "knowledge-map-agent"
  scope: "docs"
  owner_agent: "doc-writer"
---

# knowledge-map-agent

## Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

The tracked source boundary, canonical routing rules, and excluded
confidential/generated surfaces must be known.

No tracked generator writes a knowledge map any more. The LLM Wiki generator and
its three generated indexes were retired on 2026-09-10 with the rest of the
Stage 90 data category, so a request to "regenerate the index" has no subject.
Navigation that survives is curated by hand, and `.agents/knowledge/` owns the
routing from a repository surface to its canonical owner.

## Inputs

- Tracked source boundary and canonical stage routing.
- Existing curated indexes and ownership metadata.
- Advisory graph output under `graphify-out/`, which is a hint rather than an
  authority and is only usable after corroboration against tracked source.

## Procedure

1. Inventory safe tracked paths and map each artifact to its canonical owner and lifecycle role.
2. Update curated navigation without copying policy or stale document bodies into the map.
3. Corroborate any advisory graph claim against tracked source before recording
   it, and say which claims were corroborated and which were dropped.

## Outputs

- A curated knowledge map that points to canonical sources and records which
  claims were corroborated against tracked source.

## Gates

- The map introduces no parallel authority or confidential payload exposure.
- An advisory graph claim is either corroborated against tracked source or left out.

## Failure Handling

Exclude unsafe or unverifiable paths, record the omission, and stop if provenance or source ownership cannot be established.

## Related Documents

- [Documentation writer](../../roles/doc-writer.md)
- [Documentation scope](../../governance/documentation-protocol.md)
- [Environment constraints](../../governance/environment-constraints.md)
