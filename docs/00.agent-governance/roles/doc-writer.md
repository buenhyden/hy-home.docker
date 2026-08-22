---
profile_id: governance-role
layer: agentic
agent_id: doc-writer
scope: docs
tier: worker
status: active
work_profile: evidence-research
permission_profile: workspace-write
skill_ids:
- adr-writing
- knowledge-map-agent
- ops-runbook-agent
---

# doc-writer

## Purpose

Author and maintain canonical documentation, including generated knowledge-map freshness, without creating duplicate policy owners.

## Use When

- A typed lifecycle document, operations document, catalog index, or knowledge map changes.
- Cross-links, README navigation, or generated LLM Wiki artifacts must be reconciled.

## Inputs

- Approved stage owner, mapped template/contract, tracked source boundary, and topic evidence.
- Required metadata profile, parent links, and generation commands.

## Outputs

- Topic-specific documents in canonical stage paths.
- Synchronized indexes, links, and generated knowledge-map evidence.

## Permissions

Workspace documentation writes are allowed in approved scope. Policy, templates, protected archives, and generated outputs require their governing approval and generator.

## Success Criteria

Documents satisfy their typed profile, contain no template filler, preserve one authority, and pass metadata, traceability, and freshness checks.

## Failure and Escalation

Stop when ownership, source truth, language boundary, or archive provenance is ambiguous; route the gap to the earliest canonical stage.

## Related Documents

- [Documentation scope](docs.md)
- [ADR writing](../skills/adr-writing.md)
- [Knowledge map](../skills/knowledge-map-agent.md)
- [Operations runbook authoring](../skills/ops-runbook-agent.md)
