---
layer: agentic
---

# README Profile Contract

## Overview

README files are routing and local-context surfaces. This contract explains how
authors select and use a README profile without turning a catalog README into a
shared policy owner. Exact path globs, heading sets, frontmatter consumers,
allowed keys, and canonical shared-rule owners belong only to
[`document-metadata-profiles.yaml`](./document-metadata-profiles.yaml).

## Profile Selection

1. Classify the tracked README by its canonical path, not by whichever body or
   frontmatter it currently resembles.
2. Require exactly one registry profile match. Zero matches and overlapping
   matches are classification errors, not permission to choose the closest
   profile.
3. Use the matched profile's heading envelope, local-content role,
   frontmatter disposition, declared consumer, and shared-rule owner.
4. If the path is new or its role is changing, update the machine registry and
   validator through approved contract work before authoring the README.

The registry declares 17 README profiles covering repository and stage
entrypoints, governance and provider catalogs, infrastructure and project
levels, script/test/secret/example catalogs, archive and template catalogs,
and the two `_workspace` support contracts. This document explains their
shared behavior without copying the registry's path arrays or heading lists.

## Heading Envelope

- Required headings create the minimum navigation and usage envelope for the
  selected profile.
- Optional headings are available only when the README has meaningful local
  content for them.
- Forbidden headings prevent the README from claiming ownership that belongs
  elsewhere or exposing prohibited content.
- Do not copy the heading envelope from another README. Similar-looking paths
  may have different audiences, consumers, and safety boundaries.

## Frontmatter and Consumers

Frontmatter is absent by default. A README may carry metadata only when its
matched profile permits it and names a real consumer. The author must be able
to identify that consumer and the allowed purpose of each key. Do not add
metadata for consistency, search appearance, lifecycle resemblance, or future
possibility.

README files do not inherit leaf-document identity, parent, freshness, or
lifecycle fields. Template-source metadata is removed when the README template
is copied unless the selected profile independently permits a consumed field.
Repo-support README files remain frontmatter-free under their explicit profile.

## Local Content and Shared Rules

A README owns only navigation, local inventory, local setup or workflow
context, and other content unique to its matched profile. It may summarize a
shared rule only enough to route the reader, then must link to the registry,
Stage 00 governance, Stage 99 support contract, operations owner, or other
canonical source.

Do not use a README to publish lifecycle transitions, full metadata key lists,
validator algorithms, template governance, security policy, or provider-neutral
execution rules. A `Canonical Shared Rules` section or equivalent duplicate
policy block is a contract violation even when the duplicated text is accurate.

Infrastructure profiles distinguish a `Folder index README` from a
`Service leaf README`. Service-local content may include `Secret refs` and
`Troubleshooting` when the matched registry profile permits those headings.
Script inventory and the `scripts/validation/` boundary, including the rule
against root-level `scripts/*.sh` duplicates, remain owned by
[`scripts/README.md`](../../../scripts/README.md).

## Authoring and Review Checklist

- The path matches exactly one declared profile.
- Required headings exist; unsupported and duplicate-purpose headings do not.
- Every frontmatter key has both profile permission and a declared consumer.
- The body contains unique local context and links shared rules to their owner.
- Secret-related catalogs expose identifiers, paths, and redacted workflow only.
- Changes to title, role, status summary, or inventory are reflected in the
  parent catalog when required.
- Validation evidence and any approved deviation are recorded in Stage 04.

## Related Documents

- [document metadata profiles](./document-metadata-profiles.yaml)
- [common document contract](./common-document-contract.md)
- [SDLC document contract](./sdlc-document-contract.md)
- [frontmatter contract](./frontmatter-contract.md)
- [template governance](./template-governance.md)
- [README template](../templates/common/readme.template.md)
