---
profile_id: adr
status: active
artifact_id: ADR-0029
artifact_type: adr
parent_ids:
  - AD-0027
created: 2026-08-20
updated: 2026-08-22
supersedes:
  - ADR-0027
superseded_by: null
---

# ADR-0029: Workspace Governance Authority

## Context

The repository currently distributes document-shape rules across Stage 00,
Stage 99 support files, templates, validators, generated provider surfaces, and
aggregate gates. That distribution permits a validator, template, provider
adapter, or historical reference to conflict with the current SDLC taxonomy.
Parallel handoff files and unsupported provider experiments also kept obsolete
policy surfaces active after their purpose had ended.

The successor must make authority resolvable before the corpus moves, retain
recoverable stable identities, support Claude and Codex without provider-owned
policy, and expose comprehensible validation entrypoints without replacing
focused validators with a new monolith.

## Options Considered

### Retain the distributed control plane

This would reduce immediate file movement, but it would preserve conflicting
machine authorities and make the intended document contract dependent on which
validator or provider surface is read first.

### Make Stage 00 the authority for both policy and document mechanics

This would centralize rules, but it would mix human and AI-agent governance with
machine document profiles, schemas, lifecycle transitions, and templates. It
would also keep validators dependent on prose interpretation.

### Make generated provider surfaces authoritative

This would place instructions close to their runtimes, but Claude- and
Codex-specific formats would become competing policy sources. Regeneration
could silently change repository governance.

### Separate normative governance from typed document authority

Stage 00 owns policy, roles, provider differences, reusable skills, and the SDLC
flow. Stage 99 owns paths, profiles, identifiers, sections, lifecycle,
templates, and exceptions through one registry and its schemas. Scripts execute
those authorities, while provider directories remain generated or native
adapters. This option gives each concern one owner and is independently
testable.

## Decision

Adopt the separated authority model.

- Stage 00 is the sole normative authority for policies, roles, provider
  differences, reusable skills, handoff, and the Requirements -> Architecture
  -> Specification -> Implementation -> Operations flow.
- Stage 99 `registry.json` and its two schemas are the sole machine authority
  for document paths, profiles, stable identity spaces, required sections,
  lifecycle transitions, templates, traceability, and registered exceptions.
- Claude and Codex are the only supported providers. Root shims and provider
  runtime files adapt Stage 00 without defining policy. Unsupported provider
  experiments are historical evidence only and have no active surface.
- `.agents/skills/` is a generated compatibility projection of canonical Stage
  00 skills and cannot become a source authority.
- Migration 0003 is the review boundary for structural source dispositions.
  Git history remains the default full-content archive.
- Validation has exactly six public responsibility suites:
  `document-contract`, `document-graph`, `document-lifecycle`, `operations`,
  `agent-governance`, and `repository-integrity`. Each suite composes focused
  validators and contains no validation logic of its own.
- Root `DESIGN.md` remains the UI and design-system authority only.

This decision supersedes ADR-0027 for the two-provider target. ADR-0027 remains
in the Stage 02 decision log with the reciprocal supersession relationship
under the canonical identity contract.

## Consequences

### Positive

- Authority conflicts can be resolved by concern instead of by file precedence
  guesswork.
- Providers can evolve their native mechanics without creating new policy.
- Document moves fail closed against one registry and a reviewed migration
  selection.
- Public gates become navigable while focused validators retain single
  responsibilities.
- Retired bodies can be removed without losing recovery through Git and minimal
  Stage 98 evidence.

### Trade-offs

- Stage 99 must be installed before the corpus can adopt prefixless target
  paths and uppercase IDs.
- Generated projections require freshness validation.
- The migration ledger must distinguish structural dispositions from generated
  creations and multi-step lifecycle transitions; an ambiguous ledger cannot
  be approved or executed.
- The initial transition requires coordinated link, metadata, provider, and
  gate rewrites across several logical commits.

## Traceability

Confirmation requires all of the following after implementation:

1. Stage 99 registry/schema tests prove one machine authority and monotonic ID
   allocation.
2. Stage 00 contract tests prove the exact two-provider simplified taxonomy and
   generated projection parity.
3. Migration validation proves deterministic, collision-free, recoverable
   source dispositions before corpus mutation.
4. Each documentation stage passes its focused contract and link tests.
5. The six public suites select every atomic validator exactly once in their
   declared profile.
6. The full profile, metadata, lifecycle, link, Operations, agent-governance,
   and script-manifest gates exit zero before closure.

No runtime, deployment, remote, or secret state is asserted by this ADR.

## Follow-up Decisions

- Stage 99 defines the typed representation for create-only outputs and any
  intermediate migration state before those records can enter Migration 0003.
- Stage 02 retains the reciprocal ADR-0029/ADR-0027 supersession relationship
  under the canonical uppercase identity contract.
- Any change to the six public suite responsibilities requires a new ADR rather
  than an unreviewed manifest edit.

## Decision Drivers

The decision context above records the applicable drivers and evidence.

## Related Documents

- [Workspace Governance and SDLC Simplification Spec](../../03.specs/0153-workspace-governance-simplification/spec.md)
- [Workspace Governance and SDLC Simplification Plan](../../03.specs/0153-workspace-governance-simplification/plan.md)
- [Agent Governance Canonical Adapter Architecture Description](../descriptions/0027-agent-governance-canonical-adapter.md)
- [ADR-0027: Stage 00 Canonical Adapter Model](0027-stage-00-canonical-adapter-model.md)
