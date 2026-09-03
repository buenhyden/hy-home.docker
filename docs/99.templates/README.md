---
title: Stage 99 Document Contracts and Templates
version: 1.0.0
type: common/readme
status: active
owner: "@buenhyden"
---

# Stage 99 Document Contracts and Templates

## Overview

Stage 99 is the sole authority for document paths, profiles, identifiers,
sections, lifecycle states and transitions, traceability shapes, and copyable
templates. The machine authority is [`registry.json`](./registry.json); the two
schemas under `contracts/` validate the registry and document
frontmatter. Human and AI-agent policy remains in Stage 00, and executable gate
behavior remains in registered `scripts/` modules.

Predecessor contracts are recoverable through Git history; they are not current
authoring or validation inputs.

## Scope

Stage 99 owns:

- the Requirement Package and Architecture Description profiles;
- the Guide, Policy, Runbook, Incident, and Postmortem profiles;
- the Research, Audit, Data, and Tombstone profiles plus a transition-only
  Migration profile for the temporary records being retired by SPEC-0158;
- canonical path and stable-ID patterns;
- profile-specific frontmatter and section contracts;
- lifecycle states and allowed forward transitions;
- monotonic identity allocation state, including Requirement child spaces;
- template role-to-profile registration;
- reusable Markdown and executable interface-contract templates;
- exact Stage 03 package-index and contract-payload filenames and media types;
- the four-digit Operations subject route shape.

Stage 99 does not own agent behavior, product truth, architecture decisions,
implementation evidence, operating policy, or reference findings.

## Structure

```text
docs/99.templates/
├── README.md
├── registry.json
├── contracts/
│   ├── frontmatter.schema.json
│   └── document-profile.schema.json
└── templates/
    ├── governance/
    ├── runtime/
    ├── requirements/
    ├── architecture/
    ├── specs/
    │   └── contracts/
    ├── operations/
    ├── references/
    ├── archive/
    └── common/
```

## How to Work in This Area

1. Select a registered profile and template role.
2. Copy the registered source without changing its `profile_id` contract.
3. Allocate an ID above the persisted high-water mark.
4. Replace placeholders and add full traceability IDs.
5. Run the document-contract validator and the owning stage gate.
6. Change Registry, schemas, templates, consumers, and tests in one reviewed
   logical unit when the contract itself changes.

### Authority Model

| Surface | Authority | Purpose |
| :--- | :--- | :--- |
| [`registry.json`](./registry.json) | machine | profiles, paths, identities, lifecycle, traceability, template registration |
| [`contracts/document-profile.schema.json`](./contracts/document-profile.schema.json) | machine | registry shape |
| [`contracts/frontmatter.schema.json`](./contracts/frontmatter.schema.json) | machine | typed frontmatter value shape |
| [`templates/`](./templates/) | copy source | profile-referenced authoring forms |

Consumers must load the Registry through
`scripts.lib.document_governance.registry`. They must not reinterpret README
prose or template bodies as machine policy.

Every profile declares one `frontmatter_policy`. `required` means the canonical
Markdown artifact must carry a `type` equal to its Registry-classified profile
type; this also applies to package, domain, subject, stage, governance,
generated, and repository-support Markdown without a dedicated copy template.
`absent` is reserved for executable machine contracts that do not use Markdown
frontmatter. `unmanaged` is reserved for the unsupported fallback and never
defines a canonical target artifact.

### Identity and Lifecycle Rules

#### Registered Identity Shapes

`registry.json` states the identity shape per profile in `artifact_id_pattern`,
and the owning container in `identity_relation`. This section states the rules
those fields express, not the fields themselves.

#### Required Frontmatter Envelope

A profile's `required_frontmatter` and `optional_frontmatter` state which keys a
document declares; `common.frontmatter_order` states the order;
[`contracts/frontmatter.schema.json`](./contracts/frontmatter.schema.json)
states each value's shape. The reasons behind that envelope are:

- `type` carries the `family/kind` document role, so a reader learns a
  document's family without resolving its path.
- `title` never repeats the artifact identity, because the identity is already
  a field.
- `layer` names the owning stage without its numeric prefix, and is omitted
  wherever the canonical path already states the authority.
- `owner` is sourced from `.github/CODEOWNERS`, so accountability has one home.
- `version` starts at `1.0.0`, so a first revision is distinguishable from an
  unset value.
- A profile without an identity declares no `artifact_id`, and no domain alias
  duplicates one that exists.
- A provider-owned runtime projection is exempt from the envelope entirely,
  because its shape belongs to the runtime that reads it.

- Standalone package paths use four numeric digits and omit semantic prefixes.
- A member identity is its container's identity plus that container's own
  internal sequence, so the same member number may recur under two containers.
- Stage 90 package members are named `m####-<slug>.md`;
  `scripts/lib/document_governance/references.py` owns that rule.
- Tombstones use `identity_relation: inherited` and reuse the retired
  document's identity, so the `tombstone` space no longer issues numbers;
  `scripts/lib/document_governance/archive.py` derives the exact value.
- Incident numbers restart inside each year partition, so the year belongs to
  the identity and not only to the path.
- Stable package IDs retain their registered prefix and case.
- Requirement children use full owner-qualified IDs:
  `REQ-####-FR-####`, `REQ-####-NFR-####`, and `REQ-####-IF-####`.
- FR, NFR, and IF counters are package-owned. Registry allocation keys include
  the full owner (for example `REQ-0001.FR`), so the same child number may be
  issued independently in two Requirement Packages.
- Issued numbers are never reused. `high_water` never decreases and
  `next_number` is always greater than `high_water`.
- Operations subjects and role artifacts have independent stable IDs. The
  Registry validates the four-digit subject route and each role ID shape but
  never equates their numbers. The current catalog directory containment owns
  role-to-subject membership.
- Incident year directories are the only date-path exception.
- A lifecycle transition is valid only when registered for the profile's
  lifecycle. Terminal states have no outgoing transition.

Full Git-history allocation validation belongs to the full document-contract
profile. Changed validation uses the persisted Registry allocation state.

### Template Rules

- Copy the source registered by `template_id`/template role.
- Markdown template frontmatter declares the profile's `type` and contains no
  concrete target path.
- Placeholders are literal: `<name>` for free text, `####` for a four-digit
  number, `YYYY-MM-DD` for a date, and `"#.#.#"` for a semantic version.
  Machine contract templates use `__UPPER_SNAKE__` tokens instead.
- Replace every placeholder before promotion to a target document.
- Executable OpenAPI, GraphQL, and Proto contracts belong to the owning Stage 03
  Spec package. Their deterministic filenames and media types are Registry
  profiles; Stage 01 retains implementation-independent interface needs.
- `DESIGN.md` remains the root UI/design-system authority and is not a Stage 03
  design artifact.


## Related Documents

- [Template catalog](./templates/README.md)
- [Workspace governance authority ADR](../02.architecture/decisions/0029-workspace-governance-authority.md)
