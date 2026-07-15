---
layer: agentic
---

# Template Contract

## Overview

This document defines the non-copyable contract for template source files under
`docs/99.templates/templates/`.

## Ownership Boundary

Copyable forms live under `docs/99.templates/templates/`. Exact roles,
profiles, matchers, headings, and tokens live in the registry. Human role,
selection, lifecycle, and change governance live in their named support
owners. Catalog READMEs only route readers. A template source must not copy
those rules into its body.

## Markdown Source Form

Each registered Markdown source contains only:

1. profile-compatible source frontmatter and registered placeholders;
2. exactly one H1;
3. the registered required and applicable conditional H2 sections;
4. explicit `{{token_name}}` replacement tokens; and
5. one `## Related Documents` section.

Markdown sources use the `*.template.md` suffix and source-draft status. Typed
forms declare the target `artifact_type`; README validates source draft only;
Memory and Progress use the governance source metadata defined by the
frontmatter contract; Archive uses source draft while its rendered target is
archived.

The Archive form contains the registry's required source metadata plus the
conditional replacement and preserved-evidence fields in canonical key order.
Its required body sections are Overview, Archive Metadata, Archive Ledger, and
Related Documents. Current Replacement and Preserved Evidence are conditional;
an instantiated target removes the inapplicable fields and sections instead of
inventing replacement or preservation evidence. Exact conditions remain in
the [archive and retention contract](./archive-retention-contract.md).

Sources must not contain Rules blocks, Target comments, path-selection policy,
numbering rules, language policy, lifecycle algorithms, migration guidance,
fixed-depth link examples, or executable-looking sample commands.

## Machine-readable Source Form

OpenAPI, GraphQL, and Protobuf sources stay in their native syntax and do not
receive Markdown frontmatter or headings. They use visibly unresolved
`__TOKEN_NAME__` tokens. Their parent Markdown Spec or API Spec owns
human-readable context and cross-links.

## Instantiated Target Contract

An instantiated target resolves exactly one role and replaces every registered
frontmatter, body, link, and machine token with evidence-backed content. It
must not retain source-only comments, template instructions, placeholder text,
valid-looking example credentials, hosts, or commands. The target selects an
honest lifecycle state and direct parents from its own evidence; source draft
metadata is never approval or review evidence.

Conditional headings are included only when the concern applies. An
intentional deviation from the matched form is recorded in the owning Stage 04
Task with approval and validation evidence.

## Related Documents

- [support README](./README.md)
- [template governance](./template-governance.md)
- [frontmatter contract](./frontmatter-contract.md)
- [template selection](./template-selection.md)
- [SDLC document contract](./sdlc-document-contract.md)
- [common document contract](./common-document-contract.md)
- [README profile contract](./readme-profile-contract.md)
- [archive and retention contract](./archive-retention-contract.md)
