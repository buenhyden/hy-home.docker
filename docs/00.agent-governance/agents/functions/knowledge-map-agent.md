---
layer: agentic
artifact_type: agent-function
function_id: knowledge-map-agent
scope: docs
status: active
---

# knowledge-map-agent

## Preconditions

The tracked source boundary, canonical routing rules, generator owner, and excluded confidential/generated surfaces must be known.

## Inputs

- Tracked source boundary and canonical stage routing.
- Existing indexes, generated outputs, ownership metadata, and freshness commands.

## Procedure

1. Inventory safe tracked paths and map each artifact to its canonical owner and lifecycle role.
2. Update curated navigation or deterministic generators without copying policy or stale document bodies into the map.
3. Regenerate indexes and coverage, verify freshness, and corroborate advisory graph output against tracked source.

## Outputs

- A knowledge map or generated index that points to canonical sources and records freshness evidence.

## Gates

- Generated outputs match their canonical generators.
- The map introduces no parallel authority or confidential payload exposure.

## Failure Handling

Exclude unsafe or unverifiable paths, record the omission, and stop if provenance or source ownership cannot be established.

## Related Documents

- [Documentation writer](../agents/doc-writer.md)
- [Documentation scope](../../scopes/docs.md)
- [Environment constraints](../../rules/environment-constraints.md)
