---
layer: agentic
---

# Template Support

> non-copyable rules, contracts, and rationale for the template system

## Overview

`docs/99.templates/support` contains the rules for choosing, maintaining, and
validating templates. These files are not copied into target documents. They
define the local contract that template artifacts and target documents must
follow.

## Audience

이 README의 주요 독자:

- Documentation Writers
- AI Agents
- Repository Maintainers
- QA Engineers

## Scope

### In Scope

- Template source contract
- Template governance and protected-surface rules
- Frontmatter key and value policy
- Typed document metadata profiles, target-safe placeholders, and changed/new enforcement rules
- Lifecycle status vocabulary
- Template selection rules
- SDLC and common document-family authoring contracts
- README profile selection and local-content boundaries
- Archive-centered disposition and destructive-change rules
- Source-backed rationale for local documentation choices

### Out of Scope

- Copyable template bodies
- Active stage document content
- Runtime configuration or secret values

## Support Catalog

| Document | Role |
| --- | --- |
| [template-contract.md](./template-contract.md) | Defines copyable template shape and source requirements. |
| [template-governance.md](./template-governance.md) | Defines template change workflow, protected surfaces, archive/remove dispositions, and commit boundaries. |
| [frontmatter-contract.md](./frontmatter-contract.md) | Interprets frontmatter, source metadata, and deterministic serialization without copying registry tables. |
| [document-metadata-profiles.yaml](./document-metadata-profiles.yaml) | Sole machine owner for profiles, README profiles, 23 template roles, matchers, headings, lifecycle, parents, and exceptions. |
| [sdlc-document-contract.md](./sdlc-document-contract.md) | Owns human roles and iterative feedback from PRD through Release. |
| [common-document-contract.md](./common-document-contract.md) | Explains Reference, Audit, Archive, governance, generated, template, repo-support, and native-surface roles. |
| [readme-profile-contract.md](./readme-profile-contract.md) | Explains README profile selection, heading envelopes, consumers, and local-content ownership. |
| [lifecycle-status.md](./lifecycle-status.md) | Defines lifecycle status values, transition rules, and archive status boundaries. |
| [template-selection.md](./template-selection.md) | Owns exact purpose, target-path, and canonical-source routing. |
| [external-source-rationale.md](./external-source-rationale.md) | Records external source rationale behind local template rules. |

## Structure

```text
support/
├── README.md
├── external-source-rationale.md
├── document-metadata-profiles.yaml
├── sdlc-document-contract.md
├── common-document-contract.md
├── readme-profile-contract.md
├── frontmatter-contract.md
├── lifecycle-status.md
├── template-contract.md
├── template-governance.md
└── template-selection.md
```

## How to Work in This Area

1. Update the canonical support owner when a document-family, README-profile,
   metadata, template, or governance rule changes.
2. Update copyable templates separately from support rules unless both must
   change together for the same contract.
3. Keep `docs/99.templates/README.md` as a routing document and place detailed
   rules here.
4. Record validation evidence in the relevant Stage 04 task when support rules
   change.
5. Keep the exhaustive metadata inventory advisory; enforce only the safely
   selected changed/new set and the explicitly approved migrated active chain.
6. Keep this README as catalog routing; do not copy registry arrays or support
   contract policy into it.

## Related Documents

- [template catalog](../README.md)
- [template artifacts](../templates/README.md)
- [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
