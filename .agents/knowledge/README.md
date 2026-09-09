---
title: "Agent Knowledge"
version: "0.1.0"
type: "governance/knowledge-index"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-06"
created: "2026-09-06"
---

# Agent Knowledge

## Overview

`.agents/knowledge/` holds verified, living knowledge that routes a reader to a
canonical owner. It exists so an agent resolves surface ownership, repository
vocabulary, and verification coverage by reading a registered file instead of
inferring them each session.

Knowledge is not authority. A member states what is true and who owns the rule;
the rule itself stays with that owner.

## Scope

- Included: surface-to-authority routing, repository vocabulary, verification
  coverage maps, and domain knowledge that is verified and reused.
- Excluded: obligations and prohibitions, which belong to `governance/`;
  ordered procedures, which belong to `skills/`; detailed designs and
  specifications, which belong to Stage 02 and Stage 03; operator procedures,
  which belong to Stage 05; dated one-time observations, which belong to
  Stage 90; and execution state, which belongs to the current Spec Package Task.

A member that states an obligation is a defect. Route its content to
`governance/` and leave a link behind.

## Structure

```text
.agents/knowledge/
├── README.md
├── glossary.md
├── repository-map.md
└── verification-surface-map.md
```

Every member declares `observed_at` and `review_cycle` so staleness is
detectable rather than assumed, and carries a `Provenance` section naming the
tracked sources it was derived from.

## How to Work in This Area

1. Confirm no existing member already owns the content; extend it rather than
   adding a second owner.
2. Copy `docs/99.templates/templates/governance/knowledge.template.md` and keep
   its registered sections.
3. Derive every claim from a tracked source and name that source under
   `Provenance`, with the commit and date of observation.
4. State the conditions that make the member stale under `Refresh Triggers`.
5. Register the file in `canonical_sources` in the Provider Registry, then run
   the document metadata and agent governance contract checks.

### Curation Lifecycle

| Stage | Condition | Owner |
| --- | --- | --- |
| Create | An agent repeatedly reconstructs the same routing or vocabulary | `doc-writer` within an approved Task |
| Verify | Every claim traces to a tracked source at a named commit | the author, before review |
| Deduplicate | No existing governance, skill, stage document, or member already owns it | `rules-engineer` review |
| Promote | An obligation found here moves to `governance/`; a durable decision moves to an ADR | the owning stage |
| Retrieve | Entered from the bootstrap order or a role's related documents | any role |
| Re-review | A refresh trigger fires, or the declared review cycle elapses | `doc-writer` |
| Expire | The routed owner no longer exists or the claim no longer holds | `doc-writer` |
| Archive | The member is superseded or retired through the `living` lifecycle | [documentation protocol](../governance/documentation-protocol.md) |
| Delete | Never by age or count; only through the registered retirement route | [documentation protocol](../governance/documentation-protocol.md) |

Age and file count are not retention criteria. A member is retained while its
routing is correct and retired when its still-current meaning has moved to a
canonical owner.

## Related Documents

- [Agent governance index](../README.md)
- [Prompt index](../prompts/README.md)
- [Documentation protocol](../governance/documentation-protocol.md)
- Canonical knowledge and prompt surfaces decision (`docs/02.architecture/decisions/0034-canonical-knowledge-and-prompt-surfaces.md`)
- [Documentation index](../../docs/README.md)
