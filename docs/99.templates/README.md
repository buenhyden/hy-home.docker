---
profile_id: readme
layer: agentic
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

## Authority Model

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
Markdown artifact must carry a `profile_id` equal to its Registry-classified
profile; this also applies to package, domain, subject, stage, governance,
generated, and repository-support Markdown without a dedicated copy template.
`absent` is reserved for executable machine contracts that do not use Markdown
frontmatter. `unmanaged` is reserved for the unsupported fallback and never
defines a canonical target artifact.

## Identity and Lifecycle Rules

- Standalone package paths use four numeric digits and omit semantic prefixes.
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

## Template Rules

- Copy the source registered by `template_id`/template role.
- Markdown template frontmatter declares `profile_id` and contains no concrete
  target path.
- Replace every placeholder before promotion to a target document.
- Executable OpenAPI, GraphQL, and Proto contracts belong to the owning Stage 03
  Spec package. Their deterministic filenames and media types are Registry
  profiles; Stage 01 retains implementation-independent interface needs.
- `DESIGN.md` remains the root UI/design-system authority and is not a Stage 03
  design artifact.

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
    ├── requirements/
    ├── architecture/
    ├── specs/
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

## Related Documents

- [Template catalog](./templates/README.md)
- [Workspace governance authority ADR](../02.architecture/decisions/0029-workspace-governance-authority.md)
